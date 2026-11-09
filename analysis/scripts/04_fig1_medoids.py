"""Figure 1: the corpus seen whole. For each period (tablets only, n>=100), the tablet whose
z-scored 12-d VAE code lies nearest the period's coordinate-wise median, shown at true aspect ratio.
The median is computed on all tablets of the period; the example shown is the nearest tablet that is complete
and cleanly masked: not catalogued as fragmentary in CDLI, six separate views (fat-cross), obverse solidity >= 0.97,
and enclosed mask holes < 0.1% of its area (results/mask_quality.csv from 05_mask_quality.py); and its two
largest faces (obverse, reverse) each fill >= 80% of their bounding box with solidity >= 0.97, which rejects
broken pieces with a straight-looking outline (many uncatalogued Kuyunjik fragments)."""
from _paths import FIGS, WORK
from skimage.measure import label, regionprops
def faces_ok(i):
    im=np.array(Image.open(f'{WORK}/zenodo/imgs/images_b_w_tablets/{i:06d}.png').convert('L'))>127
    if im.mean()>0.5: im=~im
    r=sorted(regionprops(label(im)),key=lambda r:-r.area)[:2]
    return len(r)==2 and all(x.extent>=0.80 and x.solidity>=0.97 for x in r)
import pandas as pd, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
R=WORK; Z=f'{R}/zenodo'
d=pd.concat([pd.read_csv(f'{Z}/vae_encoding_df_April16_w_class_{s}.csv') for s in ['train','val','test']])
m=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','artifact_type','artifact_preservation'],low_memory=False)
mq=pd.read_csv(f'{R}/results/mask_quality.csv')
d=d.merge(m,left_on='CDLI_id',right_on='artifact_id')
d=d[d.artifact_type.isin(['tablet','tablet & envelope'])].merge(mq,on='CDLI_id').copy()
BROKEN=['fragment','50%','25%','75%','incomplete','fragmentary','broken']
d['clean']=(~d.artifact_preservation.fillna('').str.lower().isin(BROKEN))&(d.n_big_parts==6)&(d.main_solidity>=0.97)&(d.hole_frac<0.001)
X=[f'X{i}' for i in range(1,13)]; d[X]=(d[X]-d[X].mean())/d[X].std()
DATES={'Uruk III':'c. 3200–3000','Proto-Elamite':'c. 3100–2900','ED I-II':'c. 2900–2600','ED IIIa':'c. 2600–2500',
'ED IIIb':'c. 2500–2340','Ebla':'c. 2400–2300','Old Akkadian':'c. 2340–2200','Lagash II':'c. 2200–2100','Ur III':'2110–2003',
'Early Old Babylonian':'2003–1900','Old Babylonian':'1900–1600','Old Assyrian':'1950–1750','Middle Assyrian':'1400–1000',
'Middle Babylonian':'1400–1100','Middle Elamite':'1500–1100','Hittite':'1650–1180','Neo-Assyrian':'911–612',
'Neo-Babylonian':'626–539','Achaemenid':'539–330','Hellenistic':'330–30'}
rows=[]
for p in DATES:
    g=d[d.Period_Name==p]
    if len(g)<100: continue
    dist=np.linalg.norm(g[X].values-np.median(g[X].values,0),axis=1)
    c=g.assign(dist=dist)[g.clean].sort_values('dist').head(300)
    c=c[[faces_ok(int(j)) for j in c.CDLI_id]]
    rows.append((p,len(g),int(c.CDLI_id.iloc[0]),int((g.assign(dist=dist).dist<c.dist.iloc[0]).sum())))
pd.DataFrame(rows,columns=['period','n_tablets','example_cdli_id','n_closer_but_excluded']).to_csv(f'{R}/results/fig1_medoids.csv',index=False)
nc=6; nr=int(np.ceil(len(rows)/nc))
fig,ax=plt.subplots(nr,nc,figsize=(7.0,1.55*nr+0.1),dpi=300)
for a in ax.flat: a.axis('off')
for a,(p,n,i,_) in zip(ax.flat,rows):
    im=np.array(Image.open(f'{Z}/imgs/images_b_w_tablets/{i:06d}.png').convert('L'))
    fg=im>127 if (im>127).mean()<0.5 else im<=127          # foreground = minority pixels
    ys,xs=np.where(fg); c=fg[ys.min():ys.max()+1,xs.min():xs.max()+1]
    a.imshow(~c,cmap='gray',vmin=0,vmax=1,interpolation='antialiased')
    a.set_title(f'{p.replace("Early Old Babylonian","Early OB")}\n{DATES[p]} BCE · n={n:,}',fontsize=5.6,pad=2)
    a.text(0.5,-0.06,f'P{i:06d}',transform=a.transAxes,ha='center',va='top',fontsize=4.6,color='#555')
plt.tight_layout(pad=0.4,h_pad=1.1)
for ext in ['png','pdf']: plt.savefig(f'{FIGS}/fig1_period_medoids.{ext}')
print(rows)
