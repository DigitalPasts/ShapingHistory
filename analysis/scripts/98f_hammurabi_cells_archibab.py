"""98b rerun with Archibab years added (98d): T7 (Hammurabi conquers Larsa, 1763) inside every site x genre cell with at
least 10 dated tablets on both sides (1790-1764 vs 1763-1739). Year = CDLI ruler + regnal year, else Archibab absolute
year (middle chronology). Standardized median shift (pooled MAD) and a permutation p within the cell (5,000 draws).
Output: turning/hammurabi_cells_archibab.csv"""
from _paths import WORK
import pandas as pd, numpy as np
R=WORK; rng=np.random.default_rng(7)
d=pd.read_parquet(f'{R}/master_tablets.parquet'); d=d[(d.period=='Old Babylonian')&d.photo_hw.between(1/3,3)].copy()
if 'loghw' not in d: d['loghw']=np.log(d.photo_hw)
OB={'Rim-Sin':1822,'Hammurapi':1792,'Samsu-iluna':1749,'Warad-Sin':1834,'Sin-muballit':1812}
d['bce']=np.where(d.ruler.isin(OB)&d.ryear.notna(),d.ruler.map(OB)-(d.ryear.clip(lower=1)-1),np.nan)
A=pd.read_csv(f'{R}/turning/companion_dates.csv')[['id','ab_bce']]
d=d.merge(A,on='id',how='left'); d['src']=np.where(d.bce.notna(),'CDLI','Archibab'); d['bce']=d.bce.fillna(d.ab_bce)
d=d[d.bce.between(1739,1790)]; d['post']=(d.bce<=1763).astype(int)
FE=['loghw','corner_fill','rect','thick_side']+[f'X{i}' for i in range(1,13)]
mad=lambda x: np.median(np.abs(x-np.median(x)))*1.4826
cells=d.groupby(['site','genre']).post.agg(['sum','count']); cells['before']=cells['count']-cells['sum']
cells=cells[(cells['sum']>=10)&(cells.before>=10)&~cells.index.get_level_values(0).isin(['unknown','uncertain'])]
print(cells)
rows=[]
for (site,g) in cells.index:
    c=d[(d.site==site)&(d.genre==g)]
    for f in FE:
        x=c[[f,'post']].dropna(); a=x[x.post==1][f].values; b=x[x.post==0][f].values
        if len(a)<8 or len(b)<8: continue
        s=mad(x[f].values) or x[f].std(); obs=(np.median(a)-np.median(b))/s
        v=x[f].values; n=len(a); null=np.empty(5000)
        for i in range(5000):
            p=rng.permutation(v); null[i]=(np.median(p[:n])-np.median(p[n:]))/s
        rows.append(dict(site=site,genre=g,feature=f,n_before=len(b),n_after=len(a),from_archibab=int((c.src=='Archibab').sum()),shift=round(obs,2),p=round(float(np.mean(np.abs(null)>=abs(obs))),4)))
r=pd.DataFrame(rows)
# Benjamini-Hochberg across all tests
r=r.sort_values('p'); m=len(r); r['q']=np.minimum.accumulate((r.p*m/np.arange(1,m+1))[::-1])[::-1].clip(upper=1).round(4)
r.sort_values(['site','genre','feature']).to_csv(f'{R}/turning/hammurabi_cells_archibab.csv',index=False)
print(r.sort_values('p').head(12).to_string()); print('tests',m,'q<0.05:',int((r.q<0.05).sum()))
