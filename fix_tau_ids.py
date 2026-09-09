"""Refine approximate tau-development review IDs from nearby full review text."""

from difflib import SequenceMatcher
import re
import unicodedata
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
TAU = ROOT / "sidequestz" / "tau-selection.csv"
REVIEWS = ROOT / "data" / "processed" / "reviews_cleaned.csv"
SCORE = re.compile(r"\s*\[\s*-?\d+(?:\.\d+)?\s*,\s*-?\d+(?:\.\d+)?\s*,\s*-?\d+(?:\.\d+)?\s*\]\s*$")


def key(value):
    value = SCORE.sub("", str(value))
    value = unicodedata.normalize("NFKC", value).replace("’", "'").lower()
    return re.sub(r"[^\w]+", "", value)


def main():
    tau = pd.read_csv(TAU)
    reviews = pd.read_csv(REVIEWS)
    tau["_clause"] = tau.clause_with_score.map(key)
    source = tau.groupby("review_id", sort=False)._clause.agg("".join).to_dict()
    targets = dict(zip(reviews.review_id.astype(int), reviews.review.map(key)))
    replacements = {}
    diagnostics = []
    for approximate_id, content in source.items():
        candidates = [(target_id, text) for target_id, text in targets.items()
                      if int(approximate_id) - 10 <= target_id <= int(approximate_id) + 10]
        exact = [target_id for target_id, text in candidates if text == content]
        scored = sorted(((target_id, SequenceMatcher(None, content, text).ratio())
                         for target_id, text in candidates), key=lambda item: item[1], reverse=True)
        best_id, best_score = scored[0]
        next_score = scored[1][1]
        if len(exact) == 1:
            replacements[approximate_id] = exact[0]
            diagnostics.append((approximate_id, exact[0], "exact", 1.0, 0.0))
        elif best_score >= 0.92 and best_score - next_score >= 0.05:
            replacements[approximate_id] = best_id
            diagnostics.append((approximate_id, best_id, "similarity", best_score, next_score))
        else:
            diagnostics.append((approximate_id, pd.NA, "unresolved", best_score, next_score))
    unresolved = [row for row in diagnostics if row[2] == "unresolved"]
    if unresolved:
        print(pd.DataFrame(
            unresolved,
            columns=["approximate_id", "current_id", "method", "score", "runner_up"],
        ).to_string(index=False))
        raise ValueError(f"Refusing to rewrite: {len(unresolved)} IDs are not uniquely resolved")
    tau.review_id = tau.review_id.map(replacements)
    tau.drop(columns="_clause").to_csv(TAU, index=False)
    print(f"Rewrote {len(replacements)} tau-development review IDs.")
    print(pd.DataFrame(diagnostics, columns=["approximate_id", "current_id", "method", "score", "runner_up"]).to_string(index=False))


if __name__ == "__main__":
    main()
