import numpy as np, json, requests, sys, os
from PIL import Image, ImageDraw, ImageFont
from pyproj import Transformer
ROOT=r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git\07_scale"
OUT=ROOT+r"\bathymetry\gold_coast\annotated"
T=os.environ['TEMP']+r"\gc_bathy"
img=np.load(T+r"\modeimg.npy")
X0,Y0=515775,6938225
to28356=Transformer.from_crs(4326,28356,always_xy=True)
to3857=Transformer.from_crs(4326,3857,always_xy=True)
from_28356=Transformer.from_crs(28356,4326,always_xy=True)
H={'User-Agent':'Mozilla/5.0'}
def font(sz):
    for f in [r"C:\Windows\Fonts\arial.ttf",r"C:\Windows\Fonts\segoeui.ttf"]:
        if os.path.exists(f): return ImageFont.truetype(f,sz)
    return ImageFont.load_default()
def make(imgpath,geojson,title,out,reefpts,notes):
    g=json.load(open(geojson))
    b=g['bounds']; im=Image.open(imgpath).convert('RGB'); W,Hh=im.size
    # contrast stretch for dark images
    a=np.asarray(im).astype(float); lo,hi=np.percentile(a,1),np.percentile(a,99.5)
    a=np.clip((a-lo)/(hi-lo)*255,0,255).astype(np.uint8); im=Image.fromarray(a)
    xw,yn=to3857.transform(b['west'],b['north']); xe,ys=to3857.transform(b['east'],b['south'])
    def ll2px(lon,lat):
        x,y=to3857.transform(lon,lat); return (x-xw)/(xe-xw)*W,(yn-y)/(yn-ys)*Hh
    def mga2px(x,y):
        lo_,la_=from_28356.transform(x,y); return ll2px(lo_,la_)
    ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    # blocks present in metadata raster
    # window in MGA
    corners=[to28356.transform(b['west'],b['north']),to28356.transform(b['east'],b['south'])]
    xmin,xmax=corners[0][0]-300,corners[1][0]+300; ymin,ymax=corners[1][1]-300,corners[0][1]+300
    c0=int((xmin-X0)//128); c1=int((xmax-X0)//128); r0=int((Y0-ymax)//128); r1=int((Y0-ymin)//128)
    n_present=0; n_absent=0
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            v=img[r,c] if (0<=r<img.shape[0] and 0<=c<img.shape[1]) else -1
            x0=X0+c*128; y1=Y0-r*128; x1=x0+128; y0=y1-128
            poly=[mga2px(x0,y1),mga2px(x1,y1),mga2px(x1,y0),mga2px(x0,y0)]
            if v>=0:
                d.polygon(poly,fill=(255,200,0,70),outline=(255,200,0,230)); n_present+=1
            else:
                d.polygon(poly,outline=(0,200,255,160)); n_absent+=1
    # contour 0 m (layer 8) in window
    p={'f':'json','where':'1=1','geometry':json.dumps({'xmin':xmin,'ymin':ymin,'xmax':xmax,'ymax':ymax,'spatialReference':{'wkid':28356}}),'geometryType':'esriGeometryEnvelope','spatialRel':'esriSpatialRelIntersects','outFields':'ELEVATION','returnGeometry':'true','outSR':'28356'}
    r=requests.get('https://maps1.goldcoast.qld.gov.au/arcgis/rest/services/Contours/MapServer/8/query',params=p,headers=H,timeout=90).json()
    zs=set()
    for f in r.get('features',[]):
        z=f['attributes']['ELEVATION']; zs.add(z)
        col=(255,60,60,255) if z==0 else (60,255,60,255)
        for path in f['geometry']['paths']:
            pts=[mga2px(x,y) for x,y in path]
            d.line(pts,fill=col,width=3 if z==0 else 2)
    # reef markers
    for name,(lon,lat) in reefpts.items():
        x,y=ll2px(lon,lat); d.ellipse([x-9,y-9,x+9,y+9],outline=(255,255,255,255),width=3)
        d.text((x+14,y-10),name,fill=(255,255,255,255),font=font(26))
    im=Image.alpha_composite(im.convert('RGBA'),ov)
    d=ImageDraw.Draw(im)
    # caption box
    lines=[title]+notes+['Yellow = 128 m blocks that hold a survey-source value in the City DTM_Metadata raster; cyan outline = no value (no DTM cell).','Red = City 1 m contour layer, ELEVATION = 0 m AHD; green = other elevations (found: %s).'%sorted(zs),'Contours minimum in this window = %s m AHD. Blocks with data: %d, without: %d.'%(min(zs) if zs else 'n/a',n_present,n_absent)]
    f=font(24); h=sum(30 for _ in lines)+16
    d.rectangle([0,0,W,h],fill=(0,0,0,215))
    y=8
    for t in lines: d.text((12,y),t,fill=(255,255,255,255),font=f); y+=30
    im.convert('RGB').save(out)
    print(out,sorted(zs),n_present,n_absent)
make(ROOT+r"\shapes\palm-beach-gold-coast\src\pb_context_z18.png",ROOT+r"\shapes\palm-beach-gold-coast\src\pb_context_z18.png.geo.json",
     "Q1 Palm Beach: City of Gold Coast DTM has no cells over the reef or offshore (EPSG:28356 blocks, vertical datum AHD)",
     OUT+r"\q1_palm_beach_dtm_source_coverage_on_esri.png",
     {'Palm Beach Reef':(153.470913,-28.107334)},
     ['Base: Esri World Imagery 2025-12-01 (private research copy, contrast stretched). Sources: data.gov.au Gold Coast DTM Metadata (CC BY 2.5 AU); City contours MapServer.'])
make(ROOT+r"\shapes\narrowneck-gold-coast\src\nn_esri_z19_current.png",ROOT+r"\shapes\narrowneck-gold-coast\src\nn_esri_z19_current.png.geo.json",
     "Q1 Narrowneck: City of Gold Coast DTM has no cells over the reef or offshore (EPSG:28356 blocks, vertical datum AHD)",
     OUT+r"\q1_narrowneck_dtm_source_coverage_on_esri.png",
     {'Narrowneck reef (council polygon centre)':(153.4346,-27.9866)},
     ['Base: Esri World Imagery 2025-10-10 (private research copy, contrast stretched). Sources: data.gov.au Gold Coast DTM Metadata (CC BY 2.5 AU); City contours MapServer.'])
