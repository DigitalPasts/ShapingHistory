"""Fig. 5: uniformity of archival tablets (MAD of log h/w within museum, and median VAE distance within museum) against
the three polity indices, fourteen periods; rho and permutation p from script 86 (centralization/stats_spearman.csv).
Output: SH_FIGS/Fig5_polity_uniformity.png/pdf"""
from _paths import WORK
import os, pandas as pd
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams.update({'font.family': 'Inter', 'font.size': 7.5, 'axes.spines.top': False, 'axes.spines.right': False})
C = f'{WORK}/centralization'; FIG = os.environ.get('SH_FIGS', f'{WORK}/figs_paper')
T = pd.read_csv(f'{C}/stats_period_table.csv', index_col=0); S = pd.read_csv(f'{C}/stats_spearman.csv')
AB = {'ED IIIa': 'ED IIIa', 'ED IIIb': 'ED IIIb', 'Ebla': 'Ebla', 'Old Akkadian': 'OAkk', 'Ur III': 'Ur III', 'Early Old Babylonian': 'EOB',
      'Old Babylonian': 'OB', 'Old Assyrian': 'OA', 'Middle Babylonian': 'MB', 'Middle Assyrian': 'MA', 'Neo-Assyrian': 'NA',
      'Neo-Babylonian': 'NB', 'Achaemenid': 'Ach', 'Hellenistic': 'Hell'}
IDX = [('A_polity_reach', 'A  polity reach'), ('B_institutional_economy', 'B  institutional economy'), ('C_control_of_writing', 'C  control of writing')]
OUT = [('MAD_in_museum', 'variation in proportion\n(MAD of log h/w, within museum)'), ('VAEd_in_museum', 'variation in outline\n(VAE distance, within museum)')]
fig, axs = plt.subplots(2, 3, figsize=(7.1, 4.4), sharey='row', gridspec_kw=dict(hspace=0.45, wspace=0.12))
for i, (o, ol) in enumerate(OUT):
    for j, (k, kl) in enumerate(IDX):
        ax = axs[i, j]; ax.scatter(T[k], T[o], s=18, color='#2a5db0', edgecolor='white', linewidth=0.5)
        for p, r in T.iterrows(): ax.annotate(AB[p], (r[k], r[o]), xytext=(3, 2), textcoords='offset points', fontsize=5.8, color='#444')
        s = S[(S.outcome == o) & (S['index'] == k)].iloc[0]
        ax.set_title(f'ρ = {s.rho:.2f}, p = {s.p_perm:.2f}', fontsize=7, loc='right', color='#444')
        if i == 1: ax.set_xlabel(kl + ' (0-3)')
        if j == 0: ax.set_ylabel(ol)
        ax.grid(color='#eee', lw=0.5); ax.set_axisbelow(True)
fig.savefig(f'{FIG}/Fig5_polity_uniformity.png', dpi=300, bbox_inches='tight'); fig.savefig(f'{FIG}/Fig5_polity_uniformity.pdf', bbox_inches='tight')
print('ok')
