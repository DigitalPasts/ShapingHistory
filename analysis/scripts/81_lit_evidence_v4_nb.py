"""Fifth round (8 Nov 2026), after ShG's second assessment. Neo-Babylonian. ShG's notes: LAW (Wunsch, Kleber, Holtz),
BUR, STD, TERR need more concrete citations; SCHOOL adjudicated 2.5 (Veldhuis 2003, Hackl on scribes in the periphery);
TEMP adjudicated 2.5 ("the crown in control of temples in a more complex way", Jursa and Gordin 2019 and more); PAL and
COMM undecided (Jursa's chapter in Radner 2014). Not in the library: Veldhuis 2003, Holtz 2014, the Wunsch articles on the
royal judges (acquisition list).
Sources (local texts; printed pages from running heads):
- M. Jursa and Sh. Gordin 2019, JANER 19: 35-54: pdf n = p. 34+n.
- M. Jursa 2014, "The Lost State Correspondence of the Babylonian Empire", in K. Radner (ed.), State Correspondence in the
  Ancient World (OUP), pp. 94-111: pdf n = p. n-14.
- K. Kleber 2008, Tempel und Palast (AOAT 358): pdf n = p. n+14.
- P. Gesche 2000, Schulunterricht in Babylonien (AOAT 275): scanned spreads (pdf 87 = pp. 138-139).
- J. Hackl 2017, "Babylonian Scribal Practices in Rural Contexts", in Berlejung, Maeir and Schüle (eds), Wandering Arameans
  (Harrassowitz), pp. 125-140: pdf n = p. 124+n."""
P='Neo-Babylonian'
JG='jursaUrukeanPriestsNeoBabylonian2019'; JR='jursaLostStateCorrespondence2014'; KLE='kleberTempelUnd2008'
GES='gescheSchulunterrichtBabylonien2000'; HAC='hacklBabylonianScribalPractices2017'
E=[
# ---------------------------------------------------------------- TEMP / TCTL (ShG: TEMP 2.5)
dict(param='TCTL',score=3,stance='supports',key=JG,where='p. 40',basis='documented',genre='admin',archive='Eanna; Ebabbar',
 quote="In Eanna, the power of priestly administrators (be they of Babylonian or local origin) was curtailed, and courtiers (ša rēši) and other bureaucrats with a link to the royal administration were brought in. Until the end of the Neo-Babylonian period, the kings continued to interfere with not only with the staffing, but also with the structure of the temple administrations’ top echelons",
 note=''),
dict(param='TCTL',score=3,stance='supports',key=JG,where='p. 44',basis='documented',genre='admin',archive='Eanna; Ebabbar',
 quote="The results were stronger imperial institutions, more centralization, and more royal control over bureaucratic processes in provincial cities.",
 note=''),
dict(param='TEMP',score=2.5,stance='qualifies',key=JG,where='p. 42',basis='documented',genre='letters',archive='Eanna; Nineveh letters',
 quote="The provincial priests’ rootedness in local networks that owed little or nothing to the king continued to come to the fore even after the end of the great political conflict between Assyria and Babylonia ... Nowhere is this clearer than in the interaction between priests and the royal officials delegated by the king to represent his interests in the provincial cities.",
 note='Temples remain local powers that royal officials must push (cf. p. 43, Ninurta-šarru-uṣur and the šatammu).'),
dict(param='TEMP',score=2.5,stance='qualifies',key=KLE,where='p. 335',basis='substantial',genre='admin',archive='Eanna',
 quote="Die Wollproduktion war der wichtigste Wirtschaftszweig Eannas zur Erwirtschaftung eines Silbereinkommens. Sichere Aussagen über die produzierte Gesamtmenge sind nicht möglich, Schätzungen belaufen sich auf 750 bis 1125 Tonnen Wolle pro Jahr. Ungefähr 70% dieser Menge wurde an königliche Institutionen verkauft.",
 note='A large temple economy whose main product went to the crown.'),
# ---------------------------------------------------------------- PAL (undecided)
dict(param='PAL',score=2.5,stance='supports',key=KLE,where='p. 335',basis='substantial',genre='admin',archive='Eanna',
 quote="Ungefähr 70% dieser Menge wurde an königliche Institutionen verkauft. Eine Textilproduktion für den Verkauf gab es am Tempel nicht. ... Neben dem Palast in Babylon war das Meerland einer der Hauptabnehmer der Wolle. Die Verarbeitung zu Textilien besorgten neben männlichen Webern auch Frauen, die wahrscheinlich zum Personal eines Palastes in der Stadt Madakalšu im Meerland gehörten.",
 note='Palace workshops in Babylon and the Sealand absorb the temple surplus.'),
dict(param='PAL',score=2,stance='qualifies',key=JR,where='p. 96',basis='documented',genre='royal',archive='Hofkalender (Nebuchadnezzar)',
 quote="the monarchy was in actual fact but one of three distinct elements whose interaction and shifting balance of power defined the structure of the Babylonian state in its core throughout its history in the first millennium BC, including the imperial phase. The other two elements were, first, the old Babylonian cities of the southern Mesopotamian alluvium and, second, the Chaldean and Aramean tribes",
 note='The palace shares power with the cities and the tribes.'),
# ---------------------------------------------------------------- COMM (undecided)
dict(param='COMM',score=2.5,stance='supports',key=JR,where='p. 111',basis='documented',genre='letters',archive='Eanna; Ebabbar (royal letters)',
 quote="The available documentation for royal correspondence during the Neo-Babylonian period gives us at best a glimpse of what must have been a regular stream of missives that were exchanged among the king, the court, and the royal chancellery on one hand and royal officials, priests, and office-holding urban notables in the cities of the empire.",
 note='A regular royal correspondence, mostly lost (state archives not found).'),
dict(param='COMM',score=2.5,stance='supports',key=KLE,where='p. 335',basis='documented',genre='admin',archive='Eanna',
 quote="Er erhielt Speisen von der Göttermahlzeit, die durch spezielle Boten regelmäßig an ihn überbracht wurden, selbst wenn er sich fernab der Hauptstadt, auf Feldzügen oder, im Falle Nabonids, in Arabien aufhielt.",
 note='Regular courier service from Uruk to the king, even to Arabia.'),
# ---------------------------------------------------------------- BUR
dict(param='BUR',score=2.5,stance='supports',key=JR,where='p. 111',basis='documented',genre='letters',archive='Eanna; Ebabbar (royal letters)',
 quote="Administrative procedures were in part bureaucratic and rational, as expected—the standardized structure of the letters and the probable use of documents sealed with the royal bureau seal (unqu) being cases in point. On the other hand, official hierarchies were obviously steep and comparatively unarticulated. ... This reflects the nature of the Babylonian administrative system as a patrimonial bureaucracy.",
 note='Standard letters and a royal bureau seal, but a patrimonial bureaucracy.'),
dict(param='BUR',score=3,stance='supports',key=JG,where='p. 40',basis='documented',genre='admin',archive='Eanna; Ebabbar',
 quote="Especially the most prominent of these contractors had royal backing, and their function was just as much streamlining of administrative procedures as controlling the temples’ resources in the crown’s interest.",
 note=''),
# ---------------------------------------------------------------- STD
dict(param='STD',score=3,stance='supports',key=JG,where='p. 46',basis='documented',genre='admin',archive='Eanna; Ebabbar',
 quote="Concomitantly, the Neo-Babylonian Empire pushed for an increasing countrywide standardization of procedures in the administration of the temples and the cult. The re-organization of the accounting cycles for the offerings (maššartu) sometime after the 24th year of Nebuchadnezzar is a case in point",
 note='A countrywide administrative reform dated to after Nbk 24.'),
dict(param='STD',score=2.5,stance='qualifies',key=JG,where='p. 48',basis='documented',genre='admin',archive='Eanna',
 quote="What would seem to be an innovation here is that the institution setting the standard is named: Esangila and Ezida were responsible—they set and presumably could adapt these rates as they saw fit.",
 note='The standards are set by the capital temples, not directly by the crown.'),
# ---------------------------------------------------------------- LAW
dict(param='LAW',score=2.5,stance='supports',key=KLE,where='p. 71',basis='documented',genre='legal',archive='Eanna',
 quote="Wie bereits einleitend erwähnt, war die Tempel- und Stadtversammlung (puhru) ein auf der städtischen Ebene angesiedeltes Gericht, das über Eigentumsstreitigkeiten, Kult- und Statusfragen und kleinere Delikte (z. B. Prügeleien) entschied. Schwere Delikte ... dürften in die Zuständigkeit eines königlichen Gerichtes gefallen sein. Aber auch Fälle, in denen der Tempel selbst und ein privater Bürger die Streitparteien waren, wurden vor einem Gericht in Babylon oder vor den „Richtern des Königs“ verhandelt.",
 note='Two tiers: local assemblies and royal courts.'),
dict(param='LAW',score=3,stance='supports',key=KLE,where='p. 72',basis='documented',genre='legal',archive='Eanna',
 quote="In der Zeit von 9 Kyr bis 3 Kam lässt sich noch ein anderes Team von zwei königlichen Richtern in Uruk nachweisen, denen ein Tontafelschreiber und ein Pergamentschreiber zugeordnet sind",
 note='Royal judges stationed in a provincial city, with their own scribes.'),
dict(param='LAW',score=2,stance='qualifies',key=KLE,where='p. 71',basis='documented',genre='legal',archive='Eanna',
 quote="war die Tempel- und Stadtversammlung (puhru) ein auf der städtischen Ebene angesiedeltes Gericht, das über Eigentumsstreitigkeiten, Kult- und Statusfragen und kleinere Delikte (z. B. Prügeleien) entschied.",
 note='Most justice remains local.'),
# ---------------------------------------------------------------- SCHOOL (ShG: 2.5)
dict(param='SCHOOL',score=2.5,stance='supports',key=GES,where='p. 139',basis='substantial',genre='scholarly',archive='school tablets (Sippar, Babylon, Uruk, Ur)',
 quote="Derartige Texte gehören nicht zu dem einheitlichen Curriculum, wie es aus den neu- und spätbabylonischen Schultafeln rekonstruiert werden kann, sondern sie wurden in der an den Schulunterricht anschließenden Ausbildung behandelt. Ein weiterer Hinweis darauf, daß die Tafeln in einer Umgebung entstanden sind, in der Wirtschaftstexte geschrieben wurden",
 note='One curriculum across the Babylonian cities.'),
dict(param='SCHOOL',score=2.5,stance='supports',key=HAC,where='p. 125',basis='substantial',genre='legal',archive='urban and rural legal records',
 quote="First millennium Babylonian, and that of the long sixth century in particular (c. 620–480 BCE), is characterized by a high degree of grammatical homogeneity, regardless of where and, albeit to a lesser extent, when it was committed to writing. This suggests that the process of dialect admixture and eventual levelling had taken place early on in the first millennium BCE",
 note='Uniform written Babylonian across the cities: a shared scribal training.'),
dict(param='SCHOOL',score=2,stance='qualifies',key=HAC,where='p. 138',basis='documented',genre='legal',archive='Āl-Yāhūdu and related (CUSAS 28, BaAr 6)',
 quote="The most obvious explanation for this asymmetry is the fact that the scribes of our documents are by comparison poorly trained which, in turn, enhanced this process of diffusion. What little we know about them suggests that they were trained in an urban setting (most likely in Nippur) and then sent to villages in the countryside, perhaps because they completed their scribal education at a relatively low level.",
 note='Periphery: scribes trained in the cities, less well.'),
# ---------------------------------------------------------------- TERR
dict(param='TERR',score=2.5,stance='qualifies',key=JR,where='p. 95 (fig. 4.1)',basis='documented',genre='mixed',archive='mixed',
 quote="Map indicating the maximum extent of the Babylonian Empire and the sites mentioned in the text. The shaded areas in the Arab desert and around Susa are contested regions under partial control of the Neo-Babylonian Empire.",
 note='Core plus contested margins.'),
]
# ShG on the Kleber LAW row (8 Nov): "We have neo Babylonian laws!! Find relevant citations". The Neo-Babylonian Laws
# themselves (Roth 1997: 143-149; Oelsner 1997) are not in the library and go on the acquisition list; Gesche 2000: 218
# n. 831 places the tablet in advanced professional training, not in the courts. Two statements on royal judges:
E.append(dict(param='LAW',score=2.5,stance='supports',key='demarelafontJudicialDecisionmaking2011',where='p. 342',basis='documented',genre='legal',archive='mixed (Babylon; Sippar; Uruk)',
 quote="In the Old Babylonian period, the title of ‘royal judge’ (di-ku5 lugal) was held by those judges who exercised justice on behalf and by proxy of the sovereign ... Royal judges are also attested in the Neo-Babylonian period (Wunsch 2000).",
 note='Royal judges act for the king; Wunsch 2000 goes on the acquisition list.'))
E.append(dict(param='LAW',score=2.5,stance='supports',key='demarelafontJudicialDecisionmaking2011',where='p. 341',basis='documented',genre='legal',archive='mixed',
 quote="While the usual term dayyānum ‘judge’ was no longer used for human judges in the Neo-Assyrian period, various high officials are attested in judicial roles (Radner 2003: 890). The same types of personnel were also active in Neo-Babylonian law cases (Oelsner, Wells, and Wunsch 2003: 919).",
 note='Crown officials judge beside temple assemblies.'))
