"""Literature evidence for the centralization codebook: Old Babylonian (Babylon dynasty, c. 1894-1595 BC; scored for the
period after Hammurabi's unification, with Postgate 2001 in 81_lit_evidence_cross.py). Format as 81_lit_evidence_ur3.py.
Read by 85_build_scores.py."""
P='Old Babylonian'
B='boivinKingdomBabylonKingdom2022'  # Boivin, O. 2022. The kingdom of Babylon and the kingdom of the Sealand. OHANE II, ch. 18, 566-655.
E=[
 dict(param='TERR',score=3,stance='supports',key=B,where='OHANE II, ch. 18, §18.6, p. 596',
  quote="With the conquest of the kingdom of Larsa, Babylon became a major power, harkening back to the kingdoms of Akkad and Ur"),
 dict(param='TERR',score=2,stance='qualifies',key=B,where='OHANE II, ch. 18, §18.11 (title) and §18.10, p. 610',
  quote="From a short-lived empire ... the large demographic movement that nearly emptied ancient urban centers, beginning in the reign of Samsu-iluna in the south",
  note='Unification of the south lasted c. 25 years (1763 to Samsu-iluna 11); for most of the period Babylon is a regional kingdom.'),
 dict(param='HIER',score=2,stance='supports',key=B,where='OHANE II, ch. 18, §18.8, p. 605',
  quote="Regional land administrators (šāpir mātim/nārim) and land managers (šassukkum) also had judicial functions, as did the province governor, whether dealing with cases at the provincial level or acting on behalf of the king. The judiciary thus permeated several levels of state administration."),
 dict(param='HIER',score=3,stance='qualifies',key=B,where='OHANE II, ch. 18, §18.9, p. 608',
  quote="The management of palace-controlled land, including irrigation, is best documented in the province of Larsa shortly after its conquest, in the letter archives of the governor Sin-iddinam and of the land manager Šamaš-hazir",
  note='Detailed hierarchy documented for one newly conquered province (Fiette 2018); not shown polity-wide.'),
 dict(param='FISC',score=2,stance='supports',key=B,where='OHANE II, ch. 18, §18.9, p. 608',
  quote="Individual landholders worked small land plots encumbered with rent owed to the palace (tenancy field; eqel biltim), or a service obligation, which could be military or other skilled work (subsistence field; šukūsum) ... Palace reserve fields were exploited by agricultural entrepreneurs (iššakkum)."),
 dict(param='PAL',score=2,stance='supports',key=B,where='OHANE II, ch. 18, §18.9, pp. 607-608',
  quote="Administrative and legal texts, even though they document primarily the management of palace-controlled land, paint the picture of a fairly fragmented land tenure situation, perhaps partly the result of a transition toward a tributary and entrepreneurial economy ... The palace marketed its surpluses of cereals, dates, wool, and other resources through merchants, thereby acquiring silver."),
 dict(param='TCTL',score=1,stance='supports',key=B,where='OHANE II, ch. 18, §18.7, p. 601',
  quote="kings of Babylon patronized the cloister, at least three of them sending a daughter there, beginning with Sumu-la-El ... The later Babylonian kings expended a great deal of effort and resources to keep the cult at Nippur active, as long as they possibly could."),
 dict(param='PRIV',score=3,stance='supports',key=B,where='OHANE II, ch. 18, §18.9, pp. 608-609',
  quote="Private ownership of arable land, defined by the possibility to alienate it, is attested only in northern Babylonia ... From their correspondence and various contracts, we learn that they loaned silver and owned property, including fields and orchards, that produced revenue."),
 dict(param='SCHOOL',score=1,stance='supports',key=B,where='OHANE II, ch. 18, §18.10, p. 612',
  quote="The extent of control exercised by the state over scribal training is a matter of debate. It is generally acknowledged that it was lower than in the earlier Ur III scribal academies. Old Babylonian scribal training normally took place in private houses, and the compositions copied there are generally less centered on the person of the king than in the Ur III corpus."),
 dict(param='SCHOOL',score=2,stance='qualifies',key=B,where='OHANE II, ch. 18, §18.10, pp. 612-613',
  quote="Some Sumerian compositions belonged to a standard curriculum, while others were less widely copied ... There were local differences, however, and institutional control may have been greater at Nippur than at Ur. This is suggested by the greater mastery of the Sumerian language achieved by students at Nippur, and by the lower degree of diversity in the Nippurite curriculum"),
 dict(param='LAW',score=3,stance='supports',key=B,where='OHANE II, ch. 18, §18.8, pp. 603-604',
  quote="the main body of the text, comprising at least 282 articles called “just pronouncements,” used the standard Old Babylonian dialect ... Nowadays positions are converging toward a middle ground, as most scholars consider that the LH has legislative content expressed in “examples” or “model decisions.”"),
 dict(param='LAW',score=3,stance='supports',key=B,where='OHANE II, ch. 18, §18.8, p. 606',
  quote="Attested throughout the dynasty, royal edicts of economic redress (mīšarum), mainly aimed at canceling arrears owed to the palace and non-commercial private debts, became a typical inaugural gesture in the reign of Hammurabi."),
 dict(param='LAW',score=2,stance='qualifies',key=B,where='OHANE II, ch. 18, §18.8, pp. 604-605',
  quote="Hammurabi’s role as a legislator was probably the corollary of his political function as king, and not specifically directed at weakening local structures. Indeed, most conflicts were resolved locally ... There is, however, no evidence of the direct application of the LH in any recorded judicial proceedings."),
 dict(param='STD',score=2,stance='supports',key=B,where='OHANE II, ch. 18, §18.6, p. 596',
  quote="Hammurabi first laid siege to Rim-Sin I’s northern stronghold Maškan-šapir, which apparently fell without battle. This change of allegiance cascaded down throughout the northern portion of the kingdom, as reflected in the year names used in documents.",
  note='Year names of Babylon replace local ones on conquest; calendar standardization needs Cohen 2015 / Sallaberger.'),
]
UR3=[  # cross-chapter disagreement recorded under Ur III
 dict(period='Ur III',param='SCHOOL',score=2,stance='contests',key=B,where='OHANE II, ch. 18, §18.10, p. 612',
  quote="It is generally acknowledged that it was lower than in the earlier Ur III scribal academies.",
  note='Contrasts with Garfinkle (OHANE II ch. 13, p. 148) on local scribal training under Ur III.'),
]
GAPS={'COMM':'OB royal messengers and Mari correspondence: Charpin 2010 (Reading and Writing in Babylon); Durand LAPO',
      'TEMP':'Charpin 2017 (La vie méconnue des temples mésopotamiens) on temple economies after Ur III',
      'BUR':'Fiette 2018 (Le palais, la terre et les hommes) on Larsa province administration; Charpin 2004 OBO 160/4',
      'STD':'Cohen 2015 on calendar unification under Samsu-iluna; Chambon 2011 on metrology'}
