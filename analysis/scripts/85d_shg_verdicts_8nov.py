"""ShG's second assessment (desk, 4-8 Nov 2026). The desk saved verdicts to its artifact database
(collections stmverdicts and cellverdicts); the export is kept in centralization/shg_stmverdicts_8nov.json and
shg_cellverdicts_8nov.json. This script flattens them for 85b:
  shg_stm_8nov.csv  one row per statement verdict (accept / reject, rescore, comment), keyed period|param|key|quote[:50]
  shg_cell_8nov.csv one row per cell: agree (score kept), change (ShG's own score, band, confidence), or blank (undecided:
                    'cannot score without more citations'), plus ShG's note and the score shown to him on the desk."""
from _paths import WORK
import json, pandas as pd
C=WORK+'/centralization'
S=[d['data'] for d in json.load(open(f'{C}/shg_stmverdicts_8nov.json'))]
rows=[]
for d in S:
    per,par,key,qk=d['sid'].split('|',3)
    rows.append(dict(period=per,param=par,key=key,qk=qk.strip(),verdict=d.get('v') or '',rescore=d.get('rescore'),comment=d.get('comment') or '',at=d.get('at')))
st=pd.DataFrame(rows); st['rescore']=pd.to_numeric(st.rescore,errors='coerce')
st.to_csv(f'{C}/shg_stm_8nov.csv',index=False)
shown=pd.read_csv(f'{C}/lit_scores_v2_before_8nov.csv').set_index(['period','param'])
R=[]
for d in [x['data'] for x in json.load(open(f'{C}/shg_cellverdicts_8nov.json'))]:
    a=d.get('agree') or ''
    status={'agree':'agreed','change':'adjudicated'}.get(a,'pending')
    k=(d['period'],d['param']); sh=shown.loc[k] if k in shown.index else None
    R.append(dict(period=d['period'],param=d['param'],status=status,shg_score=d.get('score'),shg_lo=d.get('lo'),shg_hi=d.get('hi'),
                  shg_conf=d.get('conf') or '',shg_note=(d.get('note') or '').strip(),
                  shown_score=None if sh is None else sh.score,shown_band=None if sh is None else sh.band,shown_conf=None if sh is None else sh.conf))
ce=pd.DataFrame(R); ce.to_csv(f'{C}/shg_cell_8nov.csv',index=False)
print(len(st),'statement verdicts:',st.verdict.value_counts().to_dict(),'rescored',st.rescore.notna().sum(),'comments',(st.comment!='').sum())
print(len(ce),'cells:',ce.status.value_counts().to_dict(),'notes',(ce.shg_note!='').sum())
