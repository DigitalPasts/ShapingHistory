"""Do document types keep their shape across periods? OB reference groups = Archibab text types (museum-balanced
centroids: mean of per-museum medians, museums with >=5 tablets). Query = later/earlier periods by CDLI genre
(Letter, Legal, Administrative). For each query tablet: which OB type centroid is nearest. Compare the letter/legal
pattern with what the period's own mix predicts (row-normalised shares; same-genre excess)."""
from _paths import WORK
import pandas as pd, numpy as np, re
from scipy.spatial.distance import cdist
R=WORK
F=pd.read_csv(f'{R}/results/tablet_latent_damage_adjusted.csv'); Z=[c for c in F.columns if re.fullmatch(r'Z\d+',c)]
M=pd.read_csv(f'{R}/results/archibab_cdli_match.csv').drop_duplicates('CDLI_id'); M['coll']=M.collections.fillna('?').str.split(';').str[0]
T={'lettre':'letter','prêt à intérêt':'loan','prêt autre':'loan','achat':'purchase','location':'rental/lease','fermage':'rental/lease',
   'reçu':'receipt','quittance':'receipt','dépense':'expenditure','compte récapitulatif':'account','liste de personnes':'list'}
M['t']=M.type.map(T); O=M.dropna(subset=['t']).merge(F[['CDLI_id']+Z],on='CDLI_id')
cent={}
for t,g in O.groupby('t'):
    per=[gg[Z].median().values for c,gg in g.groupby('coll') if len(gg)>=5]
    if len(per)>=2: cent[t]=np.mean(per,0)
C=pd.DataFrame(cent).T; print('OB type centroids:',list(C.index))
a=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','genres'],low_memory=False).rename(columns={'artifact_id':'CDLI_id'})
Q=F.merge(a,on='CDLI_id'); Q=Q[Q.Period_Name!='Old Babylonian']
Q['g']=np.select([Q.genres.fillna('').str.contains('Letter'),Q.genres.fillna('').str.contains('Legal'),Q.genres.fillna('')=='Administrative'],['Letter','Legal','Administrative'],'')
Q=Q[Q.g!='']
near=C.index.values[cdist(Q[Z].values,C.values).argmin(1)]; Q['nearest']=near
tab=pd.crosstab([Q.Period_Name,Q.g],Q.nearest,normalize='index').round(2)
n=Q.groupby(['Period_Name','g']).size(); tab=tab[n.reindex(tab.index)>=40]; tab['n']=n
pd.set_option('display.width',220); print(tab.to_string())
tab.to_csv(f'{R}/results/doc_type_across_periods.csv')
# same-genre excess: within each period, letters' share nearest to OB letters minus legal/admin share nearest to OB letters, etc.
rows=[]
for p,g in Q.groupby('Period_Name'):
    for ref,qq in [('letter','Letter'),('loan','Legal'),('purchase','Legal')]:
        s=g[g.g==qq]; o=g[g.g!=qq]
        if len(s)>=40 and len(o)>=40: rows.append(dict(period=p,ob_type=ref,genre=qq,share_same=(s.nearest==ref).mean(),share_other=(o.nearest==ref).mean(),n_same=len(s),n_other=len(o)))
E2=pd.DataFrame(rows); E2['excess']=E2.share_same-E2.share_other; print(E2.round(2).to_string(index=False)); E2.to_csv(f'{R}/results/doc_type_excess.csv',index=False)
