"""Museum-confound tests on DINOv2 ViT-B/14 mask embeddings (tablets only).
(1) museum predictability within period x findspot; (2) period classification, random vs museum-held-out CV;
(3) share of non-Neo-Assyrian British Museum tablets predicted Neo-Assyrian."""
import os, time, numpy as np, pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, StratifiedGroupKFold, cross_val_predict
from sklearn.metrics import balanced_accuracy_score, accuracy_score, f1_score, recall_score

t0 = time.time()
ROOT = os.path.expanduser('~/deeplomatics-repro')
OUT = f'{ROOT}/museum_tests'
SEED = 0
emb = np.load(f'{ROOT}/results/emb_dinov2_vitb14_224.npy')
ids = pd.read_csv(f'{ROOT}/results/emb_dinov2_vitb14_224_ids.csv')
ids['row'] = np.arange(len(ids))
art = pd.read_csv(os.path.expanduser('~/Dropbox/Git-projects/ShapingHistory/artifacts.csv'),
                  usecols=['artifact_id', 'period', 'provenience', 'collections', 'genres', 'artifact_type'], low_memory=False)
df = ids.merge(art, left_on='CDLI_id', right_on='artifact_id')
df = df[df.artifact_type.isin(['tablet', 'tablet & envelope'])].reset_index(drop=True)
df['per'] = df.period.fillna('').str.split(' (', regex=False).str[0].str.strip()
df['city'] = df.provenience.fillna('uncertain').str.split(' (', regex=False).str[0].str.strip()
df['museum'] = df.collections.fillna('unknown').str.split(';').str[0].str.strip()
X = emb[df.row.values]
print('tablets:', len(df))

def clf(): return make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000))

# (1)
rows = []
for per, city in [('Ur III', 'Puzriš-Dagan'), ('Ur III', 'Umma'), ('Ur III', 'Girsu'), ('Old Babylonian', 'Sippar-Yahrurum'),
                  ('Old Babylonian', 'Nippur'), ('Neo-Babylonian', 'uncertain')]:
    g = df[(df.per == per) & (df.city == city)]
    vc = g.museum.value_counts()
    top = vc[vc >= 60].index[:5]
    if len(top) < 2:
        rows.append(dict(period=per, city=city, n_museums=len(top))); continue
    m = vc[top].min()
    s = pd.concat([g[g.museum == mu].sample(m, random_state=SEED) for mu in top])
    yp = cross_val_predict(clf(), X[s.index], s.museum.values, cv=StratifiedKFold(5, shuffle=True, random_state=SEED))
    rows.append(dict(period=per, city=city, n_museums=len(top), n_per_museum=m, balanced_acc=balanced_accuracy_score(s.museum, yp),
                     chance=1 / len(top), museums=' | '.join(f'{mu} ({vc[mu]})' for mu in top)))
t1 = pd.DataFrame(rows); t1.to_csv(f'{OUT}/test1_museum_within_period_site.csv', index=False)

# (2)
PERIODS = ['ED IIIb', 'Ebla', 'Old Akkadian', 'Ur III', 'Early Old Babylonian', 'Old Babylonian', 'Old Assyrian',
           'Middle Babylonian', 'Middle Assyrian', 'Neo-Assyrian', 'Neo-Babylonian', 'Achaemenid']
p = df[df.per.isin(PERIODS)]
p = pd.concat([g.sample(min(len(g), 3000), random_state=SEED) for _, g in p.groupby('per')])
Xp, yp_true, grp = X[p.index], p.per.values, p.museum.values
preds, summ = {}, []
for name, cv in [('random', StratifiedKFold(5, shuffle=True, random_state=SEED)),
                 ('museum_held_out', StratifiedGroupKFold(5, shuffle=True, random_state=SEED))]:
    pr = cross_val_predict(clf(), Xp, yp_true, cv=cv, groups=grp if name != 'random' else None, n_jobs=5)
    preds[name] = pr
    summ.append(dict(split=name, n=len(p), accuracy=accuracy_score(yp_true, pr), macro_f1=f1_score(yp_true, pr, average='macro')))
t2 = pd.DataFrame(summ)
rec = pd.DataFrame({k: recall_score(yp_true, v, labels=PERIODS, average=None) for k, v in preds.items()}, index=PERIODS)
rec['n'] = pd.Series(yp_true).value_counts().reindex(PERIODS).values
t2.to_csv(f'{OUT}/test2_period_summary.csv', index=False); rec.to_csv(f'{OUT}/test2_period_recall.csv')
p.assign(pred_random=preds['random'], pred_museum_held_out=preds['museum_held_out'])[
    ['CDLI_id', 'per', 'city', 'museum', 'pred_random', 'pred_museum_held_out']].to_csv(f'{OUT}/test2_predictions.csv', index=False)

# (3)
q = p.assign(pred=preds['random'])
q = q[q.per != 'Neo-Assyrian']
bm = q.museum == 'British Museum, London, UK'
t3 = pd.DataFrame([dict(group='British Museum', n_non_NA=int(bm.sum()), share_pred_NA=(q[bm].pred == 'Neo-Assyrian').mean()),
                   dict(group='other museums', n_non_NA=int((~bm).sum()), share_pred_NA=(q[~bm].pred == 'Neo-Assyrian').mean())])
t3_by = q[bm].groupby('per').apply(lambda g: pd.Series(dict(n=len(g), share_pred_NA=(g.pred == 'Neo-Assyrian').mean())))
t3.to_csv(f'{OUT}/test3_bm_predicted_NA.csv', index=False); t3_by.to_csv(f'{OUT}/test3_bm_predicted_NA_by_period.csv')

pd.set_option('display.width', 250); pd.set_option('display.precision', 3); pd.set_option('display.max_colwidth', 120)
print(t1.to_string(index=False)); print(t2.to_string(index=False)); print(rec.to_string())
print(t3.to_string(index=False)); print(t3_by.to_string())
print(f'runtime {time.time() - t0:.0f}s')
