=== Stage 6: Validation ===
Pairs: 77; no majority: 0; non-directional majority: 1; missing model deltas: 0; evaluable: 77

=== Three-expert attenuation validation ===
condition  n_total  n_complete  n_missing  observed_agreement  expected_agreement  fleiss_kappa
  Overall       77          77          0            0.818182            0.467926      0.658284
   Coarse       43          43          0            0.906977            0.486329      0.818905
     Fine       34          34          0            0.705882            0.446559      0.468565

Generalized Fleiss' kappa excluding individual label-3 votes:
condition  n_total  n_agreement_pairs  n_marginal_pairs  n_two_raters  n_three_raters  n_one_rater  n_zero_raters  n_excluded_3  n_blank_votes  observed_agreement  expected_agreement  generalized_fleiss_kappa
  Overall       77                 76                77             9              67            1              0            11              0            0.903509            0.509005                  0.803478
   Coarse       43                 43                43             4              39            0              0             4              0            0.968992            0.515894                  0.935948
     Fine       34                 33                34             5              28            1              0             7              0            0.818182            0.503076                  0.634113
Pairs with one retained vote contribute only to chance agreement; pairs with zero retained votes are excluded.
Pairs without model deltas (overall kappa only): 0

Accuracy and two-sided 95% Wilson intervals:
No-majority and label-3-majority pairs with model deltas count as incorrect.
Individual label-3 votes count as incorrect; blank votes are excluded.
         target condition  n  correct  accuracy  confidence   ci_low  ci_high
consensus_label   Overall 77       64  0.831169        0.95 0.732271 0.898593
consensus_label    Coarse 43       43         1        0.95  0.91799        1
consensus_label      Fine 34       21  0.617647        0.95  0.45041 0.760998
       expert_1   Overall 77       62  0.805195        0.95 0.703149 0.878236
       expert_1    Coarse 43       38  0.883721        0.95 0.755208 0.949296
       expert_1      Fine 34       24  0.705882        0.95 0.538311 0.831654
       expert_2   Overall 77       64  0.831169        0.95 0.732271 0.898593
       expert_2    Coarse 43       43         1        0.95  0.91799        1
       expert_2      Fine 34       21  0.617647        0.95  0.45041 0.760998
       expert_3   Overall 77       62  0.805195        0.95 0.703149 0.878236
       expert_3    Coarse 43       42  0.976744        0.95  0.87941 0.995883
       expert_3      Fine 34       20  0.588235        0.95 0.422216  0.73634

=== Stage 7: Robustness ===
Loading model and data...

  s values: [0.5, 0.75, 1.0, 1.25, 1.5]   (pipeline uses S_VALUE = 1.0)
  Held-out misc reviews: 2,052

==================================================================
  Delta agreement across s (held-out professors)
==================================================================

 $s_a$  $s_b$  Pearson $r$  Spearman $\rho$  Mean $|\Delta_a - \Delta_b|$  Max $|\Delta_a - \Delta_b|$
0.5000 0.7500       0.9914           0.9165                        0.0427                       0.4066
0.5000 1.0000       0.9803           0.8243                        0.0629                       0.8358
0.5000 1.2500       0.9712           0.7545                        0.0742                       1.0260
0.5000 1.5000       0.9635           0.6887                        0.0830                       1.1482
0.7500 1.0000       0.9953           0.9198                        0.0294                       0.4292
0.7500 1.2500       0.9899           0.8479                        0.0425                       0.6194
0.7500 1.5000       0.9845           0.7805                        0.0521                       0.7416
1.0000 1.2500       0.9973           0.9165                        0.0216                       0.2654
1.0000 1.5000       0.9941           0.8528                        0.0311                       0.3719
1.2500 1.5000       0.9982           0.9190                        0.0168                       0.1729

==================================================================
  Modulator correlations across s (held-out professors)
==================================================================

   $s$  $\Delta^+$ Pearson $r$  $\Delta^+$ Spearman $\rho$  $\Delta^-$ Pearson $r$  $\Delta^-$ Spearman $\rho$
0.5000                  0.6765                      0.5046                 -0.6880                     -0.5020
0.7500                  0.6837                      0.5756                 -0.7031                     -0.5421
1.0000                  0.6872                      0.6142                 -0.7077                     -0.6001
1.2500                  0.6858                      0.6557                 -0.7094                     -0.6464
1.5000                  0.6769                      0.6800                 -0.7167                     -0.6942

==================================================================
  Expert paired-comparison accuracy across s (full sample)
==================================================================

   s       Overall    Coarse    Fine
  ━━━━━━  ━━━━━━━━━  ━━━━━━━━  ━━━━━━━━
   0.50    0.8831     1.0000    0.7353
  ──────  ─────────  ────────  ────────
   0.75    0.8831     1.0000    0.7353
  ──────  ─────────  ────────  ────────
   1.00    0.8312     1.0000    0.6176
  ──────  ─────────  ────────  ────────
   1.25    0.8701     1.0000    0.7059
  ──────  ─────────  ────────  ────────
   1.50    0.8701     1.0000    0.7059

  Observed (true D_misc), s = 1.0...
Pairs: 77; no majority: 0; non-directional majority: 1; missing model deltas: 0; evaluable: 77
    Expert accuracy (overall) : 0.8312  (n = 77)
    Expert accuracy (coarse)  : 1.0000
    Expert accuracy (fine)    : 0.6176
    Delta+ vs D_misc (r)      : 0.6872
    Delta- vs D_misc (r)      : -0.7077

  Running 1000 permutations of D_misc...
    10/1000
    ...
    1000/1000
==================================================================
  PERMUTATION CONTROL
==================================================================
  Test 1: bins recomputed after each permutation

  expert_accuracy subgroup size: observed=77; mean=77.00, SD=0.00, min=77, max=77, empty=0

  expert_accuracy
    observed        : 0.8312
    permuted mean   : 0.6330  (SD 0.0490)
    permuted range  : [0.4805, 0.7662]
    valid permutations: 1000/1000
    permutations reaching observed: 0/1000   p = 0.0010

  expert_coarse subgroup size: observed=43; mean=10.51, SD=2.85, min=3, max=20, empty=0

  expert_coarse
    observed        : 1.0000
    permuted mean   : 0.8491  (SD 0.1087)
    permuted range  : [0.4444, 1.0000]
    valid permutations: 1000/1000
    permutations reaching observed: 179/1000   p = 0.1798

  expert_fine subgroup size: observed=34; mean=66.49, SD=2.85, min=57, max=74, empty=0

  expert_fine
    observed        : 0.6176
    permuted mean   : 0.5988  (SD 0.0541)
    permuted range  : [0.4308, 0.7619]
    valid permutations: 1000/1000
    permutations reaching observed: 377/1000   p = 0.3776

  Test 2: bins fixed at observed s=1.0 (same shuffles)
  Overall accuracy is identical to Test 1; only subgroup tests are repeated.

  expert_coarse_fixed fixed subgroup size: 43

  expert_coarse_fixed
    observed        : 1.0000
    permuted mean   : 0.6887  (SD 0.0628)
    permuted range  : [0.4884, 0.8837]
    valid permutations: 1000/1000
    permutations reaching observed: 0/1000   p = 0.0010

  expert_fine_fixed fixed subgroup size: 34

  expert_fine_fixed
    observed        : 0.6176
    permuted mean   : 0.5625  (SD 0.0751)
    permuted range  : [0.2941, 0.7941]
    valid permutations: 1000/1000
    permutations reaching observed: 320/1000   p = 0.3207

  pos_pearson
    observed        : 0.6872
    permuted mean   : 0.2327  (SD 0.0291)
    permuted range  : [0.1278, 0.3235]
    valid permutations: 1000/1000
    permutations reaching observed: 0/1000   p = 0.0010

  neg_pearson
    observed        : -0.7077
    permuted mean   : -0.1579  (SD 0.0374)
    permuted range  : [-0.2744, -0.0476]
    valid permutations: 1000/1000
    permutations reaching observed: 0/1000   p = 0.0010

  Bootstrap professor stability (1000 iterations)...
    100/1000
    ...
    1000/1000

==================================================================
  BOOTSTRAP PROFESSOR STABILITY (held-out professors)
==================================================================

  Δ+ vs D_misc (Pearson r)
    mean: 0.6869   SD: 0.0174
    95% CI: [0.6514, 0.7202]

  Δ- vs D_misc (Pearson r)
    mean: -0.7073   SD: 0.0181
    95% CI: [-0.7406, -0.6715]

  Δ+ vs D_misc (Spearman ρ)
    mean: 0.6132   SD: 0.0265
    95% CI: [0.5569, 0.6610]

  Δ- vs D_misc (Spearman ρ)
    mean: -0.6005   SD: 0.0252
    95% CI: [-0.6493, -0.5498]