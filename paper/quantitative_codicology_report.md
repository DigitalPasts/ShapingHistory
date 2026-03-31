# Structural Codicology meets Cuneiform Diplomatics: A Quantitative Synthesis

This report contextualizes the statistical analyses of cuneiform tablet dimensions (height/width ratios, chronological drift, and standardization metrics) against established quantitative methodologies used in manuscript studies, evolutionary archaeology, and digital codicology.

## 1. Measuring Institutional Control: The Coefficient of Variation (CV)

**The Notebook Approach:**
In your statistical pipeline, you calculate the Coefficient of Variation (CV) specifically for tablets within the "Administrative" genre across different periods. This isolates intentional institutional standardization from general morphological noise.

**Insights from the Literature:**
Your methodology directly aligns with the gold-standard theories in evolutionary archaeology and material culture studies, specifically the framework established by **Eerkens and Bettinger (2001)** (*"Techniques for Assessing Standardization in Artifact Assemblages"*). 
*   **The CV Advantage:** Because CV scales the standard deviation to the mean ($\text{CV} = \sigma / \mu$), it is the only statistically sound way to compare the variability of objects across completely different size tiers (e.g., small Old Assyrian letters vs. massive Neo-Assyrian treaties) or different media (clay vs. parchment). 
*   **Random vs. Stimulated Variation:** By tracking changes in the CV over time, you can distinguish between "random background variation" (natural human drift when shaping clay by hand) and "stimulated variation" (top-down institutional mandates for standardized archiving). A sharp drop in the CV of administrative texts strongly indicates a tightening of state bureaucracy and specialized scribal training.

## 2. Diachronic Morphometrics and "Remarkable Rectangles"

**The Notebook Approach:**
You utilize log-scale distributions to symmetrically represent portrait vs. landscape ratios, Kruskal-Wallis/Mann-Whitney U tests to find significant shifts between periods, and Spearman rank correlations to measure directional diachronic drift.

**Insights from the Literature:**
Quantitative codicology has long obsessed over the geometric constraints of the *mise en page* (page layout). The literature highlights two competing philosophies in manuscript production that can be directly tested on your cuneiform data:
*   **"Fixed Balance" vs. "Variable Balance":** Literature discussing Jan Tschichold’s theories (e.g., *10.1515_9783110743838-013*) contrasts "fixed balance" documents—where proportions conform to strict, pre-determined geometric rules (the "remarkable rectangles")—with "variable balance" layouts that dynamically shape themselves around the mass of the text. 
*   **Geometric Rules in Early Books:** **A. George's** analysis (*The Geometry of Early Qur'anic Manuscripts*) proves that early medieval bookmakers adhered to strictly regulated proportion ratios (width-to-height). By using log-scale distributions and non-parametric tests, your notebook treats the cuneiform tablet as a precursor to the codex page. If the Kruskal-Wallis tests show rigid stability in aspect ratios across certain periods despite varying geographic locations, it proves cuneiform scribes were utilizing a "fixed balance" cognitive template for tablet shaping centuries before parchment geometry.

## 3. From 3D Objects to 2D Data Models: The Digital Codicology Evolution

**The Notebook Approach:**
Extracting 2D physical dimensions (and eventually latent image representations via VAEs/CNNs in your broader project) to reduce complex 3D clay objects into structured, flat arrays for omnibus testing.

**Insights from the Literature:**
*   **The Materiality of the Text:** Scholars like **Stokes** (*Digital approaches to paleography*) emphasize that a book is fundamentally a 3D material object with affective properties—weight, thickness, and hand-feel. Converting this complex shape into flat database dimensions involves a theoretical reduction. 
*   **Automated Feature Extraction:** Sources like **Busch and Chandna** (*eCodicology: The Computer and the Mediaeval Library*) detail modern computational tools designed to extract structural codicology data at scale. Your work places Assyriology at the forefront of this movement. By merging your rigorous ratio statistics with DinoV2/VAE latent space analysis (as seen elsewhere in your workspace), you bypass the limitations of simple height/width lists, allowing the neural networks to handle the "affective," high-dimensional physical features that Stokes argues are usually lost in traditional databases.

### Conclusion and Next Steps for the Manuscript

To maximize the impact of your results in the paper:
1.  **Frame the CV results** not just as a statistical quirk, but as a direct proxy for bureaucratic centralization, citing Eerkens & Bettinger to bridge the gap between Assyriology and broader Archaeological theory.
2.  **Use the codicological vocabulary** ("fixed balance", *mise en page*) to describe tablet shaping. This translates cuneiform diplomatics into a language immediately legible to medievalists and historians of the book.
3.  **Highlight the Log-Scale Ratio:** Explicitly state in the text that your use of the log-scale corrects the mathematical asymmetries that have historically plagued proportional studies of manuscripts and artifacts.