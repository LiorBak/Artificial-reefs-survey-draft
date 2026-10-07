import json, numpy as np, tifffile
from scipy import ndimage as ndi
from pyproj import Transformer
from shapely.geometry import Polygon
from PIL import Image, ImageDraw
D=r"C:\Users\lior\AppData\Local\Temp\claude\C--\cd973dbd-a674-4cd5-adf1-ffb4c361545f\scratchpad\borth_verify\dl"
dsm=tifffile.imread(D+r"\wg_dsm_SN6089.tif"); dtm=tifffile.imread(D+r"\wg_dtm_SN6089.tif")
base=r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git\07_scale\shapes\borth-coastal-defence-reef"
sh=json.load(open(base+r"\shape.json",encoding='utf-8'))
tf=Transformer.from_crs('EPSG:4326','EPSG:27700',always_xy=True)
polys_en=[]
for poly in sh['geo']['polygons_latlon']:
    polys_en.append([tf.transform(lon,lat) for lat,lon in poly])
# window
E0,E1,N0,N1=260380,260640,289080,289380
r0,r1=290000-N1,290000-N0; c0,c1=E0-260000,E1-260000
W=dsm[r0:r1,c0:c1]; Wt=dtm[r0:r1,c0:c1]
valid=W>-9000
lab,n=ndi.label(valid)
print('components',n,[ (i,int((lab==i).sum())) for i in range(1,n+1)])
# identify mound comps by centroid
for i in range(1,n+1):
    ys,xs=np.where(lab==i)
    print(i,'n',len(xs),'E',xs.min()+E0,xs.max()+E0,'N',N1-ys.max(),N1-ys.min(),'z min/med/max',round(float(W[lab==i].min()),2),round(float(np.median(W[lab==i])),2),round(float(W[lab==i].max()),2))
np.save('lab.npy',lab)
# rasterize traced polygons to grid (cell centres)
def raster(poly):
    img=Image.new('L',(c1-c0,r1-r0),0); d=ImageDraw.Draw(img)
    # pixel coords: x = E - E0 (cell index), y = N1 - N
    pts=[(e-E0,N1-n) for e,n in poly]
    d.polygon(pts,fill=1,outline=1)
    return np.array(img).astype(bool)
Rn=raster(polys_en[0]); Rs=raster(polys_en[1])
print('traced N cells',Rn.sum(),'S cells',Rs.sum())
for name,R in (('N',Rn),('S',Rs)):
    ids=np.unique(lab[R&valid]); ids=ids[ids>0]; print(name,'overlapping comps',ids)
json.dump({'E0':E0,'N1':N1},open('lidar_win.json','w'))
np.save('Rn.npy',Rn); np.save('Rs.npy',Rs)
