"""What eBL adds to our photographed tablets (37d harvest, 9 Nov 2026): dates (king from eBL's chronology list, Kings.json
of the eBL frontend; eponym dates flagged isAssyrianDate), excavation site where CDLI has none, and thickness where CDLI
has none. Outputs: ebl/ebl_dates.csv, turning/ebl_additions_by_period.csv"""
from _paths import WORK
import pandas as pd, json, glob
R=WORK
K={k['orderGlobal']:k for k in json.load(open(f'{R}/ebl/kings.json'))}
E=[json.loads(l) for f in glob.glob(f'{R}/ebl/ebl_*.jsonl') for l in open(f)]; E=[r for r in E if r.get('status')==200]
rows=[]
for r in E:
    dt=r.get('date') or {}; kg=(dt.get('king') or {}); o=kg.get('orderGlobal'); a=r.get('archaeology') or {}
    th=(r.get('thickness') or {}).get('value')
    rows.append(dict(id=r['cdli_id'],period=r['period_cdli'],ebl=r['ebl_key'],ebl_period=(r.get('script') or {}).get('period'),
        king=K[o]['name'] if o in K else None,dynasty=K[o]['dynastyName'] if o in K else None,year=(dt.get('year') or {}).get('value') or None,
        eponym=json.dumps(dt.get('eponym'),ensure_ascii=False) if dt.get('eponym') else None,assyrian_date=dt.get('isAssyrianDate'),
        site=a.get('site'),findspot=json.dumps(a.get('findspot'),ensure_ascii=False) if a.get('findspot') else None,thickness=th,
        dates_in_text=len(r.get('datesInText') or [])))
D=pd.DataFrame(rows); D.to_csv(f'{R}/ebl/ebl_dates.csv',index=False)
d=pd.read_parquet(f'{R}/master_tablets.parquet')[['id','site','ruler','thick_side']]
X=D.merge(d,on='id',how='left',suffixes=('','_cdli'))
X['cdli_dated']=X.ruler.notna()&~X.ruler.isin(['--','-'])
X['ebl_dated']=X.king.notna()|X.eponym.notna()
X['site_gain']=X.site_cdli.isin(['unknown','uncertain'])&X.site.notna()
X['thick_gain']=X.thickness.notna()
T=X.groupby('period').agg(in_ebl=('id','size'),ebl_dated=('ebl_dated','sum'),date_gain=('ebl_dated',lambda s:int((s&~X.loc[s.index,'cdli_dated']).sum())),
    site_gain=('site_gain','sum'),thickness=('thick_gain','sum'),period_differs=('ebl_period',lambda s:int((s.notna()&(s!=X.loc[s.index,'period'])).sum())))
T.to_csv(f'{R}/turning/ebl_additions_by_period.csv'); print(T.to_string())
print(X[X.site_gain].site.value_counts().head(8).to_dict())
