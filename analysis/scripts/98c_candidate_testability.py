"""Testability of every turning-point candidate (ShG, 8 Nov 2026): dated archival tablets within +/-20 years of the date,
at named sites present on both sides. Chronology table as in 94_turning_points_pilot.py (middle chronology; regnal year 1
when the year is missing, counted separately). Output: turning/candidate_testability.csv"""
from _paths import WORK
import pandas as pd, numpy as np, re
R=WORK
src=open(f'{R}/scripts/94_turning_points_pilot.py').read()
ns={}; exec(src[src.find('U3='):src.find("d['bce']")],ns)
CH={**ns['U3'],**ns['OB'],**ns['NB'],**ns['NA'],**ns['OAK'],**ns['LAG']}
d=pd.read_parquet(f'{R}/master_tablets.parquet')
d=d[d.genre.isin(['Administrative','Letter','Legal','Business / Contracts'])].copy()
d['bce']=np.where(d.ruler.isin(CH),d.ruler.map(CH)-(d.ryear.fillna(1).clip(lower=1)-1),np.nan)
C=[('Urukagina reform','3rd',2351,['ED IIIb']),('Naram-Sin reform','3rd',2230,['Old Akkadian']),('Šulgi 21','3rd',2072,['Ur III']),
   ('Puzriš-Dagān, Š39','3rd',2054,['Ur III']),('Ibbi-Suen 3, provinces lost','3rd',2024,['Ur III']),
   ('Hammurabi takes Larsa','2nd',1763,['Old Babylonian']),('Samsu-iluna loses the south','2nd',1739,['Old Babylonian']),
   ('Nabopolassar, independence','1st',626,['Neo-Babylonian']),('Cyrus takes Babylon','1st',539,['Neo-Babylonian','Achaemenid']),
   ('Darius I reorganisation','1st',521,['Neo-Babylonian','Achaemenid']),('Xerxes, end of archives','1st',484,['Achaemenid','Neo-Babylonian']),
   ('Sargon II to Sennacherib (by reign)','1st',705,['Neo-Assyrian'])]
rows=[]
for name,mil,yr,pers in C:
    g=d[d.period.isin(pers)&d.bce.notna()]
    b=g[g.bce.between(yr+1,yr+20)]; a=g[g.bce.between(yr-19,yr)]
    S=(set(b.site)&set(a.site))-{'unknown','uncertain'}
    bb=b[b.site.isin(S)]; aa=a[a.site.isin(S)]
    rows.append(dict(candidate=name,millennium=mil,date_bce=yr,before=len(bb),after=len(aa),sites=', '.join(sorted(S)),
        year_known=int(bb.ryear.notna().sum()+aa.ryear.notna().sum()),testable=(len(bb)>=30)&(len(aa)>=30)))
r=pd.DataFrame(rows); r.to_csv(f'{R}/turning/candidate_testability.csv',index=False); print(r.to_string())
