"""Bibliometric overview of the field for the 14 main periods x 12 parameters (4 Nov 2026).
Sources (ShG's Dropbox, Data-Files/ANE-Bibliography; copied to /home/user/lit/bibdata):
  keibi_57_82.txt                  OCR of Keilschriftbibliographie 57-81 (Orientalia, 1997-2023 literature)
  KeiBi_82_entries_classified.tsv  KeiBi 82 (2024), one entry per row
  ebl_bibliography.json            eBL bibliography, CSL-JSON (all years)
Method, kept simple and transparent:
  1. Parse every entry into first author, all author surnames, year, title. KeiBi volumes are found where the entry
     numbering restarts; a KeiBi entry that reviews a book ("[vol:no]: BO 54 (1997) 411-416 (reviewer); JNES ...") is
     not counted as a new work, but its number of reviews is credited to the reviewed book (a proxy for influence).
  2. Merge KeiBi and eBL on (first-author surname, first five title words); report the overlap.
  3. Tag each work with periods (multilingual title lexicon, PER below) and parameters (the title keyword lists of
     93_keibi_screen.py, K below, with German, French and Italian terms).
  4. For each period x parameter cell: number of works, works since 2010, leading authors, reviews, and how far our
     evidence base covers the field: share of the cell's ten most productive authors whom we cite for that period,
     and the most reviewed or most recent works by authors we do not cite ('unread core').
Title keywords miss works whose titles do not name a period or topic, and OCR damage loses entries in some volumes
(the per-volume yields are reported). The counts measure attention in the field, not evidence for a score.
Outputs: centralization/biblio/{works.csv.gz, cells.csv, periods.csv, unread.csv, summary.json}."""
from _paths import LIT, WORK
import warnings; warnings.filterwarnings('ignore')
import re, json, gzip, collections, unicodedata, glob, os
import pandas as pd
B=LIT+'/bibdata'; C=WORK+'/centralization'; O=f'{C}/biblio'; os.makedirs(O,exist_ok=True)
MAIN=['ED IIIa','ED IIIb','Ebla','Old Akkadian','Ur III','Early Old Babylonian','Old Babylonian','Old Assyrian',
      'Middle Babylonian','Middle Assyrian','Neo-Assyrian','Neo-Babylonian','Achaemenid','Hellenistic']
def fold(s):
    s=unicodedata.normalize('NFKD',str(s)); s=''.join(c for c in s if not unicodedata.combining(c))
    return s.replace('ḫ','h').replace('Ḫ','H').lower()
# ---------------------------------------------------------------- period lexicon (matched on folded titles)
PER={
 'ED IIIa':r'\bfara\b|suruppak|shuruppak|abu ?salabikh|early dynastic iiia|\bed iiia\b',
 'ED IIIb':r'lagas|lagash|girsu|pre-?sargoni|presargoni|prasargoni|vorsargoni|presargoni|uru-?(inim)?gina|urukagina|lugalanda|enmetena|eannatum|lugalzage|early dynastic iiib|\bed iiib\b|fruhdynast|early dynastic',
 'Ebla':r'\bebla|eblait|eblaite|\bmardikh',
 'Old Akkadian':r'(?<!pre-)(?<!pre)(?<!pra)(?<!vor)(?<!pre )sargoni(c|que|sch|ca|co)|old akkadian|altakkad|paleo-?akkad|sargonique|sargonisch|naram-?s[iu]n|\bakkade\b|agade|manistusu|rimus|sar-?kali-?sarri|accadico antico',
 'Ur III':r'\bur iii\b|third dynasty of ur|terza dinastia di ur|troisieme dynastie d.ur|dritten? dynastie von ur|messenger texts|\bbala\b|ur-?iii|neo-?sumer|neusumer|neosumer|sulgi|shulgi|drehem|puzris-?dagan|ur-?namma|amar-?suen|su-?sin\b|ibbi-?sin|ur 3\b',
 'Early Old Babylonian':r'isin-?larsa|\bisin\b|\blarsa\b|esnunna|eshnunna|rim-?s[iu]n|lipit-?istar|isbi-?erra|warad-?sin|sumu-?la-?el|early old babylonian|fruhaltbabylon',
 'Old Babylonian':r'old babylonian|altbabylon|paleo-?babylon|paleobabilon|paleo-?babilon|hammu-?rabi|hammurapi|samsu-?iluna|\bmari\b|ammi-?saduqa|ammi-?ditana',
 'Old Assyrian':r'old assyrian|altassyr|paleo-?assyr|\bkanis\b|\bkanes\b|kanesh|kultepe|\bkarum|paleoassiri|paleo-?assiro',
 'Middle Babylonian':r'kassite|kassit|cassite|middle babylonian|mittelbabylon|medio-?babilon|medio-?babylon|kurigalzu|burna-?burias|nazi-?maruttas|kudurru',
 'Middle Assyrian':r'middle-? ?assyrian|mittelassyr|medio-?assir|medio-?assyr|paleo-?assyrien recent|tukulti-?ninurta( i\b|(?! ii))|dur-?katlimmu|sheikh hamad|tell sabi abyad|assur-?uballit( i\b|(?! ii))|adad-?nirari i\b|salmanassar i\b|shalmaneser i\b|tiglath-?pileser i\b|tiglat-?pileser i\b',
 'Neo-Assyrian':r'neo-?assyr|neuassyr|neoassir|neo-?assiro|(?<!middle )(?<!middle-)(?<!middle- )assyrian empire|sennacherib|sanherib|esarhaddon|asarhaddon|tiglath-?pileser(?! i\b)|tiglat-?pileser(?! i\b)|sargonid|tukulti-?ninurta ii\b|adad-?nirari ii\b|assur-?uballit ii\b|ashurbanipal|assurbanipal|sargon ii|kalhu|nimrud|nineveh|ninive|niniveh',
 'Neo-Babylonian':r'neo-?babylon|neubabylon|neobabilon|neo-?babilon|nebuchadne|nebukadne|nabuchodono|nabonidus|nabonid|nabopolassar|\beanna\b|ebabbar|chaldean dynasty',
 'Achaemenid':r'achaemenid|achamenid|achemenid|achemenide|persepolis|persian empire|perserreich|empire perse|darius|dareios|xerxes|cambyses|kambyses|murasu|cyrus|kyros|teispid|roi perse|persian king',
 'Hellenistic':r'seleucid|seleukid|seleucide|hellenistic|hellenist|arsacid|parthian|antiochus|astronomical diar',
}
PER={k:re.compile(v) for k,v in PER.items()}
# Period-mixing guard (ShG 8 Nov: Boivin 2024 on sixth-century Larsa was listed under Early Old Babylonian; Turowski 2026
# on the Kanisurra gate of Uruk under Old Assyrian). A city name alone (WEAK) does not date a title: Larsa, Isin, Mari,
# Kaneš, Nineveh or the Ebabbar occur in several periods. A tag that rests only on such a name is dropped when the title
# names another period (a tag that does not itself rest on a city name) or a date in another millennium (ERA).
# 'Late Babylonian' (c. 750 BC onwards) is a date, not the Hellenistic period. 'Sargonid' is Neo-Assyrian, 'pre-Sargonic' ED IIIb. The Second Dynasty of Isin is Middle Babylonian, not Early Old Babylonian.
WEAK={'ED IIIa':r'\bfara\b|suruppak|shuruppak|abu ?salabikh','ED IIIb':r'lagas|lagash|girsu',
 'Ebla':r'\bebla\b|\bmardikh','Old Akkadian':r'\bakkade\b|agade','Ur III':r'drehem','Early Old Babylonian':r'\bisin\b|\blarsa\b|esnunna|eshnunna',
 'Old Babylonian':r'\bmari\b','Old Assyrian':r'\bkanis\b|\bkanes\b|kanesh|kultepe|\bkarum','Middle Babylonian':r'kudurru',
 'Middle Assyrian':r'dur-?katlimmu|sheikh hamad|tell sabi abyad','Neo-Assyrian':r'kalhu|nimrud|nineveh|ninive|niniveh',
 'Neo-Babylonian':r'\beanna\b|ebabbar','Achaemenid':r'^$','Hellenistic':r'^$'}
WEAK={k:re.compile(v) for k,v in WEAK.items()}
ERA={'0':r'neolithic|chalcolithic|ubaid|uruk period|jemdet nasr|early dynastic i\b|early dynastic ii\b|early dynastic i-ii|\bed i-ii|archaic ur',
     '3':r'sakkanakku|\b2[0-6]\d\d (b\.?c|v\. ?chr|av\.)|third millennium|3rd millennium|\b3\. jahrtausend|iiie millenaire|iii millennio|\b(xxi|xxii|xxiii|xxiv|xxv|xxvi)(e|th)? (siecle|century)|\b2[1-6]th century',
     '2':r'\b1[3-9]\d\d(-\d{3,4})? (b\.?c|v\. ?chr|av\.)|second millennium|2nd millennium|\b2\. jahrtausend|iie millenaire|ii millennio|bronze age|\b1[2-9]th century|\b(twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|eighteenth|nineteenth) century',
     '1':r'\b(1[0-2]|[2-9])\d\d(-\d{2,4})? (b\.?c|v\. ?chr|av\.)|first millennium|1st millennium|\b1\. jahrtausend|ier millenaire|i millennio|iron age|\b([4-9]|1[01])th century|\b(fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh) century|\b[4-9]\. jh|late babylonian|spatbabylon|isin ii\b|second dynasty of isin|ii\. dynastie von isin'}
ERA={k:re.compile(v) for k,v in ERA.items()}
EPOCH={'ED IIIa':'3','ED IIIb':'3','Ebla':'3','Old Akkadian':'3','Ur III':'3','Early Old Babylonian':'2','Old Babylonian':'2','Old Assyrian':'2',
       'Middle Babylonian':'2','Middle Assyrian':'2','Neo-Assyrian':'1','Neo-Babylonian':'1','Achaemenid':'1','Hellenistic':'1'}
def strong(t,p): return bool(PER[p].search(WEAK[p].sub(' ',t)))
def guard(t):
    hits=[p for p in PER if PER[p].search(t)]
    if re.search(r'naram-?s[iu]n (of|von|d.) ?esnunna',t): hits=[p for p in hits if p!='Old Akkadian']+(['Early Old Babylonian'] if 'Early Old Babylonian' not in hits else [])
    sure={p for p in hits if strong(t,p)}; eras={EPOCH[p] for p in sure}|{e for e,rx in ERA.items() if rx.search(t)}
    # a tag resting only on a city name is dropped when the title names another period (any millennium) or a date in another millennium
    # ('Old Babylonian' in the field's usage includes the Isin-Larsa period, so it does not displace an Early Old Babylonian city tag)
    keep=[p for p in hits if p in sure or (not (eras-{EPOCH[p]}) and not (sure-{p}-({'Old Babylonian'} if p=='Early Old Babylonian' else set())))]
    if re.search(r'early dynastic (i|ii|i-ii)\b|\bed i-ii\b',t) and not re.search(r'iii',t): keep=[p for p in keep if p not in ('ED IIIa','ED IIIb')]
    # Larsa, Isin or Esnunna titles that name Hammurabi or Samsu-iluna are after 1763 (Old Babylonian)
    if 'Early Old Babylonian' in keep and 'Early Old Babylonian' not in sure and re.search(r'hammu-?rabi|hammurapi|samsu-?iluna|babylonian conquest|conquete babylon',t): keep.remove('Early Old Babylonian')
    return keep, [p for p in hits if p not in keep]
K={  # 93_keibi_screen.py, extended with German, French and Italian terms
 'TERR':r'empire|imperial|territor|provinc|conquest|hegemon|state formation|annex|vassal|expansion|frontier|border|reich|provinz|imper|conquete|conquista|eroberung',
 'HIER':r'\bking|kingship|ruler|governor|\bensi|official|elite|hierarch|court\b|aristocr|elders|assembl|vizier|minister|konig|herrscher|beamte|\broi\b|royaute|sovran|funzionar|statthalter|gouverneur',
 'FISC':r'\btax|tribut|levy|corvee|\bbala\b|tithe|ilkum|service obligation|conscript|labou?r|steuer|abgabe|impot|tass[ae]|fron\b|dienstpflicht',
 'COMM':r'\bletters?\b|messenger|\broads?\b|communicat|correspond|courier|travel|itinerar|\bbrief|lettre|messag|posta\b|bote',
 'PAL':r'palace|palatial|palast|palais|palazz|royal household|crown',
 'TEMP':r'temple|sanctuar|priest|\bcult\b|tempel|tempio|offering|clergy|prebend|heiligtum|pretre|sacerdo',
 'TCTL':r'temple (and|&) (the )?(palace|state|crown|king)|(palace|state|crown|royal) (and|&) (the )?temple|temple administra|royal (control|official)|tempelverwalt|tempelwirtschaft|temple economy|tempelstadt|temple-?state',
 'PRIV':r'privat|family archive|merchant|entrepreneur|\bloan|\bsale|land tenure|ownership|propert|\bdebt|commerc|\btrade|business|household archive|famil|kaufmann|handel|marchand|commercio|eigentum',
 'BUR':r'administra|bureaucra|accounting|\baccount|archiv|record|scribe|verwaltung|archivi|amministr|ragioner|schreiber|scribal|comptab',
 'SCHOOL':r'school|education|curricul|lexical|exercise|edubba|tablet house|teaching|schul|ecole|scuola|student|apprentic|lexikal',
 'LAW':r'\blaws?\b|legal|edict|justice|lawsuit|trial|recht|gesetz|\bloi\b|droit|diritto|contract|misharum|mısarum|verdict|court case|codex|code de',
 'STD':r'standard|metrolog|weights?\b|measure|calendar|month name|uniform|format|palaeograph|paleograph|orthograph|kalender|\bmass|metrologia|calendrier|tablet shape|tafelform|diplomatic',
}
K={k:re.compile(v) for k,v in K.items()}
# ---------------------------------------------------------------- 1a. KeiBi 57-81 (OCR)
BAD=re.compile(r'This content downloaded|All use subject to|^Keilschriftbibliographie|^\d+\* |H\. Neumann|^\s*$')
L=open(f'{B}/keibi_57_82.txt',errors='ignore').read().split('\n')
kb=[];cur=None;prev=0;vol=57
for ln in L:
    if BAD.search(ln): continue
    m=re.match(r'^(\d{1,4})\.\s+(\S.*)',ln)
    if m:
        n=int(m.group(1))
        restart=n<=3 and prev>300
        if restart: vol+=1
        if restart or not kb or 0<n-prev<40:
            cur=dict(src='KeiBi',vol=vol,no=n,text=m.group(2)); kb.append(cur); prev=n; continue
    if cur: cur['text']+=' '+ln.strip()
# ---------------------------------------------------------------- 1b. KeiBi 82 (TSV)
for ln in open(f'{B}/KeiBi_82_entries_classified.tsv',errors='ignore'):
    f=ln.rstrip('\r\n').split('\t')
    if len(f)>=4 and f[1].isdigit(): kb.append(dict(src='KeiBi',vol=82,no=int(f[1]),text=f[3]))
NAME=r"\*?[A-ZÀ-ÞĀ-ž][^,:\[\]()]{0,40}?,\s*(?:[^,:\[\]]{1,30}?)\*?(?:\s*\((?:Hg|Hrsg|ed|eds)\.?\))?"
AUTH=re.compile(rf"^((?:{NAME}\s*[-–—]\s*)*{NAME}),\s*(.+)$")
def parse_kb(e):
    t=e['text'].replace('*','')
    m=AUTH.match(t)
    if m: auth,rest=m.group(1),m.group(2)
    else: auth,rest=t.split(',')[0],','.join(t.split(',')[1:])
    fams=[a.split(',')[0].strip(' .') for a in re.split(r'\s*[-–—]\s*(?=[A-ZÀ-ÞĀ-ž][^,]{0,40},)',auth)]
    title=re.split(r':\s|\s\[\d|\s\((?:[A-Z][A-Za-z]{1,8}|Hg)',rest)[0].strip(' .')
    yrs=[int(y) for y in re.findall(r'\b(19[5-9]\d|20[0-2]\d)\b',rest)]
    rev=re.search(r'\[\d{2}:\d{1,4}\]\s*:',t)
    nrev=len([s for s in re.split(r"[;']\s",t[rev.end():]) if re.search(r'\(\D',s)]) if rev else 0
    return dict(src='KeiBi',id=f"KeiBi {e['vol']}:{e['no']}",fam=fams[0],fams='; '.join(fams),title=title,
                year=max(yrs) if yrs else 1941+e['vol'],is_review=bool(rev),n_reviews=nrev)
K1=[parse_kb(e) for e in kb]
yield_by_vol=collections.Counter(e['vol'] for e in kb)
# ---------------------------------------------------------------- 1c. eBL
E=[]
for d in json.load(open(f'{B}/ebl_bibliography.json')):
    a=d.get('author') or d.get('editor') or []
    fams=[x.get('family') or x.get('literal') or '' for x in a]
    dp_=(d.get('issued') or {}).get('date-parts') or [[None]]; y=(dp_[0] or [None])[0] if dp_ else None
    E.append(dict(src='eBL',id=f"eBL {d.get('id')}",fam=fams[0] if fams else '',fams='; '.join(fams),title=str(d.get('title','')),
                  year=int(y) if str(y).isdigit() else None,is_review=False,n_reviews=0,container=d.get('container-title','')))
# ---------------------------------------------------------------- 2. merge
def wkey(fam,title): return fold(fam).split()[0] if fam else '', ' '.join(re.findall(r'[a-z0-9]+',fold(title))[:5])
W={}; rev=collections.Counter()
for r in K1:
    k=wkey(r['fam'],r['title'])
    if r['is_review']: rev[k]+=r['n_reviews']
    if r['is_review'] and k in W: continue
    W.setdefault(k,dict(r,srcs={'KeiBi'}))
n_kb=len(W); overlap=0
for r in E:
    k=wkey(r['fam'],r['title'])
    if k in W: W[k]['srcs'].add('eBL'); overlap+=1
    else: W[k]=dict(r,srcs={'eBL'})
for k,w in W.items(): w['n_reviews']=rev.get(k,0); w['srcs']='+'.join(sorted(w['srcs']))
df=pd.DataFrame(W.values())
df=df[df.title.str.len()>8].copy()
ft=df.title.map(fold)
G=ft.map(guard); df['dropped']=G.map(lambda g:'; '.join(g[1]))
for p in PER: df['P_'+p]=G.map(lambda g,p=p:p in g[0])
for k,rx in K.items(): df['K_'+k]=ft.str.contains(rx)
# Girsu and Lagaš titles are ED IIIb only when they do not also name Ur III / Lagaš II
amb=ft.str.contains(r'gudea|lagas(h)? ii\b|ur-?ningirsu|ur-?baba|nam-?mahani')
df['P_ED IIIb']=df['P_ED IIIb'] & ~df['P_Ur III'] & ~amb
df['periods']=df[[f'P_{p}' for p in MAIN]].apply(lambda r:'; '.join(p for p in MAIN if r[f'P_{p}']),axis=1)
df['params']=df[[f'K_{k}' for k in K]].apply(lambda r:'; '.join(k for k in K if r[f'K_{k}']),axis=1)
df[['src','srcs','id','fam','fams','year','title','is_review','n_reviews','periods','params','dropped']].to_csv(f'{O}/works.csv.gz',index=False,compression='gzip')
# ---------------------------------------------------------------- 3. our evidence base: (surname, year) of every cited work
bib={}
for f in glob.glob(f'{C}/*.bib'):
    for ent in re.split(r'\n@',open(f).read()):
        m=re.match(r'\s*@?\w+\{([^,]+),',ent)
        if not m: continue
        a=re.search(r'\b(?:author|editor)\s*=\s*\{(.+?)\},?\n',ent,re.S); y=re.search(r'\byear\s*=\s*\{?(\d{4})',ent)
        fams=[fold(x.split(',')[0]).strip('{} ').split()[-1] for x in re.split(r'\s+and\s+',a.group(1))] if a else []
        bib[m.group(1)]=(fams,int(y.group(1)) if y else None)
ev=pd.read_csv(f'{C}/lit_evidence_v2_long.csv')
ev['pmain']=ev.period.str.replace(r' \((Babylonia|Persepolis)\)','',regex=True)
cited_fams={p:set() for p in MAIN}; cited_fy=set(); unk=set()
for _,r in ev.iterrows():
    fy=bib.get(r.key)
    if not fy: unk.add(r.key); continue
    for f in fy[0]:
        cited_fy.add((f,fy[1]))
        if r.pmain in cited_fams: cited_fams[r.pmain].add(f)
def lastword(f):
    w=fold(f).replace('{','').replace('}','').strip().split()
    return w[-1] if w and w[-1][0].isalpha() else ''
df['fam_n']=df.fam.map(lastword)
df['fams_n']=df.fams.map(lambda s:[lastword(x) for x in str(s).split('; ') if x.strip()])
df['ours']=df.apply(lambda r:any((f,r.year) in cited_fy for f in r.fams_n),axis=1)
# ---------------------------------------------------------------- 4. cells
cells=[];unread=[];periods=[]
works=df[~df.is_review]
for p in MAIN:
    dp=works[works['P_'+p]]
    top_all=collections.Counter(f for fs in dp.fams_n for f in fs if f).most_common(10)
    periods.append(dict(period=p,works=len(dp),since2010=int((dp.year>=2010).sum()),with_param=int(dp[[f'K_{k}' for k in K]].any(axis=1).sum()),
        ours=int(dp.ours.sum()),top_authors='; '.join(f'{a} ({n})' for a,n in top_all),
        top_cited=sum(a in cited_fams[p] for a,_ in top_all),statements=int((ev.pmain==p).sum()),cited_works=int(ev[ev.pmain==p].key.nunique())))
    for k in K:
        d=dp[dp['K_'+k]]
        top=collections.Counter(f for fs in d.fams_n for f in fs if f).most_common(10)
        cov=sum(a in cited_fams[p] for a,_ in top)
        u=d.loc[~d.fams_n.map(lambda fs:any(f in cited_fams[p] for f in fs)).astype(bool)].copy()
        u=u.sort_values(['n_reviews','year'],ascending=False).head(5)
        for _,r in u.iterrows():
            unread.append(dict(period=p,param=k,id=r.id,authors=r.fams,year=r.year,title=r.title[:160],reviews=int(r.n_reviews),src=r.srcs))
        cells.append(dict(period=p,param=k,works=len(d),since2010=int((d.year>=2010).sum()),reviews=int(d.n_reviews.sum()),
            top_authors='; '.join(f'{a} ({n})' for a,n in top[:5]),top10_cited=cov,top10_n=len(top),ours=int(d.ours.sum())))
cells=pd.DataFrame(cells); periods=pd.DataFrame(periods); unread=pd.DataFrame(unread)
tot=periods.with_param.sum(); st=periods.statements.sum()
periods['field_share']=(periods.with_param/tot).round(3); periods['our_share']=(periods.statements/st).round(3)
periods['ratio']=(periods.our_share/periods.field_share).round(2)
cells.to_csv(f'{O}/cells.csv',index=False); periods.to_csv(f'{O}/periods.csv',index=False); unread.to_csv(f'{O}/unread.csv',index=False)
S=dict(keibi_entries=len(kb),keibi_vol_yield={int(k):v for k,v in sorted(yield_by_vol.items())},keibi_reviews=int(sum(r['is_review'] for r in K1)),
       keibi_works=n_kb,ebl_entries=len(E),ebl_matched_keibi=overlap,merged_works=len(df),
       period_tagged=int((df.periods!='').sum()),dropped_by_guard=int((df.dropped!='').sum()),unmatched_keys=sorted(unk),
       rho_field_vs_ours=round(periods[['with_param','statements']].corr('spearman').iloc[0,1],2))
json.dump(S,open(f'{O}/summary.json','w'),indent=1,ensure_ascii=False)
print(json.dumps({k:v for k,v in S.items() if k!='keibi_vol_yield'},ensure_ascii=False))
print(periods[['period','works','since2010','with_param','ours','top_cited','statements','field_share','our_share','ratio']].to_string())
