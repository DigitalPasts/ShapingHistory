**\[1\]**  
Thank you for joining me today. Over the next 30 minutes, I want to demonstrate how computer vision—the technology that helps self-driving cars ‘see’ the road—can help us address fundamental epigraphic questions about cuneiform tablets. This isn't about replacing human expertise; it's about scaling it systematically across the unprecedented volume of digitized materials now available to us.

**\[2\]**  
As Assyriologists, we've always practiced a form of ‘close reading’—examining individual tablets with meticulous attention to paleographic detail, linguistic features, and material characteristics. But digitization has fundamentally changed our field. We now have access to hundreds of thousands of tablet images. The question is no longer just ‘Can we read this tablet?’ but ‘How do we systematically analyze patterns across entire corpora?’ This is where computational methods become not just useful, but necessary.

**\[3\]**  
The term 'distant viewing' comes from Taylor Arnold and Lauren Tilton's work on large visual corpora. Their key insight—which applies perfectly to cuneiform—is that unlike text, which already exists as a code system, images require us to explicitly create that code system first. When we as Assyriologists look at a tablet, we're already performing this ‘viewing’ process implicitly: we recognize sign forms, assess ductus, evaluate damage patterns. Distant viewing simply makes this process explicit and systematic, allowing computational tools to replicate it at scale.

**\[4\]**  
I want to be very clear about what I'm advocating here. Computer vision doesn't replace Assyriological training. It doesn't understand literary context, it can't read damaged signs the way an experienced epigrapher can, and it certainly can't interpret historical significance. What it CAN do is provide systematic, reproducible preliminary analyses that help us prioritize our attention, identify outliers, and test hypotheses about patterns across large datasets. Think of it as a research assistant that can work 24/7 measuring tablets—but you still need to interpret what those measurements mean.

**\[5\]**  
**CASE STUDY 1**: How do we systematically match idealized sign forms (cuneiform fonts, reference tables) with actual sign executions across periods, scribal hands, and preservation states? Every Assyriologist here has performed this task countless times: you look at a sign, you mentally compare it to your internalized prototype of what that sign ‘should’ look like, and you identify it—often accounting for period, hand, and damage simultaneously. It’s a remarkable cognitive feat. But if we want to do this computationally across tens of thousands of signs, we need to make this process explicit. How do we define ‘wedge-ness’? How do we specify acceptable variation while maintaining identity? This is where the ProtoSnap AI model offers an elegant solution.

**\[6\]**  
The elegance of ProtoSnap lies in how it exploits cuneiform’s fundamental characteristic: signs are compositional. Every complex sign is built from elementary wedges in consistent spatial relationships. By training a deep learning model on thousands of examples, the system learns what makes a ‘wedge’ a wedge—not at the pixel level, but at a deeper semantic level. It can then match idealized prototypes to messy real-world impressions. And remarkably, this works across linguistic and temporal boundaries because the fundamental geometry of cuneiform impressions remains structurally consistent.

**\[7\]**  
These results demonstrate that ProtoSnap isn’t just a theoretical achievement—it's a practical tool. The most impactful application has been generating synthetic training data. In machine learning, you typically need thousands of examples to train a model. But for rare cuneiform signs, we might have only a handful of clear examples. ProtoSnap solves this by generating photorealistic variations—different lighting, different damage patterns, different clay textures—that let us train robust OCR models even for rare signs. This is particularly valuable for peripheral cuneiform traditions where sign frequencies differ from Babylonian standards.

**\[8\]**  
This brings us to a crucial methodological point. The real power of ProtoSnap isn't just in recognizing signs—it's in extracting MEASURABLE features from those signs. Every time ProtoSnap aligns a prototype to a tablet image, it's identifying specific geometric landmarks: wedge endpoints, intersection points, angular relationships. These landmarks can then be subjected to geometric morphometric analysis—the same statistical techniques used in archaeology to study pottery shapes or in biology to study skull morphology. This is where computer vision becomes truly integrated with traditional paleographic inquiry.

**\[9\]**  
**CASE STUDY 2**: To what extent do these historically contingent factors leave measurable traces in tablet morphology that can be detected and quantified computationally? For those familiar with diplomatics—the systematic study of document forms—this isn't a new question. Scholars have long noted that tablet shapes correlate with genres, periods, and archive practices. Eva Cancik-Kirschbaum, Dominique Charpin, Johannes Hackl and others have written extensively about how document format reflects institutional practices. 

**\[10\]**  
What's new here is applying this insight systematically across the largest corpus ever assembled, using computational methods that make our analytical criteria explicit and our results reproducible. We're not discovering that shape matters—we're quantifying HOW MUCH it matters and WHICH features matter most. The largest most diverse source is still the **CDLI Catalogue**, from which we could extract 94,470 tablet images, fat-crosses, in fact, that record most tablet dimensions, in 21 distinct historical periods spanning \~3,300 years, from Uruk IV \[3500 BCE\] to the Hellenistic period \[64 BCE\]. Most tablets are written in Akkadian, but also much Sumerian, as well as some Hittite, Elamite, Hurrian and others. The biggest **challenge** is the highly unbalanced nature of the dataset, in which the top 4 periods – Ur3, NA, OB, and MB – make up 63% of data.

**\[11\]**  
To create the “Code System” of distant viewing the images require preprocessing. In this case we ask the following question: *How much period information is preserved in tablet shape alone?* This preprocessing pipeline embodies the ‘viewing’ stage of distant viewing. We’re making explicit decisions about what features to preserve and what to discard.   
**Step 1: Standardization**

* Resize all images to 512×512 pixels (preserve aspect ratio)  
* Convert to grayscale (remove color variation)  
* Normalize brightness and contrast

**Step 2: Silhouette Extraction**

* Apply Gaussian blur to reduce noise  
* Binary thresholding to isolate tablet from background  
* Morphological operations to clean masks  
* Extract largest connected component

By creating binary silhouettes—pure black-and-white outlines—we're testing whether shape ALONE carries a historical signal, independent of surface details like sign forms or clay texture. This is the computational equivalent of traditional diplomatic analysis that describes tablet formats. The difference is we're doing it systematically for nearly 100,000 tablets.

**\[12\]**  
To test our hypothesis that shape indicates period, we trained several machine learning models for the task of **period classification**. As you can see from the resulting metrics in the slide, the numbers in bold belong to our best performing model: **ResNet 50**. For those less familiar with machine learning, think of ResNet50 as a highly sophisticated pattern recognition system. It learns a hierarchy of features: early layers detect basic elements like edges and textures, middle layers recognize wedge configurations and tablet profiles, and final layers integrate these into period classifications. The key innovation of ResNet is ‘skip connections’—shortcuts that allow information to bypass layers. This prevents the vanishing gradient problem that plagued earlier deep networks. We're not training this from scratch; we start with a model pre-trained on millions of general images and fine-tune it on our cuneiform tablets. We ran with 2 parallel Experiments:   
(1) **Grayscale input**: Full image information  
(2) **Silhouette input**: Shape information only  
The comparison would help to quantify contribution of shape vs. surface features.

Let’s interpret these results carefully. **Our key finding**: Silhouettes retain \~86% of classification information (61%/71%), validating shape as primary historical signal. A 71% accuracy rate (Macro-F1) for grayscale image input across 21 periods spanning 3,000 years is quite strong, far above the 4.8% random baseline. But more revealing than overall accuracy are the PATTERNS of confusion. When the model confuses Old Babylonian and Early Old Babylonian, as marked with a green arrow, that’s not really a failure – it’s detecting the genuine continuity between adjacent periods. The most impressive result is the Neo-Assyrian performance: 95% accuracy despite heavy fragmentation, as marked with a red arrow, because those fragments have such distinctive shapes – characteristic of letter formats. The same can be said for the Ur 3 tablets with 87% accuracy, given they were produced by a standardized bureaucracy. This is the model detecting patterns that align with diplomatic scholarship.

**\[13\]**  
But ResNet50 has \~25 million parameters and while it can make good predictions, it doesn't explain WHY, it is what we call a ‘Black Box’. For humanistic scholarship, explanation is as important as prediction, for example: what features distinguish Old Babylonian from Neo-Assyrian shapes? This is where we move from ‘machine learning’ to humanistic interpretation. VAE models or Variational Autoencoders, solve the black box problem by forcing all the complex shape information into just 12 numbers. It’s like compressing the hundreds of thousands of pixels of an image into 12 **essential features**. Because there are only 12, we can actually examine them, plot them, and interpret them. Think of it as the computational equivalent of traditional diplomatic description – but instead of saying ‘rectangular with rounded corners’, we're saying ‘VAE feature 3 \= 0.87, feature 7 \= \-0.34’. This makes the model’s reasoning transparent and allows us to ask: WHAT is feature 3 measuring? How does it correlate with known tablet shape criteria?

**\[14\]**  
This dendrogram is one of the most satisfying results from the *deeplomatics* project. We didn't tell the model anything about historical relationships, linguistic groupings, or scholarly theories about transmission. We just said: ‘Here are average tablet shapes from different periods – which are most similar?’ And it produced clusters that align beautifully with established scholarly understanding. The clustering of Old Babylonian → Middle Babylonian reflects documented continuity in Babylonian legal practices. The Neo-Babylonian → Achaemenid → Hellenistic cluster shows the persistence of Late Babylonian traditions even under Persian and Greek rule. This isn't replacing scholarship, it's providing computational validation for decades of traditional research.

**\[15\]**  
This graph is the first quantitative, large-scale evidence for diachronic shape evolution in cuneiform tablets – it moves beyond anecdotal observations to statistical demonstration. This finding emerged serendipitously from the VAE analysis. While examining which features the model was using, we noticed that one VAE dimension strongly correlated with height/width ratios, also known as the aspect ratio. When we plotted these across time, a clear trend emerged: tablets get progressively ‘wider’ over three millennia. Now, this isn’t universal, there's considerable variation within each period, but the aggregate trend is statistically robust. Why might this be? One possibility is functional: landscape tablets work better for multi-column scholarly texts that become prevalent in the first millennium. Another is archival: perhaps storage practices changed. Yet another is administrative: it is possible that certain writing practices, such as Aramaic on parchment, or Achaemenid-Elamite, influenced this change, especially in Mesopotamia. This is where computational analysis generates hypotheses that traditional scholarship can then investigate using contextual evidence.

**\[16\]**  
These interactive tools are designed to put ‘distant viewing’ directly in your hands. Instead of just accepting model predictions, you can explore WHY the model makes those predictions. The **feature explorer** (bottom right) lets you manipulate individual VAE dimensions and see what aspects of shape they control. For example, feature 4 controls aspect ratio, feature 7 seems to control tablet thickness at its upper and lower edges (marked with red arrows), and feature 8 controls corner rounding. The **interpolation widget** is particularly fun for teaching – students can literally watch tablets ‘morph’ from one period to another, seeing which features change first. The code of these tools is available on Huggingface and GitHub right now, and a demo will be ready soon. I'll now demonstrate their functionality in two short videos.

**\[17\]**  
The **feature explorer**

**\[18\]**  
The **interpolation widget**

**\[19\]**  
Now comes the fun part. I'm going to test whether 30 minutes of ‘distant viewing’ theory has made you better computational palaeographers. I'll show you tablet silhouettes – just the black-and-white outlines, no sign details – and I want you to guess the period. Don't worry about being ‘right’; the goal is to make your reasoning explicit. When you vote, think about WHAT features you're using to decide. Is it the shape? The size? The proportions? After we see the model’s prediction and the actual answer, we'll discuss where human and machine reasoning align or diverge. This exercise embodies the key insight of distant viewing: making implicit expertise explicit and systematic.

**\[20\]**  
Tablet example \#1: Ur 3, Admin

**\[21\]**  
Let's look at the features that guided predictions. Those who voted Ur III—what tipped you off? \[Wait for responses\]. Exactly—that portrait orientation is highly characteristic of third millennium administrative tablets. The model picked up on the same signal, with 92% confidence. Notice how the VAE features align: Feature 4, which we know controls aspect ratio, is \-1.84, very high on the portrait scale. Feature 7, controlling top and bottom thickness, indicates that characteristic ‘rounded rectangle’ profile. This is a case where human expertise and computational analysis perfectly align.

**\[22\]**  
Tablet example \#2: OB, Legal

**\[23\]**

**\[24\]**

**\[25\]**

**\[26\]**  
This exercise demonstrates the core argument of distant viewing: computational methods work best when integrated with human expertise. Notice that when we COMBINED human votes with model predictions, using an ‘or’ logic – if either humans OR model got it right – our accuracy got better. That’s higher than either alone. This isn’t human vs. machine; it’s human WITH the machine. The model provides systematic, reproducible preliminary analysis; you provide contextual validation and interpretive judgment. Think how these tools could actually support your research.

**\[27\]**  
Here is one such example: preliminary tablet dating, but there are more, such as shape-based archive analysis, which I am currently doing, as well as using these AI tools for teaching and public Engagement. I want to emphasize accessibility. You don't need to be a computer scientist to use these tools. Our GitHub repository includes 'quickstart' notebooks where you literally just change one line—the path to your tablet image—and run the cells. It will output period predictions with confidence scores. If you want to go deeper – extract VAE features, perform clustering – there are tutorials for that too. And if you get stuck, you can email me. The goal is to make distant viewing genuinely accessible to practicing Assyriologists, not just computational specialists.

**\[28\]**  
I want to be transparent about what this method cannot do and where we're heading next. Currently, we're limited to 2D analysis, which means we're missing important information about 3D tablet geometry. We’re also constrained by image quality and dataset imbalances. But these are solvable problems. If you work on a specific archive and want to apply these methods, let's talk. If you have high-quality data, I urge you to publish it in proper repositories for others to reuse, like Zenodo, where we have a community repository for the Digital Ancient Near Eastern Studies Network (DANES).

**\[29\]**  
Let me conclude with what I hope are the main takeaways. **First**, distant viewing is fundamentally about making our interpretive frameworks explicit and systematic. When we teach students to recognize palaeographic features, we’re already creating ‘code systems’ – distant viewing just makes those systems computational. **Second**, these methods work at different scales than traditional scholarship. They’re not better or worse; they’re complementary. Close reading reveals nuances; distant viewing reveals aggregate patterns. **Third**, the goal is partnership between human and machine. Models generate hypotheses; scholars validate and interpret them. **Fourth**, for humanistic applications, interpretability is non-negotiable. We need to understand not just predictions but reasoning. **Finally**, these tools only serve the field if they’re accessible. That’s why I've emphasized open-source code, documentation, and user-friendly interfaces. Digital epigraphy isn’t a separate discipline — it’s a set of methods that should be available to any scholar who finds them useful.