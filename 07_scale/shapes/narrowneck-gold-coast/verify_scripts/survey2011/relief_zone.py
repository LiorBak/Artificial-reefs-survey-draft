"""relief_zone.py (2026-10-10): digitise the dense-contour relief zone of Jackson et al. 2012 Fig 5a (GCCC bathymetric survey 2011-06-09).
Fig 5a has no depth legend, so only a RELIEF ZONE (where the seabed varies strongly = reef containers) can be outlined, not a depth contour.
Method: contour pixels = coloured (saturation>=28; red/green/blue/purple contours); thick black design loops and grid excluded; density in a
13x13 px window; zone = density > thr, closed r=5, small blobs dropped, largest 2 components (N and S reef) kept.  Fig 5a px -> Fig 2 crop px by the
inverse of fig5a_register.json (params_f2crop_to_f5a) -> Fig 7 -> s3 -> canonical (design_outline_2004.py chain).  Writes relief_zone.json."""
import numpy as np, cv2, json, os, math
from PIL import Image
from shapely.geometry import Polygon
from shapely.ops import unary_union
HERE=os.path.dirname(os.path.abspath(__file__)); V=os.path.dirname(HERE); ROOT=os.path.dirname(V)
f5=np.asarray(Image.open(ROOT+"/src/gov/narrowneck-gold-coast_jackson2012_fig5a_reef_bathymetry_2011-06-09_native.jpeg").convert("RGB")).astype(int)
H,W,_=f5.shape; sat=f5.max(2)-f5.min(2)
col=(sat>=28).astype(np.float32)
res={}
reg=json.load(open(V+"/fig5a_register.json")); s,a,th,tx,ty=reg["params_f2crop_to_f5a"]; c0=np.array(reg["c0_f2crop"])
def f5_to_f2crop(P):
    q=np.asarray(P,float)-[tx,ty]; c,sn=math.cos(-th),math.sin(-th); q=np.c_[c*q[:,0]-sn*q[:,1],sn*q[:,0]+c*q[:,1]]
    return np.c_[q[:,0]/s,q[:,1]/(s*a)]+c0
f27=json.load(open(V+"/design_outline_2004.json"))["fit_fig2_to_fig7"]; c27=np.array(f27["c0"])
T=np.array(json.load(open(ROOT+"/design_registration_out.json"))["fig7_px_to_s3_px_affine"])
def tf(P,c0_,s_,a_,th_,tx_,ty_):
    q=P-c0_; c,sn=math.cos(th_),math.sin(th_); X=q[:,0]*s_; Y=q[:,1]*s_*a_
    return np.c_[c*X-sn*Y+tx_, sn*X+c*Y+ty_]
b=math.radians(356.212); u=np.array([math.sin(b),-math.cos(b)]); nn=np.array([math.sin(b+math.pi/2),-math.cos(b+math.pi/2)]); org=np.array([-517.90,821.74]); mpp=0.263665
def chain(P5):
    P2=f5_to_f2crop(P5)+np.array([1020.0,0]); P7=tf(P2,c27,f27["s"],f27["aspect"],f27["theta"],f27["tx"],f27["ty"])
    h=np.c_[P7,np.ones(len(P7))]@T.T; rel=h[:,:2]-org; return np.c_[rel@u*mpp,rel@nn*mpp]
dens=cv2.blur(col,(13,13))
out={}
for thr in (0.10,0.14,0.18):
    m=(dens>thr).astype(np.uint8); m[:, :60]=0; m[:,560:]=0   # shore-parallel natural contours at the sides are not reef
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11)))
    n,lab,st,cen=cv2.connectedComponentsWithStats(m,8)
    comps=sorted([(st[i,4],i) for i in range(1,n)],reverse=True)[:2]
    polys=[]
    for ar_,i in comps:
        mm=(lab==i).astype(np.uint8); cc,_=cv2.findContours(mm,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); c=max(cc,key=cv2.contourArea)
        c=cv2.approxPolyDP(c,1.5,True)[:,0,:].astype(float); polys.append((c,chain(c)))
    areas=[Polygon(p[1]).buffer(0).area for p in polys]
    out[thr]={"areas_m2":[round(x) for x in areas],"total_m2":round(sum(areas)),"bounds":[[round(v,1) for v in Polygon(p[1]).buffer(0).bounds] for p in polys],"f5_px":[p[0].round(1).tolist() for p in polys],"canonical_m":[p[1].round(2).tolist() for p in polys]}
    print("thr",thr,"areas m2",out[thr]["areas_m2"],"total",out[thr]["total_m2"],"bounds",out[thr]["bounds"])
    vis=f5.astype(np.uint8).copy(); cv2.drawContours(vis,[np.round(p[0]).astype(np.int32).reshape(-1,1,2) for p in polys],-1,(255,0,255),2)
    Image.fromarray(vis).save("/tmp/w/rz_%s.png"%thr)
json.dump(out,open(HERE+"/relief_zone.json","w"))
