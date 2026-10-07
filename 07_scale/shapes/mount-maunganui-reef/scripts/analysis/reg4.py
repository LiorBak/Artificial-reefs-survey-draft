import numpy as np, math, json
from PIL import Image
from scipy import ndimage as ndi
from scipy.optimize import minimize
R='C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/07_scale/shapes/mount-maunganui-reef/'
exec(open('reg_inst.py').read().split('mI_raw=')[0])
def imask(T):
    m=(depI>T)&okI; m=ndi.binary_opening(m,iterations=1); return np.rot90(m,k=-1)
H3,W3=m3.shape
m3f=ndi.gaussian_filter(m3.astype(float),1.5)
def warp(mask_f,s,th,tx,ty):
    # p3 = (1/s) R(th) pI + t ; ndimage.affine_transform maps output coords (p3) -> input coords (pI): pI = s R(-th) (p3 - t)
    c,sn=math.cos(math.radians(th)),math.sin(math.radians(th))
    Rinv=np.array([[c,sn],[-sn,c]])   # R(-th) acting on (x,y)
    # arrays are indexed (row=y, col=x); build matrix for (y,x) ordering
    M_xy=s*Rinv
    M=np.array([[M_xy[1,1],M_xy[1,0]],[M_xy[0,1],M_xy[0,0]]])
    t_xy=np.array([tx,ty]); off_xy=-M_xy@t_xy
    off=np.array([off_xy[1],off_xy[0]])
    return ndi.affine_transform(mask_f,M,offset=off,output_shape=(H3,W3),order=1)
def score(p,mIf):
    s,th,tx,ty=p
    w=warp(mIf,s,th,tx,ty)
    return -(w*m3f).sum()/math.sqrt((w**2).sum()*(m3f**2).sum()+1e-9)
# initial translation from FFT: ix,iy offset in crop (150,300) -> tx=150+ix, ty=300+iy
for T,(s0,ix,iy) in {-3.8:(1.19,91,18),-4.2:(1.19,95,24)}.items():
    mIf=ndi.gaussian_filter(imask(T).astype(float),1.5)
    p0=[s0,0.0,150+ix,300+iy]
    r=minimize(score,p0,args=(mIf,),method='Nelder-Mead',options=dict(xatol=1e-3,fatol=1e-6,maxiter=600,initial_simplex=None))
    print(T,'start',-score(p0,mIf),'->',r.x,-r.fun)
    json.dump(dict(T=T,s=r.x[0],th=r.x[1],tx=r.x[2],ty=r.x[3],score=-r.fun),open(f'reg_T{abs(T)}.json','w'))
