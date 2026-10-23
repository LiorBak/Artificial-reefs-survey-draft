"""Extra metrics: min-rotated-rectangle dims (length along the long axis, width), crest-line bearing, IoU of objective mask vs manual trace."""
import json, math, numpy as np
from shapely.geometry import Polygon
o = json.load(open('build_out.json')); mpp = o['mpp']
beta = o['shoreline']['bearing_deg']
res = {}
def frame_to_enu(m):
    m = np.array(m); u_al = np.array([math.sin(math.radians(beta)), math.cos(math.radians(beta))]); u_of = np.array([math.sin(math.radians(beta+90)), math.cos(math.radians(beta+90))])
    return np.outer(m[:,0], u_al) + np.outer(m[:,1], u_of)   # (east, north) relative to origin
for key in ('sat', 'design'):
    pg = Polygon(frame_to_enu(o[key]['polygon_m']))
    mrr = pg.minimum_rotated_rectangle; c = list(mrr.exterior.coords)
    e = [(c[i+1][0]-c[i][0], c[i+1][1]-c[i][1]) for i in range(2)]
    L = max(e, key=lambda v: math.hypot(*v)); W = min(e, key=lambda v: math.hypot(*v))
    brg = math.degrees(math.atan2(L[0], L[1])) % 180
    # angle of long axis to shoreline and to the shore normal
    ang_shore = abs(((brg - beta) + 90) % 180 - 90)
    res[key] = dict(rect_length_m=round(math.hypot(*L),1), rect_width_m=round(math.hypot(*W),1), long_axis_bearing_deg=round(brg,1),
                    long_axis_vs_shoreline_deg=round(ang_shore,1), area_m2=round(pg.area,1), rect_fill=round(pg.area/mrr.area,2))
# crest (landward/north) edge bearing: sat polygon apex (px 397,418) -> east tip (px 712,482)
P = json.load(open('polys_px.json'))['sat2026_trace']; a, b = np.array(P[0]), np.array(P[P.index([712,482])])
de, dn = (b[0]-a[0])*mpp, -(b[1]-a[1])*mpp
res['sat_crest_edge_bearing_apex_to_east_deg'] = round(math.degrees(math.atan2(de, dn)) % 360, 1)   # direction apex -> east tip
res['sat_crest_edge_bearing_east_to_apex_deg'] = round((math.degrees(math.atan2(de, dn)) + 180) % 360, 1)
res['sat_crest_edge_length_m'] = round(math.hypot(de, dn), 1)
# design: dashed crest line px (520,300)->(765,335) (read on zoom), north-up, 1.52 px/m
dd = np.array([765-520, -(335-300)]); res['design_dashed_line_bearing_east_to_west_deg'] = round((math.degrees(math.atan2(dd[0], dd[1])) + 180) % 360, 1)
# IoU: objective mask (T=30) vs manual trace
mk = Polygon(json.load(open('mask30_px.json'))).buffer(0); mn = Polygon(P)
res['iou_mask30_vs_manual'] = round(mk.intersection(mn).area/mk.union(mn).area, 3); res['mask30_area_m2'] = round(mk.area*mpp**2,0); res['mask30_inside_manual_frac'] = round(mk.intersection(mn).area/mk.area,3)
json.dump(res, open('analysis_out.json','w'), indent=1); print(json.dumps(res))
# extents along / across the crest line (bearing 281.5 sat; 278.1 design): "length" and "width" in the sense of the City's 165 m x 110 m
for key, brgk in (('sat', res['sat_crest_edge_bearing_east_to_apex_deg']), ('design', res['design_dashed_line_bearing_east_to_west_deg'])):
    E = frame_to_enu(o[key]['polygon_m']); u = np.array([math.sin(math.radians(brgk)), math.cos(math.radians(brgk))]); v = np.array([-u[1], u[0]])
    s, t = E@u, E@v
    res[key]['extent_along_crest_m'] = round(float(s.max()-s.min()),1); res[key]['extent_across_crest_m'] = round(float(t.max()-t.min()),1)
json.dump(res, open('analysis_out.json','w'), indent=1); print(res['sat'], res['design'])
