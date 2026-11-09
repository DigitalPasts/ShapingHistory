"""Figure 5 options (the shift in tablet proportions) and Figure 6 (what the scribe held fixed).
Catalogue dimensions, tablets only. Rows are scribal traditions; colours as in Fig 4.
Option A 'tablet strip': each period's median tablet drawn to scale (mm) at its date.
Option B 'ribbon': median h/w with interquartile range on a time axis, one line per tradition.
Option C 'ridgeline': distribution of h/w per period, in date order.
Fig 6: median height x width by size quintile, drawn to scale, for ED IIIb, Ur III, OB, NB, Achaemenid."""
from _paths import FIGS, WORK
import numpy as np, pandas as pd, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from scipy.stats import gaussian_kde
R=WORK; OUT=FIGS
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.spines.top':False,'axes.spines.right':False})
COL={'Babylonian':'#eb6834','Assyrian':'#2a78d6','Elamite':'#1baf7a','Syrian':'#8e5cd9'}
# period, tradition, start, end, abbreviation; provenience filter (None = all)
P=[('Uruk IV','Babylonian',-3350,-3200,'Uruk IV',None),('Uruk III','Babylonian',-3200,-3000,'Uruk III',None),
 ('ED IIIa','Babylonian',-2600,-2500,'ED IIIa',None),('ED IIIb','Babylonian',-2500,-2340,'ED IIIb',None),
 ('Old Akkadian','Babylonian',-2340,-2200,'OAkk',None),('Ur III','Babylonian',-2110,-2003,'Ur III',None),
 ('Early Old Babylonian','Babylonian',-2003,-1900,'EOB',None),('Old Babylonian','Babylonian',-1900,-1600,'OB',None),
 ('Middle Babylonian','Babylonian',-1400,-1100,'MB',None),('Neo-Babylonian','Babylonian',-626,-539,'NB',None),
 ('Achaemenid','Babylonian',-539,-330,'Ach',None),('Hellenistic','Babylonian',-330,-60,'Hell',None),
 ('Old Assyrian','Assyrian',-1950,-1750,'OA (Kaneš)',None),('Middle Assyrian','Assyrian',-1400,-1000,'MA',None),
 ('Neo-Assyrian','Assyrian',-911,-612,'NA',None),
 ('Proto-Elamite','Elamite',-3100,-2900,'Proto-El.',None),('Middle Elamite','Elamite',-1450,-1300,'ME (Haft Tepe)',None),
 ('Ebla','Syrian',-2400,-2300,'Ebla',None)]
# cleaned dimensions (script 38): reversed entries corrected against photographs, impossible ratios dropped.
# Archival documents only (administrative, legal, letters). Ḫattuša left out: too few archival tablets measured (21), see SI.
c=pd.read_csv(f'{R}/results/tablet_dims_clean.csv'); c=c.rename(columns={'P':'Pn'})
m=c[c.archival]
rows=[]
for p,t,s,e,ab,_ in P:
    g=m[m.Pn==p]
    rows.append(dict(period=p,trad=t,start=s,end=e,mid=(s+e)/2,ab=ab,n=len(g),h=g.height.median(),w=g.width.median(),
        hw=g.hw.median(),q1=g.hw.quantile(.25),q3=g.hw.quantile(.75)))
D=pd.DataFrame(rows); D.to_csv(f'{R}/results/fig5_period_formats.csv',index=False); print(D.round(2).to_string(index=False))
TR=list(COL)
# ---------- Option A: tablet strip
fig,ax=plt.subplots(figsize=(7.2,4.4)); K=2.2  # years per mm
ROW={t:-i*135 for i,t in enumerate(TR)}
for t in TR:
    ax.axhline(ROW[t],color='#d9d9d6',lw=0.6,zorder=0); ax.text(-3420,ROW[t]+40,t,ha='left',va='bottom',fontsize=8,color='#333')
for _,r in D.iterrows():
    x0=r.mid-r.w*K/2; y0=ROW[r.trad]
    ax.add_patch(FancyBboxPatch((x0,y0),r.w*K,r.h,boxstyle=f'round,pad=0,rounding_size={4}',mutation_aspect=1/K,
        fc=COL[r.trad],ec='white',lw=1.2,alpha=0.9))
    dy=-6-(26 if r.ab in ('ED IIIb','EOB','Uruk III') else 0)
    ax.text(r.mid,y0+dy,f'{r.ab}\n{r.hw:.2f}',ha='center',va='top',fontsize=6.2,color='#333')
ax.set_xlim(-3450,0); ax.set_ylim(ROW[TR[-1]]-60,110); ax.set_yticks([]); ax.set_aspect(K)
ax.set_xticks(range(-3000,1,500)); ax.set_xticklabels([f'{-x} BCE' if x else '0' for x in range(-3000,1,500)])
ax.spines['left'].set_visible(False)
ax.plot([-400,-400+50*K],[ROW[TR[-1]]-30]*2,color='#333',lw=1); ax.text(-400+25*K,ROW[TR[-1]]-27,'50 mm',ha='center',va='bottom',fontsize=6)
ax.set_title('Median tablet of each period, drawn to scale (height × width); number = height-to-width ratio',fontsize=8,loc='left')
ax.annotate('Administrative, legal and epistolary tablets. CDLI catalogue dimensions checked against photographs (SI).',(0,-0.16),xycoords='axes fraction',fontsize=6,color='#666')
fig.tight_layout(); fig.savefig(f'{OUT}/Fig5_optionA_tablet_strip.png',dpi=300,bbox_inches='tight'); fig.savefig(f'{OUT}/Fig5_optionA_tablet_strip.pdf',bbox_inches='tight'); plt.close()
# ---------- Option B: ribbon
fig,ax=plt.subplots(figsize=(7.2,3.4))
ax.axhspan(1,1.9,color='#f3f1ec',zorder=0); ax.axhline(1,color='#999',lw=0.8,ls='--')
ax.text(-3420,1.83,'taller than wide',fontsize=7,color='#777',va='top'); ax.text(-3420,0.66,'wider than tall',fontsize=7,color='#777',va='bottom')
for t in TR:
    g=D[D.trad==t].sort_values('mid')
    seg=(g.mid.diff()>500).cumsum()
    for _,gg in g.groupby(seg): ax.plot(gg.mid,gg.hw,color=COL[t],lw=2,marker='o',ms=5,mec='white',mew=1.2,zorder=3)
    ax.plot([],[],color=COL[t],lw=2,marker='o',label=t)
    for _,r in g.iterrows():
        ax.plot([r.mid,r.mid],[r.q1,r.q3],color=COL[t],lw=1,alpha=0.6,zorder=2)
        ax.hlines(r.hw,r.start,r.end,color=COL[t],lw=0.8,alpha=0.5)
        ax.annotate(r.ab,(r.mid,r.hw),xytext=(0,(-11 if r.ab in ('Ebla','ED IIIa','Uruk III','MA') else 6) if t!='Assyrian' else (-10 if r.ab!='MA' else -12)),textcoords='offset points',ha='center',fontsize=6,color='#333')
ax.set_yscale('log'); ax.set_yticks([0.6,0.8,1,1.25,1.5,1.8]); ax.set_yticklabels(['0.6','0.8','1','1.25','1.5','1.8']); ax.minorticks_off()
ax.set_ylim(0.6,1.9); ax.set_xlim(-3450,0); ax.set_xticks(range(-3000,1,500)); ax.set_xticklabels([f'{-x} BCE' if x else '0' for x in range(-3000,1,500)])
ax.set_ylabel('height-to-width ratio\n(median and middle half)'); ax.legend(frameon=False,fontsize=7,loc='lower left',ncol=4,bbox_to_anchor=(0,-0.32))
ax.grid(axis='y',color='#eee',lw=0.5); fig.tight_layout(); fig.savefig(f'{OUT}/Fig5_optionB_ribbon.png',dpi=300); fig.savefig(f'{OUT}/Fig5_optionB_ribbon.pdf'); plt.close()
# ---------- Option C: ridgeline
Do=D.sort_values('mid'); fig,ax=plt.subplots(figsize=(4.2,6.2)); xs=np.linspace(np.log(0.4),np.log(2.6),300)
for i,(_,r) in enumerate(Do.iterrows()):
    v=np.log(m[m.Pn==r.period].hw.values); k=gaussian_kde(v,bw_method=0.25)(xs); k=k/k.max()*1.15; y=-i
    ax.fill_between(np.exp(xs),y,y+k,color=COL[r.trad],alpha=0.85,lw=0,zorder=100-i); ax.plot(np.exp(xs),y+k,color='white',lw=1,zorder=100-i)
    ax.text(0.39,y+0.15,f'{r.ab}  ({-int(r.start)}–{-int(r.end)})',ha='right',fontsize=6.5,color='#333')
ax.axvline(1,color='#666',lw=0.8,ls='--',zorder=200); ax.set_xscale('log'); ax.set_xticks([0.5,0.75,1,1.5,2]); ax.set_xticklabels(['0.5','0.75','1','1.5','2'])
ax.minorticks_off(); ax.set_yticks([]); ax.spines['left'].set_visible(False); ax.set_xlim(0.4,2.6); ax.set_xlabel('height-to-width ratio')
for t in TR: ax.plot([],[],color=COL[t],lw=6,label=t)
ax.legend(frameon=False,fontsize=6.5,loc='lower center',bbox_to_anchor=(0.5,-0.16),ncol=2); fig.tight_layout()
fig.savefig(f'{OUT}/Fig5_optionC_ridgeline.png',dpi=300); fig.savefig(f'{OUT}/Fig5_optionC_ridgeline.pdf'); plt.close()
# ---------- Fig 6: what the scribe held fixed
SEL=[('ED IIIb','ED IIIb\n2500–2340','Babylonian'),('Ur III','Ur III\n2110–2003','Babylonian'),('Old Babylonian','Old Babylonian\n1900–1600','Babylonian'),
     ('Neo-Babylonian','Neo-Babylonian\n626–539','Babylonian'),('Achaemenid','Achaemenid\n539–330','Babylonian')]
fig,axs=plt.subplots(1,len(SEL)+1,figsize=(7.4,2.9),gridspec_kw={'width_ratios':[1]*len(SEL)+[1.5]})
shades=['#fbd9c6','#f6b08b','#f08650','#d0581f','#8f3a12']; fq=[]
for ax,(p,lab,t) in zip(axs,SEL):
    g=m[m.Pn==p].copy(); g['q']=pd.qcut(np.sqrt(g.height*g.width),5,labels=False)
    q=g.groupby('q').agg(h=('height','median'),w=('width','median'),hw=('hw','median')).reset_index(); q['period']=p; fq.append(q)
    for i,r in q[::-1].iterrows():
        ax.add_patch(FancyBboxPatch((0,0),r.w,r.h,boxstyle='round,pad=0,rounding_size=2.5',fc=shades[i],ec='white',lw=1))
    ax.set_xlim(-2,82); ax.set_ylim(-2,100); ax.set_aspect('equal'); ax.set_title(lab,fontsize=6.8,loc='left')
    ax.set_xticks([0,40,80]); ax.set_yticks([0,40,80]); ax.tick_params(labelsize=6)
axs[0].set_ylabel('height (mm)',fontsize=7); axs[2].set_xlabel('width (mm); five size classes, smallest in front',fontsize=7)
F=pd.concat(fq); F.to_csv(f'{R}/results/fig6_size_classes.csv',index=False); ax=axs[-1]
LS={'ED IIIb':':','Ur III':'-','Old Babylonian':'-','Neo-Babylonian':'--','Achaemenid':'--'}; MK={'ED IIIb':'s','Ur III':'o','Old Babylonian':'^','Neo-Babylonian':'D','Achaemenid':'v'}
for p,g in F.groupby('period'):
    ax.plot(g.q+1,g.hw,ls=LS[p],marker=MK[p],color='#333' if p!='Old Babylonian' else '#eb6834',ms=4,lw=1.2)
    ax.annotate({'ED IIIb':'ED IIIb','Ur III':'Ur III','Old Babylonian':'OB','Neo-Babylonian':'NB','Achaemenid':'Ach'}[p],(5,g.hw.iloc[-1]),xytext=(4,0),textcoords='offset points',fontsize=6,va='center')
ax.axhline(1,color='#999',lw=0.6,ls='--'); ax.set_xticks(range(1,6)); ax.set_xticklabels(['small','','','','large'],fontsize=6)
ax.set_ylabel('height-to-width ratio',fontsize=7); ax.tick_params(labelsize=6); ax.set_xlim(0.7,5.9); ax.set_title('ratio by size class',fontsize=6.8,loc='left')
fig.tight_layout(); fig.savefig(f'{OUT}/Fig6_fixed_balance.png',dpi=300); fig.savefig(f'{OUT}/Fig6_fixed_balance.pdf'); plt.close()
print(F.round(2).to_string(index=False))
