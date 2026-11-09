"""Pilot 5 (point 9): did legal documents become more uniform, or converge between north and south, after Hammurabi
conquered Larsa (1763 BCE)?
Dates: Archibab absolute year where linked (script 19), else CDLI ruler and regnal year converted with the middle
chronology (accession years in ACC); tablets dated only by ruler are placed by the ruler's reign.
Regions: south = the former kingdom of Larsa (Larsa, Ur, Nippur, Isin, Kutalla, Uruk, Lagaba); north = the kingdom of
Babylon throughout (Sippar, Kish, Dilbat, Babylon). Pre = before 1763; post = 1763-1712 (Hammurabi 31 to the end of
Samsu-iluna; 'post_narrow' = 1763-1740, before the southern revolt).
Tests, separately for legal documents (Legal; Business/Contracts) and for letters and administrative documents:
 (1) difference-in-differences on log h/w (OLS, museum fixed effects, damage; HC1 errors);
 (2) uniformity: MAD of log h/w by region x phase (bootstrap CI);
 (3) convergence: distance between the south and north median VAE vectors, pre vs post, with a permutation test of phase.
"""
from _paths import SHARED, WORK
import pandas as pd, numpy as np, warnings; warnings.filterwarnings('ignore')
import statsmodels.formula.api as smf
R=WORK; rng=np.random.default_rng(3)
X=[f'X{i}' for i in range(1,13)]
d=pd.read_parquet(f'{R}/master_tablets.parquet')
ob=d[d.period.isin(['Old Babylonian','Early Old Babylonian'])&d.photo_hw.between(1/3,3)].copy()
M=pd.read_csv(SHARED+'/archibab_cdli_match.csv').drop_duplicates('CDLI_id')
M['bce']=M.date.str.extract(r':\s*(\d{4})\s*$').astype(float)
ob=ob.merge(M[['CDLI_id','bce','type']].rename(columns={'CDLI_id':'id'}),on='id',how='left')
ACC={'Sumu-la-El':1880,'Sabium':1844,'Apil-Sin':1830,'Sin-muballit':1812,'Hammurapi':1792,'Samsu-iluna':1749,'Abi-ešuḫ':1711,
     'Ammi-ditana':1683,'Ammi-saduqa':1646,'Samsu-ditana':1625,'Rim-Sin':1822,'Warad-Sin':1834,'Sin-iddinam':1849,'Gungunum':1932,'Sumu-el':1894,'Nur-Adad':1865}
REIGN={'Rim-Sin':(1822,1763),'Warad-Sin':(1834,1823),'Sin-iddinam':(1849,1843),'Sin-muballit':(1812,1793),'Apil-Sin':(1830,1813),
       'Sumu-el':(1894,1866),'Nur-Adad':(1865,1850),'Gungunum':(1932,1906),'Samsu-iluna':(1749,1712),'Abi-ešuḫ':(1711,1684),
       'Ammi-ditana':(1683,1647),'Ammi-saduqa':(1646,1626),'Samsu-ditana':(1625,1595)}
ob['bce_cdli']=ob.ruler.map(ACC)-(ob.ryear-1)
ob['bce_all']=ob.bce.fillna(ob.bce_cdli)
ob['phase']=np.select([ob.bce_all>1763,ob.bce_all.between(1712,1763)],['pre','post'],None)
for r,(a,b) in REIGN.items():
    m=ob.phase.isna()&ob.bce_all.isna()&ob.ruler.eq(r)
    ob.loc[m,'phase']='pre' if b>1763 else ('post' if a<=1763 and b>=1712 else None)
ob['narrow']=ob.phase.eq('pre')|(ob.phase.eq('post')&(ob.bce_all.isna()|(ob.bce_all>=1740)))
ob.loc[ob.phase.eq('post')&ob.bce_all.isna()&ob.ruler.eq('Samsu-iluna'),'narrow']=False
S={'Larsa','Ur','Nippur','Isin','Kutalla','Uruk','Lagaba'}; N={'Sippar-Yahrurum','Sippar-Amnanum','Sippar','Kish','Dilbat','Babylon'}
ob['region']=np.select([ob.site.isin(S),ob.site.isin(N)],['south','north'],None)
ob['grp']=np.select([ob.genre.isin(['Legal','Business / Contracts']),ob.genre.eq('Letter'),ob.genre.eq('Administrative')],['legal','letter','admin'],None)
ob=ob[ob.phase.notna()&ob.region.notna()&ob.grp.notna()].copy()
ob['lh']=np.log(ob.photo_hw); ob['south']=(ob.region=='south').astype(int); ob['post']=(ob.phase=='post').astype(int)
ob['damage']=ob.damage.fillna(ob.damage.median())
ob[['id','site','region','phase','narrow','grp','genre','type','ruler','ryear','bce_all','museum','photo_hw','damage']+X].to_csv(f'{R}/pilot5_hammurabi_tablets.csv',index=False)
def mad(x): return np.median(np.abs(x-np.median(x)))
out=[]
for grp in ['legal','letter','admin']:
    for win in ['post (1763-1712)','post_narrow (1763-1740)']:
        g=ob[(ob.grp==grp)&(ob.narrow if 'narrow' in win else True)]
        if g.groupby(['region','phase']).size().min()<10 if len(g.groupby(['region','phase']).size())==4 else True:
            out.append(dict(group=grp,window=win,note='a cell has <10 tablets',cells=g.groupby(['region','phase']).size().to_dict())); continue
        m=smf.ols('lh ~ south*post + C(museum) + damage',data=g).fit(cov_type='HC1')
        row=dict(group=grp,window=win,cells=g.groupby(['region','phase']).size().to_dict(),
                 DiD_loghw=round(m.params['south:post'],3),DiD_se=round(m.bse['south:post'],3),DiD_p=round(m.pvalues['south:post'],4))
        for (rg,ph),c in g.groupby(['region','phase']):
            bs=[mad(rng.choice(c.lh.values,len(c))) for _ in range(1000)]
            row[f'MAD_{rg}_{ph}']=f'{mad(c.lh.values):.3f} [{np.percentile(bs,2.5):.3f}-{np.percentile(bs,97.5):.3f}]'
            row[f'medHW_{rg}_{ph}']=round(float(np.exp(np.median(c.lh))),3)
        def gap(df):
            a=df[df.region=='south'][X].median(); b=df[df.region=='north'][X].median(); return float(np.linalg.norm(a-b))
        gpre=gap(g[g.phase=='pre']); gpost=gap(g[g.phase=='post']); obs=gpost-gpre; null=[]
        for _ in range(2000):
            h=g.copy(); h['phase']=h.groupby('region').phase.transform(lambda s: rng.permutation(s.values)); null.append(gap(h[h.phase=='post'])-gap(h[h.phase=='pre']))
        null=np.array(null)
        row.update(VAE_gap_pre=round(gpre,3),VAE_gap_post=round(gpost,3),VAE_gap_change=round(obs,3),p_perm_convergence=round((1+(null<=obs).sum())/2001,4))
        out.append(row)
O=pd.DataFrame(out); O.to_csv(f'{R}/pilot5_hammurabi.csv',index=False)
# document types (Archibab) for legal tablets: what changed?
T=ob[(ob.grp=='legal')&ob.type.notna()].groupby(['region','phase','type']).agg(n=('lh','size'),med_hw=('photo_hw','median')).reset_index()
T=T[T.n>=5]; T.to_csv(f'{R}/pilot5_hammurabi_types.csv',index=False)
if __name__=='__main__':
    pd.set_option('display.width',250); pd.set_option('display.max_colwidth',80)
    print(O.T.to_string()); print(T.to_string())
