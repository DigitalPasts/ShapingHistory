"""What do the twelve VAE dimensions record?  Each dimension is regressed on the twelve view-wise descriptors of
script 56 (all tablets with a silhouette in the case-study sets), and the strongest descriptor correlations are listed.
Also: which descriptors separate the groups in the clearest case-study contrasts."""
from _paths import WORK
import pandas as pd, numpy as np
from sklearn.linear_model import LinearRegression
from scipy.stats import mannwhitneyu, spearmanr
R=WORK; X=[f'X{i}' for i in range(1,13)]
GEO=['hw','rect','solidity','circ','corner_fill','taper','side_bulge','end_bulge','rev_corner_fill','rev_obv','thick_side','thick_end']
v=pd.concat([pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_{s}.csv') for s in ['train','val','test']]).drop_duplicates('CDLI_id').rename(columns={'CDLI_id':'id'})
g=pd.read_csv(f'{R}/results/silhouette_geometry.csv'); g=g.fillna(g.median()); g['hw']=np.log(g.hw)
F=v[['id']+X].merge(g,on='id'); Gz=(F[GEO]-F[GEO].median())/F[GEO].std()
rows=[]
for x in X:
    r2=LinearRegression().fit(Gz.clip(-5,5),F[x]).score(Gz.clip(-5,5),F[x])
    cs=sorted(((spearmanr(F[x],F[c])[0],c) for c in GEO),key=lambda t:-abs(t[0]))[:3]
    rows.append(dict(dim=x,R2_from_descriptors=round(r2,2),top=', '.join(f'{c} {r:+.2f}' for r,c in cs)))
T=pd.DataFrame(rows); print(len(F),'tablets'); print(T.to_string(index=False)); T.to_csv(f'{R}/results/vae_dimensions.csv',index=False)
# contrasts
U=pd.read_csv(f'{R}/results/SI_ur3_text_types.csv'); U['id']=U.P.str[1:].astype(int)
a=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','collections'],low_memory=False).rename(columns={'artifact_id':'id'})
U=U.drop(columns='hw').merge(a,on='id').merge(g,on='id')
A=pd.read_csv(f'{R}/amarna/SI_amarna_letters.csv'); A['id']=A.P.str[1:].astype(float); A=A[A.museum.eq('Vorderasiatisches Museum')].merge(g,on='id')
great={'Babylon','Mittani','Hattusa','Alashiya','Arzawa','Assur','Egypt','Akhetaten'}
C=[('Ur III receipts at Harvard',U[U.collections.fillna('').str.startswith('Harvard')&U.type_used.eq('receipt (šu ba-ti)')],'province','Puzriš-Dagan','Girsu'),
   ('Ur III messenger texts at Harvard',U[U.collections.fillna('').str.startswith('Harvard')&U.type_used.eq('Messenger Text')],'province','Girsu','Umma'),
   ('Amarna vassal letters in Berlin',A[~A.city.isin(great)].assign(b=lambda d:np.where(d.city.eq('Byblos'),'Byblos','other')),'b','Byblos','other')]
out=[]
for name,d,lab,p,q in C:
    for c in GEO:
        x,y=d[d[lab]==p][c],d[d[lab]==q][c]
        out.append(dict(contrast=name,group1=p,group2=q,descriptor=c,median1=round(x.median(),3),median2=round(y.median(),3),n1=len(x),n2=len(y),p=mannwhitneyu(x,y).pvalue))
O=pd.DataFrame(out); O.to_csv(f'{R}/results/vae_contrast_descriptors.csv',index=False)
print(O[O.p<0.01].assign(p=lambda d:d.p.map('{:.0e}'.format)).to_string(index=False))
# the other direction: how well do the twelve VAE dimensions recover each measurable feature? (5-fold CV R2, ridge)
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import cross_val_score
NAMES={'hw':'proportion (height ÷ width, obverse)','thick_side':'thickness at the sides ÷ width','thick_end':'thickness at top and bottom ÷ width',
 'corner_fill':'squareness of the corners (obverse)','rev_corner_fill':'squareness of the corners (reverse)','rect':'rectangularity of the obverse',
 'circ':'roundness of the outline','solidity':'regularity of the outline (no notches or breaks)','side_bulge':'bulge of the long sides',
 'end_bulge':'bulge of the short sides','taper':'taper (top width ÷ bottom width)','rev_obv':'reverse larger than obverse'}
rows=[]
for c in GEO:
    y=F[c].clip(F[c].quantile(.01),F[c].quantile(.99))
    r2=cross_val_score(RidgeCV(alphas=[0.1,1,10]),F[X].values,y,cv=5,scoring='r2').mean()
    rows.append(dict(feature=c,description=NAMES[c],R2_from_VAE=round(r2,2)))
V=pd.DataFrame(rows).sort_values('R2_from_VAE',ascending=False); print(V.to_string(index=False)); V.to_csv(f'{R}/results/vae_feature_recovery.csv',index=False)
