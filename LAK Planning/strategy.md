
## Strategy — current state (updated 2026-08-27)

The LAK transformation required four targeted moves. Status of each:

### 1. Redirect the deployment vision — DONE

§5.2 (Responsible Interpretation) and §5.3 (Non-Use) are drafted and in place.
Source §6.3 paragraphs 2–3 (automated deployment) were not transferred.

### 2. Add LA situating language — DONE

All required citations added to `references.bib` and placed in the manuscript:

| Citation | Status | Placement |
|---|---|---|
| Gašević, Dawson, & Siemens (2015) | Added | §2.4 Research Gap — "enhance and support stakeholder interpretation" |
| Lockyer, Heathcote, & Dawson (2013) | Added | §1.2 — bridge between taxonomy and pedagogical intent |
| Ferguson & Clow (2017) | Added | Future Work — evidence standard for intervention claims |
| Drachsler & Greller (2016) | Added | §2.3 Design Principle, §2.4 Research Gap (transparency) |
| Tsai & Martinez-Maldonado (2022) | Added | §1.3 Contribution — complementary to raw ratings |
| Butt et al. (2025) | Added | §2.2 — BERT vs LLM contrast, no validity rule |

Prinsloo & Slade was removed as redundant with Drachsler & Greller.

### 3. Miscellaneous ≠ unimportant — DONE

§2.3 Design Principle drafted by user. Learner-voice preservation, pedagogical
role vs. experience-signal role, bounded monotonic rule.

### 4. Foreground stakeholder-defined taxonomy — DONE

Central claim (~line 190): "that stakeholders have the ability to control."
Conclusion: stakeholder-defined taxonomy as closing design principle.
Skipped contribution bullet (too close to central claim, would be redundant).

## Reviewer anticipation table

| Reviewer concern | Best response |
|---|---|
| "Why adjust scores rather than analyze text?" | Contribution is moving from descriptive detection to transparent, bounded intervention on modelled influence. |
| "Is this truly learning analytics?" | Analytics of teaching-feedback traces aimed at responsible interpretation for teaching improvement. |
| "Can it establish teaching quality?" | No; tests whether an interpretable attenuation mechanism behaves consistently with a stated validity argument. |
| "Why this formula/taxonomy?" | Intentionally simple, monotonic, auditable, grounded in CIV; paper documents limits. |
| "Why RMP?" | Intentionally difficult, noisy stress-test — not a surrogate for institutional SET. |
| "Isn't the coarse expert result circular?" | Conceded in paper. Coarse is a manipulation check; validity claim rests on fine-grained condition and permutation control. |

## Handle the coarse expert condition candidly

Report coarse as a **manipulation check**, not the headline. The permutation
control results confirm this framing: coarse accuracy under permutation drops
only modestly (p = 0.233) because other features carry the signal for obvious
cases. Fine-grained accuracy degrades significantly (p = 0.007), and modulator
correlations collapse entirely (p < 0.001). Lead with fine + correlations.

Do **not** report a single pooled accuracy across both conditions.

## What does NOT need to change

- Method, equations, pipeline, validation design
- RQ framing (already appropriate)
- Limitations section (already honest)
- Body claim language (already careful — don't over-correct)
