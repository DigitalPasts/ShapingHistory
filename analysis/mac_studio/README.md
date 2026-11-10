# Scripts run on S.G.'s computers

Source code copied from the Mac export of 10 November 2026 (`deeplomatics-repro`): the Archibab linking and label-signal
analyses (`archibab/01-09`), the museum tests (`museum_tests/`), the NaBuCCo and Prosobab parsers, and the pipeline
figure. Data files, results and the original notebooks (already in this repository) were left out. The DINOv2 ViT-B/14
embeddings of the masks (92,876 x 768, float16) were computed there with Python 3.12, torch 2.14 and timm 1.0; they are
read by `analysis/scripts/103_dinov2_prepare.py`. See `INDEX.md` for the original layout.
