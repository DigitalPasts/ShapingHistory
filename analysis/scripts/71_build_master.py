"""Tablet-level master table for the centralization pilots.
Joins: VAE codes (Zenodo 12787746), CDLI catalogue (artifacts.csv, export used by the project), damage index (script 06),
photo-measured obverse ratio and outline features (script 56), cleaned catalogue dimensions (script 38).
Parses CDLI 'dates' into ruler and regnal year. Output: master_tablets.parquet"""
from _paths import SHARED, WORK
import pandas as pd, numpy as np, re
R=WORK; P=SHARED
X=[f'X{i}' for i in range(1,13)]
v=pd.concat([pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_{s}.csv') for s in ['train','val','test']]).drop_duplicates('CDLI_id')
v=v.rename(columns={'CDLI_id':'id','Period_Name':'period','Genre_Name':'genre_vae'})[['id','period','genre_vae']+X]
a=pd.read_csv(f'{R}/artifacts.csv',low_memory=False,usecols=['artifact_id','provenience','genres','dates','collections','artifact_type','is_school_text','archive','designation','museum_no']).rename(columns={'artifact_id':'id'})
d=v.merge(a,on='id',how='left')
dmg=pd.read_csv(f'{P}/damage_score.csv').rename(columns={'CDLI_id':'id'})[['id','damage']]
g=pd.read_csv(f'{P}/results/silhouette_geometry.csv').rename(columns={'hw':'obv_hw'})
pix=pd.read_csv(f'{R}/zenodo/h_w_ratio_df_all.csv'); pix['id']=pix.tablet_p_id_CDLI.str.lstrip('P').astype(int)
pix=pix.groupby('id').hw_ratio.mean().rename('photo_hw').reset_index()
t=pd.read_csv(f'{P}/tablet_dims_clean.csv').rename(columns={'artifact_id':'id','hw':'cat_hw'})[['id','height','width','cat_hw','archival']]
d=d.merge(dmg,on='id',how='left').merge(g,on='id',how='left').merge(pix,on='id',how='left').merge(t,on='id',how='left')
d=d[d.artifact_type.fillna('tablet').str.contains('tablet')]
d['site']=d.provenience.fillna('unknown').str.replace(r'\s*\(mod\..*\)','',regex=True).str.replace(r'\s*\(.*\)','',regex=True).str.strip()
d['museum']=d.collections.fillna('?').str.split(',').str[0].str.strip()
d['genre']=d.genres.fillna('').str.split(';').str[0].str.strip().replace('','unknown')
def parse(s):
    s=str(s)
    m=re.match(r'^([^.\d][^.]*?)\.(\d+|--|00|xx|x)',s)
    if m:
        y=m.group(2); return m.group(1).strip(), (int(y) if y.isdigit() and int(y)>0 else np.nan)
    m=re.match(r'^([A-Za-zŠšṢṣṬṭĀāĪīŪū\-\' ]+)$',s.strip())
    if m and s.strip() not in ('nan',): return s.strip(), np.nan
    return np.nan, np.nan
pr=d.dates.map(parse); d['ruler']=[p[0] for p in pr]; d['ryear']=[p[1] for p in pr]
d['loghw']=np.log(d.photo_hw)
d.to_parquet(f'{R}/master_tablets.parquet')
print(d.shape); print(d.groupby('period').agg(n=('id','size'),photo=('photo_hw','count'),cat=('cat_hw','count'),ruler=('ruler','count')).sort_values('n',ascending=False).head(22))
print(d[d.period=='Old Babylonian'].ruler.value_counts().head(25))
