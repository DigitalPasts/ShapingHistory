"""Read ShG's assessment worksheet (uploaded 3 Nov 2026) and store his verdicts so the scoring can apply them:
Evidence sheet K = accept / reject, L = comment, D = score implied (a changed D is a rescore); Assess sheet P-T = his
reading of each cell (score, status, confidence, source to add, comment). Output: centralization/shg_verdicts.csv and
centralization/shg_cell_reading.csv."""
from _paths import SCRIPTS, WORK
import openpyxl, pandas as pd, runpy, glob, os
W='/tmp/claude-0/shg/ws.xlsx'; OUT=WORK+'/centralization'; S=SCRIPTS
wb=openpyxl.load_workbook(W)
ev=wb['Evidence']; rows=[]
for r in range(2,ev.max_row+1):
    v=[ev.cell(r,c).value for c in range(1,13)]
    if not v[1]: continue
    if v[10] is None and v[11] is None: continue
    rows.append(dict(row=r,period=v[1],param=v[2],score_ws=v[3],stance=v[4],source=v[5],where=v[6],quote=str(v[7] or ''),
                     verdict=(v[10] or '').strip().lower(),comment=v[11]))
V=pd.DataFrame(rows)
# original scores, to detect rescoring
orig=[]
for f in sorted(glob.glob(f'{S}/81_lit_evidence_*.py')):
    if 'v2_' in f: continue
    d=runpy.run_path(f)
    for name in ['E','UR3','RIMSIN','ACH']:
        for e in d.get(name,[]):
            e=dict(e); e.setdefault('period',d.get('P')); orig.append(e)
O=pd.DataFrame(orig)
def match(r):
    g=O[(O.period==r.period)&(O.param==r.param)&(O.stance==r.stance)]
    g=g[g.quote.str[:50].str.strip()==r.quote[:50].strip()] if len(g)>1 else g
    return (int(g.iloc[0].score), g.iloc[0].key, g.iloc[0].where, g.iloc[0].quote) if len(g) else (None,None,None,None)
m=V.apply(match,axis=1,result_type='expand'); V[['score_orig','key','where_full','quote_full']]=m
V['rescore']=V.apply(lambda r: r.score_ws if r.score_orig is not None and r.score_ws!=r.score_orig else None,axis=1)
V.to_csv(f'{OUT}/shg_verdicts.csv',index=False)
a=wb['Assess']; hdr=[c.value for c in a[1]]; R=[]
for r in range(2,a.max_row+1):
    v=[a.cell(r,c).value for c in range(1,21)]
    if any(v[15:20]): R.append(dict(period=v[2],param=v[3],your_score=v[15],status=v[16],conf=v[17],source_to_add=v[18],comment=v[19],row=r))
C=pd.DataFrame(R); C.to_csv(f'{OUT}/shg_cell_reading.csv',index=False)
print(len(V),'evidence verdicts;',(V.verdict=='reject').sum(),'rejected;',V.rescore.notna().sum(),'rescored;',V.key.isna().sum(),'unmatched')
print(len(C),'cell readings'); print(hdr[:6])
