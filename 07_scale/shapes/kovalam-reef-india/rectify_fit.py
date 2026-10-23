"""rectify_fit.py - kovalam-reef-india: single-photo rectification of the ASR aerial (img1) onto the 2011-02-28 Esri frame.
Run:  python rectify_fit.py            (writes rectify_result.json and overlays/*.png; ~2-4 min)
Method (see METHOD.md section 3): pinhole camera, zero roll, horizon row fixed from the photo, pitch from horizon and f; unknown camera
E, N, height H, azimuth, focal length f (px). Fit = distance of the photo's swash-line points to the satellite swash line projected through
the camera. H is NOT determined by the fit (rms flat for H 25-80 m) so it is fixed per hypothesis and swept.
Inputs: src/satellite_2014.png(+.geo.json) (= 2011-02-28 capture), src/img1_asr_aerial.png, pixel_polys_img1_v2.json. Written 2026-10-10."""
import numpy as np, json, math, os
from scipy.optimize import least_squares
from shapely.geometry import Polygon
from PIL import Image, ImageDraw
HERE=os.path.dirname(os.path.abspath(__file__))
geo=json.load(open(f'{HERE}/src/satellite_2014.png.geo.json')); b=geo['bounds']; W,Hh=geo['width'],geo['height']
LAT0,LON0=8.3885,76.9745
def merc_y(lat): return math.log(math.tan(math.pi/4+math.radians(lat)/2))
def px2ll(x,y):
    my=merc_y(b['north'])+(merc_y(b['south'])-merc_y(b['north']))*y/Hh
    return math.degrees(2*math.atan(math.exp(my))-math.pi/2), b['west']+(b['east']-b['west'])*x/W
def ll2en(lat,lon): return ((lon-LON0)*111320*math.cos(math.radians(LAT0)),(lat-LAT0)*110574)
def en2ll(e,n): return (LAT0+n/110574, LON0+e/(111320*math.cos(math.radians(LAT0))))
def ll2px(lat,lon):
    y=(merc_y(b['north'])-merc_y(lat))/(merc_y(b['north'])-merc_y(b['south']))*Hh; x=(lon-b['west'])/(b['east']-b['west'])*W; return x,y
# swash-line (landward edge of the surf foam) read by eye: satellite on 2x view coordinates (view/2 = native px), photo in img1 px
SAT_VIEW=[(392,212),(450,240),(520,290),(580,340),(640,395),(700,455),(750,520),(790,590),(808,660),(795,725),(785,760)]
sat=np.array([ll2en(*px2ll(x/2,y/2)) for x,y in SAT_VIEW])
def dens(p,n=200):
    d=np.r_[0,np.cumsum(np.hypot(*np.diff(p,axis=0).T))]; t=np.linspace(0,d[-1],n); return np.c_[np.interp(t,d,p[:,0]),np.interp(t,d,p[:,1])]
satd=dens(sat)
PHOTO=np.array([(405,284),(440,289),(480,294),(520,303),(560,318),(600,334),(640,352),(680,370),(720,386),(760,404),(800,424),(840,448),(880,478),(910,505)],float)
POLY=np.array(json.load(open(f'{HERE}/pixel_polys_img1_v2.json'))[0],float)
CX,CY,YH=467.,360.,191.
def cam(E,N,H,az,f,yh):
    p=math.atan((CY-yh)/f); a=math.radians(az)
    fwd=np.array([math.sin(a)*math.cos(p),math.cos(a)*math.cos(p),-math.sin(p)]); right=np.array([math.cos(a),-math.sin(a),0]); return fwd,right,np.cross(right,fwd)
def project(P,q,yh=YH):
    E,N,H,az,f=q; fwd,right,up=cam(E,N,H,az,f,yh); d=np.c_[P[:,0]-E,P[:,1]-N,-H*np.ones(len(P))]; z=d@fwd
    return np.c_[CX+f*(d@right)/z, CY-f*(d@up)/z], z
def unproject(px,q,yh=YH):
    E,N,H,az,f=q; fwd,right,up=cam(E,N,H,az,f,yh); out=[]
    for x,y in px:
        ray=fwd+((x-CX)/f)*right+((CY-y)/f)*up; t=H/(-ray[2]); out.append((E+t*ray[0],N+t*ray[1]))
    return np.array(out)
def resid(q,yh=YH,photo=PHOTO,sd=satd):
    pr,z=project(sd,q,yh)
    if (z<=1).any(): return np.ones(len(photo))*500
    r=[]
    for pt in photo:
        a=pr[:-1]; ab=pr[1:]-a; t=np.clip(((pt-a)*ab).sum(1)/np.maximum((ab**2).sum(1),1e-9),0,1); r.append(np.min(np.hypot(*(a+ab*t[:,None]-pt).T)))
    return np.array(r)
def canon(pts,shore=satd):
    c=pts.mean(0); i=int(np.argmin(np.hypot(*(shore-c).T))); t=shore[min(i+3,len(shore)-1)]-shore[max(i-3,0)]; t=t/np.hypot(*t)
    n=np.array([-t[1],t[0]]); n=-n if n[0]>0 else n   # offshore = away from land (west)
    d=pts-shore[i]; return np.c_[d@t,d@n],t,n,shore[i]
def fit_fixed_H(H,yh=YH,sd=satd,start=None,fs=(500,700,1050,1500),dds=(0,60,-60,-120),photo=PHOTO):
    q0=start or [174,-139,326,1050]; best=None
    for f0 in fs:
        for dd in dds:
            def r(p): return resid([p[0],p[1],H,p[2],p[3]],yh,photo,sd)
            try: s=least_squares(r,[q0[0]+dd*math.sin(math.radians(q0[2])),q0[1]+dd*math.cos(math.radians(q0[2])),q0[2]+dd/10,f0],bounds=([-600,-600,250,400],[600,600,380,3500]))
            except Exception: continue
            if best is None or s.cost<best.cost: best=s
    return [best.x[0],best.x[1],H,best.x[2],best.x[3]], math.sqrt(2*best.cost/len(photo))
def summary(q,yh=YH):
    en=unproject(POLY,q,yh); m,t,n,s0=canon(en); P=Polygon(m)
    return dict(q=[round(float(v),2) for v in q],area_m2=round(P.area),along_m=round(float(np.ptp(m[:,0]))),cross_m=round(float(np.ptp(m[:,1]))),
                off_min=round(float(m[:,1].min())),off_mean=round(float(m[:,1].mean())),off_max=round(float(m[:,1].max())),fov_deg=round(2*math.degrees(math.atan(447/q[4])),1))
if __name__=='__main__':
    res={'method':'see docstring','swash_pairs':{'photo_px':PHOTO.tolist(),'sat_view2x_px':SAT_VIEW}}
    # 1 global multi-start at H free (coarse) is documented in METHOD.md; here sweep H
    sweep=[]
    for H in (30,35,40,45,50,55,60,65,70,80,90,100):
        q,rms=fit_fixed_H(H); s=summary(q); s['H']=H; s['rms_px']=round(rms,2); sweep.append(s); print(s)
    res['H_sweep']=sweep
    HSEL=60.0
    qsel,rms=fit_fixed_H(HSEL); res['selected']=dict(summary(qsel),H=HSEL,rms_px=round(rms,2))
    # sensitivity at selected H: horizon row +-6 px; satellite swash line shifted 10 m landward/seaward; photo swash points +-8 px
    sens=[]
    for dy in (-6,6):
        q,r=fit_fixed_H(HSEL,yh=YH+dy,start=[qsel[0],qsel[1],qsel[3],qsel[4]]); s=summary(q,YH+dy); s.update(case=f'horizon row {YH+dy}',rms_px=round(r,2)); sens.append(s)
    for dm in (-10,10):
        tt=satd.copy(); c=satd.mean(0)
        _,tg,nn,_=canon(satd[:1]); # offshore normal at first point
        sd=satd+dm*nn; q,r=fit_fixed_H(HSEL,sd=sd,start=[qsel[0],qsel[1],qsel[3],qsel[4]])
        en=unproject(POLY,q); m,_,_,_=canon(en); s=summary(q); s.update(case=f'satellite swash line moved {dm} m offshore',rms_px=round(r,2)); sens.append(s)
    res['sensitivity']=sens
    # geometry of the selected solution
    en=unproject(POLY,qsel); m,t,n,s0=canon(en)
    res['canonical_polygon_m']=[[round(float(x),1),round(float(y),1)] for x,y in m]
    res['polygon_latlon']=[[round(v,6) for v in en2ll(*p)] for p in en]
    res['frame']=dict(origin_latlon=[round(v,6) for v in en2ll(*s0)],x_bearing_deg=round(math.degrees(math.atan2(t[0],t[1]))%360,1),y_bearing_deg=round(math.degrees(math.atan2(n[0],n[1]))%360,1))
    res['camera_latlon']=[round(v,6) for v in en2ll(qsel[0],qsel[1])]
    # strip direction: top edge (vertex 0->5 of POLY) and bottom edge (vertices 10->15) rectified, bearing vs shoreline tangent
    def edge_angle(i,j):
        e=unproject(POLY[[i,j]],qsel); v=e[1]-e[0]; ang=math.degrees(math.atan2(v[0],v[1]))%360; return ang
    tb=math.degrees(math.atan2(t[0],t[1]))%360
    res['strip_edges']={'top_edge_bearing':round(edge_angle(0,5),1),'bottom_edge_bearing':round(edge_angle(15,10),1),'shoreline_tangent_bearing':round(tb,1)}
    json.dump(res,open(f'{HERE}/rectify_result.json','w'),indent=1)
    # overlay 1: photo
    im=Image.open(f'{HERE}/src/img1_asr_aerial.png').convert('RGB'); d=ImageDraw.Draw(im)
    pr,z=project(satd,qsel); d.line([tuple(p) for p in pr],fill=(0,255,255),width=2)
    for p in PHOTO: d.ellipse([p[0]-4,p[1]-4,p[0]+4,p[1]+4],outline=(255,255,0),width=2)
    d.line([tuple(p) for p in POLY]+[tuple(POLY[0])],fill=(255,40,40),width=2)
    d.line([(20,YH),(915,YH)],fill=(255,255,255),width=1); d.text((24,YH-12),'horizon row 191 (read from photo)',fill=(255,255,255))
    d.text((30,20),'cyan = 2011 satellite swash line projected through fitted camera; yellow = swash points read on photo; red = traced strips',fill=(255,255,255))
    im.save(f'{HERE}/overlays/img1_camera_fit_check.png')
    # overlay 2: satellite plan
    sat_im=Image.open(f'{HERE}/src/satellite_2014.png').convert('RGB').resize((W*2,Hh*2),Image.LANCZOS); d=ImageDraw.Draw(sat_im)
    def sp(e,n): x,y=ll2px(*en2ll(e,n)); return (x*2,y*2)
    d.line([sp(*p) for p in satd],fill=(0,255,255),width=2)
    d.polygon([sp(*p) for p in en],outline=(255,40,40)); d.line([sp(*p) for p in en]+[sp(*en[0])],fill=(255,40,40),width=3)
    c=sp(qsel[0],qsel[1]); d.ellipse([c[0]-6,c[1]-6,c[0]+6,c[1]+6],fill=(255,255,0)); d.text((c[0]+8,c[1]-4),f'camera (fitted, H={HSEL:.0f} m assumed)',fill=(255,255,0))
    mpp=1.1815512/2; L=50/mpp; x0,y0=40,sat_im.height-40; d.line([(x0,y0),(x0+L,y0)],fill=(255,255,255),width=4); d.text((x0,y0-16),'50 m (z17, 1.18 m/px native)',fill=(255,255,255))
    d.text((20,14),'Esri World Imagery Wayback 2011-02-28; red = reef strips rectified (LOW confidence); cyan = swash line used for the fit',fill=(255,255,255))
    sat_im.save(f'{HERE}/overlays/sat2011_plan_reconstruction.png')
    print(json.dumps({k:res[k] for k in ('selected','frame','camera_latlon','strip_edges')}))
