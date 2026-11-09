"""Answers ShG's guide notes of 8 Nov 2026: how many tablets are dated in each period, where from and in which genres,
and what lies behind the Hammurabi 'no shift' result (T7, conquest of Larsa 1763 BCE).
Data: master_tablets.parquet (photographed CDLI tablets used in the paper). 'Dated' = a ruler name in the CDLI date
field; 'dated to the year' = ruler plus regnal year.
Outputs: turning/dated_counts_period.csv, turning/dated_counts_period_site_genre.csv, turning/hammurabi_window.csv"""
from _paths import WORK
import pandas as pd, numpy as np
R=WORK; O=f'{R}/turning'
d=pd.read_parquet(f'{R}/master_tablets.parquet')
MAIN=['ED IIIa','ED IIIb','Ebla','Old Akkadian','Ur III','Early Old Babylonian','Old Babylonian','Old Assyrian','Middle Babylonian',
      'Middle Assyrian','Neo-Assyrian','Neo-Babylonian','Achaemenid','Hellenistic']
d=d[d.period.isin(MAIN)].copy()
d['dated']=d.ruler.notna(); d['dated_year']=d.ruler.notna()&d.ryear.notna()
g3=lambda s: s.where(s.isin(['Administrative','Letter','Legal','Business / Contracts']),'other')
d['g']=g3(d.genre)
P=d.groupby('period').agg(n=('id','size'),dated=('dated','sum'),dated_year=('dated_year','sum'),
    sites=('site','nunique')).reindex(MAIN)
P['pct_dated']=(100*P.dated/P.n).round(0)
for gg in ['Administrative','Letter','Legal']:
    P[f'dated_{gg[:5].lower()}']=d[d.dated&(d.g==gg)].groupby('period').size().reindex(MAIN).fillna(0).astype(int)
top=d[d.dated].groupby(['period','site']).size().reset_index(name='k').sort_values(['period','k'],ascending=[True,False])
P['top_dated_sites']=[', '.join(f'{r.site} {r.k}' for r in top[top.period==p].head(3).itertuples()) for p in MAIN]
P.to_csv(f'{O}/dated_counts_period.csv')
S=d[d.dated].groupby(['period','site','g']).size().reset_index(name='n_dated')
S.to_csv(f'{O}/dated_counts_period_site_genre.csv',index=False)
# Hammurabi window: same chronology table as 94
OB={'Rim-Sin':1822,'Hammurapi':1792,'Samsu-iluna':1749,'Abi-ešuh':1711,'Ammi-ditana':1683,'Ammi-saduqa':1646,'Samsu-ditana':1625,'Warad-Sin':1834,'Sin-muballit':1812}
o=d[d.period=='Old Babylonian'].copy()
o['bce']=np.where(o.ruler.isin(OB),o.ruler.map(OB)-(o.ryear.fillna(1).clip(lower=1)-1),np.nan)
o['yr_known']=o.ryear.notna()
o=o[o.bce.between(1739,1790)]
o['side']=np.where(o.bce>=1764,'before (1790-1764)','after (1763-1739)')
H=o.groupby(['side','site','g']).agg(n=('id','size'),with_year=('yr_known','sum')).reset_index()
H.to_csv(f'{O}/hammurabi_window.csv',index=False)
print(P[['n','dated','dated_year','pct_dated','dated_admin','dated_lette','dated_legal','top_dated_sites']].to_string())
print('\nHammurabi window (OB, 1790-1739):'); print(H.pivot_table(index=['site','g'],columns='side',values='n',aggfunc='sum',fill_value=0).to_string())
print('year-1 fills in window:', int((~o.yr_known).sum()), 'of', len(o))
