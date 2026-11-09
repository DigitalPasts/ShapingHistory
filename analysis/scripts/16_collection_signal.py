"""Do silhouettes carry the holding collection (photography/imaging conventions), beyond city and period?
Within one period and one findspot, predict the museum from damage-adjusted VAE codes + damage (5-fold CV, balanced accuracy vs chance).
Comparison: predict the city within one period and one collection."""
from _paths import WORK
import pandas as pd, numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.metrics import balanced_accuracy_score
R=WORK
L=pd.read_csv(f'{R}/results/tablet_latent_damage_adjusted.csv')
a=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','collections'],low_memory=False).rename(columns={'artifact_id':'CDLI_id'})
L=L.drop(columns=['coll'],errors='ignore').merge(a,on='CDLI_id'); L['coll']=L.collections.fillna('?').str.split(';').str[0].str.strip().str.split(',').str[0]
Z=[f'Z{i}' for i in range(1,13)]+['damage']
def test(s,target,label,top=5,min_n=60):
    vc=s[target].value_counts(); keep=vc[vc>=min_n].index[:top]; s=s[s[target].isin(keep)]
    if len(keep)<2: return
    # balance classes by downsampling to the smallest
    m=s[target].value_counts().min(); s=s.groupby(target).sample(m,random_state=0)
    p=cross_val_predict(HistGradientBoostingClassifier(max_iter=200,random_state=0),s[Z],s[target],cv=StratifiedKFold(5,shuffle=True,random_state=0))
    rows.append(dict(test=label,target=target,classes=len(keep),n_per_class=m,bal_acc=balanced_accuracy_score(s[target],p),chance=1/len(keep)))
rows=[]
for per,city in [('Ur III','Puzriš-Dagan'),('Ur III','Umma'),('Ur III','Girsu'),('Old Babylonian','Sippar-Yahrurum'),('Old Babylonian','Nippur'),('Neo-Babylonian','uncertain'),('Neo-Assyrian','Nineveh')]:
    test(L[(L.Period_Name==per)&(L.city==city)],'coll',f'museum within {per} {city}')
for per,coll in [('Ur III','British Museum'),('Ur III','Yale Babylonian Collection'),('Old Babylonian','British Museum'),('Old Babylonian','Penn Museum')]:
    test(L[(L.Period_Name==per)&(L.coll==coll)&(L.city!='uncertain')],'city',f'city within {per} {coll}')
o=pd.DataFrame(rows); print(o.round(3).to_string(index=False)); o.to_csv(f'{R}/results/collection_signal.csv',index=False)
