"""Draft figure: which Mesopotamian traditions peripheral tablet groups resemble (DINOv2, museum controlled).
A: map of peripheral sites with their strongest robust affinity. B: lift by period (share of cross-museum
nearest neighbours relative to tablets in the same museums); filled = 95% CI above 1."""
from _paths import WORK
import json, pandas as pd, numpy as np, matplotlib.pyplot as plt
from matplotlib.lines import Line2D
R=WORK; G=f'{R}/geo'
C=pd.read_csv(f'{R}/results/dino_periphery_split.csv'); C=C[C.share>=0.01]
C['group']=C.group+C['mode'].map({'all':'','admin':' adm','letters':' let'})
INK='#222222'; MUTED='#777777'; ASS='#2a78d6'; BAB='#eb6834'; PER='#1baf7a'; OLD='#9a9a9a'
fig=plt.figure(figsize=(13,6.2)); axm=fig.add_axes([0.02,0.06,0.43,0.88]); axd=fig.add_axes([0.56,0.2,0.43,0.72])
def draw(f,**kw):
    for ft in json.load(open(f))['features']:
        g=ft['geometry']; parts=g['coordinates'] if g['type']=='MultiLineString' else [g['coordinates']] if g['type']=='LineString' else [p[0] for p in g['coordinates']] if g['type']=='MultiPolygon' else [g['coordinates'][0]]
        for p in parts:
            a=np.array(p); axm.plot(a[:,0],a[:,1],**kw)
draw(f'{G}/ne_50m_coastline.geojson',color='#b9c3cc',lw=0.8)
draw(f'{G}/ne_50m_rivers_lake_centerlines.geojson',color='#c9d8e6',lw=0.8)
axm.set_xlim(27,55); axm.set_ylim(25.5,42.5); axm.set_aspect(1/np.cos(np.radians(34)))
axm.set_xticks([]); axm.set_yticks([]); [s.set_visible(False) for s in axm.spines.values()]
core={'Assur':(43.26,35.46),'Nippur':(45.23,32.13),'Babylon':(44.42,32.54),'Ur':(46.10,30.96),'Persepolis':(52.89,29.93)}
peri={'Kanesh':(35.63,38.85),'Ḫattuša':(34.62,40.02),'Alalakh':(36.38,36.24),'Tuttul':(39.05,35.95),'Amarna':(30.90,27.65),
      'Nuzi':(44.31,35.39),'Susa':(48.26,32.19),'Anšan':(52.41,30.01)}
links=[('Kanesh','Assur',ASS,'-','Middle Assyrian letters ×8.9'),('Nuzi','Assur',ASS,'-','Middle Assyrian ×3.1'),
       ('Ḫattuša','Nippur',BAB,'-','Middle Babylonian ×2.0'),('Susa','Nippur',BAB,'-','Middle & Neo-Babylonian ×6'),
       ('Tuttul','Babylon',BAB,'-','Old Babylonian ×1.3 (check)'),('Anšan','Persepolis',PER,'-','Persepolis ×9'),
       ('Alalakh','Ur',OLD,(0,(3,3)),'Ur III ×3–4: British Museum effect')]
RAD={'Ḫattuša':-0.35,'Kanesh':0.15,'Tuttul':0.1,'Alalakh':0.1,'Nuzi':0.3,'Susa':0.2,'Anšan':0.5}
for a,b,c,ls,_ in links:
    (x0,y0),(x1,y1)=peri[a],core[b]
    axm.annotate('',xy=(x1,y1),xytext=(x0,y0),arrowprops=dict(arrowstyle='-|>',color=c,lw=1.8,ls=ls,shrinkA=5,shrinkB=6,connectionstyle=f'arc3,rad={RAD[a]}'),zorder=3)
CO={'Assur':(-1.6,-0.75),'Nippur':(0.35,-0.6),'Babylon':(-2.6,-0.2),'Ur':(0.35,-0.6),'Persepolis':(0.2,-0.8)}
for n,(x,y) in core.items():
    axm.scatter(x,y,marker='s',s=34,color='white',edgecolor=INK,lw=1.2,zorder=4); axm.text(x+CO[n][0],y+CO[n][1],n,fontsize=8,color=MUTED,zorder=5)
col={a:c for a,_,c,_,_ in links}; col['Amarna']=OLD
off={'Kanesh':(0.4,0.35),'Ḫattuša':(0.4,0.35),'Alalakh':(-3.2,-0.6),'Tuttul':(0.3,0.4),'Amarna':(0.45,0.2),'Nuzi':(0.4,0.35),'Susa':(0.4,0.35),'Anšan':(-0.6,0.55)}
for n,(x,y) in peri.items():
    axm.scatter(x,y,s=60,color=col[n],edgecolor='white',lw=1.4,zorder=6); dx,dy=off[n]; axm.text(x+dx,y+dy,n,fontsize=9.5,color=INK,fontweight='bold',zorder=7)
axm.text(30.9+0.45,27.65-0.6,'no affinity',fontsize=8,color=MUTED); axm.text(52.6,31.2,'×9',fontsize=8.5,color=PER,fontweight='bold')
axm.legend(handles=[Line2D([],[],color=ASS,lw=2,label='Assyrian'),Line2D([],[],color=BAB,lw=2,label='Babylonian'),Line2D([],[],color=PER,lw=2,label='Persepolis (Elamite)'),
    Line2D([],[],color=OLD,lw=2,ls=(0,(3,3)),label='collection effect'),Line2D([],[],marker='s',color='white',markeredgecolor=INK,ls='',label='reference site')],
    loc='upper right',frameon=False,fontsize=8.5)
axm.set_title('A  Where peripheral tablets find their closest matches',loc='left',fontsize=10.5,color=INK,fontweight='bold')
# B
periods=['ED IIIa','ED IIIb','Old Akkadian','Ur III','Early Old Babylonian','Old Babylonian','Middle Babylonian','Middle Assyrian','Neo-Assyrian','Neo-Babylonian','Achaemenid-Babylonia','Achaemenid-Persepolis','Hellenistic']
short=['ED IIIa','ED IIIb','OAkk','Ur III','EOB','OB','MB','MA','NA','NB','Ach\nBab.','Ach\nPers.','Hell']
pc={p:(ASS if p in ['Middle Assyrian','Neo-Assyrian'] else BAB if p in ['Early Old Babylonian','Old Babylonian','Middle Babylonian','Neo-Babylonian','Achaemenid-Babylonia'] else PER if p=='Achaemenid-Persepolis' else OLD) for p in periods}
groups=['Kanesh','Kanesh let','Ḫattuša','Alalakh VII','Alalakh IV','Tuttul (OB)','Amarna','Nuzi','Susa (OB)','Anšan','Anšan adm']
gl={'Kanesh':'Kanesh (Old Assyrian)','Ḫattuša':'Ḫattuša (Hittite)','Alalakh VII':'Alalakh VII (OB)','Alalakh IV':'Alalakh IV (MB)','Tuttul (OB)':'Tuttul (OB)','Amarna':'Amarna (MB)','Nuzi':'Nuzi (MB)','Susa (OB)':'Susa (OB)','Anšan':'Anšan (Middle Elamite)','Kanesh let':'   letters only','Anšan adm':'   administrative only'}
contemp={'Kanesh':['Ur III','Old Babylonian'],'Kanesh let':['Ur III','Old Babylonian'],'Anšan adm':['Middle Babylonian','Middle Assyrian'],'Ḫattuša':['Middle Babylonian','Middle Assyrian'],'Alalakh VII':['Old Babylonian'],'Alalakh IV':['Middle Babylonian'],'Tuttul (OB)':['Old Babylonian'],
         'Amarna':['Middle Babylonian'],'Nuzi':['Middle Babylonian','Middle Assyrian'],'Susa (OB)':['Old Babylonian'],'Anšan':['Middle Babylonian','Middle Assyrian']}
for i,g in enumerate(groups):
    for p in contemp[g]: axd.scatter(periods.index(p),i,s=420,facecolor='none',edgecolor='#cfcfcf',lw=1.2,zorder=1)
    for _,r in C[C.group==g].iterrows():
        if r.period not in periods or r.lift<=1: continue
        j=periods.index(r.period); s=40*min(r.lift,9)
        robust=r.lo>1
        axd.scatter(j,i,s=s,facecolor=pc[r.period] if robust else 'white',edgecolor=pc[r.period],lw=1.4,zorder=3)
axd.set_xticks(range(len(periods))); axd.set_xticklabels(short,fontsize=8.5,color=INK,rotation=0)
axd.set_yticks(range(len(groups))); axd.set_yticklabels([gl[g] for g in groups],fontsize=8.5,color=INK); axd.invert_yaxis()
axd.set_xlim(-0.6,len(periods)-0.4); axd.set_ylim(len(groups)-0.4,-0.6)
for s in axd.spines.values(): s.set_visible(False)
axd.tick_params(length=0); axd.grid(color='#f0f0f0',lw=0.8); axd.set_axisbelow(True)
axd.set_title('B  Resemblance by period (times expected)',loc='left',fontsize=10.5,color=INK,fontweight='bold')
h=[axd.scatter([],[],s=40*v,facecolor=OLD,edgecolor=OLD,label=f'×{v}') for v in [2,4,8]]
h+= [axd.scatter([],[],s=80,facecolor='white',edgecolor=OLD,lw=1.4,label='uncertain (CI includes 1)'),axd.scatter([],[],s=420,facecolor='none',edgecolor='#cfcfcf',lw=1.2,label='contemporary period')]
axd.legend(handles=h,loc='upper center',bbox_to_anchor=(0.45,-0.09),ncol=5,frameon=False,fontsize=8,columnspacing=1.2,handletextpad=0.3)
out=f'{R}/figures/Fig4_periphery_dinov2'; plt.savefig(out+'.png',dpi=200); plt.savefig(out+'.pdf'); print(out)
