"""One date per photographed tablet from CDLI and the companion databases (ShG, 9 Nov 2026).
Rule (ShG's guide note): where a specialist database names a different king from CDLI, its date is used and the tablet is
flagged (conflict=True, with both readings kept). Priority among databases: Archibab (OB), BDTNS (Ur III), NaBuCCo,
Prosobab (NB, Achaemenid), OARE eponyms dated by the REL of Barjamovic, Hertel and Larsen 2012 (Old Assyrian, 37i), Oracc catalogues (oracc-parser Zenodo 2026 + live download), eBL. Absolute years are taken as
given where a source has them (Archibab middle chronology, Oracc date_gen, HBTIN Seleucid era: BCE = 312 - SE); otherwise
accession year from the chronology table of 94 (extended below) minus (regnal year - 1).
Output: turning/tablet_dates_consolidated.csv"""
from _paths import WORK
import pandas as pd, numpy as np, json, glob, re, unicodedata
R=WORK
src=open(f'{R}/scripts/94_turning_points_pilot.py').read(); ns={}; exec(src[src.find('U3='):src.find("d['bce']")],ns)
CH={**ns['U3'],**ns['OB'],**ns['NB'],**ns['NA'],**ns['OAK'],**ns['LAG']}
CH.update({'Darius2':424,'Artaxerxes2':405,'Artaxerxes3':359,'Kandalānu':647,'Šamaš-šuma-ukīn':668,'Assur-etel-ilani':631,'Sin-sharru-ishkun':627,
           'Tiglath-pileser3':745,'Shalmaneser5':727,'Bardiya':522,'Ur-Namma':2110})
def nk(x):
    if not isinstance(x,str) or not x.strip(): return None
    a=unicodedata.normalize('NFKD',x).encode('ascii','ignore').decode().lower().replace(' ','').replace('-','').replace('_','')
    M={'nabopolassar':'Nabopolassar','npl':'Nabopolassar','nabuaplausur':'Nabopolassar','nebuchadnezzarii':'Nebuchadnezzar2','nebuchadnezzar2':'Nebuchadnezzar2','nbk':'Nebuchadnezzar2','nabukudurriusurii':'Nebuchadnezzar2',
       'amelmarduk':'Amēl-Marduk','am':'Amēl-Marduk','neriglissar':'Neriglissar','ner':'Neriglissar','nergalsharruusur':'Neriglissar','nergalsarrusur':'Neriglissar','nabonidus':'Nabonidus','nbn':'Nabonidus','nabunaid':'Nabonidus',
       'cyrus':'Cyrus','cyrusii':'Cyrus','cyrus2':'Cyrus','cyr':'Cyrus','cambyses':'Cambyses','cambysesii':'Cambyses','cambyses2':'Cambyses','cam':'Cambyses','camb':'Cambyses',
       'dariusi':'Darius1','darius1':'Darius1','dari':'Darius1','dar':'Darius1','darius':'Darius1','xerxes':'Xerxes','xerxesi':'Xerxes','xer':'Xerxes','artaxerxesi':'Artaxerxes1','artaxerxes1':'Artaxerxes1','arti':'Artaxerxes1',
       'dariusii':'Darius2','darius2':'Darius2','darii':'Darius2','artaxerxesii':'Artaxerxes2','artaxerxes2':'Artaxerxes2','artii':'Artaxerxes2','artaxerxesiii':'Artaxerxes3','bardiya':'Bardiya','bar':'Bardiya',
       'sargon2':'Sargon2','sargonii':'Sargon2','sennacherib':'Sennacherib','esarhaddon':'Esarhaddon','assurbanipal':'Assurbanipal','ashurbanipal':'Assurbanipal','assuretelilani':'Assur-etel-ilani','sinsharruishkun':'Sin-sharru-ishkun',
       'tiglathpileser3':'Tiglath-pileser3','tiglathpileseriii':'Tiglath-pileser3','shalmaneser5':'Shalmaneser5','kandalanu':'Kandalānu','samassumaukin':'Šamaš-šuma-ukīn','samassumukin':'Šamaš-šuma-ukīn','shamashshumaukin':'Šamaš-šuma-ukīn',
       'urnamma':'Ur-Namma','sulgi':'Šulgi','shulgi':'Šulgi','amarsuen':'Amar-Suen','amarsin':'Amar-Suen','susuen':'Šū-Suen','shusuen':'Šū-Suen','shusin':'Šū-Suen','ibbisuen':'Ibbi-Suen','ibbisin':'Ibbi-Suen',
       'hammurabi':'Hammurapi','hammurapi':'Hammurapi','samsuiluna':'Samsu-iluna','rimsini':'Rim-Sin','rimsin':'Rim-Sin','abiesuh':'Abi-ešuh','ammiditana':'Ammi-ditana','ammisaduqa':'Ammi-saduqa','samsuditana':'Samsu-ditana',
       'waradsin':'Warad-Sin','sinmuballit':'Sin-muballit'}
    return M.get(a,x.strip())
d=pd.read_parquet(f'{R}/master_tablets.parquet')[['id','period','site','genre','ruler','ryear']]
d['cdli_king']=d.ruler.where(~d.ruler.isin(['--','-','?','','needed'])).map(nk); d['cdli_year']=d.ryear
C=[]  # candidate readings: id, source, king, year, bce_abs
A=pd.read_csv(f'{R}/turning/companion_dates.csv'); C.append(A[A.ab_dated].assign(source='Archibab',king=A.ab_ruler.map(nk),year=A.ab_year,bce_abs=A.ab_bce)[['id','source','king','year','bce_abs']])
B=pd.read_csv(f'{R}/turning/ur3_bdtns_dates.csv'); B=B[B.b_dated]; C.append(B.assign(source='BDTNS',king=B.b_ruler.map(nk),year=B.b_year,bce_abs=np.nan)[['id','source','king','year','bce_abs']])
N=pd.read_csv(f'{R}/nabucco/nabucco_matched.csv'); N=N[N.nb_king.notna()&(N.nb_king!='XXX')]; C.append(N.assign(source='NaBuCCo',king=N.nb_king.map(nk),year=N.nb_year,bce_abs=np.nan)[['id','source','king','year','bce_abs']])
P=pd.read_csv(f'{R}/prosobab/prosobab_matched.csv'); P=P[P.King.notna()]; C.append(P.assign(source='Prosobab',king=P.King.map(nk),year=pd.to_numeric(P._Year,errors='coerce'),bce_abs=np.nan)[['id','source','king','year','bce_abs']])
Q=pd.read_csv(f'{R}/oracc/oracc_matched.csv'); Q=Q[Q.o_dated]
se=pd.to_numeric(Q.dates_referenced.fillna('').str.extract(r'^HE\.SE\.(\d+)')[0],errors='coerce')
gen=pd.to_numeric(Q.date_gen.fillna('').str.extract(r'^(\d{3,4})')[0],errors='coerce')
dbce=pd.to_numeric(Q.date_bce.fillna('').str.extract(r'^-?(\d{3,4})')[0],errors='coerce')
C.append(Q.assign(source='Oracc',king=Q.o_king.map(nk),year=np.nan,bce_abs=gen.fillna(312-se).fillna(dbce))[['id','source','king','year','bce_abs']])
E=pd.read_csv(f'{R}/ebl/ebl_dates.csv'); E=E[E.king.notna()]; C.append(E.assign(source='eBL',king=E.king.map(nk),year=pd.to_numeric(E.year,errors='coerce'),bce_abs=np.nan)[['id','source','king','year','bce_abs']])
O=pd.read_csv(f'{R}/oare/oa_eponym_dates.csv'); O=O[O.rel.notna()]   # Old Assyrian: OARE eponym + REL (37i), year of the eponym
C.append(O.assign(source='OARE+REL',king=O.king.map(nk),year=np.nan,bce_abs=O.bce)[['id','source','king','year','bce_abs']])
C=pd.concat(C); C['rank']=C.source.map({'Archibab':0,'BDTNS':1,'NaBuCCo':2,'Prosobab':3,'Oracc':4,'eBL':5,'OARE+REL':6})
best=C.sort_values(['rank']).drop_duplicates('id').set_index('id')
X=d.set_index('id').join(best,how='left')
def loose(v):
    v=v.astype(str).str.replace('Sh','S').str.replace('sh','s').str.normalize('NFKD').str.encode('ascii','ignore').str.decode('ascii').str.lower()
    v=v.str.replace(r'_.*','',regex=True).str.replace(r'[^a-z0-9]','',regex=True).str.replace('e','i').str.replace('p','b').str.replace('uu','u')
    return v.str.replace(r'(ii|2)$','2',regex=True).str[:6]
X['conflict']=X.cdli_king.notna()&X.king.notna()&(loose(X.cdli_king)!=loose(X.king))
use_db=X.king.notna()&(X.cdli_king.isna()|X.conflict) | (X.cdli_king.notna()&~X.conflict&X.cdli_year.isna()&(X.year.notna()|X.bce_abs.notna()))
use_db=use_db | (X.king.isna()&X.bce_abs.notna()&X.cdli_king.isna())   # absolute year without a king name (e.g. Seleucid-era dates in Oracc)
X['date_source']=np.where(use_db,X.source,np.where(X.cdli_king.notna(),'CDLI',None))
X['king_final']=np.where(use_db,X.king,X.cdli_king)
X['year_final']=np.where(use_db,X.year,X.cdli_year)
X['bce']=np.where(use_db&X.bce_abs.notna(),X.bce_abs,X.king_final.map(CH)-(pd.to_numeric(X.year_final,errors='coerce').fillna(1).clip(lower=1)-1))
X['year_known']=pd.to_numeric(X.year_final,errors='coerce').notna()|(use_db&X.bce_abs.notna())
X['note']=np.where(X.conflict,'CDLI names '+X.cdli_king.astype(str)+'; '+X.source.astype(str)+' names '+X.king.astype(str)+' (database reading used)','')
X=X.reset_index()[['id','period','site','genre','king_final','year_final','bce','year_known','date_source','conflict','cdli_king','cdli_year','source','king','year','note']]
X.to_csv(f'{R}/turning/tablet_dates_consolidated.csv',index=False)
print('dated',int((X.king_final.notna()|X.bce.notna()).sum()),'| with BCE year',int(X.bce.notna().sum()),'| conflicts',int(X.conflict.sum()),X[X.conflict].source.value_counts().to_dict())
print(X[X.king_final.notna()].date_source.value_counts().to_dict())
print('kings without chronology (no BCE):',X[X.king_final.notna()&X.bce.isna()].king_final.value_counts().head(12).to_dict())
