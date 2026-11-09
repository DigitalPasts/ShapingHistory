"""Probe for case B: do the Amarna letters carry their sender's region in tablet shape? Sender groups by EA number
(Moran 1992 ordering). Photograph h/w and VAE silhouette features; leave-one-out 5-NN accuracy vs label shuffling.
Vorderasiatisches Museum tablets only (one museum, so no collection confound). Preliminary."""
from _paths import WORK
import pandas as pd, numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_predict, LeaveOneOut
R=WORK; rng=np.random.default_rng(0)
a=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','designation','provenience','collections'],low_memory=False)
a=a[a.provenience.fillna('').str.startswith('Akhetaten')]
v=pd.concat([pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_{s}.csv') for s in ['train','val','test']]).drop_duplicates('CDLI_id')
p=pd.read_csv(f'{R}/zenodo/h_w_ratio_df_all.csv'); p['artifact_id']=p.tablet_p_id_CDLI.str[1:].astype(int)
X=[f'X{i}' for i in range(1,13)]
m=a.merge(v[['CDLI_id']+X],left_on='artifact_id',right_on='CDLI_id').merge(p[['artifact_id','hw_ratio']],on='artifact_id',how='left')
m['EA']=m.designation.str.extract(r'EA (\d+)')[0].astype(float)
bins=[0,44,67,140,171,243,339,400]; lab=['Great kings (1-44)','North Syria (45-67)','Byblos (68-140)','Coast and Amurru (141-171)','Central Syria (172-243)','Southern Canaan (244-339)','Scholarly texts (340+)']
m['grp']=pd.cut(m.EA,bins,labels=lab)
m['vam']=m.collections.fillna('').str.startswith('Vorderasiatisches')
print(m.groupby('grp',observed=True).agg(n=('EA','size'),vam=('vam','sum'),photo_hw=('hw_ratio','median')).to_string())
g=m[m.vam&m.grp.notna()]; g=g[g.groupby('grp',observed=True).grp.transform('size')>=8]
Z=((g[X]-g[X].mean())/g[X].std()).values; y=g.grp.astype(str).values
knn=KNeighborsClassifier(5)
acc=(cross_val_predict(knn,Z,y,cv=LeaveOneOut())==y).mean()
null=[(cross_val_predict(knn,Z,(yy:=rng.permutation(y)),cv=LeaveOneOut())==yy).mean() for _ in range(100)]
print('VAM n',len(y),'groups',len(set(y)),'5-NN accuracy',round(acc,3),'shuffled mean',round(np.mean(null),3),'p',np.mean(np.array(null)>=acc))
m[['artifact_id','designation','EA','grp','collections','hw_ratio']].to_csv(f'{R}/results/case_b_amarna.csv',index=False)
