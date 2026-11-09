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

{{TABLE_S1}}

**Moved from the main text: genres and findspots.** CDLI assigns genres along the conventional Assyriological division between archival documents (administrative, legal, letters) and the literary and scholarly texts of the "stream of tradition" [@oppenheimAncientMesopotamia1977; @pedersenArchivesLibraries1998]. Administrative documents make up 48% of all tablets and more than 85% of every period before 2000 BCE, while a quarter of the tablets, among them 65% of the Neo-Assyrian ones, have no genre assigned. The shape of the corpus is also the shape of what survived and of how it was found: ancient preservation and destruction, chance discoveries, excavation priorities and the antiquities market filled museums with tablets from a few sites [@rattenborgArchaeologicalDistributionCuneiform2023; @michelIdentifyingMissingEvidence2025]. 99% of Old Assyrian tablets come from Kanesh, where the merchants' archives were preserved in their houses in the lower town, while the contemporary archives of Assur remain largely unexcavated [@larsenAncientKanesh2015]. 96% of Neo-Assyrian tablets come from Nineveh, 83% of Hittite tablets from Ḫattuša and 77% of Middle Assyrian tablets from Assur. Another 15% of all tablets have no recorded findspot; for many, it can be reconstructed from publications, museum records or internal evidence such as month names and prosopography [@brumfieldKeyCity2019], but this is an extra step between catalogue and inference. Middle Babylonian tablets come 78% from Nippur, so what we measure as Middle Babylonian practice is largely the practice of Nippur's administration, which may not represent the norm of the Kassite state.

{{FIG_S1}}

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

{{TABLE_S2}}

An earlier version of this analysis restricted uniformity to complete tablets and found a different ranking. That result was a selection artefact: only 2% of Neo-Assyrian tablets survive such a filter, and these are not typical of the period.

# S3. Period identification and the museum layer

## S3.1 Classifiers

Three classifiers were used, for different questions.

1. **The released ResNet50 on silhouettes** (notebooks 9 and 9.1). Fine-tuned from ImageNet weights on the masks. On its held-out test set it reaches accuracy 0.77 and macro-F1 0.61 over the fourteen classes of the original release (tablets only: 0.78 and 0.59). Over the full set of 21 period labels macro-F1 is 0.43. A decision tree on the ratio alone reaches 0.39, against 0.30 for always answering "Ur III" (Table S3). Fig. S2 shows its confusions for the twelve main periods [scripts 03, 12, 14].
2. **DINOv2 features of the silhouettes with logistic regression** for the museum test (S3.2): twelve periods from Early Dynastic IIIb to Achaemenid, at most 3,000 tablets per period, five-fold cross-validation either random or with museums held out. This classifier gives the 57% of the main text. DINOv2 [@oquabDINOv2LearningRobust2023] is trained without any period labels.
3. **Gradient-boosted trees on the damage-adjusted VAE codes**, as a check on the same split (Table S4) [script 18].

{{TABLE_S3}}

{{FIG_S2}}

## S3.2 Museums before periods

The silhouettes reveal which museum holds a tablet. Within one period and findspot, a classifier on the VAE codes names the museum far above chance: among Ur III tablets from Umma, 74% against 20%; from Puzriš-Dagan and Girsu, 58% and 57%; among Old Babylonian tablets from Sippar, 95% against 50% (Table S5) [script 16]. The DINOv2 features give the same result (Umma 76%). Two histories lie behind this. CDLI's images were made over two decades by scanning, studio photography and museums' own photographs [@dahlLookingForwardBack2019; @chenClassificationPaleographic2024], and British Museum masks, for example, have about 20% fewer foreground pixels than others. And excavation, the antiquities market and dispersed archives sent the tablets of one period and city to a few museums [@charpinPublicationDocumentsArchives2026; @deboerDesertDesk2026]: 99% of Neo-Assyrian tablets are in the British Museum, 88% of Middle Assyrian ones in Berlin, 78% of Middle Babylonian ones in the Penn Museum and 57% of the Ebla tablets in Idlib.

{{TABLE_S5}}

Tested only on museums it never saw, the DINOv2 classifier falls from 57% to 30% accuracy. Ur III recognition holds (72% to 69%); Old Assyrian, Neo-Babylonian and Old Babylonian recognition hold in part; Neo-Assyrian recognition falls from 86% to almost nothing. The released ResNet assigns 30% of the British Museum's other tablets to Neo-Assyrian, against 0.9% of tablets elsewhere. The VAE check gives the same picture (51% to 25%; Table S4).

{{TABLE_S4}}

The ranking of periods by uniformity survives the museum control. Measured after removing museum means from the codes, it agrees with the damage-adjusted ranking at Spearman 0.95, and measured within each period's largest museum at 0.91 [script 17].

**Moved from the main text: two calibrations.** Achaemenid tablets from Persepolis are recognised 94% of the time, those from Babylonia only 33%, since most of the latter are assigned to Neo-Babylonian, six times more often than expected, in line with the continuity of Babylonian scribal practice under Persian rule [@waerzeggers_marduk-remanni_2014; @jursaDiplomaticsLateBabylonian2021]. In Early Old Babylonian only royal inscriptions and cones are recognised, not everyday documents, so the label marks a dynastic division [@charpinMesopotamienAltbabylonische2004] rather than a change in how ordinary tablets were made. Ebla is assigned to ED IIIb far more often than expected, in line with their shared square format (S5).

# S4. Old Babylonian labels and regional lines

## S4.1 Label signals within the Old Babylonian period

For each Archibab label (text type, archive, city, date), and each group with at least eight tablets in at least two museums, we measured the mean distance between tablets that share the label but are held in different museums, and divided it by the same quantity after permuting labels within museum (and within the other labels). A ratio below one means that shape carries the label across collections. The p-value is the share of 500 permutations with a ratio as low as the observed one. Table S6 gives the results on DINOv2 features; the VAE codes give the same order (loans 0.76 to 0.87, receipts 0.86, purchases 0.91, letters 0.94) [scripts 21, 27].

{{TABLE_S6}}

{{FIG_S3}}

**Moved from the main text.** Old Babylonian comprises several scribal traditions, with schools that differed from city to city [@robsonTabletHouseScribal2001; @tanretAsperaAdAstra2002; @wagensonnerLarsaSchoolsPalaeographic2019; @delneroArchivesLibrariesOld2019]. Shape follows document type most closely. Specialists recognise a loan or a sale at a glance, and even small private archives standardised their formats [@goddeerisShapeSizeArchival2023]; what is new is that this can be measured across cities and collections, and that it outweighs city and reign. Archive comes next: the tablets of Šamaš-hazir, who managed the royal domain of Larsa for Hammurabi after 1763 BCE [@fietteArchibab3Palais2018], are now in six museums, yet resemble each other more than other tablets of the same types in those museums (ratio 0.84, p < 0.002). Across museums, only Larsa (0.92) and the Hammurabi years (0.96) stand out among cities and reigns. Within one museum, tablets of the same type from the same city are more alike, so a local habit sits on top of the shared form.

The counter-example is expenditure lists and summary accounts, which show no shared form (ratios 1.00 and 0.98). Text length explains at most a seventh of the variation in shape of any type (R² 0.06 for letters, 0.07 for receipts, 0.11 for expenditure lists, 0.14 for purchases; line counts from the CDLI transliterations) [script 24]. More likely, these modern categories group records that scribes kept apart, such as single disbursements and monthly or yearly summaries, which at Nippur differ in form [@goddeerisShapeSizeArchival2023]. A millennium later the pattern recurs: Neo-Babylonian promissory notes and receipts now in different museums resemble each other more than chance (ratios 0.94 and 0.90; Prosobab labels), while the place of writing leaves no trace [script 26].

## S4.2 Document forms across periods

Within Babylonia, later letters and legal documents are as close to the Old Babylonian forms as any other tablets of their period once museum is controlled. Measured within museum on DINOv2 features, Old Assyrian letters gain nothing (+0.10 on the VAE without control, about 0 with it), and Neo-Assyrian, Neo-Babylonian and Achaemenid documents gain nothing. The only exceptions are small: Middle Babylonian letters (+0.04 to +0.05, one museum; e.g. the Kassite letters from Nippur in the Penn Museum, BE 17/1 and PBS 1/2) and Ur III legal documents with Old Babylonian loans (+0.06 to +0.11, two museums). Old Akkadian, Middle Assyrian and Hellenistic tablets could not be tested. We therefore make no claim of a genealogy of forms from period to period within Babylonia [script 22].

## S4.3 Regional lines

For each tablet of a group from the edges of the Babylonian world, we took its nearest neighbours among tablets of other periods held in other museums (DINOv2 features, cosine similarity) and compared the share from each period with the share expected from the tablets of those museums (lift); intervals are bootstrap 95% intervals over query tablets (Table S7, Fig. S4) [scripts 23, 30].

{{TABLE_S7}}

{{FIG_S4}}

**Moved from the main text.** The administrative tablets of Middle Elamite Anšan (Tall-i Malyan) find almost a quarter of their closest matches in the Persepolis Fortification archive, nine times the expected share; Malyan 59, for example, is closest to PF 102 [@stolperTextsTalliMalyan1984]. Achaemenid administration in Fārs continued Elamite practice [@henkelmanAchaemenidHeartland2012]. Old Assyrian letters from Kanesh are matched with Middle Assyrian letters from Assur nine times as often as chance predicts, though such matches remain few (7 in 100; e.g. TCL 19, 65 is closest to VS 1, 105). The Middle Babylonian tablets of Nuzi resemble Middle Assyrian ones three times as often as expected [@postgateMiddleAssyrianTablets1986], and those of Ḫattuša resemble their Babylonian and Assyrian contemporaries twice as often. Old Babylonian letters from Susa, such as MDP 18, 246, find most of their closest matches among later tablets, Kassite ones from Nippur and Neo-Babylonian ones from Borsippa and Uruk. The Amarna letters show no particular affinity. The Alalakh tablets' resemblance to Ur III (lift 3 to 4) follows the British Museum, which holds both groups, rather than history. Regional traditions such as Emar's two tablet formats [@flemingTabletTerminologyEmar2009] have too few photographs to test. An earlier result, that Old Babylonian literary tablets from Ur resemble the Nineveh library tablets, was also a British Museum artefact and is withdrawn.

# S5. Tablet proportions

## S5.1 Catalogue dimensions

Section 4 uses catalogue heights and widths, cleaned in three steps [script 38]. (i) Tablets only, with height and width given. (ii) Where a photograph exists and the tablet is clearly not square (|log photo ratio| > 0.15), a catalogue ratio close to the inverse of the photographed one (|log catalogue + log photo| < 0.1) means that height and width were entered the other way round; these were swapped. (iii) Ratios above 3 or below 1/3 that the photograph does not explain were dropped, mostly entries of the de Liagre Böhl Collection (Leiden). For Neo-Assyrian, catalogue and photograph disagree before cleaning (Spearman 0.00), so only photo-checked Neo-Assyrian tablets are used. Archival documents are administrative, legal and epistolary tablets, including contracts, receipts and accounts, that are not school texts: 60,207 tablets. Table S8 lists the changes by period and the agreement between catalogue and photograph before and after cleaning.

{{TABLE_S8}}

An earlier finding that Neo-Babylonian tablets are the most varied of all came from Leiden entries with wrong dimensions and disappears after cleaning. All measured Middle Elamite tablets come from Haft Tepe.

## S5.2 Uniformity

Uniformity is the median absolute deviation (MAD) of the log height-to-width ratio from the period median: 0.04 means that half the tablets lie within about 4% of the typical proportion. We report bootstrap 95% intervals (300 resamples) and recompute it within museum (the size-weighted mean of within-museum MADs, for museums with at least 20 tablets) and within damage tercile [script 31]. Unlike the coefficient of variation used in earlier drafts, the MAD is not driven by a few outliers. Table S9 gives the archival documents of each period.

{{TABLE_S9}}

{{FIG_S5}}

**Moved from the main text: two formats in one period.** Old Babylonian is less uniform because it had two formats. Records of a single transaction, such as letter-orders, receipts and loans, are near square, while letters and documents about land and persons, such as purchases, leases, lawsuits and inheritance divisions, are tall (a receipt in OECT 15, 189 at 1.07 against a purchase in OECT 15, 268 at 1.58, both from Larsa in the Ashmolean Museum; Archibab types in Table S10). Model contracts used in the Nippur school taught these document types [@spadaSumerianModelContracts2018]. Neo-Babylonian uniformity has another source: promissory notes, receipts and leases from different archives and cities share one wide format (medians 0.76 to 0.84; Table S10) [@jursaDiplomaticsLateBabylonian2021; @waerzeggersProsobabProsopographyBabylonia2019]. Neo-Assyrian documents are the most varied because letters (1.34) and legal documents (1.27) are tall and administrative records (0.86) wide, as Radner showed [@radnerRelationFormat1995].

{{TABLE_S10}}

**Moved from the main text: format and storage.** Veenhof observed that archivists could sort tablets by their size, shape and layout, and that the link has to be analysed per period [@veenhofCuneiformArchivesIntroduction1986]. In Ur III, single-transaction tablets were kept in labelled baskets [@nelsonPisanDubBaTexts1976] and summarised in balanced accounts [@molinaArchivesBookkeepingSouthern2016]; the small, uniform receipt and the large, tall account (Table S12) mirror these two levels of bookkeeping. In the Old Babylonian period, the tall family consists of documents kept as evidence, often sealed in envelopes and stored in jars at home [@veenhofCuneiformArchivesIntroduction1986; @vanlerbergheStorageOldBabylonian1993], whereas the square records of single transactions served for a shorter time.

## S5.3 Scribes fixing the proportions

Manuscript scholars speak of a fixed balance when a scribe keeps the proportion of a page whatever its size [@georgeGeometryEarlyQuranic2010]. We ranked the documents of each period by size (the square root of height × width) and divided them into five equal groups. Table S11 gives the correlation of size with ratio and the median ratio of the smallest and largest fifth [script 32]. Where the correlation is near zero, scribes kept a fixed balance; where it is positive, larger tablets are taller.

{{TABLE_S11}}

{{FIG_S6}}

In Early Dynastic Girsu the small and the large tablet are the same square (VS 14, 22 at 35 × 35 mm and VS 14, 57 at 85 × 85 mm, Vorderasiatisches Museum), and in the first millennium the wide format keeps its proportion at every size. From the Sargonic to the Old Babylonian period scribes held the width and let the height grow: Old Babylonian documents vary in width between about 31 and 55 mm but in height between 32 and 91 mm, so the largest fifth is 1.7 times taller than wide while the smallest fifth is square. In Ur III the proportion is fixed for all but the largest fifth, the large accounts and lists (1.47).

## S5.4 Literary tablets and counter-examples

Literary, lexical and school tablets follow other rules. Old Babylonian literary and school tablets, unlike the documents, keep their proportion as they grow. Not every group follows its period: Ebla, in the Early Dynastic period, is square but much more varied than Šuruppak or Girsu (MAD 0.19); the Achaemenid tablets of Persepolis follow a format of their own (S3). Ḫattuša is left out of Fig. 2 because its 157 measured tablets are mostly fragments of mixed genres and dates [@waalHittiteDiplomaticsStudies2015].

## S5.5 Ur III provinces

Text types come from BDTNS where available and otherwise from bookkeeping terms (S1.3). Table S12 gives the median ratio and size of the main types in the three provinces. The difference between Girsu and Umma, compared within the same text type, shrinks reign by reign (Table S13): from 0.156 (log ratio) in Šulgi 1 to 40 to 0.021 under Ibbi-Suen, which is no longer distinguishable from zero [script 34]. Examples: a Girsu messenger text, HLC 163 (45 × 30 mm, ISAC Chicago), against an Umma one, Nisaba 27, 228 (28 × 26 mm, Yale Babylonian Collection) [@manderMessengerTextsGirsu2008; @dagostinoUmmaMessengerTexts2008]; a Girsu loan, Nisaba 10, 91 (36 × 39 mm, British Museum), against an Umma loan, BCT 2, 80 (39 × 37 mm). Puzriš-Dagan, the crown's livestock agency founded under Šulgi [@tsouparopoulouReconstructionPuzrisDagan2013], made the smallest receipts (Nisaba 8, 299, 25 × 27 mm, British Museum).

{{TABLE_S12}}

{{TABLE_S13}}

# S6. Case studies and the VAE dimensions

## S6.1 Group assignment: what each description adds

For each case-study question, the same classifier was given four descriptions of the same tablets: the ratio; for Ur III, height and width in millimetres from the catalogue ("ruler"); twelve outline and thickness measurements computed from the six views ("outline"; S6.4); and the twelve VAE dimensions. The classifier is an L2-regularised logistic regression on standardised features, with equal numbers per group, repeated stratified five-fold cross-validation and balanced accuracy; the null comes from 200 label permutations. All comparisons are made within one museum [script 57]. Table S14 gives the results.

{{TABLE_S14}}

**Ur III, moved from the main text.** The Harvard messenger texts are separated by the VAE as well as by the outline measures (93%), better than by the ratio (83%). For Harvard receipts the ratio fails (45%) while the outline and the VAE succeed (78%, 83%): the difference is the corners. At ISAC Chicago size in millimetres separates Puzriš-Dagan from Girsu receipts best (95%), and in the New York Public Library the ratio fails and the VAE is weak (68%). Within the same text type, the VAE distance between Girsu and Umma is stable from Šulgi to Amar-Suen (1.79 to 1.94) and falls to 1.16 under Šū-Suen and 0.60 under Ibbi-Suen (Table S13) [script 49]. Example tablets: MVN 11, 109 (Girsu, late Šulgi, 44 × 32 mm) and Nisaba 27, 12 (Umma, Šū-Suen, 31 × 29 mm).

## S6.2 The Amarna letters

Dataset S3 lists all 378 letters with CDLI number, museum, sender, city, place of making and clay group according to Goren et al. with its reliability, coordinates and measured ratio. 198 are photographed in CDLI, 176 of them in the Vorderasiatisches Museum, Berlin. The tablets of EA 289 and EA 290 are photographed as joined fragments and were not used for proportions; excluding all multi-piece photographs leaves the ranking of places unchanged (Spearman 0.95). Following Goren et al., EA 136 and EA 138 were made at Beirut [@gorenInscribedClayProvenance2004]; Mandell gives the places of EA 285 and EA 291 the other way round [@mandellCanaaniteScribalCreativity2026, 175], and we follow Goren (also Mandell p. 626 n. 47).

{{TABLE_S15}}

Proportion differs between places of making (Kruskal–Wallis on the ratio, 131 Berlin letters from 17 places with at least three letters, p = 0.004) [script 51]. Table S16 compares letters sent to Egypt with letters found at home. EA 15 is not in CDLI; its ratio was measured on the open-access photograph of the Metropolitan Museum of Art (24.2.11), 1.37, close to the 1.40 of the published measurements (7.7 × 5.5 cm) [@metEA15; script 62]. EA 16 (Cairo) is not photographed.

{{TABLE_S16}}

**Moved from the main text.** Goren and colleagues found that the great kings wrote at home, most Canaanite rulers used local clay, some letters were written at the Egyptian centres of Gaza and Beth-Shean, and the kings of Amurru moved from the slopes of Mount Lebanon to Ardata, Irqata and Sumur [@gorenPetrographicInvestigationAmarna2002; @gorenInscribedClayProvenance2004]. Philologists group the letters by scribe, with one to four scribes writing for a city in a generation [@vitaCanaaniteScribesAmarna2015; @cohenCuneiformWriting2018]. For 42 of 100 letters the most similar letter in Berlin, by the VAE, comes from the same city, against 29 by chance and 30 for the ratio; without Byblos, 29 against 16 (Table S17). The pairs are telling: EA 287 is closest to EA 286, both from Jerusalem; EA 157 to EA 60, the two letters of Amurru made of Mount Lebanon clay; EA 281 to EA 283, both from Gath. EA 285, sent by Abdi-Ḫeba but made of clay from the Beth-Shean area, is closest to a letter from Gath, not to the other Jerusalem letters. Byblos letters are tall and thin: their thickness is about a quarter of their width, against a third for the other vassals. By place of making the VAE retrieval is weaker (16% against 10%, p = 0.06), because many places have only three or four letters.

{{TABLE_S17}}

## S6.3 The Eanna archive

DigEanna text form, date and format were merged with the CDLI photographs (Dataset S4). The project's format labels and our measurements agree: tablets it calls landscape have a median ratio of 0.72, those it calls portrait 1.69. Table S18 gives the archive by reign and Table S19 the lists by subject before and after Nebuchadnezzar [script 53].

{{TABLE_S18}}

{{TABLE_S19}}

**Moved from the main text.** In Eanna, from about 584 BCE the temple was run by royal officials rather than priests, and the kings pressed Eanna to follow the procedures of Esangila, as Nabonidus did soon after his accession, ordering offerings "as in Esangila and Ezida" (YOS 6, 10) [@kleberTempelUnd2008; @jursaOustingNurSins2018; @jursaUrukeanPriestsNeoBabylonian2019]. Diplomatic studies of the archive have linked format to function [@kleberTabletFormatBookkeeping2021; @levaviDiplomaticsNeoBabylonian2021]; Quillien found a change of format and layout in the textile accounts of the Ebabbar of Sippar in the same years as Pirngruber's Eanna inventories [@quillienDiachronicChangeTablet2021; @pirngruberDiplomaticsApproachEanna2021]. The administrative notes, the commonest form of the archive, are identified as "Note" by their operative phrases, chiefly *ina pāni* "at the disposal of" (396 of 1,620), *maḫir* "received" (359) and *našû* "has taken" (328); the *taḫsistu* memorandum is a different form. The notes became less wide in each large collection (Goucher College 0.70 to 0.74, Yale 0.70 to 0.75, Newell 0.70 to 0.74, Nies 0.69 to 0.73; 819 notes before the 560s, 348 after). A typical pair from one collection is GCCI 2, 4 (Nabopolassar year 12, 26 × 38 mm) and GCCI 1, 280 (Nabonidus year 10, 33 × 44 mm). Within small collections the VAE adds nothing to the ratio (Table S20).

{{TABLE_S20}}

## S6.4 The VAE and what its dimensions measure

**Architecture and training.** The VAE [@kingmaVAE2013] takes a 512 × 512 binary mask. The encoder has five convolutional layers (32, 64, 128, 256 and 256 channels, kernel 5, stride 2) and two linear heads for the mean and log-variance of a twelve-dimensional latent space; the decoder mirrors it with transposed convolutions. A linear classification head on the latent vector adds a period loss with class weights that equalise the periods. Training used 94,936 masks, batch size 8, Adam with learning rate 0.0001, β = 1 and 30 epochs; the released checkpoint is from epoch 22 (step 213,621). Because the period loss uses labels, every uniformity and neighbour result was repeated on DINOv2 features, which use none; the two rankings of periods agree (Spearman 0.83).

**What the dimensions measure.** For 76,049 tablets whose silhouette has six clean views, we measured twelve features directly on the views: the ratio of the obverse, how rectangular it is, the regularity of the outline (solidity), roundness, the squareness of the corners on obverse and reverse, taper, the bulge of the long and short sides, the size of the reverse against the obverse, and thickness at the sides and at the ends against the width [script 56]. Table S21 names, for each VAE dimension, the closest of these measurements (Spearman ρ). Ridge regression with five-fold cross-validation then shows how well the twelve VAE numbers recover each measurement (Table S22), on the 47,714 well-preserved tablets (obverse solidity > 0.97 and reverse within 0.8 to 1.25 of the obverse) and on all measured tablets [script 64]. Features with R² ≥ 0.65 are recovered reliably, those with R² ≥ 0.4 in part, enough to compare groups but not single tablets. Fig. S7 shows real tablets at the low, middle and high end of the three clearest dimensions.

{{TABLE_S21}}

{{TABLE_S22}}

{{FIG_S7}}

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
