import json, math, numpy as np
from shapely.geometry import Polygon
R=6378137.0
base=r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git\07_scale\shapes\borth-coastal-defence-reef"
sh=json.load(open(base+r"\shape.json",encoding='utf-8'))
def geo(f): return json.load(open(base+r"\src\\"+f+".geo.json"))
g24=geo("borth_esri_2024-09-17_z19.png"); gsh=geo("borth_shoreline_z19.png")
def merc(lat,lon): return R*math.radians(lon), R*math.log(math.tan(math.pi/4+math.radians(lat)/2))
def imerc(x,y): return math.degrees(2*math.atan(math.exp(y/R))-math.pi/2), math.degrees(x/R)
def pix2ll(g,x,y):
    b=g['bounds']; w,h=g['width'],g['height']
    xw,yn=merc(b['north'],b['west']); xe,ys=merc(b['south'],b['east'])
    # (note merc returns (x,y) with args (lat,lon))
    mx=xw+x/w*(xe-xw); my=yn+y/h*(ys-yn)
    return imerc(mx,my)
# independent scale check
for g in (g24,gsh):
    b=g['bounds']; xw,yn=merc(b['north'],b['west']); xe,ys=merc(b['south'],b['east'])
    lat0=(b['north']+b['south'])/2
    mpp_x=(xe-xw)/g['width']*math.cos(math.radians(lat0)); mpp_y=(yn-ys)/g['height']*math.cos(math.radians(lat0))
    # true ground distance: lat span
    ground_h=math.radians(b['north']-b['south'])*R/g['height']
    ground_w=math.radians(b['east']-b['west'])*R*math.cos(math.radians(lat0))/g['width']
    print(g['image'],'m/px (merc*cos)',round(mpp_x,5),round(mpp_y,5),'ground lat-span',round(ground_h,5),'lon-span',round(ground_w,5),'-> px/m',round(1/mpp_x,4))
# shoreline fit in satshore
pts=[(1795,1100),(1800,1500),(1803,2000),(1805,2500),(1808,2600)]
ll=[pix2ll(gsh,*p) for p in pts]
lat0,lon0=52.4832,-4.0562
def loc(lat,lon): return (math.radians(lon-lon0)*R*math.cos(math.radians(lat0)), math.radians(lat-lat0)*R)
E=np.array([loc(*p) for p in ll])
c=E.mean(0); u,s,vt=np.linalg.svd(E-c); d=vt[0]
if d[1]<0: d=-d
brg=(math.degrees(math.atan2(d[0],d[1]))+360)%360
print('defence-line bearing (via TLS in local metres)',round(brg,3))
res=[abs(np.cross(d,e-c)) for e in E]; print('residuals m',[round(r,2) for r in res])
# frame: +x along d (north), +y offshore = d rotated 90deg CCW (west): n=(-d1,d0)... for d=(sin b,cos b), west normal = (-cos b, sin b)
n=np.array([-d[1],d[0]])
print('offshore bearing',round((math.degrees(math.atan2(n[0],n[1]))+360)%360,3))
polys=sh['sources'][0]['pixel_polygons']
P=[]
allpts=[]
for poly in polys:
    m=np.array([loc(*pix2ll(g24,x,y)) for x,y in poly]); P.append(m); allpts.append(m)
allm=np.vstack(allpts)
# centroid of union (area-weighted of both polygons)
cents=[];areas=[]
for m in P:
    pg=Polygon(m); cents.append(np.array(pg.centroid.coords[0])); areas.append(pg.area)
cen=(cents[0]*areas[0]+cents[1]*areas[1])/sum(areas)
# origin: foot of perpendicular from cen onto line (point c, dir d)
t=np.dot(cen-c,d); org=c+t*d
can=[]
for m in P:
    rel=m-org
    can.append(np.column_stack([rel@d, rel@n]))
stored=sh['canonical']['polygons_m']
mx=max(np.abs(np.array(a)-np.array(b)).max() for a,b in zip(can,stored))
print('max diff to stored canonical (m):',round(mx,3))
cp=[Polygon(x) for x in can]
tot=sum(p.area for p in cp); print('areas',[round(p.area,1) for p in cp],'total',round(tot,1),'stored',sh['canonical']['area_m2'])
A=np.vstack(can); print('x range',A[:,0].min().round(2),A[:,0].max().round(2),'y range',A[:,1].min().round(2),A[:,1].max().round(2))
print('alongshore bbox',round(np.ptp(A[:,0]),1),'cross',round(np.ptp(A[:,1]),1))
# centroid offshore distance
cc=sum(np.array(p.centroid.coords[0])*p.area for p in cp)/tot; print('centroid canon',cc.round(2))
# max dimension
from scipy.spatial.distance import pdist
print('max dim',round(pdist(A).max(),1))
# hand check point: sat2024 N mound vertex 12? pick N0
import json as J
J.dump({'can':[x.tolist() for x in can],'org_ll':list(imerc(*[0,0])) if False else None},open(r"C:\Users\lior\AppData\Local\Temp\claude\C--\cd973dbd-a674-4cd5-adf1-ffb4c361545f\scratchpad\borth_verify\can_mine.json",'w'))
print('N0 px',polys[0][0],'-> mine',can[0][0].round(2),'stored',stored[0][0])
print('S10 px',polys[1][10],'-> mine',can[1][10].round(2),'stored',stored[1][10])
