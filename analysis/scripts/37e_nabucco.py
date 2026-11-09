"""ShG's note of 9 Nov 2026: NaBuCCo (Neo-Babylonian Cuneiform Corpus, nabucco.acdh.oeaw.ac.at; Jursa, Abraham, Gordin)
metadata for our Neo-Babylonian, Achaemenid and Hellenistic tablets. The full CSV export fails on the server, so the
tablet list is exported archive by archive (?archiv=<id>&_export=csv: ID, publication, text no., museum no., type,
archive, place of issue, period), then matched to our photographed tablets by museum number; the detail page of each
matched tablet is read for its date. Outputs: nabucco/nabucco_tablets.csv, nabucco/nabucco_matched.csv"""
from _paths import WORK
import requests, pandas as pd, io, re, time, sys, os
R=WORK; B='https://nabucco.acdh.oeaw.ac.at'; S=requests.Session(); S.headers['User-Agent']='shaping-history-research'
if not os.path.exists(f'{R}/nabucco/nabucco_tablets.csv'):
    arch=[]; url=f'{B}/api/archivs/'
    while url:
        j=S.get(url,timeout=60).json(); arch+=[int(a['url'].rstrip('/').split('/')[-1]) for a in j['results']]; url=j['next']; time.sleep(0.5)
    parts=[]
    for a in arch:
        r=S.get(f'{B}/archiv/tablet/?archiv={a}&_export=csv',timeout=300)
        if r.status_code==200 and r.text.startswith('ID'): parts.append(pd.read_csv(io.StringIO(r.text),dtype=str).assign(archiv_id=a))
        else: print('archive',a,'export failed',r.status_code)
        time.sleep(0.5)
    T=pd.concat(parts).drop_duplicates('ID'); T.to_csv(f'{R}/nabucco/nabucco_tablets.csv',index=False); print('NaBuCCo tablets',len(T),'from',len(parts),'archives')
T=pd.read_csv(f'{R}/nabucco/nabucco_tablets.csv',dtype=str)
def mk(s):
    if not isinstance(s,str): return None
    m=re.match(r'\s*([A-Za-z]+)\.?\s*0*(\d+)',s); return f'{m.group(1).upper()}{m.group(2)}' if m else None
T['k']=T['Museum No.'].map(mk)
d=pd.read_parquet(f'{R}/master_tablets.parquet'); d=d[d.period.isin(['Neo-Babylonian','Achaemenid','Hellenistic'])][['id','period','site','museum_no','ruler','ryear']]
d['k']=d.museum_no.map(mk)
M=d.merge(T,on='k',how='inner'); amb=M.groupby('id').ID.nunique(); M=M[M.id.isin(amb[amb==1].index)].drop_duplicates('id')
print('our NB/Ach/Hell tablets',len(d),'matched',len(M), M.period.value_counts().to_dict())
rows=[]
for r in M.itertuples():
    try: s=S.get(f'{B}/archiv/tablet/detail/{r.ID}',timeout=60).text
    except Exception: s=''
    txt=re.sub(r'(\| ?)+','|',re.sub(r'\s+',' ',re.sub(r'<[^>]+>','|',s)))
    g=lambda lab: (re.search(re.escape(lab)+r'\|\s*([^|]*)',txt) or [None,None])[1]
    dr=(g('Babylonian Date (year-month-day): ') or '').strip()
    m=re.match(r'([A-Za-zŠšĀāĪīŪū\-\s]+?)\.?\s+(\d+|yy)',dr)
    rows.append(dict(id=r.id,nabucco_id=r.ID,cdli_p=(g('CDLI P-Identifier') or '').strip(),date_raw=dr,
                     nb_king=m.group(1).strip() if m else None,nb_year=int(m.group(2)) if m and m.group(2).isdigit() else None))
    time.sleep(0.7)
D=M.merge(pd.DataFrame(rows),on='id',how='left'); D.to_csv(f'{R}/nabucco/nabucco_matched.csv',index=False)
print('with king',D.nb_king.notna().sum(),'with year',D.nb_year.notna().sum()); print(D.nb_king.value_counts().head(12).to_dict())
