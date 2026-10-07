import numpy as np, math
from scipy import ndimage as ndi
dep=np.load('dep.npy')
ab=315.98; ob=ab+90
ux=np.array([math.sin(math.radians(ab)),math.cos(math.radians(ab))]); uy=np.array([math.sin(math.radians(ob)),math.cos(math.radians(ob))])
pxm=5.45
H,W=dep.shape
yy,xx=np.mgrid[0:H,0:W]
E=(xx-109)/pxm; N=-(yy-82)/pxm
X=E*ux[0]+N*ux[1]; Y=E*uy[0]+N*uy[1]
win=np.zeros((H,W),bool); win[330:790,180:720]=True
for T in [-1.0,-1.4,-1.8,-2.0,-2.2,-2.4,-2.6,-2.8,-3.0,-3.2]:
    m=(dep>T)&win
    m=ndi.binary_closing(m,iterations=2); m=ndi.binary_fill_holes(m)
    lab,n=ndi.label(m)
    sizes=ndi.sum(m,lab,range(1,n+1))
    keep=[i+1 for i,s in enumerate(sizes) if s>300]
    mm=np.isin(lab,keep)
    area=mm.sum()/pxm**2
    xs=X[mm];ys=Y[mm]
    # touches window edge?
    edge=mm[330,:].any() or mm[789,:].any() or mm[:,180].any() or mm[:,719].any()
    # E-W and N-S extents
    print(f"T={T:5.1f} comps={len(keep)} area={area:7.0f} m2  alongshore {xs.max()-xs.min():5.1f}  crossshore {ys.max()-ys.min():5.1f}  E-W {(E[mm].max()-E[mm].min()):5.1f} N-S {(N[mm].max()-N[mm].min()):5.1f}  edge={edge}")
