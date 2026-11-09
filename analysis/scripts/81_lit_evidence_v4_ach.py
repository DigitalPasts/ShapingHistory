"""Fifth round (8 Nov 2026), after ShG's second assessment on the desk. Achaemenid (one period; statements carry a region
when the literature speaks of one province). ShG asked for more, and more qualifying, citations for LAW, STD, TEMP, PAL
(undecided), FISC, HIER, PRIV, SCHOOL (Young 2024) and BUR.
Source: B. Jacobs and R. Rollinger (eds), A Companion to the Achaemenid Persian Empire (Wiley 2021), local text of
ShG's PDF (Literature folder). Printed pages are read from the running heads of each page (the PDF offset changes from
chapter to chapter): Pirngruber ch. 75 pp. 1087-1096; Quack ch. 39 pp. 553-566; Hoernes ch. 57 pp. 793-814; Gzella
ch. 66 pp. 951-965; Stolper ch. 7 pp. 87-100; Steele ch. 90 pp. 1315-1324; Kleber ch. 63 pp. 905-922; Wunsch ch. 68
pp. 981-991; Hackl & Ruffing ch. 67 pp. 967-979; Henkelman ch. 62 pp. 881-904; Henkelman ch. 86 pp. 1243-1270.
Young 2024 (KASKAL n.s. 1): pp. 341-360, page numbers from the PDF footers.
Tuplin 2015 (Justice of Darius, ShG added it 8 Nov): scanned spreads, OCR; PDF n = pp. 2n+70 and 2n+71."""
P='Achaemenid'
PIR='pirngruberJurisdiction2021'; QUA='quackEgypt2021'; HOE='hoernesRoyalCoinage2021'; GZE='gzellaBactria2021'
STO='stolperElamiteSources2021'; STE='steeleAstronomyAstrology2021'; KLE='kleberBabylonia2021'; WUN='wunschTempleEconomy2021'
HAC='hacklTaxesTributes2021'; HEN='henkelmanPersia2021'; HEW='henkelmanPracticeWorship2021'; YOU='youngApprenticeshipMaterialityTexts2024'; TUP='tuplinJusticeDariusReflections2015'
E=[
# ---------------------------------------------------------------- LAW
dict(param='LAW',score=2,stance='qualifies',key=PIR,where='p. 1088',basis='documented',genre='mixed',archive='royal inscriptions',
 quote='Contemporary research unanimously agrees that in these and other instances in royal inscriptions (DNa § 3, DSe §4, XPh § 4d), dāta does not refer to a unified law code as had been postulated by Albert T. Olmstead',
 note='No empire-wide law code: rules out 3 in its strict sense (law collection AND royal judges AND edicts).'),
dict(param='LAW',score=2.5,stance='supports',key=PIR,where='p. 1088',basis='documented',genre='legal',archive='Eanna; private archives',region='Babylonia',
 quote='In Babylonia, for example, such royal decrees (dātu ša šarri) can be demonstrated to have stipulated (and at least tentatively unitized) the amount of fiscal and customs obligations, as well as of penalty payments. Furthermore, they also regulated business transaction involving deposits (Kleber 2010: pp. 60–61, who also makes the case for translating dāta as “law,” 51–2).',
 note='Royal decrees with legal force, applied in Babylonian documents.'),
dict(param='LAW',score=2.5,stance='supports',key=PIR,where='p. 1093',basis='documented',genre='legal',archive='Eanna; private archives',region='Babylonia',
 quote='In the royal court (bīt dīni ša šarri), the more severe types of crimes, such as treason or perjury, are usually thought to have been adjudicated ... In them, a variable number – between three and eight, to be precise – of “royal judges” (dayyānū ša šarri and similar) dispensed justice ... Here, the Achaemenid Great Kings continued a tradition inherited from their Neo‐Babylonian predecessors',
 note='Royal courts and royal judges, continued from the Neo-Babylonian state.'),
dict(param='LAW',score=2,stance='qualifies',key=PIR,where='p. 1092',basis='documented',genre='mixed',archive='mixed',
 quote='In the context of this debate, also the absence of an empire‐wide law(‐code) and especially the practice of dispensing justice on the basis of individual cases – under the key word of Einzelfallgerechtigkeit – have been emphasized (e.g. Wiesehöfer 1995; another important critique is Kuhrt 2001).',
 note='Against Frei\'s "imperial authorization": justice case by case, no imperial code.'),
dict(param='LAW',score=2.5,stance='supports',key=QUA,where='p. 557',basis='documented',genre='legal',archive='Demotic Chronicle',region='Egypt',
 quote='It is well documented that on his initiative all existing laws of Egypt were collected and assembled, probably quite immediately after he reassured Persian rule in Egypt in his third year. Over the next years (until his regnal year 19), they were also translated into Aramaic in order to be accessible to the imperial administration.',
 note='A royal order to compile a provincial law collection for the imperial administration (Egypt only).'),
# ---------------------------------------------------------------- STD
dict(param='STD',score=2.5,stance='supports',key=GZE,where='p. 960',basis='documented',genre='admin',archive='Khalili (Akhvamazda) archive',region='Bactria',
 quote='The system of measures appears to correspond to evidence from both Elephantine in Egypt and Persepolis (Naveh and Shaked 2012: p. 37); it is thus indicative of at least some standardization in bookkeeping.',
 note='The same measures at the two ends of the empire and in the heartland.'),
dict(param='STD',score=2.5,stance='supports',key=HOE,where='p. 798',basis='documented',genre='mixed',archive='coins',
 quote='Paradoxically, it is not the siglos but the gold series whose weight was based on the shekel standard. Darius raised the weight of his gold coins, in comparison with the croeseid standard, from 8.06 g to 8.36 g to adapt it to the shekel. By contrast, the silver sigloi maintained the croeseid standard of 5.38 g initially.',
 note='A royal act aligning the imperial gold coinage with the Mesopotamian shekel; silver kept another standard.'),
dict(param='STD',score=2,stance='qualifies',key=STO,where='p. 96',basis='documented',genre='admin',archive='Persepolis Fortification',region='Persepolis',
 quote='Like the use of Elamite month names instead of transcribed Iranian month names (Hallock 1969: pp. 74–75), and use of Elamite synonyms for Iranian words, some of these choices were geographically conditioned. The Elamite options appear mostly in texts written to the northwest of Persepolis, along the route to Susa',
 note='Even within the heartland archive the month names were not uniform.'),
dict(param='STD',score=2.5,stance='qualifies',key=STE,where='p. 1316',basis='documented',genre='scholarly',archive='astronomical texts',region='Babylonia',
 quote='early in the Achaemenid period a fixed 19‐year cycle of intercalation was adopted (Britton 2007) ... Previously, regulation of the calendar was both the prerogative and the responsibility of the king ... After the introduction of the 19‐year cycle, however, responsibility for the administration of the calendar lay with the astronomical experts who were attached to the temples (Steele 2011a).',
 note='The Babylonian calendar became fixed, but by temple experts, not by royal imposition: a uniform calendar without a royal act.'),
# ---------------------------------------------------------------- BUR / SCHOOL
dict(param='BUR',score=3,stance='supports',key=GZE,where='p. 953',basis='documented',genre='letters',archive='Khalili (Akhvamazda) archive',region='Bactria',
 quote='These functionaries seem to have learned Aramaic as part of their scribal training according to the largely centralized linguistic standard of the Achaemenid chancery, including genre conventions such as the general structure of a letter and the proper forms of address.',
 note='One chancery standard across provinces (Bactria matches Egypt and the heartland).'),
dict(param='SCHOOL',score=2.5,stance='supports',key=GZE,where='p. 953',basis='fragmentary',genre='letters',archive='Khalili (Akhvamazda) archive',region='Bactria',
 quote='These functionaries seem to have learned Aramaic as part of their scribal training according to the largely centralized linguistic standard of the Achaemenid chancery',
 note='Training of Aramaic chancery scribes to one standard; inferred from the letters ("seem").'),
dict(param='SCHOOL',score=1,stance='supports',key=YOU,where='p. 346',basis='documented',genre='scholarly',archive='Uruk Ue XVIII houses',region='Babylonia',
 quote='A big part of the tablets found in Ue XVIII was the product of scribal training for pupils who studied Akkadian and Sumerian scholarly series in order to specialise in the art of the healer at a later stage. Various phases of the school curriculum are evident in the assemblage, highlighting the domestic context of apprenticeship.',
 note='ShG asked for Young 2024. Cuneiform schooling in Babylonia: shared curriculum, household locus (anchor 1).'),
dict(param='SCHOOL',score=1.5,stance='qualifies',key=YOU,where='p. 344',basis='documented',genre='scholarly',archive='Uruk Ue XVIII houses',region='Babylonia',
 quote='Although the members of the Šangi-Ninurta family did not bear any title showing an institutional affiliation, the colophons of their tablets show twice that they nonetheless had access to the collection of the Eanna temple.',
 note='Household teaching with access to temple holdings: between 1 and 2.'),
# ---------------------------------------------------------------- TEMP / TCTL
dict(param='TEMP',score=2.5,stance='supports',key=WUN,where='p. 981',basis='substantial',genre='admin',archive='Eanna; Ebabbar',region='Babylonia',
 quote='Babylonian temples were the cultic focus and economic centers for their regions. Far from being autonomous, self‐sufficient institutions operating an autarkic redistributive system (as was often assumed), the temples of the sixth and early fifth centuries BCE interacted with and depended on the outside economy.',
 note='Major institutions of their regions but embedded in a market economy: 2-3.'),
dict(param='TCTL',score=2.5,stance='supports',key=WUN,where='p. 981',basis='documented',genre='admin',archive='Eanna',region='Babylonia',
 quote='The main sanctuary was Esagil of Babylon ... which collected taxes from the other temples, ultimately for the benefit of the king, amounting to 3.5% of the agricultural income in the case of the Eanna of Uruk (Jursa 2010: pp. 68–70).',
 note='Levies on temples for the crown (anchor 2), channelled through Esagil.'),
dict(param='TCTL',score=3,stance='supports',key=WUN,where='p. 982',basis='documented',genre='admin',archive='Eanna; Ebabbar',region='Babylonia',
 quote='Most of the administrative functions that used to be vested in the king were delegated to the satrap of Babylon and Transpotamia. While the temples’ obligations toward the crown and the kings’ control remained or increased, the latter’s sponsorship for the temples gradually diminished ... As a result of Xerxes’ retaliation against those circles that had supported his contenders for the throne, the leading families in the major Babylonian cities that had staffed the higher echelons of the temples for ages were removed from their offices',
 note='Control kept or increased, patronage withdrawn; after 484 the crown removed the temple elites.'),
dict(param='TCTL',score=2.5,stance='supports',key=KLE,where='p. 914',basis='documented',genre='admin',archive='Eanna; Ebabbar',region='Babylonia',
 quote='Babylonian temples were state institutions but traditionally also a focal point of local power, identity, and prestige for the local urban elite. Already in the reign of Nebuchadnezzar the crown felt the need to introduce royal courtiers in local temples’ administrations in addition to the royal superintendent (qīpu).',
 note='State institutions with local elite power: 2-3.'),
dict(param='TEMP',score=1,stance='supports',key=HEN,where='p. 896',basis='fragmentary',genre='admin',archive='Persepolis Fortification',region='Persepolis',
 quote='The exceptional delivery of 9405 l of wine to a temple at Hakurtiš (NN 2240) suggests an institution of some importance, yet not integrated in the economic grid visible in the PFA',
 note='Temples in Fārs stand outside the institutional economy the archive records.'),
dict(param='TCTL',score=3,stance='supports',key=HEW,where='p. 1243',basis='documented',genre='admin',archive='Persepolis Fortification',region='Persepolis',
 quote='This reveals that the central administration worked with prescriptive documentation regulating sacrifices (a cultic calendar, lists of rites on wax boards, etc.; Henkelman 2008: pp. 283–285); that the director could intervene if necessary; that the authorities recognized the principle that the deities to receive state‐sponsored worship were simply those belonging to the place in question.',
 note='In the heartland, cult was provisioned and regulated by the state administration.'),
# ---------------------------------------------------------------- PAL / FISC
dict(param='PAL',score=3,stance='supports',key=HEN,where='p. 884',basis='substantial',genre='admin',archive='Persepolis Fortification',region='Persepolis',
 quote='The same traditional system is found at Persepolis more than a century later: The PFA describes a centralized (yet not all‐embracing) institutional economy under directorship of Parnakka. It had thousands of dependent workers known as kurtaš',
 note='The crown\'s institutional economy dominates the heartland record ("not all-embracing").'),
dict(param='PAL',score=3,stance='supports',key=HEN,where='p. 886',basis='substantial',genre='admin',archive='Persepolis Fortification',region='Persepolis',
 quote='In size, the territory of the Persepolis institutional economy roughly matches that of modern‐day Switzerland. This comparison also underlines the vertical organization of the landscape ... Lower valleys and larger intermontane plains were fully integrated in the institutional sphere. Higher altitudes, especially fit for summer pasture, fell outside',
 note='Scale of the royal economy in Fārs.'),
dict(param='PAL',score=1.5,stance='qualifies',key=HAC,where='p. 973',basis='documented',genre='admin',archive='Eanna; Murašû',region='Babylonia',
 quote='What limited and mostly indirect evidence we have for royal domain land indicates that they, too, were an important source of income for the crown. It is clear, however, that by comparison with private or temple land, such estates played a minor role with respect to the overall agricultural output.',
 note='In Babylonia the crown\'s own estates were minor; its weight came through taxation, not a palace economy.'),
dict(param='FISC',score=3,stance='supports',key=HAC,where='p. 974',basis='substantial',genre='admin',archive='Murašû; Eanna',region='Babylonia',
 quote='The central element of this system were land allotments (e.g. bīt qašti bow properties) granted by the crown or its representatives to numerous individuals or to a group of individuals (organized in kiṣru or hadru collectives) in return for a form of military service (Van Driel 2002: pp. 226–273).',
 note='Land-for-service system, organized in collectives under crown officials.'),
dict(param='FISC',score=2.5,stance='qualifies',key=HAC,where='p. 976',basis='documented',genre='admin',archive='Murašû; Eanna',region='Babylonia',
 quote='In contrast to Herodotus’ assessment, money taxes directly paid to the crown do not seem to have been the principal means by which the Persians exploited the resources of Babylonia. Instead, we see a system that was primarily geared toward the mobilization of workers and soldiers.',
 note='Qualifies the Herodotean picture of a monetary tribute list: heavy, but labour and service rather than an integrated money tax.'),
# ---------------------------------------------------------------- LAW: Tuplin 2015 (ShG: "See for example The Justice of Darius")
dict(param='LAW',score=2.5,stance='supports',key=TUP,where='p. 113',basis='fragmentary',genre='mixed',archive='royal inscriptions; Greek sources',
 quote='Use of the word data is evidence for the distinctive importance of something we can call ‘law’ in the interaction between imperial ruler and subjects. ... There is some other (at least partly) non-Greek evidence in favour of that view, viz. the collection of Egyptian native law ordered by Darius and the alleged commission to Ezra. ... It is my contention that, among the characteristics of that stable situation, a significant and distinctive one is the rule of law.',
 note='Tuplin calls his own argument "cumulative and impressionistic": royal law (data) as a hallmark of the empire, without an empire-wide code.'),
dict(param='LAW',score=2,stance='qualifies',key=TUP,where='p. 103 n. 134',basis='documented',genre='legal',archive='Babylonian legal texts',region='Babylonia',
 quote='In Babylonia, where the (much more extensive) documentation is of a different character, the few Iranian-named judges are a decided minority ... and even people with special titles such as ‘royal judge’, ‘judge of the palace-gate’ and databara or ‘judge of Gubaru or Artareme’ can have Babylonian names. (Babylonian-named judges even appear in Susa — a sign that the legal norms in use reflect the identity of the litigants and locus delicti, not the location of the process',
 note='Royal judicial titles exist, but the law applied followed the litigants (local law), not an imperial norm.'),
]
# Added 8 Nov (second pass, ShG on TERR: "Please add more qualifying citations"): the western provinces of the same
# Companion. Dusinberre ch. 43 pp. 595-611; Mehl ch. 44 pp. 613-621.
E.append(dict(param='TERR',score=2.5,stance='qualifies',key='mehlCyprusMediterranean2021',where='p. 615',basis='documented',genre='mixed',archive='Greek historians (Diodorus); inscriptions',region='Cyprus',
 quote="When some time after Euagoras’ death (374 BCE) Phoenicia and Cyprus revolted, both were subdued a few years later in 345 BCE. Nonetheless, the Great King Artaxerxes III did not replace indirect rule by direct administration.",
 note='City kings remain under Persian supremacy: the empire tolerates indirect rule at its edges.'))
E.append(dict(param='TERR',score=2.5,stance='qualifies',key='dusinberreAsiaMinor2021',where='p. 608',basis='substantial',genre='mixed',archive='archaeology; seals; funerary stelae',region='Asia Minor',
 quote="Achaemenid Anatolia was a place where imperial authority could be and was expressed powerfully, but it was also a place where individuals exercised autonomy, mostly in ways that allowed them to express their individual identity within the rubric of administrative authority.",
 note='Satrapal authority with local autonomy.'))
