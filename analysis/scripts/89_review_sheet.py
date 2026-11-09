"""Review workbook for ShG: scores with ranges, every quoted statement with its citation, gaps, and the statistics.
Opens in Excel or Google Sheets; the 'ShG verdict' and 'ShG comment' columns are for the review."""
from _paths import WORK
import json, pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
C=WORK+'/centralization'; OUT=f'{C}/centralization_literature_review.xlsx'
MAIN=['ED IIIa','ED IIIb','Ebla','Old Akkadian','Ur III','Early Old Babylonian','Old Babylonian','Old Assyrian','Middle Babylonian','Middle Assyrian','Neo-Assyrian','Neo-Babylonian','Achaemenid','Hellenistic']
NAMES={'TERR':'Territorial reach','HIER':'Administrative hierarchy','FISC':'Fiscal extraction','COMM':'Communications','PAL':'Palace economy','TEMP':'Temple economy','TCTL':'Royal control of temples','PRIV':'Private sector (reversed in indices)','BUR':'Standardized bureaucracy','SCHOOL':'Scribal training','LAW':'Royal law','STD':'Standard measures and calendar'}
L=pd.read_csv(f'{C}/lit_scores_long.csv'); E=pd.read_csv(f'{C}/lit_evidence_long.csv')
L['group']=L.period.map(lambda p:'main' if p in MAIN else 'SI')
L['parameter']=L.param.map(NAMES); L['range']=L.lo.astype(str)+'-'+L.hi.astype(str)
L['changed_from_prior']=(L.source=='literature')&(L.score!=L.prior)
S=L[['group','period','param','parameter','score','range','contested','conf','source','n_entries','n_support','n_sources','prior','changed_from_prior']].copy()
S['ShG verdict']=''; S['ShG comment']=''
E=E.sort_values(['period','param','stance']); E['parameter']=E.param.map(NAMES)
Ev=E[['period','param','parameter','score','stance','quote','where','key','note','region']].rename(columns={'score':'score implied','where':'citation','key':'BibTeX key'})
Ev['ShG verdict (accept / reject / rescore)']=''; Ev['ShG comment']=''
G=json.load(open(f'{C}/lit_gaps.json')); Gp=pd.DataFrame([dict(period=p,param=k,literature_to_add=v) for p,d in G.items() for k,v in d.items()])
W=L[L.group=='main'].pivot(index='period',columns='param',values='score').loc[MAIN][list(NAMES)]
with pd.ExcelWriter(OUT,engine='openpyxl') as x:
    pd.DataFrame({'Read me':[
     'Each score (0-3) is derived mechanically from the quoted statements in the Evidence sheet (rules in script 85_build_scores.py).',
     'Point score = median of the scores implied by supporting statements; range = all statements; contested = a contesting statement disagrees.',
     'Confidence H/M/L; source = literature, or prior (cells not yet grounded in a quotation, to be filled).',
     'Please mark each statement in Evidence: accept, reject, or rescore (give the score you think the statement implies). Comments are welcome.',
     'OHANE vols I and IV have no printed page numbers in the Dropbox PDFs: cited by section and PDF page. Zotero gives Schrakamp ch. 9 start as p. 612 = PDF 540, so vol I printed page is probably PDF + 72 (to verify).',
     'Drive-only sources (Pirngruber 2017, Monerie and Clancier 2023) carry page numbers marked "to verify".']}).to_excel(x,sheet_name='Read me',index=False)
    W.to_excel(x,sheet_name='Score matrix (main)')
    S.to_excel(x,sheet_name='Scores',index=False); Ev.to_excel(x,sheet_name='Evidence',index=False); Gp.to_excel(x,sheet_name='Gaps and requests',index=False)
    pd.read_csv(f'{C}/reading_log.tsv',sep='\t').to_excel(x,sheet_name='Reading log',index=False)
    for f,sh in [('stats_period_table.csv','Stats period table'),('stats_spearman.csv','Stats Spearman'),('stats_wild_cluster.csv','Stats wild cluster'),('hammurabi_breaks.csv','Hammurabi breaks'),('hammurabi_break_scan.csv','Hammurabi scan')]:
        pd.read_csv(f'{C}/{f}').to_excel(x,sheet_name=sh,index=False)
wb=load_workbook(OUT)
for ws in wb.worksheets:
    for c in ws[1]: c.font=Font(bold=True); c.fill=PatternFill('solid',fgColor='DDE6EE')
    ws.freeze_panes='A2'
    for col in ws.columns:
        L_=max(len(str(c.value or '')) for c in col[:200]); ws.column_dimensions[col[0].column_letter].width=min(max(10,L_*0.9),70)
ws=wb['Evidence']
for row in ws.iter_rows(min_row=2):
    for c in row: c.alignment=Alignment(wrap_text=True,vertical='top')
ws.column_dimensions['F'].width=90
wb.save(OUT); print(OUT,len(Ev),'statements')
