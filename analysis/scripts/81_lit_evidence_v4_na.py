"""Fifth round (8 Nov 2026), after ShG's second assessment. Neo-Assyrian. ShG's notes: HIER (Mattila 2000; Groß), FISC
(Mattila 2018, not local), TCTL and TEMP ("too much missing literature"), LAW adjudicated 3 ("find citations, several"),
PRIV (Gaspa; Radner's provincial Urkunden; not local), COMM (Itach, Aster, McLellan, Faust 2023; not local), STD ("at
least 3 different" standards), PAL ("several more"), SCHOOL adjudicated 3 ("at least 5 more"), TERR (a chronological
sequence). The works not in the library go on the acquisition list in the next-stage guide.
Chronology: the reforms of Shalmaneser III (the King's Road, the imperial seal) and Sargon II (the vizier and chief judge,
the eponym order, the mina of Carchemish after 717) are tagged in the notes as turning-point candidates.
Sources (local texts; printed pages from running heads):
- R. Mattila 2000, The King's Magnates (SAAS 11): pdf n = p. n-10.
- K. Radner 2014, "An Imperial Communication Network: The State Correspondence of the Neo-Assyrian Empire", in Radner (ed.),
  State Correspondence in the Ancient World (OUP), pp. 64-93: pdf n = p. n-14.
- J. N. Postgate 1974, Taxation and Conscription in the Assyrian Empire (Studia Pohl SM 3): letter-spaced text layer,
  wording checked against the page; pdf n = p. n-21.
- M. Weeden 2023, OHANE IV ch. 46; F. M. Fales 2023, OHANE IV ch. 40 (cited by chapter, section and PDF page).
- Radner and Robson (eds) 2011, The Oxford Handbook of Cuneiform Culture: pdf n = p. n+32 (Démare-Lafont, Steele,
  Zamazalová chapters).
- E. Robson 2019, Ancient Knowledge Networks (UCL Press): pdf n = p. n-25.
- B. Menzel 1981, Assyrische Tempel (Studia Pohl SM 10): OCR of the notes volume; cited by note number."""
P='Neo-Assyrian'
MAT='mattilaKingsMagnatesStudy2000'; RAD='radnerImperialCommunicationNetwork2014'; PG='postgateTaxationConscriptionAssyrian1974'
WEE='weedenIronAgeStates2023'; FAL='falesAssyrianEmpirePerspectives2023'
DEM='demarelafontJudicialDecisionmaking2011'; STE='steeleMakingSenseTime2011'; ZAM='zamazalovaEducationNeoAssyrian2011'
ROB='robsonAncientKnowledgeNetworks2019'; MEN='menzelAssyrischeTempel1981'
E=[
# ---------------------------------------------------------------- HIER (Mattila 2000)
dict(param='HIER',score=3,stance='supports',key=MAT,where='p. 163',basis='documented',genre='mixed',archive='mixed (SAA letters, legal and administrative texts)',
 quote="During the reign of Sargon the system was in a process of some development, as is shown by the rise in importance of the vizier and the chief judge during his reign. The division of the office of the commander-in-chief and Sargon's revision of the eponym order ... may together well reflect his policy to control the power of these high officials",
 note='Turning-point candidate: Sargon II reorganises the top of the hierarchy.'),
dict(param='HIER',score=2.5,stance='qualifies',key=MAT,where='p. 162',basis='fragmentary',genre='mixed',archive='mixed',
 quote="Due to the lack of local archives ... little is known",
 note='The magnates left routine provincial business to deputies; how the provinces were run day to day is poorly documented.'),
# ---------------------------------------------------------------- LAW (ShG adjudicated 3)
dict(param='LAW',score=2.5,stance='supports',key=MAT,where='p. 163',basis='documented',genre='letters',archive='mixed (SAA letters, legal texts)',
 quote="the king's magnates convened as a royal council to settle judicial disputes, and especially cases where petitions against administrative officials had been raised",
 note='A royal council of magnates as a court of appeal against officials.'),
dict(param='LAW',score=2.5,stance='supports',key=DEM,where='p. 339',basis='documented',genre='legal',archive='mixed',
 quote="In the Neo-Assyrian period, the 'king's word' (abat šarri) overruled any earlier decision",
 note='Royal justice overrides local decisions.'),
dict(param='LAW',score=2,stance='qualifies',key=DEM,where='p. 341',basis='documented',genre='legal',archive='mixed',
 quote="While the usual term dayyānum 'judge' was no longer used for human judges in the Neo-Assyrian period, various high officials are attested in judicial roles",
 note='Justice is done by officials rather than by a separate judiciary; no law collection is known.'),
# ---------------------------------------------------------------- COMM / TERR / BUR (Radner 2014)
dict(param='COMM',score=3,stance='supports',key=RAD,where='p. 71',basis='documented',genre='letters',archive='state letters (SAA)',
 quote="The Neo-Assyrian state maintained a privileged communication system for state letters and envoys traveling on state business. This system is likely to be an innovation of the reign of Shalmaneser III (r. 858-824 BC), when a number of administrative reforms were undertaken that successfully consolidated the territorial gains of the past century ... All Assyrian governors had to help maintain this imperial communication network, which was known as the 'King's Road'",
 note='Turning-point candidate: the King\'s Road under Shalmaneser III.'),
dict(param='COMM',score=3,stance='supports',key=RAD,where='p. 74',basis='documented',genre='letters',archive='state letters (SAA)',
 quote="an innovation of the Neo-Assyrian state ... set the standard for communication speed for almost three millennia",
 note='The relay system (kalliu): letters passed to fresh couriers at post stations.'),
dict(param='TERR',score=3,stance='supports',key=RAD,where='p. 71',basis='documented',genre='royal',archive='state letters; royal inscriptions',
 quote="a number of administrative reforms were undertaken that successfully consolidated the territorial gains of the past century",
 note='Sequence: 9th-century reconquest, consolidation under Shalmaneser III, provincial reform under Tiglath-pileser III (Charpin; Fales 2023 already coded).'),
dict(param='BUR',score=3,stance='supports',key=RAD,where='p. 70',basis='documented',genre='letters',archive='state letters (SAA)',
 quote="any letter sealed by the imperial seal and delivered by the imperial relay postal service was expected to be handed to them in person and as a matter of urgency: several royal letters contain the explicit order to act \"the day you see this letter\"",
 note='Royal letters sealed with the imperial seal were to be acted on at once (the imperial seal is a Shalmaneser III innovation, p. 71).'),
# ---------------------------------------------------------------- TEMP / TCTL / PAL (Postgate 1974; Menzel 1981)
dict(param='TEMP',score=1,stance='supports',key=PG,where='p. 213',basis='documented',genre='admin',archive='mixed (letters, grants)',
 quote="the temples in the large Assyrian cities had lost their one-time self-sufficiency, and could not any longer be supported by the contributions ... of the community they served. Instead, they depended on the bounty of the kings who had in fact first placed them in that position by building bigger temples and endowing them with larger staff than the community could afford to maintain",
 note='Temples as royal foundations without an independent economy.'),
dict(param='TEMP',score=1.5,stance='qualifies',key=PG,where='p. 213 n. 2',basis='fragmentary',genre='admin',archive='Balawat (Mamu temple); Kalhu (Nabû temple)',
 quote="As observed by van Driel, the picture is a little one-sided, and liable to stress the importance of royal intervention, because of the nature of the sources. Evidence for the temples' independent activities could however have been quoted by him from the economic archives of the Mamu temple at Balawat ... and the Nabu temple at Kalhu",
 note='Postgate notes the picture is one-sided: the Mamu temple at Balawat and the Nabû temple at Kalhu archives show some activity of their own.'),
dict(param='TCTL',score=2.5,stance='supports',key=PG,where='p. 214',basis='documented',genre='letters',archive='state letters (ABL 532)',
 quote="This letter shows that the responsibility for the supply of offerings to the Assur temple (at Assur) was shared between the provincial governors (and other high officials), who took it in turns to provide for a specified period.",
 note='ABL 532: the crown organises the supply of the Aššur temple through the provinces (Postgate compares the Ur III bala).'),
dict(param='TCTL',score=2.5,stance='supports',key=MEN,where='vol. II, n. 3904',basis='documented',genre='letters',archive='state letters (ABL)',
 quote="dass das Ausbleiben von Abgaben z.B. vom abarak bīt Aššur oder anderen königlichen Beauftragten für Tempelangelegenheiten (Akkullānu, [Daddî?], Iddina-Aššur) beim König ... angemahnt wird",
 note='Royal commissioners for temple affairs (index: "Beauftragte, königliche (für Tempelangelegenheiten)", pp. 288ff.) report temple arrears to the king.'),
dict(param='PAL',score=2.5,stance='supports',key=PG,where='pp. 204-205',basis='documented',genre='admin',archive='Harran census; Nimrud',
 quote="large, though probably not dominant, part of the available pasturage",
 note='Palace craftsmen "an offshoot of the palace"; palace flocks of 7,621 sheep in the Harran census.'),
dict(param='PAL',score=3,stance='supports',key=MAT,where='pp. 157-158',basis='documented',genre='admin',archive='mixed',
 quote="In addition to his duties as treasurer of the state, he was in charge of a border province, the Land of the Treasurer, on the northern border of Assyria ... the fact that the treasurer is first attested as early as 881 during the reign of Assurnasirpal ... shows continuity in the central role of the chief treasurer.",
 note='The magnates held provinces as offices of the royal household, continuous from Assurnasirpal II.'),
# ---------------------------------------------------------------- STD (three standards)
dict(param='STD',score=3,stance='supports',key=WEE,where='OHANE IV, ch. 46, §46.7 (PDF p. 884)',basis='substantial',genre='legal',archive='Neo-Assyrian legal contracts',
 quote="From the time that Sargon claimed the treasury of Carchemish, with its 2,100 talents of silver, the preferred monetary standard of the Assyrian Empire was switched from copper to silver, and specifically to silver according to the 'mina of Carchemish,' as the plentiful documentation in the Assyrian legal contracts demonstrates",
 note='Turning-point candidate: one silver standard across the empire after 717 BC (a second standard beside the eponym dating already coded).'),
dict(param='STD',score=3,stance='supports',key=STE,where='p. 472',basis='documented',genre='letters',archive='scholars\' letters to Esarhaddon and Assurbanipal (SAA 8, 10)',
 quote="From 7th-century bc Assyria we have a large body of correspondence sent by Assyrian and Babylonian scholars to the kings Esarhaddon and Assurbanipal, a significant number of which are concerned with the watch for the new moon at the end of a month, intercalation, and other calendrical matters ... From the letters and reports sent by these scholars we can understand how the calendar operated in practice.",
 note='A third standard: the calendar, with intercalation decided at court on the scholars\' reports of the new moon.'),
# ---------------------------------------------------------------- PRIV
dict(param='PRIV',score=2,stance='supports',key=FAL,where='OHANE IV, ch. 40, §40.5.3 (PDF p. 451)',basis='documented',genre='legal',archive='Dur-Katlimmu; Guzana; Burmarina; Til Barsip; Assur; Nineveh',
 quote="These finds demonstrate the widespread use of private legal documents in the form of clay tablets inscribed in cuneiform script and the Assyrian language, but frequently also in the Aramaic language and alphabetic script.",
 note='Private archives across the provinces.'),
# ---------------------------------------------------------------- SCHOOL (ShG adjudicated 3)
dict(param='SCHOOL',score=2.5,stance='supports',key=ROB,where='p. 136',basis='documented',genre='scholarly',archive='Huzirina (Sultantepe)',
 quote="the remains of a scribal school, run by Qurdi-Nergal and his descendants",
 note='About twenty šamallû apprentices, some sons of scribes of the turtānu.'),
dict(param='SCHOOL',score=2.5,stance='supports',key=ROB,where='p. 138',basis='documented',genre='scholarly',archive='Huzirina; Kullania',
 quote="predominantly the sons of provincial officials, priests and scholars ... destined for positions in the middle ranks of imperial governance",
 note='Kullania "hints that the school at Huzirina may not have been entirely exceptional".'),
dict(param='SCHOOL',score=2.5,stance='supports',key=ROB,where='p. 140',basis='documented',genre='scholarly',archive='Huzirina; Assur; Kalhu',
 quote="from across the middle echelons of the imperial governing classes",
 note='Training feeds the imperial administration.'),
dict(param='SCHOOL',score=1.5,stance='qualifies',key=ROB,where='p. 131',basis='documented',genre='scholarly',archive='Assur (house of the āšipus)',
 quote="the collection accrued over the course of the seventh century bc, as three generations of men wrote, copied and stored scholarly tablets as part of their training and professional business as āšipus of Aššur’s temple in Assur",
 note='Training within a scholarly household over three generations, not in a state school.'),
dict(param='SCHOOL',score=2.5,stance='qualifies',key=ZAM,where='p. 318',basis='documented',genre='letters',archive='scholars\' letters (SAA 10)',
 quote="presumably supervised by separate teams of teachers (Villard 1997: 144). In addition to the advanced scribal education and his training in the arts of war ... Assurbanipal was closely involved in the government of Assyria",
 note='The princes were educated at court by teams of scholars: elite education close to the crown.'),
]
