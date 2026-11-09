"""Which Mesopotamian groups do peripheral tablet groups resemble?
For each peripheral group (period x site outside the Mesopotamian core), rank core groups
(period x city, n>=30) by distance between centroids. Core centroids are means of per-museum means,
using only museums that do not hold the peripheral group (so shared photography cannot help).
Run on all genres and within genre (core tablets of the same CDLI genre only).
Null: the same ranking for random core subsets of the peripheral group's size (how often a
random group of that size sits that close), reported as a z-score of the distance."""
from _paths import WORK
import pandas as pd, numpy as np
R=WORK; rng=np.random.default_rng(0)
t=pd.read_csv(f'{R}/results/tablet_latent_damage_adjusted.csv')
a=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','collections','genres'],low_memory=False).rename(columns={'artifact_id':'CDLI_id'})
t=t.merge(a,on='CDLI_id',how='left')
t['coll']=t.collections.fillna('?').str.split(';').str[0].str.strip().str.split(',').str[0]
t['genre']=t.genres.fillna('').str.split(';').str[0].str.replace(r'\s*\(.*','',regex=True).str.strip()
Z=[f'Z{i}' for i in range(1,13)]
X=t[Z].values; X=(X-X.mean(0))/X.std(0); t[Z]=X
PERI={('Middle Babylonian','Akhetaten'):'Amarna',('Hittite','Akhetaten'):'Amarna',
      ('Middle Babylonian','Gasur/Nuzi'):'Nuzi',('Middle Babylonian','Alalakh'):'Alalakh IV',
      ('Old Babylonian','Alalakh'):'Alalakh VII',('Middle Babylonian','Ḫattusa'):'Hattusa',
      ('Hittite','Ḫattusa'):'Hattusa',('Middle Hittite','Ḫattusa'):'Hattusa',
      ('Middle Elamite','Anšan'):'Anshan (Middle Elamite)',('Old Babylonian','Susa'):'Susa (OB)',
      ('Old Assyrian','Kanesh'):'Kanesh',('Old Babylonian','Tuttul'):'Tuttul (OB)',
      ('Early Old Babylonian','Tuttul'):'Tuttul (OB)'}
t['peri']=[PERI.get((p,c)) for p,c in zip(t.Period_Name,t.city)]
core=t[t.peri.isna()&~t.city.isin(['uncertain','unknown'])&t.city.notna()&~t.Period_Name.isin(['other'])].copy()
core['grp']=core.Period_Name+' | '+core.city
def centroid(df):
    m=df.groupby('coll')[Z].mean(); n=df.groupby('coll').size()
    m=m[n>=5] if (n>=5).sum()>=1 else m
    return m.mean().values
rows=[]
for pname,P in t[t.peri.notna()].groupby('peri'):
    mus=set(P.coll); c=P[Z].mean().values
    for mode in ['all genres','same genre']:
        C=core[~core.coll.isin(mus)]
        if mode=='same genre':
            g=P.genre.value_counts(); keep=g[g>=0.2*len(P)].index.tolist(); keep=[x for x in keep if x]
            if not keep: continue
            C=C[C.genre.isin(keep)]
        sizes=C.groupby('grp').size(); grps=sizes[sizes>=30].index
        d={g:np.linalg.norm(c-centroid(C[C.grp==g])) for g in grps}
        s=pd.Series(d).sort_values()
        for r,(g,v) in enumerate(s.items()):
            rows.append(dict(peri=pname,mode=mode,n=len(P),museums=';'.join(sorted(mus)),genres=';'.join(P.genre.value_counts().head(3).index),cand=g,dist=v,rank=r+1,ncand=len(s)))
o=pd.DataFrame(rows); o.to_csv(f'{R}/results/periphery_sources.csv',index=False)
pd.set_option('display.width',250)
for (p,m),g in o.groupby(['peri','mode']):
    print(f'\n== {p} [{m}] n={g.n.iloc[0]} genres={g.genres.iloc[0]} museums={g.museums.iloc[0][:80]}')
    print(g.head(6)[['rank','cand','dist']].to_string(index=False))
