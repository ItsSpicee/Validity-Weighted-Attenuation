# LAK27 Draft — Status (updated 2026-08-28)

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

Current counts: **5** `\todo`, **14** `\new`, **0** `\citeneeded`.

## Remaining TODOs

### Must-do before submission

1. **Multi-expert consensus** — §4.3.1 expert validation results need updating from single-expert to multi-expert consensus (majority vote, Fleiss' κ, Wilson intervals). Single-expert figures deliberately not transferred. **Blocks items 2–4 below.**
2. **§3.9 expert protocol** — wording is singular ("the expert"); must move to multi-expert consensus language once consensus is implemented. (Blocked by #1.)
3. **Limitations paragraph** — source manuscript's single-expert limitation paragraph not transferred; replace with multi-expert limits once results exist. (Blocked by #1.)
4. **Abstract expert placeholder** — abstract contains `\todo{[placeholder: multi-expert consensus results]}`. Fill once consensus is run. (Blocked by #1.)
5. **Funding statement** — check if required; currently a `\todo`.
6. **Strip all red text** — zero `\new`, `\todo` should remain at submission. All are drafting scaffolding.

### Cut phase (after all additions are in)

The paper is over the 14-page limit. Cuts needed:
- **Results and Method** are the biggest overruns
- Results: cut paragraphs that narrate figures no longer present
- Method: cut duplicative pipeline list, trim preprocessing detail
- New robustness tables (sensitivity + bootstrap) add ~1 page; account for this
- See page budget in `full_paper_framing.md`

## Completed work (2026-08-24 through 2026-08-28)

### Abstract — DRAFTED
~195 words. Opens with LA-situated framing ("underspecified data source for learning analytics"), introduces VWA with CIV-mitigation framing under definable taxonomy, cites key results (permutation p < 0.001, conservative adjustments, 60% of reviews adjusted), includes boundary statement ("not validated estimates of teaching quality"), closes with complement-to-raw-ratings positioning. One placeholder remains for multi-expert consensus results.

### Contribution sentence — CONSOLIDATED
Duplicate introduction removed. Single contribution sentence now lives in §1.2: "We introduce **validity-weighted attenuation**, an interpretable, clause-level method that proportionally attenuates the modelled contribution of affect in content classified as outside of a stated pedagogical taxonomy that stakeholders have the ability to control, while retaining the original review and a review-level audit trail."

### Category table — ADDED
Four-category ATC taxonomy table added to §3.4 with representative descriptors from `constants.py`.

### BERT introduction — RESOLVED
Already introduced on line ~235 via Butt et al. (2025): "BERT (Bidirectional Encoder Representations from Transformers)."

### RQ2/RQ3 discussion — REALIGNED
- Old "RQ2" paragraphs (CIV presence via SHAP baseline) relabeled as RQ1 continuation
- Old "RQ3" paragraphs (SHAP shifts, correlation changes, deltas) relabeled as RQ2 answer
- New RQ3 discussion paragraphs authored: modulator correlations, bootstrap stability, permutation controls, expert accuracy, sensitivity analysis

### s-circularity fix
- Dropped exponent optimization; s=1.0 set as principled default per Huber's (1964) proportional downweighting principle
- Sensitivity sweep reframed as robustness check ("results don't depend on this choice"), not justification for an optimized value
- `SENSITIVITY_S_VALUES` changed from `[0.37, 0.62, 0.91, 1.2]` to `[0.5, 0.75, 1.25, 1.5]` — symmetric around 1.0

### Robustness sections — ADDED to §4.3
- **§4.3.3 Sensitivity to Attenuation Exponent**: three tables (delta agreement, modulator correlations, expert accuracy summary), Huber justification for s=1.0, notes on Spearman trend and max-delta context
- **§4.3.4 Bootstrap Professor Stability**: correlation-only bootstrap (expert accuracy removed — not meaningful with small n), 1,000 resamples, tight CIs (SD ≤ 0.027)
- `src/robustness.py`: expert accuracy removed from bootstrap function

### Citations — all LAK anchors added (prior session)
Gašević (2015), Lockyer (2013), Ferguson & Clow (2017), Drachsler & Greller (2016), Tsai & Martinez-Maldonado (2022), Butt (2025). Prinsloo & Slade removed as redundant.

### `\citeneeded` — ALL RESOLVED (0 remain)

### Structural improvements (prior session)
- §2.1: Added Schiekirka & Raupach paragraph, transition sentence, closing synthesis
- §2.2: Butt et al. citation resolved, description corrected
- §2.4: Doshi-Velez + Drachsler transparency citations added
- Central claim: "stakeholders have the ability to control" language
- Conclusion: drafted (3 paragraphs)
- 15 obsolete comment blocks removed

### Robustness (prior session)
- Permutation control results table and interpretation written into §4.3.2
  - Coarse/fine expert accuracy reported separately (not pooled)
  - Coarse framed as manipulation check (p = 0.233)
  - Fine as load-bearing result (p = 0.007)
  - Modulator correlations as cleanest evidence (p < 0.001)
- `src/robustness.py`: coarse/fine breakdown added to `expert_accuracy()` and permutation output

### Corrections (prior session)
- Ferguson & Clow moved from incorrect "proof of concept" placement to Future Work
- `correlation_plots.py` percentage calculation fixed (absolute → relative change)
- Non-breaking space (U+00A0) issue in main.tex identified and worked around

## Known rough edges

- §3.1 "The distribution is negatively skewed" lost its antecedent figure
- Three density equations collapsed into one indexed equation (flagged; restore if wanted)
- `Diagrams/pdfs/pseudocode.pdf` is stale (not included in draft)
- All table floats changed to `[H]` — may need adjustment if layout shifts after cuts
- Manuscript comments not yet pruned — many `%%%` transfer-provenance comments remain
