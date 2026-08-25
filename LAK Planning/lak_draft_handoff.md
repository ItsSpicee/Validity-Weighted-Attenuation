# LAK27 Draft — Handoff

State of `LAK Planning/LAK_draft/main.tex` as of 2026-08-24.

## Intended workflow (decided 2026-08-23)

Work in this order. **Do not cut before the additions are in** — the point is to
cut with full knowledge of what the finished paper needs, rather than guessing
at the value of sections that do not exist yet.

1. **Citations.** Decide the additional references and add them to
   `references.bib` (see *Citations* below — the LAK anchors are the scope risk).
2. **Red comments.** Work through every `\todo`, `\new`, and `\citeneeded` one
   by one, writing the new content and approving or replacing the reworded text.
3. **Cut the verbatim transferred content.** Only now, with the whole paper
   visible. See *Open problem: length* for the budget and targets.
4. **Reassess length.**
5. **Polish.**

Expect step 3 to be large: the finished-at-current-scope estimate is ~23 pages
against a 14-page cap.

## Assessment of source manuscript (added 2026-08-24)

A full reading of the source manuscript confirms that the paper is **already
epistemically careful**. It consistently uses bounded language ("aims to
generate," "seeks to mitigate," "proof-of-concept," "tentative evidence")
throughout its methods, results, and limitations. The problematic spots are
**narrow — two locations, not a systemic issue**: the conclusion's opening line
and Section 6.3's deployment vision (paragraphs 2–3). The LAK transformation
is three targeted moves, not a wholesale reframe:

1. **Redirect the deployment vision** — from automated platform/institutional
   deployment to an educator interpretation tool (§5.2, §5.3)
2. **Add LA situating language** — citations and connecting prose so the paper
   is visibly situated in learning analytics
3. **Miscellaneous ≠ unimportant** — preserve student voice, separate its
   pedagogical role from its experience-signal role (§2.3)

The original strategy docs overstated the gap. Most transferred body prose is
already fine and does not need claim-level revision.

## Where this stands

The LAK draft exists, compiles clean, and is a **structural skeleton filled with
verbatim source prose**. It is not a written paper yet. Every section that the
framing doc marks Revise or Rewrite is a marked placeholder rather than
finished text, and the two evidence sections that depend on pipeline reruns are
empty by design.

The long-form manuscript in `Paper/ABSA_Validity_Weighted_Framework_With_Revisions_v4___honest (2)/main.tex`
is untouched and remains the source document.

## Build

```
cd "LAK Planning/LAK_draft"
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

Compiles with no errors and no undefined citations. `JLA_article.cls` and
`header.png` were copied into `LAK_draft/`, so the folder builds standalone.
`Diagrams/` was already mirrored there.

Current output: **21 pages** (~18 body, ~3 references).

## The one rule that governs this file

**Black body text is verbatim from the source manuscript. Red text is not.**

Nothing that is not your own wording can appear as ordinary black body copy.
Four macros, all rendering red:

| Marker | Meaning |
|---|---|
| `\todo{...}` | red bold `[TODO: ...]` — action needed |
| `\new{...}` | red text — added by Claude or reworded from the source |
| `\begin{newcontent}` | same, for multi-paragraph blocks |
| `\citeneeded{...}` | citation not yet in `references.bib` |

Pure **deletions are not marked** — cutting was part of the brief. Only
**additions and rewordings** are. Comment banners `%%% VERBATIM`,
`%%% [FROM FRAMING DOC]`, and `%%% PLACEHOLDER` explain each block's provenance
in the source.

Counts (as of 2026-08-24): **18** `\new` spans, **26** `\todo` (2 resolved), **4** `\citeneeded`.

Worklist:

```powershell
Select-String -Path main.tex -Pattern '\\todo\{'
```

Only mechanical edits were applied to transferred prose: parenthetical
author-year citations converted to apacite `\cite{}`/`\citeA{}`, and whole
blocks deleted. No sentence was paraphrased or condensed silently.

## Blocking items — nothing else can fill these

1. **Multi-expert consensus results** (§4.3.1). Needs majority-vote consensus
   implemented and validation rerun. Requires overall/coarse/fine accuracy with
   95% Wilson intervals, Fleiss' κ, the 77-of-80 accounting, and the treatment
   of unsure labels. The single-expert figures (62/77 = 80.5%; coarse 38/43 =
   88.4%; fine 24/34 = 70.6%) are **deliberately not transferred** — the framing
   doc supersedes them.
2. **Permutation control results** (§4.3.2). Needs the 1,000-permutation rerun
   under the fixed-positive-density design. `newresults.md` predates the
   fixed-population correction and must not be cited.

## Sections needing new writing (source has no usable counterpart)

| Location | What is needed |
|---|---|
| Abstract | ≤200 words. Anchor on the framing doc's one-sentence contribution statement, quoted in a comment above the `\Abstract`. |
| Keywords | Suggested pool present, not fixed. |
| §1.3 boundary paragraph | **DONE** — authored by user. Not a measure of true teaching quality; CIV scoped to taxonomy; empowering stakeholders with more information. |
| §2.3 design principle | **DONE** — authored by user. Learner-voice preservation, pedagogical role vs. experience-signal role, bounded monotonic rule, exposure of every adjustment, auditability limits. |
| §5.2 responsible use | **DONE** — authored by user. Three stakeholder scenarios (educator, student, platform responsibility), raw data preservation, bridge to §5.3. |
| §5.3 non-use | **DONE** — authored by user. Five paragraphs: not a quality measure / not a substitute for reading reviews, platform responsibility, automated calculation vs. deployment, unaddressed bias sources, auditability limits as responsible-use requirement. |
| Conclusion | Not transferred — the source conclusion opens with a claim on the framing doc's prohibited list. |

## Sections needing revision of transferred text

*Updated 2026-08-24: the source paper is more careful than originally assumed.
Most "revision" items below are light touch — the body prose is already
epistemically appropriate. Only §1.1's final sentence and the deployment
redirection (§5.2/5.3) are substantive claim-level changes.*

Flagged in place with `\todo`. Highest-value first:

- §1.1 last sentence contains "misrepresents true teaching effectiveness" — the one clear overclaim in the intro. **TODO** — reword.
- §1.1 opening paragraph and transition — **DONE** by author.
- §1.2 Lockyer citation added alongside Doshi-Velez — **DONE** by author. Gap framing is fine as-is.
- §1.3 contribution bullets revised — **DONE** by author. Boundary paragraph added.
- §2.2 Ren/Butt contrasts rewritten — **DONE** by author.
- §2.4 Research Gap rewritten — **DONE** by author.
- §3.4.1 contestability sentence added — **DONE** by author.
- §3.9 expert-pair protocol is written in the singular ("the expert") and must move to the multi-expert consensus wording. **TODO**.
- §5.1 needs Ferguson & Clow (2017) citation added. **TODO** — light touch only.
- §5.2 responsible use — **DONE** by author.
- §5.3 boundaries, risks, and non-use — **DONE** by author.

## What was cut

**15 of 19 floats.** Kept 9 (5 image-based, 4 typeset tables): framework
schematic, worked example 3, `D_misc` distribution, SHAP %-change, weighted
correlation change, clause/review frequency table, ATC classification report,
merged CV + held-out performance, modulator correlations.

Cut: all 3 EDA figures, data-examples table, pseudocode, ATC sub-schematic, all
3 emotion heatmaps, topic-frequency / topic-combinations / rating heatmap,
baseline SHAP beeswarm, all 4 adjustment-distribution figures, absolute
SHAP-delta figure, per-feature correlation figure, ATC confusion matrix,
Cohen's κ table, exploratory model-comparison table.

**Sections cut:** Domain-Adjacent Applications, worked examples 1–2 (retained as
prose), all inline regex / clause-segmentation / density walkthroughs,
per-study paragraphs in the computational-SET review, standalone Future Work
(merged into Limitations).

**Anonymization:** Acknowledgments section removed entirely (names supervisor,
institution, course code). REB institution name replaced. Restore at
camera-ready.

### Pseudocode — decided against

Not included. Three reasons, in order:

1. The rendered asset encoded the **obsolete exponent rule** `ζ ← 1 − (D_misc)^s`,
   which would have contradicted Eq. `ζ = 1 − D_misc` in the same paper. *This
   has since been fixed in `pseudo.tex` but the decision stands.*
2. Redundant — all eight stages already appear in the five-stage description
   list, the schematic, and the equations.
3. Expensive — source page is 14 × 21.1 cm (ratio 1.5), ~0.75 page even at
   `0.6\linewidth`.

`pseudo.tex` is corrected and retained in `LAK_draft/` if the decision is ever
reversed; `Diagrams/pdfs/pseudocode.pdf` is **stale** and would need
regenerating.

## Open problem: length

The page limit **includes references and Notes for Practice** — CFP line 82:
*"Full research papers (from 10 to 14 pages in JLA format, including references
and notes for practitioners)."* References are ~2.3 pages of the current 21 and
cannot be moved off the count.

Arithmetic for the finished paper at current scope:

| | pages |
|---|---|
| Current | 21.0 |
| − red `\todo` text, once deleted | −2.3 |
| + filling the placeholders (~2,400 words + expert table) | +4.25 |
| + ~7 more references | +0.3 |
| **Finished at current scope** | **≈ 23.2** |
| Target | 14.0 |

**≈ 9.2 pages must be cut** — about 5,500 of the ~11,300 body words, roughly
half. Free savings (figure sizing, `ex3.pdf` bottom trim) are already taken.

### The budget to cut against

`full_paper_framing.md` already specifies a 14-page paper: Intro 1.25,
Background 1.5, Method 3, Results 2.25, Discussion 1.5, Limitations 0.75,
Conclusion 0.35, Notes 0.25 = 10.85, plus ~2.6 references ≈ 13.5. The plan was
sound; the overrun came from transferring verbatim well past those budgets.

Measured against it:

| Section | now | target | over |
|---|---|---|---|
| Front matter + §1 Intro | 2.5 | 1.75 | +0.75 |
| §2 Background | 2.3 | 1.5 | +0.8 |
| §3 Method | 5.5 | 3.0 | **+2.5** |
| §4 Results | 6.0 | 2.25 | **+3.75** |
| §5 Discussion | 1.7 → ~3.5 (§5.2+§5.3 drafted) | 1.5 | +2.0 |
| §6 Limitations | 1.0 | 0.75 | +0.25 |
| §7 Conclusion | 0 → 0.35 | 0.35 | — |
| References | 2.3 → 2.6 | 2.6 | — |

**Results and Method are 6.25 of the 9.2.** Results is worst because nearly all
its prose was kept after fifteen figures were cut, leaving paragraphs that
narrate figures no longer present.

### Where the cuts come from

**Results 6.0 → 2.25.** Biggest win. Cut the topic-combinations,
rating-heatmap, review-level-elaboration and section-summary paragraphs in
§4.1.1 (all describe cut figures); collapse the LLM-κ and containment-criterion
explanations to two sentences; cut the two SHAP directional-coherence
paragraphs (RQ1 is argued in the Discussion regardless); cut the §4.2 closing
summary and the internal-validation conclusion, which restate what precedes.

**Method 5.5 → 3.0.** Cut the five-stage Model Pipeline list (duplicates the
schematic and §3.3–3.9); re-cut the 28-emotion label list; trim preprocessing to
the exclusion criteria; reduce the CatBoost justification to one sentence.

**Background 2.3 → 1.5.** Cut the Sorour / Louis / Xiong relevance-estimation
block and one SET-contamination paragraph.

**Intro 2.5 → 1.75** and **Limitations 1.0 → 0.75** are trims, not structural cuts.

### Two decisions still open

- **Target 13 rather than 14?** A page of slack absorbs the expert-results
  table, whose size is unknown until the consensus run lands.
- **Drop a whole result family?** Results currently spans eight of them in a
  2.25-page budget. Candidate: the ATC/sentiment descriptive material
  (§4.1.1–4.1.2), keeping only the `D_misc` distribution since it motivates the
  proportional design. ~1.2 pages, and it costs descriptive context rather than
  evidence.

### Appendix — do not plan on one

The JLA class has **no appendix machinery**, and the CFP says nothing about
appendices either way. The CFP also notes the submission guidelines page was
"coming soon," so the authoritative rules are not in the materials here.

Inference, flagged as such: the limit reads "10 to 14 pages... **including**
references and notes for practitioners" — it names what counts and names no
carve-out. Assume anything in the PDF counts. Plan to fit 14 inclusive; put
overflow in an anonymized supplementary repo (`anonymous.4open.science` or an
OSF anonymized view). Confirm with `lakconference@gmail.com`, which the CFP
gives specifically for length and format questions.

## Citations

`references.bib` (50 entries) resolves cleanly, but **lacks every
learning-analytics anchor** — Gašević, Lockyer, Ferguson & Clow, Drachsler &
Greller, Prinsloo & Slade, Tsai & Martinez-Maldonado — and Butt et al. (2025).
Four `\citeneeded{}` markers show where they go.

This is the single highest scope risk. The CFP states: *"A paper that does not
mention 'learning analytics' in its text or references is highly likely to be
out of scope."*

**Style fix already applied.** apacite implements APA 6th, which spells out all
authors on a 3–5 author work's first citation. Two preamble lines force APA 7th
behaviour document-wide:

```latex
\let\cite\shortcite
\let\citeA\shortciteA
```

No per-key list, so it keeps working as references are added. Reference list
still lists all authors; apacite's `\fullcite`/`\fullciteA` remain available.

## Corrections made after the first draft — including outside `LAK_draft/`

Three of these changed files elsewhere in the repo.

**1. A false scope claim, introduced by the restructuring.** The verbatim
sentence *"All metrics in this section are computed on the 206 held-out
professors"* headed source §4.3, where everything below it was held-out. The
draft merged the **full-corpus** Adjustment Outcomes (source §5.4) into the same
subsection, so the claim came to cover seven full-corpus statistics — the
10,375 / 60.58% count, mean Δ, mean |Δ|, the extremes, and the Wilcoxon
W = 24,260,091. Verified against `attenuation_plots.py:356-363`, whose own
comment says those summaries *"stay on the full sample."* The source had a guard
sentence pointing at §5.4; deleting it as a dead cross-reference is what let the
error through. Fixed by moving the scope paragraph below Adjustment Outcomes.

All underlying counts were checked against the data and are correct: 1,029
professors (206 held out), 17,127 reviews (3,414 held out), 10,375 with
`misc_d > 0` (2,052 held out), 60.58%.

**2. "Predicted ratings" in the correlation section — wrong in both files.**
`correlation_plots.py:62-94` correlates baseline emotion sums against the raw
rating and against `rating + weighting_delta`. Neither side is a model
prediction. Corrected in the draft **and in the long-form manuscript at
`main.tex:829`**, with identical wording so the two cannot drift. The other
eight occurrences of "predicted ratings" in the long form were checked and are
correct — they refer to genuine model output.

**3. `correlation_plots.py` — the "% change" figure was not a percentage.**
It computed `(abs(attuned) - abs(raw)) * 100`, an absolute difference in
correlation units labelled as a percent, while the neighbouring SHAP figure
(`attenuation_plots.py:200`) computed a genuine relative change. Two figures,
both with "%" axes, reporting incommensurable quantities — and the magnitudes
landed close enough to invite the confusion.

Changed to match the SHAP convention: `(abs(att) - abs(raw)) / abs(raw) * 100`.
Also added `MIN_BASELINE_CORR = 0.01` (relative change is meaningless against a
near-zero baseline; below it the value is NaN, skipped by `nanmean` so one
polarity group cannot void a topic), dropped the false "Weighted" from the title
and axis, renamed `plot_weighted_pct_change` → `plot_relative_pct_change`, and
added a per-topic printout so the numbers are recoverable without reading bars.

> **This inflates the reported magnitudes, roughly doubling them or more.** The
> old form understated the result hardest exactly where it mattered: the
> miscellaneous correlations are the weaker ones, so their suppression was
> compressed most. Example: r 0.40 → 0.325 was plotted as −7.5%, is truly
> −18.75%.

> **Not yet run.** No `pandas` in the Python on PATH and no venv in the repo
> root, so the module is syntax-checked and the arithmetic verified in
> isolation, but the numbers are unverified. `correlation_plots.py` has no
> `savefig` — it only calls `plt.show()`, so the figure must be re-saved by hand
> after rerunning. The existing PNG is still named `weighted_corr_changes.png`;
> worth renaming.

## Known rough edges

- §3.1 "The distribution is negatively skewed" has lost its antecedent (the
  rating-frequency figure it referred to is cut). Flagged.
- The four-category taxonomy is defined in prose only. The framing doc asks for
  a category table; it would need building from the descriptor strings in the
  codebase. Flagged.
- Three density equations were collapsed into one indexed equation, and four
  display equations inlined, purely for space. All flagged; restore if wanted.
- The clause/review frequency table is a transposed re-layout of the source
  table — same numbers, no wording changed.

## Next-session checklist

Follows the *Intended workflow* at the top — additions first, cuts afterwards.

**Step 1 — citations**

1. Add the LAK anchors and Butt et al. (2025) to `references.bib`. Add any new
   3+ author key to nothing — the `\let\cite\shortcite` aliasing handles et al.
   automatically.

**Step 2 — red comments, one by one**

2. Write §2.3 (design principle) and §5.2–5.3 (responsible use, non-use). These
   are the LAK-specific contribution and have no counterpart in the source.
3. Address the revision `\todo`s on transferred text — the prohibited-claim
   sentence in §1.1, the gap framing in §1.2, the contribution bullets in §1.3,
   the Ren/Butt contrasts in §2.2, the singular "the expert" in §3.9, the
   primitive framing in §5.1.
4. Fill the two blocked evidence sections once the reruns land.
5. Write the conclusion, then the abstract last.
6. Approve or replace each of the 18 `\new` spans; strip the marking as you go.

**Step 3–5 — cut, reassess, polish**

7. Cut against the section budget table above; deletion only, no rewording.
8. Recompile and remeasure.
9. Confirm **zero red text remains** before submission — it is all drafting
   scaffolding and none of it should ship.

**Independent of the above — needs a pipeline run**

- ~~Rerun `correlation_plots.py` and re-save the figure~~ — **done**, figure
  regenerated and renamed `average_corr_changes.png`; caption updated.
  No prose numbers needed changing: §4.2's correlation text is entirely
  qualitative, and every figure in it traces to `attenuation_plots.py`, which
  was not touched.
- Rerun validation with multi-expert consensus, and robustness with 1,000
  permutations.
