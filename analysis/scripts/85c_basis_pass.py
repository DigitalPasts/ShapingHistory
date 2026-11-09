"""Systematic confidence pass (4 Nov 2026, ShG's rubric). Every statement that had no hand-coded basis was read again and
given: basis (assertion / fragmentary / documented / substantial), genre (Sitz im Leben of the underlying sources) and,
where the quote or note names it, the archive. Codes: first letter A/F/D/S = basis; second letter a admin, l legal,
L letters, r royal, t literary, x lexical/school, g archaeology, m mixed. The reading is recorded in
centralization/basis_pass_codes.txt (statement number in the export order of this script) and written to
centralization/basis_pass.csv, which 85b_build_scores_v2.py merges by statement id.
Archive: matched from site and archive names in the quote, note and citation (ARCH below); 'unspecified' otherwise.
The archive only matters for the dominant-archive rule in 85b, so an unmatched statement is never down-weighted."""
from _paths import SCRIPTS, WORK
import runpy, glob, re, pandas as pd
S=SCRIPTS; OUT=WORK+'/centralization'
rows=[]
for f in sorted(glob.glob(f'{S}/81_lit_evidence_*.py')):
    d=runpy.run_path(f)
    for name in ['E','UR3','RIMSIN','ACH']:
        for e in d.get(name,[]):
            r=dict(e); r.setdefault('period',d.get('P')); rows.append(r)
ev=pd.DataFrame(rows)
todo=ev[ev.basis.isna()].copy().reset_index(drop=True)
todo['sid']=todo.apply(lambda r:f"{r['period']}|{r['param']}|{r['key']}|{str(r['quote'])[:50]}",axis=1)
codes={}
for tok in open(f'{OUT}/basis_pass_codes.txt').read().split():
    m=re.match(r'(\d+)([AFDS])([alLrtxgm])$',tok); codes[int(m.group(1))]=(m.group(2),m.group(3))
B={'A':'assertion','F':'fragmentary','D':'documented','S':'substantial'}
G={'a':'admin','l':'legal','L':'letters','r':'royal','t':'literary','x':'lexical','g':'archaeology','m':'mixed'}
ARCH=[(r'Girsu|Lagaš|Lagash|Bau\b|Bawa|Ba-?U\b|e2-mi2|Emunus','Girsu'),(r'\bUmma\b','Umma'),(r'\bAdab\b','Adab'),(r'Nippur|Ekur','Nippur'),
 (r'Fara|Šuruppag|Šuruppak|Shuruppag','Fara'),(r'Abu Salabikh','Abu Salabikh'),(r'\bEbla','Ebla palace G'),
 (r'Puzriš-Dagan|Puzris-Dagan|Puzriš-Dagān|Drehem','Puzriš-Dagān, Ur (royal)'),(r'Persepolis|Fortification','Persepolis Fortification and Treasury'),
 (r'Eanna|Ebabbar','Eanna (Uruk), Ebabbar (Sippar)'),(r'Murašû|Murasu|Egibi','Babylonian family and Murašû archives; Eanna/Ebabbar'),
 (r'Kaneš|Kanesh|Kaniš|kārum|karum','Kaneš merchant houses'),(r'\bMari\b','Mari palace; Larsa crown'),(r'Šamaš-ha?ḫ?zir|Šamaš-hazir|Sîn-iddinam|Sin-iddinam','Mari palace; Larsa crown'),
 (r'Nineveh|Kalhu|Kalḫu','Nineveh royal archives and library'),(r'Haft T[ae]p+e|Kabnak','Haft Tepe'),(r'Isin craft|craft archive|Isin archive','Isin craft archive; Larsa; Ešnunna'),
 (r'Offerings House|House of Offerings|gina.?u|Dur-?Katlimmu|Dūr-Katlimmu|Sabi Abyad','Assur, Dūr-Katlimmu, Tell Sabi Abyad state archives'),
 (r'Bīt Rēš|Bit Res|Rēš|Esagil','Rēš and Esagil temple archives')]
def arch(r,g):
    t=' '.join(str(r.get(c) or '') for c in ['quote','note','where'])
    hits=[]
    for pat,a in ARCH:
        if re.search(pat,t) and a not in hits: hits.append(a)
    if hits: return '; '.join(hits[:3])
    if g=='royal': return 'royal inscriptions'
    return 'unspecified'
out=[]
for i,r in todo.iterrows():
    b,g=codes[i]; out.append(dict(sid=r.sid,period=r.period,param=r.param,key=r.key,basis=B[b],genre=G[g],archive=arch(r,G[g])))
P=pd.DataFrame(out); P.to_csv(f'{OUT}/basis_pass.csv',index=False)
print(len(todo),'statements;',len(codes),'codes'); print(P.basis.value_counts().to_dict()); print(P.genre.value_counts().to_dict())
print((P.archive!='unspecified').sum(),'with an archive')
