"""Eanna, early (Kandalanu-Nebuchadnezzar) vs late (Nabonidus-Cambyses) tablets of one text form, compared within
collections: each collection contributes equal numbers of early and late tablets; the permutation null shuffles the labels
within collection.  Tiers as in script 57.  Only tablets in the 2024 VAE set can be used (Yale and Goucher are absent)."""
from _paths import WORK
import pandas as pd, numpy as np, warnings; warnings.filterwarnings('ignore')
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold, cross_val_score
R=WORK; rng=np.random.default_rng(0); X=[f'X{i}' for i in range(1,13)]
v=pd.concat([pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_{s}.csv') for s in ['train','val','test']]).drop_duplicates('CDLI_id').rename(columns={'CDLI_id':'id'})
g=pd.read_csv(f'{R}/results/silhouette_geometry.csv').rename(columns={'hw':'shw'}); g['loghw']=np.log(g.shw); g=g.fillna(g.median())
D=pd.read_csv(f'{R}/nabucco/digeanna_merged.csv'); D['id']=D.P.astype(str).str.extract(r'(\d+)')[0].astype(float)
D=D.merge(v[['id']+X],on='id').merge(g,on='id'); D['form']=D['Text Form'].str.split(' ').str[0]
D['coll']=D.museum.fillna(D.collections.fillna('?').str.split(',').str[0])
D['el']=np.where(D.reign.isin(['Kandalānu','Nabopolassar','Nebuchadnezzar II']),'early',np.where(D.reign.isin(['Nabonidus','Cyrus','Cambyses']),'late',None))
GEO=['hw','rect','solidity','circ','corner_fill','taper','side_bulge','end_bulge','rev_corner_fill','rev_obv','thick_side','thick_end']; T={'ratio':['loghw'],'outline':['loghw']+GEO[1:],'VAE':X}
rows=[]
for f in ['Note','List','Debt']:
    d=D[D.form.eq(f)&D.el.notna()]; ct=pd.crosstab(d.coll,d.el); ok=ct[(ct.min(1)>=4)].index
    parts=[]
    for c in ok:
        k=ct.loc[c].min(); parts+= [d[(d.coll==c)&(d.el==e)].sample(k,random_state=0) for e in ['early','late']]
    if not parts or len(pd.concat(parts))<20: continue
    s=pd.concat(parts).reset_index(drop=True); s['grp']=np.arange(len(s))%5
    y=s.el.values
    for t,cols in T.items():
        m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000))
        acc=cross_val_score(m,s[cols].values,y,cv=RepeatedStratifiedKFold(n_splits=5,n_repeats=5,random_state=0),scoring='balanced_accuracy').mean(); null=[]
        for _ in range(200):
            yy=s.groupby('coll').el.transform(lambda z: rng.permutation(z.values)).values
            null.append(cross_val_score(m,s[cols].values,yy,cv=StratifiedKFold(5,shuffle=True,random_state=0),scoring='balanced_accuracy').mean())
        null=np.array(null); rows.append(dict(form=f,collections='; '.join(f'{c} {ct.loc[c].min()}+{ct.loc[c].min()}' for c in ok),n=len(s),tier=t,acc=round(acc,3),chance=round(null.mean(),3),p=round((1+(null>=acc).sum())/201,3)))
T2=pd.DataFrame(rows); print(T2.to_string(index=False)); T2.to_csv(f'{R}/results/vae_eanna_within_collection.csv',index=False)
