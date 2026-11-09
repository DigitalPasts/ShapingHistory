"""Robust tests of the centralization hypothesis on the 14 main periods, using the literature-grounded scores (script 85).

Question: are the archival tablets of more centralized regimes more uniform in shape?
Outcome (tablet level): y = log(height/width) from the photograph, archival genres only. Dispersion of y within a period
is the quantity of interest; the VAE vector (12 dimensions) gives a second outcome.
Predictors (period level): four indices built from the 12 parameters (PRIV reversed): A polity reach (TERR, HIER, FISC,
COMM), B institutional economy (PAL, TEMP, TCTL, PRIV), C control of writing (BUR, SCHOOL, LAW, STD), and the mean of all 12.

Step 1. Period table: MAD of y (pooled and within museum), median VAE distance (pooled and within museum).
Step 2. Spearman rank correlation of each outcome with each index; two-sided p from 50,000 random permutations of the
        index values across the 14 periods (Fisher randomization: under the null, the scores carry no information about
        dispersion, so any assignment of scores to periods is equally likely).
Step 3. Score uncertainty: 2,000 draws of the whole score table, each cell drawn from its distribution (script 85, rule 7);
        the Spearman correlation is recomputed for every draw. We report its median and 2.5-97.5% range.
Step 4. Tablet-level regression with museum fixed effects: |y - period median| (and |y - period-by-museum median|) on the
        index; inference by the wild cluster restricted bootstrap (Webb six-point weights, 9,999 draws, clusters = the 14
        periods), which keeps the right size with few clusters (Cameron, Gelbach and Miller 2008; Webb 2023; Roodman et al. 2019).
Outputs go to centralization/stats_*.csv."""
from _paths import WORK
import json, numpy as np, pandas as pd
from scipy.stats import spearmanr
R=WORK; C=f'{R}/centralization'; rng=np.random.default_rng(7)
PARAMS=['TERR','HIER','FISC','COMM','PAL','TEMP','TCTL','PRIV','BUR','SCHOOL','LAW','STD']
MAIN=['ED IIIa','ED IIIb','Ebla','Old Akkadian','Ur III','Early Old Babylonian','Old Babylonian','Old Assyrian',
      'Middle Babylonian','Middle Assyrian','Neo-Assyrian','Neo-Babylonian','Achaemenid','Hellenistic']
DIMS={'A_polity_reach':['TERR','HIER','FISC','COMM'],'B_institutional_economy':['PAL','TEMP','TCTL','PRIV'],
      'C_control_of_writing':['BUR','SCHOOL','LAW','STD'],'mean_all':PARAMS}
X=[f'X{i}' for i in range(1,13)]
ARCH=['Administrative','Letter','Legal','Business / Contracts','Account','Receipt']
d=pd.read_parquet(f'{R}/master_tablets.parquet')
d=d[d.genre.isin(ARCH)&d.photo_hw.between(1/3,3)&d.period.isin(MAIN)].copy()
d['y']=np.log(d.photo_hw); d[X]=(d[X]-d[X].mean())/d[X].std()
def indices(W):
    Z=W.copy(); Z['PRIV']=3-Z['PRIV']; return pd.DataFrame({k:Z[v].mean(axis=1) for k,v in DIMS.items()})
L=pd.read_csv(f'{C}/lit_scores_long.csv'); L=L[L.period.isin(MAIN)]
W=L.pivot(index='period',columns='param',values='score')[PARAMS].loc[MAIN]; I=indices(W)
# Step 1
def mad(x): return np.median(np.abs(x-np.median(x)))
def vaed(v): return np.median(np.linalg.norm(v-np.median(v,axis=0),axis=1))
def within(g,f,cols):
    out=[(f(m[cols].values),len(m)) for _,m in g.groupby('museum') if len(m)>=30]
    if not out: return np.nan
    v,n=zip(*out); return np.average(v,weights=n)
rows=[]
for p,g in d.groupby('period'):
    rows.append(dict(period=p,n=len(g),n_museums=g.museum.nunique(),MAD=mad(g.y.values),MAD_in_museum=within(g,lambda a:mad(a.ravel()),['y']),
                     VAEd=vaed(g[X].values),VAEd_in_museum=within(g,vaed,X)))
T=pd.DataFrame(rows).set_index('period').loc[MAIN].join(I)
T.round(4).to_csv(f'{C}/stats_period_table.csv')
OUT=['MAD','MAD_in_museum','VAEd','VAEd_in_museum']
# Step 2 and 3
cells={(r.period,r.param):(lambda a:a/a.sum())(np.array(json.loads(r.dist))) for r in L.itertuples()}
draws=[]
for _ in range(2000):
    Wd=W.copy().astype(float)
    for (p,k),pr in cells.items(): Wd.loc[p,k]=rng.choice(4,p=pr)
    draws.append(indices(Wd))
res=[]
for o in OUT:
    t=T.dropna(subset=[o])
    for k in DIMS:
        x=t[k].values; y=t[o].values; r=spearmanr(x,y)[0]
        null=np.array([spearmanr(rng.permutation(x),y)[0] for _ in range(50000)])
        rd=np.array([spearmanr(D.loc[t.index,k].values,y)[0] for D in draws])
        res.append(dict(outcome=o,index=k,n_periods=len(t),rho=r,p_perm=(1+(np.abs(null)>=abs(r)).sum())/50001,
                        rho_draws_median=np.nanmedian(rd),rho_draws_lo=np.nanpercentile(rd,2.5),rho_draws_hi=np.nanpercentile(rd,97.5),
                        share_draws_negative=np.mean(rd<0)))
S=pd.DataFrame(res); S.round(4).to_csv(f'{C}/stats_spearman.csv',index=False)
# Step 4
top=d.museum.value_counts(); keep=top[top>=200].index; d['mus']=np.where(d.museum.isin(keep),d.museum,'other')
d['dev_period']=(d.y-d.groupby('period').y.transform('median')).abs()
d['dev_pm']=(d.y-d.groupby(['period','mus']).y.transform('median')).abs()
D=pd.get_dummies(d.mus,drop_first=False).values.astype(float)
def partial(v):  # residualize on museum dummies (fixed effects)
    beta,*_=np.linalg.lstsq(D,v,rcond=None); return v-D@beta
WEBB=np.array([-np.sqrt(1.5),-1,-np.sqrt(.5),np.sqrt(.5),1,np.sqrt(1.5)])
g=pd.Categorical(d.period,categories=MAIN).codes; G=len(MAIN)
wcb=[]
for outc in ['dev_period','dev_pm']:
    yt=partial(d[outc].values)
    for k in DIMS:
        xt=partial(d.period.map(I[k]).values.astype(float)); xt=(xt)/xt.std()
        Sxx=(xt**2).sum(); b=(xt*yt).sum()/Sxx; e=yt-b*xt
        Sg=np.bincount(g,xt*e,G); se=np.sqrt(G/(G-1)*(Sg**2).sum())/Sxx; t=b/se
        u=yt  # restricted residuals (b=0)
        Su=np.bincount(g,xt*u,G); Sxxg=np.bincount(g,xt**2,G)
        w=rng.choice(WEBB,size=(9999,G))
        bs=(w*Su).sum(1)/Sxx
        sc=w*Su-bs[:,None]*Sxxg
        ses=np.sqrt(G/(G-1)*(sc**2).sum(1))/Sxx; ts=bs/ses
        wcb.append(dict(outcome=outc,index=k,b_per_sd=b,se_cluster=se,t=t,p_wcr=(1+(np.abs(ts)>=abs(t)).sum())/10000,
                        mean_outcome=d[outc].mean(),n_tablets=len(d)))
B=pd.DataFrame(wcb); B.round(5).to_csv(f'{C}/stats_wild_cluster.csv',index=False)
print(T.round(3).to_string()); print(S.round(3).to_string()); print(B.round(4).to_string())
