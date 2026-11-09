"""Centralization parameters for the periods of the article: codebook, scores, evidence and references.
Draft for ShG's correction (28 Oct 2026). Every score is an argued judgement from the cited literature, on a 0-3 scale with
explicit anchors (CODEBOOK), and carries a confidence level (H/M/L). Writes:
  centralization_codebook.csv, centralization_scores_long.csv, centralization_scores_wide.csv, centralization_indices.csv
Indices: three dimension means (A polity reach, B institutional economy, C control of writing and norms) and a first
principal component of all twelve; PRIV enters reversed (a large private sector = less institutional control)."""
from _paths import WORK
import pandas as pd, numpy as np
R=WORK

CODEBOOK=[
# id, dimension, name, framework, anchors 0..3, measurable proxy
('TERR','A','Territorial scope of the polity','Seshat Social Scale (polity territory); Mann 1986 extensive power',
 '0 single city-state | 1 multi-city regional state or league | 2 territorial kingdom unifying a region | 3 multi-regional empire with provinces or vassals',
 'Seshat polity territory (km2); number of cities under one ruler'),
('HIER','A','Administrative tiers under royal appointees','Seshat Hierarchical Complexity (administrative levels); Weber',
 '0 one tier (household or city) | 1 capital + dependent towns | 2 appointed provincial governors | 3 four or more tiers (provinces/satrapies, districts, local) with appointees',
 'Seshat administrative levels; attested titles of provincial officials'),
('FISC','A','Fiscal extraction recorded in writing','Monson and Scheidel 2015; Hanson and Sigman 2021 (extractive capacity); Scott 2017',
 '0 none beyond institutional income | 1 ad hoc tribute and gifts | 2 regular levies on land or service, recorded locally | 3 integrated, centrally recorded system across provinces',
 'named tax or levy systems (bala, gun2 ma-da, ilkum, ginā\'u, sāḫu, satrapal taxes) and their archives'),
('COMM','A','Royal communication infrastructure','Mann 1984 infrastructural power; Seshat Information (couriers, postal stations)',
 '0 none known | 1 ad hoc messengers | 2 regular royal messenger service | 3 relay stations or road network documented by ration records',
 'messenger texts, road stations, travel rations'),
('PAL','B','Weight of the palace (crown) sector','Gelb 1979; Diakonoff 1982; Renger 1994; Schloen 2001 (patrimonial household)',
 '0 marginal | 1 present, minor in the record | 2 a major institution | 3 dominant institution of the economy and of the written record',
 'share of archives from palace or crown households'),
('TEMP','B','Weight of the temple sector','same',
 '0 marginal | 1 present, minor | 2 major institution | 3 dominant institution of economy and record',
 'share of archives from temple households'),
('TCTL','B','Crown control of temples','Jursa 2010; Kleber 2008; Sallaberger and Westenholz 1999',
 '0 autonomous | 1 royal patronage only | 2 royal appointees, levies on temples | 3 temples run as units of the state',
 'royal officials (qīpu, ša rēš šarri, šabra appointed by king), temple accounts audited by the crown'),
('PRIV','B','Private (house) sector in writing [reversed in indices]','Diakonoff two-sector model; Van De Mieroop 1992; Garfinkle 2012; Schloen 2001',
 '0 negligible | 1 some private legal documents | 2 substantial private archives | 3 private archives dominate the written record',
 'share of private/family archives (Archibab, Prosobab, CDLI archive field)'),
('BUR','C','Standardized administrative procedure','Weber 1922 bureaucracy; Postgate 2013; Steinkeller 2003',
 '0 none detectable | 1 local conventions | 2 standardized accounting within major institutions | 3 standardized procedures across provinces (balanced accounts, instructions for officials, audits)',
 'balanced accounts, instructions, standardized document types'),
('SCHOOL','C','Institutional scribal training','Veldhuis 2011; Robson 2001; Gesche 2001; Visicato 2000',
 '0 household apprenticeship, no shared curriculum | 1 shared curriculum, household locus | 2 institutional (palace/temple) schooling with shared curriculum | 3 state-controlled training producing scribes for the whole polity',
 'find contexts of school tablets; curriculum overlap across cities'),
('LAW','C','Codified law and royal justice','Seshat Law (formal legal code, judges, courts); Westbrook 2003; Charpin 2010',
 '0 no evidence | 1 royal edicts or royal judgements only | 2 a law collection or royal courts | 3 law collection and royal judges and edicts',
 'law collections, royal judges (dayyān šarrim), mīšarum edicts'),
('STD','C','State-imposed standards (measures, calendar, dating)','Scott 1998 legibility; Brambor et al. 2020 information capacity',
 '0 local systems | 1 partial or local standard | 2 polity-wide standard measures or dating | 3 polity-wide measures and dating/calendar imposed',
 'royal measures (gur of Akkade, gur lugal, mina of the king), dating systems (year names, regnal years, eponyms, era)'),
]

S={}  # period -> {param: (score, conf, evidence, refs)}
S['ED IIIa']=dict(  # Šuruppak (Fara), Abu Salabikh, c. 2600-2450
 TERR=(1,'M','Šuruppak belongs to a league of Sumerian cities (the "Kengir league"), with troop lists from several cities in its archive.','pomponioVisicato1994; bartash2020'),
 HIER=(1,'L','City institutions with dependent settlements; no royal provincial officials.','bartash2020'),
 FISC=(1,'L','Contributions among league cities; no tax archive.','pomponioVisicato1994'),
 COMM=(1,'L','Messengers among league cities.','pomponioVisicato1994'),
 PAL=(2,'M','The great household (é-gal) of Šuruppak dominates the administrative archive.','pomponioVisicato1994; visicato2000'),
 TEMP=(1,'L','Temples present; the archive is mostly of the central household.','bartash2020'),
 TCTL=(1,'L','Not documented in detail.','bartash2020'),
 PRIV=(1,'M','House and field sale contracts on clay and stone.','gelbSteinkellerWhiting1991'),
 BUR=(2,'M','Hundreds of named scribes and standardized ration and personnel lists.','visicato2000'),
 SCHOOL=(2,'M','Lexical and literary texts shared by Fara and Abu Salabikh; scribes trained in institutional settings.','visicato2000; veldhuis2014'),
 LAW=(0,'M','No law collection or royal edicts.','bartash2020'),
 STD=(1,'L','Local metrology; no royal dating system.','bartash2020'))
S['ED IIIb']=dict(  # Girsu (Lagaš), Umma, Zabalam, Adab, c. 2450-2350
 TERR=(1,'H','The state of Lagaš (Girsu, Lagaš, Nina) and its rival Umma: multi-city city-states.','bartash2020'),
 HIER=(1,'M','Ruler (ensi2) with dependent towns; no provinces.','bartash2020'),
 FISC=(1,'M','Dues collected by the ruler; Urukagina reform text complains of officials\' levies.','bartash2020'),
 COMM=(1,'L','Messengers in the Bau archive.','beld2002'),
 PAL=(2,'M','Ruler\'s household (é-gal) beside the household of his wife.','beld2002; bartash2020'),
 TEMP=(3,'H','The é-mí / é-dBa-ú archive of Girsu, a temple household of about 1,200 dependants, is the main archive of the period.','beld2002; maekawa1973'),
 TCTL=(3,'H','The household was run by the ruler\'s wife; Urukagina renamed it after the goddess but kept it in the ruling family.','maekawa1973; beld2002'),
 PRIV=(1,'M','Few private documents; some sales of land and houses.','gelbSteinkellerWhiting1991'),
 BUR=(2,'H','Monthly ration lists with fixed formulary and closing sections.','beld2002'),
 SCHOOL=(1,'L','Little school material from Girsu; training within the household.','veldhuis2014'),
 LAW=(1,'M','Urukagina\'s reform inscriptions; no law collection.','bartash2020'),
 STD=(1,'M','Local month names and regnal-year dating within Lagaš only.','bartash2020'))
S['Ebla']=dict(  # Palace G archive, c. 2400-2300
 TERR=(2,'M','A regional kingdom of northern Syria with dependent towns and treaties with neighbours.','archi2015; matthiaeMarchetti2013'),
 HIER=(2,'M','King, vizier and lords (lugal) over dependent centres.','archi2015'),
 FISC=(2,'M','Annual deliveries (mu-DU) of silver and textiles from dependent centres.','archi2015'),
 COMM=(2,'M','Messengers and gift exchange with Mari, Nagar, Kiš.','archi2015'),
 PAL=(3,'H','The archive is the palace\'s own; the palace dominates the economy.','archi2015'),
 TEMP=(1,'M','Temples receive offerings from the palace; no temple archive.','archi2015'),
 TCTL=(2,'M','Offerings to gods recorded as palace expenditures.','archi2015'),
 PRIV=(0,'H','No private archives.','archi2015'),
 BUR=(2,'M','Annual textile and metal accounts with fixed formulary.','archi2015'),
 SCHOOL=(2,'M','Palace school: lexical lists from the Kiš tradition and bilingual vocabularies.','archi2015; veldhuis2014'),
 LAW=(1,'L','Some legal decisions and treaties; no law collection.','archi2015'),
 STD=(1,'M','Local metrology and month names; no dating by year names.','archi2015'))
S['Old Akkadian']=dict(  # Sargonic, c. 2350-2150
 TERR=(3,'H','First empire uniting Babylonia with campaigns to Syria, Elam and the Gulf.','schrakamp2020; foster2016'),
 HIER=(2,'H','Governors (ensi2) appointed in Sumerian cities, Akkadian officials and garrisons.','schrakamp2020; foster2016'),
 FISC=(2,'M','Royal estates and levies; no integrated tax archive.','schrakamp2020'),
 COMM=(2,'M','Royal messengers; Seshat codes couriers and postal stations present.','foster2016; seshat2020'),
 PAL=(2,'M','Royal estates (e.g. the Mesag archive of Umma) and governors\' households.','foster2016'),
 TEMP=(1,'M','Temples continue but are not the main archive holders.','schrakamp2020'),
 TCTL=(2,'M','Royal daughters as high priestesses (Enheduana at Ur); royal patronage at Nippur.','foster2016'),
 PRIV=(1,'M','Private and kin-group land sales (Maništušu obelisk records royal purchases from kin groups).','gelbSteinkellerWhiting1991'),
 BUR=(2,'M','Sargonic administrative reforms: standard formats of accounts in several cities.','foster2016; schrakamp2020'),
 SCHOOL=(2,'L','Sargonic orthography and script are uniform across Babylonia, implying shared training.','foster2016'),
 LAW=(1,'L','No law collection survives; royal judgements.','schrakamp2020'),
 STD=(3,'M','Standard units (the gur of Akkade) and Akkadian as a language of administration across cities; year names.','foster2016; schrakamp2020'))
S['Ur III']=dict(  # 2110-2003
 TERR=(3,'H','Core provinces of Babylonia and a taxed periphery to the east and north.','steinkeller1987; garfinkle2022'),
 HIER=(3,'H','Grand vizier (sukkal-mah), provincial governors (ensi2), military governors in the periphery, temple and estate managers.','steinkeller1987; sharlach2004'),
 FISC=(3,'H','bala rotation of the core provinces and gun2 ma-da tax of the periphery, centralised at Puzriš-Dagan.','sharlach2004; steinkeller1987'),
 COMM=(3,'H','Messenger texts of Girsu, Umma and Irisagrig record travellers and road stations.','manderMessengerTextsGirsu2008; dagostinoUmmaMessengerTexts2008'),
 PAL=(3,'H','Crown and provincial households dominate the economy and its record (about 100,000 administrative tablets).','steinkeller2003archival; garfinkle2022'),
 TEMP=(2,'H','Provincial temple households (e.g. Šara at Umma) form the units of provincial administration.','steinkeller1987'),
 TCTL=(3,'M','Temple households run as provincial units under the governor; disputed by those who stress household autonomy.','steinkeller1987; garfinkle2008'),
 PRIV=(1,'M','Private loans and the archive of SI.A-a show a small private sector.','garfinkle2012'),
 BUR=(3,'H','Balanced accounts, standard text types and seals of officials across provinces.','englund1990; molinaArchivesBookkeepingSouthern2016'),
 SCHOOL=(2,'L','A uniform script and bookkeeping suggest institutional training, but the evidence is indirect (the claim of royal schools comes from a royal hymn).','michalowski2011; veldhuis2014'),
 LAW=(3,'H','Laws of Ur-Namma, royal courts and case records (di-til-la).','roth1997; molina2000ditilla'),
 STD=(2,'M','The royal gur and standard metrology everywhere; local calendars persisted (Widell 2004 argues against an imposed state calendar).','widellCalendarNeoSumerianUr2004'))
S['Early Old Babylonian']=dict(  # Isin-Larsa, 2000-1850
 TERR=(1,'H','Competing kingdoms: Isin, Larsa, Ešnunna, Uruk, Babylon.','wagensonner2022'),
 HIER=(1,'M','Kings with governors in a few cities.','wagensonner2022'),
 FISC=(1,'M','Palace income from crown land and dues; little central record.','wagensonner2022'),
 COMM=(1,'L','Royal messengers between kingdoms.','wagensonner2022'),
 PAL=(2,'M','Palace households (e.g. the Isin craft archive).','vandemieroop1987crafts'),
 TEMP=(1,'M','Temples present; temple archives rarer.','wagensonner2022'),
 TCTL=(2,'L','Kings appoint priests and endow temples.','wagensonner2022'),
 PRIV=(2,'H','Private archives grow (Ur, Nippur, Larsa).','vandemieroop1992'),
 BUR=(1,'M','Local conventions in each kingdom.','wagensonner2022'),
 SCHOOL=(1,'H','Schooling in private houses (Nippur House F, Ur No. 7 Quiet Street) with a shared curriculum.','robsonTabletHouseScribal2001; veldhuis2014'),
 LAW=(2,'H','Laws of Lipit-Ištar and of Ešnunna.','roth1997'),
 STD=(1,'M','Year names per kingdom; local calendars.','wagensonner2022'))
S['Old Babylonian']=dict(  # 1850-1595, mostly Babylon dynasty
 TERR=(2,'H','Hammurabi unified Babylonia and the middle Euphrates (1763-1739 BCE); before and after, regional kingdoms.','boivin2022; charpinMesopotamienAltbabylonische2004'),
 HIER=(2,'H','Royal agents in conquered cities (Šamaš-hazir and Sin-iddinam at Larsa), city mayors and assemblies.','charpinMesopotamienAltbabylonische2004; seri2005'),
 FISC=(2,'H','ilkum service fields, biltum on palace land, palace commerce through merchants.','stol2004'),
 COMM=(2,'M','Royal letters to agents in the provinces.','charpinMesopotamienAltbabylonische2004'),
 PAL=(2,'H','Palace estates leased out; the palace works through entrepreneurs.','stol2004; renger1994'),
 TEMP=(1,'M','Temples reduced in economic weight; cloister of nadītus at Sippar.','stol2004'),
 TCTL=(2,'M','Kings appoint temple officials and control temple land.','charpinMesopotamienAltbabylonische2004'),
 PRIV=(3,'H','Family archives of sales, loans and leases dominate the legal record.','charpinMesopotamienAltbabylonische2004; goddeerisShapeSizeArchival2023'),
 BUR=(2,'M','Standard document types and formulary across cities; palace accounts.','charpinMesopotamienAltbabylonische2004'),
 SCHOOL=(1,'H','Schooling in houses with a shared curriculum and model contracts.','robsonTabletHouseScribal2001; spadaSumerianModelContracts2018'),
 LAW=(3,'H','Laws of Hammurabi, royal judges, mīšarum edicts (Ammi-ṣaduqa).','charpin2010writing; roth1997'),
 STD=(2,'M','Babylonian year names imposed after conquest; the Babylonian calendar spreads.','charpinMesopotamienAltbabylonische2004'))
S['Old Assyrian']=dict(  # Assur and Kanesh, 1950-1720
 TERR=(0,'H','The city-state of Assur; the Anatolian trading colonies were not provinces.','larsenAncientKanesh2015; barjamovic2022'),
 HIER=(1,'H','City Hall (bēt ālim), assembly, kārum courts in Anatolia.','larsenAncientKanesh2015'),
 FISC=(1,'H','Export and import taxes of the City and of Anatolian rulers.','larsenAncientKanesh2015'),
 COMM=(2,'M','Regular caravans and messengers between Assur and Kanesh, under treaties.','barjamovic2022'),
 PAL=(0,'H','The ruler (iššiak Aššur) has a minor economic role.','larsenAncientKanesh2015'),
 TEMP=(1,'M','The Aššur temple holds funds and weights; no temple archive.','larsenAncientKanesh2015'),
 TCTL=(0,'L','Not applicable in the Kanesh record.','larsenAncientKanesh2015'),
 PRIV=(3,'H','About 23,000 tablets from merchants\' houses; private letters and contracts.','larsenAncientKanesh2015; michel2020women'),
 BUR=(1,'M','Merchant conventions (envelopes, sealed witnessed contracts), not state procedure.','veenhof2003'),
 SCHOOL=(0,'H','Writing learned in merchant families, including women.','michel2020women; larsenAncientKanesh2015'),
 LAW=(2,'M','The "words of the stele" in Assur; verdicts of the City and the kārum.','veenhof1995stele'),
 STD=(2,'M','Eponym (līmum) dating and standard weights of the City.','larsenAncientKanesh2015'))
S['Middle Babylonian']=dict(  # Kassite, 1500-1150 (78% Nippur)
 TERR=(2,'H','Kassite kings ruled all of Babylonia for four centuries.','paulus2022'),
 HIER=(2,'M','Provinces (pīḫatu) under governors; the governor of Nippur (šandabakku).','paulus2022'),
 FISC=(2,'M','Redistribution through the governor\'s office; royal land grants (kudurrus) exempt holders from levies.','paulus2022; paulus2014kudurru'),
 COMM=(2,'M','International messengers (Amarna letters); internal messengers.','paulus2022'),
 PAL=(3,'M','The archive of the governor of Nippur is the bulk of the record.','paulus2022'),
 TEMP=(2,'M','Temple of Enlil at Nippur linked to the governor\'s office.','paulus2022'),
 TCTL=(2,'M','The šandabakku combined civil and temple functions.','paulus2022'),
 PRIV=(1,'M','Few private archives (Ur, Nippur).','paulus2022'),
 BUR=(2,'M','Highly regular redistribution accounts at Nippur.','paulus2022'),
 SCHOOL=(2,'L','Scribal families with ancestor names; school texts from Nippur.','veldhuis2014'),
 LAW=(1,'M','No law collection; royal judgements and kudurru grants.','paulus2014kudurru'),
 STD=(2,'H','Dating by regnal years replaces year names across Babylonia.','paulus2022'))
S['Middle Assyrian']=dict(  # 1400-1050
 TERR=(3,'H','From city-state to empire with provinces from the Zagros to the Euphrates.','reculeau2022'),
 HIER=(3,'H','Provinces (pāḫutu) under governors; vizier and great households.','postgate2013; reculeau2022'),
 FISC=(3,'H','ginā\'u offerings delivered by every province to the Aššur temple; ilku service.','postgate2013'),
 COMM=(3,'M','Road stations and messengers between capital and provincial centres (Dur-Katlimmu).','reculeau2022; postgate2013'),
 PAL=(3,'H','Palace and great households dominate the archives.','postgate2013'),
 TEMP=(1,'M','The Aššur temple receives provincial offerings managed by state officials.','postgate2013'),
 TCTL=(3,'M','Offerings to Aššur organised by the provincial administration.','postgate2013'),
 PRIV=(1,'M','Some family archives at Assur (Urad-Šerua, Babu-aha-iddina).','postgate2013'),
 BUR=(3,'H','Bureaucratic record-keeping across ten government archives (Postgate); Palace Decrees.','postgate2013; postgateMiddleAssyrianTablets1986'),
 SCHOOL=(2,'M','Royal scribes and scholarly libraries at Assur.','reculeau2022'),
 LAW=(3,'H','Middle Assyrian Laws and Palace Decrees.','roth1997'),
 STD=(2,'H','Eponym dating and Assyrian calendar across provinces.','reculeau2022'))
S['Middle Elamite']=dict(  # Haft Tepe (Kabnak) 15th c.; Malyan (Anšan) c. 1100
 TERR=(2,'M','Kingdom of Susa and Anšan.','mofidiNasrabadi2022'),
 HIER=(1,'L','Royal centres at Susa, Kabnak, Anšan.','mofidiNasrabadi2022'),
 FISC=(1,'L','Little evidence.','mofidiNasrabadi2022'),
 COMM=(1,'L','Little evidence.','mofidiNasrabadi2022'),
 PAL=(3,'M','Royal (and royal tomb-temple) administration at Kabnak and Anšan.','herreroHaftTepeChoix1990; stolperTextsTalliMalyan1984'),
 TEMP=(2,'L','Temple-tomb complex of Tepti-ahar at Haft Tepe.','mofidiNasrabadi2022'),
 TCTL=(2,'L','Cult sites founded by kings.','mofidiNasrabadi2022'),
 PRIV=(0,'M','Almost no private archives.','mofidiNasrabadi2022'),
 BUR=(2,'L','Uniform administrative records at each site.','stolperTextsTalliMalyan1984'),
 SCHOOL=(1,'L','School texts at Haft Tepe and Susa; little known.','mofidiNasrabadi2022'),
 LAW=(1,'L','Legal documents from Susa; no law collection.','mofidiNasrabadi2022'),
 STD=(1,'L','Little evidence.','mofidiNasrabadi2022'))
S['Hittite']=dict(  # 16th-12th c.
 TERR=(3,'H','An empire of Anatolia and northern Syria with vassal treaties.','weeden2022'),
 HIER=(3,'M','Provincial lords (bēl madgalti), viceroys at Karkamiš and Aleppo, vassal kings.','weeden2022'),
 FISC=(2,'M','Service and tax obligations (šaḫḫan, luzzi) and royal storehouses ("seal houses").','weeden2022'),
 COMM=(2,'M','Royal correspondence with provinces (Maşat) and abroad.','weeden2022'),
 PAL=(3,'H','Palace and royal storehouses dominate the record.','weeden2022'),
 TEMP=(2,'M','Temples as large institutions in the capital; cult inventories.','weeden2022'),
 TCTL=(3,'M','The king as chief priest; cult inventories reorganised by Tudḫaliya IV.','weeden2022'),
 PRIV=(0,'H','Private documents almost absent.','weeden2022'),
 BUR=(3,'M','Instruction texts for officials (many from Arnuwanda I) and standard land-donation tablets that "standardize and parcel out the Anatolian landscape"; Weeden doubts how effective the instructions were as instruments of control.','miller2013instructions; weeden2022 (pp. 564, 568-569)'),
 SCHOOL=(2,'M','Palace and temple scribes trained with Mesopotamian lexical lists at Ḫattuša.','weeden2022'),
 LAW=(3,'H','Hittite Laws, treaties, royal courts.','roth1997; weeden2022'),
 STD=(1,'L','Little evidence for imposed measures or dating.','weeden2022'))
S['Neo-Assyrian']=dict(  # 911-612
 TERR=(3,'H','The largest empire of its time, from Egypt to western Iran.','baker2023; radner2014network'),
 HIER=(3,'H','Provinces under governors, magnates, a royal household of officials.','baker2023'),
 FISC=(3,'H','Provincial taxes, tribute of vassals, labour and military service.','baker2023'),
 COMM=(3,'H','The king\'s road with relay stations (bēt mardēti) and royal messengers (kalliu).','radner2014network'),
 PAL=(3,'H','Palace archives of Nineveh, Kalḫu; the royal household as the state.','baker2023'),
 TEMP=(1,'M','Temples dependent on the crown.','baker2023'),
 TCTL=(3,'M','Temples subordinated and supplied by provinces.','baker2023'),
 PRIV=(2,'M','Legal archives of officials and families at Assur, Nineveh and Kalḫu.','radnerRelationFormat1995; baker2023'),
 BUR=(2,'M','Standard formats per document type (letters, legal, administrative), but much business in Aramaic on perishable media.','radnerRelationFormat1995; baker2023'),
 SCHOOL=(2,'M','Palace scribes and scholars; Aramaic scribes beside cuneiform scribes.','baker2023'),
 LAW=(1,'M','No law collection; royal justice. Seshat codes formal legal code absent.','seshat2020'),
 STD=(2,'H','Eponym dating and the "mina of the king" across the empire.','baker2023'))
S['Neo-Babylonian']=dict(  # 626-539
 TERR=(3,'H','Empire from the Gulf to the Levant.','jursa2023'),
 HIER=(2,'M','Provinces and governors; less documented than Assyria.','jursa2023'),
 FISC=(2,'H','Taxes and service on temples and land (ilku, urāšu); royal demands on temple estates.','jursa2010; jursa2011taxation'),
 COMM=(2,'M','Royal messengers; canals and roads.','jursa2023'),
 PAL=(2,'M','Palace economy known indirectly; royal estates.','jursa2010'),
 TEMP=(3,'H','Eanna and Ebabbar are the largest archives.','jursa2010; kleberTempelUnd2008'),
 TCTL=(3,'H','Royal officials (qīpu, ša rēš šarri bēl piqitti) run Eanna from about 584 BCE; Nabonidus imposes Esangila norms.','kleberTempelUnd2008; jursaUrukeanPriestsNeoBabylonian2019'),
 PRIV=(3,'H','Family archives of entrepreneurs (Egibi) and priests.','jursa2010; waerzeggers_marduk-remanni_2014'),
 BUR=(2,'H','Standard temple bookkeeping; uniform legal formulary.','jursa2004accounting; jursaDiplomaticsLateBabylonian2021'),
 SCHOOL=(1,'H','Training in priestly and scribal families within temple communities; shared curriculum.','gesche2001'),
 LAW=(1,'M','A fragment of Neo-Babylonian laws; royal judges.','roth1997'),
 STD=(3,'H','Regnal-year dating and a standard calendar; standard silver (ginnu) marks.','jursa2010'))
S['Achaemenid (Babylonia)']=dict(  # 539-331
 TERR=(3,'H','The largest empire yet; Babylonia a satrapy.','heller2023; potts2023'),
 HIER=(3,'H','Satrap, governors, royal officials, the ḫaṭru system.','heller2023'),
 FISC=(3,'H','Land-for-service (bow fiefs, ḫaṭru) and taxes in silver.','jursaAspectsTaxationAchaemenid2009; heller2023'),
 COMM=(3,'M','Royal road and messengers (documented best at Persepolis).','henkelmanAchaemenidHeartland2012'),
 PAL=(2,'M','Crown estates and royal officials in Babylonia.','heller2023'),
 TEMP=(2,'H','Temples continue until the end of central archives after 484 BCE.','waerzeggers2003end'),
 TCTL=(3,'H','Temples under royal control; northern temple archives end after the revolts of 484 BCE.','waerzeggers2003end; jursa2010'),
 PRIV=(3,'H','Private archives (Egibi, Murašû) dominate.','jursa2010; heller2023'),
 BUR=(2,'M','Neo-Babylonian procedures continue.','jursaDiplomaticsLateBabylonian2021'),
 SCHOOL=(1,'H','Babylonian scribal families as before.','gesche2001'),
 LAW=(1,'M','Royal "law of the king" (dātu); no law collection.','heller2023'),
 STD=(3,'M','Regnal-year dating and standard measures across the satrapy.','heller2023'))
S['Achaemenid (Persepolis)']=dict(  # Persepolis Fortification and Treasury, 509-457
 TERR=(3,'H','Imperial heartland.','potts2023; basello2023'),
 HIER=(3,'H','Director (Parnakka), regional and local officials in Fārs.','henkelmanAchaemenidHeartland2012'),
 FISC=(3,'H','Collection and redistribution of commodities across Fārs.','henkelmanAchaemenidHeartland2012'),
 COMM=(3,'H','Travel rations at road stations along the royal road.','henkelmanAchaemenidHeartland2012'),
 PAL=(3,'H','The royal economy of Fārs is the archive.','henkelmanAchaemenidHeartland2012'),
 TEMP=(0,'H','Offerings issued by the administration; no temple archive.','henkelmanAchaemenidHeartland2012'),
 TCTL=(3,'H','Cults supplied by the crown administration.','henkelmanAchaemenidHeartland2012'),
 PRIV=(0,'H','No private archives.','henkelmanAchaemenidHeartland2012'),
 BUR=(3,'H','Standard memoranda, journals and accounts with seals of officials.','henkelmanAchaemenidHeartland2012'),
 SCHOOL=(2,'M','Elamite scribes of the administration, an Elamite tradition from Anšan.','henkelmanAchaemenidHeartland2012; basello2023'),
 LAW=(1,'L','Not documented in the archive.','basello2023'),
 STD=(3,'H','Standard rations, measures and regnal-year dating.','henkelmanAchaemenidHeartland2012'))
S['Hellenistic']=dict(  # Seleucid and Arsacid Babylonia, cuneiform at Uruk and Babylon
 TERR=(3,'H','Seleucid empire.','clancierMonerie2014'),
 HIER=(3,'M','Satraps, royal officials, city institutions.','clancierMonerie2014'),
 FISC=(2,'M','Royal taxes, recorded mostly in Greek.','clancierMonerie2014'),
 COMM=(2,'L','Not documented in cuneiform.','clancierMonerie2014'),
 PAL=(1,'M','The crown is largely invisible in cuneiform.','clancierMonerie2014'),
 TEMP=(3,'H','Cuneiform survives in the temple communities of Uruk (Rēš) and Babylon (Esagil).','clancierMonerie2014'),
 TCTL=(1,'M','Temples governed by their own assemblies and officials.','clancierMonerie2014'),
 PRIV=(2,'H','Private legal archives of the temple elite (prebend sales).','clancierMonerie2014'),
 BUR=(1,'M','Cuneiform administration limited to the temples.','clancierMonerie2014'),
 SCHOOL=(2,'H','Scholarly families in the temples train scribes.','clancierMonerie2014'),
 LAW=(1,'L','Royal law in Greek; no cuneiform law collection.','clancierMonerie2014'),
 STD=(3,'H','The Seleucid era as a single, continuous dating system.','clancierMonerie2014'))

PARAMS=[c[0] for c in CODEBOOK]
cb=pd.DataFrame(CODEBOOK,columns=['param','dimension','name','framework','anchors','proxy'])
rows=[]
for p,d in S.items():
    for k in PARAMS:
        s,c,e,r=d[k]; rows.append(dict(period=p,param=k,score=s,conf=c,evidence=e,refs=r))
L=pd.DataFrame(rows)
W=L.pivot(index='period',columns='param',values='score')[PARAMS].loc[list(S)]
Z=W.copy(); Z['PRIV']=3-Z['PRIV']
dims={'A':[c for c in PARAMS if cb.set_index('param').dimension[c]=='A'],'B':['PAL','TEMP','TCTL','PRIV'],'C':['BUR','SCHOOL','LAW','STD']}
I=pd.DataFrame({'A_polity_reach':Z[dims['A']].mean(axis=1),'B_institutional_economy':Z[dims['B']].mean(axis=1),'C_control_of_writing':Z[dims['C']].mean(axis=1)})
I['scribal_institution']=Z[['BUR','SCHOOL']].mean(axis=1)
Zs=(Z-Z.mean())/Z.std(ddof=0).replace(0,1)
u,s,vt=np.linalg.svd(Zs.values,full_matrices=False)
pc1=u[:,0]*s[0]; pc1=pc1*np.sign(np.corrcoef(pc1,Z.mean(axis=1))[0,1])
I['PC1_all']=pc1; I['mean_all']=Z.mean(axis=1)
I['PC1_var_explained']=(s[0]**2/(s**2).sum())
load=pd.Series(vt[0]*np.sign(np.corrcoef(u[:,0],Z.mean(axis=1))[0,1]),index=PARAMS)
cb.to_csv(f'{R}/centralization_codebook.csv',index=False); L.to_csv(f'{R}/centralization_scores_long.csv',index=False)
W.to_csv(f'{R}/centralization_scores_wide.csv'); I.round(3).to_csv(f'{R}/centralization_indices.csv')
load.round(3).to_csv(f'{R}/centralization_pc1_loadings.csv')
if __name__=='__main__':
    print(W.to_string()); print(I.round(2).to_string()); print('PC1 loadings',load.round(2).to_dict())
    print(L.conf.value_counts())
