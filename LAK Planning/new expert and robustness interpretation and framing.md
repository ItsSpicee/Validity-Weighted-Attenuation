# New expert and robustness interpretation/framing

Surgical revision plan for the completed LAK manuscript — 6 September 2026

## Scope and central framing

Keep the title, structure, research questions, and contribution architecture. Fill the placeholders, update superseded numbers, and change only the interpretations affected by the expanded evaluation. The previous version of this document proposed too much restructuring.

The fine result becomes useful through its specificity: a defined task, observed agreement, two permutation benchmarks, and a diagnostic breakdown showing where disagreement occurs.

> The three-expert evaluation supports strong alignment on large model adjustment contrasts, while neither binning specification rejects its fine-grained permutation null. Within the fine condition, model–majority disagreements concentrate in pairs that also divide experts, although three occur despite unanimous judgments. This characterizes a limitation in the tested setting and provides a reproducible benchmark for subsequent improvements.

Call this **an empirically characterized limitation in close comparisons**, rather than an established discrimination threshold. The 0.5 cutoff defines the tested groups; these analyses did not estimate it as the point where discrimination stops. Lower fine-condition κ does not establish that the cutoff is optimal or reveal an expert-resolution ceiling.

Source: [expert_and_robustness_results.md](robust_validation_context/expert_and_robustness_results.md). Target: [LAK_draft/main.tex](LAK_draft/main.tex). This document plans the edits; it does not apply them.

## Six targeted edits to main.tex

| Location | Required edit |
|---|---|
| 1. Abstract, around line 102 | Replace expert placeholders and stale fine p=.007 with the overall 83% agreement, overall permutation p=.001, and the plain-language close-comparison limitation below. Keep the boundary clause and closing sentence as drafted. |
| 2. Expert Paired Comparisons, around lines 539–541 | Replace the TODO with a concise protocol paragraph, the consensus/κ table, and the compact disagreement diagnostic below. |
| 3. Permutation Control, around lines 548–567 | Replace single-expert numbers, retain the recomputed-bin test, and add supplementary fixed-bin results. Explain the coarse group-size/composition shift briefly. |
| 4. Discussion RQ3, around line 655 | Remove the fine “tiebreaker” success claim and coarse “only a manipulation check” interpretation. State the new coarse evidence, fine non-rejection, and concrete implication for future evaluation. |
| 5. Limitations, around line 714 | Replace the single-expert TODO and adjacent singular-expert wording with the panel and task limitations. Preserve the existing broader limitations. |
| 6. Numerical consistency throughout | Consistently report p=.001 for zero exceedances in 1,000 permutations, including the existing modulator rows and associated prose. Refresh the stale expert-sensitivity range and bootstrap intervals in the existing robustness section. |

Abstract replacement text:

> ...expert paired comparisons agreed with the relative magnitude of adjustment in 83% of pairs, exceeding the permutation null (p = .001); on close comparisons, agreement did not exceed the null.

Do not list 100% coarse agreement or the two subgroup p-values in the abstract. Keep the coarse result and its dependence on the binning specification in the results, where the curated comparison design and supplementary status of the fixed-bin analysis can be explained. Avoid “fine non-rejection under both specifications” in the abstract; reserve that terminology for the methods and results. Preserve the existing boundary clause and closing sentence.

The protocol should state documented pair construction and ATC verification, the raw-text task and blinding, randomized presentation, panel background and independent votes, majority rule, and scoring against smaller absolute attenuation. State the 80-to-77 inclusion accounting once. Confirm undocumented panel details rather than inventing them. Use the actual “both valid” response meaning; one such majority counts as incorrect. Among retained pairs, no votes or majorities are missing.

## Main expert table

| Condition | Correct/n | Majority agreement | 95% Wilson CI | Fleiss’ κ |
|---|---:|---:|---:|---:|
| Overall | 64/77 | 83.1% | 73.2–89.9% | .658 |
| Coarse | 43/43 | 100% | 91.8–100% | .819 |
| Fine | 21/34 | 61.8% | 45.0–76.1% | .469 |

Define coarse as an absolute-delta difference ≥0.5 and fine as [0, 0.5), at s=1. These are model adjustment contrasts, not independently measured differences in pedagogical validity. Use all-response κ in the main table; individual-expert scores and κ excluding label-3 votes can remain supporting detail.

## Permutation findings: preserve both interpretations compactly

| Condition | Observed | Recomputed null mean | p | Fixed null mean | p |
|---|---:|---:|---:|---:|---:|
| Overall | 83.1% | 63.3% | .001 | Identical overall test | — |
| Coarse | 100% | 84.9% | .180 | 68.9% | .001 |
| Fine | 61.8% | 59.9% | .378 | 56.3% | .321 |

**Coarse:** recomputation reduces the group from 43 to a mean of 10.51 pairs (range 3–20), leaving a mean of 66.49 fine pairs. These smaller, newly selected coarse groups retain high agreement; 179/1,000 achieve 100%. Holding the original 43 pairs fixed instead yields a lower null mean, with no shuffle matching observed agreement. Both size and composition change; the summaries do not isolate size as the sole cause.

**Fine:** neither specification rejects its respective null. This conclusion survives the binning choice. The tests use the same labels and shuffles, so they are not independent replications. Observed advantages over the null means are 1.9 and 5.5 percentage points.

Keep the original test visible and identify fixed bins as a supplementary sensitivity analysis added after the original results. Do not replace the original analysis because the fixed-bin coarse p-value is smaller. Both concern the specified density-assignment perturbation; neither proves that the density proxy is correct or that proportional attenuation outperforms simpler methods.

**Space decision:** use the compact table above, or retain the existing permutation table and add the fixed-bin coarse/fine means and p-values in one sentence. Put group-size details in the note or supporting material. No new standalone section is needed.

## Fine-condition disagreement diagnostic

Include a compact table after the main expert results, introduced as a post hoc descriptive analysis. These counts come from the earlier audit of pair-level labels and saved deltas; reproduce them against the final frozen data before publication.

| Expert voting pattern | Model agrees with majority | Model disagrees | Agreement |
|---|---:|---:|---:|
| Unanimous | 16 | 3 | 84.2% |
| Split | 5 | 10 | 33.3% |

Suggested results paragraph:

> To characterize the fine-condition disagreements, we examined model agreement with the expert majority by voting pattern. The model agreed on 16 of 19 unanimous pairs (84.2%) and 5 of 15 split-vote pairs (33.3%). Ten of the thirteen model–majority disagreements therefore occurred on pairs that also divided experts. Three disagreements remained despite unanimous expert judgments, showing that within-panel disagreement does not account for every discrepancy.

This locates errors that **co-occur with expert disagreement** and errors that **remain despite unanimity**. It does not causally separate task ambiguity from model limitations. Split-vote pairs still have a majority and remain errors under the chosen scoring rule; do not dismiss those ten cases as having no ground truth worth matching.

Suggested interpretive sentence:

> Disagreement may reflect differences between experts’ holistic validity judgments and the taxonomy-based relevance operationalized by the method, or limitations of the mechanism at small adjustment contrasts; the present design cannot distinguish these explanations.

Keep 21/34 as the primary fine result. The 84.2% unanimous-subset result is diagnostic, not a replacement headline or evidence of proximity to a measured performance ceiling. Unanimity is stronger panel agreement, not proof of objective validity.

## Make the fine finding a concrete foundation for future research

1. **Reproducible benchmark.** Preserve the pair set, labels, bin definitions, scoring rules, and both permutation specifications. Future versions can be compared on the same task, with independent data needed to validate improvements developed using these pairs.
2. **Specific diagnostic targets.** Inspect the three unanimous failures for model/proxy limitations and the fifteen split-vote pairs for contested judgments, using expert notes where available. Richer semantic representations, multi-label categorization, or alternative density measures are hypotheses to test, not explanations established by the table.
3. **Practical interpretation boundary.** Small adjustment differences have not been validated as fine validity orderings in this task. They call for inspection of original feedback and the audit trail. Coarse agreement does not authorize automatic decisions above 0.5 either.

The 1.9–5.5 percentage-point advantages are observed benchmark gaps, not reliable population effect estimates or a ready-made power calculation. Future sample planning should specify a meaningful improvement and account for uncertainty, clustering, and expert disagreement. Estimating an actual resolution threshold would require broader coverage across contrasts and an analysis designed to locate that threshold.

Suggested Discussion RQ3 replacement:

> The expanded evaluation provides strong expert alignment on large adjustment contrasts while identifying unresolved fine-grained discrimination. On the original coarse pairs, agreement exceeded the shuffled-density benchmark in the supplementary fixed-bin analysis (p=.001); the recomputed-bin analysis evaluated much smaller, changing coarse groups and did not reject its null (p=.180). Neither fine-condition analysis rejected its respective null (p=.378 and .321). Fine disagreements were concentrated in split-vote pairs, although three occurred despite unanimous judgments. Together, these findings provide a concrete benchmark for future improvements and indicate that small adjustment differences should not be interpreted as established validity orderings.

Retain the existing discussion of internal coherence and bootstrap stability alongside this paragraph, keeping those checks distinct from expert evidence.

## Limitations replacement and numerical housekeeping

Permutation p-value convention: use **p = .001** throughout the manuscript for zero exceedances in 1,000 shuffles, including the abstract, expert results, modulator table rows, captions, and discussion. The corrected value is 1/1001 ≈ .000999, so p < .001 is also numerically true; the choice of p = .001 is a consistent rounding convention, not a correction of an invalid inequality. Do not change unrelated p-values from other tests.

Suggested replacement for the panel limitation:

> The three-expert evaluation concerns relative review judgments on a small, curated pair set and does not validate exact adjustment magnitudes or teaching-quality inferences. Majority agreement remains conditional on this panel and the selection protocol, including verification of ATC assignments. Wilson intervals condition on these experts and assume independent pairs. The post hoc unanimity breakdown is descriptive, and the tested 0.5 contrast cutoff should not be interpreted as an estimated discrimination threshold.

Maintain the distinction between full-sample expert comparisons and held-out-instructor robustness. The separate ATC annotation study does not become three-expert merely because attenuation validation now has three experts.

Refresh sensitivity prose: overall agreement is **83.1–88.3%**, coarse remains **100%**, and fine varies **61.8–73.5%**, with bins fixed at s=1. Describe aggregate behaviour as relatively stable while acknowledging sensitivity in close comparisons; avoid “all results are exponent-independent.”

Refresh bootstrap intervals: positive/negative Pearson [.6514, .7202] and [−.7406, −.6715]; positive/negative Spearman [.5569, .6610] and [−.6493, −.5498]. Preserve their interpretation as internal relationships under professor resampling.

## Completion criterion

The six edits agree numerically and interpretively, the diagnostic counts are reproducible, and the abstract and discussion convey the same finding: **strong coarse alignment, fine non-rejection under both specifications, and a specific benchmark and disagreement pattern for subsequent research.** The existing paper remains intact; the new evidence makes its claims more precise.
