
## Assessment of the original paper (updated 2026-08-24)

After a full reading of the source manuscript, the original paper is **already epistemically
careful** throughout its methods, results, and limitations. It consistently uses bounded
language ("aims to generate," "seeks to mitigate," "proof-of-concept," "tentative evidence")
and its limitations section explicitly states that adjusted ratings do not "definitively prove"
better reflection of teaching quality. The strategy originally overstated the gap between the
source paper's claims and what LAK requires.

**The problematic spots are narrow — two locations, not a systemic issue:**

1. **The conclusion's opening line** (Section 9): "producing adjusted numerical ratings that
   aim to better reflect actual pedagogical quality." This is the one sentence that crosses
   the line the rest of the paper carefully stays behind.

2. **Section 6.3, paragraphs 2–3** (Theoretical & Practical Implications): proposes deployment
   on student-facing platforms to "increase the trustworthiness of ratings" and suggests
   institutional SET processing. This is where the paper closes the stakeholder loop — but in
   the wrong direction for LAK. It proposes automated deployment, which is exactly what LAK
   reviewers will challenge.

## The three actual changes needed for LAK

The transformation is **not** a wholesale reframe. It is three targeted moves:

### 1. Redirect the deployment vision

The source paper's Section 6.3 proposes the framework as something platforms and institutions
deploy on ratings automatically. The LAK version needs to flip this: it is a tool an instructor
or teaching-support person uses to *read* feedback more carefully, not something that
automatically adjusts scores in a database.

The audit trail machinery already supports this — the worked examples, the SHAP traces, the
clause-level breakdown. They just need to be pointed at a different user: someone sitting down
to interpret feedback, not a system processing ratings at scale.

This is the content of §5.2 (Responsible Interpretation) and §5.3 (Non-Use). The source
manuscript's Section 6.3 paragraphs 2–3 argue the opposite framing and were deliberately not
transferred to the LAK draft.

### 2. Add LA situating language

The paper needs a small number of learning-analytics citations so the work is visibly situated
in the field. The CFP states: "A paper that does not mention 'learning analytics' in its text
or references is highly likely to be out of scope."

This is not about changing the method or the claims. It is about showing LAK reviewers that
the author knows they are speaking to an LA audience and that the work matters to LA concerns
(stakeholder interpretation, pedagogical action, responsible use of educational data).

Required citations (none currently in references.bib):
- Gašević, Dawson, & Siemens (2015) — LA must connect to learning/teaching
- Lockyer, Heathcote, & Dawson (2013) — pedagogical action
- Ferguson & Clow (2017) — bounded proof-of-concept framing
- Drachsler & Greller (2016) — transparency, governance
- Prinsloo & Slade — ethics, non-use, contestability
- Tsai & Martinez-Maldonado (2022) — human-in-the-loop (optional)
- Butt et al. (2025) — adjacent ABSA method contrast

### 3. Miscellaneous ≠ unimportant

The source paper treats Miscellaneous as noise/contamination throughout. But content like
"I'll miss his quirkiness" or "too bad he retired" is real, meaningful student experience —
it is just not about pedagogy. Making this distinction explicit — preserve the content, separate
its role in a pedagogical reading from its role as an experience signal, do not dismiss it — is
a small writing change but reframes the ethics of the approach in a way LAK cares about deeply.

This is the strongest LAK-specific contribution and belongs in §2.3 (Design Principle) as the
ethical core of the framing.

## What does NOT need to change

- The method, equations, pipeline, and validation design are unchanged.
- The RQ framing is already appropriate (the LAK draft's RQs were rewritten but the originals
  were not far off — RQ3 asks "can" not "does").
- The limitations section is already honest and does not need softening.
- The claim language throughout the body is already careful. Do not over-correct into
  apologetic hedging — the tone should be "novel but careful," not tentative.

## Reviewer anticipation table

  Reviewer concern                                 Best response already available in the work
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  "Why adjust scores rather than analyze text?"    The contribution is moving from descriptive detection of
                                                   contamination to a transparent, bounded intervention on its modeled
                                                   influence.
 ───────────────────────────────────────────────  ─────────────────────────────────────────────────────────────────────
  "Is this truly learning analytics?"              It is analytics of teaching-feedback traces aimed at more
                                                   responsible interpretation of feedback for teaching improvement.
 ───────────────────────────────────────────────  ─────────────────────────────────────────────────────────────────────
  "Can it establish teaching quality?"             No; it does not claim to. It tests whether an interpretable
                                                   attenuation mechanism behaves consistently with a stated validity
                                                   argument.
 ───────────────────────────────────────────────  ─────────────────────────────────────────────────────────────────────
  "Why this formula/taxonomy?"                     The rule is intentionally simple, monotonic, auditable, and
                                                   grounded in construct-irrelevant variance; the paper documents its
                                                   limits rather than presenting it as universal.
 ───────────────────────────────────────────────  ─────────────────────────────────────────────────────────────────────
  "Why RMP?"                                       It is an intentionally difficult, noisy stress-test environment—not
                                                   a surrogate for institutional SET.
 ───────────────────────────────────────────────  ─────────────────────────────────────────────────────────────────────
  "Isn't the coarse expert result circular?"       Conceded in the paper before a reviewer raises it. The coarse
                                                   condition is presented as a sanity check; the validity claim rests
                                                   on the fine-grained condition and the permutation control.

## Handle the coarse expert condition candidly, not as the headline

The single sharpest attack available to a reviewer is that the coarse paired comparison is close to tautological.
Correctness is defined as the expert preferring the review the mechanism adjusted less. In the coarse bin
(|Δ| < 0.15 versus |Δ| ≥ 0.65) the contrast is usually a focused review against one visibly full of off-topic
content. Both a human and D_misc will detect that. The high coarse accuracy therefore mostly re-demonstrates that
ATC works—which is already established separately in the ATC validation—rather than showing that attenuation
tracks expert judgment of validity.

This is not a reason to drop the coarse condition. It is a reason to name its limits in the paper's own voice.

What to do:

- Report the coarse condition explicitly as a **manipulation check**: confirmation that the mechanism responds to
  gross differences in construct-irrelevant content in the direction the rationale predicts, and that experts
  perceive the same differences. That is a real and necessary result. It is simply not evidence of discrimination.

- Rest the validity claim on the **fine-grained condition** and the **permutation control**. These are the
  conditions where the mechanism could have failed. Lead the reporting with them even though the number is lower
  and less flattering.

- State the asymmetry as an expected property, not a disappointment: larger differences in off-topic content are
  easier for both experts and the mechanism to detect, so a gap between the two conditions is what the rationale
  predicts. A mechanism that scored equally on both would be the surprising result and would invite suspicion.

- Do **not** report a single pooled accuracy figure across both conditions. Pooling lets the near-tautological
  condition inflate the headline and is exactly what a skeptical reviewer will unpick.

Why this is worth the loss of glamour: a reviewer who finds this weakness unaided concludes the headline number was
oversold and re-reads everything else with suspicion. A paper that raises it first is read as self-aware, and the
concession costs little because the coarse condition was never carrying the argument.

The same principle applies wherever a result flatters the mechanism by construction. Where a metric is partly
definitional—D_misc correlating with Δ is the clearest case, since D_misc sets ζ—say so in the sentence that
reports it, rather than leaving the reader to notice.
