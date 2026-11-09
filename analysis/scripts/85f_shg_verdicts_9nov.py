"""ShG's third pass on the desk (night 8-9 Nov 2026). Export: centralization/shg_stmverdicts_9nov.json and
shg_cellverdicts_9nov.json (the 8 Nov export with every document written after it replaced by id). Same flattening as 85d:
  shg_stm_9nov.csv  one row per statement verdict
  shg_cell_9nov.csv one row per cell: agreed / adjudicated / pending, ShG's note, and the score shown when he decided.
Shown score: a cell decided after the round 3b desk went live (8 Nov 23:08 UTC) saw lit_scores_v2_before_9nov.csv;
earlier decisions keep the score shown in 85d. A cell ShG had agreed earlier counts as rechecked when he accepted the new
statements in it on 9 Nov and left the cell agreed (the desk writes no new cell document when 'agree' is clicked again)."""
from _paths import WORK
import json, pandas as pd
C=WORK+'/centralization'; LIVE='2026-11-08T23:08:00Z'
S=[d['data'] for d in json.load(open(f'{C}/shg_stmverdicts_9nov.json'))]
rows=[]
for d in S:
    per,par,key,qk=d['sid'].split('|',3)
    rows.append(dict(period=per,param=par,key=key,qk=qk.strip(),verdict=d.get('v') or '',rescore=d.get('rescore'),comment=d.get('comment') or '',at=d.get('at')))
st=pd.DataFrame(rows); st['rescore']=pd.to_numeric(st.rescore,errors='coerce')
st.to_csv(f'{C}/shg_stm_9nov.csv',index=False)
new=pd.read_csv(f'{C}/lit_scores_v2_before_9nov.csv').set_index(['period','param'])
old=pd.read_csv(f'{C}/shg_cell_8nov.csv').set_index(['period','param'])
touched9=set(map(tuple,st[st['at']>=LIVE][['period','param']].values))
R=[]
for d in [x['data'] for x in json.load(open(f'{C}/shg_cellverdicts_9nov.json'))]:
    a=d.get('agree') or ''; status={'agree':'agreed','change':'adjudicated'}.get(a,'pending'); k=(d['period'],d['param'])
    late=(d.get('at') or '')>=LIVE or (status=='agreed' and k in touched9)
    if late and k in new.index: sh=dict(shown_score=new.loc[k].score,shown_band=new.loc[k].band,shown_conf=new.loc[k].conf)
    elif k in old.index: sh=dict(shown_score=old.loc[k].shown_score,shown_band=old.loc[k].shown_band,shown_conf=old.loc[k].shown_conf)
    else: sh=dict(shown_score=None,shown_band=None,shown_conf=None)
    R.append(dict(period=d['period'],param=d['param'],status=status,shg_score=d.get('score'),shg_lo=d.get('lo'),shg_hi=d.get('hi'),
                  shg_conf=d.get('conf') or '',shg_note=(d.get('note') or '').strip(),decided=d.get('at'),seen9=late,**sh))
ce=pd.DataFrame(R); ce.to_csv(f'{C}/shg_cell_9nov.csv',index=False)
print(len(st),'statement verdicts:',st.verdict.value_counts().to_dict(),'| on 9 Nov:',int((st['at']>=LIVE).sum()))
print(len(ce),'cells:',ce.status.value_counts().to_dict(),'| seen on 9 Nov:',int(ce.seen9.sum()))
