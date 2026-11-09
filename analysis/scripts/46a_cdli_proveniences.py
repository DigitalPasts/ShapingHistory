"""Collect CDLI proveniences (id, name, location id) and coordinates of selected locations from the CDLI API."""
from _paths import WORK
import json, urllib.request, pandas as pd, sys
B='https://cdli.earth'
def get(u):
    r=urllib.request.Request(u,headers={'Accept':'application/json'}); return json.load(urllib.request.urlopen(r,timeout=60))
rows=[]; page=1
while True:
    d=get(f'{B}/proveniences.json?page={page}&limit=100')
    if not d: break
    rows+= [dict(id=x['id'],provenience=x['provenience'],location_id=x.get('location_id')) for x in d]
    if len(d)<100: break
    page+=1
P=pd.DataFrame(rows); P.to_csv(WORK+'/geo/cdli_proveniences.csv',index=False); print(len(P), P.location_id.notna().sum())
