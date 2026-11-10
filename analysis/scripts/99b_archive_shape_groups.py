"""Shape groups across and within archives (ShG, 9 Nov 2026): do the groups that tablet shape forms line up with genre,
date, holding museum or other metadata?
Archive labels: Archibab (OB), NaBuCCo and Prosobab (NB, Achaemenid), Oracc catalogues (Pedersén's Middle Assyrian
archives in TCMA; Neo-Assyrian findspot archives in ATAE), CDLI archive field; 'Miscellaneous' and unknown dropped.
Shape: the 12 VAE dimensions plus log h/w (the VAE dimensions already carry thickness and corners), each scaled by median and MAD within the period,
after removing the part explained by damage (robust linear fit on the damage score within the period), so breakage does not drive the groups. Dates from 98j.
ACROSS archives (periods with >= 2 archives of >= 30 tablets): leave-one-out nearest-median classification of the archive
from shape against 1,000 label permutations; distances between archive medians compared (Mantel, Spearman, 2,000
permutations) with distances in genre mix, museum mix (Jensen-Shannon) and median date.
WITHIN archives (>= 50 tablets): k-means (k = 2-4 by silhouette) on shape; normalized mutual information of the clusters
with genre, holding museum, reign, decade, damage tercile and site, each against 1,000 permutations; BH-corrected.
Outputs: turning/archive_across.csv, turning/archive_mantel.csv, turning/archive_within.csv, figures/archive_shape_*.png"""
from _paths import WORK
import pandas as pd, numpy as np, warnings; warnings.filterwarnings('ignore')
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, normalized_mutual_info_score as NMI
from scipy.spatial.distance import jensenshannon, pdist, squareform
from scipy.stats import spearmanr
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import os
R=WORK; rng=np.random.default_rng(11)
REP=os.environ.get('SH_REP','vae'); SUF='' if REP=='vae' else '_dinov2'   # 'dinov2': first 12 DINOv2 principal components (script 103) in place of the VAE
d=pd.read_parquet(f'{R}/master_tablets.parquet')
if REP=='dinov2':
    Pd=pd.read_parquet(f'{R}/dinov2_pca.parquet')[['id']+[f'D{i}' for i in range(1,13)]]
    d=d.drop(columns=[f'X{i}' for i in range(1,13)]).merge(Pd.rename(columns={f'D{i}':f'X{i}' for i in range(1,13)}),on='id',how='inner')
F=[f'X{i}' for i in range(1,13)]+['loghw']   # rectangularity, corners and thickness are missing for many archive tablets; the VAE dims carry them
src=[('Archibab',pd.read_csv(f'{R}/turning/companion_dates.csv')[['id','ab_archive']].rename(columns={'ab_archive':'archive_db'})),
     ('NaBuCCo',pd.read_csv(f'{R}/nabucco/nabucco_matched.csv')[['id','Archive']].rename(columns={'Archive':'archive_db'})),
     ('Prosobab',pd.read_csv(f'{R}/prosobab/prosobab_matched.csv')[['id','ArchiveName']].rename(columns={'ArchiveName':'archive_db'})),
     ('Oracc',pd.read_csv(f'{R}/oracc/oracc_matched.csv')[['id','archive']].rename(columns={'archive':'archive_db'})),
     ('CDLI',d[['id','archive']].rename(columns={'archive':'archive_db'})),
     ('Ur III provinces',pd.read_csv(f'{R}/results/s4_ur3_tablets_bdtns.csv').rename(columns={'artifact_id':'id'}).assign(archive_db=lambda u: 'Ur III '+u.province+' provincial archive')[['id','archive_db']])]
L=pd.concat([s.assign(archive_src=n) for n,s in src]).dropna(subset=['archive_db'])
L=L[~L.archive_db.astype(str).str.contains(r'Miscellaneous|Unknown|^\?',regex=True)].drop_duplicates('id')
D=pd.read_csv(f'{R}/turning/tablet_dates_consolidated.csv')[['id','king_final','bce']]
X=d.merge(L,on='id').merge(D,on='id',how='left')
# finer text type from the specialist databases where they have one (Oracc subgenre or genre, NaBuCCo type, Archibab type), else CDLI genre
Qo=pd.read_csv(f'{R}/oracc/oracc_matched.csv'); Qo['tt']=Qo.subgenre.where(Qo.period=='Middle Assyrian').fillna(Qo.genre)
TT=pd.concat([Qo[['id','tt']],
    pd.read_csv(f'{R}/nabucco/nabucco_matched.csv').rename(columns={'Type and content (legacy)':'tt'})[['id','tt']],
    pd.read_csv(f'{R}/turning/companion_dates.csv').rename(columns={'ab_type':'tt'})[['id','tt']],
    pd.read_csv(f'{R}/results/s4_ur3_tablets_bdtns.csv').rename(columns={'artifact_id':'id','type':'tt'})[['id','tt']]]).dropna().drop_duplicates('id')
X=X.merge(TT,on='id',how='left'); X['text_type']=X.tt.fillna(X.genre)
X=X[X.photo_hw.between(1/3,3)].dropna(subset=F)
def scale(g):
    G=g[F].copy(); dm=g.damage.fillna(g.damage.median()).values
    for f in F:   # remove the damage trend (Theil-Sen slope) within the period
        from scipy.stats import theilslopes
        sl,ic,_,_=theilslopes(G[f].values,dm); G[f]=G[f]-sl*dm
    m=G.median(); s=(G-m).abs().median()*1.4826; return (G-m)/s.replace(0,np.nan)
Z=pd.concat([scale(X[X.period==p]) for p in X.period.unique()]).loc[X.index].fillna(0).clip(-6,6)
X['dam3']=X.groupby('period').damage.transform(lambda s: pd.qcut(s.rank(method='first'),3,labels=False) if len(s)>=3 else 0)
X['decade']=(X.bce//10*10)
# ---------- across archives
big=X.groupby(['period','archive_db']).size(); big=big[big>=30]
acr=[]; man=[]; maps={}
for p in sorted({i[0] for i in big.index}):
    arcs=[a for (pp,a) in big.index if pp==p]
    if len(arcs)<2: continue
    g=X[(X.period==p)&X.archive_db.isin(arcs)]
    if len(g)>3000: g=g.loc[np.concatenate([t.sample(min(len(t),300),random_state=0).index.values for _,t in g.groupby('archive_db')])]
    z=Z.loc[g.index].values; y=g.archive_db.values
    def loo_acc(lab):
        meds={a:np.median(z[lab==a],axis=0) for a in arcs}; ok=0
        for i in range(len(z)):
            best=None;bd=1e9
            for a in arcs:
                m=meds[a] if lab[i]!=a else np.median(np.delete(z[lab==a],np.where(np.where(lab==a)[0]==i)[0],axis=0),axis=0)
                dd=np.abs(z[i]-m).sum()
                if dd<bd: bd,best=dd,a
            ok+=best==lab[i]
        return ok/len(z)
    obs=loo_acc(y); null=[loo_acc(rng.permutation(y)) for _ in range(200)]
    chance=max(np.mean(y==a) for a in arcs)
    acr.append(dict(period=p,archives=len(arcs),n=len(g),loo_accuracy=round(obs,3),majority_baseline=round(chance,3),perm_mean=round(np.mean(null),3),p=round((1+sum(n>=obs for n in null))/(1+len(null)),4)))
    med=np.array([np.median(Z.loc[g[g.archive_db==a].index].values,axis=0) for a in arcs]); Ds=squareform(pdist(med,'cityblock'))
    maps[p]=(arcs,med,[g[g.archive_db==a] for a in arcs])
    if len(arcs)>=4:
        def comp(col):
            cats=sorted(g[col].dropna().astype(str).unique())
            P=np.array([[np.mean(g[g.archive_db==a][col].astype(str)==c) for c in cats] for a in arcs]); return squareform(pdist(P,jensenshannon))
        mats={'text-type mix':comp('text_type'),'genre mix':comp('genre'),'museum mix':comp('museum'),'site mix':comp('site'),
              'median date':squareform(pdist(np.array([[g[g.archive_db==a].bce.median()] for a in arcs]))) }
        iu=np.triu_indices(len(arcs),1)
        for k,M in mats.items():
            if np.isnan(M[iu]).all() or np.nanstd(M[iu])==0: continue
            r=spearmanr(Ds[iu],M[iu],nan_policy='omit').correlation; nl=[]
            for _ in range(2000):
                pi=rng.permutation(len(arcs)); nl.append(spearmanr(Ds[iu],M[pi][:,pi][iu],nan_policy='omit').correlation)
            man.append(dict(period=p,archives=len(arcs),metadata=k,rho=round(r,3),p=round((1+np.sum(np.array(nl)>=r))/2001,4)))
pd.DataFrame(acr).to_csv(f'{R}/turning/archive_across{SUF}.csv',index=False); pd.DataFrame(man).to_csv(f'{R}/turning/archive_mantel{SUF}.csv',index=False)
print(pd.DataFrame(acr).to_string()); print(pd.DataFrame(man).to_string())
# ---------- within archives
VARS={'text type':'text_type','genre':'genre','museum':'museum','reign':'king_final','decade':'decade','damage':'dam3','site':'site'}
win=[]; clus={}
for (p,a),n in X.groupby(['period','archive_db']).size().items():
    if n<50: continue
    g=X[(X.period==p)&(X.archive_db==a)]; z=Z.loc[g.index].values
    best=max(range(2,5),key=lambda k: silhouette_score(z,KMeans(k,n_init=10,random_state=0).fit_predict(z),sample_size=min(len(z),3000),random_state=0))
    lab=KMeans(best,n_init=10,random_state=0).fit_predict(z); sil=silhouette_score(z,lab,sample_size=min(len(z),3000),random_state=0); clus[(p,a)]=(g,lab)
    for v,col in VARS.items():
        s=g[col]; ok=s.notna().values
        if ok.sum()<30 or s[ok].astype(str).nunique()<2: continue
        yv=s[ok].astype(str).values; lv=lab[ok]; obs=NMI(lv,yv); nl=np.array([NMI(lv,rng.permutation(yv)) for _ in range(1000)])
        win.append(dict(period=p,archive=a,n=len(g),k=best,silhouette=round(sil,3),variable=v,levels=int(s[ok].astype(str).nunique()),n_known=int(ok.sum()),
                        nmi=round(obs,3),nmi_null=round(nl.mean(),3),p=(1+np.sum(nl>=obs))/1001))
W=pd.DataFrame(win).sort_values('p'); m=len(W); W['q']=np.minimum.accumulate((W.p*m/np.arange(1,m+1))[::-1])[::-1].clip(upper=1)
W=W.sort_values(['period','archive','variable']); W.to_csv(f'{R}/turning/archive_within{SUF}.csv',index=False)
print(W[['period','archive','n','k','silhouette','variable','levels','nmi','nmi_null','q']].to_string())
# ---------- figures
import matplotlib.cm as cm
ps=[p for p in maps if len(maps[p][0])>=3]
fig,axs=plt.subplots(1,max(1,len(ps)),figsize=(6*max(1,len(ps)),5.2))
axs=np.atleast_1d(axs); PAL=['#2a6fdb','#e8590c','#2b8a3e','#c2255c','#7048e8','#868e96','#f08c00','#0b7285','#5c940d','#a61e4d']
DOMS=[]
for p in ps:
    for gs_ in maps[p][2]: DOMS.append(gs_.text_type.value_counts().index[0])
DOMS=list(dict.fromkeys(DOMS)); col={g_:PAL[i%len(PAL)] for i,g_ in enumerate(DOMS)}
for ax,p in zip(axs,ps):
    arcs,med,gs=maps[p]; M=squareform(pdist(med,'cityblock')); n=len(arcs)
    J=np.eye(n)-1/n; B=-0.5*J@(M**2)@J; w,v=np.linalg.eigh(B); idx=np.argsort(w)[::-1][:2]; Y=v[:,idx]*np.sqrt(np.maximum(w[idx],0))
    for i,a in enumerate(arcs):
        gm=gs[i].text_type.value_counts(normalize=True); dom=gm.index[0]
        ax.scatter(Y[i,0],Y[i,1],s=30+3*len(gs[i]),color=col.get(dom,'#adb5bd'),edgecolor='white',linewidth=1.5,zorder=3)
        mus=gs[i].museum.value_counts(normalize=True)
        ax.annotate(f"{a.replace(' Archive','')}\n{dom} {gm.iloc[0]:.0%}; {mus.index[0][:18]} {mus.iloc[0]:.0%}",(Y[i,0],Y[i,1]),fontsize=7,xytext=(6,4),textcoords='offset points')
    ax.set_title(f'{p}: {n} archives, distances between median shapes',fontsize=10); ax.set_xticks([]); ax.set_yticks([])
    for s_ in ax.spines.values(): s_.set_color('#ccc')
handles=[plt.Line2D([],[],marker='o',ls='',color=col[gn],label=gn) for gn in DOMS]
fig.legend(handles=handles,loc='lower center',ncol=len(handles),fontsize=8,frameon=False,title='dominant text type (dot colour); dot size = tablets',title_fontsize=8)
plt.tight_layout(rect=(0,0.08,1,1)); plt.savefig(f'{R}/figures/archive_shape_across{SUF}.png',dpi=200); plt.close()
P=W.pivot_table(index=['period','archive'],columns='variable',values='nmi'); Q=W.pivot_table(index=['period','archive'],columns='variable',values='q')
cols=[c for c in ['text type','genre','museum','site','reign','decade','damage'] if c in P.columns]; P=P[cols]; Q=Q[cols]
fig,ax=plt.subplots(figsize=(1.3*len(cols)+4,0.45*len(P)+1.6))
im=ax.imshow(P.values,cmap='Blues',vmin=0,vmax=max(0.3,np.nanmax(P.values)),aspect='auto')
for i in range(P.shape[0]):
    for j in range(P.shape[1]):
        v=P.values[i,j]; q=Q.values[i,j]
        if not np.isnan(v): ax.text(j,i,f'{v:.2f}'+('*' if q<0.05 else ''),ha='center',va='center',fontsize=8,color='white' if v>0.2 else '#222')
ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols); ax.set_yticks(range(len(P))); ax.set_yticklabels([f'{a} ({p})' for p,a in P.index],fontsize=8)
ax.set_title('Within archives: how far shape clusters follow each metadata field\n(normalized mutual information; * = q < 0.05 against 1,000 permutations)',fontsize=9)
plt.colorbar(im,ax=ax,shrink=0.6); plt.tight_layout(); plt.savefig(f'{R}/figures/archive_shape_within{SUF}.png',dpi=200); plt.close()
print('figures written')
