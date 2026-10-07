import json, math, sys, numpy as np
sys.path.insert(0,"C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/07_scale/tools")
import geom, satellite as S
import shapely.geometry as sg
ROOT="C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/07_scale/shapes/narrowneck-gold-coast"
sh=json.load(open(ROOT+"/shape.json",encoding='utf-8'))
c=sh['canonical']; P=c['polygons_m']; names=['north_arm','south_arm','wing_patch_NW_a','wing_patch_NW_b','weir_1','weir_2_faint','weir_3_faint']
fr=json.load(open('frame.json')); SHORE=fr['bearing_north_heading_deg']
out={'per_polygon':{}}
def axis(poly):
    pg=sg.Polygon(poly)
    # area-weighted PCA via dense interior samples
    minx,miny,maxx,maxy=pg.bounds; xs=np.arange(minx,maxx,0.5); ys=np.arange(miny,maxy,0.5)
    pts=np.array([(x,y) for x in xs for y in ys if pg.contains(sg.Point(x,y))])
    m=pts.mean(0); u,s,vt=np.linalg.svd(pts-m,full_matrices=False)
    v=vt[0]; 
    if v[1]<0: v=-v     # point seaward (+y) when possible
    ang_from_alongshore=math.degrees(math.atan2(v[1],v[0]))   # +x alongshore (toward N), +y offshore
    L=4*s[0]/math.sqrt(len(pts))*math.sqrt(1)  # not used
    # oriented extents along/perp the axis
    d=pts-m; a=d@v; pperp=d@np.array([-v[1],v[0]])
    return v,ang_from_alongshore,(a.min(),a.max()),(pperp.min(),pperp.max()),pg
for nm,poly in zip(names,P):
    v,ang,ea,ep,pg=axis(poly)
    # compass bearing of axis direction (seaward-pointing): shore normal bearing + (angle from normal)
    # canonical +y has bearing SHORE+90 ; +x has bearing SHORE
    bearing=(SHORE+ (90-ang)*0 + 0)  # placeholder, computed below
    b=math.radians(SHORE); ex=np.array([math.sin(b),math.cos(b)]); ey=np.array([math.sin(b+math.pi/2),math.cos(b+math.pi/2)])
    vec=v[0]*ex+v[1]*ey; brg=math.degrees(math.atan2(vec[0],vec[1]))%360
    acute=geom.angle_to_shoreline(brg,SHORE)
    out['per_polygon'][nm]={'area_m2':round(pg.area,1),'axis_bearing_deg':round(brg,1),'axis_to_shoreline_deg':round(acute,1),
        'length_along_axis_m':round(ea[1]-ea[0],1),'width_perp_axis_m':round(ep[1]-ep[0],1),'centroid_xy_m':[round(pg.centroid.x,1),round(pg.centroid.y,1)],
        'bbox_xy_m':[round(t,1) for t in pg.bounds]}
    print(nm,out['per_polygon'][nm])
# arm separation, channel width: distance between N arm and S arm polygons
nA,sA=sg.Polygon(P[0]),sg.Polygon(P[1])
out['arm_gap_min_m']=round(nA.distance(sA),1)
out['arm_centroid_separation_alongshore_m']=round(nA.centroid.x-sA.centroid.x,1)
# lat/lon polygons
geo=json.load(open(ROOT+"/src/wayback/nn_wayback_2020-08-08_r9812_z19.png.geo.json"))
src=[s for s in sh['sources'] if s['id']=='s3'][0]
ll=[[list(S.pix2ll(geo,x,y)) for x,y in poly] for poly in src['pixel_polygons']]
cen=nA.union(sA).centroid
cx,cy=cen.x,cen.y
out['latlon_polygons']=[[[round(a,7),round(b,7)] for a,b in poly] for poly in ll]
print('arm gap',out['arm_gap_min_m'],'centroid sep',out['arm_centroid_separation_alongshore_m'])
# union-based overall dims of the two arms only and of all polygons
allp=sg.MultiPolygon([sg.Polygon(p) for p in P]) 
out['bbox_all_m']={'alongshore':round(allp.bounds[2]-allp.bounds[0],1),'crossshore':round(allp.bounds[3]-allp.bounds[1],1)}
arms=sg.MultiPolygon([nA,sA]); out['bbox_arms_m']={'alongshore':round(arms.bounds[2]-arms.bounds[0],1),'crossshore':round(arms.bounds[3]-arms.bounds[1],1)}
out['area_arms_m2']=round(nA.area+sA.area,1); out['area_all_m2']=round(sum(sg.Polygon(p).area for p in P),1)
print(out['bbox_all_m'],out['bbox_arms_m'],out['area_arms_m2'],out['area_all_m2'])
# edge bearings of each arm's long upper/lower sides: use the polygon's minimum rotated rectangle for the arms
for nm,pg in (('north_arm',nA),('south_arm',sA)):
    r=pg.minimum_rotated_rectangle; co=list(r.exterior.coords)[:4]
    e=[(co[(i+1)%4][0]-co[i][0],co[(i+1)%4][1]-co[i][1]) for i in range(4)]
    L=[math.hypot(*t) for t in e]; i=int(np.argmax(L))
    b=math.radians(SHORE); ex=np.array([math.sin(b),math.cos(b)]); ey=np.array([math.sin(b+math.pi/2),math.cos(b+math.pi/2)])
    vec=e[i][0]*ex+e[i][1]*ey; brg=math.degrees(math.atan2(vec[0],vec[1]))%360
    out.setdefault('min_rect',{})[nm]={'length_m':round(max(L),1),'width_m':round(min(L),1),'long_side_bearing_deg':round(brg%180,1),'to_shoreline_deg':round(geom.angle_to_shoreline(brg,SHORE),1)}
    print(nm,out['min_rect'][nm])
json.dump(out,open('metrics_out.json','w'))
