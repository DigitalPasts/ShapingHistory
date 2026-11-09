"""Pilot: clay colour from CDLI photographs. For each tablet, download the CDLI photo (cdli.earth/dl/photo/P......jpg),
mask the black background (V > 0.16 in HSV, largest components kept by area), and record the median and spread of the
tablet pixels in CIELAB (L*, a*, b*), chroma and hue angle. Photos are deleted after measurement.
Caution: colour depends on lighting and camera; compare only tablets photographed in the same campaign/museum."""
from _paths import WORK
import sys, io, urllib.request, numpy as np, pandas as pd, concurrent.futures as cf
from PIL import Image
from skimage.color import rgb2lab, rgb2hsv
R=WORK
ids=pd.read_csv(sys.argv[1]).artifact_id.astype(int).tolist(); out=sys.argv[2]
def one(i):
    u=f'https://cdli.earth/dl/photo/P{i:06d}.jpg'
    try:
        b=urllib.request.urlopen(u,timeout=90).read()
        im=Image.open(io.BytesIO(b)).convert('RGB'); im.thumbnail((800,800)); x=np.asarray(im)/255.0
        hsv=rgb2hsv(x); m=(hsv[...,2]>0.16)&(hsv[...,1]<0.75)   # tablet pixels: not background, not colour chart
        if m.sum()<2000: return dict(artifact_id=i,ok=False)
        lab=rgb2lab(x)[m]; L,A,B=np.median(lab,axis=0)
        return dict(artifact_id=i,ok=True,L=L,a=A,b=B,chroma=np.hypot(A,B),hue=np.degrees(np.arctan2(B,A)),
                    L_iqr=np.subtract(*np.percentile(lab[:,0],[75,25])),px=int(m.sum()),w=x.shape[1],h=x.shape[0])
    except Exception as e: return dict(artifact_id=i,ok=False,err=str(e)[:80])
with cf.ThreadPoolExecutor(8) as ex: rows=list(ex.map(one,ids))
pd.DataFrame(rows).to_csv(out,index=False); print(out,sum(r.get('ok',False) for r in rows),'of',len(rows))
