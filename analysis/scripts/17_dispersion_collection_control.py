"""Does the period uniformity ranking survive a museum control?
(a) damage-adjusted VAE codes further residualised on museum within period (museum fixed effects, museums with >=30 tablets);
(b) dispersion within the single largest museum of each period. Compare rankings with the damage-adjusted baseline."""
from _paths import WORK
import pandas as pd, numpy as np
from scipy.stats import spearmanr
R=WORK
L=pd.read_csv(f'{R}/results/tablet_latent_damage_adjusted.csv')
a=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','collections'],low_memory=False).rename(columns={'artifact_id':'CDLI_id'})
L=L.drop(columns=['coll'],errors='ignore').merge(a,on='CDLI_id'); L['coll']=L.collections.fillna('?').str.split(';').str[0].str.strip()
Z=[f'Z{i}' for i in range(1,13)]
def disp(V): return np.median(np.linalg.norm(V-np.median(V,0),axis=1))
rows=[]
for p,g in L.groupby('Period_Name'):
    if len(g)<100 or p=='other': continue
    vc=g.coll.value_counts(); big=vc[vc>=30].index
    gg=g[g.coll.isin(big)]
    res=gg[Z]-gg.groupby('coll')[Z].transform('mean')+gg[Z].mean()
    top=g[g.coll==vc.index[0]]
    rows.append(dict(period=p,n=len(g),museums=len(big),top_museum=vc.index[0][:30],top_share=vc.iloc[0]/len(g),
                     disp_damage_adj=disp(g[Z].values),disp_museum_adj=disp(res.values),disp_top_museum=disp(top[Z].values) if len(top)>=30 else np.nan))
T=pd.DataFrame(rows).sort_values('disp_damage_adj')
print(T.round(2).to_string(index=False))
print('rank agreement damage-adj vs museum-adj', round(spearmanr(T.disp_damage_adj,T.disp_museum_adj)[0],2),
      '| vs top museum only', round(spearmanr(T.disp_damage_adj,T.disp_top_museum,nan_policy='omit')[0],2))
T.to_csv(f'{R}/results/dispersion_museum_control.csv',index=False)
