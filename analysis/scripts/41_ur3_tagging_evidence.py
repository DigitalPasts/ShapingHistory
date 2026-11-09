"""SI evidence for the Ur III text types: for every measured archival Ur III tablet, the type used in Section 4,
its source (BDTNS label or transliteration keyword), and the transliteration line that triggered the keyword,
so any reader can check the tagging. Also a fixed random sample (seed 0) of 10 tablets per keyword type for hand checking."""
from _paths import WORK
import re, numpy as np, pandas as pd
R=WORK
U=pd.read_csv(f'{R}/results/s4_ur3_tablets_bdtns.csv')
TYPES=[('balanced account',r'nig2-ka9'),('messenger text',r'(lu2-kin-gi4-a|kas4).*(ninda|kasz|i3)|(ninda|kasz).*(lu2-kin-gi4-a|kas4)'),
 ('labour',r'(gurusz|geme2).*u4 \d|u4 \d.*(gurusz|geme2)|a2 (lu2|gurusz|geme2)'),('delivery (mu-DU)',r'mu-ku\(x\)|mu-kux|mu-DU'),
 ('transfer (i-dab)',r'i3-dab5'),('expenditure (ba-zi)',r'(?<!ki )(?<!ugula )(?<!\{d\})\bba-zi\b(?![-\w])'),('receipt (šu ba-ti)',r'szu ba(-an)?-ti'),('offerings',r'sa2-du11|nig2-dab5')]
ids=set(U.artifact_id); txt={}; cur=None
for l in open(f'{R}/atf/cdliatf.atf',encoding='utf-8',errors='ignore'):
    if l.startswith('&P'):
        k=int(l[2:8]); cur=k if k in ids else None
        if cur: txt[cur]=[]
    elif cur and re.match(r"^\d+[\'’]*\.",l): txt[cur].append(l.strip())
def hit(i,ty):
    rx=dict(TYPES).get(ty)
    if not rx or i not in txt: return ''
    L=txt[i]
    for a in L:
        if re.search(rx,a.split('.',1)[1]): return a
    j=' | '.join(L)   # pattern spans two lines (messenger texts, labour)
    return j[:200]
KEEP=['delivery (mu-DU)','transfer (i-dab)','expenditure (ba-zi)','receipt (šu ba-ti)','balanced account']
BL=['Messenger Text','Letter-order','Loan Document','Sale Document','Legal Text: court record','Legal Text: other']
def comb(r):
    if isinstance(r.bdtns,str):
        for L in BL:
            if L in r.bdtns: return L,'BDTNS'
    return (r.type,'keyword') if r.type in KEEP else ('other','none')
U[['type_used','source']]=U.apply(lambda r: pd.Series(comb(r)),axis=1)
U['matched_line']=[hit(i,t) if s=='keyword' else '' for i,t,s in zip(U.artifact_id,U.type_used,U.source)]
U['P']=U.artifact_id.map(lambda i:f'P{i:06d}')
cols=['P','province','reign','height','width','hw','bdtns','type','type_used','source','matched_line']
U[cols].to_csv(f'{R}/results/SI_ur3_text_types.csv',index=False)
K=U[U.source=='keyword']; S=pd.concat([g.sample(min(10,len(g)),random_state=0) for _,g in K.groupby('type_used')])
S[['P','province','type_used','matched_line']].to_csv(f'{R}/results/SI_ur3_tagging_sample.csv',index=False)
print(U.groupby(['type_used','source']).size())
print(S[['P','type_used','matched_line']].to_string(index=False,max_colwidth=90))
