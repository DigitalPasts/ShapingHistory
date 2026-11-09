"""Build the one-page assessment desk (HTML) for ShG: rewritten codebook, every cell with its statements in context,
links to the PDFs, archive inventory, regional sub-scores, KeiBi candidates, and verdict controls (saved by the page).
Input: outputs of 84, 85a, 85b, 93, 95; text of 92 (parameter definitions). Output: assess/assessment_desk.html"""
from _paths import REPO, TEMPLATES, WORK
import json, re, runpy, os, collections, math, pandas as pd, numpy as np, html, importlib.util, sys
R=WORK; C=f'{R}/centralization'
sys.path.insert(0,f'{R}/assess'); import period_notes as PN, responses_8nov as RS
P92=runpy.run_path(f'{R}/scripts/92_si_codebook.py',run_name='lib')['P']
cb=pd.read_csv(f'{R}/centralization_codebook.csv').set_index('param')
sc=pd.read_csv(f'{C}/lit_scores_v2_long.csv'); ev=pd.read_csv(f'{C}/lit_evidence_v2_long.csv'); rej=pd.read_csv(f'{C}/lit_evidence_rejected.csv')
ctx=json.load(open(f'{C}/quote_context.json')); inv=pd.read_csv(f'{C}/archive_inventory.csv'); shg=pd.read_csv(f'{C}/shg_cell_reading.csv')
PARAMS=['TERR','HIER','FISC','COMM','PAL','TEMP','TCTL','PRIV','BUR','SCHOOL','LAW','STD']
MAIN=['ED IIIa','ED IIIb','Ebla','Old Akkadian','Ur III','Early Old Babylonian','Old Babylonian','Old Assyrian','Middle Babylonian','Middle Assyrian','Neo-Assyrian','Neo-Babylonian','Achaemenid','Hellenistic']
SI=['Hittite','Middle Elamite']  # the two Achaemenid sub-periods were merged into Achaemenid (8 Nov)
# author-year labels from the bib files
bib=''
for f in [f'{C}/lit_centralization.bib',f'{C}/lit_extra.bib',REPO+'/paper/Library300326.bib',f'{C}/codebook_theory.bib']:
    if os.path.exists(f): bib+=open(f,errors='ignore').read()+'\n'
LAB={}
for m in re.finditer(r'@\w+\{([^,\s]+),(.*?)\n\}',bib,re.S):
    k,b=m.group(1),m.group(2)
    if k in LAB: continue
    a=re.search(r'\bauthor\s*=\s*\{(.+?)\},?\n',b) or re.search(r'\beditor\s*=\s*\{(.+?)\},?\n',b); y=re.search(r'\byear\s*=\s*\{?(\d{4})',b)
    if not a: continue
    names=[n.split(',')[0].strip(' {}') for n in re.split(r'\s+and\s+',a.group(1))]
    names=[re.sub(r'[{}\\]','',n) for n in names]
    lab=names[0] if len(names)==1 else (f'{names[0]} & {names[1]}' if len(names)==2 else f'{names[0]} et al.')
    LAB[k]=f"{lab} {y.group(1) if y else ''}".strip()
def label(k):
    if k in LAB: return LAB[k]
    m=re.match(r'([a-z]+)[A-Z].*?(\d{4})$',str(k)); return f"{m.group(1).capitalize()} {m.group(2)}" if m else str(k)
def sid(r): return f"{r['period']}|{r['param']}|{r['key']}|{str(r['quote'])[:50]}"
B8=pd.read_csv(f'{C}/lit_evidence_v2_before_8nov.csv'); OLD8=set(B8.apply(sid,axis=1))
def newflag(r):
    if str(r['file']).startswith('81_lit_evidence_v5'): return '9 Nov'
    if sid(r) not in OLD8: return '8 Nov'
    return '4 Nov' if str(r['file']).startswith('81_lit_evidence_v3') else ''
# ShG's 8 Nov statement comments (desk round 2) and my replies
S8=pd.read_csv(f'{C}/shg_stm_8nov.csv'); S8C={}
for x in S8.itertuples():
    if isinstance(x.comment,str) and x.comment.strip(): S8C[(x.period,x.param,x.key,str(x.qk)[:40])]=x.comment.strip()
# field literature per cell (97_bibliometrics.py: KeiBi 57-82 and eBL)
BC=pd.read_csv(f'{C}/biblio/cells.csv'); BU=pd.read_csv(f'{C}/biblio/unread.csv'); BP=pd.read_csv(f'{C}/biblio/periods.csv')
BS=json.load(open(f'{C}/biblio/summary.json'))
KB={}; KBN=dict(zip(BP.period,BP.works))
for r in BC.itertuples():
    u=BU[(BU.period==r.period)&(BU.param==r.param)]
    KB[f'{r.period}|{r.param}']=dict(n=int(r.works),s10=int(r.since2010),rv=int(r.reviews),top=None if pd.isna(r.top_authors) else r.top_authors,
        cov=int(r.top10_cited),covn=int(r.top10_n),ours=int(r.ours),
        items=[dict(t=re.sub(r'<[^>]+>','',str(x.title)),a=x.authors,y=None if pd.isna(x.year) else int(x.year),id=x.id,rv=int(x.reviews)) for x in u.itertuples()])
BIB=dict(periods=json.loads(BP.to_json(orient='records')),summary={k:v for k,v in BS.items() if k!='unmatched_keys'})
# scores before this round (4 Nov morning), for the change table
PREV=pd.read_csv('/tmp/claude-0/-home-user-ShapingHistory/02e98270-7c91-5b75-ba56-028bd738e74e/scratchpad/scores_before.csv') if os.path.exists('/tmp/claude-0/-home-user-ShapingHistory/02e98270-7c91-5b75-ba56-028bd738e74e/scratchpad/scores_before.csv') else pd.read_csv(f'{C}/lit_scores_v2_before_4nov.csv')
PREV.to_csv(f'{C}/lit_scores_v2_before_4nov.csv',index=False)
PV={f'{r.period}|{r.param}':(r.score,r.band,r.conf) for r in PREV.itertuples()}
cells={}
for r in sc.itertuples():
    k=f'{r.period}|{r.param}'
    s=shg[(shg.period==r.period)&(shg.param==r.param)]
    pv=PV.get(k)
    cells[k]=dict(prev=None if pv is None else dict(s=float(pv[0]),b=str(pv[1]),c=str(pv[2])),score=r.score,lo=r.lo,hi=r.hi,band=r.band,conf=r.conf,af=bool(r.archive_flag),contested=bool(r.contested),n=int(r.n_entries),nw=int(r.n_works),
                  v1=None if pd.isna(r.v1) else float(r.v1),src=r.source,reg=json.loads(r.regions) if isinstance(r.regions,str) and r.regions else {},
                  shg=(None if s.empty else {kk:(None if pd.isna(v) else v) for kk,v in s.iloc[0][['your_score','status','conf','source_to_add','comment']].to_dict().items()}),
                  r8=dict(status=r.status,shg=None if pd.isna(r.shg_score) else float(r.shg_score),note=None if pd.isna(r.shg_note) else str(r.shg_note),
                          shown=None if pd.isna(r.shown_score) else float(r.shown_score),shown_band=None if pd.isna(r.shown_band) else str(r.shown_band),
                          fin=None if pd.isna(r.score_final) else float(r.score_final),fin_conf=None if pd.isna(r.conf_final) else str(r.conf_final),
                          rc=bool(r.recheck),ans=RS.R.get((r.period,r.param))))
stm=collections.defaultdict(list)
for _,r in ev.iterrows():
    c=ctx.get(sid(r)) or {}
    stm[f"{r['period']}|{r['param']}"].append(dict(id=sid(r),s=r['score'],st=r['stance'],k=r['key'],lab=label(r['key']),w=str(r['where']),q=str(r['quote']),
        n=None if pd.isna(r['note']) else str(r['note']),reg=None if pd.isna(r['region']) else r['region'],b=r['basis_eff'],bs=r['basis_src'],g=r['genre'],
        ar=None if pd.isna(r['archive']) else r['archive'],af=None if pd.isna(r['arch_flag']) else r['arch_flag'],wt=round(r['w'],2),
        pv=None if pd.isna(r['shg']) else r['shg'],pc=None if pd.isna(r['shg_comment']) else r['shg_comment'],
        url=c.get('url'),pg=c.get('pdf_page'),cx=c.get('context'),fn=c.get('file'),nw=newflag(r)))
    q8=S8C.get((r['period'],r['param'],r['key'],str(r['quote'])[:40]))
    if q8: stm[f"{r['period']}|{r['param']}"][-1].update(c8=q8,a8=RS.STM.get((r['period'],r['param'])))
for v in stm.values(): v.sort(key=lambda x:(-{'supports':2,'qualifies':1,'contests':0}[x['st']],-x['wt']))
rejl=collections.defaultdict(list)
for _,r in rej.iterrows(): rejl[f"{r['period']}|{r['param']}"].append(dict(lab=label(r['key']),w=str(r['where']),q=str(r['quote'])[:400],s=r['score'],c=None if pd.isna(r['shg_comment']) else r['shg_comment']))
params={}
for p in PARAMS:
    d=P92[p]; params[p]=dict(name=cb.loc[p,'name'],dim=cb.loc[p,'dimension'],anchors=[a.strip() for a in cb.loc[p,'anchors'].split('|')],
        what=d['what'],why=d['why'],origin=d['origin'],tests=d['tests'],rules=d['rules'],cross=d.get('cross',''),framework=cb.loc[p,'framework'])
periods=[]
for p in MAIN+SI:
    base=p.split(' (')[0]; nt=PN.NOTES.get(p) or PN.NOTES.get(base) or {}
    iv=inv[inv.period==base][['archive','kind','share','key','where']].to_dict('records')
    for x in iv: x['lab']=label(x['key']) if isinstance(x['key'],str) else ''; x['key']=None if not isinstance(x['key'],str) else x['key']
    sites=[dict(n=s,r=reg,lat=PN.COORD[s][0],lon=PN.COORD[s][1]) for s,reg in (nt.get('sites') or {}).items() if s in PN.COORD]
    periods.append(dict(name=p,group='main' if p in MAIN else 'SI',span=nt.get('span',''),text=nt.get('text',''),regions=nt.get('regions',[]),inv=iv,sites=sites,route=nt.get('route',[]),pad=nt.get('pad',[]),kbn=KBN.get(p)))
DATA=dict(bib=BIB,params=params,periods=periods,cells=cells,stm=stm,rej=rejl,kb=KB,rivers=PN.RIVERS,gulf=PN.GULF,
          stats=dict(statements=int(len(ev[ev.period.isin(MAIN)])),works=int(ev.key.nunique()),hand=int((ev.basis_src=='hand').sum()),readpass=int((ev.basis_src=='read').sum()),auto=int((ev.basis_src=='auto').sum()),new=int(ev.file.astype(str).str.startswith('81_lit_evidence_v3').sum()),new8=int(((~ev.apply(sid,axis=1).isin(OLD8))&~ev.file.astype(str).str.startswith('81_lit_evidence_v5')).sum()),new9=int(ev.file.astype(str).str.startswith('81_lit_evidence_v5').sum()),works9=int(ev[ev.file.astype(str).str.startswith('81_lit_evidence_v5')].key.nunique()),notes8=int(sc.shg_note.notna().sum()),recheck=int(sc.recheck.sum()),adjud=int((sc.status=='adjudicated').sum()),pending=int((sc.status=='pending').sum()),rej8=int((S8.verdict=='reject').sum()),located=sum(1 for v in ctx.values() if v),rejected=int(len(rej))))

# archives and known tablet collections per period (84b; ShG 9 Nov)
AO=pd.read_csv(f'{C}/archive_overview.csv'); AN=pd.read_csv(f'{C}/archive_period_notes.csv').set_index('period').summary.to_dict()
AC=pd.read_csv(f'{C}/archive_sample_compare.csv'); AD=pd.read_csv(f'{C}/archive_dispersal.csv').set_index('period')
arch=[]
for p in MAIN+SI:
    g=AO[AO.period==p]; c=AC[AC.period==p].drop_duplicates('site').set_index('site'); ents=[]; seen=set()
    for r in g.itertuples():
        cs=c.loc[r.site] if (isinstance(r.sample_site,str) and r.site in c.index and r.site not in seen) else None
        if cs is not None: seen.add(r.site)
        st=lambda v: v if isinstance(v,str) else ''
        ents.append(dict(a=r.archive,s=st(r.site),k=st(r.kind),n=None if pd.isna(r.n) else int(r.n),sp=st(r.span),g=st(r.genres),lab=label(r.key),key=r.key,w=r.where,q=r.quote,nt=st(r.note),loc=bool(r.located),
            ls=None if cs is None else float(cs.lit_share),ss=None if cs is None or pd.isna(cs.sample_share) else float(cs.sample_share),sn=None if cs is None else int(cs.sample_n)))
    dd={k:(v.item() if hasattr(v,'item') else v) for k,v in AD.loc[p].to_dict().items()} if p in AD.index else None
    arch.append(dict(p=p,sum=AN.get(p,''),e=ents,d=dd,works=int(g.key.nunique())))
DATA['arch']=arch
DATA['stats']['arch_entries']=int(len(AO)); DATA['stats']['arch_works']=int(AO.key.nunique())
js=json.dumps(DATA,ensure_ascii=False).replace('</','<\\/').replace('\ufffd','[?]')
tpl=open(f'{TEMPLATES}/desk_template.html').read()
codebook=open(f'{R}/assess/codebook_body.html').read()
out=tpl.replace('/*__DATA__*/',js).replace('<!--__CODEBOOK__-->',codebook)
open(f'{R}/assess/assessment_desk.html','w').write(out); print('written',len(out)//1024,'KB','statements',len(ev),'cells',len(cells))
