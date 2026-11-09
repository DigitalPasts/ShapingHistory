"""Literature evidence for the centralization codebook: Hellenistic Babylonia (Seleucid and early Arsacid, 331-c. 100 BC).
OHANE ends with Alexander; sources are from ShG's Google Drive. Page numbers taken from Drive text extraction are marked
'to verify'. Format as 81_lit_evidence_ur3.py."""
P='Hellenistic'
MC='monerieCompendiumOfficialCorrespondence2023'  # Monerie, J., and Clancier, P. 2023. A compendium of official correspondence from Seleucid Uruk. AoF 50: 63-82.
PI='pirngruberEconomyLateAchaemenid2017'          # Pirngruber, R. 2017. The economy of Late Achaemenid and Seleucid Babylonia. Cambridge: CUP.
E=[
 dict(param='TERR',score=3,stance='supports',key=PI,where='Pirngruber 2017, ch. 2, p. 19 (to verify)',
  quote="The diary given as example closes with a brief historical passage, which relates a visit from the satrap from his residence in the provincial capital Seleucia-on-the-Tigris to Babylon for a sojourn of ten days.",
  note='Babylonia as a satrapy of the Seleucid empire.'),
 dict(param='HIER',score=2,stance='supports',key=MC,where='p. 72',
  quote="Despite the comparative wealth of the Babylonian documentation, surprisingly little is known of the satrapy’s administration during the first decades of the Seleucid era ... it is not unreasonable to assume that most of them were Seleucid officials operating at various levels of the satrapal administration."),
 dict(param='TEMP',score=3,stance='supports',key=MC,where='p. 73',
  quote="Similarly to the Seleucid letters addressed to the temple administrator (šatammu) of the Esagil and/or the “Babylonians” (i.e., the temple assembly representing the city) recorded in the astronomical diaries and chronicles from the third century BC, the final recipients and/or main beneficiaries of the documents translated in YOS 20, 87 seem to have been a certain Kidin-Anu, along with the Urukean temple assembly."),
 dict(param='TCTL',score=1,stance='supports',key=MC,where='Monerie and Clancier 2023, abstract, p. 63',
  quote="it is an Akkadian translation of a collection of Greek official documents issued by the Seleucid administration in the first quarter of the third century BC, concerning the rebuilding of the Bīt Rēš, the main sanctuary of Uruk at the time ... a valuable addition to the dossier of Seleucid euergetic policy in Babylonia.",
  note='Royal patronage (euergetism) rather than direct management; the crown dealt with temples through the šatammu and the assembly.'),
 dict(param='PAL',score=2,stance='supports',key=MC,where='p. 73',
  quote="A more promising lead would be to understand them as officials of the local basilikon, the royal institution in charge of managing the Crown’s resources, which played a major part in the local implementation of royal euergetic actions."),
 dict(param='BUR',score=1,stance='supports',key=MC,where='p. 72',
  quote="Babylonian sources from Northern Babylonia such as the astronomical diaries and the chronicles regularly mention the reception of leather documents (kuššipištu) sent to local authorities by the royal chancery, but their content is rarely reproduced verbatim ... the letters received from the Seleucid administration were fully translated from Greek to Akkadian",
  note='State administration in Greek on leather and parchment; cuneiform clay records only the temple and private spheres. Clay tablets are not the state record in this period.'),
]
ACH=[dict(period='Achaemenid',param='TCTL',score=3,stance='supports',key=PI,where='Pirngruber 2017, ch. 3, pp. 35-36 (to verify)',region='Babylonia',
  quote="Most importantly, the traditional local power structures were utterly uprooted. In Babylon, the prebendary system, the mainstay of the local elites whence they derived social prestige, political power and material wealth, was abolished. Likewise, the office of šatammu ... as the highest representative of local interest vis-à-vis the crown disappears from the record for decades to come. A new elite was created, whose power base was their ties to the crown and its representatives.",
  note='After the revolts against Xerxes, 484 BC (Waerzeggers 2003/4).')]
GAPS={'FISC':'Seleucid taxation in Babylonia: Monerie 2018 (L’économie de la Babylonie à l’époque hellénistique, SANER 14); Kosmin 2014; Capdetrey 2007',
      'PRIV':'private archives of Uruk and Babylon: Corò 2005 (prebends); Wallenfels; Monerie 2018',
      'SCHOOL':'Hellenistic scholarly families and libraries: Clancier 2009 (Les bibliothèques en Babylonie); Robson',
      'LAW':'Seleucid legal practice in Babylonia: Doty 1977; Monerie','STD':'Seleucid Era dating and coinage: Boiy 2004; Kosmin 2018 (Time and its Adversaries)',
      'COMM':'no direct statement found','HIER':'Capdetrey 2007 (Le pouvoir séleucide)'}
