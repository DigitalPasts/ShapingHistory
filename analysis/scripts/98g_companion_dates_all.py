"""All companion databases together (ShG, 9 Nov 2026): dated share per period before and after adding dates from
Archibab (OB, 98d), BDTNS (Ur III, 98e), NaBuCCo (NB, Achaemenid, Hellenistic, 37e), Prosobab (DANS dump 2022, 37g), Oracc catalogues (98i) and eBL (all periods, 37d);
script dates for Hittite from the Konkordanz (37f). 'Dated' = a king is named. Output: turning/dated_counts_all_sources.csv"""
from _paths import WORK
import pandas as pd, numpy as np, json, glob, os
R=WORK; O=f'{R}/turning'
MAIN=['ED IIIa','ED IIIb','Ebla','Old Akkadian','Ur III','Early Old Babylonian','Old Babylonian','Old Assyrian','Middle Babylonian',
      'Middle Assyrian','Neo-Assyrian','Neo-Babylonian','Achaemenid','Hellenistic','Hittite','Middle Elamite']
d=pd.read_parquet(f'{R}/master_tablets.parquet'); d=d[d.period.isin(MAIN)][['id','period','ruler']].copy()
d['cdli']=d.ruler.notna()&~d.ruler.isin(['--','-','?',''])
src={}
A=pd.read_csv(f'{O}/companion_dates.csv'); src['Archibab']=set(A[A.ab_dated].id)
B=pd.read_csv(f'{O}/ur3_bdtns_dates.csv'); src['BDTNS']=set(B[B.b_dated].id)
N=pd.read_csv(f'{R}/nabucco/nabucco_matched.csv'); src['NaBuCCo']=set(N[N.nb_king.notna()&(N.nb_king!='XXX')].id)
P=pd.read_csv(f'{R}/prosobab/prosobab_matched.csv'); src['Prosobab']=set(P[P.King.notna()].id)
Q=pd.read_csv(f'{R}/oracc/oracc_matched.csv'); src['Oracc']=set(Q[Q.o_dated].id)
E=[json.loads(l) for f in glob.glob(f'{R}/ebl/ebl_*.jsonl') for l in open(f)]
src['eBL']={r['cdli_id'] for r in E if r.get('status')==200 and (r.get('date') or {}).get('king') and (r['date']['king'].get('orderGlobal') is not None)}
ebl_seen={r['cdli_id'] for r in E if r.get('status')==200}
for k,s in src.items(): d[k]=d.id.isin(s)
d['any']=d.cdli|d[list(src)].any(axis=1)
T=d.groupby('period').agg(n=('id','size'),cdli=('cdli','sum'),**{k:(k,'sum') for k in src},after=('any','sum')).reindex(MAIN)
for k in src: T[f'gain_{k}']=d[~d.cdli&d[k]].groupby('period').size().reindex(MAIN).fillna(0).astype(int)
T['pct_before']=(100*T.cdli/T.n).round(1); T['pct_after']=(100*T.after/T.n).round(1)
T['ebl_fetched']=d[d.id.isin(ebl_seen)].groupby('period').size().reindex(MAIN).fillna(0).astype(int)
H=f'{R}/hethport/hittite_konkordanz.csv'
if os.path.exists(H):
    h=pd.read_csv(H); T.loc['Hittite','script_dated']=int(h.zeit.isin(['ah.','ah.?','ah.?/mh.?','mh.','mh.?','jh.','sjh.']).sum())
T.to_csv(f'{O}/dated_counts_all_sources.csv'); print(T[['n','cdli','after','pct_before','pct_after']+[f'gain_{k}' for k in src]+['ebl_fetched']].to_string())
