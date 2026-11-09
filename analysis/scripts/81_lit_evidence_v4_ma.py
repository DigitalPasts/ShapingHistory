"""Fifth round (8 Nov 2026), after ShG's second assessment. Middle Assyrian. ShG's notes: TCTL, TEMP, PAL (Llop "and others"),
LAW, COMM ("better as 3 but evidence is missing"), STD, SCHOOL (adjudicated 3), TERR need more field literature.
Correction: the file "Sigillophobe suppliers and idiosyncratic scribes" in the library is Henkelman's study of Achaemenid
Pārsa (Achaemenid History XVI), not Llop; Llop's Middle Assyrian work is not local and goes on the acquisition list.
Sources (local texts; printed pages from running heads):
- J. N. Postgate 2013, Bronze Age Bureaucracy (CUP): pdf n = p. n+11.
- S. Jakob 2003, Mittelassyrische Verwaltung und Sozialstruktur (CM 29): scanned spreads, page read from the running heads.
- F. A. M. Wiggermann 2008, "A Babylonian Scholar in Assur", in Studies Stol: spreads, pdf 4 = pp. 208-209."""
P='Middle Assyrian'
PG='postgateBronzeAgeBureaucracy2013'; JAK='jakobMittelassyrischeVerwaltungUnd2003'; WIG='wiggermannBabylonianScholarAssur2008'
E=[
# ---------------------------------------------------------------- COMM
dict(param='COMM',score=3,stance='supports',key=PG,where='p. 68',basis='documented',genre='letters',archive='Dur-Katlimmu',
 quote="the suspicion that it would have been sealed and enclosed in an envelope is confirmed by a letter from the king found at Durkatlimmu in which he writes \"I have sent a directive to Adaya, (and) I have sealed the envelope and the tablet with my seals\"",
 note='Sealed royal directives reach a provincial centre on the Habur.'),
dict(param='COMM',score=2.5,stance='supports',key=PG,where='p. 426',basis='documented',genre='admin',archive='mixed (Assur; Dur-Katlimmu; Tell Chuera)',
 quote="Royal commands (abat sarri) could come in a letter authenticated by a royal seal, and the word sipirtu ... is employed for requests brought by messenger from a different sector of the administration.",
 note='Written royal orders beside oral messages.'),
# ---------------------------------------------------------------- LAW
dict(param='LAW',score=2.5,stance='supports',key=PG,where='p. 36',basis='documented',genre='legal',archive='Middle Assyrian Laws, Tablet B',
 quote="one of the chancellors serving the king, the city scribe, the herald and the king's representatives shall be present. The person who is acquiring the village, the field or the house, the mayor (and) three elders of the village shall be present, shall have the herald proclaim",
 note='Land transfer under royal officials, with tablets written for the judges.'),
dict(param='LAW',score=2.5,stance='supports',key=PG,where='p. 61',basis='documented',genre='legal',archive='Middle Assyrian Laws, Tablet B',
 quote="in §§ 17-18 we read that a dissatisfied farmer could secure a written order from judges to authorise his use of water resources",
 note=''),
# ---------------------------------------------------------------- STD
dict(param='STD',score=2,stance='supports',key=PG,where='p. 52',basis='documented',genre='admin',archive='mixed',
 quote="Whether the official calendar had a year of 354 or of 360 days, there is no sign in the Middle Assyrian calendar of the intercalary months which had been used for centuries in Babylonia to adjust the lunar to the solar year",
 note='One official calendar and eponym dating; the Babylonian calendar was adopted under Tiglath-pileser I or Aššur-rēša-iši (n. 29): a turning-point candidate.'),
# ---------------------------------------------------------------- TCTL / TEMP
dict(param='TCTL',score=2.5,stance='supports',key=PG,where='p. 122',basis='documented',genre='admin',archive='Assur Offerings House (archive M4)',
 quote="a payment made on the instruction of (ina sipirti) an official outside the temple (Col. F: in Nos. 9 and 19 the Governor of the Land (i.e. Assur province); in No. 31 another provincial governor)",
 note='The temple\'s offerings office acts on governors\' orders and lends to palace officials.'),
dict(param='TEMP',score=1.5,stance='supports',key=PG,where='p. 122',basis='documented',genre='admin',archive='Assur Offerings House (archive M4)',
 quote="The \"debtors\" include a palace overseer (No. 23), the mayors of Sudugi (No. 7) and Kilizi (No. 31), a priest of Adad (No. 14), a palace scribe (No. 16), boatmen (Nos. 1; 20), a diviner (No. 22), a provincial governor (No. 29) and the Governor of the Land (No. 30).",
 note='The Aššur temple\'s supply is woven into the state system rather than run on its own estates.'),
# ---------------------------------------------------------------- SCHOOL (ShG adjudicated 3)
dict(param='SCHOOL',score=2.5,stance='supports',key=WIG,where='p. 209',basis='documented',genre='scholarly',archive='Assur (colophons)',
 quote="In the Middle Assyrian kingdom the position of tupsar sarre \"royal scribe\" was an elevated one. The title occurs only in the capital, close to the king ... The only function that is actually attested for Middle Assyrian royal scribes is that of teacher.",
 note=''),
dict(param='SCHOOL',score=2,stance='qualifies',key=WIG,where='p. 210',basis='documented',genre='scholarly',archive='Assur (colophons)',
 quote="The evidence indicates that there was never more than one \"royal scribe\" at a time; occasionally his \"son\" and student might succeed him (5 to 6), but non-royal scribes trained students too (8), and it was undoubtedly the king who had the final choice.",
 note='Training in scribal families, with one royal teacher at the top.'),
dict(param='SCHOOL',score=2.5,stance='supports',key=JAK,where='p. 537',basis='fragmentary',genre='admin',archive='Kar-Tukulti-Ninurta (MARV II 17)',
 quote="werden asû neben einem Beschwörer (āšipu), einem Seher (bārû) und einem Schreiber des Tafelhauses (ṭupšarru ša bēt ṭuppāte) als den bēlē perre zugehörig geführt, die bei der Anlage eines Gartens im Palast von Kār-Tukultī-Ninurta",
 note='A "scribe of the tablet house" in the royal palace.'),
# ---------------------------------------------------------------- TERR
dict(param='TERR',score=3,stance='supports',key=PG,where='p. 17',basis='documented',genre='royal',archive='royal inscriptions; Assur, Tell Chuera and Dur-Katlimmu lists',
 quote="Shalmaneser claims to have blinded and taken captive 14,400 people from Hanigalbat after defeating Šattuara, and Tukulti-Ninurta \"uprooted\" 28,800 \"Hittites\" from his campaign west of the Euphrates and moved them into \"my land\". Independent confirmation that such deportations did take place is provided by administrative documents",
 note='Sequence: Aššur-uballiṭ I independence; Adad-nārārī I and Shalmaneser I take Hanigalbat; Tukultī-Ninurta I west of the Euphrates (Reculeau 2022 already coded).'),
]
