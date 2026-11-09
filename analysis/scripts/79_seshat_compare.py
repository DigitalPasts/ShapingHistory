"""Compare the ANE codebook (script 72) with Seshat Equinox-2020 codes for the matching polities (script 70).
Matches are approximate (Seshat polities are dynasties in a region, our rows are corpus periods)."""
from _paths import WORK
import pandas as pd, numpy as np
from scipy.stats import spearmanr
R=WORK
w=pd.read_csv(f'{R}/seshat/seshat_codes_wide.csv',index_col=0)
MAP={'ED IIIa':'IqEDyn*','ED IIIb':'IqEDyn*','Old Akkadian':'IqAkkad','Ur III':'IqUrIII','Early Old Babylonian':'IqIsinL','Old Babylonian':'IqBabAm',
     'Old Assyrian':'TrBrzMD','Middle Babylonian':'IqBabKs','Middle Elamite':'IrMElm1','Hittite':'TrHatNK','Neo-Assyrian':'IqNAssr',
     'Neo-Babylonian':'IqNeoBb','Achaemenid (Babylonia)':'IrAchae','Achaemenid (Persepolis)':'IrAchae','Hellenistic':'IrSeleu'}
V=['Polity territory','Administrative levels','Settlement hierarchy','Full-time bureaucrats','Formal legal code','Judges','Courts','Examination system','Couriers','Postal stations','Calendar','Specialized government buildings']
W=pd.read_csv(f'{R}/centralization_scores_wide.csv',index_col=0)
S=pd.DataFrame({r:w.loc[p,V] for r,p in MAP.items()}).T
S.insert(0,'seshat_polity',pd.Series(MAP))
S.to_csv(f'{R}/seshat_vs_codebook.csv')
J=W.join(S)
out={}
for a,b in [('TERR','Polity territory'),('HIER','Administrative levels'),('LAW','Formal legal code'),('COMM','Couriers')]:
    t=J[[a,b]].dropna(); out[f'{a} vs {b}']=(round(spearmanr(t[a],t[b])[0],2),len(t))
nonvar={v:S[v].dropna().nunique() for v in V}
pd.Series(out).to_csv(f'{R}/seshat_vs_codebook_rho.csv')
if __name__=='__main__':
    print(S.to_string()); print(out); print('distinct values per Seshat variable:',nonvar)
