"""Round 3b (8-9 Nov 2026), continued: Old Babylonian Larsa (Middeke-Conlin 2020) and Old Assyrian (Barjamovic 2011).
Middeke-Conlin 2020 (WSAWM 4): pdf n = p. n+19. Its Larsa texts date to Rim-Sin, so they are coded under
Old Babylonian, not Early Old Babylonian (ShG suggested the book for Early OB SCHOOL and BUR).
Barjamovic 2011 (CNI 38): pdf n = p. n+17.
"""
P='Old Babylonian'
MID='middekeconlinMakingScribeErrors2020'; BAR='barjamovicHistoricalGeographyAnatolia2011'
OA='Old Assyrian'
E=[
dict(param='SCHOOL',score=1.5,stance='supports',key=MID,where='p. 37',basis='fragmentary',genre='lexical',archive='school tablets (Larsa, Nippur)',
 quote="These fragmentary texts allow for a very tentative suggestion that the scribal curriculum at Larsa was presented in the same order as that found at Nippur.",
 note='Shared curriculum between cities.'),
dict(param='SCHOOL',score=1,stance='supports',key=MID,where='p. 39',basis='documented',genre='lexical',archive='school tablets (Larsa)',
 quote="Because course 1 shows signs of a complete elementary curriculum—metrological tables as well as numerical tables of multiplication, squares and roots—while course 2 is limited to numerical tables, it is suggested here that there are two different schools represented in the texts from Larsa.",
 note='Several schools in one city with different courses: no single institutional school.'),
dict(param='BUR',score=2,stance='supports',key=MID,where='p. 96',basis='substantial',genre='admin',archive='Larsa merchant archives (Rim-Sin)',
 quote="the silver balanced accounts are records of prior transactions used by merchants to maintain accountability for a higher authority, the palace, to assist this authority in planning income and cost.",
 note=''),
dict(param='PAL',score=2.5,stance='supports',key=MID,where='p. 101',basis='substantial',genre='admin',archive='Larsa merchant archives (Rim-Sin)',
 quote="merchants, members of the local kārum, act as intermediaries on behalf of the temples and crown, assessing excess capital or grain owned or controlled by the temples and crown in silver or labor",
 note=''),
dict(param='BUR',score=2,stance='qualifies',key=MID,where='p. 102',basis='substantial',genre='admin',archive='Larsa archives (Rim-Sin)',
 quote="Actors in personal household archives could also produce merchant archives as well, such as the merchant intermediaries who assess excess capital in silver values on behalf of the crown. This level of organization bridged local administration and regional administration.",
 note='Crown accounting runs through private intermediaries.'),
dict(period=OA,param='TERR',score=0.5,stance='supports',key=BAR,where='p. 26',basis='documented',genre='legal',archive='Kaneš (treaty drafts)',
 quote="The draft of a treaty between the Assyrian traders and a local Anatolian state specifies that the ruler would receive a tiny fee for each donkey passing through his territory. In return, he would guarantee the safety of the Assyrian caravans, compensate losses, and extradite those",
 note='Assur works through treaties with Anatolian rulers, not territorial rule.'),
]
