"""ShG's note of 9 Nov 2026: Prosobab (Waerzeggers and Groß 2022, DANS doi:10.17026/dans-zvn-eece, dump of 3 June 2022)
for our Neo-Babylonian and Achaemenid tablets: archive, place of writing, king and year. Parses the MySQL dump
(tables e_tablets, s_kings, c_archives, s_localities) and matches by CDLI P-number, else by museum number.
Outputs: prosobab/prosobab_tablets.csv, prosobab/prosobab_matched.csv"""
from _paths import WORK
import re, pandas as pd
R=WORK; SQL=f'{R}/prosobab/prosobab-dump-2022-06-03.sql'
s=open(SQL,encoding='utf-8',errors='replace').read().replace('\r\n','\n')
def cols(t): return re.findall(r'^\s+`([^`]+)`',re.search(r'CREATE TABLE `%s` \((.*?)\n\)'%t,s,re.S).group(1),re.M)
def rows(t):
    out=[]
    for m in re.finditer(r'INSERT INTO `%s` (?:\([^)]*\) )?VALUES\s*(.*?);\s*\n'%t,s,re.S):
        v=m.group(1); i=0; row=[]; cur=''; inq=False; depth=0
        while i<len(v):
            c=v[i]
            if inq:
                if c=='\\': cur+=v[i+1]; i+=2; continue
                if c=="'": inq=False
                else: cur+=c
            elif c=="'": inq=True
            elif c=='(' and depth==0: depth=1; row=[]; cur=''
            elif c==',' and depth==1: row.append(cur.strip()); cur=''
            elif c==')' and depth==1: row.append(cur.strip()); out.append(row); depth=0; cur=''
            elif depth==1: cur+=c
            i+=1
    D=pd.DataFrame(out,columns=cols(t)); return D.replace({'NULL':None})
T=rows('e_tablets'); K=rows('s_kings'); A=rows('c_archives'); L=rows('s_localities')
T=T.merge(K[['KingID','King','Abbreviation']],on='KingID',how='left').merge(A[['ArchiveID','ArchiveName','Provenance']],on='ArchiveID',how='left')\
   .merge(L[['LocalityID','LocName']].rename(columns={'LocalityID':'PlaceOfWritingID','LocName':'place_of_writing'}),on='PlaceOfWritingID',how='left')
T['cdli_p']=T.CDLI_URL.str.extract(r'P(\d{6})')[0]
keep=['TabletID','MuseumNr','PublicationTablet','cdli_p','King','_Year','_Month','_Day','JulianDate','place_of_writing','ArchiveName','Provenance','TypeID','Status']
T[keep].to_csv(f'{R}/prosobab/prosobab_tablets.csv',index=False)
print('Prosobab tablets',len(T),'| with CDLI P',T.cdli_p.notna().sum(),'| with king',T.King.notna().sum())
mk=lambda x: (lambda m: f'{m.group(1).upper()}{m.group(2)}' if m else None)(re.match(r'\s*([A-Za-z]+)\.?\s*0*(\d+)',x)) if isinstance(x,str) else None
d=pd.read_parquet(f'{R}/master_tablets.parquet'); d=d[d.period.isin(['Neo-Babylonian','Achaemenid','Hellenistic'])][['id','period','site','museum_no','ruler','ryear']]
d['k']=d.museum_no.map(mk); T['k']=T.MuseumNr.map(mk)
a=d.merge(T[keep].assign(id=pd.to_numeric(T.cdli_p,errors='coerce')).dropna(subset=['id']).astype({'id':int}),on='id',how='inner').assign(how='CDLI P')
b=d[~d.id.isin(a.id)].merge(T[keep+['k']],on='k',how='inner').assign(how='museum no.')
amb=b.groupby('id').TabletID.nunique(); b=b[b.id.isin(amb[amb==1].index)]
M=pd.concat([a,b]).drop_duplicates('id'); M.to_csv(f'{R}/prosobab/prosobab_matched.csv',index=False)
cd=M.ruler.notna()&~M.ruler.isin(['--'])
print('our NB/Ach/Hell',len(d),'matched',len(M),M.how.value_counts().to_dict(),M.period.value_counts().to_dict())
print('gain king',int((~cd&M.King.notna()).sum()),'| archives',M.ArchiveName.value_counts().head(8).to_dict())
