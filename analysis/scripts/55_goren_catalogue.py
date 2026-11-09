"""Case B: the per-letter catalogue of Goren, Finkelstein and Na'aman, Inscribed in Clay (2004), parsed from the
text of the book (supplied by ShG). Each catalogue entry gives museum number, sender and addressee, sampling method,
reliability, matrix (with its colour in plane-polarised light), inclusions, palaeontology, firing and the authors'
geological interpretation. The chapter and section in which the entry stands give the city to which the letter is
attributed. Output: goren/goren2004_catalogue.csv."""
from _paths import WORK
import re, pandas as pd
T=open(WORK+'/goren/inscribed_in_clay.txt',encoding='utf-8',errors='ignore').read().split('\n')
start=next(i for i,l in enumerate(T) if l.strip()=='CHAPTER 3')
rows=[]; chap=sec=None; cur=None
hdr=re.compile(r'^\s*(EA \d+[a-z]?(?:\s*\+\s*\d+)?)\s*\(([^)]*)\),?\s*(.*)$')
fields=['Sampling method','Reliability','Matrix','Inclusions','Palaeontology','Firing temperature','Geological interpretation']
for l in T[start:]:
    s=l.strip()
    if re.match(r'^CHAPTER \d+',s): chap=s; continue
    m=re.match(r'^([IVX]+)\.\s+(.+)$',s)
    if m and not re.search(r'[a-z]',s): sec=m.group(2).strip(); continue
    m=hdr.match(s)
    if m and ('from' in m.group(3) or 'inventory' in m.group(3).lower() or 'to the' in m.group(3) or m.group(3)==''):
        cur=dict(EA=m.group(1),museum_no=m.group(2),title=m.group(3),chapter=chap,section=sec,field=None); rows.append(cur); continue
    if cur is None: continue
    f=next((f for f in fields if s.startswith(f+':') or s.startswith(f+' (')),None)
    if f: cur['field']=f; cur[f]=s.split(':',1)[1].strip() if ':' in s else ''; continue
    if cur.get('field')=='Geological interpretation' and (not re.search(r'[a-z]',s) and len(s)>3 or s.startswith('CONCLUSION')): cur['field']=None; continue
    if cur.get('field') and s and not re.match(r'^\d+$',s) and not s.startswith('Fig.') and not s.isupper():
        cur[cur['field']]=cur.get(cur['field'],'')+' '+s
D=pd.DataFrame(rows).drop(columns='field')
D['EA_n']=D.EA.str.extract(r'EA (\d+)')[0].astype(int)
D=D[D['Matrix'].notna()|D['Geological interpretation'].notna()]
for c in fields:
    if c in D: D[c]=D[c].fillna('').str.replace(r'\s+',' ',regex=True).str.strip()
D['ppl_colour']=D['Matrix'].str.extract(r'([A-Za-z\- ]+?) in PPL')[0].str.split(',').str[-1].str.strip()
D['concl']=D['Geological interpretation'].str.extract(r'Conclusions?:\s*(.*)$')[0].fillna('')
# place where the tablet was made, after the authors' conclusions: default = the city of the section in which the
# entry stands; exceptions set by hand from each entry's conclusion (see SI Section S6.2)
city={'EGYPT':'Egypt','ïATTI':'Hattusa','BABYLONIA':'Babylon','MITANNI':'Mittani','ARZAWA':'Arzawa','ALASHIYA':'Alashiya',
 'UGARIT':'Ugarit','NUïASHE':'Nuhasse','QATNA':'Qatna','QIDSHU':'Kadesh','AMURRU':'Amurru','TUNIP':'Tunip','IRQATA':'Irqata',
 'BYBLOS (GUBLA)':'Byblos','BEIRUT (BIRUTA)':'Beirut','SIDON (êIDUNA)':'Sidon','TYRE (êÊURRU)':'Tyre','DAMASCUS (DIMASHQU)':'Damascus',
 'HAZOR (ÏïAêURA)':'Hazor','ACHSHAPH (AKSHAPA)':'Akshapa','SHIM>ON (SHAMïUNA)':'Shimon','ACCO (AKKA)':'Akko','ANAHARATH':'Anaharath',
 'MEGIDDO (MAGIDDA)':'Megiddo','REHOB':'Rehob','[URUX-(X)-I]G-MA-TE':'Yokneam','GINTI-KIRMIL':'Ginti-kirmil','PEHEL (PIïILU)':'Pella',
 'SHECHEM (SHAKMU)':'Shechem','JERUSALEM (URUSALIM)':'Jerusalem','GEZER (GAZRU)':'Gezer','GATH (GIMTU)':'Gath','LACHISH (LAKISHA)':'Lachish',
 'ASHDOD':'Ashdod','ASHKELON (AŠQALUNA)':'Ashkelon','YURZA':'Yurza','LETTERS OF UNPROVENANCED RULERS, SENT FROM GAZA':'Gaza'}
D['made_at']=D.section.map(city)
over={'Mt Lebanon (E of Tripoli)':[60,157],'Ardata':[61,62,156,159],'Irqata':[100,161,164,169,170,171],
 'Sumur':[78,103,126,165,166,167,228],'Gaza':[97,168,298,299,378,329,321,215,317,318,66,307,308,309,310,312,211,212,213],
 'Beth-Shean':[224,232,234,235,285,263,249],'Egypt':[1,14,162,163,190,367,370,382,339,172],'Gezer':[291],'Beirut':[136,138],'Tyre':[295,151,155],
 'Gath':[63,64,65,229,335,278],'Ullasa? (Tripoli area)':[58],'unknown':[80,146,230,251,319,50]}
for k,v in over.items(): D.loc[D.EA_n.isin(v),'made_at']=k
D['clay_source']='Goren, Finkelstein and Na\'aman 2004'
D.to_csv(WORK+'/goren/goren2004_catalogue.csv',index=False)
print(D.made_at.value_counts(dropna=False).to_string())
print(len(D), D.EA_n.nunique()); print(D.chapter.value_counts().to_string()); print(D.Reliability.str[:12].value_counts().head(8))

# smaller places, grouped by region as in the book's chapters
fill={'NII (?)':'Nii','êÊUMUR':'Sumur','SHARUNA':'Sharuna'}
beqa=['LABANA','RUïIZZI','ENISHASI','ïASI','GUDDASHUNA','A GROUP OF IDENTICAL LETTERS SENT BY FOUR BEQA> RULERS',
      'LETTERS OF UNSPECIFIED LOCATIONS, POSSIBLY FROM THE BEQA> VALLEY']
bashan=['MUSHIÏïUNA','Z/êÊIRIBASHANI','SHASïIMI','QANU','TUBU','ASHTAROTH (ASHTARTU)','ZUïRA','TABLETS FROM UNSPECIFIED CITIES IN THE BASHAN']
fill.update({s:'Beqa valley' for s in beqa}); fill.update({s:'Bashan' for s in bashan})
m=D.made_at.isna(); D.loc[m,'made_at']=D.loc[m,'section'].map(fill).fillna('unknown')
D.to_csv(WORK+'/goren/goren2004_catalogue.csv',index=False)
print('unassigned now:',(D.made_at=='unknown').sum())
