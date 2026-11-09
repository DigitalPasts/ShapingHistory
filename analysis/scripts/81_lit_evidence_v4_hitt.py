"""Fifth round (8 Nov 2026), after ShG's second assessment. Hittite (SI period). ShG's notes: STD, FISC, TCTL, TEMP and PAL
cannot be scored without more citations, qualifying ones included; HIER and TERR change between the Old Kingdom and the
Empire; two more for PRIV; Hoffner on letters for COMM; one or two qualifying for LAW; Gordin 2015 and Weeden (logograms)
for SCHOOL (neither is in the library; see the acquisition list in the next-stage guide).
Chronology: statements about one phase carry region='Old Kingdom' or region='Empire', so 85b reports a sub-score for each
phase beside the period score (the same mechanism as the regional entities of ED IIIa and Achaemenid).
Sources (local texts of ShG's PDFs; printed pages from running heads):
- T. Bilgin 2018 [2019], Officials and Administration in the Hittite World (SANER 21): pdf n = p. n-16.
- Th. van den Hout 2020, A History of Hittite Literacy (CUP): pdf n = p. n-26.
- H. A. Hoffner 2009, Letters from the Hittite Kingdom (WAW 15): pdf n = p. n-19.
- H. A. Hoffner 1997, The Laws of the Hittites: OCR; pdf 12 = p. 5."""
P='Hittite'
BIL='bilginOfficialsAdministrationHittite2018'; VDH='vandenhoutHistoryHittiteLiteracy2020'; HOL='hoffnerLettersHittite2009'; HOF='hoffnerLawsHittites1997'
E=[
# ---------------------------------------------------------------- TERR / HIER by phase
dict(param='HIER',score=1.5,stance='qualifies',key=BIL,where='p. 452',basis='fragmentary',genre='mixed',archive='mixed',region='Old Kingdom',
 quote="During the early Old Kingdom, the state was made up of small provinces, each centered around an important settlement of the time and ruled by Hittite princes. Our sources from this period are too scarce to determine how centralized or feudal this structure was.",
 note='Old Kingdom: princes in small provinces; degree of central control unknown.'),
dict(param='HIER',score=3,stance='supports',key=BIL,where='p. 452',basis='documented',genre='mixed',archive='mixed',region='Empire',
 quote="Starting with the early Empire period, following the permanent integration of Kizzuwatna into the Hittite domain, we see the first instances of the installation of princes as appanage kings. This continued with the expansion into northern Syria ... In the meantime the internal territories were organized into governorships of various sizes under Provincial Governors and Frontier Governors.",
 note='Empire: appanage kingdoms and graded governorships.'),
dict(param='HIER',score=2.5,stance='qualifies',key=BIL,where='p. 453',basis='documented',genre='mixed',archive='mixed',
 quote="In terms of changes in these administrative offices, no particular period of Hittite history may be recognized as a time of radical transformation. Instead the changes seem to have taken place gradually throughout the state’s existence. Growth in number of offices more or less parallels the growth of the state into an empire",
 note='No single break: offices grow gradually with the territory.'),
dict(param='TERR',score=2,stance='supports',key=BIL,where='p. 452',basis='fragmentary',genre='mixed',archive='mixed',region='Old Kingdom',
 quote="During the early Old Kingdom, the state was made up of small provinces, each centered around an important settlement of the time and ruled by Hittite princes.",
 note='Old Kingdom: a central Anatolian state.'),
dict(param='TERR',score=3,stance='supports',key=BIL,where='p. 452',basis='documented',genre='mixed',archive='mixed',region='Empire',
 quote="Distribution of the territories to royal princes can be described as a feudal organization on the one hand, but the state was also highly centralized on the other. While the appanage kings had their own territorial responsibilities, they were often called to the assistance of the Great King",
 note='Empire: Anatolia and northern Syria under one king.'),
# ---------------------------------------------------------------- PAL (undecided)
dict(param='PAL',score=2.5,stance='supports',key=VDH,where='p. 10',basis='documented',genre='mixed',archive='Telipinu Proclamation; silos',
 quote="The second part of King Telipinu’s proclamation of the late sixteenth century bc documents a network of over ninety storehouses for grain throughout Central Anatolia ... on the archaeological side, the silos in Hattusa and provincial centers are an eloquent testament to the Hittite state seeking to guarantee a regular and steady ﬂow of foodstuffs.",
 note='A royal storage network across the core.'),
dict(param='PAL',score=2,stance='qualifies',key=VDH,where='p. 10',basis='documented',genre='mixed',archive='Telipinu Proclamation; silos',
 quote="The storage facilities mentioned in the Telipinu text cover the core of Hatti-Land as well as the Upper and Lower Land and bespeak a ﬁne-grained and therefore also highly localized or decentralized system of local networks that together form the Hittite kingdom. Within such a system it is possible to work without written records to a large extent.",
 note='The palace economy ran through local networks, largely without records.'),
dict(param='PAL',score=2.5,stance='supports',key=BIL,where='p. 447',basis='documented',genre='mixed',archive='mixed',region='Empire',
 quote="There were several regional palaces which not only served as administrative institutions but also acted as royal residences during the visits of the king.",
 note=''),
# ---------------------------------------------------------------- TCTL / TEMP (undecided)
dict(param='TCTL',score=2.5,stance='supports',key=VDH,where='p. 155',basis='documented',genre='admin',archive='cult inventories (Ḫattuša)',region='Empire',
 quote="Given the general attitude to incorporate and support such local religious traditions, regular inspections were carried out. These were laid down in written reports known as cult inventories ... cult inventories were reports drawn up town by town. These were purely administrative records whose life expired once the next inspection came around or when the changes ordained from the capital on receiving the report had been implemented.",
 note='The capital inspected and reordered local cults, town by town.'),
dict(param='TCTL',score=2.5,stance='supports',key=VDH,where='p. 10',basis='documented',genre='admin',archive='Instruction for Temple Personnel',
 quote="the passage from the Instruction of the Temple Personnel ... offers the perfect example for the control the palace tried to exert on the distribution of wealth and possible related record keeping: If by the palace silver, gold, textiles, (and/or) things of bronze are given to him (i.e., a member of the temple personnel) as a gift, it should be speciﬁed: “King so-and-so has given it to him” and it should likewise be recorded how much its weight is.",
 note='Royal instructions regulate temple staff.'),
dict(param='TEMP',score=1.5,stance='qualifies',key=VDH,where='p. 155',basis='documented',genre='admin',archive='cult inventories (Ḫattuša)',region='Empire',
 quote="Given the general attitude to incorporate and support such local religious traditions, regular inspections were carried out.",
 note='Local temples depend on royal support and inspection rather than running an economy of their own.'),
# ---------------------------------------------------------------- FISC (undecided)
dict(param='FISC',score=2,stance='supports',key=VDH,where='p. 10',basis='documented',genre='mixed',archive='Telipinu Proclamation; silos',
 quote="In order to avoid this, the state invested in mobilizing the staples and organizing them at a local level and thus tried to provide for the inevitable lean years.",
 note='Levies in kind stored locally.'),
dict(param='FISC',score=2,stance='supports',key=BIL,where='p. 396',basis='fragmentary',genre='admin',archive='inventories (Ḫattuša)',region='Empire',
 quote="In the tribute (MANDATTU) inventory text KUB 26.66 with dupl. KBo 18.153 rev. 15, two minas of silver held by Walwaziti and Pupuli are said to have been previously taken up by the queen.",
 note='Tribute inventories at the capital.'),
# ---------------------------------------------------------------- STD (undecided)
dict(param='STD',score=2,stance='supports',key=BIL,where='p. 396',basis='fragmentary',genre='admin',archive='inventories (Ḫattuša)',region='Empire',
 quote="KUB 42.66 rev. 4'–6' refers to weight?-stones (stamped) with the seal of the queen",
 note='Weights sealed by the queen: a palace standard (one text).'),
dict(param='STD',score=2,stance='supports',key=BIL,where='p. 367',basis='fragmentary',genre='legal',archive='instructions',
 quote="It makes reference to standard weights and scales, as well as bribery, but the context is too damaged to obtain a clear understanding.",
 note=''),
dict(param='STD',score=1,stance='qualifies',key=HOL,where='p. 39',basis='documented',genre='letters',archive='Ḫattuša; Maşat',
 quote="Dating of letters by historical criteria is often impossible. Although royal senders or receivers are indicated by name in the diplomatic correspondence, in the internal correspondence the king and queen are not identified by name. ... Hagenbuchner (1989a, 106) cites KBo 28.66, KBo 18.59, and KUB 3.80 as rare examples of letters that gives their dates.",
 note='No dating system in administrative writing: rules out STD 3 (measures and dating).'),
# ---------------------------------------------------------------- COMM
dict(param='COMM',score=2.5,stance='supports',key=HOL,where='p. 1',basis='documented',genre='letters',archive='Ḫattuša; Maşat; Ortaköy; Kuşaklı',
 quote="The texts recovered from the Hittite capital city, Ḫattuša, as well as from the three provincial centers that have yielded an appreciable number of tablets (Tapikka [Maşat Höyük], Šapinuwa [Ortaköy near Çorum], and Šarišša [Kuşaklı]), represent official correspondence carried on in the course of administrating the business of the king.",
 note='Royal letters reach provincial centres.'),
dict(param='COMM',score=2.5,stance='supports',key=BIL,where='p. 454',basis='documented',genre='letters',archive='Maşat',
 quote="In all instruction and oath texts, the king demands the direct loyalty of all of his nobles and high officials to himself alone, with no intervening layers of administration. The Maşat letters are particularly demonstrative of the micro-management of the Hittite king regarding various trivial matters.",
 note=''),
dict(param='COMM',score=2,stance='qualifies',key=HOL,where='p. 18',basis='documented',genre='letters',archive='Maşat',
 quote="Travel in winter within Anatolia was extremely slow and hazardous, and was avoided when possible. ... But the presence of ice and snow on the roads was always a reason not to travel",
 note='Seasonal limits on communication.'),
# ---------------------------------------------------------------- PRIV
dict(param='PRIV',score=0,stance='supports',key=HOL,where='p. 1',basis='fragmentary',genre='letters',archive='Ḫattuša; Maşat; Ortaköy; Kuşaklı',
 quote="Unfortunately, what private, unofficial letter writing went on has left no examples.",
 note='Silent record: absence of evidence, not evidence of absence.'),
dict(param='PRIV',score=0.5,stance='supports',key=VDH,where='p. 10',basis='fragmentary',genre='mixed',archive='mixed',
 quote="Finally, there is the near-total silence of the Hittite sources on trade.",
 note='Silent record.'),
# ---------------------------------------------------------------- LAW
dict(param='LAW',score=3,stance='supports',key=HOF,where='p. 5',basis='documented',genre='legal',archive='Ḫattuša (law manuscripts)',
 quote="Reforms and Modifications of the Laws. The following diachronic stages in the formulation of Hittite law can be distinguished.",
 note='The collection was revised by the crown from the Old to the New Hittite manuscripts.'),
dict(param='LAW',score=2.5,stance='qualifies',key=BIL,where='p. 452',basis='documented',genre='mixed',archive='mixed',region='Empire',
 quote="they oversaw the judicial activities of their local vassals, but were frequently in need of the Great King’s intervention",
 note='Royal justice exists but depends on the king in person.'),
]
