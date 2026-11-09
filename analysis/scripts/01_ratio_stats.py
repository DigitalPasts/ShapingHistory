"""Independent re-computation of h/w ratio statistics (physical = CDLI catalogue dims, pixel = Zenodo silhouettes)."""
from _paths import WORK
import re, numpy as np, pandas as pd
R=WORK
ORDER=['Uruk IV','Uruk III','Proto-Elamite','ED I-II','ED IIIa','ED IIIb','Ebla','Old Akkadian','Lagash II','Ur III',
 'Early Old Babylonian','Old Babylonian','Old Assyrian','Middle Assyrian','Middle Babylonian','Middle Elamite','Hittite',
 'Neo-Assyrian','Neo-Babylonian','Achaemenid','Hellenistic']
meta=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','period','genres','height','width','provenience'],low_memory=False)
meta['Period_Name']=meta['period'].str.extract(r'^([^\(]+?)\s*(?:\(|$)')[0].str.strip().replace({'Middle Hittite':'Hittite'})
g=meta['genres'].fillna('').str.lower()
meta['admin']=g.str.contains('administrative|account|list or inventory|label')
pix=pd.read_csv(f'{R}/zenodo/h_w_ratio_df_all.csv')
pix['artifact_id']=pix['tablet_p_id_CDLI'].str.lstrip('P').astype(int)
print('pixel rows',len(pix),'unique ids',pix.artifact_id.nunique())
pix=pix.merge(meta.drop(columns=['height','width']),on='artifact_id',how='left')
phys=meta.copy(); phys['hw_ratio']=phys.height/phys.width
phys=phys[phys.hw_ratio.between(0.05,9,inclusive='neither')]
def stats(df,label):
    rows=[]
    for p in ORDER:
        for sub,name in [(df,'all'),(df[df.admin==True],'admin')]:
            v=sub.loc[sub.Period_Name==p,'hw_ratio'].dropna().values
            if len(v)<5: continue
            q1,med,q3=np.percentile(v,[25,50,75]); lv=np.log(v)
            rows.append(dict(source=label,genre=name,period=p,n=len(v),median=round(med,3),IQR=round(q3-q1,3),
                CV=round(v.std(ddof=1)/v.mean(),3),rel_IQR=round((q3-q1)/med,3),
                MAD_log=round(np.median(np.abs(lv-np.median(lv))),3),share_portrait=round((v>1).mean(),3)))
    return pd.DataFrame(rows)
out=pd.concat([stats(phys,'physical'),stats(pix,'pixel')])
out.to_csv(f'{R}/results/ratio_stats_recomputed.csv',index=False)
pd.set_option('display.width',200); pd.set_option('display.max_rows',200)
print(out.to_string(index=False))
# overlap: how many pixel-corpus tablets also have physical dims
both=pix.merge(phys[['artifact_id','hw_ratio']].rename(columns={'hw_ratio':'phys'}),on='artifact_id')
print('pixel tablets with catalogue dims:',len(both),' spearman pixel vs phys:',round(both[['hw_ratio','phys']].corr('spearman').iloc[0,1],3))
print('Lagash II pixel sample provenience:',pix[pix.Period_Name=='Lagash II'].provenience.value_counts().head(5).to_dict())
