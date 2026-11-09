"""How much of period recognition is museum? Period classifier on damage-adjusted VAE codes (+damage),
random 5-fold CV vs museum-grouped 5-fold CV (no museum in both train and test). 13 main periods, tablets only."""
from _paths import WORK
import pandas as pd, numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import cross_val_predict, StratifiedKFold, StratifiedGroupKFold
from sklearn.metrics import accuracy_score, f1_score
R=WORK
L=pd.read_csv(f'{R}/results/tablet_latent_damage_adjusted.csv')
a=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','collections'],low_memory=False).rename(columns={'artifact_id':'CDLI_id'})
L=L.drop(columns=['coll'],errors='ignore').merge(a,on='CDLI_id'); L['coll']=L.collections.fillna('?').str.split(';').str[0].str.strip()
P=['ED IIIb','Ebla','Old Akkadian','Ur III','Early Old Babylonian','Old Babylonian','Old Assyrian','Middle Babylonian','Middle Assyrian','Neo-Assyrian','Neo-Babylonian','Achaemenid']
L=L[L.Period_Name.isin(P)&(L.coll!='?')]
L=L.groupby('Period_Name',group_keys=False).sample(frac=1,random_state=0).groupby('Period_Name').head(3000)   # cap big periods
Z=[f'Z{i}' for i in range(1,13)]+['damage']
m=HistGradientBoostingClassifier(max_iter=300,random_state=0)
rows=[]
for name,cv,g in [('random split',StratifiedKFold(5,shuffle=True,random_state=0),None),('museum-held-out split',StratifiedGroupKFold(5,shuffle=True,random_state=0),L.coll)]:
    p=cross_val_predict(m,L[Z],L.Period_Name,cv=cv,groups=g)
    r=dict(split=name,acc=accuracy_score(L.Period_Name,p),macroF1=f1_score(L.Period_Name,p,average='macro'))
    for per in P: r[per]=((p==per)&(L.Period_Name==per)).sum()/(L.Period_Name==per).sum()
    rows.append(r)
o=pd.DataFrame(rows).set_index('split').T; print(o.round(3).to_string()); o.to_csv(f'{R}/results/period_by_museum_split.csv')
print('n per period', L.Period_Name.value_counts().to_dict())
