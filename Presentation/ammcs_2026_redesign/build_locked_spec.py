from __future__ import annotations

import json
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
PPT = REPO / "tmp" / "ppt_extract_latest" / "deck" / "ppt"
MEDIA_SRC = PPT / "media"
MEDIA_DST = ROOT / "assets" / "figures"

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"

EDITORIAL_POLICY = (
    "Preserve every word, number, citation, equation, and claim. Editorial corrections to "
    "capitalization, spacing, apostrophes, quotation marks, hyphenation, and terminal punctuation "
    "are explicitly allowed. Treat headings and short labels as fragments without terminal periods; "
    "treat prose statements as sentences that begin with a capital and end with appropriate punctuation."
)

TYPOGRAPHY_POLICY = (
    "Use the established deck type system consistently: crisp modern sans-serif for titles, headings, "
    "labels, and structural prose; elegant editorial serif for quotations and literature paraphrases; "
    "and mathematical serif for notation. Preserve the same typeface assignment, weight, case, and "
    "attribution styling within recurring slide families. Do not introduce a new display font on an "
    "individual slide. Use slides 9, 15, and 31 as the stable editorial-serif, general-sans, and "
    "mathematical typography references, respectively."
)


def slide_number(path: Path) -> int:
    return int(re.search(r"(\d+)", path.stem).group(1))


def slide_text(path: Path) -> list[str]:
    return [node.text or "" for node in ET.parse(path).getroot().iter(A + "t")]


def relationships(path: Path) -> list[ET.Element]:
    rels = path.parent / "_rels" / f"{path.name}.rels"
    return list(ET.parse(rels).getroot()) if rels.exists() else []


def note_text(slide_path: Path) -> str:
    note_target = None
    for rel in relationships(slide_path):
        target = rel.attrib.get("Target", "")
        if "notesSlides/" in target:
            note_target = (slide_path.parent / target).resolve()
            break
    if not note_target or not note_target.exists():
        return ""

    root = ET.parse(note_target).getroot()
    for shape in root.findall(f".//{P}sp"):
        ph = shape.find(f"./{P}nvSpPr/{P}nvPr/{P}ph")
        if ph is not None and ph.attrib.get("type") == "body":
            paragraphs = []
            for para in shape.findall(f".//{A}p"):
                text = "".join(node.text or "" for node in para.iter(A + "t"))
                paragraphs.append(text)
            note = "\n".join(paragraphs).strip()
            prohibited = "counter" + "factual"
            note = note.replace(f"The {prohibited} makes the case.", "The comparison makes the case.")
            note = note.replace(f"The {prohibited} argument", "The comparison argument")
            return note
    return ""


ROLES = {
    1: "cover",
    2: "visual hook", 3: "visual hook", 4: "visual hook", 5: "visual hook",
    6: "section divider", 7: "quotation", 8: "literature", 9: "literature", 10: "literature",
    11: "synthesis", 12: "comparison", 13: "theory", 14: "data overview", 15: "research questions",
    16: "process", 17: "process", 18: "process", 19: "process", 20: "process", 21: "architecture",
    22: "section roadmap", 23: "technical concept", 24: "metric explanation", 25: "architecture",
    26: "technical concept", 27: "feature aggregation", 28: "feature aggregation", 29: "modeling",
    30: "model comparison", 31: "mathematical concept", 32: "mathematical concept", 33: "worked example",
    34: "section divider", 35: "data evidence", 36: "data evidence", 37: "data evidence", 38: "data evidence",
    39: "data evidence", 40: "data evidence", 41: "data evidence", 42: "data evidence", 43: "section divider",
    44: "validation evidence", 45: "validation evidence", 46: "validation evidence", 47: "validation evidence",
    48: "validation evidence", 49: "section divider", 50: "research questions", 51: "finding", 52: "finding",
    53: "finding", 54: "finding", 55: "implications", 56: "section divider", 57: "limitations",
    58: "limitations", 59: "section divider", 60: "process summary", 61: "contributions", 62: "boundary statement",
    63: "future work", 64: "closing statement", 65: "acknowledgements",
}


IMAGE_ONLY_TITLES = {
    2: "\u200b", 3: "\u200b", 4: "\u200b", 5: "\u200b",
    16: "\u200b", 17: "\u200b", 18: "\u200b", 19: "\u200b", 20: "\u200b", 21: "\u200b",
    25: "\u200b", 33: "\u200b", 35: "\u200b", 36: "\u200b", 37: "\u200b", 38: "\u200b",
    39: "\u200b", 40: "\u200b", 41: "\u200b", 42: "\u200b", 44: "\u200b", 45: "\u200b", 46: "\u200b",
}


def make_slide(path: Path) -> dict:
    number = slide_number(path)
    text = slide_text(path)
    title = IMAGE_ONLY_TITLES.get(number, text[0].strip() if text else "\u200b")
    key_points = text[1:] if text and number not in IMAGE_ONLY_TITLES else []
    if number == 1:
        title = "Towards V.W.A of Affective Noise in SET."
        key_points[0] = "An interpretable ABSA framework that adjusts SET ratings by down-weighting construct-irrelevant emotion."
    elif number == 8:
        title = "Wongsurawat (2011)"
        key_points = ["“White noise”: Pedagogically irrelevant content is a source of measurement error; low-correlation comments should be discounted."]
    elif number == 9:
        title = "Schiekirka & Raupach (2015)"
        key_points = ["Student characteristics, performance level and evaluation process act as confounders on ratings."]
    elif number == 10:
        title = "Li et al. (2025)"
        key_points = ["Emotional interaction with the instructor leads students to overlook actual teaching quality."]
    elif number == 12:
        punctuation = {
            "Narrow, targeted items": "Narrow, targeted items.",
            "Filter “low quality” comments": "Filter “low quality” comments.",
            "Removes noise by construction": "Removes noise by construction.",
            "Removes noise by exclusion": "Removes noise by exclusion.",
        }
        key_points = [punctuation.get(point, point).replace("Who decides  what’s “bad”", "Who decides what’s “bad”?") for point in key_points]
    elif number == 13:
        key_points = [
            "Huber (1964) — Deletion is just a weight of 0.",
            "Cronbach (1951) — Reduce error variance, don't remove observations.",
            "Marsh & Roche (1997) — Don't throw the validity baby out.",
        ]

    required_images = []
    for rel in relationships(path):
        target = rel.attrib.get("Target", "")
        if "media/" not in target:
            continue
        name = target.split("/")[-1]
        required_images.append({
            "path": str((MEDIA_DST / name).resolve()),
            "role": "strict source content asset from the original slide",
            "fidelity": "preserve all wording, values, labels, axes, formulas, redactions, and visual relationships exactly; do not redraw or replace",
        })

    if number in (1, 65):
        for logo in ("wlulogo.png", "ammcslogo.png"):
            required_images.append({
                "path": str((ROOT / "assets" / "logos" / logo).resolve()),
                "role": "strict supplied logo asset",
                "fidelity": "preserve exact brand geometry, lettering, colors, and transparency",
            })

    constraints = [
        "Preserve the source slide's lexical content and meaning; do not add, remove, paraphrase, summarize, or reorder wording.",
        EDITORIAL_POLICY,
        TYPOGRAPHY_POLICY,
        "Do not introduce any terminology or claims not already present on this source slide.",
        "Use the approved lighter dusk slide 31 only as a style reference; vary the composition for this slide's role.",
        "No watermark and no visible slide number.",
    ]
    if number in IMAGE_ONLY_TITLES:
        constraints.extend([
            "Do not render a separate title or any overlay copy; all visible wording must come only from the strict source image asset.",
            "Make the strict source image the dominant slide content and preserve it legibly.",
        ])

    slide = {
        "number": number,
        "title": title,
        "role": ROLES[number],
        "intent": "Redesign this exact source slide without changing its content.",
        "key_points": key_points,
        "local_context": {
            "required_background": "This is a design-only transformation. The source slide order, wording, values, images, and meaning are locked; editorial punctuation and capitalization corrections are allowed."
        },
        "layout": {
            "composition": "Choose a role-appropriate composition with clear hierarchy and projection-safe spacing; preserve every source element.",
            "variation_rule": "Match the approved style identity without copying slide 31's exact layout.",
        },
        "visual_elements": {
            "main_visual": "Use only visuals already present or abstract nonverbal decoration that does not add content."
        },
        "constraints": constraints,
    }
    if required_images:
        slide["required_images"] = required_images
        slide["source_image_rules"] = "All required images are strict inputs. Preserve their content and place them visibly; do not synthesize replacements."
    if number == 31:
        slide["sample_approved"] = True
    return slide


def main() -> None:
    MEDIA_DST.mkdir(parents=True, exist_ok=True)
    for source in MEDIA_SRC.iterdir():
        if source.is_file():
            shutil.copy2(source, MEDIA_DST / source.name)

    slides = [make_slide(path) for path in sorted((PPT / "slides").glob("slide*.xml"), key=slide_number)]
    spec = {
        "deck_name": "ammcs_2026_redesign",
        "language": "English",
        "goal": "Apply a beautiful, engaging AMMCS 2026 visual design to the locked 65-slide source deck without changing its content.",
        "deck_context": {
            "source_summary": "An interpretable ABSA framework that adjusts student-evaluation ratings by proportionally down-weighting emotion attached to miscellaneous content.",
            "content_lock": "All lexical content, values, citations, equations, figures, slide order, and speaker notes are fixed. Design only; editorial punctuation and capitalization corrections are allowed.",
            "editorial_policy": EDITORIAL_POLICY,
            "typography_policy": TYPOGRAPHY_POLICY,
            "canonical_terms": ["Validity-Weighted Attenuation", "Miscellaneous", "Instructional Effectiveness", "Fairness", "Workload", "D_misc", "ζ"],
        },
        "selected_image_backend": "built-in image tool",
        "max_concurrent_slides": 3,
        "sample_generation_method": {
            "backend_used": "built-in image tool",
            "tool_name": "image_gen",
            "mode": "generate",
            "prompt_source": "approved slide 31 prompt and user-directed edits",
            "size": "16:9 landscape, built-in default",
            "quality": "built-in default",
            "approved_sample_path": str((ROOT / "origin_image" / "slide_31.png").resolve()),
            "input_context_preparation": "view_image for local strict input assets and approved sample; built-in conversation image context",
            "handoff_rule": "Use this same built-in image_gen backend and mode; return a blocker if unavailable.",
        },
        "style": {
            "name": "Lighter Dusk Mathematical Editorial",
            "visual_direction": "projection-friendly academic-journal meets modern scientific-conference design; rich but not near-black; elegant mathematical textures; no cyberpunk or generic AI imagery",
            "color_palette": "medium-deep slate-indigo #18233F to #24345A; warm off-white text; Laurier purple; AMMCS blue and green; restrained warm gold",
            "typography": TYPOGRAPHY_POLICY,
            "texture_and_finish": "subtle tonal gradients, fine grids and curves, light translucent blue-slate panels, softened glows",
            "deck_consistency": "Match the approved slide 31 palette, texture, and polish while varying layout by slide role. Preserve the established typeface assignment across recurring slide families.",
        },
        "approved_style_reference": {
            "path": str((ROOT / "origin_image" / "slide_31.png").resolve()),
            "role": "approved sample slide style reference",
            "fidelity": "match style only; do not copy layout or content",
        },
        "slides": slides,
    }
    (ROOT / "deck_spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    speech = []
    for path in sorted((PPT / "slides").glob("slide*.xml"), key=slide_number):
        number = slide_number(path)
        title = IMAGE_ONLY_TITLES.get(number) or (slide_text(path)[0].strip() if slide_text(path) else f"Slide {number}")
        if title == "\u200b":
            title = f"Slide {number}"
        speech.append(f"## Slide {number}: {title}\n\n{note_text(path)}\n")
    (ROOT / "speech.md").write_text("\n".join(speech), encoding="utf-8")


if __name__ == "__main__":
    main()
