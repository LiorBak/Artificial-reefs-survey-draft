"""option2_compare.py: Option 2 (Corbett 2023 Fig 2 right) vs the 2020 trace and the 2004 design; writes option2_compare.json + overlays/option2_on_s3.png"""
import json,os,math,numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely import affinity
from PIL import Image, ImageDraw
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(os.path.dirname(HERE))
o=json.load(open(HERE+"/option2_outline.json")); sh=json.load(open(ROOT+"/shape.json")); ref=json.load(open(ROOT+"/verify_scripts/design_outline_2004.json"))
tr=[Polygon(p) for p in sh["canonical"]["polygons_m"]]; N,S=tr[0],tr[1]; arms=unary_union([N,S])
O2=Polygon(o["R"]["outer_-6.0"]["canonical_m"]).buffer(0); O1=Polygon(o["L"]["outer_-6.0"]["canonical_m"]).buffer(0); D04=Polygon(ref["outer_-6.0"]["canonical_m"]).buffer(0)
res={"area_O2_-6":O2.area,"area_O1_-6":O1.area,"area_2004_-6":D04.area}
res["frac_trace_arms_inside_O2"]=arms.intersection(O2).area/arms.area
res["frac_trace_arms_inside_O1"]=arms.intersection(O1).area/arms.area
res["frac_trace_arms_inside_2004"]=arms.intersection(D04).area/arms.area
res["frac_trace_N_inside_O2"]=N.intersection(O2).area/N.area; res["frac_trace_S_inside_O2"]=S.intersection(O2).area/S.area
res["frac_trace_N_inside_2004"]=N.intersection(D04).area/N.area; res["frac_trace_S_inside_2004"]=S.intersection(D04).area/S.area
L2=[Polygon(q["canonical_m"]).buffer(0) for q in o["R"]["crest_-2.5"]]; L1=[Polygon(q["canonical_m"]).buffer(0) for q in o["L"]["crest_-2.5"]]
def ext(p): b=p.bounds; return [round(v,1) for v in b]
res["crest_loops_O2_bounds(minx,miny,maxx,maxy)"]=[ext(p) for p in L2]; res["crest_loops_O1_bounds"]=[ext(p) for p in L1]
res["crest_loops_2004_bounds"]=[ext(Polygon(q["canonical_m"]).buffer(0)) for q in ref["inner_-2.5"]]
res["outer_O2_bounds"]=ext(O2); res["outer_O1_bounds"]=ext(O1); res["outer_2004_bounds"]=ext(D04)
# centroid of the half of the -6 polygon on each reef vs trace
res["centroid_O2_N_half"]=None
for nm,half,tp in (("N",O2.intersection(Polygon([(-1e3,1e3),(1e3,1e3),(1e3,5),(-1e3,5)])),N),("S",O2.intersection(Polygon([(-1e3,-1e3),(1e3,-1e3),(1e3,5),(-1e3,5)])),S)):
    pass
# translation scan: shift O2 (dx alongshore, dy offshore) to maximise IoU with arms+wings+... (arms only: coverage - penalty) ; report IoU of the N half only
Nhalf=O2.intersection(Polygon([(-5,-1e3),(1e3,-1e3),(1e3,1e3),(-5,1e3)])); Shalf=O2.intersection(Polygon([(-1e3,-1e3),(-5,-1e3),(-5,1e3),(-1e3,1e3)]))
best={}
for nm,half,tp in (("N",Nhalf,N),("S",Shalf,S)):
    r=[]
    for dx in range(-30,31,2):
        for dy in range(-40,41,2):
            h=affinity.translate(half,dx,dy); r.append((tp.intersection(h).area/tp.union(h).area,dx,dy))
    r.sort(reverse=True); best[nm]={"IoU_nominal":tp.intersection(half).area/tp.union(half).area,"best_IoU":r[0][0],"best_dx":r[0][1],"best_dy":r[0][2],"area_half_m2":half.area}
    # inner crest loop centroid vs trace centroid
res["translation_scan_half_vs_trace_arm"]=best
res["note_IoU"]="IoU is low by construction (design -6 envelope 6.6-7k m2 per half vs visible container field 2.3-3.7k m2); use the coverage fractions and the offsets of the extents"
json.dump(res,open(HERE+"/option2_compare.json","w"),indent=1)
for k,v in res.items(): print(k,v if not isinstance(v,float) else round(v,3))
# overlay on s3
b=math.radians(356.212); u=np.array([math.sin(b),-math.cos(b)]); nn=np.array([math.sin(b+math.pi/2),-math.cos(b+math.pi/2)]); org=np.array([-517.90,821.74]); mpp=0.263665
def px(P): P=np.asarray(P); return [tuple(org+(x*u+y*nn)/mpp) for x,y in P]
im=Image.open(ROOT+"/src/wayback/nn_wayback_2020-08-08_r9812_z19.png").convert("RGB"); d=ImageDraw.Draw(im,"RGBA")
def poly(p,col,w=3): 
    xy=px(p.exterior.coords); d.line(xy+[xy[0]],fill=col,width=w)
poly(O2,(255,0,255,255)); poly(D04,(0,200,255,255),2)
for p in L2: poly(p,(255,0,255,255))
for p in tr[:2]: poly(p,(255,255,0,255),2)
d.text((15,15),"magenta = Corbett 2023 Option 2 (-6 contour + -2.5 crest loops); cyan = 2004 design -6 (Jackson 2012); yellow = 2020 trace arms",fill=(255,255,255,255))
os.makedirs(ROOT+"/overlays",exist_ok=True)
im.resize((1000,1000)).save(ROOT+"/overlays/option2_on_s3.png")
