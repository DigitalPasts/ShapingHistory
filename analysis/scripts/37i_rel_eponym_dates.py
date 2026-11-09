"""Old Assyrian eponym dates (ShG, 9 Nov 2026).
1) REL: the Revised Eponym List of Barjamovic, Hertel and Larsen 2012 (Ups and Downs at Kanesh, PIHANS 120,
   Appendix 1, pp. 92-97), transcribed by hand from the page images into oare/rel_bhl2012_raw.tsv
   (REL number, KEL G Günbattı, KEL G revised, MEC, eponym as printed). Absolute year (Middle Chronology,
   BHL 2012 section 1.7): BCE = 1973 - REL (REL 1 = 1972, REL 138 = 1835, REL 255 = 1718). King column from the
   reign table on p. 91.
2) Eponyms named in the OARE transliterations of our photographed Old Assyrian tablets (37h) are read here one
   by one (table EPON below: tablet, eponym as written, REL candidates, basis). A tablet is dated only when one
   REL entry fits: name and patronym agree, or the name occurs once in the REL before the destruction of level II
   (REL <= 142), since museum Old Assyrian tablets are level II unless the patronym says otherwise. Homonyms
   without a patronym keep their candidate list and a year range, not a year.
Outputs: oare/rel_bhl2012.csv, oare/oa_eponym_dates.csv"""
from _paths import WORK
import pandas as pd, re
R=WORK
rel=pd.read_csv(f'{R}/oare/rel_bhl2012_raw.tsv',sep='\t',dtype=str)
rel['rel']=rel.rel.astype(int); rel['bce']=1973-rel.rel
reigns=[('Erišum I',1,40),('Ikūnum',41,55),('Šarru-kēn',56,95),('Puzur-Aššur II',96,103),('Narām-Suen',104,137),
        ('Narām-Suen / Erišum II',138,157),('Erišum II',158,164),('Šamšī-Adad I',165,197),('Išme-Dagan I',198,237)]
rel['king']=rel.rel.map(lambda r: next((k for k,a,b in reigns if a<=r<=b),'after Išme-Dagan I (uncertain)'))
p=rel.eponym_as_printed.str.extract(r'^(.*?)(?:\s+\(?s\.\s+(.*?)\)?)?(\*)?$')
rel['eponym']=p[0].str.strip(); rel['patronym']=p[1]
rel['level']=rel.rel.map(lambda r:'II' if r<=138 else 'Ib')
rel=rel[['rel','bce','king','level','eponym','patronym','eponym_as_printed','kelg_gunbatti','kelg_revised','mec']]
rel.to_csv(f'{R}/oare/rel_bhl2012.csv',index=False)

# tablet (CDLI P-number), eponym as written in OARE, REL candidates, basis
EPON=[
 (332983,'i-dí-a-ḫu-um',[110],'name unique'),
 (360977,'i-dí-na-ḫi-im',[110],'name unique'),
 (333894,'aḫ-mar-ší',[79],'name unique'),(359055,'aḫ-mar-ší',[79],'name unique'),(361120,'aḫ-mar-ší',[79],'name unique'),
 (357410,'ša qá-té iš-ma-a-šùr DUMU é-a-dan',[119],'name + patronym'),
 (357653,'i-dí-a-šùr DUMU ku-bi4-dí',[81],'name + patronym'),(359968,'i-dí-a-šur DUMU ku-bi-dí',[81],'name + patronym'),
 (357657,'PUZUR4-{d}MUŠ',[85],'name unique before REL 142 (167 is level Ib)'),
 (359280,'ša qá-té PUZUR4-{d}MUŠ',[85],'name unique before REL 142'),
 (359950,'PUZUR4-ni-ra-aḫ',[85],'name unique before REL 142'),(333905,'PUZUR4-ni-ra-aḫ',[85],'name unique before REL 142'),
 (359322,'PUZUR4-ni-ra-aḫ',[85],'name unique before REL 142'),
 (357763,'a-šùr-ba-lá-aṭ',[137],'name unique'),
 (357778,'šu-ḫu-bur',[47,88],'homonyms'),
 (357779,'en-na-ma-nim',[113],'name unique'),
 (357790,'ša qá-té en-na-sú-en6 DUMU šu-a-šur',[107],'name + patronym'),(357796,'i-na-sú-en6 DUMU šu-a-šùr',[107],'name + patronym'),
 (357401,'en-na-sú-en6 DUMU šu-a-šur',[107],'name + patronym'),
 (357795,'en-na-sú-en6 DUMU šu-IŠTAR',[115],'name + patronym'),
 (357816,'en-na-sú-en6 DUMU i-dí-a-bi-im',[136],'name + patronym'),
 (357794,'bu-zu-zu',[87],'name unique'),(359186,'bu-zu-zu',[87],'name unique'),(359393,'bu-zu-zu',[87],'name unique'),
 (357798,'DINGIR-šu-GAL',[89],'name unique'),
 (357800,'ku-bi4-a',[97],'name unique'),(361047,'ku-bi-a',[97],'name unique'),
 (357804,'šu-sú-en6 / a-šùr-ma-lik (two eponyms on one tablet)',[36,104,52,56,57,105,134],'homonyms'),
 (357814,'ša qá-té-e sú-kà-li-a',[80],'name unique'),
 (358243,'e-lá-li',[92],'name unique'),
 (358259,'i-dí-a-bu-um DUMU na-ar-bi4-tim',[93],'name + patronym'),
 (358461,'a-šùr-i-mì-tí',[106,124],'homonyms'),(359214,'a-šur-i-mì-tí',[106,124],'homonyms'),(357400,'a-šùr-i-mì-tí',[106,124],'homonyms'),
 (359261,'a-šur-i-mì-tí ma-lá-ḫu-um',[106],'name + title malāhum'),
 (358490,'šu-ra-ma',[132],'name unique'),(359074,'šu-ra-ma',[132],'name unique'),
 (358506,'ì-lí-dan',[98,123],'homonyms'),(359103,'ì-lí-dan',[98,123],'homonyms'),
 (357802,'ša qá-té ì-lí-dan DUMU ú-zu-a',[123],'name + patronym (s. Azuza / Azua)'),
 (358508,'i-dí-a-bu-um',[93,122],'homonyms'),(359189,'i-dí-a-bu-um',[93,122],'homonyms'),(359198,'i-dí-a-bi4-im',[93,122],'homonyms'),
 (361171,'i-dí-a-bi4-im',[93,122],'homonyms'),(387679,'i-dí-a-bu-um',[93,122],'homonyms'),
 (359066,'DUG-a-šur DUMU ú-zu-a',[131],'name + patronym'),
 (359071,'i-ku-pí-IŠTAR',[101],'name unique before REL 142 (202 is level Ib)'),(359120,'i-ku-pí-IŠTAR',[101],'name unique before REL 142'),
 (359964,'i-ku-pí-IŠTAR DUMU i-ku-a',[101],'name + patronym'),
 (359270,'bu-zu-ta-a',[22,102],'homonyms'),
 (359150,'ša qá-té šu-da-a DUMU en-na-nim',[82],'name + patronym'),
 (359941,'a-al-DUG DUMU pì-lá-aḫ-a-a',[83],'name + patronym'),(359952,'a-al-DUG DUMU ib-ni-lí',[83],'name + variant patronym (BHL 2012 n. 1)'),
 (393107,'a-al-DU10',[83],'name unique'),
 (359976,'a-šur-na-da DUMU ì-lí-bi4-na-ni',[100],'name + patronym'),
 (361136,'a-šur-na-da DUMU PÚZUR-a-na',[96],'name + patronym'),
 (361117,'a-gu5-tum',[108],'name unique (Akutum)'),
 (361635,'pì-lá-aḫ-sú-en6 DUMU i-ku-nim',[239],'name + patronym (level Ib)'),
 (390554,'a-šur-i-dí',[95],'name unique (Aššur-iddin)'),
 (357783,'da-né-a DUMU a-ba-qar',[135],'name + patronym'),
]
# read in OARE but not an eponym of the REL, or not an eponym formula (li-mì-im 'thousand', broken, letters):
NOT=[260378,333893,333923,333932,357356,357499,357510,357533,357539,357700,358276,359335,361160,361566,390568,216609,390566,359099]
E=pd.DataFrame(EPON,columns=['id','eponym_written','rel_candidates','basis'])
E['n_cand']=E.rel_candidates.str.len()
E['rel']=E.rel_candidates.map(lambda c:c[0] if len(c)==1 else None)
E['bce']=E.rel.map(lambda r:1973-r if pd.notna(r) else None)
E['bce_range']=E.rel_candidates.map(lambda c:f'{1973-max(c)}-{1973-min(c)}')
E=E.merge(rel[['rel','eponym','patronym','king']],on='rel',how='left')
E['rel_candidates']=E.rel_candidates.map(lambda c:'/'.join(map(str,c)))
E['source']='OARE transliteration; REL of Barjamovic, Hertel and Larsen 2012'
E.to_csv(f'{R}/oare/oa_eponym_dates.csv',index=False)
print('REL rows',len(rel),'| tablets read',len(E)+len(NOT),'| eponym of REL',len(E),'| dated to one year',E.rel.notna().sum(),
      '| homonyms left as range',E.rel.isna().sum(),'| not an REL eponym / no formula',len(NOT))
print(E[E.rel.notna()].groupby('king').size().to_string()); print('BCE span',E.bce.min(),E.bce.max())
