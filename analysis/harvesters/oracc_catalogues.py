"""Download the Oracc catalogues that carry dates, findspots and archives for archival tablets, and save them as one CSV.
Run on your own computer (Oracc does not answer from the cloud machine):   python3 oracc_catalogues.py
Needs only Python 3 (no extra packages). Writes oracc_catalogues.csv next to this script; upload that file to the project.
Projects: tcma (Middle Assyrian archival texts, now ATMAP), atae (Archival Texts of the Assyrian Empire, all sub-projects),
saao (State Archives of Assyria online, all volumes), hbtin (Hellenistic Babylonia: texts), cams (Corpus of Ancient
Mesopotamian Scholarship: Late Babylonian Uruk and Babylon tablets), aemw (Amarna and other Akkadian of the Mediterranean
world, incl. aemw/amarna), balt (Babylonian Administrative and Legal Texts, Neo-Babylonian, with NaBuCCo metadata)."""
import urllib.request, zipfile, io, json, csv, os, sys, time
WANT=('tcma','atae','saao','hbtin','cams','aemw','balt')
BASES=('https://oracc.museum.upenn.edu','https://build-oracc.museum.upenn.edu','http://oracc.museum.upenn.edu')
HERE=os.path.dirname(os.path.abspath(__file__))
def get(path):
    for b in BASES:
        try:
            with urllib.request.urlopen(urllib.request.Request(b+path,headers={'User-Agent':'shaping-history-research'}),timeout=120) as r:
                return r.read()
        except Exception as e:
            last=e
    print('  could not fetch',path,'-',last); return None
def projects():
    raw=get('/projects.json'); names=set(WANT)
    if raw:
        try:
            pj=json.loads(raw); ids=pj.get('public',pj) if isinstance(pj,dict) else pj
            for p in ids:
                p=p if isinstance(p,str) else p.get('pathname','')
                if p.split('/')[0] in WANT: names.add(p)
        except Exception as e: print('projects.json not readable:',e)
    return sorted(names)
rows=[]; keys=set()
for p in projects():
    z=get('/json/'+p.replace('/','-')+'.zip'); time.sleep(1)
    if not z: continue
    try: zf=zipfile.ZipFile(io.BytesIO(z))
    except zipfile.BadZipFile: print('  not a zip:',p); continue
    n0=len(rows)
    for name in zf.namelist():
        if not name.endswith('catalogue.json'): continue
        cat=json.loads(zf.read(name)); proj=cat.get('project',name.rsplit('/',1)[0])
        for tid,m in (cat.get('members') or {}).items():
            r={'oracc_project':proj,'id_text':tid}
            for k,v in m.items(): r[k]=json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v
            rows.append(r); keys|=set(r)
    print(f'{p}: {len(rows)-n0} catalogue entries')
seen={}; 
for r in rows: seen[(r['oracc_project'],r['id_text'])]=r
rows=list(seen.values())
first=['oracc_project','id_text','designation','museum_no','period','provenience','genre','subgenre','date_of_origin','dates_referenced','archive']
cols=[c for c in first if c in keys]+sorted(keys-set(first))
out=os.path.join(HERE,'oracc_catalogues.csv')
with open(out,'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
print(f'\nwrote {out}: {len(rows)} entries, {len(cols)} columns')
