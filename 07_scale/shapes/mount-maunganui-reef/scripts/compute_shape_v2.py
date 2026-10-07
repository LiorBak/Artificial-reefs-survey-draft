"""Mount Maunganui reef - canonical shape (v2, 2026-10-05 run #4).
Inputs: work_polys_fig3_m20_v2.json (Fig 3 -2.0 m CD bag-field outlines, native px), work_installed_toe_fig3px.json (ASR Installed outlines warped into Fig 3 px),
work_shoreline_px.json (wet/dry-sand line, Esri 2011-01-15 z18 wide), calibration in geo_tools.py.
Chain: Fig 3 px -> BOPTM E,N (tick calibration) -> metres -> rotate: +x alongshore toward NW (grid bearing along_b), +y offshore (along_b+90) ; origin = nearest point of the shoreline line to the survey-outline centroid.
Writes ../work_canonical_v2.json. Cross-checks with geom.py make_canonical (explicit-rotation result must agree to < 0.01 m)."""
import json, math, sys, copy
import numpy as np
from itertools import combinations
from pyproj import Geod
from shapely.geometry import Polygon
from shapely.ops import unary_union
sys.path.insert(0, '.')
from geo_tools import *
sys.path.insert(0, 'C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/07_scale/tools')
import geom
from satellite import pix2ll

polys_px = json.load(open(ROOT + 'work_polys_fig3_m20_v2.json'))
toe_all = json.load(open(ROOT + 'work_installed_toe_fig3px.json'))
toe_px = toe_all['-4.2']; mid_px = toe_all['-3.8']
polys_en = [[f3_en(x, y) for x, y in p] for p in polys_px]
g = Geod(ellps='WGS84')
e0, n0 = 376740.0, 812880.0
lon0, lat0 = T_boptm_to_ll.transform(e0, n0)
lon1, lat1, _ = g.fwd(lon0, lat0, 0.0, 1000.0)
e1, n1 = T_ll_to_boptm.transform(lon1, lat1)
true_north_in_grid = math.degrees(math.atan2(e1 - e0, n1 - n0))          # grid bearing of true north
tb = lambda gb: (gb - true_north_in_grid) % 360.0                         # grid bearing -> true bearing
sh = json.load(open(ROOT + 'work_shoreline_px.json'))
geo = json.load(open(ROOT + 'src/esri_wayback_2011-01-15_z18_wide.png.geo.json'))
def sat_en(x, y):
    lat, lon = pix2ll(geo, x, y); return T_ll_to_boptm.transform(lon, lat)
s1, s2 = sat_en(*sh['p1']), sat_en(*sh['p2'])
d_sh = np.array(s2) - np.array(s1)
shore_grid_b = math.degrees(math.atan2(d_sh[0], d_sh[1])) % 360.0
if abs(((shore_grid_b - 136 + 180) % 360) - 180) > 90: shore_grid_b = (shore_grid_b + 180) % 360
along_b = (shore_grid_b + 180) % 360; off_b = (along_b + 90) % 360
ux = np.array([math.sin(math.radians(along_b)), math.cos(math.radians(along_b))])
uy = np.array([math.sin(math.radians(off_b)), math.cos(math.radians(off_b))])
sd = np.array([math.sin(math.radians(shore_grid_b)), math.cos(math.radians(shore_grid_b))])
U = unary_union([Polygon(p) for p in polys_en]); cen = np.array([U.centroid.x, U.centroid.y])
foot = np.array(s1) + sd * np.dot(cen - np.array(s1), sd); O = foot
def canon(pt):
    q = np.array(pt) - O; return (float(q @ ux), float(q @ uy))
def to_m(polys_px_): return [[canon(f3_en(x, y)) for x, y in p] for p in polys_px_]
polys_m = to_m(polys_px); toe_m = to_m(toe_px); mid_m = to_m(mid_px)
def stats(pm):
    P = [Polygon(p) for p in pm]; Um = unary_union(P)
    pts = np.array([c for p in pm for c in p]); hull = np.array(Um.convex_hull.exterior.coords)
    md = max(np.linalg.norm(a - b) for a, b in combinations(hull, 2))
    mrr = Um.minimum_rotated_rectangle; mc = np.array(mrr.exterior.coords)
    e1_ = np.linalg.norm(mc[1] - mc[0]); e2_ = np.linalg.norm(mc[2] - mc[1])
    return dict(area_m2=round(sum(p.area for p in P), 1), n_polys=len(P), comp_areas_m2=[round(p.area, 1) for p in P],
                bbox_alongshore_m=round(float(pts[:, 0].max() - pts[:, 0].min()), 1), bbox_crossshore_m=round(float(pts[:, 1].max() - pts[:, 1].min()), 1),
                x_range=[round(float(pts[:, 0].min()), 1), round(float(pts[:, 0].max()), 1)], y_range=[round(float(pts[:, 1].min()), 1), round(float(pts[:, 1].max()), 1)],
                max_dim_m=round(float(md), 1), min_rot_rect_m=[round(float(max(e1_, e2_)), 1), round(float(min(e1_, e2_)), 1)],
                centroid_m=[round(Um.centroid.x, 1), round(Um.centroid.y, 1)])
res = dict(true_north_in_grid_deg=true_north_in_grid, shoreline_grid_bearing_deg=shore_grid_b, shoreline_true_bearing_deg=tb(shore_grid_b),
           alongshore_x_true_bearing_deg=tb(along_b), offshore_y_true_bearing_deg=tb(off_b),
           origin_boptm_en=[float(O[0]), float(O[1])], centroid_boptm_en=[float(cen[0]), float(cen[1])])
lon_o, lat_o = T_boptm_to_ll.transform(*O); res['origin_latlon'] = [round(lat_o, 7), round(lon_o, 7)]
res['survey'] = stats(polys_m); res['toe_installed_T-4.2'] = stats(toe_m); res['mid_installed_T-3.8'] = stats(mid_m)
res['survey_polygons_m'] = [[[round(x, 2), round(y, 2)] for x, y in p] for p in polys_m]
res['toe_polygons_m'] = [[[round(x, 2), round(y, 2)] for x, y in p] for p in toe_m]
def ll(en): lon, lat = T_boptm_to_ll.transform(*en); return [round(lat, 7), round(lon, 7)]
res['survey_polygons_latlon'] = [[ll(f3_en(x, y)) for x, y in p] for p in polys_px]
res['toe_polygons_latlon'] = [[ll(f3_en(x, y)) for x, y in p] for p in toe_px]
res['survey_polygons_en_boptm'] = [[[round(a, 2), round(b, 2)] for a, b in p] for p in polys_en]
cen_en = np.array(U.centroid.coords[0]); lon_c, lat_c = T_boptm_to_ll.transform(*cen_en); res['survey_centroid_latlon'] = [round(lat_c, 7), round(lon_c, 7)]
res['dist_survey_centroid_to_shoreline_m'] = float(np.linalg.norm(cen - foot))
# --- cross-check against geom.make_canonical (fixed 2026-10-05) using Fig 3 pixel polygons
ox_px, oy_px = en_f3(*O)
adx, ady = math.sin(math.radians(along_b)), -math.cos(math.radians(along_b))     # alongshore dir in pixel space (x east, y down)
tmp = {'sources': [{'id': 'img1', 'pixel_polygons': polys_px, 'scale': {'px_per_m': F3_PXM}}]}
import tempfile, os
fn = os.path.join(tempfile.gettempdir(), 'mmr_tmp_shape.json'); json.dump(tmp, open(fn, 'w'))
can = geom.make_canonical(fn, 'img1', (ox_px, oy_px), (adx, ady), alongshore_compass_deg=tb(along_b), write=False)
dmax = max(math.hypot(a[0] - b[0], a[1] - b[1]) for pa, pb in zip(can['polygons_m'], polys_m) for a, b in zip(pa, pb))
res['geom_make_canonical_check'] = dict(max_vertex_diff_m=dmax, area_m2=can['area_m2'], bbox=can['bbox_m'], max_dim_m=can['max_dim_m'], shore_normal_bearing_deg=can['shore_normal_bearing_deg'])
json.dump(res, open(ROOT + 'work_canonical_v2.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if not k.endswith(('polygons_m', 'polygons_latlon', 'polygons_en_boptm'))}, indent=1))
