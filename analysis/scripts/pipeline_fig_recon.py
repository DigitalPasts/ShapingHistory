from _paths import REPO, WORK
import sys; sys.path.insert(0,REPO); sys.path.insert(0,WORK+'/pipeline_fig/stub')
import torch, numpy as np, cv2, glob
from VAE_model_tablets_class import VAE
ck=glob.glob(WORK+'/zenodo/vae_model/VAE_trained_model/*/checkpoints/*.ckpt')[0]
sd=torch.load(ck,map_location='cpu',weights_only=False)['state_dict']
nc=[v.shape[0] for k,v in sd.items() if k.endswith('weight') and v.dim()==2 and v.shape[1]==12 and 'fc3' not in k][0]
m=VAE(num_classes=nc); m.load_state_dict(sd,strict=False); m.eval()
a=cv2.imread(WORK+'/zenodo/imgs/images_b_w_tablets/104315.png',0).astype(np.float32)/255
x=torch.tensor(a)[None,None]
with torch.no_grad():
    h=m.encoder(x); mu,lv=m.fc1(h),m.fc2(h); print(mu.numpy().round(2))
    r=m.decoder(m.fc3(mu)).numpy()[0,0]
cv2.imwrite('recon_104315.png',(np.clip(r,0,1)*255).astype(np.uint8)); print(r.min(),r.max())
z0=mu.clone()
for d,vals in [(1,[-2.5,2.5]),(11,[-1.0,3.0]),(2,[-2.0,2.0])]:
    for v in vals:
        z=z0.clone(); z[0,d]=v
        with torch.no_grad(): r=m.decoder(m.fc3(z)).numpy()[0,0]
        cv2.imwrite(f'trav_X{d+1}_{v:+.1f}.png',(np.clip(r,0,1)*255).astype(np.uint8))
