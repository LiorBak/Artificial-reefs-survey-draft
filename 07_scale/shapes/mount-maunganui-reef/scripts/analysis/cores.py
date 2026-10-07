import numpy as np, math, json
from scipy import ndimage as ndi
dep=np.load('dep.npy')
ab=315.98            # grid bearing of +x (alongshore, toward NW) [from compute_shape]
true_north_in_grid=-0.16095
pxm=5.45
H,W=dep.shape
def bearing_true(dE,dN):   # grid bearing of vector -> true bearing
    gb=math.degrees(math.atan2(dE,dN))%360
    return (gb-true_north_in_grid)%360
win=np.zeros((H,W),bool); win[380:760,240:660]=True
for T in (-1.0,-1.2,-1.4):
    m=(dep>T)&win
    m=ndi.binary_opening(m,iterations=1)
    lab,n=ndi.label(m)
    print('threshold',T)
    for i in range(1,n+1):
        mm=lab==i
        a=mm.sum()/pxm**2
        if a<8: continue
        yy,xx=np.nonzero(mm)
        E=xx/pxm; N=-yy/pxm
        pts=np.stack([E,N],1); mu=pts.mean(0); cov=np.cov((pts-mu).T); w,v=np.linalg.eigh(cov); ax=v[:,1]
        if ax[1]<0: ax=-ax
        b=bearing_true(ax[0],ax[1])%180
        t=(pts-mu)@ax; L=t.max()-t.min(); n_=(pts-mu)@np.array([-ax[1],ax[0]]); Wd=n_.max()-n_.min()
        # angle to shoreline (true bearing 136.15 -> mod 180)
        shore=136.145
        ang=abs(((b-shore+90)%180)-90)
        cx,cy=xx.mean(),yy.mean()
        print(f"  core at px({cx:.0f},{cy:.0f}) area {a:5.1f} m2  axis true bearing {b:6.1f} deg  angle to shore {ang:5.1f}  length {L:5.1f} m  width {Wd:4.1f} m")
