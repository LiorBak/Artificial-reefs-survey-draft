import json, math, pickle, numpy as np, tifffile
from pyproj import Transformer
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi
D=r"C:\Users\lior\AppData\Local\Temp\claude\C--\cd973dbd-a674-4cd5-adf1-ffb4c361545f\scratchpad\borth_verify"
base=r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git\07_scale\shapes\borth-coastal-defence-reef"
sh=json.load(open(base+r"\shape.json",encoding='utf-8'))
g=json.load(open(base+r"\src\borth_esri_2024-09-17_z19.png.geo.json"))
R=6378137.0; S=5.4995
tf=Transformer.from_crs('EPSG:27700','EPSG:4326',always_xy=True)
def merc(lat,lon): return R*math.radians(lon), R*math.log(math.tan(math.pi/4+math.radians(lat)/2))
b=g['bounds']; w,h=g['width'],g['height']
xw,yn=merc(b['north'],b['west']); xe,ys=merc(b['south'],b['east'])
def en2px(e,n):
    lon,lat=tf.transform(e,n); mx,my=merc(lat,lon); return ((mx-xw)/(xe-xw)*w,(my-yn)/(ys-yn)*h)
rings=pickle.load(open(D+r"\design_rings.pkl",'rb'))
dsm=tifffile.imread(D+r"\dl\wg_dsm_SN6089.tif")
lab=np.load(D+r"\lab.npy"); E0,N1=260380,289380
# LiDAR polygons (BNG) from label masks: union of cells
def mask_poly(i):
    ys_,xs_=np.where(lab==i)
    cells=[box(E0+x,N1-y-1,E0+x+1,N1-y) for x,y in zip(xs_,ys_)]
    P=unary_union(cells).buffer(0.01)
    if P.geom_type!='Polygon': P=max(P.geoms,key=lambda q:q.area)
    return P.simplify(0.4)
LN,LS=mask_poly(2),mask_poly(3)
pickle.dump({'LN':list(LN.exterior.coords),'LS':list(LS.exterior.coords)},open(D+r"\lidar_polys.pkl",'wb'))
def dims(P):
    mrr=P.minimum_rotated_rectangle; c=np.array(mrr.exterior.coords)[:4]
    e=[np.hypot(*(c[(i+1)%4]-c[i])) for i in range(4)]
    L,Wd=max(e[0],e[1]),min(e[0],e[1])
    # bearing of long side
    i=0 if e[0]>=e[1] else 1; v=c[(i+1)%4]-c[i]; brg=(math.degrees(math.atan2(v[0],v[1]))+360)%180
    return L,Wd,brg
print('design inner N: area %.0f  minrect %.1f x %.1f  axis bearing %.1f  | mean width = area/(len along axis)'%((Polygon(rings['N'][4]).area,)+dims(Polygon(rings['N'][4]))))
print('design outer N: area %.0f  minrect %.1f x %.1f  axis %.1f'%((Polygon(rings['N'][0]).area,)+dims(Polygon(rings['N'][0]))))
print('design inner S: area %.0f  minrect %.1f x %.1f  axis %.1f'%((Polygon(rings['S'][4]).area,)+dims(Polygon(rings['S'][4]))))
print('design outer S: area %.0f  minrect %.1f x %.1f  axis %.1f'%((Polygon(rings['S'][0]).area,)+dims(Polygon(rings['S'][0]))))
print('LiDAR N: area %.0f minrect %.1f x %.1f axis %.1f'%((LN.area,)+dims(LN)))
print('LiDAR S: area %.0f minrect %.1f x %.1f axis %.1f'%((LS.area,)+dims(LS)))
# traced dims
from shapely.geometry import Polygon as P2
pp=[P2(np.array(p)/S) for p in sh['sources'][0]['pixel_polygons']]
for nm,q in zip('NS',pp): print('traced',nm,'area %.0f minrect %.1f x %.1f axis %.1f'%((q.area,)+dims(q)))
# overlay figure on sat2024
im=Image.open(base+r"\src\borth_esri_2024-09-17_z19.png").convert('RGB'); d=ImageDraw.Draw(im)
def draw(poly_px,col,wd=2):
    pts=[tuple(p) for p in poly_px]; d.line(pts+[pts[0]],fill=col,width=wd)
for p in sh['sources'][0]['pixel_polygons']: draw(p,(255,40,40),3)
for reg in 'NS':
    draw([en2px(e,n) for e,n in rings[reg][4]],(0,255,255),2)
    draw([en2px(e,n) for e,n in rings[reg][0]],(80,120,255),1)
draw([en2px(e,n) for e,n in LN.exterior.coords],(255,230,0),2)
draw([en2px(e,n) for e,n in LS.exterior.coords],(255,230,0),2)
f=ImageFont.truetype("arial.ttf",22)
leg=[("traced rock edge (sat 2024-09-17) - shape.json",(255,40,40)),("design armour foot, DRG 9V5090/1020 (Type 4 toe, about -2.2 mODN)",(0,255,255)),("design seabed edge incl. toe apron (same drawing)",(80,120,255)),("LiDAR 2022-03-19 exposed outline (about -2.3 mODN)",(255,230,0))]
d.rectangle([20,20,880,150],fill=(0,0,0))
for i,(t,c) in enumerate(leg): d.text((30,26+i*30),t,fill=c,font=f)
im.save(base+r"\overlays\verify_design_lidar_vs_trace_sat2024.png")
print('saved')
