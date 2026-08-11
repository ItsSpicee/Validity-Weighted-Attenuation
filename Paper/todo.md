# Paper TODO — s-circularity fix

**Status as of 2026-08-09: the paper is numerically and textually consistent with
the s = 0.83 held-out pipeline.** Everything in the original list is done. What
remains is recorded at the bottom.

---

## Done

### Values and tables

All updated from the pipeline run of 2026-08-09 and cross-checked with a
stale-value sweep over every `.tex` in the folder (clean, apart from three false
positives: an emotion value `0.863`, a CV fold `0.7241`, and a DOI containing
`0.2047`).

- **§3.9** — `s = 0.86` → `0.83`; sentence rewritten to drop the "maximizes these
  criteria" overclaim and to state training-professor-only selection.
- **§3.10 worked examples** — `ex2.tex`, `ex3.tex` table bodies and captions;
  `main.tex` prose at ~634/637 restated the same numbers. `ex1.tex` needed no
  change ($D_{misc} = 0$, so $\zeta = 1$ at any `s`). PDFs recompiled.
- **§4.3.3** — all eight cells of `tab:correlation_deltas`; Mann-Whitney n, U and
  rank-biserial.
- **§4.4** — fine row 21 → 22 correct, 0.724 → 0.759; prose 72.4% → 75.9%,
  p < 0.012 → p < 0.005. Coarse row unchanged.
- **§5.4** — prose, `tab:adjustment-stats` and the Wilcoxon W.
- **§6.2** — the four SHAP percentages, both §4.3.3 restatements (lines ~1100 and
  ~1102 quote the entire modulator table in prose), and mean |Δ|.

### Prose

- **1.1** Future Work circularity paragraph deleted, replaced with independent
  dataset / formal external criterion.
- **1.2** Limitations rewritten around weak identification of `s`.
- **1.4** All five "stratified" → "grouped".
- **2.1** Paragraph at the end of §3.7 stating the split governs three stages,
  ending "No professor contributes reviews to both parameter selection and
  reported evaluation."
- **2.2** §4.3 header states the population and both n values.
- **2.3** §4.4 full-sample justification (constraints + no circularity risk).
- **2.4** Framing paragraph separating §4.3 (verification) from §4.4 (independent
  evidence).
- Every §4.2/§4.3 float now declares its population and n.

### Populations, for reference

The two n values in §4.3 are different and both correct:

| Analysis | Source | n |
|---|---|---|
| SHAP (beeswarm, importance, % change) | `final_emotions.csv`, held-out | 3,414 |
| Correlation changes, modulators, Mann-Whitney | `attuned_ratings.csv`, held-out | 2,052 |
| Expert validation (§4.4) | full sample, deliberately | 77 pairs |
| Adjustment outcomes (§5.4) | full corpus | 10,380 |

Split: 823 training professors (13,718 reviews) / 206 held-out (3,414).

---

## Remaining

1. **§4.2 and §5.3 regression numbers are unverified, not verified-unchanged.**
   ρ = 0.7355 and R² = 0.6140 at ~line 1096, plus `tab:CatBoost-performance`. The
   split refactor was behaviour-preserving and the model was not re-specified, so
   they should not have moved — but the pipeline run did not print regression
   metrics, so this was never confirmed. Worth one check.

2. **`sidequestz/` optional analyses, none run.** Sensitivity tables, Wilson CIs,
   permutation control. The permutation test is the highest-value one. See
   `sidequestz/context.md`.

3. **Optional labelling symmetry.** `tab:external-validation` (§4.4) and
   `tab:adjustment-stats` (§5.4) do not say "full sample". Inferable from the
   §4.3 header, so this is cosmetic.
