"""Parse the Prosobab SQL dump (DANS doi:10.17026/DANS-ZVN-EECE, 2022-06-03) into CSVs."""
from _paths import WORK
import re,csv,io,pandas as pd,sys
D=WORK+'/prosobab'; s=open(f'{D}/prosobab.sql',encoding='utf-8').read()
def table(name):
    cols=re.findall(r"^\s+`(\w+)`",re.search(r"CREATE TABLE `%s` \((.*?)\n\)"%name,s,re.S).group(1),re.M)
    rows=[]
    for block in re.findall(r"INSERT INTO `%s` \(.*?\) VALUES\s*\n?(.*?);\n"%name,s,re.S):
        for line in re.split(r"\),\s*\n\(",block.strip()[1:-1]):
            r=next(csv.reader(io.StringIO(line),quotechar="'",escapechar='\\',skipinitialspace=True,doublequote=False))
            rows.append(r)
    return pd.DataFrame([r[:len(cols)] for r in rows],columns=cols)
for n in ['e_tablets','s_types','s_subtypes','s_localities','c_archives','x_mentionedsubtypesobjects','s_kings']:
    t=table(n); t.to_csv(f'{D}/{n}.csv',index=False); print(n,len(t))
