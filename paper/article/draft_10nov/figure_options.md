---
title: "Shaping History: figure options"
subtitle: "Every figure and variant made during the writing, for choosing the PNAS set"
date: "10 November 2026"
---

**How to use this file.** The draft article uses six main figures (Fig. 1 to Fig. 6) and refers to SI figures. Each entry below gives the figure, what it shows, where the draft uses it, and the alternatives. PNAS allows up to six figures and tables for a standard research article; anything not chosen can go to the SI. Figures marked *new* were made for this draft (10 November 2026). All are produced by the numbered scripts in the repository.

**Main set used in the draft (numbered in order of citation).** Fig. 1 turning points (new); Fig. 2 blind scan (new); Fig. 3 polity scores and uniformity (new scatter); Fig. 4 archives (new heatmap); Fig. 5 map of form by millennium (new); Fig. 6 proportions across three millennia (option A strip). The pipeline figure (option B "telescope") could replace Fig. 4 or open the SI.

# 1. Political turning points (new; draft Fig. 1)

![Fig. 1. Change in tablet form at ten political turning points. For each event, the grey bar is the range that chance alone produces (95th percentile of 2,000 within-stratum permutations), and the dot is the observed change (length of the twelve stratum-weighted median shifts in robust SD units, same site and document type on both sides, damage controlled). Filled dots survive Benjamini-Hochberg correction. Left, the VAE features; right, DINOv2 features that never saw a period label. Right margin: tablets before/after, and whether the change survives the museum control.](FIGDIR/Fig1_turning_points.png){width=100%}

*Why it fits the PNAS look:* one panel per representation, events in date order, the reader sees at once which dots leave their grey band. *Alternative:* the earlier heatmap of the pilot (events by feature, below), which shows *what* changed but is harder to read.

![Alternative: pilot heatmap of shifts by feature and event (script 98k, 9 November). Superseded by the protocol figure; kept for the SI if the feature-level view is wanted.](REPRO/turning/tp_heatmap.png){width=85%}

# 2. Form across three millennia, mapped (new; draft Fig. 5)

![Draft Fig. 5. Sites sized by number of photographed tablets and coloured by the share of their tablets whose period the model recognises; dashed lines join peripheral sites to the heartland site nearest in median shape in the same millennium. Answers ShG's note that claim 1 should be shown geographically as well as by shape.](REPRO/figs_paper/FigMap_millennia.png){width=100%}

*Options to consider:* (a) as is, three millennia side by side; (b) a single map with the three millennia as small multiples stacked vertically (better for a one-column PNAS figure); (c) add the median tablet silhouette next to each large site, which would join the "shape" and "geography" views in one image.

# 3. The blind change-point scan (new; draft Fig. 2)

![Draft Fig. 2. Where tablet form changes when the test is not told the dates of political events. Each point compares the archival tablets of the ten years before a year with those of the ten years from it, within the same site and document type; orange points are change points (q < 0.05 and a local maximum); blue ticks are the listed political events.](FIGDIR/Fig3_blind_scan.png){width=100%}

# 4. Pipeline: from one tablet to every tablet (options; SI or main)

![Option A: strip layout, photograph to silhouette to measures to the twelve VAE numbers.](FIGS/FigP_optionA_strip.png){width=100%}

![Option B: "the microscope and the telescope", one tablet (AUCT 3, 084, Horn Museum) beside the whole corpus, with three summary panels.](FIGS/FigP_optionB_telescope.png){width=100%}

![Option C: matrix layout, the three descriptions (proportion, whole silhouette, VAE code) as rows, each with its main result.](FIGS/FigP_optionC_matrix.png){width=100%}

# 5. Corpus overview (options; SI Fig. S1 or main)

![Fig1_final: periods with the shaded millennium band (approved for the earlier Section 2).](FIGS/Fig1_final.png){width=100%}

![Band version.](FIGS/fig1_corpus_overview_band.png){width=100%}

![Blocks version.](FIGS/fig1_corpus_overview_blocks.png){width=100%}

![Timeline version (SI Fig. S1).](FIGS/FigS1_corpus_timeline.png){width=100%}

![Option A corpus overview.](FIGS/fig1_optionA_corpus_overview.png){width=100%}

![Option B: findspot and damage by period.](FIGS/fig1_optionB_findspot_damage.png){width=100%}

![Period medoids: the most typical tablet of each period, drawn from the silhouettes.](FIGS/fig1_period_medoids.png){width=100%}

# 6. Periods read from silhouettes (SI)

![Confusion matrix ordered by date: rows are true periods, columns predicted; outlined cells are confusions larger than the general pull of the predicted period.](FIGS/Fig2_confusion_chrono_draft.png){width=85%}

# 7. Old Babylonian labels (SI or inside Fig. 6)

![DINOv2 version: distance between tablets sharing an Archibab label across museums, relative to permuted labels.](FIGS/Fig3_ob_label_signal_dinov2.png){width=85%}

![VAE version (earlier draft).](FIGS/Fig3_ob_label_signal_draft.png){width=85%}

# 8. Regional lines (SI, or merged into the map)

![DINOv2 version: share of closest matches in another period's group relative to expectation, museum controlled.](FIGS/Fig4_periphery_dinov2.png){width=85%}

![VAE version (earlier draft).](FIGS/Fig4_periphery_draft.png){width=85%}

# 9. Proportions across three millennia (draft Fig. 6; three options)

![Option A: the median tablet of each period drawn to scale at its date, rows by scribal tradition (used in the draft).](FIGS/Fig5_optionA_tablet_strip.png){width=100%}

![Option B: ribbon of the distribution over time.](FIGS/Fig5_optionB_ribbon.png){width=100%}

![Option C: ridgeline of the distribution per period.](FIGS/Fig5_optionC_ridgeline.png){width=100%}

# 10. Scribes fixing the proportions (SI or main)

![Size quintiles of each period's documents, drawn to scale; right, the median ratio by quintile.](FIGS/Fig6_fixed_balance.png){width=100%}

# 10b. Polity scores and uniformity (new; draft Fig. 3)

![Draft Fig. 3. Uniformity of archival tablets within museum against the three polity indices, fourteen periods.](FIGDIR/Fig5_polity_uniformity.png){width=100%}

# 11. Archives (new; draft Fig. 4)

![Across archives: archive medians in shape space and their distances (script 99b).](REPRO/figures/archive_shape_across.png){width=100%}

![Within archives: normalised mutual information of shape clusters with document type, museum, reign, decade, damage and site (script 99b). Answers ShG's note on how claim 2 fits the archive and collection experiment.](REPRO/figures/archive_shape_within.png){width=100%}

# 12. Case studies (SI)

![Amarna letters and the Eanna archive (the earlier main Fig. 7).](FIGS/fig7_amarna_eanna.png){width=100%}

![Amarna letters only.](FIGS/fig7_amarna.png){width=100%}

![Eanna only.](FIGS/fig8_eanna.png){width=100%}

# 13. What the VAE measures (SI)

![What the silhouette adds over the ratio and simple measures (the earlier Fig. 8).](FIGS/fig9_vae.png){width=100%}

![A guide to the twelve VAE dimensions: decoded silhouettes at low and high values of each.](FIGS/fig_vae_dimension_guide.png){width=100%}

# 14. Ideas not yet drawn

- **Polity scores with uncertainty**: the draft Fig. 3 scatter could add horizontal bars for the score uncertainty from the 2,000 redraws.
- **Before and after tablets**: for each significant turning point, the median silhouette of the 20 years before and after, overlaid, at the same site and for the same document type. This would show the reader *what* changed (e.g. corners at Puzriš-Dagan).
- **Ur III convergence**: the distance between Girsu and Umma tablets of the same type by reign (SI S5.5), as a small line chart beside the Ur III turning points.
- **Eanna two steps**: the share of tall lists by decade with the 584 BCE takeover and the accession of Nabonidus marked (now inside the case-study figure).
- **A "dashboard" figure**: one column per period with corpus size, damage, museum concentration, uniformity and recognition, as a PNAS-style compact overview.
