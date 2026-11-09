"""Pilot: do political turning points show up in tablet form, and in which features? (ShG, 3 Nov 2026: place turning points
on a timeline and correlate them with each VAE vector on its own, h/w, corners and proportions.)
Turning points are fixed in advance from the literature (middle chronology), before looking at the data:
  T1  Urukagina becomes ensi of Lagaš and issues his 'reforms' (c. 2351)      ED IIIb, Girsu, Lugalanda -> Urukagina
  T2  Urukagina takes the title lugal (his year 2)                              ED IIIb, Girsu, Urukagina ensi -> lugal
  T3  Naram-Sin -> Šar-kali-šarri (deified king to the crisis of Akkade, 2218)  Old Akkadian
  T4  Šulgi's reforms (Šulgi 21, 2072: army, calendar, standard accounts)       Ur III, all provinces
  T5  Puzriš-Dagān founded (Šulgi 39, 2054)                                     Ur III
  T6  Ibbi-Suen loses the provinces (Ibbi-Suen 3, 2024)                         Ur III
  T7  Hammurabi conquers Larsa (1763)                                           Old Babylonian, south
  T8  Samsu-iluna loses the south (Si 12, 1738; revolt of Rīm-Sîn II)           Old Babylonian
  T9  Nabopolassar -> Nebuchadnezzar II (605)                                   Neo-Babylonian
  T10 Cyrus takes Babylon (539)                                                 Neo-Babylonian -> Achaemenid
  T11 Xerxes crushes the Babylonian revolts (484)                               Achaemenid Babylonia
  T12 Sargon II -> Sennacherib (705)                                            Neo-Assyrian
For each turning point: dated archival tablets in a window before and after (same sites on both sides). For every feature
(12 VAE dimensions, log h/w, corner fill, thickness, rectangularity, taper, bulges): standardized shift
= (median after - median before) / pooled MAD, and a permutation p (2,000 draws; 'after' labels permuted within site), and a
dispersion shift (MAD after / MAD before). Also the macro view: per-period medians of every feature along the timeline.
Outputs: turning/tp_shifts.csv, turning/tp_macro.csv, turning/tp_heatmap.png, turning/tp_macro.png."""
from _paths import WORK
import numpy as np, pandas as pd, re, warnings; warnings.filterwarnings('ignore')
R=WORK; O=f'{R}/turning'; rng=np.random.default_rng(3)
d=pd.read_parquet(f'{R}/master_tablets.parquet')
ARCH=['Administrative','Letter','Legal','Business / Contracts']
d=d[d.genre.isin(ARCH)&d.photo_hw.between(1/3,3)].copy(); d['loghw']=np.log(d.photo_hw)
FE=[f'X{i}' for i in range(1,13)]+['loghw','corner_fill','thick_side','thick_end','rect','taper','side_bulge','end_bulge']
FE=[f for f in FE if f in d.columns]
U3={'Ur-Namma':2110,'Šulgi':2092,'Amar-Suen':2044,'Šū-Suen':2035,'Ibbi-Suen':2026}
OB={'Rim-Sin':1822,'Hammurapi':1792,'Samsu-iluna':1749,'Abi-ešuh':1711,'Ammi-ditana':1683,'Ammi-saduqa':1646,'Samsu-ditana':1625,'Warad-Sin':1834,'Sin-muballit':1812}
NB={'Nabopolassar':626,'Nebuchadnezzar2':605,'Nebuchadnezzar':605,'Amēl-Marduk':562,'Neriglissar':560,'Nabonidus':556,'Cyrus':539,'Cyrus2':539,
    'Cambyses':530,'Cambyses2':530,'Darius':522,'Darius1':522,'Xerxes':486,'Xerxes1':486,'Artaxerxes':465,'Artaxerxes1':465,'Darius2':424}
NA={'Sargon2':722,'Sennacherib':705,'Esarhaddon':681,'Assurbanipal':669,'Ashurbanipal':669}
OAK={'Sargon':2334,'Rimush':2278,'Naramsin':2254,'Shar-kali-sharri':2217}
LAG={'Enentarzi':2364,'Lugalanda':2358,'Urukagina_e':2351,'Urukagina_l':2350,'Urukagina':2351}
CH={**U3,**OB,**NB,**NA,**OAK,**LAG}
d['bce']=np.where(d.ruler.isin(CH),d.ruler.map(CH)-(d.ryear.fillna(1).clip(lower=1)-1),np.nan)
TP=[('T1 Urukagina ensi, "reforms"','ED IIIb',lambda g:g.ruler.isin(['Lugalanda','Enentarzi']),lambda g:g.ruler.isin(['Urukagina_e','Urukagina_l','Urukagina']),2351),
    ('T2 Urukagina becomes lugal','ED IIIb',lambda g:g.ruler.isin(['Urukagina_e']),lambda g:g.ruler.isin(['Urukagina_l']),2350),
    ('T3 Naram-Sin to Šar-kali-šarri','Old Akkadian',lambda g:g.ruler.eq('Naramsin'),lambda g:g.ruler.eq('Shar-kali-sharri'),2218),
    ('T4 Šulgi reforms (Š21)','Ur III',lambda g:g.bce.between(2073,2092),lambda g:g.bce.between(2055,2072),2072),
    ('T5 Puzriš-Dagān founded (Š39)','Ur III',lambda g:g.bce.between(2055,2072),lambda g:g.bce.between(2036,2054),2054),
    ('T6 Ibbi-Suen loses provinces (IS3)','Ur III',lambda g:g.bce.between(2025,2040),lambda g:g.bce.between(2010,2024),2024),
    ('T7 Hammurabi conquers Larsa','Old Babylonian',lambda g:g.bce.between(1764,1790),lambda g:g.bce.between(1739,1763),1763),
    ('T8 Samsu-iluna loses the south','Old Babylonian',lambda g:g.bce.between(1739,1763),lambda g:g.bce.between(1700,1738),1738),
    ('T9 Nabopolassar to Nebuchadnezzar','Neo-Babylonian',lambda g:g.bce.between(606,626),lambda g:g.bce.between(580,605),605),
    ('T10 Cyrus takes Babylon','NB+Ach',lambda g:g.bce.between(540,560),lambda g:g.bce.between(515,539),539),
    ('T11 Xerxes and the revolts (484)','NB+Ach',lambda g:g.bce.between(485,522),lambda g:g.bce.between(400,484),484),
    ('T12 Sargon II to Sennacherib','Neo-Assyrian',lambda g:g.ruler.eq('Sargon2'),lambda g:g.ruler.isin(['Sennacherib']),705)]
def mad(x): x=np.asarray(x,float); return np.median(np.abs(x-np.median(x)))
rows=[]
for name,per,fb,fa,yr in TP:
    g=d[d.period.isin(['Neo-Babylonian','Achaemenid'])] if per=='NB+Ach' else d[d.period==per]
    b=g[fb(g)].copy(); a=g[fa(g)].copy(); b['post']=0; a['post']=1
    sites=set(b.site.dropna())&set(a.site.dropna()); h=pd.concat([b,a]); h=h[h.site.isin(sites)]
    if h.post.sum()<15 or (1-h.post).sum()<15: rows.append(dict(tp=name,year=yr,n_before=int((1-h.post).sum()),n_after=int(h.post.sum()),note='too few dated tablets')); continue
    for f in FE:
        x=h[[f,'post','site']].dropna()
        if x.post.sum()<15 or (1-x.post).sum()<15: continue
        s=mad(x[f])*1.4826 or x[f].std()
        obs=(x[x.post==1][f].median()-x[x.post==0][f].median())/s
        disp=mad(x[x.post==1][f])/max(mad(x[x.post==0][f]),1e-9)
        null=[]
        for _ in range(2000):
            p=x.groupby('site').post.transform(lambda v: rng.permutation(v.values))
            null.append((x[p==1][f].median()-x[p==0][f].median())/s)
        pval=(np.sum(np.abs(null)>=abs(obs))+1)/(len(null)+1)
        rows.append(dict(tp=name,year=yr,feature=f,n_before=int((1-x.post).sum()),n_after=int(x.post.sum()),sites=len(sites),shift=round(obs,3),disp_ratio=round(disp,3),p=round(pval,4)))
T=pd.DataFrame(rows); T.to_csv(f'{O}/tp_shifts.csv',index=False)
# Benjamini-Hochberg within the table
t=T.dropna(subset=['p']).copy(); t=t.sort_values('p'); m=len(t); t['q']=(t.p*m/np.arange(1,m+1))[::-1].cummin()[::-1].clip(upper=1); T=T.merge(t[['tp','feature','q']],on=['tp','feature'],how='left')
T.to_csv(f'{O}/tp_shifts.csv',index=False)
# macro timeline
MID={'ED IIIa':2550,'ED IIIb':2400,'Ebla':2350,'Old Akkadian':2250,'Ur III':2060,'Early Old Babylonian':1925,'Old Babylonian':1750,'Old Assyrian':1880,
     'Middle Babylonian':1300,'Middle Assyrian':1250,'Neo-Assyrian':750,'Neo-Babylonian':580,'Achaemenid':450,'Hellenistic':200}
M=d[d.period.isin(MID)].groupby('period')[FE].median().assign(mid=lambda x: x.index.map(MID)).sort_values('mid',ascending=False)
Ms=d[d.period.isin(MID)].groupby('period')[FE].agg(mad).add_suffix('_mad')
M=M.join(Ms); M['n']=d[d.period.isin(MID)].groupby('period').size(); M.to_csv(f'{O}/tp_macro.csv')
print(T[T.feature.notna()].pivot(index='feature',columns='tp',values='shift').round(2).to_string())
print(T[T.q<0.05].groupby('tp').feature.apply(list).to_string())
print(T.groupby('tp')[['n_before','n_after']].max().to_string())
