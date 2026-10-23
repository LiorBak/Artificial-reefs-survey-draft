"""option2_outline.py (2026-10-10): Corbett et al. 2023 Fig 2 (src/gov/corbett2023_extracted/p3_x88.png) -> polygons in the canonical frame.
Left panel = Option 1 (= 2004 modified design), right panel = Option 2 (built 2018; grey = Option 1). Panel offset right->left = 358 px: Option 1 grey silhouette in the right panel fits the left panel at dx=352 (coverage fit; S dy -7, N dy -18) and 363 px if the text 20 m seaward shift is exact; NOT the crop offset 404 (panel crops
x 10-354 / 414-760; N-loop centroids 401.6, line fit 395-408 => +-6 px = +-3 m).  Mapping Corbett left px -> Jackson 2012 Fig 2-right crop px:
verify_scripts/corbett_scale/c3_fit.json (chamfer fit, s=1.504); then Jackson crop px (+X0=1020) -> Fig 7 px -> s3 px -> canonical as in
design_outline_2004.py.  Also the Option 1 panel is processed as a closure test against design_outline_2004.json.  Output: option2_outline.json"""
import numpy as np, cv2, json, os, math
from PIL import Image
from shapely.geometry import Polygon
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(os.path.dirname(HERE))
cb=np.asarray(Image.open(ROOT+"/src/gov/corbett2023_extracted/p3_x88.png").convert("RGB")).astype(int)
H,W,_=cb.shape; sat=cb.max(2)-cb.min(2)
OFF=358; X0=1020   # OFF = where Option 1 (grey, right panel) sits relative to the left panel: grey-fit 352 px (step2_grey_blobs), 363 px if the text 20 m seaward shift is exact; crop offset 404 would be WRONG (it puts Option 2 on Option 1)
fitj=json.load(open(HERE+"/../corbett_scale/c3_fit.json")); s,a,th,tx,ty=fitj["fit"]; c0=np.array(fitj["c0"])
T=np.array(json.load(open(ROOT+"/design_registration_out.json"))["fig7_px_to_s3_px_affine"])
# Fig 2 crop px -> Fig 7 px (fit from design_outline_2004.json)
f27=json.load(open(ROOT+"/verify_scripts/design_outline_2004.json"))["fit_fig2_to_fig7"]
c27=np.array(f27["c0"])
def tf(P,c0_,s_,a_,th_,tx_,ty_):
    q=P-c0_; c,sn=math.cos(th_),math.sin(th_); X=q[:,0]*s_; Y=q[:,1]*s_*a_
    return np.c_[c*X-sn*Y+tx_, sn*X+c*Y+ty_]
b=math.radians(356.212); u=np.array([math.sin(b),-math.cos(b)]); nn=np.array([math.sin(b+math.pi/2),-math.cos(b+math.pi/2)])
org=np.array([-517.90,821.74]); mpp=0.263665
def chain(Pc, panel):
    """Pc: Corbett px (full image) of the given panel -> canonical metres"""
    if panel=="R": Pc=Pc-np.array([OFF,0.0])
    Pj=tf(Pc,c0,s,a,th,tx,ty)                     # Jackson Fig 2-right crop px
    Pj=Pj+np.array([X0,0.0])                      # full Fig 2 image px
    P7=tf(Pj,c27,f27["s"],f27["aspect"],f27["theta"],f27["tx"],f27["ty"])
    h=np.c_[P7,np.ones(len(P7))]@T.T; rel=h[:,:2]-org
    return np.c_[rel@u*mpp, rel@nn*mpp]
def masks(x0,x1):
    line=((sat>=35)|(cb.min(2)<150)).astype(np.uint8)
    m=np.zeros_like(line); m[14:320,x0:x1]=line[14:320,x0:x1]
    if x0>400: m[262:,600:760]=0                    # scale bar + numbers
    return m
def outer_boundary(m,r_=15):
    n,lab,st,_=cv2.connectedComponentsWithStats(m,8); keep=np.zeros_like(m)
    for i in range(1,n):
        if st[i,4]>=60: keep[lab==i]=1
    pad=40
    cl=cv2.morphologyEx(np.pad(keep,pad),cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*r_+1,2*r_+1)))
    n2,lab2,_,_=cv2.connectedComponentsWithStats((1-cl).astype(np.uint8),4); M=(lab2!=lab2[0,0]).astype(np.uint8)[pad:-pad,pad:-pad]
    cc,_=cv2.findContours(M,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); c=max(cc,key=cv2.contourArea)
    return cv2.approxPolyDP(c,1.5,True)[:,0,:].astype(float)
def crest_loops(x0,x1):
    blk=((cb.max(2)<140)&(sat<40)).astype(np.uint8); mm=np.zeros_like(blk); mm[14:320,x0:x1]=blk[14:320,x0:x1]
    if x0>400: cv2.line(mm,(488,270),(517,258),1,1)   # HAND PATCH (+-2 px): bottom edge of the Option 2 south crest loop is broken by the '-3.0m' label
    mm=cv2.dilate(mm,np.ones((3,3),np.uint8))
    n,lab,st,cen=cv2.connectedComponentsWithStats(1-mm,4); res=[]
    for i in range(1,n):
        x,y,w,h,ar=st[i]
        if 1500<ar<9000 and x>x0+3 and x+w<x1-3 and y>15 and y+h<300:
            reg=cv2.morphologyEx((lab==i).astype(np.uint8),cv2.MORPH_CLOSE,np.ones((9,9),np.uint8)); reg=cv2.dilate(reg,np.ones((7,7),np.uint8))   # back out to the line centre (dilate 3 px each side: line mask was thickened by 1 + half line width)
            cc,_=cv2.findContours(reg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); c=max(cc,key=cv2.contourArea)
            res.append(cv2.approxPolyDP(c,1.2,True)[:,0,:].astype(float))
    return res
out={"panel_offset_px":OFF,"m_per_px_bar":0.5155}
for panel,(x0,x1) in (("L",(10,354)),("R",(414,760))):
    ob=outer_boundary(masks(x0,x1)); cl=crest_loops(x0,x1)
    d={"outer_-6.0":None,"crest_-2.5":[]}
    mo=chain(ob,panel); P=Polygon(mo).buffer(0); d["outer_-6.0"]={"canonical_m":mo.round(2).tolist(),"area_m2":P.area,"bounds":[round(v,1) for v in P.bounds]}
    for lp in cl:
        m_=chain(lp,panel); Q=Polygon(m_).buffer(0); d["crest_-2.5"].append({"canonical_m":m_.round(2).tolist(),"area_m2":Q.area,"centroid":[round(Q.centroid.x,1),round(Q.centroid.y,1)],"minrect_m":None})
        r=cv2.minAreaRect(lp.astype(np.float32)); d["crest_-2.5"][-1]["minrect_m_bar"]=[round(r[1][0]*0.5155,1),round(r[1][1]*0.5155,1)]
        d["crest_-2.5"][-1]["area_m2_bar"]=round(cv2.contourArea(lp.astype(np.float32))*0.5155**2,0)
    out[panel]=d
    print(panel,"outer -6 area (chain m2)",round(P.area),"bounds",d["outer_-6.0"]["bounds"],"loops",[(round(q["area_m2"]),q["centroid"],q["area_m2_bar"],q["minrect_m_bar"]) for q in d["crest_-2.5"]])
ref=json.load(open(ROOT+"/verify_scripts/design_outline_2004.json"))
Pref=Polygon(ref["outer_-6.0"]["canonical_m"]).buffer(0); PL=Polygon(out["L"]["outer_-6.0"]["canonical_m"]).buffer(0)
print("closure: Option1 panel vs 2004 design -6: area",round(PL.area),"vs",round(Pref.area),"IoU",round(PL.intersection(Pref).area/PL.union(Pref).area,3))
for q in ref["inner_-2.5"]: print(" 2004 crest loop",round(q["area_m2"]),[round(v,1) for v in Polygon(q["canonical_m"]).centroid.coords[0]])
json.dump(out,open(HERE+"/option2_outline.json","w"))
