"""Literature evidence for the centralization codebook: Early Old Babylonian (c. 2000-1900 BC: Isin I, early Larsa, Ešnunna).
Late Larsa under Rim-Sin (1822-1763) falls in the CDLI 'Old Babylonian' period and is recorded in RIMSIN below, which
85_build_scores.py adds to Old Babylonian. Format as 81_lit_evidence_ur3.py."""
P='Early Old Babylonian'
W='wagensonnerMiddleEastFall2022'  # Wagensonner, K. 2022. The Middle East after the fall of Ur: Isin and Larsa. OHANE II, ch. 14, 190-310.
D='degraefMiddleEastFall2022'      # De Graef, K. 2022. The Middle East after the fall of Ur: from Ešnunna and the Zagros to Susa. OHANE II, ch. 16, 408-496.
E=[
 dict(param='TERR',score=1,stance='supports',key=W,where='OHANE II, ch. 14, §14.1.1, p. 191',
  quote="In doing so, we also encounter other states in the area that managed to exert some level of independence for shorter periods of time, such as Uruk, Kisurra, and later Babylon",
  note='Competing regional kingdoms (Isin, Larsa, Uruk, Kisurra, Ešnunna, Babylon) after the fall of Ur.'),
 dict(param='TERR',score=2,stance='qualifies',key=D,where='OHANE II, ch. 16, §16.2.3, p. 424',
  quote="The military and political influence of Ešnunna was coupled with considerable cultural influence. During the reign of Yahdun-Lim, Mari adopted the writing system of the scribal school of Ešnunna."),
 dict(param='FISC',score=2,stance='supports',key=W,where='OHANE II, ch. 14, §14.2.4, p. 224',
  quote="Probably in one of his early years he “freed the inhabitants of Nippur from corvée labor and remitted the arrears of royalty, which weighed on their necks.”",
  note='Year name of Ur-Ninurta of Isin: corvée and royal arrears exist as regular obligations.'),
 dict(param='TEMP',score=2,stance='supports',key=W,where='OHANE II, ch. 14, §14.3.2, p. 232',
  quote="At Ur the archive of documents found in the temple of Ningal covers 120 years, from the ninth year of Gungunum to the nineteenth year of Rim-Sin. This long durée of archives shows that temples and their economy were not necessarily vulnerable to changes in the political landscape."),
 dict(param='TCTL',score=1,stance='supports',key=W,where='OHANE II, ch. 14, §14.2.4, p. 222',
  quote="Probably late in his reign, the king of Isin chose his daughter Enninsunzi as en priestess of Ningublaga by divination ... the king of Larsa installed Enninsunzi into this high religious office, probably two or three years later."),
 dict(param='BUR',score=2,stance='supports',key=W,where='OHANE II, ch. 14, §14.1.2, p. 200',
  quote="Sumerian occupied an important position in the intellectual, religious, and economic life of the period. Administrative and legal documents were generally written in Sumerian."),
 dict(param='BUR',score=3,stance='qualifies',key=W,where='OHANE II, ch. 14, §14.1, p. 190',
  quote="The decline and subsequent collapse of the tightly bureaucratized and centralized kingdom of Ur (ca. 2112–2004 bc; see chapter 13 in this volume) made room for a number of opportunists to establish local dynasties in the areas formerly held by Ur.",
  note='Continuity of Ur III administrative practice at Isin; specialist sources needed (Van De Mieroop 1987 on Isin crafts archive).'),
 dict(param='SCHOOL',score=2,stance='supports',key=D,where='OHANE II, ch. 16, §16.2.3, p. 424',
  quote="During the reign of Yahdun-Lim, Mari adopted the writing system of the scribal school of Ešnunna."),
 dict(param='LAW',score=2,stance='supports',key=W,where='OHANE II, ch. 14, §14.2.4, p. 220',
  quote="Lipit-Eštar’s construction of the “House of Justice” (Sumerian e2 niĝ2-si-sa2) is commemorated on a large number of small, headless cones ... This project was probably related to Lipit-Eštar’s establishment of a law code. Written in the Sumerian language, his laws are the earliest laws of the Old Babylonian period."),
 dict(param='LAW',score=2,stance='supports',key=D,where='OHANE II, ch. 16, §16.2.3, p. 424',
  quote="It was probably during Naram-Sin’s reign that the so-called Laws of Ešnunna were compiled, the first law collection to be composed in Akkadian."),
 dict(param='STD',score=1,stance='supports',key=W,where='OHANE II, ch. 14, §14.1.1, p. 197',
  quote="The wording of year names is highly flexible, adapting often to local tradition or the idiosyncrasies of a particular scribe. Many year names have short versions and long versions."),
]
RIMSIN=[  # Larsa under Rim-Sin, recorded under Old Babylonian
 dict(period='Old Babylonian',param='BUR',score=3,stance='supports',key=W,where='OHANE II, ch. 14, §14.9.3, p. 290, citing Charpin 2010a: 120',
  quote="Letters of the chancellery of Rim-Sin tended to use a standardized tablet format. These tablets are usually rather elongated and, depending on the length of the letter, were only partially inscribed ... Both letters and texts of the administration also exhibit other external features that distinguish them from earlier and later Old Babylonian archival texts. A striking external feature of these often elongated, rectangular tablets is their rather pointed corners (figure 14.8).",
  note='Direct published claim about tablet format under one regime: testable against our silhouettes (Larsa, Rim-Sin).'),
 dict(period='Old Babylonian',param='STD',score=3,stance='supports',key=W,where='OHANE II, ch. 14, §14.9.3, pp. 290-291',
  quote="Another reform concerned the calendar. We have already seen that, after Isin’s annexation, year names were counted consecutively. Up to this point, the administration used the traditional Nippur calendar of twelve months. In the middle of Rim-Sin’s reign, however, his administrators ... This new system is chiefly attested in texts from Nippur."),
 dict(period='Old Babylonian',param='LAW',score=2,stance='supports',key=W,where='OHANE II, ch. 14, §14.9.3, pp. 291-292',
  quote="Rim-Sin’s edicts in his twenty-fifth, thirty-fourth, and forty-first years partially counteracted these developments, as the palace intervened in the economic affairs of private businessmen ... No law collections survive from Rim-Sin’s reign."),
 dict(period='Old Babylonian',param='PRIV',score=3,stance='supports',key=W,where='OHANE II, ch. 14, §14.9.3, p. 291',
  quote="Probably the most influential businessman in this period was Balmunamhe, who amassed a huge amount of real estate during his career ... Most of the records at our disposal are legal transactions (sale, lease, hire, loan, partnership, marriage, adoption, and the division of inheritance)."),
]
GAPS={'PAL':'Isin palace craft archive: Van De Mieroop 1987 (Crafts in the Early Isin Period)',
      'HIER':'Larsa provincial administration before Hammurabi: Fiette 2018; Charpin 2004 (OBO 160/4)',
      'COMM':'no direct statement found in OHANE ch. 14 or 16'}
