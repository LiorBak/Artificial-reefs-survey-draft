"""navionics_polys.py (verifier 2026-10-07): polygons of the Navionics SonarChart shoal contours around Narrowneck from the saved screenshots
src/navionics/sonar_z18_shade00.0.png (contour lines) and sonar_z18_shade04.0.png (area shallower than 4 m filled blue).
Georeference ASSUMPTION (same as the tracer): map centre = reef centroid (-27.986629, 153.434052) = image centre pixel, z18 Web-Mercator
0.5273 m/px (0.597164 * cos(lat)).  This is only good to ~20 m: the app does not show coordinates in the screenshot.
Writes navionics_polys.json (canonical metres + lat/lon)."""
import numpy as np, cv2, json, math, os
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
N=ROOT+"/src/navionics/"
lat0,lon0=-27.986629,153.434052
mpp=0.597164*math.cos(math.radians(lat0))
im4=np.asarray(Image.open(N+"sonar_z18_shade04.0.png").convert("RGB")).astype(int)
H,W,_=im4.shape; cx,cy=W/2,H/2
# line mask: dark grey/black thin lines (not magenta symbols, not red dots)
line=((im4.max(axis=2)<110)).astype(np.uint8)
blue=((np.abs(im4[...,0]-190)<25)&(np.abs(im4[...,1]-225)<20)&(im4[...,2]>235)).astype(np.uint8)
n,lab,st,cen=cv2.connectedComponentsWithStats(blue,8)
shoals=[(int(st[i,4]),tuple(cen[i])) for i in range(1,n) if 80<st[i,4]<5000]
print("blue shoals (area px, centroid)",shoals)
def loop_from_seed(seed):
    free=(1-cv2.dilate(line,np.ones((3,3),np.uint8))).astype(np.uint8)
    n2,lab2,st2,_=cv2.connectedComponentsWithStats(free,4)
    l=lab2[seed[1],seed[0]]; reg=(lab2==l).astype(np.uint8)
    return reg,int(st2[l,4])
out={}
def to_m(pts):
    # pts px -> east/north metres from map centre -> canonical
    E=(pts[:,0]-cx)*mpp; Nn=-(pts[:,1]-cy)*mpp
    # canonical origin = lat -27.986800, lon 153.431127
    olat,olon=-27.986800,153.431127
    E0=math.radians(lon0-olon)*6378137*math.cos(math.radians(lat0)); N0=math.radians(lat0-olat)*6378137
    E+=E0; Nn+=N0
    b=math.radians(356.212)
    x=E*math.sin(b)+Nn*math.cos(b); y=E*math.sin(b+math.pi/2)+Nn*math.cos(b+math.pi/2)
    return np.c_[x,y]
def to_ll(pts):
    E=(pts[:,0]-cx)*mpp; Nn=-(pts[:,1]-cy)*mpp
    return [[lat0+math.degrees(n_/6378137), lon0+math.degrees(e/(6378137*math.cos(math.radians(lat0))))] for e,n_ in zip(E,Nn)]
res=[]
for name,seed in [("N_arm_4.5m_loop",(456,297)),("S_arm_4.5m_loop",(441,437))]:
    reg,a=loop_from_seed(seed); print(name,"region px",a)
    cn,_=cv2.findContours(reg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); c=max(cn,key=cv2.contourArea)[:,0,:].astype(np.float32)
    ap=cv2.approxPolyDP(c.reshape(-1,1,2),1.2,True)[:,0,:].astype(float)
    res.append((name,"4.5",ap))
# 4.0 m shoals from blue
for i in range(1,n):
    if 80<st[i,4]<5000:
        cn,_=cv2.findContours((lab==i).astype(np.uint8),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); c=max(cn,key=cv2.contourArea)[:,0,:].astype(np.float32)
        ap=cv2.approxPolyDP(c.reshape(-1,1,2),1.0,True)[:,0,:].astype(float)
        res.append(("shoal_4.0m_%s"%("N" if cen[i][1]<cy else "S"),"4.0",ap))
from shapely.geometry import Polygon
for name,lev,ap in res:
    m=to_m(ap); pg=Polygon(m)
    out[name]={"level_m":float(lev),"canonical_m":m.round(2).tolist(),"latlon":[[round(a,7),round(b,7)] for a,b in to_ll(ap)],"area_m2":pg.area,"bounds":[round(v,1) for v in pg.bounds],"centroid_m":[round(v,1) for v in pg.centroid.coords[0]]}
    print(name,"area m2",round(pg.area),"bounds",out[name]["bounds"],"centroid",out[name]["centroid_m"])
json.dump(out,open(HERE+"/navionics_polys.json","w"))
