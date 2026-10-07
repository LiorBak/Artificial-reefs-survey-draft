import json, math, sys, numpy as np
sys.path.insert(0,"C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/07_scale/tools")
import satellite as S, shapely.geometry as sg
ROOT="C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/07_scale/shapes/narrowneck-gold-coast"
g=json.load(open(ROOT+"/src/gc_opendata_artificial_reef_raw_4326.geojson"))
f=[x for x in g['features'] if x['properties'].get('OBJECTID')==4637][0]
ring=f['geometry']['coordinates'][0]
geo=json.load(open(ROOT+"/src/wayback/nn_wayback_2020-08-08_r9812_z19.png.geo.json")); fr=json.load(open('frame.json'))
mpp=geo['m_per_px_center']; O=np.array(fr['origin_px']); u=np.array(fr['alongshore_dir_px']); n=np.array([-u[1],u[0]])
pts=[]
for lon,lat in ring:
    x,y=S.ll2pix(geo,lat,lon); d=np.array([x,y])-O; pts.append((float(d@u*mpp),float(d@n*mpp)))
cp=sg.Polygon(pts); sh=json.load(open(ROOT+"/shape.json")); P=[sg.Polygon(p) for p in sh['canonical']['polygons_m']]
arms=P[0].union(P[1])
print('council polygon in our frame: x %.0f..%.0f (%.0f m alongshore)  y %.0f..%.0f (%.0f m cross-shore)  area %.0f m2'%(cp.bounds[0],cp.bounds[2],cp.bounds[2]-cp.bounds[0],cp.bounds[1],cp.bounds[3],cp.bounds[3]-cp.bounds[1],cp.area))
allr=P[0]
for p in P[1:]: allr=allr.union(p)
print('traced reef area inside council polygon: %.0f of %.0f m2 (%.0f%%)'%(allr.intersection(cp).area,allr.area,100*allr.intersection(cp).area/allr.area))
print('centroid council (%.0f,%.0f)  traced arms centroid (%.0f,%.0f)'%(cp.centroid.x,cp.centroid.y,arms.centroid.x,arms.centroid.y))
json.dump({'council_polygon_xy_m':[[round(a,1),round(b,1)] for a,b in pts],'bounds':[round(t,1) for t in cp.bounds],'area':round(cp.area,0),'inside_pct':round(100*allr.intersection(cp).area/allr.area,1)},open('council_in_frame.json','w'))
