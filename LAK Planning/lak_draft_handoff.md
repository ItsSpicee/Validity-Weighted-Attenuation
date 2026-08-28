# LAK27 Draft — Status (updated 2026-08-27)

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
| `\citeneeded{...}` | citation not yet in `references.bib` |
| `\auth{...}` | authored text, styled blue — will convert to black at submission |

Current counts: **8** `\todo`, **14** `\new`, **5** `\citeneeded`.

## Remaining TODOs

### Must-do before submission

1. **Abstract** — not yet written. ≤200 words.
2. **Multi-expert consensus** — §4.3.1 expert validation results need updating from single-expert to multi-expert consensus (majority vote, Fleiss' κ, Wilson intervals). Single-expert figures deliberately not transferred.
3. **§3.9 expert protocol** — wording is singular ("the expert"); must move to multi-expert consensus language once consensus is implemented.
4. **Category table** — four-category taxonomy is defined in prose only; framing doc asks for a table.
5. **Remaining `\todo` items** — 8 remain in manuscript. Work through each.
6. **Remaining `\citeneeded` items** — 5 remain. Resolve each.
7. **Strip all red text** — zero `\new`, `\todo`, `\citeneeded` should remain at submission. All are drafting scaffolding.
8. **BERT introduction** — BERT is first used on line ~285 without being introduced.

### Cut phase (after all additions are in)

The paper is over the 14-page limit. Cuts needed:
- **Results and Method** are the biggest overruns
- Results: cut paragraphs that narrate figures no longer present
- Method: cut duplicative pipeline list, trim preprocessing detail
- See page budget in `full_paper_framing.md`

### Nice-to-have

- **Bootstrap professor stability test** — code implemented in `src/robustness.py`, not yet run or written into manuscript. Low effort; can cut if space is tight.
- **Funding statement** — check if required.

## Completed work (2026-08-24 through 2026-08-27)

### Citations — all LAK anchors added
Gašević (2015), Lockyer (2013), Ferguson & Clow (2017), Drachsler & Greller (2016), Tsai & Martinez-Maldonado (2022), Butt (2025). Prinsloo & Slade removed as redundant.

### Structural improvements
- §2.1: Added Schiekirka & Raupach paragraph, transition sentence, closing synthesis
- §2.2: Butt et al. citation resolved, description corrected
- §2.4: Doshi-Velez + Drachsler transparency citations added
- Central claim: "stakeholders have the ability to control" language
- Conclusion: drafted (3 paragraphs)
- 15 obsolete comment blocks removed

### Robustness
- Permutation control results table and interpretation written into §4.3.2
  - Coarse/fine expert accuracy reported separately (not pooled)
  - Coarse framed as manipulation check (p = 0.233)
  - Fine as load-bearing result (p = 0.007)
  - Modulator correlations as cleanest evidence (p < 0.001)
- `src/robustness.py`: coarse/fine breakdown added to `expert_accuracy()` and permutation output
- `src/robustness.py`: bootstrap professor stability test implemented (not yet run)

### Corrections
- Ferguson & Clow moved from incorrect "proof of concept" placement to Future Work
- `correlation_plots.py` percentage calculation fixed (absolute → relative change)
- Non-breaking space (U+00A0) issue in main.tex identified and worked around

## Known rough edges

- §3.1 "The distribution is negatively skewed" lost its antecedent figure
- Three density equations collapsed into one indexed equation (flagged; restore if wanted)
- `Diagrams/pdfs/pseudocode.pdf` is stale (not included in draft)
