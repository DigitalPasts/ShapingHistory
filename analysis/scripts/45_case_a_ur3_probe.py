"""Probe for case A: do Ur III silhouettes (VAE features) carry the province within one museum? Leave-one-out 5-NN on
Umma, Girsu, Puzriš-Dagan, Nippur, Garšana tablets, balanced classes per museum, against label shuffling within museum."""
from _paths import WORK
import pandas as pd, numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_predict, StratifiedKFold
R=WORK; rng=np.random.default_rng(0)
U=pd.read_csv(f'{R}/results/s4_ur3_tablets_bdtns.csv')[['artifact_id','province','reign','bdtns','type']]
a=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','collections'],low_memory=False)
v=pd.concat([pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_{s}.csv') for s in ['train','val','test']]).drop_duplicates('CDLI_id')
X=[f'X{i}' for i in range(1,13)]
m=U.merge(a,on='artifact_id').merge(v[['CDLI_id']+X],left_on='artifact_id',right_on='CDLI_id')
m['coll']=m.collections.fillna('?').str.split(',').str[0]
m=m[m.province.isin(['Umma','Girsu','Puzriš-Dagan','Nippur','Garšana'])]
print(pd.crosstab(m.coll,m.province).query('Umma+Girsu>200').to_string())
rows=[]
for c,g in m.groupby('coll'):
    vc=g.province.value_counts(); keep=vc[vc>=40].index
    if len(keep)<2: continue
    k=min(vc[keep].min(),300); g=pd.concat([g[g.province==p].sample(k,random_state=0) for p in keep])
    Z=((g[X]-g[X].mean())/g[X].std()).values; y=g.province.values
    cv=StratifiedKFold(10,shuffle=True,random_state=0); knn=KNeighborsClassifier(5)
    acc=(cross_val_predict(knn,Z,y,cv=cv)==y).mean()
    null=[(cross_val_predict(knn,Z,(yy:=rng.permutation(y)),cv=cv)==yy).mean() for _ in range(50)]
    rows.append(dict(museum=c,provinces=', '.join(keep),n_each=k,acc=round(acc,3),chance=round(np.mean(null),3),p=np.mean(np.array(null)>=acc)))
T=pd.DataFrame(rows); print(T.to_string(index=False)); T.to_csv(f'{R}/results/case_a_province_probe.csv',index=False)
