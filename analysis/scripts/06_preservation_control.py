"""Preservation as a control (not a filter).
1. A per-tablet damage score: logistic model predicting CDLI's own preservation label (fragment/partial vs
   complete) from mask features (obverse solidity, enclosed holes, number of views). Applied to every tablet.
2. How damage relates to each result: (a) VAE latent dispersion, raw vs adjusted for damage (latent codes
   residualised on damage within periods); (b) masked-ResNet F1 by damage tercile; (c) agreement of pixel
   and physical h/w by damage tercile."""
from _paths import WORK
import pandas as pd, numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import roc_auc_score, f1_score
from scipy.stats import spearmanr
R=WORK
d=pd.concat([pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_{s}.csv') for s in ['train','val','test']])
m=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','artifact_type','artifact_preservation','height','width','provenience'],low_memory=False)
q=pd.read_csv(f'{R}/results/mask_quality.csv').merge(pd.read_csv(f'{R}/results/face_features.csv'),on='CDLI_id')
d=d.merge(m,left_on='CDLI_id',right_on='artifact_id').merge(q,on='CDLI_id')
d=d[d.artifact_type.isin(['tablet','tablet & envelope'])].copy()
# outline features; the score is fitted with period dummies so it learns damage WITHIN periods, not period shape
F=pd.DataFrame({'ext1':d.ext1,'ext2':d.ext2,'sol1':d.sol1,'sol2':d.sol2,'hole':np.log1p(100*d.hole_frac.clip(0,1)),
                'parts':(d.n_big_parts-6).abs().clip(0,6)}).fillna(0)
D=pd.get_dummies(d.Period_Name,prefix='p',dtype=float)
lab=d.artifact_preservation.fillna('').str.lower().map(lambda s: 0 if s in ('complete','nearly complete') else (1 if s=='fragment' else np.nan))
k=lab.notna().values
clf=LogisticRegression(max_iter=3000,C=1.0)
FD=pd.concat([F,D],axis=1)
cv=cross_val_predict(clf,FD[k],lab[k],cv=5,method='predict_proba')[:,1]
print('labelled tablets',k.sum(),'| fragment share',lab[k].mean().round(3),'| CV AUC of damage score',round(roc_auc_score(lab[k],cv),3))
clf.fit(FD[k],lab[k]); w=clf.coef_[0][:F.shape[1]]
print('coef',dict(zip(F.columns,w.round(2))))
d['damage']=1/(1+np.exp(-(F.values@w - (F.values@w).mean())))   # period-free damage index (features only)
print('AUC of period-free index on labelled', round(roc_auc_score(lab[k],d.damage[k]),3))
X=[f'X{i}' for i in range(1,13)]; Z=(d[X]-d[X].mean())/d[X].std()
# within-period residualisation on damage (period fixed effects)
Zc=Z-Z.groupby(d.Period_Name).transform('mean'); dc=d.damage-d.groupby('Period_Name').damage.transform('mean')
lr=LinearRegression().fit(np.c_[dc,dc**2],Zc); Zadj=Z-lr.predict(np.c_[dc,dc**2])+lr.predict(np.zeros((1,2)))
print('share of within-period latent variance explained by damage', round(1-((Zc-lr.predict(np.c_[dc,dc**2]))**2).values.sum()/(Zc**2).values.sum(),3))
def disp(V): return np.median(np.linalg.norm(V-np.median(V,0),axis=1))
rows=[]
for p,g in d.groupby('Period_Name'):
    if len(g)<100 or p=='other': continue
    i=g.index; zi=Z.loc[i].values; dist=np.linalg.norm(zi-np.median(zi,0),axis=1)
    rows.append(dict(period=p,n=len(g),mean_damage=g.damage.mean(),disp_raw=disp(zi),disp_adj=disp(Zadj.loc[i].values),
                     rho_damage_vs_distance=spearmanr(g.damage,dist)[0]))
T=pd.DataFrame(rows).sort_values('disp_raw'); T['rank_raw']=T.disp_raw.rank(); T['rank_adj']=T.disp_adj.rank()
print(T.round(2).to_string(index=False)); print('rank agreement raw vs adjusted', round(spearmanr(T.disp_raw,T.disp_adj)[0],2),
      '| damage vs raw dispersion across periods', round(spearmanr(T.mean_damage,T.disp_raw)[0],2))
T.to_csv(f'{R}/results/dispersion_damage_adjusted.csv',index=False)
# classification by damage tercile
P=pd.read_csv(f'{R}/results/resnet_masked_test_predictions.csv').merge(d[['CDLI_id','damage']],on='CDLI_id')
P['terc']=pd.qcut(P.damage,3,labels=['least damaged','middle','most damaged'])
c=P.groupby('terc',observed=True).apply(lambda s: pd.Series({'n':len(s),'acc':(s.y==s.pred).mean(),'macroF1_present':f1_score(s.y,s.pred,average='macro')}))
print(c.round(3)); c.to_csv(f'{R}/results/resnet_by_damage.csv')
# pixel vs physical by damage
pix=pd.read_csv(f'{R}/zenodo/h_w_ratio_df_all.csv'); pix['CDLI_id']=pix.tablet_p_id_CDLI.str.lstrip('P').astype(int)
x=d.merge(pix[['CDLI_id','hw_ratio']],on='CDLI_id'); x=x[x.height.gt(0)&x.width.gt(0)].copy(); x['phys']=x.height/x.width
x['terc']=pd.qcut(x.damage,3,labels=['least damaged','middle','most damaged'])
print(x.groupby('terc',observed=True).apply(lambda s: pd.Series({'n':len(s),'rho_pixel_physical':spearmanr(s.hw_ratio,s.phys)[0],
      'orientation_disagree':((s.hw_ratio>1)!=(s.phys>1)).mean()})).round(3))
d[['CDLI_id','Period_Name','damage']].to_csv(f'{R}/results/damage_score.csv',index=False)
