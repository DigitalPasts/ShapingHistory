"""Case C figure: the Eanna documents, 630 to 520 BCE. (A) median height-to-width ratio of notes (photograph proportion,
CDLI) in five-year bins; (B) share of lists labelled 'portrait' by the DigEanna project; (C) median note and list of the
first and second half drawn to scale. Data: nabucco/eanna_by_5yr.csv, nabucco/digeanna_merged.csv. Output: figures/fig8_eanna.png."""
from _paths import FIGS, WORK
import pandas as pd, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
R=WORK; FIG=FIGS
B=pd.read_csv(f'{R}/nabucco/eanna_by_5yr.csv'); D=pd.read_csv(f'{R}/nabucco/digeanna_merged.csv')
B['x']=B['bin']+2.5
PA,PB='A','B'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7})
fig=plt.figure(figsize=(7.0,3.3)); a1=fig.add_axes([0.07,0.56,0.6,0.38]); a2=fig.add_axes([0.07,0.13,0.6,0.38],sharex=a1); a3=fig.add_axes([0.71,0.1,0.28,0.84])
reigns=[('Npl',626,605),('Nebuchadnezzar II',605,562),('',562,556),('Nabonidus',556,539),('Cyrus',539,530),('Camb.',530,522)]
for ax in (a1,a2):
    for i,(n,s,e) in enumerate(reigns):
        if i%2==0: ax.axvspan(e,s,color='#f2f1ee',lw=0)
    ax.axvline(584,c='#9a9893',lw=0.6,ls='--'); ax.axvline(556,c='#9a9893',lw=0.6,ls='--')
    for s_ in ['top','right']: ax.spines[s_].set_visible(False)
b=B[B.note_n>=20]; a1.plot(b.x,b.note_ratio,c='#2a78d6',lw=1.5,marker='o',ms=3.5)
a1.set_ylabel('notes: median h/w',fontsize=6.5); a1.set_ylim(0.62,0.80)
for n,s,e in reigns: a1.text((s+e)/2,0.795,n,ha='center',va='top',fontsize=5.6,color='#52514e')
a1.text(583,0.63,'temple run by royal officials (c. 584)',fontsize=5.2,color='#52514e',ha='right')
# lists by subject, ten-year bins (DigEanna transaction type): animals and personnel vs staples, goods and agriculture
L=D[D['Text Form'].str.startswith('List',na=False)&D.bce.notna()&D.fmt.isin(['landscape','portrait'])].copy(); tt=L['Transaction Type'].fillna('')
L['grp']=np.where(tt.str.contains('Animal husbandry|Personnel'),'lists of animals and people',np.where(tt.str.contains('allocation of staples|allocation of miscellaneous|Agriculture'),'lists of staples and goods',None))
L['bin']=(L.bce//10*10).astype(int); LB=L.dropna(subset=['grp']).groupby(['grp','bin']).fmt.agg(n='size',tall=lambda s:(s=='portrait').mean()).reset_index()
LB.to_csv(f'{R}/nabucco/eanna_lists_by_decade.csv',index=False)
for g_,c_ in [('lists of animals and people','#eb6834'),('lists of staples and goods','#6250d6')]:
    b=LB[(LB.grp==g_)&(LB.n>=6)]; a2.plot(b.bin+5,b.tall*100,c=c_,lw=1.5,marker='o',ms=3.5,label=g_)
a2.legend(fontsize=5.4,frameon=False,loc='upper left')
a2.set_ylabel('lists: % labelled tall (DigEanna)',fontsize=6.5); a2.set_ylim(0,100); a2.set_xlim(628,518); a2.set_xlabel('BCE')
plt.setp(a1.get_xticklabels(),visible=False)
a1.text(-0.08,1.04,PA,transform=a1.transAxes,fontsize=10,weight='bold'); a2.text(-0.08,1.04,PB,transform=a2.transAxes,fontsize=10,weight='bold')
# C: drawn medians
a3.set_xlim(0,2.2); a3.set_ylim(0,3.4); a3.axis('off'); a3.text(0,3.38,'C',fontsize=10,weight='bold',va='top')
early=D.reign.isin(['Nabopolassar','Nebuchadnezzar II']); late=D.reign.isin(['Nabonidus','Cyrus','Cambyses'])
def med(form,m): x=D[D['Text Form'].str.startswith(form,na=False)&m]; return x.ratio.median(), x.ratio.count()
for j,(form,lab) in enumerate([('Note','notes'),('List','lists')]):
    for i,(m,t) in enumerate([(early,'Npl–Nbk'),(late,'Nbn–Camb')]):
        r,n=med(form,m); x=0.55+i*1.05; y=2.45-j*1.7; A=0.36; w=np.sqrt(A/r); h=w*r
        a3.add_patch(Rectangle((x-w/2,y-h/2),w,h,fc='#e6e2d8',ec='#0b0b0b',lw=0.6))
        a3.text(x,y-0.5,f'{t}\n{r:.2f} (n={n})',ha='center',va='top',fontsize=5.6)
    a3.text(1.08,y+0.55,lab,ha='center',fontsize=6.5,weight='bold')
fig.savefig(f'{FIG}/fig8_eanna.png',dpi=300)
# strip for the merged Fig. 7 (panels D and E): the same two time series without the drawn medians
a3.remove(); a1.set_position([0.08,0.56,0.9,0.38]); a2.set_position([0.08,0.13,0.9,0.38])
for t in a1.texts+a2.texts:
    if t.get_text() in ('A','B'): t.set_text({'A':'C','B':'D'}[t.get_text()]); t.set_x(-0.055)
fig.savefig(f'{R}/figures/fig7_eanna_strip.png',dpi=300)
from PIL import Image
top=Image.open(f'{FIG}/fig7_amarna.png'); bot=Image.open(f'{R}/figures/fig7_eanna_strip.png')
bot=bot.resize((top.width,int(bot.height*top.width/bot.width))); out=Image.new('RGB',(top.width,top.height+bot.height),'white')
out.paste(top.convert('RGB'),(0,0)); out.paste(bot.convert('RGB'),(0,top.height)); out.save(f'{FIG}/fig7_amarna_eanna.png'); print('saved')
