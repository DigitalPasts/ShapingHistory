"""Extract Seshat Equinox-2020 codes for the polities matching the paper's periods.
Source: seshat-equinox-23-10-20.csv (Zenodo 10526926, a copy of the Equinox-2020 release; CC BY-NC-SA).
Output: seshat_codes_long.csv (all variables) and seshat_codes_wide.csv (one row per polity, numeric codes)."""
from _paths import WORK
import pandas as pd, numpy as np
R=WORK
d=pd.read_csv(f'{R}/seshat/eq.csv',low_memory=False)
POL={'IqEDyn*':'Early Dynastic','IqAkkad':'Old Akkadian','IqUrIII':'Ur III','IqIsinL':'Isin-Larsa (Early OB)',
     'IqBabAm':'Old Babylonian (Amorite dynasty)','IqBabKs':'Kassite (Middle Babylonian)','IqNAssr':'Neo-Assyrian',
     'IqNeoBb':'Neo-Babylonian','IrAchae':'Achaemenid','IrSeleu':'Seleucid (Hellenistic)','IrMElm1':'Middle Elamite I',
     'IrMElm2':'Middle Elamite II','IrMElm3':'Middle Elamite III','TrBrzMD':'Old Assyrian colony (Anatolia MBA)',
     'TrHatOK':'Hittite Old Kingdom','TrHatNK':'Hittite New Kingdom','IrSukkE':'Early Sukkalmah','IrShima':'Shimashki'}
m=d[d.Polity.isin(POL)].copy(); m['period']=m.Polity.map(POL)
m.to_csv(f'{R}/seshat/seshat_codes_long.csv',index=False)
def num(v):
    v=str(v).strip().lower()
    if v in ('present','inferred present'): return 1.0
    if v in ('absent','inferred absent'): return 0.0
    if v in ('unknown','suspected unknown','nan',''): return np.nan
    try: return float(v.replace(',',''))
    except: return np.nan
m['vf']=m['Value.From'].map(num); m['vt']=m['Value.To'].map(num)
m['v']=m[['vf','vt']].mean(axis=1)
sc=m[m.Section.isin(['Social Complexity variables'])]
w=sc.groupby(['Polity','Variable']).v.mean().unstack()
w.insert(0,'period',w.index.map(POL))
w.to_csv(f'{R}/seshat/seshat_codes_wide.csv')
print(w.T.to_string())
