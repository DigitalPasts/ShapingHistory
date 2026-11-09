"""Fifth round (8 Nov 2026), after ShG's second assessment. Old Akkadian. ShG's notes: PAL (Molina 2019, The Palace of Adab,
not local), COMM adjudicated 1 ("more from the field literature"), STD ("the difference between 2 and 3 needs to be better
defined for all of the periods": see the sharper definition in the codebook; Old Akkadian has a royal measure but no unified
calendar, which places it at 2 under the new rule), TEMP, PRIV, LAW (Wilcke, not local: Wilcke 2003 and 2007 go on the
acquisition list).
Sources: B. R. Foster 2016, The Age of Agade (Routledge): an e-book text without printed page numbers, cited by chapter and
section; I. Schrakamp 2014, CDLN 2014:23 (Sargonic texts from Adab)."""
P='Old Akkadian'
FOS='fosterAgeAgadeInventing2016'; SCH='schrakampSargonicTextsAdab2014'
E=[
dict(param='STD',score=1.5,stance='qualifies',key=FOS,where='ch. 6 §7',basis='documented',genre='mixed',archive='mixed (Adab, Nippur, Umma, Girsu)',
 quote="The Akkadian Empire did not have a unified calendar, as was attempted by a successor state, the Kingdom of Ur. Each city and region had its own calendar and feast days",
 note='Royal measures (ch. 1 §6; Bartash 2019) but no common calendar: one domain only, so STD 2 under the sharper definition.'),
dict(param='STD',score=1.5,stance='qualifies',key=SCH,where='CDLN 2014:23',basis='documented',genre='admin',archive='Adab (Sargonic)',
 quote="References to governors (ensi2) of Adab, the Adab calendar, prosopography, onomastic elements, divine names, and cultic places characteristic of Adab",
 note='The largest Sargonic corpus keeps its local calendar.'),
dict(param='TEMP',score=1.5,stance='supports',key=FOS,where='ch. 2 §4',basis='documented',genre='admin',archive='Girsu; Umma; Adab; Nippur',
 quote="The sanga had previously overseen the temple lands, gardens, herds, flocks, and other resources, but now, in Sumer at least, he was subordinate to both the local governor and the representatives of the king’s household.",
 note='Temples remain large but lose economic autonomy.'),
dict(param='TEMP',score=1.5,stance='supports',key=FOS,where='ch. 2 §4',basis='documented',genre='royal',archive='mixed',
 quote="In Akkad, it seems, temples generally had far less land and staff, so they were more directly dependent on the king’s household than in Sumer.",
 note=''),
dict(param='TCTL',score=3,stance='supports',key=FOS,where='ch. 2 §4',basis='documented',genre='royal',archive='mixed',
 quote="ancient temples were now dependent on the Akkadian king for support, renovation, dedications, and gifts",
 note=''),
dict(param='PRIV',score=2,stance='supports',key=FOS,where='ch. 8 §2',basis='documented',genre='letters',archive='Sippar (Quradum); Umma (Ama-e)',
 quote="In the Akkadian period, most of the surviving trade and business documents are records of transactions intended to be profitable to one of the parties. Many individuals, sometimes on their own, sometimes as agents for others, participated in for-profit enterprises.",
 note='Private business records beside the institutional ones.'),
dict(param='LAW',score=1.5,stance='qualifies',key=FOS,where='ch. 2 §3',basis='documented',genre='legal',archive='mixed',
 quote="Although no formal collection of legal decisions, promulgations, or pronouncements about law has come down to us from the Akkadian period, we can reconstruct aspects of its law from a rich inventory of documents recording instances of its practice, from both Sumer and Akkad, as well as the earliest known records of litigation.",
 note='Some practices imposed by rulers; after Naram-Sin\'s deification oaths are sworn by the king\'s name.'),
dict(param='COMM',score=1.5,stance='supports',key=FOS,where='ch. 2 §4',basis='documented',genre='admin',archive='mixed',
 quote="Courtiers included those who gave personal services to the royal family. They ... readied and maintained their transport animals and wagons, entertained them, served as their messengers and couriers",
 note='Couriers belong to the court; no relay system is documented (ch. 7 §4 already coded).'),
]
