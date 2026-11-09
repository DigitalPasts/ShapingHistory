"""Pilot 3 (point 7): which elements of form go with which parameter?
Elements = proportion (log h/w, photographs) and four features estimated from the twelve VAE dimensions with ridge
regression trained on tablets measured directly from their six views (script 56; Ur III, Middle Babylonian, Middle
Assyrian, Neo-Babylonian): thickness at the sides, thickness at the ends, rectangularity, corner fill.
For each period row (archival documents): median and robust spread (MAD) of each element. Then Spearman correlation of
each element with each parameter across periods, with permutation p (5,000)."""
from _paths import WORK
import pandas as pd, numpy as np
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import cross_val_score
from scipy.stats import spearmanr
R=WORK; rng=np.random.default_rng(4)
X=[f'X{i}' for i in range(1,13)]; FE=['thick_side','thick_end','rect','corner_fill']
d=pd.read_parquet(f'{R}/master_tablets.parquet')
tr=d.dropna(subset=FE+X)
rec={}
for f in FE:
    m=RidgeCV(alphas=np.logspace(-2,3,12)); rec[f]=cross_val_score(m,tr[X].values,tr[f].values,cv=5,scoring='r2').mean()
    d[f+'_est']=m.fit(tr[X].values,tr[f].values).predict(d[X].values)
ARCH=['Administrative','Letter','Legal','Business / Contracts','Account','Receipt']
d=d[d.genre.isin(ARCH)&d.photo_hw.between(1/3,3)].copy(); d['lh']=np.log(d.photo_hw)
d['row']=d.period
d.loc[(d.period=='Achaemenid')&(d.site=='Pārśa'),'row']='Achaemenid (Persepolis)'
d.loc[(d.period=='Achaemenid')&(d.site!='Pārśa'),'row']='Achaemenid (Babylonia)'
W=pd.read_csv(f'{R}/centralization_scores_wide.csv',index_col=0); I=pd.read_csv(f'{R}/centralization_indices.csv',index_col=0)
P=W.join(I[['A_polity_reach','B_institutional_economy','C_control_of_writing','PC1_all']])
EL=['lh']+[f+'_est' for f in FE]
def mad(x): return np.median(np.abs(x-np.median(x)))
T=d[d.row.isin(P.index)].groupby('row').filter(lambda g:len(g)>=30).groupby('row')[EL].agg(['median',mad])
T.columns=[f'{a}_{b}' for a,b in T.columns]; T.round(4).to_csv(f'{R}/pilot3_period_elements.csv')
res=[]
for e in T.columns:
    for p in P.columns:
        x=P.loc[T.index,p].values; y=T[e].values; r=spearmanr(x,y)[0]
        null=np.array([spearmanr(rng.permutation(x),y)[0] for _ in range(5000)])
        res.append(dict(element=e,parameter=p,rho=round(r,3),p_perm=round((1+(np.abs(null)>=abs(r)).sum())/5001,4)))
S=pd.DataFrame(res); S.to_csv(f'{R}/pilot3_parameters_vs_elements.csv',index=False)
pd.Series(rec).round(3).to_csv(f'{R}/pilot3_feature_recovery.csv')
if __name__=='__main__':
    print('recovery R2',{k:round(v,2) for k,v in rec.items()},'train n',len(tr))
    print(T.round(3).to_string())
    print(S.pivot(index='parameter',columns='element',values='rho').to_string())
    s=S[S.p_perm<0.05].sort_values('p_perm'); print(s.to_string())
