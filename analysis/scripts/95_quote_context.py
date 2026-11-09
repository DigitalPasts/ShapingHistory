"""Locate every quoted statement in the full texts of the works (Dropbox PDFs converted with pdftotext) and keep the
surrounding passage, the PDF page and the Dropbox file, so the assessment page can show each quote in context and link to
the PDF. Output: centralization/quote_context.json keyed by statement id (period|param|key|first 50 chars of the quote)."""
from _paths import LIT, WORK
import os, re, json, bisect, unicodedata, pandas as pd, urllib.parse
T=LIT+'/txt'; OH=LIT+'/ohane'; OUT=WORK+'/centralization'
LIT='/Research-current/Deeplomatics/Literature/'
SPECIAL={'Archi_2015_Ebla_Archives.txt':'/Pdf Articles/A/Archi/(Studies in Ancient Near Eastern Records 7) Alfonso Archi-Ebla and its Archives_ Texts, History, and Society-Walter de Gruyter (2015).pdf',
 'Vita_2021_HAL.txt':'/Pdf Articles/Vita 2021 History of the Akkadian Language. HdO 152. 2 Vols.pdf','Archi_AGI.2020.txt':'/Pdf Articles/A/Archi/Archi_AGI.2020.pdf',
 'Molina_2016_Archives_and_bookkeeping_in_Southern_Me.txt':'/Pdf Articles/M/Molina/Molina_2016_Archives_and_bookkeeping_in_Southern_Me.pdf',
 'Ur3Archives.txt':'/Uruk_Region/Literature/Ur3Archives.pdf','The_Temple_and_the_Land_in_ICDOG_7_Tempe.txt':'/Old-Mac-Jul25/Download-files/The_Temple_and_the_Land_in_ICDOG_7_Tempe.pdf'}
PRAGUE='/Review&Editorial/PeerReview/Taxation_vol_Prague/Mynarova-Alivernini_taxation_2020.zip Folder/'
def dbx(fn):
    if fn in SPECIAL: return SPECIAL[fn]
    if fn.startswith('OHANE_'): return LIT+fn.replace('.txt','_small.pdf')
    b=fn[:-4]
    if os.path.exists(f'{LIT}/dbx/{b}.docx'): return PRAGUE+b+'.docx'
    return LIT+b+'.pdf'
def url(p): return 'https://www.dropbox.com/preview'+urllib.parse.quote(p)
def norm(s):
    s=unicodedata.normalize('NFKC',s); s=re.sub(r'-\s*\n\s*(\w)',r'\1',s); s=s.lower()
    s=re.sub(r'[‘’“”"\'`´]','',s); s=re.sub(r'[^\w]+',' ',s); return re.sub(r'\s+',' ',s).strip()
files=[(f'{T}/{f}',f) for f in sorted(os.listdir(T)) if f.endswith('.txt')]+[(f'{OH}/{f}',f) for f in sorted(os.listdir(OH)) if f.endswith('.txt')]
IDX=[]
for path,fn in files:
    pages=open(path,errors='ignore').read().split('\f'); buf=[]; starts=[]; pos=0
    for p in pages:
        n=norm(p); starts.append(pos); buf.append(n); pos+=len(n)+1
    IDX.append((fn,' '.join(buf),starts,pages))
print('indexed',len(IDX))
ev=pd.read_csv(f'{OUT}/lit_evidence_v2_long.csv')
def sid(r): return f"{r['period']}|{r['param']}|{r['key']}|{str(r['quote'])[:50]}"
def segs(q):
    parts=[norm(x) for x in re.split(r'\.\.\.|…|\[[^\]]*\]',str(q))]; parts=[p for p in parts if len(p)>=25]
    return sorted(parts,key=len,reverse=True)
# prefer files whose name shares the author's surname
def cand(key):
    sur=re.match(r'[a-z]+',key).group(0) if isinstance(key,str) else ''
    a=[x for x in IDX if sur and sur in x[0].lower()]; return a+[x for x in IDX if x not in a]
out={}; miss=0
for _,r in ev.drop_duplicates(subset=['period','param','key','quote']).iterrows():
    k=sid(r)
    if k in out: continue
    found=None
    # probes: the start of the longest segments, then two inner windows (OCR often drops ligatures such as 'Th', 'fi')
    probes=[x[:120] for x in segs(r['quote'])[:2]]+[x[a:a+60] for x in segs(r['quote'])[:1] for a in (30,len(x)//2) if len(x)>=a+60]
    for probe in probes:
        for fn,txt,starts,pages in cand(r['key']):
            i=txt.find(probe)
            if i>=0: found=(fn,i,starts,pages); break
        if found: break
    if not found: miss+=1; out[k]=None; continue
    fn,i,starts,pages=found; pg=bisect.bisect_right(starts,i)-1
    raw=re.sub(r'-\s*\n\s*(\w)',r'\1',pages[pg]); raw=re.sub(r'\s+',' ',raw)
    # locate approx position in raw page by the first words
    w=probe.split()[:4]; m=re.search(r'\W+'.join(map(re.escape,w)),raw,re.I)
    c=m.start() if m else len(raw)//2
    a=max(0,c-650); b=min(len(raw),c+len(str(r['quote']))+650)
    out[k]=dict(file=fn,pdf_page=pg+1,dropbox=dbx(fn),url=url(dbx(fn)),context=('…' if a>0 else '')+raw[a:b]+('…' if b<len(raw) else ''))
json.dump(out,open(f'{OUT}/quote_context.json','w'),ensure_ascii=False)
print('statements',len(out),'located',len(out)-miss,'not found',miss)
