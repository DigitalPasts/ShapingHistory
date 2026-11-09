"""Period table for the SI, regenerated from the released data (tablets only) and checked against the
current CDLI catalogue (artifacts.csv export; an 800-tablet sample checked against the live API agreed 99.9%)."""
from _paths import WORK
import pandas as pd, numpy as np
R=WORK
d=pd.concat([pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_{s}.csv',usecols=['CDLI_id','Period_Name','Genre_Name']) for s in ['train','val','test']])
m=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','artifact_type','period','provenience','height','width'],low_memory=False)
d=d.merge(m,left_on='CDLI_id',right_on='artifact_id',how='left').merge(pd.read_csv(f'{R}/results/damage_score.csv')[['CDLI_id','damage']],on='CDLI_id',how='left')
print('all objects',len(d),'| tablets',d.artifact_type.isin(['tablet','tablet & envelope']).sum())
t=d[d.artifact_type.isin(['tablet','tablet & envelope'])].copy()
t['now']=t.period.fillna('').str.split(' \\(').str[0]; t['site']=t.provenience.fillna('unknown').str.split(' \\(').str[0].replace({'uncertain':'unknown'})
q=d.damage.quantile(2/3)
def row(g):
    sc=g.site.value_counts(normalize=True)
    return pd.Series({'tablets':len(g),'with_mm_dimensions':int((g.height>0).sum()),'administrative':(g.Genre_Name=='Administrative').mean(),
        'main_findspot':sc.index[0],'main_findspot_share':sc.iloc[0],'most_damaged_third':(g.damage>q).mean(),
        'relabelled_in_CDLI_since_2024':(g.now!=g.name).mean()})
T=t.groupby('Period_Name').apply(row).sort_values('tablets',ascending=False)
T.to_csv(f'{R}/results/period_table_SI.csv'); print(T.round(2).to_string())
print('periods >=100 tablets', (T.tablets>=100).sum(), 'covering', T[T.tablets>=100].tablets.sum())
