"""Pilot 4 (point 8): regime and tablet production.
(a) Ur III, year by year: number of dated tablets in the whole CDLI catalogue (photographed or not) per province, and the
    uniformity of administrative tablets (MAD of log h/w, photographs) per province and year (>= 20 tablets).
    Question: does format tighten when production intensifies (the 'production intensity' reading of standardization in
    craft studies: Costin 1991, Roux 2003), and does it track the regime's milestones (Puzriš-Dagan founded Šulgi 39;
    the last two reigns)?
(b) Neo-Babylonian and Achaemenid, reign by reign: dated tablets per regnal year, and the share of tall archival tablets.
(c) Across periods: production rate (catalogued tablets per century of the period) and regime type vs uniformity.
Absolute years: Ur III after Sallaberger (Ur-Namma 2110 ... Ibbi-Suen 2026-2003); first millennium standard dates."""
from _paths import WORK
import pandas as pd, numpy as np, re
from scipy.stats import spearmanr, kruskal
R=WORK
a=pd.read_csv(f'{R}/artifacts.csv',low_memory=False,usecols=['artifact_id','period','provenience','genres','dates'])
a['site']=a.provenience.fillna('unknown').str.replace(r'\s*\(.*\)','',regex=True).str.strip()
def parse(s):
    m=re.match(r'^([^.\d][^.]*?)\.(\d+)',str(s)); return (m.group(1).strip(),int(m.group(2))) if m else (None,None)
pr=a.dates.map(parse); a['ruler']=[p[0] for p in pr]; a['ry']=[p[1] for p in pr]
# ---------- (a) Ur III
U3={'Ur-Namma':2110,'Šulgi':2092,'Amar-Suen':2044,'Šū-Suen':2035,'Ibbi-Suen':2026}
u=a[a.period.str.startswith('Ur III',na=False)&a.ruler.isin(U3)&(a.ry>0)].copy()
u['bce']=u.ruler.map(U3)-(u.ry-1); u['prov']=u.site.replace({'Puzriš-Dagan':'Puzriš-Dagan','Drehem':'Puzriš-Dagan'})
prod=u.groupby(['bce','prov']).size().unstack(fill_value=0)
top=[c for c in ['Umma','Girsu','Puzriš-Dagan','Ur','Nippur','Irisagrig','Garšana'] if c in prod.columns]
prod=prod[top]; prod['all']=u.groupby('bce').size(); prod=prod.sort_index(ascending=False)
prod.to_csv(f'{R}/pilot4_ur3_production_by_year.csv')
d=pd.read_parquet(f'{R}/master_tablets.parquet')
du=d[(d.period=='Ur III')&d.ruler.isin(U3)&(d.ryear>0)&d.genre.eq('Administrative')&d.photo_hw.between(1/3,3)].copy()
du['bce']=du.ruler.map(U3)-(du.ryear-1); du['lh']=np.log(du.photo_hw)
def mad(x): return np.median(np.abs(x-np.median(x)))
fm=du.groupby(['site','bce']).agg(n=('lh','size'),MAD=('lh',mad),med=('lh','median')).reset_index()
fm=fm[fm.n>=20]; fm['production']=[prod.loc[b,s] if (s in prod.columns and b in prod.index) else np.nan for s,b in zip(fm.site,fm.bce)]
fm.to_csv(f'{R}/pilot4_ur3_format_by_year.csv',index=False)
rows=[]
for s,g in fm.groupby('site'):
    if len(g)>=8:
        r1=spearmanr(g.production,g.MAD)[0]; r2=spearmanr(-g.bce,g.MAD)[0]
        rows.append(dict(site=s,years=len(g),rho_production_vs_MAD=round(r1,3),rho_time_vs_MAD=round(r2,3),
                         MAD_before_S39=round(g[g.bce>2054].MAD.median(),3) if (g.bce>2054).sum() else np.nan,
                         MAD_S39_AS=round(g[(g.bce<=2054)&(g.bce>2035)].MAD.median(),3),MAD_SS_IS=round(g[g.bce<=2035].MAD.median(),3)))
UR=pd.DataFrame(rows); UR.to_csv(f'{R}/pilot4_ur3_summary.csv',index=False)
# ---------- (b) first millennium by reign
NB={'Nabopolassar':(626,21),'Nebuchadnezzar2':(605,43),'Nebuchadnezzar':(605,43),'Amēl-Marduk':(562,2),'Neriglissar':(560,4),'Nabonidus':(556,17),
    'Cyrus':(539,9),'Cyrus2':(539,9),'Cambyses':(530,8),'Cambyses2':(530,8),'Darius':(522,36),'Darius1':(522,36),'Xerxes':(486,21),'Xerxes1':(486,21),
    'Artaxerxes':(465,41),'Artaxerxes1':(465,41),'Darius2':(424,19)}
CAN={'Nebuchadnezzar':'Nebuchadnezzar2','Cyrus2':'Cyrus','Cambyses2':'Cambyses','Darius':'Darius1','Xerxes1':'Xerxes','Artaxerxes':'Artaxerxes1'}
f=a[a.period.str.contains('Neo-Babylonian|Achaemenid',na=False)&a.ruler.isin(NB)].copy(); f['ruler']=f.ruler.replace(CAN)
reign=f.groupby('ruler').size().rename('dated_tablets').to_frame()
reign['years']=[NB[r][1] for r in reign.index]; reign['start_bce']=[NB[r][0] for r in reign.index]; reign['per_year']=reign.dated_tablets/reign.years
df=d[d.period.isin(['Neo-Babylonian','Achaemenid'])&d.ruler.isin(NB)&d.genre.isin(['Administrative','Legal','Letter','Business / Contracts'])&d.photo_hw.between(1/3,3)].copy()
df['ruler']=df.ruler.replace(CAN)
reign=reign.join(df.groupby('ruler').agg(photographed=('id','size'),tall_share=('photo_hw',lambda x:(x>1.05).mean()),MAD=('photo_hw',lambda x:mad(np.log(x)))))
reign=reign.sort_values('start_bce',ascending=False); reign.round(3).to_csv(f'{R}/pilot4_first_millennium_by_reign.csv')
# ---------- (c) across periods
DUR={'ED IIIa':150,'ED IIIb':100,'Ebla':100,'Old Akkadian':200,'Ur III':108,'Early Old Babylonian':150,'Old Babylonian':255,'Old Assyrian':230,
     'Middle Babylonian':350,'Middle Assyrian':350,'Neo-Assyrian':300,'Neo-Babylonian':87,'Achaemenid':208,'Hellenistic':300}
REG={'ED IIIa':'city-state league','ED IIIb':'city-state','Ebla':'regional kingdom','Old Akkadian':'tributary empire','Ur III':'tributary empire',
     'Early Old Babylonian':'regional kingdoms','Old Babylonian':'territorial kingdom','Old Assyrian':'merchant city-state','Middle Babylonian':'territorial kingdom',
     'Middle Assyrian':'tributary empire','Neo-Assyrian':'tributary empire','Neo-Babylonian':'tributary empire','Achaemenid':'tributary empire','Hellenistic':'tributary empire (temple cities)'}
a['P']=a.period.str.extract(r'^([^\(]+?)\s*(?:\(|$)')[0].str.strip()
cat=a.P.value_counts()
P1=pd.read_csv(f'{R}/pilot1_period_table.csv',index_col=0)
P1.loc['Achaemenid']=P1.loc[['Achaemenid (Babylonia)','Achaemenid (Persepolis)']].mean(numeric_only=True)
C=pd.DataFrame({'catalogued':cat.reindex(list(DUR)),'duration_years':pd.Series(DUR)}); C['per_century']=100*C.catalogued/C.duration_years
C['regime']=pd.Series(REG); C=C.join(P1[['MAD','MAD_in_museum','VAEd_in_museum']])
C.round(3).to_csv(f'{R}/pilot4_periods_production.csv')
cc=C.dropna(subset=['MAD'])
res=dict(rho_rate_MAD=spearmanr(cc.per_century,cc.MAD_in_museum),rho_rate_VAEd=spearmanr(cc.per_century,cc.VAEd_in_museum),
         kruskal_regime_MAD=kruskal(*[g.MAD_in_museum.values for _,g in cc.groupby('regime') if len(g)>1]))
if __name__=='__main__':
    pd.set_option('display.width',200)
    print(prod.head(60).to_string()); print(UR.to_string()); print(reign.round(3).to_string()); print(C.round(3).to_string()); print(res)
