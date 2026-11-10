"""Three options for an opener pipeline figure: tablet photo -> mask -> VAE latent -> shape statistics.
Data from prep.py (example tablet AAS 015 = AO 19752, Ur III, Umma; P100003) and earlier results CSVs."""
import os, numpy as np, pandas as pd, matplotlib as mpl, matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Polygon, FancyArrowPatch, Rectangle, FancyBboxPatch
ROOT = os.path.expanduser('~/deeplomatics-repro'); OUT = f'{ROOT}/pipeline_figure'
D = np.load(f'{OUT}/prep.npz'); C = pd.read_csv(f'{OUT}/prep_corpus.csv')
DISP = pd.read_csv(f'{ROOT}/results/disp_vae_euc_pca12z_period.csv')
BETW = pd.read_csv(f'{ROOT}/results/disp_vae_euc_pca12z_between_site_admin.csv')

INK, INK2, MUTED, GRID = '#0b0b0b', '#52514e', '#8a8984', '#e4e3df'
UR3, OB, NA, OTHER = '#2a78d6', '#eb6834', '#1baf7a', '#cfcec9'
CLAY = LinearSegmentedColormap.from_list('clay', ['#ffffff', '#a8714a'])
HW_LO, HW_HI = 0.9, 1.1   # landscape < 0.9 <= nearly square <= 1.1 < portrait  (placeholder thresholds; align with paper)
mpl.rcParams.update({'font.family': 'Helvetica', 'font.size': 7, 'axes.labelsize': 7, 'axes.titlesize': 7.5, 'xtick.labelsize': 6,
                     'ytick.labelsize': 6, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK2, 'xtick.color': MUTED, 'ytick.color': MUTED,
                     'axes.linewidth': 0.6, 'xtick.major.width': 0.6, 'ytick.major.width': 0.6, 'axes.spines.top': False,
                     'axes.spines.right': False, 'savefig.dpi': 400, 'pdf.fonttype': 42, 'svg.fonttype': 'none'})
PERIODS8 = ['Ur III', 'ED IIIb', 'Old Babylonian', 'Neo-Babylonian', 'Achaemenid', 'Old Akkadian', 'Middle Babylonian', 'Neo-Assyrian']

def letter(ax, s, x=-0.02, y=1.16):
    ax.text(x, y, s, transform=ax.transAxes, fontsize=9, fontweight='bold', color=INK, va='bottom', ha='left')
def header(fig, x, y, L, text):
    fig.text(x, y, L, fontsize=9, fontweight='bold', color=INK, va='baseline')
    fig.text(x + 0.022, y, text, fontsize=7.5, color=INK, va='baseline')
import cv2
_n, _lab, _st, _cen = cv2.connectedComponentsWithStats((D['mask'] > 0.5).astype(np.uint8))
_big = [i for i in range(1, _n) if _st[i, 4] > 2000]
OBV = max(_big[:4], key=lambda i: _st[i, 4]) if False else min(_big, key=lambda i: (abs(_cen[i][0] - 256) + abs(_cen[i][1] - 165)) if _st[i, 4] > 20000 else 1e9)
def obverse_measure(ax, title=True):
    x, y, w, h = _st[OBV, :4]; pad = 34
    crop = D['mask'][y - pad:y + h + pad, x - pad:x + w + pad]
    img(ax, crop, cmap=CLAY); x0, y0 = pad, pad
    ax.add_patch(Rectangle((x0, y0), w, h, fill=False, ec=UR3, lw=0.8, ls=(0, (3, 2))))
    ax.annotate('', (x0 - 14, y0), (x0 - 14, y0 + h), arrowprops=dict(arrowstyle='<->', color=INK, lw=0.6))
    ax.annotate('', (x0, y0 + h + 14), (x0 + w, y0 + h + 14), arrowprops=dict(arrowstyle='<->', color=INK, lw=0.6))
    ax.text(x0 - 20, y0 + h / 2, 'h', ha='right', va='center', fontsize=6.5, color=INK, style='italic')
    ax.text(x0 + w / 2, y0 + h + 20, 'w', ha='center', va='top', fontsize=6.5, color=INK, style='italic')
    if title: ax.set_title(f'obverse: h/w = {h / w:.2f}', color=INK, pad=3)
def img(ax, a, cmap='gray', title=None, vmin=None, vmax=None):
    ax.imshow(a, cmap=cmap, vmin=vmin, vmax=vmax, interpolation='lanczos'); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    if title: ax.set_title(title, color=INK, pad=3)
def arrow(fig, a, b, text=None, rad=0.0, dy=0.012, lw=0.8):
    p = FancyArrowPatch(a, b, transform=fig.transFigure, arrowstyle='-|>', mutation_scale=7, lw=lw, color=INK2, connectionstyle=f'arc3,rad={rad}')
    fig.patches.append(p)
    if text: fig.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + dy, text, ha='center', va='bottom', fontsize=6, color=INK2)
def vae_schematic(ax, kind):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    pts = [(0.05, 0.05), (0.95, 0.35), (0.95, 0.65), (0.05, 0.95)] if kind == 'enc' else [(0.05, 0.35), (0.95, 0.05), (0.95, 0.95), (0.05, 0.65)]
    ax.add_patch(Polygon(pts, closed=True, fc='#eef3fb', ec=UR3, lw=0.8))
    ax.text(0.5, 0.5, 'encoder' if kind == 'enc' else 'decoder', ha='center', va='center', fontsize=6.5, color=INK)
    ax.text(0.5, -0.06, '5 conv layers' if kind == 'enc' else '5 deconv layers', ha='center', va='top', fontsize=5.5, color=MUTED, transform=ax.transAxes)
def latent_bars(ax, horizontal=False):
    mu, kh = D['mu'], int(D['kh']); cols = [UR3 if k == kh else '#9c9b96' for k in range(12)]
    if horizontal:
        ax.bar(np.arange(12), mu, color=cols, width=0.7); ax.axhline(0, color=MUTED, lw=0.5)
        ax.set_xticks(range(12)); ax.set_xticklabels([f'z{k + 1}' for k in range(12)], fontsize=5); ax.set_ylabel('value')
    else:
        ax.barh(np.arange(12)[::-1], mu, color=cols, height=0.7); ax.axvline(0, color=MUTED, lw=0.5)
        ax.set_yticks(np.arange(12)[::-1]); ax.set_yticklabels([f'z{k + 1}' for k in range(12)], fontsize=5)
        ax.tick_params(axis='y', length=0); ax.spines['left'].set_visible(False)
    ax.set_title('12-d shape code', color=INK, pad=3)
def hw_hist(ax, mark=True):
    v = C.hw_ratio.dropna(); v = v[(v > 0.3) & (v < 2.4)]; bins = np.linspace(0.3, 2.4, 64)
    ax.axvspan(HW_LO, HW_HI, color='#e9e8e4', lw=0, zorder=0)
    ax.hist(v, bins=bins, color='#9c9b96', lw=0, zorder=1)
    for xx, yy, lab in [(0.55, 1.0, 'landscape'), (1.0, 1.09, 'nearly square'), (1.85, 1.0, 'portrait')]:
        ax.text(xx, yy, lab, transform=ax.get_xaxis_transform(), ha='center', va='bottom', fontsize=5.5, color=INK2)
    ax.plot([1.0, 1.0], [1.0, 1.08], transform=ax.get_xaxis_transform(), color=MUTED, lw=0.4, clip_on=False)
    ax.set_xlim(0.3, 2.4)
    if mark:
        e = C.loc[C.CDLI_id == 100003, 'hw_ratio'].iat[0]; ax.axvline(e, color=UR3, lw=1, zorder=2)
        ax.text(e - 0.05, 0.62, f'AAS 015\n{e:.2f}', transform=ax.get_xaxis_transform(), fontsize=5.5, color=UR3, va='top', ha='right',
                bbox=dict(boxstyle='square,pad=0.1', fc='white', ec='none', alpha=0.85), zorder=3)
    ax.set_xlabel('height / width (obverse)'); ax.set_ylabel('tablets'); ax.set_yticks([]); ax.spines['left'].set_visible(False)
    ax.set_title('Proportion of the obverse', color=INK, pad=20)
def latent_map(ax, n=2500):
    rng = np.random.default_rng(0)
    bg = C.sample(8000, random_state=0); ax.scatter(bg.pc1, bg.pc2, s=0.6, c=OTHER, lw=0, rasterized=True)
    for p, col in [('Neo-Assyrian', NA), ('Old Babylonian', OB), ('Ur III', UR3)]:
        g = C[C.Period_Name == p]; g = g.sample(min(n, len(g)), random_state=0)
        ax.scatter(g.pc1, g.pc2, s=0.8, c=col, lw=0, alpha=0.55, rasterized=True)
    for i, (p, col) in enumerate([('Ur III', UR3), ('Old Babylonian', OB), ('Neo-Assyrian', NA), ('other periods', OTHER)]):
        ax.scatter([0.04], [0.95 - i * 0.07], s=12, c=col, transform=ax.transAxes, clip_on=False)
        ax.text(0.075, 0.95 - i * 0.07, p, transform=ax.transAxes, va='center', fontsize=5.8, color=INK2)
    e = C[C.CDLI_id == 100003]; ax.scatter(e.pc1, e.pc2, s=40, marker='*', c=INK, ec='white', lw=0.6, zorder=5)
    ax.annotate('AAS 015', (e.pc1.iat[0], e.pc2.iat[0]), (0.05, 0.55), textcoords='axes fraction', fontsize=5.8, color=INK,
                arrowprops=dict(arrowstyle='-', color=INK, lw=0.5))
    y0, y1 = C.pc2.quantile([0.001, 0.999]); x0, x1 = C.pc1.quantile([0.001, 0.999])
    ax.set_ylim(y0, y1 + 0.45 * (y1 - y0)); ax.set_xlim(x0, x1)
    ax.set_xlabel('PC 1 of shape code'); ax.set_ylabel('PC 2'); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title('Corpus in shape space (87,783 tablets)', color=INK, pad=3)
def dispersion(ax, compact=False):
    t = DISP[(DISP.scope == 'admin') & DISP.period.isin(PERIODS8)].set_index('period').loc[PERIODS8[::-1]]
    y = np.arange(len(t)); cols = [UR3 if p == 'Ur III' else (OB if p == 'Old Babylonian' else (NA if p == 'Neo-Assyrian' else '#7d7c77')) for p in t.index]
    ax.hlines(y, t.lo, t.hi, color=cols, lw=1.2); ax.scatter(t.disp, y, s=14, c=cols, zorder=3, ec='white', lw=0.6)
    ax.set_yticks(y); ax.set_yticklabels(t.index, fontsize=5.8); ax.tick_params(axis='y', length=0); ax.spines['left'].set_visible(False)
    ax.set_xlabel('dispersion  (lower = more uniform)'); ax.grid(axis='x', color=GRID, lw=0.5); ax.set_axisbelow(True)
    ax.set_title('Uniformity by period\n(administrative; 95% bootstrap CI)', color=INK, pad=3)
def disp_schematic(ax):
    g = C[(C.Period_Name == 'Ur III') & (C.Genre_Name == 'Administrative')].sample(80, random_state=1)
    x, y = g.pc1.values, g.pc2.values; mx, my = np.median(x), np.median(y)
    keep = np.hypot(x - mx, y - my) <= np.quantile(np.hypot(x - mx, y - my), 0.9); x, y = x[keep], y[keep]
    for a, b in zip(x, y): ax.plot([a, mx], [b, my], color='#b9cfee', lw=0.5, zorder=1)
    ax.scatter(x, y, s=5, c=UR3, lw=0, zorder=2); ax.scatter([mx], [my], s=40, marker='+', c=INK, lw=1.2, zorder=3)
    ax.text(mx, my - 0.18 * (y.max() - y.min()), 'group median', ha='center', fontsize=5.5, color=INK)
    ax.set_xticks([]); ax.set_yticks([]); [s.set_visible(False) for s in ax.spines.values()]
    ax.set_title('Dispersion = median of distances', color=INK, pad=3)
    ax.text(0.5, -0.04, 'bootstrap: 200 × n = 100', transform=ax.transAxes, ha='center', va='top', fontsize=5.5, color=MUTED)
def between(ax):
    t = BETW.set_index('period').loc[['Ur III', 'Old Babylonian', 'Old Akkadian']]
    cols = [UR3, OB, '#7d7c77']; ax.bar(range(3), t.between_median, color=cols, width=0.6)
    for i, (v, n) in enumerate(zip(t.between_median, t.n_sites)): ax.text(i, v + 0.05, f'{v:.2f}\n{n} sites', ha='center', va='bottom', fontsize=5.5, color=INK2)
    ax.set_xticks(range(3)); ax.set_xticklabels(['Ur III', 'OB', 'Old Akk.'], fontsize=6); ax.set_ylabel('distance between city medians')
    ax.set_ylim(0, 2.7); ax.set_title('Cities converge\n(administrative)', color=INK, pad=3)
def nn_strip(axs, title=True):
    for i, ax in enumerate(axs):
        img(ax, D['nn_masks'][i] / 255., cmap=CLAY)
        cid = int(D['nn_ids'][i]); r = C[C.CDLI_id == cid].iloc[0]
        ax.text(0.5, -0.04, f"{r.designation.split(' SA')[0]}\n{str(r.provenience).split(' (')[0]}", transform=ax.transAxes, ha='center', va='top', fontsize=5, color=INK2)
    if title: axs[0].text(0, 1.08, 'Nearest shapes in other museums: all Ur III', transform=axs[0].transAxes, fontsize=7, color=INK)
def traversal(axs):
    vals = D['trav_vals']
    for ax, im, v in zip(axs, D['trav'], vals):
        img(ax, im, cmap=CLAY, vmin=0, vmax=1); ax.text(0.5, -0.03, f'{v:+.0f}σ' if v else '0', transform=ax.transAxes, ha='center', va='top', fontsize=5.5, color=INK2)

def save(fig, name):
    for ext in ['pdf', 'png', 'svg']: fig.savefig(f'{OUT}/{name}.{ext}', facecolor='white', bbox_inches='tight', pad_inches=0.04)
    plt.close(fig)


# ---------------- Option A: landscape strip + analysis panels (double column) ----------------
def option_a():
    fig = plt.figure(figsize=(7.08, 4.9))
    ty, th, cy = 0.60, 0.30, 0.75
    pa = fig.add_axes([0.00, ty, 0.115, th]); img(pa, D['photo'], cmap=None, title='CDLI photograph'); letter(pa, 'A', -0.02, 1.13)
    pb = fig.add_axes([0.14, ty, 0.11, th]); img(pb, D['gray512'], title='grayscale 512²')
    pc = fig.add_axes([0.27, ty, 0.11, th]); img(pc, D['mask'], cmap=CLAY, title='mask')
    en = fig.add_axes([0.405, ty + 0.03, 0.07, th - 0.06]); vae_schematic(en, 'enc')
    lb = fig.add_axes([0.53, ty, 0.075, th]); latent_bars(lb)
    de = fig.add_axes([0.635, ty + 0.03, 0.07, th - 0.06]); vae_schematic(de, 'dec')
    rc = fig.add_axes([0.725, ty, 0.11, th]); img(rc, D['recon'], cmap=CLAY, vmin=0, vmax=1, title='decoded')
    ob = fig.add_axes([0.865, ty, 0.135, th]); obverse_measure(ob)
    for p, q, off in [(pa, pb, 0), (pb, pc, 0), (pc, en, 0), (en, lb, 0.03), (lb, de, 0), (de, rc, 0)]:
        arrow(fig, (p.get_position().x1 + 0.004, cy), (q.get_position().x0 - 0.004 - off, cy))
    fig.text(0.0, 0.965, 'AAS 015 (Louvre AO 19752), Ur III administrative tablet, Umma, Šulgi 46', fontsize=6.5, color=INK2)
    tv = [fig.add_axes([0.40 + i * 0.065, 0.455, 0.055, 0.085]) for i in range(5)]; traversal(tv)
    fig.text(0.30, 0.495, f'moving along z{int(D["kh"]) + 1}\n(r = {D["corr"][int(D["kh"])]:.2f} with h/w)', fontsize=5.8, color=INK2, va='center')
    nn = [fig.add_axes([0.76 + i * 0.04, 0.455, 0.037, 0.085]) for i in range(6)]
    for i, ax in enumerate(nn): img(ax, D['nn_masks'][i] / 255., cmap=CLAY)
    fig.text(0.76, 0.555, 'nearest shapes in other museums: 6/6 Ur III', fontsize=5.8, color=INK2)
    b1 = fig.add_axes([0.03, 0.07, 0.20, 0.30]); hw_hist(b1); letter(b1, 'B', -0.12, 1.12)
    b2 = fig.add_axes([0.28, 0.07, 0.22, 0.30]); latent_map(b2); letter(b2, 'C', -0.08, 1.12)
    b3 = fig.add_axes([0.63, 0.07, 0.17, 0.30]); dispersion(b3); letter(b3, 'D', -0.6, 1.12)
    b4 = fig.add_axes([0.87, 0.07, 0.13, 0.30]); between(b4); letter(b4, 'E', -0.45, 1.12)
    save(fig, 'option_A_landscape_strip')

# ---------------- Option B: portrait narrative (full page) ----------------
def option_b():
    fig = plt.figure(figsize=(7.08, 7.6))
    header(fig, 0.0, 0.975, 'A', 'From photograph to outline')
    a0 = fig.add_axes([0.0, 0.64, 0.21, 0.31]); img(a0, D['photo'], cmap=None)
    a1 = fig.add_axes([0.25, 0.70, 0.15, 0.20]); img(a1, D['gray512'], title='grayscale, padded to 512²')
    a2 = fig.add_axes([0.43, 0.70, 0.15, 0.20]); img(a2, D['blur'], title='Gaussian blur 11 × 11')
    a3 = fig.add_axes([0.61, 0.70, 0.15, 0.20]); img(a3, D['mask'], cmap=CLAY, title='threshold: mask of all faces')
    a4 = fig.add_axes([0.82, 0.70, 0.18, 0.20]); obverse_measure(a4)
    for p, q in [(a0, a1), (a1, a2), (a2, a3), (a3, a4)]:
        arrow(fig, (p.get_position().x1 + 0.005, 0.80), (q.get_position().x0 - 0.005, 0.80))
    fig.text(0.25, 0.655, 'AAS 015 (Louvre AO 19752), Ur III administrative tablet, Umma, Šulgi 46. CDLI photographs show obverse, reverse and edges ("fat cross").\n'
             'Script, colour and surface texture are discarded; only the outline is kept.', fontsize=5.8, color=MUTED, va='top')
    header(fig, 0.0, 0.585, 'B', 'A variational autoencoder compresses each outline to 12 numbers')
    e = fig.add_axes([0.0, 0.37, 0.13, 0.18]); img(e, D['mask'], cmap=CLAY)
    en = fig.add_axes([0.16, 0.39, 0.09, 0.14]); vae_schematic(en, 'enc')
    lb = fig.add_axes([0.31, 0.37, 0.12, 0.18]); latent_bars(lb)
    de = fig.add_axes([0.47, 0.39, 0.09, 0.14]); vae_schematic(de, 'dec')
    rc = fig.add_axes([0.59, 0.37, 0.13, 0.18]); img(rc, D['recon'], cmap=CLAY, vmin=0, vmax=1, title='decoded')
    for p, q, off in [(e, en, 0), (en, lb, 0.03), (lb, de, 0), (de, rc, 0)]:
        arrow(fig, (p.get_position().x1 + 0.004, 0.46), (q.get_position().x0 - 0.004 - off, 0.46))
    tv = [fig.add_axes([0.76 + i * 0.048, 0.42, 0.044, 0.08]) for i in range(5)]; traversal(tv)
    fig.text(0.76, 0.535, f'moving along z{int(D["kh"]) + 1} changes proportion\n(r = {D["corr"][int(D["kh"])]:.2f} with h/w)', fontsize=5.8, color=INK2, va='center')
    header(fig, 0.0, 0.30, 'C', 'Comparing groups of tablets')
    c1 = fig.add_axes([0.03, 0.05, 0.25, 0.21]); latent_map(c1)
    c2 = fig.add_axes([0.33, 0.05, 0.17, 0.21]); disp_schematic(c2)
    c3 = fig.add_axes([0.62, 0.05, 0.17, 0.21]); dispersion(c3)
    c4 = fig.add_axes([0.87, 0.05, 0.13, 0.21]); between(c4)
    save(fig, 'option_B_portrait_narrative')

# ---------------- Option C: hub with the tablet at the centre ----------------
def option_c():
    fig = plt.figure(figsize=(7.08, 6.4))
    cen = fig.add_axes([0.375, 0.33, 0.25, 0.40]); img(cen, D['photo'], cmap=None)
    fig.text(0.5, 0.315, 'AAS 015 (Louvre AO 19752)\nUr III administrative, Umma', ha='center', va='top', fontsize=6.5, color=INK2)
    p1 = fig.add_axes([0.02, 0.78, 0.12, 0.17]); img(p1, D['gray512'], title='grayscale'); letter(p1, 'A', -0.02, 1.15)
    p2 = fig.add_axes([0.17, 0.78, 0.12, 0.17]); img(p2, D['mask'], cmap=CLAY, title='mask')
    arrow(fig, (0.145, 0.865), (0.165, 0.865))
    fig.text(0.02, 0.765, 'outline only: resize, blur, threshold', fontsize=5.8, color=MUTED, va='top')
    q1 = fig.add_axes([0.66, 0.80, 0.06, 0.13]); vae_schematic(q1, 'enc'); letter(q1, 'B', -0.3, 1.18)
    q2 = fig.add_axes([0.765, 0.78, 0.085, 0.17]); latent_bars(q2)
    q3 = fig.add_axes([0.87, 0.78, 0.12, 0.17]); img(q3, D['recon'], cmap=CLAY, vmin=0, vmax=1, title='decoded')
    arrow(fig, (0.722, 0.865), (0.735, 0.865)); arrow(fig, (0.852, 0.865), (0.868, 0.865))
    tv = [fig.add_axes([0.67 + i * 0.065, 0.62, 0.06, 0.09]) for i in range(5)]; traversal(tv)
    fig.text(0.67, 0.725, f'z{int(D["kh"]) + 1} tracks proportion (r = {D["corr"][int(D["kh"])]:.2f} with h/w)', fontsize=5.8, color=INK2)
    w0 = fig.add_axes([0.02, 0.43, 0.12, 0.22]); obverse_measure(w0, title=False); letter(w0, 'C', -0.02, 1.08)
    w1 = fig.add_axes([0.18, 0.44, 0.15, 0.19]); hw_hist(w1)
    s1 = fig.add_axes([0.04, 0.05, 0.26, 0.27]); latent_map(s1); letter(s1, 'D', -0.12, 1.1)
    nn = [fig.add_axes([0.37 + i * 0.065, 0.075, 0.058, 0.12]) for i in range(4)]; nn_strip(nn); letter(nn[0], 'E', -0.1, 1.25)
    e1 = fig.add_axes([0.80, 0.34, 0.19, 0.22]); dispersion(e1); letter(e1, 'F', -0.62, 1.12)
    e2 = fig.add_axes([0.86, 0.05, 0.13, 0.17]); between(e2)
    for a, b in [((0.38, 0.70), (0.29, 0.77)), ((0.62, 0.70), (0.68, 0.78)), ((0.375, 0.52), (0.335, 0.52)),
                 ((0.40, 0.335), (0.30, 0.27)), ((0.5, 0.27), (0.5, 0.215)), ((0.625, 0.50), (0.665, 0.50))]:
        arrow(fig, a, b, lw=0.7)
    save(fig, 'option_C_hub')

option_a(); option_b(); option_c()
print('saved')
