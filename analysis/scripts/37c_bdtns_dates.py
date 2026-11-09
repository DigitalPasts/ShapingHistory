"""ShG's guide note of 9 Nov 2026: date the Ur III tablets from BDTNS (Database of Neo-Sumerian Texts, bdtns.cesga.es,
M. Molina, CSIC) where the CDLI date field is empty. Pages through the site's full search (all texts, 100 per page,
one request per second) and keeps BDTNS id, CDLI P-number, provenience and the BDTNS date (e.g. 'AS02 - 04 - 00' =
Amar-Suen year 2, month 4, day unknown). Run per provenience group in parallel: python3 37c_bdtns_dates.py <tag> <province> [<province> ...];
writes bdtns/bdtns_dates_<tag>.csv; then python3 37c_bdtns_dates.py merge -> bdtns/bdtns_dates.csv."""
from _paths import WORK
import re, time, requests, os, csv, sys
R=WORK; B='https://bdtns.cesga.es'; OUT=None
F=dict(numMuseo='',numBDTS='',numCDLI='',procedencia='TODOS',sello='TODOS',fechaPub='',datacion='',abreviatura='',autor='',
       propietario='',tipoobjeto='TODOS',tipotexto='TODOS',lexema_sello='',tipoperiodo='TODOS',tipolenguaje='TODOS',orden='')
def rows(s):
    out=[]
    for ch in s.split('resultado_bibliografia.php?id_bdts=')[1:]:
        bid=ch[:6]; p=re.search(r'CDLI P(\d{6})',ch)
        pr=re.search(r'<!--Procedencia-->\s*<td>\s*<div align="center">(.*?)</div>',ch,re.S)
        dt=re.search(r'<!--Dataci.n-->.*?<td width="100px">(.*?)</td>',ch,re.S)
        out.append(dict(bdtns_id=bid,CDLI_id=p.group(1) if p else '',provenience=pr.group(1).strip() if pr else '',
                        date=re.sub(r'\s+',' ',dt.group(1)).strip() if dt else ''))
    return out
def harvest(prov,w,done):
    S=requests.Session(); S.get(f'{B}/index.php?p=formulario_urIII',timeout=60); S.get(f'{B}/principal.php',params=dict(F,procedencia=prov),timeout=300)
    s=S.get(f'{B}/columna1.php?lexema_sello=&lexema=',timeout=300).content.decode('utf-8','replace')
    m=re.search(r'out of&nbsp;(\d+)',s)
    if not m: print(prov,'no results',flush=True); return
    tot=int(m.group(1)); got=0; page=1; fails=0
    while True:
        r=rows(s)
        for x in r:
            if x['bdtns_id'] not in done: w.writerow(dict(x,query=prov)); done.add(x['bdtns_id'])
        got+=len(r)
        if page%25==0: print(f'{prov}: page {page}, {got} of {tot}',flush=True)
        if got>=tot or not r: break
        time.sleep(1)
        try: s=S.get(f'{B}/columna1.php?bloque=1',timeout=300).content.decode('utf-8','replace'); fails=0
        except Exception as e:
            fails+=1; print('retry',e,flush=True); time.sleep(10*fails)
            if fails>4: break
            continue
        page+=1
    print(prov,'done',got,'of',tot,flush=True)
if sys.argv[1]=='merge':
    import pandas as pd, glob
    D=pd.concat([pd.read_csv(f,dtype=str) for f in glob.glob(f'{R}/bdtns/bdtns_dates_*.csv')]).drop_duplicates('bdtns_id')
    D.to_csv(f'{R}/bdtns/bdtns_dates.csv',index=False); print(len(D))
else:
    tag=sys.argv[1]; OUT=f'{R}/bdtns/bdtns_dates_{tag}.csv'
    f=open(OUT,'w',newline='',encoding='utf-8'); w=csv.DictWriter(f,fieldnames=['bdtns_id','CDLI_id','provenience','date','query']); w.writeheader()
    done=set()
    for prov in sys.argv[2:]: harvest(prov,w,done); f.flush()
