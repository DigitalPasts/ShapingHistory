"""Assessment worksheet for ShG: re-score every cell from the quoted literature, mark whether a score rests on evidence
of absence or on a silent record, and see the indices and their rank correlation with tablet uniformity recompute live.
Opens in Excel or Google Sheets. Inputs: centralization_codebook.csv, lit_scores_long.csv, lit_evidence_long.csv,
stats_period_table.csv. Output: centralization/centralization_assessment_worksheet.xlsx"""
from _paths import SHARED, WORK
import re, pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import ColorScaleRule, FormulaRule
from openpyxl.utils import get_column_letter as CL
C=WORK+'/centralization'; PJ=SHARED+'/centralization'
OUT=f'{C}/centralization_assessment_worksheet.xlsx'
MAIN=['ED IIIa','ED IIIb','Ebla','Old Akkadian','Ur III','Early Old Babylonian','Old Babylonian','Old Assyrian',
      'Middle Babylonian','Middle Assyrian','Neo-Assyrian','Neo-Babylonian','Achaemenid','Hellenistic']
SI=['Achaemenid (Babylonia)','Achaemenid (Persepolis)','Hittite','Middle Elamite']
PARAMS=['TERR','HIER','FISC','COMM','PAL','TEMP','TCTL','PRIV','BUR','SCHOOL','LAW','STD']
DIMS={'A':['TERR','HIER','FISC','COMM'],'B':['PAL','TEMP','TCTL','PRIV'],'C':['BUR','SCHOOL','LAW','STD']}
CB=pd.read_csv(f'{PJ}/centralization_codebook.csv').set_index('param')
L=pd.read_csv(f'{C}/lit_scores_long.csv'); E=pd.read_csv(f'{C}/lit_evidence_long.csv')
T=pd.read_csv(f'{C}/stats_period_table.csv').set_index('period')

# Where each parameter comes from. Seshat analogue = the Seshat Equinox-2020 variable it matches (script 79).
ORIGIN={
 'TERR':('Polity territory','Mann 1986 (extensive power); Seshat Social Scale','Size of Sargonic and Ur III states vs. city-states; "empire" for Akkad and Ur III (Steinkeller; Sallaberger)'),
 'HIER':('Administrative levels','Weber (bureaucratic hierarchy); Seshat Hierarchical Complexity','Provincial governors (ensi2) under Ur III; OB governors and šāpirum; NA provinces'),
 'FISC':('none','Monson and Scheidel 2015; Hanson and Sigman 2021 (extractive capacity); Scott 2017','bala and gun2 ma-da (Sharlach; Steinkeller); ilkum; Achaemenid satrapal taxes (Jursa)'),
 'COMM':('Couriers; Postal stations','Mann 1984 (infrastructural power)','Ur III messenger texts (Sallaberger); OB and Mari letters (Charpin); NA royal road (Radner)'),
 'PAL':('none','Gelb 1979; Diakonoff 1982; Renger 1994; Schloen 2001','Palace vs. temple economy debate: temple-city model (Deimel, Falkenstein) and its critique'),
 'TEMP':('none','same as PAL','Same debate; Jursa 2010 and Kleber 2008 for 1st millennium temples'),
 'TCTL':('none','Jursa 2010; Kleber 2008; Sallaberger and Westenholz 1999','Royal appointees in temples (šabra, qīpu, ša rēš šarri); Nabonidus and Eanna'),
 'PRIV':('none','Diakonoff two-sector model; Van De Mieroop 1992; Garfinkle 2012; Schloen 2001','Private sector debate (Diakonoff vs. Gelb); OB private archives; NB family archives'),
 'BUR':('Full-time bureaucrats (partial)','Weber 1922; Postgate 2013; Steinkeller 2003','Ur III accounting and the "bureaucratic state" (Steinkeller; Dahl; Garfinkle critique)'),
 'SCHOOL':('Examination system (poor fit)','Veldhuis 2011; Robson 2001; Gesche 2001; Visicato 2000','Edubba vs. household schooling (Charpin; Veldhuis; Tinney); Ur III royal scribal training'),
 'LAW':('Formal legal code; Judges; Courts','Westbrook 2003; Charpin 2010','Are law collections legislation? (Kraus, Bottéro, Westbrook, Charpin); mīšarum edicts'),
 'STD':('Calendar (partial)','Scott 1998 (legibility); Brambor et al. 2020 (information capacity)','Sargonic gur of Akkade; Ur III standard calendar and gur lugal; Achaemenid royal measures'),
}
# What 0 means for each parameter: 'low' = a real, low state of affairs; 'absence' = the anchor itself is "no evidence".
ZERO={p:'absence' if p in ('COMM','BUR','LAW') else 'low' for p in PARAMS}
# Hand reading of the eight cells that currently score 0 (see Evidence sheet for the quotations).
ZNOTE={
 ('ED IIIa','PRIV'):'Rounding: one statement implies 0 (Steinkeller, private sector "poorly developed"), one implies 1 (Bartash, sale contracts). The rule rounds a 0/1 tie down. Evidence of a small sector, not of absence.',
 ('Ebla','TEMP'):'Evidence of absence: Steinkeller says the temple household "did not exist" at Ebla.',
 ('Ebla','PRIV'):'Rounding: 0/1 tie rounded down (Steinkeller allows private land; Bartash sees the palace lens).',
 ('Old Assyrian','TERR'):'Real low state: Assur is a city-state (Arkhipov). The commercial network is not territory.',
 ('Old Assyrian','PAL'):'Evidence of absence from the record: OA texts "never mention a palace" (Veenhof).',
 ('Old Assyrian','SCHOOL'):'Real low state: household literacy among merchants (Larsen); Larsen p. 85 school texts qualify it.',
 ('Hittite','PRIV'):'Silent record: few private records survive; Van den Hout warns this may be a "false equilibrium". Candidate for "insufficient evidence".',
 ('Middle Elamite','PRIV'):'Silent record: no private documents survive for the period (Mofidi Nasrabadi). Candidate for "insufficient evidence".',
}
def short(k):
    m=re.match(r'([a-z]+?)(?=[A-Z]|$)',str(k)); y=re.search(r'(\d{4})[a-z]?$',str(k))
    a=(m.group(1) if m else str(k))
    FIX={'vandemieroop':'Van De Mieroop','vandenhout':'van den Hout','mofidi':'Mofidi Nasrabadi','mofidinasrabadi':'Mofidi Nasrabadi',
         'degraef':'De Graef','coro':'Corò','malbran':'Malbran-Labat','basello':'Basello and Giovinazzo','sassmannshausen':'Sassmannshausen'}
    a=FIX.get(a,a[:1].upper()+a[1:])
    return f"{a} {y.group(1) if y else ''}".strip()

wb=Workbook()
H=Font(bold=True,color='FFFFFF'); HF=PatternFill('solid',fgColor='34495E'); YOU=PatternFill('solid',fgColor='FFF4CC')
WR=Alignment(wrap_text=True,vertical='top'); thin=Side(style='thin',color='BBBBBB')
def header(ws,cols,row=1,fill=HF):
    for j,c in enumerate(cols,1):
        x=ws.cell(row,j,c); x.font=H; x.fill=fill; x.alignment=Alignment(wrap_text=True,vertical='center')

# 1 Read me
ws=wb.active; ws.title='Read me'
txt=[
 ('How to use this worksheet',None),
 ('1. Work in the "Assess" sheet. Each row is one period x parameter cell. Grey columns are my scoring; yellow columns are yours.',None),
 ('2. "Your score": 0, 1, 2 or 3. Leave blank to keep my score.',None),
 ('3. "Evidence status" says what kind of ground the score stands on. Choose "Insufficient evidence" to take the cell out of the indices altogether (it is then blank, not 0).',None),
 ('4. "Statements" opens the quotations for that cell in the Evidence sheet. You can also filter Evidence by the Cell column.',None),
 ('5. The "Matrix and indices" sheet recomputes the four indices from your scores (or mine where you left a blank) and their Spearman correlation with tablet uniformity (MAD), next to my values.',None),
 ('',None),
 ('Is 0 a null?',None),
 ('No. 0 is the lowest anchor of each scale, a real low state such as "single city-state" (TERR) or "marginal" (PAL, TEMP). For COMM, BUR and LAW the 0 anchor reads "none known / no evidence", so a 0 there would mix absence with silence; no main cell currently scores 0 on these three.',None),
 ('Thin evidence is not coded as 0. It shows as confidence L, a wide range (lo-hi), and few sources. Eight cells score 0; the "Zero reading" column says for each whether it is evidence of absence, a real low state, a rounding tie, or a silent record.',None),
 ('PAL, TEMP and PRIV measure weight in the written record, so recovery bias (which archives were excavated) affects them. Mark such cells "Silent record" if you think the score reflects survival rather than history.',None),
 ('',None),
 ('Where the parameters come from',None),
 ('A combination. I drafted the 12 parameters on 28 Oct 2026 from three sources: (a) Seshat variables where one exists (territory, administrative levels, couriers, legal code), (b) general state-capacity theory (Mann, Weber, Scott, Monson and Scheidel), and (c) the debates in Assyriology about palace, temple and private sectors, schooling and law. The Codebook sheet gives all three for each parameter. Seshat alone was too coarse: most of its variables do not vary across our periods. The grouping into A, B and C is mine and is not from a published scheme.',None),
 ('',None),
 ('Scoring rules (script 85_build_scores.py)',None),
 ('Point score = median of the scores implied by supporting statements, rounded down at .5. Range = all statements. Contested = a contesting statement implies a different score. Confidence H = 2+ supporting, no contest, no spread; M = 1+ supporting and spread <= 1; L = otherwise. PRIV is reversed (3 - PRIV) in index B.',None),
]
for i,(t,_) in enumerate(txt,1):
    c=ws.cell(i,1,t); c.alignment=WR
    if t and not t[0].isdigit() and len(t)<45: c.font=Font(bold=True,size=12)
ws.column_dimensions['A'].width=130

# 2 Codebook
ws=wb.create_sheet('Codebook')
cols=['Param','Dimension','Name','0','1','2','3','What 0 means','Seshat analogue','Theory','Assyriological debate','Proxy in the record']
header(ws,cols)
for i,p in enumerate(PARAMS,2):
    a=[s.split(' ',1)[1] if ' ' in s else s for s in CB.loc[p,'anchors'].split(' | ')]
    row=[p,CB.loc[p,'dimension'],CB.loc[p,'name']]+a+['"No evidence" (absence and silence not separated)' if ZERO[p]=='absence' else 'A real low state']+list(ORIGIN[p])+[CB.loc[p,'proxy']]
    for j,v in enumerate(row,1): ws.cell(i,j,v).alignment=WR
for j,w in enumerate([8,9,26,22,22,22,26,22,18,30,40,30],1): ws.column_dimensions[CL(j)].width=w
ws.freeze_panes='D2'

# 5 Evidence (built first so Assess can link to rows)
E['Cell']=E.period+' | '+E.param
E['ord_p']=E.period.map({p:i for i,p in enumerate(MAIN+SI)}).fillna(99); E['ord_q']=E.param.map(PARAMS.index)
E=E.sort_values(['ord_p','ord_q','stance','score']).reset_index(drop=True)
we=wb.create_sheet('Evidence')
ecols=['Cell','Period','Param','Score implied','Stance','Source','Citation','Quotation','Note','BibTeX key','Your reading (accept / reject / rescore)','Your comment']
header(we,ecols); first={}
for i,r in enumerate(E.itertuples(),2):
    first.setdefault(r.Cell,i)
    row=[r.Cell,r.period,r.param,int(r.score),r.stance,short(r.key),r.where,r.quote,(r.note if isinstance(r.note,str) else ''),r.key,'','']
    for j,v in enumerate(row,1):
        c=we.cell(i,j,v); c.alignment=WR
        if j>=11: c.fill=YOU
for j,w in enumerate([24,16,8,8,10,18,26,90,30,28,18,30],1): we.column_dimensions[CL(j)].width=w
we.freeze_panes='B2'; we.auto_filter.ref=f'A1:{CL(len(ecols))}{len(E)+1}'
dvr=DataValidation(type='list',formula1='"accept,reject,rescore 0,rescore 1,rescore 2,rescore 3"',allow_blank=True)
we.add_data_validation(dvr); dvr.add(f'K2:K{len(E)+1}')

# 3 Assess
wa=wb.create_sheet('Assess',1)
acols=['Key','Group','Period','Param','Name','Anchors (0 | 1 | 2 | 3)','My score','Range','Confidence','Sources','Supports / qualifies / contests','Contested','Statements (score, source)','Zero reading','Open statements',
       'Your score','Evidence status','Your confidence','Source to add','Your comment','Used in indices','Differs from mine']
header(wa,acols)
for j in range(16,21): wa.cell(1,j).fill=PatternFill('solid',fgColor='B7950B')
STAT='"Evidence of presence,Evidence of absence,Silent record,Insufficient evidence"'
rows=L[L.period.isin(MAIN+SI)].copy()
rows['op']=rows.period.map({p:i for i,p in enumerate(MAIN+SI)}); rows['oq']=rows.param.map(PARAMS.index)
rows=rows.sort_values(['op','oq'])
for i,r in enumerate(rows.itertuples(),2):
    key=f'{r.period} | {r.param}'; g=E[E.Cell==key]
    stm='; '.join(f'{int(s.score)} {s.stance[0]}: {short(s.key)}' for s in g.itertuples())
    cnt=f"{(g.stance=='supports').sum()} / {(g.stance=='qualifies').sum()} / {(g.stance=='contests').sum()}"
    anchors=' | '.join(s.split(' ',1)[1] for s in CB.loc[r.param,'anchors'].split(' | '))
    row=[key,'main' if r.period in MAIN else 'SI',r.period,r.param,CB.loc[r.param,'name'],anchors,int(r.score),f'{r.lo}-{r.hi}',r.conf,int(r.n_sources),cnt,
         'yes' if r.contested else '',stm,ZNOTE.get((r.period,r.param),'')]
    for j,v in enumerate(row,1): wa.cell(i,j,v).alignment=WR
    if key in first:
        c=wa.cell(i,15,f'=HYPERLINK("#\'Evidence\'!A{first[key]}","{len(g)} statements")'); c.font=Font(color='1F4E9A',underline='single')
    for j in range(16,21): wa.cell(i,j).fill=YOU
    wa.cell(i,21,f'=IF(Q{i}="Insufficient evidence","",IF(P{i}="",G{i},P{i}))')
    wa.cell(i,22,f'=IF(AND(P{i}<>"",P{i}<>G{i}),"changed",IF(Q{i}="Insufficient evidence","dropped",""))')
n=len(rows)+1
for rng,f in [(f'P2:P{n}','"0,1,2,3"'),(f'Q2:Q{n}',STAT),(f'R2:R{n}','"H,M,L"')]:
    dv=DataValidation(type='list',formula1=f,allow_blank=True); wa.add_data_validation(dv); dv.add(rng)
for j,w in enumerate([22,6,18,8,20,40,7,7,6,7,10,7,44,40,12,8,16,8,22,30,8,9],1): wa.column_dimensions[CL(j)].width=w
wa.freeze_panes='E2'; wa.auto_filter.ref=f'A1:V{n}'
wa.conditional_formatting.add(f'G2:G{n}',FormulaRule(formula=[f'$G2=0'],fill=PatternFill('solid',fgColor='F5B7B1')))
wa.conditional_formatting.add(f'I2:I{n}',FormulaRule(formula=[f'$I2="L"'],fill=PatternFill('solid',fgColor='FADBD8')))

# 4 Matrix and indices (live formulas)
wm=wb.create_sheet('Matrix and indices',2)
ORD=['TERR','HIER','FISC','COMM','PAL','TEMP','TCTL','PRIVrev','BUR','SCHOOL','LAW','STD']
mc=['Period']+ORD+['PRIV (raw)','A polity reach','B institutional economy','C control of writing','Mean of 12','MAD (uniformity)',
    'My A','My B','My C','My mean','rank MAD','rank A','rank B','rank C','rank mean']
wm.cell(1,1,'Your scores (my score where you left a blank; blank where you chose "Insufficient evidence"). PRIV enters index B reversed (3 - PRIV). Lower MAD = more uniform tablets.').font=Font(italic=True)
header(wm,mc,row=2)
for i,per in enumerate(MAIN,3):
    wm.cell(i,1,per)
    for j,p in enumerate(ORD,2):
        if p=='PRIVrev': f=f'=IF(N{i}="","",3-N{i})'
        else: f=f'=IFERROR(INDEX(Assess!$U$2:$U${n},MATCH($A{i}&" | {p}",Assess!$A$2:$A${n},0)),"")'
        wm.cell(i,j,f)
    wm.cell(i,14,f'=IFERROR(INDEX(Assess!$U$2:$U${n},MATCH($A{i}&" | PRIV",Assess!$A$2:$A${n},0)),"")')
    wm.cell(i,15,f'=IFERROR(AVERAGE(B{i}:E{i}),"")'); wm.cell(i,16,f'=IFERROR(AVERAGE(F{i}:I{i}),"")')
    wm.cell(i,17,f'=IFERROR(AVERAGE(J{i}:M{i}),"")'); wm.cell(i,18,f'=IFERROR(AVERAGE(B{i}:M{i}),"")')
    wm.cell(i,19,float(T.loc[per,'MAD']))
    for j,c in enumerate(['A_polity_reach','B_institutional_economy','C_control_of_writing','mean_all'],20): wm.cell(i,j,round(float(T.loc[per,c]),3))
    for j,src in zip(range(24,29),['S','O','P','Q','R']): wm.cell(i,j,f'=IFERROR(_xlfn.RANK.AVG({src}{i},${src}$3:${src}$16,1),"")')
last=2+len(MAIN); r0=last+2
wm.cell(r0,1,'Spearman rho with MAD (rank correlation, 14 periods)').font=Font(bold=True)
wm.cell(r0+1,1,'Your scores'); wm.cell(r0+2,1,'My scores')
for j,(rk,mine) in enumerate([('Y','T'),('Z','U'),('AA','V'),('AB','W')],15):
    wm.cell(r0,j,['A','B','C','Mean'][j-15]).font=Font(bold=True)
    wm.cell(r0+1,j,f'=CORREL($X$3:$X${last},{rk}3:{rk}{last})').number_format='0.00'
    wm.cell(r0+2,j,f'=CORREL(ARRAYFORMULA(RANK.AVG($S$3:$S${last},$S$3:$S${last},1)),ARRAYFORMULA(RANK.AVG({mine}3:{mine}{last},{mine}3:{mine}{last},1)))').number_format='0.00'
# my rho as fixed values from script 86 (the line above needs Sheets); overwrite with values for Excel safety
SP=pd.read_csv(f'{C}/stats_spearman.csv'); SP=SP[SP.outcome=='MAD'].set_index('index')
for j,k in enumerate(['A_polity_reach','B_institutional_economy','C_control_of_writing','mean_all'],15):
    wm.cell(r0+2,j,round(float(SP.loc[k,'rho']),2))
wm.cell(r0+3,1,'Negative rho = higher index goes with more uniform tablets. The p-values and uncertainty draws come from rerunning script 86 on your scores.').font=Font(italic=True)
for j in range(1,len(mc)+1): wm.column_dimensions[CL(j)].width=9
wm.column_dimensions['A'].width=22
for j in range(15,24):
    for i in range(3,last+1): wm.cell(i,j).number_format='0.00'
wm.conditional_formatting.add(f'B3:N{last}',ColorScaleRule(start_type='num',start_value=0,start_color='F7FBFF',end_type='num',end_value=3,end_color='2E6DA4'))
wm.freeze_panes='B3'
for ws_ in [wa,we]:
    for c in ws_[1]: c.alignment=Alignment(wrap_text=True,vertical='center')
wb.save(OUT); print(OUT,'cells',n-1,'statements',len(E))
