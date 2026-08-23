# Paper TODO

**Status:** the pipeline rerun is complete, on the corrected 17,127-review corpus
and with `s` fixed at 1.0. Every number needed to update the paper is in
`handoff.md` under "Current results (2026-08-22, final run)", with the raw
console output in `newresults.md`.

**Done since:** the figures are regenerated, `Paper/worked_examples.py` has run
and its consistency check passes (max |Delta_recomputed - Delta_pipeline| =
8.3e-17 against `attuned_ratings_full.csv` at s = 1.0), `ex1/ex2/ex3.tex` carry
the new values, and **every number in `main.tex` has been transcribed** — A1
through A4 are complete. See "State of Part A" below for what is left.

**Order of work:**

- **Part A** — regenerate figures, then update the existing paper in place.
  Numbers and wording only; no new sections. **A1-A4 done; A5, A6, A7 open.**
- **Part B** — start the LAK submission as a new file, assembling from the
  existing paper.
- **Part C** — blocked on the third expert's labels.
- **Part D** — decisions that need a judgement call, not a rerun.

Parts A and B are the work available now. Part C unblocks when the labels land.

---

# Part A — regenerate and update the existing paper

## State of Part A

**Done.** A1 (figures + worked examples), A2 (§4.2 fold table and the CV/test
sentence), A3 (§4.3 / §4.4 / §5.3 / §5.4 values), A4 (bin-partition and
threshold-dependence sentence). The itemised subsections below are kept as the
record of what was changed; they no longer describe outstanding work.

Values transcribed into `main.tex`, for cross-checking:

| Location | Value |
|---|---|
| §4.2 folds | 0.6396 / 0.6254 / 0.6373 / 0.6306 / 0.6172; mean 0.6300 +/- 0.0081, rho 0.7284 +/- 0.0152, R2 0.6255 +/- 0.0088 |
| §4.3.3 modulators | Delta+ vs D_misc 0.6872 / 0.6142; Delta- vs D_misc -0.7077 / -0.6001; Delta+ vs neg E_misc 0.4008 / 0.4327; Delta- vs pos E_misc -0.2470 / -0.1125 |
| §4.3.3 Mann-Whitney | U = 313,494, \|r\| = 0.789 (n = 690 / 508 unchanged) |
| §4.4 | coarse 43 / 3 unsure / 38 / 0.884; fine 34 / 1 / 24 / 0.706, p = 0.012 |
| §5.1 | Miscellaneous clause frequency 17,607 -> **17,602** (the only §5.1 number that moved) |
| §5.3 | 0.6347 / 0.7352 / 0.6168 |
| §5.4 | 10,375 (60.58%), mean Delta 0.0440, mean \|Delta\| 0.1964, max +2.7103, min -1.3908, min \|Delta\| 1.77e-6, Wilcoxon W = 24,260,091 |
| Discussion | SHAP shifts -9.6% Misc, +1.6 / +2.5 / +2.2 IE / F / W |
| §3.9 caption | +0.427, zeta = 0.550, -0.061 (matches `ex2.tex` / `ex3.tex`) |

Re-verified against the data and **unchanged**, so not edited: all other §5.1
figures (review frequencies, clauses-per-review, D_misc median 0.11 / mean 0.22,
the ~27% 1-star Miscellaneous gap), the §4.3.2 correlation-change wording
(signal +1.0-1.3%, noise -7.5 / -10.0%), and "the mean professor average
increases minimally" (+0.023).

**Open.** A5 (population labels), A6 (§3.5 case against total exclusion), and
**A7 in full** — §3.5 still describes the grid search and states `s` = 0.83,
§4.3's preamble still refers to "the grid search that selected `s`", and the
weak-identification limitation is still in §6. These were deliberately deferred,
not missed: the `s` write-up is the one remaining inconsistency between the
paper and the code.

## A1. Regenerate the figures

Nothing in the pipeline needs to rerun; the model and CSVs are current. Run:

```
python pipeline.py --visualize-only
python Paper/worked_examples.py
```

Regenerates `Diagrams/SHAP/`, `Diagrams/correlations/`,
`Diagrams/adjustment_visuals/` and the Section 3.9 worked examples in
`ex1/ex2/ex3.tex`.

`--optimize-s` no longer exists: `s` is fixed at 1.0 in `constants.py` and every
stage reads it from there, so no rerun can desynchronise the exponent.

If `pipeline.py` fails on a spaCy DLL block (Windows Smart App Control), run the
visualization modules directly instead - none of them import spaCy:

```
python -m src.visualizations.descriptive_plots
python -m src.visualizations.attenuation_plots
python -m src.visualizations.correlation_plots
```

`worked_examples.py` is the only cross-file consistency check in the repo and is
not wired into `pipeline.py` — it recomputes deltas from the model and warns if
the committed CSVs were produced at a different `s`. Run it and read its output;
it is the tripwire for the whole rerun.

One descriptive figure did change beyond a rerun. `topic-combinations.png` had
unreadable labels: `_load_exploded` already maps topics to display names, so the
second lookup in `plot_topic_combinations` was a no-op and the legend printed
"Workload = workload" against invisible white patches. `constants.py` now
carries `TOPIC_ABBREVIATIONS` (IE / W / F / M) and the plot abbreviates from
either the raw key or the display name. The figure's data is unchanged, so §5.1's
co-occurrence prose still holds as written.

Unchanged and needing no regeneration: every other descriptive figure,
`Diagrams/roberta/`, `Diagrams/atc_visuals/`, `Diagrams/Schematic_Diagrams/`.

## A2. Section 4.2 — CatBoost numbers and wording

| Location | Change |
|---|---|
| `main.tex:535` | Drop the "Early Stopping Rounds / 50" row from `tab:CatBoost-params` |
| `main.tex:523` | Weaken the hyperparameter-provenance claim. The exploratory CV that chose this configuration ran under the biased protocol, so say the configuration was fixed beforehand and not re-selected, rather than implying it was validated under the current one |
| `main.tex:543` | Describe fixed-iteration fitting instead of early stopping |
| `main.tex:545` | "No professor contributes reviews to both parameter selection and reported evaluation" — this is now true as written. Keep it |
| §3.5 (new sentence) | State that the iteration count is fixed at 1000 with no early stopping, and that the loss curve is flat over the final iterations (0.63700 -> 0.63698 -> 0.63697) so the cap is not performing selection |
| `main.tex:767` | Rewrite for fixed-iteration fitting. Also drop "controlling for overfitting across folds" — that is not what CV does here. Say it shows performance is consistent across professor subsets, and that the held-out MAE falls within the fold range, so CV and the final test agree rather than conflict |
| `main.tex:769-785` | New fold table (`tab:CatBoost`) — see `handoff.md` |
| `main.tex:1019` | New final MAE / rho / R2: **0.6347 / 0.7352 / 0.6168** |
| `main.tex:1024` | "low absolute error ... substantial explained variance" — re-checked against the new numbers, survives unchanged |

**Do not** write the CV/test ordering as a problem. CV mean 0.6300 against a
final test of 0.6347 is between-professor heterogeneity, not leakage, and the
test MAE now falls **inside** the fold range (0.6172-0.6396, SD 0.0081). The
folds tightened considerably on the corrected corpus, so the honest sentence is
simply that cross-validation and the held-out test agree. `handoff.md` has the
reasoning.

## A3. Section 4.3 / 4.4 / 5.4 — regenerated values

- `main.tex:568` — **`s` = 1.0, fixed a priori** (was 0.83, tuned). See A7.
- §4.3 correlation and modulator values, from the regenerated figures and
  `results/`. Modulator Pearson at the operating point: **0.6872** positive,
  **-0.7077** negative.
- §4.4 — 77 pairs, **80.5%** overall; coarse **38/43 = 88.4%**; fine
  **24/34 = 70.6%**, p = 0.0122.
- §5.4 adjustment statistics at `main.tex:1029`. The console prints only
  `max |delta|` **2.7103** and `mean |delta|` **0.1964** — the signed mean,
  signed max/min and smallest non-zero |delta| must be recomputed from
  `attuned_ratings_full.csv`, not transcribed.
- **The corpus is now genuinely 17,127** (was 17,132 in every earlier run — the
  preprocessing fix had never been applied because stages 1-3 were last run on
  9 August). Consequently `misc_d > 0` is now **10,375**, and the adjusted-review
  share is **60.58%**. Update both figures wherever they appear; the old 10,380 /
  60.59% pair is stale.
- Still usable as fixed anchors: all §4.1 ATC results (densities verified
  bit-identical for every shared review), the 823/206 professor split, and the
  3,414 / 2,052 / 77 reporting populations.

## A4. Section 4.4 — the bin-partition sentence

`FINE_DELTA_MAX` now equals `COARSE_DELTA_THRESHOLD` with a half-open fine bin,
so the two conditions partition the pairs instead of leaving a gap at (0.4, 0.5).
Section 4.4 should say so. The split came out **43 coarse / 34 fine** — neither
bin is small, so the paragraph does not need to hedge on sample size.

Also state that bin membership is **threshold-dependent**. The split was 45/32 at
s = 0.93 and moved to 43/34 at s = 1.0, purely because the deltas changed and
pairs crossed the 0.5 boundary. Both bins stayed significant and the fine bin
improved (68.8% -> 70.6%), so this is a disclosure, not a problem — but a
reviewer who reruns anything will see the *n*s move, and the paper should have
already said why.

## A7. Methods — `s` is now fixed, not tuned

The grid search is gone from the code (`--optimize-s`, `optimize_s()`, and the
`ALPHA`/`BETA`/`DELTA`/`LAMBDA`/`S_SEARCH_*` constants). The paper has to follow.

| Location | Change |
|---|---|
| §3.5 | State zeta = 1 - D_misc: the exponent is fixed at 1 so attenuation is exactly proportional to measured off-topic density. This is the Huber argument the section already makes, now instantiated rather than asserted |
| Methods — grid search | **Cut entirely.** The loss function, its weights, and the search range all go |
| Limitations — weak identification of `s` | **Cut.** No longer applicable; replace with one clause noting `s` is fixed, not estimated, and pointing at the sensitivity range |
| Limitations — in-criterion results | **Cut.** §4.3.2, §4.3.3 and the Mann-Whitney test are no longer terms in a fitted objective, so they can be claimed straightforwardly for the first time |
| `main.tex:545` | Simpler to state now — one fewer selected parameter |

Do **not** narrate the grid search's instability in the paper. "The exponent is
fixed at 1 rather than estimated" is true and sufficient. `handoff.md` records
the full reasoning if a reviewer asks directly.

What does **not** change: the deltas still come from a CatBoost model fit on
training professors, so §4.3 stays on held-out professors and `src/splits.py` is
untouched.

## A5. Population labels

Add explicit "full sample" labels to the external-validation and
adjustment-outcomes tables, for consistency with the held-out labelling used in
§4.2 and §4.3.

## A6. Section 3.5 — the case against total exclusion

The section asserts proportional attenuation is preferable to zeroing `E_misc`
and leaves it at the Huber citation. Strengthen it with a clause noting that
discarding forfeits the information in partially off-topic reviews and
introduces a discontinuity at `D_misc = 0`. See Part D for why no empirical
ablation accompanies this.

---

# Part B — the LAK submission

Assemble as a **new `.tex` file**, drawing from the existing paper rather than
editing it. The existing paper stays as the long-form record; the LAK version is
a selection from it.

## B1. Set up the file

- New file in `Paper/`, ACM `sigconf` format — **verify the current LAK template
  and page limit against the call for papers before laying anything out.** The
  12-page figure carried in these notes is a working assumption, not a checked
  requirement, and the limit drives every decision below.
- Reuse `Diagrams/` in place; no need to duplicate assets.
- `data.tex`, `pseudo.tex` and `ex1/ex2/ex3.tex` are includes and can be pulled
  in or dropped individually.

## B2. What earns space

Priority order if the page limit binds, carried over from the length-budget
analysis and updated with the current results:

**Keep:**
- The **permutation control**. It is the one addition that turns Section 4.3
  from a description of designed behaviour into evidence, and it compresses to a
  short paragraph plus one small table. With N = 1000 and p < 0.001 on all three
  metrics it is now the strongest single result in the paper.
- The **expert paired comparison** (§4.4). Load-bearing external validation.
- **Confidence intervals** once Part C lands — three extra columns in a table
  that already exists, so they cost almost nothing.

**Compress:**
- **Sensitivity Table A** (delta agreement) reduces to a sentence with the range
  quoted inline: r = 0.9524-0.9990 across `s` in [0.37, 1.2].
- **Table B** duplicates much of Table A's message; drop to a clause quoting the
  Pearson range 0.670-0.687. See Part D.
- **Section 3.9's three worked examples** are prose-heavy; one example plus an
  appendix pointer.

**Cut first:**
- **Sensitivity Table C.** See Part D. The operating point is now the *lowest*
  row in it (s = 1.0 -> 80.5%, against 0.62 -> 87.0%), so it needs a paragraph of
  defence to avoid undermining the choice of `s` — a poor use of a tight page
  budget.
- **The model-comparison table** (`main.tex:750-762`) if its provenance cannot
  be resolved, which also settles the orphaned-baselines problem.

## B3. Framing notes for the LAK audience

- The permuted expert-accuracy baseline is **0.6061, not 0.5**. State this
  explicitly when the permutation control is written up — the observed 0.8052 is
  a gain over ~0.61. A reader who computes against chance will overread it.
- Describe the permutation null as the **graded** one: "the amount of off-topic
  content is unrelated to which review it is", not "off-topic content is
  absent". This is the claim §4.3.3 and §4.4 make, and it is deliberate.
- `s` is **fixed at 1.0, not estimated** (see A7), so the weak-identification and
  in-criterion limitations from the long version both come out. Sensitivity Table
  A's range is the evidence the choice does not matter downstream.

---

# Part C — blocked on the third expert's labels

Nothing here is blocked on anything else. When the labels arrive:

## C1. Majority-vote label resolution in `src/validation.py`

Rule: majority of *cast* votes; ties resolve to unsure; unsure stays counted as
incorrect, matching the existing convention. Report how many pairs land in each
bucket.

**This must live in exactly one function that everything imports.** Stage 6, the
permutation control and sensitivity Table C all consume "what the expert said",
and three copies of the rule will drift — the same failure mode `src/splits.py`
was created to prevent for the professor split. Write it to auto-detect however
many label columns are present, so it runs unchanged with one expert or three.

## C2. Wilson confidence intervals

Currently `sidequestz/expert_confidence_intervals.py`, kept there so it stays
runnable against the single-expert file; fold it into `src/validation.py`.
n = 77 is small enough that a reviewer will ask how stable the accuracy is. The
claim to make is that the lower bound clears 0.5.

Expect the fine-grained condition's interval to straddle 0.5 (24/34 = 70.6%).
Those are pairs the model nearly could not separate, so low accuracy there is
the expected shape — accuracy rising with the size of the separation is itself
evidence that `|delta|` carries graded information. Write it that way rather
than as an independent success.

## C3. Inter-rater agreement, and reframing §4.4 around it

Three raters give mean pairwise agreement or Fleiss' kappa — roughly twenty
lines, no new dependency. This matters more than it sounds. At present the
model's accuracy is implicitly benchmarked against a 100% ceiling, which is the
wrong comparison. If three trained experts agree with each other ~75% of the
time, that is the ceiling. "The model agrees with expert consensus about as
often as experts agree with one another" is a much stronger and more defensible
claim than a bare accuracy figure, and it costs nothing beyond labels already
being collected. Plan the §4.4 rewrite around it.

Note this compounds with the permutation baseline in B3: the model's 80.5% then
sits between a null of ~0.63 and a human ceiling, which is a far more honest
frame than 80.5% against 50%.

## C4. Confirm the three dropped pairs

`review_id` not found in attuned data: 14144/18846, 13330/678, 18844/7083,
leaving 77 of 80. Likely `misc_d = 0` reviews and legitimately absent, but
unconfirmed, and the paper mentions no exclusions. Either confirm and state the
exclusion, or recover the pairs.

---

# Part D — decisions, not reruns

## D1. The model-comparison table has no generating code

Nothing in the repo produces the Ordinal / Linear / RF / XGBoost / CatBoost rows
at `main.tex:750-762`, so the four baselines cannot be regenerated under the
corrected protocol, and CatBoost's 0.6492 there will not match anything else in
the paper. The paper carries three unexplained CatBoost MAEs (0.6492, 0.6369,
CV mean 0.6300).

Decide between regenerating all five under one protocol, footnoting the table's
provenance, and dropping it.

**The pressure is off**: XGBoost's 0.6710 is still comfortably above the honest
CatBoost 0.6347, so the selection argument at `main.tex:764` is not contradicted
by the new numbers. This is now a tidiness and page-budget decision rather than
a correctness one.

## D2. Sensitivity Table C undercuts the choice of `s` unless defended

The operating point has the **lowest** expert accuracy of every value tested:
s = 1.0 -> 80.5%, against 0.37 -> 85.7%, 0.62 -> 87.0%, 0.91 -> 84.4%,
1.2 -> 83.1%. A reviewer will ask why not 0.62.

The answer is the same one that rejected the total-exclusion ablation below:
**the validation metric is not scale-free.** Smaller `s` attenuates harder,
producing larger deltas, larger `delta_diff`, and more pairs in the regime where
the paired comparison is easy. So 0.37's 87% partly measures how aggressively it
adjusts rather than how well it measures.

Note the argument is directionally right but not clean: s = 1.2 attenuates even
less than 1.0 yet scores *higher* (83.1%), so scale explains the trend and noise
on 77 pairs explains the rest. That is a messy sentence to write. Given the page
budget, cutting the table is the cheaper resolution.

## D3. Table B invites the same question in a second form

At `s` = 1.2 the modulator correlations are marginally stronger on some columns
(negative Pearson -0.7145 vs -0.7077 at the operating point; negative Spearman
-0.6519 vs -0.6001).

This is now a much smaller problem than it was, because `s` is no longer chosen
by maximising anything — so there is no argmin to defend. The answer is simply
that `s` is fixed on measurement-theoretic grounds and Table B shows the
modulator relationship holds across the whole range (Pearson 0.670-0.687
positive, -0.669 to -0.715 negative). Flatness is the message.

Quote Table B as an inline range (Pearson 0.670-0.687 across `s`, i.e. flat)
rather than printing the table.

## D4. No empirical ablation against total exclusion — settled, keep it settled

An ablation was considered and **rejected**, for two reasons worth keeping on
record.

First, the validation metric is not scale-free (see D2): total exclusion
produces larger deltas, larger deltas shift pairs into the easy regime, so the
comparison would partly reward aggressive attenuation for reasons unrelated to
measurement quality. "Total exclusion scores higher" would be close to
uninterpretable.

Second, proportional down-weighting is a measurement-theoretic commitment
following Huber's robust-estimation argument, not a hypothesis to settle by
whichever variant maximises a downstream accuracy number. Validating it that way
would be optimising the wrong objective. The answer stays principled — see A6.

For the record, it would have been nearly free: total exclusion is the `s -> 0`
limit of the existing family, since zeta = 1 - D^s tends to 0 for any D > 0 as
`s` tends to 0, so it is one extra row in the stage 7 sensitivity tables. The
decision is about what the test would mean, not what it would cost.

## D5. `SENSITIVITY_S_VALUES` — closed

Now `[0.37, 0.62, 0.91, 1.2]`, and **not to be re-derived**. The instruction to
re-derive assumed the modes came from code in the repo; they came from a deleted
throwaway diagnostic present in no commit. The finding stands anyway —
multimodality is a property of the loss surface, not of the fitted model — and
the values are spread comparison points rather than estimates. `constants.py`
carries the full reasoning. The list is `[0.37, 0.62, 0.91, 1.2]` and stage 7
adds `S_VALUE` at runtime, so the tables bracket the 1.0 operating point on both
sides without further edits.
