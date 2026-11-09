"""Do Old Babylonian document types keep their form whatever the length of the text?
Line counts come from CDLI's ATF transliterations (cdli-gh/data, cdliatf_unblocked.atf).
For each Archibab type: correlation of log line count with log h/w ratio and with each latent axis
(variance in shape explained by length, R2 from linear regression of the 12 codes on log lines),
and the label-signal ratio recomputed after removing length from the codes."""
from _paths import WORK
import pandas as pd, numpy as np, re, sys
from scipy.stats import spearmanr
from scipy.spatial.distance import cdist
R=WORK; rng=np.random.default_rng(0)
lines={}; cols={}; cur=None
for l in open(f'{R}/atf/cdliatf.atf',encoding='utf-8',errors='ignore'):
    if l.startswith('&P'): cur=int(l[2:8]); lines[cur]=0; cols[cur]=0
    elif cur is not None:
        if re.match(r"^\d+[\'’]*\.",l): lines[cur]+=1
        elif l.startswith('@column'): cols[cur]+=1
L=pd.DataFrame({'CDLI_id':list(lines),'nlines':list(lines.values()),'ncols':[cols[k] for k in lines]})
M=pd.read_csv(f'{R}/results/archibab_cdli_match.csv'); M['coll']=M.collections.fillna('?').str.split(';').str[0].str.strip()
F=pd.read_csv(f'{R}/results/tablet_latent_damage_adjusted.csv'); Z=[f'Z{i}' for i in range(1,13)]
H=pd.read_csv(f'{R}/zenodo/h_w_ratio_df_all.csv')
idc=[c for c in H.columns if 'id' in c.lower()][0]; rc=[c for c in H.columns if 'ratio' in c.lower()][0]
H=H.rename(columns={idc:'CDLI_id',rc:'hw'})[['CDLI_id','hw']]
H['CDLI_id']=H.CDLI_id.astype(str).str.extract(r'(\d+)').astype(int); H=H.groupby('CDLI_id').hw.mean().reset_index()
D=M.drop_duplicates('CDLI_id').merge(F[['CDLI_id','damage']+Z],on='CDLI_id').merge(L,on='CDLI_id').merge(H,on='CDLI_id',how='left')
D=D[(D.nlines>0)&D.type.notna()]; D['ll']=np.log(D.nlines)
print('tablets with transliteration:',len(D))
rows=[]
for ty,g in D.groupby('type'):
    if len(g)<40: continue
    A=np.c_[np.ones(len(g)),g.ll]; Y=g[Z].values
    res=Y-A@np.linalg.lstsq(A,Y,rcond=None)[0]; r2=1-res.var(0).sum()/Y.var(0).sum()
    rho=spearmanr(g.ll,np.log(g.hw),nan_policy='omit')[0] if g.hw.notna().sum()>20 else np.nan
    rows.append(dict(type=ty,n=len(g),median_lines=g.nlines.median(),iqr_lines=g.nlines.quantile(.75)-g.nlines.quantile(.25),
        cv_lines=g.nlines.std()/g.nlines.mean(),multicol=(g.ncols>1).mean(),rho_lines_hw=rho,R2_shape_on_length=r2))
o=pd.DataFrame(rows).sort_values('R2_shape_on_length'); pd.set_option('display.width',200)
print(o.round(3).to_string(index=False)); o.to_csv(f'{R}/results/ob_type_length.csv',index=False)
