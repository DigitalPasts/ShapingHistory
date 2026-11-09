"""Per-tablet outline features of the two largest faces (obverse, reverse): solidity, extent, area ratio.
A broken tablet has an irregular (non-convex) outline; a complete one is close to convex."""
from _paths import WORK
import pandas as pd, numpy as np
from PIL import Image
from skimage.measure import regionprops, label
from concurrent.futures import ProcessPoolExecutor
Z=WORK+'/zenodo/imgs/images_b_w_tablets'
def f(i):
    try: im=np.array(Image.open(f'{Z}/{i:06d}.png').convert('L'))>127
    except Exception: return (i,)+(np.nan,)*5
    if im.mean()>0.5: im=~im
    r=sorted(regionprops(label(im)),key=lambda r:-r.area)[:2]
    if len(r)<2: r=r*2
    return (i,r[0].solidity,r[1].solidity,r[0].extent,r[1].extent,r[1].area/r[0].area)
if __name__=='__main__':
    ids=pd.read_csv(WORK+'/results/mask_quality.csv').CDLI_id.tolist()
    with ProcessPoolExecutor() as ex: rows=list(ex.map(f,ids,chunksize=200))
    pd.DataFrame(rows,columns=['CDLI_id','sol1','sol2','ext1','ext2','area_ratio']).to_csv(WORK+'/results/face_features.csv',index=False)
