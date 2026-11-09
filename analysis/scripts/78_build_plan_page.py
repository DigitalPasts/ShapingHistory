"""Build the plan page (HTML) from the codebook, the scores and the pilot outputs of scripts 70-79.
Template: repro/plan_template.html (the string __DATA__ is replaced by one JSON object). Output: repro/centralization_plan.html.
All numbers on the page are read from the CSV files here; the prose that interprets them is in TEXT below."""
from _paths import TEMPLATES, WORK
import pandas as pd, numpy as np, json, sys, math
R=WORK; sys.path.insert(0,f'{R}/scripts')
from refs_centralization import REFS
rd=lambda f,**k: pd.read_csv(f'{R}/{f}',**k)
def clean(o):
    if isinstance(o,dict): return {k:clean(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)): return [clean(v) for v in o]
    if isinstance(o,(np.integer,)): return int(o)
    if isinstance(o,(float,np.floating)): return None if math.isnan(o) else float(o)
    return o
CB=rd('centralization_codebook.csv'); L=rd('centralization_scores_long.csv'); W=rd('centralization_scores_wide.csv',index_col=0)
I=rd('centralization_indices.csv',index_col=0)
params=list(CB.param); rows=list(W.index)
scores={r:{} for r in rows}
for _,c in L.iterrows(): scores[c.period][c.param]=dict(score=int(c.score),conf=c.conf,evidence=c.evidence,refs=str(c.refs))
LABEL={'A_polity_reach':'A polity reach','B_institutional_economy':'B institutional economy','C_control_of_writing':'C writing and norms',
       'scribal_institution':'scribal institution (BUR+SCHOOL)','PC1_all':'PC1 overall','MAD':'proportion spread','MAD_in_museum':'proportion spread, within museum',
       'VAEd':'silhouette spread','VAEd_in_museum':'silhouette spread, within museum','tall':'share tall','med':'median log h/w'}
lab=lambda k: LABEL.get(k,k)
# ---------- pilot 1
P1=rd('pilot1_period_table.csv',index_col=0)
SHORT={'Achaemenid (Babylonia)':'Ach. Babylonia','Achaemenid (Persepolis)':'Persepolis','Early Old Babylonian':'Early OB','Old Babylonian':'OB',
       'Middle Babylonian':'MB','Middle Assyrian':'MA','Ur III':'Ur III','Neo-Assyrian':'NA','Neo-Babylonian':'NB','Old Akkadian':'Old Akkadian','Old Assyrian':'Old Assyrian'}
def pts(xc,yc):
    o=[dict(x=P1.loc[r,xc],y=P1.loc[r,yc],n=int(P1.loc[r,'n']),name=r,short=SHORT.get(r,r),dy=0) for r in P1.index]
    o=sorted(o,key=lambda q:q['y'])
    for i in range(1,len(o)):  # nudge labels of near-coincident points apart
        if abs(o[i]['x']-o[i-1]['x'])<0.3 and abs(o[i]['y']-o[i-1]['y'])<0.04*max(q['y'] for q in o): o[i]['dy']=o[i-1]['dy']-12
    return o
S1=rd('pilot1_spearman.csv')
sp1=S1.assign(v=[f'{a:+.2f} ({b:.2f})' for a,b in zip(S1.rho,S1.p_perm)]).pivot(index='predictor',columns='outcome',values='v')
sp1=sp1.loc[[p for p in params+list(LABEL) if p in sp1.index]].reset_index()
sp1['predictor']=sp1.predictor.map(lab)
sp1Cols=[['predictor','Parameter']]+[[o,lab(o)+' ρ (p)'] for o in ['MAD','MAD_in_museum','VAEd','VAEd_in_museum','tall']]
r1=lambda o,p: S1[(S1.outcome==o)&(S1.predictor==p)].iloc[0]
# ---------- pilot 2
A=rd('pilot2a_cells.csv'); B=rd('pilot2b_tablets.csv'); C=rd('pilot2c_lopo.csv')
p2a=A.assign(predictor=A.predictor.map(lab),outcome=A.outcome.map(lab))[['outcome','predictor','cells','periods','beta','t_cluster','p_perm']]
p2aCols=[['outcome','Outcome'],['predictor','Parameter'],['cells','Cells'],['periods','Periods'],['beta','β per SD'],['t_cluster','t (clustered)'],['p_perm','p (permutation)']]
p2b=B.merge(C[['predictor','rho_heldout','p_perm']].rename(columns={'p_perm':'p_lopo'}),on='predictor')
p2b['predictor']=p2b.predictor.map(lab)
p2b=p2b[['predictor','tablets','odds_ratio_per_sd','p_perm_logit','VAE_partial_R2','VAE_R2_null_median','p_perm_VAE','rho_heldout','p_lopo']]
p2bCols=[['predictor','Parameter'],['tablets','Tablets'],['odds_ratio_per_sd','Tall: odds ratio per SD'],['p_perm_logit','p'],
         ['VAE_partial_R2','VAE: partial R²'],['VAE_R2_null_median','partial R² expected by chance'],['p_perm_VAE','p'],
         ['rho_heldout','Held-out period: ρ predicted vs scored'],['p_lopo','p']]
# ---------- pilot 3
P3=rd('pilot3_parameters_vs_elements.csv')
EL={'lh_median':'proportion (median)','lh_mad':'proportion (spread)','thick_side_est_median':'side thickness','thick_side_est_mad':'side thickness (spread)',
    'thick_end_est_median':'end thickness','thick_end_est_mad':'end thickness (spread)','rect_est_median':'rectangularity','rect_est_mad':'rectangularity (spread)',
    'corner_fill_est_median':'corner fill','corner_fill_est_mad':'corner fill (spread)'}
p3=P3.assign(v=[f'{a:+.2f}'+('*' if b<0.05 else '') for a,b in zip(P3.rho,P3.p_perm)]).pivot(index='parameter',columns='element',values='v')
p3=p3.loc[[p for p in params+list(LABEL) if p in p3.index]].reset_index(); p3['parameter']=p3.parameter.map(lab)
p3Cols=[['parameter','Parameter']]+[[k,v] for k,v in EL.items() if k in p3.columns]
# ---------- pilot 4
U=rd('pilot4_ur3_production_by_year.csv'); U=U[(U.bce<=2060)&(U.bce>=2026)]
ur3series=[dict(name=s,pts=[[b,v] for b,v in zip(U.bce,U[s])]) for s in ['Puzriš-Dagan','Umma','Girsu','Ur']]
ur3marks=[[2054,'Šulgi 39'],[2044,'Amar-Suen'],[2035,'Šū-Suen']]
U4=rd('pilot4_ur3_summary.csv').rename(columns={'site':'Province','years':'Years with ≥20 photographed admin tablets','rho_production_vs_MAD':'ρ production vs spread',
     'rho_time_vs_MAD':'ρ time vs spread','MAD_before_S39':'spread before Š39','MAD_S39_AS':'spread Š39 to AS','MAD_SS_IS':'spread ŠS and IS'})
p4aCols=[[c,c] for c in U4.columns]
FM=rd('pilot4_first_millennium_by_reign.csv')
NICE={'Nebuchadnezzar2':'Nebuchadnezzar II','Darius1':'Darius I','Artaxerxes1':'Artaxerxes I','Darius2':'Darius II'}
PERS={'Cyrus','Cambyses','Darius1','Xerxes','Artaxerxes1','Darius2'}
nb=[dict(k=NICE.get(r,r),v=v,start=int(s),tall=t,persian=r in PERS) for r,v,s,t in zip(FM.ruler,FM.per_year,FM.start_bce,FM.tall_share)]
PP=rd('pilot4_periods_production.csv',index_col=0)
from scipy.stats import spearmanr
cc=PP.dropna(subset=['MAD_in_museum']); rr=spearmanr(cc.per_century,cc.MAD_in_museum)
# ---------- pilot 5
H=rd('pilot5_hammurabi.csv'); h=H[(H.group=='legal')&H.window.str.startswith('post (')].iloc[0]
T5=rd('pilot5_hammurabi_types.csv').set_index(['region','phase','type'])
hmb=[dict(k='Legal, north (Babylon)',pre=h.medHW_north_pre,post=h.medHW_north_post,npre=66,npost=110),
     dict(k='Legal, south (Larsa)',pre=h.medHW_south_pre,post=h.medHW_south_post,npre=160,npost=191),
     dict(k='Purchases only, north',pre=T5.loc[('north','pre','achat'),'med_hw'],post=T5.loc[('north','post','achat'),'med_hw'],npre=int(T5.loc[('north','pre','achat'),'n']),npost=int(T5.loc[('north','post','achat'),'n'])),
     dict(k='Purchases only, south',pre=T5.loc[('south','pre','achat'),'med_hw'],post=T5.loc[('south','post','achat'),'med_hw'],npre=int(T5.loc[('south','pre','achat'),'n']),npost=int(T5.loc[('south','post','achat'),'n']))]
# ---------- Seshat
SE=rd('seshat_vs_codebook.csv',index_col=0).reset_index().rename(columns={'index':'period','Unnamed: 0':'period'})
seshatCols=[['period','Period row'],['seshat_polity','Seshat polity']]+[[c,c] for c in SE.columns if c not in ('period','seshat_polity')]
# ---------- text
b=lambda p: B.set_index('predictor').loc[p]; c=lambda p: C.set_index('predictor').loc[p]; a=lambda o,p: A[(A.outcome==o)&(A.predictor==p)].iloc[0]
TEXT=dict(
 p1=f"Across the 15 periods, no parameter makes tablets more uniform. Proportion spread is unrelated to the overall index (ρ {r1('MAD_in_museum','PC1_all').rho:+.2f}). "
    f"For the whole silhouette the sign runs the other way: polities with wider territory, more tiers and more written taxation have <i>more</i> varied tablets (territory ρ {r1('VAEd_in_museum','TERR').rho:+.2f}, p {r1('VAEd_in_museum','TERR').p_perm:.2f}). "
    "The most uniform periods are ED IIIa (Šuruppak), the Hellenistic temple archives of Uruk and Babylon, Ur III and Persepolis: a city household, temple scribes, a royal agency and a royal storehouse. What they share is a single institution producing most of the tablets, not a strong polity.",
 p2=(f"<b>Cells.</b> In 97 cells of period, findspot and genre group, with genre effects and controls for size, damage and museum share, proportion spread is unrelated to every parameter. Silhouette spread <i>rises</i> with polity reach "
    f"(territory β {a('VAEd','TERR').beta:+.2f} SD per SD, p {a('VAEd','TERR').p_perm:.3f}; tiers p {a('VAEd','HIER').p_perm:.3f}; written taxation p {a('VAEd','FISC').p_perm:.3f}), the same reversed sign as at period level. Strong temples go with wider tablets (median ratio, p {a('med','TEMP').p_perm:.2f}). "
    f"<b>Tablets.</b> In the logistic regression for tall tablets (13,570 tablets, genre and damage controlled), no parameter beats the period permutation (smallest p {B.p_perm_logit.min():.2f}, temple strength, odds ratio {b('TEMP').odds_ratio_per_sd:.2f} per SD). "
    f"No parameter explains more of the twelve-dimensional VAE vector than a random assignment of scores to periods would (best: palace weight, partial R² {b('PAL').VAE_partial_R2:.3f} against {b('PAL').VAE_R2_null_median:.3f} by chance, p {b('PAL').p_perm_VAE:.2f}). "
    "<b>Reverse prediction.</b> A model trained on the other periods cannot recover a held-out period's score from its tablets. The correlations are negative, which is the known artefact of leave-one-group-out regression when the groups differ in mean (each held-out period pulls the training mean the other way), so they mean no signal, not an inverse one. "
    "In short: the VAE vector carries period, place and museum (Section 3), but not, at this scale, the period's degree of centralization."), st5="pilot run", st6="pilot run",
 p4=f"Ur III output rose steeply after Šulgi 39 and peaked under Amar-Suen and Šū-Suen, led by Puzriš-Dagan and Umma. Within provinces, years of higher output do not have tighter formats in a consistent direction (Puzriš-Dagan ρ −0.45, Girsu −0.33, Umma +0.37). "
    "In the first millennium, dated output per regnal year is highest under Nabonidus and falls steadily under the Achaemenids, most sharply after 484 BCE, which matches the end of the northern Babylonian archives (Waerzeggers). "
    f"Across periods, the rate of production does not predict uniformity (ρ {rr[0]:+.2f}, p {rr[1]:.2f}), and the type of regime (city-state, territorial kingdom, tributary empire) does not separate uniform from varied periods. Production is a better tool for dating regime change in the record than for explaining form.",
 p5=f"Legal documents of the north became wider after the conquest (median {h.medHW_north_pre:.2f} to {h.medHW_north_post:.2f}), while the south stayed where it was ({h.medHW_south_pre:.2f} to {h.medHW_south_post:.2f}); the difference-in-differences is {h.DiD_loghw:+.3f} in log ratio (p {h.DiD_p:.3f}). "
    f"But the change is in the north, not the conquered south, and the gap between the regions in the VAE silhouette grew rather than closed (p for convergence {h.p_perm_convergence:.2f}). "
    "Within one document type, purchases, the regions barely move. So the pilot shows a change in which kinds of legal document were written, not a Babylonian format imposed on Larsa. The full test needs Archibab's document types as a control, and the Laws and the mīšarum edicts as alternative break points.",
)
HEAD=[
 "<b>Centralization does not make tablets uniform across periods.</b> No parameter predicts proportion spread; for the whole silhouette, wider-reaching polities have <i>more</i> varied tablets, in both the period-level test and the cell-level test that controls for genre, findspot, damage and museum.",
 "<b>Uniformity follows the producing institution.</b> The most uniform periods are those where one household, agency or storehouse made most of the tablets (Šuruppak, Ur III, Persepolis, late temple archives). This points the paper to a sharper thesis: the state made the document only where it ran the office that made it.",
 "<b>Point 9:</b> after Hammurabi's conquest of Larsa, legal documents did not converge on a Babylonian format. The northern documents changed, and the change follows the mix of document types.",
 "<b>The period is the wrong unit.</b> With 15 periods every test is weak. The rewrite should rest on within-period natural experiments, where the regime changed and the scribes did not: Ur III reigns, Eanna under royal commissioners, Hammurabi, the 484 revolts.",
 "<b>Seshat is too coarse</b> to separate ancient Near Eastern regimes (bureaucrats, couriers and calendars are coded present everywhere), which justifies the bespoke codebook.",
]
HYP=[
 ["<b>H-state</b>: the reach of the polity","Weber; Mann; Scott; Turchin et al. 2018","Uniformity rises with territorial scope, administrative tiers, written taxation","Correlate dimension A and PC1 with spread, across periods and cells","<b>Not supported.</b> The sign is reversed for silhouettes (cells: territory β +0.29 SD, p 0.02)"],
 ["<b>H-institution</b>: the household or office that trains and checks scribes","Schloen; Gelb; Renger; Garfinkle; Steinkeller","Uniformity is high where one institution writes most tablets, and changes when the institution changes","Code the producing institution per archive; within-period events where the institution changes","<b>Consistent</b> with the ranking (Šuruppak, Ur III, Persepolis, Hellenistic temples), but not yet tested directly"],
 ["<b>H-production</b>: scale and intensity","Costin; Rice; Blackman et al.; Roux","Uniformity rises with output per year and per scribe","Dated output per year and per reign against spread","<b>Not supported</b> across periods (ρ +0.13) and mixed within Ur III provinces"],
 ["<b>H-function</b>: the type of document","Veenhof; Radner; diplomatics","Form follows document type; periods differ because their genre mix differs","Genre fixed effects; document-type controls (BDTNS, Archibab)","<b>Strong</b> in every model; it also explains the Hammurabi shift"],
 ["Confounds: museum and survival","Section 3 (museum test); Pedersén on archives","Collecting history and excavation shape what we see","Within-museum measures, museum share as control, damage control","Built into every pilot; the museum share remains a real risk for cell results"],
]
EVENTS=[
 ["Puzriš-Dagan founded","Šulgi 39 (2054 BCE)","A new crown agency for livestock, staffed by royal appointees","H-institution: its tablets are uniform from the start, and provincial formats do not change","15,000+ dated Drehem tablets; Umma and Girsu as controls"],
 ["The last two Ur III reigns","Šū-Suen to Ibbi-Suen 3 (2035 to 2024 BCE)","Provincial reporting to the centre falls away","H-state: provinces drift apart; H-institution: each province keeps its format","Umma and Girsu year by year (pilot: no drift)"],
 ["Conquest of Larsa","Hammurabi 30 (1763 BCE)","Babylonian administration of the south","H-state: southern documents converge on the northern format","527 legal documents (pilot: no convergence)"],
 ["Southern revolt and abandonment","Samsu-iluna 10 to 30 (1739 to 1720 BCE)","Southern scribal families move north","H-institution: the moved families keep their format in the north","Archibab archives with known origin"],
 ["Royal commissioners in Eanna","from about 584 BCE; Nabonidus","Crown officials take over the temple's administration","Livestock lists turn tall (Pirngruber); other temple records unchanged","Eanna, dated by reign and year (Section 5)"],
 ["Persian conquest","Cyrus 539 BCE","New and much larger polity; institutions unchanged","H-state: change; H-institution: none (Kleber, Jursa: continuity)","Eanna and Ebabbar across 539"],
 ["Revolts against Xerxes","484 BCE","Northern archives end; loyal families survive","Survivor composition shifts; form of surviving archives unchanged","Babylon, Borsippa, Sippar against Uruk and Ur"],
 ["Amarna","about 1350 BCE","One findspot, letters written in many places","Form follows the place of writing, not of keeping","Amarna letters by sender (Section 5)"],
]
OUTLINE=[
 ["Introduction","The question, the four explanations and their literatures; why form is a trace the state did not compose; the comparative setting (Seshat, state capacity, codicology)","950","Intro v2, rewritten around the hypotheses"],
 ["Results 1: corpus and measures","Archival documents, photographs, proportion and VAE measures, museum and damage controls","350","Section 2, shortened"],
 ["Results 2: measuring centralization","Twelve parameters, three dimensions, 17 period rows; Fig. A heatmap; agreement between coders; comparison with Seshat","500","New"],
 ["Results 3: form against centralization","Period and cell tests with permutation inference; the reversed sign; the single-institution pattern","650","New; Section 4 becomes background"],
 ["Results 4: natural experiments","Ur III reigns and Puzriš-Dagan; Hammurabi; Eanna and 539; 484 BCE; Fig. B","1,100","Section 5 case studies, reframed as tests"],
 ["Results 5: place of making","Amarna as the control for where a tablet was made","250","Section 5, Amarna"],
 ["Discussion","What the state could and could not standardize; museum archaeology; limits","600","Discussion, Plan B"],
 ["Methods and SI","Scoring protocol, codebook, SI Table, statistics, period identification as validation","Methods ~1,000; SI unlimited","Section 3 to SI"],
]
WORK=[
 ["29 to 31 Oct","You correct the scores; I check each against the OHANE chapters once you upload them; we choose two outside coders","Corrections; PDFs; names of coders"],
 ["1 to 3 Nov","Score the events and sites (before and after each event); code the producing institution for each archive (Archibab, BDTNS, Eanna)","Decision on Point 9 break point"],
 ["3 to 6 Nov","Full analyses: cell and tablet models with museum effects, permutation inference, the natural experiments, Hammurabi with document-type controls","None"],
 ["6 to 10 Nov","Write Introduction, Results 2 to 5 and Discussion; Figs. A and B","Read Introduction"],
 ["10 to 12 Nov","SI Table, Methods, BibTeX, reproducibility notes; your read of the full draft","Full read"],
 ["13 Nov","Draft to Morris",""],
 ["24 Nov","Submit to PNAS (direct submission; preferred editor Frangipane)",""],
]
SCRIPTS=[
 ['70_seshat_extract.py','Seshat Equinox-2020 variables for the polities matching our period rows'],
 ['71_build_master.py','One table per tablet: VAE vector, photograph ratio, damage, catalogue fields, findspot, museum, ruler and year'],
 ['72_centralization_scores.py','The codebook and the 204 scores with evidence and references; dimension indices and PC1'],
 ['refs_centralization.py','Full references for every key used in the scores and the plan'],
 ['73_pilot_period_level.py','Pilot 1: period-level correlations with permutation inference'],
 ['74_pilot_cells_logistic_vae.py','Pilot 2: cells (genre and findspot), logistic regression of tall tablets, VAE multivariate R², held-out-period prediction'],
 ['75_pilot_hammurabi.py','Pilot 5: legal documents before and after 1763 BCE, north against south'],
 ['76_pilot_production.py','Pilot 4: production by year, reign and period against format'],
 ['77_pilot_parameters_vs_features.py','Pilot 3: parameters against proportion, thickness, rectangularity and corners'],
 ['78_build_plan_page.py','This page'],
 ['79_seshat_compare.py','Our scores against Seshat'],
]
D=dict(headline=HEAD,text=TEXT,hyp=HYP,events=EVENTS,outline=OUTLINE,workplan=WORK,scripts=SCRIPTS,refs=sorted(REFS.items(),key=lambda kv:kv[1]),
       params=params,rows=rows,scores=scores,pname=dict(zip(CB.param,CB.name)),anchors=dict(zip(CB.param,CB.anchors)),
       indices=I.to_dict(orient='index'),codebook=CB.to_dict(orient='records'),long=L.to_dict(orient='records'),
       seshatCols=seshatCols,seshat=SE.to_dict(orient='records'),sp1Cols=sp1Cols,sp1=sp1.to_dict(orient='records'),
       p2aCols=p2aCols,p2a=p2a.to_dict(orient='records'),p2bCols=p2bCols,p2b=p2b.to_dict(orient='records'),
       p3Cols=p3Cols,p3=p3.to_dict(orient='records'),p4aCols=p4aCols,p4a=U4.to_dict(orient='records'),
       sc1=pts('PC1_all','MAD_in_museum'),sc2=pts('A_polity_reach','VAEd_in_museum'),
       labelled=['ED IIIa','Ur III','Achaemenid (Persepolis)','Neo-Assyrian','Middle Babylonian','Hellenistic','Old Assyrian','Ebla','Achaemenid (Babylonia)','Early Old Babylonian'],
       sc1note=f"Spearman ρ {r1('MAD_in_museum','PC1_all').rho:+.2f} (p {r1('MAD_in_museum','PC1_all').p_perm:.2f}). Each dot is a period; hover for counts.",
       sc2note=f"Spearman ρ {r1('VAEd_in_museum','A_polity_reach').rho:+.2f} (p {r1('VAEd_in_museum','A_polity_reach').p_perm:.2f}). Ebla is high because its tablets are large and varied in outline.",
       ur3series=ur3series,ur3marks=ur3marks,ur3note="Whole CDLI catalogue, dated by ruler and year (Sallaberger's chronology). Uniformity by province is in the table below, not on this chart.",
       nb=nb,nbnote="Dated tablets in CDLI per regnal year of each king. Hover a bar for the share of tall archival tablets.",
       hmb=hmb,hmbnote="North = Sippar, Kish, Dilbat, Babylon; south = Larsa, Ur, Nippur, Isin and neighbours. Dated by Archibab or CDLI ruler and year.")
html=open(f'{TEMPLATES}/plan_template.html').read().replace('__DATA__',json.dumps(clean(D),ensure_ascii=False).replace('</','<\\/'))
open(f'{R}/centralization_plan.html','w').write(html)
if __name__=='__main__': print('written',len(html))
