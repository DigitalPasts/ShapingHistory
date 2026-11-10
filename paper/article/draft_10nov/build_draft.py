"""Build the Word files of the 10 November 2026 draft: main text, SI and figure options.
Main = 01_front_intro + 02_results_turning + 03_results_long + 05_discussion + 04_methods (+ references);
SI = si_header + old SI S1-S6 + si_new_sections (tables filled from the result CSVs) + codebook appendix.
Paths: FIGDIR = new figures, FIGS = project figures folder, REPRO = analysis work folder."""
import os, re, subprocess, pandas as pd, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); P = os.path.abspath(f'{H}/../..')
REPRO = os.environ.get('SH_WORK', '/home/user/repro'); FIGDIR = f'{REPRO}/figs_paper'
FIGS = '/mnt/project-files/ShapingHistory/figures'; OUT = os.environ.get('SH_OUT', '/mnt/project-files/ShapingHistory/paper/draft_10nov')
os.makedirs(OUT, exist_ok=True)
BIB = [f'{P}/Library300326.bib', f'{P}/deeplomatics.bib', f'{P}/sections/05_new_refs.bib', f'{P}/article/article_refs.bib',
       f'{P}/centralization/codebook_theory.bib', f'{P}/centralization/lit_centralization.bib', f'{P}/centralization/lit_extra.bib',
       f'{H}/article_refs_10nov.bib']
BIB = [b for b in BIB if os.path.exists(b)]
T = f'{REPRO}/turning'; C = f'{REPRO}/centralization'

def paths(s):
    s = s.replace('FIGDIR/', FIGDIR + '/').replace('FIGS/', FIGS + '/').replace('REPRO/', REPRO + '/')
    return s.replace('../../figures/', FIGS + '/')

def md(df, cap):
    df = df.copy()
    for c in df.columns:
        if df[c].dtype.kind == 'f': df[c] = df[c].map(lambda v: '' if pd.isna(v) else (f'{v:.3f}' if abs(v) < 10 else f'{v:.0f}'))
    head = '| ' + ' | '.join(map(str, df.columns)) + ' |\n|' + '---|' * len(df.columns) + '\n'
    rows = ''.join('| ' + ' | '.join(str(x) for x in r) + ' |\n' for r in df.itertuples(index=False))
    return f'**{cap}**\n\n{head}{rows}\n'

def tables():
    t = {}
    D = pd.read_csv(f'{T}/tablet_dates_consolidated.csv'); g = D[D.bce.notna()]
    s = g.groupby('date_source').agg(tablets=('id', 'size'), to_the_year=('year_known', lambda v: int(v.astype(bool).sum()))).sort_values('tablets', ascending=False).reset_index()
    t['si_dates_sources'] = md(s, 'Table S7.1. Source of the final date of each tablet dated in years BCE.')
    for suf, lab in [('', 'VAE'), ('_dinov2', 'DINOv2')]:
        if not os.path.exists(f'{T}/tp_protocol_events{suf}.csv'): continue
        E = pd.read_csv(f'{T}/tp_protocol_events{suf}.csv')
        e = E[['event', 'type', 'control', 'n_before', 'n_after', 'strata', 'vae_shift', 'vae_shift_null_median', 'vae_shift_excess', 'p_vae_shift', 'q_vae_shift', 'vae_disp', 'q_vae_disp']].rename(columns={
            'vae_shift': 'change', 'vae_shift_null_median': 'null median', 'vae_shift_excess': 'excess', 'p_vae_shift': 'p', 'q_vae_shift': 'q', 'vae_disp': 'log dispersion ratio', 'q_vae_disp': 'q (dispersion)'})
        t.setdefault('si_tp_events', ''); t['si_tp_events'] += md(e, f'Table S8.1{"a" if suf == "" else "b"}. Turning-point protocol, {lab} features: change in form (length of the 12 stratum-weighted median shifts, robust SD units), its null median, excess, permutation p and BH q; dispersion after vs before.')
        F = pd.read_csv(f'{T}/tp_protocol_features{suf}.csv')
        f = F[F.feature.isin(['loghw', 'corner_fill', 'rect', 'taper', 'thick_side', 'thick_end']) & F.control.str.startswith('site x type,') & F['shift'].notna()]
        f = f[['event', 'feature', 'n_measured', 'shift', 'p_shift', 'q_shift', 'log_disp', 'q_disp']]
        t.setdefault('si_tp_features', ''); t['si_tp_features'] += md(f, f'Table S8.2{"a" if suf == "" else "b"}. Simple measures at each event ({lab} run; strata of site and type): median shift in robust SD units and dispersion ratio. loghw = log height/width; corner_fill, rect (rectangularity), taper, thick_side, thick_end as defined in S6.4.')
        if os.path.exists(f'{T}/tp_power{suf}.csv'):
            pw = pd.read_csv(f'{T}/tp_power{suf}.csv')[['event', 'n_before', 'n_after', 'strata', 'null_95', 'observed', 'mds_sulgi39_direction', 'mds_random_direction', 'power_at_Sulgi39_excess', 'power_at_Ibbi-Suen3_excess']]
            t.setdefault('si_tp_power', ''); t['si_tp_power'] += md(pw, f'Table S8.3{"a" if suf == "" else "b"}. Power of each test ({lab}): 95th percentile of the null, observed change, smallest change detectable with 80% power (in the direction of the Puzriš-Dagan change, and averaged over random directions), and power at the excess observed at Šulgi 39 and at Ibbi-Suen 3.')
            pp = pd.read_csv(f'{T}/tp_power_pooled{suf}.csv')
            t.setdefault('si_tp_pooled', ''); t['si_tp_pooled'] += md(pp, f'Table S8.4{"a" if suf == "" else "b"}. Pooled tests by type of event ({lab}).')
    if os.path.exists(f'{T}/cp_scan_points.csv'):
        sp = pd.read_csv(f'{T}/cp_scan_points.csv')[['stretch', 'group', 'year', 'n_before', 'n_after', 'strata', 'excess', 'q', 'near_event']].fillna('')
        t['si_scan_points'] = md(sp, 'Table S9.1. Change points of the blind scan, for all sites and types together and within site and type groups of at least 200 dated tablets.')
    pt = pd.read_csv(f'{C}/stats_period_table.csv').rename(columns={'Unnamed: 0': 'period'})
    t['si_period_table'] = md(pt, 'Table S10.1. Uniformity of archival tablets and polity indices by period. MAD = median absolute deviation of log height/width (pooled, and within museum); VAEd = median distance from the period median in the 12 VAE dimensions.')
    t['si_spearman'] = md(pd.read_csv(f'{C}/stats_spearman.csv'), 'Table S10.2. Spearman correlation of uniformity with each index (14 periods), permutation p (50,000), and the median and 2.5-97.5% range across 2,000 redraws of the score table.')
    t['si_wild'] = md(pd.read_csv(f'{C}/stats_wild_cluster.csv'), 'Table S10.3. Tablet-level regressions of deviation from the period median (dev_period) and from the period-by-museum median (dev_pm) on each index, museum fixed effects; p from the wild cluster restricted bootstrap (14 clusters).')
    t['si_arch_across'] = md(pd.read_csv(f'{T}/archive_across.csv'), 'Table S11.1. Predicting the archive of a tablet from its shape (leave-one-out nearest median) against permuted labels.')
    t['si_arch_mantel'] = md(pd.read_csv(f'{T}/archive_mantel.csv'), 'Table S11.2. Mantel tests: distances between archive medians against distances in metadata (Spearman, 2,000 permutations).')
    w = pd.read_csv(f'{T}/archive_within.csv')
    keep = [c for c in ['period', 'archive', 'n', 'k', 'silhouette', 'variable', 'levels', 'nmi', 'nmi_null', 'q'] if c in w.columns]
    t['si_arch_within'] = md(w[keep], 'Table S11.3. Within archives: normalised mutual information between shape groups (k-means) and each field, its permutation mean, and BH q.')
    return t

def pandoc(src, dst, extra=()):
    cmd = ['pandoc', src, '-o', dst, '--citeproc', '--resource-path', f'{H}:{FIGS}:{FIGDIR}'] + sum([['--bibliography', b] for b in BIB], []) + list(extra)
    r = subprocess.run(cmd, capture_output=True, text=True)
    warn = [l for l in r.stderr.splitlines() if 'Citeproc' in l or 'not found' in l]
    print(dst, 'ok' if r.returncode == 0 else r.stderr[:500]); print('\n'.join(sorted(set(warn))[:80]))

ref = ['--reference-doc', f'{H}/reference.docx'] if os.path.exists(f'{H}/reference.docx') else []
main = ''.join(open(f'{H}/{f}').read() for f in ['01_front_intro.md', '02_results_turning.md', '03_results_long.md', '05_discussion.md', '04_methods.md'])
main += '\n\n# References\n\n::: {#refs}\n:::\n'
open(f'{H}/_main.md', 'w').write(paths(main)); pandoc(f'{H}/_main.md', f'{OUT}/ShapingHistory_main_draft_10nov.docx', ref)

old = open(f'{P}/article/supplementary_information.md').read()
body = old[old.index('# S1.'):old.index('# S7.')]
tb = tables(); new = open(f'{H}/si_new_sections.md').read()
new = re.sub(r'\{\{TABLE:(\w+)\}\}', lambda m: tb.get(m.group(1), f'*[table {m.group(1)} not available]*'), new)
cb = ''.join(open(f'{P}/centralization/{f}').read() + '\n\n' for f in ['si_codebook_0_intro.md', 'si_codebook_1_A.md', 'si_codebook_2_B.md', 'si_codebook_3_C.md', 'si_codebook_4_limits.md'])
cb = re.sub(r'^(#+) ', lambda m: '#' + m.group(1) + ' ', cb, flags=re.M)   # codebook headings one level down
si = open(f'{H}/si_header.md').read() + body + new + '\n\n# Appendix: Codebook for the polity scores\n\n' + cb + '\n\n# References\n\n::: {#refs}\n:::\n'
open(f'{H}/_si.md', 'w').write(paths(si)); pandoc(f'{H}/_si.md', f'{OUT}/ShapingHistory_SI_draft_10nov.docx', ref)

fo = open(f'{H}/figure_options.md').read()
open(f'{H}/_fig.md', 'w').write(paths(fo)); pandoc(f'{H}/_fig.md', f'{OUT}/ShapingHistory_figure_options_10nov.docx', ref)
