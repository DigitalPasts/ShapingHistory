"""Regional sub-scores in a flat table (ShG, 8 Nov 2026: 'how does one see in the final dataset the different regional
scores?'). One row per period x parameter x region, from the regions column of lit_scores_v2_long.csv, next to the
cell's final score. Output: centralization/lit_scores_regional.csv"""
from _paths import WORK
import pandas as pd, json
R=WORK+'/centralization'
d=pd.read_csv(f'{R}/lit_scores_v2_long.csv'); rows=[]
for r in d.itertuples():
    if isinstance(r.regions,str) and r.regions.strip() not in ('','{}'):
        for reg,v in json.loads(r.regions).items():
            lo,hi=(v.split('-')+[v])[:2]
            rows.append(dict(period=r.period,param=r.param,region=reg,region_score_band=v,region_lo=float(lo),region_hi=float(hi),
                             cell_score_final=r.score_final,cell_status=r.status))
o=pd.DataFrame(rows); o.to_csv(f'{R}/lit_scores_regional.csv',index=False)
print(len(o),'rows;', o.groupby('period').size().to_dict())
