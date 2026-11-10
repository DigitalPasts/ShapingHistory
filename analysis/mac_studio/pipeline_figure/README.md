# Pipeline / opener figure — three options (draft, 27–28 Oct 2026)

Example tablet: AAS 015 = Louvre AO 19752 (P100003), Ur III administrative, Umma, Šulgi 46.
Photo: CDLI (cdli.earth/dl/photo/P100003.jpg); mask: Zenodo 12787746; shape code, reconstruction and z2 traversal:
the published VAE checkpoint (epoch=22-step=213621) run on that mask; corpus panels: Zenodo VAE codes (87,783 tablets) and
results/disp_vae_* (the dispersion values reproduced earlier).

- option_A_landscape_strip.(pdf|png|svg): one-row pipeline (photo -> grayscale -> mask -> encoder -> 12-d code -> decoder -> decoded,
  plus obverse h/w measurement), z2 traversal and nearest cross-museum neighbours, then B proportion histogram, C shape-space map,
  D dispersion by period, E between-city convergence. Double-column, 7.08 x 4.9 in.
- option_B_portrait_narrative: three titled bands (A photograph -> outline, B VAE, C comparing groups incl. a schematic of the
  dispersion statistic). Full page, 7.08 x 7.6 in.
- option_C_hub: the photograph at the centre, methods arranged around it (preprocessing, encoding, proportion, shape space,
  nearest neighbours, dispersion, convergence). 7.08 x 6.4 in.

Notes / to check
- Shape classes use placeholder cut-offs: landscape h/w < 0.9, nearly square 0.9-1.1, portrait > 1.1 (HW_LO/HW_HI in figures.py). Align with the paper.
- h/w is the obverse bounding box (165 x 169 px for AAS 015 = 1.02, identical to h_w_ratio_df_all.csv).
- z2 is the latent dimension most correlated with h/w (r = -0.67 over the corpus); traversal = decoder(mu + k*sd*e2), k = -2..2.
- Nearest neighbours: z-scored 12-d codes, Euclidean, tablets held in other museums only; all 6 are Ur III (4 Puzriš-Dagan, 2 Umma).
- Colours: Ur III blue, Old Babylonian orange, Neo-Assyrian aqua (first three slots of a colour-blind-checked palette); clay brown for masks.
Scripts: prep.py (data), figures.py (all three options).
