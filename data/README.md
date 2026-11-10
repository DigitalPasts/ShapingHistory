# Data

## What is in this folder

`derived/` holds the result tables behind the article, written by the scripts in `analysis/scripts/`. Files over 2 MB are
gzipped (`pandas.read_csv` reads them as they are).

| Folder | Contents | Written by |
|---|---|---|
| `derived/corpus_sections2-5/` | Ratio statistics, dispersion by period and site, damage score, mask quality, period tables, museum and archive signal, Section 4 format tables, case-study tables, VAE dimension guide | scripts 01-64 |
| `derived/centralization/` | Codebook, literature evidence (quoted statements with pages), scores before and after each of ShG's review rounds, regional sub-scores, robust statistics, pilots, archive overview | scripts 70-97 |
| `derived/dating/` | Dates per tablet from the companion databases (BDTNS, NaBuCCo, Prosobab, Oracc, eBL, Hethport) and the consolidated date table | scripts 37c-37i, 98d-98j |
| `derived/turning_points/` | Dated counts, candidate testability, Hammurabi cells, group scan | scripts 94, 98-98k, 99 |
| `derived/archives/` | Shape groups across and within archives | script 99b |
| `derived/old_assyrian/` | Revised Eponym List (REL), eponym dates of Old Assyrian tablets, OARE genre and object type | scripts 37h, 37i |

## Inputs (download into `$SH_WORK`)

| Input | Source | Licence / note |
|---|---|---|
| Tablet silhouettes, VAE encodings, trained models | Zenodo [10.5281/zenodo.11668220](https://doi.org/10.5281/zenodo.11668220), [10.5281/zenodo.12787746](https://doi.org/10.5281/zenodo.12787746) | as on Zenodo |
| CDLI catalogue (`artifacts.csv`) | [cdli.earth](https://cdli.earth) data export | CC0 |
| BDTNS text types and dates | [bdtns.cesga.es](http://bdtns.cesga.es) (harvested by 37, 37c) | cite Molina, BDTNS |
| NaBuCCo | [nabucco.acdh.oeaw.ac.at](https://nabucco.acdh.oeaw.ac.at), per-archive CSV export (37e) | cite NaBuCCo |
| Prosobab | DANS [10.17026/dans-zvn-eece](https://doi.org/10.17026/dans-zvn-eece), dump of 3 June 2022 (37g) | as on DANS |
| Oracc catalogues | oracc-parser datasets, Zenodo [10.5281/zenodo.20625379](https://doi.org/10.5281/zenodo.20625379), plus `harvesters/oracc_catalogues.py` | per Oracc project |
| eBL fragment metadata | eBL public API (37d) | per eBL |
| Hethiter Konkordanz | [hethport.net](https://www.hethport.net) (37f) | per Hethport |
| Archibab text table | [archibab.fr](https://www.archibab.fr/textes), saved with `harvesters/archibab_table_v2.py` | **not redistributed**; see below |
| OARE published texts | Deep Past Challenge release (Kaggle, deep-past-initiative-machine-translation) | **not redistributed**; see below |
| Revised Eponym List | Barjamovic, Hertel and Larsen 2012, PIHANS 120, Appendix 1, transcribed in `derived/old_assyrian/rel_bhl2012.csv` | cite the book |
| Seshat Equinox-2020 | seshatdatabank.info (70) | CC BY-NC-SA |

## Withheld or reduced

- **Archibab.** Following ShG's decision of 10 Nov 2026, the dates taken from Archibab are released with the digital citation
  of each text: `dating/tablet_dates_consolidated_public.csv.gz` gives king, year and absolute date for the 608 tablets dated from
  Archibab, with the Archibab text identifier (`archibab_id`) and its URL (`archibab_url`, e.g. https://www.archibab.fr/T3955).
  Archibab's own records (summaries, references, archive labels) are not redistributed; `dating/archibab_cdli_links_ids_only.csv`
  gives only the identifier links. Cite: Charpin et al., ARCHIBAB, https://www.archibab.fr (accessed 9 Nov 2026).
- **OARE.** Only the OARE identifiers, genre and object type are released (`old_assyrian/oare_metadata_public.csv`), not the
  transliterations.
- **Goren et al. 2004** per-letter catalogue (case study B) and the literature full texts used to check quotations are not released.
