"""faint_patches.py (2026-10-10): recompute the faint seaward dark patches (VERIFY check 1 recipe): G channel of s3, gaussian blur 2 px, local water
background = normalised gaussian (sigma 30 px) excluding the traced polygons (dilated 6 px), patch = background - G > 4 DN, >= 10 m2, seaward of x... Writes faint_patches.json."""
import numpy as np, cv2, json, os, math
from PIL import Image
from scipy import ndimage
from shapely.geometry import Polygon
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(os.path.dirname(HERE))
im=np.asarray(Image.open(ROOT+"/src/wayback/nn_wayback_2020-08-08_r9812_z19.png").convert("RGB")).astype(np.float32); G=im[...,1]
sh=json.load(open(ROOT+"/shape.json")); pp=[s for s in sh["sources"] if s.get("id")=="s3"][0]["pixel_polygons"]
if isinstance(pp,dict): pp=list(pp.values())
mask=np.zeros(G.shape,np.uint8)
for p in pp:
    if isinstance(p,dict): p=p.get("pixel") or p.get("polygon")
    cv2.fillPoly(mask,[np.round(np.array(p)).astype(np.int32)],1)
mask=cv2.dilate(mask,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13,13)))
g=cv2.GaussianBlur(G,(0,0),2); w=(1-mask).astype(np.float32)
bg=cv2.GaussianBlur(g*w,(0,0),30)/np.maximum(cv2.GaussianBlur(w,(0,0),30),1e-3)
diff=bg-g; m=((diff>4)&(mask==0)).astype(np.uint8)
m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((2,2),np.uint8))
n,lab,st,cen=cv2.connectedComponentsWithStats(m,8)
mpp=0.263665; b=math.radians(356.212); u=np.array([math.sin(b),-math.cos(b)]); nn=np.array([math.sin(b+math.pi/2),-math.cos(b+math.pi/2)]); org=np.array([-517.90,821.74])
out=[]
for i in range(1,n):
    a_m2=st[i,4]*mpp**2
    if a_m2<10: continue
    cc,_=cv2.findContours((lab==i).astype(np.uint8),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); c=max(cc,key=cv2.contourArea)[:,0,:].astype(float)
    if len(c)<3: continue
    c=cv2.approxPolyDP(c.astype(np.float32).reshape(-1,1,2),1.0,True)[:,0,:].astype(float)
    rel=c-org; mc=np.c_[rel@u*mpp,rel@nn*mpp]
    out.append({"area_m2":round(float(a_m2),1),"mean_diff_DN":round(float(diff[lab==i].mean()),1),"centroid_m":[round(float(v),1) for v in Polygon(mc).buffer(0).centroid.coords[0]],"canonical_m":mc.round(2).tolist()})
out.sort(key=lambda o:o["centroid_m"][1])
print("patches",len(out),"total m2",round(sum(o["area_m2"] for o in out)),"y range",min(o["centroid_m"][1] for o in out) if out else None,max(o["centroid_m"][1] for o in out) if out else None, "x",[o["centroid_m"][0] for o in out][:3])
json.dump(out,open(HERE+"/faint_patches.json","w"))
