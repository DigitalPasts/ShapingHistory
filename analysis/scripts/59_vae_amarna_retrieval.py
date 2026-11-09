"""Amarna letters in Berlin: does a letter's nearest neighbour in outline space come from the same city (vassals with
three or more photographed letters) or from the same place of making (Goren et al. 2004)?  Leave-one-out 1-NN on
standardised features; null from 1000 label permutations.  Tiers as in script 57."""
from _paths import WORK
import pandas as pd, numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import pairwise_distances
R=WORK; rng=np.random.default_rng(0); X=[f'X{i}' for i in range(1,13)]
v=pd.concat([pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_{s}.csv') for s in ['train','val','test']]).drop_duplicates('CDLI_id').rename(columns={'CDLI_id':'id'})
g=pd.read_csv(f'{R}/results/silhouette_geometry.csv').rename(columns={'hw':'shw'}); g['loghw']=np.log(g.shw); g=g.fillna(g.median())
A=pd.read_csv(f'{R}/amarna/SI_amarna_letters.csv'); A['id']=A.P.str[1:].astype(float)
G=pd.read_csv(f'{R}/goren/goren2004_catalogue.csv')[['EA_n','made_at']]; A=A.merge(G,left_on='EA',right_on='EA_n',how='left')
A=A[A.museum.eq('Vorderasiatisches Museum')].merge(v[['id']+X],on='id').merge(g,on='id')
GEO=['hw','rect','solidity','circ','corner_fill','taper','side_bulge','end_bulge','rev_corner_fill','rev_obv','thick_side','thick_end']; T={'ratio':['loghw'],'outline':['loghw']+GEO[1:],'VAE':X}
great={'Babylon','Mittani','Hattusa','Alashiya','Arzawa','Assur','Egypt','Akhetaten'}
rows=[]
for lab in ['city','made_at']:
    d=A[~A.city.isin(great)].dropna(subset=[lab]); d=d[d[lab].map(d[lab].value_counts())>=3]; y=d[lab].values
    for t,cols in T.items():
        Z=StandardScaler().fit_transform(d[cols].values); Dm=pairwise_distances(Z); np.fill_diagonal(Dm,np.inf); nn=Dm.argmin(1)
        hit=(y[nn]==y).mean(); null=np.array([(yy[nn]==yy).mean() for yy in (rng.permutation(y) for _ in range(1000))])
        rows.append(dict(label=lab,groups=d[lab].nunique(),n=len(d),tier=t,same_group_nn=round(hit,3),chance=round(null.mean(),3),p=round((1+(null>=hit).sum())/1001,3)))
T2=pd.DataFrame(rows); print(T2.to_string(index=False)); T2.to_csv(f'{R}/results/vae_amarna_retrieval.csv',index=False)
