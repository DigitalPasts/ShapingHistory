"""Pilot 1 (points 3, 4, 7): do period-level centralization scores predict how uniform, and how tall, each period's
documents are?  Unit = period row of the parameter table (17 rows; Achaemenid split into Babylonia and Persepolis).
Outcomes, archival documents only (Administrative, Letter, Legal, Business/Contracts, Account, Receipt), from the photographs:
  MAD    median absolute deviation of log h/w around the period median (pooled, and within museum, the museum-controlled
         version: median of within-museum MADs over museums with >= 30 tablets, weighted by n)
  VAEd   median Euclidean distance to the period's median VAE vector (12 standardized dimensions), pooled and within museum
  tall   share of tablets taller than wide (h/w > 1.05)
Tests: Spearman rank correlation with each parameter and index; p from 20,000 permutations of the score rows across
periods (n = 17 is small; this is a pilot, not a result)."""
from _paths import WORK
import pandas as pd, numpy as np
from scipy.stats import spearmanr
R=WORK; rng=np.random.default_rng(1)
X=[f'X{i}' for i in range(1,13)]
d=pd.read_parquet(f'{R}/master_tablets.parquet')
ARCH=['Administrative','Letter','Legal','Business / Contracts','Account','Receipt']
d=d[d.genre.isin(ARCH)&d.photo_hw.between(1/3,3)].copy()
d['row']=d.period
d.loc[(d.period=='Achaemenid')&(d.site=='Pārśa'),'row']='Achaemenid (Persepolis)'
d.loc[(d.period=='Achaemenid')&(d.site!='Pārśa'),'row']='Achaemenid (Babylonia)'
d['lh']=np.log(d.photo_hw)
Zs=(d[X]-d[X].mean())/d[X].std(); d[X]=Zs
W=pd.read_csv(f'{R}/centralization_scores_wide.csv',index_col=0); I=pd.read_csv(f'{R}/centralization_indices.csv',index_col=0)
def mad(x): return np.median(np.abs(x-np.median(x)))
def vaed(v): return np.median(np.linalg.norm(v-np.median(v,axis=0),axis=1))
def within(g,f,col):
    out=[(f(m[col].values if col!='X' else m[X].values),len(m)) for _,m in g.groupby('museum') if len(m)>=30]
    if not out: return np.nan
    v,n=zip(*out); return np.average(v,weights=n)
rows=[]
for r,g in d.groupby('row'):
    if r not in W.index or len(g)<30: continue
    rows.append(dict(row=r,n=len(g),median_hw=np.exp(np.median(g.lh)),tall=(g.photo_hw>1.05).mean(),MAD=mad(g.lh.values),
        MAD_in_museum=within(g,mad,'lh'),VAEd=vaed(g[X].values),VAEd_in_museum=within(g,vaed,'X'),
        damage=g.damage.median(),top_museum_share=g.museum.value_counts(normalize=True).iloc[0]))
O=pd.DataFrame(rows).set_index('row')
T=O.join(W).join(I)
T.round(4).to_csv(f'{R}/pilot1_period_table.csv')
PRED=list(W.columns)+['A_polity_reach','B_institutional_economy','C_control_of_writing','scribal_institution','PC1_all']
OUT=['MAD','MAD_in_museum','VAEd','VAEd_in_museum','tall']
res=[]
for o in OUT:
    t=T.dropna(subset=[o])
    for p in PRED:
        x=t[p].values; y=t[o].values; r=spearmanr(x,y)[0]
        null=np.array([spearmanr(rng.permutation(x),y)[0] for _ in range(20000)])
        res.append(dict(outcome=o,predictor=p,n_periods=len(t),rho=round(r,3),p_perm=round((1+(np.abs(null)>=abs(r)).sum())/20001,4)))
S=pd.DataFrame(res); S.to_csv(f'{R}/pilot1_spearman.csv',index=False)
if __name__=='__main__':
    print(T[['n','median_hw','tall','MAD','MAD_in_museum','VAEd','VAEd_in_museum','A_polity_reach','B_institutional_economy','C_control_of_writing','PC1_all']].round(3).to_string())
    print(S.pivot(index='predictor',columns='outcome',values='rho').loc[PRED].to_string())
    print(S.pivot(index='predictor',columns='outcome',values='p_perm').loc[PRED].to_string())
