"""design_outline_2004.py (verifier, 2026-10-07): polygons of the 2004 revised design (Jackson et al. 2012 Fig 2 right = same CAD drawing as the
contours on Fig 7) placed on the s3 image and in the canonical frame.
Steps: (1) chamfer fit of the Fig 2-right line drawing onto the white contour lines of Fig 7 (similarity+aspect; residual ~1 px, 93 % of line
points within 2.5 px); (2) outer boundary of the nested contour group = the -6.0 m contour (label gaps bridged by closing r=18; -8.00 envelope
line erased first; one label notch patched by hand); closed inner loops = the -2.5 m crest contours; (3) Fig 7 px -> s3 px with design_registration_out.json
(0.21 m/px +-10 %, ends +-15 m); (4) s3 px -> canonical metres (origin px (-517.90,821.74), 356.212 deg).
Writes design_outline_2004.json next to this script.  Needs numpy, opencv-python, scipy, scikit-image, pillow."""
import numpy as np, cv2, json, os, math
from PIL import Image
from scipy import ndimage, optimize
from skimage.morphology import skeletonize
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
G=ROOT+"/src/gov/narrowneck-gold-coast_jackson2012_"
f2=np.asarray(Image.open(G+"fig2_reef_levels_original_and_revised_design_300dpi_crop.png").convert("L"))
X0=1020; f2r=f2[:,X0:]
f7=np.asarray(Image.open(G+"fig7_overlay_2011-07_aerial_with_design_contours_and_containers_native.jpeg").convert("RGB"))
# (1) chamfer fit
white=(f7.min(axis=2)>185); dt7=ndimage.distance_transform_edt(~white); H7,W7=dt7.shape
sk=skeletonize(f2r<120); py,px=np.where(sk); pts=np.c_[px+X0,py].astype(float); c0=pts.mean(0)
def tf(p,s,a,th,tx,ty,P=None):
    P=pts if P is None else P
    q=P-c0; c,sn=math.cos(th),math.sin(th); X=q[:,0]*s; Y=q[:,1]*s*a
    return np.c_[c*X-sn*Y+tx, sn*X+c*Y+ty]
def cost(p):
    s,a,th,tx,ty=p
    if not(0.2<s<3 and 0.7<a<1.4 and abs(th)<0.3): return 1e3
    q=tf(None,s,a,th,tx,ty); ins=(q[:,0]>=0)&(q[:,0]<W7-1)&(q[:,1]>=0)&(q[:,1]<H7-1)
    if ins.sum()<0.35*len(pts): return 1e3
    d=ndimage.map_coordinates(dt7,[q[ins,1],q[ins,0]],order=1)
    return float(np.mean(np.minimum(d,10))+2.0*(1-ins.mean()))
P0=[1.55,1.0,0.0,550,400]
r=optimize.minimize(cost,P0,method="Nelder-Mead",options={"xatol":1e-4,"fatol":1e-5,"maxiter":4000}); prm=r.x
q=tf(None,*prm); ins=(q[:,0]>=0)&(q[:,0]<W7-1)&(q[:,1]>=0)&(q[:,1]<H7-1)
d=ndimage.map_coordinates(dt7,[q[ins,1],q[ins,0]],order=1)
fit={"s":prm[0],"aspect":prm[1],"theta":prm[2],"tx":prm[3],"ty":prm[4],"c0":c0.tolist(),"median_chamfer_px":float(np.median(d)),"frac_inside":float(ins.mean()),"frac_within_2.5px":float((d<2.5).mean()),"frac_within_1.5px":float((d<1.5).mean())}
print("fit",{k:(round(v,4) if isinstance(v,float) else v) for k,v in fit.items() if k!="c0"})
# (2) outer -6.0 boundary
dark=(f2r<150).astype(np.uint8); H,W=dark.shape; yy,xx=np.mgrid[0:H,0:W]
dark[:,500:]=0; dark[(xx>238)&(np.abs(yy-(45+0.157*(xx-230)))<7)]=0; dark[(yy>527)&(xx>195)]=0
n,lab,st,_=cv2.connectedComponentsWithStats(dark,8); keep=np.zeros_like(dark)
for i in range(1,n):
    if st[i,4]>=150: keep[lab==i]=1
pad=40; r_=18
cl=cv2.morphologyEx(np.pad(keep,pad),cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*r_+1,2*r_+1)))
n2,lab2,st2,_=cv2.connectedComponentsWithStats((1-cl).astype(np.uint8),4); M=(lab2!=lab2[0,0]).astype(np.uint8)
patch=np.array([(258,466),(262,490),(281,481.5),(301,471),(300,462),(280,455),(262,458)],float)   # label notch of the S flank
Mp=np.pad(M,0)[pad:-pad,pad:-pad].copy(); cv2.fillPoly(Mp,[np.round(patch).astype(np.int32)],1)
cn,_=cv2.findContours(Mp,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); outer=max(cn,key=cv2.contourArea)[:,0,:].astype(float)
outer_s=cv2.approxPolyDP(outer.astype(np.float32).reshape(-1,1,2),1.5,True)[:,0,:].astype(float)
# closed inner loops (-2.5 contours): label gaps bridged with closing r=16 on the line mask (-8.00 envelope removed)
dk2=(f2r<150).astype(np.uint8); dk2[:,500:]=0
n,lab,st,_=cv2.connectedComponentsWithStats(dk2,8); kp2=np.zeros_like(dk2)
for i in range(1,n):
    if st[i,4]>=150: kp2[lab==i]=1
cl2=cv2.morphologyEx(np.pad(kp2,pad),cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(33,33)))
n3,lab3,st3,cen3=cv2.connectedComponentsWithStats((1-cl2).astype(np.uint8),4)
inner=[]
for i in range(1,n3):
    cx,cy=cen3[i]-pad
    if 5000<st3[i,4]<20000 and cx<260 and (cy<250 or cy>350):
        reg=cv2.dilate((lab3==i).astype(np.uint8),np.ones((3,3),np.uint8))[pad:-pad,pad:-pad]
        cc,_=cv2.findContours(reg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        c=max(cc,key=cv2.contourArea)[:,0,:].astype(np.float32)
        inner.append(cv2.approxPolyDP(c.reshape(-1,1,2),1.5,True)[:,0,:].astype(float))
print("outer vertices",len(outer_s),"inner loops",len(inner),[len(i) for i in inner])
# (3),(4) transforms
T=np.array(json.load(open(ROOT+"/design_registration_out.json"))["fig7_px_to_s3_px_affine"])
b=math.radians(356.212); u=np.array([math.sin(b),-math.cos(b)]); nn=np.array([math.sin(b+math.pi/2),-math.cos(b+math.pi/2)])
org=np.array([-517.90,821.74]); mpp=0.263665
geo=json.load(open(ROOT+"/src/wayback/nn_wayback_2020-08-08_r9812_z19.png.geo.json"))["bounds"]
def my(lat): return math.log(math.tan(math.pi/4+math.radians(lat)/2))
def px2ll(x,y):
    lon=geo["west"]+x/1517*(geo["east"]-geo["west"]); m=my(geo["north"])+y/1517*(my(geo["south"])-my(geo["north"]))
    return math.degrees(2*math.atan(math.exp(m))-math.pi/2),lon
def chain(P2):                                  # P2: Fig 2 full-image px (x already includes X0)
    P7=tf(None,*prm,P=P2); h=np.c_[P7,np.ones(len(P7))]@T.T; s3=h[:,:2]; rel=s3-org
    return s3,np.c_[rel@u*mpp,rel@nn*mpp]
from shapely.geometry import Polygon
out={"fit_fig2_to_fig7":fit,"patch_fig2_px":patch.tolist()}
s3o,mo=chain(outer_s+np.array([X0,0]))
out["outer_-6.0"]={"s3_px":s3o.round(1).tolist(),"canonical_m":mo.round(2).tolist(),"latlon":[list(px2ll(*p)) for p in s3o],"area_m2":Polygon(mo).area}
out["inner_-2.5"]=[]
for lp in inner:
    s3i,mi=chain(lp+np.array([X0,0])); out["inner_-2.5"].append({"canonical_m":mi.round(2).tolist(),"s3_px":s3i.round(1).tolist(),"latlon":[list(px2ll(*p)) for p in s3i],"area_m2":Polygon(mi).area})
pg=Polygon(mo); print("outer -6.0 area m2",round(pg.area),"bounds",[round(v,1) for v in pg.bounds],"inner areas",[round(i['area_m2']) for i in out["inner_-2.5"]])
json.dump(out,open(HERE+"/design_outline_2004.json","w"))
