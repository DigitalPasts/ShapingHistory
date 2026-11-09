"""Build literature-grounded centralization scores from the evidence files 81_lit_evidence_*.py.

Rules (stated in the SI, applied mechanically here):
 1. Each evidence entry is one published statement: period, parameter, the score it implies (0-3), its stance
    ('supports', 'qualifies' = accepts the institution but limits its reach, 'contests' = argues against), a verbatim
    quotation and an exact citation.
 2. Point score = median of the scores implied by 'supports' entries, rounded down at .5 (the conservative choice).
    If a cell has no 'supports' entry, the median of all entries is used and confidence is set to L.
 3. Range = min and max over all entries of the cell, whatever their stance.
 4. Contested = the cell has a 'contests' entry whose score differs from the point score.
 5. Confidence: H = at least two supporting statements, no contesting statement, range width 0;
    M = at least one supporting statement and range width <= 1; L = otherwise.
 6. Cells with no literature entry keep the earlier coding (centralization_scores_long.csv), flagged source='prior'
    and confidence L, and are listed as gaps.
 7. For uncertainty propagation, each cell gets a discrete distribution over 0-3: weight 1 for each supporting
    statement, 0.5 for each qualifying or contesting one, placed on the score each implies; prior-only cells get
    weight 1 on the prior score and 0.5 on each neighbour. Script 86 resamples from these.
Main analysis: 14 periods (Achaemenid merged). SI: Achaemenid split by region, Hittite, Middle Elamite."""
from _paths import SCRIPTS, SHARED, WORK
import runpy, glob, os, json, numpy as np, pandas as pd
S=SCRIPTS; OUT=WORK+'/centralization'; PJ=SHARED+'/centralization'
PARAMS=['TERR','HIER','FISC','COMM','PAL','TEMP','TCTL','PRIV','BUR','SCHOOL','LAW','STD']
MAIN=['ED IIIa','ED IIIb','Ebla','Old Akkadian','Ur III','Early Old Babylonian','Old Babylonian','Old Assyrian',
      'Middle Babylonian','Middle Assyrian','Neo-Assyrian','Neo-Babylonian','Achaemenid','Hellenistic']
SI=['Achaemenid (Babylonia)','Achaemenid (Persepolis)','Hittite','Middle Elamite']
rows=[]; gaps={}
for f in sorted(glob.glob(f'{S}/81_lit_evidence_*.py')):
    d=runpy.run_path(f); src=os.path.basename(f)
    for name in ['E','UR3','RIMSIN','ACH']:
        for e in d.get(name,[]):
            r=dict(e); r.setdefault('period',d.get('P')); r['file']=src; rows.append(r)
    for k,v in d.get('GAPS',{}).items(): gaps.setdefault(d.get('P','SI'),{})[k]=v
ev=pd.DataFrame(rows); ev['period']=ev['period'].replace({'Old Babylonian':'Old Babylonian'})
for c in ['note','region']:
    if c not in ev: ev[c]=None
assert ev.param.isin(PARAMS).all() and ev.score.between(0,3).all() and ev.stance.isin(['supports','qualifies','contests']).all()
# SI split of Achaemenid: regional statements go to their region, general ones to both
ach=ev[ev.period=='Achaemenid']
split=[]
for reg in ['Babylonia','Persepolis']:
    a=ach[ach.region.isna()|(ach.region==reg)].copy(); a['period']=f'Achaemenid ({reg})'; split.append(a)
evx=pd.concat([ev]+split,ignore_index=True)
prior=pd.read_csv(f'{PJ}/centralization_scores_long.csv')
pr={(r.period,r.param):int(r.score) for r in prior.itertuples()}
for reg in ['Babylonia','Persepolis']:
    for p in PARAMS: pr.setdefault(('Achaemenid',p),pr.get((f'Achaemenid ({reg})',p)))
def lowmed(x):
    x=sorted(x); n=len(x); return x[(n-1)//2] if n%2 else int(np.floor((x[n//2-1]+x[n//2])/2))
out=[]
for per in MAIN+SI:
    for p in PARAMS:
        g=evx[(evx.period==per)&(evx.param==p)]; sup=g[g.stance=='supports']
        dist=np.zeros(4)
        if len(g):
            pt=lowmed(sup.score.tolist()) if len(sup) else lowmed(g.score.tolist())
            lo,hi=int(g.score.min()),int(g.score.max())
            cont=bool(((g.stance=='contests')&(g.score!=pt)).any())
            if len(sup)>=2 and not (g.stance=='contests').any() and hi==lo: conf='H'
            elif len(sup)>=1 and hi-lo<=1: conf='M'
            else: conf='L'
            for r in g.itertuples(): dist[int(r.score)]+=1.0 if r.stance=='supports' else 0.5
            src='literature'
        else:
            pt=pr.get((per,p)); lo=hi=pt; cont=False; conf='L'; src='prior'
            if pt is None: continue
            dist[pt]+=1; 
            if pt>0: dist[pt-1]+=0.5
            if pt<3: dist[pt+1]+=0.5
        dist=dist/dist.sum()
        out.append(dict(period=per,param=p,score=int(pt),lo=lo,hi=hi,contested=cont,conf=conf,source=src,
                        n_entries=len(g),n_support=len(sup),n_sources=g.key.nunique() if len(g) else 0,
                        prior=pr.get((per,p)),dist=json.dumps([round(v,3) for v in dist])))
sc=pd.DataFrame(out)
wide=sc.pivot(index='period',columns='param',values='score')[PARAMS].reindex(MAIN+SI)
ev.drop(columns=[c for c in ev.columns if c=='file']).to_csv(f'{OUT}/lit_evidence_long.csv',index=False)
sc.to_csv(f'{OUT}/lit_scores_long.csv',index=False); wide.to_csv(f'{OUT}/lit_scores_wide.csv')
json.dump(gaps,open(f'{OUT}/lit_gaps.json','w'),ensure_ascii=False,indent=1)
m=sc[sc.period.isin(MAIN)]
print('entries',len(ev),'sources',ev.key.nunique())
print('main cells',len(m),'literature-grounded',(m.source=='literature').sum(),'contested',m.contested.sum(),
      'conf',m.conf.value_counts().to_dict())
ch=m[(m.source=='literature')&(m.score!=m.prior)]
print('changed vs prior coding:',len(ch)); print(ch[['period','param','prior','score','lo','hi','contested','conf']].to_string(index=False))
print(wide.to_string())
