"""
sidequestz/sensitivity_across_s.py
----------------------------------
Side-quest items 1, 2 and 6: robustness of the framework to the down-weighting
exponent `s`.

Produces three tables (readable + LaTeX):

  Table A (item 1) — attenuation delta agreement across s.
      Pairwise Pearson/Spearman between the delta vectors produced at different
      s values, plus mean absolute divergence in rating points. Shows the
      mechanism produces near-identical adjustments across the plausible range.

  Table B (item 2) — modulator correlations across s.
      The Section 4.3.3 delta-vs-D_misc correlations recomputed at each s.
      Shows the headline modulator result is not an artifact of the tuned value.

  Table C (item 6) — expert paired-comparison accuracy across s.
      OVERALL accuracy only, deliberately. The coarse/fine bins are defined by
      `delta_diff` thresholds that are themselves functions of s, so bin
      membership shifts between settings and those columns would compare
      different subsets of pairs. Overall keeps n fixed and is the only
      apples-to-apples comparison available. State that reason in the paper.

Tables A and B are computed on held-out professors, matching the reporting
convention in Section 4.3. Table C uses the full sample, since the expert pairs
span all professors and restricting them would leave too few to be informative.

Read-only: loads the trained model, never refits, writes nothing except its own
output files.

Usage:
    python sidequestz/sensitivity_across_s.py [--s-values 0.37 0.62 0.83 0.91]
"""

from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor
from scipy import stats
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

# Modes observed in the s_stability.py resample distribution, with the tuned
# value substituted in for the mode it belongs to.
DEFAULT_S_VALUES = [0.37, 0.62, S_VALUE, 0.91]


# ==============================================================================
# LATEX
# ==============================================================================

def to_latex(df: pd.DataFrame, caption: str, label: str, float_fmt: str = "%.4f") -> str:
    body = df.to_latex(
        index=False, escape=True, float_format=float_fmt, column_format="l" * len(df.columns)
    )
    return (
        "\\begin{table}[htbp]\n\\centering\n"
        f"\\caption{{{caption}}}\n\\label{{{label}}}\n"
        f"{body}"
        "\\end{table}\n"
    )


# ==============================================================================
# DELTAS
# ==============================================================================

def deltas_for(model: CatBoostRegressor, df: pd.DataFrame, s: float) -> pd.DataFrame:
    """Per-review deltas at one `s`, mirroring attenuation.run()."""
    full = attenuate(model, df, s)
    return full[full[MISC_D_COL] > 0].reset_index(drop=True)


# ==============================================================================
# TABLE A — DELTA AGREEMENT (item 1)
# ==============================================================================

def table_delta_agreement(delta_by_s: dict[float, np.ndarray]) -> pd.DataFrame:
    rows = []
    for s_a, s_b in itertools.combinations(delta_by_s, 2):
        a, b = delta_by_s[s_a], delta_by_s[s_b]
        rows.append({
            "$s_a$": s_a,
            "$s_b$": s_b,
            "Pearson $r$": pearsonr(a, b)[0],
            "Spearman $\\rho$": spearmanr(a, b)[0],
            "Mean $|\\Delta_a - \\Delta_b|$": np.abs(a - b).mean(),
            "Max $|\\Delta_a - \\Delta_b|$": np.abs(a - b).max(),
        })
    return pd.DataFrame(rows)


# ==============================================================================
# TABLE B — MODULATOR CORRELATIONS (item 2)
# ==============================================================================

def table_modulator_corrs(
    delta_by_s: dict[float, np.ndarray], misc_d: np.ndarray
) -> pd.DataFrame:
    rows = []
    for s, d in delta_by_s.items():
        row = {"$s$": s}
        for name, mask, sym in (("pos", d > 0, "^+"), ("neg", d < 0, "^-")):
            if mask.sum() >= 2:
                row[f"$\\Delta{sym}$ Pearson $r$"] = pearsonr(d[mask], misc_d[mask])[0]
                row[f"$\\Delta{sym}$ Spearman $\\rho$"] = spearmanr(d[mask], misc_d[mask])[0]
            else:
                row[f"$\\Delta{sym}$ Pearson $r$"] = np.nan
                row[f"$\\Delta{sym}$ Spearman $\\rho$"] = np.nan
        rows.append(row)
    return pd.DataFrame(rows)


# ==============================================================================
# TABLE C — EXPERT ACCURACY (item 6)
# ==============================================================================

def table_expert_accuracy(
    model: CatBoostRegressor, df: pd.DataFrame, s_values: list[float]
) -> pd.DataFrame:
    rows = []
    for s in s_values:
        attuned = deltas_for(model, df, s)

        # load_and_merge reads deltas from a CSV path, so round-trip this s's
        # deltas through a temp file rather than duplicating the join logic.
        tmp = OUT_DIR / f".tmp_attuned_{s}.csv"
        attuned.to_csv(tmp, index=False)
        try:
            expert = score_predictions(load_and_merge(attuned_path=tmp))
        finally:
            tmp.unlink(missing_ok=True)

        n = len(expert)
        correct = int(expert["correct"].sum())
        p = stats.binomtest(correct, n, p=0.5, alternative="greater").pvalue
        rows.append({
            "$s$": s,
            "Pairs": n,
            "Correct": correct,
            "Accuracy": correct / n,
            "$p$": p,
        })
    return pd.DataFrame(rows)


# ==============================================================================
# ENTRY POINT
# ==============================================================================

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--s-values", type=float, nargs="+", default=DEFAULT_S_VALUES)
    args = ap.parse_args()
    s_values = sorted(set(args.s_values))

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading model and data...")
    model = CatBoostRegressor()
    model.load_model(str(CATBOOST_FINAL_MODEL), format="cbm")
    df = pd.read_csv(FINAL_EMOTIONS)
    _, test_profs = professor_split(df)

    print(f"  s values: {s_values}   (pipeline uses S_VALUE = {S_VALUE})")

    # Tables A and B are validation metrics, so they use held-out professors only.
    delta_by_s, misc_d = {}, None
    for s in s_values:
        attuned = deltas_for(model, df, s)
        mask = heldout_mask(attuned, test_profs).to_numpy(dtype=bool)
        delta_by_s[s] = attuned.loc[mask, "weighting_delta"].to_numpy()
        if misc_d is None:
            misc_d = attuned.loc[mask, MISC_D_COL].to_numpy()
            print(f"  Held-out misc reviews: {mask.sum():,}")

    tables = [
        (
            table_delta_agreement(delta_by_s),
            "Agreement between attenuation $\\Delta$s produced at different values of $s$ "
            "(held-out professors).",
            "tab:sensitivity-delta-agreement",
            "delta_agreement",
        ),
        (
            table_modulator_corrs(delta_by_s, misc_d),
            "Modulator correlations ($\\Delta$ versus $D_{misc}$) across values of $s$ "
            "(held-out professors).",
            "tab:sensitivity-modulators",
            "modulator_corrs",
        ),
    ]

    if Path(EXPERT_LABELS_PATH).exists():
        tables.append((
            table_expert_accuracy(model, df, s_values),
            "Overall expert paired-comparison accuracy across values of $s$. Coarse and "
            "fine bins are omitted because bin membership is itself a function of $s$.",
            "tab:sensitivity-expert",
            "expert_accuracy",
        ))
    else:
        print(f"\n  Skipping Table C — expert labels not found at {EXPERT_LABELS_PATH}")

    latex_parts = []
    for table, caption, label, stem in tables:
        print(f"\n{'=' * 66}\n  {label}\n{'=' * 66}\n")
        print(table.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
        table.to_csv(OUT_DIR / f"{stem}.csv", index=False)
        latex_parts.append(to_latex(table, caption, label))

    (OUT_DIR / "sensitivity_tables.tex").write_text("\n".join(latex_parts), encoding="utf-8")
    print(f"\nSaved CSVs and sensitivity_tables.tex to {OUT_DIR}")


if __name__ == "__main__":
    main()
