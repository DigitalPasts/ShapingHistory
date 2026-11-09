"""Period table on the cleaned dimensions (script 38): all tablets and archival documents only.
Uniformity = median absolute deviation of log(h/w) (MAD), with 95% bootstrap interval; also within museum.
Size classes: within each period, tablets are ranked by size (square root of height x width) and cut into five
equal-count classes (quintiles); the median height, width and ratio of each class are reported."""
from _paths import WORK
import numpy as np, pandas as pd
from scipy.stats import spearmanr
R=WORK; rng=np.random.default_rng(0)
c=pd.read_csv(f'{R}/results/tablet_dims_clean.csv'); c['l']=np.log(c.hw); c['coll']=c.collections.fillna('?').str.split(';').str[0]
dm=pd.read_csv(f'{R}/results/damage_score.csv').rename(columns={'CDLI_id':'artifact_id'})[['artifact_id','damage']]; c=c.merge(dm,on='artifact_id',how='left')
mad=lambda v: np.median(np.abs(v-np.median(v)))
def within(g,k):
    s=[(len(x),mad(x.l.values)) for _,x in g.groupby(k) if len(x)>=20]
    return np.average([b for a,b in s],weights=[a for a,b in s]) if s else np.nan
ORDER=['Uruk IV','Uruk III','Proto-Elamite','ED IIIa','ED IIIb','Ebla','Old Akkadian','Ur III','Early Old Babylonian','Old Babylonian',
 'Old Assyrian','Middle Assyrian','Middle Babylonian','Middle Elamite','Hittite','Neo-Assyrian','Neo-Babylonian','Achaemenid','Hellenistic']
rows=[]
for scope in ['all','archival']:
    for p in ORDER:
        g=c[c.P==p]; g=g[g.archival] if scope=='archival' else g
        if len(g)<50: continue
        bs=[mad(rng.choice(g.l.values,len(g))) for _ in range(300)]
        gd=g[g.damage.notna()]; md=np.nan
        if len(gd)>=60: md=within(gd.assign(dt=pd.qcut(gd.damage.rank(method='first'),3,labels=False)),'dt')
        sz=np.sqrt(g.height*g.width)
        rows.append(dict(scope=scope,period=p,n=len(g),median=round(g.hw.median(),3),share_wide=round((g.hw<1).mean(),3),
            MAD=round(mad(g.l.values),3),lo=round(np.percentile(bs,2.5),3),hi=round(np.percentile(bs,97.5),3),
            MAD_in_museum=round(within(g,'coll'),3),MAD_in_damage=round(md,3),rho_size_ratio=round(spearmanr(sz,g.l)[0],2),
            width_p10_p90=f'{g.width.quantile(.1):.0f}-{g.width.quantile(.9):.0f}',height_p10_p90=f'{g.height.quantile(.1):.0f}-{g.height.quantile(.9):.0f}'))
T=pd.DataFrame(rows); pd.set_option('display.width',250); print(T.to_string(index=False)); T.to_csv(f'{R}/results/s4_period_table_clean.csv',index=False)
a=T[T.scope=='archival'].set_index('period'); b=T[T.scope=='all'].set_index('period'); k=a.index.intersection(b.index)
print('rank agreement all vs archival MAD',round(spearmanr(a.loc[k,'MAD'],b.loc[k,'MAD'])[0],2))
print('rank agreement MAD vs within museum (archival)',round(spearmanr(a.MAD,a.MAD_in_museum)[0],2),' vs damage',round(spearmanr(a.MAD,a.MAD_in_damage,nan_policy='omit')[0],2))
# OB by genre group
ob=c[c.P=='Old Babylonian']
for lab,g in [('archival',ob[ob.archival]),('literary, lexical, school, mathematical',ob[ob.genre1.isin(['Literary','Lexical','Mathematical','Wisdom or proverb'])|(~ob.archival&(ob.genre1!='unknown'))])]:
    g=g.assign(q=pd.qcut(np.sqrt(g.height*g.width),5,labels=False))
    print('OB',lab,len(g),'median',round(g.hw.median(),2),'MAD',round(mad(g.l),3),'by size class',g.groupby('q').hw.median().round(2).tolist())
