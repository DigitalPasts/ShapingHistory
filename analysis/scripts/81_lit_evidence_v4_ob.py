"""Fifth round (8 Nov 2026), after ShG's second assessment. Old Babylonian. ShG's notes: PAL ("rescoring needed after more
citations"), TEMP, SCHOOL, TERR (adjudicated 2; Kiš and Babylon labels collide on the map), BUR, LAW, PRIV (Spada 2026, not
local), COMM, STD need more field literature.
Note on period mixing: Fiette 2018 (Šamaš-hazir) documents Larsa after Hammurabi's conquest, so it belongs here, not in Early
Old Babylonian, where ShG suggested it for PAL; the EOB cell keeps its own evidence.
Sources (local texts; printed pages from running heads):
- M. Van De Mieroop 2005, King Hammurabi of Babylon (Blackwell): pdf n = p. n+13.
- B. Fiette 2018, "Le domaine royal de Hammurabi de Babylone", Histoire & Sociétés Rurales 49: 7-53: pdf n = p. n+7.
- D. Charpin 2017, La vie méconnue des temples mésopotamiens (Les Belles Lettres): pdf n = p. n+1.
- D. Charpin 2010, Reading and Writing in Babylon (Harvard): scanned spreads, pdf n = pp. 2n-18/2n-17.
- D. Charpin 2014, "The Historian and the Old Babylonian Archives", in H. Baker and M. Jursa (eds), Documentary Sources in
  Ancient Near Eastern and Greco-Roman Economic History (Oxbow), pp. 24-58: pdf n = p. n+18.
- W. F. Leemans and M. Stol 2023, Old Babylonian Texts from Dilbat, Sippar and Other Places: pdf n = p. n-9."""
P='Old Babylonian'
VDM='vandemieroopKingHammurabiBabylon2005'; FIE='fietteDomaineRoyalHammurabi2018'; CH17='charpinVieMeconnueTemples2017'
CH10='charpinReadingWriting2010'; CH14='charpinHistorianOldBabylonian2014'; LS='leemansOldBabylonianTexts2023'
E=[
# ---------------------------------------------------------------- PAL
dict(param='PAL',score=3,stance='supports',key=FIE,where='p. 19',basis='substantial',genre='letters',archive='Šamaš-hazir (Larsa)',
 quote="Les champs du domaine royal sont divisés en deux catégories. D’une part, les champs appartenant à la « réserve » du Palais sont confiés aux gouverneurs-šâpirum et sont cultivés et entretenus par leurs intendants agricoles iššakkum. ... D’autre part, Hammurabi attache ses sujets aux terres de son nouveau domaine, grâce à un système de rémunération de leurs services par le régime des tenures.",
 note='A palace reserve producing biltum and a tenure system for ilkum service.'),
dict(param='PAL',score=2.5,stance='qualifies',key=FIE,where='p. 13',basis='documented',genre='letters',archive='Šamaš-hazir (Larsa)',
 quote="Il s’agissait de l’ancien domaine de Rim-Sin, que Hammurabi s’était approprié par droit de conquête. Le domaine royal de Larsa était constitué de terroirs situés dans les campagnes de plusieurs grandes villes comme Larsa, Ur, Bad-tibira, Umma ou encore Lagaš. Il est actuellement impossible d’en évaluer la superficie, même de façon approximative.",
 note='The palace domain is large but its share of the land cannot be measured.'),
# ---------------------------------------------------------------- TEMP / TCTL
dict(param='TEMP',score=2,stance='supports',key=VDM,where='p. 96',basis='documented',genre='legal',archive='Laws of Hammurabi §32',
 quote="If the soldier had enough assets, he was to pay up himself. If not, first the city-temple’s resources were used, and only if those were also insufficient would the palace step in (§ 32).",
 note='City temples hold resources of their own, called on before the palace.'),
dict(param='TEMP',score=1.5,stance='qualifies',key=LS,where='p. 14',basis='documented',genre='admin',archive='Bad-tibira (Dumuzi temple)',
 quote="It was already known from the other tablets that (the) Dumuzi (temple) was concerned with landed property and ... records the renting of such land by the intermediary of Ṣilli-Šamaš at the rent of 33 gur of barley, to be delivered to the palace",
 note='Temple land whose rent goes to the palace (Rim-Sin, Larsa).'),
dict(param='TCTL',score=2.5,stance='supports',key=LS,where='p. 14',basis='documented',genre='admin',archive='Bad-tibira (Dumuzi temple)',
 quote="the rent of 33 gur of barley, to be delivered to the palace on Simānu 1st (Rīm-Sîn IIb)",
 note='The palace takes the revenue of temple land.'),
# ---------------------------------------------------------------- BUR
dict(param='BUR',score=2.5,stance='supports',key=VDM,where='p. 88',basis='substantial',genre='letters',archive='Šamaš-hazir (Larsa)',
 quote="Hammurabi’s canal projects opened up new tracts of land for cultivation, but often Shamash-hazir had to identify and allocate land in regions where many plots were already occupied. Numerous letters to him deal with this issue.",
 note='A land registry run by letter from Babylon.'),
dict(param='BUR',score=2.5,stance='supports',key=CH17,where='p. 129',basis='documented',genre='letters',archive='Šamaš-hazir (AbB 4 118)',
 quote="Il y est question d’« anciennes tablettes », ce qui fait sans doute allusion à la situation politique : le royaume de Larsa avait été récemment annexé par Hammu-rabi de Babylone, et plus d’une fois on se réfère de cette manière à la situation qui prévalait du temps du roi vaincu, Rim-Sin.",
 note='Rim-Sin\'s ilkum registers, kept in the temple of Nisaba, are consulted by the Babylonian administration.'),
# ---------------------------------------------------------------- COMM
dict(param='COMM',score=2.5,stance='supports',key=VDM,where='p. 85',basis='documented',genre='letters',archive='Sin-iddinam; Šamaš-hazir (Larsa)',
 quote="Hammurabi himself advised Sin-iddinam of his arrival. A letter found in Larsa states: To Sin-iddinam say, thus speaks Hammurabi: Herewith I send you Igmil-Sin, son of Puzur-Shamash, and Nabijatum, the mounted",
 note='Royal letters and messengers between Babylon and Larsa.'),
dict(param='COMM',score=2.5,stance='supports',key=CH14,where='p. 25',basis='substantial',genre='letters',archive='mixed',
 quote="The number of letters and legal documents in the Old Babylonian archives is, by contrast, much greater, and the geographical distribution of the archives is much broader.",
 note='About 2,762 letters in AbB alone (p. 29).'),
# ---------------------------------------------------------------- TERR (ShG adjudicated 2)
dict(param='TERR',score=2,stance='qualifies',key=VDM,where='p. 52',basis='documented',genre='mixed',archive='Ešnunna region',
 quote="Nor do records dated with Hammurabi’s year-names replace those of a local Eshnunna ruler. ... He seems thus to have had an official residence in Eshnunna territory close to the border with Babylonia, but is unlikely to have fully incorporated Eshnunna into his kingdom.",
 note='Conquest without full incorporation (p. 53: "He did not annex its territory").'),
dict(param='TERR',score=2.5,stance='supports',key=FIE,where='p. 13',basis='documented',genre='letters',archive='Šamaš-hazir (Larsa)',
 quote="elles révèlent l’implantation et la mainmise des Babyloniens sur un territoire conquis, ce qu’aucun autre corpus ne permet d’observer par ailleurs",
 note='Larsa is fully incorporated; the north is not.'),
# ---------------------------------------------------------------- STD
dict(param='STD',score=2,stance='qualifies',key=VDM,where='p. 52',basis='documented',genre='legal',archive='Ešnunna region',
 quote="Nor do records dated with Hammurabi’s year-names replace those of a local Eshnunna ruler.",
 note='The Babylonian dating system follows full incorporation only.'),
dict(param='STD',score=2.5,stance='supports',key=LS,where='p. 7',basis='documented',genre='admin',archive='Larsa taxation documents (Hammurabi)',
 quote="They record the valuation of amounts of barley from different plots of land, specifying the surface measure (col. 1: eqlum), the estimated yield (col. 2: níg-gar = šukunnûm, i.e., 5, 10, 15 or 20 gur per bur) and the output of barley (col. 3: še-bi).",
 note='Assessment of yields on a fixed scale per bur.'),
# ---------------------------------------------------------------- SCHOOL
dict(param='SCHOOL',score=1.5,stance='supports',key=CH10,where='pp. 30-31',basis='substantial',genre='scholarly',archive='Nippur (House F and neighbours)',
 quote="But given that one of these houses yielded more than 1,400 school tablets, that explanation hardly seems credible. Much more likely, these were the houses of masters (um.mi.a) who taught from their homes (Robson 2001).",
 note='Schooling in private houses of masters.'),
dict(param='SCHOOL',score=2,stance='qualifies',key=CH10,where='pp. 40-41',basis='documented',genre='scholarly',archive='Nippur; Ur',
 quote="To write an inheritance contract, they not only had to have learned by heart the corresponding model, they also had to be able to divide up the land area to be distributed among the heirs. Arithmetic, knowledge of the systems of weights and measures, and surveying were thus part of the curriculum.",
 note='A shared curriculum across cities, without a state school.'),
dict(param='SCHOOL',score=1.5,stance='supports',key=CH10,where='pp. 60-61',basis='documented',genre='scholarly',archive='Sippar-Amnanum (Ur-Utu)',
 quote="But an analysis of the curriculum revealed by these tablets indicates that the level of proficiency he reached was not very high. It was enough that he know the basics: how to read and write.",
 note='Household training for a temple official\'s son.'),
# ---------------------------------------------------------------- PRIV
dict(param='PRIV',score=3,stance='supports',key=LS,where='p. 12',basis='documented',genre='legal',archive='Larsa (orchard lease)',
 quote="Accordingly we can conclude that Pirḫum assumes the responsibility for the revenues of the orchard of Šamaš-māgir.",
 note='Private orchard leases with entrepreneurs (cf. Renger in Interdependency of Institutions and Private Entrepreneurs).'),
]
# Added 8 Nov (second pass, ShG on LAW: "Need more citations from the field literature").
E.append(dict(param='LAW',score=3,stance='supports',key=VDM,where='p. 108',basis='substantial',genre='letters',archive='Hammurabi letters (Larsa)',
 quote="Someone who felt that his property had been stolen, for example, could address the king, who had the matter investigated by his officials or considered by groups of judges. The investigation was based on registers and documents, or, if these were missing, on testimonies by witnesses or a divine judge in the form of the river ordeal. Rightful ownership was established and, if needed, the decision was enforced with the help of a soldier.",
 note='Royal justice by petition, officials, judges and enforcement.'))
E.append(dict(param='LAW',score=2.5,stance='qualifies',key=VDM,where='p. 108',basis='documented',genre='letters',archive='Hammurabi letters (Larsa)',
 quote="Whatever the verdict, it was not necessary for the judges to explain it by referring to a body of law. That was not the function of Hammurabi’s code.",
 note='The code is not applied as statute.'))
