"""Within one Archibab document type, do same-findspot tablets look more alike than different-findspot ones, comparing only
tablets held in the same museum? ratio = mean d(same museum, different findspot) / mean d(same museum, same findspot);
> 1 = local form. Null: findspot permuted within museum (type groups: within museum x type), 1,000 times.
Only museum x findspot cells with >= 3 tablets, in museums with >= 2 such cells, enter the pairs."""
import os, numpy as np, pandas as pd
from sklearn.decomposition import PCA
from scipy.spatial.distance import pdist, squareform

ROOT = os.path.expanduser('~/deeplomatics-repro'); OUT = f'{ROOT}/archibab'
SEED, NPERM, MIN_CELL, MIN_TYPE = 0, 1000, 3, 30
rng = np.random.default_rng(SEED)
ids = pd.read_csv(f'{ROOT}/results/emb_dinov2_vitb14_224_ids.csv').CDLI_id.values
emb = np.load(f'{ROOT}/results/emb_dinov2_vitb14_224.npy').astype(np.float64)
pos = pd.Series(np.arange(len(ids)), index=ids)
art = pd.read_csv(os.path.expanduser('~/Dropbox/Git-projects/ShapingHistory/artifacts.csv'), low_memory=False, usecols=['artifact_id', 'artifact_type'])
Tall = art[art.artifact_id.isin(ids) & art.artifact_type.isin(['tablet', 'tablet & envelope'])].artifact_id.values
Z = PCA(12, random_state=SEED).fit_transform(emb[pos.loc[Tall].values]); Z = pd.DataFrame((Z - Z.mean(0)) / Z.std(0), index=Tall)

L = pd.read_csv(f'{OUT}/cdli_archibab_linked.csv')
L = L[L.in_photo_dataset & L.artifact_type.isin(['tablet', 'tablet & envelope'])].drop_duplicates('artifact_id').reset_index(drop=True)
L['findspot'] = (L.from_to.fillna('').str.split('→').str[-1].str.replace('°', '', regex=False)
                 .str.replace(r'\s*\(royaume de –\)', '', regex=True).str.strip())
L['type'] = L.type.fillna('').str.strip()
L['museum'] = L.collections.fillna('unknown').str.split(';').str[0].str.strip()
L = L[(L.findspot != '') & (L.type != '')].reset_index(drop=True)
GROUPS = {'legal': ['prêt à intérêt', 'prêt autre', 'achat', 'location', 'fermage', 'quittance'],
          'administrative': ['dépense', 'compte récapitulatif', 'reçu', 'attribution de ration', 'gestion de personnel', 'liste de personnes'],
          'letters': ['lettre']}
sets = [(t, [t], False) for t, n in L.type.value_counts().items() if n >= MIN_TYPE] + [(g, ts, True) for g, ts in GROUPS.items()]

def ratio(fs, mus, D, sm):
    same = sm & (fs[:, None] == fs[None]); diff = sm & ~same
    np.fill_diagonal(same, False)
    return D[diff].mean() / D[same].mean(), D[same].mean(), D[diff].mean()

rows = []
for name, types, is_group in sets:
    S = L[L.type.isin(types)]
    cell = S.groupby(['museum', 'findspot']).artifact_id.transform('size')
    S = S[cell >= MIN_CELL]
    ncell = S.groupby('museum').findspot.transform('nunique'); S = S[ncell >= 2].reset_index(drop=True)
    n_cells = S.groupby(['museum', 'findspot']).ngroups
    if n_cells < 2:
        rows.append(dict(set=name, n=len(S), n_cells=n_cells)); continue
    fs = S.findspot.to_numpy(dtype=object); mus = S.museum.to_numpy(dtype=object)
    sm = mus[:, None] == mus[None]
    strata = (S.museum + '|' + (S.type if is_group else '')).to_numpy(dtype=object)
    idx = [np.where(strata == s)[0] for s in np.unique(strata)]
    E = emb[pos.loc[S.artifact_id].values]
    for sp, D in [('DINOv2_full_cosine', squareform(pdist(E / np.linalg.norm(E, axis=1, keepdims=True), 'cosine'))),
                  ('DINOv2_pca12z_euclid', squareform(pdist(Z.loc[S.artifact_id].values)))]:
        r, ds, dd = ratio(fs, mus, D, sm)
        null = []
        for _ in range(NPERM):
            p = fs.copy()
            for g in idx: p[g] = fs[rng.permutation(g)]
            null.append(ratio(p, mus, D, sm)[0])
        null = np.array(null)
        rows.append(dict(set=name, space=sp, n=len(S), n_cells=n_cells, n_museums=S.museum.nunique(),
                         findspots=' | '.join(f'{k} ({v})' for k, v in S.findspot.value_counts().items()),
                         d_same_site=ds, d_diff_site=dd, ratio=r, null_mean=null.mean(),
                         p_local=(null >= r).mean(), p_shared=(null <= r).mean()))
R = pd.DataFrame(rows); R.to_csv(f'{OUT}/06_type_by_site.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.precision', 3); pd.set_option('display.max_colwidth', 120)
print(R.drop(columns='findspots').to_string(index=False))
print(R.drop_duplicates('set')[['set', 'findspots']].to_string(index=False))
