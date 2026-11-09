# Analysis code

Every number and figure in the article comes from a script in `scripts/`. Scripts are numbered in the order they were written;
the stages below group them by the part of the paper they serve. Each script starts with a docstring that says what it reads,
what it does and what it writes.

## Running

```bash
pip install -r analysis/requirements.txt
export SH_WORK=/path/to/work        # data folder: inputs from data/README.md, outputs are written here
cd analysis/scripts && python 71_build_master.py   # then any script, e.g. python 98k_testability_all_dates.py
```

Paths are set in `scripts/_paths.py` (`SH_WORK`, `SH_SHARED`, `SH_FIGS`, `SH_PAPER`, `SH_LIT`). The original runs used
`/home/user/repro` (work) and the shared project folder; both now default to `<repo>/work`.

`harvesters/` holds the two scrapers that must run on a computer where the site opens normally (Archibab, Oracc).
`templates/` holds the HTML and markdown templates used by the page and SI builders.

Three inputs are not redistributed here and must be obtained from their owners (see `data/README.md`): the Archibab text table,
the OARE published-texts file (Deep Past Challenge release) and the literature PDFs used to check quotations.

## Stages

### A. Corpus, data quality and controls

Paper: Section 2, SI S1-S2.

| Script | What it does |
|---|---|
| `01_ratio_stats.py` | Independent re-computation of h/w ratio statistics (physical = CDLI catalogue dims, pixel = Zenodo silhouettes). |
| `02_vae_dispersion.py` | Tablet-only shape dispersion: robust h/w measure and VAE latent dispersion, by period and by site x period. Latent dispersion = median Euclidean distance of eac |
| `03_eval_resnet_masked.py` | Re-score (masks fed as released, no second blur) the released masked ResNet50 (Zenodo 11668220) on its own test split (= VAE test csv ids), all objects vs table |
| `04_fig1_medoids.py` | Figure 1: the corpus seen whole. For each period (tablets only, n>=100), the tablet whose z-scored 12-d VAE code lies nearest the period's coordinate-wise media |
| `05_mask_quality.py` | Mask quality per tablet: number of large components, obverse solidity, enclosed-hole area. Used to (a) quantify holes in the Zenodo masks and (b) pick complete, |
| `05b_face_features.py` | Per-tablet outline features of the two largest faces (obverse, reverse): solidity, extent, area ratio. A broken tablet has an irregular (non-convex) outline; a  |
| `06_preservation_control.py` | Preservation as a control (not a filter). 1. A per-tablet damage score: logistic model predicting CDLI's own preservation label (fragment/partial vs complete) f |
| `07_fig1_corpus_overview.py` | Figure 1 option A, 'the corpus seen whole': one column per period (chronological), showing the typical tablet as found (nearest the period median, any preservat |
| `08_fig1_optionB_scatter.py` | Figure 1 option B, panel b: where each period's tablets come from and how broken they are. x = share of the period's tablets from its main findspot; y = share i |
| `09_period_table.py` | Period table for the SI, regenerated from the released data (tablets only) and checked against the current CDLI catalogue (artifacts.csv export; an 800-tablet s |
| `11_current_labels_check.py` | Does relabelling in the current CDLI catalogue (vs the April 2024 labels used for training) change the uniformity results? Recompute VAE latent dispersion by pe |
| `38_clean_dimensions.py` | Cleaned catalogue dimensions for Section 4. 1 Tablets only (CDLI artifact_type contains 'tablet'), height and width given. 2 Checked against the photograph (Zen |
| `39_period_table_clean.py` | Period table on the cleaned dimensions (script 38): all tablets and archival documents only. Uniformity = median absolute deviation of log(h/w) (MAD), with 95%  |
| `56_silhouette_geometry.py` | Each silhouette is a composite of six views in the CDLI 'fat cross' layout: top edge, obverse with the left and right edges beside it, bottom edge, reverse. The |
| `71_build_master.py` | Tablet-level master table for the centralization pilots. Joins: VAE codes (Zenodo 12787746), CDLI catalogue (artifacts.csv, export used by the project), damage  |

### B. Period identification, museum and archive signal

Paper: Section 3, SI S3.

| Script | What it does |
|---|---|
| `12_ratio_tree_baseline.py` | Period from the single h/w ratio: decision tree on the ResNet/VAE train split, scored on the same test split. Reports accuracy, macro-F1 over all true classes,  |
| `13_confusion_class_size.py` | Confusions of the released silhouette model, corrected for class size. Lift(i->j) = P(pred=j / true=i, error) / P(pred=j / error, true not in {j}); >1 means i i |
| `14_fig2_confusion_chrono.py` | Figure 2: chronological confusion map of the released silhouette model (tablets only). Cell shade = share of a period's test tablets assigned to each period (ro |
| `15_ob_subgroups_neighbours.py` | Which Old Babylonian sub-groups do later tablets resemble? Damage-adjusted VAE codes (as in 06). For each non-OB tablet, take its k=25 nearest OB tablets; count |
| `16_collection_signal.py` | Do silhouettes carry the holding collection (photography/imaging conventions), beyond city and period? Within one period and one findspot, predict the museum fr |
| `17_dispersion_collection_control.py` | Does the period uniformity ranking survive a museum control? (a) damage-adjusted VAE codes further residualised on museum within period (museum fixed effects, m |
| `18_period_by_museum_split.py` | How much of period recognition is museum? Period classifier on damage-adjusted VAE codes (+damage), random 5-fold CV vs museum-grouped 5-fold CV (no museum in b |
| `19b_archibab_match_v2.py` | Link Archibab texts (full table, all 36,060 texts, saved 9 Nov 2026 by archibab_table_v2.py) to CDLI photographed OB tablets, by museum number and by publicatio |
| `20_archive_signal_across_museums.py` | Is an Old Babylonian archive recognisable in tablet shape ACROSS museums? For each Archibab archive held in >=2 museums (>=8 tablets each in >=2 museums): mean  |
| `21_ob_label_signal.py` | Which Archibab labels does tablet shape carry within Old Babylonian, beyond museum? For a label (date bin, writing site, text type, archive), each group with >= |
| `22_doc_type_across_periods.py` | Do document types keep their shape across periods? OB reference groups = Archibab text types (museum-balanced centroids: mean of per-museum medians, museums wit |
| `23_periphery_sources.py` | Which Mesopotamian groups do peripheral tablet groups resemble? For each peripheral group (period x site outside the Mesopotamian core), rank core groups (perio |
| `24_accounts_length.py` | Do Old Babylonian document types keep their form whatever the length of the text? Line counts come from CDLI's ATF transliterations (cdli-gh/data, cdliatf_unblo |
| `25_prosobab_parse.py` | Parse the Prosobab SQL dump (DANS doi:10.17026/DANS-ZVN-EECE, 2022-06-03) into CSVs. |
| `26_prosobab_label_signal.py` | Neo-Babylonian / Achaemenid: does shape carry Prosobab's document subtype, archive and place of writing across museums? Link Prosobab tablets to photographed CD |
| `27_fig_ob_label_signal.py` | Draft figure: what OB tablet shape carries across museums (from 21_ob_label_signal.py output). x = mean distance between same-label tablets in different museums |
| `30_fig_periphery.py` | Draft figure: which Mesopotamian traditions peripheral tablet groups resemble (DINOv2, museum controlled). A: map of peripheral sites with their strongest robus |

### C. Tablet proportions

Paper: Section 4, SI S4-S5.

| Script | What it does |
|---|---|
| `31_section4_shape.py` | Section 4 checks on the height-to-width ratio (physical dimensions from the CDLI catalogue, tablets only). 1 robust dispersion by period, raw and within museum, |
| `32_section4_extra.py` | Section 4 extras: Leiden dimension errors, width vs height growth with text length, density peaks of log h/w. |
| `33_uniformity_two_measures.py` | Uniformity of h/w by period on two measures: catalogue dimensions and photographs (Zenodo silhouettes). Photographs restricted to cleanly masked, unbroken table |
| `34_ur3_formats.py` | Ur III tablet formats: province, reign, text type (tagged from CDLI ATF keywords) and size. Catalogue dimensions (tablets only, h/w between 0.05 and 9). For eac |
| `35_formats_within_period.py` | Formats inside a period: do size-and-shape groups follow document type, archive, city or reign? Old Babylonian (Archibab labels) and Neo-Babylonian/Achaemenid ( |
| `36_fig5_shift_options.py` | Figure 5 options (the shift in tablet proportions) and Figure 6 (what the scribe held fixed). Catalogue dimensions, tablets only. Rows are scribal traditions; c |
| `37_bdtns_types.py` | Download BDTNS (Database of Neo-Sumerian Texts, bdtns.cesga.es; M. Molina, CSIC) text-type labels for Ur III texts, as an independent check on the keyword taggi |
| `40_bdtns_check.py` | Check the keyword tagging of Ur III text types (script 34) against BDTNS text-type labels (script 37), and repeat the Girsu/Umma comparison on BDTNS labels alon |
| `41_ur3_tagging_evidence.py` | SI evidence for the Ur III text types: for every measured archival Ur III tablet, the type used in Section 4, its source (BDTNS label or transliteration keyword |

### D. Case studies (Ur III provinces, Amarna, Eanna) and what the VAE adds

Paper: Section 5, SI S6.

| Script | What it does |
|---|---|
| `42_case_study_scan.py` | Feasibility scan for Section 5 case studies: how many tablets (with photograph-based VAE encoding, with catalogue dimensions) are available per site, period and |
| `43_case_b_periphery_probe.py` | Probe for case B (second-millennium peripheries): photograph h/w and VAE distance of each peripheral site to the contemporary Babylonian centre (OB: Sippar, Nip |
| `44_case_b_amarna_probe.py` | Probe for case B: do the Amarna letters carry their sender's region in tablet shape? Sender groups by EA number (Moran 1992 ordering). Photograph h/w and VAE si |
| `45_case_a_ur3_probe.py` | Probe for case A: do Ur III silhouettes (VAE features) carry the province within one museum? Leave-one-out 5-NN on Umma, Girsu, Puzriš-Dagan, Nippur, Garšana ta |
| `46_amarna_senders.py` | Case B data: sender and city of each Amarna letter (attributions after Moran 1992, to be checked against Rainey 2015), clay provenance where Goren, Finkelstein  |
| `46a_cdli_proveniences.py` | Collect CDLI proveniences (id, name, location id) and coordinates of selected locations from the CDLI API. |
| `47_tablet_colour.py` | Pilot: clay colour from CDLI photographs. For each tablet, download the CDLI photo (cdli.earth/dl/photo/P......jpg), mask the black background (V > 0.16 in HSV, |
| `48_nabucco_digeanna.py` | Case C data: DigEanna tablets from NaBuCCo (nabucco.acdh.oeaw.ac.at, ACDH Vienna), scraped from the public browse pages (the API and CSV export returned server  |
| `49_case_a_within_type.py` | Case A: is the Ur III province signal in the silhouette (VAE features) present within one text type and one museum, and does the silhouette distance between Gir |
| `50_amarna_sites.py` | Case B: coordinates for the Amarna sender cities and the control sites. Pleiades first (places dump, Pleiades gazetteer), else CDLI locations (cdli.earth/locati |
| `51_amarna_figure.py` | Case B figure and SI data file. Each Amarna letter: sender and city after Moran 1992, clay provenance where published by Goren, Finkelstein and Na'aman (2002, 2 |
| `52_labasi_tablets.py` | LaBaSi (Late Babylonian Signs, ACDH Vienna): tablet records with scribe, archive, place, date and ductus, from the public API (labasi.acdh.oeaw.ac.at/data/api/t |
| `53_eanna_analysis.py` | Case C: the Eanna archive under the Neo-Babylonian and early Achaemenid kings. DigEanna records (NaBuCCo, script 48) give date, text form, legal purpose and the |
| `54_eanna_figure.py` | Case C figure: the Eanna documents, 630 to 520 BCE. (A) median height-to-width ratio of notes (photograph proportion, CDLI) in five-year bins; (B) share of list |
| `55_goren_catalogue.py` | Case B: the per-letter catalogue of Goren, Finkelstein and Na'aman, Inscribed in Clay (2004), parsed from the text of the book (supplied by ShG). Each catalogue |
| `57_vae_case_studies.py` | What does the VAE add to hand measurement in the three case studies? For each question the same classifier is run on several descriptions of the same tablets: ( |
| `58_vae_eanna_within_collection.py` | Eanna, early (Kandalanu-Nebuchadnezzar) vs late (Nabonidus-Cambyses) tablets of one text form, compared within collections: each collection contributes equal nu |
| `59_vae_amarna_retrieval.py` | Amarna letters in Berlin: does a letter's nearest neighbour in outline space come from the same city (vassals with three or more photographed letters) or from t |
| `60_vae_figure.py` | Fig. 9 (draft): what the VAE adds to hand measurement in the three case studies (scripts 57-59). A: accuracy of the same classifier given the ratio, height and  |
| `61_vae_dimensions.py` | What do the twelve VAE dimensions record? Each dimension is regressed on the twelve view-wise descriptors of script 56 (all tablets with a silhouette in the cas |
| `62_external_photos.py` | Amarna letters not photographed in the CDLI but published as public-domain photographs by their museum. EA 15 (Aššur-uballiṭ I to the king of Egypt): Metropolit |
| `64_vae_dimension_guide.py` | A guide to the twelve VAE numbers, for the notebook and the one-page summary released with the article. For every tablet with a VAE vector (Zenodo 10.5281/zenod |

### E. Centralization parameters from the literature (supporting test)

Paper: SI codebook and literature SI.

| Script | What it does |
|---|---|
| `70_seshat_extract.py` | Extract Seshat Equinox-2020 codes for the polities matching the paper's periods. Source: seshat-equinox-23-10-20.csv (Zenodo 10526926, a copy of the Equinox-202 |
| `72_centralization_scores.py` | Centralization parameters for the periods of the article: codebook, scores, evidence and references. Draft for ShG's correction (28 Oct 2026). Every score is an |
| `73_pilot_period_level.py` | Pilot 1 (points 3, 4, 7): do period-level centralization scores predict how uniform, and how tall, each period's documents are? Unit = period row of the paramet |
| `74_pilot_cells_logistic_vae.py` | Pilot 2 (points 5, 6, 7): genre, place and the centralization parameters, at the level of cells and of tablets. Data: archival documents with photographs (Admin |
| `76_pilot_production.py` | Pilot 4 (point 8): regime and tablet production. (a) Ur III, year by year: number of dated tablets in the whole CDLI catalogue (photographed or not) per provinc |
| `77_pilot_parameters_vs_features.py` | Pilot 3 (point 7): which elements of form go with which parameter? Elements = proportion (log h/w, photographs) and four features estimated from the twelve VAE  |
| `78_build_plan_page.py` | Build the plan page (HTML) from the codebook, the scores and the pilot outputs of scripts 70-79. Template: repro/plan_template.html (the string __DATA__ is repl |
| `79_seshat_compare.py` | Compare the ANE codebook (script 72) with Seshat Equinox-2020 codes for the matching polities (script 70). Matches are approximate (Seshat polities are dynastie |
| `80_ohane_index.py` | Index the five OHANE volumes by page so that every quotation can be cited exactly. Input: OHANE_{I..V}.pdf (K. Radner, N. Moeller, D. T. Potts eds., The Oxford  |
| `84_archive_inventory.py` | Archive inventory per period (ShG, 3 Nov 2026: 'certain kinds of evidence come only from specific archives ... we should have weights for that built in'). For e |
| `84b_archive_overview.py` | Archives and known tablet collections per period (ShG, 9 Nov 2026: "add to the assessment the overview of archives and known tablet collections ... especially i |
| `85_build_scores.py` | Build literature-grounded centralization scores from the evidence files 81_lit_evidence_*.py. |
| `85a_shg_verdicts.py` | Read ShG's assessment worksheet (uploaded 3 Nov 2026) and store his verdicts so the scoring can apply them: Evidence sheet K = accept / reject, L = comment, D = |
| `85b_build_scores_v2.py` | Scoring v2 (4 Nov 2026), after ShG's review of ED IIIa, ED IIIb and Ebla. Changes from v1 (85_build_scores.py): 1. In-between scores. A statement may imply a ha |
| `85c_basis_pass.py` | Systematic confidence pass (4 Nov 2026, ShG's rubric). Every statement that had no hand-coded basis was read again and given: basis (assertion / fragmentary / d |
| `85d_shg_verdicts_8nov.py` | ShG's second assessment (desk, 4-8 Nov 2026). The desk saved verdicts to its artifact database (collections stmverdicts and cellverdicts); the export is kept in |
| `85e_regional_export.py` | Regional sub-scores in a flat table (ShG, 8 Nov 2026: 'how does one see in the final dataset the different regional scores?'). One row per period x parameter x  |
| `85f_shg_verdicts_9nov.py` | ShG's third pass on the desk (night 8-9 Nov 2026). Export: centralization/shg_stmverdicts_9nov.json and shg_cellverdicts_9nov.json (the 8 Nov export with every  |
| `86_robust_stats.py` | Robust tests of the centralization hypothesis on the 14 main periods, using the literature-grounded scores (script 85). |
| `88_lit_bib.py` | BibTeX for the literature SI (sources quoted in 81_lit_evidence_*.py). Keys follow ShG's Zotero (Better BibTeX); entries already in Library300326.bib are copied |
| `89_review_sheet.py` | Review workbook for ShG: scores with ranges, every quoted statement with its citation, gaps, and the statistics. Opens in Excel or Google Sheets; the 'ShG verdi |
| `90_review_page.py` | Build the HTML review page (literature evidence, scores, statistics, Hammurabi break points). |
| `91_assessment_worksheet.py` | Assessment worksheet for ShG: re-score every cell from the quoted literature, mark whether a score rests on evidence of absence or on a silent record, and see t |
| `92_si_codebook.py` | SI text codebook for the centralization parameters: definitions, origin, anchors with operational tests, decision rules, boundary cases, and for every period th |
| `93_keibi_screen.py` | Bibliometric screen of the KeiBi bibliography (vergil.uni-tuebingen.de/keibi, public VuFind search, RSS view). For each period, harvest every KeiBi title that m |
| `95_quote_context.py` | Locate every quoted statement in the full texts of the works (Dropbox PDFs converted with pdftotext) and keep the surrounding passage, the PDF page and the Drop |
| `96_assessment_page.py` | Build the one-page assessment desk (HTML) for ShG: rewritten codebook, every cell with its statements in context, links to the PDFs, archive inventory, regional |
| `97_bibliometrics.py` | Bibliometric overview of the field for the 14 main periods x 12 parameters (4 Nov 2026). Sources (ShG's Dropbox, Data-Files/ANE-Bibliography; copied to /home/us |
| `ohane_tools.py` | Helpers to read OHANE chapters with exact citations (used while scoring; see 81_literature_scores.py). |
| `refs_centralization.py` | Reference list for the centralization codebook and plan (keys as used in script 72). [check] = page range or detail not verified tonight; existing article keys  |
| `81_lit_evidence_*.py` (52 files) | Quoted statements from the literature, with page citations, one file per period and reading round; read by 85b. |

### F. Companion databases and dating

Paper: Methods, SI datasets.

| Script | What it does |
|---|---|
| `10_hittite_konkordanz.py` | Finer dating for the Hittite tablets from S. Kosak, Konkordanz der hethitischen Keilschrifttafeln (hethiter.net/: hetkonk), queried by inventory number, then by |
| `37c_bdtns_dates.py` | ShG's guide note of 9 Nov 2026: date the Ur III tablets from BDTNS (Database of Neo-Sumerian Texts, bdtns.cesga.es, M. Molina, CSIC) where the CDLI date field i |
| `37d_ebl_metadata.py` | ShG's note of 9 Nov 2026: metadata for our photographed tablets from the electronic Babylonian Library (eBL, www.ebl.lmu.de, LMU Munich), through its public API |
| `37e_nabucco.py` | ShG's note of 9 Nov 2026: NaBuCCo (Neo-Babylonian Cuneiform Corpus, nabucco.acdh.oeaw.ac.at; Jursa, Abraham, Gordin) metadata for our Neo-Babylonian, Achaemenid |
| `37f_hethport_konkordanz.py` | ShG's note of 9 Nov 2026: findspot, script date (ah./mh./jh., Old/Middle/New Hittite) and CTH for our photographed Hittite tablets from S. Košak's Konkordanz de |
| `37g_prosobab.py` | ShG's note of 9 Nov 2026: Prosobab (Waerzeggers and Groß 2022, DANS doi:10.17026/dans-zvn-eece, dump of 3 June 2022) for our Neo-Babylonian and Achaemenid table |
| `37h_oare_metadata.py` | Old Assyrian metadata from OARE (Old Assyrian Research Environment, BYU), published_texts.csv as released for the Deep Past Challenge (Kaggle, deep-past-initiat |
| `37i_rel_eponym_dates.py` | Old Assyrian eponym dates (ShG, 9 Nov 2026). 1) REL: the Revised Eponym List of Barjamovic, Hertel and Larsen 2012 (Ups and Downs at Kanesh, PIHANS 120, Appendi |
| `98_dated_counts.py` | Answers ShG's guide notes of 8 Nov 2026: how many tablets are dated in each period, where from and in which genres, and what lies behind the Hammurabi 'no shift |
| `98d_companion_dates.py` | ShG's guide notes of 9 Nov 2026: complete the dating of the photographed tablets from companion databases. Old Babylonian and Early Old Babylonian: Archibab (fu |
| `98e_bdtns_ur3_dates.py` | ShG's guide note of 9 Nov 2026: Ur III dates from BDTNS where CDLI has none (bdtns/bdtns_dates.csv from 37c). BDTNS date codes: UN/SH/AS/SS/IS + regnal year (Ur |
| `98g_companion_dates_all.py` | All companion databases together (ShG, 9 Nov 2026): dated share per period before and after adding dates from Archibab (OB, 98d), BDTNS (Ur III, 98e), NaBuCCo ( |
| `98h_ebl_summary.py` | What eBL adds to our photographed tablets (37d harvest, 9 Nov 2026): dates (king from eBL's chronology list, Kings.json of the eBL frontend; eponym dates flagge |
| `98i_oracc_dates.py` | Oracc catalogues as packaged for the oracc-parser package (Romach, Spencer and Gordin 2026, Zenodo doi 10.5281/zenodo.20625379, catalogues.zip: the original Ora |
| `98j_consolidated_dates.py` | One date per photographed tablet from CDLI and the companion databases (ShG, 9 Nov 2026). Rule (ShG's guide note): where a specialist database names a different |

### G. Political turning points

Paper: Results (turning points), SI.

| Script | What it does |
|---|---|
| `75_pilot_hammurabi.py` | Pilot 5 (point 9): did legal documents become more uniform, or converge between north and south, after Hammurabi conquered Larsa (1763 BCE)? Dates: Archibab abs |
| `87_hammurabi_breaks.py` | Point 9 revisited: which event in Hammurabi's reign (if any) marks a change in legal tablets? Candidate break points, chosen from the historical literature befo |
| `94_turning_points_pilot.py` | Pilot: do political turning points show up in tablet form, and in which features? (ShG, 3 Nov 2026: place turning points on a timeline and correlate them with e |
| `98b_hammurabi_cells.py` | T7 (Hammurabi conquers Larsa, 1763) inside the only site x genre cells with at least 10 dated tablets on both sides (1790-1764 vs 1763-1739). Standardized media |
| `98c_candidate_testability.py` | Testability of every turning-point candidate (ShG, 8 Nov 2026): dated archival tablets within +/-20 years of the date, at named sites present on both sides. Chr |
| `98f_hammurabi_cells_archibab.py` | 98b rerun with Archibab years added (98d): T7 (Hammurabi conquers Larsa, 1763) inside every site x genre cell with at least 10 dated tablets on both sides (1790 |
| `98k_testability_all_dates.py` | 98c rerun with the consolidated dates of 98j (CDLI + Archibab, BDTNS, NaBuCCo, Prosobab, Oracc, eBL; ShG 9 Nov 2026). Same rule: archival tablets (administrativ |
| `99_group_scan.py` | First-step scan (ShG, 8 Nov 2026): how many distinct ('interesting') tablet groups exist per period, by area and genre, before any turning point is tested. A gr |

### H. Shape groups across and within archives

Paper: Results / Discussion.

| Script | What it does |
|---|---|
| `99b_archive_shape_groups.py` | Shape groups across and within archives (ShG, 9 Nov 2026): do the groups that tablet shape forms line up with genre, date, holding museum or other metadata? Arc |

### I. Figures and SI assembly

Paper: Figures, SI.

| Script | What it does |
|---|---|
| `pipeline_fig_options.py` | Three layouts of the pipeline opener figure. Usage: python options.py [A/B/C ...] |
| `pipeline_fig_panels.py` | Shared data and panels for the pipeline opener figure (three layout options in options.py). Example tablet: AUCT 3, 084 (P104315), Ur III, Puzriš-Dagan, Horn Mu |
| `pipeline_fig_recon.py` | (no docstring) |
| `si_build.py` | Build the SI markdown from si_template.md and the result CSVs, then render .docx with pandoc. Usage: python build_si.py -> /mnt/project-files/ShapingHistory/pap |
