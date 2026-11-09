"""ShG's note of 9 Nov 2026: metadata for our photographed tablets from the electronic Babylonian Library (eBL,
www.ebl.lmu.de, LMU Munich), through its public API. The eBL fragment number comes from CDLI's own external-resource
links (artifacts.csv, column external_resources = 'eBL'). Keeps: script period, genres, date (king, year, eponym),
dates in the text, excavation site and findspot, length/width/thickness, collection, dossiers and other numbers.
Usage: python3 37d_ebl_metadata.py <worker> <n_workers>   (writes ebl/ebl_<worker>.jsonl, resumable);
       python3 37d_ebl_metadata.py merge                   (writes ebl/ebl_metadata.csv)."""
from _paths import WORK
import json, os, sys, time, requests, pandas as pd
R=WORK; API='https://www.ebl.lmu.de/api/fragments/'
KEEP=['museumNumber','collection','museum','script','legacyScript','genres','date','datesInText','archaeology','width','length',
      'thickness','externalNumbers','dossiers','projects','accession','acquisitions']
if sys.argv[1]=='merge':
    rows=[]
    for f in sorted(os.listdir(f'{R}/ebl')):
        if f.startswith('ebl_') and f.endswith('.jsonl'):
            for line in open(f'{R}/ebl/{f}'): rows.append(json.loads(line))
    D=pd.json_normalize(rows); D.to_csv(f'{R}/ebl/ebl_metadata.csv',index=False); print(len(D),'rows', D.shape[1],'columns'); sys.exit()
w,n=int(sys.argv[1]),int(sys.argv[2])
E=pd.read_csv(f'{R}/turning/cdli_external_resources.csv'); E=E[E.res=='eBL'].drop_duplicates('id')
E['na']=(E.period=='Neo-Assyrian').astype(int); E=E.sort_values(['na','id'])   # Neo-Assyrian last: other periods need dates most
E=E.iloc[w::n]; out=f'{R}/ebl/ebl_{w}.jsonl'
done=set()
for f_ in os.listdir(f'{R}/ebl'):
    if f_.endswith('.jsonl'): done|={json.loads(l)['cdli_id'] for l in open(f'{R}/ebl/{f_}') if l.strip()}
S=requests.Session(); S.headers['User-Agent']='shaping-history-research (CDLI tablet metadata)'
f=open(out,'a'); k=0
for r in E.itertuples():
    if r.id in done: continue
    for attempt in range(4):
        try:
            x=S.get(API+requests.utils.quote(str(r.key),safe=''),timeout=60)
            if x.status_code==200:
                j=x.json(); rec={'cdli_id':int(r.id),'period_cdli':r.period,'ebl_key':r.key,'status':200}
                rec.update({k_:j.get(k_) for k_ in KEEP}); break
            rec={'cdli_id':int(r.id),'period_cdli':r.period,'ebl_key':r.key,'status':x.status_code}
            if x.status_code in (404,400): break
        except Exception as e: rec={'cdli_id':int(r.id),'period_cdli':r.period,'ebl_key':r.key,'status':'error'}
        time.sleep(5*(attempt+1))
    f.write(json.dumps(rec,ensure_ascii=False)+'\n'); k+=1
    if k%500==0: f.flush(); print(w,k,flush=True)
    time.sleep(0.3)
f.close(); print('worker',w,'done',k)
