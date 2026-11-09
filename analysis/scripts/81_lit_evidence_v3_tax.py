"""Fourth round (4 Nov 2026), part 2: taxation chapters already in the Literature folder but not yet cited, for the later
periods whose FISC cells rested on one or two works. Richardson 2020 and De Graef 2020 are chapters 8 and 7 of the Prague
volume (Mynářová & Alivernini eds.; printed page = PDF page + 199 and + 135 in the copies used). Jursa & Moreno García 2015
is ch. 4 of Monson & Scheidel eds., Fiscal Regimes (printed page = PDF page + 114). Jursa 2009 (Persika 14): printed page =
PDF page + 231. Jursa 2011 (Herodot und das Persische Weltreich): printed pages in the running heads.
Fields as in 81_lit_evidence_v2_ed_ebla.py."""
RI='richardsonOldBabylonianTaxation2020'; DG='degraefTaxationLateOld2020'; JM='jursaAncientNearEast2015'
J09='jursaAspectsTaxationAchaemenid2009'; J11='jursaTaxationService2011'
E=[
# ------------------------------------------------------------------ Ur III
dict(period='Ur III',param='FISC',score=3,stance='supports',key=JM,where='p. 127',basis='substantial',genre='admin',archive='Umma, Girsu, Irisaĝrig (provincial)',
 quote='The resulting image is that of a fairly coherent and centralized system of resource extraction that tapped most, if not all, areas of economic production, withdrawing, according to a very rough estimate, on average perhaps about one-third of the output.',
 note='Rests on the bala and gún ma-da records (pp. 125-126), i.e. the bulk of the provincial archives.'),
dict(period='Ur III',param='HIER',score=2.5,stance='qualifies',key=JM,where='p. 158 n. 156',basis='assertion',genre='mixed',archive='none',
 quote='In actual practice, local particularism and resistance on the part of local elites undermined the uniform monolithic structure of the Ur III state.',note='A footnote without evidence cited.'),
# ------------------------------------------------------------------ Early Old Babylonian / Old Babylonian
dict(period='Early Old Babylonian',param='PAL',score=3,stance='supports',key=JM,where='p. 127',basis='documented',genre='admin',archive='Isin craft archive; Larsa; Ešnunna',
 quote='In the early Old Babylonian period the southern Babylonian city states financed themselves mostly through the production of the royal domain, which was under direct management and was worked by dependent laborers.',note=''),
dict(period='Old Babylonian',param='PRIV',score=2,stance='supports',key=JM,where='p. 127',basis='documented',genre='mixed',archive='family and private archives (Sippar, Nippur, Ur)',
 quote='Overall, one notes an “individualization” of agricultural production. Royal land was in large part not under the direct management of the royal administration anymore.',
 note='Later OB, especially the north: crown land held by soldier-tenants who owed service and rents.'),
dict(period='Old Babylonian',param='FISC',score=1.5,stance='contests',key=RI,where='p. 217',basis='documented',genre='mixed',archive='family and private archives (Sippar, Nippur, Ur)',
 quote='no system of state income was regularized in such a way that it was expected to meet future state costs.',
 note='Richardson\'s thesis: OB taxation served "to create political subjectivity, more than to support regular systems of state income and outlays" (p. 217). p. 222 reviews the tax terms: most were "restricted in area/time of use", "occasional rather than regular" or "uncommon".'),
dict(period='Old Babylonian',param='FISC',score=1.5,stance='contests',key=RI,where='p. 236',basis='documented',genre='mixed',archive='family and private archives (Sippar, Nippur, Ur)',
 quote='Nevertheless, the limited focii of Old Babylonian taxation suggests that states of that time were minority shareholders in GDP wealth.',
 note='p. 238: letters and transactions "demonstrate how asystematic taxation was in practice".'),
dict(period='Old Babylonian',param='FISC',score=2,stance='supports',key=DG,where='p. 171',basis='documented',genre='admin',archive='Chief dirge singers\' archive (Sippar-Amnānum)',
 quote='In conclusion, the igisûm was an annual tax due in silver, to be paid in instalments in the first and seventh months. In reality, payments (no doubt in part overdue) were done throughout the year.',
 note='Late OB (Ammi-ditana to Samsu-ditana), northern Babylonia. p. 185: biltum was a tax on the yield of state land; p. 201: merchants and the kārum converted taxes in kind into silver for the palace.'),
dict(period='Old Babylonian',param='FISC',score=2,stance='supports',key=DG,where='p. 185',basis='documented',genre='admin',archive='Chief dirge singers\' archive (Sippar-Amnānum)',
 quote='In conclusion, the biltum was a tax on the yield of state land assigned to persons and/or institutions.',
 note='Part of the biltum stayed in Sippar for the temple; part went to storehouses for army rations: levies recorded locally.'),
# ------------------------------------------------------------------ Neo-Assyrian
dict(period='Neo-Assyrian',param='FISC',score=3,stance='supports',key=JM,where='p. 158',basis='documented',genre='admin',archive='Nineveh royal archives and library',
 quote='The Neo-Assyrian Empire developed a fairly uniform and effective taxation model with its grain, straw, and cattle taxes.',note='Following Radner 2007 (p. 129 n. 39).'),
dict(period='Neo-Assyrian',param='FISC',score=2.5,stance='qualifies',key=JM,where='p. 129',basis='documented',genre='admin',archive='Nineveh royal archives and library',
 quote='Land taxes were payable not to a central institution but either to provincial governments (the most frequent option) or to temples',
 note='Uniform rules, but collected and spent in the provinces.'),
# ------------------------------------------------------------------ Neo-Babylonian and Achaemenid Babylonia
dict(period='Neo-Babylonian',param='FISC',score=2.5,stance='supports',key=JM,where='p. 131',basis='substantial',genre='mixed',archive='Eanna (Uruk), Ebabbar (Sippar)',
 quote='As in the Neo-Assyrian period, taxation has to be considered the principal source of state revenue; the yield of royal domain land would seem to have been of less importance.',
 note='Same page: "There is no fundamental break between the two periods/systems" (Neo-Babylonian and Achaemenid). p. 158: "the broadening of the tax base by a considerable expansion of indirect taxation and the corresponding extension of accounting and information-gathering procedures".'),
dict(period='Neo-Babylonian',param='TCTL',score=2.5,stance='supports',key=J09,where='p. 254',basis='documented',genre='admin',archive='Eanna (Uruk), Ebabbar (Sippar)',
 quote='at least since the reign of Nabonidus, and probably even earlier, a part of the yield of temple lands was directly collected by the Marduk temple (via the bēl pīhāti of Esangila) for the crown, and that this tax persisted into the Achaemenid period.',note='A crown levy on temple harvests.'),
dict(period='Achaemenid',param='FISC',score=2,stance='supports',key=J11,where='p. 440',basis='documented',genre='admin',archive='Babylonian family and Murašû archives; Eanna/Ebabbar',
 quote='the entire organisation was in Babylonian hands, and the tax money circulated primarily among Babylonians. No record of the pertinent transactions would have reached the royal administration.',
 note='p. 438: neither the Achaemenid conquest nor Darius "brought qualitative change in the system"; payments hired substitute workers "in an entirely decentralised manner". Regular levies recorded locally: 2. A null for the turning points of 539 and Darius.'),
dict(period='Achaemenid',param='FISC',score=2,stance='supports',key=J09,where='p. 265',basis='documented',genre='admin',archive='Babylonian family and Murašû archives; Eanna/Ebabbar',
 quote='The systematisation and standardisation certainly had limits, however; there was no centralised collection of Babylonian taxes, and local institutions dealt directly with the Persian overlords in the country or in Elam.',
 note='Same page: "In its basic structure, the Achaemenid tax system in Babylonia was a continuation of native Babylonian practice. Changes were gradual, not radical, even under Darius". Borsippa priestly archives.'),
dict(period='Achaemenid',param='BUR',score=2,stance='qualifies',key=J09,where='p. 265',basis='documented',genre='admin',archive='Babylonian family and Murašû archives; Eanna/Ebabbar',
 quote='There may have been a tendency towards more uniformity in that the terminology related to the system of taxation based on the bow tax and the ‘bow fief’ was sometimes applied to older land allotment schemes',
 note='Uniform terminology spread, but no central collection.'),
]
