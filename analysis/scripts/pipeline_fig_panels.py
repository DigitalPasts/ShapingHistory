"""Shared data and panels for the pipeline opener figure (three layout options in options.py).
Example tablet: AUCT 3, 084 (P104315), Ur III, Puzriš-Dagan, Horn Museum (Andrews University); the Ur III medoid of Fig. 1."""
from _paths import SHARED, WORK
import numpy as np, pandas as pd, cv2, os, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle, FancyArrowPatch, Polygon, FancyBboxPatch
R = WORK; H = f'{R}/pipeline_fig'
for f in fm.findSystemFonts():
    if 'Inter' in f: fm.fontManager.addfont(f)
plt.rcParams.update({'font.family': 'Inter', 'font.size': 7, 'axes.linewidth': 0.6, 'axes.edgecolor': '#52514e',
                     'xtick.color': '#52514e', 'ytick.color': '#52514e', 'xtick.major.width': 0.6, 'ytick.major.width': 0.6,
                     'axes.labelcolor': '#52514e', 'text.color': '#0b0b0b', 'savefig.facecolor': '#ffffff'})
INK, INK2, MUTE, GRID = '#0b0b0b', '#52514e', '#a3a29c', '#e6e5e0'
BLUE, ORANGE, AQUA, YELLOW, VIOLET = '#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#6250d6'
PID = 104315; LABEL = 'AUCT 3, 084'

# ---------- data ----------
photo = cv2.cvtColor(cv2.imread(f'{H}/P104315.jpg'), cv2.COLOR_BGR2RGB)
mask = cv2.imread(f'{R}/zenodo/imgs/images_b_w_tablets/{PID:06d}.png', 0) > 127
recon = cv2.imread(f'{H}/recon_104315.png', 0) / 255
trav = {v: cv2.imread(f'{H}/trav_X2_{v:+.1f}.png', 0) / 255 for v in (-2.5, 2.5)}
geo = pd.read_csv(f'{R}/results/silhouette_geometry.csv').set_index('id').loc[PID]
V = pd.concat([pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_{s}.csv') for s in ['train', 'val', 'test']]).drop_duplicates('CDLI_id')
X = [f'X{i}' for i in range(1, 13)]
code = V.set_index('CDLI_id').loc[PID, X].values.astype(float)

def components(m):
    n, lab, st, cen = cv2.connectedComponentsWithStats(m.astype(np.uint8))
    comp = sorted([i for i in range(1, n) if st[i, 4] > 0.02 * st[1:, 4].max()], key=lambda i: -st[i, 4])[:6]
    rev = max(comp[:2], key=lambda i: cen[i, 1]); obv = min(comp[:2], key=lambda i: cen[i, 1])
    ox, oy, ow, oh = st[obv, :4]
    sides = [i for i in comp if i not in (obv, rev) and abs(cen[i, 0] - cen[obv, 0]) > ow / 2]
    ends = [i for i in comp if i not in (obv, rev) and abs(cen[i, 0] - cen[obv, 0]) <= ow / 2]
    return dict(st=st, obv=obv, rev=rev, sides=sides, ends=ends)
C = components(mask)

# ---------- small helpers ----------
def clean(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
def title(ax, letter, text, y=1.0):
    ax.annotate(letter, (0, y), xycoords='axes fraction', xytext=(0, 4), textcoords='offset points', fontsize=9, fontweight='bold', va='bottom', ha='left', color=INK)
    ax.annotate(text, (0, y), xycoords='axes fraction', xytext=(11 if letter else 0, 4.6), textcoords='offset points', fontsize=7, va='bottom', ha='left', color=INK, fontweight='medium')
def spine_style(ax):
    for s in ['top', 'right']: ax.spines[s].set_visible(False)
    ax.tick_params(length=2.5, labelsize=6.2)

# ---------- panels: the single tablet ----------
def p_photo(ax, letter='A', text='Photograph (CDLI)'):
    ax.imshow(photo); clean(ax); title(ax, letter, text)
    ax.text(0.5, -0.02, f'{LABEL} (P104315)\nUr III, Puzriš-Dagan\nHorn Museum', transform=ax.transAxes, ha='center', va='top', fontsize=5.8, color=INK2)

def p_mask(ax, letter='B', text='Silhouette, six views'):
    ax.imshow(~mask, cmap='gray', vmin=0, vmax=1); clean(ax); title(ax, letter, text)
    st = C['st']
    for i, name in [(C['obv'], 'obverse'), (C['rev'], 'reverse')]:
        x, y, w, h = st[i, :4]; ax.text(x + w / 2, y + h / 2, name, ha='center', va='center', color='white', fontsize=5.5)
    ax.text(0.5, -0.02, 'signs and surface\ndiscarded', transform=ax.transAxes, ha='center', va='top', fontsize=5.6, color=INK2)

def p_measure(ax, letter='C', text='Measured on the views'):
    st = C['st']; o = C['obv']; x, y, w, h = st[o, :4]
    s = C['sides'][0]; sx, sy, sw, sh = st[s, :4]
    pad = 18; x0, x1 = min(x, sx) - pad, max(x + w, sx + sw) + pad; y0, y1 = y - pad, y + h + pad
    ax.imshow(~mask[y0:y1, x0:x1], cmap='gray', vmin=-0.25, vmax=1, extent=(x0, x1, y1, y0)); clean(ax); title(ax, letter, text)
    q = max(2, int(0.15 * min(h, w)))
    for cx, cy in [(x, y), (x + w - q, y), (x, y + h - q), (x + w - q, y + h - q)]:
        ax.add_patch(Rectangle((cx, cy), q, q, fill=False, ec=ORANGE, lw=0.9))
    # height and width arrows
    ax.annotate('', (x - 6, y), (x - 6, y + h), arrowprops=dict(arrowstyle='<->', lw=0.7, color=BLUE, shrinkA=0, shrinkB=0))
    ax.annotate('', (x, y + h + 7), (x + w, y + h + 7), arrowprops=dict(arrowstyle='<->', lw=0.7, color=BLUE, shrinkA=0, shrinkB=0))
    ax.annotate('', (sx, sy + sh + 7), (sx + sw, sy + sh + 7), arrowprops=dict(arrowstyle='<->', lw=0.7, color=AQUA, shrinkA=0, shrinkB=0))
    ax.set_xlim(x0 - 2, x1 + 2); ax.set_ylim(y1 + 14, y0 - 2)
    rows = [('height ÷ width', f'{geo.hw:.2f}', BLUE), ('thickness ÷ width', f'{geo.thick_side:.2f}', AQUA),
            ('corner fill', f'{geo.corner_fill:.2f}', ORANGE), ('rectangularity', f'{geo.rect:.2f}', INK2)]
    for k, (n, v, c) in enumerate(rows):
        yy = -0.10 - k * 0.12
        ax.add_patch(Rectangle((0.0, yy - 0.035), 0.05, 0.07, transform=ax.transAxes, color=c, clip_on=False, lw=0))
        ax.text(0.08, yy, n, transform=ax.transAxes, fontsize=5.8, color=INK2, ha='left', va='center')
        ax.text(1.32, yy, v, transform=ax.transAxes, fontsize=6.4, color=INK, ha='right', va='center', fontweight='semibold')

def p_encoder(ax, letter='D', text='VAE code: twelve numbers'):
    clean(ax); ax.set_xlim(0, 10); ax.set_ylim(-0.6, 10); title(ax, letter, text)
    ax.add_patch(Polygon([(0.0, 1.0), (0.0, 9.0), (1.8, 6.6), (1.8, 3.4)], closed=True, fc='#cde2fb', ec=BLUE, lw=0.7))
    ax.text(0.85, 5.0, 'encoder', ha='center', va='center', fontsize=5.4, color=INK, rotation=90)
    vmax = 3.2; x0 = 5.2
    for i, v in enumerate(code):
        yc = 9.0 - i * 0.74; L = abs(v) / vmax * 2.3
        col = {1: BLUE, 2: AQUA, 11: ORANGE}.get(i, '#cfcec8')
        ax.add_patch(Rectangle((x0 if v >= 0 else x0 - L, yc - 0.25), L, 0.5, color=col, lw=0))
        ax.text(2.3, yc, f'X{i + 1}', fontsize=5.4, va='center', ha='left', color=INK2)
        ax.text(9.9, yc, f'{v:+.1f}', fontsize=5.0, va='center', ha='right', color=INK2)
    ax.plot([x0, x0], [0.5, 9.4], color=INK2, lw=0.5)
    for (i, name) in [(1, 'proportion'), (2, 'thickness'), (11, 'corners')]:
        yc = 9.0 - i * 0.74; ax.text(10.1, yc, name, fontsize=5.2, va='center', ha='left', color=INK, clip_on=False)
    ax.text(x0, -0.35, 'standardised value', ha='center', fontsize=5.2, color=INK2)

def p_recon(ax, letter='E', text='Decoded'):
    clean(ax); title(ax, letter, text)
    ims = [trav[-2.5], recon, trav[2.5]]; lab = ['X2 = −2.5\n(taller)', 'this tablet', 'X2 = +2.5\n(wider)']
    W = recon.shape[1]
    big = np.hstack([np.pad(1 - im, ((0, 0), (8, 8)), constant_values=1) for im in ims])
    ax.imshow(big, cmap='gray', vmin=0, vmax=1)
    for k, l in enumerate(lab):
        ax.text((W + 16) * k + (W + 16) / 2, big.shape[0] + 20, l, ha='center', va='top', fontsize=5.6, color=INK if k == 1 else INK2)
    ax.set_ylim(big.shape[0] + 120, -5)

# ---------- panels: the corpus ----------
DATES = {'Uruk IV': -3300, 'Uruk III': -3100, 'Proto-Elamite': -3000, 'ED IIIa': -2550, 'ED IIIb': -2400, 'Ebla': -2350, 'Old Akkadian': -2250,
         'Ur III': -2050, 'Early Old Babylonian': -1950, 'Old Babylonian': -1750, 'Old Assyrian': -1880, 'Middle Assyrian': -1250,
         'Middle Babylonian': -1300, 'Middle Elamite': -1400, 'Neo-Assyrian': -750, 'Neo-Babylonian': -580, 'Achaemenid': -450, 'Hellenistic': -200}
PT = pd.read_csv(f'{R}/results/s4_period_table_clean.csv'); PT = PT[(PT.scope == 'archival') & PT.period.isin(DATES)]
def p_timeline(ax, letter='F', text='Proportion over time'):
    spine_style(ax); title(ax, letter, text)
    d = PT.assign(t=PT.period.map(DATES)).sort_values('t')
    ax.axhline(1, color=GRID, lw=0.8, zorder=0)
    lo = np.exp(np.log(d['median']) - d.MAD); hi = np.exp(np.log(d['median']) + d.MAD)
    ax.vlines(d.t, lo, hi, color=MUTE, lw=1.2, zorder=1)
    ax.scatter(d.t, d['median'], s=14, color=INK2, zorder=2, lw=0)
    u = d[d.period == 'Ur III']; ax.scatter(u.t, u['median'], s=34, color=BLUE, zorder=3, ec='white', lw=1)
    ax.annotate('Ur III', (u.t.iloc[0], u['median'].iloc[0]), (u.t.iloc[0] + 260, 1.55), fontsize=6, color=BLUE, arrowprops=dict(arrowstyle='-', lw=0.5, color=BLUE))
    nb = d[d.period == 'Neo-Babylonian']; ax.annotate('Neo-Bab.', (nb.t.iloc[0], nb['median'].iloc[0]), (nb.t.iloc[0] - 300, 0.52), fontsize=6, color=INK2, arrowprops=dict(arrowstyle='-', lw=0.5, color=INK2))
    ax.set_yscale('log'); ax.set_yticks([0.6, 0.8, 1, 1.25, 1.6]); ax.set_yticklabels(['0.6', '0.8', '1', '1.25', '1.6']); ax.minorticks_off()
    ax.set_ylim(0.48, 1.9); ax.set_xticks([-3000, -2000, -1000, 0]); ax.set_xticklabels(['3000', '2000', '1000', '0 BCE'])
    ax.set_ylabel('height ÷ width', fontsize=6)
    ax.text(-3350, 1.75, 'tall', fontsize=5.6, color=INK2); ax.text(-3350, 0.53, 'wide', fontsize=5.6, color=INK2)

DIMS = pd.read_csv(f'{R}/results/tablet_dims_clean.csv'); DIMS = DIMS[DIMS.archival & (DIMS.hw.between(1 / 3, 3))]
def p_uniformity(ax, letter='G', text='Strictness of norms'):
    spine_style(ax); title(ax, letter, text)
    sel = [('Neo-Assyrian', '#104281', 0.336), ('Ur III', BLUE, 0.079), ('ED IIIa', '#86b6ef', 0.038)]
    bins = np.linspace(-0.9, 0.9, 61)
    for k, (p, c, mad) in enumerate(sel):
        v = np.log(DIMS[DIMS.P == p].hw.values); hst, e = np.histogram(v - np.median(v), bins=bins, density=True)
        ax.fill_between(e[:-1], k * 1.15, k * 1.15 + hst / hst.max(), step='post', color=c, lw=0, alpha=0.9)
        pass
    ax.set_yticks([k * 1.15 + 0.3 for k in range(3)]); ax.set_yticklabels([f'{p}\nMAD {m:.3f}' for p, c, m in sel], fontsize=5.4); ax.tick_params(axis='y', length=0); ax.spines['left'].set_visible(False)
    ax.set_xlabel('log ratio − period median', fontsize=6); ax.set_xlim(-0.9, 0.95)

def p_museum(ax, letter='H', text='Period recognised'):
    spine_style(ax); title(ax, letter, text)
    rows = [('all twelve periods', 57, 30), ('Ur III', 72, 69), ('Neo-Assyrian', 86, 0)]
    for k, (n, a, b) in enumerate(rows):
        y = 2 - k
        ax.plot([b, a], [y, y], color=GRID, lw=2.2, solid_capstyle='round', zorder=0)
        ax.scatter([a], [y], s=22, color=BLUE, zorder=2, lw=0); ax.scatter([b], [y], s=22, color=ORANGE, zorder=2, lw=0)
        ax.text(0, y + 0.18 if k else y + 0.62, n, ha='left', va='bottom', fontsize=5.8, color=INK)
    ax.set_xlim(0, 100); ax.set_yticks([]); ax.spines['left'].set_visible(False)
    ax.set_xlabel('% recognised', fontsize=6)
    ax.text(61, 2, 'random', fontsize=5.2, color=BLUE, ha='left', va='center')
    ax.text(26, 2, 'held out', fontsize=5.2, color=ORANGE, ha='right', va='center')
    ax.set_ylim(-0.6, 3.0)

LS = pd.read_csv(SHARED+'/dino_label_signal.csv')
def p_labels(ax, letter='I', text='Shape follows type'):
    spine_style(ax); title(ax, letter, text)
    tr = {'prêt à intérêt': 'loan, interest', 'reçu': 'receipt', 'location': 'lease', 'achat': 'purchase', 'lettre': 'letter',
          'compte récapitulatif': 'summary account', 'dépense': 'expenditure'}
    d = LS[(LS.label == 'type') & LS.group.isin(tr)].assign(n=lambda x: x.group.map(tr)).sort_values('ratio')
    d = pd.concat([d, LS[LS.label == 'archive'].assign(n='archive: Šamaš-hazir'), LS[(LS.label == 'site') & (LS.group == 'larsa')].assign(n='city: Larsa')]).sort_values('ratio')
    y = np.arange(len(d))[::-1]
    ax.axvline(1, color=INK2, lw=0.6, ls=(0, (2, 2)))
    ax.hlines(y, d.ratio, 1, color=GRID, lw=1.6)
    ax.scatter(d.ratio, y, s=14, color=[BLUE if p < 0.05 else MUTE for p in d.p], zorder=3, lw=0)
    ax.set_yticks(y); ax.set_yticklabels(d.n, fontsize=5.8); ax.tick_params(axis='y', length=0)
    ax.set_xlim(0.74, 1.06); ax.set_xlabel('distance across museums ÷ permuted', fontsize=6)
    ax.text(0.755, -1.3, 'more alike', fontsize=5.4, color=INK2); ax.set_ylim(-1.8, len(d) - 0.4)

RC = pd.read_csv(f'{R}/results/vae_feature_recovery_all.csv')
def p_recovery(ax, letter='J', text='Code recovers'):
    spine_style(ax); title(ax, letter, text)
    nm = {'hw': 'proportion', 'thick_side': 'thickness, sides', 'thick_end': 'thickness, ends', 'rect': 'rectangularity', 'corner_fill': 'corners',
          'side_bulge': 'side bulge', 'circ': 'roundness', 'taper': 'taper', 'solidity': 'breaks'}
    d = RC[RC.feature.isin(nm)].sort_values('R2_well_preserved'); y = np.arange(len(d))
    col = [BLUE if r >= 0.65 else ('#86b6ef' if r >= 0.4 else '#d9d8d2') for r in d.R2_well_preserved]
    ax.barh(y, d.R2_well_preserved, color=col, height=0.62, lw=0)
    ax.set_yticks(y); ax.set_yticklabels(d.feature.map(nm), fontsize=5.8); ax.tick_params(axis='y', length=0)
    ax.set_xlim(0, 1); ax.set_xlabel('cross-validated R²', fontsize=6)
    for yy, r in zip(y, d.R2_well_preserved): ax.text(r + 0.02, yy, f'{r:.2f}', va='center', fontsize=5.4, color=INK2)

# corpus map (t-SNE of VAE codes, cached)
MAPF = f'{H}/tsne_cache.csv'
def corpus_map():
    if os.path.exists(MAPF): return pd.read_csv(MAPF)
    from sklearn.manifold import TSNE
    s = V.groupby('Period_Name', group_keys=False).apply(lambda g: g.sample(min(len(g), 1200), random_state=0))
    if PID not in s.CDLI_id.values: s = pd.concat([s, V[V.CDLI_id == PID]])
    Z = (s[X] - V[X].mean()) / V[X].std()
    e = TSNE(2, perplexity=40, init='pca', random_state=0).fit_transform(Z.values)
    out = s[['CDLI_id', 'Period_Name']].assign(x=e[:, 0], y=e[:, 1]); out.to_csv(MAPF, index=False); return out
MILL = {p: (3 if DATES.get(p, 0) <= -2000 else (2 if DATES.get(p, 0) <= -1000 else 1)) for p in DATES}
def p_map(ax, letter='K', text='Every tablet as twelve numbers'):
    M = corpus_map(); clean(ax); title(ax, letter, text)
    M = M[M.Period_Name.isin(DATES)]; m = M.Period_Name.map(MILL)
    cols = {3: '#86b6ef', 2: YELLOW, 1: VIOLET}; names = {3: '3rd millennium', 2: '2nd millennium', 1: '1st millennium'}
    for k in (3, 2, 1):
        q = M[m == k]; ax.scatter(q.x, q.y, s=1.2, color=cols[k], lw=0, alpha=0.55, rasterized=True)
    t = M[M.CDLI_id == PID]
    ax.scatter(t.x, t.y, s=60, marker='*', color=INK, ec='white', lw=0.8, zorder=5)
    ax.annotate(LABEL, (t.x.iloc[0], t.y.iloc[0]), xytext=(22, 26), textcoords='offset points', fontsize=6, color=INK, arrowprops=dict(arrowstyle='-', lw=0.5), bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.85))
    for j, k in enumerate((3, 2, 1)):
        ax.scatter([0.03], [0.1 - j * 0.07 + 0.14], s=12, color=cols[k], transform=ax.transAxes, lw=0, clip_on=False)
        ax.text(0.06, 0.1 - j * 0.07 + 0.14, names[k], transform=ax.transAxes, fontsize=5.6, va='center', color=INK2)
    ax.text(0.5, -0.02, f'{len(M):,} tablets sampled across periods (t-SNE of the VAE code)', transform=ax.transAxes, ha='center', va='top', fontsize=5.6, color=INK2)

def arrow(fig, a, b, text=None, color=INK2):
    fig.add_artist(FancyArrowPatch(a, b, transform=fig.transFigure, arrowstyle='-|>', mutation_scale=7, lw=0.8, color=color))
    if text: fig.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 0.012, text, ha='center', va='bottom', fontsize=5.6, color=INK2)
