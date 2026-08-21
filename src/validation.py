"""
src/validation.py
-----------------
Stage 6: External expert validation of the attenuation mechanism.

Evaluates whether the model's attenuation delta correctly identifies
which review in a pair is more pedagogically valid, using expert labels.

Produces:
  - Overall paired comparison accuracy
  - Coarse accuracy  (Difference in |Δ| ≥ COARSE_DELTA_THRESHOLD)
  - Fine-grained accuracy  (FINE_DELTA_MIN ≤ Difference in |Δ| ≤ FINE_DELTA_MAX)
"""

import numpy as np
import pandas as pd
from scipy import stats

from constants import (
    ATTUNED_RATINGS,
    EXPERT_LABELS_PATH,
    COARSE_DELTA_THRESHOLD,
    FINE_DELTA_MIN,
    FINE_DELTA_MAX,
)


# ==============================================================================
# DATA PREPARATION
# ==============================================================================

def merge_expert_deltas(
    attuned: pd.DataFrame,
    expert_path=EXPERT_LABELS_PATH,
    verbose: bool = True,
) -> pd.DataFrame:
    """Attach attenuation deltas to the expert pair labels.

    Split out from `load_and_merge` so callers that already hold an attuned
    frame can reuse this join instead of round-tripping through a CSV. The
    robustness analyses build one attuned frame per permutation and per `s`, so
    without this they would either write hundreds of temp files or duplicate the
    join — and a duplicated copy would drift once expert labels move to a
    majority vote across several raters.

    `verbose=False` silences the per-call dropped-pair and unsure notices, which
    are identical on every iteration of a permutation loop.
    """
    expert = pd.read_csv(expert_path)

    delta_map = attuned.set_index("review_id")["weighting_delta"].to_dict()
    expert["delta_1"] = expert["review_id_1"].map(delta_map)
    expert["delta_2"] = expert["review_id_2"].map(delta_map)

    missing = expert["delta_1"].isna() | expert["delta_2"].isna()
    if missing.any():
        missing_df = expert[missing]
        if verbose:
            print(f"  Warning: {missing.sum()} pair(s) dropped — review_id not found in attuned data.")
            for _, row in missing_df.iterrows():
                print(f"    review_id_1={row['review_id_1']}  review_id_2={row['review_id_2']}")
        expert = expert[~missing].copy()

    # Unsure labels (NaN) → 0, which never matches model prediction (1 or 2)
    unsure = expert["Expert Label:"].isna()
    if unsure.any() and verbose:
        print(f"  Note: {unsure.sum()} pair(s) marked unsure — counted as incorrect.")
    expert["Expert Label:"] = expert["Expert Label:"].fillna(0)
    expert["unsure"] = unsure

    return expert


def load_and_merge(
    attuned_path=ATTUNED_RATINGS,
    expert_path=EXPERT_LABELS_PATH,
) -> pd.DataFrame:
    return merge_expert_deltas(pd.read_csv(attuned_path), expert_path)


# ==============================================================================
# PREDICTION & SCORING
# ==============================================================================

def score_predictions(expert: pd.DataFrame) -> pd.DataFrame:
    """
    Model predicts the review with the SMALLER absolute delta is more valid
    (less adjustment needed → less construct-irrelevant content).
    """
    expert["abs_delta_1"] = expert["delta_1"].abs()
    expert["abs_delta_2"] = expert["delta_2"].abs()
    expert["delta_diff"]  = (expert["abs_delta_1"] - expert["abs_delta_2"]).abs()
    
    expert["model_pred"]    = np.where(expert["abs_delta_1"] <= expert["abs_delta_2"], 1, 2)
    expert["expert_label"]  = expert["Expert Label:"].astype(int)
    expert["correct"]       = expert["model_pred"] == expert["expert_label"]

    return expert


# ==============================================================================
# REPORTING
# ==============================================================================

def _accuracy_report(df: pd.DataFrame, label: str) -> None:
    n         = len(df)
    n_unsure  = df["unsure"].sum()
    correct   = df["correct"].sum()
    acc       = correct / n if n > 0 else float("nan")

    p_value = float("nan")
    if n > 0:
        p_value = stats.binomtest(correct, n, p=0.5, alternative="greater").pvalue

    print(f"  {'─' * 48}")
    print(f"  {label}")
    print(f"  {'─' * 48}")
    print(f"  Pairs evaluated : {n}  ({n_unsure} unsure → incorrect)")
    print(f"  Correct         : {correct}")
    print(f"  Accuracy        : {acc:.1%}")
    print(f"  Binomial p-value (vs. chance = 0.5): {p_value:.7f}")
    print()
    

def report(expert: pd.DataFrame) -> None:
    # Half-open fine bin so the two conditions partition the pairs rather than
    # leaving a gap between FINE_DELTA_MAX and COARSE_DELTA_THRESHOLD.
    coarse_mask = expert["delta_diff"] >= COARSE_DELTA_THRESHOLD
    fine_mask   = expert["delta_diff"].between(
        FINE_DELTA_MIN, FINE_DELTA_MAX, inclusive="left"
    )

    print("\n" + "=" * 52)
    print("  EXPERT VALIDATION RESULTS")
    print("=" * 52 + "\n")
    _accuracy_report(expert,               "Overall")
    _accuracy_report(expert[coarse_mask],  f"Coarse  (Difference in |Δ| ≥ {COARSE_DELTA_THRESHOLD})")
    _accuracy_report(expert[fine_mask],    f"Fine    ({FINE_DELTA_MIN} ≤ Difference in |Δ| < {FINE_DELTA_MAX})")
    print(f"  Bins partition the pairs: "
          f"{int(coarse_mask.sum()) + int(fine_mask.sum())} of {len(expert)} assigned.")


# ==============================================================================
# ENTRY POINT
# ==============================================================================

def run() -> None:
    print("\n=== Stage 6: Validation ===")

    expert = load_and_merge()
    expert = score_predictions(expert)
    report(expert)


if __name__ == "__main__":
    run()
