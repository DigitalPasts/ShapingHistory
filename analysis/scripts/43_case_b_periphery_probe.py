"""Probe for case B (second-millennium peripheries): photograph h/w and VAE distance of each peripheral site to the
contemporary Babylonian centre (OB: Sippar, Nippur, Larsa, Ur; MB: Nippur, Dur-Kurigalzu, Babylon), with a
permutation-free bootstrap of the centroid distance. Preliminary; museum is not yet controlled."""
from _paths import WORK
import pandas as pd, numpy as np
R=WORK; rng=np.random.default_rng(0)
a=pd.read_csv(f'{R}/results/case_scan_tablets.csv',low_memory=False)
v=pd.concat([pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_{s}.csv') for s in ['train','val','test']]).drop_duplicates('CDLI_id')
X=[f'X{i}' for i in range(1,13)]
p=pd.read_csv(f'{R}/zenodo/h_w_ratio_df_all.csv'); p['artifact_id']=p.tablet_p_id_CDLI.str[1:].astype(int)
m=a.merge(v[['CDLI_id']+X],left_on='artifact_id',right_on='CDLI_id').merge(p[['artifact_id','hw_ratio']],on='artifact_id',how='left')
Z=(m[X]-m[X].mean())/m[X].std(); m[X]=Z
centre={'OB':m[(m.per=='Old Babylonian')&m.site.isin(['Sippar-Yahrurum','Nippur','Larsa','Ur','Sippar-Amnanum','Kish','Dilbat','Lagaba'])],
        'MB':m[(m.per=='Middle Babylonian')&m.site.isin(['Nippur','Dur-Kurigalzu','Babylon','Ur'])]}
groups=[('Kanesh','Old Assyrian','OB'),('Tuttul','Old Babylonian','OB'),('Pī-Kasî','Old Babylonian','OB'),('Alalakh','Old Babylonian','OB'),
        ('Susa','Old Babylonian','OB'),('Gasur/Nuzi','Middle Babylonian','MB'),('Alalakh','Middle Babylonian','MB'),('Akhetaten','Middle Babylonian','MB'),
        ('Ḫattusa','Middle Hittite','MB'),('Assur','Middle Assyrian','MB'),('Kar-Tukulti-Ninurta','Middle Assyrian','MB'),('Šibaniba','Middle Assyrian','MB')]
for k,c in centre.items(): print(k,'centre n',len(c),'photo h/w',round(c.hw_ratio.median(),2))
rows=[]
for s,per,k in groups:
    g=m[(m.site==s)&(m.per==per)]
    if len(g)<20: continue
    c=centre[k]; d=np.linalg.norm(g[X].mean()-c[X].mean())
    # reference: distance between two random halves of the centre, same size as g
    ref=np.median([np.linalg.norm(c.sample(len(g),random_state=i)[X].mean()-c[X].mean()) for i in range(200)])
    rows.append(dict(site=s,period=per,n=len(g),photo_hw=round(g.hw_ratio.median(),2),dist_to_centre=round(d,2),ref=round(ref,2),
                     ratio=round(d/ref,1),museums=g.collections.fillna('?').str.split(',').str[0].nunique()))
T=pd.DataFrame(rows); print(T.to_string(index=False)); T.to_csv(f'{R}/results/case_b_probe.csv',index=False)
