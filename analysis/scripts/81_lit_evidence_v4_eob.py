"""Fifth round (8 Nov 2026), after ShG's second assessment. Early Old Babylonian (c. 2000-1900 BC: Isin I, early Larsa,
Ešnunna). ShG's notes: HIER adjudicated 1 ("what you found is really unclear"); TEMP, LAW, COMM, STD (with qualifications),
SCHOOL, FISC need more field literature; BUR (Michel with Middeke-Conlin and Proust 2020; Middeke-Conlin 2020; Maggio 2019);
PAL (Fiette 2018); PRIV (Boer 2021; Boivin 2024 is first-millennium Larsa and was removed from this period).
Period checks: Fiette 2018 (Šamaš-hazir) is post-conquest Larsa under Hammurabi and is coded under Old Babylonian. The Michel,
Middeke-Conlin and Proust chapter is only a preview in the library (front matter and first page); it treats Larsa from the
twentieth to the eighteenth century and goes on the acquisition list with Middeke-Conlin 2020, Maggio 2019 and Boer 2021.
Sources: D. Charpin 2004, "Histoire politique du Proche-Orient amorrite (2002-1595)", in Charpin, Edzard and Stol,
Mesopotamien. Die altbabylonische Zeit (OBO 160/4): new French OCR of pdf 29-80 (the old text layer was unreadable);
pdf n = p. n+37."""
P='Early Old Babylonian'
CH='charpinMesopotamienAltbabylonische2004'
E=[
dict(param='BUR',score=2.5,stance='supports',key=CH,where='p. 79',basis='documented',genre='admin',archive='Isin craft archive; Nippur (Inanna temple)',
 quote="C'est à Nippur que la continuité est la plus complète, puisqu'il n'y a pas de rupture dans les archives du temple d'Inanna. Apparemment, rien n'a changé dans le pays de Sumer et d'Akkad, sinon que le siège du pouvoir s'est déplacé d'Ur à Isin, selon la volonté divine: c'est du moins l'idéologie que les souverains d'Isin s'efforcèrent de répandre",
 note='Isin keeps Ur III record-keeping; continuity is also an ideological claim.'),
dict(param='TCTL',score=2.5,stance='supports',key=CH,where='p. 80',basis='documented',genre='royal',archive='royal inscriptions and year names (Isin)',
 quote="Le souverain est «pourvoyeur de Nippur», le roi d'Isin étant responsable de l'approvisionnement des temples de cette ville.",
 note='Under Išme-Dagan; his daughter Enanatuma installed as entum at Ur.'),
dict(param='TEMP',score=2,stance='supports',key=CH,where='p. 77',basis='substantial',genre='admin',archive='Nippur (Ninurta temple); Ur (Ganunmah of Ningal)',
 quote="Les temples semblent avoir été moins sensibles aux aléas de la vie politico-militaire, puisqu'ils ont dans certains cas conservé leurs textes administratifs sur une durée plus longue. Ainsi, les archives du temple de Ninurta à Nippur (l'Ešumeša) s'étendent sur plus de 75 ans ... celles du magasin du temple de Ningal à Ur (le Ganunmah), couvrent 120 années",
 note='Temple economies outlast changes of ruler.'),
dict(param='HIER',score=1,stance='supports',key=CH,where='p. 81',basis='documented',genre='royal',archive='Ešnunna (Šu-Sin temple and Palace of the Rulers)',
 quote="Ešnunna ... était à l'époque de la troisième dynastie d'Ur le siège d'un gouverneur (ensi). Lorsque le royaume d'Ur se décomposa sous Ibbi-Sîn, Šu-iliya, fils du gouverneur Ituriya, se proclama roi à Ešnunna",
 note='Former Ur III governors become kings: the provincial hierarchy dissolves into city-states.'),
dict(param='TERR',score=1,stance='supports',key=CH,where='p. 85',basis='documented',genre='royal',archive='year names (Isin, Larsa)',
 quote="Ur-Ninurta se proclama «pasteur d'Ur», alors qu'il put seulement envoyer des offrandes au temple de Ningal en l'an 9 et 13 de Gungunum. Bur-Sin (1897-1876) porta le titre de «puissant fermier d'Ur»; il est vrai qu'il reprit le contrôle sur Ur, mais il le perdit rapidement",
 note='Titles claim more territory than the kings held.'),
dict(param='COMM',score=1.5,stance='supports',key=CH,where='p. 82',basis='documented',genre='letters',archive='Ešnunna (Palace of the Rulers)',
 quote="Outre un certain nombre de lettres qui lui furent adressées, on a retrouvé de nombreux textes administratifs dans le palais, encore inédits",
 note='Royal letters exist at Ešnunna (Bilalama) and Isin (Lipit-Eštar and his general Nanna-kiag, p. 84), but in small numbers.'),
dict(param='COMM',score=1,stance='qualifies',key=CH,where='p. 79',basis='documented',genre='letters',archive='Sumerian royal letters (later school copies)',
 quote="Il s'agit de lettres en sumérien dont les rois d'Isin sont les expéditeurs ou les destinataires; elles ne sont connues que par des copies plus tardives, effectuées dans des écoles à titre d'exercice",
 note='The Isin royal correspondence survives only as later school copies; its authenticity is debated.'),
dict(param='STD',score=1.5,stance='qualifies',key=CH,where='p. 72',basis='documented',genre='mixed',archive='mixed',
 quote="tous les royaumes n'ajoutaient pas de mois intercalaires au même moment, d'où des décalages entre les calendriers des différents royaumes. À la fin de chaque année, la chancellerie faisait parvenir aux différentes villes de province une tablette comportant le nom de la nouvelle année.",
 note='Year names are standard within each kingdom, but each kingdom keeps its own calendar.'),
dict(param='SCHOOL',score=1.5,stance='qualifies',key=CH,where='p. 79',basis='documented',genre='scholarly',archive='Isin royal hymns; later school copies',
 quote="au point que de véritables plagiats ont pu être constatés dans le cas de certains hymnes d'Išme-Dagan, décalquant ceux de Šulgi",
 note='The Isin court continues Ur III scholarly production; direct evidence for schools of this period is thin.'),
]
# Added 8 Nov (second pass, ShG on LAW "a tendency close to 3 even or 2.5" and FISC "check also field literature").
E.append(dict(param='LAW',score=2.5,stance='supports',key=CH,where='p. 84',basis='documented',genre='royal',archive='royal inscriptions (Isin)',
 quote="On doit mentionner en premier lieu la promulgation d'un «Code de lois», que rappellent presque toutes les inscriptions commémoratives de ce souverain, à commencer par celle consacrée à la construction de la «Maison de la Justice» (é ni-si-sá).",
 note='Lipit-Eštar of Isin. Charpin adds that these aspects "pourraient faire illusion": the kingdom was already losing ground to Larsa.'))
E.append(dict(param='LAW',score=2.5,stance='supports',key=CH,where='p. 74',basis='documented',genre='legal',archive='law collections (school copies)',
 quote="Le «Code» du roi d'Isin Lipit-Eštar, le plus ancien, fut rédigé en sumérien. ... Alors que le Code de Lipit-Eštar et les Lois d'Ešnunna ne sont connus que par des copies sur tablettes",
 note='The oldest of the three Old Babylonian law collections; known from tablet copies only.'))
E.append(dict(param='FISC',score=2,stance='supports',key=CH,where='p. 81',basis='documented',genre='royal',archive='royal inscriptions (Isin)',
 quote="Du moins observe-t-on qu'Išme-Dagan exempta Nippur de son tribut et ses habitants du service militaire",
 note='An exemption presupposes a royal levy of tribute and military service on the cities of the kingdom.'))
