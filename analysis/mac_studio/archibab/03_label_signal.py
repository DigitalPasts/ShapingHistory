"""Which Archibab labels does tablet shape carry ACROSS museums, within OB? (linked photographed OB/EOB tablets)
Statistic per label value (>= 8 tablets in >= 2 museums): mean pairwise distance between tablets with that value held in
different museums. Null: 500 permutations of the label within strata (museum x the other labels). p = share of perms <= obs.
Spaces: DINOv2 PCA-12 z-scored (Euclidean) and full 768-d L2-normalised (cosine)."""
import os, re, unicodedata, numpy as np, pandas as pd
from sklearn.decomposition import PCA
from scipy.spatial.distance import pdist, squareform

ROOT = os.path.expanduser('~/deeplomatics-repro'); OUT = f'{ROOT}/archibab'
SEED, NPERM, MIN_N = 0, 500, 8
rng = np.random.default_rng(SEED)
fold = lambda s: unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode().lower().replace('-', '').replace(' ', '')
ALIAS = {'babilim': 'babylon', 'kis': 'kish', 'susum': 'susa', 'alahtum': 'alalakh', 'sipparyahrurum': 'sippar', 'sipparamnanum': 'sippar', 'yahrurum': 'sippar'}
canon = lambda s: ALIAS.get(fold(s), fold(s))

ids = pd.read_csv(f'{ROOT}/results/emb_dinov2_vitb14_224_ids.csv').CDLI_id.values
emb = np.load(f'{ROOT}/results/emb_dinov2_vitb14_224.npy').astype(np.float64)
pos = pd.Series(np.arange(len(ids)), index=ids)
art = pd.read_csv(os.path.expanduser('~/Dropbox/Git-projects/ShapingHistory/artifacts.csv'), low_memory=False, usecols=['artifact_id', 'artifact_type'])
T = art[art.artifact_id.isin(ids) & art.artifact_type.isin(['tablet', 'tablet & envelope'])].artifact_id.values
Z = PCA(12, random_state=SEED).fit_transform(emb[pos.loc[T].values]); Z = (Z - Z.mean(0)) / Z.std(0)   # same as earlier runs
Z = pd.DataFrame(Z, index=T)

L = pd.read_csv(f'{OUT}/cdli_archibab_linked.csv')
L = L[L.in_photo_dataset & L.artifact_type.isin(['tablet', 'tablet & envelope'])].drop_duplicates('artifact_id').reset_index(drop=True)
rhs = L.from_to.fillna('').str.split('→').str[-1]
site = rhs.str.replace(r'\s*\(\d+\)|°', '', regex=True).str.strip()
L['site'] = np.where(site.str.contains('royaume') | (site == ''), 'NA', site.map(canon))
L['type'] = L.type.fillna('NA').str.strip().replace('', 'NA')
y = L.ab_year_bc
L['date'] = np.select([y > 1810, (y <= 1810) & (y >= 1793), (y <= 1792) & (y >= 1750), y < 1750],
                      ['before 1810', '1810-1793', '1792-1750 (Hammurabi)', 'after 1750'], 'NA')
L['archive'] = L.archives.fillna('NA').str.strip().replace('', 'NA')
L['museum'] = L.collections.fillna('unknown').str.split(';').str[0].str.strip()
print('tablets:', len(L))

STRATA = {'type': ['museum', 'site'], 'site': ['museum', 'type', 'date'], 'date': ['museum', 'type', 'site'], 'archive': ['museum', 'type']}
mus = pd.factorize(L.museum)[0]; diff = (mus[:, None] != mus[None]).astype(np.float64)
spaces = {'DINOv2_pca12z_euclid': squareform(pdist(Z.loc[L.artifact_id].values)),
          'DINOv2_full_cosine': squareform(pdist(emb[pos.loc[L.artifact_id].values] / np.linalg.norm(emb[pos.loc[L.artifact_id].values], axis=1, keepdims=True), 'cosine'))}

def stat(lab, vals, Dd):
    M = (lab[:, None] == np.array(vals)[None]).astype(np.float64)        # n x V
    num = np.einsum('iv,ij,jv->v', M, Dd, M); den = np.einsum('iv,ij,jv->v', M, diff, M)
    return num / den

rows = []
for kind, other in STRATA.items():
    lab = L[kind].to_numpy(dtype=object)
    ct = L[L[kind] != 'NA'].groupby([kind, 'museum']).size()
    vals = [v for v, s in ct.groupby(level=0) if (s >= MIN_N).sum() >= 2]
    if not vals: continue
    strata = L[other].astype(str).agg('|'.join, axis=1).values
    groups = [np.where(strata == s)[0] for s in np.unique(strata)]
    perms = []
    for _ in range(NPERM):
        p = lab.copy()
        for g in groups:
            if len(g) > 1: p[g] = lab[rng.permutation(g)]
        perms.append(p)
    for sp, D in spaces.items():
        Dd = D * diff
        obs = stat(lab, vals, Dd); null = np.stack([stat(p, vals, Dd) for p in perms])
        for k, v in enumerate(vals):
            s = ct.loc[v]
            rows.append(dict(space=sp, label=kind, value=v, n=int((lab == v).sum()), n_museums_ge8=int((s >= MIN_N).sum()),
                             obs=obs[k], null_mean=null[:, k].mean(), ratio=obs[k] / null[:, k].mean(), p=(null[:, k] <= obs[k]).mean()))
R = pd.DataFrame(rows).sort_values(['space', 'label', 'ratio'])
R.to_csv(f'{OUT}/03_label_signal.csv', index=False)
pd.set_option('display.width', 220); pd.set_option('display.precision', 3); pd.set_option('display.max_rows', 300)
print(R.to_string(index=False))
