import json, numpy as np, tifffile
from scipy import ndimage as ndi
D=r"C:\Users\lior\AppData\Local\Temp\claude\C--\cd973dbd-a674-4cd5-adf1-ffb4c361545f\scratchpad\borth_verify\dl"
dsm=tifffile.imread(D+r"\wg_dsm_SN6089.tif"); dtm=tifffile.imread(D+r"\wg_dtm_SN6089.tif")
w=json.load(open('lidar_win.json')); E0,N1=w['E0'],w['N1']
lab=np.load('lab.npy'); 
E1,N0=260640,289080
r0=290000-N1; c0=E0-260000
W=dsm[r0:r0+lab.shape[0],c0:c0+lab.shape[1]]; Wt=dtm[r0:r0+lab.shape[0],c0:c0+lab.shape[1]]
for nm,i in (('N mound',2),('S mound',3)):
    m=lab==i
    z=W[m]; zt=Wt[m]
    print(nm,'cells',m.sum())
    print(' DSM percentiles 1,5,25,50,75,90,95,99,max:',[round(float(np.percentile(z,p)),2) for p in (1,5,25,50,75,90,95,99,100)])
    print(' DTM percentiles 1,5,25,50,75,90,95,99,max:',[round(float(np.percentile(zt,p)),2) for p in (1,5,25,50,75,90,95,99,100)])
    print(' DSM-DTM mean',round(float((z-zt).mean()),3),'std',round(float((z-zt).std()),3), 'cells DSM>DTM+0.05',int(((z-zt)>0.05).sum()))
    for thr in (-2.0,-1.5,-1.0,-0.5,0.0,0.5,1.0,1.5):
        print('   area above',thr,'mODN:',int((z>thr).sum()),'m2')
# whole-data: lowest valid values at water edge
print('edge min across window',float(W[W>-9000].min()))
