"""Export the shared multi-expert accuracy and 95% Wilson intervals."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.validation import accuracy_summary, load_and_merge, score_predictions, wilson_interval

OUT_DIR = Path(__file__).resolve().parent / "output"


def main():
    table = accuracy_summary(score_predictions(load_and_merge()))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUT_DIR / "expert_confidence_intervals.csv", index=False)
    table.to_latex(OUT_DIR / "expert_confidence_intervals.tex", index=False, float_format="%.4f")
    print(table.to_string(index=False, float_format=lambda x: f"{x:.6g}"))


if __name__ == "__main__":
    main()
