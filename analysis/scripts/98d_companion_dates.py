"""ShG's guide notes of 9 Nov 2026: complete the dating of the photographed tablets from companion databases.
Old Babylonian and Early Old Babylonian: Archibab (full texts table, 36,060 texts, saved 9 Nov 2026 with archibab_table_v2.py on ShG's laptop),
linked to CDLI two ways: (a) CDLI's own Archibab cross-references (cdli_archibab_ids.csv) and (b) our museum-number /
publication match (19_archibab_match.py, unambiguous links only). Archibab dates carry the reign, year and an absolute
year (middle chronology), e.g. 'i/ Samsu-iluna 30 :1720'.
Outputs: turning/companion_dates.csv (one row per tablet that gains or confirms a date),
turning/dated_counts_with_companions.csv, turning/hammurabi_window_archibab.csv"""
from _paths import SHARED, WORK
import pandas as pd, numpy as np, re
R=WORK; O=f'{R}/turning'; P=SHARED
d=pd.read_parquet(f'{R}/master_tablets.parquet')
A=pd.read_csv(f'{P}/archibab/archibab_textes_v2.csv').drop_duplicates('id')   # full table, 9 Nov 2026
I=pd.read_csv(f'{P}/cdli_archibab_ids.csv'); I['archibab_id']='T'+I.archibab_id.astype(str)
I=I.rename(columns={'artifact_id':'id'})[['id','archibab_id']].assign(how='CDLI cross-reference')
M=pd.read_csv(f'{P}/archibab_cdli_match.csv').rename(columns={'CDLI_id':'id'})[['id','archibab_id']].assign(how='our match')
L=pd.concat([I,M]).drop_duplicates(['id','archibab_id'])
n_ab=L.groupby('id').archibab_id.nunique(); L=L[L.id.isin(n_ab[n_ab==1].index)]           # one Archibab text per tablet
L=L.groupby('id').agg(archibab_id=('archibab_id','first'),how=('how',lambda s:' + '.join(sorted(set(s))))).reset_index()
L=L.merge(A[['id','date','type','archives','from_to']].rename(columns={'id':'archibab_id','date':'ab_date','type':'ab_type','archives':'ab_archive'}),on='archibab_id',how='left')
def parse(s):
    if not isinstance(s,str) or not s.strip(): return (None,None,None)
    m=re.search(r'([A-ZŠṢṬ][\w\-šṣṭḫāēīū]+(?:-[\w\-šṣṭḫāēīū]+)*)\s*(?::|\s)\s*(\d+|Année_indéterminée)?.*?:\s*(\d{4})\b',s)
    if not m: 
        m2=re.search(r':\s*(\d{4})\b',s); return (None,None,int(m2.group(1)) if m2 else None)
    yr=int(m.group(2)) if m.group(2) and m.group(2).isdigit() else None
    return (m.group(1),yr,int(m.group(3)))
L[['ab_ruler','ab_year','ab_bce']]=pd.DataFrame(L.ab_date.map(parse).tolist(),index=L.index)
OBP=['Early Old Babylonian','Old Babylonian']
o=d[d.period.isin(OBP)][['id','period','site','genre','ruler','ryear']].merge(L,on='id',how='left')
o['ruler']=o.ruler.where(~o.ruler.isin(['--','-','?','']));
nm=lambda x: x.astype(str).str.translate(str.maketrans('ŠšṢṣṬṭḪḫ','SsSsTtHh')).str.replace('sh','s').str.replace('Sh','S').str.replace(r'_.*','',regex=True).str.replace(r'[^A-Za-z]','',regex=True).str.lower().str.replace('e','i').str.replace('p','b').str[:5]
o['cdli_dated']=o.ruler.notna(); o['ab_dated']=o.ab_ruler.notna()|o.ab_bce.notna()
o['gain']=~o.cdli_dated&o.ab_dated
o['conflict']=o.cdli_dated&o.ab_ruler.notna()&(nm(o.ruler).str.replace('erra','irra').str.replace('rap','rab')!=nm(o.ab_ruler).str.replace('erra','irra').str.replace('rap','rab'))
o[o.archibab_id.notna()].to_csv(f'{O}/companion_dates.csv',index=False)
T=o.groupby('period').agg(n=('id','size'),linked=('archibab_id','count'),cdli_dated=('cdli_dated','sum'),archibab_dated=('ab_dated','sum'),
    gain=('gain','sum'),conflicts=('conflict','sum')).reindex(OBP)
T['dated_after']=T.cdli_dated+T.gain; T['pct_before']=(100*T.cdli_dated/T.n).round(1); T['pct_after']=(100*T.dated_after/T.n).round(1)
T.to_csv(f'{O}/dated_counts_with_companions.csv'); print(T.to_string())
print('linked by:',L[L.id.isin(o.id)].how.value_counts().to_dict())
print('gains by site (top):',o[o.gain].site.value_counts().head(8).to_dict())
print('gains by archive (top):',o[o.gain].ab_archive.value_counts().head(8).to_dict())
# Hammurabi window (1790-1739, conquest of Larsa 1763) with Archibab absolute years where CDLI has none
OB={'Rim-Sin':1822,'Hammurapi':1792,'Samsu-iluna':1749,'Abi-ešuh':1711,'Ammi-ditana':1683,'Ammi-saduqa':1646,'Samsu-ditana':1625,'Warad-Sin':1834,'Sin-muballit':1812}
o['bce_cdli']=np.where(o.ruler.isin(OB)&o.ryear.notna(),o.ruler.map(OB)-(o.ryear-1),np.nan)
o['bce']=o.bce_cdli.fillna(o.ab_bce)
o['src']=np.where(o.bce_cdli.notna(),'CDLI',np.where(o.ab_bce.notna(),'Archibab',''))
w=o[o.bce.between(1739,1790)].copy(); w['side']=np.where(w.bce>=1764,'before','after')
g3=lambda s: s.where(s.isin(['Administrative','Letter','Legal']),'other')
w['g']=g3(w.genre)
H=w.groupby(['side','site','g','src']).size().unstack('src',fill_value=0).reset_index()
H.to_csv(f'{O}/hammurabi_window_archibab.csv',index=False)
print('\nHammurabi window, year known:',w.groupby(['side','src']).size().unstack(fill_value=0).to_string())
print(w.groupby(['site','side']).size().unstack(fill_value=0).sort_values('after',ascending=False).head(10).to_string())
