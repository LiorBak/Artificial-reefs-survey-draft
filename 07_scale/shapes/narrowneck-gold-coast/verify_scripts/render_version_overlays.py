"""render_version_overlays.py: overlays of each outline version + faint patches on s3, from shape.json. Output ../overlays/*.png (1200 px)"""
import json,os,math,numpy as np
from PIL import Image, ImageDraw
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
sh=json.load(open(ROOT+"/shape.json")); V={v["id"]:v for v in sh["outline_versions"]}
b=math.radians(356.212); u=np.array([math.sin(b),-math.cos(b)]); nn=np.array([math.sin(b+math.pi/2),-math.cos(b+math.pi/2)]); org=np.array([-517.90,821.74]); mpp=0.263665
def px(P): return [tuple((org+(x*u+y*nn)/mpp)) for x,y in P]
base=Image.open(ROOT+"/src/wayback/nn_wayback_2020-08-08_r9812_z19.png").convert("RGB")
def render(name,items,label):
    im=base.copy(); d=ImageDraw.Draw(im,"RGBA")
    for polys,col,w in items:
        for p in polys:
            xy=px(p); d.line(xy+[xy[0]],fill=col,width=w)
    # 20 m bar (73.9 px) 
    d.rectangle((20,1470,20+int(20/mpp),1476),fill=(255,255,255,255)); d.text((20,1450),"20 m",fill=(255,255,255,255)); d.text((15,12),label,fill=(255,255,255,255))
    im.crop((250,330,1350,1230)).save(ROOT+"/overlays/"+name)   # reef region, 1100x900
photo=V["photo_2020-08-08"]["polygons_m"]
render("design_2004_minus6_on_s3.png",[(V["design_2004_revised"]["polygons_m"],(0,200,255,255),3),(V["design_2004_revised"]["crest_loops_m"],(0,200,255,255),2),(photo,(255,255,0,255),2)],"cyan = 2004 revised design -6 m / -2.5 m crest (Jackson et al. 2012, placed +-15 m); yellow = 2020 trace")
render("survey2011_zone_on_s3.png",[(V["survey_2011-06-09"]["polygons_m"],(255,0,255,255),3),(photo,(255,255,0,255),2)],"magenta = relief zone of the 9 Jun 2011 survey (Jackson 2012 Fig 5a, pre-renewal); yellow = 2020 trace")
render("faint_patches_on_s3.png",[([p["canonical_m"] for p in sh["faint_seaward_patches"]["patches"]],(255,128,0,255),2),(photo,(255,255,0,255),2)],"orange = 24 faint dark patches not in the polygons (local-contrast detection); yellow = 2020 trace")
render("navionics_shoals_on_s3.png",[(V["navionics_4.0m_shoals"]["polygons_m"],(255,0,255,255),3),(photo,(255,255,0,255),2)],"magenta = Navionics 4.0 m shoals (indicative only); yellow = 2020 trace")
print("ok")
