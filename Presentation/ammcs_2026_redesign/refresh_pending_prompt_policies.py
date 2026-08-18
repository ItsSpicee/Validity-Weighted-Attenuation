from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FIRST_PENDING_SLIDE = 21
LAST_SLIDE = 65
SKIP_SLIDES = {31}

OLD_CONTENT_LOCK = (
    "All source wording, values, citations, equations, figures, slide order, and speaker notes are fixed. Design only."
)
NEW_CONTENT_LOCK = (
    "All lexical content, values, citations, equations, figures, slide order, and speaker notes are fixed. "
    "Design only; editorial punctuation and capitalization corrections are allowed."
)
OLD_LOCAL_CONTEXT = (
    "This is a design-only transformation. The source slide order, wording, values, images, and meaning are locked."
)
NEW_LOCAL_CONTEXT = (
    "This is a design-only transformation. The source slide order, wording, values, images, and meaning are "
    "locked; editorial punctuation and capitalization corrections are allowed."
)
OLD_TYPOGRAPHY = (
    "crisp modern sans-serif for prose and elegant mathematical serif notation; large projection-safe hierarchy"
)
TYPOGRAPHY_POLICY = (
    "Use the established deck type system consistently: crisp modern sans-serif for titles, headings, labels, "
    "and structural prose; elegant editorial serif for quotations and literature paraphrases; and mathematical "
    "serif for notation. Preserve the same typeface assignment, weight, case, and attribution styling within "
    "recurring slide families. Do not introduce a new display font on an individual slide. Use slides 9, 15, "
    "and 31 as the stable editorial-serif, general-sans, and mathematical typography references, respectively."
)
OLD_DECK_CONSISTENCY = (
    "match the approved slide 31 palette, typography mood, texture, and polish while varying layout by slide role"
)
NEW_DECK_CONSISTENCY = (
    "Match the approved slide 31 palette, texture, and polish while varying layout by slide role. Preserve the "
    "established typeface assignment across recurring slide families."
)
OLD_PRESERVATION_CONSTRAINT = (
    "Preserve the source slide content exactly; do not add, remove, paraphrase, summarize, correct, or reorder wording."
)
NEW_PRESERVATION_CONSTRAINT = (
    "Preserve the source slide's lexical content and meaning; do not add, remove, paraphrase, summarize, or reorder wording."
)
EDITORIAL_POLICY = (
    "Preserve every word, number, citation, equation, and claim. Editorial corrections to capitalization, spacing, "
    "apostrophes, quotation marks, hyphenation, and terminal punctuation are explicitly allowed. Treat headings "
    "and short labels as fragments without terminal periods; treat prose statements as sentences that begin with "
    "a capital and end with appropriate punctuation."
)


def update_prompt_text(text: str) -> str:
    replacements = {
        OLD_CONTENT_LOCK: NEW_CONTENT_LOCK,
        OLD_LOCAL_CONTEXT: NEW_LOCAL_CONTEXT,
        OLD_TYPOGRAPHY: TYPOGRAPHY_POLICY,
        OLD_DECK_CONSISTENCY: NEW_DECK_CONSISTENCY,
        OLD_PRESERVATION_CONSTRAINT: NEW_PRESERVATION_CONSTRAINT,
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    marker = f'  "{NEW_PRESERVATION_CONSTRAINT}",\n'
    additions = f'  "{EDITORIAL_POLICY}",\n  "{TYPOGRAPHY_POLICY}",\n'
    if EDITORIAL_POLICY not in text:
        if marker not in text:
            raise ValueError("Could not locate the preservation constraint in prompt text")
        text = text.replace(marker, marker + additions, 1)
    return text


def update_deck_spec() -> None:
    path = ROOT / "deck_spec.json"
    spec = json.loads(path.read_text(encoding="utf-8"))
    spec["deck_context"]["content_lock"] = NEW_CONTENT_LOCK
    spec["deck_context"]["editorial_policy"] = EDITORIAL_POLICY
    spec["deck_context"]["typography_policy"] = TYPOGRAPHY_POLICY
    spec["style"]["typography"] = TYPOGRAPHY_POLICY
    spec["style"]["deck_consistency"] = NEW_DECK_CONSISTENCY

    for slide in spec["slides"]:
        if not (FIRST_PENDING_SLIDE <= slide["number"] <= LAST_SLIDE) or slide["number"] in SKIP_SLIDES:
            continue
        slide["local_context"]["required_background"] = NEW_LOCAL_CONTEXT
        constraints = slide["constraints"]
        constraints[:] = [
            NEW_PRESERVATION_CONSTRAINT if value == OLD_PRESERVATION_CONSTRAINT else value
            for value in constraints
        ]
        insert_at = constraints.index(NEW_PRESERVATION_CONSTRAINT) + 1
        for policy in reversed((EDITORIAL_POLICY, TYPOGRAPHY_POLICY)):
            if policy not in constraints:
                constraints.insert(insert_at, policy)

    path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_pending_prompts() -> int:
    updated = 0
    for number in range(FIRST_PENDING_SLIDE, LAST_SLIDE + 1):
        if number in SKIP_SLIDES:
            continue
        path = ROOT / "prompts" / f"slide_{number:02}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["prompt"] = update_prompt_text(data["prompt"])
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        updated += 1
    return updated


def main() -> None:
    update_deck_spec()
    count = update_pending_prompts()
    print(f"updated deck_spec.json and {count} pending slide prompts")


if __name__ == "__main__":
    main()
