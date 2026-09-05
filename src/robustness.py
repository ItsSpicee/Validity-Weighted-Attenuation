"""
src/robustness.py
-----------------
Stage 7: robustness analyses supporting Sections 4.3 and 4.4. Opt-in — this
stage is not part of a default pipeline run, because the permutation control
re-attenuates the corpus N_PERMUTATIONS times.

Three independent analyses:

  Permutation control
      Every result in Section 4.3 shows that attenuation behaves as designed,
      but none of them establish that the behaviour depends on a review's
      *actual* off-topic content. A mechanism that adjusted ratings by an
      arbitrary review-specific amount would also produce structured-looking
      correlations. Permuting D_misc among the reviews that have off-topic
      content breaks the correspondence between measured density and applied
      attenuation while leaving the marginal distribution and the analytic
      population intact, so it is the control condition that separates the two.
      The null is therefore "the amount of off-topic content is unrelated to
      which review it is", not "off-topic content is absent" -- the graded
      claim Sections 4.3.3 and 4.4 actually make.

  Sensitivity across s
      Table A — agreement between the deltas produced at different s.
      Table B — the Section 4.3.3 modulator correlations recomputed at each s.
      Table C — expert paired-comparison accuracy at each s.
      Together these show the framework's behaviour is not an artifact of the
      particular exponent the grid search happened to select, which matters
      because the s objective has several near-equivalent minima.

  Bootstrap professor stability
      Resamples the 206 held-out professors with replacement across N iterations,
      recomputing modulator correlations and expert accuracy on each bootstrap
      sample. Reports means, SDs, and 95% CIs, showing that the results are not
      an artifact of which professors happen to fall on the held-out side.

Read-only with respect to the pipeline: loads the trained model, never refits,
and writes only into RESULTS_DIR.

Produces (in RESULTS_DIR):
  - permutation_test.csv / permutation_summary.csv
  - bootstrap_professors.csv / bootstrap_summary.csv
  - delta_agreement.csv / modulator_corrs.csv / expert_accuracy.csv
  - robustness_tables.tex

Usage:
    python pipeline.py --robustness
    python -m src.robustness --skip-permutation
    python -m src.robustness --n-permutations 20 --s-values 0.4 0.83
"""

from __future__ import annotations

import itertools

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor
from scipy import stats
from scipy.stats import pearsonr, spearmanr

from constants import (
    CATBOOST_FINAL_MODEL,
    COARSE_DELTA_THRESHOLD,
    EXPERT_LABELS_PATH,
    FINAL_EMOTIONS,
    FINE_DELTA_MIN,
    FINE_DELTA_MAX,
    MISC_D_COL,
    N_PERMUTATIONS,
    PERMUTATION_SEED,
    RESULTS_DIR,
    SENSITIVITY_S_VALUES,
    S_VALUE,
)
from src.attenuation import attenuate
from src.splits import heldout_mask, professor_split
from src.validation import merge_expert_deltas, score_predictions


# ==============================================================================
# SHARED HELPERS
# ==============================================================================

def _to_latex(df: pd.DataFrame, caption: str, label: str, float_fmt: str = "%.4f") -> str:
    body = df.to_latex(
        index=False, escape=True, float_format=float_fmt, column_format="l" * len(df.columns)
    )
    return (
        "\\begin{table}[htbp]\n\\centering\n"
        f"\\caption{{{caption}}}\n\\label{{{label}}}\n"
        f"{body}"
        "\\end{table}\n"
    )


def deltas_for(model: CatBoostRegressor, df: pd.DataFrame, s: float) -> pd.DataFrame:
    """Per-review deltas at one `s`, mirroring attenuation.run()."""
    full = attenuate(model, df, s)
    return full[full[MISC_D_COL] > 0].reset_index(drop=True)


def expert_accuracy(
    attuned: pd.DataFrame, verbose: bool = False
) -> dict[str, tuple[int, int]]:
    """Per-condition (correct, n) for the expert paired comparison.

    Returns a dict with keys 'overall', 'coarse', 'fine'.
    """
    expert = score_predictions(merge_expert_deltas(attuned, verbose=verbose))
    expert = expert.loc[expert["evaluable"]]
    coarse = expert[expert["delta_diff"] >= COARSE_DELTA_THRESHOLD]
    fine = expert[expert["delta_diff"].between(FINE_DELTA_MIN, FINE_DELTA_MAX, inclusive="left")]
    return {
        "overall": (int(expert["correct"].sum()), len(expert)),
        "coarse": (int(coarse["correct"].sum()), len(coarse)),
        "fine": (int(fine["correct"].sum()), len(fine)),
    }


def _modulator_corrs(delta: np.ndarray, misc_d: np.ndarray) -> dict[str, float]:
    """Delta-vs-D_misc correlations, split by direction of adjustment."""
    out: dict[str, float] = {}
    for name, mask in (("pos", delta > 0), ("neg", delta < 0)):
        if mask.sum() >= 2:
            out[f"{name}_pearson"]  = pearsonr(delta[mask], misc_d[mask])[0]
            out[f"{name}_spearman"] = spearmanr(delta[mask], misc_d[mask])[0]
        else:
            out[f"{name}_pearson"] = out[f"{name}_spearman"] = np.nan
    return out


# ==============================================================================
# PERMUTATION CONTROL
# ==============================================================================

def _permutation_measure(
    model: CatBoostRegressor,
    df_variant: pd.DataFrame,
    test_profs,
    true_misc_d: pd.Series,
    verbose: bool = False,
) -> tuple[float, int, dict[str, float]]:
    """Attenuate one frame; return (expert accuracy, expert n, modulator corrs).

    Correlations are measured against the TRUE densities, joined on `review_id`,
    not against whatever densities this frame carries. That is the whole point of
    the control: the paper claims the adjustment a review receives tracks its
    *real* off-topic content, so the null has to ask whether a mechanism driven
    by shuffled densities still reproduces that relationship. Correlating the
    permuted deltas against the permuted densities would instead re-measure the
    mechanism against its own input and return roughly the observed value at
    every permutation, testing nothing.

    The join is on values, not on population: the permutation is restricted to
    non-zero densities (see `permutation_control`), so the `D_misc > 0` subset is
    already identical to the observed one in every permutation. What the join
    supplies is each review's TRUE density as the correlate.
    """
    full = attenuate(model, df_variant, S_VALUE)

    # Expert accuracy mirrors the pipeline, which scores against the misc subset
    # of this frame. Because the permutation preserves the zero pattern, that
    # subset is the same set of reviews every iteration and n holds at the
    # observed value; it is still returned so a drift would be visible rather
    # than assumed away.
    if all(path.exists() for path in EXPERT_LABELS_PATH):
        misc_subset = full[full[MISC_D_COL] > 0].reset_index(drop=True)
        accs = expert_accuracy(misc_subset, verbose=verbose)
        acc_overall = accs["overall"][0] / accs["overall"][1] if accs["overall"][1] else float("nan")
        acc_coarse = accs["coarse"][0] / accs["coarse"][1] if accs["coarse"][1] else float("nan")
        acc_fine = accs["fine"][0] / accs["fine"][1] if accs["fine"][1] else float("nan")
        n = accs["overall"][1]
    else:
        acc_overall = acc_coarse = acc_fine = float("nan")
        n = 0

    true_d = full["review_id"].map(true_misc_d)
    mask = heldout_mask(full, test_profs).to_numpy(dtype=bool) & (true_d > 0).to_numpy()

    return acc_overall, acc_coarse, acc_fine, n, _modulator_corrs(
        full.loc[mask, "weighting_delta"].to_numpy(), true_d[mask].to_numpy()
    )


def _summarise_permutation(
    perm: pd.DataFrame, col: str, observed: float, direction: str
) -> dict:
    vals = perm[col].dropna().to_numpy()
    # One-sided: how often does the permuted null reach what we observed?
    hits = int((vals >= observed).sum()) if direction == "greater" else int((vals <= observed).sum())
    # +1 correction: a permutation p-value can never legitimately be zero.
    p = (hits + 1) / (len(vals) + 1)

    print(f"\n  {col}")
    print(f"    observed        : {observed:.4f}")
    print(f"    permuted mean   : {vals.mean():.4f}  (SD {vals.std(ddof=1):.4f})")
    print(f"    permuted range  : [{vals.min():.4f}, {vals.max():.4f}]")
    print(f"    permutations reaching observed: {hits}/{len(vals)}   p = {p:.4f}")

    return {
        "metric": col, "observed": observed, "perm_mean": vals.mean(),
        "perm_sd": vals.std(ddof=1), "p_value": p,
    }


def permutation_control(
    model: CatBoostRegressor,
    df: pd.DataFrame,
    test_profs,
    n_permutations: int = N_PERMUTATIONS,
    seed: int = PERMUTATION_SEED,
) -> pd.DataFrame:
    """Permute D_misc, re-attenuate, and compare against the observed result."""
    true_misc_d = df.set_index("review_id")[MISC_D_COL]

    print(f"\n  Observed (true D_misc), s = {S_VALUE}...")
    obs_acc, obs_coarse, obs_fine, obs_n, obs_corrs = _permutation_measure(
        model, df, test_profs, true_misc_d, verbose=True
    )
    print(f"    Expert accuracy (overall) : {obs_acc:.4f}  (n = {obs_n})")
    print(f"    Expert accuracy (coarse)  : {obs_coarse:.4f}")
    print(f"    Expert accuracy (fine)    : {obs_fine:.4f}")
    print(f"    Delta+ vs D_misc (r)      : {obs_corrs['pos_pearson']:.4f}")
    print(f"    Delta- vs D_misc (r)      : {obs_corrs['neg_pearson']:.4f}")

    print(f"\n  Running {n_permutations} permutations of D_misc...")
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n_permutations):
        df_perm = df.copy()
        # Permuting the column permutes it everywhere it is consumed: as a model
        # feature and as the zeta driver inside _apply_down_weighting. Permuting
        # only one would leave a back-channel through which true density still
        # influences the adjustment.
        #
        # The shuffle is restricted to reviews whose density is already non-zero,
        # so zeros stay zero. That subset IS the analytic population: Section 4.3
        # reports on `D_misc > 0` and all expert pairs fall inside it, so
        # exchangeability only has to hold there. Permuting the full column
        # instead relocates the zeros, which silently resamples the reporting
        # population every iteration -- the expert comparison then scores only
        # those pairs whose BOTH reviews happened to draw a positive density
        # (~0.606^2 x 80 = ~29 of 77), inflating the null's variance and making
        # the resulting p-value a small-sample artifact.
        vals = df_perm[MISC_D_COL].to_numpy().copy()
        nz = np.flatnonzero(vals > 0)
        vals[nz] = rng.permutation(vals[nz])
        df_perm[MISC_D_COL] = vals

        acc, coarse, fine, n, corrs = _permutation_measure(model, df_perm, test_profs, true_misc_d)
        rows.append({
            "permutation": i,
            "expert_accuracy": acc, "expert_coarse": coarse, "expert_fine": fine,
            "expert_n": n, **corrs,
        })

        if (i + 1) % 10 == 0:
            print(f"    {i + 1}/{n_permutations}")

    perm = pd.DataFrame(rows)
    perm.to_csv(RESULTS_DIR / "permutation_test.csv", index=False)

    print("\n" + "=" * 66)
    print("  PERMUTATION CONTROL")
    print("=" * 66)
    summary = pd.DataFrame([
        _summarise_permutation(perm, "expert_accuracy", obs_acc, "greater"),
        _summarise_permutation(perm, "expert_coarse", obs_coarse, "greater"),
        _summarise_permutation(perm, "expert_fine", obs_fine, "greater"),
        _summarise_permutation(perm, "pos_pearson", obs_corrs["pos_pearson"], "greater"),
        _summarise_permutation(perm, "neg_pearson", obs_corrs["neg_pearson"], "less"),
    ])
    summary.to_csv(RESULTS_DIR / "permutation_summary.csv", index=False)
    return summary


# ==============================================================================
# SENSITIVITY ACROSS S
# ==============================================================================

def table_delta_agreement(delta_by_s: dict[float, np.ndarray]) -> pd.DataFrame:
    """Table A — do different s values produce the same adjustments?"""
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


def table_modulator_corrs(
    delta_by_s: dict[float, np.ndarray], misc_d: np.ndarray
) -> pd.DataFrame:
    """Table B — is the Section 4.3.3 result an artifact of the tuned s?"""
    rows = []
    for s, d in delta_by_s.items():
        row: dict = {"$s$": s}
        for name, mask, sym in (("pos", d > 0, "^+"), ("neg", d < 0, "^-")):
            if mask.sum() >= 2:
                row[f"$\\Delta{sym}$ Pearson $r$"]      = pearsonr(d[mask], misc_d[mask])[0]
                row[f"$\\Delta{sym}$ Spearman $\\rho$"] = spearmanr(d[mask], misc_d[mask])[0]
            else:
                row[f"$\\Delta{sym}$ Pearson $r$"]      = np.nan
                row[f"$\\Delta{sym}$ Spearman $\\rho$"] = np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def table_expert_accuracy(
    model: CatBoostRegressor, df: pd.DataFrame, s_values: list[float]
) -> pd.DataFrame:
    """Table C — expert paired-comparison accuracy at each s.

    OVERALL accuracy only, deliberately. The coarse and fine bins are defined by
    `delta_diff` thresholds that are themselves functions of s, so bin
    membership shifts between settings and those columns would compare different
    subsets of pairs rather than the same pairs under different treatment.
    Overall keeps n fixed and is the only apples-to-apples comparison available.
    State that reason if the table goes in the paper.
    """
    rows = []
    for s in s_values:
        accs = expert_accuracy(deltas_for(model, df, s))
        correct, n = accs["overall"]
        c_correct, c_n = accs["coarse"]
        f_correct, f_n = accs["fine"]
        rows.append({
            "$s$": s,
            "Pairs": n,
            "Overall": correct / n if n else np.nan,
            "Coarse": c_correct / c_n if c_n else np.nan,
            "Fine": f_correct / f_n if f_n else np.nan,
            "$p$": stats.binomtest(correct, n, p=0.5, alternative="greater").pvalue if n else np.nan,
        })
    return pd.DataFrame(rows)


def sensitivity_across_s(
    model: CatBoostRegressor,
    df: pd.DataFrame,
    test_profs,
    s_values: list[float],
) -> list[tuple[pd.DataFrame, str, str, str]]:
    """Build Tables A, B and C. Returns (table, caption, label, stem) tuples."""
    print(f"\n  s values: {s_values}   (pipeline uses S_VALUE = {S_VALUE})")

    # Tables A and B are validation metrics, so they use held-out professors,
    # matching the reporting convention in Section 4.3.
    delta_by_s: dict[float, np.ndarray] = {}
    misc_d: np.ndarray | None = None
    for s in s_values:
        attuned = deltas_for(model, df, s)
        mask = heldout_mask(attuned, test_profs).to_numpy(dtype=bool)
        delta_by_s[s] = attuned.loc[mask, "weighting_delta"].to_numpy()
        if misc_d is None:
            misc_d = attuned.loc[mask, MISC_D_COL].to_numpy()
            print(f"  Held-out misc reviews: {int(mask.sum()):,}")

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

    # Table C uses the full sample: the expert pairs span all professors and
    # restricting them to held-out ones would leave too few to be informative.
    if all(path.exists() for path in EXPERT_LABELS_PATH):
        tables.append((
            table_expert_accuracy(model, df, s_values),
            "Overall expert paired-comparison accuracy across values of $s$ (full sample). "
            "Coarse and fine bins are omitted because bin membership is itself a function "
            "of $s$.",
            "tab:sensitivity-expert",
            "expert_accuracy",
        ))
    else:
        missing = [str(path) for path in EXPERT_LABELS_PATH if not path.exists()]
        print(f"\n  Skipping Table C — expert labels not found: {', '.join(missing)}")

    return tables


# ==============================================================================
# BOOTSTRAP PROFESSOR STABILITY
# ==============================================================================

N_BOOTSTRAP = 1000
BOOTSTRAP_SEED = 42


def bootstrap_professor_stability(
    model: CatBoostRegressor,
    df: pd.DataFrame,
    test_profs,
    n_bootstrap: int = N_BOOTSTRAP,
    seed: int = BOOTSTRAP_SEED,
) -> pd.DataFrame:
    """Resample held-out professors with replacement; show metric stability.

    The held-out set has 206 professors. Each iteration draws 206 professors
    with replacement, recomputes modulator correlations and expert accuracy
    on the resampled set, and records the results. No re-fitting or
    re-attenuating — the attenuated data is computed once from the true model.
    """
    print(f"\n  Bootstrap professor stability ({n_bootstrap} iterations)...")

    full = attenuate(model, df, S_VALUE)
    misc = full[full[MISC_D_COL] > 0].reset_index(drop=True)
    held_mask = heldout_mask(misc, test_profs).to_numpy(dtype=bool)
    held = misc[held_mask].copy()

    test_prof_list = list(test_profs)
    rng = np.random.default_rng(seed)

    rows = []
    for i in range(n_bootstrap):
        sampled_profs = rng.choice(test_prof_list, size=len(test_prof_list), replace=True)
        # Build the bootstrap sample: all reviews belonging to sampled professors.
        # A professor drawn k times contributes k copies of their reviews.
        parts = []
        for p in sampled_profs:
            parts.append(held[held["prof_ID"] == p])
        boot = pd.concat(parts, ignore_index=True)

        delta = boot["weighting_delta"].to_numpy()
        misc_d = boot[MISC_D_COL].to_numpy()
        corrs = _modulator_corrs(delta, misc_d)

        rows.append({
            "iteration": i,
            "pos_pearson": corrs["pos_pearson"],
            "neg_pearson": corrs["neg_pearson"],
            "pos_spearman": corrs["pos_spearman"],
            "neg_spearman": corrs["neg_spearman"],
        })

        if (i + 1) % 100 == 0:
            print(f"    {i + 1}/{n_bootstrap}")

    boot_df = pd.DataFrame(rows)
    boot_df.to_csv(RESULTS_DIR / "bootstrap_professors.csv", index=False)

    # Report
    print("\n" + "=" * 66)
    print("  BOOTSTRAP PROFESSOR STABILITY (held-out professors)")
    print("=" * 66)

    summary_rows = []
    for col, label in [
        ("pos_pearson",   "Δ+ vs D_misc (Pearson r)"),
        ("neg_pearson",   "Δ- vs D_misc (Pearson r)"),
        ("pos_spearman",  "Δ+ vs D_misc (Spearman ρ)"),
        ("neg_spearman",  "Δ- vs D_misc (Spearman ρ)"),
    ]:
        vals = boot_df[col].dropna().to_numpy()
        if len(vals) == 0:
            continue
        lo, hi = np.percentile(vals, [2.5, 97.5])
        print(f"\n  {label}")
        print(f"    mean: {vals.mean():.4f}   SD: {vals.std(ddof=1):.4f}")
        print(f"    95% CI: [{lo:.4f}, {hi:.4f}]")
        summary_rows.append({
            "metric": label,
            "mean": vals.mean(),
            "sd": vals.std(ddof=1),
            "ci_lo": lo,
            "ci_hi": hi,
        })

    summary = pd.DataFrame(summary_rows)
    summary.to_csv(RESULTS_DIR / "bootstrap_summary.csv", index=False)
    return summary


# ==============================================================================
# ENTRY POINT
# ==============================================================================

def run(
    skip_permutation: bool = False,
    skip_sensitivity: bool = False,
    skip_bootstrap: bool = False,
    n_permutations: int = N_PERMUTATIONS,
    n_bootstrap: int = N_BOOTSTRAP,
    s_values: list[float] | None = None,
) -> None:
    print("\n=== Stage 7: Robustness ===")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading model and data...")
    model = CatBoostRegressor()
    model.load_model(str(CATBOOST_FINAL_MODEL), format="cbm")
    df = pd.read_csv(FINAL_EMOTIONS)
    _, test_profs = professor_split(df)

    latex_parts: list[str] = []

    if not skip_sensitivity:
        resolved = sorted(set(s_values if s_values else SENSITIVITY_S_VALUES + [S_VALUE]))
        for table, caption, label, stem in sensitivity_across_s(model, df, test_profs, resolved):
            print(f"\n{'=' * 66}\n  {label}\n{'=' * 66}\n")
            print(table.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
            table.to_csv(RESULTS_DIR / f"{stem}.csv", index=False)
            latex_parts.append(_to_latex(table, caption, label))
    else:
        print("  Skipping sensitivity tables.")

    if not skip_permutation:
        summary = permutation_control(model, df, test_profs, n_permutations=n_permutations)
        latex_parts.append(_to_latex(
            summary,
            "Permutation control: observed statistics against a null in which $D_{misc}$ "
            "is permuted across reviews.",
            "tab:permutation-control",
        ))
    else:
        print("\n  Skipping permutation control.")

    if not skip_bootstrap:
        boot_summary = bootstrap_professor_stability(
            model, df, test_profs, n_bootstrap=n_bootstrap
        )
        latex_parts.append(_to_latex(
            boot_summary,
            "Bootstrap professor stability: 95\\% confidence intervals from resampling "
            "held-out professors with replacement.",
            "tab:bootstrap-professors",
        ))
    else:
        print("\n  Skipping bootstrap professor stability.")

    if latex_parts:
        (RESULTS_DIR / "robustness_tables.tex").write_text(
            "\n".join(latex_parts), encoding="utf-8"
        )
        print(f"\n  Saved CSVs and robustness_tables.tex to {RESULTS_DIR}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Stage 7: robustness analyses")
    parser.add_argument("--skip-permutation", action="store_true")
    parser.add_argument("--skip-sensitivity", action="store_true")
    parser.add_argument("--skip-bootstrap", action="store_true")
    parser.add_argument("--n-permutations", type=int, default=N_PERMUTATIONS)
    parser.add_argument("--n-bootstrap", type=int, default=N_BOOTSTRAP)
    parser.add_argument("--s-values", type=float, nargs="+", default=None)
    args = parser.parse_args()

    run(
        skip_permutation=args.skip_permutation,
        skip_sensitivity=args.skip_sensitivity,
        skip_bootstrap=args.skip_bootstrap,
        n_permutations=args.n_permutations,
        n_bootstrap=args.n_bootstrap,
        s_values=args.s_values,
    )
