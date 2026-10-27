"""A guide to the twelve VAE numbers, for the notebook and the one-page summary released with the article.
For every tablet with a VAE vector (Zenodo 10.5281/zenodo.12787746) the silhouette is measured view by view (script 56).
(1) Each VAE number is matched to the physical measurement it follows most closely (Spearman correlation).
(2) Each measurement is predicted from the twelve numbers (ridge regression, 5-fold cross-validation), which gives its
    reliability, and out-of-fold predictions are saved for every tablet.
(3) For each number, three real tablets are drawn: low, middle and high on that number, typical on the other eleven."""
import pandas as pd, numpy as np, cv2
from scipy.stats import spearmanr
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import KFold, cross_val_predict
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
R='/home/user/repro'; IMG=f'{R}/zenodo/imgs/images_b_w_tablets'; X=[f'X{i}' for i in range(1,13)]
NAMES={'hw':'proportion (height ÷ width of the obverse)','thick_side':'thickness at the sides ÷ width','thick_end':'thickness at top and bottom ÷ width',
 'corner_fill':'squareness of the corners (obverse)','rev_corner_fill':'squareness of the corners (reverse)','rect':'how rectangular the obverse is',
 'circ':'roundness of the outline','solidity':'regularity of the outline (no notches or breaks)','side_bulge':'bulge of the long sides',
 'end_bulge':'bulge of the short sides','taper':'taper (top width ÷ bottom width)','rev_obv':'reverse larger than obverse'}
SHORT={'hw':'proportion','thick_side':'thickness (sides)','thick_end':'thickness (ends)','corner_fill':'square corners','rev_corner_fill':'square corners (rev.)',
 'rect':'rectangularity','circ':'roundness','solidity':'regular outline','side_bulge':'bulging long sides','end_bulge':'bulging short sides','taper':'taper','rev_obv':'reverse > obverse'}
GEO=list(NAMES)
UP={'hw':'taller','thick_side':'thicker at the sides','thick_end':'thicker at the ends','corner_fill':'squarer corners','rev_corner_fill':'squarer corners',
 'rect':'more rectangular','circ':'rounder','solidity':'more regular outline','side_bulge':'bulging long sides','end_bulge':'bulging short sides','taper':'wider at the top','rev_obv':'larger reverse'}
DOWN={'hw':'wider','thick_side':'thinner at the sides','thick_end':'thinner at the ends','corner_fill':'rounder corners','rev_corner_fill':'rounder corners',
 'rect':'less rectangular, more rounded','circ':'less round','solidity':'more irregular outline','side_bulge':'straighter long sides','end_bulge':'straighter short sides','taper':'wider at the bottom','rev_obv':'smaller reverse'}
v=pd.concat([pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_{s}.csv') for s in ['train','val','test']]).drop_duplicates('CDLI_id').rename(columns={'CDLI_id':'id'})
g=pd.read_csv(f'{R}/results/silhouette_geometry.csv')
F=v[['id','Period_Name','Genre_Name']+X].merge(g,on='id'); print(len(v),'vectors,',len(F),'measured')
F['well_preserved']=(F.solidity>0.97)&F.rev_obv.between(0.8,1.25)      # intact outline, obverse and reverse of similar size
F['log_hw']=np.log(F.hw)
# (1) closest measurement for each number
rows=[]
for x in X:
    cs=sorted(((spearmanr(F[x],F[c],nan_policy='omit')[0],c) for c in GEO),key=lambda t:-abs(t[0]))
    (r1,c1),(r2,c2)=cs[0],cs[1]
    rows.append(dict(dim=x,closest=c1,closest_name=NAMES[c1],rho=round(r1,2),second=c2,rho2=round(r2,2),
                     reads='higher = '+(UP[c1] if r1>0 else DOWN[c1]),
                     strength='clear' if abs(r1)>=0.55 else 'partial' if abs(r1)>=0.4 else 'weak'))
D=pd.DataFrame(rows); D.to_csv(f'{R}/results/vae_dimension_guide.csv',index=False); print(D.to_string(index=False))
# (2) reliability of each measurement and out-of-fold predictions for every tablet
P=v[['id']+X].merge(F[['id','well_preserved']],on='id',how='left'); P['well_preserved']=P.well_preserved.fillna(False).astype(bool); P['measured']=P.id.isin(F.id); rel=[]
for c in GEO:
    t='log_hw' if c=='hw' else c; ok=F[t].notna(); lo,hi=F[t].quantile(.01),F[t].quantile(.99)
    y=F[t].clip(lo,hi); W=ok&F.well_preserved; r2={}
    for lab,S in [('all',ok),('well_preserved',W)]:
        pred=cross_val_predict(RidgeCV(alphas=[0.1,1,10]),F.loc[S,X].values,y[S],cv=KFold(5,shuffle=True,random_state=0))
        r2[lab]=1-((y[S]-pred)**2).sum()/((y[S]-y[S].mean())**2).sum()
        if lab=='well_preserved': P.loc[P.id.isin(F.loc[S,'id']),c+'_pred']=np.exp(pred) if c=='hw' else pred
    m=RidgeCV(alphas=[0.1,1,10]).fit(F.loc[W,X].values,y[W]); rest=P[c+'_pred'].isna() if c+'_pred' in P else P.id.notna()   # all other tablets: model fitted on the well-preserved
    pr=m.predict(P.loc[rest,X].values); P.loc[rest,c+'_pred']=np.exp(pr) if c=='hw' else pr
    rel.append(dict(feature=c,description=NAMES[c],R2_well_preserved=round(r2['well_preserved'],2),R2_all=round(r2['all'],2),
                    n_well_preserved=int(W.sum()),n_all=int(ok.sum()),
                    reliability='reliable' if r2['well_preserved']>=0.65 else 'partial' if r2['well_preserved']>=0.4 else 'not recovered'))
Rl=pd.DataFrame(rel).sort_values('R2_well_preserved',ascending=False); Rl.to_csv(f'{R}/results/vae_feature_recovery_all.csv',index=False); print(Rl.to_string(index=False))
P.drop(columns=X+[f+'_pred' for f in Rl[Rl.reliability=='not recovered'].feature]).merge(F[['id']+GEO],on='id',how='left').round(3).to_csv(f'{R}/results/vae_measured_and_predicted.csv',index=False)
# (3) example tablets
Z=(F[X]-F[X].median())/F[X].std()
def pick(x,q):
    lo,hi=F[x].quantile(q-.02),F[x].quantile(q+.02); band=F[(F[x]>=lo)&(F[x]<=hi)&F.well_preserved&F.thick_side.notna()&F.thick_end.notna()]
    other=[o for o in X if o!=x]; d=np.sqrt((Z.loc[band.index,other]**2).sum(axis=1)).sort_values()
    for i in d.index:                                     # first typical tablet whose photograph shows exactly six clean views
        pid=int(band.loc[i,'id']); a=cv2.imread(f'{IMG}/{pid:06d}.png',0)>127
        if a.mean()>.5: a=~a
        n,_,st,_=cv2.connectedComponentsWithStats(a.astype(np.uint8)); big=(st[1:,4]>0.01*a.sum()).sum()
        if big==6: return pid
def crop(pid):
    a=cv2.imread(f'{IMG}/{pid:06d}.png',0)>127
    if a.mean()>.5: a=~a
    ys,xs=np.nonzero(a); return a[ys.min():ys.max()+1,xs.min():xs.max()+1]
order=D.assign(a=D.rho.abs()).sort_values('a',ascending=False).dim.tolist()
fig,ax=plt.subplots(len(X),4,figsize=(7.2,15),gridspec_kw=dict(width_ratios=[3.0,1,1,1],hspace=.25,wspace=.05))
for c,t in zip(range(1,4),['low','middle','high']): ax[0,c].set_title(t,fontsize=9,color='#444')
ex=[]
for i,x in enumerate(order):
    r=D.set_index('dim').loc[x]; a=ax[i,0]; a.axis('off')
    a.text(0,.72,x,fontsize=11,fontweight='bold',transform=a.transAxes,color='#1a1a1a')
    a.text(0,.42,r.reads,fontsize=8.5,transform=a.transAxes,color='#1a1a1a')
    a.text(0,.16,f'closest measurement: {SHORT[r.closest]}, ρ = {r.rho:+.2f} ({r.strength})',fontsize=7.5,transform=a.transAxes,color='#666')
    for j,q in enumerate([.1,.5,.9]):
        pid=pick(x,q); ex.append(dict(dim=x,q=q,id=pid)); b=ax[i,j+1]; b.imshow(~crop(pid),cmap='gray',interpolation='nearest'); b.axis('off')
        b.text(.5,-.04,f'P{pid:06d}',fontsize=5.5,ha='center',va='top',transform=b.transAxes,color='#666')
fig.savefig(f'{R}/figures/fig_vae_dimension_guide.png',dpi=200,bbox_inches='tight',facecolor='white')
pd.DataFrame(ex).merge(F[['id','Period_Name','Genre_Name']],on='id').to_csv(f'{R}/results/vae_dimension_examples.csv',index=False)
