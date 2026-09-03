# LAK27 Draft — Status (updated 2026-09-03)

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

~16 pages estimated (down from ~17.75 after redundancy compression pass, ~21 pre-cut). Target: 14 pages. Submission deadline: 2026-09-28 (25 days).

## Remaining TODOs

### Must-do before submission

1. **Multi-expert consensus** — §4.3.1 expert validation results need updating from single-expert to multi-expert consensus (majority vote, Fleiss' κ, Wilson intervals). Single-expert figures deliberately not transferred. **Blocks items 2–4 below.**
2. **Result-local evaluation protocols** — the standalone Evaluation Strategy subsection was deleted during the cut pass. Once consensus is implemented, add the finalized expert-comparison procedure to §4.3.1 and the necessary permutation procedure to §4.3.2. The §4.3.1 insertion must explain pair construction and coarse/fine allocation; the blinded raw-text task and randomized order; the more-valid-review / unsure response options; scoring against the smaller $|\Delta|$; panel composition, independent labels, consensus/tie handling, and Fleiss' $\kappa$; and final inclusion/exclusion accounting. Do not restore the obsolete single-expert wording. (Blocked by #1.)
3. **Limitations paragraph** — source manuscript's single-expert limitation paragraph not transferred; replace with multi-expert limits once results exist. (Blocked by #1.)
4. **Abstract expert placeholder** — abstract contains `\todo{[placeholder: multi-expert consensus results]}`. Fill once consensus is run. (Blocked by #1.)
5. **Funding statement** — check if required; currently a `\todo`.
6. **Strip all red text** — zero `\new`, `\todo` should remain at submission. All are drafting scaffolding.

### Discussion hardening pass (2026-09-03)

This pass tightened the validity argument from a LAK/psychometric-review
perspective. The governing distinction is now: **mechanistic coherence** shows
that the implemented rule behaves as specified; **robustness and falsification**
show that this behaviour is stable and depends on the review-level density
assignment; **expert paired comparisons** provide bounded human-judgment
evidence under their curated protocol. None establishes that the taxonomy or
density proxy is correct, or that adjusted ratings measure teaching quality.

- §5.1 now frames SHAP as attribution within the fitted model, rather than as
  causal evidence about rating drivers. It describes \textit{Miscellaneous} as
  content classified outside the stated taxonomy, rather than inherently
  irrelevant or unimportant content.
- RQ3 is organized in four short moves: mechanistic coherence; bootstrap,
  exponent-sensitivity, and permutation checks; expert paired-comparison
  evidence; then a bounded synthesis. Keep this architecture when inserting
  the finalized multi-expert results. Current single-expert figures remain
  temporarily, by author decision, until those results arrive.
- §5.2 has been narrowed to its practical and theoretical value: an auditable,
  corpus-scale review queue sortable by $|\Delta|$ for human inspection, and an
  explicit, in-principle configurable taxonomy aligned to purpose and learning
  design. Aggregate use is intentionally one sentence and limited to
  exploratory topic profiles, not rankings or performance measures. Tsai &
  Martinez-Maldonado, Gašević et al., and Lockyer et al. anchor this LAK
  framing.
- §5.3 now explicitly rejects consequential institutional/platform deployment
  and automated decision-making; it retains the raw review and rating as the
  primary record and cites documented demographic/popularity bias risks.
- §6 replaces the “objective ground truth” formulation with the precise
  limitation: there is no independent, triangulated external evidence to
  support stronger inferences from adjusted than raw ratings. It also sharpens
  the RMP, ATC, neutral-content, taxonomy-scope, and formal-SET caveats.
- §7 conclusion now describes the operation (attenuating the modelled
  contribution of affect under a stated taxonomy) rather than claiming that
  construct-irrelevant variance has been eliminated. It positions the work as
  a theoretical complement and extension to learning-analytics approaches to
  open-ended teaching feedback.

**Process rule for subsequent prose edits:** prefer minimally additive,
claim-matched changes. Do not broaden uses or reintroduce “signal-to-noise,”
causal-driver, ground-truth, or ready-for-deployment language without new
evidence. A final copy-edit is still needed after expert results are inserted;
the current discussion pass was substantive, not a full typography/spacing
pass.

### Redundancy compression pass (2026-09-03)

Systematic redundancy and excessive-negation pass, applied point-by-point with
author approval. Estimated ~1.75 pages saved from prose alone (layout-dependent).

- §5.1 RQ1 discussion: removed restatement of topic frequencies, elaboration
  depth, and SHAP hierarchy already reported in §4.1; kept interpretive framing
  only
- §5.1 RQ3 discussion: collapsed four paragraphs to two — dropped restated
  correlation values, CI widths, and expert accuracy numbers; kept evidence-type
  summary with key p-values and bounded synthesis
- §5.1 positioning paragraph: cut Messick/Cronbach/Huber/Doshi-Velez/Drachsler/
  Gašević restatement (all appear in §1–2); kept Zhai contrast and "initial
  method evidence" positioning
- §5.3 Boundaries: merged three paragraphs into two — combined deployment
  prohibition, DELICATE framing, and automated-vs-decision-making distinction;
  dropped repeated contestation/governance language
- §1.3: removed "not validated estimates / not for high-stakes decisions"
  sentence (covered fully in §5.3); kept Misc ≠ unimportant and Tsai citation
- §4.3.2 permutation control: replaced "does not establish X; establishes Y"
  with positive claim only
- §7 conclusion: cut "it does not silence student voice" (positive half already
  says "preserves every original review and its full emotional profile")
- §2.1: collapsed Zhai paragraph into synthesis sentence; preserved citation
  and controlled-conditions contrast
- §5.2→5.3 bridge: deleted redundant paragraph; moved "additional information
  is not inherently safer to act on" to open §5.3 as transition
- §4.2: merged Feature Importance, Correlation Changes, and Modulator
  Correlations subsubsections into single "Mechanistic Coherence" subsubsection;
  dropped three headers and tightened prose
- Figure caption fixes: "Relative changes" → "Change (%)" in both panels of
  the mechanistic-checks figure

### Next phase — layout and strategic omission

- Continue from the ~16-page baseline. Compile and inspect actual page count
  before further cuts.
- Decision: retain the full Section 4.3 evidence in the compact three-panel
  Table 8(a--c), rather than moving those results to supplementary material.
- Regenerate the source images used in the SHAP/correlation two-panel figure with larger
  axis, tick, legend, and annotation fonts; the new side-by-side layout is
  space-efficient, but its labels need to remain readable at panel scale.
- Remaining cut candidates if needed: one-star heatmap to supplementary (~0.4p),
  sensitivity Table 8(a) to supplementary with representative subset (~0.3p),
  SHAP beeswarm to supplementary (~0.4p), citation cluster trimming (~0.15p).
- Reassess after compile — float placement may recover or lose space
  unpredictably.

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
