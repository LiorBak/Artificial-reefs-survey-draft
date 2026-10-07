import json, numpy as np, tifffile
from scipy import ndimage as ndi
D=r"C:\Users\lior\AppData\Local\Temp\claude\C--\cd973dbd-a674-4cd5-adf1-ffb4c361545f\scratchpad\borth_verify\dl"
dsm=tifffile.imread(D+r"\wg_dsm_SN6089.tif")
w=json.load(open('lidar_win.json')); E0,N1=w['E0'],w['N1']
lab=np.load('lab.npy'); r0=290000-N1; c0=E0-260000
W=dsm[r0:r0+lab.shape[0],c0:c0+lab.shape[1]].astype(float)
def grid_xy(m):
    ys,xs=np.where(m); return xs+E0+0.5, N1-ys-0.5
# smoothed gradient in flank zones
for nm,i in (('N',2),('S',3)):
    m=lab==i
    Z=np.where(m,W,np.nan)
    # fill nan with nearest for filtering? use normalized convolution
    k=np.ones((5,5)); 
    num=ndi.convolve(np.where(m,W,0),k,mode='constant'); den=ndi.convolve(m.astype(float),k,mode='constant')
    Zs=np.where(den>20,num/np.maximum(den,1),np.nan)
    gy,gx=np.gradient(Zs); g=np.hypot(gx,gy)
    for lo,hi in ((-2.2,-1.5),(-1.5,-0.5),(-0.5,0.2),(0.2,0.8),(0.8,1.6)):
        sel=(Zs>lo)&(Zs<=hi)&np.isfinite(g)
        gm=np.nanmedian(g[sel]); print(nm,f'z {lo}..{hi}: median |grad| {gm:.3f} => slope 1:{1/gm:.1f} (H:V)  cells {sel.sum()}')
# long axis profile of N mound: PCA axis
m=lab==2; x,y=grid_xy(m); z=W[m]
P=np.column_stack([x,y]); c=P.mean(0); u,s,vt=np.linalg.svd(P-c,full_matrices=False); ax=vt[0]; nrm=np.array([-ax[1],ax[0]])
if ax[0]<0: ax=-ax; nrm=-nrm
t=(P-c)@ax; q=(P-c)@nrm
print('N axis bearing deg',(np.degrees(np.arctan2(ax[0],ax[1]))+360)%360,'length extent',t.min(),t.max())
# crest along axis: for each 10 m bin, 90th percentile and median of top-cells
for a in range(int(t.min()),int(t.max()),10):
    sel=(t>=a)&(t<a+10)
    if sel.sum()<20: continue
    zz=z[sel]; print(f' N axis {a:4d}..{a+10:4d}: n {sel.sum():4d} width {q[sel].max()-q[sel].min():5.1f} m  z p50 {np.percentile(zz,50):5.2f} p90 {np.percentile(zz,90):5.2f} max {zz.max():5.2f}')
m=lab==3; x,y=grid_xy(m); z=W[m]
for a in range(int(y.min()),int(y.max()),8):
    sel=(y>=a)&(y<a+8)
    if sel.sum()<10: continue
    zz=z[sel]; print(f' S N={a}..{a+8}: n {sel.sum():4d} width {x[sel].max()-x[sel].min():5.1f} z p50 {np.percentile(zz,50):5.2f} p90 {np.percentile(zz,90):5.2f} max {zz.max():5.2f}')
