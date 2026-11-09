"""ShG's guide note of 9 Nov 2026: Ur III dates from BDTNS where CDLI has none (bdtns/bdtns_dates.csv from 37c).
BDTNS date codes: UN/SH/AS/SS/IS + regnal year (Ur-Namma, Šulgi, Amar-Suen, Šu-Suen, Ibbi-Suen); 'SH42//AS06' lists
alternatives (kept only when every alternative names the same king); 'XXXX' or '0000' = year not preserved.
Outputs: turning/ur3_bdtns_dates.csv, and an Ur III row added to turning/dated_counts_with_companions.csv"""
from _paths import WORK
import pandas as pd, numpy as np, re, glob, os
R=WORK; O=f'{R}/turning'
f=f'{R}/bdtns/bdtns_dates.csv'
B=pd.read_csv(f,dtype=str) if os.path.exists(f) else pd.concat([pd.read_csv(x,dtype=str) for x in glob.glob(f'{R}/bdtns/bdtns_dates_*.csv')])
B=B.drop_duplicates('bdtns_id'); B=B[B.CDLI_id.notna()&(B.CDLI_id!='')]
K={'UN':'Ur-Namma','SH':'Šulgi','AS':'Amar-Suen','SS':'Šu-Suen','IS':'Ibbi-Suen'}
def parse(s):
    if not isinstance(s,str): return (None,None)
    y=s.split(' - ')[0].strip(); alts=[a for a in y.split('//') if a]
    ks={a[:2] for a in alts if a[:2] in K}
    if len(ks)!=1: return (None,None)
    k=ks.pop(); yrs={re.match(r'\d+',a[2:]).group(0) for a in alts if a[:2]==k and re.match(r'\d+',a[2:])}
    return (K[k], int(yrs.pop()) if len(yrs)==1 and len(alts)==1 else None)
B[['b_ruler','b_year']]=pd.DataFrame(B.date.map(parse).tolist(),index=B.index)
B['id']=B.CDLI_id.astype(int)
b=B.groupby('id').agg(bdtns_id=('bdtns_id','first'),b_date=('date','first'),b_ruler=('b_ruler','first'),b_year=('b_year','first'),b_prov=('provenience','first')).reset_index()
d=pd.read_parquet(f'{R}/master_tablets.parquet'); u=d[d.period=='Ur III'][['id','site','genre','ruler','ryear']].copy()
u['ruler']=u.ruler.where(~u.ruler.isin(['--','-','?','']))
u=u.merge(b,on='id',how='left')
nm=lambda x: x.astype(str).str.replace('Sh','S').str.normalize('NFKD').str.encode('ascii','ignore').str.decode('ascii').str.replace('Sh','S').str.replace('sh','s').str.replace(r'[^A-Za-z]','',regex=True).str.lower().str[:4]
u['cdli_dated']=u.ruler.notna(); u['in_bdtns']=u.bdtns_id.notna(); u['b_dated']=u.b_ruler.notna()
u['gain']=~u.cdli_dated&u.b_dated; u['gain_year']=(u.ryear.isna())&u.b_year.notna()
u[u.in_bdtns].to_csv(f'{O}/ur3_bdtns_dates.csv',index=False)
row=dict(n=len(u),linked=int(u.in_bdtns.sum()),cdli_dated=int(u.cdli_dated.sum()),archibab_dated=np.nan,bdtns_dated=int(u.b_dated.sum()),
         gain=int(u.gain.sum()),conflicts=int((u.cdli_dated&u.b_dated&(nm(u.ruler)!=nm(u.b_ruler))).sum()))
row['dated_after']=row['cdli_dated']+row['gain']; row['pct_before']=round(100*row['cdli_dated']/row['n'],1); row['pct_after']=round(100*row['dated_after']/row['n'],1)
T=pd.read_csv(f'{O}/dated_counts_with_companions.csv',index_col=0)
T.loc['Ur III']=pd.Series(row); T.to_csv(f'{O}/dated_counts_with_companions.csv')
print(T.to_string()); print('year newly known:',int(u.gain_year.sum()),'| BDTNS rows harvested',len(B))
print('gains by site:',u[u.gain].site.value_counts().head(6).to_dict())
