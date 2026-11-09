"""First-step scan (ShG, 8 Nov 2026): how many distinct ('interesting') tablet groups exist per period, by area and genre,
before any turning point is tested. A group = period x site x genre with >= 30 tablets (sites 'unknown'/'uncertain' and
genre 'unknown' left out). Features: 12 VAE dimensions + log h/w.
Distinctness = root mean square, over the 13 features, of (group median - median of the rest of the period) / period MAD.
Null: the same statistic for random sets of the same size drawn from the period (500 draws); a group is distinct when it
exceeds the 95th percentile of its null (Benjamini-Hochberg over all groups at q = 0.05).
Museum control: the same test run only against tablets of the same period held in the same museum as most of the group.
Variety = median over features of (group MAD / period MAD): below 1 the group is more uniform than its period.
Outputs: turning/group_scan.csv, turning/group_scan_period.csv"""
from _paths import WORK
import pandas as pd, numpy as np
R=WORK; rng=np.random.default_rng(11)
MAIN=['ED IIIa','ED IIIb','Ebla','Old Akkadian','Ur III','Early Old Babylonian','Old Babylonian','Old Assyrian','Middle Babylonian',
      'Middle Assyrian','Neo-Assyrian','Neo-Babylonian','Achaemenid','Hellenistic']
d=pd.read_parquet(f'{R}/master_tablets.parquet')
d=d[d.period.isin(MAIN)&d.photo_hw.between(1/3,3)&~d.site.isin(['unknown','uncertain'])&(d.genre!='unknown')].copy()
FE=[f'X{i}' for i in range(1,13)]+['loghw']; d=d.dropna(subset=FE)
def mad(a,ax=0): return np.median(np.abs(a-np.median(a,axis=ax)),axis=ax)*1.4826
def stat(G,Rst,s): return float(np.sqrt(np.mean(((np.median(G,0)-np.median(Rst,0))/s)**2)))
rows=[]
for per,P in d.groupby('period'):
    X=P[FE].values; s=mad(X); s[s==0]=X.std(0)[s==0]
    for (site,g),Gd in P.groupby(['site','genre']):
        n=len(Gd)
        if n<30 or n>len(P)-30: continue
        idx=P.index.get_indexer(Gd.index); m=np.zeros(len(P),bool); m[idx]=True
        obs=stat(X[m],X[~m],s)
        null=[]
        for _ in range(500):
            r=np.zeros(len(P),bool); r[rng.choice(len(P),n,replace=False)]=True; null.append(stat(X[r],X[~r],s))
        p=(1+np.sum(np.array(null)>=obs))/501
        mus=Gd.museum.value_counts(); mu=mus.index[0]; share=mus.iloc[0]/n
        Q=P[P.museum==mu]; pm=np.nan; obs_m=np.nan
        G2=Gd[Gd.museum==mu]; Rm=Q.drop(G2.index)
        if len(G2)>=20 and len(Rm)>=20:
            obs_m=stat(G2[FE].values,Rm[FE].values,s); Xq=Q[FE].values; k=len(G2); nm=[]
            for _ in range(500):
                r=np.zeros(len(Q),bool); r[rng.choice(len(Q),k,replace=False)]=True; nm.append(stat(Xq[r],Xq[~r],s))
            pm=(1+np.sum(np.array(nm)>=obs_m))/501
        var=float(np.median(mad(X[m])/s))
        rows.append(dict(period=per,site=site,genre=g,n=n,distinct=round(obs,3),p=p,museum=mu,museum_share=round(share,2),
                         distinct_in_museum=None if np.isnan(obs_m) else round(obs_m,3),p_in_museum=pm,variety=round(var,2)))
r=pd.DataFrame(rows)
def bh(p):
    p=np.asarray(p,float); o=np.argsort(p); q=np.empty_like(p); n=len(p)
    q[o]=np.minimum.accumulate((p[o]*n/np.arange(1,n+1))[::-1])[::-1]; return np.minimum(q,1)
r['q']=bh(r.p); ok=r.p_in_museum.notna(); r.loc[ok,'q_in_museum']=bh(r.loc[ok,'p_in_museum'])
r['is_distinct']=r.q<0.05; r['distinct_after_museum']=r.q_in_museum<0.05
r.sort_values(['period','distinct'],ascending=[True,False]).to_csv(f'{R}/turning/group_scan.csv',index=False)
S=r.groupby('period').agg(groups=('n','size'),tablets=('n','sum'),distinct=('is_distinct','sum'),
    testable_in_museum=('p_in_museum',lambda x:x.notna().sum()),distinct_after_museum=('distinct_after_museum','sum'),
    more_uniform=('variety',lambda v:(v<0.8).sum()),more_varied=('variety',lambda v:(v>1.2).sum())).reindex(MAIN).fillna(0).astype(int)
S.to_csv(f'{R}/turning/group_scan_period.csv'); print(S.to_string())
print(r[r.is_distinct].sort_values('distinct',ascending=False).head(25)[['period','site','genre','n','distinct','museum','museum_share','distinct_after_museum','variety']].to_string())
