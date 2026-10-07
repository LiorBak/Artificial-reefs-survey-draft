"""fig5a_register.py (verifier 2026-10-07): register Jackson et al. 2012 Fig 5a (GCCC bathymetric survey 2011-06-09, contours + thick black
design contours) to the Fig 2-right design drawing by chamfer fit of the design -2.5 loops and the outer -6.0 contour (output of design_outline_2004.py)
and write fig5a_register.json (affine Fig5a px -> Fig 2 px crop coordinates, and -> s3 px / canonical)."""
import numpy as np, cv2, json, os, math
from PIL import Image
from scipy import ndimage, optimize
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
G=ROOT+"/src/gov/narrowneck-gold-coast_jackson2012_"
f5=np.asarray(Image.open(G+"fig5a_reef_bathymetry_2011-06-09_native.jpeg").convert("RGB")).astype(int)
H,W,_=f5.shape
black=(f5.max(axis=2)<70)
dt=ndimage.distance_transform_edt(~black)
D=json.load(open(HERE+"/design_outline_2004.json"))
# model points: need Fig 2 crop coordinates of the outer -6 boundary and the -2.5 loops: recompute from s3 px is not possible -> re-run extraction here
import importlib.util
spec=importlib.util.spec_from_file_location("dod",HERE+"/design_outline_2004.py"); 
src=open(HERE+"/design_outline_2004.py").read().split("# (3),(4) transforms")[0]
ns={"__file__":HERE+"/design_outline_2004.py"}; exec(compile(src,"dod","exec"),ns)
outer,inner=ns["outer_s"],ns["inner"]
def dens(poly,step=2.0):
    p=np.vstack([poly,poly[:1]]); out=[]
    for a,b in zip(p[:-1],p[1:]):
        n=max(1,int(np.hypot(*(b-a))/step)); out+= [a+(b-a)*t/n for t in range(n)]
    return np.array(out)
M=np.vstack([dens(outer)]+[dens(i) for i in inner])
# drop outer points that lie on the shoreward side only? keep all
c0=M.mean(0)
def tf(p,P):
    s,a,th,tx,ty=p; q=P-c0; c,sn=math.cos(th),math.sin(th); X=q[:,0]*s; Y=q[:,1]*s*a
    return np.c_[c*X-sn*Y+tx, sn*X+c*Y+ty]
def cost(p):
    s,a,th,tx,ty=p
    if not(0.5<s<1.2 and 0.85<a<1.15 and abs(th)<0.2): return 1e3
    q=tf(p,M); ins=(q[:,0]>=0)&(q[:,0]<W-1)&(q[:,1]>=0)&(q[:,1]<H-1)
    if ins.sum()<0.8*len(M): return 1e3
    d=ndimage.map_coordinates(dt,[q[ins,1],q[ins,0]],order=1)
    return float(np.mean(np.minimum(d,8)))
best=None
for s in np.arange(0.68,0.95,0.02):
    for tx in range(120,360,8):
        for ty in range(120,340,8):
            v=cost([s,1.0,0.0,tx,ty])
            if best is None or v<best[0]: best=(v,[s,1.0,0.0,tx,ty])
r=optimize.minimize(cost,best[1],method="Nelder-Mead",options={"xatol":1e-5,"fatol":1e-6,"maxiter":6000}); p=r.x
q=tf(p,M); d=ndimage.map_coordinates(dt,[q[:,1],q[:,0]],order=1)
print("grid best",best[0],"fit",[round(v,4) for v in p],"mean capped",round(cost(p),2),"frac<=1.5px",round(float((d<=1.5).mean()),3),"frac<=3px",round(float((d<=3).mean()),3))
# also isotropic (a=1, th=0 fixed) for the reported scale
def cost_iso(pp): return cost([pp[0],1.0,pp[1],pp[2],pp[3]])
r2=optimize.minimize(cost_iso,[p[0],p[2],p[3],p[4]],method="Nelder-Mead"); print("iso fit s,th,tx,ty",[round(v,4) for v in r2.x],"cost",round(r2.fun,2))
json.dump({"params_f2crop_to_f5a":p.tolist(),"c0_f2crop":c0.tolist(),"cost":cost(p),"frac_le_1.5px":float((d<=1.5).mean()),"frac_le_3px":float((d<=3).mean()),"iso":[float(v) for v in r2.x]},open(HERE+"/fig5a_register.json","w"))
vis=np.asarray(Image.open(G+"fig5a_reef_bathymetry_2011-06-09_native.jpeg").convert("RGB")).copy()
for x,y in q.astype(int):
    if 0<=x<W and 0<=y<H: cv2.circle(vis,(x,y),1,(255,0,255),-1)
Image.fromarray(vis).resize((W*2,H*2),Image.LANCZOS).save(os.environ.get("TEMP","/tmp")+"/fig5a_fit.png")
