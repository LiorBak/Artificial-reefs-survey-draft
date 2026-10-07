import json, math, numpy as np
from pyproj import Transformer
from shapely.geometry import Polygon, Point
sop={'R1':(260409.145,289284.522),'R2':(260501.860,289331.154),'R3':(260528.445,289332.669),'R4':(260527.416,289323.700),'R5':(260503.909,289322.361),'R6':(260451.697,289299.380),'R7':(260449.504,289284.783),'R8':(260445.718,289281.518),'R9':(260434.301,289276.451),'R10':(260424.002,289276.269),'R11':(260519.537,289254.981),'R12':(260551.566,289116.844),'R13':(260568.429,289104.990),'R14':(260470.000,289162.000),'R15':(260470.000,289200.000)}
base=r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git\07_scale\shapes\borth-coastal-defence-reef"
g=json.load(open(base+r"\src\borth_esri_2024-09-17_z19.png.geo.json"))
R=6378137.0
def merc(lat,lon): return R*math.radians(lon), R*math.log(math.tan(math.pi/4+math.radians(lat)/2))
def ll2pix(lat,lon):
    b=g['bounds']; w,h=g['width'],g['height']
    xw,yn=merc(b['north'],b['west']); xe,ys=merc(b['south'],b['east']); mx,my=merc(lat,lon)
    return (mx-xw)/(xe-xw)*w,(my-yn)/(ys-yn)*h
sh=json.load(open(base+r"\shape.json",encoding='utf-8'))
polys=sh['sources'][0]['pixel_polygons']
out={}
for tfm_name,tf in (('OSTN-less EPSG:27700->4326 (pyproj default)',Transformer.from_crs('EPSG:27700','EPSG:4326',always_xy=True)),):
    for k,(e,n) in sop.items():
        lon,lat=tf.transform(e,n); x,y=ll2pix(lat,lon)
        inside=[Polygon(p).contains(Point(x,y)) for p in polys]
        d=[Polygon(p).exterior.distance(Point(x,y))/5.4995 for p in polys]
        out[k]=(lat,lon,x,y)
        print(k,round(lat,6),round(lon,6),'px',round(x),round(y),'inside N/S',inside,'dist to outline m',[round(v,1) for v in d])
json.dump(out,open('sop_ll.json','w'))
# geometry check: distance R1-R2 etc
import itertools
pts={k:np.array(v) for k,v in sop.items()}
print('R14-R15 crest length',np.linalg.norm(pts['R14']-pts['R15']))
print('R3-R4',np.linalg.norm(pts['R3']-pts['R4']),'R5-R2',np.linalg.norm(pts['R5']-pts['R2']))
