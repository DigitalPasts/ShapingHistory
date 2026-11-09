"""ShG's note of 9 Nov 2026: findspot, script date (ah./mh./jh., Old/Middle/New Hittite) and CTH for our photographed
Hittite tablets from S. Košak's Konkordanz der hethitischen Keilschrifttafeln (Hethitologie-Portal Mainz,
hethport.net/hetkonk). Query by publication (VS 28 = VSNF 12; KBo, KUB, IBoT ...) else by inventory number.
Output: hethport/hittite_konkordanz.csv"""
from _paths import WORK
import requests, re, time, pandas as pd
R=WORK; U='https://hethport.net/hetkonk/hetkonk_abfrage.php'
BL=dict(xrefnr1='',xrefnr2='',xcth1='',xcth2='',xpubl1='',xpubl2='',xpubl3='',xtextdat='',xanmerk='',xanmerkvgl='',xfundb='',xcthspan='',xmuseum='',xsortix='',per='')
SER=['ABoT','FHG','FHL','HFAC','HKM','HT','IBoT','KBo','KuSa','KUB','UBT','VBoT','VSNF']
def query(f):
    s=requests.post(U,data=dict(BL,**f),timeout=60).content.decode('utf-8','replace')
    out=[]
    for r in re.findall(r'<tr[^>]*>(.*?)</tr>',s,re.S):
        c=[re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',x)).strip() for x in re.findall(r'<td[^>]*>(.*?)</td>',r,re.S)]
        if len(c)>=8 and c[0]!='Inventarnummer': out.append(dict(inv=c[0],publ=c[3],cth=c[4],fundort=c[5],zeit=c[6],anm=c[7][:300]))
    return out
d=pd.read_parquet(f'{R}/master_tablets.parquet'); h=d[d.period=='Hittite'][['id','designation','museum_no','site']]
rows=[]
for r in h.itertuples():
    des=str(r.designation); f=None
    m=re.match(r'VS 28,\s*0*(\d+)',des)
    if m: f=dict(xpubl1='VSNF',xpubl2='12',xpubl3=m.group(1))
    else:
        m=re.match(r'(%s)\s+0*(\d+)[,.\s]+0*(\d+)'%'|'.join(SER),des)
        if m: f=dict(xpubl1=m.group(1),xpubl2=m.group(2),xpubl3=m.group(3))
        else:
            m=re.match(r'(%s)\s+0*(\d+)\s*$'%'|'.join(SER),des)
            if m: f=dict(xpubl1=m.group(1),xpubl3=m.group(2))
    if f is None and isinstance(r.museum_no,str) and r.museum_no[:2] not in ('BM',): f=dict(xmuseum=re.sub(r'\b0+(\d)',r'\1',r.museum_no.split('=')[0].strip()))
    hits=query(f) if f else []
    target=(f or {}).get('xpubl1','')
    want=(f'{target} {f["xpubl2"]}.{f["xpubl3"]}' if f.get('xpubl2') else f'{target} {f.get("xpubl3")}') if f else ''
    hit=next((x for x in hits if target and re.search(re.escape(want)+r'(?![\d.])',x['publ'])),hits[0] if len(hits)==1 else None)
    rows.append(dict(id=r.id,designation=des,museum_no=r.museum_no,site_cdli=r.site,query=str(f),n_hits=len(hits),**(hit or {})))
    time.sleep(1)
D=pd.DataFrame(rows); D.to_csv(f'{R}/hethport/hittite_konkordanz.csv',index=False)
print(len(D),'queried;',D.zeit.notna().sum(),'found'); print(D.zeit.value_counts().to_dict()); print(D.fundort.str.split(' ').str[0].value_counts().head(8).to_dict())
