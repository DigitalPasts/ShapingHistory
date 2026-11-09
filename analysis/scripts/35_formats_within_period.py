"""Formats inside a period: do size-and-shape groups follow document type, archive, city or reign?
Old Babylonian (Archibab labels) and Neo-Babylonian/Achaemenid (Prosobab labels), catalogue dimensions.
eta2 = share of variance in log h/w, log height, log width explained by each label (groups >= 15 tablets);
Gaussian-mixture clusters on (log height, log width) compared with labels (adjusted mutual information)."""
from _paths import WORK
import numpy as np, pandas as pd, re
from sklearn.mixture import GaussianMixture
from sklearn.metrics import adjusted_mutual_info_score as ami
R=WORK
m=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','height','width','artifact_type','period'],low_memory=False)
m=m[m.artifact_type.fillna('').str.lower().str.contains('tablet')]; m['hw']=m.height/m.width; m=m[m.hw.between(0.05,9,inclusive='neither')]
for c in ['hw','height','width']: m['l'+c]=np.log(m[c])
def eta2(df,f,y,minn=15):
    g=df.dropna(subset=[f]); g=g[g.groupby(f)[f].transform('size')>=minn]
    if g[f].nunique()<2: return np.nan
    return round(1-g.groupby(f)[y].transform(lambda v: v-v.mean()).var()/g[y].var(),3)
madlog=lambda v: np.median(np.abs(v-np.median(v)))
def run(df,labels,name):
    print(f'\n=== {name}: {len(df)} tablets with labels and dimensions')
    E=pd.DataFrame([{**{'label':f,'groups':(df[f].value_counts()>=15).sum()},**{y:eta2(df,f,y) for y in ['lhw','lheight','lwidth']}} for f in labels]); print(E.to_string(index=False))
    X=df[['lheight','lwidth']].values
    bic={k:GaussianMixture(k,random_state=0,n_init=3).fit(X).bic(X) for k in range(1,7)}; k=min(bic,key=bic.get)
    df=df.assign(cluster=GaussianMixture(k,random_state=0,n_init=3).fit(X).predict(X))
    print('clusters',k); print(df.groupby('cluster').agg(n=('hw','size'),h=('height','median'),w=('width','median'),hw=('hw','median')).round(2).to_string())
    for f in labels: g=df.dropna(subset=[f]); print('AMI',f,round(ami(g.cluster,g[f]),3))
    return E.assign(period=name)
# OB
A=pd.read_csv(f'{R}/results/archibab_cdli_match.csv').drop_duplicates('CDLI_id').rename(columns={'CDLI_id':'artifact_id'})
A['city']=A.from_to.fillna('').str.extract(r'→\s*([^°]+)')[0].str.strip()
A['reign']=A.date.fillna('').str.extract(r'/\s*([A-Za-zÀ-ž\-]+(?:-[a-z]+)*)')[0]
A['archive']=A.archives.fillna('').str.split(';').str[0].replace('',np.nan)
A['type']=A['type'].replace('',np.nan)
ob=m.merge(A[['artifact_id','type','city','reign','archive']],on='artifact_id')
o1=run(ob,['type','archive','city','reign'],'Old Babylonian (Archibab)')
T=ob.groupby('type').agg(n=('hw','size'),median_hw=('hw','median'),h=('height','median'),w=('width','median'),MAD=('lhw',madlog)).query('n>=20').sort_values('median_hw').round(3)
print(T.to_string()); T.to_csv(f'{R}/results/s4_ob_type_formats.csv')
# NB / Achaemenid
P=pd.read_csv(f'{R}/results/prosobab_cdli_match.csv').drop_duplicates('CDLI_id').rename(columns={'CDLI_id':'artifact_id'})
nb=m.merge(P[['artifact_id','Type','sub','arch','place']],on='artifact_id')
o2=run(nb,['sub','Type','arch','place'],'Neo-Babylonian/Achaemenid (Prosobab)')
T2=nb.groupby('sub').agg(n=('hw','size'),median_hw=('hw','median'),h=('height','median'),w=('width','median'),MAD=('lhw',madlog)).query('n>=15').sort_values('median_hw').round(3)
print(T2.to_string()); T2.to_csv(f'{R}/results/s4_nb_type_formats.csv')
u=pd.read_csv(f'{R}/results/s4_ur3_eta2.csv').assign(period='Ur III (ATF tags)')
pd.concat([o1,o2,u]).to_csv(f'{R}/results/s4_eta2_all.csv',index=False)
# Photographs: catalogue dimensions are too sparse for the linked sets, so use the photo h/w (all tablets, damage as control)
pix=pd.read_csv(f'{R}/zenodo/h_w_ratio_df_all.csv'); pix['artifact_id']=pix.tablet_p_id_CDLI.str.lstrip('P').astype(int)
pix=pix.groupby('artifact_id').hw_ratio.mean().rename('phw').reset_index()
dm=pd.read_csv(f'{R}/results/damage_score.csv').rename(columns={'CDLI_id':'artifact_id'})[['artifact_id','damage']]
def photo(df,labels,name):
    df=df.merge(pix,on='artifact_id').merge(dm,on='artifact_id',how='left'); df['l']=np.log(df.phw)
    df['dt']=pd.qcut(df.damage.rank(method='first'),3,labels=False)
    # residualise on damage tercile so damage acts as a control
    df['lr']=df.l-df.groupby('dt').l.transform('median')
    rows=[]
    for f in labels:
        g=df.dropna(subset=[f]); g=g[g.groupby(f)[f].transform('size')>=15]
        if g[f].nunique()<2: continue
        e=1-g.groupby(f).lr.transform(lambda v:v-v.mean()).var()/g.lr.var()
        null=[]
        rng=np.random.default_rng(1)
        for _ in range(200):
            s=g.assign(p=rng.permutation(g[f].values)); null.append(1-s.groupby('p').lr.transform(lambda v:v-v.mean()).var()/s.lr.var())
        rows.append(dict(period=name,label=f,n=len(g),groups=g[f].nunique(),eta2=round(e,3),null95=round(np.percentile(null,95),3),p=round((np.array(null)>=e).mean(),3)))
    print(pd.DataFrame(rows).to_string(index=False)); return pd.DataFrame(rows),df
A2=A.rename(columns={'artifact_id':'artifact_id'}); A2['type2']=A2['type']
p1,obp=photo(A2[['artifact_id','type','archive','city','reign']],['type','archive','city','reign'],'Old Babylonian')
P2=P[['artifact_id','Type','sub','arch','place']]
p2,nbp=photo(P2,['sub','Type','arch','place'],'Neo-Babylonian/Achaemenid')
T=obp.groupby('type').agg(n=('phw','size'),median_hw=('phw','median'),MAD=('l',madlog)).query('n>=25').sort_values('median_hw').round(3); print(T.to_string())
T2=nbp.groupby('sub').agg(n=('phw','size'),median_hw=('phw','median'),MAD=('l',madlog)).query('n>=15').sort_values('median_hw').round(3); print(T2.to_string())
pd.concat([p1,p2]).to_csv(f'{R}/results/s4_photo_eta2.csv',index=False); T.to_csv(f'{R}/results/s4_ob_type_formats.csv'); T2.to_csv(f'{R}/results/s4_nb_type_formats.csv')
