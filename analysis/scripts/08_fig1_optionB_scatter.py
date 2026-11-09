"""Figure 1 option B, panel b: where each period's tablets come from and how broken they are.
x = share of the period's tablets from its main findspot; y = share in the most-damaged third; area = tablets."""
from _paths import FIGS, WORK
import pandas as pd, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
T=pd.read_csv(WORK+'/results/fig1_corpus_overview.csv')
fig,a=plt.subplots(figsize=(3.4,3.0),dpi=300)
a.scatter(T.site_share,T.l2,s=np.sqrt(T.n)*2.2,color='#2a78d6',alpha=0.85,edgecolor='white',linewidth=0.8,zorder=3)
OFF={'Early Old Babylonian':(-7,-12,'right'),'Neo-Babylonian':(5,-9,'left'),'Hellenistic':(-6,4,'right'),'Lagash II':(5,-8,'left'),
     'Middle Assyrian':(5,-9,'left'),'Middle Babylonian':(6,4,'left'),'Ebla':(-9,-4,'right'),'Old Babylonian':(8,4,'left'),'Ur III':(9,3,'left'),'Neo-Assyrian':(-14,6,'right')}
POS={'Old Akkadian':(0.265,0.175),'Early Old Babylonian':(0.458,0.258),'Neo-Babylonian':(0.50,0.383),'Old Babylonian':(0.30,0.43),'Ebla':(0.475,0.47),'Achaemenid':(0.395,0.165)}
for _,r in T.iterrows():
    if r.period in POS:
        a.text(*POS[r.period],f"{r.period}\n({r.site})",fontsize=4.2,color='#0b0b0b',va='center'); continue
    dx,dy,ha=OFF.get(r.period,(4,3,'left'))
    a.annotate(f"{r.period}\n({r.site})",(r.site_share,r.l2),xytext=(dx,dy),textcoords='offset points',fontsize=4.2,color='#0b0b0b',ha=ha)
a.set_xlabel('Share of tablets from the main findspot',fontsize=6,color='#52514e'); a.set_ylabel('Share in the most damaged third',fontsize=6,color='#52514e')
a.set_xlim(0.25,1.08); a.set_ylim(0,0.95)
a.xaxis.set_major_formatter(plt.FuncFormatter(lambda v,_:f'{v:.0%}')); a.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_:f'{v:.0%}'))
a.tick_params(labelsize=5,colors='#52514e',length=2); a.grid(color='#e6e5e1',linewidth=0.4,zorder=0)
for sp in ['top','right']: a.spines[sp].set_visible(False)
for sp in ['left','bottom']: a.spines[sp].set_color('#c3c2b7'); a.spines[sp].set_linewidth(0.5)
a.text(0.27,0.92,'Circle area = number of tablets',fontsize=4.6,color='#52514e',va='top')
plt.tight_layout(pad=0.4)
for ext in ['png','pdf']: fig.savefig(f'{FIGS}/fig1_optionB_findspot_damage.{ext}')
