"""Case A: is the Ur III province signal in the silhouette (VAE features) present within one text type and one museum,
and does the silhouette distance between Girsu and Umma shrink over the reigns? Text types as in Section 4
(BDTNS label, else bookkeeping keyword). Leave-one-out style 10-fold 5-NN, balanced classes, label shuffling null."""
from _paths import WORK
import pandas as pd, numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_predict, StratifiedKFold
R=WORK; rng=np.random.default_rng(0)
U=pd.read_csv(f'{R}/results/SI_ur3_text_types.csv'); U['artifact_id']=U.P.str[1:].astype(int)
a=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','collections'],low_memory=False)
v=pd.concat([pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_{s}.csv') for s in ['train','val','test']]).drop_duplicates('CDLI_id')
X=[f'X{i}' for i in range(1,13)]
m=U.merge(a,on='artifact_id').merge(v[['CDLI_id']+X],left_on='artifact_id',right_on='CDLI_id')
m['coll']=m.collections.fillna('?').str.split(',').str[0]
Z=(m[X]-m[X].mean())/m[X].std(); m[X]=Z
def knn(g,lab):
    vc=g[lab].value_counts(); keep=vc[vc>=25].index
    if len(keep)<2: return None
    k=min(vc[keep].min(),300); g=pd.concat([g[g[lab]==p].sample(k,random_state=0) for p in keep])
    y=g[lab].values; cv=StratifiedKFold(5,shuffle=True,random_state=0); c=KNeighborsClassifier(5)
    acc=(cross_val_predict(c,g[X].values,y,cv=cv)==y).mean()
    null=[(cross_val_predict(c,g[X].values,(yy:=rng.permutation(y)),cv=cv)==yy).mean() for _ in range(30)]
    return dict(n_each=k,classes=', '.join(keep),acc=round(acc,3),chance=round(np.mean(null),3),p=np.mean(np.array(null)>=acc))
rows=[]
for (t,c),g in m[m.province.isin(['Umma','Girsu','Puzriš-Dagan'])].groupby(['type_used','coll']):
    r=knn(g,'province')
    if r: rows.append(dict(type=t,museum=c,**r))
T=pd.DataFrame(rows).sort_values('n_each',ascending=False); print(T.to_string(index=False)); T.to_csv(f'{R}/results/case_a_within_type.csv',index=False)
# convergence of silhouettes: Girsu-Umma centroid distance within type, by reign, against within-province split-half distance
RO=['Šulgi 1-40','Šulgi 41-48','Amar-Suen','Šū-Suen','Ibbi-Suen']; out=[]
for r in RO:
    g=m[(m.reign==r)&m.province.isin(['Girsu','Umma'])]
    ds=[];ws=[]
    for t,x in g.groupby('type_used'):
        G=x[x.province=='Girsu'];Uu=x[x.province=='Umma']
        if min(len(G),len(Uu))<10: continue
        d=np.linalg.norm(G[X].mean()-Uu[X].mean()); ds.append((d,len(x)))
    if ds: out.append(dict(reign=r,n=sum(w for _,w in ds),types=len(ds),dist=round(np.average([d for d,_ in ds],weights=[w for _,w in ds]),3)))
C=pd.DataFrame(out); print(C.to_string(index=False)); C.to_csv(f'{R}/results/case_a_convergence_vae.csv',index=False)
