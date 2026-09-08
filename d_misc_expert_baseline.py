"""Compare density-only and attenuation rankings against the same expert pairs.

Run from the project root:
    python d_misc_expert_baseline.py
    python d_misc_expert_baseline.py --pairs-output density_expert_pairs.csv

Uses existing attenuation outputs; does not fit models or rerun the pipeline.
Lower misc_d predicts the more valid review. The comparator prefers smaller
absolute weighting_delta. Coarse/fine bins remain defined by the saved model
deltas, exactly as in src.validation, NOT by differences in density.

Primary scoring preserves validation's first-displayed-review rule for exact
ties. A second analysis counts ties as incorrect for BOTH methods. Missing or
non-directional majorities count as incorrect, following existing validation.
Intervals and exact McNemar tests assume independent pairs and condition on
this fixed panel and curated sample; they do not establish population accuracy.
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest

from constants import ATTUNED_RATINGS, MISC_D_COL
from src.validation import (
    PAIR_KEYS,
    condition_masks,
    merge_expert_deltas,
    score_predictions,
    wilson_interval,
)


def prepare_pairs(ratings):
    """Join both scores to the shared, orientation-aligned expert consensus."""
    ratings = ratings[["review_id", "weighting_delta", MISC_D_COL]].copy()
    if ratings.review_id.isna().any() or ratings.review_id.duplicated().any():
        raise ValueError("Ratings must have unique, nonmissing review IDs")
    for column in ("weighting_delta", MISC_D_COL):
        ratings[column] = pd.to_numeric(ratings[column], errors="raise")
    density = ratings[MISC_D_COL]
    if (density.notna() & (~np.isfinite(density) | ~density.between(0, 1))).any():
        raise ValueError("Nonmissing densities must be finite and within [0, 1]")

    pairs = score_predictions(merge_expert_deltas(ratings))
    density_map = ratings.set_index("review_id")[MISC_D_COL]
    for number in (1, 2):
        pairs[f"density_{number}"] = pairs[f"review_id_{number}"].map(density_map)
    pairs["missing_density"] = pairs[["density_1", "density_2"]].isna().any(axis=1)
    pairs["common_evaluable"] = pairs.evaluable & ~pairs.missing_density
    pairs["density_tie"] = pairs.density_1.eq(pairs.density_2)
    pairs["density_pred"] = np.where(pairs.density_1 <= pairs.density_2, 1., 2.)
    pairs.loc[pairs.missing_density, "density_pred"] = np.nan
    pairs["density_correct"] = (
        pairs.density_pred.eq(pairs.consensus_label)
        & pairs.consensus_label.isin([1, 2])
    )
    pairs["condition"] = "Unbinned"
    for name, mask in condition_masks(pairs).items():
        if name != "Overall":
            pairs.loc[mask, "condition"] = name
    return pairs


def summarize(pairs, ties_incorrect=False):
    """Report matched-sample accuracy and exact paired correctness comparisons."""
    accuracy_rows, comparison_rows = [], []
    for condition, mask in condition_masks(pairs).items():
        subset = pairs.loc[mask & pairs.common_evaluable]
        n = len(subset)
        model_ok = subset.correct.fillna(False).astype(bool)
        density_ok = subset.density_correct.copy()
        if ties_incorrect:
            model_ok = model_ok & ~subset.model_tie
            density_ok = density_ok & ~subset.density_tie
        for method, correct, ties in (
            ("Attenuation", model_ok, subset.model_tie),
            ("Density only", density_ok, subset.density_tie),
        ):
            count = int(correct.sum())
            low, high = wilson_interval(count, n)
            accuracy_rows.append(dict(
                condition=condition, method=method, n=n, correct=count,
                agreement=count / n if n else np.nan,
                ci_low=low, ci_high=high, exact_ties=int(ties.sum()),
            ))
        model_only = int((model_ok & ~density_ok).sum())
        density_only = int((density_ok & ~model_ok).sum())
        discordant = model_only + density_only
        comparison_rows.append(dict(
            condition=condition, n=n,
            both_correct=int((model_ok & density_ok).sum()),
            attenuation_only=model_only, density_only=density_only,
            both_incorrect=int((~model_ok & ~density_ok).sum()),
            attenuation_minus_density_pp=(100 * (model_only - density_only) / n
                                          if n else np.nan),
            mcnemar_exact_p=(binomtest(model_only, discordant, 0.5).pvalue
                             if discordant else (1.0 if n else np.nan)),
        ))
    return pd.DataFrame(accuracy_rows), pd.DataFrame(comparison_rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ratings", type=Path, default=ATTUNED_RATINGS,
                        help="Saved attenuation CSV containing review_id, misc_d and weighting_delta")
    parser.add_argument("--pairs-output", type=Path,
                        help="Optional pair-level CSV; refuses to overwrite an existing file")
    args = parser.parse_args()
    pairs = prepare_pairs(pd.read_csv(args.ratings))
    print(f"\nRatings source: {args.ratings}")
    print(f"Missing density pairs: {int(pairs.missing_density.sum())}; "
          f"common evaluable pairs: {int(pairs.common_evaluable.sum())}/{len(pairs)}")
    common = pairs.loc[pairs.common_evaluable]
    ids = common[PAIR_KEYS].to_numpy().ravel()
    reused = int((pd.Series(ids).value_counts() > 1).sum())
    print(f"Distinct reviews: {len(set(ids))}; reviews reused across pairs: {reused}")
    print("Coarse/fine membership uses saved attenuation deltas and shared validation thresholds.")
    print("Absent or non-directional majorities count as incorrect for both methods.")
    for ties_incorrect in (False, True):
        policy = ("Sensitivity: exact ties count as incorrect"
                  if ties_incorrect else "Primary: exact ties select displayed review 1")
        print(f"\n=== {policy} ===")
        accuracy, comparisons = summarize(pairs, ties_incorrect)
        print("Agreement and two-sided 95% Wilson intervals:")
        print(accuracy.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        print("\nPaired comparison (positive difference favours attenuation):")
        print(comparisons.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\nInference conditions on the curated pairs and fixed expert panel.")
    print("Wilson intervals and McNemar p-values assume independent pairs; review/instructor "
          "overlap may violate this. Subgroup tests are exploratory, without multiplicity correction.")
    print("A nonsignificant paired test does not establish equivalence between methods.")
    if args.pairs_output:
        pairs.to_csv(args.pairs_output, index=False, mode="x")
        print(f"Saved pair audit: {args.pairs_output}")


if __name__ == "__main__":
    main()
