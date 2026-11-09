"""Draft figure: what OB tablet shape carries across museums (from 21_ob_label_signal.py output).
x = mean distance between same-label tablets in different museums / same after shuffling labels within museum strata.
Below 1 = more alike than chance. Filled = p < 0.05."""
from _paths import WORK
import pandas as pd, matplotlib.pyplot as plt, sys
R=WORK; f=sys.argv[1] if len(sys.argv)>1 else f'{R}/results/ob_label_signal.csv'
o=pd.read_csv(f)
if 'space' in o: o=o[o.space=='cos'].copy(); o['label']=o.label.map({'type':'type','archive':'arch','site':'fsite','date':'date_bin'})
EN={'prêt à intérêt':'loan at interest','prêt autre':'loan, other','reçu':'receipt','location':'lease','fermage':'field lease','achat':'purchase','lettre':'letter',
 'quittance':'quittance','liste de personnes':'list of persons','attribution de ration':'ration allocation','compte récapitulatif':'summary account','dépense':'expenditure',
 'gestion de personnel':'personnel management','quantités + noms propres':'quantities + names','texte indéterminé':'undetermined','Babylone':'Babylon','Kiš':'Kish','apport':'contribution','larsa':'Larsa','kish':'Kish','sippar':'Sippar','dilbat':'Dilbat','1792-1750 (Hammurabi)':'Hammurabi (1792–1750)','1810-1793':'Rim-Sin, Sin-muballit (1810–1793)','after 1750':'after 1750'}
KIND={'type':'Document type','arch':'Archive','fsite':'Findspot','date_bin':'Reign'}
o=o[o.group!='texte indéterminé']; o['name']=o.group.map(lambda g: EN.get(g, g.split('/')[-1] if '/' in g else g))
o['kind']=o.label.map(KIND); o=o[o.kind.notna()]
order=['Document type','Archive','Findspot','Reign']
fig,ax=plt.subplots(figsize=(6.2,7.6)); y=0; ticks=[]; labels=[]; ink='#333333'; c='#2a6fb0'
for k in order:
    g=o[o.kind==k].sort_values('ratio')
    ax.text(0.66,y-0.2,k,fontsize=10,fontweight='bold',color=ink,va='bottom'); y+=0.9
    for _,r in g.iterrows():
        sig=r.p<0.05
        ax.plot([1,r.ratio],[y,y],color='#c8c8c8',lw=1,zorder=1)
        ax.scatter(r.ratio,y,s=46,facecolor=c if sig else 'white',edgecolor=c,linewidth=1.6,zorder=3)
        ticks.append(y); labels.append(f'{r["name"]} (n={r.n})'); y+=1
    y+=0.6
ax.axvline(1,color='#888888',lw=1,ls=(0,(3,3)))
ax.set_yticks(ticks); ax.set_yticklabels(labels,fontsize=8.5,color=ink); ax.invert_yaxis()
ax.set_xlim(0.66,1.34); ax.set_xlabel('Distance between same-label tablets in different museums\n(relative to shuffled labels; below 1 = more alike than chance)',fontsize=8.5,color=ink)
for s in ['top','right','left']: ax.spines[s].set_visible(False)
ax.tick_params(axis='y',length=0); ax.grid(axis='x',color='#eeeeee',lw=0.8); ax.set_axisbelow(True)
ax.scatter([],[],s=46,facecolor=c,edgecolor=c,label='p < 0.05'); ax.scatter([],[],s=46,facecolor='white',edgecolor=c,linewidth=1.6,label='not significant')
ax.legend(loc='lower right',frameon=False,fontsize=8.5)
plt.tight_layout(); out=f'{R}/figures/Fig3_ob_label_signal'+('_dinov2' if 'dino' in f else '_vae'); plt.savefig(out+'.png',dpi=200); plt.savefig(out+'.pdf'); print(out)
