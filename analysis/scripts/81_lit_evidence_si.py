"""Literature evidence for the SI periods (Hittite, Middle Elamite). Thinner than the main periods; gaps listed.
Format as 81_lit_evidence_ur3.py, with an explicit period per entry."""
WE='weedenHittiteEmpire2022'               # Weeden, M. 2022. The Hittite Empire. OHANE III, ch. 30, 529-622.
MN='mofidinasrabadiElamLateBronze2022'     # Mofidi-Nasrabadi, B. 2022. Elam in the Late Bronze Age. OHANE III, ch. 34, 869-977.
E=[
 dict(period='Hittite',param='TERR',score=3,stance='supports',key=WE,where='OHANE III, ch. 30, §30.2, p. 535',
  quote="The process that resulted in the development of this fragmented political landscape into a territorial formation can be illustrated by looking at the kinds of settlements where the elements of a central Anatolian culture associated with the Hittite state, the instruments of Hittite state control, and its administration developed"),
 dict(period='Hittite',param='HIER',score=2,stance='supports',key=WE,where='OHANE III, ch. 30, §30.4, p. 581',
  quote="The danger of installing family members as local kings (the equivalent of provincial governors) is well attested by empires throughout history, but this does not seem to have been a problem for Hittite succession south of the Taurus."),
 dict(period='Hittite',param='HIER',score=1,stance='qualifies',key=WE,where='OHANE III, ch. 30, §30.2, p. 544',
  quote="The Telipinu Edict tells us that Labarna established control over seven Central Anatolian towns, and sent his sons out to govern them ... It is also not always clear precisely to what degree these officials could be said to be “governing” the areas to which they were assigned.",
  note='Old Kingdom; the Empire period has the bēl madgalti frontier governors (specialist literature needed).'),
 dict(period='Hittite',param='LAW',score=2,stance='supports',key=WE,where='OHANE III, ch. 30, §30.2, p. 553',
  quote="It is possible that collections such as the Hittite Laws, the earliest manuscript of which is likely to be dated to around the time of Telipinu, grew during this period out of texts similar to these types."),
 dict(period='Middle Elamite',param='TEMP',score=3,stance='supports',key=MN,where='OHANE III, ch. 34, §34.3, p. 887',
  quote="While these texts provide insights into the central administration and religious life of the temple, they shed very little light on the daily life of ordinary people."),
 dict(period='Middle Elamite',param='PRIV',score=0,stance='supports',key=MN,where='OHANE III, ch. 34, §34.3, p. 887',
  quote="Moreover, archives from private houses and private legal texts are rare in the ME I phase. Other than a purchase contract from Susa dating to the reign of Tepti-ahar, the only private texts are a group of legal texts known as the “Malamir Tablets,”"),
 dict(period='Middle Elamite',param='SCHOOL',score=1,stance='supports',key=MN,where='OHANE III, ch. 34, §34.3, p. 884',
  quote="As was the case during the Sukkalmah period, ME I Elam witnessed the use of Mesopotamian cuneiform writing and the Akkadian language."),
 dict(period='Middle Elamite',param='BUR',score=2,stance='supports',key=MN,where='OHANE III, ch. 34, §34.5.2, p. 922',
  quote="Ginadu, the “archivist” (puhu teppu) of the ME I king Inšušinak-šar-ili ... Ginadu’s sarcophagus was found on the floor of a room (no. 19) in a building adjoining an administrative complex",
  note='Our measured Middle Elamite tablets are all from Haft Tepe (Section 4), so this is a single-archive period.'),
]
GAPS={'Hittite':'Bilgin 2018 (Officials and administration in the Hittite world); van den Hout 2020 (A history of Hittite literacy) for SCHOOL and BUR; Hoffner 1997 (Laws)',
      'Middle Elamite':'Haft Tepe administrative texts: Mofidi-Nasrabadi; Daneshmand; Glassner'}
