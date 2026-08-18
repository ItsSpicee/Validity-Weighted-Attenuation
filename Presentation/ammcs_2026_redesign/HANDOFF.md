# AMMCS 2026 presentation redesign handoff

Updated: 2026-08-16 (America/Toronto)

## Objective

Redesign the latest 65-slide source presentation for AMMCS 2026, special session “Mathematical Foundations, Reasoning, and Applications of Large Language Models.” The work is design-only: preserve slide count, order, lexical content, values, citations, equations, supplied figures, and speaker notes. Editorial corrections to capitalization, spacing, apostrophes, quotation marks, hyphenation, and punctuation are explicitly allowed and expected.

Source deck:

`Presentation/AMMCS PREZZY (simplified) v2.pptx`

Working project:

`Presentation/ammcs_2026_redesign/`

## Non-negotiable user directions

- Keep exactly 65 slides and preserve all existing content and notes.
- Do not add wording unless required for the explicitly approved editorial corrections.
- Never use the prohibited term represented in code as `"counter" + "factual"`. It is intentionally not written contiguously here. `build_locked_spec.py` already replaces its two occurrences in speaker notes with “comparison.”
- The work is not to be described using that prohibited term.
- Use Greek `ζ`, never the spelled-out name or mojibake.
- Use proper capitalization and punctuation throughout.
- Preserve the established fonts. Recurring slide families must not switch typefaces from slide to slide.
- Generate and review ten slides at a time.
- The deck must remain image-based and must ultimately be exportable as slide PNGs.

## Approved design system

Name: Lighter Dusk Mathematical Editorial.

- Medium-deep slate-indigo backgrounds (`#18233F` to `#24345A`), not near-black.
- Warm off-white text.
- Laurier purple, AMMCS blue/green, and restrained warm gold accents.
- Subtle gradients, fine grids/curves, translucent blue-slate panels, softened glows.
- Academic-journal meets scientific-conference aesthetic; no cyberpunk or generic AI imagery.
- Modern sans-serif: titles, headings, labels, structural prose.
- Editorial serif: quotations and literature paraphrases.
- Mathematical serif: equations and notation.
- Stable typography references:
  - slide 9: editorial serif literature body and sans-serif attribution;
  - slide 15: general sans-serif system;
  - slide 31: mathematical typography and approved overall style.

Approved sample:

`origin_image/slide_31.png`

Selected backend: built-in `image_gen` image tool. Do not create final slide art with Pillow, SVG/HTML/canvas screenshots, native PowerPoint drawing, or manually composited text overlays.

## Completed and approved work state

- Slides 1–20: generated and recorded; previously reviewed.
- Slides 21–30: generated and recorded; pending user review.
- Slide 31: approved sample/accepted.
- Slides 32–41: generated and recorded; pending user review.
- Slides 42–51: generated and recorded; pending user review.
- Slides 52–61: generated and recorded; pending user review.
- Slides 62–65: generated and recorded; pending user review.
- Current run status: `slides_recorded`.
- Maximum concurrent slide workers: 3.

Review sheets:

- `review_batch_01_slides_01-10.png`
- `review_batch_02_slides_11-20.png`
- `review_batch_03_slides_21-30.png`
- `review_range_slides_21-31.png` (includes accepted slide 31 for sequence context)
- `review_batch_04_slides_32-41.png`
- `review_batch_05_slides_42-51.png`
- `review_batch_06_slides_52-61.png`
- `review_batch_07_slides_62-65.png`

Important completed corrections:

- Slide 1 title: `Towards VWA of Affective Noise in SET` (VWA has no periods).
- Slide 1 corpus source/unit: one bubble formatted as star icon, `RateMyProfessors Reviews`, review icon.
- Slide 13 order: Cronbach, Huber, Marsh & Roche.
- Slide 30 was regenerated from the revised native table in `AMMCS PREZZY (simplified) v2.pptx`; the full title is `Other non-CatBoost Options`, all revised values are preserved, and `CatBoost` is one unbroken word on one line.
- Slide 13 Huber text: `Huber (1964) — Down-weighting over deletion for stability.`
- Slide 1 subtitle: `An interpretable ABSA framework that adjusts SET ratings by down-weighting construct-irrelevant emotion.`
- Slides 7–10 use a consistent editorial-serif body and sans-serif attribution system.
- Slides 8–10 are paraphrases, not direct quotations.
- On slide 8, quotation marks remain only around “White noise.”
- Slides 9 and 10 have no quotation marks around the paraphrases.
- Slide 12 has consistent punctuation on all explanatory points; its three column headings remain unpunctuated.
- Slide 12 ends `Who decides what’s “bad”?` with a question mark.
- Slide 13 post-dash statements begin `Deletion`, `Reduce`, and `Don’t`.
- Slide 58 uses terminal periods consistently on all six limitation statements.
- Slide 60 capitalizes the first word of all five workflow steps consistently.
- Slide 65 uses the supplied white-background AMMCS logo alongside the Laurier logo.

## Policy scripts added/updated

`build_locked_spec.py` now permanently includes:

- explicit permission and rules for editorial punctuation/capitalization corrections;
- consistent typography policy by semantic role and recurring slide family;
- updated content-lock wording that distinguishes lexical preservation from editorial mechanics.

`refresh_pending_prompt_policies.py` applies those policies to the current `deck_spec.json` and every pending prompt without resetting completed slide state.

It has already been run. All 44 pending prompts (slides 21–65 except accepted slide 31) were validated to contain both editorial and typography policies.

If the policies are changed later, rerun:

```powershell
$py = 'C:\Users\Amer\.codex-ppt-skill\.venv\Scripts\python.exe'
& $py 'Presentation\ammcs_2026_redesign\refresh_pending_prompt_policies.py'
```

## Resume workflow tomorrow

1. Read the full codex-ppt skill and required references before acting.
2. Check state:

```powershell
$py = 'C:\Users\Amer\.codex-ppt-skill\.venv\Scripts\python.exe'
& $py 'C:\Users\Amer\.codex\skills\codex-ppt\scripts\slide_job_status.py' 'Presentation\ammcs_2026_redesign'
```

3. After slides 62–65 are approved, assemble the final 65-slide PPTX with the existing speaker notes. Slide 31 is already accepted and must not be regenerated.
4. Use one slide worker per slide, with at most three concurrent workers.
5. The installed skill does not contain `acquire_slide_job.py`. Use the supported `record_slide_dispatch.py` and `record_slide_result.py` scripts.
6. Each worker must:
   - read its entire prompt JSON as UTF-8;
   - inspect `origin_image/slide_31.png` and the role-appropriate typography reference;
   - inspect every strict local asset before generation;
   - use built-in `image_gen`;
   - verify exact content, proper punctuation/capitalization, font continuity, no added text, and no prohibited terminology;
   - return `backend_used`, `selected_source`, and `qa_note`;
   - record the accepted result.
7. Inspect each recorded PNG at original resolution.
8. After final approval, assemble, render, and inspect the complete 65-slide deck before delivery.

## Job-state caution

During slides 18–20, a transient image backend error left job ownership mismatched. It was resolved, and slides 18–20 are recorded. Avoid calling `record_slide_blocker.py` merely to release a transient failed dispatch because it marks the whole run blocked. If a worker fails before producing a result, reconcile the individual job’s dispatch cleanly before reassigning. Never record another worker’s output under a false agent identity.

## Key project files

- `outline.md`: locked 65-slide content map.
- `deck_spec.json`: current deck specification.
- `speech.md`: extracted speaker notes with prohibited terminology removed.
- `prompts/slide_01.json` through `prompts/slide_65.json`: slide prompts.
- `slide_jobs.json`: authoritative per-slide job state.
- `slide_run_state.json`: current run state.
- `origin_image/`: accepted slide PNGs.
- `assets/figures/`: strict source figures.
- `assets/logos/`: supplied Laurier and AMMCS logos.

## Final assembly requirements

After every batch is approved:

- assemble exactly 65 image-based slides in source order;
- preserve and reattach all speaker notes;
- verify no slide/content/notes were lost;
- export/render all slides to PNG and visually inspect the result;
- deliver the final PPTX plus rendered PNG set/contact sheet.
