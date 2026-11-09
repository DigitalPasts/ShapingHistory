"""Round 4 (9 Nov 2026): Middle Elamite. ShG reviewed this SI period on the desk (9 Nov) and asked for sources for TERR
(his score 2, band 1-2) and found COMM and TEMP impossible to score with one citation each.
Sources: Mofidi-Nasrabadi 2022 = OHANE III ch. 34 (printed pages; pdf n = p. n+25); Mofidi-Nasrabadi 2018 and Basello and
Giovinazzo 2018 = The Elamite World (printed pages); Glassner 1991 (RAI 36) printed pages from the running heads.
"""
P='Middle Elamite'
MN='mofidinasrabadiElamLateBronze2022'; MN18='mofidiNasrabadiElamMiddleElamite2018'; BG='baselloElamiteAdministration2018'
GL='glassnerTextesHaftTepe1991'
E=[
# TERR
dict(param='TERR',score=2,stance='qualifies',key=MN,where='OHANE III, ch. 34, §34.4.1, p. 895',basis='substantial',genre='royal inscriptions',archive='royal inscriptions',
 quote="Kidin-Hutran’s conquest at the end of ME II established a pattern of Elamite interest in and periodic control over Babylonia that continued to grow under the Šutrukid dynasty (ME III).",
 note='Control beyond Susiana and Fars was periodic.'),
dict(param='TERR',score=2,stance='qualifies',key=MN,where='OHANE III, ch. 34, §34.6, p. 934',basis='substantial',genre='royal inscriptions',archive='royal inscriptions',
 quote="The last Igihalkid and, especially, the Šutrukid rulers were powerful enough to pursue an expansionary military policy that led to Elamite supremacy in Babylonia for some decades.",
 note='Babylonia held for decades, not generations.'),
dict(param='TERR',score=2,stance='supports',key=MN18,where='p. 231',basis='substantial',genre='royal inscriptions',archive='royal inscriptions',
 quote="The cities of Susa in Khuzestan and Anshan (Tall-e Malyan) in the province of Fars seem to be the capitals of the two main Elamite territories, Elam and Shimashki, respectively.",
 note='A two-core realm (lowland Susiana, highland Fars) under one king.'),
# COMM
dict(param='COMM',score=2,stance='supports',key=MN,where='OHANE III, ch. 34, §34.3, p. 890',basis='documented',genre='royal inscriptions',archive='inscribed bricks (Susa, Chogha Zanbil, Liyan)',
 quote="It is therefore likely that the building activities of the Igihalkid rulers throughout their realm were organized at the capital Susa",
 note='Bricks for the temple at Liyan (near Bushehr, c. 400 km away) and for Chogha Zanbil were drafted at Susa: works across the realm were directed from the capital.'),
dict(param='COMM',score=2,stance='supports',key=GL,where='p. 111',basis='fragmentary',genre='admin',archive='Haft Tepe (Kabnak)',
 quote="témoignent des rapports que le souverain entretenait, à part Suse, Kabnak et Anšan, avec Karduniaš, c’est-à-dire la Babylonie",
 note='Haft Tepe texts on Tepti-ahar link Susa, Kabnak and Anšan; footnote numbers removed from the quote.'),
dict(param='COMM',score=1,stance='qualifies',key=BG,where='p. 488',basis='documented',genre='admin',archive='Tall-e Malyan EDD',
 quote="Single and multiple issue memoranda seem to be related to an outward movement of goods and supplies within a local administration",
 note='The Malyan archive (c. 1000 BCE) is local; only its "dispatches" record movements outside the organization. No written evidence for regular communication between Susa and Anšan.'),
# TEMP
dict(param='TEMP',score=2,stance='supports',key=MN,where='OHANE III, ch. 34, §34.4.4, p. 905',basis='fragmentary',genre='admin',archive='Haft Tepe (Kabnak)',
 quote="Several of the cuneiform texts recovered from a nearby room record the receipt of gold, silver, and bronze, and the delivery of manufactured products. Such activities could well be connected to the workings of a temple workshop.",
 note='Workshop integrated in the terrace complex of the presumed sanctuary at Haft Tepe.'),
dict(param='TEMP',score=2,stance='supports',key=MN,where='OHANE III, ch. 34, §34.5.3, p. 931',basis='documented',genre='archaeology',archive='Chogha Zanbil',
 quote="Later at Chogha Zanbil, during the ME II phase, pottery production in temple workshops is well attested.",
 note='Temples produce, but within the royal foundation.'),
dict(param='TEMP',score=2,stance='qualifies',key=MN,where='OHANE III, ch. 34, §34.4.3, p. 901',basis='substantial',genre='admin',archive='Haft Tepe stele; Haft Tepe and Chogha Zanbil workshops',
 quote="These sanctuaries were likely part of the same centralized system of resource management.",
 note='Temples as part of the crown system, not independent households: the same passage says "ultimately, the king would have been in charge" (also TCTL).'),
dict(param='TCTL',score=3,stance='supports',key=MN,where='OHANE III, ch. 34, §34.4.3, p. 901',basis='substantial',genre='admin',archive='Haft Tepe stele',
 quote="pointing to the existence of a well-organized administrative system for the running of the temples and the cults, and the evidence strongly suggests that, ultimately, the king would have been in charge.",
 note=''),
dict(param='TEMP',score=2,stance='supports',key=MN,where='OHANE III, ch. 34, §34.4.4, p. 918',basis='substantial',genre='royal inscriptions',archive='royal inscriptions; temples',
 quote="the official, royal-sponsored state cult practiced at a large number of temples across the realm with complex sacred rituals conducted by priests in the presence of only a small elite",
 note='Many temples, royally sponsored; no temple archive or temple estate is documented.'),
]
