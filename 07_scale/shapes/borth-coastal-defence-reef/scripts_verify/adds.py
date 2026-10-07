import json, math, pickle, numpy as np
from pyproj import Transformer
from shapely.geometry import Polygon
D="C:/Users/lior/AppData/Local/Temp/claude/C--/cd973dbd-a674-4cd5-adf1-ffb4c361545f/scratchpad/borth_verify"
base="C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/07_scale/shapes/borth-coastal-defence-reef"
R=6378137.0
sh=json.load(open(base+"/shape.json",encoding='utf-8'))
g24=json.load(open(base+"/src/borth_esri_2024-09-17_z19.png.geo.json")); gsh=json.load(open(base+"/src/borth_shoreline_z19.png.geo.json"))
def merc(lat,lon): return R*math.radians(lon), R*math.log(math.tan(math.pi/4+math.radians(lat)/2))
def imerc(x,y): return math.degrees(2*math.atan(math.exp(y/R))-math.pi/2), math.degrees(x/R)
def pix2ll(g,x,y):
    b=g['bounds']; w,h=g['width'],g['height']; xw,yn=merc(b['north'],b['west']); xe,ys=merc(b['south'],b['east'])
    return imerc(xw+x/w*(xe-xw), yn+y/h*(ys-yn))
lat0,lon0=52.4832,-4.0562
def loc(lat,lon): return np.array([math.radians(lon-lon0)*R*math.cos(math.radians(lat0)), math.radians(lat-lat0)*R])
pts=[(1795,1100),(1800,1500),(1803,2000),(1805,2500),(1808,2600)]
E=np.array([loc(*pix2ll(gsh,*p)) for p in pts]); c=E.mean(0); d=np.linalg.svd(E-c)[2][0]
if d[1]<0: d=-d
n=np.array([-d[1],d[0]])               # old frame: x north, y west
polys=sh['sources'][0]['pixel_polygons']
P=[np.array([loc(*pix2ll(g24,x,y)) for x,y in p]) for p in polys]
cens=[Polygon(p).centroid.coords[0] for p in P]; ar=[Polygon(p).area for p in P]
cen=(np.array(cens[0])*ar[0]+np.array(cens[1])*ar[1])/sum(ar); org=c+np.dot(cen-c,d)*d
def canon_new(en_list):  # BNG list -> new canonical (x south, y west)
    tf=Transformer.from_crs('EPSG:27700','EPSG:4326',always_xy=True)
    out=[]
    for e,nn in en_list:
        lon,lat=tf.transform(e,nn); rel=loc(lat,lon)-org
        out.append([round(float(-(rel@d)),2),round(float(rel@n),2)])
    return out
rings=pickle.load(open(D+"/design_rings.pkl",'rb')); lid=pickle.load(open(D+"/lidar_polys.pkl",'rb'))
alt={'design_N_armour_foot':canon_new(rings['N'][4]),'design_N_seabed_edge':canon_new(rings['N'][0]),
     'design_S_armour_foot':canon_new(rings['S'][4]),'design_S_seabed_edge':canon_new(rings['S'][0]),
     'lidar_N_exposed_2022-03-19':canon_new(lid['LN']),'lidar_S_exposed_2022-03-19':canon_new(lid['LS'])}
for k,v in alt.items():
    pg=Polygon(v); a=np.array(v); print(k,'area %.0f'%pg.area,'x %.1f..%.1f y %.1f..%.1f'%(a[:,0].min(),a[:,0].max(),a[:,1].min(),a[:,1].max()))
# separations
cN=Polygon(alt['design_N_armour_foot']).centroid; cS=Polygon(alt['design_S_armour_foot']).centroid
print('design centroid separation N-S: %.1f m (x,y)'%cN.distance(cS), np.array(cN.coords[0])-np.array(cS.coords[0]))
trN=Polygon(sh['canonical']['polygons_m'][0]).centroid; trS=Polygon(sh['canonical']['polygons_m'][1]).centroid
print('traced separation %.1f'%trN.distance(trS))
print('design gap between armour feet %.1f m'%Polygon(alt['design_N_armour_foot']).distance(Polygon(alt['design_S_armour_foot'])), 'traced gap %.1f'%Polygon(sh['canonical']['polygons_m'][0]).distance(Polygon(sh['canonical']['polygons_m'][1])))
# design drawing pixel polygons (PNG at 110 dpi): forward fit BNG->pdf pt
fit=pickle.load(open(D+"/design_fit.pkl",'rb'))['fit']; err,refl,s,Rm,sm,dm=fit
def bng2pdf(e,nn): return s*((np.array([e,nn])-sm)@Rm.T)+dm
k=110/72
dpx=[[ [round(float(v*k),1) for v in bng2pdf(e,nn)] for e,nn in r] for r in (rings['N'][4],rings['N'][0],rings['S'][4],rings['S'][0])]
print('drawing px polygon sizes',[len(p) for p in dpx],'px/m',round(float(s*k),3))
json.dump({'alt':alt,'dpx':dpx,'pxm':float(s*k),'org_old':list(map(float,org)),'d':list(map(float,d))},open(D+"/adds.json",'w'))
# lidar crest numbers recomputed? use earlier
