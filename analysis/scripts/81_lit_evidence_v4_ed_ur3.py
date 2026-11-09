"""Fifth round (8 Nov 2026), after ShG's second assessment. ED IIIa (TERR, HIER: NABU 1991 and "field literature added to
the folder") and Ur III (LAW, TEMP, TERR adjudicated 2).
ED IIIa: NABU 1991 holds Visicato's note on territorial reorganisation in the Fara archive. The other new file
("Wirtschaftstexte aus Fara II") is a philological review in ZA 107 (2017) of Steible and Yıldız, without a statement on
hierarchy; the book itself goes on the acquisition list.
Sources (local texts; printed pages from running heads):
- G. Visicato 1991, "Un nuovo esempio di ristrutturazione di territori all'epoca di Fara", NABU 1991/15.
- W. Sallaberger 1999, "Ur III-Zeit", in Sallaberger and Westenholz, Mesopotamien. Akkade-Zeit und Ur III-Zeit (OBO 160/3):
  pdf n = p. n+6.
- S. Garfinkle 2020, "Violence and State Power in Early Mesopotamia", in G. G. Fagan et al. (eds), The Cambridge World History
  of Violence I, ch. 10: the offprint has no page numbers; cited by PDF page of the chapter."""
P='Ur III'
VIS='visicatoNuovoEsempioRistrutturazione1991'; SAL='sallabergerUrIIIZeit1999'; GAR='garfinkleViolenceStatePower2020'
E=[
# ---------------------------------------------------------------- ED IIIa
dict(period='ED IIIa',param='TERR',score=1.5,stance='supports',key=VIS,where='NABU 1991/15',basis='fragmentary',genre='admin',archive='Šuruppak (TSS 242, TSS 758)',region='south',
 quote="Questo potrebbe essere un altro indizio a conferma dell’ipotesi di una possibile struttura socio-politica che unisse, all’epoca degli archivi di Fara, almeno una parte della Mesopotamia.",
 note='Fields of three cities regrouped into a new administrative unit, recorded at Šuruppak: a hypothesis of a supra-city structure.'),
dict(period='ED IIIa',param='HIER',score=1.5,stance='qualifies',key=VIS,where='NABU 1991/15',basis='fragmentary',genre='admin',archive='Šuruppak (TSS 242)',region='south',
 quote="una « ristrutturazione di parte dei territori agricoli delle città di Adab, Umma e Lagash, in seguito alla creazione di una nuova unità amministrativa con centro ad ‘Unken’, sotto la giurisdizione di Lagash »",
 note='One city given jurisdiction over a unit formed from the land of others (Pettinato\'s reading, endorsed by Visicato).'),
# ---------------------------------------------------------------- Ur III LAW
dict(param='LAW',score=2.5,stance='supports',key=SAL,where='p. 137',basis='documented',genre='legal',archive='Codex Ur-Namma',
 quote="Ur-Namma schafft schließlich eine gültige Rechtsordnung, die in seinem \"Codex Ur-Namma\" niedergelegt ist, die älteste bekannte altorientalische Gesetzessammlung.",
 note='A royal law collection at the start of the dynasty.'),
# ---------------------------------------------------------------- Ur III TEMP
dict(param='TEMP',score=2,stance='qualifies',key=SAL,where='p. 146',basis='documented',genre='royal',archive='year names (Šulgi 21)',
 quote="Und wie ist Datum S 21 zu verstehen, das von einer Reformierung des Tempellandes von Enlil und Ninlil zu sprechen scheint: werden damit alle Tempel dem König unterstellt, wie man dies allgemein annimmt? ... Eine Frage, die wir wohl aufgrund der dürftigen Urkundenlage nicht beantworten können; ein markanter Unterschied scheint sich jedoch für den Süden des Landes nicht anzudeuten.",
 note='The supposed royal takeover of temple land under Šulgi is not visible in the southern archives.'),
dict(param='TEMP',score=2,stance='supports',key=SAL,where='p. 186',basis='documented',genre='admin',archive='mixed (Girsu, Umma, Nippur, Puzriš-Dagan)',
 quote="Viele wichtige Ämter des Reiches sind regional gebunden: ensi2 und zum Teil šagina an die Provinz, sanga und šabra an den Tempel, hazannum an die Ortschaft, jeweils sind ihnen untergebene Verwaltungsstrukturen zugeordnet. Daneben existiert eine königlich-staatliche Administration",
 note='Temple households keep their own administration inside the provincial system.'),
# ---------------------------------------------------------------- Ur III TERR (ShG adjudicated 2)
dict(param='TERR',score=2,stance='supports',key=GAR,where='ch. 10, PDF p. 14',basis='documented',genre='royal',archive='royal inscriptions; Puzriš-Dagan',
 quote="The military activities of the Ur III kings to the east and north-east of their frontier were undertaken to ensure the continued flow of this tribute, both from dependent states and from military personnel and high-ranking officials of the kingdom. Significantly, these were raids aimed at securing resources and weakening outside groups; they were not aimed at the outright control of foreign territory.",
 note='A core of provinces with a tributary periphery, not annexation.'),
dict(param='TERR',score=2,stance='supports',key=SAL,where='p. 157 (fig. 4)',basis='documented',genre='admin',archive='mixed',
 quote="Kernland und Peripherie des Ur III-Reiches (nach P. Steinkeller, SAOC 46)",
 note='The map of core, periphery and vassal states follows Steinkeller 1987.'),
]
