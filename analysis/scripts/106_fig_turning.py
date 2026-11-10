"""Figures for the turning-point results (scripts 100, 101, 105).
Fig. 1 (main): for each event, the observed change in tablet form (length of the 12 stratum-weighted median shifts,
robust SD units) against the band that chance alone produces (0 to the 95th percentile of the permutation null), for
the VAE and the label-free DINOv2 features. A dot beyond its band is a change. Events in date order, coloured by type.
Fig. 3 (main): the blind scan, excess change by year in each densely dated stretch, change points marked, listed events
as ticks.
Outputs: SH_FIGS/Fig1_turning_points.png/pdf, SH_FIGS/Fig3_blind_scan.png/pdf"""
from _paths import WORK
import os, numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams.update({'font.family': 'Inter', 'font.size': 8, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.edgecolor': '#666', 'axes.labelcolor': '#222', 'xtick.color': '#444', 'ytick.color': '#444'})
O = f'{WORK}/turning'; FIG = os.environ.get('SH_FIGS', f'{WORK}/figs_paper'); os.makedirs(FIG, exist_ok=True)
TYPE_COL = {'reform': '#1b7f6b', 'foundation': '#2a5db0', 'collapse': '#c46a12', 'conquest': '#8a3a8f', 'succession': '#7a7a7a'}
LABEL = {'Urukagina': 'Urukagina of Lagaš (c. 2351)', 'Sulgi 21': 'Šulgi year 21 (2072)', 'Sulgi 39': 'Šulgi year 39, Puzriš-Dagan (2054)',
         'Ibbi-Suen 3': 'Ibbi-Suen year 3 (2024)', 'Hammurabi 1763': 'Hammurabi takes Larsa (1763)',
         'Samsu-iluna 1739': 'Samsu-iluna loses the south (1739)', 'Sargon II > Sennacherib': 'Sargon II to Sennacherib (705)',
         'Esarhaddon 681': 'Esarhaddon (681)', 'Cyrus 539': 'Cyrus takes Babylon (539)', 'Darius I 521': 'Darius I (521)'}
fig, axs = plt.subplots(1, 2, figsize=(7.1, 3.6), sharey=True, gridspec_kw=dict(wspace=0.08))
for ax, suf, title in zip(axs, ['', '_dinov2'], ['VAE shape features', 'DINOv2 (no period labels)']):
    if not os.path.exists(f'{O}/tp_power{suf}.csv'): continue
    P = pd.read_csv(f'{O}/tp_power{suf}.csv'); E = pd.read_csv(f'{O}/tp_protocol_events{suf}.csv')
    E1 = E[E.control.eq('site x type, damage')].set_index('event'); Em = E[E.control.str.contains('museum')].set_index('event')
    for i, r in enumerate(P.itertuples()):
        y = len(P) - 1 - i; t = E1.loc[r.event, 'type']; c = TYPE_COL[t]
        ax.plot([0, r.null_95], [y, y], color='#ddd', lw=7, solid_capstyle='butt', zorder=1)
        q = E1.loc[r.event, 'q_vae_shift']; sig = q < 0.05
        ax.scatter(r.observed, y, s=34, color=c if sig else 'white', edgecolor=c, linewidth=1.4, zorder=3)
        qm = Em.loc[r.event, 'q_vae_shift'] if r.event in Em.index else np.nan
        ax.text(1.98, y, '' if np.isnan(qm) else ('museum ✓' if qm < 0.05 else 'museum ✗'), va='center', ha='right', fontsize=6, color='#555')
        if suf == '_dinov2': ax.text(2.04, y, f'n {r.n_before}/{r.n_after}', va='center', ha='left', fontsize=6.3, color='#555')
    ax.set_xlim(0, 2.0); ax.set_title(title, fontsize=8.5, loc='left'); ax.set_xlabel('change in tablet form (robust SD units)')
    ax.set_yticks(range(len(P))); ax.set_yticklabels([LABEL[e] for e in P.event[::-1]])
    ax.grid(axis='x', color='#eee', lw=0.6); ax.set_axisbelow(True)
from matplotlib.lines import Line2D
h = [Line2D([], [], marker='o', ls='', color=c, label=t) for t, c in TYPE_COL.items()]
h += [Line2D([], [], color='#ddd', lw=7, label='range of chance (95%)'), Line2D([], [], marker='o', ls='', mfc='white', mec='#444', label='not significant (q ≥ 0.05)')]
fig.legend(handles=h, loc='lower center', ncol=7, frameon=False, fontsize=6.5, bbox_to_anchor=(0.5, -0.06))
fig.savefig(f'{FIG}/Fig1_turning_points.png', dpi=300, bbox_inches='tight'); fig.savefig(f'{FIG}/Fig1_turning_points.pdf', bbox_inches='tight')

# blind scan
Y = pd.read_csv(f'{O}/cp_scan_years.csv'); P = pd.read_csv(f'{O}/cp_scan_points.csv')
EVENTS = {2072: 'Š21', 2054: 'Š39', 2044: 'AS', 2035: 'ŠS', 2024: 'IS3', 1822: 'RS', 1792: 'Ha', 1763: 'Larsa', 1749: 'Si', 1739: 'south lost',
          745: 'TP III', 722: 'Sar II', 705: 'Senn', 681: 'Esarh', 669: 'Asb', 652: 'revolt', 626: 'Nabop', 605: 'Nbk', 556: 'Nbn',
          539: 'Cyrus', 530: 'Camb', 521: 'Dar I', 484: 'Xerxes'}
st = list(Y.stretch.unique()); fig, axs = plt.subplots(len(st), 1, figsize=(7.1, 1.35 * len(st)), gridspec_kw=dict(hspace=0.75))
for ax, s in zip(np.atleast_1d(axs), st):
    g = Y[Y.stretch == s].sort_values('year'); ax.plot(g.year, g.excess, color='#333', lw=1.1)
    ax.fill_between(g.year, 0, g.excess.clip(lower=0), color='#bbb', alpha=0.35, lw=0)
    cp = P[(P.stretch == s) & (P.group == 'all sites and types')]
    ax.scatter(cp.year, cp.excess, s=22, color='#c46a12', zorder=3)
    for yr, lab in EVENTS.items():
        if g.year.min() - 1 <= yr <= g.year.max() + 1:
            ax.axvline(yr, color='#2a5db0', lw=0.6, ls=(0, (2, 2))); ax.text(yr, g.excess.max() * 1.08, lab, fontsize=5.8, color='#2a5db0', ha='center')
    ax.set_xlim(g.year.max() + 2, g.year.min() - 2); ax.axhline(0, color='#999', lw=0.5)
    ax.set_title(f'{s}: {len(cp)} change point{"s" if len(cp) != 1 else ""}', fontsize=8, loc='left'); ax.set_ylabel('excess', fontsize=7)
np.atleast_1d(axs)[-1].set_xlabel('year BCE (each point compares the 10 years before with the 10 years from it)')
fig.savefig(f'{FIG}/Fig3_blind_scan.png', dpi=300, bbox_inches='tight'); fig.savefig(f'{FIG}/Fig3_blind_scan.pdf', bbox_inches='tight')
print('figures written')
