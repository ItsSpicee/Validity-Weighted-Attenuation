"""Report review-ID overlap between the tau development and ATC validation sets.

Run from the project root:
    python tau_validation_id_overlap.py
"""

import argparse
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
DEFAULT_TAU = ROOT / "sidequestz" / "tau-selection.csv"
DEFAULT_VALIDATION = ROOT / "data" / "raw" / "atc_predictions.csv"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tau", type=Path, default=DEFAULT_TAU)
    parser.add_argument("--validation", type=Path, default=DEFAULT_VALIDATION)
    args = parser.parse_args()

    tau = pd.read_csv(args.tau)
    validation = pd.read_csv(args.validation)
    for frame, name in ((tau, "tau development"), (validation, "validation")):
        if "review_id" not in frame.columns:
            raise ValueError(f"{name} file has no review_id column")

    tau_ids = set(pd.to_numeric(tau.review_id, errors="raise").astype(int))
    validation_ids = set(pd.to_numeric(validation.review_id, errors="raise").astype(int))
    overlap = sorted(tau_ids & validation_ids)
    overlapping_clauses = validation.loc[validation.review_id.isin(tau_ids)]

    print(f"Tau development reviews: {len(tau_ids)}")
    print(f"Validation reviews: {len(validation_ids)}")
    print(f"Shared review IDs: {len(overlap)}")
    print(f"Validation clauses in shared reviews: {len(overlapping_clauses)}")
    print("Overlap IDs: " + (", ".join(map(str, overlap)) if overlap else "None"))


if __name__ == "__main__":
    main()
