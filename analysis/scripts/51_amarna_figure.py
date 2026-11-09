"""Case B figure and SI data file. Each Amarna letter: sender and city after Moran 1992, clay provenance where published
by Goren, Finkelstein and Na'aman (2002, 2003), tablet proportion from the CDLI photograph, and median clay colour
(CIELAB) measured on the CDLI photograph (script 47). Letters of Amurru are placed at the town where Goren et al.
locate their clay. Colour is compared only within the Vorderasiatisches Museum, Berlin, because photographs from
different museums differ in lighting. Outputs: amarna/SI_amarna_letters.csv, amarna/SI_amarna_cities.csv,
figures/fig7_amarna.png."""
from _paths import FIGS, WORK
import pandas as pd, numpy as np, json, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from skimage.color import lab2rgb
from scipy.stats import kruskal, mannwhitneyu
R=WORK; FIG=FIGS
L=pd.read_csv(f'{R}/amarna/amarna_letters.csv'); C=pd.read_csv(f'{R}/amarna/colour_amarna.csv')
S=pd.read_csv(f'{R}/geo/amarna_sites.csv').set_index('site')
L=L.merge(C[['artifact_id','L','a','b','chroma','hue']],on='artifact_id',how='left')
L['museum']=L.collections.str.split(',').str[0]
L['colour_ok']=L.L.notna()&(L.L<=85)&L.museum.eq('Vorderasiatisches Museum')
# place of making after the petrographic catalogue of Goren, Finkelstein and Na'aman 2004 (script 55); letters they
# did not sample keep the sender's city; letters whose clay they could not place are left off the map
G=pd.read_csv(f'{R}/goren/goren2004_catalogue.csv').rename(columns={'section':'goren_section','Reliability':'goren_reliability','Matrix':'goren_matrix','concl':'goren_conclusion','ppl_colour':'goren_matrix_colour'})
G['made_at']=G.made_at.replace({'Mt Lebanon (E of Tripoli)':'Mt Lebanon','Ullasa? (Tripoli area)':'Ullasa?'})
G['goren_reliability']=G.goren_reliability.fillna('').str.extract(r'^(High|Satisfactory|Moderate|Fair|Fairly reliable)')[0]
L=L.merge(G[['EA_n','made_at','goren_section','goren_reliability','goren_matrix_colour','goren_conclusion']].drop_duplicates('EA_n'),left_on='EA',right_on='EA_n',how='left')
L['written_at']=np.where(L.made_at.notna(),L.made_at,L.city); L.loc[L.written_at.eq('unknown'),'written_at']=np.nan
L=L.join(S[['lat','lon','source']].rename(columns={'source':'coord_source'}),on='written_at')
L['sender_source']='Moran 1992'; L.loc[L.clay_published.notna(),'clay_source']='Goren, Finkelstein and Na\'aman 2002; 2003'; L.loc[L.made_at.notna(),'clay_source']='Goren, Finkelstein and Na\'aman 2004'
L['shape_source']='CDLI photograph'; L.loc[L.L.notna(),'colour_source']='CDLI photograph (script 47)'
cols=['EA','P','designation','museum_no','museum','sender','city','region','written_at','lat','lon','coord_source','clay_published','goren_section','goren_reliability','goren_matrix_colour','goren_conclusion','clay_source','hw_ratio','shape_source','sender_source']
L[cols].to_csv(f'{R}/amarna/SI_amarna_letters.csv',index=False)
# city summary
g=L[L.written_at.ne('Akhetaten')&L.hw_ratio.notna()].groupby('written_at')
T=pd.DataFrame({'n_shape':g.hw_ratio.size(),'hw':g.hw_ratio.median()})
gc=L[L.colour_ok&L.written_at.ne('Akhetaten')].groupby('written_at')
T=T.join(pd.DataFrame({'n_colour':gc.L.size(),'L':gc.L.median(),'a':gc.a.median(),'b':gc.b.median()})).join(S[['lat','lon','source']])
T.drop(columns=['n_colour','L','a','b']).round(3).to_csv(f'{R}/amarna/SI_amarna_cities.csv'); print(T.round(2).to_string())
v=L[L.colour_ok&L.written_at.ne('Akhetaten')]; k=v.groupby('written_at').filter(lambda x:len(x)>=3)
print('Kruskal b*',kruskal(*[x.b for _,x in k.groupby('written_at')]).pvalue,'a*',kruskal(*[x.a for _,x in k.groupby('written_at')]).pvalue,
      'h/w',kruskal(*[x.hw_ratio.dropna() for _,x in k.groupby('written_at')]).pvalue, 'cities',k.written_at.nunique(),'letters',len(k))
by=v.city.eq('Byblos'); print('Byblos b*',v[by].b.median(),v[~by].b.median(),mannwhitneyu(v[by].b,v[~by].b).pvalue)
# controls: domestic letters at home (photograph proportions, as for the Amarna letters)
cs=pd.read_csv(f'{R}/results/case_scan_tablets.csv',low_memory=False)
p=pd.read_csv(f'{R}/zenodo/h_w_ratio_df_all.csv'); p['artifact_id']=p.tablet_p_id_CDLI.str[1:].astype(int)
cs=cs.drop(columns='hw').merge(p[['artifact_id','hw_ratio']].drop_duplicates('artifact_id').rename(columns={'hw_ratio':'hw'}),on='artifact_id')
let=cs[cs.genres.fillna('').str.contains('Letter')]
home={'Babylonia (Nippur, Middle Babylonian)':let[(let.site=='Nippur')&let.per.str.contains('Middle Babylonian',na=False)],
      'Nuzi (Middle Babylonian)':let[let.site.isin(['Nuzi','Gasur/Nuzi'])],'Aššur (Middle Assyrian)':let[(let.site=='Assur')&let.per.str.contains('Middle Assyrian',na=False)],
      'Alalakh (Middle Babylonian)':let[(let.site=='Alalakh')&let.per.str.contains('Middle Babylonian',na=False)]}
abroad={'Babylonia (Nippur, Middle Babylonian)':('Babylon',L[L.city=='Babylon']),'Nuzi (Middle Babylonian)':('Mittani',L[L.city=='Mittani']),
        'Aššur (Middle Assyrian)':('Assur',pd.DataFrame({'hw_ratio':pd.read_csv(f'{R}/amarna/external_photos.csv').query('EA==15').hw_photo})),'Alalakh (Middle Babylonian)':('Ugarit',L[L.city=='Ugarit'])}
H=[]
for k_,h in home.items():
    a_=abroad[k_][1].hw_ratio.dropna(); H.append(dict(home=k_,n_home=len(h),hw_home=h.hw.median(),sent_from=abroad[k_][0],n_abroad=len(a_),hw_abroad=a_.median()))
H=pd.DataFrame(H); H.round(3).to_csv(f'{R}/amarna/SI_amarna_home_abroad.csv',index=False); print(H.round(2).to_string())
def rgb(l,a,b): return np.clip(lab2rgb(np.array([[[l,a,b]]]))[0,0],0,1)
# ---------- figure ----------
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8})
fig=plt.figure(figsize=(7.2,5.6)); axA=fig.add_axes([0.0,0.04,0.64,0.94]); axB=fig.add_axes([0.655,0.30,0.34,0.45])
coast=json.load(open(f'{R}/geo/ne_50m_coastline.geojson'))
for f in coast['features']:
    gm=f['geometry']; parts=gm['coordinates'] if gm['type']=='MultiLineString' else [gm['coordinates']]
    for p in parts: p=np.array(p); axA.plot(p[:,0],p[:,1],c='#9a9893',lw=0.6)
axA.set_xlim(30.35,39.75); axA.set_ylim(30.95,36.25); axA.set_aspect(1/np.cos(np.radians(33.5))); axA.axis('off')
west=['Alashiya','Ugarit','Sumur','Ardata','Byblos','Beirut','Sidon','Tyre','Akko','Ginti-kirmil','Ashdod','Ashkelon','Gath','Gaza','Yurza']
east=['Nuhasse','Tunip','Qatna','Kadesh','Irqata','Mt Lebanon','Beqa valley','Kumidi','Damascus','Hazor','Bashan','Anaharath','Megiddo','Yokneam','Beth-Shean','Shechem','Pella','Jerusalem','Gezer','Lachish']
lab={'Mt Lebanon':'Mt Lebanon (Amurru)','Alashiya':'Alašiya','Beqa valley':'Beqaʿ','Beth-Shean':'Beth-Shean (Eg.)','Gaza':'Gaza (Eg.)'}
H0=0.22; k=1/np.cos(np.radians(33.5))
for side,names,xc in [('w',west,32.75),('e',east,37.55)]:
    r_=T.loc[[c for c in names if c in T.index]].sort_values('lat',ascending=False)
    gap=(36.1-31.15)/(len(r_)-1); ys=np.linspace(36.1,31.15,len(r_))
    for (c,r),y in zip(r_.iterrows(),ys):
        h=H0; w=H0/r.hw*k; fc='#e6e2d8'
        edge=xc+(w/2 if side=='w' else -w/2)
        axA.plot([edge,r.lon],[y,r.lat],c='#c3c2b7',lw=0.45,zorder=1); axA.plot(r.lon,r.lat,'o',ms=2.2,c='#52514e',zorder=2)
        axA.add_patch(Rectangle((xc-w/2,y-h/2),w,h,fc=fc,ec='#0b0b0b',lw=0.5,zorder=3))
        t=f"{lab.get(c,c)}  {r.hw:.2f} ({int(r.n_shape)})"
        if side=='w': axA.text(xc-0.33,y,t,ha='right',va='center',fontsize=5.0)
        else: axA.text(xc+0.33,y,t,ha='left',va='center',fontsize=5.0)
axA.text(30.4,36.4,'A',fontsize=11,weight='bold',va='top')
axA.text(35.0,30.85,'Each group of letters drawn at its median height-to-width ratio (number of letters).\nLetters are placed where Goren et al. (2004) locate their clay; (Eg.) = Egyptian centre.',fontsize=5.2,va='top',ha='center',color='#52514e')
# B: home vs abroad
axB.set_xlim(0,4); axB.set_ylim(-0.2,2.2); axB.axis('off'); axB.text(0,2.2,'B',fontsize=11,weight='bold',va='top')
axB.text(0.3,2.15,'Letters at home and letters to Egypt',fontsize=6.5,va='top')
for i,r in H.iterrows():
    for j,(hw,n,t) in enumerate([(r.hw_home,r.n_home,'at home'),(r.hw_abroad,r.n_abroad,'to Egypt')]):
        if pd.isna(hw):
            axB.text(0.5+i*1.0+(j-0.5)*0.42,1.2,'no\nphoto',ha='center',va='center',fontsize=5.2,color='#52514e'); continue
        x=0.5+i*1.0+(j-0.5)*0.42; h=0.75; w=h/hw*0.55
        axB.add_patch(Rectangle((x-w/2,0.85),w,h,fc='white' if j==0 else '#e6e2d8',ec='#0b0b0b',lw=0.6))
        axB.text(x,0.8,f"{hw:.2f}\nn={n}",ha='center',va='top',fontsize=5.6)
    axB.text(0.5+i,1.75,r.home.split(' (')[0].replace('Nuzi','Mittani / Nuzi').replace('Alalakh','Alalakh / Ugarit'),ha='center',fontsize=5.4,weight='bold')
axB.text(2.0,-0.15,'white: letters found at home\ngrey: letters sent to Egypt\n(Aššur: EA 15, Metropolitan Museum photograph)',ha='center',fontsize=5.4,color='#52514e')
fig.savefig(f'{FIG}/fig7_amarna.png',dpi=300,bbox_inches='tight',pad_inches=0.05); print('saved')
