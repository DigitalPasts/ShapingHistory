"""DINOv2 representation for the confirmation runs (plan step 5). Input: the embeddings exported from the Mac Studio
(dinov2_vitb14_224_masked_cls.npz: DINOv2 ViT-B/14 CLS token, pretrained, no fine-tuning, on the Zenodo 12787746 binary
masks at 224 x 224, made by deeplomatics-repro/results/01_dinov2_embed.py). Output: WORK/dinov2_pca.parquet with the
first 32 principal components (fitted on all tablets in master_tablets) and the explained variance."""
from _paths import WORK
import numpy as np, pandas as pd
from sklearn.decomposition import PCA
z = np.load(f'{WORK}/mac_export/dinov2_vitb14_224_masked_cls.npz')
ids = pd.Series(z['ids']).str.replace('P', '', regex=False).astype(int).values
X = z['X'].astype(np.float32)
m = pd.read_parquet(f'{WORK}/master_tablets.parquet', columns=['id'])
keep = np.isin(ids, m.id.values); ids, X = ids[keep], X[keep]
_, first = np.unique(ids, return_index=True); ids, X = ids[first], X[first]
p = PCA(32, random_state=0).fit(X); Y = p.transform(X)
out = pd.DataFrame(Y, columns=[f'D{i}' for i in range(1, 33)]); out.insert(0, 'id', ids)
out.to_parquet(f'{WORK}/dinov2_pca.parquet', index=False)
pd.DataFrame({'pc': range(1, 33), 'explained': p.explained_variance_ratio_}).to_csv(f'{WORK}/dinov2_pca_variance.csv', index=False)
print(len(out), 'tablets with DINOv2;', 'variance in 12 PCs', round(p.explained_variance_ratio_[:12].sum(), 3), 'in 32', round(p.explained_variance_ratio_.sum(), 3))
