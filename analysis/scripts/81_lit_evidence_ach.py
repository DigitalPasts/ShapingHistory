"""Literature evidence for the centralization codebook: Achaemenid (539-331 BC). The main analysis merges Babylonia and
Persepolis; entries carry region='Persepolis' or 'Babylonia' where the statement is regional, for the SI split.
Format as 81_lit_evidence_ur3.py."""
P='Achaemenid'
PO='pottsPersianEmpireAchaemenid2023'   # Potts, D. T. 2023. The Persian Empire under the Achaemenid dynasty, from Darius I to Darius III. OHANE V, ch. 55, 417-520.
HE='hellerSatrapiesPersianEmpire2023'   # Heller, A. 2023. The satrapies of the Persian Empire: Babylonia and Assyria. OHANE V, ch. 59, 649-688.
E=[
 dict(param='TERR',score=3,stance='supports',key=PO,where='OHANE V, ch. 55, §55.2.4.5, p. 452',
  quote="It is a truism that conquering territory and laying claim to a kingdom or empire are one thing, but governing it and holding on to geographically disparate provinces are another. The extraction of wealth in a systematic, recurring fashion for the maintenance of the ruler’s estate ... are essential to the longevity of any state."),
 dict(param='HIER',score=3,stance='supports',key=HE,where='OHANE V, ch. 59, §59.6, p. 669',region='Babylonia',
  quote="Thereafter a new administrative unit was created, which received the designation “Babylonia and Across-the-River” ... and comprised Babylonia, Assyria, Northern Mesopotamia, and the lands west of the Euphrates ... At the local level, the Persians retained the administrative structures and offices in the districts, cities, and temples."),
 dict(param='HIER',score=3,stance='supports',key=PO,where='OHANE V, ch. 55, §55.2.4.5, p. 454',region='Persepolis',
  quote="The names of a number of administrators occur regularly in the Persepolis texts, most notably the director Parnakka (Greek Pharnaces), who sat atop the bureaucratic pyramid, answering directly to Darius I, and the deputy-director Ziššawiš."),
 dict(param='FISC',score=3,stance='supports',key=PO,where='OHANE V, ch. 55, §55.2.4.5, p. 452',
  quote="Perhaps no aspect of Persian imperial history has received as much attention in recent years as the administrative system in the Persian heartland, the details of which are preserved in the ca. 15,000 tablets, mainly written in Elamite, from the Persepolis Fortification archives ... The extraction of wealth in a systematic, recurring fashion"),
 dict(param='COMM',score=3,stance='supports',key=PO,where='OHANE V, ch. 55, §55.2.4.5, p. 454',region='Persepolis',
  quote="the Fortification texts are the records of a highly organized bureaucratic administration charged with booking the receipt, storage, and disbursement of a wide range of naturalia ... to pack animals, travelers, messengers, laborers, officials, nobility, members of the royal family, and deities"),
 dict(param='PAL',score=3,stance='supports',key=PO,where='OHANE V, ch. 55, §55.2.4.5, p. 454',region='Persepolis',
  quote="The Treasury texts, on the other hand, record payments in foodstuffs and uncoined silver."),
 dict(param='TEMP',score=2,stance='supports',key=HE,where='OHANE V, ch. 59, §59.8, p. 673',region='Babylonia',
  quote="The Eanna temple, whose archive also broke off at that time, functioned until early in the reign of Xerxes."),
 dict(param='TCTL',score=3,stance='supports',key=HE,where='OHANE V, ch. 59, §59.8, p. 673',region='Babylonia',
  quote="The “end of the archives” at Uruk, beginning in the year 520 bc, is best explained as the result of administrative restructuring ... But already under Cyrus, new administrative offices emerged, whose Persian designations underline the increasing influence of the new lords: ganzabāra (treasurer), umarzanapāta or uppadētu (city administrator), and databāra (judge)."),
 dict(param='PRIV',score=3,stance='supports',key=HE,where='OHANE V, ch. 59, §59.6, p. 669',region='Babylonia',
  quote="The functionaries and the entrepreneurs who acted on royal order, e.g., in the agricultural sector, largely remained in office.",
  note='Murašû and Egibi archives: Stolper 1985; Wunsch; Waerzeggers 2003 on the 484 BC break.'),
 dict(param='BUR',score=3,stance='supports',key=PO,where='OHANE V, ch. 55, §55.2.4.5, p. 454',region='Persepolis',
  quote="From a bureaucratic point of view, the texts fall into diverse categories, including records of single transactions, letter-orders, and journals (summaries or registers) ... constitute only a slice of the Persepolis bureaucracy which was “part of a larger mosaic of sources.”"),
 dict(param='LAW',score=3,stance='supports',key=HE,where='OHANE V, ch. 59, §59.8, p. 673',region='Babylonia',
  quote="The primary task of these new positions seems to have been to enforce the “king’s law” (data ša šarri)."),
 dict(param='STD',score=2,stance='supports',key=PO,where='OHANE V, ch. 55, §55.2.4.5, p. 455',
  quote="Darius I introduced, first, silver sigloi ... and later the gold Dareikos stater, or “daric,” weighing theoretically 8.36 g. Darius I’s monetary reform probably began, at the latest, by 510 bc. The limited circulation of this coinage, beyond western Asia Minor, however"),
 dict(param='STD',score=1,stance='qualifies',key=HE,where='OHANE V, ch. 59, §59.6, p. 669',region='Babylonia',
  quote="Although Cyrus had been “King of Anšan” since 559 bc, he began counting his regnal years anew upon his entry into Babylon, adopting the Babylonian dating system that reckoned the time from enthronement to the year’s end as an accession year."),
]
GAPS={'SCHOOL':'scribal training at Persepolis (Elamite, Aramaic) and in Babylonia: Henkelman; Gesche 2001; Jursa 2010',
      'PRIV':'Stolper 1985 (Entrepreneurs and Empire); Waerzeggers 2003/4 (The Babylonian revolts against Xerxes and the end of archives)',
      'COMM':'Henkelman & Jacobs on the Persian road system (halmi travel documents); Briant 2002'}
