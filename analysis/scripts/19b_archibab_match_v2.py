"""Link Archibab texts (full table, all 36,060 texts, saved 9 Nov 2026 by archibab_table_v2.py) to CDLI photographed OB tablets,
by museum number and by publication reference. Writes results/archibab_cdli_match.csv."""
from _paths import WORK
import pandas as pd, re
R=WORK
A=pd.read_csv(f'{R}/archibab/archibab_textes_v2.csv').drop_duplicates('id')
C=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','museum_no','designation','provenience','collections','genres'],low_memory=False)
L=pd.read_parquet(f'{R}/master_tablets.parquet',columns=['id','period']).rename(columns={'id':'CDLI_id','period':'Period_Name'})
C=C[C.artifact_id.isin(L[L.Period_Name.isin(['Old Babylonian','Early Old Babylonian'])].CDLI_id)]
MUS=re.compile(r'\b([A-Z][A-Za-z]{0,5})\.?\s?(\d{1,3}(?:[ ,]?\d{3})*|\d+)\b')
def mkeys(s):
    if not isinstance(s,str): return []
    out=[]
    for p,n in MUS.findall(s):
        n=re.sub(r'\D','',n).lstrip('0')
        if n and p not in ('A','M','S','T','N') or (p in ('A','M','N') and n): out.append(f'{p.upper()}{n}')
    return out
def pkey(s):
    if not isinstance(s,str): return None
    s=re.sub(r'\[.*?\]','',s).split(',')[0] if '[' in s else s
    m=re.match(r'\s*([A-Za-z][A-Za-z.]*)\s+(\d+)[ ,/]+(\d+)',s)
    return f'{m.group(1).upper().rstrip(".")}|{int(m.group(2))}|{int(m.group(3))}' if m else None
rows=[]
for _,a in A.iterrows():
    for k in mkeys(a.museum_no): rows.append((k,'museum',a.id))
    k=pkey(a.reference)
    if k: rows.append((k,'publication',a.id))
K=pd.DataFrame(rows,columns=['key','how','archibab_id']).drop_duplicates()
cr=[]
for _,c in C.iterrows():
    for k in mkeys(c.museum_no): cr.append((k,'museum',c.artifact_id))
    k=pkey(c.designation)
    if k: cr.append((k,'publication',c.artifact_id))
CK=pd.DataFrame(cr,columns=['key','how','CDLI_id']).drop_duplicates()
M=CK.merge(K,on=['key','how'])
amb=M.groupby('CDLI_id').archibab_id.nunique()
M=M[M.CDLI_id.isin(amb[amb==1].index)].drop_duplicates(['CDLI_id','archibab_id'])   # keep unambiguous links only
M=M.merge(A[['id','reference','museum_no','type','from_to','date','archives']].rename(columns={'id':'archibab_id','museum_no':'archibab_museum_no'}),on='archibab_id')
M=M.merge(C.rename(columns={'artifact_id':'CDLI_id'}),on='CDLI_id')
M.to_csv(f'{R}/results/archibab_cdli_match.csv',index=False)
print('photographed OB tablets',len(C),'| linked',M.CDLI_id.nunique(),'| by',M.groupby('how').CDLI_id.nunique().to_dict(),'| ambiguous dropped',(amb>1).sum())
print('with archive label',M.archives.notna().sum()); print(M.archives.value_counts().head(25).to_string())
print(M.sample(8,random_state=0)[['how','key','museum_no','designation','reference','archives']].to_string())
