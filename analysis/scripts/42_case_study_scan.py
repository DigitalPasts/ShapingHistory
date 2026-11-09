"""Feasibility scan for Section 5 case studies: how many tablets (with photograph-based VAE encoding, with catalogue
dimensions) are available per site, period and reign for the three proposed cases."""
from _paths import WORK
import pandas as pd, numpy as np, re
R=WORK
a=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','period','provenience','dates','genres','collections','artifact_type','languages','archive'],low_memory=False)
a=a[a.artifact_type.fillna('').str.lower().str.contains('tablet')]
v=pd.concat([pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_{s}.csv') for s in ['train','val','test']])
a['vae']=a.artifact_id.isin(v.CDLI_id)
c=pd.read_csv(f'{R}/results/tablet_dims_clean.csv')[['artifact_id','hw','archival']]
a=a.merge(c,on='artifact_id',how='left')
a['site']=a.provenience.fillna('?').str.split(' \\(').str[0]
a['per']=a.period.fillna('?').str.split(' \\(').str[0]
def tab(df,by):
    g=df.groupby(by).agg(n=('artifact_id','size'),photo=('vae','sum'),dims=('hw','count'),hw_med=('hw','median'),archival=('archival','sum'))
    return g.sort_values('n',ascending=False)
print('=== B: second-millennium periphery (non-Babylonian sites) ===')
P2=['Old Assyrian','Old Babylonian','Middle Babylonian','Middle Assyrian','Middle Hittite','Old Hittite','Hittite','Middle Elamite','Old Elamite']
B=a[a.per.isin(P2)]
BAB=['Sippar','Nippur','Ur','Larsa','Babylon','Kish','Isin','Uruk','Lagaba','Dilbat','Kutha','Borsippa','Marad','?','uncertain','Adab','Tell ed-Der','Kisurra','Sippar-Amnanum','Girsu','Umma','Šaduppum','Nerebtum','Ešnunna','Tutub','Damrum']
Bp=B[~B.site.isin(BAB)]
t=tab(Bp,['site','per']); print(t[t.n>=30].to_string())
print('\n=== C: first millennium Babylonia by site ===')
C=a[a.per.isin(['Neo-Babylonian','Achaemenid','Hellenistic'])]
t=tab(C,['per','site']); print(t[t.n>=50].to_string())
print('\n=== C: by reign (first word of date) ===')
C=C.assign(king=C.dates.fillna('').str.extract(r'^([A-Za-zÀ-ž\-\s]+?)\.')[0].str.strip())
t=tab(C,['king']); print(t[t.n>=50].head(25).to_string())
print('\n=== A: Ur III by province (photos) ===')
U=a[a.per=='Ur III']; t=tab(U,['site']); print(t.head(10).to_string())
a.to_csv(f'{R}/results/case_scan_tablets.csv',index=False)
