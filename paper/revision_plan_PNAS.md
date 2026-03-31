# Revision Plan: "Shaping History at Scale" → PNAS Submission

**Prepared by:** Claude (computational historian role)
**Date:** 2026-03-29
**Source materials consulted:**
- `paper/Deeplomatics.pdf` — current draft (18 pp., PNAS template, marked DRAFT)
- `paper/corrections.md` — supervisor's correction notes
- `paper/DistantViewing-Assyriology.md` — talk given by Shai Gordin, key framing & conclusions
- Repository notebooks (26 `.ipynb` files) and published datasets/models (Zenodo)
- Chen et al. (2023), *CuneiML*, JOHD — fetched and analyzed 2026-03-29
- Chen et al. (2024), *ML4AL 2024* — fetched and analyzed 2026-03-29

---

## 1. Executive Assessment

The current draft is a technically competent machine-learning paper that has been shoe-horned into a PNAS template. Its principal weaknesses for PNAS publication are:

1. **Structural disorder**: Related Work appears after Discussion (pp. 10–14), inverting conventional logic and burying the paper's intellectual lineage.
2. **Thin humanistic framing**: The core contribution — that tablet *shape* is a systematic, measurable carrier of diplomatic, institutional, and scribal-training history — is asserted but not argued through engagement with the relevant humanities literature.
3. **Underdeveloped flagship finding**: The diachronic shift toward landscape tablets (the "widening" trend) is the most historically novel result, but it is treated as a secondary observation rather than the paper's central empirical argument.
4. **Missing clarifications** that leave the method opaque to both Assyriologists and ML reviewers.
5. **Verbose Related Work** in ML/XAI that overwhelms the humanities substance and is disproportionate to the paper's actual technical novelty.
6. **Absent case study** of the interactive widgets doing real historical work.

The talk script (`DistantViewing-Assyriology.md`) contains a clearer, more confident narrative than the paper itself. The revision should bring the paper's argument into alignment with that narrative while adding the missing humanistic depth.

---

## 2. Proposed New Architecture

The paper must be completely restructured, not merely patched. The following architecture is proposed:

```
Abstract (revised)
Significance Statement (revised)

1. Introduction
   1.1  Diplomatics and the problem of tablet dating
   1.2  Distant viewing applied to cuneiform
   1.3  Research questions and scope

2. Background (= condensed Related Work, moved here)
   2.1  Diplomatics: historiography
   2.2  Tablet shaping as scribal practice
   2.3  Computational approaches to ancient document analysis

3. Dataset and Preprocessing
   3.1  CDLI corpus: scope and limitations
   3.2  Why ratios? (absence of absolute dimensions)
   3.3  Silhouette extraction pipeline
   3.4  Which models see which views (sides vs. fronts)

4. Results
   4.1  Diachronic shape evolution: the "widening" trend  [FLAGSHIP]
   4.2  Height-to-width ratio analysis
   4.3  Period classification models (Decision Tree → CNN → ResNet50)
   4.4  VAE: interpretable feature extraction
   4.5  Hierarchical clustering and diplomatic genealogies
   4.6  Case study: edge contours and the widgets

5. Discussion
   5.1  Shape as institutional signal: standardization scale
   5.2  Achaemenid anomaly and Neo-Babylonian continuity
   5.3  Limitations: what ratios cannot tell us
   5.4  Human + machine partnership

6. Conclusions

Materials and Methods (condensed, technical detail to SI)
Acknowledgements
References
```

**Rationale**: PNAS readers expect to see the intellectual problem motivating the research before the technical solution. Moving Related Work to position 2 (as Background) situates the computational work within its disciplinary context. Placing the diachronic finding first in Results foregrounds the most historically significant result.

---

## 3. Section-by-Section Analysis and Recommendations

### 3.1 Abstract

**Current problems:**
- Leads with cuneiform history rather than with the research contribution.
- Does not name the flagship finding (diachronic widening trend).
- The phrase "our results offer a series of feature vectors" is jargon that communicates nothing to a PNAS reader.
- "longue durée" in a scientific abstract needs justification or removal.

**Recommended revisions:**
- Open with the research question: *Can the physical shape of a writing support encode, and reveal, the institutional history of the civilizations that produced it?*
- State the scale: 94,936 tablet images, 21 historical periods, ~3,300 years.
- Name the three main results in order of historical significance: (1) diachronic evolution from portrait to landscape orientation across three millennia; (2) period-distinctive shape signatures captured by ResNet50 at 71% macro-F1 (vs. 4.8% random baseline) even using only silhouettes; (3) interpretable VAE features that map onto known diplomatic categories.
- Remove or contextualize "longue durée"; this French historiographical term needs a brief anchor.
- Target: ~250 words, three clear beats (problem → method → findings).

### 3.2 Significance Statement

**Current version** is reasonable but too generic. Revise to emphasize:
- The unique crossing of computational vision and ancient Near Eastern diplomatics.
- The specific historical claims: portrait-to-landscape shift, Ur III standardization, Achaemenid continuity from Neo-Babylonian practice.
- Why this matters beyond Assyriology: a model for applying distant viewing to other ancient document corpora.

### 3.3 Introduction (current pp. 1–2, col. 1)

**Current problems:**
- Archaeomagnetic dating detour (ll. 60–131) consumes more space than it merits and is largely irrelevant; it should be cut to a single sentence or moved to a footnote.
- No mention of "distant viewing" as a methodological framework despite this being the talk's organizing concept. This omission leaves the paper without an explicit methodological identity.
- The five-point contributions list on p. 3 is dry and reads like a grant deliverables list. It should be transformed into a narrative argument.
- Missing: any reference to tablet-shaping as part of scribal training — this is the humanistic foundation that explains *why* shapes carry institutional signals.

**Recommended additions:**
- Open with a disciplinary provocation: the study of document format (*diplomatics*) is one of the oldest methods of document analysis, yet its application to cuneiform has remained largely qualitative and based on small corpora. Digital access now makes systematic, quantitative diplomatics possible.
- Introduce "distant viewing" (Arnold & Tilton) explicitly in the introduction, not only implicitly in the methods. This provides the paper with a methodological anchor in digital humanities.
- Add 2–3 sentences on **tablet shaping as a component of scribal training**: the ductus of the tablet — its physical formation — was practiced and standardized as part of scribal education, implying that shape consistency is not accidental but institutionally regulated. Cite relevant literature (e.g., Niek Veldhuis on scribal curriculum, Delnero on Ur III scribal practice).
- Compress the archaeomagnetic dating passage to ≤2 sentences.

### 3.4 Related Work / Background (current pp. 10–14 — MUST BE MOVED)

This section must be moved to before the Results. It is currently placed after Discussion, which is structurally incoherent: the paper presents and interprets results before explaining the intellectual tradition within which those results are situated.

**3.4.1 Tablet Dating sub-section**

Current version briefly mentions Charpin, Cancik-Kirschbaum, and Hackl, but does not engage with the field of **diplomatics as a scholarly tradition**. This is identified as a critical gap in `corrections.md` (point 2a).

Required additions:
- **Historiography of diplomatics in the humanities**: Begin with classical European diplomatics (the study of charters and medieval documents; Mabillon, 17th c.) and its institutionalization in the 19th century. Then trace the application of diplomatic principles to cuneiform — Julius Lewy, Dominique Charpin (*Reading the Past*, 2004; his extensive work on Old Babylonian archive organization), Eva Cancik-Kirschbaum (on Middle Assyrian administrative documents), and Johannes Hackl (cited as ref. [40] in the draft — his *Altorientalische Forschungen* 2021 article on Late Babylonian Tattannu archive is directly relevant and already cited). Add: Lecompte (ref. [44]) and Matthews (ref. [41]) on the materiality of cuneiform. The point to make is that the field has long recognized format as a historical signal — the contribution here is *quantification at scale*.
- Explicitly discuss the significance of **tablet format in scribal education**: Training tablets (practice tablets, *im-gíd-da* and *im-šu* in Sumerian terminology) are the clearest evidence of institutionalized shape norms. Niek Veldhuis's work on Nippur scribal curriculum; Paul Delnero on Ur III practice tablets. The Ur III model's 87% accuracy is partly explicable by this institutional standardization — a point the current paper notes but does not theorize.

**3.4.2 Computational approaches**

The existing ML/XAI sub-sections are **excessively long** (pp. 10–14, ~4 pages of Related Work). For PNAS, which expects the computational methods to serve the historical argument rather than the reverse, this section should be **compressed to approximately 1 page**. Key pruning targets:
- The extended discussion of LIME, SHAP, VAE-LIME, pi-VAE, oi-VAE, NVAE, β-VAE, DDPMs, StyleGAN, etc. (current ll. 1264–1430) should be reduced to a single paragraph noting the XAI landscape and explaining why VAE was chosen over alternatives. The current version reads as a background chapter from a CS thesis.
- Retain the explanation of the Generative Learning Trilemma (useful for justifying VAE choice) but compress.
- Add: Jacobo Myerston's article in the *Journal of Open Humanities Data* (ALP2024) on CDLI data — this is explicitly required by `corrections.md` point 4a. It provides the data-sharing context for the study and reflects community standards for open data in DANES.

### 3.5 Results

**3.5.1 Height-to-Width Ratio Analysis (current pp. 3–4)**

This section is serviceable but requires several additions:

**Add: Why ratios? (corrections.md, point 2d)**
There is currently no explicit statement that *absolute tablet dimensions are not available in the CDLI catalogue for most entries*. This needs to be stated clearly, both as a limitation and as a justification for the ratio approach. A sentence such as: "Because the CDLI catalogue does not systematically record physical dimensions for the majority of entries, we rely on height-to-width ratios extracted from image pixel dimensions, which are relative to camera distance and original image proportions rather than absolute measurements."

**Add: Implications of ratio-only data for interpretation (corrections.md, point 2e)**
The fact that ratios have considerable overlap across periods is acknowledged only implicitly. Make it explicit: "It is worth emphasizing that height-to-width ratios from photographs are imperfect proxies for actual tablet dimensions, and there is substantial distributional overlap between periods (Figure 4). The ability of our models to achieve classification accuracy far above baseline under these conditions is therefore stronger evidence of genuine shape differentiation than the absolute accuracy scores alone might suggest."

**Revise the discussion of Achaemenid period (corrections.md, point 2f)**
The current treatment notes that Achaemenid tablets show more landscape orientation but does not analyze *why* or contextualize it within the scholarly discourse on:
- **Neo-Babylonian continuity**: The Neo-Babylonian → Achaemenid → Hellenistic cluster in the dendrogram reflects well-established scholarly understanding of Late Babylonian institutional continuity under Achaemenid rule. Cite: Jursa on Neo-Babylonian economy and institutions; Waerzeggers on Babylonian temple archives under Achaemenid rule; Hackl (ref. [40]) on Late Babylonian diplomatics.
- **Aramaic influence hypothesis**: The talk (slide [15]) raises the hypothesis that Aramaic writing on parchment may have influenced tablet shape toward landscape format. This is a compelling and novel hypothesis that should appear in the paper, framed as a hypothesis for future investigation with appropriate caution.
- **Scale of standardization**: Per `corrections.md` point 2f, add a quantitative analysis of the *degree* of standardization in tablet shapes across periods, specifically for administrative texts. Create a scale: Ur III (high standardization) → early Old Babylonian (low standardization; competing city-states, diverse practices) → Achaemenid (moderate-high standardization in landscape format). This can be operationalized using the coefficient of variation (CV) or interquartile range of height/width ratios per period in administrative genre.

**3.5.2 Tablet Period Classification Models**

**Add: Clarification on which models use tablet sides (corrections.md, point 2c)**
The paper currently does not clearly distinguish between:
- Images showing the **front face only** (obverse or reverse)
- Images showing **multiple faces on a single canvas** (obverse, reverse, and/or sides composite views)
- The **largest connected component** extraction (which removes side views)

This is a methodological ambiguity that a reviewer will certainly flag. Add a clear paragraph explaining: (a) that the CDLI images vary significantly in what they show; (b) that the binary masking and largest-component extraction was designed to address this; (c) which specific experimental conditions (grayscale vs. masked) are affected by this issue; and (d) that images photographed with multiple views on a single canvas constitute a known confound in the Administrative genre clustering (currently acknowledged in one sentence on p. 9 but not connected to the methods section where it belongs).

**Strengthen the 86% finding framing**
The talk frames the key finding as "Silhouettes retain ~86% of classification information (61%/71%)" — this is a striking result that the paper buries. In the revised paper, this should be a named, highlighted finding: shape alone accounts for 86% of the historical signal detectable from full grayscale images. Verify the calculation and present it as a named result with statistical framing.

**3.5.3 VAE Results**

The VAE results are well-presented but the paper does not adequately explain the gap between VAE+XGBoost (43% macro-F1) and ResNet50 (71% macro-F1). This needs a brief honest discussion: VAEs optimize for reconstruction fidelity and latent space regularity rather than discriminative accuracy, so lower classification performance is expected. The value of VAEs is interpretability and generativity, not classification performance. This distinction is implied but not stated clearly.

**3.5.4 New section required: Case Study with the Widgets (corrections.md, point 3)**

The current paper describes the two interactive widgets but does not demonstrate their use in actual historical argumentation. The corrections note specifically requests: "a case study of using the widgets and how they can aid/complement historical argumentation, maybe something that talks about edges shape?"

Recommended case study structure (new subsection ~500 words + 1 figure):
- Choose a specific historical question: e.g., "What distinguishes the typical Late Babylonian (Neo-Babylonian + Achaemenid) administrative tablet silhouette from its Ur III counterpart?"
- Use the **feature explorer widget** to isolate the VAE dimensions most responsible for this distinction (the talk identifies Feature 4 [aspect ratio] and Feature 7 [top/bottom thickness]).
- Use the **interpolation widget** to visualize the morphological path between the mean Ur III administrative tablet and the mean Achaemenid administrative tablet.
- **Interpret the edge shape**: If Feature 7 controls top/bottom tablet thickness and this dimension separates periods, what does that mean for our understanding of how different cultures held and inscribed their tablets? The rounded rectangle of Ur III tablets vs. the squatter landscape of Achaemenid tablets may reflect different archival and handling practices.
- This case study demonstrates that the tools support historical inference, not just pattern recognition — a crucial argument for PNAS which values interdisciplinary significance.

### 3.6 Discussion (current pp. 6–9)

**Current problems:**
- The discussion is largely a restatement of results.
- The most historically significant finding — the diachronic widening trend — is discussed in one paragraph.
- The discussion of Ur III standardization as evidence of "state control" (hinted at in corrections point 2f and the talk) is not developed.
- Missing: a clear statement of what this methodology cannot do.

**Recommended additions:**

**3.6.1 State control and standardization as a diplomatic phenomenon**
The Ur III state (2,110–2,003 BCE) produced the most standardized administrative tablets in Mesopotamian history. The model's 87% accuracy (or 84–92% depending on model) for Ur III is not just a technical success; it is computational evidence for a well-documented historical phenomenon: centralized scribal training and administrative standardization under the Third Dynasty of Ur. The paper should make this connection explicitly, citing the archaeological and textual evidence for Ur III scribal schools (e-dub-ba-a) and standardized administrative practices (Steinkeller on Ur III administration; Englund on Ur III grain accounting).

Extend this to a comparative argument: build the "standardization scale" requested in corrections (point 2f). Which historical periods produced the most homogeneous tablet shapes for administrative texts? Quantify this with the IQR or CV of height/width ratios per period (administrative genre only). The expected order from most to least standardized: Ur III > Hellenistic (Seleucid) > Achaemenid > Neo-Assyrian (letter genre specifically) > early Old Babylonian. This scale is a novel empirical contribution that can anchor the Discussion.

**3.6.2 Achaemenid anomaly: Neo-Babylonian continuity vs. external influences**
Expand the discussion of the Achaemenid period's placement in the VAE dendrogram (Neo-Babylonian → Achaemenid → Hellenistic cluster). Currently one sentence. Needed:
- Acknowledge what scholarship says about institutional continuity of Babylonian temple and administrative practices under Achaemenid rule (Waerzeggers, Jursa, Hackl).
- Raise, with appropriate scholarly caution, the Aramaic influence hypothesis: if Aramaic scribes writing on parchment in a landscape format co-existed with cuneiform scribes in Achaemenid Babylonia, could this have influenced the format norms of late cuneiform administrative tablets? This is framed as a hypothesis, not a conclusion.
- Compare to Middle Elamite (1,450–1,050 BCE) influence: the talk mentions this as a possible influence on Achaemenid practices through Achaemenid-Elamite administrative traditions. Middle Elamite tablets from Persepolis are a relevant comparandum.

**3.6.3 Limitations: honest accounting**
Required per corrections (points 2c, 2d, 2e) and consistent with PNAS standards:
- Ratios are proxies; absolute dimensions would resolve much remaining ambiguity.
- The CDLI corpus is non-random: it reflects excavation histories, museum collection policies, and digitization priorities — the four dominant periods (Ur III, Neo-Assyrian, Old Babylonian, Middle Babylonian = 63% of data) are over-represented because of historical accidents of discovery and acquisition, not because they were historically more tablet-rich.
- Image quality variation and multi-view composite images introduce known confounds.
- 2D silhouettes discard information about tablet thickness, surface curvature, and edge profiles that would potentially improve classification.
- The models classify into modern scholarly period categories, which are themselves periodization conventions with fuzzy boundaries (Early Old Babylonian vs. Old Babylonian confusion in the confusion matrix is partly a reflection of scholarly periodization conventions, not just model error).

**3.6.4 Human + machine partnership**
The talk makes a compelling point (slide [26]) that combined human + model predictions outperform either alone. If this experiment was done, include the data and discuss its implications for how Assyriologists should use these tools. If not done, this is a recommended new analysis (see Section 6).

### 3.7 Conclusions

The current conclusion is adequate but too generic. Revise to:
1. State the flagship empirical finding (diachronic widening trend) in a memorable sentence.
2. State the methodological contribution: distant viewing applied to diplomatics at scale — making implicit interpretive frameworks explicit and reproducible.
3. Name specific future applications: (a) archive-based shape analysis (the talk mentions this as ongoing work by Gordin); (b) preliminary tablet dating tool accessible to non-specialists; (c) integration with 3D photogrammetry data (acknowledged limitation that becomes a research agenda).
4. End with the broader significance: this methodology is transferable to any corpus of inscribed portable objects — seals, sealings, bullae, ostraca, papyri — wherever shape carries historical signal.

---

## 4. Missing Content: Required New Additions

### 4.1 Historiography of Diplomatics (High Priority)

Write a 400–600 word subsection (to appear in Background/Related Work section) that traces:
1. Classical diplomatics: Mabillon's *De Re Diplomatica* (1681) as the founding text; the 19th-century institutionalization of diplomatic analysis (Bresslau, Sickel) for European medieval documents.
2. Application to Near Eastern documents: the concept of "tablet format" in Assyriology, from early systematic observations (Pedersén on archive studies) to modern diplomatic analysis. Key scholars: Charpin, Cancik-Kirschbaum, Lecompte [44], Matthews [41], Hackl [40], Radner [35].
3. The gap: existing diplomatic analysis is qualitative, small-corpus, and expert-dependent. Computational diplomatics at scale is the missing piece.
4. Transition to computational method: "distant viewing" (Arnold & Tilton, 2019) as the framework for making implicit diplomatic criteria explicit and computational.

### 4.2 Tablet Shaping as Scribal Training (Medium Priority)

Write a 200–300 word passage explaining:
- In cuneiform scribal education, the physical preparation of the clay tablet was itself a practiced skill, not incidental to writing. The size, shape, and clay quality of tablets were not random but reflected genre conventions taught in scribal schools.
- Evidence from Nippur scribal curriculum (Veldhuis) shows that different text genres systematically used different tablet formats (lenticular practice tablets vs. multi-column literary tablets vs. small administrative tablets).
- This means shape consistency within a period is *partly a product of scribal education* — the model is detecting, among other signals, the output of standardized training practices.
- This is especially significant for Ur III, where the scale of administrative production implied an organized scribal training system, and for Neo-Assyrian letter archives, where the distinctive small fragment shape reflects a specific genre convention.

### 4.3 Standardization Scale Analysis (Medium Priority — New Analysis)

**Notebook work required**: Using the existing height/width ratio data (notebook `2.1 EDA - height-weight ratio of tablets.ipynb`), compute the **coefficient of variation (CV = std/mean)** of height/width ratios for administrative tablets per period. Plot as a bar chart ordered by CV (low = high standardization). This provides a single, memorable visualization of "state control visible in tablet shapes" that the corrections (point 2f) request.

Expected result: Ur III will have the lowest CV (high standardization), early Bronze Age periods and early Old Babylonian will have high CV (low standardization), Achaemenid will be moderate. This is a novel quantitative contribution supporting the Discussion.

### 4.4 Widget Case Study (Required per corrections.md, point 3)

As described in Section 3.5.4 above. This requires:
- Running the feature explorer for Ur III administrative vs. Achaemenid administrative tablets
- Generating the interpolation path
- Writing 400–500 words of historical interpretation focused on edge shape and what the VAE dimension controlling top/bottom thickness (Feature 7, from the talk) reveals about tablet handling practices
- One new figure combining feature explorer output and interpolation widget output

### 4.5 Citation: Jacobo Myerston ALP2024 (Required per corrections.md, point 4a)

Add the citation to Jacobo Myerston's article in the *Journal of Open Humanities Data* (ALP2024 issue) using CDLI data. This should appear in:
- The Data Acquisition sub-section of Materials and Methods (when discussing CDLI as a data source and community standards for open data)
- The Related Work / Background section (when situating the study within DANES community practices)

---

## 5. Content to Remove or Substantially Reduce

### 5.1 XAI Background (current ll. 1264–1430, ~4 pages)

**Target: reduce by ~70%**, retaining only:
- One paragraph on the general importance of interpretability in ML applied to humanities (LIME, SHAP mentioned by name only)
- Two paragraphs on VAE interpretability specifically, retaining the Generative Learning Trilemma explanation (it does useful work justifying the VAE choice) but removing the extended discussion of specific disentanglement models (pi-VAE, oi-VAE, NVAE, β-VAE variants) — these belong in SI at most.
- One paragraph on DDPMs and why they were not chosen (the Trilemma).

**Rationale**: PNAS reviewers from humanities backgrounds will be alienated by 4 pages of ML background that is not directly relevant to the paper's findings. Reviewers from ML backgrounds will find this survey too elementary to add value. The section currently serves neither audience.

### 5.2 Archaeomagnetic Dating Detour (current ll. 60–131)

**Target: reduce to ≤3 sentences**. The archaeomagnetic approach is mentioned as context for how novel absolute dating methods are being developed. This is marginally relevant and currently takes 70 lines of the Introduction. Compress to: "Recent advances in physical dating methods, including archaeomagnetic analysis of baked clay artifacts [cite], offer complementary absolute chronological tools, though their application remains limited to baked materials and specific regional datasets."

### 5.3 Verbose Methods Detail

Several methodological passages can move to SI:
- The detailed CNN architecture specification (current ll. 1683–1695)
- The detailed hyperparameter search protocols (footnotes §, ¶, †, ‡)
- The full VAE architecture specification (current ll. 1741–1763)

These belong in the SI Methods appendix, consistent with PNAS norms.

### 5.4 Redundant Prose (corrections.md, point 4b)

Run a targeted pass on the Discussion section to remove restatements of results that are already presented in Results. The current Discussion section substantially repeats what Figure 4, Figure 9, Figure 10, and Table 1 already show. Discussion should interpret, contextualize, and argue — not re-describe.

---

## 6. Recommended New Analyses

These analyses are feasible with the existing data and notebooks and would strengthen the paper's contribution:

### 6.1 Standardization Scale (CV by Period, Administrative Genre)
- **Notebook**: `2.1 EDA - height-weight ratio of tablets.ipynb`
- **Analysis**: Compute CV of H/W ratio per period for administrative texts only
- **Output**: One bar chart figure
- **Contribution**: First quantitative scale of administrative tablet standardization over 3 millennia; supports the discussion of state control and institutional norms

### 6.2 Achaemenid vs. Neo-Babylonian vs. Middle Elamite Shape Comparison
- **Notebook**: `11. analyze_VAE.ipynb` and `11.1 Heirarchical clustering of tablets.ipynb`
- **Analysis**: Focused pairwise comparison of VAE bottleneck vectors for Neo-Babylonian, Achaemenid, and Middle Elamite administrative and legal texts
- **Output**: Supplementary figure; 200 words in Discussion
- **Contribution**: Quantitative support for the hypothesis of Neo-Babylonian → Achaemenid shape continuity and possible Middle Elamite influence

### 6.3 Human vs. Model vs. Combined Accuracy (if data available from the talk exercise)
- The talk (slide [26]) suggests human participants + model predictions outperformed either alone
- If quantitative data from the audience experiment exists, add as a supplementary analysis
- **Contribution**: Directly supports the human+machine partnership framing; compelling for PNAS readers

### 6.4 Statistical Significance of the Diachronic Trend
- **Notebook**: `2.1 EDA - height-weight ratio of tablets.ipynb`
- **Analysis**: Fit a regression of median H/W ratio on time (BCE), test for trend significance; or use Spearman rank correlation of period-median H/W ratio with chronological order
- **Output**: One statistical test result (p-value, effect size), added to the Results section
- **Contribution**: The diachronic "widening" trend is currently described as visible in plots; it needs a formal statistical test for PNAS standards

### 6.5 Distribution Shift Evaluation (OOD Test by Museum Collection) — *Motivated by Chen et al. 2024*
- **Notebook**: New or adapted from `8.1 test ResNet50 period classifier - greyscale tablets.ipynb` and `9.1 test ResNet50 period classifier - masked tablets.ipynb`
- **Analysis**: Stratify the test set by museum/collection of origin (available in CDLI metadata). Report macro F1 separately for in-collection vs. held-out-collection splits. Compare silhouette (masked) vs. grayscale degradation across splits. This directly answers whether the silhouette approach is more robust to collection-specific photographic confounds.
- **Output**: A 2×2 comparison table (grayscale vs. masked × in-distribution vs. OOD F1), plus 1–2 sentences in Discussion noting that Chen et al. 2024 identify this as the key methodological risk in CDLI-based ML dating.
- **Contribution**: Provides an honest evaluation of cross-collection generalizability; simultaneously positions the silhouette approach as a partial solution to the confound problem Chen et al. identify; directly addresses what will certainly be a referee question given the visibility of Chen et al. 2024 in the field.
- **Expected finding**: Silhouette (masked) models should degrade less under OOD shift than grayscale models, because binary masks strip away the photographic texture artifacts (scanning hardware signatures, lighting conditions, color profiles) that differ systematically between museum collections.

---

## 7. Literature Revisions

### 7.1 Required Additions

| Citation | Where to add | Why |
|---|---|---|
| Chen, Agarwal, Berg-Kirkpatrick & Myerston (2023), *CuneiML*, JOHD 9(1), p. 30. DOI: 10.5334/johd.151 | Data Acquisition; Background §2.3 | CDLI data pipeline precedent; scale reference point; ML benchmark for period classification |
| Chen, Tian, Weng, Berg-Kirkpatrick & Myerston (2024), *ML4AL 2024*, pp. 30–41 | Background §2.3; Limitations; Discussion | Distribution shift analysis; OOD generalization problem; silhouette robustness argument |
| Niek Veldhuis, *Religion, Learning and Scholarship in the Nippur Scribal School* (or equivalent) | Background: scribal training | Tablet shaping as scribal education |
| Paul Delnero on Ur III practice tablets | Background: scribal training | Standardized formats in scribal training |
| Michael Jursa on Neo-Babylonian economy | Discussion: Achaemenid analysis | Neo-Babylonian institutional continuity |
| Caroline Waerzeggers on Babylonian archives under Achaemenid rule | Discussion: Achaemenid analysis | Achaemenid continuity from Neo-Babylonian |
| Taylor Arnold & Lauren Tilton, *Distant Viewing* (2023 book or 2019 article) | Introduction | "Distant viewing" methodological framework |
| Dominique Charpin, *Reading the Past* / *Writing, Law and Kingship* | Background: diplomatics | Foundational diplomatics scholarship |

> **DOI correction**: The CuneiML citation as supplied has an incorrect DOI (`johd.176`). The correct DOI, verified by retrieval, is `10.5334/johd.151`. Use the corrected DOI in all references.

### 7.2 Detailed Analysis of the Two New Key Citations

Both papers come from the same research group (Berg-Kirkpatrick / Myerston at UCSD), work directly on CDLI data, and represent the most important recent computational prior work for the Shaping History paper. They must be engaged with carefully, not just cited in passing.

---

#### 7.2.1 Chen, Agarwal, Berg-Kirkpatrick & Myerston (2023) — *CuneiML*

**Full reference:** Chen, D., Agarwal, A., Berg-Kirkpatrick, T. and Myerston, J. (2023) 'CuneiML: A Cuneiform Dataset for Machine Learning', *Journal of Open Humanities Data*, 9(1), p. 30. DOI: **10.5334/johd.151**.
*(Note: the DOI `johd.176` in the original citation is incorrect; verified correct DOI is `johd.151`.)*
Code and data: https://github.com/taineleau/CuneiML | https://doi.org/10.5281/zenodo.8307503

**What the paper does:**
CuneiML creates the first large-scale, ML-ready, multi-modal cuneiform dataset (38,947 tablets) from CDLI, combining high-resolution 2D photographs with major-face cutouts (extracted using a consensus of three segmentation algorithms), Latin transliterations, cuneiform Unicode transcriptions, and structured metadata (period, genre, provenance). The dataset is 20× larger than the previous benchmark (HeiCuBeDa, 1,977 tablets). Baseline classification experiments using ResNet-101 on images and LSTM on text show period classification accuracy up to 97.66% — a figure that Paper 2 later reveals to be heavily inflated by distribution shift.

**Key performance data (baseline classifiers):**

| Task | ResNet-101 (images) | LSTM (Unicode) | LSTM (transliteration) |
|---|---|---|---|
| Time period (14 classes) | 97.66% acc | 90.50% | 87.17% |
| Provenance (25 classes) | 85.72% | 61.71% | 68.60% |
| Genre (12 classes) | 89.00% | 81.50% | 86.21% |

**Relationship to Shaping History:**
- Same primary source (CDLI), so both papers share the same dataset limitations (label imbalance, possible circular reasoning in assigned dates, variable image quality).
- Shaping History uses ~94,936 images — a larger extraction than CuneiML's 38,947 — because it does not require transliteration data and applies different filtering criteria.
- Shaping History's ResNet50 achieves 71% macro-F1 (grayscale) and 61% (masked) versus CuneiML's 97.66% accuracy. This difference is *not* a failure of Shaping History: (a) macro-F1 is more stringent than accuracy on imbalanced datasets; (b) Shaping History uses 21 period classes versus CuneiML's 14; (c) CuneiML's figures are heavily inflated by in-distribution leakage (see Paper 2). The Shaping History paper should make these distinctions explicit when citing CuneiML.
- CuneiML's preprocessing pipeline (major-face extraction via consensus segmentation) parallels Shaping History's binary mask + largest-component approach. Cite CuneiML when describing image preprocessing.

**Where to cite:**
1. **Background §2.3 (ML approaches):** Introduce CuneiML as the principal benchmark dataset for the field; describe its scale and multimodal nature; note its period classification baseline; then distinguish Shaping History's silhouette-only, interpretability-focused approach.
2. **Data Acquisition (Methods):** Reference CuneiML's preprocessing pipeline as a methodological precedent for CDLI face extraction.
3. **Results — classification performance table:** Add a comparison row for CuneiML baseline, with an explanatory footnote about why the metrics are not directly comparable (macro-F1 vs. accuracy; 21 vs. 14 classes; i.i.d. vs. potential OOD leakage).

**Suggested in-text language:**
> "Chen et al. (2023) introduced CuneiML, a curated multi-modal dataset of 38,947 CDLI tablets with paired photographs, transliterations, and metadata, establishing baseline period classification performance of up to 97.66% accuracy using image and text features combined. Our study extends this work both in scale (94,936 tablets, 21 period classes) and in methodological focus: by restricting analysis to binary silhouettes, we isolate shape as a pure diplomatic signal, independent of inscription content, writing style, or scanning apparatus — features that, as Chen et al. (2024) demonstrate, can systematically inflate classification performance."

---

#### 7.2.2 Chen, Tian, Weng, Berg-Kirkpatrick & Myerston (2024) — *ML4AL 2024*

**Full reference:** Chen, D., Tian, J., Weng, Y., Berg-Kirkpatrick, T. and Myerston, J. (2024) 'Classification of Paleographic Artifacts at Scale: Mitigating Confounds and Distribution Shift in Cuneiform Tablet Dating', in *Proceedings of the 1st Workshop on Machine Learning for Ancient Languages (ML4AL 2024)*, Bangkok, Thailand and online. Association for Computational Linguistics, pp. 30–41. https://aclanthology.org/2024.ml4al-1.4

**What the paper does:**
This paper is the most important methodological warning for the Shaping History project. It demonstrates that standard i.i.d. train/test splits on CDLI data are severely contaminated by two compounding problems:
1. **Label shift:** Museum collections are not temporally random — each museum tends to hold tablets from one or two periods. A random split therefore places tablets from the same museum in both training and test sets, leaking collection identity as a period predictor.
2. **Covariate shift (photographic confound):** Different museums use different scanning hardware, lighting, and backgrounds. Models can learn to identify the *museum* from image texture — and since museum identity predicts period, this inflates apparent classification accuracy without the model having learned anything about temporal shape.

The paper constructs three carefully designed test splits:
- **test1 (OOD):** Entire museum collections are held out; no tablet from held-out collections seen in training. This is the honest evaluation of real-world generalizability.
- **test2 (label-shift ID):** Same period distribution as test1, but drawn from seen collections.
- **test3 (in-distribution ID):** Standard i.i.d. split.

**Key performance results:**

| Model / Features | test1 OOD macro-F1 | test3 ID macro-F1 | Drop |
|---|---|---|---|
| ResNet-50, raw image | 28.46 | 78.73 | −64% |
| ResNet-50, major cutout | 34.82 | 80.60 | −54% |
| ResNet-50 + CORAL, major cutout | **41.06** | 48.61 | −15% |
| char-LSTM, transliteration | 16.14 | 84.42 | −81% |
| Naive Bayes, provenance alone | 39.48 | 61.15 | −36% |

**Sobering implication:** The headline figures from CuneiML (97.66%) and from Shaping History (71% / 61%) should be understood as in-distribution performance, not generalizable accuracy. The honest OOD figure for image-based models on CDLI data is approximately 30–40% macro-F1 before mitigation — similar in order of magnitude to Shaping History's masked-image ResNet50.

**Why this matters for Shaping History — three distinct implications:**

1. **The confound problem directly applies.** Shaping History uses a standard i.i.d. split (80/10/10) without explicitly controlling for museum collection. Its 71%/61% figures are therefore subject to the same label shift and covariate shift identified by Chen et al. The paper must acknowledge this, discuss whether the silhouette approach partially mitigates it, and add analysis 6.5 (OOD test by collection).

2. **Silhouette approach has a structural advantage.** Binary masks remove all photographic texture — the precise confound that inflates image-based results. Chen et al.'s finding that raw images perform *worse* than cutouts under OOD shift (28.46% vs. 34.82%) shows that removing photographic artifacts helps. Binary masks take this logic to its extreme. The Shaping History paper can argue: *our approach is by design more resistant to the covariate shift Chen et al. identify, because we discard the very features (photographic appearance) that drive this confound.* This converts a limitation (ignoring image content) into a methodological virtue.

3. **The circular reasoning concern about CDLI dates applies here too.** Chen et al. flag that date assignments in CDLI may encode implicit scholarly assumptions, biasing ground-truth labels. The Shaping History paper already mentions this concern ("assumptions regarding dates recorded in existing datasets may be biased or based on circular reasoning," l. 1247–1249), but Chen et al. 2024 provide the most systematic empirical treatment of this risk and should be co-cited there.

**Where to cite:**
1. **Background §2.3:** Introduce Chen et al. 2024 as the paper that establishes OOD generalization as the central methodological challenge in CDLI-based ML dating; describe their three-split evaluation design.
2. **Methods — Evaluation Metrics:** When defending the choice of macro-F1, note that Chen et al. 2024 establish macro-F1 as the appropriate metric for severely imbalanced CDLI data.
3. **Results — discussion of classification performance:** Note that in-distribution figures should be interpreted in light of the distribution shift problem; refer readers to analysis 6.5 for the OOD evaluation.
4. **Discussion — Limitations:** This is the most critical placement. Add an explicit paragraph:

> "A fundamental challenge in CDLI-based machine learning — systematically analyzed by Chen et al. (2024) — is the conflation of museum collection identity with temporal period labels, which can cause models to learn photographic artifacts rather than genuine temporal features. Our binary silhouette approach partially addresses the covariate dimension of this problem, since black-and-white masks remove scanning hardware signatures by construction. We nonetheless evaluate our models on a held-out collection split (see SI Analysis S[X]) and find that [results from analysis 6.5]. Full mitigation of this problem, potentially through methods such as CORAL domain adaptation, remains an important direction for future work."

**Suggested in-text comparative statement for Results:**
> "Chen et al. (2024) demonstrate that CDLI-based image classifiers typically achieve 28–35% macro-F1 on held-out museum collections (out-of-distribution), compared to 78–80% on in-distribution splits — a 54–64% degradation driven by photographic confounds. Our masked-image ResNet50, which operates on binary silhouettes stripped of photographic content, achieves [OOD F1 from analysis 6.5], consistent with the prediction that shape-based features are more robust to this confound than texture-based features."

---

#### 7.2.3 Positioning the Two Papers Together in the Revised Narrative

The Berg-Kirkpatrick/Myerston group's two papers bracket the Shaping History paper:
- CuneiML (2023) establishes the dataset infrastructure and baseline performance.
- ML4AL (2024) reveals that those baselines are overestimates and defines the OOD generalization problem.
- Shaping History addresses a complementary question — *what does shape alone tell us, and can shape be made interpretable?* — that neither CuneiML nor ML4AL attempts.

A concise comparative table should appear in the Background section of the revised paper:

| Feature | CuneiML (2023) | Chen et al. (2024) | **Shaping History** |
|---|---|---|---|
| N tablets | 38,947 | 38,937 | **94,936** |
| Signal used | Image + text | Image + text | **Silhouette only** |
| Periods | 14 classes | 14 classes | **21 classes** |
| Best in-dist. F1 | ~97% acc (inflated) | 41% macro-F1 (OOD) | **71% macro-F1** |
| OOD evaluation | No | Yes (central) | **Proposed (analysis 6.5)** |
| Interpretability | None | None | **VAE bottleneck** |
| Historical analysis | None | None | **Diplomatics, diachronic trends** |

This table makes the Shaping History paper's distinctive contribution clear: largest scale, shape-only signal, interpretable model, and humanistic analysis.

---

### 7.3 Citations Requiring Verification

The following in-text citations use `[==CITE==]` placeholders (l. 364) and must be resolved:
- The citation for Aramaic scribes and parchment practice modeled after Aramaic scribal work — identify the specific reference (possibly Lemaire on Aramaic scribes in Babylonia, or Joannès on administration bilingue).

### 7.3 Citation Style Notes

- Reference [35] (Radner on Neo-Assyrian texts) is cited at l. 358 in the context of consistent tablet format within text types. Expand this discussion: Radner's argument that Neo-Assyrian letter format is one of the most consistent in the corpus directly supports the model's 95% accuracy for Neo-Assyrian.
- References [45, 46] (Parisotto et al. and Cardarelli et al. on ceramic shape analysis with VAEs) are used as methodological precedents. Expand slightly: these are the closest methodological parallels, and explicitly comparing this study to the ceramic morphometrics tradition will help PNAS reviewers from archaeology situate the contribution.

---

## 8. PNAS-Specific Formatting and Submission Requirements

### 8.1 Structural requirements
- **Main text**: PNAS target for research articles is typically 6 pages when formatted. The current 18-page draft (which includes 4 pages of XAI background and extensive SI-appropriate methods detail) needs substantial compression. After the cuts described in Section 5, and with SI for extended methods and supplementary figures, the main text should target ~8–10 PNAS-formatted pages.
- **SI Appendix**: All extended methods (CNN architecture, VAE architecture, hyperparameter search protocols, full confusion matrices beyond what's in main text, genre-specific dendrograms S1–S3) should be explicitly labeled and submitted as SI. The current draft references "supporting information published on the PNAS website" but the SI is not structured as a proper appendix.
- **Figures**: Current 15 main-text figures are too many for PNAS main text. Recommended: 7–8 main text figures, remainder as SI.
  - Keep in main text: Fig. 2 (sample count); Fig. 4 (H/W ratio per period — flagship); Fig. 5 (per millennium); the new standardization CV figure; the dendrogram (Fig. 9 or Fig. 10, choose one representative); Fig. 7 or confusion matrix; Fig. 3 (widgets — with new case study).
  - Move to SI: Fig. 6 (Pearson correlation), Fig. 8 (VAE confusion matrix), Fig. 11 (VAE entry X7 boxplot), Fig. 12 (VAE dendrogram), Fig. 13 (preprocessing examples), Fig. 14 (component extraction), Fig. 15 (masking pipeline).

### 8.2 Author requirements
- **ORCID**: The current author note instructs "Individual authors must link their ORCID account to their PNAS account." Ensure all three authors (Epshtain, Fire, Gordin) have active ORCID IDs registered with PNAS Central before submission.
- **Affiliation addresses**: Currently incomplete (ZIP/postal codes missing per the template instruction on ll. 1872–1876). Complete all author affiliations with full postal addresses.
- **Author contributions**: PNAS requires a formal author contributions statement. Not present in current draft — add before submission.

### 8.3 Data and code availability
The current Code and Data Availability statement (ll. 1863–1870) is adequate but should be updated to:
- Include the specific Zenodo DOIs (datasets: `10.5281/zenodo.12787745`; models: `10.5281/zenodo.11668219`) directly in the statement, not only via hyperlinks (hyperlinks are not stable in print).
- Confirm that Huggingface links for the interactive widgets are also cited.
- Add: "Notebooks for reproducing all analyses are available at [GitHub URL]."

### 8.4 Significance Statement
Already present (good). Revise per Section 3.2 above.

---

## 9. Prioritized Action List

The following is ordered from highest impact / most blocking to lower priority:

**Phase 1 — Structural (must happen first)**
1. [ ] Restructure document architecture: move Related Work before Results, rename to Background
2. [ ] Write new Background sub-section on diplomatics historiography (~500 words)
3. [ ] Write new passage on tablet shaping as scribal training (~250 words)
4. [ ] Compress XAI background by ~70%, move cut material to SI
5. [ ] Compress archaeomagnetic dating passage to ≤3 sentences

**Phase 2 — New analyses (informs new content)**
6. [ ] Run CV analysis (standardization scale) in notebook 2.1; generate figure
7. [ ] Run formal statistical test on diachronic widening trend (Spearman or regression)
8. [ ] Run pairwise VAE comparison: Neo-Babylonian vs. Achaemenid vs. Middle Elamite (admin and legal)
9. [ ] Develop widget case study: Ur III → Achaemenid morphological path with edge shape focus

**Phase 3 — Rewriting**
10. [ ] Revise Abstract (target: 250 words, three beats)
11. [ ] Revise Significance Statement
12. [ ] Revise Introduction: integrate distant viewing framework, scribal training passage
13. [ ] Revise Results: add clarification on silhouette sides (3.5.2), add ratio caveats (3.5.1), add Achaemenid analysis (3.5.1), add widget case study (3.5.4)
14. [ ] Revise Discussion: add standardization scale argument, expand Achaemenid section, add limitations section, expand diachronic finding
15. [ ] Revise Conclusions

**Phase 4 — Literature and formatting**
16. [ ] Add Chen et al. (2023) *CuneiML* (DOI: 10.5334/johd.151 — **not** johd.176) — Background §2.3, Data Acquisition, Results table
17. [ ] Add Chen et al. (2024) *ML4AL* — Background §2.3, Methods (evaluation metrics), Results, Limitations
18. [ ] Add comparative table (CuneiML / ML4AL / Shaping History) to Background §2.3
19. [ ] Add Veldhuis, Delnero, Jursa, Waerzeggers, Arnold & Tilton citations
20. [ ] Resolve `[==CITE==]` placeholder(s)
19. [ ] Restructure SI appendix
20. [ ] Reduce main-text figures to 7–8, move remainder to SI
21. [ ] Complete author information (ORCIDs, postal addresses, author contributions)
22. [ ] Update Code and Data Availability with Zenodo DOIs

---

## 10. Framing Note for the Revised Paper

The revised paper's core argument, distilled from the talk and the corrections, should be:

> **Cuneiform tablet shapes are not arbitrary. They are the material residue of institutional, educational, and diplomatic norms that were socially enforced and changed over time. For the first time, we can measure these norms at scale — across 94,936 tablets and 3,300 years — and read from them a quantitative history of scribal institutions. The most significant finding is a systematic three-millennium shift from portrait to landscape tablet orientation, whose pace correlates with documented changes in state organization, scribal training, and administrative technology. This is computational diplomatics.**

Every section of the revised paper should serve this argument. Material that does not serve it — however technically interesting — belongs in SI or in a separate paper.

---

*End of revision plan. Total estimated new writing: ~3,000–4,000 words (historiography, scribal training, case study, expanded Achaemenid discussion, limitations). Total estimated cuts: ~3,500–4,000 words (XAI background, archaeomagnetic detour, redundant discussion). New analyses: 4–5 targeted computational tasks, all feasible with existing notebooks and data.*

---

## 11. Quarto/PNAS Template Specification for the Revised Manuscript

The revised paper should be authored in **Quarto Markdown (`.qmd`)** using the [`christopherkenny/pnas`](https://github.com/christopherkenny/pnas) extension. This section documents everything needed to write the full manuscript file from scratch.

### 11.1 Installation

```bash
# Scaffold a new project directory (recommended):
quarto use template christopherkenny/pnas

# Or add to the existing repo directory:
quarto add christopherkenny/pnas
```

**Requirements:** Quarto ≥ 1.3.0; a working LaTeX distribution (TinyTeX sufficient). Render with:

```bash
quarto render shaping_history_revised.qmd
```

The extension produces **PDF only** — there is no HTML output mode.

---

### 11.2 Complete YAML Front Matter for This Paper

The following is the complete, ready-to-use YAML header for the revised Shaping History manuscript. Fill in ORCIDs and postal codes before submission.

```yaml
---
title: "Shaping History at Scale: Computational Diplomatics and the Diachronic
  Evolution of Cuneiform Tablet Morphology over Three Millennia"

format:
  pnas-pdf: default

author:
  - name: Danielle Kapon Epshtain
    affiliations:
      - name: Ben-Gurion University of the Negev
        id: a
        department: Department of Software and Information Systems Engineering
        city: Be'er Sheva
        postal-code: "8410501"
        country: Israel
    orcid: 0000-0000-0000-0000   # REPLACE with actual ORCID
    attributes:
      equal-contributor: true

  - name: Michael Fire
    affiliations:
      - ref: a
    orcid: 0000-0000-0000-0000   # REPLACE with actual ORCID
    attributes:
      equal-contributor: true

  - name: Shai Gordin
    affiliations:
      - name: Ariel University
        id: b
        department: Department of Land of Israel Studies and Archaeology
        city: Ariel
        postal-code: "40700"
        country: Israel
      - name: Open University of Israel
        id: c
        department: Digital Humanities and Social Sciences Hub
        city: Ra'anana
        postal-code: "4353701"
        country: Israel
    email: shaigo@ariel.ac.il
    orcid: 0000-0000-0000-0000   # REPLACE with actual ORCID
    attributes:
      corresponding: true

abstract: |
  [REVISE — target 250 words, three beats: problem → method → findings.
  Open with the research question; name the diachronic widening finding;
  state 71%/61% macro-F1 vs. 4.8% random baseline; name VAE interpretability.]

runningauthor: "Kapon Epshtain, Fire, and Gordin"

significance: |
  [REVISE — target 120 words, undergraduate-level scientific audience.
  Emphasize: (1) first quantitative measurement of tablet shape norms over
  3,300 years; (2) systematic portrait-to-landscape shift detected;
  (3) interpretable AI model reveals institutional and diplomatic patterns
  invisible to manual inspection at this scale.]

keywords:
  - cuneiform
  - diplomatics
  - longue durée
  - deep learning
  - variational autoencoders
  - tablet dating
  - shape analysis
  - computational archaeology

bibliography: bibliography.bib

acknowledgements: |
  We thank Ben-Gurion University of the Negev and the Department of Software
  and Information Systems Engineering for computational resources. We thank
  Morris Alper for his role in initiating this project. We acknowledge the
  assistance of large language models (ChatGPT, Gemini) for enhancing the
  clarity and richness of the text.

author_contributions: >
  D.K.E. designed and implemented machine learning models, performed data
  analysis, and co-wrote the paper; M.F. supervised the computational
  methodology and co-wrote the paper; S.G. conceived the research, provided
  Assyriological expertise, performed historical analysis, and co-wrote the paper.

conflict_of_interest: "The authors declare no competing interests."

equal-contributor: >
  D.K.E. and M.F. contributed equally to the computational aspects of
  this work.

fontsize: "9pt"
classoption:
  - twocolumn
  - twoside
---
```

---

### 11.3 Document Body Structure and LaTeX Commands

#### Opening
Every PNAS article body opens with a **drop capital** — no "Introduction" heading:

```markdown
\dropcap{T}he emergence of writing in ancient Mesopotamia...
```

The `\firstpage{N}` command controls where the two-column body begins on page 1. Set it after the first paragraph once you can see the compiled output; `N` is the count of paragraphs (including headings) that should appear before the column break. Typical value: `\firstpage{8}` to `\firstpage{12}` depending on abstract length.

```latex
\firstpage{10}
```

#### Section Headings
PNAS uses a specific heading hierarchy. Map as follows in Quarto markdown:

| PNAS style | Quarto markdown |
|---|---|
| Bold inline heading (e.g., **Results.**) | `**Results.**` inline in paragraph — or use `##` and rely on class formatting |
| Numbered section | `##` (but `number-sections: false` is set — headings are unnumbered by default) |
| Sub-section | `###` |
| Bold inline sub-heading | `**Sub-heading.**` followed by text on same line |

PNAS research articles do **not** use an "Introduction" heading — the first section of the body is unheaded (implied introduction).

#### Cross-references
```markdown
@fig-ratioperiod          <!-- Figure cross-reference -->
@tbl-results              <!-- Table cross-reference -->
[@charpin2004; @hackl2021] <!-- Citations: numerical, in order of appearance -->
```

---

### 11.4 Figures: Specifications for This Paper

All figures should be placed in a `figs/` subdirectory. Preferred formats: high-resolution PDF or EPS. Sizing:
- **Single-column**: 8.7 cm wide — most main-text figures
- **Full-width** (`figure*`): 17.8 cm — use for confusion matrices (Fig. 7) and full-period dendrograms (Fig. 9 or 10)

#### Standard single-column figure
```markdown
![Caption text. {#fig-ratioperiod}](figs/fig_ratio_period.pdf)
```

#### Full-width figure (two-column span)
```r
#| label: fig-confusion
#| fig-cap: "Confusion matrices for ResNet50 on grayscale and masked images."
#| fig-env: "figure*"
#| echo: false
knitr::include_graphics('figs/fig_confusion_matrix.pdf')
```

Or in raw LaTeX within the `.qmd`:
```latex
\begin{figure*}[bt!]
  \centering
  \includegraphics[width=\textwidth]{figs/fig_confusion_matrix.pdf}
  \caption{Confusion matrices comparing ResNet50 classification performance
    on grayscale and masked images across 21 historical periods.}
  \label{fig:confusion}
\end{figure*}
```

#### Recommended figure list for main text (7–8 figures)
1. `fig-samples` — Sample count per period and genre (current Fig. 2)
2. `fig-ratioperiod` — H/W ratio per period (current Fig. 4) — *flagship*
3. `fig-ratiomillennium` — H/W ratio per millennium, boxplot + KDE (current Fig. 5)
4. `fig-standardization` — **NEW**: CV of H/W ratio per period, administrative genre (analysis 6.1)
5. `fig-widgets` — Interactive widgets, expanded with case study (current Fig. 3)
6. `fig-dendrogram` — Hierarchical clustering (choose either Fig. 9 or Fig. 10)
7. `fig-confusion` — ResNet50 confusion matrices, full-width (current Fig. 7)
8. `fig-vaefeatures` — VAE bottleneck feature analysis (current Fig. 11, revised)

All other current figures (Fig. 1, 6, 8, 12, 13, 14, 15) move to **SI Appendix**.

---

### 11.5 Tables

Use Quarto pipe table syntax. The main results table (Table 1 in current draft) remains in the main text:

```markdown
| Model | Grayscale Macro-F1 | Masked Macro-F1 | Grayscale AUC | Masked AUC |
|---|---|---|---|---|
| Decision Tree (H/W ratio only) | — | 0.08 | — | 0.64 |
| DINOv2-vits14 (zero-shot) | 0.02 | 0.42 | 0.54 | 0.88 |
| CNN | 0.61 | 0.49 | 0.93 | 0.88 |
| **ResNet50** | **0.71** | **0.61** | **0.97** | **0.93** |

: Tablet Period Classification — Model Performance Summary. Bold indicates
  best-performing model. {#tbl-results}
```

**Add a new row** for CuneiML baseline (Chen et al. 2023) with a footnote explaining the metric difference (accuracy vs. macro-F1, 14 vs. 21 classes, i.i.d. vs. potential distribution shift). **Add a new row** for OOD evaluation result from analysis 6.5.

---

### 11.6 References Section

Place at the very end of the document body. The `\bibsplit[N]` value (N = number of references in left column) must be adjusted after compilation. Start with `\bibsplit[30]` and tune.

```markdown
# References

\bibsplit[30]

:::{#refs}
:::
```

The `pnas-new.bst` style (loaded automatically by the extension) handles PNAS-format reference formatting and automatic journal name abbreviation. Do **not** set `biblio-style:` in YAML.

---

### 11.7 Supplementary Information (SI) Appendix

SI is a **separate `.qmd` or `.tex` file** compiled to a separate PDF and submitted alongside the main manuscript. It is **not** part of the main `.qmd` document.

Create `shaping_history_SI.qmd` with standard Quarto format (or plain LaTeX using the [PNAS Overleaf SI template](https://www.overleaf.com/latex/templates/pnas-template-for-supplementary-information/wqfsfqwyjtsd)).

**Contents of SI for this paper:**
- Fig. S1 — Average tablet shape per genre (genre-specific means, current supporting Fig. S1)
- Fig. S2 — Mean VAE encodings per period (current supporting Fig. S2)
- Fig. S3 — Administrative genre dendrograms per millennium (current supporting Fig. S3)
- Fig. S4 — Preprocessing pipeline illustration (current Fig. 13)
- Fig. S5 — Silhouette extraction process (current Figs. 14–15)
- Fig. S6 — Pearson correlation H/W per period (current Fig. 6)
- Fig. S7 — VAE confusion matrix / XGBoost dendrogram (current Figs. 8, 12)
- Fig. S8 — VAE feature X7 boxplot (current Fig. 11)
- Table S1 — Full confusion matrices for all models
- Table S2 — OOD evaluation by museum collection (analysis 6.5)
- Methods S1 — CNN architecture specification
- Methods S2 — ResNet50 fine-tuning hyperparameters
- Methods S3 — VAE architecture and loss function details
- Methods S4 — Hyperparameter search protocol

Reference SI from the main text: *"(see SI Appendix, Fig. S1)"* or *"(SI Appendix, Methods S2)"*.

---

### 11.8 Known Compilation Gotchas Specific to This Paper

1. **Short draft issue**: During early drafting, if the manuscript is less than one full compiled page, LaTeX throws a cryptic `Not in outer par mode` error. Add `{{< lipsum 5 >}}` as temporary filler.

2. **`\firstpage{N}` must be tuned**: After writing each major section, recompile and count the paragraph breaks on page 1. Adjust N until the two-column body begins at the correct position — typically where the Introduction ends and Results begins.

3. **`\bibsplit[N]` must be tuned**: Compile with all references, count how many appear in the left column on the last page, set N to that value. Start with `\bibsplit[30]`.

4. **Full-width figures and dendrograms**: The hierarchical clustering dendrograms (current Figs. 9, 10) are wide. Use `fig-env: "figure*"` for these. Place them as close as possible to their first in-text reference using `[bt!]` float positioning.

5. **Long confusion matrix figures**: Current Fig. 7 has two side-by-side confusion matrices. Use `figure*` with `\includegraphics[width=\textwidth]`. Alternatively, use the `SCfigure*` side-legend environment if the caption is long.

6. **`widetext` is deprecated**: The current LaTeX draft may use `widetext` for equations. Replace all instances with `figure*`.

7. **Bibliography**: The current draft's reference list (117 entries) will be substantially modified. The `jabbrv` package (bundled with the extension) will automatically abbreviate journal names — verify that abbreviated forms are correct for Assyriology journals (*Journal of Cuneiform Studies*, *Zeitschrift für Assyriologie*, *Altorientalische Forschungen*, *Archiv für Orientforschung*) that may not be in the LTWA abbreviation list.

---

### 11.9 Recommended File Structure for the Revised Paper

```
paper/
├── shaping_history_revised.qmd      # Main manuscript
├── shaping_history_SI.qmd           # Supplementary Information (separate PDF)
├── bibliography.bib                 # All references in BibTeX format
├── figs/
│   ├── fig_sample_counts.pdf
│   ├── fig_ratio_period.pdf         # H/W ratio per period (flagship)
│   ├── fig_ratio_millennium.pdf
│   ├── fig_standardization_cv.pdf   # NEW — analysis 6.1
│   ├── fig_widgets_casestudy.pdf    # NEW — expanded with case study
│   ├── fig_dendrogram_legal.pdf
│   ├── fig_confusion_resnet.pdf
│   ├── fig_vae_features.pdf
│   └── si/                          # SI figures
│       ├── fig_s1_genre_means.pdf
│       ├── fig_s2_vae_encodings.pdf
│       └── ...
└── _extensions/
    └── pnas/                        # Installed by: quarto add christopherkenny/pnas
```
