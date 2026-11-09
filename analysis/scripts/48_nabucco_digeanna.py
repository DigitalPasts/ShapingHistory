"""Case C data: DigEanna tablets from NaBuCCo (nabucco.acdh.oeaw.ac.at, ACDH Vienna), scraped from the public
browse pages (the API and CSV export returned server errors on 27 Oct 2026). For each tablet: NaBuCCo id, museum
number, publication, CDLI P-number, place of issue, archive, period, date, text form, legal purpose, transaction type,
tablet format as annotated by the project, and the scribe named in the paraphrase. Output: nabucco/digeanna_tablets.csv."""
from _paths import WORK
import re, html, time, urllib.request, pandas as pd, concurrent.futures as cf, sys
B='https://nabucco.acdh.oeaw.ac.at'
def get(u,tries=3):
    for k in range(tries):
        try: return urllib.request.urlopen(u,timeout=120).read().decode('utf-8','ignore')
        except Exception: time.sleep(2+3*k)
    return ''
ids=set(); page=1
while True:
    t=get(f'{B}/archiv/tablet/?project=8&page={page}')
    new=set(re.findall(r'/archiv/tablet/detail/(\d+)',t))
    if not new or new<=ids: break
    ids|=new; page+=1; time.sleep(0.3)
print('detail ids',len(ids),'pages',page-1,flush=True)
F=['NaBuCCo ID','Museum No.','Primary Publication','CDLI P-Identifier','Place of issue','Regional setting','Archive','Period','Date (year-month-day):','Date BCE','Text Form','Legal Purpose','Transaction Type','Format of the tablet','Content Paraphrase']
def parse(i):
    t=get(f'{B}/archiv/tablet/detail/{i}'); t=re.sub(r'<(script|style).*?</\1>','',t,flags=re.S)
    s=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',t)))
    s=s[s.find('Basic Metadata'):]
    pos=sorted([(s.find(' '+f+' '),f) for f in F if s.find(' '+f+' ')>=0])
    d={'detail_id':i}
    for k,(p,f) in enumerate(pos):
        end=pos[k+1][0] if k+1<len(pos) else s.find('Legacy Paraphrase') if s.find('Legacy Paraphrase')>p else p+600
        d[f.rstrip(':')]=s[p+len(f)+2:end].strip()
    m=re.search(r'scribe ([A-ZŠṢṬĀĒĪŪ][^ ,;.()]+(?: ?/[^ ,;.()]+)?(?: ?//[^ ,;.()]+)?)',d.get('Content Paraphrase',''))
    d['scribe']=m.group(1) if m else None
    return d
with cf.ThreadPoolExecutor(4) as ex: rows=list(ex.map(parse,sorted(ids,key=int)))
D=pd.DataFrame(rows); D.to_csv(WORK+'/nabucco/digeanna_tablets.csv',index=False)
print(len(D)); print(D.notna().sum().to_string())
