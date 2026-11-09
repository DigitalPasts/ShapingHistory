"""Fifth round (8 Nov 2026), after ShG's second assessment. Old Assyrian. ShG's notes: COMM adjudicated 3 ("the whole point
of the Old Assyrian system is that it's built around trade and messages"); SCHOOL adjudicated 1 (cite Beyer); BUR (Beyer and
Dercksen); PAL (Michel; Barjamovic); TERR (Forlanini; Kaneš not Kaniš; more find spots between Assur and Kaneš; Kouwenberg's
chapter in Vita 2021); FISC, LAW, TCTL, TEMP, PRIV, STD need more field literature. Turowski 2026 (a first-millennium Uruk note)
is removed from OA HIER by 97_guard.
Sources (local texts; printed pages from running heads):
- M. T. Larsen 2015, Ancient Kanesh (CUP): pdf n = p. n+13.
- K. R. Veenhof 2010, "Ancient Assur: The City, its Traders, and its Commercial Network", JESHO 53: 39-82: pdf n = p. n+38.
- W. Beyer 2019, The Identification of Scribal Hands on the Basis of an Old Assyrian Archive (diss. Hamburg): pdf n = p. n+9.
- N. J. C. Kouwenberg 2021, "Old Assyrian", in J.-P. Vita (ed.), History of the Akkadian Language (HdO 152), ch. 15:
  pdf n = p. n+48.
- J. G. Dercksen 2008, "The Assyrian Colony at Kanesh", in G. Wilhelm (ed.), Hattuša-Boğazköy (CDOG 6), pp. 109-124: OCR,
  pdf 2 = p. 109.
- M. Forlanini 2009, "Upper Mesopotamia in the Middle of the 17th Century B.C. According to the Hittite Texts", KASKAL 6:
  49-78: pdf 1 = p. 49.
Michel's PAL work and Barjamovic's Anatolian monograph are not in the local library beyond the OHANE chapter already coded
(Michel 2008 PIHANS 111 is on Assyrian men and Anatolian wives); see the acquisition list."""
P='Old Assyrian'
LAR='larsenAncientKaneshMerchant2015'; VEE='veenhofAncientAssurCity2010'; BEY='beyerIdentificationScribalHands2019'
KOU='kouwenbergOldAssyrian2021'; DER='dercksenAssyrianColonyKanesh2008'; FOR='forlaniniUpperMesopotamiaMiddle2009'
E=[
# ---------------------------------------------------------------- COMM (ShG adjudicated 3)
dict(param='COMM',score=3,stance='supports',key=VEE,where='p. 46',basis='substantial',genre='letters',archive='Kültepe (Kaneš), lower town',
 quote="They were communicated by means of official letters sent to kārum Kanesh, which had to make their contents known to the other colonies (occasionally by \"messengers of the kārum\") and supervise and enforce their implementation. More direct control by, and contact with, the mother-city was secured by the \"Envoys of the City,\" regularly present in Anatolia ... The Assyrian colonial system was accordingly rather tightly knit, characterized by a good coherence and much mutual communication.",
 note='Official letters from Assur to the colonies, relayed by the Kaneš colony to the others.'),
dict(param='COMM',score=3,stance='supports',key=VEE,where='p. 46',basis='substantial',genre='letters',archive='Kültepe (Kaneš), lower town',
 quote="Members of the same trading families regularly lived in one of the colonies and in Assur—with caravans, traders, messengers, and mail regularly traveling both ways",
 note='A regular mail across more than 1,000 km (six weeks each way).'),
dict(param='COMM',score=3,stance='supports',key=LAR,where='p. 151',basis='documented',genre='letters',archive='Kültepe (Kaneš), lower town',
 quote="Obviously, relations with the local authorities both in northern Syria and in Anatolia were monitored closely by the Kanesh colony and ultimately by the city assembly in Assur. There are several references to special envoys of the city assembly, who came to Kanesh and perhaps even stayed there for long periods.",
 note=''),
# ---------------------------------------------------------------- PAL / TCTL / TEMP
dict(param='PAL',score=0,stance='supports',key=LAR,where='p. 110',basis='documented',genre='letters',archive='Kültepe (Kaneš), lower town',
 quote="One of the extraordinary facts about Assur is that there is no reference in the texts we possess to a royal palace. Obviously, the king had a grand house somewhere ... but its absence from the texts tells us that the palace played a very small, possibly no role in the administrative and economic life of the city.",
 note='Economic functions sit with the City Hall, not a palace.'),
dict(param='PAL',score=0.5,stance='qualifies',key=VEE,where='p. 52',basis='documented',genre='letters',archive='Kültepe (Kaneš), lower town',
 quote="The ruler of the city too bought merchandise that he gave in commission to agents traveling to Anatolia and some records mention the silver earned for him that was sent back to Assur.",
 note='The ruler trades like a merchant (Larsen p. 110: royal princes carry the king\'s shipments).'),
dict(param='TEMP',score=1,stance='supports',key=VEE,where='p. 52',basis='documented',genre='letters',archive='Kültepe (Kaneš), lower town',
 quote="This also involved persons attached to the temples, since the latter invested in trade, by using the numerous votive gifts they received, and we even meet a priest who was the owner of a warehouse and another who officiated as līmum, that is manager of the City Hall.",
 note='Temples are investors in private trade, not large economies.'),
dict(param='TCTL',score=1,stance='qualifies',key=LAR,where='p. 127',basis='fragmentary',genre='admin',archive='Acemhöyük (bulla)',
 quote="We have two seals from the Old Assyrian period that are said to belong to the City Hall. One, found impressed on a bulla in the palace archive at Acemhoyuk, has the legend: Belonging to divine Assur. Of the import tax of City Hall.",
 note='The god Aššur and the city government are fused; there is no separate royal control over temples.'),
# ---------------------------------------------------------------- FISC
dict(param='FISC',score=1.5,stance='supports',key=LAR,where='p. 128',basis='documented',genre='letters',archive='Kültepe (Kaneš), lower town',
 quote="It seems likely that the City Hall managed both the granary and the central treasury, and there is evidence that metals were assayed and that the standard weights were kept here. Certain taxes were paid to City Hall, such as an export tax on caravans leaving for Anatolia and an import excise on the silver brought back.",
 note='City taxes on trade, not on land or people.'),
dict(param='FISC',score=1.5,stance='supports',key=VEE,where='p. 51',basis='documented',genre='royal',archive='Assur royal inscriptions; eponym lists',
 quote="The institution of a līmum, an annually appointed official who managed the important City Hall and was responsible for the City’s finances, took place at the beginning of his reign",
 note='Turning point inside the period: Erišum I creates the eponym office that runs the city finances.'),
dict(param='FISC',score=1,stance='qualifies',key=DER,where='p. 114',basis='documented',genre='legal',archive='Kültepe treaties (Level Ib)',
 quote="The Treaty with Hahhum stipulates the right of the Palace to levy nishatum-tax and to pre-empt a limited number of textiles. A similar privilege was afforded to the Palace of Kanesh, where the nishatum-tax on incoming tin was usually at the rate of 2 to 65",
 note='Most taxes the merchants paid went to Anatolian palaces under treaty, not to Assur.'),
# ---------------------------------------------------------------- LAW
dict(param='LAW',score=2,stance='supports',key=LAR,where='p. 122',basis='documented',genre='legal',archive='Kültepe (Kaneš), lower town',
 quote="The year eponymy stands as the counterpart to the assembly, which functioned as a high court and as a decision-making body, the highest political authority in the city",
 note=''),
dict(param='LAW',score=2,stance='supports',key=LAR,where='p. 117',basis='documented',genre='letters',archive='Kültepe (Kaneš), lower town',
 quote="The general rules that governed the way in which the trade was conducted and the relationship to other groups were formulated here, as we can see from one of the king's letters to the Kanesh colony: The letter with a verdict of the City dealing with gold that we sent to you, that letter is invalid. ... In accordance with the words of the stela",
 note='City verdicts and a law stela bind the colonies.'),
dict(param='LAW',score=2,stance='supports',key=LAR,where='p. 159',basis='substantial',genre='legal',archive='Kültepe (Kaneš), lower town',
 quote="hundreds of primarily judicial documents; they refer to its various activities, such as the appointment or certification of witnesses or the issuing of verdicts in concrete cases, but although numerous, these texts usually limit themselves to certain standardised phrases",
 note='A standard judicial procedure in the colony courts.'),
# ---------------------------------------------------------------- PRIV
dict(param='PRIV',score=3,stance='supports',key=VEE,where='p. 52',basis='substantial',genre='letters',archive='Kültepe (Kaneš), lower town',
 quote="But all this does not change the picture of a predominantly trading city, with a powerful merchant class that also played an important role in its administration.",
 note=''),
dict(param='PRIV',score=3,stance='supports',key=VEE,where='p. 48',basis='substantial',genre='letters',archive='Kültepe (Kaneš), lower town',
 quote="Assur was a trading city and in itself an important emporium, inhabited by many trading families, with a market and public and private warehouses.",
 note=''),
# ---------------------------------------------------------------- STD
dict(param='STD',score=2,stance='supports',key=LAR,where='p. 128',basis='documented',genre='letters',archive='Kültepe (Kaneš), lower town',
 quote="there is evidence that metals were assayed and that the standard weights were kept here",
 note='Weights kept by the City Hall; dating by the year eponym of the same office (p. 122).'),
dict(param='STD',score=1.5,stance='qualifies',key=LAR,where='p. 117',basis='documented',genre='legal',archive='Kültepe (Kaneš), lower town',
 quote="We also know that certain central procedures such as the joint-stock partnership were always formulated using the gold standard.",
 note='Standards are commercial conventions of the city, not imposed by a crown.'),
# ---------------------------------------------------------------- BUR (Beyer; Dercksen)
dict(param='BUR',score=1,stance='supports',key=BEY,where='pp. 11-12',basis='documented',genre='letters',archive='Kültepe (Kaneš), lower town',
 quote="Taking a professional scribes on a trip was certainly an option, but an inconvenient and expensive one. Therefore, it is more likely that at least most of the merchants were able to manage their own correspondence, and probably even everyday documents",
 note='Writing in the hands of merchants, not of an administrative corps.'),
dict(param='BUR',score=1.5,stance='qualifies',key=DER,where='p. 113',basis='documented',genre='letters',archive='Kültepe (Kaneš), lower town',
 quote="Detailed information about the assembly of a caravan in Assur stems from the so-called caravan accounts, letters sent by the representatives in Assur to the head of the Kanesh-branch.",
 note='Regular document types, but private ones (caravan accounts, sealed loads).'),
# ---------------------------------------------------------------- SCHOOL (ShG adjudicated 1)
dict(param='SCHOOL',score=1,stance='supports',key=BEY,where='p. 209',basis='documented',genre='letters',archive='Kültepe (Kaneš), lower town',
 quote="Almost nothing is known about Old Assyrian schooling. Michel noted that especially the school material discovered in Kaneš is mostly dated into the second phase of the trade, level Ib. ... And in only one letter, a boy or young man asks his father for a present for his teacher of the scribal arts.",
 note='CCT 4, 6e: "As you know, we are learning the scribal art. Send me an epattum-garment for my teacher".'),
dict(param='SCHOOL',score=1,stance='supports',key=BEY,where='p. 209',basis='documented',genre='scholarly',archive='Kültepe (Kaneš) school tablets',
 quote="Thus, it appears that even though the formal structure of the school tablets coincides with the Old Babylonian material, their content was adapted to the needs of the merchants",
 note='Training for trade inside merchant families.'),
dict(param='SCHOOL',score=1,stance='supports',key=KOU,where='p. 1107',basis='fragmentary',genre='scholarly',archive='Assur; Kültepe',
 quote="school texts (oab 139–40) with calculations and spellings of measurements and commodities",
 note=''),
dict(param='SCHOOL',score=1,stance='qualifies',key=BEY,where='p. 11',basis='documented',genre='letters',archive='Kültepe (Kaneš), lower town',
 quote="Kryszat, who studied the Old Assyrian syllabary, noticed two different traditions based on the selection of signs for certain phonetic values.",
 note='Two writing traditions, older and younger: no single school norm.'),
# ---------------------------------------------------------------- TERR (Forlanini; find spots)
dict(param='TERR',score=0,stance='supports',key=VEE,where='p. 48',basis='documented',genre='mixed',archive='mixed',
 quote="it was not the capital of an empire. Assyria as a country did not yet exist; the city-state covered a limited territory of unknown size, just north of the fertile Mesopotamian flood plain",
 note=''),
dict(param='TERR',score=0.5,stance='qualifies',key=FOR,where='p. 49',basis='documented',genre='mixed',archive='Hittite texts; Mari; Tell Leilan',
 quote="The Hittite interest in northern Mesopotamia was aroused at first by the decline of the Assyrian trade organisation, whose caravans had crossed the area for 250 years",
 note='A network across Upper Mesopotamia, not territorial rule.'),
dict(param='TERR',score=0.5,stance='qualifies',key=DER,where='p. 110',basis='documented',genre='mixed',archive='Kültepe; Alişar; Boğazköy; Acemhöyük; Kaman-Kalehöyük; Kayalıpınar',
 quote="At present, texts (including inscribed clay bullae) have been unearthed in Kültepe (about 23,000), Alişar Höyük, Boğazköy, Acemhöyük, Kaman Kalehöyük and Kayalıpınar",
 note='The map now shows these find spots (and Nuzi and Tell Leilan, Kouwenberg 2021 p. 1108); the network spans about 40 colonies and stations (Veenhof 2010 p. 46).'),
dict(param='HIER',score=1.5,stance='qualifies',key=VEE,where='p. 46',basis='documented',genre='letters',archive='Kültepe (Kaneš), lower town',
 quote="Of the Assyrian commercial settlements ten were spread out over northern Mesopotamia ... Another thirty were established in Anatolia",
 note='A ranked network of colonies under Kaneš and the City, but no provincial officials.'),
]
