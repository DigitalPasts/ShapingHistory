"""Archive inventory per period (ShG, 3 Nov 2026: 'certain kinds of evidence come only from specific archives ... we should
have weights for that built in'). For each period: the main archives behind the textual record, the kind of institution
that kept them, and a share. Shares for ED-Ur III come from published corpus counts (cited); the 'corpus' column gives the
share of the dated tablets in our own image corpus (CDLI) by site, so the two can be compared.
KIND decides which parameters an archive can inflate (its own institution looks large because it kept the records) and
which it can hide (the institutions that did not write into it look absent). Used by 85b_build_scores_v2.py."""
from _paths import WORK
import pandas as pd, json
INFLATES={'palace':['PAL','TCTL','BUR'],'temple':['TEMP','BUR'],'state':['BUR','FISC','STD','HIER'],
          'private':['PRIV','LAW'],'royal inscriptions':['TERR','HIER','LAW'],'school':['SCHOOL'],'mixed':[]}
HIDES={'palace':['TEMP','PRIV'],'temple':['PAL','PRIV'],'state':['PRIV'],'private':['PAL','TEMP','BUR'],
       'royal inscriptions':['PRIV','FISC'],'school':[],'mixed':[]}
INV={
 'ED IIIa':[('Fara','mixed',0.64,'bramantiTaxationEarlyMesopotamia2020','p. 25: c. 900 texts (administrative, city "houses")'),
            ('Abu Salabikh','school',0.36,'bramantiTaxationEarlyMesopotamia2020','p. 25: c. 500 texts, mostly lexical and literary')],
 'ED IIIb':[('Girsu','temple',0.47,'bramantiTaxationEarlyMesopotamia2020','p. 25: c. 1,800 texts, the é-mí / Bau household run by the ruler’s wife. Schrakamp & Zólyomi 2025 p. 93: nearly all from one household, 2335-2315 BC; Schrakamp 2013 p. 446: Gelb criticized a model built on an archive of "lediglich 20 Jahren Laufzeit"'),
            ('Umma','mixed',0.29,'bramantiTaxationEarlyMesopotamia2020','p. 25: c. 1,100 texts'),
            ('Adab','mixed',0.13,'bramantiTaxationEarlyMesopotamia2020','p. 25: c. 500 texts'),
            ('Nippur','mixed',0.12,'bramantiTaxationEarlyMesopotamia2020','p. 25: c. 450 texts')],
 'Ebla':[('Ebla palace G','palace',1.0,'archiEblaItsArchives2015','p. 84: c. 3,000-3,500 tablets, all from the palace; central archive L. 2769 holds 1,757. pp. 19-20: monthly and annual farming and livestock accounts were not kept')],
 'Old Akkadian':[('Girsu','state',0.38,'bramantiTaxationEarlyMesopotamia2020','p. 26: c. 2,300 texts'),('Adab','state',0.38,'bramantiTaxationEarlyMesopotamia2020','p. 26: c. 2,300 texts. Schrakamp, CDLN 2014:23: illicit Adab texts "currently provide the largest corpus of Sargonic texts"; Schrakamp 2017 p. 82: c. 8,000 Sargonic texts from over 20 sites'),
                 ('Umma','state',0.12,'bramantiTaxationEarlyMesopotamia2020','p. 26: c. 700 texts'),('Nippur','mixed',0.11,'bramantiTaxationEarlyMesopotamia2020','p. 26: c. 650 texts')],
 'Ur III':[('Umma, Girsu, Irisaĝrig (provincial)','state',0.55,'molinaArchivesBookkeepingSouthern2016','§27-29: "the great majority of our texts come from large institutions, i.e. provincial or royal archives"'),
           ('Puzriš-Dagān, Ur (royal)','state',0.35,'molinaArchivesBookkeepingSouthern2016','§27'),
           ('Nippur Inanna temple; private (Tūram-ilī, SI.A-a)','mixed',0.10,'molinaArchivesBookkeepingSouthern2016','§22, §27')],
 'Early Old Babylonian':[('Isin craft archive; Larsa; Ešnunna','state',0.6,None,'our estimate; no published share found yet'),('private','private',0.4,None,'our estimate; no published share found yet')],
 'Old Babylonian':[('family and private archives (Sippar, Nippur, Ur)','private',0.6,None,'our estimate; no published share found yet'),('Mari palace; Larsa crown','palace',0.4,None,'our estimate; no published share found yet')],
 'Old Assyrian':[('Kaneš merchant houses','private',0.95,'vitaHistoryAkkadianLanguage2021','p. 40: "In the homes of merchants in Kaneš, over 23,000 tablets were discovered"; p. 1105: c. 22,300 from Kültepe by 2003')],
 'Middle Babylonian':[('Nippur governor’s office','state',0.8,None,'our estimate; no published share found yet'),('private','private',0.2,None,'our estimate; no published share found yet')],
 'Middle Assyrian':[('Assur, Dūr-Katlimmu, Tell Sabi Abyad state archives','state',0.7,None,'our estimate; no published share found yet'),('Assur family archives','private',0.3,None,'our estimate; no published share found yet')],
 'Neo-Assyrian':[('Nineveh royal archives and library','palace',0.6,None,'our estimate; no published share found yet'),('private archives (Assur, Kalḫu, Dūr-Katlimmu)','private',0.4,None,'our estimate; no published share found yet')],
 'Neo-Babylonian':[('Eanna (Uruk), Ebabbar (Sippar)','temple',0.6,'jursaAspectsEconomic2010','p. 9: "more than half of the published texts ... are made up of just two huge temple archives, those of Eanna in Uruk and of Ebabbar in Sippar"; the royal administration left no archives apart from palace ration lists'),('family archives (Egibi etc.)','private',0.4,'jursaAspectsEconomic2010','p. 9 n. 42: the largest private archive (Egibi) has c. 1,700 tablets, Murašû c. 750')],
 'Achaemenid':[('Persepolis Fortification and Treasury','state',0.5,None,'our estimate; no published share found yet'),('Babylonian family and Murašû archives; Eanna/Ebabbar','private',0.5,None,'our estimate; no published share found yet')],
 'Hellenistic':[('Rēš and Esagil temple archives','temple',0.5,'jursaAspectsEconomic2010','p. 6: "only two principal sites, Uruk and Babylon ... have yielded several hundred archival documents"; share is our estimate'),('private (Uruk, Babylon)','private',0.5,None,'our estimate; no published share found yet')],
}
def table():
    rows=[]
    for p,L in INV.items():
        for a,k,s,key,w in L: rows.append(dict(period=p,archive=a,kind=k,share=s,key=key,where=w))
    return pd.DataFrame(rows)
def dominant(p):
    L=INV.get(p,[]); 
    if not L: return None
    a=max(L,key=lambda x:x[2]); return dict(archive=a[0],kind=a[1],share=a[2])
if __name__=='__main__':
    t=table(); d=pd.read_parquet(WORK+'/master_tablets.parquet',columns=['period','site'])
    cs={p:g.site.value_counts(normalize=True).head(4).round(2).to_dict() for p,g in d.groupby('period')}
    t['corpus_sites']=t.period.map(lambda p: json.dumps(cs.get(p,{}),ensure_ascii=False))
    t.to_csv(WORK+'/centralization/archive_inventory.csv',index=False); print(t.to_string())
