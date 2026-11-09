"""Case C: the Eanna archive under the Neo-Babylonian and early Achaemenid kings. DigEanna records (NaBuCCo, script 48)
give date, text form, legal purpose and the project's own label for the format of each tablet; CDLI gives the photograph
proportion (zenodo h_w_ratio_df_all) and catalogue dimensions. Tests: does the project's format label agree with our
measurement; does the proportion change by reign within one text form; does it change within the work of one scribe;
and is there a break at Nebuchadnezzar's administrative reform of the 580s. Outputs in nabucco/."""
from _paths import WORK
import pandas as pd, numpy as np, re
from scipy.stats import mannwhitneyu, spearmanr
R=WORK
D=pd.read_csv(f'{R}/nabucco/digeanna_tablets.csv')
D['P']=D['CDLI P-Identifier'].astype(str).str.extract(r'(P\d{6})')[0]
K={'Kan':('Kandalānu',647),'Npl':('Nabopolassar',626),'Nbk':('Nebuchadnezzar II',605),'AM':('Amēl-Marduk',562),'Ner':('Neriglissar',560),
   'LM':('Lābāši-Marduk',556),'Nbn':('Nabonidus',556),'Cyr':('Cyrus',539),'Cam':('Cambyses',530),'Bar':('Bardiya',522),'Dar':('Darius I',522)}
def reign(s):
    m=re.match(r'^([^.\s]+)\.\s*(\d+|Acc)',str(s))
    if not m or m.group(1) not in K: return pd.Series([None,np.nan,np.nan])
    n,st=K[m.group(1)]; y=0 if m.group(2)=='Acc' else int(m.group(2))
    return pd.Series([n,st,y])
D[['reign','start','year']]=D['Date (year-month-day)'].apply(reign)
D['bce']=D.start-D.year
p=pd.read_csv(f'{R}/zenodo/h_w_ratio_df_all.csv'); p['P']=p.tablet_p_id_CDLI
D=D.merge(p[['P','hw_ratio']].drop_duplicates('P'),on='P',how='left')
cs=pd.read_csv(f'{R}/results/case_scan_tablets.csv',usecols=['artifact_id','hw','collections'],low_memory=False); cs['P']='P'+cs.artifact_id.astype(str).str.zfill(6)
D=D.merge(cs[['P','hw','collections']],on='P',how='left'); D['museum']=D.collections.fillna('').str.split(',').str[0]
D['ratio']=D.hw_ratio.fillna(D.hw); D['fmt']=D['Format of the tablet'].fillna('').str.strip().str.lower().str.split().str[0].fillna('')
D.to_csv(f'{R}/nabucco/digeanna_merged.csv',index=False)
print('records',len(D),'with P',D.P.notna().sum(),'with ratio',D.ratio.notna().sum(),'reign',D.reign.notna().sum(),'scribe',D.scribe.notna().sum())
print(D.fmt.value_counts().head(10))
print(D.groupby('fmt').ratio.agg(['size','count','median']).query('count>=5'))
order=[v[0] for v in K.values()]
r=D[D.reign.notna()]
T=r.groupby('reign').agg(n=('reign','size'),n_ratio=('ratio','count'),ratio=('ratio','median')).reindex(order).dropna(how='all')
for f in ['landscape','square','portrait']: T[f'share_{f}']=r.groupby('reign').fmt.apply(lambda x:(x==f).sum()/max((x!='').sum(),1)).reindex(T.index).round(2)
print(T.round(3).to_string()); T.to_csv(f'{R}/nabucco/eanna_by_reign.csv')
tf=r['Text Form'].value_counts().head(6).index
W=r[r['Text Form'].isin(tf)].groupby(['Text Form','reign']).ratio.agg(['count','median']).query('count>=8').unstack(0)
print(W.reindex(order).dropna(how='all').round(2).to_string()); W.to_csv(f'{R}/nabucco/eanna_by_reign_textform.csv')
nbk=r[r.reign=='Nebuchadnezzar II'].copy(); nbk['phase']=np.where(nbk.year<=20,'Nbk 1-20','Nbk 21-43')
print(nbk.groupby('phase').agg(n=('ratio','count'),ratio=('ratio','median'),landscape=('fmt',lambda x:(x=='landscape').mean())))
a,b=nbk[nbk.phase=='Nbk 1-20'].ratio.dropna(),nbk[nbk.phase=='Nbk 21-43'].ratio.dropna(); print('reform test p',mannwhitneyu(a,b).pvalue if len(a)>3 and len(b)>3 else None)
r['grp']=np.select([r.reign.isin(['Nabopolassar','Nebuchadnezzar II']),r.reign.isin(['Neriglissar','Nabonidus','Lābāši-Marduk','Amēl-Marduk']),r.reign.isin(['Cyrus','Cambyses','Darius I','Bardiya'])],['early','late NB','Achaemenid'],None)
S=r[r.scribe.notna()&r.ratio.notna()]
sc=S.groupby(['scribe','grp']).ratio.agg(['count','median']).unstack(1)
both=sc[(sc[('count','early')]>=3)&(sc[('count','late NB')]>=3)] if ('count','late NB') in sc.columns and ('count','early') in sc.columns else pd.DataFrame()
print('scribes active early and late:',len(both)); print(both.round(2).to_string())
sc.to_csv(f'{R}/nabucco/eanna_scribes.csv')
print(S.groupby('grp').scribe.nunique())
# --- timing of the change: notes (proportion) and lists (share labelled portrait by DigEanna), five-year bins
note=D[D['Text Form'].str.startswith('Note',na=False)&D.bce.notna()&D.ratio.notna()].copy(); note['bin']=(note.bce//5*5).astype(int)
lst=D[D['Text Form'].str.startswith('List',na=False)&D.bce.notna()&D.fmt.isin(['landscape','portrait'])].copy(); lst['bin']=(lst.bce//5*5).astype(int)
B=note.groupby('bin').ratio.agg(note_n='count',note_ratio='median').join(lst.groupby('bin').fmt.agg(list_n='size',list_portrait=lambda x:(x=='portrait').mean()),how='outer').sort_index(ascending=False)
B.round(3).to_csv(f'{R}/nabucco/eanna_by_5yr.csv'); print(B.round(2).to_string())
lr=D[D['Text Form'].str.startswith('List',na=False)&D.ratio.notna()].copy()
lr['domain']=lr['Transaction Type'].fillna('').str.extract(r'Domain \(Eanna\) ([A-Za-z ,()-]+?)(?: Formatting| Further|$)')[0].str.strip()
lr['grp']=np.where(lr.reign.isin(['Nabopolassar','Nebuchadnezzar II','Kandalānu']),'to Nbk','after Nbk')
Ld=lr.groupby(['domain','grp']).ratio.agg(['count','median']).unstack(1); Ld.round(2).to_csv(f'{R}/nabucco/eanna_lists_by_domain.csv'); print(Ld.round(2).to_string())
nb=note[note.reign.isin(['Nabopolassar','Nebuchadnezzar II'])].ratio; nl=note[note.reign.isin(['Nabonidus','Cyrus'])].ratio
print('notes Npl+Nbk vs Nbn+Cyr',nb.median(),nl.median(),len(nb),len(nl),mannwhitneyu(nb,nl).pvalue)
