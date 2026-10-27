"""Each silhouette is a composite of six views in the CDLI 'fat cross' layout: top edge, obverse with the left and right
edges beside it, bottom edge, reverse.  The views are separated and described one by one.  Shape descriptors that a scholar could describe but not easily measure with a ruler, computed from the same
black-and-white silhouettes that the VAE encodes (Zenodo 10.5281/zenodo.12787746). Used as a middle tier between the
height-to-width ratio and the twelve VAE dimensions (script 57). Computed for the tablets of the three case studies."""
import pandas as pd, numpy as np, cv2, os, sys
from concurrent.futures import ProcessPoolExecutor
R='/home/user/repro'; IMG=f'{R}/zenodo/imgs/images_b_w_tablets'
def shape(m):
    ys,xs=np.nonzero(m); y,x,h,w=ys.min(),xs.min(),ys.max()-ys.min()+1,xs.max()-xs.min()+1; area=m.sum()
    cs,_=cv2.findContours(m.astype(np.uint8),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); c=max(cs,key=cv2.contourArea)
    hull=cv2.convexHull(c); per=cv2.arcLength(c,True)
    b=m[y:y+h,x:x+w].astype(bool); q=max(2,int(0.15*min(h,w)))
    corners=np.mean([b[:q,:q].mean(),b[:q,-q:].mean(),b[-q:,:q].mean(),b[-q:,-q:].mean()])
    rows=b.sum(1); cols=b.sum(0); t=max(1,int(0.1*h)); s=max(1,int(0.1*w))
    return dict(hw=h/w,w=w,h=h,area=area,rect=area/(w*h),solidity=area/max(cv2.contourArea(hull),1),circ=4*np.pi*area/per**2,corner_fill=corners,
                taper=rows[:t].mean()/max(rows[-t:].mean(),1),
                side_bulge=rows[int(.45*h):int(.55*h)+1].mean()/max(np.r_[rows[t:2*t],rows[-2*t:-t]].mean(),1),
                end_bulge=cols[int(.45*w):int(.55*w)+1].mean()/max(np.r_[cols[s:2*s],cols[-2*s:-s]].mean(),1))
def feats(pid):
    f=f'{IMG}/{pid:06d}.png'
    if not os.path.exists(f): return None
    a=cv2.imread(f,0)>127
    if a.mean()>0.5: a=~a
    n,lab,st,cen=cv2.connectedComponentsWithStats(a.astype(np.uint8))
    comp=sorted([i for i in range(1,n) if st[i,4]>0.02*st[1:,4].max()],key=lambda i:-st[i,4])[:6]
    if len(comp)<4: return None
    rev=max(comp[:2],key=lambda i:cen[i,1]); obv=min(comp[:2],key=lambda i:cen[i,1])
    ox,oy,ow,oh=st[obv,:4]; colx=cen[obv,0]
    sides=[i for i in comp if i not in (obv,rev) and abs(cen[i,0]-colx)>ow/2]
    tops=[i for i in comp if i not in (obv,rev) and abs(cen[i,0]-colx)<=ow/2]
    O=shape(lab==obv); Rv=shape(lab==rev)
    d=dict(id=pid,**{k:O[k] for k in ['hw','rect','solidity','circ','corner_fill','taper','side_bulge','end_bulge']})
    d['thick_side']=np.median([st[i,2] for i in sides])/ow if sides else np.nan     # thickness at the sides / width
    d['thick_end']=np.median([st[i,3] for i in tops])/ow if tops else np.nan        # thickness at top and bottom / width
    d['rev_obv']=Rv['area']/O['area']                                                 # reverse larger than obverse?
    d['rev_corner_fill']=Rv['corner_fill']
    return d
if __name__=='__main__':
    ids=sorted(set(int(i) for i in pd.read_csv(sys.argv[1]).id.dropna()))
    with ProcessPoolExecutor() as ex: out=[r for r in ex.map(feats,ids,chunksize=200) if r]
    pd.DataFrame(out).to_csv(f'{R}/results/silhouette_geometry.csv',index=False); print(len(out),'of',len(ids))
