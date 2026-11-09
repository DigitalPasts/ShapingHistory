"""Index the five OHANE volumes by page so that every quotation can be cited exactly.
Input: OHANE_{I..V}.pdf (K. Radner, N. Moeller, D. T. Potts eds., The Oxford History of the Ancient Near East, 2020-2023),
from ShG's Dropbox (Research-current/Deeplomatics/Literature), converted with `pdftotext -layout`.
Output: /home/user/lit/ohane/ohane_pages.parquet, one row per PDF page: volume, PDF page, printed page (volumes II, III and V
carry running heads with page numbers; the copies of volumes I and IV do not, so they are cited by chapter and section),
chapter number, author, chapter title, current section number (e.g. 13.4.2), and the page text.
Also: ohane_chapters.csv (chapter, author, title, first and last PDF page)."""
from _paths import LIT
import re, pandas as pd
D=LIT+'/ohane'; rows=[]
for v in ['I','II','III','IV','V']:
    pages=open(f'{D}/OHANE_{v}.txt',encoding='utf-8',errors='ignore').read().split('\f')
    chap=None; head=None; sec=None
    for i,t in enumerate(pages):
        t=t.replace('​','').replace('­','')
        lines=[l.strip() for l in t.splitlines() if l.strip()]
        # chapter opening page: first line is the chapter number, followed (within the page) by the heading "N.1."
        for k in (0,1):
            if len(lines)>k+1 and re.fullmatch(r'\d{1,2}',lines[k]) and re.search(rf'(?m)^\s*{lines[k]}\.1\.',t[:2500]):
                chap=int(lines[k]); head=' / '.join(re.sub(r'\s{2,}',' / ',l) for l in lines[k+1:k+4] if not re.match(rf'^{chap}\.1',l)); sec=f'{chap}.1'; break
        printed=None
        if len(lines)>=2:
            m=re.search(r'\s(\d{1,4})$',lines[1]); m2=re.match(r'^(\d{1,4})\s',lines[1])
            if m and not re.match(r'^\d+\.\d',lines[1]): printed=int(m.group(1))
            elif m2: printed=int(m2.group(1))
        for s in re.findall(r'(?m)^\s*(\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)\.\s+\S',t):
            if chap and s.split('.')[0]==str(chap): sec=s
        rows.append(dict(vol=v,pdf=i+1,printed=printed,chapter=chap,heading=head,section=sec,text=t))
P=pd.DataFrame(rows)
# chapter 15 of volume II (From Assur to the Levant) opens without the usual number line; set it by hand (opening on PDF p. 332)
m=(P.vol=='II')&(P.pdf>=332)&(P.chapter==14); P.loc[m,'chapter']=15; P.loc[m,'heading']='The Middle East after the Fall of Ur / From Assur to the Levant'
# printed page numbers: keep only values consistent with the PDF offset of the volume, then fill gaps (chapter openings) from the offset
for v,g in P.groupby('vol'):
    off=(g.printed-g.pdf).dropna()
    if len(off)>100:
        o=off.mode().iloc[0]; P.loc[g.index,'printed']=g.pdf+o
    else: P.loc[g.index,'printed']=None
P.to_parquet(f'{D}/ohane_pages.parquet')
C=P.dropna(subset=['chapter']).groupby(['vol','chapter']).agg(heading=('heading','first'),pdf0=('pdf','min'),pdf1=('pdf','max'),
   p0=('printed','min'),p1=('printed','max')).reset_index()
C.to_csv(f'{D}/ohane_chapters.csv',index=False)
if __name__=='__main__':
    pd.set_option('display.width',250); print(C.to_string())
