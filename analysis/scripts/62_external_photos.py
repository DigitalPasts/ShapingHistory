"""Amarna letters not photographed in the CDLI but published as public-domain photographs by their museum.
EA 15 (Aššur-uballiṭ I to the king of Egypt): Metropolitan Museum of Art 24.2.11, object 544695, Open Access (CC0).
The obverse is segmented against the dark background of the museum photograph and its height-to-width ratio taken
from the bounding box, as for the CDLI photographs; the museum's catalogue dimensions are kept for comparison.
Output: amarna/external_photos.csv."""
from _paths import WORK
import json, urllib.request, os, numpy as np, cv2, pandas as pd
R=WORK; D=f'{R}/amarna/external'; os.makedirs(D,exist_ok=True)
rows=[]
for ea,obj in [(15,544695)]:
    m=json.load(urllib.request.urlopen(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj}'))
    f=f'{D}/EA{ea:03d}_met{obj}.jpg'
    if not os.path.exists(f): urllib.request.urlretrieve(m['primaryImage'],f)
    g=cv2.cvtColor(cv2.imread(f),cv2.COLOR_BGR2GRAY)
    bg=np.median(np.r_[g[:20].ravel(),g[-20:].ravel(),g[:,:20].ravel(),g[:,-20:].ravel()])
    d=cv2.morphologyEx((np.abs(g.astype(int)-bg)>25).astype(np.uint8),cv2.MORPH_OPEN,np.ones((15,15),np.uint8))
    n,l,st,_=cv2.connectedComponentsWithStats(d); k=1+np.argmax(st[1:,4]); x,y,w,h,a=st[k]
    rows.append(dict(EA=ea,museum='Metropolitan Museum of Art',museum_no=m['accessionNumber'],title=m['title'],photo=m['primaryImage'],
                     licence='Met Open Access (public domain)' if m['isPublicDomain'] else '?',hw_photo=round(h/w,3),catalogue_dimensions=m['dimensions']))
P=pd.DataFrame(rows); P.to_csv(f'{R}/amarna/external_photos.csv',index=False); print(P.T)
