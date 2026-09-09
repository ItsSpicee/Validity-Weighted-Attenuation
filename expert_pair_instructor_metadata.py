"""Describe instructor recurrence in the expert-review-pair evaluation.

Run from the project root:
    python expert_pair_instructor_metadata.py
    python expert_pair_instructor_metadata.py --pairs-output expert_pair_instructor_audit.csv

The primary report uses the same 77 model-evaluable pairs as ``src.validation``.
An instructor's pair count is the number of distinct pairs in which one of their
reviews appears; a pair with two reviews from the same instructor counts once.
"""

import argparse
from pathlib import Path

import pandas as pd

from constants import ATTUNED_RATINGS
from src.validation import PAIR_KEYS, merge_expert_deltas


def load_pair_instructors(ratings_path: Path) -> pd.DataFrame:
    """Attach instructor IDs to the shared expert-pair audit table."""
    ratings = pd.read_csv(ratings_path)
    required = {"review_id", "prof_ID", "weighting_delta"}
    missing = required.difference(ratings.columns)
    if missing:
        raise ValueError(f"{ratings_path} is missing required columns: {sorted(missing)}")
    if ratings.review_id.isna().any() or ratings.review_id.duplicated().any():
        raise ValueError("Ratings must have unique, nonmissing review IDs")
    if ratings.prof_ID.isna().any():
        raise ValueError("Ratings contains missing instructor IDs")

    pairs = merge_expert_deltas(ratings, verbose=False).copy()
    instructor_map = ratings.set_index("review_id").prof_ID
    for number in (1, 2):
        pairs[f"prof_ID_{number}"] = pairs[f"review_id_{number}"].map(instructor_map)
    pairs["missing_instructor"] = pairs[["prof_ID_1", "prof_ID_2"]].isna().any(axis=1)
    pairs["same_instructor"] = pairs.prof_ID_1.eq(pairs.prof_ID_2)
    return pairs


def instructor_recurrence(pairs: pd.DataFrame) -> pd.DataFrame:
    """Count unique evaluable pairs per instructor without double-counting pairs."""
    evaluable = pairs.loc[pairs.evaluable & ~pairs.missing_instructor].copy()
    left = evaluable[["review_id_1", "prof_ID_1"]].rename(
        columns={"review_id_1": "review_id", "prof_ID_1": "prof_ID"}
    )
    right = evaluable[["review_id_2", "prof_ID_2"]].rename(
        columns={"review_id_2": "review_id", "prof_ID_2": "prof_ID"}
    )
    appearances = pd.concat([left, right], ignore_index=True)
    pair_ids = evaluable.reset_index(names="pair_id")[["pair_id", *PAIR_KEYS]]
    long = pd.concat([
        pair_ids[["pair_id", "review_id_1"]].rename(columns={"review_id_1": "review_id"}),
        pair_ids[["pair_id", "review_id_2"]].rename(columns={"review_id_2": "review_id"}),
    ], ignore_index=True).merge(appearances.drop_duplicates("review_id"), on="review_id", validate="many_to_one")
    return (long.drop_duplicates(["pair_id", "prof_ID"])
                .groupby("prof_ID", as_index=False)
                .agg(n_pairs=("pair_id", "nunique"), n_reviews=("review_id", "nunique"))
                .sort_values(["n_pairs", "n_reviews", "prof_ID"], ascending=[False, False, True]))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ratings", type=Path, default=ATTUNED_RATINGS,
                        help="Attenuation CSV with review_id, prof_ID, and weighting_delta")
    parser.add_argument("--pairs-output", type=Path,
                        help="Optional pair-level audit CSV; refuses to overwrite")
    args = parser.parse_args()

    pairs = load_pair_instructors(args.ratings)
    recurrence = instructor_recurrence(pairs)
    evaluable = pairs.loc[pairs.evaluable & ~pairs.missing_instructor]
    counts = recurrence.n_pairs

    print(f"Pairs in expert label files: {len(pairs)}")
    print(f"Model-evaluable pairs with instructor metadata: {len(evaluable)}")
    print(f"Distinct instructors across evaluable pairs: {len(recurrence)}")
    print(f"Maximum pairs involving one instructor: {int(counts.max()) if len(counts) else 0}")
    print(f"Instructors appearing in more than one pair: {int((counts > 1).sum())}")
    print(f"Pairs whose two reviews share an instructor: {int(evaluable.same_instructor.sum())}")
    print("\nInstructor recurrence (instructors with more than one pair):")
    repeated = recurrence.loc[recurrence.n_pairs > 1]
    print(repeated.to_string(index=False) if len(repeated) else "None")

    if args.pairs_output:
        audit_columns = [*PAIR_KEYS, "prof_ID_1", "prof_ID_2", "same_instructor",
                         "evaluable", "missing_delta", "missing_instructor"]
        pairs[audit_columns].to_csv(args.pairs_output, index=False, mode="x")
        print(f"\nSaved pair audit: {args.pairs_output}")


if __name__ == "__main__":
    main()
