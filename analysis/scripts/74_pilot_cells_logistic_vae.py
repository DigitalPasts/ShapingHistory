"""Pilot 2 (points 5, 6, 7): genre, place and the centralization parameters, at the level of cells and of tablets.
Data: archival documents with photographs (Administrative/Account/Receipt = admin; Legal/Business = legal; Letter = letter).
(a) Cells = period row x findspot x genre group with >= 25 tablets. OLS of cell uniformity (MAD of log h/w; VAE dispersion)
    on one parameter at a time (z-scored), with genre-group fixed effects and controls (log n, median damage, share of the
    largest museum). Inference: permutation of the parameter rows across periods (2,000), which keeps the fact that the
    parameters vary only between periods.
(b) Tablets: logistic regression of "tall" (h/w > 1.05) on a parameter + genre group + damage, and the same model with the
    full VAE vector as the outcome (multivariate regression; share of VAE variance explained by the parameter beyond genre).
    Permutation across periods as in (a).
(c) Reverse: can the VAE vector of a tablet predict the centralization score of its period when that period is held out?
    Leave-one-period-out ridge regression; the held-out period's mean prediction is compared with its true score.
Pilot only: 15 periods with enough archival photographs."""
from _paths import WORK
import pandas as pd, numpy as np, warnings; warnings.filterwarnings('ignore')
import statsmodels.formula.api as smf
from sklearn.linear_model import Ridge, LogisticRegression
from scipy.stats import spearmanr
R=WORK; rng=np.random.default_rng(2)
X=[f'X{i}' for i in range(1,13)]
d=pd.read_parquet(f'{R}/master_tablets.parquet')
G={'Administrative':'admin','Account':'admin','Receipt':'admin','Legal':'legal','Business / Contracts':'legal','Letter':'letter'}
d=d[d.genre.isin(G)&d.photo_hw.between(1/3,3)].copy(); d['gg']=d.genre.map(G)
d['row']=d.period
d.loc[(d.period=='Achaemenid')&(d.site=='Pārśa'),'row']='Achaemenid (Persepolis)'
d.loc[(d.period=='Achaemenid')&(d.site!='Pārśa'),'row']='Achaemenid (Babylonia)'
W=pd.read_csv(f'{R}/centralization_scores_wide.csv',index_col=0); I=pd.read_csv(f'{R}/centralization_indices.csv',index_col=0)
P=W.join(I[['A_polity_reach','B_institutional_economy','C_control_of_writing','scribal_institution','PC1_all']])
d=d[d.row.isin(P.index)]; keep=d.row.value_counts(); d=d[d.row.isin(keep[keep>=30].index)]
d['lh']=np.log(d.photo_hw); d[X]=(d[X]-d[X].mean())/d[X].std(); d['damage']=d.damage.fillna(d.damage.median())
rows_=sorted(d.row.unique()); Pz=(P.loc[rows_]-P.loc[rows_].mean())/P.loc[rows_].std().replace(0,1)
PRED=['TERR','HIER','FISC','COMM','PAL','TEMP','TCTL','PRIV','BUR','SCHOOL','LAW','STD','A_polity_reach','B_institutional_economy','C_control_of_writing','scribal_institution','PC1_all']
def mad(x): return np.median(np.abs(x-np.median(x)))
# ---------- (a) cells
CELLS=[]
for (r,s,g),c in d[d.site.ne('unknown')].groupby(['row','site','gg']):
    if len(c)<25: continue
    CELLS.append(dict(row=r,site=s,gg=g,n=len(c),MAD=mad(c.lh.values),VAEd=np.median(np.linalg.norm(c[X].values-np.median(c[X].values,0),axis=1)),
                  med=np.median(c.lh),dmg=c.damage.median(),topmus=c.museum.value_counts(normalize=True).iloc[0]))
CELLS=pd.DataFrame(CELLS); CELLS["logn"]=np.log(CELLS.n); CELLS.to_csv(f'{R}/pilot2_cells.csv',index=False)
def fit_cells(Cx,p,o):
    m=smf.ols(f'{o} ~ z + C(gg) + logn + dmg + topmus',data=Cx).fit(cov_type='cluster',cov_kwds={'groups':Cx.row.astype('category').cat.codes})
    return m.params['z'],m.tvalues['z']
import os
outa_done=os.path.exists(f'{R}/pilot2a_cells.csv') and os.environ.get('RERUN_A')!='1'  # (a) is slow; set RERUN_A=1 to redo
outA=[]
for o in ([] if outa_done else ['MAD','VAEd','med']):
    for p in PRED:
        Cx=CELLS.copy(); Cx['z']=Cx.row.map(Pz[p]); b,t=fit_cells(Cx,p,o)
        null=[]
        for _ in range(1000):
            perm=dict(zip(rows_,rng.permutation(Pz[p].values))); Cx['z']=Cx.row.map(perm); null.append(fit_cells(Cx,p,o)[0])
        null=np.array(null); outA.append(dict(outcome=o,predictor=p,cells=len(CELLS),periods=CELLS.row.nunique(),beta=round(b,4),t_cluster=round(t,2),
                                             p_perm=round((1+(np.abs(null)>=abs(b)).sum())/1001,4)))
A=pd.read_csv(f'{R}/pilot2a_cells.csv') if outa_done else pd.DataFrame(outA)
if not outa_done: A.to_csv(f'{R}/pilot2a_cells.csv',index=False)
# ---------- (b) tablets: logistic (tall) and multivariate (VAE)
sub=pd.concat([g.sample(min(len(g),1500),random_state=0) for _,g in d.groupby('row')])
sub['tall']=(sub.photo_hw>1.05).astype(int)
GD=pd.get_dummies(sub.gg,drop_first=True).astype(float).values
def logit_beta(z):
    Xm=np.column_stack([z,GD,sub.damage.values]); m=LogisticRegression(C=1e4,max_iter=2000).fit(Xm,sub.tall.values); return m.coef_[0][0]
def vae_r2(z):
    base=np.column_stack([np.ones(len(sub)),GD,sub.damage.values]); full=np.column_stack([base,z]); Y=sub[X].values
    rb=Y-base@np.linalg.lstsq(base,Y,rcond=None)[0]; rf=Y-full@np.linalg.lstsq(full,Y,rcond=None)[0]
    return 1-(rf**2).sum()/(rb**2).sum()
outB=[]
for p in PRED:
    z=sub.row.map(Pz[p]).values; b=logit_beta(z); r2=vae_r2(z); nb=[]; nr=[]
    for _ in range(500):
        perm=dict(zip(rows_,rng.permutation(Pz[p].values))); zz=sub.row.map(perm).values; nb.append(logit_beta(zz)); nr.append(vae_r2(zz))
    nb=np.array(nb); nr=np.array(nr)
    outB.append(dict(predictor=p,tablets=len(sub),periods=sub.row.nunique(),logit_beta_tall=round(b,3),odds_ratio_per_sd=round(np.exp(b),2),
                     p_perm_logit=round((1+(np.abs(nb)>=abs(b)).sum())/501,4),VAE_partial_R2=round(r2,4),
                     VAE_R2_null_median=round(np.median(nr),4),p_perm_VAE=round((1+(nr>=r2).sum())/501,4)))
B=pd.DataFrame(outB); B.to_csv(f'{R}/pilot2b_tablets.csv',index=False)
# ---------- (c) reverse: LOPO prediction of period scores from VAE (+ ratio)
outC=[]
for p in PRED:
    pred={}
    for r in rows_:
        tr=sub[sub.row!=r]; te=sub[sub.row==r]
        m=Ridge(alpha=10).fit(tr[X+['lh']].values,tr.row.map(P[p]).values); pred[r]=m.predict(te[X+['lh']].values).mean()
    t=pd.Series(pred); true=P.loc[t.index,p]; rho=spearmanr(t,true)[0]
    null=[spearmanr(t,rng.permutation(true.values))[0] for _ in range(5000)]
    outC.append(dict(predictor=p,periods=len(t),rho_heldout=round(rho,3),p_perm=round((1+(np.abs(null)>=abs(rho)).sum())/5001,4)))
Cc=pd.DataFrame(outC); Cc.to_csv(f'{R}/pilot2c_lopo.csv',index=False)
if __name__=='__main__':
    print("cells",len(CELLS),"periods",CELLS.row.nunique())
    print(A.pivot(index='predictor',columns='outcome',values='beta').loc[PRED].round(3).to_string())
    print(A.pivot(index='predictor',columns='outcome',values='p_perm').loc[PRED].to_string())
    print(B.to_string()); print(Cc.to_string())
