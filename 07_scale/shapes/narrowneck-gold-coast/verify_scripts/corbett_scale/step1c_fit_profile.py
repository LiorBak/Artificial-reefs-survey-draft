import numpy as np, cv2, json, math
from PIL import Image
from scipy import ndimage, optimize
from skimage.morphology import skeletonize
R="C:/Users/lior/Documents/Claude/Projects/Artificial reef/07_scale/shapes/narrowneck-gold-coast/"
cb=np.asarray(Image.open(R+"src/gov/corbett2023_extracted/p3_x88.png").convert("RGB")).astype(int)
jk=np.asarray(Image.open(R+"src/gov/narrowneck-gold-coast_jackson2012_fig2_reef_levels_original_and_revised_design_300dpi_crop.png").convert("L"))
X0=1020; jr=jk[:,X0:]
# Jackson line points: skeleton of dark; exclude -8 envelope & right region (x>500 of jr as in previous script)
jd=(jr<150); jd[:,500:]=False
jsk=skeletonize(jd); jy,jx=np.where(jsk); JP=np.c_[jx,jy].astype(float)
dtJ=ndimage.distance_transform_edt(~jsk)
# Corbett: lines in each panel = not near-white; remove frame
def cpts(x0,x1):
    sub=cb[14:320,x0:x1]; lum=sub.min(axis=2)
    m=(lum<200)
    # remove thin text? keep; skeleton
    sk=skeletonize(m); y,x=np.where(sk); return np.c_[x+x0,y+14].astype(float), sk
CL,skL=cpts(10,354); CR,skR=cpts(414,760)
print(len(JP),len(CL),len(CR))
H,W=dtJ.shape
def tf(P,c0,s,a,th,tx,ty):
    q=P-c0; c,sn=math.cos(th),math.sin(th); X=q[:,0]*s; Y=q[:,1]*s*a
    return np.c_[c*X-sn*Y+tx, sn*X+c*Y+ty]
def cost_fixed(p,P,c0,s_fixed=None):
    s,a,th,tx,ty=p
    if s_fixed: s=s_fixed
    if not(0.5<s<3 and 0.6<a<1.6 and abs(th)<0.4): return 1e3
    q=tf(P,c0,s,a,th,tx,ty); ins=(q[:,0]>=0)&(q[:,0]<W-1)&(q[:,1]>=0)&(q[:,1]<H-1)
    if ins.sum()<0.3*len(P): return 1e3
    d=ndimage.map_coordinates(dtJ,[q[ins,1],q[ins,0]],order=1)
    return float(np.mean(np.minimum(d,12))+3*(1-ins.mean()))
res={}
for name,P in (("left_Option1",CL),("right_Option2",CR)):
    c0=P.mean(0)
    best=None
    # profile in s (free aspect, rot, shift), with several starting shifts
    prof=[]
    for s in np.arange(1.15,2.01,0.05):
        bb=None
        for tx0 in (150,250,350,450):
            for ty0 in (250,350,450):
                r=optimize.minimize(lambda q: cost_fixed([s,q[0],q[1],q[2],q[3]],P,c0), [1.0,0.0,tx0,ty0],method="Nelder-Mead",options={"xatol":1e-3,"fatol":1e-4,"maxiter":1500})
                if bb is None or r.fun<bb.fun: bb=r
        prof.append((round(s,2),round(bb.fun,3),[round(v,3) for v in bb.x]))
    print(name)
    for p in prof: print("  ",p)
    res[name]=prof
json.dump({"c0_note":"profiles of chamfer cost vs s (Jackson Fig2 px per Corbett px)","res":res},open("c3_profile.json","w"))
