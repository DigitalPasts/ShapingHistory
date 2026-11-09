"""Fourth round (4 Nov 2026): the works ShG added to the Literature folder on 4 Nov ("what was missing and more").
Settles the open ED IIIb TEMP/PAL/TCTL question (Schrakamp on the 'Sumerian temple city'), adds the first proof that a
reform was enacted (Urukagina, for turning point T1), the Sargonic letters (FAOS 19) for COMM, Schrakamp's Akkade chapter
(royal domains, provincial integration, Naram-Sin's administrative reform) and RlA 'Steuer A' for FISC, and Archi 2015 on
the temples of Ebla.
Page conventions (checked against the PDFs in /Research-current/Deeplomatics/Literature):
  Schrakamp 2013 (CDOG 7): PDF pages are two-page spreads; the chapter is PDF 229-238 = pp. 445-464.
  Schrakamp & Zolyomi 2025 (AoF 52): printed page = PDF page + 92.
  Schrakamp 2015 (AVO 15): printed page = PDF page + 296.
  Schrakamp 2017 (RessourcenKulturen 5): printed page = PDF page + 70.
  Schrakamp 2018 (Water Management, BSAW 53): printed page = PDF page + 109.
  Kienast & Volk 1995 (FAOS 19): scanned spreads, OCR; PDF 12 = p. 1, PDF 13 = pp. 2-3, PDF 22 = pp. 20-21.
  Paoletti & Schrakamp 2011 (RlA 13): two-column text; quotes rejoined across columns. Sections 1-2 Schrakamp, 3 Paoletti.
  Archi 2015: printed page = PDF page - 25.
Fields as in 81_lit_evidence_v2_ed_ebla.py (basis, genre, archive, region all read by hand)."""
S13='schrakampSumerischeTempelstadtHeute2013'; SZ='schrakampReevaluatingReformsUrukagina2025'
S15='schrakampUrukaginaUndGeschichte2015'; S17='schrakampRessourcenUndHerrschaft2017'
S18='schrakampIrrigation3rdMillennium2018'; KV='kienastSumerischenUndAkkadischen1995'
RLA='paolettiSteuerBabylonien3Jahrtausend2011'; AR='archiEblaItsArchives2015'
E=[
# ------------------------------------------------------------------ ED IIIa (north, Kiš)
dict(period='ED IIIa',param='PRIV',score=2,stance='qualifies',key=S17,where='p. 89',basis='fragmentary',genre='mixed',archive='none (extrapolated)',region='north (Kiš)',
 quote='Wirtschaft und Gesellschaft waren durch eine starke Privatwirtschaft, tributäre Wirtschaftsformen und einen hohen Anteil privaten Grundeigentums gekennzeichnet, das sich in Händen des Herrschers konzentrierte',
 note='Schrakamp summarizing Steinkeller (1993, 1999) on the pre-Sargonic north. Private land is concentrated in the ruler\'s hands, so this is royal more than private ownership; n. 6 notes that Yoffee 1995 thinks the north-south dichotomy overdrawn.'),
dict(period='ED IIIa',param='FISC',score=2,stance='supports',key=RLA,where='p. 162 (§ 2, Schrakamp)',basis='fragmentary',genre='admin',archive='Fara',region='north (Kiš)',
 quote='Fāra-Texte über Truppen aus Uruk, Lagaš, Umma, Šuruppag, Adab und Nippur, die einem wohl von Kiš geführten Städtebund angehörten, könnten wie das Ur III-zeitl. bala Verpflichtungen zur Stellung von (Arbeits-)Truppen belegen.',
 note='Hedged ("wohl", "könnten"). Agrees with Bramanti 2020 p. 29 on the Fara league; adds that Kiš probably led it.'),
# ------------------------------------------------------------------ ED IIIb: temple and palace (Schrakamp)
dict(period='ED IIIb',param='TEMP',score=2,stance='supports',key=S13,where='p. 445 (abstract)',basis='substantial',genre='admin',archive='Girsu',
 quote='the Early Dynastic temple was an institution that managed a subsistence economy and provided for the population, while the centre of power and the state was the palace, which controlled the flow of strategic goods, long-distance trade and the military and could dispose of the property and production of the temple.',
 note='The direct test of the "Sumerian temple city" against the c. 1,700 Girsu texts (p. 447). Temples are a major institution (2), not the dominant one (3). This is the source ShG asked for on ED IIIb TEMP.'),
dict(period='ED IIIb',param='PAL',score=3,stance='supports',key=S13,where='p. 445 (abstract)',basis='substantial',genre='admin',archive='Girsu',
 quote='the centre of power and the state was the palace, which controlled the flow of strategic goods, long-distance trade and the military and could dispose of the property and production of the temple.',note=''),
dict(period='ED IIIb',param='TCTL',score=3,stance='supports',key=S13,where='p. 450',basis='documented',genre='admin',archive='Girsu',
 quote='Der Palast kontrollierte demnach die Erzeugnisse des Tempels und leitete Überschüsse dem Fernhandel zu. Diese Beispiele zeigen, daß der Palast den Fluß von Metall, Edelmetall, Prestige- und Luxusgütern sowie Fernhandel und Diplomatie kontrollierte und Produkte des Tempels abschöpfte.',
 note='p. 451: the ruler himself mustered temple troops in the palace (AWEL 3; DP 135), and 17 clay "olives" record troop contingents from several temples posted on the city wall, i.e. a central palace administration.'),
dict(period='ED IIIb',param='TEMP',score=2,stance='supports',key=S13,where='p. 452',basis='documented',genre='admin',archive='Girsu',
 quote='Die Tempel verwalteten die Felder, beschäftigten große Teile der Bevölkerung hauptsächlich in Land- und Gartenwirtschaft, Fischerei und Viehzucht, boten sie für Arbeits- und Wehrdienst auf und sicherten im Gegenzug durch Rationen ihren Unterhalt.',
 note='Same page: "Zentrum der militärischen und wirtschaftlichen Macht war jedoch der Palast, der Militär, Fernhandel und den Verkehr strategischer Güter kontrollierte und auf Tempelbesitz zugreifen konnte."'),
dict(period='ED IIIb',param='TEMP',score=2,stance='supports',key=S13,where='p. 454',basis='documented',genre='admin',archive='Umma',
 quote='Damit erscheinen auch die Tempel im Nachbarstaat Umma als Institutionen, die in erster Linie Subsistenzwirtschaft betrieben, die im Tempel beschäftigte Bevölkerung versorgten und Tempelbeschäftigte für öffentliche Arbeiten und für Wehrdienst bereitstellten.',
 note='A second archive (Umma) gives the same picture, so the temple result is not only a Girsu effect.'),
dict(period='ED IIIb',param='PRIV',score=1.5,stance='qualifies',key=S13,where='p. 456',basis='fragmentary',genre='royal',archive='royal inscriptions',
 quote='Die Reformtexte belegen damit eine Verwaltungsreform, deren Kern in der nominellen Übertragung der Eigentumsrechte der Felder an die Tempel und der Abschaffung von Amtsmißbrauch durch Funktionäre bestand. Beides kann als Maßnahme zur Eindämmung der ausufernden Privatwirtschaft verstanden werden.',
 note='A "rampant private economy" of officials before Urukagina; read from the reform texts (royal), so fragmentary.'),
dict(period='ED IIIb',param='BUR',score=2,stance='supports',key=S13,where='pp. 456-457',basis='documented',genre='admin',archive='Girsu',
 quote='Die Umsetzung der Reform ist an den Unterschriften der Texte des Bau-Tempels abzulesen.',
 note='The colophons change at the reform: under Lugalanda "house of the ruler\'s wife", under Urukagina "property of Bau". A document-form change tied to a political act (turning point T1). [format]'),
dict(period='ED IIIb',param='TCTL',score=3,stance='supports',key=SZ,where='p. 93',basis='substantial',genre='admin',archive='Girsu',
 quote='These were subservient to the palace, through which the ruler controlled the circulation of strategic resources, long-distance trade and the military and interfered with the temples.',
 note='p. 93: Lagaš has "ca. 150 royal inscriptions, ca. 1800 archival documents", almost all from one household (e2-mi2 / Bau), which employed about 1,000 people.'),
dict(period='ED IIIb',param='FISC',score=2,stance='supports',key=SZ,where='p. 105',basis='documented',genre='royal',archive='royal inscriptions',
 quote='“the m a š k i m official (responsible) for (the custom) that all the temple-administrators delivered d u b s i g (-contributions) to the palace”',
 note='Urukagina\'s reform text (FAOS 5/1 Ukg. 4-5); p. 111: archival texts prove that the maškim "authorized the debiting of arrears and the charging of penalties and collected these payments". Levies flow from temples to the palace.'),
dict(period='ED IIIb',param='TCTL',score=2.5,stance='supports',key=SZ,where='p. 111',basis='documented',genre='admin',archive='Girsu',
 quote='the removal of the m a š k i m agrees with the assumption that Urukagina’s decrees were meant to ascertain the ruler a more direct control of the state and its assets.',
 note='p. 110: the maškim vanishes from the records from Urukagina\'s accession year (Ukg. E1), and the new ownership formula appears in the colophons from the same year. p. 111: "(some of) Urukagina’s acts were evidently implemented and ... his claims cannot be taken as mere propaganda." This dates turning point T1 to Ukg. E1 from the archive itself.'),
dict(period='ED IIIb',param='PAL',score=3,stance='supports',key=S18,where='p. 124',basis='substantial',genre='admin',archive='Girsu',
 quote='Above all, the temples were subservient to the palace, which interfered in the temple economies, was the center of royal power, and administered by the ruler (ensi2), who acted as the earthly steward of the gods.',
 note='Same page: the Bau household held at least 9,000 ha and employed c. 1,200 people; "This characterization likewise applies to other temple archives, such as the contemporary temple of Inanna of Zabala".'),
dict(period='ED IIIb',param='TCTL',score=2.5,stance='supports',key=S18,where='p. 182',basis='documented',genre='admin',archive='Girsu',
 quote='conducted by the ruler, who drew on the contingents of corvée troops mobilized by the temples of the state',
 note='Primary canals and regulators were built by the ruler with temple corvée; the temples kept up the lower-level works. p. 182: "a bipartite administrative and economic structure that was typical of the entire state".'),
dict(period='ED IIIb',param='HIER',score=2,stance='supports',key=S18,where='p. 182',basis='documented',genre='royal',archive='royal inscriptions',region='Lagaš',
 quote='the construction of new primary canals is almost exclusively reported in the inscriptions of Urnanše and his grandson Eanatum probably reflects their attempt to establish a four-level irrigation network upon the unification of the cities of Lagaš into a single state',note='A multi-city state with one irrigation hierarchy.'),
dict(period='ED IIIb',param='TERR',score=2,stance='qualifies',key=S15,where='p. 360',basis='documented',genre='royal',archive='royal inscriptions',
 quote='Da Lugalzagesis Reich nach seiner Nippur-Inschrift Umma, KI.AN und Zabalam, die Kultzentren Uruk, Larsa, Ur und Nippur sowie ausweislich der religiösen Titel auch Ereš, Eridu und Keš umfasste',
 note='Reporting Sallaberger & Schrakamp 2015. Lugalzagesi\'s rule over Adab is "durch das Meskigala-Archiv gut dokumentiert". Applies to the last years of ED IIIb only, so coded as qualifying the period picture; p. 303 places Urukagina at "den Wechsel von Partikularismus und Kleinstaaterei zum Territorialstaat".'),
dict(period='ED IIIb',param='TCTL',score=2.5,stance='supports',key=S15,where='p. 365',basis='documented',genre='admin',archive='Girsu',
 quote='Diese Texte belegen, dass auch andere Wirtschaftseinheiten Truppen aufbieten mussten und dokumentieren zudem die Aufstellung von Wachmannschaften durch bestimmte Berufsgruppen wie Hirten.',
 note='The 17 wall-guard tablets from Urukagina\'s reign: troop levies on several temple households.'),
dict(period='ED IIIb',param='FISC',score=2,stance='supports',key=RLA,where='p. 162 (§ 2, Schrakamp)',basis='documented',genre='admin',archive='Girsu; Umma',
 quote='In (prä)sarg. Zeit war für die Nutzung institutionellen (Pacht-)Landes (aša5 apin-lá, aša5 dubsig) (zusätzlich zur Pacht) eine Bewässerungsabgabe (maš aša5/a-šà-ga, maš ki-duru5) in Silber (und Kleinvieh) zu leisten.',
 note='Same column: "Urukagina rühmt sich in den „Reformen“, neben anderen Gebühren die dubsig-Abgabe der Tempelverwalter abgeschafft zu haben."'),
dict(period='ED IIIb',param='COMM',score=1,stance='supports',key=KV,where='p. 1',basis='fragmentary',genre='letters',archive='Girsu',
 quote='Nur sechs präsargonische Briefe (fünf aus Girsu, einer unbekannter Herkunft), deutlich erkennbar an der abweichenden Formulierung der Briefeinleitungsformel sind bezeugt.',
 note='p. 2: asGir 1 is a letter from the temple administrator of Ninmar to Enentarzi, temple administrator of Ningirsu: correspondence inside one state, no royal network.'),
# ------------------------------------------------------------------ Ebla (Archi 2015)
dict(period='Ebla',param='TEMP',score=0,stance='supports',key=AR,where='p. 20',basis='documented',genre='admin',archive='Ebla palace G',
 quote='The temples in Ebla did not derive income from direct ownership of land. Their personnel consisted normally of one or two “purification servants” (pa4-šeš) for each god.',
 note='Same page: "These temples, altogether irrelevant as centres of economic power, formed part of the palace organisation." The source is the palace archive, so the absence rule caps this at fragmentary.'),
dict(period='Ebla',param='TCTL',score=3,stance='supports',key=AR,where='p. 20',basis='documented',genre='admin',archive='Ebla palace G',
 quote='These temples, altogether irrelevant as centres of economic power, formed part of the palace organisation.',
 note='p. 256: the priestess of Hadabal was one of the few women "high enough to use Palace lands for their own support", so cult personnel lived on palace land.'),
# ------------------------------------------------------------------ Old Akkadian (Schrakamp 2017; FAOS 19; RlA)
dict(period='Old Akkadian',param='PAL',score=3,stance='supports',key=S17,where='p. 82 (abstract)',basis='documented',genre='mixed',archive='Girsu; Adab; Umma; Nippur',
 quote='This ‘northern’ RESOURCECULTURE was borne by a secular and autocratic kingship with territorial claims to power, characterised by patrimonial dominion, a network of royal patronage, and a tributary or palace-economy based on royal land holdings.',
 note='p. 82: the period has "rund 8000 Keilschrifttexten" from "über 20 Fundorten".'),
dict(period='Old Akkadian',param='TCTL',score=3,stance='supports',key=S17,where='p. 82 (abstract)',basis='documented',genre='mixed',archive='Girsu; Adab; Umma; Nippur',
 quote='administered and exploited through a centralised administration, the inclusion of the provincial economies of the former city-states into the royal household, and the establishment of rural agricultural domains.',
 note='p. 108: royal land purchases in Girsu/Lagaš and Umma were "Faktisch ... Enteignungen, die zu Lasten der Tempel gingen".'),
dict(period='Old Akkadian',param='BUR',score=3,stance='supports',key=S17,where='p. 83',basis='documented',genre='admin',archive='Girsu; Adab; Umma; Nippur',
 quote='Zugleich schreibt man Naramsin eine umfassende Verwaltungsreform zu, die sich in erster Linie in der reichsweiten Einheitlichkeit der Urkunden aus staatlichen Verwaltungsinstitutionen, der Standardisierung von Maßen und Gewichten, der Einrichtung königlicher Stützpunkte und einer deutlich auf die Hauptstadt Akkade gerichteten Zentralisierung niederschlug.',
 note='The Naram-Sin reform as a dated turning point: empire-wide uniform documents after the Great Revolt. [format] (mentions document uniformity).'),
dict(period='Old Akkadian',param='STD',score=3,stance='supports',key=S17,where='p. 83',basis='documented',genre='admin',archive='Girsu; Adab; Umma; Nippur',
 quote='der Standardisierung von Maßen und Gewichten',note='Part of the Naram-Sin reform passage (see BUR).'),
dict(period='Old Akkadian',param='STD',score=2,stance='qualifies',key=S17,where='p. 98',basis='documented',genre='admin',archive='Mesag; Lugalra; Šuilišu (crown domains)',
 quote='belegen außerdem ein Nebeneinander lokaler und standardisierter bzw. „königlicher“ Maße und Verwaltungspraktiken',
 note='In the crown-domain archives of the south, local and royal measures were used side by side.'),
dict(period='Old Akkadian',param='BUR',score=2,stance='qualifies',key=S17,where='p. 103',basis='documented',genre='admin',archive='Mesag; Lugalra; Šuilišu (crown domains)',
 quote='Der Gebrauch der akkadischen Verwaltungssprache und -praxis, die typisch akkadischen Tafelformate und ihre Lokalisierung im Umland der Provinzhauptstädte weisen diese Institutionen als Neugründungen und Fremdkörper im sozioökonomischen Gefüge des Südens aus.',
 note='Same page: the lack of contact with the provincial administrations points to "eine strikte Trennung der königlichen und der lokalen Wirtschaftsverwaltung auf Provinzebene": two parallel bureaucracies. [format]'),
dict(period='Old Akkadian',param='FISC',score=2.5,stance='supports',key=S17,where='p. 112',basis='documented',genre='admin',archive='Girsu; Umma',
 quote='Der Überblick über die ensi2-Archive von Girsu/Lagaš und Umma zeigt, dass auch die sumerischen Provinzzentren fest in die königliche Tributwirtschaft integriert waren.',
 note='p. 98: two thirds of Mesag\'s land counted as crown land whose yield was owed to the king, recorded as grain deliveries to Akkade (BIN 8, 122).'),
dict(period='Old Akkadian',param='HIER',score=3,stance='supports',key=S17,where='p. 112',basis='documented',genre='admin',archive='Girsu; Umma',
 quote='die zwar aus der lokalen Elite stammten, aber fest in das Netzwerk königlicher Patronagen integriert, an die Weisungen ranghöherer akkadischer Funktionäre gebunden, dem Herrscher loyal ergeben waren und somit als königliche Funktionäre auf Provinzebene betrachtet werden dürfen.',
 note='The governors (ensi2) as royal officials. p. 104: "Die Provinzen des Nordens befanden sich unter direkter Kontrolle des Herrscherhauses".'),
dict(period='Old Akkadian',param='FISC',score=2,stance='qualifies',key=RLA,where='p. 162 (§ 2, Schrakamp)',basis='fragmentary',genre='admin',archive='Girsu; Adab; Umma; Nippur',
 quote='Viktualienlieferungen institutioneller oikoi des Südens nach Akkade deutet man vorbehaltlich als S.',note='"vorbehaltlich": a cautious reading of deliveries as tax.'),
dict(period='Old Akkadian',param='COMM',score=2,stance='supports',key=KV,where='p. 1',basis='documented',genre='letters',archive='Girsu; Adab; Umma; Nippur',
 quote='Die sargonischen (und: Gutäer-zeitlichen) Belege verteilen sich auf Babylonien und seine Randgebiete',
 note='111 letters: southern Babylonia 70, northern 9, periphery 32 (Diyala, Ešnunna, Gasur, Susa, Tell Brak), against six pre-Sargonic letters. Correspondence of state officials across the empire; no relay-station records, so 2 rather than 3.'),
dict(period='Old Akkadian',param='STD',score=2,stance='qualifies',key=KV,where='p. 3',basis='documented',genre='letters',archive='Girsu; Adab; Umma; Nippur',
 quote='Nur in Südbabylonien sind etwa zwei Drittel aller Briefe (44 von 69) in sumerischer Sprache abgefasst; bei den Briefen in akkadischer Sprache trägt dort immer mindestens einer der Korrespondenten einen semitischen Namen; in Nordbabylonien und in den Randgebieten bedient man sich ausnahmslos des Akkadischen.',
 note='Akkadian as the language of state correspondence everywhere except the Sumerian south: a regional limit on standardization.'),
# ------------------------------------------------------------------ Ur III (RlA, Paoletti; Schrakamp 2017)
dict(period='Ur III',param='FISC',score=3,stance='supports',key=RLA,where='p. 163 (§ 3, Paoletti)',basis='substantial',genre='admin',archive='Umma, Girsu, Irisaĝrig (provincial)',
 quote='Das zentrale staatliche Abgabe- und Leistungssystem auf Provinzebene war bala „Wechselamt“. Die ca. 20 Provinzen des Kernlandes erfüllten jeweils in bestimmten Perioden oder Monaten Verpflichtungen gegenüber der Zentralverwaltung',
 note='The periphery paid gún ma-da in fixed rates of livestock; "Der Staat beanspruchte im Mittel ⅓ der Produktion verschiedener Wirtschaftsbereiche".'),
dict(period='Ur III',param='BUR',score=3,stance='supports',key=RLA,where='p. 163 (§ 3, Paoletti)',basis='substantial',genre='admin',archive='Umma, Girsu, Irisaĝrig (provincial)',
 quote='Ein System von Wertäquivalenzen ermöglichte die Umrechnung aller Produkte und Arbeitskräfte in Silber, das die Zentralverwaltung in regelmäßigen Abrechnungen verschiedener Berufsgruppen erfasste.',note=''),
dict(period='Ur III',param='TCTL',score=3,stance='supports',key=S17,where='p. 116',basis='documented',genre='mixed',archive='Umma, Girsu, Irisaĝrig (provincial)',
 quote='knüpften sie in der Konzeption des Einheitsstaates, der herausragenden Stellung des Königs und seiner Vergöttlichung, der königlichen Kontrolle über Grund und Boden und den Verwaltungsstukturen in Vielem an das Reich von Akkade an, selbst wenn Urnamma und Šulgi das Grundeigentum der Tempel in Teilen nominell wiederherstellten',
 note='Schrakamp 2013 p. 456 n. 59: Šulgi\'s administrative reform in his 21st year transferred fields to the temples (Steinkeller 1987), a parallel to Urukagina and relevant to turning point T4.'),
]
