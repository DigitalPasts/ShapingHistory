"""Old Assyrian metadata from OARE (Old Assyrian Research Environment, BYU), published_texts.csv as released for the
Deep Past Challenge (Kaggle, deep-past-initiative-machine-translation); file supplied by ShG, 9 Nov 2026.
Links OARE records to our photographed Old Assyrian tablets by CDLI P-number and keeps, per tablet:
OARE genre, object (tablet / envelope; a CDLI number that holds both is flagged), eponym named in the text
(li-mu-um / li-mì-im formula; name only, years need the Kültepe eponym list), and simple text measures
(words, logogram share) for later orthography work. Output: oare/oare_matched.csv, turning/oare_summary.csv"""
from _paths import WORK
import pandas as pd, re
R=WORK
d=pd.read_csv(f'{R}/oare/published_texts.csv',low_memory=False)
d['id']=pd.to_numeric(d.cdli_id.str.extract(r'P(\d+)')[0],errors='coerce')
m=pd.read_parquet(f'{R}/master_tablets.parquet',columns=['id','period','genres','collections'])
oa=m[m.period=='Old Assyrian']
h=oa.merge(d,on='id')
h['object']=h.description.str.extract(r'Cuneiform (\w+)')[0]
t=h.transliteration.fillna('')
h['eponym']=t.str.extract(r'li-m(?:u-um|ì-im|ì|u)\s+(?:ša\s+qá-té\s+)?((?:[^\s<]+)(?:\s+DUMU\s+[^\s<]+)?)')[0]
h.loc[h.eponym.fillna('').str.match(r'^(ša|[A-Z]+(\.[A-Z]+)+)$'),'eponym']=None      # 'ša' without qātē, or a logogram: not a name
w=t.str.replace(r'<gap>','',regex=True).str.split()
h['n_words']=w.str.len()
h['logogram_share']=w.apply(lambda x: sum(bool(re.search(r'[A-ZŠḪṢṬ]{2,}',s)) for s in x)/len(x) if len(x) else None)
g=h.groupby('id')
out=g.agg(oare_ids=('oare_id',lambda s:' | '.join(s)),labels=('label',lambda s:' | '.join(s)),
          oare_genre=('genre_label',lambda s:' | '.join(sorted(set(x for x in s if x!='unknown'))) or 'unknown'),
          objects=('object',lambda s:' + '.join(sorted(set(s.dropna())))),
          eponym=('eponym',lambda s:' | '.join(s.dropna().unique())),
          n_words=('n_words','sum'),logogram_share=('logogram_share','mean'),
          cdli_genre=('genres','first'),collection=('collections','first')).reset_index()
out['tablet_and_envelope']=out.objects.str.contains(r'\+')
out.to_csv(f'{R}/oare/oare_matched.csv',index=False)
s=pd.Series({'OA photographed':len(oa),'matched in OARE':len(out),
  'CDLI genre missing':int(out.cdli_genre.isna().sum()),
  'CDLI genre missing, OARE genre known':int((out.cdli_genre.isna()&(out.oare_genre!='unknown')).sum()),
  'envelope only':int((out.objects=='envelope').sum()),'tablet and envelope under one number':int(out.tablet_and_envelope.sum()),
  'eponym named':int((out.eponym!='').sum()),'with transliteration':int((out.n_words>0).sum())})
s.to_csv(f'{R}/turning/oare_summary.csv',header=['n']); print(s.to_string())
print(out.oare_genre.value_counts().head(12).to_string()); print(out[out.eponym!=''].eponym.value_counts().head(10).to_string())
