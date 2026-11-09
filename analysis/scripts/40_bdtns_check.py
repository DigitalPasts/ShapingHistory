"""Check the keyword tagging of Ur III text types (script 34) against BDTNS text-type labels (script 37),
and repeat the Girsu/Umma comparison on BDTNS labels alone."""
from _paths import WORK
import numpy as np, pandas as pd
R=WORK
U=pd.read_csv(f'{R}/results/s4_ur3_tablets.csv')
B=pd.read_csv(f'{R}/bdtns/bdtns_types.csv').dropna(subset=['CDLI_id']); B['CDLI_id']=B.CDLI_id.astype(int)
lab=B.groupby('CDLI_id').label.agg(lambda x:'; '.join(sorted(set(x)))).rename('bdtns').reset_index()
U=U.merge(lab,left_on='artifact_id',right_on='CDLI_id',how='left')
t=U[U.type.notna()]
print('Ur III measured archival tablets with transliteration:',len(t),'| with a BDTNS type label:',t.bdtns.notna().sum())
bm=t.bdtns.fillna('').str.contains('Messenger'); km=t.type=='messenger text'
print('BDTNS messenger:',bm.sum(),'| keyword messenger:',km.sum(),'| both:',(bm&km).sum())
print('precision (keyword tag confirmed by BDTNS):',round((bm&km).sum()/km.sum(),3),' recall (BDTNS messenger found by keywords):',round((bm&km).sum()/bm.sum(),3))
print('keyword type of BDTNS messenger texts:',t[bm].type.value_counts().to_dict())
print('BDTNS label of keyword messenger texts not in BDTNS messenger:',t[km&~bm].bdtns.fillna('none').value_counts().head(5).to_dict())
rows=[]
for L in ['Messenger Text','Letter-order','Loan Document','Sale Document','Legal Text: court record','pisan dub-ba','Tablet and Envelope']:
    g=U[U.bdtns.fillna('').str.contains(L,regex=False)]
    for p,x in g.groupby('province'):
        if len(x)>=20: rows.append(dict(bdtns_type=L,province=p,n=len(x),median_hw=round(x.hw.median(),3),h=x.height.median(),w=x.width.median(),
            MAD=round(np.median(np.abs(np.log(x.hw)-np.median(np.log(x.hw)))),3)))
T=pd.DataFrame(rows); print(T.to_string(index=False)); T.to_csv(f'{R}/results/s4_bdtns_type_province.csv',index=False)
# Girsu vs Umma messenger texts by reign on BDTNS labels
g=U[U.bdtns.fillna('').str.contains('Messenger')&U.province.isin(['Girsu','Umma'])]
print(g.groupby(['reign','province']).hw.agg(['size','median']).round(3))
U.to_csv(f'{R}/results/s4_ur3_tablets_bdtns.csv',index=False)
# Combined text type: BDTNS label where it exists (messenger texts, letter-orders, loans, sales, court records),
# else the formula-based keyword tag for the four Puzriš-Dagan transaction types (mu-DU, i3-dab5, ba-zi, šu ba-ti)
# and balanced accounts (nig2-ka9-ak), else 'other'. Then Girsu minus Umma by reign within type, bootstrap CI.
KEEP=['delivery (mu-DU)','transfer (i-dab)','expenditure (ba-zi)','receipt (šu ba-ti)','balanced account']
def comb(r):
    if isinstance(r.bdtns,str):
        for L in ['Messenger Text','Letter-order','Loan Document','Sale Document','Legal Text: court record','Legal Text: other']:
            if L in r.bdtns: return L
    return r.type if r.type in KEEP else 'other'
U['type2']=U.apply(comb,axis=1); U['l']=np.log(U.hw)
RO=['Šulgi 1-40','Šulgi 41-48','Amar-Suen','Šū-Suen','Ibbi-Suen']
gu=U[U.province.isin(['Girsu','Umma'])&U.reign.notna()]
def diff(df):
    num=den=0
    for t,x in df.groupby('type2'):
        a=x[x.province=='Girsu'].l; b=x[x.province=='Umma'].l
        if len(a)>=10 and len(b)>=10: w=min(len(a),len(b)); num+=w*(np.median(a)-np.median(b)); den+=w
    return num/den if den else np.nan
res=[]
for r in RO:
    g=gu[gu.reign==r]; est=diff(g); bs=[diff(g.sample(len(g),replace=True,random_state=i)) for i in range(300)]
    raw=np.median(g[g.province=='Girsu'].l)-np.median(g[g.province=='Umma'].l)
    res.append(dict(reign=r,n=len(g),raw_diff=round(raw,3),within_type_diff=round(est,3),lo=round(np.nanpercentile(bs,2.5),3),hi=round(np.nanpercentile(bs,97.5),3)))
GU=pd.DataFrame(res); print(GU.to_string(index=False)); GU.to_csv(f'{R}/results/s4_ur3_girsu_umma_v2.csv',index=False)
print(U.type2.value_counts().to_dict())
