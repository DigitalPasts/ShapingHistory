"""Label-signal test (as archibab/03) on Neo-Babylonian / Achaemenid tablets with Prosobab labels
(Prosobab dump, DANS doi:10.17026/DANS-ZVN-EECE, CC BY-NC; parsed by parse_prosobab.py).
Statistic per label value (>= 8 tablets in >= 2 museums): mean pairwise distance between same-label tablets held in different
museums; null = 500 permutations within strata (Type, subtype: museum x place; archive: museum x subtype; place: museum x subtype).
Spaces: DINOv2 768-d L2-normalised (cosine) and PCA-12 z-scored (Euclidean)."""
import os, re, numpy as np, pandas as pd
from sklearn.decomposition import PCA
from scipy.spatial.distance import pdist, squareform

ROOT = os.path.expanduser('~/deeplomatics-repro'); OUT = f'{ROOT}/prosobab'; D = f'{OUT}/data'
SEED, NPERM, MIN_N = 0, 500, 8
rng = np.random.default_rng(SEED)
rd = lambda t: pd.read_csv(f'{D}/{t}.csv', low_memory=False)
tab, typ, sub, loc, arc, xso = (rd(t) for t in ['e_tablets', 's_types', 's_subtypes', 's_localities', 'c_archives', 'x_mentionedsubtypesobjects'])
main = xso.sort_values(['TabletID', 'Importance', 'id']).drop_duplicates('TabletID')[['TabletID', 'SubTypeID']]
P = (tab[['TabletID', 'MuseumNr', 'CDLI_URL', 'TypeID', 'PlaceOfWritingID', 'ArchiveID']]
     .merge(typ, on='TypeID', how='left').merge(main, on='TabletID', how='left')
     .merge(sub[['SubTypeID', 'SubTypeGroup']], on='SubTypeID', how='left')
     .merge(loc[['LocalityID', 'LocName']], left_on='PlaceOfWritingID', right_on='LocalityID', how='left')
     .merge(arc[['ArchiveID', 'ArchiveName']], on='ArchiveID', how='left'))

ids = pd.read_csv(f'{ROOT}/results/emb_dinov2_vitb14_224_ids.csv').CDLI_id.values
emb = np.load(f'{ROOT}/results/emb_dinov2_vitb14_224.npy').astype(np.float64)
pos = pd.Series(np.arange(len(ids)), index=ids)
art = pd.read_csv(os.path.expanduser('~/Dropbox/Git-projects/ShapingHistory/artifacts.csv'), low_memory=False,
                  usecols=['artifact_id', 'museum_no', 'period', 'collections', 'artifact_type'])
Tall = art[art.artifact_id.isin(ids) & art.artifact_type.isin(['tablet', 'tablet & envelope'])]
Z = PCA(12, random_state=SEED).fit_transform(emb[pos.loc[Tall.artifact_id].values]); Z = pd.DataFrame((Z - Z.mean(0)) / Z.std(0), index=Tall.artifact_id.values)

def mkey(s):  # letter prefix + first digit run, leading zeros stripped
    m = re.match(r'\s*([A-Za-z][A-Za-z\.\s]*?)\s*\.?\s*0*(\d+)', str(s))
    return (re.sub(r'[\s\.]', '', m.group(1)).upper() + m.group(2)) if m else None
art['mk'] = art.museum_no.map(mkey)
uniq = art.mk.value_counts(); art_u = art[art.mk.isin(uniq[uniq == 1].index)].set_index('mk').artifact_id
P['P_cdli'] = P.CDLI_URL.fillna('').str.extract(r'P(\d{6})')[0].astype(float)
P['P_mus'] = P.MuseumNr.map(mkey).map(art_u)
P['artifact_id'] = P.P_cdli.fillna(P.P_mus); P['route'] = np.where(P.P_cdli.notna(), 'cdli_url', np.where(P.P_mus.notna(), 'museum_no', ''))
P = P.dropna(subset=['artifact_id']).astype({'artifact_id': int})
P = P.merge(Tall[['artifact_id', 'period', 'collections']], on='artifact_id', how='inner')
P['per'] = P.period.fillna('').str.split(' (', regex=False).str[0].str.strip()
n_linked_all = len(P)
P = P[P.per.isin(['Neo-Babylonian', 'Achaemenid'])].drop_duplicates('artifact_id').reset_index(drop=True)
P['museum'] = P.collections.fillna('unknown').str.split(';').str[0].str.strip()
for c, src in [('type', 'Type'), ('subtype', 'SubTypeGroup'), ('archive', 'ArchiveName'), ('place', 'LocName')]:
    P[c] = P[src].fillna('NA').astype(str).str.strip().replace('', 'NA')
P.to_csv(f'{OUT}/07_prosobab_cdli_linked.csv', index=False)
print(f'linked photographed tablets: {n_linked_all} | NB/Achaemenid: {len(P)} | routes {P.route.value_counts().to_dict()} | museums {P.museum.nunique()}')

STRATA = {'type': ['museum', 'place'], 'subtype': ['museum', 'place'], 'archive': ['museum', 'subtype'], 'place': ['museum', 'subtype']}
mus = pd.factorize(P.museum)[0]; diff = (mus[:, None] != mus[None]).astype(np.float64)
E = emb[pos.loc[P.artifact_id].values]
spaces = {'DINOv2_full_cosine': squareform(pdist(E / np.linalg.norm(E, axis=1, keepdims=True), 'cosine')),
          'DINOv2_pca12z_euclid': squareform(pdist(Z.loc[P.artifact_id].values))}
def stat(lab, vals, Dd):
    M = (lab[:, None] == np.array(vals, dtype=object)[None]).astype(np.float64)
    return np.einsum('iv,ij,jv->v', M, Dd, M) / np.einsum('iv,ij,jv->v', M, diff, M)
rows = []
for kind, other in STRATA.items():
    lab = P[kind].to_numpy(dtype=object)
    ct = P[P[kind] != 'NA'].groupby([kind, 'museum']).size()
    vals = [v for v, s in ct.groupby(level=0) if (s >= MIN_N).sum() >= 2]
    if not vals: continue
    strata = P[other].astype(str).agg('|'.join, axis=1).values
    groups = [np.where(strata == s)[0] for s in np.unique(strata)]
    perms = []
    for _ in range(NPERM):
        p = lab.copy()
        for g in groups:
            if len(g) > 1: p[g] = lab[rng.permutation(g)]
        perms.append(p)
    for sp, Dm in spaces.items():
        Dd = Dm * diff; obs = stat(lab, vals, Dd); null = np.stack([stat(p, vals, Dd) for p in perms])
        for k, v in enumerate(vals):
            rows.append(dict(space=sp, label=kind, value=v, n=int((lab == v).sum()), n_museums_ge8=int((ct.loc[v] >= MIN_N).sum()),
                             obs=obs[k], null_mean=null[:, k].mean(), ratio=obs[k] / null[:, k].mean(), p=(null[:, k] <= obs[k]).mean()))
R = pd.DataFrame(rows).sort_values(['space', 'label', 'ratio']); R.to_csv(f'{OUT}/07_nb_label_signal.csv', index=False)
pd.set_option('display.width', 220); pd.set_option('display.precision', 3); pd.set_option('display.max_rows', 300)
print(P.museum.value_counts().to_string()); print(R.to_string(index=False))
