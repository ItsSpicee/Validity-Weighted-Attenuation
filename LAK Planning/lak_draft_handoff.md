# LAK27 Draft — Status (updated 2026-09-01)

> Last layout update: 2026-09-02.

## Build

```
cd "LAK Planning/LAK_draft"
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

## The one rule that governs this file

**Black body text is verbatim from the source manuscript. Red text is not.**

| Marker | Meaning |
|---|---|
| `\todo{...}` | red bold `[TODO: ...]` — action needed |
| `\new{...}` | red text — added or reworded |
| `\begin{newcontent}` | same, for multi-paragraph blocks |
| `\auth{...}` | authored text, styled blue — will convert to black at submission |

Current active counts: **4** `\todo`, **14** `\new`, **0** `\citeneeded`.

## Current page estimate

~17.75 pages (down from ~21 pre-cut). Target: 14 pages. Submission deadline: 2026-09-28 (26 days).

## Remaining TODOs

### Must-do before submission

1. **Multi-expert consensus** — §4.3.1 expert validation results need updating from single-expert to multi-expert consensus (majority vote, Fleiss' κ, Wilson intervals). Single-expert figures deliberately not transferred. **Blocks items 2–4 below.**
2. **Result-local evaluation protocols** — the standalone Evaluation Strategy subsection was deleted during the cut pass. Once consensus is implemented, add only the finalized expert-comparison procedure to §4.3.1 and the necessary permutation procedure to §4.3.2. Do not restore the obsolete single-expert wording. (Blocked by #1.)
3. **Limitations paragraph** — source manuscript's single-expert limitation paragraph not transferred; replace with multi-expert limits once results exist. (Blocked by #1.)
4. **Abstract expert placeholder** — abstract contains `\todo{[placeholder: multi-expert consensus results]}`. Fill once consensus is run. (Blocked by #1.)
5. **Funding statement** — check if required; currently a `\todo`.
6. **Strip all red text** — zero `\new`, `\todo` should remain at submission. All are drafting scaffolding.

### Next phase — reformatting and strategic omission

The prose-cut pass is complete: the paper has been compressed as far as is
useful without weakening its argument. Do not pursue further global prose
compression.

- Continue the layout pass from the current 17.75-page baseline. The ordinary
  floats have been re-enabled and reflowed; inspect each subsequent layout
  change against the page budget rather than assuming a local compression saves
  a physical page.
- Decision: retain the full Section 4.3 evidence in the compact three-panel
  Table 8(a--c), rather than moving those results to supplementary material.
- Regenerate the source images used in the SHAP/correlation two-panel figure with larger
  axis, tick, legend, and annotation fonts; the new side-by-side layout is
  space-efficient, but its labels need to remain readable at panel scale.
- Make deliberate, argument-preserving omissions where needed: retain the core
  validity mechanism and its direct evidence; move or omit secondary supporting
  material rather than thinning the protected responsible-use and non-use
  content.
- In particular, decide whether every §4.3 sensitivity table belongs in the
  main paper or whether selected detail should move to supplementary material.
- Reassess the final narrative order and visual hierarchy only after the
  reformatted layout makes the remaining page pressure visible.

## Cut phase — completed passes

**Guiding principles (agreed with author):**
- Highest priority: remove redundant, over-verbose, and low-impact content
- SHAP feature-importance shift and correlation changes are mechanistic coherence checks, not evidence — present proportionally (compact), not at same weight as modulator correlations/permutation control
- §5.2 Responsible Interpretation and §5.3 Non-Use are essential LAK positioning — protect these
- All citations must be accurately attributed to what they actually support
- Compress before deleting — prefer tightening prose over removing ideas

### Intro & Background cuts (2026-08-31)

- §1.1: Deleted Emery/Dowell standalone paragraph; absorbed citations into preceding paragraph
- §1.2: Cut five-stage pipeline enumeration after "17,127 RMP student evaluations" — pipeline detail deferred to Method
- §1.3: Deleted redundant first sentence of boundary paragraph; kept Misc ≠ unimportant and non-use statements with Tsai citation
- §2.1: Deleted Li2025 and Schiekirka standalone paragraphs; absorbed as parenthetical citations into closing synthesis sentence
- §2.2: Collapsed Kopciuszewska, Kim, Sorour, Louis/Xiong from four paragraphs to two sentences with all citations preserved
- §2.3: Cut Misc ≠ unimportant / audit trail / raw-ratings-preserved sentences (covered in §1.3 and §5.3); kept bounded+proportional property, stakeholder taxonomy (Lockyer sole home), changed "monotonic" to "proportional"
- §2.4: Deleted recap paragraph and pipeline re-enumeration; kept gap statement; absorbed Doshi-Velez, Drachsler, Gašević citations with accurate attribution

### Method cut pass (2026-08-31)

- Deleted the standalone Model Pipeline subsection; moved the schematic to the end of Study Context and Data
- Compressed Study Context and Data while retaining RMP provenance, no-scraping/permission account, exclusion rules, preprocessing rationale, and corpus statistics
- Merged Clause Extraction into Aspect-Term Categorization; consolidated the ATC decision rule into one equation
- Merged pedagogical density with emotion extraction
- Compressed emotion extraction, rating modelling, and validity-weighted attenuation subsections
- Deleted the standalone Evaluation Strategy subsection (procedural content to be reinstated beside corresponding results)

### Results & Discussion compression pass (2026-09-01)

- §3.1: Compressed cleaning paragraph from 4 sentences to 1; deleted distribution paragraph (rating skew covered in Results); deleted "ABSA is difficult" catalogue sentence
- §4.1.1 (ATC Topic Structure): Compressed intro, clause-density, co-occurrence, low-rating, D_misc, and summary paragraphs — all ideas retained in ~half the words
- §4.1.2 (Sentiment Extraction): Compressed from 6 sentences to 3; retained nuanced/multi-dimensional conclusion
- §4.1.3 (ATC Validation): Compressed LLM inter-rater from 4 sentences to 1; expert validation from 8 sentences to 3; closing reframed as proof-of-concept acknowledgement of accuracy limitations; expert experience updated to 15 years
- §4.1.4 (Rating Regression): Compressed opening from 5 sentences to 2; SHAP paragraphs from 8 sentences to 3; retained low-intensity inversion finding
- §4.2 intro: Compressed from 3 sentences to 1
- §4.2.1 (Adjustment Outcomes): Compressed stats + Wilcoxon from 7 sentences to 3; closing from 4 sentences to 1
- §4.2.2 (Feature Importance): Compressed from 5 sentences to 2; figure retained
- §4.2.3 (Correlation Changes): Compressed opening from 7 sentences to 2; post-figure from 4 sentences to 1; figure caption compressed
- §4.2.4 (Modulator Correlations): Compressed intro from 3 sentences to 1; post-table + Mann-Whitney + closing from 10 sentences to 4
- §5.1 (Discussion): Compressed RQ1 discussion from 6 paragraphs to 6 short paragraphs (~half word count); compressed RQ2 from 3 paragraphs to 3 short paragraphs; merged positioning + interpretability paragraphs into one with LA-trace framing, Doshi-Velez/Drachsler/Gašević citations advancing from intro usage

### Final limitation compression (2026-09-01)

- §6: Consolidated the overlapping final limitations material. The remaining
  multi-expert limitation is intentionally deferred until consensus results are
  available; no further prose compression is planned.

### Layout and evidence pass (2026-09-02)

- Added the one-star emotion heatmap to Sentiment Extraction and the SHAP
  beeswarm to Rating Regression Performance; both are now intended main-paper
  evidence, not supplementary candidates.
- Combined SHAP feature-importance change and correlation change into a
  side-by-side figure. Regenerate its source images with larger labels before
  submission.
- Replaced forced `[H]` placement with `[htbp]` for ordinary figures and
  tables; full-width figures use `[tbp]`. The introductory schematic uses
  `[!htb]` so it floats with method text rather than occupying a float-only
  page.
- Reformatted the modulator-correlation table as density and intensity panels.
- Consolidated the exponent sensitivity, modulator-correlation, and bootstrap
  stability tables into Table 8(a--c), retaining every reported value while
  using the available horizontal space effectively.

## Completed work (2026-08-24 through 2026-08-28)

### Abstract — DRAFTED
~195 words. One placeholder remains for multi-expert consensus results.

### Contribution sentence — CONSOLIDATED
Single contribution sentence in §1.2.

### Category table — ADDED
Four-category ATC taxonomy table in §3.4.

### RQ2/RQ3 discussion — REALIGNED
Old RQ2/RQ3 relabeled; new RQ3 paragraphs authored.

### s-circularity fix — DONE
s=1.0 as principled default via Huber; sensitivity reframed as robustness.

### Robustness sections — ADDED to §4.3
Sensitivity to exponent, bootstrap professor stability, permutation control.

### Citations — all LAK anchors added
Gašević, Lockyer, Ferguson & Clow, Drachsler & Greller, Tsai & Martinez-Maldonado, Butt. All `\citeneeded` resolved.

### Corrections (prior sessions)
Ferguson & Clow placement fixed; correlation_plots.py percentage calculation fixed; non-breaking space workaround.

## Known rough edges

- The standalone evaluation procedures have been removed from Method and must be reinstated in their finalized form within the relevant §4.3 results subsections.
- `main.pdf` is stale relative to source edits; do not compile unless requested.
- `Diagrams/pdfs/pseudocode.pdf` is stale (not included in draft).
- All table floats changed to `[H]` — may need adjustment if layout shifts after cuts.
- Manuscript comments not yet pruned — many `%%%` transfer-provenance comments remain.
