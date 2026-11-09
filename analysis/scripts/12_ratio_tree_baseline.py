"""Period from the single h/w ratio: decision tree on the ResNet/VAE train split, scored on the same test split.
Reports accuracy, macro-F1 over all true classes, macro-F1 'collapsed' (test support >=40, rest -> other, as notebook 8.1),
majority and stratified-random baselines."""
from _paths import WORK
import pandas as pd, numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score, accuracy_score
R=WORK
hw=pd.read_csv(f'{R}/zenodo/h_w_ratio_df_all.csv'); hw['CDLI_id']=hw.tablet_p_id_CDLI.str[1:].astype(int)
sp={s:pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_{s}.csv',usecols=['CDLI_id','Period_Name']).merge(hw[['CDLI_id','hw_ratio']],on='CDLI_id') for s in ['train','val','test']}
tr=pd.concat([sp['train'],sp['val']]); te=sp['test']
sup=te.Period_Name.value_counts(); keep=sup[sup>=40].index
def coll(y): return np.where(pd.Series(y).isin(keep),y,'other')
rows=[]
for depth in [4,6,8,10,None]:
    m=DecisionTreeClassifier(max_depth=depth,min_samples_leaf=20,random_state=0).fit(tr[['hw_ratio']],tr.Period_Name)
    p=m.predict(te[['hw_ratio']])
    rows.append(dict(model=f'tree depth {depth}',acc=accuracy_score(te.Period_Name,p),macroF1_all=f1_score(te.Period_Name,p,average='macro'),
                     macroF1_collapsed=f1_score(coll(te.Period_Name),coll(p),average='macro')))
maj=tr.Period_Name.mode()[0]; p=np.full(len(te),maj)
rows.append(dict(model=f'majority ({maj})',acc=accuracy_score(te.Period_Name,p),macroF1_all=f1_score(te.Period_Name,p,average='macro'),macroF1_collapsed=f1_score(coll(te.Period_Name),coll(p),average='macro')))
rng=np.random.default_rng(0); p=rng.choice(tr.Period_Name.values,len(te))
rows.append(dict(model='random, train frequencies',acc=accuracy_score(te.Period_Name,p),macroF1_all=f1_score(te.Period_Name,p,average='macro'),macroF1_collapsed=f1_score(coll(te.Period_Name),coll(p),average='macro')))
o=pd.DataFrame(rows).round(3); print('n test',len(te),'classes',te.Period_Name.nunique(),'collapsed',len(keep)+1); print(o.to_string(index=False))
o.to_csv(f'{R}/results/ratio_tree_baseline.csv',index=False)
