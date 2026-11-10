"""Do OB document forms (Archibab types) continue into other periods? Nearest-OB-form assignment of non-OB Letter/Legal/
Administrative tablets, with a museum control: within each (period, museum), share of genre-G tablets nearest the matching
OB form minus the share of the other tablets nearest it; n-weighted mean over museums, 95% bootstrap CI.
Spaces: DINOv2 768-d L2-normalised (cosine) and PCA-12 z-scored (Euclidean)."""
import os, numpy as np, pandas as pd
from sklearn.decomposition import PCA

ROOT = os.path.expanduser('~/deeplomatics-repro'); OUT = f'{ROOT}/archibab'
SEED, NBOOT = 0, 1000
rng = np.random.default_rng(SEED)
ids = pd.read_csv(f'{ROOT}/results/emb_dinov2_vitb14_224_ids.csv').CDLI_id.values
emb = np.load(f'{ROOT}/results/emb_dinov2_vitb14_224.npy').astype(np.float64)
pos = pd.Series(np.arange(len(ids)), index=ids)
art = pd.read_csv(os.path.expanduser('~/Dropbox/Git-projects/ShapingHistory/artifacts.csv'), low_memory=False,
                  usecols=['artifact_id', 'period', 'collections', 'genres', 'artifact_type'])
T = art[art.artifact_id.isin(ids) & art.artifact_type.isin(['tablet', 'tablet & envelope'])].set_index('artifact_id')
T['per'] = T.period.fillna('').str.split(' (', regex=False).str[0].str.strip()
T['museum'] = T.collections.fillna('unknown').str.split(';').str[0].str.strip()
T['genre'] = T.genres.fillna('').str.strip()
Z = PCA(12, random_state=SEED).fit_transform(emb[pos.loc[T.index].values]); Z = (Z - Z.mean(0)) / Z.std(0)   # as earlier runs
SPACES = {'DINOv2_full_cosine': pd.DataFrame(emb[pos.loc[T.index].values] / np.linalg.norm(emb[pos.loc[T.index].values], axis=1, keepdims=True), index=T.index),
          'DINOv2_pca12z_euclid': pd.DataFrame(Z, index=T.index)}

FORMS = {'lettre': 'letter', 'prêt à intérêt': 'loan', 'prêt autre': 'loan', 'achat': 'purchase', 'location': 'lease', 'fermage': 'lease',
         'reçu': 'receipt', 'quittance': 'receipt', 'dépense': 'expenditure', 'compte récapitulatif': 'account', 'liste de personnes': 'list'}
L = pd.read_csv(f'{OUT}/cdli_archibab_linked.csv')
L = L[L.in_photo_dataset & L.artifact_type.isin(['tablet', 'tablet & envelope']) & L.period.fillna('').str.startswith('Old Babylonian')]
L = L.drop_duplicates('artifact_id').assign(form=lambda d: d.type.str.strip().map(FORMS),
                                            museum=lambda d: d.collections.fillna('unknown').str.split(';').str[0].str.strip()).dropna(subset=['form'])
PERIODS = ['Ur III', 'Old Akkadian', 'Old Assyrian', 'Early Old Babylonian', 'Middle Babylonian', 'Middle Assyrian', 'Neo-Assyrian',
           'Neo-Babylonian', 'Achaemenid', 'Hellenistic']
PAIRS = [('Letter', ['letter']), ('Legal', ['loan']), ('Legal', ['purchase']), ('Legal', ['lease']), ('Legal', ['loan', 'purchase', 'lease'])]
Q = T[T.genre.isin(['Letter', 'Legal', 'Administrative']) & T.per.isin(PERIODS)]

rows, cent_rows = [], []
for sp, X in SPACES.items():
    cents, names = [], []
    for f, g in L.groupby('form'):
        mm = [X.loc[h.artifact_id].values.mean(0) for _, h in g.groupby('museum') if len(h) >= 5]
        cent_rows.append(dict(space=sp, form=f, n=len(g), n_museums_ge5=len(mm)))
        if len(mm) >= 2: cents.append(np.mean(mm, 0)); names.append(f)
    C = np.stack(cents)
    Xq = X.loc[Q.index].values
    near = np.array(names)[(Xq @ (C / np.linalg.norm(C, axis=1, keepdims=True)).T).argmax(1) if sp.endswith('cosine')
                           else ((Xq[:, None] - C[None]) ** 2).sum(-1).argmin(1)]
    q = Q.assign(near=near)
    for per in PERIODS:
        for G, fs in PAIRS:
            if not set(fs) <= set(names): continue
            mus = []
            for m, h in q[q.per == per].groupby('museum'):
                hit = h.near.isin(fs).values; isg = (h.genre == G).values
                if isg.sum() >= 20 and (~isg).sum() >= 20: mus.append((m, hit, isg))
            if not mus:
                rows.append(dict(space=sp, period=per, genre=G, form='+'.join(fs), n_museums=0, n=0)); continue
            ex = lambda hit, isg: hit[isg].mean() - hit[~isg].mean()
            e = np.array([ex(h, g) for _, h, g in mus]); w = np.array([len(h) for _, h, _ in mus], float)
            est = (e * w).sum() / w.sum()
            if len(mus) > 1:
                bi = rng.integers(0, len(mus), (NBOOT, len(mus))); boot = (e[bi] * w[bi]).sum(1) / w[bi].sum(1)
            else:
                _, h, g = mus[0]; gi, oi = np.where(g)[0], np.where(~g)[0]
                boot = np.array([h[rng.choice(gi, len(gi))].mean() - h[rng.choice(oi, len(oi))].mean() for _ in range(NBOOT)])
            rows.append(dict(space=sp, period=per, genre=G, form='+'.join(fs), excess=est, lo=np.percentile(boot, 2.5), hi=np.percentile(boot, 97.5),
                             n_museums=len(mus), n=int(w.sum()), n_genre=int(sum(g.sum() for _, _, g in mus)),
                             share_genre=np.average([h[g].mean() for _, h, g in mus], weights=w),
                             share_other=np.average([h[~g].mean() for _, h, g in mus], weights=w)))
R = pd.DataFrame(rows); R.to_csv(f'{OUT}/04_doc_forms_across_periods.csv', index=False)
pd.DataFrame(cent_rows).to_csv(f'{OUT}/04_ob_form_centroids.csv', index=False)
pd.set_option('display.width', 220); pd.set_option('display.precision', 3); pd.set_option('display.max_rows', 300)
print(pd.DataFrame(cent_rows).to_string(index=False)); print(R.to_string(index=False))
