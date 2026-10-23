import numpy as np, cv2, json, math
from PIL import Image
from scipy import ndimage, optimize
from skimage.morphology import skeletonize
R="C:/Users/lior/Documents/Claude/Projects/Artificial reef/07_scale/shapes/narrowneck-gold-coast/"
cb=np.asarray(Image.open(R+"src/gov/corbett2023_extracted/p3_x88.png").convert("RGB")).astype(int)
def skel(x0,x1):
    m=(cb[14:320,x0:x1].min(axis=2)<200); sk=skeletonize(m); y,x=np.where(sk); return np.c_[x+x0,y+14].astype(float),sk
PL,skL=skel(10,354); PR,skR=skel(414,760)
H,W=cb.shape[:2]
dtL=ndimage.distance_transform_edt(~np.pad(skL,((14,H-320),(10,W-354))))
dtR=ndimage.distance_transform_edt(~np.pad(skR,((14,H-320),(414,W-760))))
# Option2 pts (right) -> Option1 (left) frame: translate (-dx,-dy), rotation about pivot
def fit(sub_r,sub_l,rot=False,label=""):
    # move subset of right points onto left DT; params dx,dy[,th]
    P=PR[sub_r(PR)]
    best=None
    def cost(p):
        dx,dy=p[0],p[1]; th=p[2] if rot else 0
        c0=P.mean(0); q=P-c0; cs,sn=math.cos(th),math.sin(th)
        Q=np.c_[cs*q[:,0]-sn*q[:,1],sn*q[:,0]+cs*q[:,1]]+c0-[dx,dy]
        ok=(Q[:,0]>=0)&(Q[:,0]<W-1)&(Q[:,1]>=0)&(Q[:,1]<H-1)
        d=ndimage.map_coordinates(dtL,[Q[ok,1],Q[ok,0]],order=1)
        return float(np.mean(np.minimum(d,10)))
    for dx0 in range(340,420,8):
        for dy0 in range(-30,31,10):
            r=optimize.minimize(cost,[dx0,dy0,0.0] if rot else [dx0,dy0],method="Nelder-Mead",options={"xatol":1e-3,"fatol":1e-5})
            if best is None or r.fun<best.fun: best=r
    print(label,"rot" if rot else "trans","cost",round(best.fun,2),"params",[round(float(v),3) for v in best.x], ("rot deg %.2f"%math.degrees(best.x[2])) if rot else "")
    return best
subN=lambda P:(P[:,1]<150)&(P[:,0]<760)
subS=lambda P:(P[:,1]>200)
for lab,sub in (("N reef",subN),("S reef",subS)):
    fit(sub,None,False,lab); fit(sub,None,True,lab)
