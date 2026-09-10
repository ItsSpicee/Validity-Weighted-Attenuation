"""Create an exploratory audit of attenuation-only and density-only expert-pair successes.

The output contains the six discordant pairs from the shared 77-pair expert
evaluation: three won only by attenuation and three won only by density. It
keeps the displayed pair orientation, joins both reviews' text, topic clauses,
density, signed and absolute model responses, and miscellaneous-affect
summaries. Empty coding columns support qualitative inspection; this script
does not infer a cause of any divergence.

Run from the project root:
    python expert_method_divergence_audit.py
    python expert_method_divergence_audit.py --output my_audit.csv
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from constants import ATTUNED_RATINGS, NEG_EMOTIONS, POS_EMOTIONS
from d_misc_expert_baseline import prepare_pairs


ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT = ROOT / "expert_method_divergence_audit.csv"
REVIEWS = ROOT / "data" / "processed" / "reviews_cleaned.csv"
TOPICS = ROOT / "data" / "processed" / "ATExtracted_reviews.csv"
EMOTIONS = ROOT / "data" / "processed" / "final_emotions.csv"


def miscellaneous_emotion_summaries(emotions: pd.DataFrame) -> pd.DataFrame:
    """Return compact affect summaries rather than 28 individual probabilities."""
    output = emotions[["review_id"]].copy()
    for name, labels in (("misc_positive", POS_EMOTIONS), ("misc_negative", NEG_EMOTIONS)):
        columns = [f"{label}_misc" for label in labels if f"{label}_misc" in emotions]
        output[name] = emotions[columns].sum(axis=1) if columns else 0.0
    output["misc_affect_total"] = output.misc_positive + output.misc_negative
    return output


def review_metadata(ratings: pd.DataFrame) -> pd.DataFrame:
    """Assemble review-level evidence needed for qualitative pair inspection."""
    base = ratings[["review_id", "prof_ID", "rating", "original_pred", "weighted_pred",
                    "weighting_delta", "misc_d", "misc_pos_intensity", "misc_neg_intensity",
                    "total_misc_intensity", "is_heldout"]].copy()
    text = pd.read_csv(REVIEWS)[["review_id", "review"]]
    topics = pd.read_csv(TOPICS)[["review_id", "instructional_effectiveness", "fairness", "workload", "misc"]]
    emotions = miscellaneous_emotion_summaries(pd.read_csv(EMOTIONS))
    return (base.merge(text, on="review_id", how="left", validate="one_to_one")
                .merge(topics, on="review_id", how="left", validate="one_to_one")
                .merge(emotions, on="review_id", how="left", validate="one_to_one"))


def attach_reviews(pairs: pd.DataFrame, metadata: pd.DataFrame) -> pd.DataFrame:
    """Attach both displayed reviews while making their columns self-describing."""
    output = pairs.copy()
    for number in (1, 2):
        renamed = metadata.rename(columns={column: f"review_{number}_{column}"
                                           for column in metadata.columns if column != "review_id"})
        output = output.merge(renamed, left_on=f"review_id_{number}", right_on="review_id",
                              how="left", validate="many_to_one").drop(columns="review_id")
    return output


def build_audit(ratings: pd.DataFrame) -> pd.DataFrame:
    pairs = prepare_pairs(ratings)
    common = pairs.loc[pairs.common_evaluable].copy()
    attenuation_ok = common.correct.fillna(False).astype(bool)
    density_ok = common.density_correct.fillna(False).astype(bool)
    common["divergence_method"] = np.select(
        [attenuation_ok & ~density_ok, density_ok & ~attenuation_ok],
        ["attenuation_only", "density_only"], default="none",
    )
    divergent = common.loc[common.divergence_method.ne("none")].copy()
    divergent = attach_reviews(divergent, review_metadata(ratings))
    divergent["abs_delta_gap"] = divergent.abs_delta_1 - divergent.abs_delta_2
    divergent["density_gap"] = divergent.density_1 - divergent.density_2
    divergent["methods_select_different_reviews"] = divergent.model_pred.ne(divergent.density_pred)
    divergent["expert_selected_review_id"] = np.where(
        divergent.consensus_label.eq(1), divergent.review_id_1, divergent.review_id_2
    )
    divergent["experimental_hypothesis"] = ""
    divergent["inspection_notes"] = ""
    divergent["upstream_classification_concern"] = ""

    front = ["divergence_method", "condition", "review_id_1", "review_id_2",
             "consensus_label", "expert_selected_review_id", "model_pred", "density_pred",
             "abs_delta_1", "abs_delta_2", "abs_delta_gap", "density_1", "density_2",
             "density_gap", "methods_select_different_reviews", "experimental_hypothesis",
             "inspection_notes", "upstream_classification_concern"]
    remaining = [column for column in divergent.columns if column not in front]
    return divergent[front + remaining].sort_values(["divergence_method", "condition", "review_id_1"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ratings", type=Path, default=ATTUNED_RATINGS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                        help="Pair-level CSV to create; refuses to overwrite")
    args = parser.parse_args()
    audit = build_audit(pd.read_csv(args.ratings))
    counts = audit.divergence_method.value_counts()
    print(f"Attenuation-only pairs: {counts.get('attenuation_only', 0)}")
    print(f"Density-only pairs: {counts.get('density_only', 0)}")
    audit.to_csv(args.output, index=False, mode="x")
    print(f"Saved exploratory audit: {args.output}")


if __name__ == "__main__":
    main()
