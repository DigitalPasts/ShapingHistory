"""Section 4 extras: Leiden dimension errors, width vs height growth with text length, density peaks of log h/w."""
from _paths import WORK
import re, numpy as np, pandas as pd
from scipy.stats import spearmanr, gaussian_kde
from scipy.signal import find_peaks
R=WORK
m=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','period','height','width','collections','artifact_type'],low_memory=False)
m=m[m.artifact_type.fillna('').str.lower().str.contains('tablet')]
m['P']=m.period.str.extract(r'^([^\(]+?)\s*(?:\(|$)')[0].str.strip()
m['hw']=m.height/m.width; m=m[m.hw.between(0.05,9,inclusive='neither')]
m['coll']=m.collections.fillna('?').str.split(';').str[0].str.strip()
print('tablets with dims, all periods:',len(m))
L=m[m.coll.str.startswith('de Liagre')]
print('Leiden tablets',len(L),'extreme (hw>3 or <1/3):',((L.hw>3)|(L.hw<1/3)).sum(),' periods',L.P.value_counts().head(3).to_dict())
o=m[~m.coll.str.startswith('de Liagre')]; print('extreme elsewhere:',((o.hw>3)|(o.hw<1/3)).sum(),'of',len(o))
nb=m[(m.P=='Neo-Babylonian')&~m.coll.str.startswith('de Liagre')]; v=nb.hw
print('NB without Leiden: n',len(v),'CV',round(v.std()/v.mean(),3),'MADlog',round(np.median(np.abs(np.log(v)-np.median(np.log(v)))),3))
lines={}; cur=None
for l in open(f'{R}/atf/cdliatf.atf',encoding='utf-8',errors='ignore'):
    if l.startswith('&P'): cur=int(l[2:8]); lines[cur]=0
    elif cur is not None and re.match(r"^\d+[\'’]*\.",l): lines[cur]+=1
ml=m.merge(pd.Series(lines,name='n').rename_axis('artifact_id').reset_index(),on='artifact_id'); ml=ml[ml.n>0]
rows=[]
for p,g in ml.groupby('P'):
    if len(g)<100: continue
    ll=np.log(g.n); rows.append(dict(period=p,n=len(g),rho_lines_height=round(spearmanr(ll,g.height)[0],2),rho_lines_width=round(spearmanr(ll,g.width)[0],2),
        width_q10_q90=f'{g.width.quantile(.1):.0f}-{g.width.quantile(.9):.0f}',height_q10_q90=f'{g.height.quantile(.1):.0f}-{g.height.quantile(.9):.0f}'))
W=pd.DataFrame(rows); print(W.to_string(index=False)); W.to_csv(f'{R}/results/s4_width_height_lines.csv',index=False)
print('NB/Ach/NA n with ATF lines:',ml.P.value_counts().reindex(['Neo-Babylonian','Achaemenid','Neo-Assyrian']).to_dict())
x=np.log(m.hw.values); x=x[np.abs(x)<1.2]; k=gaussian_kde(np.random.default_rng(0).choice(x,30000,replace=False),bw_method=0.08)
g=np.linspace(-1.2,1.2,601); d=k(g); pk,_=find_peaks(d,prominence=0.03)
print('density peaks at h/w:',np.round(np.exp(g[pk]),3),'heights',np.round(d[pk],2))
print('share within 2% of square:',round((np.abs(m.hw-1)<0.02).mean(),3))
