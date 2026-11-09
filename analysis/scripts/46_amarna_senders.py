"""Case B data: sender and city of each Amarna letter (attributions after Moran 1992, to be checked against Rainey 2015),
clay provenance where Goren, Finkelstein and Na'aman published it per letter (NEA 65, 2002; AJA 107, 2003), and site
coordinates (Pleiades where the place exists there, cited by Pleiades id; otherwise the CDLI location record; otherwise
flagged 'approx'). Output: amarna/amarna_letters.csv, amarna/amarna_sites.csv."""
from _paths import WORK
import pandas as pd, numpy as np
R=WORK
# (first EA, last EA, sender, city/court, region)
S=[(1,1,'Amenhotep III (draft)','Egypt','Egypt'),(2,4,'Kadašman-Enlil I','Babylon','Great kings'),(5,5,'Amenhotep III (draft)','Egypt','Egypt'),
(6,12,'Burna-Buriaš II','Babylon','Great kings'),(13,13,'Babylonian inventory','Babylon','Great kings'),(14,14,'Egyptian inventory','Egypt','Egypt'),
(15,16,'Aššur-uballiṭ I','Assur','Great kings'),(17,29,'Tušratta','Mittani','Great kings'),(31,31,'Amenhotep III (draft)','Egypt','Egypt'),
(32,32,'Tarḫundaradu','Arzawa','Great kings'),(33,40,'King of Alašiya','Alashiya','Great kings'),(41,44,'Hittite king','Hattusa','Great kings'),
(45,49,'Kings of Ugarit','Ugarit','North Syria'),(51,51,'Addu-nirari','Nuhasse','North Syria'),(52,55,'Akizzi','Qatna','North Syria'),
(59,59,'Citizens of Tunip','Tunip','North Syria'),(60,62,'Abdi-Aširta','Amurru','Amurru and the coast'),
(68,95,'Rib-Hadda','Byblos','Amurru and the coast'),(97,98,'Yapaḫ-Hadda','Beirut?','Amurru and the coast'),(101,138,'Rib-Hadda','Byblos','Amurru and the coast'),
(139,140,'Ili-rapiḫ','Byblos','Amurru and the coast'),(141,143,'Ammunira','Beirut','Amurru and the coast'),(144,145,'Zimredda','Sidon','Amurru and the coast'),
(146,155,'Abi-Milku','Tyre','Amurru and the coast'),(156,161,'Aziru','Amurru','Amurru and the coast'),(164,171,'Aziru and his sons','Amurru','Amurru and the coast'),
(189,189,'Etakkama','Kadesh','Central Syria'),(194,197,'Biryawaza','Kumidi','Central Syria'),(227,228,'King of Hazor','Hazor','Canaan'),
(232,235,'Surata and Satatna','Akko','Canaan'),(242,247,'Biridiya','Megiddo','Canaan'),(252,254,'Labʾayu','Shechem','Canaan'),(256,256,'Mut-Baʿlu','Pella','Canaan'),
(257,259,'Baʿlu-meḫir','Yokneam','Canaan'),(264,266,'Tagi','Ginti-kirmil','Canaan'),(267,271,'Milkilu','Gezer','Canaan'),(278,284,'Šuwardata','Gath','Canaan'),
(285,290,'ʿAbdi-Ḫeba','Jerusalem','Canaan'),(292,294,'Addu-dani','Gezer','Canaan'),(297,300,'Yapaḫu','Gezer','Canaan'),(314,316,'Pu-Baʿlu','Yurza','Canaan'),
(320,326,'Yidya','Ashkelon','Canaan'),(328,332,'Rulers of Lachish','Lachish','Canaan'),(365,365,'Biridiya','Megiddo','Canaan')]
# clay provenance published per letter (Goren et al. 2002 NEA 65:196-205; 2003 AJA 107:233-255)
CLAY={33:'S Cyprus, Pakhna marl',34:'S Cyprus, Pakhna marl',38:'S Cyprus, Pakhna marl',37:'S Cyprus, Moni melange (Kalavasos)',
 60:'Mt Lebanon highland (Lower Cretaceous shale)',157:'Mt Lebanon highland (Lower Cretaceous shale)',61:'Ardata (Neogene marl)',62:'Ardata (Neogene marl)',
 156:'Ardata (Neogene marl)',159:'Ardata (Neogene marl)',161:'Irqata (Akkar inland marl)',164:'Irqata (Akkar inland marl)',169:'Irqata (Akkar inland marl)',
 170:'Irqata (Akkar inland marl)',171:'Irqata (Akkar inland marl)',165:'Sumur (Akkar coast)',166:'Sumur (Akkar coast)',167:'Sumur (Akkar coast)',
 59:'Tunip = Tell Asharneh (glauconite marl)',249:'Jordan valley S of Beth-Shean (Rehob or Beth-Shean)',257:'Yokneam (Carmel tuff)',258:'Yokneam (Carmel tuff)',
 259:'Yokneam (Carmel tuff)',264:'Jatt in the Sharon (Taqiye marl)',265:'Jatt in the Sharon (Taqiye marl)',266:'Jatt in the Sharon (Taqiye marl)',
 1:'Upper Egypt (Esna shale)',14:'Upper Egypt (Esna shale)',162:'Upper Egypt (Esna shale)',163:'Egypt (Nile silt)'}
a=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','designation','provenience','collections','genres','museum_no'],low_memory=False)
a=a[a.provenience.fillna('').str.startswith('Akhetaten')].copy()
a['EA']=a.designation.str.extract(r'^EA (\d+)')[0].astype(float)
def look(e):
    if pd.isna(e): return (None,None,None)
    if e>=340: return ('scholarly or school text','Akhetaten','Scholarly texts')
    for lo,hi,s,c,r in S:
        if lo<=e<=hi: return (s,c,r)
    return (None,None,None)
a[['sender','city','region']]=a.EA.apply(lambda e: pd.Series(look(e)))
a['clay_published']=a.EA.map(CLAY)
v=pd.concat([pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_{s}.csv',usecols=['CDLI_id']) for s in ['train','val','test']])
p=pd.read_csv(f'{R}/zenodo/h_w_ratio_df_all.csv'); p['artifact_id']=p.tablet_p_id_CDLI.str[1:].astype(int)
a['photographed']=a.artifact_id.isin(v.CDLI_id)
a=a.merge(p[['artifact_id','hw_ratio']].drop_duplicates('artifact_id'),on='artifact_id',how='left')
a['P']=a.artifact_id.map(lambda i:f'P{i:06d}')
a.sort_values('EA').to_csv(f'{R}/amarna/amarna_letters.csv',index=False)
print(a.groupby(['region','city'],dropna=False).agg(n=('EA','size'),photo=('photographed','sum'),hw=('hw_ratio','median'),clay=('clay_published','count')).to_string())
