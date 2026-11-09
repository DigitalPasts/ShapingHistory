"""98c rerun with the consolidated dates of 98j (CDLI + Archibab, BDTNS, NaBuCCo, Prosobab, Oracc, eBL; ShG 9 Nov 2026).
Same rule: archival tablets (administrative, letters, legal, contracts) within 20 years before / after the date, at named
sites present on both sides; testable = at least 30 on each side. Three Neo-Assyrian and one Hellenistic candidate are added
because Oracc now dates enough tablets; they still need the OHANE check of the turning-point rule before use.
Output: turning/candidate_testability_v2.csv"""
from _paths import WORK
import pandas as pd, numpy as np
R=WORK
X=pd.read_csv(f'{R}/turning/tablet_dates_consolidated.csv')
X=X[X.genre.isin(['Administrative','Letter','Legal','Business / Contracts'])&X.bce.notna()]
old=pd.read_csv(f'{R}/turning/candidate_testability.csv').set_index('candidate')
C=[('Urukagina reform','3rd',2351,['ED IIIb'],''),('Naram-Sin reform','3rd',2230,['Old Akkadian'],''),('Šulgi 21','3rd',2072,['Ur III'],''),
   ('Puzriš-Dagān, Š39','3rd',2054,['Ur III'],''),('Ibbi-Suen 3, provinces lost','3rd',2024,['Ur III'],''),
   ('Hammurabi takes Larsa','2nd',1763,['Old Babylonian'],''),('Samsu-iluna loses the south','2nd',1739,['Old Babylonian'],''),
   ('Nabopolassar, independence','1st',626,['Neo-Babylonian'],''),('Cyrus takes Babylon','1st',539,['Neo-Babylonian','Achaemenid'],''),
   ('Darius I reorganisation','1st',521,['Neo-Babylonian','Achaemenid'],''),('Xerxes, end of archives','1st',484,['Achaemenid','Neo-Babylonian'],''),
   ('Sargon II to Sennacherib (by reign)','1st',705,['Neo-Assyrian'],''),
   ('Tiglath-pileser III, provincial reform','1st',745,['Neo-Assyrian'],'added'),('Esarhaddon accession','1st',681,['Neo-Assyrian'],'added'),
   ('Šamaš-šuma-ukīn revolt','1st',652,['Neo-Assyrian','Neo-Babylonian'],'added'),('Parthian conquest of Babylonia','1st',141,['Hellenistic'],'added')]
rows=[]
for name,mil,yr,pers,flag in C:
    g=X[X.period.isin(pers)]
    b=g[g.bce.between(yr+1,yr+20)]; a=g[g.bce.between(yr-19,yr)]
    S=(set(b.site)&set(a.site))-{'unknown','uncertain'}
    bb=b[b.site.isin(S)]; aa=a[a.site.isin(S)]
    o=old.loc[name] if name in old.index else None
    rows.append(dict(candidate=name,millennium=mil,date_bce=yr,status=flag or 'listed 8 Nov',
        before_8nov=None if o is None else int(o.before),after_8nov=None if o is None else int(o.after),before=len(bb),after=len(aa),
        from_new_sources=int((bb.date_source!='CDLI').sum()+(aa.date_source!='CDLI').sum()),year_known=int(bb.year_known.sum()+aa.year_known.sum()),
        sites=', '.join(sorted(S)),testable=(len(bb)>=30)&(len(aa)>=30)))
r=pd.DataFrame(rows); r.to_csv(f'{R}/turning/candidate_testability_v2.csv',index=False)
print(r.drop(columns=['sites','millennium']).to_string())
