"""Mine the dataset for conference-slide review quotes.

The pitch: our framework says a lot of what students write has nothing to do
with teaching. Nothing sells that to an audience like reading the actual
reviews out loud. So we want reviews that are (a) heavily misc-dominant --
off-topic by the model's own accounting -- and (b) emotionally extreme or
stylistically unhinged, i.e. quotable rather than merely irrelevant.

    hook_score = misc_d ** misc_weight  *  (emotion_arousal + style_bonus)

Everything is filtered through a profanity / NSFW blocklist first, since these
go on a slide in front of a room.

Usage:
    python sidequestz/find_funny_reviews.py                    # top 25 hooks
    python sidequestz/find_funny_reviews.py --mode chaotic     # CAPS and !!!
    python sidequestz/find_funny_reviews.py --mode comedic     # amusement-led
    python sidequestz/find_funny_reviews.py --top 60 --min-misc-d 0.7
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUT_DIR = Path(__file__).resolve().parent / "output"

# emotion -> weight, all measured on the *_misc aspect. High weights go to the
# emotions that make an audience sit up; the bland evaluative ones (approval,
# realization, relief) are deliberately absent.
MODE_WEIGHTS = {
    # off-topic AND emotionally extreme -- the default slide material
    "hook": {
        "love": 1.00,
        "desire": 1.00,
        "grief": 0.90,
        "disgust": 0.85,
        "embarrassment": 0.80,
        "anger": 0.75,
        "surprise": 0.70,
        "amusement": 0.60,
        "excitement": 0.55,
        "fear": 0.55,
        "nervousness": 0.45,
        "sadness": 0.40,
        "pride": 0.35,
        "remorse": 0.35,
        "curiosity": 0.20,
    },
    # the original: student found the professor funny
    "comedic": {
        "amusement": 1.00,
        "surprise": 0.35,
        "embarrassment": 0.30,
        "excitement": 0.20,
        "curiosity": 0.10,
    },
    # emotion barely matters; let the writing style do the talking
    "chaotic": {
        "surprise": 0.30,
        "excitement": 0.30,
        "anger": 0.30,
        "love": 0.30,
    },
}

STYLE_BONUS = {"hook": 1.20, "comedic": 0.0, "chaotic": 2.0}

# Conservative: better to lose a good quote than to project something ugly.
# Note "profanity" is the literal placeholder token the cleaning step leaves
# behind, so its presence marks a review that was censored upstream.
BLOCKLIST = re.compile(
    r"\b(?:"
    r"profanity|"
    r"fuck\w*|shit\w*|bitch\w*|cunt\w*|whore|slut\w*|dick|cock|pussy|"
    r"tits|boobs|horny|sexy|sex\w*|rape|nigg\w+|fag\w*|retard\w*|"
    r"asshole|bastard|damn|hell|piss\w*|crap|ass|douche\w*|"
    r"hot|hottie|hotty|babe|cute|creep\w*|perv\w*|stalk\w*|"
    r"drunk|weed|stoned|drugs?|"
    r"kill|die|dead|suicide"
    r")\b",
    re.IGNORECASE,
)


def load(weights: dict[str, float]) -> pd.DataFrame:
    emo_cols = ["review_id", "misc_d"] + [f"{e}_misc" for e in weights]
    emo = pd.read_csv(PROCESSED / "weighted_emotions.csv", usecols=emo_cols)
    text = pd.read_csv(PROCESSED / "reviews_text_cleaned.csv")
    return emo.merge(text, on="review_id", how="inner")


def style_score(s: pd.Series) -> pd.Series:
    """Reward shouting, punctuation spam, and personal-anecdote framing."""
    txt = s.fillna("")
    letters = txt.str.count(r"[A-Za-z]").clip(lower=1)
    caps = txt.str.count(r"[A-Z]") / letters
    bangs = txt.str.count(r"[!?]").clip(upper=8) / 8
    ellipsis = txt.str.count(r"\.\.\.").clip(upper=3) / 3
    firstperson = txt.str.count(r"(?i)\b(i|my|me)\b").clip(upper=10) / 10
    return 0.45 * caps + 0.25 * bangs + 0.10 * ellipsis + 0.20 * firstperson


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mode", choices=list(MODE_WEIGHTS), default="hook")
    p.add_argument("--top", type=int, default=25)
    p.add_argument("--min-misc-d", type=float, default=0.6,
                   help="drop reviews whose misc dominance is below this")
    p.add_argument("--min-words", type=int, default=10)
    p.add_argument("--max-words", type=int, default=120,
                   help="anything longer won't fit on a slide")
    p.add_argument("--misc-weight", type=float, default=1.5,
                   help="exponent on misc_d; higher = leans harder off-topic")
    p.add_argument("--allow-profanity", action="store_true",
                   help="skip the blocklist (not for the slides)")
    p.add_argument("--out", type=str, default=None)
    args = p.parse_args()

    weights = MODE_WEIGHTS[args.mode]
    df = load(weights)
    n0 = len(df)

    df["arousal"] = sum(w * df[f"{e}_misc"] for e, w in weights.items())
    df["style"] = style_score(df["review"])
    df["hook_score"] = (df["misc_d"] ** args.misc_weight) * (
        df["arousal"] + STYLE_BONUS[args.mode] * df["style"]
    )

    df = df[df["misc_d"] >= args.min_misc_d]
    wc = df["review"].fillna("").str.split().str.len()
    df = df[(wc >= args.min_words) & (wc <= args.max_words)]
    n_clean = len(df)
    if not args.allow_profanity:
        df = df[~df["review"].fillna("").str.contains(BLOCKLIST)]

    df = df.sort_values("hook_score", ascending=False)

    out = Path(args.out or OUT_DIR / f"hook_reviews_{args.mode}.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    cols = ["review_id", "prof_ID", "rating", "misc_d", "arousal", "style",
            "hook_score", "review"]
    df[cols].to_csv(out, index=False)

    print(f"mode={args.mode}  {n0:,} reviews -> {n_clean:,} after "
          f"misc_d/length filters -> {len(df):,} after blocklist")
    print(f"full ranking written to {out}\n")

    for rank, (_, r) in enumerate(df.head(args.top).iterrows(), start=1):
        print(f"--- #{rank}  score={r.hook_score:.3f}  misc_d={r.misc_d:.2f}  "
              f"arousal={r.arousal:.2f}  style={r.style:.2f}  "
              f"rating={r.rating}  (id {int(r.review_id)})")
        print(f"{r.review}\n")


if __name__ == "__main__":
    main()
