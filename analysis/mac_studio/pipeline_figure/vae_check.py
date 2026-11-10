import sys, os, numpy as np, pandas as pd, torch
from PIL import Image
sys.path.insert(0, os.path.expanduser('~/Dropbox/Git-projects/ShapingHistory'))
from VAE_model_tablets_class import VAE
ck = torch.load(os.path.expanduser('~/Dropbox/Git-projects/ShapingHistory/VAE_trained_model/period_clf_bs8_lr0.0001_beta_1_epochs_30-VAE-94936_samples-masked_w_classification_loss-equalpartsloss-April16_2/checkpoints/epoch=22-step=213621.ckpt'), map_location='cpu', weights_only=False)
sd = ck['state_dict']; print([ (k, v.shape) for k, v in sd.items() if 'classify' in k]); print(ck.get('hyper_parameters'))
nc = sd['fc_classify.0.weight'].shape[0]
m = VAE(num_classes=nc); print(m.load_state_dict(sd, strict=False)); m.eval()
t = pd.read_csv(os.path.expanduser('~/deeplomatics-repro/zenodo/vae_encoding_df_April16_w_class_test.csv')).head(5)
for _, r in t.iterrows():
    x = np.asarray(Image.open(os.path.expanduser(f'~/deeplomatics-repro/zenodo/images_b_w_tablets/{int(r.CDLI_id):06d}.png'))).astype(np.float32) / 255
    with torch.no_grad():
        h = m.encoder(torch.from_numpy(x)[None, None]); mu = m.fc1(h)[0].numpy()
    print(int(r.CDLI_id), np.round(mu[:4], 3), np.round(r[['X1', 'X2', 'X3', 'X4']].values.astype(float), 3))
