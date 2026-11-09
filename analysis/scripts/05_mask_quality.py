"""Mask quality per tablet: number of large components, obverse solidity, enclosed-hole area.
Used to (a) quantify holes in the Zenodo masks and (b) pick complete, clean examples for Fig. 1."""
from _paths import WORK
import pandas as pd, numpy as np, sys
from PIL import Image
from scipy import ndimage as ndi
from skimage.measure import regionprops, label
from concurrent.futures import ProcessPoolExecutor
Z=WORK+'/zenodo/imgs/images_b_w_tablets'
def q(i):
    try: im=np.array(Image.open(f'{Z}/{i:06d}.png').convert('L'))>127
    except Exception: return (i,np.nan,np.nan,np.nan,np.nan)
    if im.mean()>0.5: im=~im
    lab=label(im); props=sorted(regionprops(lab),key=lambda r:-r.area)
    tot=im.sum(); big=[r for r in props if r.area>0.01*tot]
    filled=ndi.binary_fill_holes(im); hole=(filled&~im).sum()/max(tot,1)
    return (i,len(big),props[0].solidity if props else np.nan,hole,tot)
if __name__=='__main__':
    ids=pd.concat([pd.read_csv(f'{WORK}/zenodo/vae_encoding_df_April16_w_class_{s}.csv',usecols=['CDLI_id']) for s in ['train','val','test']]).CDLI_id.tolist()
    with ProcessPoolExecutor() as ex: rows=list(ex.map(q,ids,chunksize=200))
    d=pd.DataFrame(rows,columns=['CDLI_id','n_big_parts','main_solidity','hole_frac','fg_px'])
    d.to_csv(WORK+'/results/mask_quality.csv',index=False)
    print(d.describe().T)
    print('share with any enclosed hole >0.1% of tablet area:',(d.hole_frac>0.001).mean())
    print('share >1%:',(d.hole_frac>0.01).mean())
