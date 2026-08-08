"""
sidequestz/permutation_test.py
------------------------------
Side-quest item 5: placebo / permutation control for the attenuation mechanism.

Rationale: every result in Section 4.3 shows that attenuation behaves as
designed, but none of them establish that the behaviour depends on a review's
actual off-topic content. A mechanism that adjusts ratings by an arbitrary
review-specific amount would also produce structured-looking correlations. This
is the control condition that separates the two.

Method: permute D_misc across reviews, breaking the correspondence between a
review's measured off-topic density and the attenuation it receives, while
leaving the marginal distribution of D_misc and every emotion feature intact.
Re-run attenuation on the permuted data and recompute:

  - expert paired-comparison accuracy (Section 4.4)
  - the delta-vs-D_misc modulator correlations (Section 4.3.3), measured
    against TRUE D_misc, since that is the relationship the paper claims

If the real framework is picking up genuine signal, permuted accuracy should
collapse toward chance (0.5) and the modulator correlations toward zero. The
reported p-value is the proportion of permutations reaching the observed value.

Note D_misc is permuted in the feature matrix as well as in the down-weighting
term, because it is both a model input and the driver of zeta. Permuting only
one would leave a back-channel through which true density still influences the
adjustment.

Usage:
    python sidequestz/permutation_test.py [--n-permutations 100] [--seed 42]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor
from scipy.stats import pearsonr, spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from constants import (  # noqa: E402
    CATBOOST_FINAL_MODEL,
    EXPERT_LABELS_PATH,
    FINAL_EMOTIONS,
    MISC_D_COL,
    S_VALUE,
)
from src.attenuation import attenuate  # noqa: E402
from src.splits import heldout_mask, professor_split  # noqa: E402
from src.validation import load_and_merge, score_predictions  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent / "output"


# ==============================================================================
# MEASUREMENTS
# ==============================================================================

def expert_accuracy(attuned: pd.DataFrame, tag: str) -> float:
    """Overall expert paired-comparison accuracy for one set of deltas."""
    tmp = OUT_DIR / f".tmp_perm_{tag}.csv"
    attuned.to_csv(tmp, index=False)
    try:
        # load_and_merge prints per-call warnings about dropped pairs; they are
        # identical every iteration, so silence them after the first.
        expert = score_predictions(load_and_merge(attuned_path=tmp))
    finally:
        tmp.unlink(missing_ok=True)
    return expert["correct"].sum() / len(expert)


def modulator_corrs(delta: np.ndarray, true_misc_d: np.ndarray) -> dict[str, float]:
    """Delta-vs-D_misc correlations, measured against the TRUE densities."""
    out = {}
    for name, mask in (("pos", delta > 0), ("neg", delta < 0)):
        if mask.sum() >= 2:
            out[f"{name}_pearson"] = pearsonr(delta[mask], true_misc_d[mask])[0]
            out[f"{name}_spearman"] = spearmanr(delta[mask], true_misc_d[mask])[0]
        else:
            out[f"{name}_pearson"] = out[f"{name}_spearman"] = np.nan
    return out


def run_once(
    model: CatBoostRegressor, df: pd.DataFrame, test_profs, tag: str
) -> tuple[float, dict[str, float]]:
    """Attenuate one frame and return (expert accuracy, held-out modulator corrs)."""
    attuned = attenuate(model, df, S_VALUE)
    attuned = attuned[attuned[MISC_D_COL] > 0].reset_index(drop=True)

    acc = expert_accuracy(attuned, tag) if Path(EXPERT_LABELS_PATH).exists() else float("nan")

    mask = heldout_mask(attuned, test_profs).to_numpy(dtype=bool)
    return acc, modulator_corrs(
        attuned.loc[mask, "weighting_delta"].to_numpy(),
        attuned.loc[mask, MISC_D_COL].to_numpy(),
    )


# ==============================================================================
# ENTRY POINT
# ==============================================================================

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-permutations", type=int, default=100)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading model and data...")
    model = CatBoostRegressor()
    model.load_model(str(CATBOOST_FINAL_MODEL), format="cbm")
    df = pd.read_csv(FINAL_EMOTIONS)
    _, test_profs = professor_split(df)

    print(f"  Using s = {S_VALUE}")

    print("\nObserved (true D_misc)...")
    obs_acc, obs_corrs = run_once(model, df, test_profs, "observed")
    print(f"  Expert accuracy      : {obs_acc:.4f}")
    print(f"  Delta+ vs D_misc (r) : {obs_corrs['pos_pearson']:.4f}")
    print(f"  Delta- vs D_misc (r) : {obs_corrs['neg_pearson']:.4f}")

    print(f"\nRunning {args.n_permutations} permutations of D_misc...")
    rng = np.random.default_rng(args.seed)
    rows = []
    for i in range(args.n_permutations):
        df_perm = df.copy()
        # Permuting the column permutes it everywhere it is consumed: as a model
        # feature and as the zeta driver inside _apply_down_weighting.
        df_perm[MISC_D_COL] = rng.permutation(df_perm[MISC_D_COL].to_numpy())

        acc, corrs = run_once(model, df_perm, test_profs, f"perm{i}")
        rows.append({"permutation": i, "expert_accuracy": acc, **corrs})

        if (i + 1) % 10 == 0:
            print(f"  {i + 1}/{args.n_permutations}")

    perm = pd.DataFrame(rows)
    perm.to_csv(OUT_DIR / "permutation_test.csv", index=False)

    print("\n" + "=" * 66)
    print("  PERMUTATION TEST RESULTS")
    print("=" * 66)

    def summarise(col: str, observed: float, direction: str) -> dict:
        vals = perm[col].dropna().to_numpy()
        # One-sided: how often does chance reach what we observed?
        if direction == "greater":
            hits = int((vals >= observed).sum())
        else:
            hits = int((vals <= observed).sum())
        # +1 correction: a permutation p-value can never be exactly zero.
        p = (hits + 1) / (len(vals) + 1)
        print(f"\n  {col}")
        print(f"    observed        : {observed:.4f}")
        print(f"    permuted mean   : {vals.mean():.4f}  (SD {vals.std(ddof=1):.4f})")
        print(f"    permuted range  : [{vals.min():.4f}, {vals.max():.4f}]")
        print(f"    permutations reaching observed: {hits}/{len(vals)}   p = {p:.4f}")
        return {"metric": col, "observed": observed, "perm_mean": vals.mean(),
                "perm_sd": vals.std(ddof=1), "p_value": p}

    summary = [
        summarise("expert_accuracy", obs_acc, "greater"),
        summarise("pos_pearson", obs_corrs["pos_pearson"], "greater"),
        summarise("neg_pearson", obs_corrs["neg_pearson"], "less"),
    ]
    pd.DataFrame(summary).to_csv(OUT_DIR / "permutation_summary.csv", index=False)

    print(f"\nSaved to {OUT_DIR}")


if __name__ == "__main__":
    main()
