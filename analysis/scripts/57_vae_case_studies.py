"""What does the VAE add to hand measurement in the three case studies?  For each question the same classifier is run on
several descriptions of the same tablets:  (1) the height-to-width ratio of the obverse;  (1b) for Ur III, height and width
in mm from the catalogue, i.e. what a ruler gives;  (2) the ratio plus eleven descriptors of the obverse, reverse and edges
computed from the silhouette (script 56: rectangularity, solidity, circularity, corner fill, taper, side and end bulge,
reverse corner fill, reverse-to-obverse area, thickness at sides and ends), i.e. what a careful scholar could describe;  (3) the twelve VAE dimensions (Zenodo 10.5281/zenodo.12787746).
Classifier: L2 logistic regression on standardised features, balanced classes, repeated stratified 5-fold CV, balanced
accuracy; null from 200 label permutations.  All comparisons are made within one museum."""
from _paths import WORK
import pandas as pd, numpy as np, warnings; warnings.filterwarnings('ignore')
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score
R=WORK; rng=np.random.default_rng(0)
X=[f'X{i}' for i in range(1,13)]; GEO=['hw','rect','solidity','circ','corner_fill','taper','side_bulge','end_bulge','rev_corner_fill','rev_obv','thick_side','thick_end']
v=pd.concat([pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_{s}.csv') for s in ['train','val','test']]).drop_duplicates('CDLI_id')
v=v.rename(columns={'CDLI_id':'id'})[['id']+X]
g=pd.read_csv(f'{R}/results/silhouette_geometry.csv'); g['loghw']=np.log(g.hw); g=g.drop(columns='hw')
F=v.merge(g.fillna(g.median()),on='id')
TIERS={'ratio':['loghw'],'outline':['loghw']+GEO[1:],'VAE':X}
def run(df,lab,name,case,nperm=200,min_n=8,cap=300,tiers=None):
    tiers=tiers or TIERS
    df=df.dropna(subset=[lab]); vc=df[lab].value_counts(); keep=vc[vc>=min_n].index
    if len(keep)<2: return []
    k=min(vc[keep].min(),cap); d=pd.concat([df[df[lab]==c].sample(k,random_state=0) for c in keep]); y=d[lab].values
    cv=RepeatedStratifiedKFold(n_splits=min(5,k),n_repeats=5,random_state=0)
    out=[]
    for t,cols in tiers.items():
        m=make_pipeline(StandardScaler(),LogisticRegression(C=1.0,max_iter=2000))
        acc=cross_val_score(m,d[cols].values,y,cv=cv,scoring='balanced_accuracy').mean()
        cv1=RepeatedStratifiedKFold(n_splits=min(5,k),n_repeats=1,random_state=1)
        null=np.array([cross_val_score(m,d[cols].values,rng.permutation(y),cv=cv1,scoring='balanced_accuracy').mean() for _ in range(nperm)])
        out.append(dict(case=case,question=name,classes=' | '.join(map(str,keep)),n_each=k,tier=t,acc=round(acc,3),
                        chance=round(null.mean(),3),p=round((1+(null>=acc).sum())/(1+nperm),3)))
    return out
rows=[]
# ---------- Case A: Ur III provinces, within text type and museum
U=pd.read_csv(f'{R}/results/SI_ur3_text_types.csv'); U['id']=U.P.str[1:].astype(int)
a=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','collections'],low_memory=False).rename(columns={'artifact_id':'id'})
U=U.drop(columns='hw').merge(a,on='id').merge(F,on='id'); U['coll']=U.collections.fillna('?').str.split(',').str[0]
U['lh']=np.log(U.height); U['lw']=np.log(U.width); U=U.dropna(subset=['lh','lw'])
TA={'ratio':TIERS['ratio'],'ruler':['lh','lw'],'outline':TIERS['outline'],'VAE':X}
for (t,c),d in U[U.province.isin(['Umma','Girsu','Puzriš-Dagan'])].groupby(['type_used','coll']):
    if t!='other' and d.province.value_counts().iloc[:2].min()>=25: rows+=run(d,'province',f'province: {t}, {c}','A Ur III',nperm=100,tiers=TA)
# ---------- Case B: Amarna letters in Berlin
A=pd.read_csv(f'{R}/amarna/SI_amarna_letters.csv'); A['id']=A.P.str[1:].astype(float)
G=pd.read_csv(f'{R}/goren/goren2004_catalogue.csv')[['EA_n','made_at','Reliability']]
A['EA_n']=A.EA; A=A.merge(G,on='EA_n',how='left').merge(F,on='id')
B=A[A.museum.eq('Vorderasiatisches Museum')].copy()
great={'Babylon','Mittani','Hattusa','Alashiya','Arzawa','Assur'}
B['rank']=np.where(B.city.isin(great),'great king','vassal'); B.loc[B.city.isin(['Egypt','Akhetaten']),'rank']=np.nan
rows+=run(B,'rank','great kings vs vassals (Berlin)','B Amarna',min_n=6)
B['byb']=np.where(B.city.eq('Byblos'),'Byblos','other Levant'); B.loc[B['rank']!='vassal','byb']=np.nan
rows+=run(B,'byb','Byblos vs other vassals (Berlin)','B Amarna')
B['made']=B.made_at.where(B.made_at.map(B.made_at.value_counts())>=6)
rows+=run(B,'made','place of making, Goren et al. (Berlin)','B Amarna',min_n=6)
# ---------- Case C: Eanna
D=pd.read_csv(f'{R}/nabucco/digeanna_merged.csv'); D['id']=D.P.astype(str).str.extract(r'(\d+)')[0].astype(float); D=D.merge(F,on='id')
D['form']=D['Text Form'].str.split(' ').str[0]
D['coll']=D.museum.fillna(D.collections.fillna('?').str.split(',').str[0])
D['phase']=np.select([D.reign.isin(['Kandalānu','Nabopolassar'])|(D.reign.eq('Nebuchadnezzar II')&(D.year<=20)),
                      D.reign.eq('Nebuchadnezzar II')&(D.year>20),D.reign.isin(['Nabonidus','Cyrus','Cambyses','Bardiya'])],
                     ['to Nbk 20','Nbk 21-43','Nbn-Camb'],None)
D['early_late']=D.phase.replace({'to Nbk 20':'Npl-Nbk','Nbk 21-43':'Npl-Nbk'})
for f in ['Note','List','Debt']:
    d=D[D.form.eq(f)]
    rows+=run(d,'early_late',f'{f}: Nabopolassar-Nebuchadnezzar vs Nabonidus-Cambyses (all collections)','C Eanna')
    for c,dc in d.groupby('coll'):
        if dc.early_late.value_counts().min()>=12 and dc.early_late.nunique()==2: rows+=run(dc,'early_late',f'{f}: early vs late, {c}','C Eanna')
d=D[D.form.eq('List')&D.phase.isin(['to Nbk 20','Nbk 21-43'])]; rows+=run(d,'phase','List: Nbk to year 20 vs years 21-43','C Eanna',min_n=6)
T=pd.DataFrame(rows); T.to_csv(f'{R}/results/vae_case_studies.csv',index=False)
P=T.pivot_table(index=['case','question','n_each'],columns='tier',values='acc').reset_index().reindex(columns=['case','question','n_each','ratio','ruler','outline','VAE'])
P=P.merge(T[T.tier=='VAE'][['question','chance','p']],on='question')
print(P[['case','question','n_each','ratio','ruler','outline','VAE','chance','p']].to_string(index=False))
