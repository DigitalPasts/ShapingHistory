"""Shared data for the pipeline figure options (cached to prep.npz / prep_corpus.csv)."""
import sys, os, numpy as np, pandas as pd, torch, cv2
from PIL import Image
from sklearn.decomposition import PCA
ROOT = os.path.expanduser('~/deeplomatics-repro'); OUT = f'{ROOT}/pipeline_figure'
sys.path.insert(0, os.path.expanduser('~/Dropbox/Git-projects/ShapingHistory'))
from VAE_model_tablets_class import VAE
PID = 100003
ck = torch.load(os.path.expanduser('~/Dropbox/Git-projects/ShapingHistory/VAE_trained_model/period_clf_bs8_lr0.0001_beta_1_epochs_30-VAE-94936_samples-masked_w_classification_loss-equalpartsloss-April16_2/checkpoints/epoch=22-step=213621.ckpt'), map_location='cpu', weights_only=False)
m = VAE(num_classes=ck['state_dict']['fc_classify.0.weight'].shape[0]); m.load_state_dict(ck['state_dict'], strict=False); m.eval()
def enc(x):
    with torch.no_grad(): return m.fc1(m.encoder(torch.from_numpy(x.astype(np.float32))[None, None]))[0].numpy()
def dec(z):
    with torch.no_grad(): return m.decoder(m.fc3(torch.from_numpy(z.astype(np.float32))[None]))[0, 0].numpy()

# preprocessing illustration (repo: grayscale, proportional resize + pad to 512, /255, GaussianBlur 11, > 0.125)
photo = np.asarray(Image.open(f'{OUT}/photos/P{PID}.jpg').convert('RGB'))
g = cv2.cvtColor(photo, cv2.COLOR_RGB2GRAY); h, w = g.shape; s = 512 / max(h, w)
r = cv2.resize(g, (int(round(w * s)), int(round(h * s))), interpolation=cv2.INTER_AREA)
gray512 = np.zeros((512, 512), np.uint8); oy, ox = (512 - r.shape[0]) // 2, (512 - r.shape[1]) // 2
gray512[oy:oy + r.shape[0], ox:ox + r.shape[1]] = r
blur = cv2.GaussianBlur(gray512.astype(np.float32) / 255, (11, 11), 0)
mask = np.asarray(Image.open(f'{ROOT}/zenodo/images_b_w_tablets/{PID:06d}.png')).astype(np.float32) / 255   # published mask
mu = enc(mask); recon = dec(mu)

# corpus: VAE codes + metadata (tablets only)
vae = pd.concat([pd.read_csv(f'{ROOT}/zenodo/vae_encoding_df_April16_w_class_{s}.csv') for s in ['train', 'val', 'test']])
art = pd.read_csv(os.path.expanduser('~/Dropbox/Git-projects/ShapingHistory/artifacts.csv'), usecols=['artifact_id', 'artifact_type', 'provenience', 'collections', 'designation'], low_memory=False)
hw = pd.read_csv(f'{ROOT}/zenodo/h_w_ratio_df_all.csv'); hw['CDLI_id'] = hw.tablet_p_id_CDLI.str[1:].astype(int)
df = vae.merge(art, left_on='CDLI_id', right_on='artifact_id', how='left').merge(hw[['CDLI_id', 'height', 'width', 'hw_ratio']], on='CDLI_id', how='left')
df = df[df.artifact_type.isin(['tablet', 'tablet & envelope'])].reset_index(drop=True)
X = df[[f'X{i}' for i in range(1, 13)]].values; sd = X.std(0)
P2 = PCA(2, random_state=0).fit(X); df[['pc1', 'pc2']] = P2.transform(X)
corr = [np.corrcoef(X[:, k], df.hw_ratio.fillna(df.hw_ratio.median()))[0, 1] for k in range(12)]
kh = int(np.argmax(np.abs(corr)))
trav_vals = np.linspace(-2, 2, 5)
trav = np.stack([dec(mu + np.eye(12)[kh] * v * sd[kh]) for v in trav_vals])
# nearest neighbours of the example in z-scored latent space, other museums only
Z = (X - X.mean(0)) / sd; me = df.index[df.CDLI_id == PID][0]
d = np.linalg.norm(Z - Z[me], axis=1); mus = df.collections.fillna('').str.split(';').str[0]
d[(mus == mus[me]).values] = np.inf
nn = np.argsort(d)[:6]
nn_masks = np.stack([np.asarray(Image.open(f'{ROOT}/zenodo/images_b_w_tablets/{int(df.CDLI_id[i]):06d}.png')) for i in nn])
np.savez_compressed(f'{OUT}/prep.npz', photo=photo, gray512=gray512, blur=blur, mask=mask, mu=mu, recon=recon, trav=trav, trav_vals=trav_vals,
                    kh=kh, corr=np.array(corr), nn_masks=nn_masks, nn_ids=df.CDLI_id.values[nn], nn_d=d[nn], me=me, sd=sd)
df[['CDLI_id', 'Period_Name', 'Genre_Name', 'provenience', 'collections', 'designation', 'height', 'width', 'hw_ratio', 'pc1', 'pc2']].to_csv(f'{OUT}/prep_corpus.csv', index=False)
print('example', df.loc[me, ['CDLI_id', 'designation', 'Period_Name', 'provenience', 'hw_ratio']].to_dict())
print('latent dim most correlated with h/w ratio: X%d r=%.2f' % (kh + 1, corr[kh])); print('corr', np.round(corr, 2))
print('nn', df.loc[nn, ['CDLI_id', 'designation', 'Period_Name', 'provenience']].to_string())
print('hw quantiles', df.hw_ratio.quantile([.05, .25, .5, .75, .95]).round(2).to_dict(), 'recon IoU', ((recon > .5) & (mask > .5)).sum() / ((recon > .5) | (mask > .5)).sum())
