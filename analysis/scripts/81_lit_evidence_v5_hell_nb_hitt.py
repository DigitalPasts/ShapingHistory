"""Round 3b (8-9 Nov 2026), continued: Hellenistic (van der Spek 2014), Neo-Babylonian law and schooling
(Holtz 2014; Veldhuis 2003), Hittite tribute and schooling (Genz 2011; Weeden 2011).
Page offsets: van der Spek 2014, JESHO 57: 203-230: pdf n = p. n+202. Holtz 2014 (WAW 35): pdf n = p. n-17.
Veldhuis 2003, JAOS 123: 627-633: pdf n = p. n+625. Genz 2011 (Colloquia Antiqua 2): pdf n = p. n+297.
Weeden 2011 (StBoT 54): read from the running heads (p. 81 = pdf 49, p. 82 = pdf 50).
"""
P='Hellenistic'
VDS='vanderspekFactorMarketsHellenistic2014'; HOL='holtzNeoBabylonianTrialRecords2014'; VEL='veldhuisCurriculumNeoBabylonianSchool2003'
GEN='genzForeignContactsHittites2011'; WEE='weedenHittiteLogogramsHittite2011'
NB='Neo-Babylonian'; HIT='Hittite'
E=[
dict(param='STD',score=2.5,stance='supports',key=VDS,where='p. 205',basis='documented',genre='legal',archive='Babylon; Uruk',
 quote="A sudden breakthrough, however, took place in the time of Alexander. As far as we can judge, all payments were made in coin from the start of his reign, even though cuneiform texts continue to speak of prices in silver, because, in contracts, this is mostly followed by the proviso “in staters (or tetradrachms, silver coins worth four drachmas) of Alexander” or any other ruler.",
 note='Royal coinage as the means of payment.'),
dict(param='STD',score=2,stance='qualifies',key=VDS,where='p. 205',basis='documented',genre='legal',archive='Babylon; Uruk',
 quote="Money continued to be weighed, but a rule of thumb probably emerged that one shekel was the equivalent of two drachmas. ... Cuneiform texts speak of a manûtu ša Bābili, “the account rate of Babylon.”",
 note='A local account standard survives beside the Attic coin standard.'),
dict(param='BUR',score=2.5,stance='supports',key=VDS,where='p. 212',basis='documented',genre='legal',archive='Uruk; Babylon',
 quote="Sales of arable land and slaves (see also below) do not appear in cuneiform after 274 BCE (Antiochus I), probably because they became subject to registration in a Greek-language record-keeping system.",
 note='A crown registration procedure displaces cuneiform conveyance records.'),
dict(param='LAW',score=1.5,stance='supports',key=VDS,where='p. 212',basis='documented',genre='legal',archive='Uruk',
 quote="The second contract stipulates that the land is leased “in accordance with the writing of the diagramma, [according to the de]cree, which the king issued.” The content of the diagramma (Greek word for royal edict) unknown",
 note='Royal edict cited as the norm in a cuneiform lease.'),
dict(param='PAL',score=2,stance='supports',key=VDS,where='pp. 213-214',basis='documented',genre='legal',archive='Esagila (Lehmann Text)',
 quote="Royal land is given to private Babylonians (eventually), and these parcels are negotiable, yet king and temple continue to play a role in the use of this land.",
 note='Crown land and royal grants recorded through the temple.'),
dict(param='FISC',score=2.5,stance='supports',key=VDS,where='p. 213',basis='documented',genre='legal',archive='Esagila (Lehmann Text)',
 quote="the Babylonians will be exempted from “the silver of the heads (tax), the silver of the king(’s tax), and the sta[te service (ilku) of the fields(?)] and the state service great and small, everything that is due to the (temple and) royal treasury as regards the fields and the people(?)”",
 note='Regular royal levies, named by type.'),
dict(param='TCTL',score=2,stance='supports',key=VDS,where='p. 213',basis='documented',genre='legal',archive='Esagila (Lehmann Text)',
 quote="The land is apparently encumbered with the obligation to pay a tithe to the king, but Antiochus orders that this be given to the temple for its upkeep.",
 note='Royal patronage and royal levies passing through the temple; the šatammu remains the temple head.'),
dict(param='PRIV',score=2,stance='supports',key=VDS,where='p. 211',basis='documented',genre='legal',archive='Uruk',
 quote="This text, too, has all characteristics of the sale of a piece of private property, though, on the west and east sides, the land was the “property of Anu” and on the south side the “property of the Lady of Uruk”",
 note=''),
dict(param='PRIV',score=1.5,stance='qualifies',key=VDS,where='p. 214',basis='documented',genre='legal',archive='Esagila (Lehmann Text)',
 quote="This may be a step in the direction of privatization of royal and temple land, but it is hardly evidence for a free market for land.",
 note=''),
# ------------------------------------------------ Neo-Babylonian law (Holtz) and schooling (Veldhuis)
dict(period=NB,param='LAW',score=3,stance='supports',key=HOL,where='p. 8',basis='substantial',genre='legal',archive='Eanna; Egibi; Babylon',
 quote="Several summonses, including some in this anthology, show the progress of cases from local adjudication by authorities in the Eanna to adjudication by royal judges (Document 16) and even to “the king’s court of law” (bīt dīni ša šarri) in Babylon (Document 39). ... The royal judges were organized in a recognizable hierarchy based on seniority and were overseen by royal officials called the sartennu and the sukallu.",
 note=''),
dict(period=NB,param='LAW',score=2.5,stance='qualifies',key=HOL,where='p. 7',basis='substantial',genre='legal',archive='Eanna; Ebabbar; Egibi',
 quote="The courtroom dramas usually take place in one of two main settings: in the presence of temple tribunals or before panels of royal judges. ... In broadest terms, temple tribunals prosecute matters internal to the temple, while royal judges adjudicate disputes at large.",
 note='Temple tribunals keep their own jurisdiction.'),
dict(period=NB,param='BUR',score=2.5,stance='supports',key=HOL,where='p. 6',basis='substantial',genre='legal',archive='Babylon (royal judges); Egibi',
 quote="Despite the obvious differences in content, different records follow consistent patterns of fixed terminology and order of elements. The highest degree of stylization occurs in the set of records from the courts of the royal judges in Babylon",
 note=''),
dict(period=NB,param='SCHOOL',score=1.5,stance='supports',key=VEL,where='p. 629',basis='documented',genre='lexical',archive='school tablets (Babylon, Sippar, Ur, Kiš)',
 quote="Two unpublished Neo-Babylonian school texts confirm that this is the standard Neo-Babylonian version",
 note='A standard Neo-Babylonian version of the lexical lists, shared across school sources; the review does not settle where teaching took place.'),
# ------------------------------------------------ Hittite
dict(period=HIT,param='FISC',score=2,stance='supports',key=GEN,where='p. 311',basis='documented',genre='mixed',archive='Ḫattuša; Ugarit',region='Empire',
 quote="Hittite power rested largely on vassal treaties which the Hittite kings concluded with the Syrian rulers. The Syrian kings were obliged to pay an annual tribute, and also to supply troops for Hittite campaigns.",
 note='Annual vassal tribute fixed by treaty.'),
dict(period=HIT,param='SCHOOL',score=1.5,stance='qualifies',key=WEE,where='p. 81',basis='documented',genre='lexical',archive='Ḫattuša tablet collections',
 quote="Work on Hittite scribal education is only just beginning. While fragments of most of the lexical lists known to the scribal curriculum of Babylonia have been found in Bogazköy, very little is known of methods of instruction, or whether these lists even played a role.",
 note=''),
dict(period=HIT,param='SCHOOL',score=1.5,stance='supports',key=WEE,where='p. 82',basis='fragmentary',genre='letters',archive='Maşat Höyük (ABoT 65)',
 quote="It is just possible that this E.DUB.BA.A was situated in Ortaköy/Sapinuwa, a periodical residence of the Hittite king and possibly the location of Hattusili, scribe and BĒL MADGALTI. In this case it would most likely have been Hattusili's house.",
 note='The one attested "tablet house" may be an official\'s household.'),
]
