"""Analyses of the photographed OB / Early OB tablets that link to Archibab.
Archibab site = right-hand side of 'de -> a' (find / attribution site); '°' = excavated; '(royaume de -)' = kingdom-level only.
(1) label audit CDLI provenience vs Archibab site; (2) shape dispersion by site, CDLI vs Archibab labels (VAE z-scored and
DINOv2 PCA-12 z-scored, bootstrap n=30); (3) museum predictability within the same Archibab site; (4) dispersion within
Archibab archives vs their whole site; (5) excavated vs not, same site; (6) OB-tracing hubness with Archibab-labelled references."""
import os, re, unicodedata, numpy as np, pandas as pd, torch
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import balanced_accuracy_score

ROOT = os.path.expanduser('~/deeplomatics-repro'); OUT = f'{ROOT}/archibab'
SEED, B, NSUB = 0, 200, 30
rng = np.random.default_rng(SEED)
fold = lambda s: unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode().lower().replace('-', '').replace(' ', '')
ALIAS = {'babilim': 'babylon', 'kis': 'kish', 'susum': 'susa', 'alahtum': 'alalakh', 'sipparyahrurum': 'sippar', 'sipparamnanum': 'sippar',
         'yahrurum': 'sippar'}  # Yahrurum = Sippar-Yahrurum district
canon = lambda s: ALIAS.get(fold(s), fold(s))

# embeddings: DINOv2 (all 92,876) and VAE codes (Zenodo csvs)
ids = pd.read_csv(f'{ROOT}/results/emb_dinov2_vitb14_224_ids.csv').CDLI_id.values
emb = np.load(f'{ROOT}/results/emb_dinov2_vitb14_224.npy').astype(np.float64)
vae = pd.concat([pd.read_csv(f'{ROOT}/zenodo/vae_encoding_df_April16_w_class_{s}.csv') for s in ['train', 'val', 'test']]).set_index('CDLI_id')
art = pd.read_csv(os.path.expanduser('~/Dropbox/Git-projects/ShapingHistory/artifacts.csv'), low_memory=False,
                  usecols=['artifact_id', 'period', 'provenience', 'collections', 'genres', 'artifact_type'])
T = art[art.artifact_id.isin(ids) & art.artifact_type.isin(['tablet', 'tablet & envelope'])].set_index('artifact_id')
pos = pd.Series(np.arange(len(ids)), index=ids)
# same normalisation as the earlier dispersion runs (fit on all 87,783 tablets)
Dz = PCA(12, random_state=SEED).fit_transform(emb[pos.loc[T.index].values]); Dz = (Dz - Dz.mean(0)) / Dz.std(0)
Dz = pd.DataFrame(Dz, index=T.index)
V = vae.loc[vae.index.isin(T.index), [f'X{i}' for i in range(1, 13)]]; V = (V - V.mean()) / V.std()
En = emb / np.linalg.norm(emb, axis=1, keepdims=True)

L = pd.read_csv(f'{OUT}/cdli_archibab_linked.csv')
L = L[L.in_photo_dataset & L.artifact_type.isin(['tablet', 'tablet & envelope'])].drop_duplicates('artifact_id').copy()
rhs = L.from_to.fillna('').str.split('→').str[-1]
L['ab_site'] = rhs.str.replace(r'\s*\(\d+\)|°', '', regex=True).str.strip()
L['ab_excavated'] = rhs.str.contains('°')
L['ab_kingdom_only'] = L.ab_site.str.contains('royaume')
L['ab_city'] = np.where(L.ab_kingdom_only | (L.ab_site == ''), '', L.ab_site.map(canon))
L['cdli_c'] = L.cdli_city.map(lambda s: '' if s in ('uncertain', 'unclear') else canon(s))
L['museum'] = L.collections.fillna('unknown').str.split(';').str[0].str.strip()
L['admin'] = L.genres.fillna('').str.contains('Administrative|Legal|Letter|Business')
L = L.set_index('artifact_id', drop=False)

# (1) audit
def audit(r):
    if r.cdli_c and r.ab_city: return 'agree' if r.cdli_c == r.ab_city else 'disagree'
    if r.cdli_c and r.ab_kingdom_only: return 'CDLI city, Archibab kingdom only'
    if r.cdli_c: return 'CDLI city, Archibab none'
    if r.ab_city: return 'CDLI uncertain -> Archibab city'
    if r.ab_kingdom_only: return 'CDLI uncertain -> Archibab kingdom only'
    return 'both unknown'
L['audit'] = L.apply(audit, axis=1)
a1 = L.audit.value_counts().rename('n').to_frame(); a1['share'] = a1.n / len(L)
a1.to_csv(f'{OUT}/a1_label_audit.csv')
dis = L[L.audit == 'disagree'].groupby(['cdli_city', 'ab_site']).size().sort_values(ascending=False).rename('n')
dis.to_csv(f'{OUT}/a1_disagreements.csv')
gain = L[L.audit == 'CDLI uncertain -> Archibab city'].ab_site.value_counts().rename('n'); gain.to_csv(f'{OUT}/a1_uncertain_gained.csv')

# dispersion helper (median distance to coordinate-wise median, bootstrap NSUB without replacement)
def disp(M):
    if len(M) < NSUB: return (np.nan,) * 3
    v = []
    for _ in range(B):
        S = M[rng.choice(len(M), NSUB, replace=False)]
        v.append(np.median(np.linalg.norm(S - np.median(S, 0), axis=1)))
    return np.median(v), np.percentile(v, 2.5), np.percentile(v, 97.5)

# (2) site dispersion with CDLI vs Archibab labels on the same linked tablets
rows = []
for lab in ['cdli_c', 'ab_city']:
    for c, g in L[L[lab] != ''].groupby(lab):
        if len(g) < NSUB: continue
        for space, Z in [('VAE', V), ('DINOv2', Dz)]:
            ii = g.index[g.index.isin(Z.index)]
            d = disp(Z.loc[ii].values)
            rows.append(dict(labels=lab.replace('cdli_c', 'CDLI').replace('ab_city', 'Archibab'), city=c, n=len(ii), space=space,
                             disp=d[0], lo=d[1], hi=d[2]))
a2 = pd.DataFrame(rows); a2.to_csv(f'{OUT}/a2_site_dispersion_cdli_vs_archibab.csv', index=False)

# (3) museum predictability within the same Archibab city (top 5 museums with >=30, downsampled)
rows = []
for c, g in L[L.ab_city != ''].groupby('ab_city'):
    vc = g.museum.value_counts(); top = vc[vc >= 30].index[:5]
    if len(top) < 2: continue
    m = vc[top].min(); s = pd.concat([g[g.museum == mu].sample(m, random_state=SEED) for mu in top])
    X = emb[pos.loc[s.index].values]
    yp = cross_val_predict(make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000)), X, s.museum.values,
                           cv=StratifiedKFold(5, shuffle=True, random_state=SEED))
    rows.append(dict(ab_city=c, n_museums=len(top), n_per_museum=m, balanced_acc=balanced_accuracy_score(s.museum, yp), chance=1 / len(top),
                     museums=' | '.join(f'{mu} ({vc[mu]})' for mu in top)))
a3 = pd.DataFrame(rows); a3.to_csv(f'{OUT}/a3_museum_within_archibab_city.csv', index=False)

# (4) archives: dispersion of each archive (>= NSUB) vs its whole Archibab city
rows = []
L['archive'] = L.archives.fillna('').str.strip()
for ar, g in L[L.archive != ''].groupby('archive'):
    if len(g) < NSUB: continue
    city = g.ab_city.mode().iat[0] if (g.ab_city != '').any() else ''
    for space, Z in [('VAE', V), ('DINOv2', Dz)]:
        ii = g.index[g.index.isin(Z.index)]; d = disp(Z.loc[ii].values)
        cc = L[(L.ab_city == city) & (L.archive != ar)].index if city else []
        cc = [i for i in cc if i in Z.index]; dc = disp(Z.loc[cc].values) if len(cc) >= NSUB else (np.nan,) * 3
        rows.append(dict(archive=ar, city=city, space=space, n=len(ii), disp_archive=d[0], lo=d[1], hi=d[2],
                         n_rest_of_city=len(cc), disp_rest_of_city=dc[0], lo_city=dc[1], hi_city=dc[2]))
a4 = pd.DataFrame(rows); a4.to_csv(f'{OUT}/a4_archive_vs_city_dispersion.csv', index=False)

# (5) excavated vs not excavated within the same Archibab city
rows = []
for c, g in L[L.ab_city != ''].groupby('ab_city'):
    e, ne = g[g.ab_excavated], g[~g.ab_excavated]
    if min(len(e), len(ne)) < NSUB: continue
    for space, Z in [('VAE', V), ('DINOv2', Dz)]:
        for tag, h in [('excavated', e), ('not_excavated', ne)]:
            ii = h.index[h.index.isin(Z.index)]; d = disp(Z.loc[ii].values)
            rows.append(dict(ab_city=c, space=space, group=tag, n=len(ii), disp=d[0], lo=d[1], hi=d[2],
                             top_museum=h.museum.value_counts().index[0], top_museum_share=h.museum.value_counts(normalize=True).iat[0]))
        Ze, Zn = Z.loc[e.index[e.index.isin(Z.index)]].values, Z.loc[ne.index[ne.index.isin(Z.index)]].values
        rows.append(dict(ab_city=c, space=space, group='distance_between_medians', disp=np.linalg.norm(np.median(Ze, 0) - np.median(Zn, 0))))
a5 = pd.DataFrame(rows); a5.to_csv(f'{OUT}/a5_excavated_vs_not.csv', index=False)

# (6) hubness of OB reference cities in the tracing set-up, CDLI vs Archibab labels, on the same linked tablets.
# Queries = every non-OB archival tablet in a (period, city) group with >=30 (as in ob_tracing.py); 25 NN, CSLS k=10;
# mode b excludes OB tablets in the query's museum.
TT = T.copy(); TT['per'] = TT.period.fillna('').str.split(' (', regex=False).str[0].str.strip()
TT['city'] = TT.provenience.fillna('uncertain').str.split(' (', regex=False).str[0].str.strip()
TT['museum'] = TT.collections.fillna('unknown').str.split(';').str[0].str.strip()
g = TT.genres.fillna('')
schol = g.str.contains('Literary|Lexical|Mathematical|Divination|Scientific|Liturg|Ritual|Incantation', case=False)
arch = g.str.contains('Administrative|Legal|Letter|Business', case=False) & ~schol
Q = TT[arch & ~TT.per.isin(['Old Babylonian', 'Early Old Babylonian', ''])]
qn = Q.groupby(['per', 'city']).size(); Q = Q[Q.set_index(['per', 'city']).index.isin(qn[qn >= 30].index)]
R = L[L.artifact_id.isin(TT[arch].index) & (L.period.fillna('').str.startswith('Old Babylonian'))]
dev = 'mps'
Qt = torch.from_numpy(En[pos.loc[Q.index].values].astype(np.float32)).to(dev)
rows = []
for lab in ['cdli_c', 'ab_city']:
    Rl = R[R[lab] != '']; vc = Rl[lab].value_counts(); Rl = Rl[Rl[lab].isin(vc[vc >= 30].index)]
    cities = sorted(Rl[lab].unique()); rc = np.array([cities.index(c) for c in Rl[lab]])
    Rt = torch.from_numpy(En[pos.loc[Rl.index].values].astype(np.float32)).to(dev)
    rS = (Rt @ Qt.T).topk(10, dim=1).values.mean(1)
    mus = pd.factorize(pd.concat([Rl.museum, Q.museum]))[0]; rm = torch.tensor(mus[:len(Rl)], device=dev); qm = torch.tensor(mus[len(Rl):], device=dev)
    size = np.bincount(rc, minlength=len(cities)).astype(float)
    mc = np.zeros((mus.max() + 1, len(cities))); np.add.at(mc, mus[:len(Rl)], np.eye(len(cities))[rc])
    for mode in ['a_all', 'b_other_museum']:
        occ = np.zeros(len(Rl)); base_sum = np.zeros(len(cities)); nq = 0
        for i in range(0, len(Qt), 4096):
            S = 2 * (Qt[i:i + 4096] @ Rt.T) - rS[None]
            if mode == 'b_other_museum': S = S.masked_fill(qm[i:i + 4096, None] == rm[None], -1e9)
            nb = S.topk(min(25, len(Rl)), dim=1).indices.cpu().numpy(); np.add.at(occ, nb.ravel(), 1)
            qmi = qm[i:i + 4096].cpu().numpy()
            rem = np.tile(size, (len(qmi), 1)) - (mc[qmi] if mode == 'b_other_museum' else 0); base_sum += (rem / rem.sum(1, keepdims=True)).sum(0); nq += len(qmi)
        for ci, c in enumerate(cities):
            sh = occ[rc == ci].sum() / occ.sum(); bs = base_sum[ci] / nq
            rows.append(dict(labels=lab.replace('cdli_c', 'CDLI').replace('ab_city', 'Archibab'), mode=mode, ob_city=c, n_ob=int(size[ci]),
                             share_of_neighbours=sh, base=bs, hub_ratio=sh / bs))
a6 = pd.DataFrame(rows); a6.to_csv(f'{OUT}/a6_hubness_cdli_vs_archibab_labels.csv', index=False)

pd.set_option('display.width', 250); pd.set_option('display.precision', 3); pd.set_option('display.max_colwidth', 90); pd.set_option('display.max_rows', 200)
print('linked photographed OB/EOB tablets:', len(L))
print(a1.to_string()); print(dis.head(15).to_string()); print(gain.head(15).to_string())
print(a2.pivot_table(index='city', columns=['space', 'labels'], values=['disp', 'n']).to_string())
print(a3.to_string(index=False)); print(a4.to_string(index=False)); print(a5.to_string(index=False))
print(a6.pivot_table(index=['labels', 'ob_city', 'n_ob'], columns='mode', values='hub_ratio').to_string())
