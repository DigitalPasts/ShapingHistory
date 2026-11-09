"""Fifth round (8 Nov 2026), after ShG's second assessment. Middle Babylonian (Kassite). ShG's notes: field literature
missing for PAL, TEMP, TCTL (adjudicated 2.5), FISC (adjudicated 3); BUR, STD, SCHOOL (2-3 expected), LAW undecided;
Paulus on kudurrus and Devecchi on administrative tablets for BUR; RlA "Maße und Gewichte" for STD; Fuchs for TERR.
Not in the library: the RlA article and Fuchs (ShG's Zotero key fuchsAssyriaNorth2017 is "Assyria and the North:
Anatolia", which is not about Kassite Babylonia; OHANE III ch. 33 cites Fuchs 2017: 127-141 in Bartelmus and Sternitzke,
Karduniaš, for the Kassites and the Zagros). Both go on the acquisition list.
Sources (local texts; printed pages from running heads):
- S. Paulus and T. Clayden (eds) 2020, Babylonia under the Sealand and Kassite Dynasties (SANER 24): Devecchi pp. 205-227
  (pdf n = p. n+6), Paulus pp. 228-252.
- L. Sassmannshausen 2001, Beiträge zur Verwaltung und Gesellschaft Babyloniens in der Kassitenzeit (BaF 21): OCR,
  pdf n = p. n-20.
- E. Bartelmus 2016, Fragmente einer großen Sprache (UAVA 12): pdf n = p. n-18.
- J. A. Brinkman 2004, JAOS 124: 283-304 (review of Sassmannshausen): pdf n = p. 281+n."""
P='Middle Babylonian'
DEV='devecchiManagingHarvestKassite2020'; PAU='paulusTurnTurnTurn2020'; SAS='sassmannshausenBeitraegeVerwaltungGesellschaft2001'
BAR='bartelmusFragmenteGrossenSprache2016'; BRI='brinkmanAdministrationSocietyKassite2004'
E=[
# ---------------------------------------------------------------- BUR (undecided)
dict(param='BUR',score=2.5,stance='supports',key=DEV,where='p. 209',basis='substantial',genre='admin',archive='Nippur granary archive; Dūr-Enlilē (CUSAS 30, 37)',
 quote="The sequence according to which these columns were arranged on the tablets seems to be quite strict and standardized, to the point that columns were sometimes inserted even though they were not actually needed and thus left empty.",
 note='Standard ledger formats in two separate administrative centres (Nippur and Dūr-Enlilē).'),
dict(param='BUR',score=2.5,stance='supports',key=DEV,where='p. 206',basis='documented',genre='admin',archive='Dūr-Enlilē (CUSAS 30, 37)',
 quote="an important contribution to the study of centralized administration in Kassite Babylonia is now provided by the Kassite tablets of the Rosen Collection ... they share a number of typological, prosopographical, geographical, and chronological features which make them the second largest coherent set of Middle Babylonian sources after those from Nippur ... “an important economic center that was to a certain degree dependent on Nippur and played an important role in the administration”",
 note='A second administrative centre tied to Nippur: the bureaucracy was not one city only.'),
dict(param='BUR',score=1.5,stance='qualifies',key=BRI,where='p. 287',basis='substantial',genre='admin',archive='Nippur',
 quote="The overwhelming majority of the texts (probably more than ninety percent of those known) come from one site (Nippur) over a restricted period of approximately five generations (c. 1360-1225) and tend to concentrate on the bookkeeping of large economic units there. How full a picture one can create even of these economic units from this documentation is not at all clear",
 note='Archive bias: one site, five generations.'),
# ---------------------------------------------------------------- FISC
dict(param='FISC',score=3,stance='supports',key=DEV,where='p. 209',basis='substantial',genre='admin',archive='Nippur granary archive; Dūr-Enlilē (CUSAS 30, 37)',
 quote="The first two columns are designated as rēš makkūri (sag níg.ga), and šibšu, which represent respectively the taxable capital and an amount paid on agricultural products that was calculated at a fixed rate upon the taxable capital.",
 note='A fixed-rate harvest tax, assessed town by town in annual ledgers.'),
dict(param='FISC',score=3,stance='supports',key=DEV,where='p. 205',basis='documented',genre='admin',archive='Nippur granary archive; Dūr-Enlilē (CUSAS 30, 37)',
 quote="the mechanisms developed by the central administration in order to control and exploit the production of agricultural goods during the Kassite period have been largely neglected in Ancient Near Eastern Studies. This research gap cannot be ascribed to the lack of sources.",
 note=''),
# ---------------------------------------------------------------- STD (undecided)
dict(param='STD',score=1.5,stance='qualifies',key=PAU,where='p. 229 n. 6',basis='documented',genre='admin',archive='Nippur granary archive',
 quote="There were different vessels used to measure capacities in the Kassite period. For an overview, see Sassmannshausen 2001: 448–49 and Brinkman 2017: 21.",
 note='Several capacity measures in use side by side.'),
dict(param='STD',score=1.5,stance='qualifies',key=SAS,where='p. 85',basis='documented',genre='admin',archive='Nippur',
 quote="Die ausgebende Stelle steht in Zusammenhang mit der Palastwirtschaft, denn die Vorderseite der Liste trägt die Überschrift \"Gerste, (nach) dem großen sutu-Maß, die von den 10 kurru (3000 qu) ,Entnahme' (massartu) des Palastes gegeben wurde\".",
 note='A palace measure; a temple measure is named elsewhere (p. 40: "dem großen sutu-Maß des Tempels"): institutional, not polity-wide, standards.'),
dict(param='STD',score=2,stance='supports',key=DEV,where='pp. 223-226 (tables 1-4)',basis='substantial',genre='admin',archive='Nippur granary archive; Dūr-Enlilē (CUSAS 30, 37)',
 quote="tēlītu gišbán gal mu.19.kam Nazi-Maruttaš lugal.e",
 note='Annual revenue accounts of many towns are headed with the same "large seah" and dated by regnal year in both centres.'),
# ---------------------------------------------------------------- SCHOOL (undecided; ShG expects 2-3)
dict(param='SCHOOL',score=2,stance='supports',key=SAS,where='p. 179',basis='fragmentary',genre='letters',archive='Nippur',
 quote="bit tuppi \"Tontafelhaus, Schule\" In einem Brief bekommt der Verwalter Innannu von einer hochgestellten Frau namens Inbi-ajjari folgende Anweisung: \"Die Söhne des Tafelhauses (= Schüler) sind dir anvertraut worden. Sorge dauernd für sie!\"",
 note='Pupils of a tablet house entrusted to the chief administrator of the Nippur granary.'),
dict(param='SCHOOL',score=2.5,stance='supports',key=BAR,where='p. 13',basis='documented',genre='scholarly',archive='Nippur',
 quote="Die von Sassmannshausen untersuchten Schülerübungen administrativen Inhalts stammen alle aus Nippur.",
 note='Exercises in administrative formats: training for the institutional bureaucracy.'),
dict(param='SCHOOL',score=2,stance='supports',key=BAR,where='p. 14',basis='fragmentary',genre='scholarly',archive='Nippur',
 quote="Die Tafel 12 N 587 ... wurde zusammen mit einer Gruppe von weiteren, bislang unveröffentlichten Übungstafeln während der 12. Nippur-Kampagne in den Aschegruben eines kassitischen Tempels (WA IV C 9) gefunden.",
 note='Exercise tablets in a temple context.'),
dict(param='SCHOOL',score=1.5,stance='qualifies',key=BAR,where='p. 2 n. 8',basis='fragmentary',genre='scholarly',archive='mixed',
 quote="dass die dürftige Quellenlage nur eine fragmentarische Bearbeitung beider Themen zulässt",
 note='Bartelmus warns the evidence on Kassite schooling is thin.'),
# ---------------------------------------------------------------- LAW (undecided)
dict(param='LAW',score=2,stance='supports',key=SAS,where='p. 7',basis='documented',genre='mixed',archive='mixed',
 quote="An der Spitze der Gesellschaft im kassitisch beherrschten Babylonien stand der König als Regent, oberster Richter und Heerfiihrer",
 note='The king as highest judge; no law collection is known for the period.'),
dict(param='LAW',score=1.5,stance='qualifies',key=SAS,where='p. 17',basis='documented',genre='legal',archive='Nippur',
 quote="Eine Gerichtsurkunde, in der es um die Frage geht, ob ein Bauer die šibšu-Abgabe zu leisten hat, und zwei weitere Prozeßurkunden zeigen, daß der \"Kanzler\" als Richter Gerichtsprozesse entscheiden konnte.",
 note='Justice by the governor of Nippur.'),
dict(param='LAW',score=1,stance='supports',key=SAS,where='p. 31',basis='documented',genre='legal',archive='Ur; Nippur',
 quote="In der dritten Urkunde ist allerdings schon ein Richter, der den Prozeß entscheidet, genannt. Aus einer Urkunde aus Nippur ist ersichtlich, daß der Bürgermeister auch an Stelle des Richters Gerichtsentscheidungen treffen",
 note='Local justice by mayors and judges.'),
# ---------------------------------------------------------------- COMM
dict(param='COMM',score=2.5,stance='supports',key=SAS,where='p. 10',basis='documented',genre='letters',archive='Nippur',
 quote="in welchem der König schreibt: \"Am selben Tag, an dem du meine Tontafel siehst, soll Šamaš-dajjān deinen Streitwagen bringen und er soll schnell herkommen!\" In einem anderen Brief ist ... von Kurierverkehr zum König die Rede",
 note='Royal letters and couriers between king and Nippur.'),
# ---------------------------------------------------------------- PAL / TEMP / TCTL
dict(param='PAL',score=2,stance='supports',key=SAS,where='p. 85',basis='documented',genre='admin',archive='Nippur',
 quote="Die ausgebende Stelle steht in Zusammenhang mit der Palastwirtschaft, denn die Vorderseite der Liste trägt die Überschrift \"Gerste, (nach) dem großen sutu-Maß, die von den 10 kurru (3000 qu) ,Entnahme' (massartu) des Palastes gegeben wurde\".",
 note='A palace economy alongside the provincial granary.'),
dict(param='PAL',score=1.5,stance='qualifies',key=BRI,where='p. 287',basis='documented',genre='admin',archive='Nippur',
 quote="one can enumerate a wide variety of officials and professions attested and detail the textual evidence about each, but still be able to say little about how the whole system functioned.",
 note='The share of palace against temple and province cannot be measured.'),
dict(param='TEMP',score=2,stance='supports',key=SAS,where='p. 40',basis='documented',genre='admin',archive='Nippur',
 quote="In einer Liste von ausgegebener \"Gerste, (mit) dem großen sutu-Maß des Tempels (gemessen), fiir die Bauern (errešu) und qattinnu von Zarat-Karkara\" findet sich ein Herold als Empfanger",
 note='Temple estates with their own farmers and measure.'),
dict(param='TCTL',score=2.5,stance='supports',key=SAS,where='p. 163',basis='documented',genre='letters',archive='Nippur',
 quote="An einen \"Kanzler\" ... dürfte wohl ein Brief gerichtet gewesen sein, der folgendermaßen beginnt: \"Land, Stadt und Tempel meines Herrn sind wohlbehalten! Die gesamte Einlieferung meines Herrn ist wohlbehalten.\"",
 note='The governor of Nippur is addressed as lord of land, city and temple.'),
# ---------------------------------------------------------------- PRIV
dict(param='PRIV',score=1,stance='qualifies',key=BRI,where='p. 287',basis='documented',genre='admin',archive='Nippur',
 quote="It is also possible that the greater part of contemporary Nippur falls completely outside the purview of these texts, including most aspects of any private economy.",
 note='Silent record for the private sector (already in the evidence as PRIV; kept once).'),
]
E=[e for e in E if not (e['param']=='PRIV')]  # the Brinkman PRIV passage is already coded (lit_evidence v1); avoid a duplicate
# Added 8 Nov (second pass, ShG on PRIV: "For the score to be clearer requires better citations").
E.append(dict(param='PRIV',score=1.5,stance='supports',key=SAS,where='pp. 103-104',basis='documented',genre='legal',archive='kudurrus; Nippur (MUN 10)',
 quote="Dies bedeutet jedoch nicht, daß alle landwirtschaftlichen Aktivitäten zentral gesteuert wurden. Hinweise auf privaten Grundbesitz liefern die Kudurru. Ihnen läßt sich entnehmen, daß zu den Landbesitzern Tempel, ein Prinz und eine Prinzessin, ein \"Kurator\" (bēl piḫāti), ein Kriegsheld ... ein Lederarbeiter ... ein Eunuch (ša rēši) des Königs ... gehörten",
 note='Private land exists, but most known holders are royal grantees and officials.'))
E.append(dict(param='PRIV',score=1.5,stance='qualifies',key=SAS,where='p. 104',basis='documented',genre='legal',archive='kudurrus; Nippur (MUN 10)',
 quote="Leider liegen keinerlei Informationen darüber vor, wie groß jeweils der Anteil der \"Krone\" und privater Eigentümer waren.",
 note='The share of private land cannot be measured.'))
