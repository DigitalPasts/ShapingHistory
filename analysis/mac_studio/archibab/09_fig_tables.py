"""Compact tables for the final figures.
1. 03_label_signal.csv reformatted (both DINOv2 variants).
2. Periphery lifts (05 method) with Achaemenid split into Persepolis (Pārśa) / Babylonia, all nine groups, all-genres mode,
   plus Anšan administrative-mode and Kanesh letters-mode rows; share >= 0.005. Reuses 08's machinery (executed, not modified)."""
import os, re, numpy as np, pandas as pd
ROOT = os.path.expanduser('~/deeplomatics-repro'); OUT = f'{ROOT}/archibab'

t = pd.read_csv(f'{OUT}/03_label_signal.csv')
t1 = t.rename(columns={'value': 'group', 'n_museums_ge8': 'n_museums'})[['space', 'label', 'group', 'n', 'n_museums', 'ratio', 'p']]
t1.to_csv(f'{OUT}/09_fig_tables_label_signal.csv', index=False)

src = open(f'{OUT}/08_followups.py').read()
shared = src.split('# ---------- 1.')[0] + '# ---------- shared' + src.split('# ---------- shared')[1].split('# ---------- 2.')[0]
g = {}; exec(compile(shared, '08_followups.py', 'exec'), g)
T = g['T']
per2 = np.where(T.per == 'Achaemenid', np.where(T.city == 'Pārśa', 'Achaemenid-Persepolis', 'Achaemenid-Babylonia'), T.per).astype(object)
R = g['lift_table'](per2, list(g['GROUPS']))
R.to_csv(f'{OUT}/09_fig_tables_periphery_full.csv', index=False)
keep = (R['mode'] == 'all_genres') | ((R['mode'] == 'same_genre') & (((R.group == 'Anshan') & (R.genre == 'Administrative')) | ((R.group == 'Kanesh') & (R.genre == 'Letter'))))
t2 = R[keep & (R.share >= 0.005)][['group', 'mode', 'genre', 'period', 'share', 'lift', 'lo', 'hi']].round(3)
t2.to_csv(f'{OUT}/09_fig_tables_periphery.csv', index=False)
pd.set_option('display.width', 200); pd.set_option('display.max_rows', 500)
print(t1.round(3).to_string(index=False)); print(t2.to_string(index=False))
