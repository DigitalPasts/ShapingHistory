"""Bibliometric screen of the KeiBi bibliography (vergil.uni-tuebingen.de/keibi, public VuFind search, RSS view).
For each period, harvest every KeiBi title that matches the period's search terms, then tag titles by parameter with
multilingual title keyword lists. Output: keibi/titles_<period>.json and keibi/screen.csv (period x parameter counts).
Polite: one request per 1.2 s. Rerun-safe (cached RSS pages)."""
from _paths import WORK
import os, re, time, json, html, subprocess, urllib.parse, collections, sys
import pandas as pd
OUT=WORK+'/centralization/keibi'; os.makedirs(f'{OUT}/cache',exist_ok=True)
Q={
 'ED IIIa':['Fara','Šuruppak','Shuruppak','Abu Salabikh','Early Dynastic','Kengir'],
 'ED IIIb':['Lagaš','Lagash','Girsu','Presargonic','Pre-Sargonic','Early Dynastic','Umma','Adab','Uruinimgina','Urukagina'],
 'Ebla':['Ebla','Eblaite'],
 'Old Akkadian':['Sargonic','Old Akkadian','Sargon','Naram-Sin','Narām-Sîn','Akkade'],
 'Ur III':['Ur III','Neo-Sumerian','Šulgi','Shulgi','Drehem','Puzriš-Dagan','Ur-Namma'],
 'Early Old Babylonian':['Isin','Larsa','Ešnunna','Eshnunna','Isin-Larsa','Rim-Sin','Rīm-Sîn','Lipit-Ištar'],
 'Old Babylonian':['Old Babylonian','Hammurabi','Ḫammurabi','Samsuiluna','Sippar','Mari'],
 'Old Assyrian':['Old Assyrian','Kaniš','Kanesh','Kültepe'],
 'Middle Babylonian':['Kassite','Middle Babylonian','Kassites'],
 'Middle Assyrian':['Middle Assyrian','Tukulti-Ninurta','Dur-Katlimmu','Tell Sheikh Hamad'],
 'Neo-Assyrian':['Neo-Assyrian','Assyrian Empire','Sennacherib','Esarhaddon','Tiglath-pileser','Ashurbanipal','Sargon II'],
 'Neo-Babylonian':['Neo-Babylonian','Nebuchadnezzar','Nabonidus','Eanna','Ebabbar'],
 'Achaemenid':['Achaemenid','Persepolis','Persian Empire','Darius','Murašû'],
 'Hellenistic':['Seleucid','Hellenistic','Late Babylonian'],
}
K={
 'TERR':r'empire|imperial|territor|provinc|conquest|hegemon|state formation|annex|vassal|expansion|frontier|border|reich|provinz|imper|conquête|conquista',
 'HIER':r'king|kingship|ruler|governor|ensi|official|elite|hierarch|court|aristocr|elders|assembl|vizier|minister|königtum|herrscher|beamte|roi|royauté|sovran|funzionar',
 'FISC':r'\btax|tribut|levy|corv[ée]e|\bbala\b|tithe|ilkum|service obligation|conscript|labou?r|steuer|abgabe|impôt|tass',
 'COMM':r'letter|messenger|\broads?\b|communicat|correspond|courier|travel|itinerar|brief|lettre|letter|messag|posta',
 'PAL':r'palace|palatial|palast|palais|palazz|royal household|crown',
 'TEMP':r'temple|sanctuar|priest|cult\b|tempel|tempio|offering|clergy|prebend',
 'TCTL':r'temple (and|&) (the )?(palace|state|crown|king)|(palace|state|crown|royal) (and|&) (the )?temple|temple administra|royal (control|official)|tempelverwalt',
 'PRIV':r'privat|family archive|merchant|entrepreneur|loan|\bsale|land tenure|ownership|propert|debt|commerc|trade|business|household archive|famil',
 'BUR':r'administra|bureaucra|accounting|account|archiv|record|scribe|verwaltung|archivi|amministr|ragioner',
 'SCHOOL':r'school|education|curricul|lexical|exercise|edubba|tablet house|teaching|schul|école|scuola|student|apprentic',
 'LAW':r'\blaws?\b|legal|edict|justice|lawsuit|trial|recht|gesetz|\bloi\b|droit|diritto|contract|misharum|mīšarum|verdict|court case',
 'STD':r'standard|metrolog|weights?\b|measure|calendar|month name|uniform|format|pal(a)?eograph|orthograph|kalender|maß|metrologia|calendrier',
}
def fetch(q,page):
    fn=f"{OUT}/cache/{re.sub(r'[^A-Za-z0-9]+','_',q)}_{page}.rss"
    if not os.path.exists(fn) or os.path.getsize(fn)<500:
        url='https://vergil.uni-tuebingen.de/keibi/Search/Results?'+urllib.parse.urlencode(dict(lookfor=f'"{q}"',type='AllFields',limit=200,page=page,view='rss',sort='relevance'))
        subprocess.run(['curl','-sS','-m','90','-o',fn,url]); time.sleep(1.2)
    return open(fn,errors='ignore').read()
def items(x):
    for it in re.findall(r'<item>(.*?)</item>',x,re.S):
        g=lambda t: html.unescape((re.search(f'<{t}>(.*?)</{t}>',it,re.S) or [None,''])[1]).strip()
        yield dict(title=g('title'),link=g('link'),date=g('dc:date'),authors=re.findall(r'<dc:creator>(.*?)</dc:creator>',it))
rows=[]
for per,qs in Q.items():
    seen={}
    for q in qs:
        x=fetch(q,1); tot=int((re.search(r'<opensearch:totalResults>(\d+)',x) or [0,0])[1])
        pages=min((tot+199)//200,15)
        for p in range(1,pages+1):
            for it in items(x if p==1 else fetch(q,p)): seen.setdefault(it['link'],it)
        print(per,q,tot,file=sys.stderr)
    T=list(seen.values())
    for t in T: t['params']=[k for k,r in K.items() if re.search(r,t['title'],re.I)]
    json.dump(T,open(f"{OUT}/titles_{re.sub(r'[^A-Za-z0-9]+','_',per)}.json",'w'),ensure_ascii=False)
    c=collections.Counter(p for t in T for p in t['params'])
    rows.append(dict(period=per,n_titles=len(T),**{k:c.get(k,0) for k in K}))
    print(per,len(T),dict(c),file=sys.stderr)
pd.DataFrame(rows).to_csv(f'{OUT}/screen.csv',index=False); print(pd.DataFrame(rows).to_string())
