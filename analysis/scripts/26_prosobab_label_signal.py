"""Neo-Babylonian / Achaemenid: does shape carry Prosobab's document subtype, archive and place of writing across museums?
Link Prosobab tablets to photographed CDLI tablets by P-number in Prosobab's CDLI link, else by unique normalised museum number.
Then the same permutation test as 21_ob_label_signal.py (cross-museum same-label distance vs labels permuted within strata).
Usage: python 26_prosobab_label_signal.py [features.csv with CDLI_id + Z*/e* columns]"""
from _paths import WORK
import pandas as pd, numpy as np, re, sys
from scipy.spatial.distance import cdist
R=WORK; P=f'{R}/prosobab'; rng=np.random.default_rng(0)
FEAT=sys.argv[1] if len(sys.argv)>1 else f'{R}/results/tablet_latent_damage_adjusted.csv'
T=pd.read_csv(f'{P}/e_tablets.csv',low_memory=False); X=pd.read_csv(f'{P}/x_mentionedsubtypesobjects.csv')
S=pd.read_csv(f'{P}/s_subtypes.csv'); Ty=pd.read_csv(f'{P}/s_types.csv'); Lo=pd.read_csv(f'{P}/s_localities.csv'); A=pd.read_csv(f'{P}/c_archives.csv')
S['sub']=S.SubTypeGroup.fillna('').str.strip()
main=X.sort_values('Importance').drop_duplicates('TabletID').merge(S[['SubTypeID','sub']],on='SubTypeID',how='left')
T=T.merge(main[['TabletID','sub']],on='TabletID',how='left').merge(Ty,on='TypeID',how='left')
lc=[c for c in Lo.columns if 'name' in c.lower() or c.lower().startswith('locality')]; T=T.merge(Lo[['LocalityID',lc[1] if len(lc)>1 else lc[0]]].rename(columns={'LocalityID':'PlaceOfWritingID',(lc[1] if len(lc)>1 else lc[0]):'place'}),on='PlaceOfWritingID',how='left')
T=T.merge(A[['ArchiveID','ArchiveName']],on='ArchiveID',how='left')
T['P']=T.CDLI_URL.fillna('').str.extract(r'P(\d{6})')[0].astype(float)
norm=lambda s: re.sub(r'[\s\.,]','',str(s)).upper().lstrip('0')
def nm(s):
    m=re.match(r'\s*([A-Za-z]{1,6})\.?\s*([\d\-\.,]+)',str(s)); return (m.group(1).upper()+re.sub(r'^0+','',re.sub(r'[\.,\s]','',m.group(2)))) if m else None
art=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','museum_no','collections','period'],low_memory=False)
art['key']=art.museum_no.map(nm); T['key']=T.MuseumNr.map(nm)
ku=art.dropna(subset=['key']).groupby('key').artifact_id.agg(lambda x: x.iloc[0] if len(x)==1 else np.nan).dropna()
T['CDLI_id']=T.P.fillna(T.key.map(ku))
F=pd.read_csv(FEAT); Z=[c for c in F.columns if re.fullmatch(r'Z\d+|e\d+|X\d+',c)]
D=T.dropna(subset=['CDLI_id']).astype({'CDLI_id':int}).drop_duplicates('CDLI_id').merge(F[['CDLI_id']+Z],on='CDLI_id').merge(art[['artifact_id','collections']].rename(columns={'artifact_id':'CDLI_id'}),on='CDLI_id')
D['coll']=D.collections.fillna('?').str.split(';').str[0].str.strip()
print('Prosobab tablets',len(T),'| linked to photographed CDLI tablets',len(D),'| museums',D.coll.nunique())
D['sub']=D['sub'].fillna(''); D['arch']=D.ArchiveName.fillna(''); D['place']=D.place.fillna('').astype(str); D['Type']=D.Type.fillna('')
Xv=D[Z].values; co=D.coll.values
def stat(lab,a):
    idx=np.where(lab==a)[0]; c=co[idx]; cross=c[:,None]!=c[None,:]
    return cdist(Xv[idx],Xv[idx])[cross].mean() if cross.any() else np.nan
TESTS={'Type':['coll','place'],'sub':['coll','place'],'arch':['coll','sub'],'place':['coll','sub']}
rows=[]
for lab,strat in TESTS.items():
    st=D[strat].astype(str).agg('|'.join,axis=1); groups=[np.asarray(ix) for ix in st.groupby(st).groups.values()]
    for a,g in D[D[lab]!=''].groupby(lab):
        vc=g.coll.value_counts()
        if (vc>=8).sum()<2: continue
        obs=stat(D[lab].values,a); perm=[]
        for _ in range(500):
            l=D[lab].values.copy()
            for ix in groups: l[ix]=rng.permutation(l[ix])
            perm.append(stat(l,a))
        perm=np.array(perm,dtype=float); perm=perm[~np.isnan(perm)]
        rows.append(dict(label=lab,group=a,n=len(g),n_museums=int((vc>=8).sum()),ratio=obs/perm.mean(),p=(np.sum(perm<=obs)+1)/(len(perm)+1)))
o=pd.DataFrame(rows); pd.set_option('display.width',200); print(o.round(3).to_string(index=False))
o.to_csv(f'{R}/results/nb_label_signal.csv',index=False); D[['CDLI_id','TabletID','MuseumNr','Type','sub','arch','place','coll']].to_csv(f'{R}/results/prosobab_cdli_match.csv',index=False)
