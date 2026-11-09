"""Download BDTNS (Database of Neo-Sumerian Texts, bdtns.cesga.es; M. Molina, CSIC) text-type labels for Ur III texts,
as an independent check on the keyword tagging of script 34. For each BDTNS text type (and the object type
'Tablet and Envelope'), run the site's search and page through the results (100 per page), keeping the BDTNS id,
CDLI P-number and provenience of each text. Output: bdtns/bdtns_types.csv. Polite: one request per second."""
from _paths import WORK
import re, time, requests, pandas as pd, html
R=WORK; B='https://bdtns.cesga.es'
TYPES=[('tipotexto',t) for t in ['Messenger Text','pisan dub-ba','Letter-order','Loan Document','Sale Document',
       'Legal Text: court record','Legal Text: other','School Text']]+[('tipoobjeto','Tablet and Envelope')]
def form(k,v):
    f=dict(numMuseo='',numBDTS='',numCDLI='',procedencia='TODOS',sello='TODOS',fechaPub='',datacion='',abreviatura='',autor='',
           propietario='',tipoobjeto='TODOS',tipotexto='TODOS',lexema_sello='',tipoperiodo='TODOS',tipolenguaje='TODOS',orden='')
    f[k]=v; return f
def rows(s):
    out=[]
    for chunk in s.split('resultado_bibliografia.php?id_bdts=')[1:]:
        bid=chunk[:6]; p=re.search(r'CDLI P(\d{6})',chunk[:4000])
        out.append(dict(bdtns_id=bid,CDLI_id=int(p.group(1)) if p else None))
    return out
recs=[]
for k,v in TYPES:
    S=requests.Session(); S.get(f'{B}/index.php?p=formulario_urIII',timeout=60)
    S.get(f'{B}/principal.php',params=form(k,v),timeout=180)  # the site's own search builds a GET query
    s=S.get(f'{B}/columna1.php?lexema_sello=&lexema=',timeout=180).content.decode('latin-1')
    tot=int(re.search(r'out of&nbsp;(\d+)',s).group(1)); got=rows(s); page=1
    while len(got)<tot and page<200:
        time.sleep(1); s=S.get(f'{B}/columna1.php?bloque=1',timeout=180).content.decode('latin-1'); r=rows(s)
        if not r: break
        got+=r; page+=1
    print(v,'total',tot,'rows',len(got),'with CDLI',sum(x['CDLI_id'] is not None for x in got),flush=True)
    recs+=[dict(**x,field=k,label=v) for x in got]
D=pd.DataFrame(recs).drop_duplicates(); D.to_csv(f'{R}/bdtns/bdtns_types.csv',index=False); print(len(D))
