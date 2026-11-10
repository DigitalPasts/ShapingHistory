# deeplomatics-repro — index of analyses (M3 Ultra, 25–26 Oct 2026)

Data
- zenodo/ — Zenodo 12787746: binary masks (images_b_w_tablets, 94,936), VAE encodings (train/val/test), h_w_ratio
- zenodo_models/ — Zenodo 11668220: masked ResNet50 checkpoint (grayscale ResNet50 checkpoint NOT available; see results/TASK1_status.md)
- results/emb_dinov2_vitb14_224.npy (+ _ids.csv) — DINOv2 ViT-B/14 CLS embeddings, 92,876 masks
- archibab/archibab_textes.csv — Archibab text table (31,100 of 36,060 ids; ~14% missing from duplicate pages)
- prosobab/data/ — Prosobab dump (DANS doi:10.17026/DANS-ZVN-EECE, CC BY-NC) + parsed CSVs
- nabucco/ — Nabucco Omeka XML (github.com/DigitalPasts/nabucco, 2021) + nabucco_items.csv
- gh-ShapingHistory/ — clone of github.com/shaigordin/ShapingHistory

Analyses (script -> outputs)
- results/01_dinov2_embed.py, 02_dispersion.py — VAE vs DINOv2 period / site dispersion (VAE numbers reproduced)
- results/03_resnet50_masked_rescore.py — masked ResNet50 re-score (acc 0.768, collapsed macro-F1 0.606 = notebook 9.1)
- museum_tests/museum_tests.py — museum confound (within-site museum prediction; random vs museum-held-out; BM -> Neo-Assyrian)
- museum_tests/ob_tracing.py — OB-city tracing with CSLS; hubness (Nerebtum etc.)
- archibab/01_link_archibab_cdli.py, 02_archibab_analyses.py — Archibab link (1,969 photographed OB tablets), label audit, dispersion
- archibab/03_label_signal.py — label signal across museums (type strongest)
- archibab/04_doc_forms_across_periods.py — OB document forms in later periods (museum-controlled)
- archibab/05_periphery_sources.py — periphery groups vs core periods (museum-controlled lifts)
- archibab/06_type_by_site.py — same type, same vs different findspot within museum (local forms in all groups)
- archibab/08_followups.py — MB letter cell (Penn/Nippur), Achaemenid split, concrete examples
- archibab/09_fig_tables.py — compact tables for the final figures
- prosobab/07_nb_label_signal.py — NB/Achaemenid label signal (promissory note 0.94)

Open items
- Grayscale ResNet50 checkpoint: probably still in lightning_logs/ on dt-gpu-02 (account kapond).
- Optional: merge ~58 extra Nabucco tablets into the Prosobab test.
- Optional: re-run archibab_table.py slowly (PAUSE 2 s) to fill the ~4,960 missing Archibab ids.
