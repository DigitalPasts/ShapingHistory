"""Helpers to read OHANE chapters with exact citations (used while scoring; see 81_literature_scores.py)."""
from _paths import LIT
import re, pandas as pd
P=pd.read_parquet(LIT+'/ohane/ohane_pages.parquet')
def cite(r): return f"OHANE {r.vol}, ch. {int(r.chapter)}, §{r.section}" + (f", p. {int(r.printed)}" if pd.notna(r.printed) else f" (PDF p. {r.pdf})")
def sections(vol,ch):
    g=P[(P.vol==vol)&(P.chapter==ch)]; out=[]
    for _,r in g.iterrows():
        for m in re.finditer(r'(?m)^\s*(%d\.\d{1,2}(?:\.\d{1,2})?)\.\s+(.+)$'%ch, r.text): out.append((m.group(1),m.group(2).strip()[:80],r.printed if pd.notna(r.printed) else r.pdf))
    return out
def text(vol,ch,sec_prefix=None,pages=None):
    g=P[(P.vol==vol)&(P.chapter==ch)]
    if sec_prefix: g=g[g.section.fillna('').str.match(re.escape(sec_prefix)+r'(\.|$)')]
    if pages: g=g[g.pdf.between(*pages)]
    return '\n'.join(f"[[{cite(r)}]]\n"+re.sub(r'\n{3,}','\n\n',r.text) for _,r in g.iterrows())
def grep(vol,ch,pat,w=350):
    g=P[(P.vol==vol)&(P.chapter==ch)]; out=[]
    for _,r in g.iterrows():
        t=re.sub(r'\s+',' ',r.text)
        for m in re.finditer(pat,t,flags=re.I): out.append(f"[{cite(r)}] …{t[max(0,m.start()-w):m.end()+w]}…")
    return out

PAT={'TERR':r'territor|hegemon|empire|imperial|provinc|vassal|conquer|unif',
     'HIER':r'governor|ensi|provincial|district|official|vizier|sukkal|šakkanakk|bēl pīḫ|satrap|appoint',
     'FISC':r'\btax|tribute|bala\b|levy|levies|ilk|corvée|extract|rent\b|tithe|gun2',
     'COMM':r'road|messeng|courier|station|letters? (were|was) sent|correspondence|relay',
     'PAL':r'palace|crown|royal household|royal estate|royal sector',
     'TEMP':r'temple',
     'PRIV':r'private|family archive|entrepreneur|merchant|household archive|house of',
     'BUR':r'bureaucr|administrat|accounting|bookkeeping|archive|record-?keeping|standardi',
     'SCHOOL':r'scrib|school|curricul|edubba|training|literacy',
     'LAW':r'\blaws?\b|edict|code|mīšar|misharum|court|judge|justice|verdict',
     'STD':r'weights? and measures|calendar|measure|standard|year names?|eponym|unit'}
def is_biblio(t):
    ls=[l for l in t.splitlines() if l.strip()]
    if not ls: return True
    b=sum(bool(re.search(r'\b(1[89]|20)\d\d[a-z]?\.\s',l)) for l in ls)
    return b/len(ls)>0.25
def digest(vol,ch,params=None,maxchars=2600,skip_notes=True):
    """Paragraph-level hits per page, labelled by parameter; bibliography pages skipped."""
    g=P[(P.vol==vol)&(P.chapter==ch)]; out=[]
    for _,r in g.iterrows():
        if is_biblio(r.text): continue
        t=r.text.replace('-\n','').replace('-\n','')
        paras=re.split(r'\n\s*\n|\n(?=\s{6,}\S)',t)
        for pa in paras:
            pa2=re.sub(r'\s+',' ',pa).strip()
            if len(pa2)<120: continue
            if skip_notes and re.match(r'^\d{1,3}\.\s',pa2): continue
            tags=[k for k,v in PAT.items() if (params is None or k in params) and re.search(v,pa2,re.I)]
            if tags: out.append(f"[{cite(r)}] <{','.join(tags)}> {pa2[:maxchars]}")
    return out

def tight(vol,ch,mintags=3,maxchars=1300,pages=None,must=None):
    """Smaller digest: paragraphs with >= mintags parameter tags (or matching `must`), citation-dense paragraphs dropped."""
    out=[]
    for x in digest(vol,ch,maxchars=maxchars):
        if len(re.findall(r'\d{4}[a-z]?:\s?\d',x))>3 or re.search(r'\]\s<[^>]*>\s*\d{1,3}\.\s',x): continue
        if pages:
            m=re.search(r'(?:p\.|PDF p\.) (\d+)',x)
            if m and not (pages[0]<=int(m.group(1))<=pages[1]): continue
        tags=x.split('<',1)[1].split('>',1)[0].split(',')
        if len(tags)>=mintags or (must and re.search(must,x,re.I)): out.append(x)
    return out
