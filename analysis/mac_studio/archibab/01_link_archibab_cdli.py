"""Link the Archibab text table (archibab_textes.csv, saved from www.archibab.fr/textes) to CDLI artifacts.
Routes: (1) CDLI external_resources ARCHIBAB key -> Archibab id T<key>; (2) normalised museum number (OB / EOB artifacts only)."""
import os, re, numpy as np, pandas as pd
ROOT = os.path.expanduser('~/deeplomatics-repro')
ab = pd.read_csv(f'{ROOT}/archibab/archibab_textes.csv').drop_duplicates('id').reset_index(drop=True)
def sites(s):
    s = '' if pd.isna(s) else s
    w, _, f = s.partition('→')
    clean = lambda x: re.sub(r'\s*\(\d+\)|°', '', x).strip()
    return clean(w), clean(f), '°' in f
ab[['ab_writing_site', 'ab_find_site', 'ab_find_excavated']] = pd.DataFrame(ab.from_to.map(sites).tolist())
ab['ab_year_bc'] = ab.date.astype(str).str.extract(r':\s*(\d{4})\s*$')[0].astype(float)
ab['ab_king'] = ab.date.astype(str).str.extract(r'^([^:\d/]+?)\s*(?:\d+|:)')[0].str.strip()

def norm(m):
    toks = re.findall(r'[A-Za-z]+|\d+', str(m).upper())
    return ' '.join(t.lstrip('0') or '0' if t.isdigit() else t for t in toks)

art = pd.read_csv(os.path.expanduser('~/Dropbox/Git-projects/ShapingHistory/artifacts.csv'), low_memory=False,
                  usecols=['artifact_id', 'museum_no', 'designation', 'period', 'provenience', 'collections', 'genres', 'artifact_type',
                           'external_resources', 'external_resources_key'])
# (1) explicit CDLI -> Archibab links
links = []
for aid, res, key in art[art.external_resources.fillna('').str.contains('ARCHIBAB')][['artifact_id', 'external_resources', 'external_resources_key']].values:
    r, k = [x.strip() for x in str(res).split(';')], [x.strip() for x in str(key).split(';')]
    for rr, kk in zip(r, k):
        if rr == 'ARCHIBAB': links.append((aid, f'T{kk}', 'cdli_link'))
# (2) museum number, OB + EOB only, both sides unique after normalisation
ob = art[art.period.fillna('').str.match(r'(Early )?Old Babylonian')].copy()
ob['mk'] = ob.museum_no.map(norm)
abk = ab[['id', 'museum_no']].assign(museum_no=ab.museum_no.fillna('').str.split(r'\s*[+,;=]\s*')).explode('museum_no')
abk['mk'] = abk.museum_no.map(norm); abk = abk[abk.mk.str.contains(r'[A-Z]') & abk.mk.str.contains(r'\d')]
u_ab = abk.groupby('mk').id.nunique(); u_ob = ob.groupby('mk').artifact_id.nunique()
ok = set(u_ab[u_ab == 1].index) & set(u_ob[u_ob == 1].index)
m = ob[ob.mk.isin(ok)][['artifact_id', 'mk']].merge(abk[abk.mk.isin(ok)][['id', 'mk']].drop_duplicates('mk'), on='mk')
links += [(a, i, 'museum_no') for a, i in m[['artifact_id', 'id']].values]
L = pd.DataFrame(links, columns=['artifact_id', 'id', 'route']).drop_duplicates(['artifact_id', 'id'])
L = L.groupby('artifact_id').first().reset_index()            # prefer the explicit CDLI link (listed first)
L = L.merge(ab, on='id', how='inner').merge(art.drop(columns=['external_resources', 'external_resources_key']), on='artifact_id', how='left')
emb_ids = set(pd.read_csv(f'{ROOT}/results/emb_dinov2_vitb14_224_ids.csv').CDLI_id)
L['in_photo_dataset'] = L.artifact_id.isin(emb_ids)
L['cdli_city'] = L.provenience.fillna('uncertain').str.split(' (', regex=False).str[0].str.strip()
L.to_csv(f'{ROOT}/archibab/cdli_archibab_linked.csv', index=False)
print('Archibab rows', len(ab), '| unique ids saved', ab.id.nunique())
print('links:', len(L), L.route.value_counts().to_dict(), '| in photo dataset:', L.in_photo_dataset.sum())
P = L[L.in_photo_dataset & L.artifact_type.isin(['tablet', 'tablet & envelope'])]
print('photo tablets linked:', len(P)); print(P.route.value_counts())
print(pd.crosstab(P.cdli_city, P.ab_find_site.replace('', '(none)')).stack().loc[lambda s: s > 0].sort_values(ascending=False).head(40).to_string())
