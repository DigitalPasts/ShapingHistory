"""Cleaned catalogue dimensions for Section 4.
1 Tablets only (CDLI artifact_type contains 'tablet'), height and width given.
2 Checked against the photograph (Zenodo silhouette h/w) where one exists: if the catalogue ratio is close to the
  inverse of the photo ratio (|log cat + log photo| < 0.1) while the tablet is clearly not square (|log photo| > 0.15),
  height and width were entered the other way round, and are swapped.
3 Ratios beyond 3 or below 1/3 that the photograph does not explain are dropped (mostly de Liagre Böhl Collection entries).
4 Neo-Assyrian: catalogue and photograph disagree before correction (Spearman 0.00), so only photo-checked tablets are kept.
5 'archival' = administrative, legal, letters, contracts, receipts and accounts, not school texts; the rest
  (literary, lexical, mathematical, scholarly, royal, unknown) is kept but flagged.
Output: results/tablet_dims_clean.csv and a log of what changed per period."""
from _paths import WORK
import numpy as np, pandas as pd
from scipy.stats import spearmanr
R=WORK
m=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','period','genres','height','width','artifact_type','is_school_text','provenience','collections'],low_memory=False)
m=m[m.artifact_type.fillna('').str.lower().str.contains('tablet')&(m.height>0)&(m.width>0)].copy()
m['P']=m.period.str.extract(r'^([^\(]+?)\s*(?:\(|$)')[0].str.strip().replace({'Middle Hittite':'Hittite'})
pix=pd.read_csv(f'{R}/zenodo/h_w_ratio_df_all.csv'); pix['artifact_id']=pix.tablet_p_id_CDLI.str.lstrip('P').astype(int)
pix=pix.groupby('artifact_id').hw_ratio.mean().rename('photo_hw').reset_index()
m=m.merge(pix,on='artifact_id',how='left')
m['cat_hw']=m.height/m.width
inv=m.photo_hw.notna()&(np.abs(np.log(m.cat_hw)+np.log(m.photo_hw))<0.1)&(np.abs(np.log(m.photo_hw))>0.15)
m['swapped']=inv
m.loc[inv,['height','width']]=m.loc[inv,['width','height']].values
m['hw']=m.height/m.width
m['dropped']=(m.hw>3)|(m.hw<1/3)
na=m.P=='Neo-Assyrian'; m.loc[na&m.photo_hw.isna(),'dropped']=True
g=m.genres.fillna('').str.split(';').str[0].str.strip()
m['archival']=g.isin(['Administrative','Letter','Legal','Business / Contracts','Receipt','Account'])&(m.is_school_text.fillna(0).astype(float)==0)
m['genre1']=g.replace('','unknown')
log=[]
for p,x in m.groupby('P'):
    b=x[x.photo_hw.notna()&~x.dropped]
    log.append(dict(period=p,n=len(x),swapped=int(x.swapped.sum()),dropped=int(x.dropped.sum()),archival_share=round(x.archival.mean(),3),
        rho_before=round(spearmanr(x[x.photo_hw.notna()].cat_hw,x[x.photo_hw.notna()].photo_hw)[0],3) if x.photo_hw.notna().sum()>20 else np.nan,
        rho_after=round(spearmanr(b.hw,b.photo_hw)[0],3) if len(b)>20 else np.nan))
L=pd.DataFrame(log).sort_values('n',ascending=False); print(L.head(25).to_string(index=False)); L.to_csv(f'{R}/results/s4_cleaning_log.csv',index=False)
c=m[~m.dropped]; print('kept',len(c),'swapped',int(c.swapped.sum()),'dropped',int(m.dropped.sum()))
c[['artifact_id','P','provenience','collections','genre1','archival','height','width','hw','photo_hw','swapped']].to_csv(f'{R}/results/tablet_dims_clean.csv',index=False)
