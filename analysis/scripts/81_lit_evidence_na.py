"""Literature evidence for the centralization codebook: Neo-Assyrian (c. 911-609 BC). Format as 81_lit_evidence_ur3.py.
Postgate 2001 entries for this period are in 81_lit_evidence_cross.py."""
P='Neo-Assyrian'
H='bakerAssyrianEmpireView2023'   # Baker, H. D. 2023. The Assyrian Empire: a view from within. OHANE IV, ch. 38.
F='falesAssyrianEmpirePerspectives2023'  # Fales, F. M. 2023. The Assyrian Empire: perspectives on culture and society. OHANE IV, ch. 40.
E=[
 dict(param='TERR',score=3,stance='supports',key=F,where='OHANE IV, ch. 40, §40.2 (PDF p. 405)',
  quote="the rich mix of texts associated with this polity, which constitutes the most extensive political-territorial formation that the Middle East had yet witnessed."),
 dict(param='HIER',score=3,stance='supports',key=H,where='OHANE IV, ch. 38, §38.1.3 (PDF p. 260)',
  quote="All of the lands that were under direct rule were organized into provinces under Assyrian governors appointed by the king. Around the fringes could be found friendly kingdoms whose rulers were permitted to retain their thrones so long as they remained submissive and delivered a fixed amount of annual tribute"),
 dict(param='HIER',score=2,stance='contests',key=H,where='OHANE IV, ch. 38, §38.3.6 (PDF pp. 278-279), citing Grayson and Liverani',
  quote="The concept of a “feudal” era spanning the late reign of Shalmaneser III down to the accession of Tiglath-pileser III in 744 BC has developed as a means of characterizing this phase of Neo-Assyrian history during which the monarchy is perceived to have been weak ... Similarly, Mario Liverani described this period as one “with provincial governors challenging the central power and Assyrian expansion coming to a temporary halt.” ... I see no evidence to suggest that the interests of these magnates were not perfectly well aligned with those of the king",
  note='Debate: Grayson/Liverani (magnates challenge the crown) vs Baker (aligned with the king). Relevant to within-period variation.'),
 dict(param='FISC',score=3,stance='supports',key=H,where='OHANE IV, ch. 38, §38.1.3 (PDF p. 260)',
  quote="friendly kingdoms whose rulers were permitted to retain their thrones so long as they remained submissive and delivered a fixed amount of annual tribute that the Assyrian king imposed on them; failure to do so was considered a justification for invasion"),
 dict(param='FISC',score=3,stance='supports',key=F,where='OHANE IV, ch. 40, §40.5.1 (PDF p. 438)',
  quote="The royal inscriptions consistently portray the Assyrian identity as an aspirational privilege and a major boon conferred by the ruler on newly integrated peoples of the empire, tied to the acceptance of all the obligations of the king’s subjects, most importantly taxation and conscription."),
 dict(param='COMM',score=3,stance='supports',key=H,where='OHANE IV, ch. 38, §38.1.1 (PDF p. 256)',
  quote="The administrative letters of the official correspondence consist mainly of letters exchanged between the king and his high officials, especially the provincial governors. These come mostly from Nineveh and are edited in the State Archives of Assyria series",
  note='The royal road and relay system (kalliu) needs Radner 2014 (State correspondence in the ancient world).'),
 dict(param='PAL',score=3,stance='supports',key=F,where='OHANE IV, ch. 40, §40.2 (PDF p. 407)',
  quote="such texts document various state-issued data sets, typically pertaining to incoming or outgoing personnel and goods, from a range of administrative contexts (palatial, provincial, or municipal), most commonly in the form of lists, inventories, notes, and accounts of various types"),
 dict(param='PRIV',score=2,stance='supports',key=F,where='OHANE IV, ch. 40, §40.2 (PDF pp. 406-407)',
  quote="there are legal materials either from private contexts or from public and official spheres ... The most important Assyrian libraries from private contexts derive from two very different locations"),
 dict(param='BUR',score=2,stance='supports',key=F,where='OHANE IV, ch. 40, §40.2 (PDF p. 407)',
  quote="This body of texts consists currently of about 6,000 clay tablets written in the Neo-Assyrian vernacular and cuneiform script. The bulk of the available material comes from Nineveh, Kalhu, and Assur in the Assyrian heartland",
  note='Agrees with Postgate 2001 (less paperwork). Much NA administration was on wax boards and in Aramaic on perishable media; clay is a partial record.'),
 dict(param='SCHOOL',score=2,stance='supports',key=F,where='OHANE IV, ch. 40, §40.2 (PDF p. 406)',
  quote="When such Babylonian manuscripts were copied, the scribes either kept the original Babylonian cuneiform script or sometimes copied the text using the Assyrian form of the cuneiform script ... with so-called colophons inserted at the end of the tablets that explain their origins and transmission and mark these manuscripts as royal property."),
 dict(param='LAW',score=2,stance='supports',key=F,where='OHANE IV, ch. 40, §40.2 (PDF p. 407)',
  quote="including royal grants and decrees, appointment documents, and treaty documents of the crown (both with other polities or internal partners within the Assyrian Empire)"),
 dict(param='STD',score=3,stance='supports',key=H,where='OHANE IV, ch. 38, §38.1.2 (PDF p. 257)',
  quote="Thanks to the various manuscripts of the Assyrian Eponym List and the Assyrian Eponym Chronicle, which combine to cover the entire period down to 649 BC, the absolute dating of most of the imperial era is well founded."),
 dict(param='STD',score=3,stance='supports',key=F,where='OHANE IV, ch. 40, §40.2 (PDF p. 407)',
  quote="Many of these texts are dated by year eponym (limmu), month, and day."),
]
GAPS={'COMM':'Radner 2014 (State correspondence; the royal road and kalliu relay); Kessler on the Assyrian road system',
      'TEMP':'Neo-Assyrian temple economy: Postgate 1974 (Taxation and Conscription) on temple dues; Menzel 1981',
      'TCTL':'royal control of temples, qīpu officials: Menzel 1981; Radner',
      'BUR':'Postgate 1974; Radner 2008 on writing boards and Aramaic in administration','SCHOOL':'Gesche 2001 is NB; for NA: Villard; Radner & Robson 2011 handbook'}
