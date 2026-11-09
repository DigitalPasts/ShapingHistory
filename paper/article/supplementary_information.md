---
title: "Supplementary Information for: Does the state make the document? Three millennia of cuneiform tablet form seen whole"
author: "Shai Gordin, Danielle Kapon Epshtain, Morris Alper, Michael Fire"
date: "Draft, 27 October 2026"
bibliography:
  - ../Library300326.bib
  - ../deeplomatics.bib
  - ../sections/05_new_refs.bib
  - article_refs.bib
link-citations: true
---

<!-- Built by repro/si/build_si.py from si_template.md and the result tables in repro/results. Edit the template, not the output. -->

**How this SI is organised.** Sections S1 to S6 follow the order of the main text. Figure and table numbers refer to the 6-page article; where the full-length version shows a figure in the main text, the SI figure is the same image. Every number below comes from a script in the code release (script numbers in brackets, e.g. [script 31]), run on the Zenodo dataset and the CDLI catalogue as checked in October 2026. Passages marked *Moved from the main text* are the full-length wording of arguments shortened in the article.

**Contents.** S1 Corpus, labels and catalogue checks. S2 Silhouettes and damage. S3 Period identification and the museum layer. S4 Old Babylonian labels and regional lines. S5 Tablet proportions. S6 Case studies and the VAE dimensions. S7 Code, data and datasets.

# S1. Corpus, labels and catalogue checks

## S1.1 The corpus

The Zenodo release contains 94,936 photographs of CDLI objects with period labels as fixed in April 2024 [@cdliContributors2024]. We removed about 5,100 objects that are not tablets (cones, cylinders, bullae, prisms, seals and similar; 72% of the Lagash II objects are cones) using the CDLI artifact type, which leaves 87,783 tablets. Of these, 87,221 fall in the seventeen periods with at least 100 tablets (Table S1). The full period list, with the number of tablets, the share of administrative documents, the main findspot, catalogue dimensions and damage, is Table S1 [script 09].

**Table S1.** Photographed tablets by period (tablets only; periods as labelled in April 2024). "With mm": catalogue dimensions recorded. Share: share of the main findspot. Most damaged third: share of the period in the most damaged third of the corpus (S2.2).

| Period | Tablets | With mm | Administrative | Main findspot | Share | Most damaged third | Re-dated since 2024 |
|---|---|---|---|---|---|---|---|
| Ur III | 27259 | 9739 | 95.7% | Umma | 35.7% | 4.4% | 0.5% |
| Neo-Assyrian | 22207 | 826 | 2.0% | Nineveh | 96.5% | 68.1% | 0.1% |
| Old Babylonian | 16306 | 1488 | 25.5% | Nippur | 40.6% | 37.0% | 0.1% |
| Middle Babylonian | 5901 | 778 | 65.5% | Nippur | 78.0% | 38.3% | 0.2% |
| Neo-Babylonian | 4327 | 436 | 32.7% | unknown | 54.0% | 31.6% | 2.1% |
| Old Akkadian | 2604 | 664 | 94.9% | Adab | 32.2% | 23.8% | 0.1% |
| Achaemenid | 1703 | 241 | 27.6% | Nippur | 42.2% | 22.4% | 0.2% |
| Old Assyrian | 1482 | 85 | 5.1% | Kanesh | 98.9% | 18.6% | 0.1% |
| Early Old Babylonian | 1428 | 212 | 23.9% | Nippur | 44.3% | 29.1% | 0.0% |
| Middle Assyrian | 1405 | 484 | 20.0% | Assur | 77.0% | 34.4% | 0.6% |
| ED IIIb | 1229 | 127 | 96.6% | Girsu | 66.5% | 33.5% | 0.1% |
| Ebla | 424 | 420 | 99.3% | Ebla | 57.3% | 43.6% | 0.0% |
| Uruk III | 301 | 259 | 97.3% | unknown | 90.0% | 32.6% | 5.3% |
| Hellenistic | 243 | 93 | 1.2% | Uruk | 79.4% | 23.9% | 0.0% |
| ED IIIa | 154 | 36 | 88.3% | Shuruppak | 59.1% | 48.7% | 0.0% |
| Lagash II | 140 | 25 | 85.7% | Girsu | 78.6% | 22.1% | 0.0% |
| Hittite | 108 | 19 | 0.0% | Ḫattusa | 83.3% | 85.2% | 100.0% |
| ED I-II | 73 | 12 | 90.4% | Ur | 76.7% | 43.8% | 0.0% |
| Middle Elamite | 22 | 0 | 86.4% | Anšan | 95.5% | 36.4% | 0.0% |
| Middle Hittite | 18 | 2 | 0.0% | Ḫattusa | 77.8% | 83.3% | 0.0% |
| Proto-Elamite | 16 | 0 | 100.0% | Susa | 100.0% | 50.0% | 0.0% |
| Uruk IV | 12 | 5 | 100.0% | unknown | 100.0% | 16.7% | 50.0% |


**Moved from the main text: genres and findspots.** CDLI assigns genres along the conventional Assyriological division between archival documents (administrative, legal, letters) and the literary and scholarly texts of the "stream of tradition" [@oppenheimAncientMesopotamia1977; @pedersenArchivesLibraries1998]. Administrative documents make up 48% of all tablets and more than 85% of every period before 2000 BCE, while a quarter of the tablets, among them 65% of the Neo-Assyrian ones, have no genre assigned. The shape of the corpus is also the shape of what survived and of how it was found: ancient preservation and destruction, chance discoveries, excavation priorities and the antiquities market filled museums with tablets from a few sites [@rattenborgArchaeologicalDistributionCuneiform2023; @michelIdentifyingMissingEvidence2025]. 99% of Old Assyrian tablets come from Kanesh, where the merchants' archives were preserved in their houses in the lower town, while the contemporary archives of Assur remain largely unexcavated [@larsenAncientKanesh2015]. 96% of Neo-Assyrian tablets come from Nineveh, 83% of Hittite tablets from Ḫattuša and 77% of Middle Assyrian tablets from Assur. Another 15% of all tablets have no recorded findspot; for many, it can be reconstructed from publications, museum records or internal evidence such as month names and prosopography [@brumfieldKeyCity2019], but this is an extra step between catalogue and inference. Middle Babylonian tablets come 78% from Nippur, so what we measure as Middle Babylonian practice is largely the practice of Nippur's administration, which may not represent the norm of the Kassite state.

![**Fig. S1.** The corpus on a timeline: photographed tablets per period, with dates.](../../figures/FigS1_corpus_timeline.png)

## S1.2 Catalogue checks

All catalogue fields used here (period, genre, findspot, museum, dimensions, preservation) were compared with the live CDLI database in October 2026 through its public API. The export used for the analysis agrees with the live records except for period labels: CDLI has re-dated 0.85% of the tablets since April 2024 (Table S1, last column). Recomputing every period's uniformity with the current labels changes it by at most 0.05 on the VAE distance scale (Hellenistic) and by less than 0.015 elsewhere [script 11].

CDLI records height and width in millimetres for 17,568 of the photographed tablets. For these, the height-to-width ratio measured on the photograph agrees with the catalogue ratio (Spearman 0.77 overall). Agreement is high for most periods (Ebla 0.88, Middle Babylonian 0.85, ED IIIb 0.80, Neo-Babylonian 0.80) and absent for Neo-Assyrian (0.00) before cleaning, because many Neo-Assyrian catalogue entries give height and width the other way round or belong to fragments (S5.1) [script 01].

## S1.3 External databases

Labels from other projects were joined to CDLI tablets by museum number or primary publication, and only exact matches were kept.

- **Archibab** (Old Babylonian archives, text types, dates, cities) [@charpinAssyriologistComputerArchibab2014]. Queried in October 2026. Archibab has no bulk download, so the text table was saved page by page (31,100 of 36,060 text identifiers; about 14% of pages repeat earlier ones and some texts are missing). 2,479 photographed tablets were linked, 373 of them with an archive label [script 19]. We release only CDLI and Archibab identifiers, not Archibab content.
- **Database of Neo-Sumerian Texts (BDTNS)** [@molinaDatabaseNeoSumerianTexts]. Text types of Ur III tablets, read on 27 October 2026. Where BDTNS gives no type, the type was assigned from bookkeeping terms in the CDLI transliteration (mu-DU, i3-dab5, ba-zi, šu ba-ti, nig2-ka9), checked on a sample [scripts 37, 40, 41; SI_ur3_text_types.csv].
- **Prosobab** [@waerzeggersProsobabProsopographyBabylonia2019] for Neo-Babylonian document types, and **DigEanna** [@nabuccoDigEanna] for the Eanna archive (4,290 records, 3,107 with a measured photograph) [scripts 25, 28, 48].
- **Amarna letters.** Senders from Moran [@moranAmarnaLetters1992]; place of making, clay group and reliability from the catalogue of Goren, Finkelstein and Na'aman [@gorenInscribedClayProvenance2004], entered for all 274 letters they analysed; coordinates from Pleiades [@pleiades] or, where Pleiades has no entry, approximate [scripts 46 to 55].

# S2. Silhouettes and damage

## S2.1 From photograph to silhouette

The silhouettes are the binary masks of the released dataset. Each CDLI photograph was converted to grayscale, its colour bar removed, thresholded and closed morphologically. The masks keep all views shown in the photograph, usually obverse, reverse and four edges in the standard "fat-cross" layout, not only the largest component; the VAE therefore sees the edges, and with them the thickness of the tablet. Height-to-width ratios were measured on the silhouette.

The masks have known errors. 35% contain an enclosed hole larger than 0.1% of the tablet area and 7% one larger than 1%. Checked against the photographs, the holes are real breaks and chips, or shadows, cracks and dark patches that fall below the threshold [script 05]. Photographs carry no scale, so sizes in millimetres come only from the catalogue.

## S2.2 Damage index

Rather than keep only complete tablets, which would leave almost no Neo-Assyrian material (98% are from Kuyunjik and most are fragments), we treat preservation as a variable. For every tablet we computed outline features: extent and solidity of obverse and reverse, size of holes, and the number of large parts compared with the expected six views. A logistic regression fitted to the CDLI preservation labels (complete or nearly complete against fragment), with period as a covariate, gives a damage index between 0 and 1. It separates the two labels with AUC 0.92 [script 06]. Damage is unevenly spread: 4% of Ur III tablets fall in the most damaged third of the corpus, against 68% of Neo-Assyrian and 85% of Hittite tablets (Table S1).

Damage matters for three results. It lowers the accuracy of the released silhouette classifier from 0.85 for the least damaged third to 0.74 for the most damaged third; it weakens the agreement between photographed and catalogue ratios (Spearman 0.84 for the least, 0.69 for the most damaged tablets); and it correlates with a period's dispersion (0.62). Regressing the damage index out of the VAE codes, however, leaves the ranking of periods by uniformity practically unchanged (Spearman 0.99; Table S2) [script 06].

**Table S2.** Uniformity of each period before and after removing damage. Dispersion: mean distance of a period's tablets from its centre in the VAE space (lower = more uniform) [script 06]. Ranks agree at Spearman 0.99.

| Period | Tablets | Mean damage | Dispersion | Dispersion, damage removed | Rank | Rank, damage removed |
|---|---|---|---|---|---|---|
| Ur III | 27259 | 0.23 | 1.73 | 1.72 | 1 | 1 |
| Lagash II | 140 | 0.38 | 1.85 | 1.97 | 2 | 3 |
| Old Assyrian | 1482 | 0.41 | 1.88 | 1.88 | 3 | 2 |
| ED IIIb | 1229 | 0.59 | 1.88 | 1.97 | 4 | 4 |
| ED IIIa | 154 | 0.64 | 2.35 | 2.28 | 5 | 5 |
| Early Old Babylonian | 1428 | 0.44 | 2.44 | 2.35 | 6 | 6 |
| Hellenistic | 243 | 0.40 | 2.55 | 2.54 | 7 | 8 |
| Achaemenid | 1703 | 0.41 | 2.59 | 2.51 | 8 | 7 |
| Uruk III | 301 | 0.53 | 2.60 | 2.69 | 9 | 11 |
| Old Babylonian | 16306 | 0.50 | 2.65 | 2.57 | 10 | 9 |
| Old Akkadian | 2604 | 0.43 | 2.68 | 2.61 | 11 | 10 |
| Middle Assyrian | 1405 | 0.49 | 2.84 | 2.74 | 12 | 12 |
| Middle Babylonian | 5901 | 0.52 | 2.85 | 2.79 | 13 | 13 |
| Neo-Babylonian | 4327 | 0.47 | 2.98 | 2.92 | 14 | 14 |
| Hittite | 108 | 0.84 | 3.17 | 3.08 | 15 | 15 |
| Neo-Assyrian | 22207 | 0.72 | 3.59 | 3.56 | 16 | 16 |
| Ebla | 424 | 0.59 | 3.83 | 3.74 | 17 | 17 |

Accuracy of the released silhouette classifier by damage tercile: least damaged 0.85; middle 0.75; most damaged 0.74.


An earlier version of this analysis restricted uniformity to complete tablets and found a different ranking. That result was a selection artefact: only 2% of Neo-Assyrian tablets survive such a filter, and these are not typical of the period.

# S3. Period identification and the museum layer

## S3.1 Classifiers

Three classifiers were used, for different questions.

1. **The released ResNet50 on silhouettes** (notebooks 9 and 9.1). Fine-tuned from ImageNet weights on the masks. On its held-out test set it reaches accuracy 0.77 and macro-F1 0.61 over the fourteen classes of the original release (tablets only: 0.78 and 0.59). Over the full set of 21 period labels macro-F1 is 0.43. A decision tree on the ratio alone reaches 0.39, against 0.30 for always answering "Ur III" (Table S3). Fig. S2 shows its confusions for the twelve main periods [scripts 03, 12, 14].
2. **DINOv2 features of the silhouettes with logistic regression** for the museum test (S3.2): twelve periods from Early Dynastic IIIb to Achaemenid, at most 3,000 tablets per period, five-fold cross-validation either random or with museums held out. This classifier gives the 57% of the main text. DINOv2 [@oquabDINOv2LearningRobust2023] is trained without any period labels.
3. **Gradient-boosted trees on the damage-adjusted VAE codes**, as a check on the same split (Table S4) [script 18].

**Table S3.** Period identification on the released test split. The ratio tree uses the height-to-width ratio alone; "majority" always answers Ur III [scripts 03, 12].

| Model | Accuracy | Macro-F1, 21 labels | Macro-F1, 14 classes |
|---|---|---|---|
| tree depth 4 | 0.39 | 0.06 | 0.09 |
| tree depth 6 | 0.39 | 0.06 | 0.09 |
| tree depth 8 | 0.39 | 0.07 | 0.10 |
| tree depth 10 | 0.39 | 0.07 | 0.10 |
| tree depth None | 0.39 | 0.07 | 0.10 |
| majority (Ur III) | 0.30 | 0.02 | 0.03 |
| random, train frequencies | 0.19 | 0.04 | 0.07 |
| ResNet50 on silhouettes (released) | 0.77 | 0.43 | 0.61 |
| ResNet50 on silhouettes, tablets only | 0.78 |  | 0.59 |


![**Fig. S2.** Periods read from silhouettes (released ResNet50, test tablets). Rows sum to one; the diagonal is the share recognised. Outlined cells are confusions larger than the general pull of the assigned period on errors.](../../figures/Fig2_confusion_chrono_draft.png)

## S3.2 Museums before periods

The silhouettes reveal which museum holds a tablet. Within one period and findspot, a classifier on the VAE codes names the museum far above chance: among Ur III tablets from Umma, 74% against 20%; from Puzriš-Dagan and Girsu, 58% and 57%; among Old Babylonian tablets from Sippar, 95% against 50% (Table S5) [script 16]. The DINOv2 features give the same result (Umma 76%). Two histories lie behind this. CDLI's images were made over two decades by scanning, studio photography and museums' own photographs [@dahlLookingForwardBack2019; @chenClassificationPaleographic2024], and British Museum masks, for example, have about 20% fewer foreground pixels than others. And excavation, the antiquities market and dispersed archives sent the tablets of one period and city to a few museums [@charpinPublicationDocumentsArchives2026; @deboerDesertDesk2026]: 99% of Neo-Assyrian tablets are in the British Museum, 88% of Middle Assyrian ones in Berlin, 78% of Middle Babylonian ones in the Penn Museum and 57% of the Ebla tablets in Idlib.

**Table S5.** How well the VAE codes name the museum (or city) within one period and findspot [script 16].

| Test | Groups | Tablets per group | Balanced accuracy | Chance |
|---|---|---|---|---|
| museum within Ur III Puzriš-Dagan | 5 | 448 | 0.58 | 0.20 |
| museum within Ur III Umma | 5 | 601 | 0.74 | 0.20 |
| museum within Ur III Girsu | 5 | 222 | 0.57 | 0.20 |
| museum within Old Babylonian Sippar-Yahrurum | 2 | 64 | 0.95 | 0.50 |
| museum within Old Babylonian Nippur | 4 | 67 | 0.49 | 0.25 |
| museum within Neo-Babylonian uncertain | 5 | 153 | 0.68 | 0.20 |
| city within Old Babylonian British Museum | 3 | 64 | 0.68 | 0.33 |
| city within Old Babylonian Penn Museum | 3 | 297 | 0.70 | 0.33 |


Tested only on museums it never saw, the DINOv2 classifier falls from 57% to 30% accuracy. Ur III recognition holds (72% to 69%); Old Assyrian, Neo-Babylonian and Old Babylonian recognition hold in part; Neo-Assyrian recognition falls from 86% to almost nothing. The released ResNet assigns 30% of the British Museum's other tablets to Neo-Assyrian, against 0.9% of tablets elsewhere. The VAE check gives the same picture (51% to 25%; Table S4).

**Table S4.** Period identification from the damage-adjusted VAE codes (gradient-boosted trees, twelve periods, at most 3,000 tablets each): accuracy, macro-F1 and recall per period, with a random five-fold split and with museums held out [script 18]. The DINOv2 classifier of the main text gives 0.57 and 0.30.

| Measure | Random split | Museums held out |
|---|---|---|
| acc | 0.51 | 0.25 |
| macroF1 | 0.47 | 0.21 |
| ED IIIb | 0.64 | 0.28 |
| Ebla | 0.33 | 0.00 |
| Old Akkadian | 0.50 | 0.26 |
| Ur III | 0.72 | 0.68 |
| Early Old Babylonian | 0.08 | 0.06 |
| Old Babylonian | 0.39 | 0.29 |
| Old Assyrian | 0.53 | 0.42 |
| Middle Babylonian | 0.46 | 0.09 |
| Middle Assyrian | 0.21 | 0.02 |
| Neo-Assyrian | 0.93 | 0.01 |
| Neo-Babylonian | 0.47 | 0.40 |
| Achaemenid | 0.33 | 0.17 |


The ranking of periods by uniformity survives the museum control. Measured after removing museum means from the codes, it agrees with the damage-adjusted ranking at Spearman 0.95, and measured within each period's largest museum at 0.91 [script 17].

**Moved from the main text: two calibrations.** Achaemenid tablets from Persepolis are recognised 94% of the time, those from Babylonia only 33%, since most of the latter are assigned to Neo-Babylonian, six times more often than expected, in line with the continuity of Babylonian scribal practice under Persian rule [@waerzeggers_marduk-remanni_2014; @jursaDiplomaticsLateBabylonian2021]. In Early Old Babylonian only royal inscriptions and cones are recognised, not everyday documents, so the label marks a dynastic division [@charpinMesopotamienAltbabylonische2004] rather than a change in how ordinary tablets were made. Ebla is assigned to ED IIIb far more often than expected, in line with their shared square format (S5).

# S4. Old Babylonian labels and regional lines

## S4.1 Label signals within the Old Babylonian period

For each Archibab label (text type, archive, city, date), and each group with at least eight tablets in at least two museums, we measured the mean distance between tablets that share the label but are held in different museums, and divided it by the same quantity after permuting labels within museum (and within the other labels). A ratio below one means that shape carries the label across collections. The p-value is the share of 500 permutations with a ratio as low as the observed one. Table S6 gives the results on DINOv2 features; the VAE codes give the same order (loans 0.76 to 0.87, receipts 0.86, purchases 0.91, letters 0.94) [scripts 21, 27].

**Table S6.** Old Babylonian labels: mean distance between tablets with the same Archibab label in different museums, divided by the same after permuting labels within museum (DINOv2 features). Below 1 = shape carries the label. Archibab text types in French as in the database: prêt = loan, reçu/quittance = receipt, location/fermage = lease, achat = purchase, lettre = letter, dépense = expenditure, compte récapitulatif = summary account.

| Label | Group (Archibab) | Tablets | Museums | Ratio | p |
|---|---|---|---|---|---|
| archive | Larsa/?/Hammu-rabi/Šamaš-hazir | 62 | 3 | 0.84 | <0.002 |
| date | 1792-1750 (Hammurabi) | 214 | 7 | 0.96 | 0.006 |
| date | 1810-1793 | 96 | 3 | 0.98 | 0.298 |
| date | before 1810 | 173 | 5 | 0.98 | 0.230 |
| date | after 1750 | 552 | 9 | 0.99 | 0.102 |
| site | larsa | 135 | 5 | 0.92 | 0.002 |
| site | kish | 100 | 4 | 0.98 | 0.278 |
| site | sippar | 424 | 5 | 0.99 | 0.290 |
| site | dilbat | 41 | 3 | 1.07 | 0.872 |
| type | prêt à intérêt | 47 | 2 | 0.78 | <0.002 |
| type | quittance | 19 | 2 | 0.79 | 0.020 |
| type | prêt autre | 92 | 3 | 0.80 | <0.002 |
| type | reçu | 155 | 5 | 0.83 | <0.002 |
| type | location | 79 | 3 | 0.86 | <0.002 |
| type | liste de personnes | 72 | 3 | 0.86 | 0.004 |
| type | quantités + noms propres | 43 | 3 | 0.90 | 0.058 |
| type | achat | 116 | 6 | 0.94 | 0.030 |
| type | fermage | 24 | 2 | 0.95 | 0.306 |
| type | lettre | 396 | 8 | 0.95 | 0.002 |
| type | apport | 35 | 2 | 0.97 | 0.348 |
| type | compte récapitulatif | 69 | 4 | 0.98 | 0.352 |
| type | dépense | 189 | 7 | 1.00 | 0.532 |
| type | attribution de ration | 37 | 2 | 1.10 | 0.898 |
| type | gestion de personnel | 35 | 2 | 1.30 | 1.000 |


![**Fig. S3.** Old Babylonian shape follows the document: ratio of same-label distance across museums to the permuted distance, by Archibab label (Table S6).](../../figures/Fig3_ob_label_signal_dinov2.png)

**Moved from the main text.** Old Babylonian comprises several scribal traditions, with schools that differed from city to city [@robsonTabletHouseScribal2001; @tanretAsperaAdAstra2002; @wagensonnerLarsaSchoolsPalaeographic2019; @delneroArchivesLibrariesOld2019]. Shape follows document type most closely. Specialists recognise a loan or a sale at a glance, and even small private archives standardised their formats [@goddeerisShapeSizeArchival2023]; what is new is that this can be measured across cities and collections, and that it outweighs city and reign. Archive comes next: the tablets of Šamaš-hazir, who managed the royal domain of Larsa for Hammurabi after 1763 BCE [@fietteArchibab3Palais2018], are now in six museums, yet resemble each other more than other tablets of the same types in those museums (ratio 0.84, p < 0.002). Across museums, only Larsa (0.92) and the Hammurabi years (0.96) stand out among cities and reigns. Within one museum, tablets of the same type from the same city are more alike, so a local habit sits on top of the shared form.

The counter-example is expenditure lists and summary accounts, which show no shared form (ratios 1.00 and 0.98). Text length explains at most a seventh of the variation in shape of any type (R² 0.06 for letters, 0.07 for receipts, 0.11 for expenditure lists, 0.14 for purchases; line counts from the CDLI transliterations) [script 24]. More likely, these modern categories group records that scribes kept apart, such as single disbursements and monthly or yearly summaries, which at Nippur differ in form [@goddeerisShapeSizeArchival2023]. A millennium later the pattern recurs: Neo-Babylonian promissory notes and receipts now in different museums resemble each other more than chance (ratios 0.94 and 0.90; Prosobab labels), while the place of writing leaves no trace [script 26].

## S4.2 Document forms across periods

Within Babylonia, later letters and legal documents are as close to the Old Babylonian forms as any other tablets of their period once museum is controlled. Measured within museum on DINOv2 features, Old Assyrian letters gain nothing (+0.10 on the VAE without control, about 0 with it), and Neo-Assyrian, Neo-Babylonian and Achaemenid documents gain nothing. The only exceptions are small: Middle Babylonian letters (+0.04 to +0.05, one museum; e.g. the Kassite letters from Nippur in the Penn Museum, BE 17/1 and PBS 1/2) and Ur III legal documents with Old Babylonian loans (+0.06 to +0.11, two museums). Old Akkadian, Middle Assyrian and Hellenistic tablets could not be tested. We therefore make no claim of a genealogy of forms from period to period within Babylonia [script 22].

## S4.3 Regional lines

For each tablet of a group from the edges of the Babylonian world, we took its nearest neighbours among tablets of other periods held in other museums (DINOv2 features, cosine similarity) and compared the share from each period with the share expected from the tablets of those museums (lift); intervals are bootstrap 95% intervals over query tablets (Table S7, Fig. S4) [scripts 23, 30].

**Table S7.** Regional lines: periods over-represented among the cross-museum nearest neighbours of each group, for all tablets and within administrative documents or letters (lift with 95% interval above 1.3, at least 1% of matches; DINOv2 features). Achaemenid is split into Persepolis and Babylonia. Small groups give wide intervals.

| Group | Tablets compared | Matched period | Share of matches | Lift | 95% low | 95% high |
|---|---|---|---|---|---|---|
| Alalakh IV | all tablets | Ur III | 0.48 | 4.16 | 3.50 | 4.76 |
| Alalakh VII | all tablets | ED IIIb | 0.03 | 3.55 | 1.73 | 5.59 |
| Alalakh VII | all tablets | Ur III | 0.42 | 3.25 | 2.77 | 3.67 |
| Anšan | administrative | Achaemenid-Persepolis | 0.23 | 9.00 | 4.92 | 13.18 |
| Anšan | administrative | Neo-Babylonian | 0.19 | 4.16 | 2.28 | 6.44 |
| Anšan | all tablets | Achaemenid-Persepolis | 0.05 | 4.67 | 1.49 | 8.70 |
| Anšan | all tablets | Neo-Assyrian | 0.58 | 1.89 | 1.47 | 2.29 |
| Kanesh | all tablets | Middle Assyrian | 0.05 | 1.62 | 1.48 | 1.77 |
| Kanesh | letters | Middle Assyrian | 0.07 | 8.90 | 8.37 | 9.47 |
| Kanesh | letters | Ur III | 0.32 | 2.74 | 2.59 | 2.88 |
| Kanesh | letters | Neo-Babylonian | 0.03 | 1.89 | 1.68 | 2.11 |
| Kanesh | letters | Old Akkadian | 0.08 | 1.41 | 1.33 | 1.50 |
| Nuzi | all tablets | Middle Assyrian | 0.07 | 3.11 | 2.82 | 3.40 |
| Nuzi | all tablets | Neo-Babylonian | 0.09 | 2.49 | 2.20 | 2.80 |
| Nuzi | all tablets | Achaemenid-Babylonia | 0.03 | 2.32 | 1.97 | 2.69 |
| Nuzi | all tablets | Neo-Assyrian | 0.02 | 2.07 | 1.62 | 2.52 |
| Nuzi | all tablets | Middle Babylonian | 0.06 | 1.65 | 1.50 | 1.81 |
| Susa (OB) | all tablets | Middle Babylonian | 0.14 | 6.12 | 3.78 | 8.64 |
| Susa (OB) | all tablets | Neo-Babylonian | 0.16 | 5.70 | 3.45 | 8.18 |
| Susa (OB) | all tablets | Middle Assyrian | 0.07 | 2.86 | 1.96 | 3.92 |
| Tuttul (OB) | all tablets | Early Old Babylonian | 0.04 | 1.78 | 1.53 | 2.07 |
| Ḫattuša | all tablets | Neo-Assyrian | 0.23 | 3.70 | 2.96 | 4.56 |
| Ḫattuša | all tablets | Middle Babylonian | 0.17 | 2.02 | 1.74 | 2.30 |
| Ḫattuša | all tablets | Middle Assyrian | 0.03 | 1.96 | 1.33 | 2.69 |
| Ḫattuša | all tablets | Old Babylonian | 0.33 | 1.67 | 1.49 | 1.84 |


![**Fig. S4.** Regional lines: peripheral groups and the periods over-represented among their cross-museum nearest neighbours (Table S7).](../../figures/Fig4_periphery_dinov2.png)

**Moved from the main text.** The administrative tablets of Middle Elamite Anšan (Tall-i Malyan) find almost a quarter of their closest matches in the Persepolis Fortification archive, nine times the expected share; Malyan 59, for example, is closest to PF 102 [@stolperTextsTalliMalyan1984]. Achaemenid administration in Fārs continued Elamite practice [@henkelmanAchaemenidHeartland2012]. Old Assyrian letters from Kanesh are matched with Middle Assyrian letters from Assur nine times as often as chance predicts, though such matches remain few (7 in 100; e.g. TCL 19, 65 is closest to VS 1, 105). The Middle Babylonian tablets of Nuzi resemble Middle Assyrian ones three times as often as expected [@postgateMiddleAssyrianTablets1986], and those of Ḫattuša resemble their Babylonian and Assyrian contemporaries twice as often. Old Babylonian letters from Susa, such as MDP 18, 246, find most of their closest matches among later tablets, Kassite ones from Nippur and Neo-Babylonian ones from Borsippa and Uruk. The Amarna letters show no particular affinity. The Alalakh tablets' resemblance to Ur III (lift 3 to 4) follows the British Museum, which holds both groups, rather than history. Regional traditions such as Emar's two tablet formats [@flemingTabletTerminologyEmar2009] have too few photographs to test. An earlier result, that Old Babylonian literary tablets from Ur resemble the Nineveh library tablets, was also a British Museum artefact and is withdrawn.

# S5. Tablet proportions

## S5.1 Catalogue dimensions

Section 4 uses catalogue heights and widths, cleaned in three steps [script 38]. (i) Tablets only, with height and width given. (ii) Where a photograph exists and the tablet is clearly not square (|log photo ratio| > 0.15), a catalogue ratio close to the inverse of the photographed one (|log catalogue + log photo| < 0.1) means that height and width were entered the other way round; these were swapped. (iii) Ratios above 3 or below 1/3 that the photograph does not explain were dropped, mostly entries of the de Liagre Böhl Collection (Leiden). For Neo-Assyrian, catalogue and photograph disagree before cleaning (Spearman 0.00), so only photo-checked Neo-Assyrian tablets are used. Archival documents are administrative, legal and epistolary tablets, including contracts, receipts and accounts, that are not school texts: 60,207 tablets. Table S8 lists the changes by period and the agreement between catalogue and photograph before and after cleaning.

**Table S8.** Cleaning of catalogue dimensions by period: entries swapped and dropped, share of archival documents, and agreement (Spearman) between catalogue and photographed ratio before and after cleaning [script 38].

| Period | Tablets with dimensions | Swapped | Dropped | Archival share | Agreement before | Agreement after |
|---|---|---|---|---|---|---|
| Ur III | 21760 | 76 | 43 | 0.99 | 0.87 | 0.89 |
| Old Babylonian | 13726 | 36 | 152 | 0.85 | 0.86 | 0.91 |
| Neo-Babylonian | 6611 | 27 | 286 | 0.95 | 0.80 | 0.93 |
| Uruk III | 3896 | 6 | 20 | 0.83 | 0.94 | 0.94 |
| Ebla | 3198 | 2 | 122 | 0.99 | 0.88 | 0.88 |
| Old Akkadian | 2708 | 45 | 19 | 0.93 | 0.55 | 0.65 |
| Middle Babylonian | 2651 | 21 | 10 | 0.95 | 0.85 | 0.94 |
| Early Old Babylonian | 2066 | 5 | 1 | 0.95 | 0.75 | 0.82 |
| Neo-Assyrian | 1874 | 199 | 1050 | 0.24 | 0.00 | 0.67 |
| Uruk IV | 1779 | 0 | 4 | 0.99 | 0.83 | 0.83 |
| ED IIIb | 1616 | 1 | 8 | 0.97 | 0.80 | 0.85 |
| Achaemenid | 1538 | 24 | 48 | 0.85 | 0.71 | 0.94 |
| Proto-Elamite | 1441 | 44 | 5 | 0.92 | 0.57 | 0.63 |
| Old Assyrian | 865 | 4 | 5 | 0.79 | 0.68 | 0.77 |
| Middle Assyrian | 791 | 42 | 9 | 0.22 | 0.63 | 0.84 |
| Middle Elamite | 437 | 0 | 9 | 1.00 |  |  |
| Hellenistic | 406 | 2 | 3 | 0.85 | 0.39 | 0.47 |
| Hittite | 163 | 0 | 6 | 0.13 | 0.93 | 0.93 |
| ED IIIa | 144 | 2 | 1 | 0.88 | 0.54 | 0.77 |


An earlier finding that Neo-Babylonian tablets are the most varied of all came from Leiden entries with wrong dimensions and disappears after cleaning. All measured Middle Elamite tablets come from Haft Tepe.

## S5.2 Uniformity

Uniformity is the median absolute deviation (MAD) of the log height-to-width ratio from the period median: 0.04 means that half the tablets lie within about 4% of the typical proportion. We report bootstrap 95% intervals (300 resamples) and recompute it within museum (the size-weighted mean of within-museum MADs, for museums with at least 20 tablets) and within damage tercile [script 31]. Unlike the coefficient of variation used in earlier drafts, the MAD is not driven by a few outliers. Table S9 gives the archival documents of each period.

**Table S9.** Proportions and uniformity of archival documents by period, from cleaned catalogue dimensions [script 31]. MAD = median absolute deviation of the log ratio from the period median.

| Period | Documents | Median ratio | Share wide | Uniformity (MAD) | 95% low | 95% high | MAD within museum | MAD within damage tercile | Size vs ratio (ρ) | Width mm (10th to 90th pct) | Height mm (10th to 90th pct) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Uruk IV | 1764 | 1.28 | 0.23 | 0.162 | 0.154 | 0.180 | 0.165 |  | 0.18 | 23-54 | 24-69 |
| Uruk III | 3208 | 1.16 | 0.32 | 0.224 | 0.216 | 0.234 | 0.205 | 0.124 | 0.22 | 22-63 | 23-80 |
| Proto-Elamite | 1316 | 1.33 | 0.18 | 0.149 | 0.137 | 0.163 | 0.155 |  | 0.09 | 28-60 | 33-75 |
| ED IIIa | 126 | 1.00 | 0.44 | 0.038 | 0.031 | 0.051 | 0.033 |  | -0.05 | 32-84 | 33-85 |
| ED IIIb | 1563 | 1.01 | 0.26 | 0.065 | 0.053 | 0.074 | 0.068 | 0.050 | -0.06 | 31-80 | 35-83 |
| Ebla | 3051 | 1.02 | 0.44 | 0.186 | 0.172 | 0.202 | 0.191 | 0.132 | -0.13 | 23-87 | 28-91 |
| Old Akkadian | 2501 | 1.21 | 0.15 | 0.139 | 0.131 | 0.146 | 0.128 | 0.140 | 0.34 | 25-51 | 27-73 |
| Ur III | 21467 | 1.12 | 0.15 | 0.079 | 0.077 | 0.081 | 0.082 | 0.072 | 0.39 | 26-50 | 27-74 |
| Early Old Babylonian | 1968 | 1.26 | 0.06 | 0.117 | 0.112 | 0.123 | 0.106 | 0.115 | 0.71 | 30-48 | 33-74 |
| Old Babylonian | 11637 | 1.28 | 0.12 | 0.194 | 0.191 | 0.197 | 0.175 | 0.189 | 0.72 | 31-55 | 32-91 |
| Old Assyrian | 678 | 1.02 | 0.47 | 0.144 | 0.133 | 0.154 | 0.140 |  | 0.61 | 36-55 | 32-67 |
| Middle Assyrian | 173 | 1.02 | 0.46 | 0.212 | 0.179 | 0.237 | 0.222 |  | 0.24 | 40-82 | 35-80 |
| Middle Babylonian | 2499 | 0.95 | 0.55 | 0.230 | 0.218 | 0.244 | 0.194 | 0.176 | 0.44 | 38-81 | 33-103 |
| Middle Elamite | 428 | 0.77 | 0.74 | 0.195 | 0.161 | 0.233 | 0.195 |  | 0.08 | 25-84 | 21-70 |
| Neo-Assyrian | 190 | 1.24 | 0.44 | 0.361 | 0.295 | 0.449 | 0.353 | 0.365 | 0.19 | 32-81 | 30-93 |
| Neo-Babylonian | 6032 | 0.73 | 0.81 | 0.080 | 0.078 | 0.084 | 0.084 | 0.086 | 0.17 | 31-66 | 24-66 |
| Achaemenid | 1262 | 0.77 | 0.88 | 0.067 | 0.060 | 0.071 | 0.063 | 0.095 | 0.16 | 40-77 | 32-76 |
| Hellenistic | 344 | 0.89 | 0.76 | 0.056 | 0.050 | 0.064 | 0.042 | 0.043 | -0.08 | 69-110 | 61-102 |


![**Fig. S5.** Distribution of the height-to-width ratio of archival documents in each period, in date order (cleaned catalogue dimensions).](../../figures/Fig5_optionC_ridgeline.png)

**Moved from the main text: two formats in one period.** Old Babylonian is less uniform because it had two formats. Records of a single transaction, such as letter-orders, receipts and loans, are near square, while letters and documents about land and persons, such as purchases, leases, lawsuits and inheritance divisions, are tall (a receipt in OECT 15, 189 at 1.07 against a purchase in OECT 15, 268 at 1.58, both from Larsa in the Ashmolean Museum; Archibab types in Table S10). Model contracts used in the Nippur school taught these document types [@spadaSumerianModelContracts2018]. Neo-Babylonian uniformity has another source: promissory notes, receipts and leases from different archives and cities share one wide format (medians 0.76 to 0.84; Table S10) [@jursaDiplomaticsLateBabylonian2021; @waerzeggersProsobabProsopographyBabylonia2019]. Neo-Assyrian documents are the most varied because letters (1.34) and legal documents (1.27) are tall and administrative records (0.86) wide, as Radner showed [@radnerRelationFormat1995].

**Table S10.** Median ratio and uniformity of document types in the Old Babylonian and Neo-Babylonian periods (types with at least 15 measured tablets).

| Period | Type | Tablets | Median ratio | MAD |
|---|---|---|---|---|
| Old Babylonian (Archibab type) | texte administratif indéterminé | 34 | 1.03 | 0.153 |
| Old Babylonian (Archibab type) | mandement (letter order) | 42 | 1.06 | 0.029 |
| Old Babylonian (Archibab type) | reçu | 166 | 1.07 | 0.072 |
| Old Babylonian (Archibab type) | texte indéterminé | 33 | 1.07 | 0.173 |
| Old Babylonian (Archibab type) | liste de personnes | 93 | 1.08 | 0.105 |
| Old Babylonian (Archibab type) | dépense | 233 | 1.12 | 0.194 |
| Old Babylonian (Archibab type) | prêt autre | 129 | 1.13 | 0.102 |
| Old Babylonian (Archibab type) | gestion de personnel | 48 | 1.14 | 0.208 |
| Old Babylonian (Archibab type) | quantités + noms propres | 88 | 1.15 | 0.279 |
| Old Babylonian (Archibab type) | créance | 26 | 1.15 | 0.095 |
| Old Babylonian (Archibab type) | apport | 31 | 1.16 | 0.210 |
| Old Babylonian (Archibab type) | prêt à intérêt | 64 | 1.18 | 0.114 |
| Old Babylonian (Archibab type) | attribution de ration | 38 | 1.24 | 0.150 |
| Old Babylonian (Archibab type) | autres documents comptables | 58 | 1.27 | 0.209 |
| Old Babylonian (Archibab type) | texte juridique indéterminé | 33 | 1.29 | 0.190 |
| Old Babylonian (Archibab type) | location | 60 | 1.47 | 0.097 |
| Old Babylonian (Archibab type) | lettre | 444 | 1.51 | 0.161 |
| Old Babylonian (Archibab type) | compte récapitulatif | 82 | 1.54 | 0.178 |
| Old Babylonian (Archibab type) | fermage | 30 | 1.55 | 0.101 |
| Old Babylonian (Archibab type) | achat | 141 | 1.58 | 0.128 |
| Old Babylonian (Archibab type) | procès | 27 | 1.70 | 0.147 |
| Old Babylonian (Archibab type) | héritage | 26 | 1.80 | 0.169 |
| Neo-Babylonian (Prosobab type) | promissory note, with interest | 17 | 0.76 | 0.076 |
| Neo-Babylonian (Prosobab type) | promissory note | 91 | 0.81 | 0.077 |
| Neo-Babylonian (Prosobab type) | receipt | 131 | 0.82 | 0.048 |
| Neo-Babylonian (Prosobab type) | promissory note, with pledge and without interest | 80 | 0.83 | 0.037 |
| Neo-Babylonian (Prosobab type) | lease contract (ana sūti) | 36 | 0.83 | 0.043 |
| Neo-Babylonian (Prosobab type) | dispute-related | 16 | 0.84 | 0.087 |
| Neo-Babylonian (Prosobab type) | broken/uncertain | 18 | 0.95 | 0.406 |


**Moved from the main text: format and storage.** Veenhof observed that archivists could sort tablets by their size, shape and layout, and that the link has to be analysed per period [@veenhofCuneiformArchivesIntroduction1986]. In Ur III, single-transaction tablets were kept in labelled baskets [@nelsonPisanDubBaTexts1976] and summarised in balanced accounts [@molinaArchivesBookkeepingSouthern2016]; the small, uniform receipt and the large, tall account (Table S12) mirror these two levels of bookkeeping. In the Old Babylonian period, the tall family consists of documents kept as evidence, often sealed in envelopes and stored in jars at home [@veenhofCuneiformArchivesIntroduction1986; @vanlerbergheStorageOldBabylonian1993], whereas the square records of single transactions served for a shorter time.

## S5.3 Scribes fixing the proportions

Manuscript scholars speak of a fixed balance when a scribe keeps the proportion of a page whatever its size [@georgeGeometryEarlyQuranic2010]. We ranked the documents of each period by size (the square root of height × width) and divided them into five equal groups. Table S11 gives the correlation of size with ratio and the median ratio of the smallest and largest fifth [script 32]. Where the correlation is near zero, scribes kept a fixed balance; where it is positive, larger tablets are taller.

**Table S11.** Fixed balance: correlation of size with proportion, and the median ratio of the smallest and largest fifth of documents [script 32].

| Period | Documents | Size vs ratio (ρ) | Median ratio, smallest fifth | Median ratio, largest fifth |
|---|---|---|---|---|
| Uruk IV | 1748 | 0.17 | 1.11 | 1.34 |
| Uruk III | 3817 | 0.20 | 1.08 | 1.32 |
| Proto-Elamite | 1418 | 0.10 | 1.23 | 1.32 |
| ED IIIa | 111 | -0.07 | 1.00 | 1.00 |
| ED IIIb | 1547 | -0.06 | 1.03 | 1.00 |
| Ebla | 1476 | -0.13 | 1.13 | 1.01 |
| Old Akkadian | 2235 | 0.30 | 1.14 | 1.39 |
| Ur III | 15435 | 0.38 | 1.09 | 1.30 |
| Early Old Babylonian | 1197 | 0.75 | 1.12 | 1.55 |
| Old Babylonian | 1970 | 0.64 | 1.06 | 1.70 |
| Old Assyrian | 702 | 0.67 | 0.87 | 1.25 |
| Middle Babylonian | 126 | 0.71 | 0.92 | 1.46 |
| Neo-Assyrian | 149 | 0.07 | 0.98 | 0.94 |


![**Fig. S6.** Scribes fixing the proportions: the median tablet of each size fifth drawn to scale, smallest in front, with the median ratio of each fifth (Table S11).](../../figures/Fig6_fixed_balance.png)

In Early Dynastic Girsu the small and the large tablet are the same square (VS 14, 22 at 35 × 35 mm and VS 14, 57 at 85 × 85 mm, Vorderasiatisches Museum), and in the first millennium the wide format keeps its proportion at every size. From the Sargonic to the Old Babylonian period scribes held the width and let the height grow: Old Babylonian documents vary in width between about 31 and 55 mm but in height between 32 and 91 mm, so the largest fifth is 1.7 times taller than wide while the smallest fifth is square. In Ur III the proportion is fixed for all but the largest fifth, the large accounts and lists (1.47).

## S5.4 Literary tablets and counter-examples

Literary, lexical and school tablets follow other rules. Old Babylonian literary and school tablets, unlike the documents, keep their proportion as they grow. Not every group follows its period: Ebla, in the Early Dynastic period, is square but much more varied than Šuruppak or Girsu (MAD 0.19); the Achaemenid tablets of Persepolis follow a format of their own (S3). Ḫattuša is left out of Fig. 2 because its 157 measured tablets are mostly fragments of mixed genres and dates [@waalHittiteDiplomaticsStudies2015].

## S5.5 Ur III provinces

Text types come from BDTNS where available and otherwise from bookkeeping terms (S1.3). Table S12 gives the median ratio and size of the main types in the three provinces. The difference between Girsu and Umma, compared within the same text type, shrinks reign by reign (Table S13): from 0.156 (log ratio) in Šulgi 1 to 40 to 0.021 under Ibbi-Suen, which is no longer distinguishable from zero [script 34]. Examples: a Girsu messenger text, HLC 163 (45 × 30 mm, ISAC Chicago), against an Umma one, Nisaba 27, 228 (28 × 26 mm, Yale Babylonian Collection) [@manderMessengerTextsGirsu2008; @dagostinoUmmaMessengerTexts2008]; a Girsu loan, Nisaba 10, 91 (36 × 39 mm, British Museum), against an Umma loan, BCT 2, 80 (39 × 37 mm). Puzriš-Dagan, the crown's livestock agency founded under Šulgi [@tsouparopoulouReconstructionPuzrisDagan2013], made the smallest receipts (Nisaba 8, 299, 25 × 27 mm, British Museum).

**Table S12.** Ur III text types by province (BDTNS labels, else bookkeeping terms) [script 34].

| Type | Province | Tablets | Median ratio | Median width mm | Median height mm |
|---|---|---|---|---|---|
| balanced account | Girsu | 127 | 1.48 | 48 | 77 |
| balanced account | Puzriš-Dagan | 35 | 1.42 | 42 | 58 |
| balanced account | Umma | 116 | 1.42 | 48 | 83 |
| delivery (mu-DU) | Girsu | 37 | 1.27 | 45 | 65 |
| delivery (mu-DU) | Puzriš-Dagan | 947 | 1.17 | 33 | 38 |
| delivery (mu-DU) | Umma | 171 | 1.12 | 38 | 41 |
| expenditure (ba-zi) | Girsu | 48 | 1.13 | 38 | 42 |
| expenditure (ba-zi) | Puzriš-Dagan | 568 | 1.15 | 33 | 38 |
| labour | Girsu | 113 | 1.25 | 44 | 56 |
| labour | Puzriš-Dagan | 40 | 1.23 | 38 | 46 |
| labour | Umma | 981 | 1.08 | 42 | 45 |
| messenger text | Girsu | 158 | 1.45 | 30 | 44 |
| messenger text | Puzriš-Dagan | 36 | 1.26 | 42 | 55 |
| messenger text | Umma | 124 | 1.13 | 31 | 32 |
| offerings | Girsu | 49 | 1.27 | 38 | 47 |
| offerings | Puzriš-Dagan | 61 | 1.15 | 33 | 39 |
| offerings | Umma | 228 | 1.11 | 39 | 40 |
| other | Girsu | 1085 | 1.21 | 37 | 44 |
| other | Nippur | 54 | 1.12 | 39 | 42 |
| other | Puzriš-Dagan | 673 | 1.15 | 33 | 37 |
| other | Umma | 4017 | 1.07 | 37 | 39 |
| receipt (šu ba-ti) | Girsu | 328 | 1.12 | 33 | 37 |
| receipt (šu ba-ti) | Puzriš-Dagan | 1019 | 1.09 | 25 | 27 |
| receipt (šu ba-ti) | Umma | 655 | 1.06 | 37 | 38 |
| transfer (i-dab) | Girsu | 95 | 1.19 | 45 | 51 |
| transfer (i-dab) | Puzriš-Dagan | 1255 | 1.12 | 29 | 33 |
| transfer (i-dab) | Umma | 135 | 1.11 | 40 | 42 |


**Table S13.** Girsu against Umma by reign: difference in log ratio between the provinces, overall and within the same text type, and the VAE distance between the provinces within type [scripts 34, 49].

| Reign | Tablets (ratio) | Difference, all types | Difference within type | 95% low | 95% high | Tablets (VAE) | VAE distance within type |
|---|---|---|---|---|---|---|---|
| Šulgi 1-40 | 821 | 0.140 | 0.156 | 0.102 | 0.191 | 193 | 1.79 |
| Šulgi 41-48 | 1653 | 0.087 | 0.092 | 0.074 | 0.105 | 706 | 1.94 |
| Amar-Suen | 3063 | 0.077 | 0.067 | 0.054 | 0.090 | 1025 | 1.83 |
| Šū-Suen | 3170 | 0.058 | 0.056 | 0.036 | 0.079 | 767 | 1.16 |
| Ibbi-Suen | 590 | 0.045 | 0.021 | -0.006 | 0.075 | 176 | 0.60 |


# S6. Case studies and the VAE dimensions

## S6.1 Group assignment: what each description adds

For each case-study question, the same classifier was given four descriptions of the same tablets: the ratio; for Ur III, height and width in millimetres from the catalogue ("ruler"); twelve outline and thickness measurements computed from the six views ("outline"; S6.4); and the twelve VAE dimensions. The classifier is an L2-regularised logistic regression on standardised features, with equal numbers per group, repeated stratified five-fold cross-validation and balanced accuracy; the null comes from 200 label permutations. All comparisons are made within one museum [script 57]. Table S14 gives the results.

**Table S14.** Group assignment from four descriptions of the same tablets (ratio; ruler = catalogue height and width in mm; outline = twelve measured outline and thickness features; VAE = twelve VAE dimensions) [script 57].

| Case | Question | Tablets per group | Description | Balanced accuracy | Chance | p |
|---|---|---|---|---|---|---|
| A Ur III | province: Messenger Text, Harvard HMANE | 137 | ratio | 0.83 | 0.51 | 0.010 |
| A Ur III | province: Messenger Text, Harvard HMANE | 137 | ruler | 0.86 | 0.50 | 0.010 |
| A Ur III | province: Messenger Text, Harvard HMANE | 137 | outline | 0.93 | 0.50 | 0.010 |
| A Ur III | province: Messenger Text, Harvard HMANE | 137 | VAE | 0.93 | 0.50 | 0.010 |
| A Ur III | province: receipt (šu ba-ti), Harvard HMANE | 45 | ratio | 0.45 | 0.51 | 0.822 |
| A Ur III | province: receipt (šu ba-ti), Harvard HMANE | 45 | ruler | 0.64 | 0.51 | 0.020 |
| A Ur III | province: receipt (šu ba-ti), Harvard HMANE | 45 | outline | 0.78 | 0.50 | 0.010 |
| A Ur III | province: receipt (šu ba-ti), Harvard HMANE | 45 | VAE | 0.83 | 0.51 | 0.010 |
| A Ur III | province: receipt (šu ba-ti), ISAC Chicago | 37 | ratio | 0.71 | 0.50 | 0.010 |
| A Ur III | province: receipt (šu ba-ti), ISAC Chicago | 37 | ruler | 0.95 | 0.51 | 0.010 |
| A Ur III | province: receipt (šu ba-ti), ISAC Chicago | 37 | outline | 0.80 | 0.51 | 0.010 |
| A Ur III | province: receipt (šu ba-ti), ISAC Chicago | 37 | VAE | 0.79 | 0.51 | 0.010 |
| A Ur III | province: receipt (šu ba-ti), New York Public Library | 25 | ratio | 0.45 | 0.49 | 0.723 |
| A Ur III | province: receipt (šu ba-ti), New York Public Library | 25 | ruler | 0.64 | 0.50 | 0.099 |
| A Ur III | province: receipt (šu ba-ti), New York Public Library | 25 | outline | 0.84 | 0.49 | 0.010 |
| A Ur III | province: receipt (šu ba-ti), New York Public Library | 25 | VAE | 0.68 | 0.50 | 0.020 |
| B Amarna | great kings vs vassals (Berlin) | 13 | ratio | 0.77 | 0.52 | 0.005 |
| B Amarna | great kings vs vassals (Berlin) | 13 | outline | 0.62 | 0.51 | 0.149 |
| B Amarna | great kings vs vassals (Berlin) | 13 | VAE | 0.65 | 0.51 | 0.100 |
| B Amarna | Byblos vs other vassals (Berlin) | 38 | ratio | 0.67 | 0.50 | 0.005 |
| B Amarna | Byblos vs other vassals (Berlin) | 38 | outline | 0.76 | 0.51 | 0.005 |
| B Amarna | Byblos vs other vassals (Berlin) | 38 | VAE | 0.74 | 0.50 | 0.005 |
| B Amarna | place of making, Goren et al. (Berlin) | 6 | ratio | 0.21 | 0.13 | 0.080 |
| B Amarna | place of making, Goren et al. (Berlin) | 6 | outline | 0.22 | 0.12 | 0.085 |
| B Amarna | place of making, Goren et al. (Berlin) | 6 | VAE | 0.15 | 0.13 | 0.338 |
| C Eanna | Note: Nabopolassar-Nebuchadnezzar vs Nabonidus-Cambyses (all collections) | 52 | ratio | 0.62 | 0.49 | 0.025 |
| C Eanna | Note: Nabopolassar-Nebuchadnezzar vs Nabonidus-Cambyses (all collections) | 52 | outline | 0.66 | 0.50 | 0.010 |
| C Eanna | Note: Nabopolassar-Nebuchadnezzar vs Nabonidus-Cambyses (all collections) | 52 | VAE | 0.66 | 0.50 | 0.005 |
| C Eanna | List: Nabopolassar-Nebuchadnezzar vs Nabonidus-Cambyses (all collections) | 33 | ratio | 0.66 | 0.52 | 0.010 |
| C Eanna | List: Nabopolassar-Nebuchadnezzar vs Nabonidus-Cambyses (all collections) | 33 | outline | 0.66 | 0.50 | 0.010 |
| C Eanna | List: Nabopolassar-Nebuchadnezzar vs Nabonidus-Cambyses (all collections) | 33 | VAE | 0.70 | 0.50 | 0.005 |
| C Eanna | Debt: Nabopolassar-Nebuchadnezzar vs Nabonidus-Cambyses (all collections) | 26 | ratio | 0.68 | 0.49 | 0.010 |
| C Eanna | Debt: Nabopolassar-Nebuchadnezzar vs Nabonidus-Cambyses (all collections) | 26 | outline | 0.78 | 0.51 | 0.005 |
| C Eanna | Debt: Nabopolassar-Nebuchadnezzar vs Nabonidus-Cambyses (all collections) | 26 | VAE | 0.82 | 0.49 | 0.005 |
| C Eanna | List: Nbk to year 20 vs years 21-43 | 17 | ratio | 0.47 | 0.50 | 0.572 |
| C Eanna | List: Nbk to year 20 vs years 21-43 | 17 | outline | 0.74 | 0.50 | 0.005 |
| C Eanna | List: Nbk to year 20 vs years 21-43 | 17 | VAE | 0.56 | 0.49 | 0.318 |


**Ur III, moved from the main text.** The Harvard messenger texts are separated by the VAE as well as by the outline measures (93%), better than by the ratio (83%). For Harvard receipts the ratio fails (45%) while the outline and the VAE succeed (78%, 83%): the difference is the corners. At ISAC Chicago size in millimetres separates Puzriš-Dagan from Girsu receipts best (95%), and in the New York Public Library the ratio fails and the VAE is weak (68%). Within the same text type, the VAE distance between Girsu and Umma is stable from Šulgi to Amar-Suen (1.79 to 1.94) and falls to 1.16 under Šū-Suen and 0.60 under Ibbi-Suen (Table S13) [script 49]. Example tablets: MVN 11, 109 (Girsu, late Šulgi, 44 × 32 mm) and Nisaba 27, 12 (Umma, Šū-Suen, 31 × 29 mm).

## S6.2 The Amarna letters

Dataset S3 lists all 378 letters with CDLI number, museum, sender, city, place of making and clay group according to Goren et al. with its reliability, coordinates and measured ratio. 198 are photographed in CDLI, 176 of them in the Vorderasiatisches Museum, Berlin. The tablets of EA 289 and EA 290 are photographed as joined fragments and were not used for proportions; excluding all multi-piece photographs leaves the ranking of places unchanged (Spearman 0.95). Following Goren et al., EA 136 and EA 138 were made at Beirut [@gorenInscribedClayProvenance2004]; Mandell gives the places of EA 285 and EA 291 the other way round [@mandellCanaaniteScribalCreativity2026, 175], and we follow Goren (also Mandell p. 626 n. 47).

**Table S15.** Amarna letters by the place where their clay was formed, places with at least three measured letters [scripts 50, 51, 55].

| Place of making (Goren et al.) | Letters measured | Median ratio | Coordinates |
|---|---|---|---|
| Jerusalem | 4 | 2.02 | Pleiades 687928 |
| Mittani | 4 | 1.54 | Pleiades 641191178 |
| Babylon | 6 | 1.53 | Pleiades 893951 |
| Byblos | 36 | 1.49 | Pleiades 668216 |
| Egypt | 3 | 1.41 | Pleiades 149576487 |
| Irqata | 4 | 1.39 | approximate |
| Sumur | 6 | 1.38 | Pleiades 668372 |
| Gezer | 5 | 1.33 | Pleiades 687904 |
| Ugarit | 4 | 1.32 | CDLI location 562 |
| Ardata | 4 | 1.30 | approximate |
| Gath | 7 | 1.24 | approximate |
| Tyre | 4 | 1.24 | Pleiades 678437 |
| Beth-Shean | 5 | 1.21 | Pleiades 678378 |
| Beqa valley | 11 | 1.21 | approximate |
| Gaza | 15 | 1.19 | Pleiades 687902 |
| Yokneam | 5 | 1.17 | Pleiades 180354033 |
| Bashan | 13 | 1.14 | approximate |
| Megiddo | 3 | 1.09 | CDLI location 332 |
| Beirut | 3 | 0.90 | Pleiades 678060 |


Proportion differs between places of making (Kruskal–Wallis on the ratio, 131 Berlin letters from 17 places with at least three letters, p = 0.004) [script 51]. Table S16 compares letters sent to Egypt with letters found at home. EA 15 is not in CDLI; its ratio was measured on the open-access photograph of the Metropolitan Museum of Art (24.2.11), 1.37, close to the 1.40 of the published measurements (7.7 × 5.5 cm) [@metEA15; script 62]. EA 16 (Cairo) is not photographed.

**Table S16.** Letters sent to Egypt against letters of the same realm found at home. Aššur abroad is EA 15 measured on the Metropolitan Museum photograph.

| Letters at home | Number | Median ratio | Sent to Egypt from | Number abroad | Median ratio abroad |
|---|---|---|---|---|---|
| Babylonia (Nippur, Middle Babylonian) | 239 | 1.33 | Babylon | 6 | 1.53 |
| Nuzi (Middle Babylonian) | 16 | 1.06 | Mittani | 4 | 1.54 |
| Aššur (Middle Assyrian) | 12 | 1.10 | Assur | 1 | 1.37 |
| Alalakh (Middle Babylonian) | 3 | 0.91 | Ugarit | 4 | 1.32 |


**Moved from the main text.** Goren and colleagues found that the great kings wrote at home, most Canaanite rulers used local clay, some letters were written at the Egyptian centres of Gaza and Beth-Shean, and the kings of Amurru moved from the slopes of Mount Lebanon to Ardata, Irqata and Sumur [@gorenPetrographicInvestigationAmarna2002; @gorenInscribedClayProvenance2004]. Philologists group the letters by scribe, with one to four scribes writing for a city in a generation [@vitaCanaaniteScribesAmarna2015; @cohenCuneiformWriting2018]. For 42 of 100 letters the most similar letter in Berlin, by the VAE, comes from the same city, against 29 by chance and 30 for the ratio; without Byblos, 29 against 16 (Table S17). The pairs are telling: EA 287 is closest to EA 286, both from Jerusalem; EA 157 to EA 60, the two letters of Amurru made of Mount Lebanon clay; EA 281 to EA 283, both from Gath. EA 285, sent by Abdi-Ḫeba but made of clay from the Beth-Shean area, is closest to a letter from Gath, not to the other Jerusalem letters. Byblos letters are tall and thin: their thickness is about a quarter of their width, against a third for the other vassals. By place of making the VAE retrieval is weaker (16% against 10%, p = 0.06), because many places have only three or four letters.

**Table S17.** Amarna letters in Berlin: share whose most similar letter comes from the same city (or place of making) [script 59].

| Grouping | Groups | Letters | Description | Closest letter in the same group | Chance | p |
|---|---|---|---|---|---|---|
| city | 9 | 76 | ratio | 0.30 | 0.28 | 0.417 |
| city | 9 | 76 | outline | 0.45 | 0.29 | 0.004 |
| city | 9 | 76 | VAE | 0.42 | 0.28 | 0.009 |
| made_at | 16 | 128 | ratio | 0.11 | 0.10 | 0.466 |
| made_at | 16 | 128 | outline | 0.14 | 0.10 | 0.158 |
| made_at | 16 | 128 | VAE | 0.16 | 0.10 | 0.059 |


## S6.3 The Eanna archive

DigEanna text form, date and format were merged with the CDLI photographs (Dataset S4). The project's format labels and our measurements agree: tablets it calls landscape have a median ratio of 0.72, those it calls portrait 1.69. Table S18 gives the archive by reign and Table S19 the lists by subject before and after Nebuchadnezzar [script 53].

**Table S18.** The Eanna archive by reign: DigEanna records, tablets measured on CDLI photographs, median ratio and DigEanna format labels [script 53].

| Reign | Records | Measured | Median ratio | Landscape | Square | Portrait |
|---|---|---|---|---|---|---|
| Kandalānu | 21 | 5 | 0.63 | 0.72 | 0.00 | 0.28 |
| Nabopolassar | 254 | 198 | 0.70 | 0.91 | 0.02 | 0.07 |
| Nebuchadnezzar II | 1391 | 1107 | 0.71 | 0.91 | 0.01 | 0.07 |
| Amēl-Marduk | 39 | 27 | 0.72 | 0.89 | 0.03 | 0.05 |
| Neriglissar | 41 | 19 | 0.73 | 0.89 | 0.00 | 0.11 |
| Lābāši-Marduk | 1 | 1 | 0.74 | 0.00 | 0.00 | 0.00 |
| Nabonidus | 808 | 658 | 0.75 | 0.84 | 0.03 | 0.12 |
| Cyrus | 193 | 135 | 0.76 | 0.83 | 0.01 | 0.15 |
| Cambyses | 239 | 178 | 0.74 | 0.86 | 0.01 | 0.12 |
| Bardiya | 2 | 1 | 0.70 | 1.00 | 0.00 | 0.00 |


**Table S19.** Eanna lists by subject: number and median ratio up to the end of Nebuchadnezzar II's reign and after it.

| Subject (DigEanna domain) | Lists to Nbk | Median to Nbk | Lists after Nbk | Median after Nbk |
|---|---|---|---|---|
| Agriculture | 4 | 0.66 | 34 | 1.42 |
| Animal husbandry | 32 | 0.73 | 58 | 1.52 |
| Craft production (non-cult related) | 6 | 0.73 | 3 | 0.71 |
| Cult and pertinent craft production | 9 | 0.74 | 22 | 0.73 |
| Higher-order management and policies | 2 | 1.25 | 3 | 1.49 |
| Personnel management and labor allocation | 13 | 0.71 | 66 | 1.00 |
| Storehouse management and allocation of miscellaneous goods | 17 | 0.73 | 32 | 0.98 |
| Storehouse management and allocation of silver | 19 | 0.69 | 34 | 0.74 |
| Storehouse management and allocation of staples | 40 | 0.74 | 57 | 1.33 |


**Moved from the main text.** In Eanna, from about 584 BCE the temple was run by royal officials rather than priests, and the kings pressed Eanna to follow the procedures of Esangila, as Nabonidus did soon after his accession, ordering offerings "as in Esangila and Ezida" (YOS 6, 10) [@kleberTempelUnd2008; @jursaOustingNurSins2018; @jursaUrukeanPriestsNeoBabylonian2019]. Diplomatic studies of the archive have linked format to function [@kleberTabletFormatBookkeeping2021; @levaviDiplomaticsNeoBabylonian2021]; Quillien found a change of format and layout in the textile accounts of the Ebabbar of Sippar in the same years as Pirngruber's Eanna inventories [@quillienDiachronicChangeTablet2021; @pirngruberDiplomaticsApproachEanna2021]. The administrative notes, the commonest form of the archive, are identified as "Note" by their operative phrases, chiefly *ina pāni* "at the disposal of" (396 of 1,620), *maḫir* "received" (359) and *našû* "has taken" (328); the *taḫsistu* memorandum is a different form. The notes became less wide in each large collection (Goucher College 0.70 to 0.74, Yale 0.70 to 0.75, Newell 0.70 to 0.74, Nies 0.69 to 0.73; 819 notes before the 560s, 348 after). A typical pair from one collection is GCCI 2, 4 (Nabopolassar year 12, 26 × 38 mm) and GCCI 1, 280 (Nabonidus year 10, 33 × 44 mm). Within small collections the VAE adds nothing to the ratio (Table S20).

**Table S20.** Eanna, before against after the 560s, within small collections: the VAE adds nothing to the ratio [script 58].

| Text form | Collections (before + after) | Tablets | Description | Balanced accuracy | Chance | p |
|---|---|---|---|---|---|---|
| Note | Claremont School of Theology 7+7; Hearst Museum of Anthropology 8+8; Spurlock Museum 11+11 | 52 | ratio | 0.65 | 0.50 | 0.035 |
| Note | Claremont School of Theology 7+7; Hearst Museum of Anthropology 8+8; Spurlock Museum 11+11 | 52 | outline | 0.61 | 0.48 | 0.080 |
| Note | Claremont School of Theology 7+7; Hearst Museum of Anthropology 8+8; Spurlock Museum 11+11 | 52 | VAE | 0.62 | 0.50 | 0.100 |
| List | Free Library of Philadelphia 4+4; Hearst Museum of Anthropology 6+6; Vorderasiatisches Museum 5+5 | 30 | ratio | 0.76 | 0.53 | 0.010 |
| List | Free Library of Philadelphia 4+4; Hearst Museum of Anthropology 6+6; Vorderasiatisches Museum 5+5 | 30 | outline | 0.71 | 0.49 | 0.010 |
| List | Free Library of Philadelphia 4+4; Hearst Museum of Anthropology 6+6; Vorderasiatisches Museum 5+5 | 30 | VAE | 0.69 | 0.45 | 0.015 |


## S6.4 The VAE and what its dimensions measure

**Architecture and training.** The VAE [@kingmaVAE2013] takes a 512 × 512 binary mask. The encoder has five convolutional layers (32, 64, 128, 256 and 256 channels, kernel 5, stride 2) and two linear heads for the mean and log-variance of a twelve-dimensional latent space; the decoder mirrors it with transposed convolutions. A linear classification head on the latent vector adds a period loss with class weights that equalise the periods. Training used 94,936 masks, batch size 8, Adam with learning rate 0.0001, β = 1 and 30 epochs; the released checkpoint is from epoch 22 (step 213,621). Because the period loss uses labels, every uniformity and neighbour result was repeated on DINOv2 features, which use none; the two rankings of periods agree (Spearman 0.83).

**What the dimensions measure.** For 76,049 tablets whose silhouette has six clean views, we measured twelve features directly on the views: the ratio of the obverse, how rectangular it is, the regularity of the outline (solidity), roundness, the squareness of the corners on obverse and reverse, taper, the bulge of the long and short sides, the size of the reverse against the obverse, and thickness at the sides and at the ends against the width [script 56]. Table S21 names, for each VAE dimension, the closest of these measurements (Spearman ρ). Ridge regression with five-fold cross-validation then shows how well the twelve VAE numbers recover each measurement (Table S22), on the 47,714 well-preserved tablets (obverse solidity > 0.97 and reverse within 0.8 to 1.25 of the obverse) and on all measured tablets [script 64]. Features with R² ≥ 0.65 are recovered reliably, those with R² ≥ 0.4 in part, enough to compare groups but not single tablets. Fig. S7 shows real tablets at the low, middle and high end of the three clearest dimensions.

**Table S21.** What each VAE dimension measures: the closest directly measured feature [script 64].

| Dimension | Closest measurement | Spearman ρ | Reading | Strength |
|---|---|---|---|---|
| X1 | proportion (height ÷ width of the obverse) | 0.27 | higher = taller | weak |
| X2 | proportion (height ÷ width of the obverse) | -0.79 | higher = wider | clear |
| X3 | thickness at the sides ÷ width | -0.64 | higher = thinner at the sides | clear |
| X4 | squareness of the corners (obverse) | -0.36 | higher = rounder corners | weak |
| X5 | roundness of the outline | 0.32 | higher = rounder | weak |
| X6 | how rectangular the obverse is | 0.35 | higher = more rectangular | weak |
| X7 | proportion (height ÷ width of the obverse) | 0.40 | higher = taller | weak |
| X8 | thickness at top and bottom ÷ width | -0.28 | higher = thinner at the ends | weak |
| X9 | thickness at top and bottom ÷ width | 0.41 | higher = thicker at the ends | partial |
| X10 | proportion (height ÷ width of the obverse) | 0.50 | higher = taller | partial |
| X11 | how rectangular the obverse is | -0.49 | higher = less rectangular, more rounded | partial |
| X12 | how rectangular the obverse is | 0.69 | higher = more rectangular | clear |


**Table S22.** How well the twelve VAE numbers recover each measured feature (ridge regression, five-fold cross-validated R²) [script 64].

| Feature | R², well preserved | R², all measured | Tablets, well preserved | Tablets, all | Recovered |
|---|---|---|---|---|---|
| proportion (height ÷ width of the obverse) | 0.82 | 0.72 | 47714 | 76049 | reliable |
| thickness at the sides ÷ width | 0.71 | 0.61 | 47096 | 74265 | reliable |
| thickness at top and bottom ÷ width | 0.70 | 0.59 | 46297 | 73131 | reliable |
| how rectangular the obverse is | 0.51 | 0.54 | 47714 | 76049 | partial |
| squareness of the corners (obverse) | 0.46 | 0.45 | 47714 | 76049 | partial |
| squareness of the corners (reverse) | 0.44 | 0.44 | 47714 | 76049 | partial |
| bulge of the long sides | 0.39 | 0.33 | 47714 | 76049 | not recovered |
| bulge of the short sides | 0.37 | 0.30 | 47714 | 76049 | not recovered |
| roundness of the outline | 0.22 | 0.14 | 47714 | 76049 | not recovered |
| taper (top width ÷ bottom width) | 0.16 | 0.15 | 47714 | 76049 | not recovered |
| regularity of the outline (no notches or breaks) | 0.10 | 0.14 | 47714 | 76049 | not recovered |
| reverse larger than obverse | 0.03 | 0.05 | 47714 | 76049 | not recovered |


![**Fig. S7.** What the clearest VAE dimensions measure: real tablets at the 10th, 50th and 90th percentile of each dimension, typical on the others, with the closest measurement (Tables S21, S22).](../../figures/fig_vae_dimension_guide.png)

The CDLI catalogue records thickness for 15% of the 92,876 tablets in the dataset and the shape of the corners for none. The notebook *14. Measure tablet features from VAE vectors* and a one-page guide, released with the article, return the measured and predicted features for any tablet and compare groups of tablets, with the reliability of each feature (Dataset S1).

# S7. Code, data and datasets

**Data.** Silhouettes, ratios, VAE codes and the trained VAE: Zenodo 10.5281/zenodo.11668220 and 10.5281/zenodo.12787746. CDLI catalogue: cdli.earth, checked October 2026.

**Code.** github.com/DigitalPasts/ShapingHistory. The numbered notebooks (0 to 14) reproduce the original pipeline, models and the measurement notebook; the scripts in `repro/scripts` (01 to 64) reproduce every number in the article and this SI, each writing a CSV to `repro/results`.

**Datasets.**

- **Dataset S1** (vae_measured_and_predicted.csv). For each of the 92,876 tablets: CDLI number, period, the twelve VAE dimensions, the measured outline features where the views are clean, and the features predicted from the VAE with their reliability.
- **Dataset S2** (tablet_dims_clean.csv). Cleaned catalogue dimensions for 66,711 tablets, with flags for swapped and dropped entries and for archival documents.
- **Dataset S3** (SI_amarna_letters.csv). The Amarna letters with sender, place of making, clay group and reliability (Goren et al. 2004), coordinates and measured ratio.
- **Dataset S4** (digeanna_merged.csv). DigEanna records merged with CDLI photographs and measured ratios.

# References
