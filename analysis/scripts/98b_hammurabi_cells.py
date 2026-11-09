"""T7 (Hammurabi conquers Larsa, 1763) inside the only site x genre cells with at least 10 dated tablets on both sides
(1790-1764 vs 1763-1739). Standardized median shift (pooled MAD) and a permutation p within the cell (5,000 draws).
Output: turning/hammurabi_cells.csv"""
from _paths import WORK
import pandas as pd, numpy as np
R=WORK; rng=np.random.default_rng(7)
d=pd.read_parquet(f'{R}/master_tablets.parquet'); d=d[(d.period=='Old Babylonian')&d.photo_hw.between(1/3,3)].copy()
OB={'Rim-Sin':1822,'Hammurapi':1792,'Samsu-iluna':1749,'Warad-Sin':1834,'Sin-muballit':1812}
d['bce']=np.where(d.ruler.isin(OB),d.ruler.map(OB)-(d.ryear.fillna(1).clip(lower=1)-1),np.nan)
d=d[d.bce.between(1739,1790)&d.ryear.notna()]; d['post']=(d.bce<=1763).astype(int)
FE=['loghw','corner_fill','rect','thick_side']+[f'X{i}' for i in range(1,13)]
mad=lambda x: np.median(np.abs(x-np.median(x)))*1.4826
rows=[]
for site,g in [('Larsa','Administrative'),('Nippur','Legal'),('Sippar-Yahrurum','Legal')]:
    c=d[(d.site==site)&(d.genre==g)]
    for f in FE:
        x=c[[f,'post']].dropna(); a=x[x.post==1][f].values; b=x[x.post==0][f].values
        if len(a)<8 or len(b)<8: continue
        s=mad(x[f].values) or x[f].std(); obs=(np.median(a)-np.median(b))/s
        v=x[f].values; n=len(a); null=[]
        for _ in range(5000):
            p=rng.permutation(v); null.append((np.median(p[:n])-np.median(p[n:]))/s)
        rows.append(dict(site=site,genre=g,feature=f,n_before=len(b),n_after=len(a),shift=round(obs,2),p=round(float(np.mean(np.abs(null)>=abs(obs))),4)))
r=pd.DataFrame(rows); r.to_csv(f'{R}/turning/hammurabi_cells.csv',index=False)
print(r.to_string())
