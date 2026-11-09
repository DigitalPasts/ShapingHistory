"""Figure 2: chronological confusion map of the released silhouette model (tablets only).
Cell shade = share of a period's test tablets assigned to each period (rows sum to 1; diagonal = recognised).
Outlined cells = confusions larger than the predicted period's general pull on errors (lift 95% CI > 1, >=10% of errors)."""
from _paths import FIGS, WORK
import pandas as pd, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
R=WORK; F=FIGS
inv={0:'other',1:'Ur III',2:'Neo-Assyrian',3:'Old Babylonian',4:'Middle Babylonian',5:'Neo-Babylonian',6:'Old Akkadian',7:'Achaemenid',8:'Early Old Babylonian',9:'ED IIIb',10:'Middle Assyrian',11:'Old Assyrian',12:'Uruk III',13:'Proto-Elamite',14:'Lagash II',15:'Ebla',16:'ED IIIa',17:'Hellenistic',18:'ED I-II',19:'Middle Elamite',20:'Hittite',21:'Uruk IV'}
ORDER=['ED IIIb','Ebla','Old Akkadian','Lagash II','Ur III','Early Old Babylonian','Old Babylonian','Old Assyrian','Middle Babylonian','Middle Assyrian','Neo-Assyrian','Neo-Babylonian','Achaemenid']
SHORT={'Early Old Babylonian':'Early OB','Old Babylonian':'Old Bab.','Middle Babylonian':'Middle Bab.','Neo-Babylonian':'Neo-Bab.','Middle Assyrian':'Middle Ass.','Neo-Assyrian':'Neo-Ass.','Old Assyrian':'Old Ass.','Old Akkadian':'Old Akkadian'}
t=pd.read_csv(f'{R}/results/resnet_masked_test_predictions.csv'); t=t[t.artifact_type.isin(['tablet','tablet & envelope'])]
t['true']=t.y.map(inv); t['p']=t.pred.map(inv).where(lambda s:s.isin(ORDER),'other')
t=t[t.true.isin(ORDER)]
M=pd.crosstab(t.true,t.p,normalize='index').reindex(index=ORDER,columns=ORDER+['other']).fillna(0)
n=t.true.value_counts()
L=pd.read_csv(f'{R}/results/confusion_lift.csv'); L=L[(L.lo>1)&(L.share_of_errors>=0.10)]
cm=LinearSegmentedColormap.from_list('b',['#ffffff','#86b6ef','#2a78d6','#104281'])
fig,ax=plt.subplots(figsize=(7.4,6.4),dpi=300)
im=ax.imshow(M.values,cmap=cm,vmin=0,vmax=1,aspect='auto')
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        v=M.values[i,j]
        if v>=0.03: ax.text(j,i,f'{v*100:.0f}',ha='center',va='center',fontsize=6.5,color='white' if v>0.55 else '#0b0b0b')
for _,r in L.iterrows():
    if r.true in ORDER and r.pred in ORDER:
        i,j=ORDER.index(r.true),ORDER.index(r.pred)
        ax.add_patch(plt.Rectangle((j-.5,i-.5),1,1,fill=False,ec='#c2410c',lw=1.6))
lab=[SHORT.get(p,p) for p in ORDER]
ax.set_xticks(range(len(ORDER)+1)); ax.set_xticklabels(lab+['other'],rotation=55,ha='right',fontsize=7.5,color='#0b0b0b')
ax.set_yticks(range(len(ORDER))); ax.set_yticklabels([f'{l}  ({n[p]:,})' for l,p in zip(lab,ORDER)],fontsize=7.5,color='#0b0b0b')
ax.set_xlabel('Period assigned from the silhouette',fontsize=8.5,color='#52514e'); ax.set_ylabel('Catalogued period (test tablets)',fontsize=8.5,color='#52514e')
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0)
cb=fig.colorbar(im,ax=ax,fraction=0.035,pad=0.02); cb.set_label('% of the period\'s tablets',fontsize=7.5,color='#52514e'); cb.ax.tick_params(labelsize=6.5); cb.outline.set_visible(False)
cb.set_ticks([0,.25,.5,.75,1]); cb.set_ticklabels(['0','25','50','75','100'])
ax.text(0,1.03,'Periods in time order; outlined = mistaken more often than period size predicts',transform=ax.transAxes,fontsize=7.5,color='#52514e')
fig.tight_layout(); fig.savefig(f'{F}/Fig2_confusion_chrono_draft.png'); fig.savefig(f'{F}/Fig2_confusion_chrono_draft.pdf')
M.round(3).to_csv(f'{R}/results/fig2_confusion_matrix.csv'); print(M.round(2).to_string())
