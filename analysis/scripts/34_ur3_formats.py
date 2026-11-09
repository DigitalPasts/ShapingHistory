"""Ur III tablet formats: province, reign, text type (tagged from CDLI ATF keywords) and size.
Catalogue dimensions (tablets only, h/w between 0.05 and 9). For each factor: share of variance in log h/w,
log height and log width explained (eta squared); medians and robust spread per group; between-province
spread of medians by reign; Gaussian-mixture clusters on (log height, log width) compared with the factors."""
from _paths import WORK
import re, numpy as np, pandas as pd
from sklearn.mixture import GaussianMixture
from sklearn.metrics import adjusted_mutual_info_score as ami
R=WORK; rng=np.random.default_rng(0)
m=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','period','height','width','thickness','provenience','dates','artifact_type','collections','seals','genres'],low_memory=False)
m=m[m.period.fillna('').str.startswith('Ur III')&m.artifact_type.fillna('').str.lower().str.contains('tablet')]
m['hw']=m.height/m.width; m=m[m.hw.between(0.05,9,inclusive='neither')].copy()
m['coll']=m.collections.fillna('?').str.split(';').str[0].str.strip()
# use the cleaned dimensions of script 38 (reversed entries corrected, archival documents only)
C=pd.read_csv(f'{R}/results/tablet_dims_clean.csv'); C=C[C.archival][['artifact_id','height','width','hw']]
m=m.drop(columns=['height','width','hw']).merge(C,on='artifact_id')
PROV={'Puzriš-Dagan':'Puzriš-Dagan','Umma':'Umma','Girsu':'Girsu','Ur (':'Ur','Nippur':'Nippur','Garšana':'Garšana','Irisagrig':'Irisagrig'}
def prov(s):
    s=str(s)
    if 'uncertain' in s.lower(): return 'unprovenanced'
    for k,v in PROV.items():
        if s.startswith(k): return v
    return 'other' if s!='nan' else 'unprovenanced'
m['province']=m.provenience.map(prov)
d=m.dates.fillna('')
m['reign']=d.str.extract(r'^(Šulgi|Amar-Suen|Šū-Suen|Ibbi-Suen)')[0]
m['year']=pd.to_numeric(d.str.extract(r'^(?:Šulgi|Amar-Suen|Šu-Suen|Ibbi-Suen)\.(\d+)')[0],errors='coerce')
m.loc[(m.reign=='Šulgi')&(m.year<=40),'reign']='Šulgi 1-40'; m.loc[(m.reign=='Šulgi')&(m.year>40),'reign']='Šulgi 41-48'
ids=set(m.artifact_id); txt={}; cur=None
for l in open(f'{R}/atf/cdliatf.atf',encoding='utf-8',errors='ignore'):
    if l.startswith('&P'):
        k=int(l[2:8]); cur=k if k in ids else None
        if cur: txt[cur]=[]
    elif cur and re.match(r"^\d+[\'’]*\.",l): txt[cur].append(l.split('.',1)[1].strip())
TYPES=[('balanced account',r'nig2-ka9'),('messenger text',r'(lu2-kin-gi4-a|kas4).*(ninda|kasz|i3)|(ninda|kasz).*(lu2-kin-gi4-a|kas4)'),
 ('labour',r'(gurusz|geme2).*u4 \d|u4 \d.*(gurusz|geme2)|a2 (lu2|gurusz|geme2)'),('delivery (mu-DU)',r'mu-ku\(x\)|mu-kux|mu-DU'),
 ('transfer (i-dab)',r'i3-dab5'),('expenditure (ba-zi)',r'(?<!ki )(?<!ugula )(?<!\{d\})\bba-zi\b(?![-\w])'),('receipt (šu ba-ti)',r'szu ba(-an)?-ti'),('offerings',r'sa2-du11|nig2-dab5')]
def ttype(i):
    if i not in txt: return np.nan
    t=' '.join(txt[i])
    for n,rx in TYPES:
        if re.search(rx,t): return n
    return 'other'
m['type']=m.artifact_id.map(ttype); m['nlines']=m.artifact_id.map(lambda i: len(txt.get(i,[])) or np.nan)
m['sealed']=m.seals.notna()
for c in ['hw','height','width']: m['l'+c]=np.log(m[c])
madlog=lambda v: np.median(np.abs(v-np.median(v)))
def eta2(df,f,y):
    g=df.dropna(subset=[f]); g=g[g.groupby(f)[f].transform('size')>=30]
    if g[f].nunique()<2: return np.nan
    return round(1-g.groupby(f)[y].transform(lambda v: v-v.mean()).var()/g[y].var(),3)
print('Ur III tablets with dims',len(m),'| with ATF',m.type.notna().sum(),'| with reign',m.reign.notna().sum())
E=pd.DataFrame([{**{'factor':f},**{y:eta2(m,f,y) for y in ['lhw','lheight','lwidth']}} for f in ['province','reign','type','sealed','coll']])
print('\nshare of variance explained\n',E.to_string(index=False)); E.to_csv(f'{R}/results/s4_ur3_eta2.csv',index=False)
out=[]
for f in ['province','reign','type']:
    for k,g in m.groupby(f):
        if len(g)<30: continue
        out.append(dict(factor=f,group=k,n=len(g),median_hw=round(g.hw.median(),3),share_landscape=round((g.hw<1).mean(),3),MAD=round(madlog(g.lhw),3),
            median_h=g.height.median(),median_w=g.width.median(),median_lines=g.nlines.median()))
G=pd.DataFrame(out); pd.set_option('display.width',220); print('\n',G.to_string(index=False)); G.to_csv(f'{R}/results/s4_ur3_groups.csv',index=False)
# convergence: provinces by reign
RO=['Šulgi 1-40','Šulgi 41-48','Amar-Suen','Šū-Suen','Ibbi-Suen']
pr=m[m.province.isin(['Umma','Girsu','Puzriš-Dagan','Ur','Nippur','Garšana','Irisagrig'])&m.reign.notna()]
C=pr.groupby(['reign','province']).agg(n=('hw','size'),median_hw=('hw','median'),MAD=('lhw',madlog)).reset_index(); C=C[C.n>=30]
C['reign']=pd.Categorical(C.reign,RO); C=C.sort_values(['reign','province']); print('\n',C.round(3).to_string(index=False)); C.to_csv(f'{R}/results/s4_ur3_reign_province.csv',index=False)
for r,g in C.groupby('reign',observed=True):
    print(r,'provinces',len(g),'spread of province medians (log, max-min)',round(np.log(g.median_hw).max()-np.log(g.median_hw).min(),3))
# within type x province: does province matter once type is fixed?
tp=m[m.type.notna()&m.province.isin(['Umma','Girsu','Puzriš-Dagan','Garšana','Irisagrig','Ur','Nippur'])]
T2=tp.groupby(['type','province']).agg(n=('hw','size'),median_hw=('hw','median'),median_w=('width','median'),median_h=('height','median')).reset_index()
print('\n',T2[T2.n>=30].round(3).to_string(index=False)); T2[T2.n>=30].to_csv(f'{R}/results/s4_ur3_type_province.csv',index=False)
print('eta2 province within type (lhw):',round(np.average([eta2(g,'province','lhw') for t,g in tp.groupby('type') if not np.isnan(eta2(g,'province','lhw'))]),3))
# clusters on size+shape
X=m[['lheight','lwidth']].values; Xs=X[rng.choice(len(X),min(len(X),15000),replace=False)]
bic={k:GaussianMixture(k,random_state=0,n_init=3).fit(Xs).bic(Xs) for k in range(1,9)}; k=min(bic,key=bic.get); print('\nBIC',{a:round(b) for a,b in bic.items()},'best k',k)
gm=GaussianMixture(k,random_state=0,n_init=3).fit(Xs); m['cluster']=gm.predict(X)
print(m.groupby('cluster').agg(n=('hw','size'),h=('height','median'),w=('width','median'),hw=('hw','median'),lines=('nlines','median')).round(2))
for f in ['province','type','reign']:
    g=m.dropna(subset=[f]); g=g[g[f]!='unprovenanced']; print('AMI cluster vs',f,round(ami(g.cluster,g[f]),3))
print(pd.crosstab(m.type,m.cluster,normalize='index').round(2))
m[['artifact_id','province','reign','year','type','nlines','height','width','hw','cluster']].to_csv(f'{R}/results/s4_ur3_tablets.csv',index=False)

# Girsu vs Umma by reign, within text type (weighted by the smaller cell), bootstrap CI
gu=m[m.province.isin(['Girsu','Umma'])&m.reign.notna()&m.type.notna()]
res=[]
for r in RO:
    g=gu[gu.reign==r]
    def diff(df):
        num=den=0
        for t,x in df.groupby('type'):
            a=x[x.province=='Girsu'].lhw; b=x[x.province=='Umma'].lhw
            if len(a)>=10 and len(b)>=10: w=min(len(a),len(b)); num+=w*(np.median(a)-np.median(b)); den+=w
        return num/den if den else np.nan
    est=diff(g); bs=[diff(g.sample(len(g),replace=True,random_state=i)) for i in range(200)]
    res.append(dict(reign=r,n=len(g),girsu_minus_umma_log=round(est,3),lo=round(np.nanpercentile(bs,2.5),3),hi=round(np.nanpercentile(bs,97.5),3)))
GU=pd.DataFrame(res); print('\nGirsu minus Umma, within type\n',GU.to_string(index=False)); GU.to_csv(f'{R}/results/s4_ur3_girsu_umma.csv',index=False)
