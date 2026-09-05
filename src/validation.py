"""Three-expert attenuation validation, Fleiss' kappa and Wilson intervals.

Labels 1/2 select a review; 3 is non-directional (both valid). Blank ratings
are missing. Kappa uses complete pairs before joining model deltas. Accuracy
counts a matching directional majority as correct and no majority as incorrect.
A label-3 majority also counts as incorrect; only unavailable deltas are excluded.
Wilson intervals assume
independent review pairs and condition on these three fixed experts.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from constants import (
    ATTUNED_RATINGS, EXPERT_LABELS_PATH, RESULTS_DIR,
    COARSE_DELTA_THRESHOLD, FINE_DELTA_MIN, FINE_DELTA_MAX,
)

PAIR_KEYS = ["review_id_1", "review_id_2"]
RATER_COLUMNS = ["expert_1", "expert_2", "expert_3"]


def load_expert_consensus(expert_paths=EXPERT_LABELS_PATH):
    """Align unordered pairs by IDs; preserve expert 1's displayed orientation.

Use the union of pairs so missing raters remain visible. Require three files;
two matching votes are required even when the third rating is missing.
"""
    if isinstance(expert_paths, (str, Path)) or len(expert_paths) != 3:
        raise ValueError("Provide exactly three expert CSV paths")
    merged = None
    for path, column in zip(expert_paths, RATER_COLUMNS):
        frame = pd.read_csv(path)[PAIR_KEYS + ["Expert Label:"]].copy()
        for key in PAIR_KEYS:
            values = pd.to_numeric(frame[key], errors="raise")
            if values.isna().any() or not np.isfinite(values).all() or (values % 1 != 0).any():
                raise ValueError(f"{path}: review IDs must be nonmissing integers")
            frame[key] = values.astype("int64")
        labels = pd.to_numeric(frame.pop("Expert Label:"), errors="raise")
        if (~labels.isna() & ~labels.isin([1, 2, 3])).any():
            raise ValueError(f"{path}: allowed labels are 1, 2, 3 or blank")
        reverse = frame.review_id_1 > frame.review_id_2
        frame[column] = labels.where(~(reverse & labels.isin([1, 2])), 3 - labels)
        frame["display_reversed"] = reverse
        frame[PAIR_KEYS] = np.sort(frame[PAIR_KEYS].to_numpy(), axis=1)
        if (frame.review_id_1 == frame.review_id_2).any() or frame.duplicated(PAIR_KEYS).any():
            raise ValueError(f"{path}: duplicate or self-comparison pair")
        if merged is None:
            merged = frame
        else:
            merged = merged.merge(frame.drop(columns="display_reversed"), on=PAIR_KEYS,
                                  how="outer", validate="one_to_one")
    reverse = merged.pop("display_reversed").eq(True)
    merged.loc[reverse, PAIR_KEYS] = merged.loc[reverse, PAIR_KEYS[::-1]].to_numpy()
    for column in RATER_COLUMNS:
        labels = merged[column]
        merged[column] = labels.where(~(reverse & labels.isin([1, 2])), 3 - labels)
    for label in (1, 2, 3):
        merged[f"votes_{label}"] = merged[RATER_COLUMNS].eq(label).sum(axis=1)
    merged["n_ratings"] = merged[RATER_COLUMNS].notna().sum(axis=1)
    merged["consensus_label"] = np.select(
        [merged[f"votes_{label}"] >= 2 for label in (1, 2, 3)], [1, 2, 3], default=np.nan)
    merged["has_majority"] = merged.consensus_label.notna()
    merged["Expert Label:"] = merged.consensus_label
    merged["unsure"] = ~merged.consensus_label.isin([1, 2])
    return merged.sort_values(PAIR_KEYS).reset_index(drop=True)


def fleiss_kappa(ratings):
    """Fixed-rater Fleiss kappa with pooled category proportions.

Use complete pairs and labels 1, 2, 3. Return NaN when undefined.
"""
    complete = ratings[RATER_COLUMNS].dropna()
    counts = np.column_stack([complete.eq(k).sum(axis=1) for k in (1, 2, 3)])
    n = len(counts)
    observed = float(np.mean((counts * (counts - 1)).sum(axis=1) / 6)) if n else np.nan
    expected = float(np.sum((counts.sum(axis=0) / (3 * n)) ** 2)) if n else np.nan
    kappa = (observed - expected) / (1 - expected) if n and expected < 1 else np.nan
    return dict(n_total=len(ratings), n_complete=n, n_missing=len(ratings) - n,
                observed_agreement=observed, expected_agreement=expected, fleiss_kappa=kappa)


def fleiss_kappa_excluding_3(ratings):
    """Generalized Fleiss kappa after excluding individual 3/blank votes.

    Uses the unweighted irrCAC formulation for variable rater counts:
    observed agreement is the mean of each pair's agreement proportion among
    pairs with >=2 directional votes. Category proportions are the mean of
    within-pair proportions among pairs with >=1 directional vote. Thus a
    singleton contributes only to chance agreement; a zero-vote pair to neither.
    With three directional votes everywhere this equals ordinary Fleiss kappa.
    Reference: https://github.com/kgwet/irrCAC/blob/master/R/agree.coeff3.raw.r
    """
    votes = ratings[RATER_COLUMNS]
    counts = np.column_stack([votes.eq(k).sum(axis=1) for k in (1, 2)])
    totals = counts.sum(axis=1)
    comparable = totals >= 2
    nonempty = totals >= 1
    observed = expected = kappa = np.nan
    if comparable.any():
        numerator = (counts[comparable] * (counts[comparable] - 1)).sum(axis=1)
        denominator = totals[comparable] * (totals[comparable] - 1)
        observed = float(np.mean(numerator / denominator))
    if nonempty.any():
        proportions = (counts[nonempty] / totals[nonempty, None]).mean(axis=0)
        expected = float(np.sum(proportions ** 2))
    if comparable.any() and expected < 1:
        kappa = (observed - expected) / (1 - expected)
    return dict(
        n_total=len(votes), n_agreement_pairs=int(comparable.sum()),
        n_marginal_pairs=int(nonempty.sum()),
        n_two_raters=int((totals == 2).sum()), n_three_raters=int((totals == 3).sum()),
        n_one_rater=int((totals == 1).sum()), n_zero_raters=int((totals == 0).sum()),
        n_excluded_3=int(votes.eq(3).sum().sum()),
        n_blank_votes=int(votes.isna().sum().sum()),
        observed_agreement=observed, expected_agreement=expected,
        generalized_fleiss_kappa=kappa,
    )


def merge_expert_deltas(attuned, expert_path=EXPERT_LABELS_PATH, verbose=True):
    """Shared validation/robustness join, retaining exclusions for audit."""
    expert = load_expert_consensus(expert_path)
    # Bootstrap callers can contain repeated identical review rows.
    deltas = attuned[["review_id", "weighting_delta"]].drop_duplicates()
    if deltas.review_id.isna().any() or deltas.review_id.duplicated().any():
        raise ValueError("Model data contains missing IDs or conflicting deltas")
    delta_map = deltas.set_index("review_id").weighting_delta
    for number in (1, 2):
        expert[f"delta_{number}"] = expert[f"review_id_{number}"].map(delta_map)
    expert["missing_delta"] = ~np.isfinite(expert[["delta_1", "delta_2"]]).all(axis=1)
    expert["evaluable"] = ~expert.missing_delta
    if verbose:
        print(f"Pairs: {len(expert)}; no majority: {(~expert.has_majority).sum()}; "
              f"non-directional majority: {expert.consensus_label.eq(3).sum()}; "
              f"missing model deltas: {expert.missing_delta.sum()}; "
              f"evaluable: {expert.evaluable.sum()}")
    return expert


def load_and_merge(attuned_path=ATTUNED_RATINGS, expert_path=EXPERT_LABELS_PATH):
    return merge_expert_deltas(pd.read_csv(attuned_path), expert_path)


def score_predictions(expert):
    expert = expert.copy()
    expert["abs_delta_1"] = expert.delta_1.abs()
    expert["abs_delta_2"] = expert.delta_2.abs()
    expert["delta_diff"] = (expert.abs_delta_1 - expert.abs_delta_2).abs()
    # Preserve the existing review-1 tie rule.
    expert["model_pred"] = np.where(expert.abs_delta_1 <= expert.abs_delta_2, 1., 2.)
    expert.loc[expert.missing_delta, "model_pred"] = np.nan
    expert["model_tie"] = expert.abs_delta_1.eq(expert.abs_delta_2)
    expert["expert_label"] = expert.consensus_label
    expert["correct"] = (
        expert.model_pred.eq(expert.expert_label).fillna(False)
        & expert.consensus_label.isin([1, 2])
    ).astype("boolean")
    expert.loc[~expert.evaluable, "correct"] = pd.NA
    return expert


def wilson_interval(correct, n, confidence=0.95):
    """Two-sided interval, independent of the one-sided accuracy test."""
    if not 0 < confidence < 1 or not 0 <= correct <= n:
        raise ValueError("Invalid confidence level or success count")
    if n == 0:
        return np.nan, np.nan
    interval = stats.binomtest(correct, n).proportion_ci(confidence, method="wilson")
    return interval.low, interval.high


def condition_masks(expert):
    """Shared disjoint delta bins; pairs without model deltas are unbinned."""
    available = ~expert.missing_delta
    return {
        "Overall": pd.Series(True, index=expert.index),
        "Coarse": available & (expert.delta_diff >= COARSE_DELTA_THRESHOLD),
        "Fine": available & expert.delta_diff.between(FINE_DELTA_MIN, FINE_DELTA_MAX, inclusive="left"),
    }


def kappa_summary(expert, exclude_3=False):
    """Recompute category proportions independently within each condition.

    Overall includes all annotated pairs. Coarse/fine require model deltas to
    assign bins, but never require a majority vote or model correctness.
    exclude_3 adds the variable-rater sensitivity analysis on directional votes.
    """
    calculate = fleiss_kappa_excluding_3 if exclude_3 else fleiss_kappa
    return pd.DataFrame([
        dict(condition=condition, **calculate(expert.loc[mask]))
        for condition, mask in condition_masks(expert).items()
    ])


def accuracy_summary(expert, confidence=0.95):
    """Consensus and individual expert accuracy with explicit denominators."""
    conditions = condition_masks(expert)
    rows = []
    for target in ["consensus_label"] + RATER_COLUMNS:
        valid = (expert.evaluable if target == "consensus_label"
                 else expert[target].isin([1, 2]) & ~expert.missing_delta)
        for condition, mask in conditions.items():
            subset = expert.loc[valid & mask]
            n = len(subset)
            correct = (int(subset.correct.sum()) if target == "consensus_label"
                       else int(subset.model_pred.eq(subset[target]).sum()))
            lo, hi = wilson_interval(correct, n, confidence)
            rows.append(dict(target=target, condition=condition, n=n, correct=correct,
                             accuracy=correct / n if n else np.nan,
                             confidence=confidence, ci_low=lo, ci_high=hi,
                             p_value=stats.binomtest(correct, n, p=0.5, alternative="greater").pvalue
                             if n else np.nan))
    return pd.DataFrame(rows)


def report(expert):
    print("\n=== Three-expert attenuation validation ===")
    print(kappa_summary(expert).to_string(index=False))
    print("\nGeneralized Fleiss' kappa excluding individual label-3 votes:")
    print(kappa_summary(expert, exclude_3=True).to_string(index=False))
    print("Pairs with one retained vote contribute only to chance agreement; "
          "pairs with zero retained votes are excluded.")
    print(f"Pairs without model deltas (overall kappa only): {expert.missing_delta.sum()}")
    print("\nAccuracy and two-sided 95% Wilson intervals:")
    print("No-majority and label-3-majority pairs with model deltas count as incorrect.")
    print(accuracy_summary(expert).to_string(index=False, float_format=lambda x: f"{x:.6g}"))
    print(f"\nModel ties (review 1 selected): {expert.model_tie.sum()}")


def run():
    expert = score_predictions(load_and_merge())
    report(expert)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    expert.to_csv(RESULTS_DIR / "expert_consensus.csv", index=False)
    accuracy_summary(expert).to_csv(RESULTS_DIR / "expert_validation.csv", index=False)
    kappa_summary(expert).to_csv(RESULTS_DIR / "expert_fleiss_kappa.csv", index=False)
    kappa_summary(expert, exclude_3=True).to_csv(
        RESULTS_DIR / "expert_fleiss_kappa_excluding_3.csv", index=False)


if __name__ == "__main__":
    run()
