"""Build the HTML review page (literature evidence, scores, statistics, Hammurabi break points)."""
from _paths import PAPER, TEMPLATES, WORK
import json, pandas as pd
C=WORK+'/centralization'
OUT=PAPER+'/centralization/centralization_literature_review.html'
MAIN=['ED IIIa','ED IIIb','Ebla','Old Akkadian','Ur III','Early Old Babylonian','Old Babylonian','Old Assyrian','Middle Babylonian','Middle Assyrian','Neo-Assyrian','Neo-Babylonian','Achaemenid','Hellenistic']
SI=['Achaemenid (Babylonia)','Achaemenid (Persepolis)','Hittite','Middle Elamite']
P=['TERR','HIER','FISC','COMM','PAL','TEMP','TCTL','PRIV','BUR','SCHOOL','LAW','STD']
NAMES={'TERR':'Territorial reach','HIER':'Administrative hierarchy','FISC':'Fiscal extraction','COMM':'Communications','PAL':'Palace economy','TEMP':'Temple economy','TCTL':'Royal control of temples','PRIV':'Private sector','BUR':'Standardized bureaucracy','SCHOOL':'Scribal training','LAW':'Royal law','STD':'Standard measures, calendar'}
L=pd.read_csv(f'{C}/lit_scores_long.csv'); E=pd.read_csv(f'{C}/lit_evidence_long.csv').fillna('')
G=json.load(open(f'{C}/lit_gaps.json'))
S=pd.read_csv(f'{C}/stats_spearman.csv'); W=pd.read_csv(f'{C}/stats_wild_cluster.csv'); T=pd.read_csv(f'{C}/stats_period_table.csv')
RL=pd.read_csv(f'{C}/reading_log.tsv',sep='\t').fillna('')
H=pd.read_csv(f'{C}/hammurabi_breaks.csv'); HS=pd.read_csv(f'{C}/hammurabi_break_scan.csv')
data=dict(main=MAIN,si=SI,params=P,names=NAMES,
  scores=L[['period','param','score','lo','hi','contested','conf','source','n_entries','prior']].to_dict('records'),
  ev=E[['period','param','score','stance','quote','where','key','note']].to_dict('records'),gaps={},reading=RL.to_dict('records'),fmt=['Foster 1982, p. 3: Sargonic tablet shape follows the level of accountability of the record.', 'Kraus 2020, p. 40: a new, uniform tablet shape appears throughout Mesopotamia under Naram-Suen; p. 29 notes the change may be organic.', 'Pomponio 2013, pp. 224-226: Umma messenger texts fall into three archive groups with different layouts and tablet shapes, one group squarer than the rest.', "Charpin 2010, p. 119: Rim-Sin's chancellery wrote all letters on large tablets of very elongated form, whatever the length of the message; Mari letters varied in size (p. 121).", 'Van De Mieroop 1987, pp. 118-119: the Early Isin craft archive keeps the language and format of Ur III texts.', 'Charpin 2010, p. 119: the size of Neo-Assyrian letter tablets was fixed.', 'Charpin 1995, p. 812: Ur III scribes received uniform training, with new formats for archival texts.', 'Yoffee 1995, p. 295: large summary tablets record six-monthly or yearly accounts at Drehem.', 'Pollock 2016, p. 284 n. 37: scribes probably shaped their own tablets.', 'Basello and Giovinazzo 2018, p. 486: at Haft Tappeh, letter orders and economic texts are on rectangular tablets, school texts on lentil (disk) tablets.', 'Basello and Giovinazzo 2018, p. 487: Middle Elamite administrative tablets from Malyan (EDD) are mostly small and cigar-shaped.', 'Basello and Giovinazzo 2018, p. 496: Persepolis recapitulative journals are on oversized rectangular tablets; some bullae share the tongue shape of the memoranda.', 'Messina 2009, p. 179: under Antiochus I, taxed contracts moved from clay tablets to sealed parchment.', 'Postgate 2013, p. 428: Neo-Assyrian government ran without the sealed bilateral documents of the Middle Assyrian administration.', "Freydank 1997, p. 47: Middle Assyrian ginā'u offering lists use a tabular landscape format with five columns.", 'Veldhuis 2000, p. 67: the Kassite pillow-shaped exercise tablet is the same type at Nippur, Babylon, Kish, Ur and Bahrain.', 'Henkelman 2008, pp. 102-103: Persepolis memoranda are tongue-shaped by text category; unsealed tablets of one official are irregular.', 'Corò 2005, p. 5: Seleucid prebend sales are temple documents; the tablets are about 1 cm thick and 10-12 cm square.'],
  spear=S.round(3).to_dict('records'),wild=W.round(4).to_dict('records'),ptab=T.round(3).to_dict('records'),
  ham=H.drop(columns=['cells']).round(4).to_dict('records'),scan=HS.round(3).to_dict('records'))
tpl=open(TEMPLATES+'/review_template.html').read()
open(OUT,'w').write(tpl.replace('/*DATA*/',json.dumps(data,ensure_ascii=False)))
print(OUT)
