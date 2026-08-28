# LAK27 Full-Paper Framing and Source Map

## Working title

**Validity-Weighted Attenuation of Affective Noise in Open-Ended Teaching Feedback: An Interpretable ABSA Framework**

## Central claim

Open-ended teaching feedback contains both pedagogically actionable evidence
and broader affective student experience. We introduce **validity-weighted
attenuation**, an interpretable, clause-level method that proportionally
attenuates the modelled contribution of affect in content classified as outside
of a pedagogical taxonomy that stakeholders have the ability to control, while
retaining the original review and a review-level audit trail.

## Research questions

**RQ1.** How are topic-specific emotional signals associated with numerical
ratings in open-ended teaching feedback?

**RQ2.** Can validity-weighted attenuation reduce the contribution of
construct-irrelevant affect to numerical ratings while preserving relevant
signals, under the taxonomy used in this study?

**RQ3.** Does the mechanism exhibit behaviour consistent with its validity
rationale on held-out instructors, expert-labelled comparisons, and robustness
controls?

## Full-paper outline (target: 12–14 JLA pages inclusive)

### 1. Introduction (~1.25 pages)
- 1.1 Open-ended teaching feedback as an LA trace
- 1.2 The unresolved methodological gap
- 1.3 Contribution and boundaries

### 2. Background (~1.5 pages)
- 2.1 Validity, CIV, and teaching feedback
- 2.2 From descriptive NLP to validity-oriented interpretation
- 2.3 Design principle: attenuation rather than deletion
- 2.4 Research gap

### 3. Method (~3 pages)
- 3.1 Study context and data
- 3.2 Clause-level representation (ATC + emotion)
- 3.3 Rating model and evaluation split
- 3.4 Validity-weighted attenuation + audit trail
- 3.5 Evaluation strategy

### 4. Results (~2.25 pages)
- 4.1 Corpus and model behaviour
- 4.2 What attenuation changes
- 4.3 Initial validity and robustness evidence
  - 4.3.1 Expert paired comparisons (multi-expert consensus — pending)
  - 4.3.2 Permutation control (written)
  - 4.3.3 Sensitivity to attenuation exponent (written — s ∈ {0.5, 0.75, 1.0, 1.25, 1.5})
  - 4.3.4 Bootstrap professor stability (written — correlation-only, 1,000 resamples)

### 5. Discussion (~1.5 pages)
- 5.1 A validity-oriented analytic primitive
- 5.2 Responsible interpretation (drafted)
- 5.3 Boundaries, risks, and non-use (drafted)

### 6. Limitations and future work (~0.75 pages)

### 7. Conclusion (~0.35 pages) — DRAFTED

### Notes for Practitioners (~0.25 pages)

## Page budget

| Section | Current | Target | Over by |
|---|---|---|---|
| Front matter + §1 | 2.5 | 1.75 | +0.75 |
| §2 Background | 2.3 | 1.5 | +0.8 |
| §3 Method | 5.5 | 3.0 | **+2.5** |
| §4 Results | 6.0 | 2.25 | **+3.75** |
| §5 Discussion | ~3.5 | 1.5 | +2.0 |
| §6 Limitations | 1.0 | 0.75 | +0.25 |
| §7 Conclusion | 0.35 | 0.35 | — |
| References | ~2.6 | 2.6 | — |

**~9.2 pages must be cut.** Results and Method account for ~6.25 of them.
Results is worst because prose narrating cut figures was retained.

## Material that must not enter the LAK draft

- Conclusion opening overclaim ("actual pedagogical quality") — rewritten
- §6.3 automated deployment paragraphs — not transferred; replaced by §5.2/5.3
- "misrepresents true teaching effectiveness" in intro — flagged for rewording
- Any statement that Miscellaneous content is unimportant
- Exponent tuning / grid-search / old s=0.83 language (RESOLVED: s=1.0 justified via Huber; sensitivity reframed as robustness)
- Single-expert figures presented as final (once consensus available)
- Identifying information in double-blind version

## Drafting rule

For every claim, distinguish among:
1. **Observed:** a result in this corpus
2. **Modelled:** a change produced by the specified method
3. **Aspirational:** a potential future validation or application
