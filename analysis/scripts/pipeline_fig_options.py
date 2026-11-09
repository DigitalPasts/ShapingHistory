"""Three layouts of the pipeline opener figure. Usage: python options.py [A|B|C ...]"""
from _paths import FIGS
import sys; from panels import *
OUT = FIGS
def save(fig, name):
    for ext in ('png', 'pdf'): fig.savefig(f'{OUT}/{name}.{ext}', dpi=300)
    fig.savefig(f'{H}/{name}.png', dpi=110); plt.close(fig)

def option_A():
    fig = plt.figure(figsize=(7.0, 4.5))
    top = [(0.015, 0.54, 0.13, 0.37), (0.18, 0.54, 0.14, 0.37), (0.36, 0.62, 0.12, 0.29), (0.56, 0.52, 0.17, 0.39), (0.82, 0.62, 0.17, 0.26)]
    for f, r in zip([p_photo, p_mask, p_measure, p_encoder, p_recon], top): f(fig.add_axes(r))
    for x0, x1 in [(0.150, 0.175), (0.325, 0.355), (0.525, 0.555), (0.785, 0.815)]: arrow(fig, (x0, 0.75), (x1, 0.75))
    fig.text(0.015, 0.99, 'From one tablet…', fontsize=8.5, fontweight='semibold', va='top', color=INK)
    fig.add_artist(plt.Line2D([0.015, 0.985], [0.435, 0.435], transform=fig.transFigure, color=GRID, lw=0.8))
    fig.text(0.015, 0.425, '…to 87,783 tablets', fontsize=8.5, fontweight='semibold', va='top', color=INK)
    bot = [(0.06, 0.11, 0.14, 0.21), (0.29, 0.11, 0.11, 0.21), (0.455, 0.11, 0.115, 0.21), (0.68, 0.11, 0.09, 0.21), (0.875, 0.11, 0.09, 0.21)]
    for f, r in zip([p_timeline, p_uniformity, p_museum, p_labels, p_recovery], bot): f(fig.add_axes(r))
    for x, t in [(0.06, 'from proportion (C)'), (0.23, 'from proportion (C)'), (0.43, 'from the silhouette (B)'), (0.585, 'from the silhouette (B)'), (0.80, 'from the VAE code (D) and C')]:
        fig.text(x, 0.375, t, fontsize=5.6, color=INK2, style='italic')
    save(fig, 'FigP_optionA_strip')

def option_B():
    fig = plt.figure(figsize=(7.0, 4.4))
    p_photo(fig.add_axes((0.01, 0.30, 0.15, 0.56)))
    p_mask(fig.add_axes((0.19, 0.55, 0.12, 0.31)), 'B', 'Silhouette')
    p_measure(fig.add_axes((0.19, 0.19, 0.105, 0.22)), 'C', 'Measures')
    p_encoder(fig.add_axes((0.36, 0.50, 0.15, 0.36)), 'D', 'Twelve numbers')
    arrow(fig, (0.163, 0.70), (0.185, 0.70)); arrow(fig, (0.315, 0.70), (0.355, 0.70))
    p_map(fig.add_axes((0.62, 0.45, 0.37, 0.41)), 'E', '')
    arrow(fig, (0.565, 0.70), (0.61, 0.70), color=INK)
    fig.text(0.01, 0.985, 'The microscope: one tablet', fontsize=8.5, fontweight='semibold', va='top')
    fig.text(0.62, 0.985, 'The telescope: every tablet', fontsize=8.5, fontweight='semibold', va='top')
    p_timeline(fig.add_axes((0.40, 0.09, 0.15, 0.22)), 'F'); p_uniformity(fig.add_axes((0.65, 0.09, 0.13, 0.22)), 'G'); p_museum(fig.add_axes((0.85, 0.09, 0.13, 0.22)), 'H')
    save(fig, 'FigP_optionB_telescope')

def option_C():
    fig = plt.figure(figsize=(7.0, 6.8))
    p_photo(fig.add_axes((0.01, 0.57, 0.13, 0.36)))
    p_mask(fig.add_axes((0.01, 0.13, 0.13, 0.30)), 'B', 'Silhouette')
    arrow(fig, (0.075, 0.475), (0.075, 0.445))
    rows = [(0.955, 'Proportion', 'height ÷ width, measured on the obverse'), (0.635, 'The whole silhouette', 'compared tablet with tablet, within and across museums'),
            (0.315, 'The VAE code', 'twelve learned numbers per tablet')]
    for y, n, sub in rows:
        fig.add_artist(plt.Line2D([0.17, 0.99], [y + 0.012, y + 0.012], transform=fig.transFigure, color=GRID, lw=0.8))
        fig.text(0.175, y, n, fontsize=8.5, fontweight='semibold', va='top'); fig.text(0.175, y - 0.022, sub, fontsize=6, color=INK2, va='top')
        arrow(fig, (0.145, 0.30), (0.17, y - 0.12), color=MUTE)
    p_measure(fig.add_axes((0.19, 0.74, 0.11, 0.15)), 'C', '')
    p_timeline(fig.add_axes((0.42, 0.70, 0.24, 0.18)), 'D'); p_uniformity(fig.add_axes((0.80, 0.70, 0.18, 0.18)), 'E')
    p_museum(fig.add_axes((0.20, 0.40, 0.22, 0.155)), 'F'); p_labels(fig.add_axes((0.62, 0.38, 0.16, 0.18)), 'G')
    p_encoder(fig.add_axes((0.19, 0.04, 0.15, 0.20)), 'H', '')
    p_recon(fig.add_axes((0.405, 0.05, 0.16, 0.19)), 'I', 'Decoded')
    p_map(fig.add_axes((0.60, 0.06, 0.19, 0.19)), 'J', 'Every tablet'); p_recovery(fig.add_axes((0.89, 0.05, 0.08, 0.19)), 'K', 'Recovered')
    save(fig, 'FigP_optionC_matrix')

for o in (sys.argv[1:] or 'ABC'): {'A': option_A, 'B': option_B, 'C': option_C}[o]()
