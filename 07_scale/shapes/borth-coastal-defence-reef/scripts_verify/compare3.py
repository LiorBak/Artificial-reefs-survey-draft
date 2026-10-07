import json, math, pickle, numpy as np
from pyproj import Transformer
from shapely.geometry import Polygon
from shapely import affinity
from scipy import ndimage as ndi
base=r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git\07_scale\shapes\borth-coastal-defence-reef"
sh=json.load(open(base+r"\shape.json",encoding='utf-8'))
g=json.load(open(base+r"\src\borth_esri_2024-09-17_z19.png.geo.json"))
R=6378137.0
tf=Transformer.from_crs('EPSG:27700','EPSG:4326',always_xy=True)
def merc(lat,lon): return R*math.radians(lon), R*math.log(math.tan(math.pi/4+math.radians(lat)/2))
b=g['bounds']; w,h=g['width'],g['height']
xw,yn=merc(b['north'],b['west']); xe,ys=merc(b['south'],b['east'])
def en2px(e,n):
    lon,lat=tf.transform(e,n); mx,my=merc(lat,lon); return ((mx-xw)/(xe-xw)*w,(my-yn)/(ys-yn)*h)
rings=pickle.load(open('design_rings.pkl','rb'))
S=5.4995
traced=[Polygon(p) for p in sh['sources'][0]['pixel_polygons']]
def pxpoly(ring): return Polygon([en2px(e,n) for e,n in ring])
out={}
for reg,idx in (('N',0),('S',1)):
    print('=====',reg,'traced area',round(traced[idx].area/S/S,1))
    for k,ring in enumerate(rings[reg]):
        P=pxpoly(ring)
        iou=P.intersection(traced[idx]).area/P.union(traced[idx]).area
        # best translation (coarse) for IoU
        best=(iou,0,0)
        for dx in range(-30,31,3):
            for dy in range(-30,31,3):
                Q=affinity.translate(P,dx,dy); v=Q.intersection(traced[idx]).area/Q.union(traced[idx]).area
                if v>best[0]: best=(v,dx,dy)
        # centroid offset
        c1=np.array(P.centroid.coords[0]); c2=np.array(traced[idx].centroid.coords[0])
        print(f' ring{k}: design area {P.area/S/S:7.1f} m2  IoU {iou:.3f}  best-shift IoU {best[0]:.3f} at dx,dy px {best[1:]} (= E {best[1]/S:+.1f} m, N {-best[2]/S:+.1f} m)  centroid design->traced px {c2-c1} = (E {(c2-c1)[0]/S:+.1f}, N {-(c2-c1)[1]/S:+.1f}) m')
        out[(reg,k)]=[tuple(map(float,q)) for q in P.exterior.coords]
pickle.dump(out,open('design_px.pkl','wb'))
