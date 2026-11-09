"""Fig. 9 (draft): what the VAE adds to hand measurement in the three case studies (scripts 57-59).
A: accuracy of the same classifier given the ratio, height and width in mm, outline descriptors, or the VAE.
B: mean outline of Ur III receipts at Harvard, Puzrish-Dagan vs Girsu (same proportion, different corners).
C: Amarna letters whose nearest VAE neighbour is a letter of the same city or the same clay."""
from _paths import WORK
import pandas as pd, numpy as np, cv2, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
R=WORK; IMG=f'{R}/zenodo/imgs/images_b_w_tablets'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':6.5,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':0.6})
INK='#0b0b0b'; MUTED='#52514e'; GRID='#e6e4df'
C={'ratio':('#9a9893','o','height ÷ width'),'ruler':('#52514e','s','height and width (mm)'),'outline':('#eb6834','^','outline descriptors'),'VAE':('#2a78d6','D','VAE (12 dimensions)')}
T=pd.read_csv(f'{R}/results/vae_case_studies.csv'); W=pd.read_csv(f'{R}/results/vae_eanna_within_collection.csv'); N=pd.read_csv(f'{R}/results/vae_amarna_retrieval.csv')
def q(df,key,col='question'): d=df[df[col].str.contains(key,regex=False)]; return dict(zip(d.tier,d.acc)),d.chance.mean()
def nn(lab): d=N[N.label==lab]; return dict(zip(d.tier,d.same_group_nn)),d.chance.mean()
rows=[('Ur III messenger texts, Girsu vs Umma (Harvard)',*q(T,'Messenger Text, Harvard')),
('Ur III receipts, Puzriš-Dagan vs Girsu (Harvard)',*q(T,'receipt (šu ba-ti), Harvard')),
('Ur III receipts, Puzriš-Dagan vs Girsu (ISAC Chicago)',*q(T,'receipt (šu ba-ti), Institute')),
('Ur III receipts, Puzriš-Dagan vs Umma (NYPL)',*q(T,'receipt (šu ba-ti), New York')),
('Amarna, Byblos vs other vassal letters (Berlin)',*q(T,'Byblos vs other')),
('Amarna, nearest letter from the same city (Berlin)',*nn('city')),
('Eanna notes, early vs late, within collection',*q(W,'Note','form')),
('Eanna lists, early vs late, within collection',*q(W,'List','form'))]
C['outline']=('#eb6834','^','outline, edges and thickness')
fig=plt.figure(figsize=(7.2,4.3)); gs=fig.add_gridspec(2,2,width_ratios=[1.55,1],height_ratios=[1,1],wspace=0.08,hspace=0.35)
a=fig.add_subplot(gs[:,0])
for i,(lab,d,ch) in enumerate(rows):
    y=len(rows)-1-i; a.plot([ch,ch],[y-.3,y+.3],c=MUTED,lw=1); a.axhline(y,c=GRID,lw=0.5,zorder=0)
    for k,v in d.items():
        if pd.isna(v): continue
        c,m,_=C[k]; a.scatter(v,y,s=26 if k=='VAE' else 20,marker=m,fc=c if k!='ratio' else 'white',ec=c,lw=1,zorder=3)
    a.text(0.005,y+0.32,lab,fontsize=6,color=INK,transform=a.get_yaxis_transform())
for y0,t in [(7.75,'A  Ur III provinces'),(3.75,'B  Amarna letters'),(1.75,'C  Eanna archive')]: pass
a.set_yticks([]); a.set_xlim(0.2,1.0); a.set_ylim(-0.6,len(rows)-0.3); a.spines['left'].set_visible(False)
a.set_xlabel('share classified correctly (balanced); tick = chance',color=MUTED)
a.legend(handles=[plt.Line2D([],[],ls='',marker=m,mfc=c if k!='ratio' else 'white',mec=c,label=l) for k,(c,m,l) in C.items()],
         loc='lower left',bbox_to_anchor=(0,1.0),ncol=2,frameon=False,fontsize=6,handletextpad=0.2,columnspacing=0.8)
a.set_title('A',loc='left',fontweight='bold',x=-0.02,y=1.05)
# B what the descriptors show: three contrasts (script 61)
O=pd.read_csv(f'{R}/results/vae_contrast_descriptors.csv'); gR=pd.read_csv(f'{R}/results/silhouette_geometry.csv')
U=pd.read_csv(f'{R}/results/SI_ur3_text_types.csv'); U['id']=U.P.str[1:].astype(int)
art=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','collections'],low_memory=False).rename(columns={'artifact_id':'id'})
U=U.drop(columns='hw').merge(art,on='id').merge(gR,on='id'); U=U[U.collections.fillna('').str.startswith('Harvard')]
Am=pd.read_csv(f'{R}/amarna/SI_amarna_letters.csv'); Am['id']=Am.P.str[1:].astype(float); Am=Am[Am.museum.eq('Vorderasiatisches Museum')].merge(gR,on='id')
grt={'Babylon','Mittani','Hattusa','Alashiya','Arzawa','Assur','Egypt','Akhetaten'}; Am=Am[~Am.city.isin(grt)]
sets=[('Ur III receipts\n(Harvard)\ncorner fill',U[U.type_used.eq('receipt (šu ba-ti)')],'province',['Puzriš-Dagan','Girsu'],'corner_fill'),
      ('Ur III messenger\n(Harvard)\nthickness ÷ width',U[U.type_used.eq('Messenger Text')],'province',['Girsu','Umma'],'thick_side'),
      ('Amarna vassals\n(Berlin)\nthickness ÷ width',Am.assign(grp=np.where(Am.city.eq('Byblos'),'Byblos','others')),'grp',['Byblos','others'],'thick_side')]
sub=gs[0,1].subgridspec(1,3,wspace=0.7)
for j,(t,d,lab,gg,col) in enumerate(sets):
    ax=fig.add_subplot(sub[0,j]); vals=[d[d[lab]==x][col].dropna().values for x in gg]
    bp=ax.boxplot(vals,widths=0.5,showfliers=False,patch_artist=True,medianprops=dict(color=INK,lw=1))
    for pt,cc in zip(bp['boxes'],['#2a78d6','#eb6834']): pt.set(facecolor=cc,alpha=0.35,edgecolor=cc)
    for k in ['whiskers','caps']: [l.set(color=MUTED,lw=0.6) for l in bp[k]]
    ax.set_xticks([1,2],[x.replace('Puzriš-Dagan','P.-Dagan') for x in gg],fontsize=5.4); ax.tick_params(axis='y',labelsize=5.4)
    ax.set_title(t,fontsize=5.4,color=INK)
fig.text(0.565,0.95,'B',fontweight='bold',fontsize=6.5)
# C pairs of Amarna letters
c=fig.add_subplot(gs[1,1]); c.axis('off'); c.set_title('C  Amarna letters and their nearest VAE neighbour',loc='left',fontsize=6.5,fontweight='bold')
P=pd.read_csv(f'{R}/amarna/SI_amarna_letters.csv').set_index('EA')
pairs=[(60,157,'Mt Lebanon clay'),(286,287,'Jerusalem'),(281,283,'Gath')]
for j,(e1,e2,lab) in enumerate(pairs):
    for k,e in enumerate([e1,e2]):
        pid=int(P.loc[e,'P'][1:]); im=cv2.imread(f'{IMG}/{pid:06d}.png',0); m=im>127; m=~m if m.mean()>.5 else m
        ys,xs=np.nonzero(m); crop=m[ys.min():ys.max()+1,xs.min():xs.max()+1]; h,w=crop.shape; sc=0.36/max(h,w)
        x0=j*0.34+k*0.15+0.02; c.imshow(np.where(crop,0.15,1.0),cmap='gray',vmin=0,vmax=1,extent=[x0,x0+w*sc,0.22,0.22+h*sc],transform=c.transAxes,zorder=2)
        c.text(x0+w*sc/2,0.14,f'EA {e}',ha='center',fontsize=5.6,transform=c.transAxes,color=INK)
    c.text(j*0.34+0.16,0.70,lab,ha='center',fontsize=5.8,color=MUTED,transform=c.transAxes)
c.set_xlim(0,1); c.set_ylim(0,1)
fig.savefig(f'{R}/figures/fig9_vae.png',dpi=300,bbox_inches='tight'); print('ok')
