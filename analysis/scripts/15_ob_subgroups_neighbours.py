"""Which Old Babylonian sub-groups do later tablets resemble?
Damage-adjusted VAE codes (as in 06). For each non-OB tablet, take its k=25 nearest OB tablets; count the OB city
(and school-text flag) among them; compare with the OB base rate of that city in the same genre pool -> lift.
Pools: 'archival' (administrative, legal, letters) and 'scholarly' (literary, lexical, mathematical, divination, school texts).
Bootstrap over query tablets for 95% CIs."""
from _paths import WORK
import pandas as pd, numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.neighbors import NearestNeighbors
R=WORK; rng=np.random.default_rng(0)
d=pd.concat([pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_{s}.csv') for s in ['train','val','test']]).drop_duplicates('CDLI_id').reset_index(drop=True)
m=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','artifact_type','artifact_preservation','provenience','genres','is_school_text','dates','external_resources','external_resources_key','collections'],low_memory=False)
q=pd.read_csv(f'{R}/results/mask_quality.csv').merge(pd.read_csv(f'{R}/results/face_features.csv'),on='CDLI_id')
d=d.merge(m,left_on='CDLI_id',right_on='artifact_id').merge(q,on='CDLI_id')
d=d[d.artifact_type.isin(['tablet','tablet & envelope'])].reset_index(drop=True)
F=pd.DataFrame({'ext1':d.ext1,'ext2':d.ext2,'sol1':d.sol1,'sol2':d.sol2,'hole':np.log1p(100*d.hole_frac.clip(0,1)),'parts':(d.n_big_parts-6).abs().clip(0,6)}).fillna(0)
D=pd.get_dummies(d.Period_Name,prefix='p',dtype=float)
lab=d.artifact_preservation.fillna('').str.lower().map(lambda s: 0 if s in ('complete','nearly complete') else (1 if s=='fragment' else np.nan)); k=lab.notna().values
clf=LogisticRegression(max_iter=3000).fit(pd.concat([F,D],axis=1)[k],lab[k]); w=clf.coef_[0][:F.shape[1]]
d['damage']=1/(1+np.exp(-(F.values@w-(F.values@w).mean())))
X=[f'X{i}' for i in range(1,13)]; Z=(d[X]-d[X].mean())/d[X].std()
Zc=Z-Z.groupby(d.Period_Name).transform('mean'); dc=d.damage-d.groupby('Period_Name').damage.transform('mean')
lr=LinearRegression().fit(np.c_[dc,dc**2],Zc); Zadj=(Z-lr.predict(np.c_[dc,dc**2])).values
d['city']=d.provenience.fillna('uncertain').str.split(r' \(').str[0]
g=d.genres.fillna('')
d['pool']=np.where(g.str.contains('Literary|Lexical|Mathematical|Divination|Scientific|Liturg|Ritual|Incantation')|(d.is_school_text==1),'scholarly',
          np.where(g.str.contains('Administrative|Legal|Letter|Business'),'archival',None))
d['coll']=d.collections.fillna('?').str.split(';').str[0].str.strip()
d['archibab']=d.external_resources.fillna('').str.contains('ARCHIBAB')
d[['CDLI_id','Period_Name','city','pool','is_school_text','damage','archibab']].assign(**{f'Z{i+1}':Zadj[:,i] for i in range(12)}).to_csv(f'{R}/results/tablet_latent_damage_adjusted.csv',index=False)
OB=d.Period_Name=='Old Babylonian'
out=[]
for pool in ['archival','scholarly']:
    ob=d[OB&(d.pool==pool)&(d.city!='uncertain')]
    cities=ob.city.value_counts(); cities=cities[cities>=60].index; ob=ob[ob.city.isin(cities)]
    Q=d[(~OB)&(d.pool==pool)&(d.Period_Name!='other')]
    grp=Q.groupby(['Period_Name','city']).size(); grp=grp[grp>=30]
    cache={}
    def ref(c):   # c=None: all OB tablets; else only OB tablets held in OTHER museums than c (museum control)
        if c not in cache:
            o=ob if c is None else ob[ob.coll!=c]
            cache[c]=(NearestNeighbors(n_neighbors=25).fit(Zadj[o.index]),o.city.values,o.city.value_counts(normalize=True).reindex(cities).fillna(0).values)
        return cache[c]
    for mode in ['no museum control','museum control']:
        for (per,city),n in grp.items():
            qi=Q[(Q.Period_Name==per)&(Q.city==city)].index; sh=np.zeros((len(qi),len(cities))); bs=np.zeros_like(sh)
            for c in d.coll[qi].unique():
                sel=np.where(d.coll[qi].values==c)[0]; nn,oc,base=ref(None if mode.startswith('no') else c)
                _,ix=nn.kneighbors(Zadj[qi[sel]]); nc=oc[ix]
                sh[sel]=np.stack([(nc==ct).mean(1) for ct in cities],1); bs[sel]=base
            boot=[]
            for _ in range(300):
                r=rng.integers(0,len(qi),len(qi)); boot.append(sh[r].mean(0)/np.maximum(bs[r].mean(0),1e-9))
            boot=np.array(boot); lift=sh.mean(0)/np.maximum(bs.mean(0),1e-9)
            for j,ct in enumerate(cities):
                out.append(dict(mode=mode,pool=pool,period=per,city=city,n=n,ob_city=ct,share=sh[:,j].mean(),base=bs[:,j].mean(),
                                lift=lift[j],lo=np.quantile(boot[:,j],.025),hi=np.quantile(boot[:,j],.975)))
o=pd.DataFrame(out); o.to_csv(f'{R}/results/ob_subgroup_neighbours.csv',index=False)
pd.set_option('display.width',220)
for pool in ['archival','scholarly']:
    s=o[(o.pool==pool)&(o['mode']=='museum control')&(o.lo>1)&(o.share>=0.05)]
    print('\n==',pool,'(museum control; lift CI>1, share>=5%)'); print(s.sort_values(['period','lift'],ascending=[True,False])[['period','city','n','ob_city','share','base','lift','lo','hi']].round(2).to_string(index=False))
