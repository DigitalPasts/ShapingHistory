"""Uniformity of h/w by period on two measures: catalogue dimensions and photographs (Zenodo silhouettes).
Photographs restricted to cleanly masked, unbroken tablets (six views, solidity >= 0.97); catalogue restricted to tablets.
Also flags catalogue height/width given the other way round (catalogue ratio ~ 1/photo ratio)."""
from _paths import WORK
import pandas as pd, numpy as np
from scipy.stats import spearmanr
R=WORK; rng=np.random.default_rng(0)
m=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','period','height','width','collections','artifact_type','artifact_preservation','genres'],low_memory=False)
m=m[m.artifact_type.fillna('').str.lower().str.contains('tablet')]
m['P']=m.period.str.extract(r'^([^\(]+?)\s*(?:\(|$)')[0].str.strip().replace({'Middle Hittite':'Hittite'})
m['coll']=m.collections.fillna('?').str.split(';').str[0].str.strip()
pix=pd.read_csv(f'{R}/zenodo/h_w_ratio_df_all.csv'); pix['artifact_id']=pix.tablet_p_id_CDLI.str.lstrip('P').astype(int)
pix=pix.groupby('artifact_id').hw_ratio.mean().rename('pix').reset_index()
mq=pd.read_csv(f'{R}/results/mask_quality.csv').rename(columns={'CDLI_id':'artifact_id'})
BROKEN=['fragment','50%','25%','75%','incomplete','fragmentary','broken']
d=m.merge(pix,on='artifact_id').merge(mq,on='artifact_id',how='left')
d['clean']=(~d.artifact_preservation.fillna('').str.lower().isin(BROKEN))&(d.n_big_parts==6)&(d.main_solidity>=0.97)
d['phys']=d.height/d.width
d['inverted']=(np.abs(np.log(d.phys)+np.log(d.pix))<0.1)&(np.abs(np.log(d.pix))>0.15)
madlog=lambda v: np.median(np.abs(np.log(v)-np.median(np.log(v))))
def within(g,col):
    s=[(len(x),madlog(x[col].values)) for _,x in g.groupby('coll') if len(x)>=20]
    return np.average([b for a,b in s],weights=[a for a,b in s]) if s else np.nan
ORDER=['Uruk IV','Uruk III','Proto-Elamite','ED I-II','ED IIIa','ED IIIb','Ebla','Old Akkadian','Lagash II','Ur III','Early Old Babylonian',
 'Old Babylonian','Old Assyrian','Middle Assyrian','Middle Babylonian','Middle Elamite','Hittite','Neo-Assyrian','Neo-Babylonian','Achaemenid','Hellenistic']
ph=pd.read_csv(f'{R}/results/s4_hw_by_period.csv').set_index('period')
rows=[]
for p in ORDER:
    g=d[(d.P==p)&d.clean]
    both=d[(d.P==p)&d.phys.between(0.05,9)]
    r=dict(period=p,n_photo_clean=len(g))
    if len(g)>=30:
        r.update(photo_median=round(g.pix.median(),3),photo_MAD=round(madlog(g.pix.values),3),photo_MAD_in_museum=round(within(g,'pix'),3))
    if len(both)>=30: r.update(n_both=len(both),rho_photo_catalogue=round(spearmanr(both.phys,both.pix)[0],2),inverted_share=round(both.inverted.mean(),3))
    if p in ph.index: r.update(cat_median=ph.loc[p,'median'],cat_MAD=ph.loc[p,'MAD_log'])
    rows.append(r)
T=pd.DataFrame(rows); pd.set_option('display.width',250); print(T.to_string(index=False))
T.to_csv(f'{R}/results/s4_uniformity_two_measures.csv',index=False)
t=T.dropna(subset=['photo_MAD','cat_MAD']); print('rank agreement photo vs catalogue MAD:',round(spearmanr(t.photo_MAD,t.cat_MAD)[0],2),'n periods',len(t))
na=d[(d.P=='Neo-Assyrian')&d.phys.between(0.05,9)]
print('NA inverted by genre:',na.groupby(na.genres.fillna('?')).inverted.agg(['size','mean']).query('size>=30').round(2).to_dict())
