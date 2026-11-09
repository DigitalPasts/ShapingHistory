"""Section 4 checks on the height-to-width ratio (physical dimensions from the CDLI catalogue, tablets only).
1 robust dispersion by period, raw and within museum, within museum x findspot, within damage tercile;
2 what drives the Neo-Babylonian CV (outliers);
3 bimodality (Hartigan dip test on log h/w) by period and overall;
4 'fixed balance': does h/w stay constant as tablets get bigger or carry more lines?
5 medians by region x period; 6 Middle Elamite provenience; 7 VAE axis vs chronology."""
from _paths import WORK
import re, numpy as np, pandas as pd, diptest
from scipy.stats import spearmanr
R=WORK; rng=np.random.default_rng(0)
ORDER=['Uruk IV','Uruk III','Proto-Elamite','ED I-II','ED IIIa','ED IIIb','Ebla','Old Akkadian','Lagash II','Ur III',
 'Early Old Babylonian','Old Babylonian','Old Assyrian','Middle Assyrian','Middle Babylonian','Middle Elamite','Hittite',
 'Neo-Assyrian','Neo-Babylonian','Achaemenid','Hellenistic']
MID={'Uruk IV':-3250,'Uruk III':-3100,'Proto-Elamite':-3000,'ED I-II':-2750,'ED IIIa':-2550,'ED IIIb':-2420,'Ebla':-2350,
 'Old Akkadian':-2250,'Lagash II':-2150,'Ur III':-2060,'Early Old Babylonian':-1950,'Old Babylonian':-1750,'Old Assyrian':-1850,
 'Middle Assyrian':-1250,'Middle Babylonian':-1250,'Middle Elamite':-1250,'Hittite':-1400,'Neo-Assyrian':-800,
 'Neo-Babylonian':-580,'Achaemenid':-430,'Hellenistic':-200}
m=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','period','genres','height','width','provenience','collections','artifact_type'],low_memory=False)
m=m[m.artifact_type.fillna('').str.lower().str.contains('tablet')]
m['P']=m.period.str.extract(r'^([^\(]+?)\s*(?:\(|$)')[0].str.strip().replace({'Middle Hittite':'Hittite'})
m['hw']=m.height/m.width; m=m[m.hw.between(0.05,9,inclusive='neither')&m.P.isin(ORDER)].copy()
m['lhw']=np.log(m.hw); m['coll']=m.collections.fillna('?').str.split(';').str[0].str.strip()
m['site']=m.provenience.fillna('?').str.replace(r'\s*\(.*','',regex=True).str.strip()
m['admin']=m.genres.fillna('').str.lower().str.contains('administrative')
dmg=pd.read_csv(f'{R}/results/damage_score.csv').rename(columns={'CDLI_id':'artifact_id'})[['artifact_id','damage']]
m=m.merge(dmg,on='artifact_id',how='left')
madlog=lambda v: np.median(np.abs(v-np.median(v)))
def within(g,key,minn=20):
    s=[(len(x),madlog(x.lhw.values)) for _,x in g.groupby(key) if len(x)>=minn]
    return np.average([b for a,b in s],weights=[a for a,b in s]) if s else np.nan
rows=[]
for p in ORDER:
    g=m[m.P==p]
    if len(g)<50: continue
    v=g.hw.values; lo,hi=np.percentile(v,[1,99]); t=v[(v>=lo)&(v<=hi)]
    gd=g[g.damage.notna()]
    if len(gd)>=60: gd=gd.assign(dt=pd.qcut(gd.damage,3,labels=False,duplicates='drop'))
    boot=[madlog(rng.choice(g.lhw.values,len(g))) for _ in range(300)]
    dip,pdip=diptest.diptest(g.lhw.values) if len(g)<=20000 else diptest.diptest(rng.choice(g.lhw.values,20000,replace=False))
    sz=np.log(np.sqrt(g.height*g.width))
    rows.append(dict(period=p,n=len(g),median=round(np.median(v),3),share_landscape=round((v<1).mean(),3),
        CV=round(v.std(ddof=1)/v.mean(),3),CV_trim1=round(t.std(ddof=1)/t.mean(),3),
        MAD_log=round(madlog(g.lhw.values),3),MAD_lo=round(np.percentile(boot,2.5),3),MAD_hi=round(np.percentile(boot,97.5),3),
        MAD_in_museum=round(within(g,'coll'),3),MAD_in_museum_site=round(within(g,['coll','site']),3),
        MAD_in_damage=round(within(gd,'dt'),3) if 'dt' in gd else np.nan,
        top_museum=g.coll.value_counts().index[0][:30],top_share=round(g.coll.value_counts(normalize=True).iloc[0],2),
        top_site=g.site.value_counts().index[0][:20],site_share=round(g.site.value_counts(normalize=True).iloc[0],2),
        dip=round(dip,4),dip_p=round(pdip,4),rho_hw_size=round(spearmanr(g.lhw,sz)[0],3)))
T=pd.DataFrame(rows); pd.set_option('display.width',250); pd.set_option('display.max_columns',30)
print(T.to_string(index=False)); T.to_csv(f'{R}/results/s4_hw_by_period.csv',index=False)
for k in ['MAD_log','MAD_in_museum','MAD_in_museum_site','MAD_in_damage','CV','CV_trim1']:
    print(k,'rank vs MAD_log rho',round(spearmanr(T.MAD_log,T[k],nan_policy='omit')[0],2))
# 2 NB outliers
nb=m[m.P=='Neo-Babylonian']; print('\nNB extremes hw>3 or <0.25:',((nb.hw>3)|(nb.hw<.25)).sum(),'of',len(nb))
print(nb.sort_values('hw').iloc[list(range(5))+list(range(-5,0))][['artifact_id','height','width','hw','coll']].to_string(index=False))
# 3 overall bimodality, 2nd vs 1st millennium
for lab,ps in [('all',ORDER),('3rd mill',ORDER[:10]),('1st mill',['Neo-Assyrian','Neo-Babylonian','Achaemenid','Hellenistic'])]:
    x=m[m.P.isin(ps)].lhw.values; x=rng.choice(x,min(len(x),20000),replace=False); print('dip',lab,diptest.diptest(x))
# 4 fixed balance with line counts
lines={}; cur=None
for l in open(f'{R}/atf/cdliatf.atf',encoding='utf-8',errors='ignore'):
    if l.startswith('&P'): cur=int(l[2:8]); lines[cur]=0
    elif cur is not None and re.match(r"^\d+[\'’]*\.",l): lines[cur]+=1
L=pd.Series(lines,name='nlines').rename_axis('artifact_id').reset_index()
ml=m.merge(L,on='artifact_id'); ml=ml[ml.nlines>0]; ml['sz']=np.log(np.sqrt(ml.height*ml.width))
fb=[]
for p in ORDER:
    g=ml[ml.P==p]
    if len(g)<100: continue
    fb.append(dict(period=p,n=len(g),rho_lines_size=round(spearmanr(np.log(g.nlines),g.sz)[0],2),
        rho_lines_hw=round(spearmanr(np.log(g.nlines),g.lhw)[0],2),rho_size_hw=round(spearmanr(g.sz,g.lhw)[0],2),
        med_hw_small=round(g[g.sz<=g.sz.quantile(.25)].hw.median(),2),med_hw_large=round(g[g.sz>=g.sz.quantile(.75)].hw.median(),2)))
FB=pd.DataFrame(fb); print('\n',FB.to_string(index=False)); FB.to_csv(f'{R}/results/s4_fixed_balance.csv',index=False)
# 5 regions
REG={'Babylonia':['Nippur','Ur','Uruk','Larsa','Sippar','Babylon','Umma','Girsu','Puzris','Drehem','Kish','Isin','Adab','Lagash','Borsippa','Dilbat','Kutha','Shuruppak','Tell ed-Der','Nerebtum','Ishchali','Eshnunna','Tutub','Marad','Kisurra','Garshana','Irisagrig','Ešnunna','Me-Turan','Zabalam'],
 'Assyria':['Assur','Nineveh','Kalhu','Nimrud','Dur-Katlimmu','Dur-Sharrukin','Tell Billa','Tell al-Rimah','Shibaniba','Tarbisu','Harran','Guzana','Tell Sheikh Hamad','Imgur-Enlil'],
 'Elam / Iran':['Susa','Anshan','Persepolis','Haft Tepe','Choga Zanbil','Malyan','Tepe Yahya','Kabnak','Chogha'],
 'Syria / Anatolia':['Kanesh','Hattusa','Ebla','Mari','Emar','Ugarit','Alalakh','Tuttul','Shubat-Enlil','Terqa','Qatna','Tell Leilan','Ekalte','Amarna','Akhetaten','Nuzi','Arrapha','Kurruhanni']}
def reg(s):
    for r,ks in REG.items():
        if any(k.lower() in s.lower() for k in ks): return r
    return 'other/unprovenanced'
m['region']=m.site.map(reg)
RG=m.groupby(['P','region']).hw.agg(n='size',median='median').reset_index(); RG=RG[RG.n>=30]
RG['P']=pd.Categorical(RG.P,ORDER); RG=RG.sort_values(['P','region'])
print('\n',RG.round(3).to_string(index=False)); RG.to_csv(f'{R}/results/s4_region_period.csv',index=False)
# 6 Middle Elamite
me=m[m.P=='Middle Elamite']; print('\nME sites',me.site.value_counts().head(6).to_dict(),'\nME museums',me.coll.value_counts().head(4).to_dict())
print(me.groupby('site').hw.agg(['size','median']).query('size>=10'))
# 7 VAE axes vs chronology (photographed tablets)
F=pd.read_csv(f'{R}/results/tablet_latent_damage_adjusted.csv'); F=F[F.Period_Name.isin(MID)]
t=F.Period_Name.map(MID)
for z in [f'Z{i}' for i in range(1,13)]:
    r=spearmanr(t,F[z])[0]; pm=F.groupby('Period_Name')[z].median(); rp=spearmanr([MID[k] for k in pm.index],pm.values)
    print(z,'tablet-level rho',round(r,3),'| period-median rho',round(rp[0],3),'p',round(rp[1],4))
