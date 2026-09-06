"""Focused checks plus a real-data smoke run for the permutation extension."""
import contextlib
import importlib.util
import io
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root))
import numpy as np
import pandas as pd

spec = importlib.util.spec_from_file_location('updated_robustness', Path(__file__).with_name('robustness.py'))
updated = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updated)
from src import robustness as original

index = pd.MultiIndex.from_tuples([(1, 2), (3, 4), (5, 6)], names=updated.PAIR_KEYS)
reference = pd.DataFrame(dict(evaluable=[True]*3, missing_delta=[False]*3,
                              delta_diff=[.7, .2, .1], correct=[True, True, False]), index=index)
variant = reference.copy()
variant['delta_diff'] = [.1, .8, .9]
variant['correct'] = [False, True, True]
dynamic = updated._expert_counts(variant)
fixed = updated._expert_counts(variant.iloc[::-1], reference)
assert dynamic == {'overall': (2, 3), 'coarse': (2, 2), 'fine': (0, 1)}
assert fixed == {'overall': (2, 3), 'coarse': (0, 1), 'fine': (2, 2)}
try:
    updated._expert_counts(variant.iloc[1:], reference)
except ValueError:
    pass
else:
    raise AssertionError('Missing reference pair should fail')
with contextlib.redirect_stdout(io.StringIO()):
    empty = updated._summarise_permutation(pd.DataFrame({'x':[np.nan]*3}), 'x', .5, 'greater')
assert np.isnan(empty['p_value']) and empty['n_valid'] == 0

# Ensure the user's sensitivity implementation is unchanged verbatim.
old_text = (root/'src/robustness.py').read_text(encoding='utf-8')
new_text = Path(__file__).with_name('robustness.py').read_text(encoding='utf-8')
def sensitivity_block(text):
    return text[text.index('def table_expert_accuracy('):text.index('# BOOTSTRAP PROFESSOR STABILITY')]
assert sensitivity_block(old_text) == sensitivity_block(new_text)

model = updated.CatBoostRegressor()
model.load_model(str(updated.CATBOOST_FINAL_MODEL), format='cbm')
df = pd.read_csv(updated.FINAL_EMOTIONS)
_, professors = updated.professor_split(df)
true_d = df.set_index('review_id')[updated.MISC_D_COL]
observed, pairs = updated._permutation_measure(model, df, professors, true_d)
reference = pairs.loc[pairs.evaluable].copy()
assert observed['expert_coarse_n'] == 43 and observed['expert_fine_n'] == 34
assert observed['expert_accuracy'] == 64/77
rng = np.random.default_rng(updated.PERMUTATION_SEED)
for _ in range(3):
    variant = df.copy()
    vals = variant[updated.MISC_D_COL].to_numpy().copy()
    nz = np.flatnonzero(vals > 0)
    vals[nz] = rng.permutation(vals[nz])
    variant[updated.MISC_D_COL] = vals
    old = original._permutation_measure(model, variant, professors, true_d)
    new, _ = updated._permutation_measure(model, variant, professors, true_d, reference=reference)
    assert (new['expert_accuracy'], new['expert_coarse'], new['expert_fine'], new['expert_accuracy_n']) == old[:4]
    assert new['expert_accuracy_fixed'] == new['expert_accuracy']
    assert new['expert_coarse_fixed_n'] == 43 and new['expert_fine_fixed_n'] == 34
    assert new['expert_coarse_n'] + new['expert_fine_n'] == 77
    for key, value in old[4].items():
        assert new[key] == value

with Path(__file__).with_name('smoke_report.txt').open('w', encoding='utf-8') as f, contextlib.redirect_stdout(f):
    summary = updated.permutation_control(model, df, professors, n_permutations=20)
assert len(summary) == 7
assert summary.n_valid.eq(20).all()
print('PASS: bin crossing, pair-ID alignment, missing-pair guard, empty null, unchanged sensitivity,')
print('original metrics preserved on three real shuffles, fixed denominators, and 20-permutation smoke run.')
