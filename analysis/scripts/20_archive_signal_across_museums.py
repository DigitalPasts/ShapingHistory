"""Is an Old Babylonian archive recognisable in tablet shape ACROSS museums?
For each Archibab archive held in >=2 museums (>=8 tablets each in >=2 museums): mean cross-museum distance between
archive tablets (in different museums) vs. the same with archive labels permuted within museum x Archibab-type strata
among all Archibab-linked OB tablets. Statistic < permuted => the archive's tablets resemble each other across museums
more than other tablets of the same museums and text types do. Features: damage-adjusted VAE codes (script 15)."""
from _paths import WORK
import pandas as pd, numpy as np, sys
from scipy.spatial.distance import cdist
R=WORK; rng=np.random.default_rng(0)
FEAT=sys.argv[1] if len(sys.argv)>1 else f'{R}/results/tablet_latent_damage_adjusted.csv'
M=pd.read_csv(f'{R}/results/archibab_cdli_match.csv'); M['coll']=M.collections.fillna('?').str.split(';').str[0].str.strip()
F=pd.read_csv(FEAT); Z=[c for c in F.columns if c.startswith('Z')]
D=M.drop_duplicates('CDLI_id').merge(F[['CDLI_id']+Z],on='CDLI_id')
D['type']=D.type.fillna('?'); D['arch']=D.archives.fillna('')
D['stratum']=D.coll+'|'+D.type
X=D[Z].values
def stat(lab,a):
    idx=np.where(lab==a)[0]; co=D.coll.values[idx]
    d=cdist(X[idx],X[idx]); cross=co[:,None]!=co[None,:]
    return d[cross].mean() if cross.any() else np.nan
rows=[]
for a,g in D[D.arch!=''].groupby('arch'):
    vc=g.coll.value_counts()
    if (vc>=8).sum()<2: continue
    obs=stat(D.arch.values,a); perm=[]
    for _ in range(1000):
        lab=D.arch.values.copy()
        for s,ix in D.groupby('stratum').indices.items():   # shuffle archive labels within museum x type
            lab[ix]=rng.permutation(lab[ix])
        perm.append(stat(lab,a))
    perm=np.array(perm); perm=perm[~np.isnan(perm)]
    rows.append(dict(archive=a,n=len(g),museums=dict(vc),types=dict(g.type.value_counts().head(3)),obs=obs,perm_mean=perm.mean(),
                     ratio=obs/perm.mean(),p=(np.sum(perm<=obs)+1)/(len(perm)+1)))
o=pd.DataFrame(rows); pd.set_option('display.width',250,'display.max_colwidth',90)
print(o.round(3).to_string(index=False)); o.to_csv(f'{R}/results/archive_signal_across_museums.csv',index=False)
