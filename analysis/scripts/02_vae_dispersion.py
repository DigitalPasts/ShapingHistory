"""Tablet-only shape dispersion: robust h/w measure and VAE latent dispersion, by period and by site x period.
Latent dispersion = median Euclidean distance of each tablet's 12-d VAE code to its group's coordinate-wise median.
Groups are subsampled to equal n (bootstrap) so that dispersion is comparable across group sizes."""
from _paths import WORK
import numpy as np, pandas as pd
R=WORK; rng=np.random.default_rng(0)
X=[f'X{i}' for i in range(1,13)]
v=pd.concat([pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_{s}.csv').assign(split=s) for s in ['train','val','test']])
m=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','period','genres','provenience','artifact_type'],low_memory=False)
pix=pd.read_csv(f'{R}/zenodo/h_w_ratio_df_all.csv'); pix['artifact_id']=pix.tablet_p_id_CDLI.str.lstrip('P').astype(int)
d=v.rename(columns={'CDLI_id':'artifact_id'}).merge(m,on='artifact_id',how='left').merge(pix[['artifact_id','hw_ratio']],on='artifact_id',how='left')
print('VAE rows',len(d),'| artifact types:',d.artifact_type.value_counts().head(6).to_dict())
d=d[d.artifact_type.isin(['tablet','tablet & envelope'])].copy()
d['site']=d.provenience.fillna('uncertain').str.extract(r'^([^\(]+)')[0].str.strip()
d['admin']=d.Genre_Name.eq('Administrative')
print('tablet-only rows',len(d))
# standardise latent dims on the whole tablet corpus so every dim weighs equally
Z=(d[X]-d[X].mean())/d[X].std(); d[X]=Z
def disp(g,n=100,B=200):
    a=g[X].values; lr=np.log(g.hw_ratio.dropna().values)
    if len(a)<n: return None
    lat=[];hw=[]
    for _ in range(B):
        s=a[rng.choice(len(a),n,replace=False)]; lat.append(np.median(np.linalg.norm(s-np.median(s,0),axis=1)))
        t=lr[rng.choice(len(lr),min(n,len(lr)),replace=False)]; hw.append(np.median(abs(t-np.median(t))))
    lat=np.array(lat); return dict(n=len(a),latent_disp=round(np.median(lat),3),lat_lo=round(np.percentile(lat,2.5),3),lat_hi=round(np.percentile(lat,97.5),3),hw_madlog=round(np.median(hw),3))
ORDER=['Uruk IV','Uruk III','Proto-Elamite','ED I-II','ED IIIa','ED IIIb','Ebla','Old Akkadian','Lagash II','Ur III','Early Old Babylonian','Old Babylonian','Old Assyrian','Middle Assyrian','Middle Babylonian','Middle Elamite','Hittite','Neo-Assyrian','Neo-Babylonian','Achaemenid','Hellenistic']
rows=[]
for scope,sub in [('all',d),('admin',d[d.admin])]:
    for p in ORDER:
        r=disp(sub[sub.Period_Name==p]); 
        if r: rows.append(dict(scope=scope,period=p,**r))
per=pd.DataFrame(rows); per.to_csv(f'{R}/results/dispersion_by_period.csv',index=False)
print(per.to_string(index=False))
a=per[per.scope=='admin']; print('Spearman latent vs hw dispersion across periods (admin):',round(a[['latent_disp','hw_madlog']].corr('spearman').iloc[0,1],2))
rows=[]
for (s,p),g in d[d.admin].groupby(['site','Period_Name']):
    r=disp(g); 
    if r: rows.append(dict(site=s,period=p,**r))
sp=pd.DataFrame(rows).sort_values(['site','period']); sp.to_csv(f'{R}/results/dispersion_by_site_period_admin.csv',index=False)
print(sp.to_string(index=False))
# synchronic baseline: distance between contemporary sites' median codes, per period (admin, sites n>=100)
rows=[]
for p,g in d[d.admin].groupby('Period_Name'):
    cs={s:np.median(h[X].values,0) for s,h in g.groupby('site') if len(h)>=100 and s!='uncertain'}
    k=list(cs)
    for i in range(len(k)):
        for j in range(i+1,len(k)): rows.append(dict(period=p,a=k[i],b=k[j],centroid_dist=round(np.linalg.norm(cs[k[i]]-cs[k[j]]),3)))
cd=pd.DataFrame(rows); cd.to_csv(f'{R}/results/between_site_distance_admin.csv',index=False); print(cd.to_string(index=False))
