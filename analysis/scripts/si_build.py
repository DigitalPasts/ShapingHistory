"""Build the SI markdown from si_template.md and the result CSVs, then render .docx with pandoc.
Usage: python build_si.py  ->  /mnt/project-files/ShapingHistory/paper/article/supplementary_information.{md,docx}"""
from _paths import PAPER, SHARED, TEMPLATES, WORK
import pandas as pd, numpy as np, re, subprocess, shutil, os
R = WORK+'/results'; P = SHARED
FIG = '../../figures'; OUT = PAPER+'/article'
T = open(TEMPLATES+'/si_template.md').read()

def md(df, caption, floatfmt=None):
    df = df.copy()
    for c in df.columns:
        if df[c].dtype.kind == 'f':
            f = (floatfmt or {}).get(c, '{:.2f}')
            df[c] = df[c].map(lambda v: '' if pd.isna(v) else f.format(v))
    head = '| ' + ' | '.join(map(str, df.columns)) + ' |\n|' + '|'.join(['---'] * len(df.columns)) + '|\n'
    rows = ''.join('| ' + ' | '.join(map(str, r)) + ' |\n' for r in df.astype(str).values)
    return f'{caption}\n\n{head}{rows}'

def fig(n, f, cap):
    return f'![**Fig. S{n}.** {cap}]({FIG}/{f})'

tab = {}
# S1 period table
d = pd.read_csv(f'{R}/period_table_SI.csv'); d = d[d.Period_Name != 'other']
d = d.rename(columns={'Period_Name': 'Period', 'tablets': 'Tablets', 'with_mm_dimensions': 'With mm', 'administrative': 'Administrative',
                      'main_findspot': 'Main findspot', 'main_findspot_share': 'Share', 'most_damaged_third': 'Most damaged third',
                      'relabelled_in_CDLI_since_2024': 'Re-dated since 2024'})
for c in ['Administrative', 'Share', 'Most damaged third', 'Re-dated since 2024']: d[c] = (100 * d[c]).round(1).astype(str) + '%'
tab['S1'] = md(d, '**Table S1.** Photographed tablets by period (tablets only; periods as labelled in April 2024). "With mm": catalogue dimensions recorded. Share: share of the main findspot. Most damaged third: share of the period in the most damaged third of the corpus (S2.2).')
# S2 damage ranks
d = pd.read_csv(f'{R}/dispersion_damage_adjusted.csv')[['period', 'n', 'mean_damage', 'disp_raw', 'disp_adj', 'rank_raw', 'rank_adj']]
d.columns = ['Period', 'Tablets', 'Mean damage', 'Dispersion', 'Dispersion, damage removed', 'Rank', 'Rank, damage removed']
d['Rank'] = d['Rank'].astype(int); d['Rank, damage removed'] = d['Rank, damage removed'].astype(int)
r = pd.read_csv(f'{R}/resnet_by_damage.csv')
tab['S2'] = md(d, '**Table S2.** Uniformity of each period before and after removing damage. Dispersion: mean distance of a period\'s tablets from its centre in the VAE space (lower = more uniform) [script 06]. Ranks agree at Spearman 0.99.') + \
    '\n' + 'Accuracy of the released silhouette classifier by damage tercile: ' + '; '.join(f'{a} {b:.2f}' for a, b in zip(r.terc, r.acc)) + '.\n'
# S3 baselines
d = pd.read_csv(f'{R}/ratio_tree_baseline.csv')
d = pd.concat([d, pd.DataFrame([{'model': 'ResNet50 on silhouettes (released)', 'acc': 0.768, 'macroF1_all': 0.43, 'macroF1_collapsed': 0.606},
                                {'model': 'ResNet50 on silhouettes, tablets only', 'acc': 0.781, 'macroF1_all': np.nan, 'macroF1_collapsed': 0.593}])])
d.columns = ['Model', 'Accuracy', 'Macro-F1, 21 labels', 'Macro-F1, 14 classes']
tab['S3'] = md(d, '**Table S3.** Period identification on the released test split. The ratio tree uses the height-to-width ratio alone; "majority" always answers Ur III [scripts 03, 12].')
# S4 museum held out (VAE)
d = pd.read_csv(f'{R}/period_by_museum_split.csv').rename(columns={'Unnamed: 0': 'Measure'})
d.columns = ['Measure', 'Random split', 'Museums held out']
tab['S4'] = md(d, '**Table S4.** Period identification from the damage-adjusted VAE codes (gradient-boosted trees, twelve periods, at most 3,000 tablets each): accuracy, macro-F1 and recall per period, with a random five-fold split and with museums held out [script 18]. The DINOv2 classifier of the main text gives 0.57 and 0.30.')
# S5 museum signal
d = pd.read_csv(f'{R}/collection_signal.csv')[['test', 'classes', 'n_per_class', 'bal_acc', 'chance']]
d.columns = ['Test', 'Groups', 'Tablets per group', 'Balanced accuracy', 'Chance']
tab['S5'] = md(d, '**Table S5.** How well the VAE codes name the museum (or city) within one period and findspot [script 16].')
# S6 OB label signal
d = pd.read_csv(f'{P}/dino_label_signal.csv')[['label', 'group', 'n', 'n_museums', 'ratio', 'p']]
d.columns = ['Label', 'Group (Archibab)', 'Tablets', 'Museums', 'Ratio', 'p']
d['p'] = d['p'].map(lambda v: '<0.002' if v == 0 else f'{v:.3f}')
tab['S6'] = md(d, '**Table S6.** Old Babylonian labels: mean distance between tablets with the same Archibab label in different museums, divided by the same after permuting labels within museum (DINOv2 features). Below 1 = shape carries the label. Archibab text types in French as in the database: prêt = loan, reçu/quittance = receipt, location/fermage = lease, achat = purchase, lettre = letter, dépense = expenditure, compte récapitulatif = summary account.')
# S7 periphery
d = pd.read_csv(f'{P}/dino_periphery_split.csv'); d = d[(d.lo > 1.3) & (d.share >= 0.01)].sort_values(['group', 'mode', 'lift'], ascending=[True, True, False])
d['mode'] = d['mode'].map({'all': 'all tablets', 'admin': 'administrative', 'letters': 'letters'})
d = d[['group', 'mode', 'period', 'share', 'lift', 'lo', 'hi']]; d.columns = ['Group', 'Tablets compared', 'Matched period', 'Share of matches', 'Lift', '95% low', '95% high']
tab['S7'] = md(d, '**Table S7.** Regional lines: periods over-represented among the cross-museum nearest neighbours of each group, for all tablets and within administrative documents or letters (lift with 95% interval above 1.3, at least 1% of matches; DINOv2 features). Achaemenid is split into Persepolis and Babylonia. Small groups give wide intervals.')
# S8 cleaning log
d = pd.read_csv(f'{R}/s4_cleaning_log.csv'); d = d[d.n >= 100]
d.columns = ['Period', 'Tablets with dimensions', 'Swapped', 'Dropped', 'Archival share', 'Agreement before', 'Agreement after']
tab['S8'] = md(d, '**Table S8.** Cleaning of catalogue dimensions by period: entries swapped and dropped, share of archival documents, and agreement (Spearman) between catalogue and photographed ratio before and after cleaning [script 38].')
# S9 clean period table
d = pd.read_csv(f'{R}/s4_period_table_clean.csv'); d = d[d.scope == 'archival'].drop(columns='scope')
d = d[['period', 'n', 'median', 'share_wide', 'MAD', 'lo', 'hi', 'MAD_in_museum', 'MAD_in_damage', 'rho_size_ratio', 'width_p10_p90', 'height_p10_p90']]
d.columns = ['Period', 'Documents', 'Median ratio', 'Share wide', 'Uniformity (MAD)', '95% low', '95% high', 'MAD within museum', 'MAD within damage tercile', 'Size vs ratio (ρ)', 'Width mm (10th to 90th pct)', 'Height mm (10th to 90th pct)']
tab['S9'] = md(d, '**Table S9.** Proportions and uniformity of archival documents by period, from cleaned catalogue dimensions [script 31]. MAD = median absolute deviation of the log ratio from the period median.',
               {'Uniformity (MAD)': '{:.3f}', '95% low': '{:.3f}', '95% high': '{:.3f}', 'MAD within museum': '{:.3f}', 'MAD within damage tercile': '{:.3f}'})
# S10 OB and NB types
a = pd.read_csv(f'{R}/s4_ob_type_formats.csv'); a.insert(0, 'Period', 'Old Babylonian (Archibab type)')
b = pd.read_csv(f'{R}/s4_nb_type_formats.csv').rename(columns={'sub': 'type'}); b.insert(0, 'Period', 'Neo-Babylonian (Prosobab type)')
d = pd.concat([a, b]); d.columns = ['Period', 'Type', 'Tablets', 'Median ratio', 'MAD']
tab['S10'] = md(d, '**Table S10.** Median ratio and uniformity of document types in the Old Babylonian and Neo-Babylonian periods (types with at least 15 measured tablets).', {'MAD': '{:.3f}'})
# S11 fixed balance
d = pd.read_csv(f'{R}/s4_fixed_balance.csv')[['period', 'n', 'rho_size_hw', 'med_hw_small', 'med_hw_large']]
d.columns = ['Period', 'Documents', 'Size vs ratio (ρ)', 'Median ratio, smallest fifth', 'Median ratio, largest fifth']
tab['S11'] = md(d, '**Table S11.** Fixed balance: correlation of size with proportion, and the median ratio of the smallest and largest fifth of documents [script 32].')
# S12 Ur III types
d = pd.read_csv(f'{R}/s4_ur3_type_province.csv'); d.columns = ['Type', 'Province', 'Tablets', 'Median ratio', 'Median width mm', 'Median height mm']
tab['S12'] = md(d, '**Table S12.** Ur III text types by province (BDTNS labels, else bookkeeping terms) [script 34].', {'Median width mm': '{:.0f}', 'Median height mm': '{:.0f}'})
# S13 convergence
a = pd.read_csv(f'{R}/s4_ur3_girsu_umma_v2.csv'); v = pd.read_csv(f'{P}/results/case_a_convergence_vae.csv')
d = a.merge(v[['reign', 'n', 'dist']].rename(columns={'n': 'n_vae'}), on='reign', how='left')
d.columns = ['Reign', 'Tablets (ratio)', 'Difference, all types', 'Difference within type', '95% low', '95% high', 'Tablets (VAE)', 'VAE distance within type']
tab['S13'] = md(d, '**Table S13.** Girsu against Umma by reign: difference in log ratio between the provinces, overall and within the same text type, and the VAE distance between the provinces within type [scripts 34, 49].', {'Difference, all types': '{:.3f}', 'Difference within type': '{:.3f}', '95% low': '{:.3f}', '95% high': '{:.3f}'})
# S14 case studies
d = pd.read_csv(f'{R}/vae_case_studies.csv')
d['question'] = d.question.str.replace('Institute for the Study of Ancient Cultures West Asia & North Africa Museum', 'ISAC Chicago').str.replace('Harvard Museum of the Ancient Near East', 'Harvard HMANE')
d = d[['case', 'question', 'n_each', 'tier', 'acc', 'chance', 'p']]
d.columns = ['Case', 'Question', 'Tablets per group', 'Description', 'Balanced accuracy', 'Chance', 'p']
tab['S14'] = md(d, '**Table S14.** Group assignment from four descriptions of the same tablets (ratio; ruler = catalogue height and width in mm; outline = twelve measured outline and thickness features; VAE = twelve VAE dimensions) [script 57].', {'p': '{:.3f}'})
# S15 Amarna places
d = pd.read_csv(f'{P}/results/SI_amarna_cities.csv'); d = d[d.n_shape >= 3].sort_values('hw', ascending=False)
d = d[['written_at', 'n_shape', 'hw', 'source']]; d.columns = ['Place of making (Goren et al.)', 'Letters measured', 'Median ratio', 'Coordinates']
tab['S15'] = md(d, '**Table S15.** Amarna letters by the place where their clay was formed, places with at least three measured letters [scripts 50, 51, 55].')
d = pd.read_csv(f'{P}/results/SI_amarna_home_abroad.csv'); d.columns = ['Letters at home', 'Number', 'Median ratio', 'Sent to Egypt from', 'Number abroad', 'Median ratio abroad']
tab['S16'] = md(d, '**Table S16.** Letters sent to Egypt against letters of the same realm found at home. Aššur abroad is EA 15 measured on the Metropolitan Museum photograph.')
d = pd.read_csv(f'{R}/vae_amarna_retrieval.csv'); d.columns = ['Grouping', 'Groups', 'Letters', 'Description', 'Closest letter in the same group', 'Chance', 'p']
tab['S17'] = md(d, '**Table S17.** Amarna letters in Berlin: share whose most similar letter comes from the same city (or place of making) [script 59].', {'p': '{:.3f}'})
d = pd.read_csv(f'{P}/nabucco/eanna_by_reign.csv'); d.columns = ['Reign', 'Records', 'Measured', 'Median ratio', 'Landscape', 'Square', 'Portrait']
d['Records'] = d['Records'].astype(int); d['Measured'] = d['Measured'].astype(int)
tab['S18'] = md(d, '**Table S18.** The Eanna archive by reign: DigEanna records, tablets measured on CDLI photographs, median ratio and DigEanna format labels [script 53].')
d = pd.read_csv(f'{P}/nabucco/eanna_lists_by_domain.csv', header=[0, 1], index_col=0); d.columns = ['Lists after Nbk', 'Lists to Nbk', 'Median after Nbk', 'Median to Nbk']
d = d.reset_index().rename(columns={d.index.name or 'index': 'Subject (DigEanna domain)'}); d = d[d.iloc[:, 0] != 'domain']
d = d.iloc[:, [0, 2, 4, 1, 3]]
tab['S19'] = md(d, '**Table S19.** Eanna lists by subject: number and median ratio up to the end of Nebuchadnezzar II\'s reign and after it.')
d = pd.read_csv(f'{R}/vae_eanna_within_collection.csv'); d.columns = ['Text form', 'Collections (before + after)', 'Tablets', 'Description', 'Balanced accuracy', 'Chance', 'p']
tab['S20'] = md(d, '**Table S20.** Eanna, before against after the 560s, within small collections: the VAE adds nothing to the ratio [script 58].', {'p': '{:.3f}'})
d = pd.read_csv(f'{R}/vae_dimension_guide.csv')[['dim', 'closest_name', 'rho', 'reads', 'strength']]
d.columns = ['Dimension', 'Closest measurement', 'Spearman ρ', 'Reading', 'Strength']
tab['S21'] = md(d, '**Table S21.** What each VAE dimension measures: the closest directly measured feature [script 64].')
d = pd.read_csv(f'{R}/vae_feature_recovery_all.csv')[['description', 'R2_well_preserved', 'R2_all', 'n_well_preserved', 'n_all', 'reliability']]
d.columns = ['Feature', 'R², well preserved', 'R², all measured', 'Tablets, well preserved', 'Tablets, all', 'Recovered']
tab['S22'] = md(d, '**Table S22.** How well the twelve VAE numbers recover each measured feature (ridge regression, five-fold cross-validated R²) [script 64].')

figs = {
    'S1': fig(1, 'FigS1_corpus_timeline.png', 'The corpus on a timeline: photographed tablets per period, with dates.'),
    'S2': fig(2, 'Fig2_confusion_chrono_draft.png', 'Periods read from silhouettes (released ResNet50, test tablets). Rows sum to one; the diagonal is the share recognised. Outlined cells are confusions larger than the general pull of the assigned period on errors.'),
    'S3': fig(3, 'Fig3_ob_label_signal_dinov2.png', 'Old Babylonian shape follows the document: ratio of same-label distance across museums to the permuted distance, by Archibab label (Table S6).'),
    'S4': fig(4, 'Fig4_periphery_dinov2.png', 'Regional lines: peripheral groups and the periods over-represented among their cross-museum nearest neighbours (Table S7).'),
    'S5': fig(5, 'Fig5_optionC_ridgeline.png', 'Distribution of the height-to-width ratio of archival documents in each period, in date order (cleaned catalogue dimensions).'),
    'S6': fig(6, 'Fig6_fixed_balance.png', 'Scribes fixing the proportions: the median tablet of each size fifth drawn to scale, smallest in front, with the median ratio of each fifth (Table S11).'),
    'S7': fig(7, 'fig_vae_dimension_guide.png', 'What the clearest VAE dimensions measure: real tablets at the 10th, 50th and 90th percentile of each dimension, typical on the others, with the closest measurement (Tables S21, S22).'),
}
for k, v in tab.items(): T = T.replace('{{TABLE_' + k + '}}', v)
for k, v in figs.items(): T = T.replace('{{FIG_' + k + '}}', v)
left = re.findall(r'\{\{[^}]+\}\}', T); assert not left, left
open(f'{OUT}/supplementary_information.md', 'w').write(T)
os.makedirs(f'{OUT}/si_datasets', exist_ok=True)
for src, dst in [(f'{R}/vae_measured_and_predicted.csv', 'Dataset_S1_vae_measured_and_predicted.csv'), (f'{R}/tablet_dims_clean.csv', 'Dataset_S2_tablet_dims_clean.csv'),
                 (f'{P}/results/SI_amarna_letters.csv', 'Dataset_S3_amarna_letters.csv'), (f'{P}/nabucco/digeanna_merged.csv', 'Dataset_S4_eanna_digeanna_merged.csv')]:
    shutil.copy(src, f'{OUT}/si_datasets/{dst}')
r = subprocess.run(['pandoc', 'supplementary_information.md', '--citeproc', '--resource-path=.:../..', '-o', 'supplementary_information.docx'], cwd=OUT, capture_output=True, text=True)
print(r.stderr[-2000:])
