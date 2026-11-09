"""Case B: coordinates for the Amarna sender cities and the control sites. Pleiades first (places dump, Pleiades
gazetteer), else CDLI locations (cdli.earth/locations/{id}.json), else an approximate position of the modern tell,
flagged as such. Output: geo/amarna_sites.csv."""
from _paths import WORK
import pandas as pd, json, urllib.request
R=WORK
P=pd.read_csv(f'{R}/geo/pleiades/places.csv.gz',low_memory=False); P['id']=pd.to_numeric(P.id,errors='coerce')
pl={'Byblos':668216,'Tyre':678437,'Sidon':678393,'Beirut':678060,'Beirut?':678060,'Qatna':412342122,'Lachish':687951,
 'Hazor':779967430,'Akhetaten':149576487,'Egypt':149576487,'Nuzi':894054,'Hattusa':283602441,'Jerusalem':687928,
 'Gezer':687904,'Ashkelon':687839,'Shechem':678403,'Kumidi':10481849,'Yokneam':180354033,'Pella':678326,
 'Kadesh':668291,'Amurru':668372,'Sumur':668372,'Babylon':893951,'Mittani':641191178,'Arzawa':35475912,'Assur':893945,
 'Alashiya':707498,'Gaza':687902,'Beth-Shean':678378,'Damascus':678106,'Ashdod':687838}
cdli={'Ugarit':562,'Alalakh':13,'Megiddo':332,'Tunip':537,'Kar-Tukulti-Ninurta':306,'Nippur':None}
approx={'Akko':(32.921,35.084,'Tel Akko'),'Gath':(31.700,34.846,'Tell es-Safi'),'Yurza':(31.389,34.432,'Tell Jemmeh'),
 'Ginti-kirmil':(32.400,35.033,'Jatt in the Sharon'),'Irqata':(34.537,36.044,'Tell Arqa'),'Ardata':(34.395,35.886,'Ardé'),
 'Nuhasse':(35.70,36.90,'region, approximate'),'Mt Lebanon':(34.30,36.05,'slopes E of Tripoli, approximate'),
 'Ullasa?':(34.45,35.85,'Tripoli area, approximate'),'Beqa valley':(33.85,35.95,'region, approximate'),'Bashan':(32.85,36.05,'region, approximate'),
 'Anaharath':(32.66,35.46,'Tel Rekhesh, approximate'),'Akshapa':(32.86,35.16,'Tel Keisan, approximate'),'Sharuna':(32.62,35.52,'approximate'),
 'Nii':(35.42,36.39,'approximate'),'Nippur':(32.127,45.231,'Pleiades 912910')}
rows=[]
for c,i in pl.items():
    r=P[P.id==i].iloc[0]; rows.append(dict(site=c,lat=r.reprLat,lon=r.reprLong,source=f'Pleiades {i}',name=r.title))
for c,i in cdli.items():
    if i is None: continue
    d=json.load(urllib.request.urlopen(f'https://cdli.earth/locations/{i}.json'))[0]
    rows.append(dict(site=c,lat=d['location_latitude_wgs1984'],lon=d['location_longitude_wgs1984'],source=f'CDLI location {i}',name=d['location']))
for c,(la,lo,n) in approx.items():
    rows.append(dict(site=c,lat=la,lon=lo,source='Pleiades 912910' if c=='Nippur' else 'approximate',name=n))
S=pd.DataFrame(rows); S.to_csv(f'{R}/geo/amarna_sites.csv',index=False); print(S.to_string(index=False))
