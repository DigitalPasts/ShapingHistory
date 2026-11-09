"""Does relabelling in the current CDLI catalogue (vs the April 2024 labels used for training) change the
uniformity results? Recompute VAE latent dispersion by period with today's labels and compare."""
from _paths import WORK
import pandas as pd, numpy as np
from scipy.stats import spearmanr
R=WORK
d=pd.concat([pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_{s}.csv') for s in ['train','val','test']])
m=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','artifact_type','period'],low_memory=False)
d=d.merge(m,left_on='CDLI_id',right_on='artifact_id'); d=d[d.artifact_type.isin(['tablet','tablet & envelope'])].copy()
d['now']=d.period.fillna('').str.split(' \\(').str[0].replace({'Middle Hittite':'Hittite','':'(none)'})
d['then']=d.Period_Name.replace({'Middle Hittite':'Hittite'})
print('tablets whose period differs (Hittite renaming ignored):', round((d.now!=d.then).mean()*100,2),'%')
X=[f'X{i}' for i in range(1,13)]; Z=(d[X]-d[X].mean())/d[X].std()
def disp(col):
    r={}
    for p,g in d.groupby(col):
        if len(g)>=100 and p not in ('other','(none)'): v=Z.loc[g.index].values; r[p]=np.median(np.linalg.norm(v-np.median(v,0),axis=1))
    return pd.Series(r)
a,b=disp('then'),disp('now'); j=pd.concat([a.rename('april2024'),b.rename('cdli_now')],axis=1).dropna()
j['diff']=j.cdli_now-j.april2024; print(j.round(3).sort_values('april2024').to_string())
print('rank agreement', round(spearmanr(j.april2024,j.cdli_now)[0],3), '| max abs change', round(j['diff'].abs().max(),3))
j.to_csv(f'{R}/results/current_labels_check.csv')
