"""Point 9 revisited: which event in Hammurabi's reign (if any) marks a change in legal tablets?
Candidate break points, chosen from the historical literature before looking at the data:
  mīšarum 1   1791 BCE  Hammurabi year 2, inaugural edict of redress (Boivin, OHANE II ch. 18, p. 606)
  conquest    1763 BCE  fall of Larsa, Hammurabi year 30/31 (Boivin p. 596)
  Laws        1754 BCE  Laws of Hammurabi, stele composed after year 38-39 (prologue lists conquests to year 38);
              sensitivity at 1750 BCE (year 43)
  mīšarum 2   1748 BCE  Samsu-iluna year 2, inaugural edict of redress
Data: dated Old Babylonian legal tablets (Legal; Business/Contracts) from script 75, absolute year from Archibab or from
the CDLI ruler and regnal year (middle chronology), 1830-1712 BCE; south = former kingdom of Larsa, north = Babylon.
For every candidate b, post = year <= b. Three outcomes:
  (1) shape: log h/w ~ south*post + museum + damage (OLS); the interaction is the difference-in-differences;
  (2) uniformity: |log h/w - median of its region-by-phase cell| ~ south*post + museum + damage;
  (3) convergence: distance between southern and northern median VAE vectors after minus before (permutation p).
'Most productive' is defined in advance as the break with the lowest AIC for outcome (1) among the candidates; Akaike
weights express how much better it is than the others. A scan of every year from 1800 to 1725 BCE shows the full profile,
so the reader can see whether the chosen break is a genuine optimum or one point on a plateau."""
from _paths import WORK
import numpy as np, pandas as pd, warnings; warnings.filterwarnings('ignore')
import statsmodels.formula.api as smf
R=WORK; CD=f'{R}/centralization'; rng=np.random.default_rng(11)
X=[f'X{i}' for i in range(1,13)]
t=pd.read_csv(f'{R}/pilot5_hammurabi_tablets.csv')
t=t[(t.grp=='legal')&t.bce_all.between(1712,1830)].copy()
t['lh']=np.log(t.photo_hw); t['south']=(t.region=='south').astype(int)
mus=t.museum.value_counts(); t['mus']=np.where(t.museum.isin(mus[mus>=15].index),t.museum,'other')
CAND={'mīšarum 1 (Ham 2, 1791)':1791,'conquest of Larsa (1763)':1763,'Laws (Ham 39, 1754)':1754,'Laws, late date (Ham 43, 1750)':1750,'mīšarum 2 (Samsu-iluna 2, 1748)':1748}
def fit(b):
    g=t.copy(); g['post']=(g.bce_all<=b).astype(int)
    g['dev']=(g.lh-g.groupby(['region','post']).lh.transform('median')).abs()
    m1=smf.ols('lh ~ south*post + C(mus) + damage',data=g).fit(cov_type='HC1')
    m2=smf.ols('dev ~ south*post + C(mus) + damage',data=g).fit(cov_type='HC1')
    return g,m1,m2
def gap(df):
    return float(np.linalg.norm(df[df.region=='south'][X].median()-df[df.region=='north'][X].median()))
rows=[]
for name,b in CAND.items():
    g,m1,m2=fit(b); cells=g.groupby(['region','post']).size().to_dict()
    obs=gap(g[g.post==1])-gap(g[g.post==0]); null=[]
    for _ in range(2000):
        h=g.copy(); h['post']=h.groupby('region').post.transform(lambda s: rng.permutation(s.values))
        null.append(gap(h[h.post==1])-gap(h[h.post==0]))
    rows.append(dict(break_point=name,year=b,cells=cells,AIC_shape=m1.aic,DiD_shape=m1.params['south:post'],DiD_shape_se=m1.bse['south:post'],DiD_shape_p=m1.pvalues['south:post'],
                     AIC_uniformity=m2.aic,DiD_uniformity=m2.params['south:post'],DiD_uniformity_se=m2.bse['south:post'],DiD_uniformity_p=m2.pvalues['south:post'],
                     VAE_gap_change=obs,p_convergence=(1+(np.array(null)<=obs).sum())/2001))
O=pd.DataFrame(rows)
for a in ['AIC_shape','AIC_uniformity']:
    dl=O[a]-O[a].min(); O[a.replace('AIC','akaike_w')]=np.exp(-dl/2)/np.exp(-dl/2).sum()
best=O.loc[O.AIC_shape.idxmin(),'break_point']; O['chosen']=O.break_point.eq(best)
O.to_csv(f'{CD}/hammurabi_breaks.csv',index=False)
scan=[]
for b in range(1800,1724,-1):
    g,m1,m2=fit(b); n=g.groupby(['region','post']).size()
    if len(n)<4 or n.min()<15: continue
    scan.append(dict(year=b,AIC_shape=m1.aic,DiD_shape=m1.params['south:post'],p_shape=m1.pvalues['south:post'],AIC_uniformity=m2.aic,DiD_uniformity=m2.params['south:post'],min_cell=int(n.min())))
Sc=pd.DataFrame(scan); Sc.to_csv(f'{CD}/hammurabi_break_scan.csv',index=False)
pd.set_option('display.width',250)
print(O.drop(columns='cells').round(4).to_string()); print(O[['break_point','cells']].to_string())
print(Sc.round(4).to_string())
