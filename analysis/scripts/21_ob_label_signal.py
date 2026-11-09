"""Which Archibab labels does tablet shape carry within Old Babylonian, beyond museum?
For a label (date bin, writing site, text type, archive), each group with >=8 tablets in >=2 museums:
mean distance between same-label tablets held in DIFFERENT museums, vs the same with labels permuted within
strata (museum x other labels). Ratio < 1 (low p) = shape carries that label across museums.
Usage: python 21_ob_label_signal.py [features.csv with CDLI_id + Z* columns]"""
from _paths import WORK
import pandas as pd, numpy as np, sys, re
from scipy.spatial.distance import cdist
R=WORK; rng=np.random.default_rng(0)
FEAT=sys.argv[1] if len(sys.argv)>1 else f'{R}/results/tablet_latent_damage_adjusted.csv'
M=pd.read_csv(f'{R}/results/archibab_cdli_match.csv'); M['coll']=M.collections.fillna('?').str.split(';').str[0].str.strip()
F=pd.read_csv(FEAT); Z=[c for c in F.columns if re.fullmatch(r'Z\d+|e\d+|X\d+',c)]
D=M.drop_duplicates('CDLI_id').merge(F[['CDLI_id']+Z],on='CDLI_id').reset_index(drop=True)
D['year']=D.date.str.extract(r':\s*(\d{4})\s*$').astype(float)
D['date_bin']=pd.cut(D.year,[0,1810,1750,1500][::-1] if False else [1500,1749,1792,1810,2100],labels=['after Hammurabi (<1750)','Hammurabi (1792-1750)','Rim-Sin/Sin-muballit (1810-1793)','before 1810']).astype(str).replace('nan','')
D['wsite']=D.from_to.fillna('').str.split('→').str[0].str.replace('°','').str.replace(r'\s*\(royaume de\s*–\)','',regex=True).str.strip()
D['fsite']=D.from_to.fillna('').str.split('→').str[-1].str.replace('°','').str.replace(r'\s*\(royaume de\s*–\)','',regex=True).str.strip()
D['type']=D.type.fillna(''); D['arch']=D.archives.fillna('')
X=D[Z].values; co=D.coll.values
def stat(lab,a):
    idx=np.where(lab==a)[0]; c=co[idx]; cross=c[:,None]!=c[None,:]
    return cdist(X[idx],X[idx])[cross].mean() if cross.any() else np.nan
TESTS={'date_bin':['coll','type','fsite'],'fsite':['coll','type','date_bin'],'type':['coll','fsite'],'arch':['coll','type']}
rows=[]
for lab,strat in TESTS.items():
    st=D[strat].fillna('').astype(str).agg('|'.join,axis=1); groups=st.groupby(st).groups
    for a,g in D[D[lab]!=''].groupby(lab):
        vc=g.coll.value_counts()
        if (vc>=8).sum()<2: continue
        obs=stat(D[lab].values,a); perm=[]
        for _ in range(500):
            l=D[lab].values.copy()
            for ix in groups.values(): ix=np.asarray(ix); l[ix]=rng.permutation(l[ix])
            perm.append(stat(l,a))
        perm=np.array(perm,dtype=float); perm=perm[~np.isnan(perm)]
        rows.append(dict(label=lab,group=a,n=len(g),n_museums=int((vc>=8).sum()),obs=obs,perm=perm.mean(),ratio=obs/perm.mean(),p=(np.sum(perm<=obs)+1)/(len(perm)+1)))
o=pd.DataFrame(rows); pd.set_option('display.width',200)
print(o.round(3).to_string(index=False)); o.to_csv(f'{R}/results/ob_label_signal.csv',index=False)
