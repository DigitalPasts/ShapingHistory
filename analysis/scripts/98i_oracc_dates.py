"""Oracc catalogues as packaged for the oracc-parser package (Romach, Spencer and Gordin 2026, Zenodo doi 10.5281/zenodo.20625379,
catalogues.zip: the original Oracc metadata of all 138 projects as CSV; ShG 9 Nov 2026). Cross-check: our own download of 7 projects
(oracc_catalogues.py run on ShG's MacBook Air, 9 Nov 2026).
dates and archives for our photographed tablets, matched by CDLI P-number (= Oracc id_text).
Dated = a king in date_of_origin (e.g. 'Esarhaddon.000.00.00'), an eponym, a generated year (date_gen) or a Seleucid/
Arsacid date (hbtin dates_referenced 'HE.SE...'). Output: oracc/oracc_matched.csv"""
from _paths import WORK
import pandas as pd, re
R=WORK
import glob, os
parts=[pd.read_csv(f,dtype=str,low_memory=False).assign(oracc_project=os.path.basename(f)[:-4].replace('-','/')) for f in sorted(glob.glob(f'{R}/oracc/parser/cat/*.csv'))]
O=pd.concat(parts,ignore_index=True).assign(source='oracc-parser Zenodo 2026')
L=f'{R}/oracc/oracc_catalogues.csv'   # live download of 9 Nov 2026 (7 projects); adds texts dated since the Zenodo snapshot
if os.path.exists(L): O=pd.concat([O,pd.read_csv(L,dtype=str,low_memory=False).assign(source='Oracc live 9 Nov 2026')],ignore_index=True)
for c in ['eponym','date_gen','dates_referenced','date_of_origin','archive','date_bce']:
    if c not in O: O[c]=None
O['id']=pd.to_numeric(O.id_text.str.extract(r'^P(\d{6})$')[0],errors='coerce'); O=O.dropna(subset=['id']).astype({'id':int})
O['proj']=O.oracc_project.str.split('/').str[0]; O=O.rename(columns={'period':'o_period','site':'o_site'})
k=O.date_of_origin.fillna('').str.split('.').str[0].str.strip()
O['o_king']=k.where(~k.isin(['','00','Broken','nd','[','NB','HE','AE','Sel']) & ~k.str.contains('<king>'))
O['o_dated']=O.o_king.notna()|O.eponym.notna()|O.date_gen.fillna('').str.match(r'^\d{3}')|O.dates_referenced.fillna('').str.match(r'^(HE|AE)\.(SE|AE|AR)\.\d')|O.date_bce.fillna('').str.match(r'^-?\d{3}')
d=pd.read_parquet(f'{R}/master_tablets.parquet')[['id','period','site']]
M=O.merge(d,on='id'); M=M.sort_values('o_dated',ascending=False).drop_duplicates('id')
keep=['source','id','period','site','oracc_project','date_bce','designation','o_king','eponym','date_gen','dates_referenced','o_dated','archive','provenience','genre','subgenre']
M[keep].to_csv(f'{R}/oracc/oracc_matched.csv',index=False)
print('matched',len(M),M.source.value_counts().to_dict()); print(M.groupby('period').agg(n=('id','size'),dated=('o_dated','sum'),archive=('archive','count')).sort_values('n',ascending=False).head(8).to_string())
print('MA archives:',M[M.period=='Middle Assyrian'].archive.value_counts().head(8).to_dict())
