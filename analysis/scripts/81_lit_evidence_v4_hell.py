"""Fifth round (8 Nov 2026), after ShG's second assessment. Hellenistic Babylonia. ShG's notes: COMM, BUR, PAL and LAW
undecided for want of citations; more for FISC, TERR, TEMP, STD (cite van der Spek 2006, not in the library), one more
qualifying PRIV; SCHOOL adjudicated 2 ("one is simply not enough").
Sources, all local texts of ShG's PDFs; printed pages read from running heads:
- J. Monerie 2017 [2018], L'économie de la Babylonie à l'époque hellénistique (SANER 14). The PDF offset changes by chapter
  (p. 54 = pdf 70; p. 183 = pdf 195; p. 238 = pdf 250; p. 281 = pdf 291).
- P. J. Kosmin 2014, The Land of the Elephant Kings (HUP): pdf n = p. n-17.
- J. Monerie and P. Clancier 2023, AoF 50: 63-82: pdf n = p. 62+n. (Corrects two earlier 'to verify' pages: the leather
  documents passage is p. 72, not p. 70.)
- P. Clancier 2009, Les bibliothèques en Babylonie (AOAT 363): OCR of scanned spreads, pdf n = pp. 2n-6 and 2n-5.
- M. Young 2024, KASKAL n.s. 1: 341-360: pdf n = p. 340+n."""
P='Hellenistic'
MON='monerieLeconomieBabylonieLepoque2018'; KOS='kosminLandElephantKings2014'; MC='monerieCompendiumOfficialCorrespondence2023'
CLA='clancierBibliothequesBabylonie2009'; YOU='youngApprenticeshipMaterialityTexts2024'
E=[
# ---------------------------------------------------------------- PAL (undecided)
dict(param='PAL',score=2.5,stance='supports',key=MON,where='p. 183',basis='documented',genre='mixed',archive='temple archives (Uruk, Babylon)',
 quote="À l’époque hellénistique, les biens de la Couronne étaient gérés par un organisme que les sources cunéiformes désignent par le nom de bīt šarri (litt. « maison du roi »), dans lequel les assyriologues s’accordent à reconnaître le basilikon des sources grecques. Cette institution remplissait également d’autres fonctions liées à l’évergétisme royal et au contrôle des activités des sanctuaires.",
 note='A royal economic office (basilikon) managing crown property and supervising the temples.'),
dict(param='PAL',score=2,stance='qualifies',key=MON,where='p. 183',basis='fragmentary',genre='mixed',archive='temple archives (Uruk, Babylon)',
 quote="La documentation cunéiforme ne permet pas de déterminer l’étendue des domaines royaux séleucides dans la région.",
 note='The size of the royal domain is unknown; the surviving archives are temple archives.'),
dict(param='PAL',score=2,stance='qualifies',key=MON,where='p. 236',basis='documented',genre='mixed',archive='mixed',
 quote="l’appui aux communautés urbaines anciennes (villes suméro-akkadiennes) et nouvelles (poleis), qui s’est traduit au cours du iiie s. par une politique de dévolution foncière destinée à s’assurer la collaboration politique de ces communautés à l’échelle locale. Les sources ne permettent pas d’estimer la part du domaine royal concernée par ces dévolutions, mais plusieurs indices portent à croire qu’elle ne fut pas négligeable",
 note='The crown gave away royal land to cities and temples: the palace sector is large but not dominant.'),
# ---------------------------------------------------------------- TCTL
dict(param='TCTL',score=2.5,stance='supports',key=MON,where='p. 183',basis='documented',genre='mixed',archive='temple archives (Uruk, Babylon)',
 quote="Cette institution remplissait également d’autres fonctions liées à l’évergétisme royal et au contrôle des activités des sanctuaires.",
 note='The royal bīt šarri supervised temple activity.'),
dict(param='TCTL',score=2,stance='qualifies',key=CLA,where='pp. 274-275',basis='documented',genre='mixed',archive='Esagil (astronomical diaries, chronicles)',region='Babylon',
 quote="C’est le šatammu qui représentait la ville auprès des rois assyriens, puis achéménides, séleucides et parthes, c’est-à-dire lorsqu’il n’y avait pas de pouvoir royal babylonien autonome. Il apparaît que ses responsabilités s’étendaient à une assez vaste région en dehors de Babylone. ... Les šatammu se succédaient de manière héréditaire",
 note='The temple head was hereditary, not a royal appointee, and spoke for the city to the king: temples as partners, not units of the state.'),
dict(param='TCTL',score=2.5,stance='supports',key=MC,where='p. 79',basis='documented',genre='letters',archive='Bīt Rēš (YOS 20, 87)',region='Uruk',
 quote="the many references to official orders (ṭēmu, ll. 4, 11, 19, 36, 37 and 39) and/or royal letters (l. 13) recorded over more than fifteen years for the sole refoundation of the Bīt Rēš, show an actual involvement from the first Seleucids in this kind of euergetism",
 note='Royal orders over fifteen years steer one temple refoundation.'),
# ---------------------------------------------------------------- TEMP
dict(param='TEMP',score=3,stance='supports',key=MON,where='p. 281',basis='documented',genre='mixed',archive='temple archives (Uruk, Babylon)',
 quote="À la fois lieux de culte, grands propriétaires terriens, conservatoires de la culture suméro-akkadienne et relais politiques du pouvoir royal, les sanctuaires occupaient une place essentielle dans le paysage institutionnel de la Babylonie hellénistique.",
 note=''),
dict(param='TEMP',score=2.5,stance='qualifies',key=MON,where='p. 285',basis='fragmentary',genre='mixed',archive='temple archives (Uruk, Babylon)',
 quote="Nous ne disposons pas, pour l’époque hellénistique, d’une documentation suffisante pour évaluer le rôle joué par les sanctuaires dans l’économie locale.",
 note='Monerie warns that in the sixth century the temples depended on crown subsidies (p. 285), and the Hellenistic evidence cannot show more.'),
# ---------------------------------------------------------------- BUR (undecided)
dict(param='BUR',score=2.5,stance='supports',key=MON,where='p. 283',basis='documented',genre='mixed',archive='temple archives (Uruk, Babylon)',
 quote="S’y ajoutaient de nombreux documents inscrits en grec ou en araméen sur peau ou (plus rarement) sur papyrus, qui avaient valeur légale devant les autorités royales. L’emploi de ces documents sur support souple était si répandu que les temples entretenaient un corps permanent de scribes spécialisés, appelés sepīrū, pour les produire.",
 note='A royal administration in Greek and Aramaic on leather, which the temples had to serve with their own scribes.'),
dict(param='BUR',score=3,stance='supports',key=MON,where='p. 238',basis='substantial',genre='admin',archive='Seleucia archive building (sealings)',
 quote="le témoignage de la documentation cunéiforme y est complété par l’apport de quelque 14 450 timbres fiscaux estampillés sur des bullae et cretulae d’argile mises au jour dans la région ... plus de 99 % de ces empreintes de sceaux fiscaux ont été mises au jour dans le bâtiment des archives de Séleucie-du-Tigre.",
 note='A central record office at the royal capital: a bureaucracy on perishable media, seen only through its sealings.'),
dict(param='BUR',score=2.5,stance='supports',key=KOS,where='p. 9',basis='documented',genre='letters',archive='Greek inscriptions',
 quote="Inscribed royal letters, issued in a recognizable chancery style by the Seleucid court or its agents, delivered instructions, appointed officials, established cults, and bestowed benefactions. These letters, sometimes inscribed alongside the forwarding notes of subordinates, provide crucial information for the titles, terminology, and hierarchical organization of the imperial administration.",
 note='A chancery and a written chain of command (empire-wide, mainly the west).'),
# ---------------------------------------------------------------- COMM (undecided)
dict(param='COMM',score=2.5,stance='supports',key=MC,where='p. 72',basis='documented',genre='letters',archive='astronomical diaries; chronicles; YOS 20, 87',
 quote="Cuneiform sources from Northern Babylonia such as the astronomical diaries and the chronicles regularly mention the reception of leather documents (kuššipištu) sent to local authorities by the royal chancery",
 note='Regular royal written orders reach the Babylonian cities.'),
dict(param='COMM',score=2.5,stance='supports',key=KOS,where='p. 166',basis='fragmentary',genre='mixed',archive='Greek and Latin sources; inscriptions',
 quote="Seleucid roadways and road infrastructure are of major importance as the material manifestation of royal movements, as instruments of territorial integration, and as a disciplinary mechanism for bodies and space. Our evidence for Seleucid “Royal Roads” is, inevitably, uneven and scant, but it is intriguing.",
 note='Royal roads exist, but the evidence is thin.'),
dict(param='COMM',score=2,stance='qualifies',key=KOS,where='p. 26',basis='documented',genre='mixed',archive='mixed',
 quote="“Trafficflow” maps of all known royal journeys identify the directionality and frequency of the kings’ movement and the practical and ideological significance of Royal Roads. It is shown that royal mobility was the major mechanism of provincial integration",
 note='Integration through the moving court rather than a fixed relay system.'),
# ---------------------------------------------------------------- HIER
dict(param='HIER',score=2.5,stance='supports',key=KOS,where='p. 9',basis='documented',genre='letters',archive='Greek inscriptions',
 quote="These letters, sometimes inscribed alongside the forwarding notes of subordinates, provide crucial information for the titles, terminology, and hierarchical organization of the imperial administration.",
 note=''),
# ---------------------------------------------------------------- FISC
dict(param='FISC',score=2.5,stance='supports',key=MON,where='p. 236',basis='documented',genre='mixed',archive='mixed',
 quote="Par ailleurs, l’imposition de service (ilku) aux propriétaires fonciers et les systèmes de dépendance rurale semblent avoir été repris à leur compte par les souverains séleucides.",
 note='Service dues on land kept from the Achaemenid system.'),
dict(param='FISC',score=3,stance='supports',key=MON,where='p. 283 n. 14',basis='documented',genre='legal',archive='Uruk private and temple archives',region='Uruk',
 quote="Le cas déjà mentionné de la taxation des ventes d’esclaves et de terres arables par l’administration séleucide à partir du milieu des années 270, qui entraîna l’enregistrement de ces",
 note='A royal sales tax that changed how contracts were written (see also Messina 2009 p. 179).'),
# ---------------------------------------------------------------- STD
dict(param='STD',score=3,stance='supports',key=KOS,where='p. 101',basis='documented',genre='mixed',archive='mixed',
 quote="By contrast, time according to the Seleucid Era, decoupled from the death-accession cycle, was transformed from being concrete, immanent, and process linked into being abstract, homogeneous, and transcendent. ... This little-heralded achievement was a highly politicized act. The Seleucid Era established the chronological backbone along which the kingdom’s",
 note='A royal dating system for the whole empire (with the Attic coin standard, Monerie 2017 p. 276).'),
dict(param='STD',score=2.5,stance='qualifies',key=MON,where='p. 87',basis='documented',genre='mixed',archive='hoards',
 quote="la plupart des monnayages d’argent qui circulaient en Basse-Mésopotamie dans la seconde moitié du Ier millénaire av. J.-C. étaient frappés selon un étalon différent de l’étalon babylonien.",
 note='Local weighing of silver against a foreign coin standard lasted into the early Hellenistic period.'),
# ---------------------------------------------------------------- TERR
dict(param='TERR',score=2.5,stance='qualifies',key=KOS,where='p. 22',basis='documented',genre='mixed',archive='mixed',
 quote="Dynastic strife and Timarchus’ revolt had fatally eroded Seleucid authority in the Upper Satrapies: under Mithridates I, the Parthian kingdom had expanded from the Caspian region to occupy Media in 148/7, Babylonia in 141, and Elymaïs in 140.",
 note='Chronology: Babylonia is a Seleucid province 311-141 BC; after 141 it is Parthian (outside this period).'),
dict(param='TERR',score=3,stance='supports',key=KOS,where='p. 20',basis='documented',genre='mixed',archive='mixed',
 quote="Antiochus III also reasserted Seleucid dominance in the Upper Satrapies. In 220 he defeated Molon, the rebellious satrap of Media, and imposed suzerainty on Artabazanes, the ruler of Media Atropatene.",
 note='Revolts of satraps and reconquest: wide reach, but contested at the edges.'),
# ---------------------------------------------------------------- LAW (undecided)
dict(param='LAW',score=2,stance='supports',key=MON,where='p. 283',basis='documented',genre='legal',archive='temple archives (Uruk, Babylon)',
 quote="S’y ajoutaient de nombreux documents inscrits en grec ou en araméen sur peau ou (plus rarement) sur papyrus, qui avaient valeur légale devant les autorités royales.",
 note='Royal authorities judge on documents in Greek; no royal law collection is known.'),
# ---------------------------------------------------------------- PRIV
dict(param='PRIV',score=2,stance='qualifies',key=MON,where='p. 283',basis='documented',genre='mixed',archive='temple archives (Uruk, Babylon)',
 quote="L’usage de ces documents, déjà fréquent au début du Ier millénaire av. J.-C., semble s’être répandu au cours des siècles, ce dont témoigne en négatif la réduction du spectre des activité documentées par les textes cunéiformes, qui apparaît beaucoup moins large à l’époque hellénistique qu’au vie s. av. J.-C.",
 note='Private business moved to parchment; the cuneiform record under-reports it.'),
# ---------------------------------------------------------------- SCHOOL (ShG: more than one source)
dict(param='SCHOOL',score=1,stance='supports',key=YOU,where='p. 346',basis='documented',genre='scholarly',archive='Ue XVIII houses (Uruk)',region='Uruk',
 quote="A big part of the tablets found in Ue XVIII was the product of scribal training for pupils who studied Akkadian and Sumerian scholarly series in order to specialise in the art of the healer at a later stage. Various phases of the school curriculum are evident in the assemblage, highlighting the domestic context of apprenticeship.",
 note='Training in the house of a healer family.'),
dict(param='SCHOOL',score=1.5,stance='qualifies',key=YOU,where='p. 345',basis='documented',genre='scholarly',archive='Ue XVIII houses (Uruk)',region='Uruk',
 quote="Several tablets from his collection were written as a part of the scribal training of his son Ištar-šum-ēreš, but also of a certain Anu‑ab-uṣur, descendant of the Kurî family, and maybe of Anu-ab-uṣur, descendant of the Gimil-Anu family. Both the Kurî and Gimil-Anu families belonged to the traditional Urukean urban elite.",
 note='Household teaching took in pupils from other temple families: a shared curriculum, not yet an institution.'),
dict(param='SCHOOL',score=1,stance='supports',key=CLA,where='pp. 46-47',basis='documented',genre='scholarly',archive='colophons (Uruk, Babylon)',
 quote="Les tablettes étaient régulièrement recopiées, pour l’apprentissage des scribes, pour la conservation des écrits ou encore pour la constitution de collections. ... la relation du copiste au propriétaire qui est très souvent familiale, le fils copiant pour le père.",
 note='Colophons show training within the family.'),
]
# Added after the OCR of L. T. Doty 1977, Cuneiform Archives from Hellenistic Uruk (diss. Yale): abstract (unnumbered front matter).
E.append(dict(param='BUR',score=3,stance='supports',key='dotyCuneiformArchivesHellenistic1977',where='Abstract',basis='substantial',genre='legal',archive='Uruk family archives (Seleucid)',
 quote="The cuneiform evidence indicates that a royal tax on the sale of slaves (andrapodon) and a general sales tax (eponion) were imposed early in the reign of Antiochus I Soter (ca. 274 B.C.). ... After the imposition of these taxes all sale documents involving slaves or arable land had to be written on papyrus or parchment, rather than cuneiform tablets, and registered with the Seleucid royal notary officer (chreophylax).",
 note='A royal registry for private sales: the state bureaucracy now writes in Greek on perishable media (chapter IV, pp. 308ff.).'))
