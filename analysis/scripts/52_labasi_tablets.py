"""LaBaSi (Late Babylonian Signs, ACDH Vienna): tablet records with scribe, archive, place, date and ductus,
from the public API (labasi.acdh.oeaw.ac.at/data/api/tablets/). Output: labasi/labasi_tablets.csv."""
from _paths import WORK
import json, subprocess, pandas as pd
import time
def fetch(x):
    for k in range(5):
        t=subprocess.run(["curl","-s","-L",x],capture_output=True,text=True).stdout
        try: return json.loads(t)
        except Exception: time.sleep(2+2*k)
    return {}
u='https://labasi.acdh.oeaw.ac.at/data/api/tablets/?format=json&limit=1000'; rows=[]; cache={}
def name(x):
    if x is None or (isinstance(x,float)) or x=='': return None
    if isinstance(x,dict): return x.get('name') or x.get('title') or x.get('label') or str(x)
    if x not in cache:
        d=fetch(x+('&' if '?' in x else '?')+'format=json')
        cache[x]=d.get('name') or d.get('title') or str(d)
    return cache[x]
while u:
    d=fetch(u); rows+=d['results']; u=d['next']
D=pd.DataFrame(rows)
for c in ['archive','place','scribe','period','text_type','region','dossier']: D[c]=D[c].map(name)
D.to_csv(WORK+'/labasi/labasi_tablets.csv',index=False); print(len(D))
print(D.place.value_counts().head(8)); print(D.archive.value_counts().head(8)); print((D.cdli_no!='').sum(), D.scribe.notna().sum())
