
# S7. Dates from the specialist databases

**Why dates.** The turning-point test compares tablets written before and after a political event, so it needs tablets dated to a year or at least to a reign. CDLI records a king or a year for part of the corpus; the specialist databases built by Assyriologists over decades record many more. We joined them to the photographed tablets by museum and publication number [scripts 37c-37i, 98d-98j].

**Sources.** Table S7.1 gives the number of tablets whose final date comes from each source. Where a database and CDLI give different dates, the database date is used and the tablet is flagged (340 tablets; SI Dataset S1, column `conflict`). Regnal years were converted to years BCE in the middle chronology used by the ARCANE volumes [@sallabergerAssociatedRegionalChronologies2015] for the third millennium and by the standard reference works for the second and first.

{{TABLE:si_dates_sources}}

**Coverage.** Of the 30,696 tablets with a date in years BCE, 21,458 are Ur III, 3,474 Neo-Assyrian, 2,289 Old Babylonian, 1,012 Neo-Babylonian, 937 Achaemenid and 805 Early Dynastic IIIb. The Old Assyrian tablets were dated through the eponym list of the REL project matched to OARE (47 tablets dated to a year; 13 eponyms with homonyms are given as ranges); of 78 eponyms read on OARE tablets, 60 were matched to the REL list and 18 were not; the full matching list is released with the code. Archibab dates are released only as dates with the digital citation of each Archibab record.

**Tablets dated only to a reign.** 4,210 tablets are dated to a reign but not to a year (for example, Neo-Assyrian letters assigned to the correspondence of Sargon II or Esarhaddon). In the consolidated table such a tablet carries the accession year of its king in the column `bce`. A first run of the turning-point and scan scripts used this column as if it were the year of writing, which heaped thousands of tablets on accession years (1,150 at 722 BCE, 974 at 681 BCE, 713 at 669 BCE) and produced spurious change points at the midpoints between accessions. All tests reported here admit a reign-dated tablet into a window only when the whole reign falls inside it (`analysis/scripts/_reigns.py`), so that a tablet of Esarhaddon (681-669 BCE) counts as "after" for an event in 681, while a tablet of Assurbanipal (669-631 BCE) enters no 20-year window around 681.

# S8. The turning-point protocol

**Choosing the events.** Candidate events were collected from the standard political histories of each period before the shape data were examined, and kept if at least 30 dated archival tablets survive on each side within 20 years at the same sites [scripts 98c, 98k]. Ten events passed (Table S8.1). Among the candidates that failed for lack of dated tablets on one side are the accession of Sargon of Akkad, the end of the Akkadian dynasty, the fall of Isin to Larsa, the reforms of Tiglath-pileser III, the fall of Nineveh and the accession of Nebuchadnezzar II.

**Typing the events.** Each event was typed by what it did to the institutions that wrote the tablets, following the model of the Introduction: *reform* (the ruler changes how existing institutions keep their records), *foundation* (a new central institution with its own scribes), *collapse* (the centre loses its provinces), *conquest* (a state takes over another state's working administration) and *succession* (a new king or a reorganisation within the same state). The typing was fixed before the test and rests on the literature cited in the main text.

**Test.** The test is the same for every event and is described in Materials and Methods. Table S8.1 gives the results for both representations and both controls; Table S8.2 gives the shifts of the simple measures (proportion, corners, rectangularity, taper, side and end thickness), which exist for about a quarter of the tablets and are therefore tested only where at least three tablets on each side of a stratum have them.

{{TABLE:si_tp_events}}

{{TABLE:si_tp_features}}

**Power.** Table S8.3 gives, for each event, the 95th percentile of the null (the change that chance alone reaches one time in twenty), the observed change, the smallest change detectable with 80% power, and the power to detect a change of the size observed at the foundation of Puzriš-Dagan. Table S8.4 gives the pooled tests by type of event.

{{TABLE:si_tp_power}}

{{TABLE:si_tp_pooled}}

**Earlier analyses of Hammurabi's reign.** Before the protocol was fixed, Hammurabi's conquest of Larsa was tested in 39 cells of site and genre and by a scan of break years within his reign [scripts 75, 87, 98b, 98f]. No cell showed a shift at q < 0.05, and the strongest break fell at his accession (1792-1791 BCE), not at the conquest. These earlier analyses did not yet exclude reign-only dates; the protocol result above does.

# S9. The blind change-point scan

**Design.** The scan repeats the turning-point comparison at every year of four densely dated stretches with 10-year windows and 300 permutations per year [script 101]. Change points are years whose p-value survives Benjamini-Hochberg correction within the stretch and whose excess change is the largest within five years. Change points are compared with 23 listed events (the ten tested events and the accessions and reorganisations of the standard histories), counting a match within three years. The chance rate of a match is the share of scanned years that lie within three years of a listed event. The scan was repeated within every site and document type with at least 200 dated tablets (Table S9.1).

{{TABLE:si_scan_points}}

# S10. Polity scores and uniformity

**Scores.** The codebook (Appendix) defines twelve parameters in three dimensions, each scored 0 to 3 in half points, with the evidence each level requires. The scores rest on 915 quoted statements from 166 works, each with a page reference; S.G. reviewed every score and statement in three rounds (4, 8 and 9 November 2026), and the full statement table is SI Dataset S5. Table S10.1 gives the indices and the uniformity measures for the fourteen periods.

{{TABLE:si_period_table}}

**Tests.** Table S10.2 gives the Spearman correlations with permutation p-values and the range across 2,000 redraws of the score table; Table S10.3 the tablet-level regressions with museum fixed effects and wild cluster restricted bootstrap p-values [script 86]. With fourteen periods, a correlation must exceed about 0.54 in absolute value to reach p < 0.05; none does.

{{TABLE:si_spearman}}

{{TABLE:si_wild}}

**Earlier scores.** With the first literature-grounded scores (3 November 2026), the institutional economy index came closest (ρ = −0.52, p = 0.06 for the proportion of archival tablets). After S.G.'s review rounds it is weaker (ρ = −0.43, p = 0.12). The direction is unchanged.

# S11. Archives and collections

**Labels.** Archive labels come from Archibab (Old Babylonian), NaBuCCo and Prosobab (Neo-Babylonian and Achaemenid), the Oracc catalogues (Pedersén's Middle Assyrian archives at Assur; Neo-Assyrian findspot archives), the BDTNS provinces (Ur III) and the CDLI archive field; "Miscellaneous" and unknown archives were dropped [script 99b]. The type of document is the finest label available: Oracc subgenre or genre, NaBuCCo type, Archibab type or BDTNS type, otherwise the CDLI genre.

**Across archives.** Table S11.1 gives, for each period with at least two archives of 30 tablets, how often a tablet's archive is predicted from its shape (leave-one-out nearest median) against permuted labels; Table S11.2 the Mantel tests comparing distances between archive medians with distances in document-type, genre, museum and site mix and in median date.

{{TABLE:si_arch_across}}

{{TABLE:si_arch_mantel}}

**Within archives.** Table S11.3 gives, for each archive with at least 50 tablets, the normalised mutual information between its shape groups and each field, with Benjamini-Hochberg q-values (the main-text Fig. 6).

{{TABLE:si_arch_within}}

# S12. Results withdrawn or revised during the study

Distant viewing produces patterns quickly, and several did not survive closer checks. We list them so that readers can judge the protocol.

- *Literary tablets.* An apparent difference in the form of literary tablets across periods followed the holding museum and was withdrawn (S3).
- *"Breakage inflates dispersion."* This came from filtering to complete tablets; with damage as a control, the ranking of periods by uniformity is unchanged (S2).
- *Neo-Babylonian as the most varied period.* This came from wrong dimensions in one museum's catalogue entries (S5.1).
- *Change points at 1792, 713 and 676 BCE.* These came from tablets dated only to a reign being placed at the accession year (S7). After correction, the 1792 BCE Old Babylonian and the 713 and 676 BCE Neo-Assyrian change points disappear, and the scan finds no change points outside Ur III (S9).
- *Ibbi-Suen year 3 with the VAE.* A first run found a change of borderline significance with the VAE (p = 0.07); the corrected run does not (p = 0.12), while DINOv2 still does (S8).
- *The "centralization makes tablets uniform" hypothesis.* The pilot scores (October 2026) and the literature-grounded scores both reject it (S10).

# S13. Code, data and datasets

**Data.** Silhouettes, ratios, VAE codes and the trained VAE: Zenodo 10.5281/zenodo.11668220 and 10.5281/zenodo.12787746. CDLI catalogue: cdli.earth, checked October 2026. DINOv2 ViT-B/14 embeddings of the masks (92,876 × 768) were computed on S.G.'s Mac Studio (Python 3.12, torch 2.14, timm 1.0) and are released with the code.

**Code.** github.com/DigitalPasts/ShapingHistory, branch for this submission. The numbered scripts in `analysis/scripts` produce every number in the article and this SI; `experiments/EXPERIMENTS.md` lists each experiment, its scripts, its result and whether it is used. The scripts run on ShG's computers (DINOv2 embeddings, Archibab harvest, Oracc dating) are in `analysis/mac_studio/`.

**Datasets.**

- **Dataset S1** (tablet_dates_consolidated_public.csv.gz). One date per tablet with its source, the reign and year, a flag for conflicts, and a digital citation of the database record (for Archibab, its URL only).
- **Dataset S2** (tablet_dims_clean.csv). Cleaned catalogue dimensions for 66,711 tablets.
- **Dataset S3** (SI_amarna_letters.csv). The Amarna letters with sender, place of making, clay group, coordinates and measured ratio.
- **Dataset S4** (digeanna_merged.csv). DigEanna records merged with CDLI photographs.
- **Dataset S5** (lit_scores_v2_long.csv, lit_evidence_v2_long.csv). Polity scores and the 915 quoted statements behind them.
- **Dataset S6** (tp_protocol_*.csv, tp_power*.csv, cp_scan_*.csv, archive_*.csv). All turning-point, scan and archive results.
- **Dataset S7** (vae_measured_and_predicted.csv). The twelve VAE dimensions with measured and predicted outline features for all 92,876 tablets.
