"""Literature evidence for the centralization codebook: Old Assyrian (Assur and the Anatolian trade, c. 2025-1720 BC).
Format as 81_lit_evidence_ur3.py."""
P='Old Assyrian'
A='arkhipovMiddleEastFall2022'   # Arkhipov, I. 2022. The Middle East after the fall of Ur: from Assur to the Levant. OHANE II, ch. 15, 311-407.
BJ='barjamovicKingdomHittitesAnatolia2022'  # Barjamovic, G. 2022. Before the kingdom of the Hittites: Anatolia in the Middle Bronze Age. OHANE II, ch. 17, 497-565.
E=[
 dict(param='TERR',score=0,stance='supports',key=A,where='OHANE II, ch. 15, §15.1.4, pp. 317-318',
  quote="Around 2025 bc, Assur gained independence from the rule of the Third Dynasty of Ur and became a city-state with a characteristic political structure ... Nothing is known about Assur’s political relations with its neighboring cities."),
 dict(param='TERR',score=1,stance='qualifies',key=BJ,where='OHANE II, ch. 17, §17.3, p. 515',
  quote="This three-tiered system formed a judicial hierarchy in which ports stood above stations, and the port at Kaneš stood above them all. The kārum in Kaneš answered directly to the governing City Assembly (puhrum/ālum ṣaher rabi) of Assur.",
  note='An extraterritorial commercial network, not territorial rule.'),
 dict(param='HIER',score=1,stance='supports',key=BJ,where='OHANE II, ch. 17, §17.3, pp. 514-515',
  quote="The Assyrians ranked their expatriate settlements based on their size and role in the trade network. Towns that were home to a sufficient number of traders to form a judicial assembly with an upper and a lower chamber were known as “ports” (kārum) in Assyrian ... This three-tiered system formed a judicial hierarchy"),
 dict(param='FISC',score=1,stance='supports',key=BJ,where='OHANE II, ch. 17, §17.2, p. 508',
  quote="Neither of the two inscriptions mention Anatolia, but they do refer to tax exemptions made on various commodities on the market of Assur, seemingly in an attempt to attract business."),
 dict(param='FISC',score=1,stance='supports',key=A,where='OHANE II, ch. 15, §15.1.4, p. 318',
  quote="public finance and commerce were the responsibility of the “City Hall” (bēt ālim) which was presided over by a magistrate appointed for a year (līmum, often translated as “year eponym”)."),
 dict(param='COMM',score=1,stance='supports',key=BJ,where='OHANE II, ch. 17, §17.4, p. 518',
  quote="a recurring feature in the texts from Anatolia in the Middle Bronze Age is the reference to inns or caravanserais that the Assyrian traders used as they passed through the region with heavy cargos. Inns were key points along the road",
  note='Infrastructure is commercial, not a state messenger service.'),
 dict(param='PAL',score=0,stance='supports',key=A,where='OHANE II, ch. 15, §15.1.4, pp. 317-318',
  quote="The city was ruled by an assembly that acted in concert with a hereditary prince who was the caretaker of the god Aššur; it was the god, and not the prince, who was considered the city’s king."),
 dict(param='PRIV',score=3,stance='supports',key=BJ,where='OHANE II, ch. 17, §17.1, p. 501',
  quote="merchants from the city of Assur ... play a particular role for our understanding of political and historical developments during the first half of the second millennium bc, since they brought with them the technology of cuneiform writing, and their business documents thus offer the first detailed re[cord]"),
 dict(param='BUR',score=1,stance='supports',key=A,where='OHANE II, ch. 15, §15.1.4, p. 318',
  quote="No later than in the twentieth century bc, Assur developed its own cuneiform syllabary for the local kind of Akkadian that we call Old Assyrian, at the time when most of Lower Mesopotamia still wrote Sumerian."),
 dict(param='SCHOOL',score=0,stance='supports',key=BJ,where='OHANE II, ch. 17, §17.5, p. 527',
  quote="A noticeable difference between the two hierarchies is the lack at Kaneš of the cadre of scribes, diviners, and healers present at the Hittite court.",
  note='Merchant literacy learned in households: Larsen 2015 (Ancient Kanesh) ch. on writing; Veenhof 2008 (OBO 160/5).'),
 dict(param='LAW',score=2,stance='supports',key=BJ,where='OHANE II, ch. 17, §17.3, p. 515',
  quote="A few commercial treaties survive to illustrate the specificities of the interactions between local authorities and the Assyrian commercial institutions ... It goes on to specify that culprits are to be extradited to the Assyrian community in case of bloodshed."),
 dict(param='STD',score=2,stance='supports',key=BJ,where='OHANE II, ch. 17, §17.2, p. 507',
  quote="Due to a few breaks and inconsistencies in the manuscripts, our modern-day reconstruction of the sequence, known as the Revised Eponym List (REL), has an uncertainty of just one or two years for the first 138 years of the period ... The entire list of officials corresponds to the years ca. 1970–1720 bc"),
]
GAPS={'TEMP':'Temple of Aššur as institution: Veenhof 2008 (OBO 160/5); Larsen 2015',
      'TCTL':'ruler as steward (ensi) of Aššur: Veenhof 2017 (Assur political organization)',
      'SCHOOL':'merchant literacy: Larsen 2015; Michel 2008 on women writing'}
