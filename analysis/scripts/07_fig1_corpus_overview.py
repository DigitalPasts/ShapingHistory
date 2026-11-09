"""Figure 1 option A, 'the corpus seen whole': one column per period (chronological), showing
the typical tablet as found (nearest the period median, any preservation), the typical complete tablet
(nearest complete one, as in 04_fig1_medoids.py), the number of tablets, the share by damage level
(damage index from 06_preservation_control.py, cut at corpus-wide terciles) and the share from the
dominant findspot."""
from _paths import FIGS, WORK
import pandas as pd, numpy as np, matplotlib, sys; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
R=WORK; Z=f'{R}/zenodo'
d=pd.concat([pd.read_csv(f'{Z}/vae_encoding_df_April16_w_class_{s}.csv') for s in ['train','val','test']])
m=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','artifact_type','provenience'],low_memory=False)
d=d.merge(m,left_on='CDLI_id',right_on='artifact_id').merge(pd.read_csv(f'{R}/results/damage_score.csv')[['CDLI_id','damage']],on='CDLI_id')
d=d[d.artifact_type.isin(['tablet','tablet & envelope'])].copy()
X=[f'X{i}' for i in range(1,13)]; d[X]=(d[X]-d[X].mean())/d[X].std()
d['site']=d.provenience.fillna('unknown').str.split(' \\(').str[0].replace({'uncertain':'unknown'})
t1,t2=d.damage.quantile([1/3,2/3]); d['lvl']=np.select([d.damage<=t1,d.damage<=t2],[0,1],2)
med=pd.read_csv(f'{R}/results/fig1_medoids.csv')
SHORT={'Early Old Babylonian':'Early OB','Old Babylonian':'Old Bab.','Middle Babylonian':'Mid. Bab.','Middle Assyrian':'Mid. Ass.',
       'Old Assyrian':'Old Ass.','Neo-Assyrian':'Neo-Ass.','Neo-Babylonian':'Neo-Bab.','Old Akkadian':'Old Akk.','Hellenistic':'Hellen.','Achaemenid':'Achaem.'}
DATES={'Uruk III':'3200','ED IIIa':'2600','ED IIIb':'2500','Ebla':'2400','Old Akkadian':'2340','Lagash II':'2200','Ur III':'2110',
       'Early Old Babylonian':'2003','Old Babylonian':'1900','Old Assyrian':'1950','Middle Assyrian':'1400','Middle Babylonian':'1400',
       'Hittite':'c. 1400','Neo-Assyrian':'911','Neo-Babylonian':'626','Achaemenid':'539','Hellenistic':'330'}
def sil(i):
    im=np.array(Image.open(f'{Z}/imgs/images_b_w_tablets/{i:06d}.png').convert('L'))>127
    if im.mean()>0.5: im=~im
    ys,xs=np.where(im); return ~im[ys.min():ys.max()+1,xs.min():xs.max()+1]
rows=[]
for _,r in med.iterrows():
    g=d[d.Period_Name==r.period]; v=g[X].values; i_found=int(g.CDLI_id.iloc[np.argmin(np.linalg.norm(v-np.median(v,0),axis=1))])
    sc=g.site.value_counts(normalize=True)
    rows.append(dict(period=r.period,n=len(g),found=i_found,complete=int(r.example_cdli_id),
                     l0=(g.lvl==0).mean(),l1=(g.lvl==1).mean(),l2=(g.lvl==2).mean(),site=sc.index[0],site_share=sc.iloc[0]))
T=pd.DataFrame(rows); T=T.iloc[T.period.map(lambda p:-int(DATES[p].replace('c. ',''))).argsort(kind='stable')].reset_index(drop=True); T.to_csv(f'{R}/results/fig1_corpus_overview.csv',index=False)
INK,MUTED,RULE='#0b0b0b','#52514e','#c3c2b7'; C=['#86b6ef','#2a78d6','#104281']
MIL={'Uruk III':'4th'}; MIL.update({p:'3rd' for p in ['ED IIIa','ED IIIb','Ebla','Old Akkadian','Lagash II','Ur III']})
MIL.update({p:'2nd' for p in ['Early Old Babylonian','Old Assyrian','Old Babylonian','Hittite','Middle Assyrian','Middle Babylonian']})
MIL.update({p:'1st' for p in ['Neo-Assyrian','Neo-Babylonian','Achaemenid','Hellenistic']})
SPAN={'Uruk III':(3200,3000),'ED IIIa':(2600,2500),'ED IIIb':(2500,2340),'Ebla':(2400,2300),'Old Akkadian':(2340,2200),'Lagash II':(2200,2100),
 'Ur III':(2110,2003),'Early Old Babylonian':(2003,1900),'Old Assyrian':(1950,1750),'Old Babylonian':(1900,1600),'Hittite':(1400,1180),
 'Middle Assyrian':(1400,1000),'Middle Babylonian':(1400,1100),'Neo-Assyrian':(911,612),'Neo-Babylonian':(626,539),'Achaemenid':(539,330),'Hellenistic':(330,30)}
def draw(style):
    nc=len(T); groups=[MIL[p] for p in T.period]
    gap=0.55 if style=='blocks' else 0.0
    # column x-positions in grid units, with optional gaps between millennium blocks
    xs=[];x=0
    for c in range(nc):
        if c>0 and groups[c]!=groups[c-1]: x+=gap
        xs.append(x); x+=1
    W=x; top_h={'band':0.55,'timeline':1.25,'blocks':0.55}[style]
    fig=plt.figure(figsize=(7.0,4.6+0.35*top_h),dpi=300)
    L,Rm,B,Tp=0.085,0.995,0.02,0.985
    H=[top_h,1.25,1.25,0.9,0.9,0.55]; tot=sum(H)+0.3; ys=[]; y=Tp
    for h in H: y-=h/tot*(Tp-B); ys.append(y)
    def ax(row,c):
        w=(Rm-L)/W; x0=L+xs[c]*w; y0=ys[row]; h=H[row]/tot*(Tp-B)
        return fig.add_axes([x0+0.06*w,y0+0.04*h,0.88*w,0.92*h])
    toprow=fig.add_axes([L,ys[0],Rm-L,H[0]/tot*(Tp-B)]); toprow.set_xlim(0,W); toprow.set_ylim(0,1); toprow.axis('off')
    blocks=[]
    for c,g in enumerate(groups):
        if not blocks or blocks[-1][0]!=g: blocks.append([g,c,c])
        else: blocks[-1][2]=c
    name={'4th':'4th mill.','3rd':'3rd millennium BCE','2nd':'2nd millennium BCE','1st':'1st millennium BCE'}
    if style=='band':
        shade=['#f0efec','#ffffff']
        for k,(g,a,b) in enumerate(blocks):
            toprow.add_patch(plt.Rectangle((xs[a],0.05),xs[b]+1-xs[a],0.6,color='#e7f1fb' if k%2==0 else '#f0efec',lw=0))
            toprow.text((xs[a]+xs[b]+1)/2,0.35,name[g],ha='center',va='center',fontsize=5.4,color=INK)
    if style=='blocks':
        for g,a,b in blocks:
            x0,x1=xs[a]+0.1,xs[b]+0.9
            toprow.plot([x0,x0,x1,x1],[0.15,0.3,0.3,0.15],color=MUTED,lw=0.6)
            toprow.text((x0+x1)/2,0.5,name[g],ha='center',va='center',fontsize=5.4,color=INK)
    if style=='timeline':
        # a true time axis (3300 to 0 BCE) with each period's span, linked to its column
        t2x=lambda t: (3300-t)/3300*W
        toprow.plot([0,W],[0.78,0.78],color=RULE,lw=0.6)
        for t in [3000,2000,1000,0]:
            toprow.plot([t2x(t)]*2,[0.74,0.82],color=MUTED,lw=0.6); toprow.text(t2x(t),0.9,f'{t} BCE' if t else '0',ha='center',fontsize=4.6,color=MUTED)
        for k,(t0,t1) in enumerate([(3300,3000),(3000,2000),(2000,1000),(1000,0)]):
            toprow.text((t2x(t0)+t2x(t1))/2,0.62,['','3rd millennium','2nd millennium','1st millennium'][k],ha='center',fontsize=5,color=INK)
        lanes={}
        for c,p in enumerate(T.period):
            a,b=SPAN[p]; lane=0
            lo,hi=b,a   # years BCE: a is the start (larger), b the end
            while any(lo<h2+40 and l2<hi+40 for l2,h2 in lanes.get(lane,[])): lane+=1
            lanes.setdefault(lane,[]).append((lo,hi)); yl=0.5-0.09*lane
            toprow.plot([t2x(a),t2x(b)],[yl,yl],color='#2a78d6',lw=1.4,solid_capstyle='butt')
            toprow.plot([(t2x(a)+t2x(b))/2,xs[c]+0.5],[yl,0.0],color=RULE,lw=0.35)
    for c,r in T.iterrows():
        for k,key in enumerate(['found','complete']):
            a=ax(1+k,c); a.imshow(sil(r[key]),cmap='gray',vmin=0,vmax=1); a.axis('off')
            if k==0: a.set_title(f"{SHORT.get(r.period,r.period)}\n{DATES[r.period]}",fontsize=4.6,pad=2,color=INK)
        a=ax(3,c); a.bar([0],[np.log10(r.n)],width=0.6,color='#2a78d6'); a.set_ylim(0,4.9); a.set_xlim(-0.6,0.6); a.axis('off')
        a.text(0,np.log10(r.n)+0.15,f'{r.n:,}',ha='center',va='bottom',fontsize=3.8,color=INK)
        a=ax(4,c); b=0
        for j,s_ in enumerate([r.l0,r.l1,r.l2]):
            a.bar([0],[s_],bottom=b,width=0.6,color=C[j],edgecolor='white',linewidth=0.4); b+=s_
        a.set_ylim(-0.12,1); a.set_xlim(-0.6,0.6); a.axis('off'); a.text(0,-0.03,f'{r.l2:.0%}',ha='center',va='top',fontsize=3.8,color=INK)
        a=ax(5,c); a.axis('off'); a.set_xlim(0,1); a.set_ylim(0,1)
        a.text(0.5,0.72,r.site.replace('Puzriš-Dagan','Puzriš-D.')[:11],ha='center',va='center',fontsize=3.7,color=INK)
        a.text(0.5,0.28,f'{r.site_share:.0%}',ha='center',va='center',fontsize=3.7,color=MUTED)
    labs=['As found\n(typical)','Complete\n(typical)','Tablets\n(log scale)','Damage\nlevel','Main\nfindspot']
    for k,l in enumerate(labs):
        h=H[k+1]/tot*(Tp-B); fig.text(0.005,ys[k+1]+h/2,l,fontsize=4.6,color=MUTED,va='center')
    from matplotlib.patches import Patch
    fig.legend(handles=[Patch(color=C[j],label=t) for j,t in enumerate(['least damaged third','middle third','most damaged third (share printed)'])],
               loc='lower right',ncol=3,fontsize=4.3,frameon=False,bbox_to_anchor=(0.995,0.0))
    for ext in ['png','pdf']: fig.savefig(f'{FIGS}/fig1_corpus_overview_{style}.{ext}')
for st in (sys.argv[1:] or ['band','blocks','timeline']): draw(st)
