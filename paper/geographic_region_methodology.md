# Geographic Region Assignment — Methodology and Citations

*For use in the Materials and Methods section and supplementary material of "Shaping History at Scale"*

---

## Overview

Each tablet in the CDLI corpus carries a `provenience` field — the archaeological site or city from which it originates. To study regional variation in tablet morphology, we assign each site to a geographic zone using a two-step process: (1) an automated lookup against the CDLI Linked Open Data geographic ontology, and (2) a small manually curated supplement for high-frequency sites absent from that ontology.

---

## Data Sources

### 1. CDLI Catalogue (`artifacts.csv`)

Provenience information is taken directly from the CDLI catalogue export. Each tablet's provenience is recorded as a free-text string in the canonical CDLI format, e.g., `Nippur (mod. Nuffar)`. The ancient site name is extracted by stripping the modern toponym parenthetical.

**Citation:** Cuneiform Digital Library Initiative (CDLI). *CDLI Catalogue*. https://cdli.ucla.edu. Data accessed 2024. For the original project see: Englund, R. K., & Grégoire, J.-P. (1991). *The Proto-Cuneiform Texts from Jemdet Nasr*. Berlin: Gebr. Mann Verlag.

### 2. CDLI Linked Open Data — `places.nt`

The file `places.nt` is an RDF N-Triples export from the CDLI Linked Open Data (LOD) infrastructure (cdli.network). It encodes 737 named provenience entities and, for 245 of them, an explicit region assignment via the CIDOC-CRM spatial containment predicate `P89_falls_within` (from the CIDOC-CRM ontology, v7.1). Each provenience entity is linked to one of **19 CDLI-defined geographic regions**.

The CDLI LOD geographic ontology is itself grounded in **Pleiades** — an open, peer-reviewed gazetteer of ancient places. This connection is encoded directly in `places.nt` via the predicate `pleiades.stoa.org/places/vocab#hasLocation`, linking each CDLI region entity to its Pleiades counterpart.

**Citation (CDLI LOD):** CDLI Linked Open Data. cdli.network. Accessed 2024.

**Citation (Pleiades):** Bagnall, R. S., et al. (eds.). *Pleiades: A community-built gazetteer and graph of ancient places*. https://pleiades.stoa.org. Institute for the Study of the Ancient World (ISAW), New York University, 2006–. Accessed 2024.

**Citation (CIDOC-CRM):** Bekiari, C., et al. (2021). *CIDOC Conceptual Reference Model*, version 7.1. International Council of Museums (ICOM). https://cidoc-crm.org.

### 3. Manual Supplement for Unmatched Sites

A small number of high-frequency sites in the 2nd–1st millennium corpus are absent from the `places.nt` region assignments. These are assigned manually by the authors on the basis of standard historical-geographic references:

| Site (CDLI label) | Manual region | Authority |
|---|---|---|
| Puzriš-Dagan | Southern Mesopotamia | Steinkeller (1987); Sigrist (1992) |
| Ḫattusa | Western and Central Anatolia | Bryce (2005) |
| Ešnunna | Central Mesopotamia | Hamblin (2006) |
| Garšana | Southern Mesopotamia | Owen & Mayr (2007) |
| Pārśa (Persepolis) | Eastern Iran | Brosius (2006) |

A complete site-level table (all sites, their CDLI region from `places.nt` or manual assignment, and tablet counts per millennium) is provided as **Supplementary Table S-Geo**.

---

## The 19 CDLI Regions

As defined in `places.nt` and cdli.network:

1. Western and Central Anatolia
2. Northern Levant
3. Southern Levant
4. Middle Euphrates
5. Jazirah
6. Tigridian Region
7. Central Mesopotamia
8. Southern Mesopotamia
9. Western Iran
10. Upper Euphrates
11. South Caucasus
12. Cyprus
13. Lower Egypt
14. Upper Egypt
15. Eastern Arabia
16. Western Mediterranean
17. Eastern Mediterranean
18. Eastern Iran
19. Arabian Peninsula

---

## Aggregation into 5 Analytical Zones

For statistical comparisons across the 2nd–1st millennium transition, the 19 CDLI regions are collapsed into 5 analytical zones. This aggregation is necessary because most individual CDLI regions have insufficient tablet counts in one or both millennia for robust non-parametric testing (minimum N ≥ 30 per cell). The collapsing reflects historical-geographic coherence as defined in standard reference works (Roaf 1990; Radner & Robson 2011).

| Analytical Zone | CDLI Regions Included | Historical rationale |
|---|---|---|
| **Southern Mesopotamia** | Southern Mesopotamia | Core Sumerian/Babylonian heartland (Nippur, Uruk, Ur, Girsu, Umma, Larsa) |
| **Central/Northern Babylonia** | Central Mesopotamia, Middle Euphrates | Babylonian cities north of Nippur plus Middle Euphrates (Sippar, Babylon, Kish, Mari, Emar) |
| **Assyria / Upper Mesopotamia** | Tigridian Region, Jazirah | Assyrian heartland and Syrian steppe (Assur, Nineveh, Kalhu, Nuzi) |
| **Elam / Western Iran** | Western Iran, Eastern Iran | Elamite sphere and Iranian plateau (Susa, Kabnak, Persepolis) |
| **Periphery** | Western & Central Anatolia, Northern Levant, Southern Levant, Upper Euphrates | Sites at the geographic margins of cuneiform culture (Kanesh, Ḫattusa, Ugarit, Alalakh, Ebla) |

**References for zone collapsing:**
- Roaf, M. (1990). *Cultural Atlas of Mesopotamia and the Ancient Near East*. Oxford: Facts on File.
- Radner, K., & Robson, E. (eds.) (2011). *The Oxford Handbook of Cuneiform Culture*. Oxford University Press.

---

## Methodological Note for the Paper (draft text)

> Geographic regions are assigned to individual tablets via the CDLI Linked Open Data ontology (`places.nt`; cdli.network), which encodes site-to-region containment relationships derived from the Pleiades ancient world gazetteer (Bagnall et al. 2006–). Of the provenience strings recorded in the CDLI catalogue, 120 unique site names carry an explicit region assignment in this ontology, covering the large majority of tablets with known provenience in the 2nd–1st millennium subsample. For five high-frequency sites absent from the automated lookup (Puzriš-Dagan, Ḫattusa, Ešnunna, Garšana, Pārśa), region assignments were made manually by the authors following standard historical-geographic references (see Supplementary Table S-Geo). Tablets with uncertain provenience (`is_provenience_uncertain = True` in the CDLI catalogue) or with the provenience string `uncertain (mod. uncertain)` are excluded from the regional analysis but retained in all other analyses. The 19 CDLI regions are further aggregated into 5 analytical zones for statistical power; the basis for this aggregation is documented in Supplementary Table S-Geo.

---

## Transparent Limitations

1. **Provenience uncertainty**: ~15,264 tablets in the full corpus are flagged `is_provenience_uncertain`. These are excluded from the geographic analysis. Their exclusion should be noted; if their period and genre distribution differs systematically from tablets with secure provenience, results may not be fully representative.

2. **The Uruk problem**: Uruk (mod. Warka) contributes 323 tablets in the 2nd millennium but 5,337 in the 1st millennium — a 16× ratio. Because Uruk is the largest single site in the 1st-millennium sample, the overall corpus-level portrait→landscape shift could partially reflect a **compositional sampling bias** toward Uruk rather than a universal production-practice change. The geographic analysis in notebook 2.6 is designed explicitly to test this: if the trend is real, it should appear *within* Uruk across time (controlling for site) and *across* multiple regions independently.

3. **`places.nt` coverage**: Of 737 provenience entities in the ontology, only 245 carry region assignments (33%). Coverage is good for the major excavated sites but sparse for smaller or uncertain proveniences. This should be disclosed.

4. **Zone boundaries are scholarly choices**: The aggregation from 19 CDLI regions to 5 analytical zones is a decision made by the authors, not derived from the data. A different aggregation could yield different within-zone vs. between-zone decomposition results. The zone boundaries and the justification for them must be explicit in the paper.

---

*Document created: 2026-03-30. Update this file when supplementary table S-Geo is finalized.*
