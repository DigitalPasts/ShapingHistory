"""Scoring v2 (4 Nov 2026), after ShG's review of ED IIIa, ED IIIb and Ebla. Changes from v1 (85_build_scores.py):
 1. In-between scores. A statement may imply a half point (1.5 = between 1 and 2). The cell score is the WEIGHTED median of
    all statements on a half-point grid (ties take the midpoint), so a literature split between 1 and 2 gives 1.5 instead of
    being rounded down. The cell also gets a band (weighted 25th-75th percentile), shown as e.g. '1-2'.
 2. Weights follow ShG's confidence rubric. basis: assertion 0.25 (no evidence given, reconstruction), fragmentary 0.5,
    documented 1, substantial 1.5 (large numbers relative to what survives from that place and period). stance: supports 1,
    qualifies and contests 0.5. Statements whose basis was not yet read by hand get basis from a transparent text rule
    (hedged wording -> fragmentary; counts of texts or finds -> substantial; otherwise documented), flagged basis_src=auto.
 3. Archive bias. 84_archive_inventory.py lists each period's archives and the institution that kept them. A statement
    drawn from the period's dominant archive (share >= 0.5) about a parameter that archive inflates (e.g. PAL from a palace
    archive) is down-weighted x0.75. A score <= 0.5 for a parameter the dominant archive hides (e.g. TEMP or PRIV in a palace
    archive) is treated as absence of evidence: basis capped at fragmentary. Such cells are flagged and capped at M.
 4. Confidence (ShG 3 Nov): H = at least one 'substantial' statement and two independent works within half a point of the
    score, no statement of weight >= 0.5 a full point or more away (whatever its stance), not archive-flagged; M = at least one 'documented' or
    'substantial' statement; L = otherwise (only assertions or fragmentary evidence, or the earlier coding).
 5. Regional sub-entities: statements tagged with a region also give a regional score (e.g. ED IIIa north (Kiš) vs south).
    The period score uses all statements.
 6. ShG's verdicts (85a_shg_verdicts.py): rejected statements are dropped (listed in the output); rescored ones use his score.
Outputs: centralization/lit_scores_v2_long.csv, lit_scores_v2_wide.csv, lit_evidence_v2_long.csv."""
from _paths import SCRIPTS, SHARED, WORK
import runpy, glob, os, re, json, numpy as np, pandas as pd, importlib.util
S=SCRIPTS; OUT=WORK+'/centralization'; PJ=SHARED+'/centralization'
spec=importlib.util.spec_from_file_location('inv',f'{S}/84_archive_inventory.py'); inv=importlib.util.module_from_spec(spec); spec.loader.exec_module(inv)
PARAMS=['TERR','HIER','FISC','COMM','PAL','TEMP','TCTL','PRIV','BUR','SCHOOL','LAW','STD']
MAIN=['ED IIIa','ED IIIb','Ebla','Old Akkadian','Ur III','Early Old Babylonian','Old Babylonian','Old Assyrian',
      'Middle Babylonian','Middle Assyrian','Neo-Assyrian','Neo-Babylonian','Achaemenid','Hellenistic']
SI=['Hittite','Middle Elamite']
BW={'assertion':0.25,'fragmentary':0.5,'documented':1.0,'substantial':1.5}; SW={'supports':1.0,'qualifies':0.5,'contests':0.5}
rows=[]
for f in sorted(glob.glob(f'{S}/81_lit_evidence_*.py')):
    d=runpy.run_path(f); src=os.path.basename(f)
    for name in ['E','UR3','RIMSIN','ACH']:
        for e in d.get(name,[]):
            r=dict(e); r.setdefault('period',d.get('P')); r['file']=src; rows.append(r)
ev=pd.DataFrame(rows)
for c in ['note','region','basis','genre','archive']:
    if c not in ev: ev[c]=None
ev['basis_src']=np.where(ev.basis.notna(),'hand','auto')
# systematic pass (85c_basis_pass.py, 4 Nov 2026): every remaining statement read and coded by hand
if os.path.exists(f'{OUT}/basis_pass.csv'):
    BP=pd.read_csv(f'{OUT}/basis_pass.csv').set_index('sid')
    sid=ev.apply(lambda r:f"{r['period']}|{r['param']}|{r['key']}|{str(r['quote'])[:50]}",axis=1)
    for c in ['basis','genre','archive']:
        m=ev[c].isna() & sid.isin(BP.index); ev.loc[m,c]=sid[m].map(BP[c])
    ev.loc[(ev.basis_src=='auto') & sid.isin(BP.index),'basis_src']='read'
HEDGE=r'\b(may|might|perhaps|possibly|probably|seems?|appears?|apparently|suggests?|likely|speculat|presumabl|it is (not )?clear|unclear|uncertain|hypothe)'
COUNT=r'(\b\d{1,3}(,\d{3})+\b|\b\d{3,}\b|hundreds|thousands|dozens|the (vast|great) majority|large (number|quantit)|numerous)'
def autobasis(q):
    q=str(q)
    if re.search(HEDGE,q,re.I): return 'fragmentary'
    if re.search(COUNT,q,re.I): return 'substantial'
    return 'documented'
def autogenre(q):
    q=str(q)
    if re.search(r'inscription|propaganda|royal hymn|Šulgi B|Sulgi B|claims?|boast|annals|stela',q,re.I): return 'royal'
    if re.search(r'\bletters?\b|correspondence',q,re.I): return 'letters'
    if re.search(r'contract|sale|loan|lawsuit|court|legal',q,re.I): return 'legal'
    return 'mixed'
m=ev.basis.isna(); ev.loc[m,'basis']=ev.loc[m,'quote'].map(autobasis)
m=ev.genre.isna(); ev.loc[m,'genre']=ev.loc[m,'quote'].map(autogenre)
# ShG verdicts
V=pd.read_csv(f'{OUT}/shg_verdicts.csv')
ev['shg']=None; ev['shg_comment']=None; ev['qk']=ev.quote.astype(str).str[:50].str.strip()
for r in V.itertuples():
    i=ev.index[(ev.period==r.period)&(ev.param==r.param)&(ev.stance==r.stance)&(ev.qk==str(r.quote)[:50].strip())]
    for j in i:
        ev.at[j,'shg']=r.verdict; ev.at[j,'shg_comment']=r.comment if isinstance(r.comment,str) else None
        if pd.notna(r.rescore): ev.at[j,'score']=float(r.rescore); ev.at[j,'note']=(str(ev.at[j,'note'] or '')+f' [Rescored by ShG from {int(r.score_orig)} to {int(r.rescore)}.]').strip()
# ShG's second assessment on the desk (85d_shg_verdicts_8nov.py): rejects, rescores, comments, matched on period|param|key|quote[:50]
V2=pd.read_csv(f'{OUT}/shg_stm_9nov.csv')  # 85f: 8 Nov + 9 Nov verdicts
for r in V2.itertuples():
    i=ev.index[(ev.period==r.period)&(ev.param==r.param)&(ev.key==r.key)&(ev.qk==str(r.qk)[:50].strip())]
    for j in i:
        if r.verdict=='reject' or ev.at[j,'shg']!='reject': ev.at[j,'shg']=r.verdict
        if isinstance(r.comment,str) and r.comment: ev.at[j,'shg_comment']=r.comment
        if pd.notna(r.rescore) and float(r.rescore)!=float(ev.at[j,'score']):
            ev.at[j,'note']=(str(ev.at[j,'note'] or '')+f' [Rescored by ShG, 8 Nov, from {ev.at[j,"score"]:g} to {float(r.rescore):g}.]').strip(); ev.at[j,'score']=float(r.rescore)
# the same passage entered twice (from two reading rounds) counts once (ShG 8 Nov: Ebla TCTL, Archi 2015 p. 20)
dup=ev.duplicated(['period','param','key','quote'],keep='first'); print('duplicate passages dropped:',int(dup.sum())); ev=ev[~dup].copy()
rejected=ev[ev.shg=='reject'].copy(); ev=ev[ev.shg!='reject'].copy()
# Achaemenid (ShG 8 Nov): ONE period, as for other periods with regional differences; Babylonia / Persepolis (Fars) / other
# regions are regional sub-scores (column regions), not separate SI rows. Old per-region statements fold into the period.
m=ev.period.str.startswith('Achaemenid (',na=False)
ev.loc[m,'region']=ev.loc[m,'region'].fillna(ev.loc[m,'period'].str.extract(r'\((\w+)\)')[0]); ev.loc[m,'period']='Achaemenid'
dup=ev.duplicated(['period','param','key','quote'],keep='first'); ev=ev[~dup].copy()
evx=ev.copy()
# archive factor
def arch(r):
    dom=inv.dominant(r.period.split(' (')[0]) if isinstance(r.period,str) else None
    fac,flag,basis=1.0,'',r.basis
    if dom and dom['share']>=0.5:
        from_dom = isinstance(r.archive,str) and dom['archive'].split(' (')[0].split(',')[0] in r.archive
        if from_dom and r.param in inv.INFLATES[dom['kind']]: fac,flag=0.75,'inflated by dominant archive'
        if r.param in inv.HIDES[dom['kind']] and r.score<=0.5 and BW[basis]>0.5: basis,flag='fragmentary','absence of evidence in dominant archive'
    return pd.Series(dict(arch_factor=fac,arch_flag=flag,basis_eff=basis))
evx[['arch_factor','arch_flag','basis_eff']]=evx.apply(arch,axis=1)
evx['w']=evx.basis_eff.map(BW)*evx.stance.map(SW)*evx.arch_factor
def wq(vals,w,q):
    o=np.argsort(vals); v=np.asarray(vals,float)[o]; ww=np.asarray(w,float)[o]; c=np.cumsum(ww)/ww.sum()
    for k in range(len(v)):
        if abs(c[k]-q)<1e-9 and k+1<len(v): return (v[k]+v[k+1])/2
        if c[k]>q: return v[k]
    return v[-1]
def half(x): return float(np.floor(x*2+0.5)/2)
prior=pd.read_csv(f'{PJ}/centralization_scores_long.csv'); pr={(r.period,r.param):int(r.score) for r in prior.itertuples()}
for reg in ['Babylonia','Persepolis']:
    for p in PARAMS: pr.setdefault(('Achaemenid',p),pr.get((f'Achaemenid ({reg})',p)))
v1=pd.read_csv(f'{OUT}/lit_scores_long.csv'); v1s={(r.period,r.param):r.score for r in v1.itertuples()}
def cell(g,per,p):
    pt=half(wq(g.score,g.w,0.5)); lo=half(wq(g.score,g.w,0.25)); hi=half(wq(g.score,g.w,0.75))
    lo,hi=min(lo,pt),max(hi,pt)
    sup=g[g.stance=='supports']
    near=g[(g.stance!='contests')&((g.score-pt).abs()<=0.5)]
    far_contest=(((g.score-pt).abs()>=1)&(g.w>=0.5)).any()  # any well-founded statement a full point away
    dom=inv.dominant(per.split(' (')[0]); aflag=bool((g.arch_flag!='').any()) or bool(dom and dom['share']>=0.6 and (p in inv.INFLATES[dom['kind']] or p in inv.HIDES[dom['kind']]))
    if (g.basis_eff=='substantial').any() and near.key.nunique()>=2 and not far_contest: conf='H'
    elif g.basis_eff.isin(['documented','substantial']).any(): conf='M'
    else: conf='L'
    if aflag and conf=='H': conf='M'
    dist=np.zeros(7)
    for r in g.itertuples(): dist[int(round(r.score*2))]+=r.w
    return dict(score=pt,lo=lo,hi=hi,band=(f'{lo:g}' if lo==hi else f'{lo:g}-{hi:g}'),conf=conf,archive_flag=aflag,
                contested=bool(((g.stance=='contests')&((g.score-pt).abs()>=0.5)).any()),n_entries=len(g),n_works=g.key.nunique(),
                n_hand=int((g.basis_src=='hand').sum()),wsum=round(g.w.sum(),2),dist7=json.dumps([round(x/dist.sum(),3) for x in dist]))
out=[]
for per in MAIN+SI:
    for p in PARAMS:
        g=evx[(evx.period==per)&(evx.param==p)]
        if len(g): r=cell(g,per,p); r['source']='literature'
        else:
            pt=pr.get((per,p))
            if pt is None: continue
            r=dict(score=float(pt),lo=float(pt),hi=float(pt),band=str(pt),conf='L',archive_flag=False,contested=False,n_entries=0,n_works=0,n_hand=0,wsum=0,
                   dist7=json.dumps([0.25 if abs(k/2-pt)==0.5 else (0.5 if k/2==pt else 0) for k in range(7)]),source='prior')
        regs={}
        for reg,gr in g[g.region.notna()].groupby('region'):
            c=cell(gr,per,p); regs[reg]=c['band']
        r.update(period=per,param=p,v1=v1s.get((per,p)),prior=pr.get((per,p)),regions=json.dumps(regs,ensure_ascii=False) if regs else '')
        out.append(r)
sc=pd.DataFrame(out)
# ShG's cell adjudication (8 Nov). score = literature score (weighted median of quoted statements). score_final = what the
# analysis uses: ShG's own score where he changed it ('adjudicated'), else the literature score. 'pending' = ShG could not
# score without more citations; the literature score is kept and flagged. 'agreed' cells whose literature score has since
# moved (new statements) are flagged recheck for ShG.
C8=pd.read_csv(f'{OUT}/shg_cell_9nov.csv')  # 85f: 8 Nov + 9 Nov verdicts
sc=sc.merge(C8,on=['period','param'],how='left'); sc['status']=sc.status.fillna('not reviewed')
adj=sc.status.eq('adjudicated')&sc.shg_score.notna()
sc['score_final']=np.where(adj,sc.shg_score,sc.score)
sc['lo_final']=np.where(adj,sc.shg_lo.fillna(sc.shg_score),sc.lo); sc['hi_final']=np.where(adj,sc.shg_hi.fillna(sc.shg_score),sc.hi)
sc['conf_final']=np.where(adj&sc.shg_conf.fillna('').ne(''),sc.shg_conf,sc.conf)
sc['recheck']=(sc.status.eq('agreed')&sc.shown_score.notna()&(sc.score!=sc.shown_score))|(adj&((sc.score-sc.shg_score).abs()>=1))
wide=sc.pivot(index='period',columns='param',values='score_final')[PARAMS].reindex(MAIN+SI)
keep=['period','param','score','stance','key','where','quote','note','region','basis','basis_src','basis_eff','genre','archive','arch_flag','w','shg','shg_comment','file']
evx[keep].to_csv(f'{OUT}/lit_evidence_v2_long.csv',index=False); rejected[['period','param','score','stance','key','where','quote','note','shg_comment']].to_csv(f'{OUT}/lit_evidence_rejected.csv',index=False)
sc.to_csv(f'{OUT}/lit_scores_v2_long.csv',index=False); wide.to_csv(f'{OUT}/lit_scores_v2_wide.csv')
m=sc[sc.period.isin(MAIN)]
print('statements',len(ev),'works',ev.key.nunique(),'rejected',len(rejected),'hand-tagged basis',(ev.basis_src=='hand').sum())
print('conf v2',m.conf.value_counts().to_dict(),'half scores',(m.score%1!=0).sum(),'bands',(m.lo!=m.hi).sum(),'archive-flagged',m.archive_flag.sum())
ch=m[(m.v1.notna())&(m.score!=m.v1)]; print('changed vs v1:',len(ch))
print('status',m.status.value_counts().to_dict(),'recheck',int(m.recheck.sum()))
print(m[m.period=='Achaemenid'][['param','score','band','conf','regions','status','score_final']].to_string(index=False))
