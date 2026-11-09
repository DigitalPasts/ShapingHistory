"""Confusions of the released silhouette model, corrected for class size.
Lift(i->j) = P(pred=j | true=i, error) / P(pred=j | error, true not in {j}); >1 means i is mistaken for j more than
j's general pull on errors predicts. Bootstrap 95% CI over test tablets. Also: accuracy by collection within period."""
from _paths import WORK
import pandas as pd, numpy as np
R=WORK
inv={0:'other',1:'Ur III',2:'Neo-Assyrian',3:'Old Babylonian',4:'Middle Babylonian',5:'Neo-Babylonian',6:'Old Akkadian',7:'Achaemenid',8:'Early Old Babylonian',9:'ED IIIb',10:'Middle Assyrian',11:'Old Assyrian',12:'Uruk III',13:'Proto-Elamite',14:'Lagash II',15:'Ebla',16:'ED IIIa',17:'Hellenistic',18:'ED I-II',19:'Middle Elamite',20:'Hittite',21:'Uruk IV'}
t=pd.read_csv(f'{R}/results/resnet_masked_test_predictions.csv'); t['p']=t.pred.map(inv); t['true']=t.y.map(inv)
t=t[t.artifact_type.isin(['tablet','tablet & envelope'])]
main=[p for p,n in t.true.value_counts().items() if n>=40 and p!='other']
def lift(d):
    e=d[d.true!=d.p]; out={}
    for i in main:
        ei=e[e.true==i]
        if len(ei)<10: continue
        for j in main:
            if j==i: continue
            base=(e[e.true!=j].p==j).mean()
            out[(i,j)]=((ei.p==j).mean()/base) if base>0 else np.nan
    return pd.Series(out)
L=lift(t); rng=np.random.default_rng(0)
B=pd.concat([lift(t.sample(len(t),replace=True,random_state=int(rng.integers(1e9)))) for _ in range(300)],axis=1)
res=pd.DataFrame({'lift':L,'lo':B.quantile(.025,axis=1),'hi':B.quantile(.975,axis=1)})
e=t[t.true!=t.p]
res['share_of_errors']=[(e[e.true==i].p==j).mean() for i,j in res.index]
res['n_err']=[(e.true==i).sum() for i,j in res.index]
res.index.names=['true','pred']; res=res.reset_index()
res.to_csv(f'{R}/results/confusion_lift.csv',index=False)
print(res[(res.lo>1)&(res.share_of_errors>=0.1)].sort_values('lift',ascending=False).round(2).to_string(index=False))
print('\nselected'); print(res[res.true.isin(['Achaemenid','Early Old Babylonian','Middle Assyrian','Hellenistic','Neo-Babylonian','Middle Babylonian'])&(res.share_of_errors>=0.08)].round(2).to_string(index=False))
# collections
a=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','collections','provenience'],low_memory=False)
t=t.drop(columns=['artifact_id']).merge(a.rename(columns={'artifact_id':'CDLI_id'}),on='CDLI_id',how='left'); t['coll']=t.collections.fillna('?').str.split(';').str[0].str.strip()
t['ok']=t.true==t.p
c=t.groupby(['true','coll']).ok.agg(['size','mean']).reset_index(); c=c[c['size']>=40]
c.to_csv(f'{R}/results/accuracy_by_collection.csv',index=False)
print(); print(c.sort_values(['true','size'],ascending=[True,False]).round(3).to_string(index=False))
