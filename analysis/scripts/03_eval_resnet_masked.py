"""Re-score (masks fed as released, no second blur) the released masked ResNet50 (Zenodo 11668220) on its own test split (= VAE test csv ids), all objects vs tablets only."""
from _paths import WORK
import glob, numpy as np, pandas as pd, torch, cv2
from torch import nn
from torchvision import models
from PIL import Image
from sklearn.metrics import f1_score, accuracy_score
R=WORK
PI={'other':0,'Ur III':1,'Neo-Assyrian':2,'Old Babylonian':3,'Middle Babylonian':4,'Neo-Babylonian':5,'Old Akkadian':6,'Achaemenid':7,'Early Old Babylonian':8,'ED IIIb':9,'Middle Assyrian':10,'Old Assyrian':11,'Uruk III':12,'Proto-Elamite':13,'Lagash II':14,'Ebla':15,'ED IIIa':16,'Hellenistic':17,'ED I-II':18,'Middle Elamite':19,'Hittite':20,'Uruk IV':21}
class M(nn.Module):
    def __init__(s,n=24):
        super().__init__(); s.gray_to_triple=nn.Conv2d(1,3,(1,1)); s.core=models.resnet50(); s.core.fc=nn.Linear(s.core.fc.in_features,n)
    def forward(s,x): return s.core(s.gray_to_triple(x.unsqueeze(1)))
ck=glob.glob(f'{R}/zenodo/models/**/*.ckpt',recursive=True)[0]
sd=torch.load(ck,map_location='cpu',weights_only=False)['state_dict']
m=M(); print(m.load_state_dict({k:v for k,v in sd.items() if not k.startswith(('train_acc','val_acc','objective'))},strict=False)); m.eval()
torch.set_num_threads(4)
t=pd.read_csv(f'{R}/zenodo/vae_encoding_df_April16_w_class_test.csv')[['CDLI_id','Period_Name']]
t['y']=t.Period_Name.map(PI).fillna(0).astype(int)
preds=[]
B=16
ids=t.CDLI_id.tolist()
for i in range(0,len(ids),B):
    xs=[]
    for c in ids[i:i+B]:
        img=np.asarray(Image.open(f'{R}/zenodo/imgs/images_b_w_tablets/{c:06d}.png')).astype(np.float32)/255
        xs.append(img)  # Zenodo masks are already blurred+thresholded by the release pipeline; blurring again lowers acc to 0.732
    with torch.no_grad(): preds+=m(torch.from_numpy(np.stack(xs))).argmax(1).tolist()
    if i%800==0: print(i,flush=True)
t['pred']=preds
a=pd.read_csv(f'{R}/artifacts.csv',usecols=['artifact_id','artifact_type'],low_memory=False)
t=t.merge(a,left_on='CDLI_id',right_on='artifact_id',how='left')
t.to_csv(f'{R}/results/resnet_masked_test_predictions.csv',index=False)
for name,s in [('all objects',t),('tablets only',t[t.artifact_type.isin(['tablet','tablet & envelope'])])]:
    print(name,len(s),'acc',round(accuracy_score(s.y,s.pred),3),'macroF1',round(f1_score(s.y,s.pred,average='macro'),3),'weightedF1',round(f1_score(s.y,s.pred,average='weighted'),3))
nt=t[~t.artifact_type.isin(['tablet','tablet & envelope'])]; print('non-tablets acc',round(accuracy_score(nt.y,nt.pred),3),len(nt))
