# Experiment register

One line per experiment: the question, the scripts, the result as it stands, and whether it is used in the article.
Status: **main** (main text), **SI**, **kept** (supports a decision, not reported on its own), **withdrawn** (wrong or superseded;
kept here so it is not repeated). Dates are 2026.

## A. Corpus and controls

| # | Question | Scripts | Result | Status |
|---|---|---|---|---|
| A1 | Do the released ratio statistics reproduce? | 01 | Exactly; ~5,100 non-tablets among 94,936 images, tablets only = 87,783 | SI |
| A2 | Robust dispersion of h/w and VAE codes by period | 02, 33, 39 | Ur III and NB tightest on h/w; Neo-Assyrian loosest; VAE and DINOv2 rankings agree (Spearman 0.83) | main |
| A3 | Does the released masked ResNet50 reproduce? | 03 | acc 0.768, macro-F1 0.606 over 14 classes (not 21) | SI |
| A4 | Breakage as a confound | 05, 05b, 06 | Damage index AUC 0.92; with damage as a control the uniformity ranking is unchanged (Spearman 0.99). The earlier "breakage inflates dispersion" claim came from a complete-only filter | main (control) / earlier claim withdrawn |
| A5 | Museum as a confound | 16, 17, 18 | Silhouettes predict the holding museum (Ur III Umma 0.74 vs chance 0.20); period accuracy falls 0.51 to 0.25 museum-held-out; uniformity ranking survives (0.95) | main (control) |
| A6 | Current CDLI labels vs April 2024 labels | 11 | 1.5% of periods changed; ranking stable | SI |
| A7 | Cleaned catalogue dimensions | 38 | 539 swapped h/w fixed, 1,820 impossible ratios dropped (mostly Leiden Böhl) | SI |

## B. Period identification

| # | Question | Scripts | Result | Status |
|---|---|---|---|---|
| B1 | Is h/w alone enough to tell periods? | 12 | No: tree acc 0.39 (the "30.1%" was the majority baseline) | SI |
| B2 | Which periods are confused, corrected for class size | 13, 14 | Achaemenid goes to NB; Persepolis 94% recognised vs 33% for Babylonian Achaemenid; Ebla to ED IIIb | main (Fig 2) |
| B3 | Old Babylonian sub-groups as ancestors of later tablets | 15 | Flips under museum control; OB Ur literary ~ Nineveh library was a British Museum artefact | withdrawn |
| B4 | What OB shape carries across museums | 19b, 20, 21, 24, 27 | Document type > archive (Šamaš-hazir) > city > reign; length explains at most 14% | main |
| B5 | Do document types keep their shape across periods? | 22 | Mostly not once museum is controlled | SI |
| B6 | Which Mesopotamian groups the peripheries resemble | 23, 30 | Kanesh letters ~ MA letters; Nuzi ~ MA; Hattusa ~ MB; Amarna none | SI |
| B7 | Prosobab labels in NB/Achaemenid shape | 25, 26 | Promissory notes recognised across museums (0.94) | SI |

## C. Proportions

| # | Question | Scripts | Result | Status |
|---|---|---|---|---|
| C1 | The long shift from landscape to portrait | 31, 32, 36 | Archival documents turn portrait over time; NA letters/legal tall (credited to Radner 1995) | main (Fig 5) |
| C2 | Ur III formats by province, reign, type | 34, 37, 40, 41 | Girsu-Umma within-type gap 0.156 (Šulgi 1-40) to 0.021 (Ibbi-Suen) | main / SI |
| C3 | Formats within periods | 35 | Size-and-shape groups follow document type | SI |

## D. Case studies

| # | Question | Scripts | Result | Status |
|---|---|---|---|---|
| D1 | Ur III provinces in the silhouette | 45, 49, 57 | Province recognisable within type and museum; VAE beats ratio (Harvard messengers 93 vs 83) | main |
| D2 | Amarna letters: place of making | 44, 46, 50, 51, 55, 59, 62 | Letter form follows place of making over scribe (with Goren 2004, Mandell 2026); same-city neighbour 42% vs chance 29% | main |
| D3 | Eanna under NB and early Achaemenid kings | 48, 52, 53, 54, 58 | Livestock lists turn tall at Nbk 23 (Pirngruber 2021); staples lists only under Nabonidus (two-step change, our addition) | main |
| D4 | What the twelve VAE numbers record | 56, 61, 64 | Proportion R² 0.82, thickness 0.71/0.70, corners 0.46 | main (Fig 9) / notebook |
| D5 | Clay colour from photographs | 47 | Pilot only; removed from the paper | future work |

## E. Centralization (supporting test)

| # | Question | Scripts | Result | Status |
|---|---|---|---|---|
| E1 | First codebook and pilots | 70-79 | Centralization does not make tablets uniform; uniform periods have one producing institution | kept |
| E2 | Literature-grounded scores (12 parameters x 14 periods) | 80, 81_*, 85-85f, 88-92, 95-97 | 915 quoted statements from 166 works; ShG reviewed in three rounds; regional sub-scores | SI |
| E3 | Do the indices predict uniformity? | 86, 107 | Rerun 10 Nov with v2 scores: no index significant; B closest for proportion (rho -0.43, p 0.12); A and C positive for outline within museum (0.47, 0.49; p 0.09, 0.07) | main Fig. 3 / SI S10 |
| E4 | Archive overview per period | 84, 84b | Photos over-represent OB Nippur, lack Mari and Sippar; Girsu and Persepolis under-represented | SI |

## F. Dating from companion databases (9 Nov)

| # | Question | Scripts | Result | Status |
|---|---|---|---|---|
| F1 | Archibab (full table, 36,060 texts) | harvesters/archibab_table_v2.py, 19b, 98d | 2,714 OB links; OB dated 12.2% -> 15.8% | kept |
| F2 | BDTNS, NaBuCCo, Prosobab, Oracc, eBL, Hethport | 37c-37g, 98e-98i | NA dated 3.0% -> 15.8%; Hellenistic 1.6% -> 49%; NB 16% -> 24%; Achaemenid 49% -> 56%; Ur III 76.5% -> 79% | kept |
| F3 | One date per tablet; database wins on conflict | 98j | 31,873 dated (116 Seleucid-era Oracc dates without a king name restored 9 Nov); 362 conflicts flagged | SI dataset |
| F4 | Old Assyrian eponyms (OARE + REL) | 37h, 37i | 1,375 OA tablets in OARE; 47 dated to a year, 13 homonyms as ranges | SI dataset |

## G. Political turning points

| # | Question | Scripts | Result | Status |
|---|---|---|---|---|
| G1 | Pilot: do turning points show in form? | 94 | Urukagina shifts 7/12 VAE dims; Š21/Š39 rectangularity and corners | main (to be confirmed) |
| G2 | Which candidates can be tested (>=30 dated on each side, +/-20 y, same sites) | 98c, 98k | Testable: Urukagina, Šulgi 21, Š39, Ibbi-Suen 3, Hammurabi 1763, Samsu-iluna 1739, Cyrus 539, Darius I 521, Sargon II -> Sennacherib 705, Esarhaddon 681 | main |
| G3 | Hammurabi 1763 inside site x genre cells | 75, 87, 98b, 98f | No shift (39 tests, none at q < 0.05); best break 1791, not the conquest | main (negative result) |
| G4 | Group scan | 99 | 109 groups, 36 differ, 18 survive museum control; mostly genre and place | kept |
| G5 | Reign-only dates heaped at accession years | _reigns.py, 100, 101, 105 | 4,210 reign-dated tablets carried the accession year; windows now admit them only if the whole reign fits. Removes the 1792, 713, 676 BCE scan breaks | SI S7, S12 |
| G6 | One protocol, ten events (10 Nov) | 100 | Robust in all four runs (VAE, DINOv2, with/without museum): Urukagina, Sulgi 39. None in any run: Hammurabi 1763, Esarhaddon 681, Cyrus 539. Mixed: Sulgi 21 (19 tablets before), Ibbi-Suen 3 (DINOv2 only), Samsu-iluna (museum only), Sargon II>Sennacherib (VAE only), Darius I (VAE museum only, 16 after) | main Fig. 1 / SI S8 |
| G7 | Power of each test | 105 | Pooled conquests: no change (VAE p 0.10, DINOv2 p 0.57); power for a Puzris-Dagan-size change 89% (VAE), 57% (DINOv2) | main / SI S8 |
| G8 | Blind change-point scan | 101, 106 | Ur III 2064, 2053, 2036, 2021; none in OB, NA, NB-Achaemenid; group-level matches 63% vs 49% chance (binomial p 0.16) | main Fig. 2 / SI S9 |
| G9 | Map of recognition and nearest heartland site | 104 | Kanesh to Kar-Tukulti-Ninurta, Ansan to Assur/Persepolis line, Alalakh to Ur (museum artefact) | main Fig. 5 |

## H. Archives

| # | Question | Scripts | Result | Status |
|---|---|---|---|---|
| H1 | Do shape groups follow genre or other metadata across and within archives? | 99b | Rerun 10 Nov with Ur III provinces: text type significant in 11 of 20 archives (Merkes A2 0.37, Ea-ilūtu-bāni 0.26, Murašû 0.18, Šamaš-hazir 0.18); reign strongest in none; museum leads at Puzriš-Dagan (0.22) | main Fig. 4 / SI S11 |
| H2 | Orthography against shape (OA) | none | Out of scope (ShG, 9 Nov) | not run |

## Run on ShG's computers

Copied 10 Nov 2026 into `analysis/mac_studio/` (Archibab 01-09, museum tests, NaBuCCo and Prosobab parsers, pipeline figure). DINOv2 ViT-B/14 embeddings computed on the Mac Studio, read by script 103.
