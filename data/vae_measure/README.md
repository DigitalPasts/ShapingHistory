# VAE measurement tables

Released with Gordin, Kapon Epshtain, Alper and Fire, *Shaping History* (PNAS). Used by the notebook
`14. Measure tablet features from VAE vectors.ipynb` and by the website page *7 · Measuring Tablets*.

| File | Content |
|---|---|
| `vae_measured_and_predicted.csv` | One row per tablet with a VAE vector (92,876). `measured`: the silhouette shows six clean views and was measured (76,049). `well_preserved`: intact obverse outline, obverse and reverse of similar size (47,714). Measured values (`hw`, `thick_side`, ...) and values read from the VAE (`*_pred`, only for features the VAE recovers). |
| `vae_feature_recovery_all.csv` | For each measurement, the share of its variation recovered from the twelve VAE numbers (R², 5-fold CV). |
| `vae_dimension_guide.csv` | For each VAE number, the measurement it follows most closely (Spearman ρ). |
| `vae_dimension_examples.csv` | The CDLI tablets shown in `fig_vae_dimension_guide.png`. |

`scripts/56_silhouette_geometry.py` measures the silhouettes; `scripts/64_vae_dimension_guide.py` builds these tables.
Set the path `R` at the top of each script to a folder holding the Zenodo files
(10.5281/zenodo.12787746: `vae_encoding_df_April16_w_class_*.csv` and the unzipped `images_b_w_tablets/`).
