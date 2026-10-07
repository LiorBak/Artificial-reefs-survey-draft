import numpy as np, math, json
from PIL import Image
from scipy import ndimage as ndi
from scipy.optimize import minimize
exec(open('reg4.py').read().split('# initial translation')[0])
out={}
for T in [-3.0,-3.4,-3.8,-4.2,-4.6]:
    mIf=ndi.gaussian_filter(imask(T).astype(float),1.0)
    p0=[1.093,1.0,220.4,305.4]
    r=minimize(score,p0,args=(mIf,),method='Nelder-Mead',options=dict(xatol=1e-4,fatol=1e-8,maxiter=1500))
    s,th,tx,ty=r.x
    w=warp(mIf,s,th,tx,ty)>0.5
    inter=(w&m3).sum(); uni=(w|m3).sum()
    print(f"T={T}: s={s:.4f} th={th:.2f} t=({tx:.1f},{ty:.1f}) corr={-r.fun:.3f} IoU={inter/uni:.3f} area_w={w.sum()/5.45**2:.0f} area_m3={m3.sum()/5.45**2:.0f}  px/m_I={5.45*s:.3f}")
    out[T]=dict(s=s,th=th,tx=tx,ty=ty,corr=-r.fun,iou=inter/uni)
json.dump({str(k):v for k,v in out.items()},open('reg_all.json','w'),indent=1)
