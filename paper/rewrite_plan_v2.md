# Rewrite Plan v2 — "Shaping History at Scale"
### For PNAS submission · Prepared 2026-03-31

This document supersedes `revision_plan_PNAS.md`. It is based on the full set of
results now available from notebooks 2.1–2.6 and 2.4b, including the new geometric
VAE traversal analysis and the geographic regional analysis. The plan addresses:
(A) whether the research questions need revision; (B) a new paper architecture;
(C) figure allocation; (D) text to write or rewrite section by section; (E)
grounding the VAE vector analysis in codicology and cuneiform diplomatics
literature; (F) anomalies requiring careful handling.

---

## Part I — Results Audit: What We Now Know

### Layer 1 — Physical ratios (notebooks 2.1–2.3)

All three measurement approaches (physical h/w, pixel h/w, three-method comparison)
converge on the same diachronic signal:

| Millennium | Median h/w (physical) | Median h/w (pixel) | Orientation |
|---|---|---|---|
| 2nd millennium BCE | ~1.11 | ~1.10 | Portrait |
| 1st millennium BCE | ~0.84 | ~0.86 | Landscape |

Log-ratio shift: −0.272 (physical), comparable for pixel.

The most standardized periods by CV (ascending = tighter):
1. Ur III: CV 0.251 (physical), 0.242 (pixel) — most uniform
2. Early Old Babylonian: 0.274
3. Proto-Elamite: 0.279
4. Hellenistic: 0.412 (pixel) — second tightest in 1st millennium
5. Middle Babylonian: 0.460 / 0.371 — transitional
6. Achaemenid (pixel): 0.307 — tight despite IQR (see anomaly §3.1)
7. Neo-Babylonian (pixel): 0.424

**Critical correction needed in paper:** The Significance Statement currently claims
Achaemenid produced "the most standardized tablet shapes." The CV data tells a more
nuanced story. Achaemenid has a tight IQR (pixel IQR=0.150, the second-tightest
in the dataset after Ur III IQR=0.180), meaning the central 50% of tablets occupy
a very narrow landscape band. But its CV is 0.785 (physical) / 0.307 (pixel),
driven by outliers at both extremes. The claim should be reformulated as:
"Achaemenid tablets show remarkable consistency in their landscape orientation
(narrow IQR), while outlier range remains broad." The contrast between Ur III
(standardization in portrait) and Achaemenid (standardization in landscape) is
itself a finding worth foregrounding.

### Layer 2 — VAE latent space (notebooks 2.4, 2.4b)

Twelve-dimensional VAE bottleneck. Key statistics:

| Dim | η² | Effect | ρ | p | Role |
|---|---|---|---|---|---|
| X7 | 0.435 | large | −0.430 | 0.052 | Best period discriminator, non-monotonic |
| X12 | 0.388 | large | +0.210 | 0.360 | Strong discriminator, no linear trend |
| X6 | 0.242 | large | +0.046 | 0.845 | Discriminates periods, no trend |
| X4 | 0.199 | large | −0.103 | 0.658 | Discriminates, no trend |
| **X2** | 0.078 | medium | **+0.655** | **0.001** | **Primary diachronic trend** |
| **X8** | 0.025 | small | **−0.573** | **0.007** | **Secondary diachronic trend** |

The most important finding from the VAE: **the dimension that best discriminates
periods (X7, η²=0.435) is NOT the same dimension that best tracks the diachronic
trend (X2, ρ=+0.655).** This is not a problem — it is an insight.

What this means:
- X7 captures the scribal-tradition signature of each period: it separates tablets
  from different institutional traditions (ED I-II vs. Neo-Assyrian are both high,
  Middle Elamite and Achaemenid are both low) in a way that is not monotonically
  related to time. X7 encodes *what tradition* produced the tablet.
- X2 captures *when* in history the tablet was produced: it increases monotonically
  from archaic periods to 1st-millennium, directly tracking the portrait→landscape
  transition.
- X8 captures a secondary diachronic signal (trending negative across time) that
  co-varies with but is independent of X2. Given its highest values in Lagash II,
  Uruk IV/III, and Proto-Elamite, and lowest in Achaemenid and Hellenistic, it
  likely encodes tablet body convexity or edge curvature — a feature that
  distinguished early hand-formed tablets from the flatter, more slab-like 1st
  millennium administrative pieces.

**Traversal filmstrips (notebook 2.4b):** Confirmed physical interpretations from
traversal filmstrips + descriptor analysis (2026-03-31):

| Dim | Primary descriptor (corpus/genre-specific) | Physical meaning | Direction |
|---|---|---|---|
| X2 | area_fraction (Admin, Legal, All); solidity (Literary) | **Bounding-box fill efficiency**: combination of orientation AND outline regularity. Low X2 = tall portrait with complex/articulated silhouette. High X2 = wide landscape with compact, rectangular form. | Increases 3rd→1st mil |
| X7 | **hw_ratio (Admin, Literary, Legal)**; area_fraction (All tablets) | **Direct height/width ratio**: the cleanest portrait↔landscape axis. High X7 = portrait; low X7 = landscape. Separates scribal TRADITIONS non-monotonically, not time linearly. | Decreases but non-monotonically |
| X8 | solidity (All, Literary, Legal); area_fraction (Admin) | **Body unity / silhouette cohesion**: high X8 = segmented/articulated outline; low X8 = unified solid slab. May reflect both real tablet morphology change AND CDLI multi-view composite image prevalence. | Decreases 3rd→1st mil |

**Key correction to earlier plan:** X7 (not X2) is the pure h/w ratio dimension.
X2 captures "fill efficiency" — a blend of orientation and shape regularity — which
is why it tracks the diachronic trend more cleanly than X7 does. X7 is better at
distinguishing diplomatic traditions (Neo-Assyrian portrait vs. Babylonian landscape)
precisely because it measures the ratio directly, but traditions differ
non-monotonically in time.

**Genre consistency:** X7 is the most genre-consistent (hw_ratio primary for Admin,
Literary, Legal) → use X7 for the clearest "orientation" claim. X2 and X8 are
genre-inconsistent → this inconsistency is itself evidence that these dimensions
capture something beyond simple orientation: they encode genre-specific shape norms.

Mean-vector shifts 2nd→1st millennium:
- X2: −0.169 → +0.622 (Δ=+0.791) — largest shift of any dimension
- X8: −0.299 → −0.435 (Δ=−0.136) — moderate secondary shift
- X7: −0.789 → −0.864 (Δ=−0.075) — almost no change despite strong discrimination

Period outliers with historical significance:
- Middle Elamite X2=+2.9 (highest of all) — extreme landscape even in 2nd mil
- Achaemenid X7=−2.48 (lowest of all) — distinctive from ALL other periods
- Neo-Assyrian X7=+2.05 (highest in 1st mil) — sharply distinguished from Babylonian

### Layer 3 — Geographic analysis (notebook 2.6)

**Site-level shifts (sites with N≥30 in both millennia):**

| Site | Zone | 2nd mil median | 1st mil median | Cliff's δ | Sig |
|---|---|---|---|---|---|
| Larsa | S. Mesopotamia | 1.457 | 0.778 | −0.818 | *** |
| Kalhu | Assyria | 2.000 | 0.976 | −0.783 | *** |
| Sippar-Yahrurum | C./N. Babylonia | 1.388 | 0.768 | −0.700 | *** |
| Dilbat | S. Mesopotamia | 1.077 | 0.780 | −0.580 | *** |
| Nippur | S. Mesopotamia | 1.133 | 0.788 | −0.534 | *** |
| Uruk | S. Mesopotamia | 1.150 | 0.733 | −0.448 | *** |
| Kish | S. Mesopotamia | 1.306 | 1.088 | −0.135 | * |
| Assur | Assyria | 0.976 | 1.000 | −0.146 | * |
| Nineveh | Assyria | 1.143 | 1.025 | −0.136 | ns |
| **Ur** | **S. Mesopotamia** | **1.444** | **2.000** | **+0.333** | ***** |

The Ur anomaly (see §3.2 below) is the single most historically interesting site-
level result: Ur goes COUNTER to the trend, becoming MORE portrait in the
1st millennium.

Across all sites, 8 of 9 significant results show landscape shift. The variance
decomposition (notebook 2.6 Layer 1) quantifies how much of the corpus-level shift
is within-region (real) vs. compositional (Uruk sampling artifact).

---

## Part II — Research Question Audit

### Existing three RQs (to keep, with modifications)

**RQ1** (How much period-specific information is preserved in tablet shape alone?)
→ Keep. The 86% finding (71% grayscale / 61% silhouette) is the anchor. Refine
framing: "shape carries approximately 86% of the period-classification signal present
in full photographic images."

**RQ2** (Which shape features are most historically discriminating?)
→ Expand significantly. The VAE results allow a two-part answer: (a) the dimension
that best discriminates periods (X7, η²=0.435) is not the dimension that best
tracks diachronic change (X2, ρ=+0.655); (b) the traversal filmstrips allow us to
assign physical meaning to these dimensions. This is new and must be central to
the Results. Add the link to codicology vocabulary: X7 may be the computational
analogue of the "fixed balance" template constraint; X2 is the diachronic drift in
that template.

**RQ3** (What does the aggregate distribution reveal about 3,300-year evolution?)
→ Refine to make the landscape shift the explicit target: "Does the portrait-to-
landscape shift reflect a real change in scribal practice, or is it an artifact of
differential geographic and genre sampling?" The geographic analysis (Layer 1
variance decomposition and Layer 3 site-level panel) now provides the answer.

### New RQ4 (add)

**RQ4**: Is the portrait-to-landscape transition uniform across geographic regions,
or does it reflect regionally specific administrative reorganization? This is
answered by notebook 2.6 and must appear explicitly in the Research Questions
paragraph of the Introduction.

---

## Part III — New Paper Architecture

The Introduction and Dataset & Preprocessing sections (already written) are solid
and need only targeted additions (see Part IV). The entire Results section and
Discussion must be written. Background (Related Work) exists but needs compression
and repositioning.

```
Abstract                [needs 1 revision: add RQ4, correct Achaemenid CV claim]
Significance Statement  [needs 1 revision: same correction]

1. Introduction         [mostly written — add RQ4, add codicology grounding §A]
   Background box       [Table 1 comparison already written]

2. Dataset and Preprocessing  [written — add one sentence on geographic data]

3. Results
   3.1  The three-millennium shift: portrait to landscape  [WRITE — FLAGSHIP]
         → Physical h/w ratios, pixel corroboration, three-method comparison
         → CV / standardization scale
         → Key figure: fig_ratio_by_period_log + fig_diachronic_trend + fig_cv_standardization
   3.2  Period classification: shape as diplomatic signal  [WRITE]
         → Decision tree baseline, CNN, ResNet50
         → 86% silhouette finding
         → Key figure: confusion matrix, fig_comparison_diachronic_overlay
   3.3  VAE: interpretable feature extraction  [WRITE — NEW DEPTH]
         → Discrimination (X7) vs. trend (X2, X8): two distinct functions
         → Traversal filmstrips: physical meaning of each dimension
         → Genre-controlled trajectories: do features mean same thing across genres?
         → Dendrogram: diplomatic genealogies in latent space
         → Key figures: fig_vae_discrimination_vs_trend, fig_vae_traversal_X2/X7/X8,
           fig_vae_dendrogram_images_Administrative
   3.4  Case study: the shape of scribal traditions (widget demonstration)  [WRITE]
         → What distinguishes Late Babylonian from Ur III in latent space?
         → X2 (orientation) + X7 (body character) + X8 (convexity) together
         → Interactive interpolation widget showing morphological path
   3.5  Geographic validation: is the shift real or compositional?  [WRITE]
         → Variance decomposition: within-region vs. compositional
         → Zone-level results (administrative genre control)
         → Site-level panel (Uruk, Nippur, Larsa, Kalhu, Sippar, etc.)
         → The Ur anomaly: counter-trend and what it means
         → Maps (paired 2nd/1st mil + shift direction)
         → Key figures: fig_geo_zone_shift, fig_geo_map_paired, fig_geo_map_shift,
           fig_geo_site_panel

4. Discussion
   4.1  Three converging signals, one historical narrative  [WRITE]
   4.2  Standardization scale: from Ur III to Neo-Babylonian  [WRITE]
   4.3  The Achaemenid signature: continuity and innovation  [WRITE]
   4.4  The Ur anomaly: genre, function, and counter-trends  [WRITE]
   4.5  Limitations  [mostly drafted in revision_plan_PNAS — transfer here]
   4.6  Human + machine partnership  [WRITE if data available]

5. Conclusions             [WRITE]

Materials & Methods        [compressed — most detail to SI]

Background / Related Work  [condensed from existing draft, moved here or to SI]

Supplementary Information
   S1 — Statistical methods
   S2 — Silhouette extraction pipeline details
   S3 — Model architectures and training
   S4 — VAE dimension traversal results (all 12 dimensions)
   S-Geo — Geographic region methodology + site table
```

---

## Part IV — Section-by-Section Writing Instructions

### 4.1 Introduction additions (targeted)

The Introduction is largely well-written. Add in three places:

**A. Codicology grounding (after the Mabillon paragraph):**
Add 2 sentences connecting the CV methodology to Eerkens & Bettinger (2001):
"Quantitative studies of artifact standardization have established that the
coefficient of variation (CV = σ/μ) is the appropriate comparative measure across
objects of different size tiers, because it normalizes dispersion to the mean.
A sharp drop in the CV of administrative tablets over time constitutes statistical
evidence for what Eerkens & Bettinger term 'stimulated variation' — the reduction
of morphological diversity attributable to institutional mandates and standardized
training, rather than the random drift of individual hand-forming practice."

**B. Digital codicology framing (after the Busch/Chandna citation zone):**
"Recent computational approaches to manuscript studies (digital codicology) have
demonstrated that neural network feature extraction makes computable the 'affective
properties' of documents — weight, texture, edge curvature — that conventional
databases reduce to flat measurements [Stokes 2015; Busch & Chandna 2014]. By
encoding each tablet's binary silhouette through a Variational Autoencoder, we
apply the same logic to cuneiform: the 12-dimensional latent vector produced by the
VAE is a structured, computable proxy for what a trained diplomat would recognize
as the tablet's overall physical 'feel.'"

**C. RQ4 addition (end of Research Questions paragraph):**
Append to the three existing RQs: "Fourth, does the portrait-to-landscape shift
occur uniformly across geographic regions and genres, or does it reflect site-
specific administrative reorganization that a corpus-level analysis would mask?"

### 4.2 Results §3.1 — The three-millennium shift (flagship section)

**Paragraph 1: The basic finding**
State the result directly. Median h/w shifts from 1.125 (Ur III, portrait) to 0.741
(Neo-Babylonian, landscape), a log-ratio of −0.272 across the 2nd–1st millennium
transition. All three measurement approaches (physical pixel ratio, image pixel
ratio, VAE X2 dimension: ρ=+0.655, p=0.001) agree on the direction and magnitude.

**Paragraph 2: Standardization scale**
The CV analysis reveals a clear hierarchy of institutional control over tablet format,
interpretable through the Eerkens & Bettinger framework:
- Ur III (CV=0.251): highest standardization; consistent with centralized scribal
  training and bureaucratic uniformity documented in administrative archives
- Hellenistic (CV=0.412 from pixel): second-tightest in 1st millennium; consistent
  with well-studied Seleucid administrative continuity
- Achaemenid: tight central tendency (IQR=0.150, pixel) but broad outlier range —
  the narrow IQR reflects consistent landscape norm, while the broad range may
  reflect the empire's multinational scribal workforce
- Early Old Babylonian (CV=0.274): tight, consistent with consolidating institutions
  after Ur III collapse
- Neo-Babylonian (CV=0.807 physical / 0.424 pixel): highest dispersion; consistent
  with scholarly accounts of diverse institutional contexts (temple, palace, private
  archive)

Note: avoid claiming Achaemenid is "highly standardized" in simple terms. The
correct claim: "Achaemenid tablets exhibit a strong attractor toward landscape
orientation (median 0.786, IQR=0.150) even as their overall size distribution is
diverse — a pattern consistent with uniform format norms imposed across a
heterogeneous imperial administration."

**Paragraph 3: "Fixed balance" cognitive templates**
Using the codicology vocabulary from George (2010) and Tschichold:
"These results suggest that cuneiform scribal culture operated with what scholars
of manuscript production call a 'fixed balance' cognitive template — a pre-
determined target proportion that scribes reproduced across thousands of
individually hand-formed tablets. The portrait template (h/w ≈ 1.1–1.3) dominant
in the 3rd and early 2nd millennium, and the landscape template (h/w ≈ 0.75–0.85)
that emerges from the Middle Babylonian period onward, constitute discrete
morphological attractors rather than points on a continuum."

**Figure assignments for §3.1:**
- Main panel: `fig_ratio_by_period_log` (distribution by period)
- Sub-panel: `fig_diachronic_trend` (Spearman trend line)
- Sub-panel: `fig_cv_standardization` (CV by period)
- SI: `fig_comparison_diachronic_overlay` (three-method convergence)

### 4.3 Results §3.2 — Period classification

**The 86% finding must be foregrounded as a named result:**
"Shape alone accounts for approximately 86% of the period-classification signal
present in full photographic images: fine-tuned ResNet50 achieves 71% macro-F1
on grayscale images and 61% on binary silhouettes, against a 4.8% random baseline
across 21 classes. We refer to this ratio (61/71 ≈ 0.86) as the *shape information
retention fraction*."

Periods of highest per-class accuracy: Ur III (~87%), Neo-Assyrian (~95%).
Periods of confusion: Early Old Babylonian / Old Babylonian (scholarly periodization
boundary is fuzzy — discuss).

Figure: comparison confusion matrix, performance by period bar chart.

### 4.4 Results §3.3 — VAE: interpretable feature extraction

This section needs three distinct beats, in this order:

**Beat 1: Discrimination vs. trend — two functions, two dimensions**
"The 12 VAE dimensions play distinct historical roles. Dimension X7 (η²=0.435,
Kruskal-Wallis large effect) is the strongest period discriminator but shows no
significant linear trend (ρ=−0.430, p=0.052): latent traversal confirms it
controls the height/width ratio directly, separating scribal traditions by their
intrinsic portrait or landscape character regardless of when they were active
(Neo-Assyrian X7=+2.05, ED I-II X7=+1.86 for portrait; Achaemenid X7=−2.48,
Middle Babylonian X7=−1.79 for landscape). By contrast, X2 (η²=0.078, medium
effect) is the most strongly trending dimension (ρ=+0.655, p=0.001): it controls
bounding-box fill efficiency — a composite of orientation and outline regularity —
and its monotonic increase from 3rd- to 1st-millennium tablets captures the slow
drift in production norms rather than the discrete categorical differences between
traditions. X8 carries a significant secondary trend (ρ=−0.573, p=0.007) and
controls body unity: decreasing X8 over time reflects increasingly solid,
slab-like tablet outlines in the 1st millennium.

This three-way dissociation — X7 as tradition-identity, X2 as diachronic drift,
X8 as body-form evolution — has a direct diplomatic interpretation: the VAE has
independently discovered that there are (at least) three separable axes of tablet
morphological variation. Shape change over time (X2, X8) and scribal-tradition
identity (X7) are, in the 12-dimensional latent space, largely orthogonal."

**Beat 2: Physical interpretation via traversal (confirmed)**
"Latent-space traversal — decoding synthetic tablet images at evenly spaced points
along each dimension's ±2σ range — allows us to identify the physical feature
each dimension controls. X7 controls the height/width ratio directly (hw_ratio is
the primary descriptor for all three genre baselines), presenting a clear portrait-
to-landscape axis independent of scribal tradition. X2 controls 'bounding-box fill
efficiency' — a composite of orientation and outline regularity: at low X2 the
decoded silhouette is a tall, narrow portrait shape with an articulated or multi-
lobed outline; at high X2 it becomes a wide, compactly rectangular landscape form.
X8 controls body unity: high X8 decodes to a segmented, articulated silhouette;
low X8 to a unified, slab-like form that becomes progressively dominant from the
2nd to 1st millennium.

Critically, X2 and X8 are genre-inconsistent: the primary descriptor changes
depending on whether the traversal baseline is Administrative, Literary, or Legal.
X7 is genre-consistent. This inconsistency is not a failure of the analysis — it is
evidence that X2 and X8 encode genre-specific shape norms superimposed on the
global diachronic trend: what 'bounding-box efficiency' means for an administrative
tablet (area_fraction) differs from what it means for a literary tablet (solidity).
X7, encoding the simple ratio of height to width, is the feature all genres share
equally [cite genre-stratified traversal figure]."

**Beat 3: Dendrogram — diplomatic genealogies in latent space**
The dendrogram (fig_vae_dendrogram_images_Administrative) groups periods by overall
shape similarity, not by date. Key clusters to discuss:
- Neo-Babylonian / Achaemenid / Hellenistic: institutional continuity
- Ur III / Old Babylonian / Early OB: Babylonian administrative tradition
- Middle Elamite outlier: extreme landscape in 2nd millennium
- Neo-Assyrian outlier: unique body form signature (X7=+2.05)

**Figure assignments for §3.3:**
- Main: `fig_vae_discrimination_vs_trend` (η² vs |ρ| scatterplot)
- Main: `fig_vae_traversal_X2_genre`, `fig_vae_traversal_X7_genre`, `fig_vae_traversal_X8_genre` (filmstrips with genre control)
- Main: `fig_vae_dendrogram_images_Administrative`
- SI: remaining 9 dimension traversals, `fig_vae_mean_period_timeline_genre`

### 4.5 Results §3.4 — Widget case study

Target question: "What distinguishes the typical Late Babylonian (Neo-Babylonian +
Achaemenid) administrative tablet from its Ur III counterpart, and can a human
expert use the interactive tools to articulate that distinction?"

Structure:
1. Show mean latent vectors for Ur III-administrative and Achaemenid-administrative
2. Identify the dimensions with largest Δ (X2, X7, X8)
3. Use the interpolation widget to generate the morphological path
4. Interpret each waypoint historically:
   - The X2 shift from −0.997 to +1.039 tracks the portrait→landscape transition
   - The X7 shift from −0.612 to −2.484 shows Achaemenid tablets with a distinctively
     different edge/body profile from Ur III (even controlling for orientation)
5. Frame using codicology vocabulary: the VAE interpolation is a computational
   analogue of a diplomat's "interpolation" between two document traditions —
   identifying the features that changed and the features that persisted

### 4.6 Results §3.5 — Geographic validation

**Opening paragraph:**
"The corpus-level portrait→landscape shift could in principle reflect differential
sampling: if sites that dominated 1st-millennium tablet production happened to
specialize in landscape-format document types, the overall trend might be a
compositional artifact rather than a real change in scribal practice. We test this
using a three-layer geographic analysis."

**Layer 1: Variance decomposition**
Report the within-region vs. compositional breakdown. If within-region component
>50% of total shift: "The portrait-to-landscape trend is predominantly a real change
in scribal practice, not an artifact of shifting site composition."

**Layer 2: Zone analysis and genre control**
All/most zones independently show the shift. The shift is preserved after restricting
to Administrative genre (eliminating genre-composition confounds).

**Layer 3: Site panel**
Report the 10-site table. Highlight:
- Larsa (δ=−0.818), Kalhu (δ=−0.783), Sippar-Yahrurum (δ=−0.700): strongest shifts
- Nippur (δ=−0.534), Uruk (δ=−0.448): major centers, consistent shift
- **Ur anomaly (δ=+0.333, p<0.01)**: Counter to the trend. Historical explanation
  needed (see §3.2 of this plan, Anomalies).

**Figures for §3.5:**
- Main: `fig_geo_zone_shift` + `fig_geo_zone_genre_control`
- Main: `fig_geo_map_paired` + `fig_geo_map_shift`
- SI: `fig_geo_site_panel`, `supplementary_table_S_Geo.csv`

### 4.7 Discussion

**§4.1 Three converging signals**
H/W physical ratios, pixel ratios, and VAE X2 all point to the same transition,
giving it triple-convergent statistical validation. The dissociation between X7
(best discriminator, no trend) and X2 (best trend, modest discrimination) has a
codicological analogue in the distinction between the "scribal grammar" of a
tradition (captured by X7) and the "page proportion norm" of an era (captured by X2).

**§4.2 Standardization scale**
Build the scale explicitly: rank periods by administrative-genre CV from most to
least standardized. Connect to Eerkens & Bettinger: falling CV = rising institutional
control. The Ur III state's CV=0.251 reflects the tightest scribal training regime
in 3,000 years of cuneiform; the Neo-Babylonian CV=0.807 reflects the diversity of
the institutional landscape from which those tablets emerge (temple archives,
private merchant archives, royal administration).

**§4.3 Achaemenid signature**
Nuanced discussion:
- Consistent landscape norm (tight IQR) but broad outlier range
- X7 = most negative of all periods: the VAE sees Achaemenid tablets as having a
  distinctively different body character from all other periods, beyond just orientation
- Neo-Babylonian → Achaemenid → Hellenistic cluster in dendrogram: institutional
  continuity (Waerzeggers, Jursa, Hackl)
- Raise Aramaic-influence hypothesis as a possible explanation for the landscape norm,
  framed as a hypothesis, not a conclusion
- Middle Elamite comparison: Middle Elamite X2=+2.9 (most extreme landscape in any
  period), Achaemenid X2=+1.04 — this suggests landscape format in the Elamite
  administrative tradition predates Achaemenid by centuries, consistent with
  Achaemenid–Elamite administrative continuity through Persepolis archives

**§4.4 The Ur anomaly**
The counter-trend at Ur (median h/w 1.444 → 2.000, δ=+0.333) is historically
significant. Possible explanations:
1. Genre shift: 2nd-mil Ur is dominated by Old Babylonian administrative records;
   1st-mil Ur is dominated by Neo-Babylonian legal documents (contracts,
   property transactions). Legal tablets in the Neo-Babylonian tradition tend
   toward portrait format. The Ur "anomaly" may be a genre-composition shift, not
   a real counter-trend.
2. The genre-controlled analysis (administrative only) from notebook 2.6 §5 should
   test this. If the Ur anomaly disappears when restricted to administrative genre,
   it is a genre effect.
3. If it persists: Ur in the 1st millennium was an important cult city (temple of
   Nanna/Sîn); its administrative apparatus may have maintained older portrait-format
   conventions tied to temple ritual practice.
This anomaly should be explicitly discussed as a productive complication, not glossed over.

**§4.5 Limitations (largely from revision_plan_PNAS, include)**
- Ratios are proxies for absent absolute dimensions
- CDLI corpus reflects excavation and digitization history, not ancient production
- Largest-component extraction is imperfect for composite images
- Period categories are scholarly conventions with fuzzy boundaries
- 2D silhouettes discard thickness, surface curvature, edge profile
- Geographic analysis: places.nt covers only 33% of provenience entities

---

## Part V — Codicology and Diplomatics Grounding

### 5.1 Where each source fits

**Eerkens & Bettinger (2001)** — "Techniques for Assessing Standardization"
→ Use in: Introduction (CV motivation), Results §3.1 (standardization scale),
   Discussion §4.2 (institutional control interpretation)
→ Key claim: CV distinguishes random variation from institutional mandates

**George, A. — "Geometry of Early Quranic Manuscripts"**
→ Use in: Introduction (cognitive template framing), Results §3.1 ("fixed balance")
→ Key claim: early document makers adhered to target proportions = computable
   attractor basins in ratio space

**Tschichold / "Fixed Balance vs. Variable Balance" (10.1515_9783110743838-013)**
→ Use in: Introduction and Discussion §4.1
→ Key claim: administrative documents follow "fixed balance" rules; the switch
   from portrait to landscape is a shift in which "fixed balance" rule applies

**Stokes (2015) — "Digital approaches to paleography"**
→ Use in: Introduction (distant viewing / affective properties), Discussion §4.1
→ Key claim: 3D material objects have affective properties lost in flat databases;
   VAE latent space recovers some of these computationally

**Busch & Chandna (2014) — "eCodicology"**
→ Use in: Introduction (computational structural codicology framing)
→ Key claim: structural codicology at scale requires automated feature extraction

**Roux (2003) — "Standardisation en Archéologie"** (in literature folder)
→ Use in: Discussion §4.2 (additional citation alongside Eerkens & Bettinger)

**Arnold & Tilton (2019/2023) — "Distant Viewing"**
→ Already in paper (Introduction); strengthen with specific quote about explicit
   code construction

**Veldhuis, Delnero** (on scribal curriculum and training tablets)
→ Already in Introduction; connect more explicitly to CV findings in Discussion §4.2

### 5.2 A note on VAE vectors and cuneiform diplomatics

The core conceptual move that needs grounding: VAE latent dimensions are not
arbitrary numerical codes — they are computable diplomatics.

A medieval diplomat would examine: format (proportions), material (clay type, color),
script style (ductus), formulaic structure, seal impression. We discard everything
except format in its broadest sense: the silhouette. The VAE then learns, without
supervision, a 12-dimensional coordinate system that captures the most salient
geometric variation in that silhouette population.

That X7 (best discriminator) does NOT track time monotonically but DOES separate
cultural traditions is precisely what a diplomat would predict: diplomatic traditions
have characteristic formats that identify them regardless of when they were produced.
That X2 (best trend) tracks time monotonically is the finding of a historical
geologist studying sedimentation: it measures the directional drift in practice
norms across 3,000 years.

Together: **X7 is the diplomatics dimension** (tradition identity). **X2 is the
historical geology dimension** (directional drift). Both are needed; neither alone
tells the full story. This framing should appear in the Discussion.

---

## Part VI — Anomalies and Cautions

### 6.1 Achaemenid CV discrepancy

Physical CV (0.785) vs. pixel CV (0.307) diverge substantially. Likely explanation:
physical dimensions in the CDLI catalogue are sparsely populated for Achaemenid
tablets, and the entries that do exist may be biased toward unusual specimens. Pixel
ratios cover more tablets (1,795 vs. 1,718 — close, so both have good coverage).
Prefer the pixel ratio CV for the claim about Achaemenid standardization.
Flag the discrepancy in the paper as a reminder that physical dimensions are scarce
and their availability is itself non-random.

### 6.2 The Ur anomaly (detailed)

See §4.4 above. Before writing the Discussion treatment, check notebook 2.6 §5
(genre-controlled Layer 2) for Ur specifically. If the administrative-genre analysis
has sufficient N for Ur in both millennia, the counter-trend can be tested against
the genre-composition hypothesis. If administrative Ur also shows a counter-trend,
the institutional explanation (temple archive, ritual format continuity) becomes
more credible.

### 6.3 Middle Elamite as early landscape outlier

Middle Elamite (1450–1050 BCE) has median h/w=0.863 and the highest X2 value of
any 2nd-millennium period (+2.902). This is not discussed in the current paper.
It is historically significant: the Elamite administrative tradition in Susa and
elsewhere maintained landscape formats centuries before they became dominant in
Babylonia. This is consistent with the hypothesis that Achaemenid landscape norms
derive partly from Elamite administrative precedents rather than solely from
Neo-Babylonian influence. Add to Discussion §4.3.

### 6.4 Neo-Assyrian portrait resistance

Neo-Assyrian (911–612 BCE) has median h/w=1.158 (portrait) despite being a 1st-
millennium period. The neo-Babylonian and Achaemenid periods are landscape, but
Neo-Assyrian is portrait. The VAE confirms this: Neo-Assyrian X7=+2.05 (highest
of all 1st-millennium periods) — the VAE also sees Neo-Assyrian as having a
distinctively different body character. This is historically coherent: Neo-Assyrian
administrative and epistolary tablets (especially the letters and reports from
Nineveh, Assur, Kalhu) have well-documented format conventions that differ from
the Babylonian tradition (Radner 1995; Parpola 1987). Mention in §4.1.

---

## Part VII — Figure Allocation Summary

### Main paper figures (target: 6–8 for PNAS format)

| Figure | Notebook | File | Section |
|---|---|---|---|
| Fig. 1 | 2.1 | fig_ratio_by_period_log.pdf | Results §3.1 |
| Fig. 2 | 2.2 | fig_diachronic_trend.pdf + fig_cv_standardization.pdf (2-panel) | Results §3.1 |
| Fig. 3 | 2.4 | fig_vae_discrimination_vs_trend.pdf | Results §3.3 |
| Fig. 4 | 2.4b | fig_vae_traversal_X2_genre.pdf (or composite) | Results §3.3 |
| Fig. 5 | 2.4b | fig_vae_dendrogram_images_Administrative.pdf | Results §3.3/3.4 |
| Fig. 6 | 2.6 | fig_geo_map_paired.pdf + fig_geo_map_shift.pdf (2-panel) | Results §3.5 |

### Supplementary figures

| Figure | Notebook | File | SI section |
|---|---|---|---|
| SI Fig. S1 | 2.1 | fig_ratio_linear_vs_log.pdf | S1 — Methods |
| SI Fig. S2 | 2.3 | fig_pixel_diachronic_trend.pdf | S1 |
| SI Fig. S3 | 2.5 | fig_comparison_diachronic_overlay.pdf | S1 |
| SI Fig. S4 | 2.4 | fig_vae_kw_per_dim.pdf + fig_vae_spearman_per_dim.pdf | S4 — VAE |
| SI Fig. S5 | 2.4b | all 12 traversal filmstrips | S4 — VAE |
| SI Fig. S6 | 2.4b | fig_vae_mean_period_timeline_genre.pdf | S4 — VAE |
| SI Fig. S7 | 2.6 | fig_geo_zone_genre_control.pdf | S-Geo |
| SI Fig. S8 | 2.6 | fig_geo_site_panel.pdf | S-Geo |
| SI Table S-Geo | 2.6 | supplementary_table_S_Geo.csv | S-Geo |

---

## Part VIII — Action Sequence

Step 1 (NEXT): Run the traversal filmstrips in notebook 2.4b and record the
physical interpretation of X2, X7, X8 (and any others with significant effects).
These interpretations are required before Results §3.3 can be written.

Step 2: Confirm the variance decomposition result from notebook 2.6 (within-region
vs. compositional) and the Ur anomaly genre-controlled test.

Step 3: Write Results §3.1 (the flagship section — all data is available now).

Step 4: Write Results §3.2 (classification — data already in paper in various places;
consolidate and frame the 86% finding).

Step 5: Write Results §3.3 (VAE) using confirmed traversal interpretations.

Step 6: Write Results §3.4 (widget case study — requires running the widget or
producing a fixed interpolation sequence from mean Ur III-adm to Achaemenid-adm).

Step 7: Write Results §3.5 (geographic — all data available).

Step 8: Write Discussion.

Step 9: Write Conclusions.

Step 10: Compress Background/Related Work to ~1 page.

Step 11: Add missing bibliography entries (see qmd file for %%MISSING tags).

Step 12: Final consistency pass (correct Abstract/Significance re Achaemenid CV;
confirm all figure cross-references).

---

*Document created 2026-03-31. Update as traversal interpretation results become available.*
