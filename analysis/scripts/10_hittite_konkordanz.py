"""Finer dating for the Hittite tablets from S. Kosak, Konkordanz der hethitischen Keilschrifttafeln
(hethiter.net/: hetkonk), queried by inventory number, then by publication. Script-based datings:
ah. = Old Hittite script, mh. = Middle Hittite, jh. = New Hittite, sjh. = late New Hittite."""
from _paths import WORK
import pandas as pd, re, html, subprocess, time, json, os
R=WORK; CACHE=f'{R}/results/konkordanz_cache'; os.makedirs(CACHE,exist_ok=True)
d=pd.concat([pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_{s}.csv',usecols=['CDLI_id','Period_Name']) for s in ['train','val','test']])
m=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','designation','museum_no','excavation_no'],low_memory=False)
x=d[d.Period_Name.isin(['Hittite','Middle Hittite'])].merge(m,left_on='CDLI_id',right_on='artifact_id')
def post(data,key):
    f=f'{CACHE}/{key}.html'
    if not os.path.exists(f):
        args=['curl','-sS','-m','40','-A','Mozilla/5.0','-X','POST']
        for k,v in data.items(): args+=['--data-urlencode',f'{k}={v}']
        open(f,'w').write(subprocess.run(args+['https://hethport.net/hetkonk/hetkonk_abfrage.php'],capture_output=True,text=True).stdout); time.sleep(0.5)
    return open(f).read()
def rows(t):
    out=[]
    for tr in re.findall(r'<tr[^>]*>(.*?)</tr>',t,flags=re.S):
        cells=[re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',c))).strip() for c in re.findall(r'<td[^>]*>(.*?)</td>',tr,flags=re.S)]
        if cells: out.append(cells)
    return out
DAT=re.compile(r'^(ah\.\?/mh\.\?|ah\.\??|mh\.\??|jh\.\??|sjh\.\??|aA|mA|mB|ass\.-mit\.)$')
def dating(t,want):
    # take only the row of the queried tablet itself (inventory or publication number), not joins or duplicates
    norm=lambda v: re.sub(r'[\s.,]+',' ',v).strip().lower()
    for c in rows(t):
        hits=[v for v in c if DAT.match(v)]
        if hits and any(norm(want)==norm(v) for v in c[:4]): return hits[0], c
    return None, None
def queries(r):
    mu=str(r.museum_no) if pd.notna(r.museum_no) else ''
    p=mu.split(' ',1)
    if len(p)==2 and p[0] in ('VAT','AO','Bo','Ashm','OIM','MAH','WML','SM','MM','HAM','IMJ'):
        yield {'xrefnr1':p[0],'xrefnr2':p[1]}, (('A '+p[1].lstrip('A0')) if p[0]=='OIM' else mu), f'inv_{p[0]}_{p[1]}'.replace('/','_').replace(' ','_')
    if re.match(r'^\d+/[a-z]+$',mu):
        n,s=mu.split('/'); yield {'xrefnr1':f'/{s}%','xrefnr2':n}, mu, f'exc_{n}_{s}'
    de=str(r.designation)
    mm=re.match(r'^(VS|FHG|VBoT|HFAC|KUB|FHL)\s*(\d+)?,?\s*(\d+[a-z]?)?',de)
    if mm:
        pub,vol,no=mm.groups(); pub={'VS':'VSNF'}.get(pub,pub)
        if pub=='VSNF' and vol=='28': vol='12'   # VS 28 = VS NF 12 in the Konkordanz
        if pub in ('FHG','VBoT','HFAC','FHL') and no is None: vol,no='',vol
        yield {'xpubl1':pub,'xpubl2':vol or '','xpubl3':str(int(no)) if no and no.isdigit() else (no or '')}, f"{pub} {vol+'.' if vol else ''}{int(no) if no and no.isdigit() else no}", f'pub_{pub}_{vol}_{no}'
res=[]
for _,r in x.iterrows():
    got=(None,None,None)
    for q,want,key in queries(r):
        dt,row=dating(post(q,key),want)
        if dt: got=(dt,key,' | '.join(row[:5])); break
    res.append(dict(CDLI_id=r.CDLI_id,designation=r.designation,museum_no=r.museum_no,konkordanz_dating=got[0],query=got[1],row=got[2]))
o=pd.DataFrame(res); o.to_csv(f'{R}/results/hittite_konkordanz_dating.csv',index=False)
print(o.konkordanz_dating.value_counts(dropna=False).to_string()); print(o[o.konkordanz_dating.isna()].designation.str.split(' ').str[0].value_counts().to_dict())
