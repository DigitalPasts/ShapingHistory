"""Archives and known tablet collections per period (ShG, 9 Nov 2026: "add to the assessment the overview of archives and
known tablet collections ... especially in Vita, History of Akkadian 2021 ... but also specialized articles that survey
periods on their own").

Each entry: one archive or text group, with its findspot, the institution that kept it, its size as the survey gives it,
and a quoted passage with page. Vita (ed.) 2021 chapters are cited by chapter author (printed pages; pdf n = p. n+48).
'sample_site' is the CDLI provenience name used in our photographed sample, so the overview can be set against the sample.
Output: centralization/archive_overview.csv (entries), archive_sample_compare.csv (literature size vs our photographs,
site by site, where the literature gives numbers), archive_period_notes.csv (what survives and what is lost, per period),
and archive_dispersal.csv (how many museums hold the photographed tablets of each period).
"""
from _paths import LIT, WORK
import re, json, unicodedata, pandas as pd, numpy as np
T=LIT+'/txt'; OUT=WORK+'/centralization'
VITA='Vita_2021_HAL.txt'
F=dict(vita=VITA,bram='02_Bramanti_text_COMPLETED.txt',archi='Archi_2015_Ebla_Archives.txt',
       molina='Molina_2016_Archives_and_bookkeeping_in_Southern_Me.txt',charpin='Charpin, D. 2014 The Historian and the Old Babylonian Archives.txt',
       foster='Foster B. R. -1982-Archives and Record-keeping in Sargonic Mesopotamia (ZA 72, 1982) 1-27.txt',
       jursa="Jursa,_Michael_Aspects_of_the_Economic_History_of_Babylonia_in_the_First_Millennium_BC_Economic_Geography,_Economic_Mentalities,_Agriculture,_the_Use_of_Money_and_t.txt",
       henk='Henkelman.Achaemenid_Heartland-libre.txt',stol='PIHANS-54 Stolper, Matthew W. - Entrepreneurs and Empire. The Murasu Archive. PIHANS 54, 1985 1.txt',
       mon="SANER 14 Monerie, J. 2017 L'économie de la Babylonie à l'époque hellénistique (IVème - IIème siècle avant J.C.).txt",
       doty='Diss. 1977 Yale - Doty, Laurence T. - Cuneiform Archives from Hellenistic Uruk.txt',hout='van den Hout 2020 A History of Hittite Literacy.txt',
       ew='Alvarez-Mon, Basello, Wicks - The Elamite World 2018.txt',glass='Glassner 1991 les textes de Haft Tepe, la Susiane et lElam au 2eme mill, RAI 36 MHEO 1.txt')
A=[]
def a(period,archive,site,kind,n,span,genres,key,where,quote,src,sample_site=None,note=''):
    A.append(dict(period=period,archive=archive,site=site,kind=kind,n=n,span=span,genres=genres,key=key,where=where,quote=quote,src=src,sample_site=sample_site,note=note))
# ---------------- ED IIIa
a('ED IIIa','Šuruppak (Fara) city archives','Šuruppak','mixed',900,'c. 2600-2500','administrative; lexical','bramantiTaxationEarlyMesopotamia2020','p. 25, n. 2',
  'ED IIIa Fara: 900; ED IIIa Abu Salabikh: 500','bram','Shuruppak','Sommerfeld (Vita 2021, p. 530) gives "ca. 1000 texts".')
a('ED IIIa','Šuruppak (Fara)','Šuruppak','mixed',1000,'c. 2570-2470','administrative; lexical; literary','sommerfeldOldAkkadian2021','p. 530',
  'The same is true of Šuruppak (Fara) [...] where the most copious finds—ca. 1000 texts—have been made.','vita',None)
a('ED IIIa','Abu Ṣalābīḫ tablets','Abu Ṣalābīḫ','school',500,'ED IIIa','lexical; literary','sommerfeldOldAkkadian2021','p. 531',
  'The majority of the more than 500 tablets and fragments that can be dated to the ed iiia period consists of lexical and literary texts.','vita','Abu Salabikh')
# ---------------- ED IIIb
a('ED IIIb','Girsu: é-mí / Bau household','Girsu','temple',1800,'c. 2350-2315 (one household, c. 20 years)','administrative','bramantiTaxationEarlyMesopotamia2020','p. 25, n. 2',
  'ED IIIb Ĝirsu/Lagaš: 1,800; ED IIIb Umma: 1,100; ED IIIb Adab: 500; ED IIIb Nippur: 450','bram','Girsu',
  'The same note gives Umma 1,100, Adab 500 and Nippur 450 (rows below). Schrakamp and Zólyomi 2025 p. 93: nearly all Girsu texts are from one household.')
a('ED IIIb','Umma / Zabalam','Umma','mixed',1100,'ED IIIb','administrative','bramantiTaxationEarlyMesopotamia2020','p. 25, n. 2','ED IIIb Umma: 1,100','bram','Umma')
a('ED IIIb','Adab','Adab','mixed',500,'ED IIIb','administrative','bramantiTaxationEarlyMesopotamia2020','p. 25, n. 2','ED IIIb Adab: 500','bram','Adab')
a('ED IIIb','Nippur','Nippur','mixed',450,'ED IIIb','administrative','bramantiTaxationEarlyMesopotamia2020','p. 25, n. 2','ED IIIb Nippur: 450','bram','Nippur')
# ---------------- Ebla
a('Ebla','Palace G archives (central archive L. 2769 and offices)','Ebla','palace',3250,'c. 40-50 years before the destruction of Palace G','administrative; lexical; letters; treaties','archiEblaItsArchives2015','p. 84',
  'According to the inventory numbers, the central archive included 1,757 tablets, in large part well preserved, 4,875 fragments, and several thousand very small fragments. In total, the number of the tablets of the central archive and the other administrative offices may be estimated at about 3,000/3,500 for a period of forty years.','archi','Ebla')
a('Ebla','Palace G archives','Ebla','palace',None,'c. 50 years','administrative; lexical','koganEblaite2021','p. 664','The texts cover a period of approximately 50 years','vita',None,
  'All Ebla texts of the period come from one palace (Kogan and Krebernik in Vita 2021, pp. 664-665).')
# ---------------- Old Akkadian
for site,n,ss in [('Girsu',2300,'Girsu'),('Adab',2300,'Adab'),('Umma',700,'Umma'),('Nippur',650,'Nippur')]:
    a('Old Akkadian',f'{site} Sargonic archives',site,'state' if site!='Nippur' else 'mixed',n,'Sargonic','administrative','bramantiTaxationEarlyMesopotamia2020','p. 25, n. 2',
      'Sargonic Ĝirsu/Lagaš: 2,300; Sargonic Umma: 700; Sargonic Adab: 2,300; Sargonic Nippur: 650','bram',ss)
a('Old Akkadian','household archives (Umma, Girsu, Mesag)','several','state',None,'Sargonic','administrative','fosterArchivesRecordkeepingSargonic1982','p. 9',
  'Household archives consist usually of a single important circle of documentation, for example, management of land and draft animals, production and distribution of food, sustenance of people involved in this process','foster',None)
# ---------------- Ur III (Molina 2016 §18, provenanced administrative texts; doubtful ascriptions in brackets there)
U=dict(Umma=29940,Girsu=26619,**{'Puzriš-Dagān':15647},Ur=4297,Nippur=3697,**{'GARšana':1507,'Irisaĝrig':1148})
SS={'Puzriš-Dagān':'Puzriš-Dagan','GARšana':'Garšana','Irisaĝrig':'Irisagrig'}
KIND={'Umma':'provincial','Girsu':'provincial','Irisaĝrig':'provincial','Puzriš-Dagān':'royal','Ur':'royal','Nippur':'temple and private','GARšana':'estate'}
for s,n in U.items():
    a('Ur III',f'{s} archive',s,KIND[s],n,'Ur III','administrative','molinaArchivesBookkeepingSouthern2016','§18',
      'At present, 27 sites have been identified as the provenance of Ur III administrative texts','molina',SS.get(s,s),f'Molina §18 counts {n:,} texts for {s}.')
a('Ur III','all archives','27 sites','state',120000,'2110-2003','administrative','molinaArchivesBookkeepingSouthern2016','abstract',
  'It is estimated that some 120,000 documents, plus an indeterminate number of texts stored in the Iraq Museum, are currently kept in collections all over the world. Unfortunately, most of them are deprived of archaeological context','molina',None)
a('Ur III','archive types','','mixed',None,'','','molinaArchivesBookkeepingSouthern2016','§26',
  'Thus we have large quantities of texts from private archives (Nippur, Tūram-ilī archive, SI.A-a archive); rural estate archives (Aradĝu archive, Šu-Eštar archive, GARšana); a temple archive (Nippur); provincial archives (Umma, Girsu, Irisaĝrig); and archives from royal institutions (Ur and Puzriš-Dagān).','molina',None)
# ---------------- Old Babylonian (Streck in Vita 2021, pp. 994-998: administrative texts = letters and documents, by site)
OB=[('Mari','Mari palace','palace',15000,'Mari','Mari: Charpin, “Archives babyloniennes”, mentions the number of 8.666 published texts from Mari.','p. 995',
     'Lowest published estimate of texts excavated (Margueron); Durand gives 20,000 + several thousand fragments.'),
    ('Sippar region','Sippar (Ebabbar, nadītum cloister, families)','mixed',6000,'Sippar-Yahrurum','Sippar: Dekiere, Old Babylonian Real Estate, 3: 6.000 texts from the Sippar region.','p. 996',''),
    ('Šaduppûm','Šaduppûm (Tell Harmal) administration','state',3100,'Šaduppum','Šaduppum: van Koppen, “Šaduppûm”, 488 §2: ca. 3.000 tablets found in regular excavations','p. 996',''),
    ('Larsa','Larsa letters and crown documents','palace',3780,'Larsa','a total of 1.780 texts (letters). For texts from Larsa kept in Yale (at least 2.000 dated texts) see below under Yale.','p. 995',''),
    ('Nippur','Nippur family archives','private',1826,'Nippur','altogether 1.826 texts','p. 996','Administrative only; Nippur school texts are counted separately by Streck.'),
    ('Kiš','Kiš and Ḫursagkalama','mixed',1600,'Kish','Together from Kiš ca. 1.600 texts.','p. 995',''),
    ('Uruk','Uruk','mixed',1066,'Uruk','together 1.066 texts','p. 997',''),
    ('Ur','Ur family archives','private',935,'Ur','Together: 935 texts.','p. 997',''),
    ('Isin','Isin','mixed',1603,'Isin','Isin: Isin i–iv: 923 texts. For further Isin texts (more than 700 dated) see Yale, below.','p. 995','923 excavated + c. 680 dated in Yale.'),
    ('Babylon','Babylon','mixed',1160,'Babylon','This means that the total of administrative texts amounts to ca. 800 texts.','p. 994','+ c. 360 dated texts in Yale.')]
for site,arch,kind,n,ss,q,w,nt in OB: a('Old Babylonian',arch,site,kind,n,'c. 2000-1600','letters; legal; administrative','streckOldBabylonian2021',w,q,'vita',ss,nt)
a('Old Babylonian','all administrative texts','c. 60 sites','mixed',50000,'2000-1600','letters; legal; administrative','streckOldBabylonian2021','p. 997',
  'The figures given above add up to ca. 35.377 (published and unpublished) texts [...] without Mari, including the published texts from Mari to ca. 44.042 texts, including the lowest figure of texts excavated in Mari given in the secondary literature to slightly more than 50.000 ob administrative texts.','vita',None)
a('Old Babylonian','family archives','','private',None,'','legal; letters','charpinHistorianOldBabylonian2014','p. 26',
  'These come no longer solely from large institutions, such as palaces and temples, as is largely the case during the third millennium. The first half of the second millennium yields numerous family archives from the houses of individuals – a clear innovation.','charpin',None)
a('Old Babylonian','institutional archives','','palace',None,'','administrative','charpinHistorianOldBabylonian2014','p. 27',
  'the span of time covered by this last group (large institutions) is noticeably shorter. This is because, for the most part, they contain only short-term documents, which were sorted out on a regular basis.','charpin',None)
# ---------------- Early Old Babylonian (no survey separates the early sites; Streck's counts for the sites that dominate our early sample)
for site,n,ss,q,w in [('Nērebtum',570,'Nerebtum','Nērebtum: Miglus, “Nērebtum”, 212: 280 tablets + perhaps the 290 tablets published in ucp 10/1: 570 texts.','p. 996'),
                      ('Tuttul',382,'Tuttul','Tuttul: Krebernik, Tall Biʿa/Tuttul ii: 382 texts.','p. 997'),
                      ('Isin',923,'Isin','Isin: Isin i–iv: 923 texts.','p. 995')]:
    a('Early Old Babylonian',site,site,'mixed',n,'OB (not split by sub-period)','administrative','streckOldBabylonian2021',w,q,'vita',ss,'Streck does not separate early from late OB; counts are for the whole OB period at the site.')
# ---------------- Old Assyrian
a('Old Assyrian','Kaneš merchant houses','Kaneš','private',22300,'c. 1930-1720','letters; legal; private records','kouwenbergOldAssyrian2021','p. 1105',
  'According to data collected by C. Michel, approximately 22,300 tablets had been unearthed in Kültepe alone by 2003','vita','Kanesh')
a('Old Assyrian','Kaneš merchant houses','Kaneš','private',None,'','','kouwenbergOldAssyrian2021','pp. 1103-1104',
  'Some 40 private houses belonging to merchant [...] families have been excavated so far, which contained the archives of several generations of merchants. Most oa texts come from these archives.','vita',None)
a('Old Assyrian','provenance of the Kaneš tablets','Kaneš','private',None,'','','kouwenbergOldAssyrian2021','p. 1105',
  'About 4,000 of the oa tablets come from illicit digging, about 1,000 were excavated by B. Hrozný in the 1920s, and the rest stem from the official excavations conducted since 1948 by the Turkish Historical Society.','vita',None,
  'Our photographs come mostly from the Hrozný (Prague) and old-market (Louvre, Berlin) groups.')
# ---------------- Middle Babylonian
a('Middle Babylonian','Nippur (governor and temple offices)','Nippur','state',12000,'1356-1223 (bulk)','administrative','vansoldtMiddleBabylonian2021','p. 1043, n. 23',
  'According to Brinkman, Materials, 41 f., there are about twelve thousand inscriptions and inscribed fragments from Nippur, most of which are administrative.','vita','Nippur')
a('Middle Babylonian','Nippur, publication state','Nippur','state',None,'','','vansoldtMiddleBabylonian2021','p. 1041','Although most of the texts from Nippur remain unpublished','vita',None)
a('Middle Babylonian','Dūr-Enlilē estate','Dūr-Enlilē','estate',776,'Kassite','administrative','vansoldtMiddleBabylonian2021','p. 1042, n. 17',
  'See now also Elena Devecchi, Middle Babylonian Texts in the Cornell Collections. ii. The Earlier Kings (Winona Lake: Eisenbrauns, 2020), editing 338 texts.','vita',None,'438 texts in van Soldt 2015 + 338 in Devecchi 2020.')
a('Middle Babylonian','Babylon private houses','Babylon','private',210,'1350-1150','legal; administrative','vansoldtMiddleBabylonian2021','p. 1041, n. 9',
  'Nine of these (M1–9) are archives found in private houses','vita','Babylon')
a('Middle Babylonian','Dūr-Kurigalzu','Dūr-Kurigalzu','palace',225,'Kassite','administrative','vansoldtMiddleBabylonian2021','p. 1042, n. 18',
  'According to Brinkman, Materials, 43, the number of inscribed objects found in Dūr-Kurigalzu is 225.','vita','Dur-Kurigalzu')
# ---------------- Middle Assyrian
a('Middle Assyrian','Assur and Kār-Tukultī-Ninurta','Assur','mixed',None,'13th-11th c.','administrative; private; library','jakobMiddleAssyrian2021','p. 1138',
  'The greatest number of texts came from the Assyrian capital Assur and the neighbouring residence Kār-Tukultī-Ninurta.','vita','Assur',
  'Only part of Assur was excavated: "it is estimated that only 10% of existing texts have been unearthed" (same page).')
a('Middle Assyrian','provincial archives (Dūr-Katlimmu, Ḫarbe, Sabi Abyad, Šibaniba, Rimah ...)','several','state',1500,'13th-12th c.','administrative; letters','jakobMiddleAssyrian2021','p. 1138',
  'All together, these sites have not even yielded one and a half thousand texts and fragments.','vita',None)
a('Middle Assyrian','published corpus','','mixed',600,'','','jakobMiddleAssyrian2021','p. 1143',
  'In 1971, when W. Mayer released his Middle Assyrian grammar, not more than approximately 600 published texts were available for analysis.','vita',None)
# ---------------- Neo-Assyrian
a('Neo-Assyrian','Nineveh (Kuyunjik collection): palace archives and library','Nineveh','palace',25000,'7th c. mostly','letters; legal; administrative; scholarly','falesNeoAssyrian2021','p. 1360, n. 50',
  'for a sum total of approximately 25,000 pieces','vita','Nineveh','Includes the library (scholarly texts in Standard Babylonian) and Babylonian letters.')
a('Neo-Assyrian','capitals and provinces','','mixed',None,'9th-7th c.','','falesNeoAssyrian2021','p. 1364',
  'Summing up, the vast majority of na texts comes from Nineveh and the other political capitals in the “Assyrian triangle”; whereas with few exceptions (Imgur-Ellil, Tušḫan and especially Dūr-Katlimmu) the provincial archives are limited to small quantities of documents, to be numbered in the dozens.','vita',None)
a('Neo-Assyrian','Assur private houses','Assur','private',None,'7th c.','legal; letters','falesNeoAssyrian2021','p. 1360',
  'produced a vast series of na tablets from private houses within the city walls','vita','Assur')
# ---------------- Neo-Babylonian
a('Neo-Babylonian','Eanna (Uruk) and Ebabbar (Sippar) temple archives','Uruk; Sippar','temple',None,'626-484','administrative; legal; letters','jursaAspectsEconomic2010','p. 9',
  'more than half of the published texts and an even higher percentage of the wipublished material are made up of just two huge temple archives, those of Eanna in Uruk and of Ebabbar in Sippar','jursa','Uruk',
  '"wipublished" is the OCR of "unpublished" in our copy.')
a('Neo-Babylonian','royal administration','Babylon','palace',None,'','','jursaAspectsEconomic2010','p. 9',
  "With the exception of a group of ration lists from Nebuchadnezzar's palace, the royal administration has left no archives; only temple and private archives are extant.",'jursa',None)
a('Neo-Babylonian','long sixth century corpus','Babylonia','mixed',19000,'c. 626-484','letters; legal; administrative','hacklLateBabylonian2021','p. 1432',
  'currently, ca. 19,000 texts are available for research and tens of thousands more await publication.','vita',None)
# ---------------- Achaemenid
a('Achaemenid','Persepolis Fortification archive','Persepolis','state',13000,'509-493','administrative (Elamite, Aramaic)','henkelmanAchaemenidHeartland2012','p. 949',
  'The Fortification archive, found in two bricked-up spaces in the northeastern terrace fortification, comprises at least 7,000 legible Elamite tablets, 5,000 anepigraphic but sealed tablets, some 1,000 Aramaic texts on clay tablets, and a handful of texts in other languages.','henk','Pārśa')
a('Achaemenid','Persepolis Treasury archive','Persepolis','state',747,'492-458','administrative (Elamite)','henkelmanAchaemenidHeartland2012','p. 949',
  'One, consisting of 747 clay tablets and fragments and 199 sealings, was found in the Treasury','henk','Pārśa')
a('Achaemenid','Babylonia after 484: Murašû and Kasr archives','Nippur; Babylon','private',2000,'484-331','legal; administrative','monerieLeconomieBabylonieLepoque2018','p. 6',
  'un peu plus de deux mille documents cunéiformes. La majeure partie de ces textes se rattache à deux archives : celle des Murašu (ca. 730 textes)','mon',None,'Kasr archive: c. 1,100 texts (same page).')
a('Achaemenid','Murašû archive','Nippur','private',730,'454-404','legal','stolperEntrepreneursEmpireMurasu1985','p. 14',
  'The Archive in its final ancient form certainly contained somewhat fewer than 868 texts.','stol','Nippur','Haynes and Hilprecht: about 730 items.')
# ---------------- Hellenistic
a('Hellenistic','all cuneiform documents','Babylonia','temple',5000,'331-c. 90','legal; administrative; astronomical','monerieLeconomieBabylonieLepoque2018','p. 5',
  'le nombre de textes conservés s’élève à au moins cinq mille documents, dont un peu plus de la moitié sont publiés à ce jour','mon',None)
a('Hellenistic','who wrote cuneiform','Babylonia','temple',None,'','','monerieLeconomieBabylonieLepoque2018','p. 5',
  'l’écriture cunéiforme n’était plus utilisée, à lʼépoque qui nous intéresse, que par le personnel des temples de la région et les membres de la notabilité','mon',None)
a('Hellenistic','Uruk (Rēš, Irigal, family archives)','Uruk','temple',1400,'Hellenistic and Parthian','legal; scholarly','monerieLeconomieBabylonieLepoque2018','p. 13',
  'On dénombre ainsi environ 1 400 tablettes cunéiformes urukéennes d’époque hellénistique et parthe, constituées pour moitié de textes de la pratique','mon','Uruk','Bīt Rēš 1 archive alone: c. 470 texts (same page).')
a('Hellenistic','Esagil administrative archive','Babylon','temple',260,'late 5th-early 3rd c.','administrative','monerieLeconomieBabylonieLepoque2018','p. 11',
  'L’archive administrative de l’Esagil (ca. 260 textes','mon','Babylon')
a('Hellenistic','Uruk legal archives','Uruk','private',535,'c. 200 years','legal','dotyCuneiformArchivesHellenistic1977','p. 48',
  'the known corpus now totals at least 535 tablets or fragments','doty','Uruk')
a('Hellenistic','second half of the first millennium','Babylonia','mixed',4200,'after 484','','hacklLateBabylonian2021','p. 1433',
  'this is reflected in the documentation from the second half of the first millennium bce, which, while still considerable, is far more limited than that of the preceding centuries (ca. 4,200 texts).','vita',None)
# ---------------- Hittite (SI)
a('Hittite','Ḫattuša archives (all periods)','Ḫattuša','palace',30000,'c. 1650-1180','ritual; festival; oracle; treaties; letters; instructions','vandenhoutHistoryHittiteLiteracy2020','p. 13',
  'To date, we have around 30,000 tablets and tablet fragments written in cuneiform','hout','Ḫattusa')
a('Hittite','provincial collections (Ortaköy, Maşat, Kayalıpınar, Kuşaklı)','several','state',4000,'15th-13th c.','letters; administrative; ritual','vandenhoutHistoryHittiteLiteracy2020','p. 170',
  'The texts from these sites illustrate the low degree of diffusion of the cuneiform script or, put differently, the high degree of centralization and appropriation of the script imposed by the capital.','hout',None,
  'Ortaköy has three to four thousand fragments; the others fewer than a hundred pieces each (same page).')
a('Hittite','13th-century production at Ḫattuša','Ḫattuša','palace',10000,'13th c.','','vandenhoutHistoryHittiteLiteracy2020','p. 273',
  'we then arrive at a total of just over ten thousand tablets for that entire century','hout',None)
# ---------------- Middle Elamite (SI)
a('Middle Elamite','Haft Tepe (Kabnak), ME I','Kabnak','palace',400,'Tepti-ahar, Inšušinak-šar-ili (15th-14th c.)','administrative; school; omens','glassnerTextesHaftTepe1991','pp. 113-114',
  'Au total, ce ne sont pas moins de cinquante-cinq [...] documents, sur un total d’environ 400 pièces dépouillées, qui font mention de Tepti-ahar ou d’Athibu.','glass','Kabnak','The OCR of our copy reads "cinquante cing" and breaks the sentence at the page turn; checked by hand.')
a('Middle Elamite','Haft Tepe find groups','Kabnak','palace',None,'ME I','','baselloElamiteAdministration2018','p. 485',
  'Many of the tablets were found together in three distinct groups','ew',None)
a('Middle Elamite','Tall-e Malyan (Anšan) EDD building','Anšan','palace',246,'c. 1300-1000, probably the last third','administrative (metals; livestock)','baselloElamiteAdministration2018','p. 487',
  '246 inscribed fragments and tablets were found','ew','Anšan',
  'The same page: half of c. 200 original tablets are published (Stolper 1984); palaeography "much closer to Neo-Elamite than Middle Elamite writing".')
A=pd.DataFrame(A)

# ---------------- what survives and what is lost (per period)
N=[('ED IIIa','Two corpora: Šuruppak administration and the Abu Ṣalābīḫ school; both are small.'),
   ('ED IIIb','Girsu is one household over c. 20 years; Umma, Adab and Nippur are smaller groups.'),
   ('Ebla','Everything comes from one palace over 40-50 years.'),
   ('Old Akkadian','Several provincial households (Girsu, Adab, Umma, Nippur), each one circle of documentation (Foster 1982).'),
   ('Ur III','c. 120,000 texts, almost all from provincial and royal archives; most were looted and have no find context (Molina 2016).'),
   ('Early Old Babylonian','No survey separates the early OB sites; our early sample is Nippur, Nērebtum and Tuttul.'),
   ('Old Babylonian','More than 50,000 archival texts from c. 60 sites; family archives appear for the first time, and institutional archives cover short spans (Charpin 2014).'),
   ('Old Assyrian','c. 22,300 tablets, almost all from c. 40 merchant houses at Kaneš; Assur itself is not documented.'),
   ('Middle Babylonian','c. 12,000 texts from Nippur, mostly unpublished, against a few hundred elsewhere.'),
   ('Middle Assyrian','Mostly Assur and Kār-Tukultī-Ninurta; perhaps 10% of Assur excavated; provinces under 1,500 texts in all.'),
   ('Neo-Assyrian','c. 25,000 pieces from Nineveh; provincial archives are counted in dozens (Fales 2021).'),
   ('Neo-Babylonian','c. 19,000 texts; more than half from the Eanna and Ebabbar temples; no royal archive survives (Jursa 2010).'),
   ('Achaemenid','Persepolis Fortification (c. 13,000 tablets) and Treasury; in Babylonia, a sharp drop after 484 to c. 2,000 texts, mostly Murašû and Kasr.'),
   ('Hellenistic','At least 5,000 texts, written only by temple staff and notables; most records were in Greek or Aramaic on perishable media (Monerie 2018).'),
   ('Hittite','c. 30,000 fragments, nearly all from Ḫattuša; provincial finds show the capital kept writing to itself (van den Hout 2020).'),
   ('Middle Elamite','c. 400 texts from Haft Tepe (ME I) and 246 from Malyan (end of the period); ME II-III have only royal inscriptions.')]
notes=pd.DataFrame(N,columns=['period','summary'])

# ---------------- locate each quote in its source (same normalisation as 95)
def norm(s):
    s=unicodedata.normalize('NFKC',s); s=re.sub(r'-\s*\n\s*(\w)',r'\1',s); s=s.lower()
    s=re.sub(r'[‘’“”"\'`´]','',s); s=re.sub(r'[^\w]+',' ',s); return re.sub(r'\s+',' ',s).strip()
cache={}
def located(src,q):
    if src not in cache: cache[src]=norm(open(f'{T}/{F[src]}',errors='ignore').read())
    ok=False
    for qq in (q,re.sub(r'(\w)-(\w)',r'\1\2',q)):
        parts=[norm(x) for x in re.split(r'\[\.\.\.\]|\.\.\.|…',qq)]; parts=[p for p in parts if len(p)>=10]
        ok=ok or (all(p[:100] in cache[src] for p in parts) if parts else False)
    return ok
A['located']=[located(s,q) for s,q in zip(A.src,A.quote)]
A.drop(columns=['src']).to_csv(f'{OUT}/archive_overview.csv',index=False)
notes.to_csv(f'{OUT}/archive_period_notes.csv',index=False)

# ---------------- literature sizes against our photographed sample
d=pd.read_parquet(WORK+'/master_tablets.parquet',columns=['period','site','museum'])
rows=[]
for per,g in A[A.n.notna()&A.sample_site.notna()].groupby('period'):
    g=g.drop_duplicates('sample_site'); s=d[d.period==per]; tot_lit=g.n.sum(); tot_s=len(s)
    for r in g.itertuples():
        k=int((s.site==r.sample_site).sum())
        rows.append(dict(period=per,site=r.site,sample_site=r.sample_site,lit_n=int(r.n),lit_share=round(r.n/tot_lit,3),sample_n=k,sample_share=round(k/tot_s,3) if tot_s else None,
                         key=r.key,where=r.where))
cmp=pd.DataFrame(rows); cmp['ratio']=(cmp.sample_share/cmp.lit_share).round(2)
cmp.to_csv(f'{OUT}/archive_sample_compare.csv',index=False)
# museum dispersal of the photographed sample: how many collections hold 80% of a period's tablets
disp=[]
for per,s in d.groupby('period'):
    if len(s)<20: continue
    c=s.museum.fillna('unknown').value_counts(); cum=c.cumsum()/c.sum()
    disp.append(dict(period=per,n=len(s),museums=len(c),museums_80=int((cum<0.8).sum()+1),top=c.index[0],top_share=round(c.iloc[0]/c.sum(),2)))
pd.DataFrame(disp).to_csv(f'{OUT}/archive_dispersal.csv',index=False)
print(len(A),'entries;',A.period.nunique(),'periods; located',int(A.located.sum()),'of',len(A))
print(A[~A.located][['period','key','where','quote']].to_string())
print(cmp[['period','site','lit_share','sample_share','ratio']].to_string())
