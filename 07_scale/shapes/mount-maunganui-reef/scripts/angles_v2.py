"""Arm axes / angles (v2). Uses work_canonical_v2.json (canonical metres; +x alongshore toward true bearing X0, +y offshore X0+90).
For each outline polygon: PCA axis of the area (dense grid), minimum-rotated-rectangle long side, length/width; bearings are TRUE bearings (grid convergence -0.161 deg applied through the canonical frame bearing)."""
import json, math, numpy as np
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union
from shapely import prepared
R = 'C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/07_scale/shapes/mount-maunganui-reef/'
c = json.load(open(R + 'work_canonical_v2.json'))
X0 = c['alongshore_x_true_bearing_deg']; shore = c['shoreline_true_bearing_deg']
P = [Polygon(p) for p in c['survey_polygons_m']]
names = ['west arm block (3 bags)', 'mid-top bag', 'NE small bag', 'NE lobe (2 bags)', 'south (long) arm']
areas = [p.area for p in P]; order = np.argsort([-a for a in areas])
def vec_bearing(vx, vy):   # canonical vector -> true bearing: +x has bearing X0, +y has bearing X0+90
    ux = np.array([math.sin(math.radians(X0)), math.cos(math.radians(X0))]); uy = np.array([math.sin(math.radians(X0 + 90)), math.cos(math.radians(X0 + 90))])
    d = vx * ux + vy * uy; return math.degrees(math.atan2(d[0], d[1])) % 360
def ang_to_shore(b): return abs(((b % 180) - (shore % 180) + 90) % 180 - 90)
def axis_stats(poly_list):
    U = unary_union(poly_list); minx, miny, maxx, maxy = U.bounds; pu = prepared.prep(U)
    xs = np.arange(minx, maxx, 0.1); ys = np.arange(miny, maxy, 0.1)
    pts = np.array([(x, y) for x in xs for y in ys if pu.contains(Point(x, y))])
    m = pts.mean(0); w, v = np.linalg.eigh(np.cov((pts - m).T)); ax = v[:, 1]
    t = (pts - m) @ ax; n = (pts - m) @ np.array([-ax[1], ax[0]])
    mrr = U.minimum_rotated_rectangle; mc = np.array(mrr.exterior.coords)
    e = [mc[1] - mc[0], mc[2] - mc[1]]; L = max(e, key=np.linalg.norm)
    b_pca = vec_bearing(*ax) % 180; b_mrr = vec_bearing(*L) % 180
    return dict(area_m2=round(U.area, 1), centroid_m=[round(m[0], 1), round(m[1], 1)], pca_axis_true_bearing_deg=round(b_pca, 1), pca_angle_to_shoreline_deg=round(ang_to_shore(b_pca), 1),
                mrr_long_side_true_bearing_deg=round(b_mrr, 1), mrr_angle_to_shoreline_deg=round(ang_to_shore(b_mrr), 1),
                length_along_pca_m=round(float(t.max() - t.min()), 1), width_across_pca_m=round(float(n.max() - n.min()), 1), mrr_dims_m=[round(float(np.linalg.norm(L)), 1), round(float(min(np.linalg.norm(x) for x in e)), 1)])
out = {}
iw, im_, ines, inel, il = [list(range(5))[i] for i in range(5)]
# identify components by centroid x (canonical): west arm has x>0 (NW), long arm x<0
cent = [(p.centroid.x, p.centroid.y, p.area, i) for i, p in enumerate(P)]
big = sorted(cent, key=lambda t: -t[2])[:2]
west = [t for t in big if t[0] > 0][0][3]; south = [t for t in big if t[0] < 0][0][3]
rest = [t[3] for t in cent if t[3] not in (west, south)]
print('west', west, 'south', south, 'rest', rest, [P[i].centroid.coords[0] for i in rest])
out['west_arm_block'] = axis_stats([P[west]]); out['south_long_arm'] = axis_stats([P[south]])
# mid-top bag = rest component with centroid x>0 ; NE = x<0
top = [i for i in rest if P[i].centroid.x > 0][0]; ne = [i for i in rest if P[i].centroid.x < 0]
out['mid_top_bag'] = axis_stats([P[top]]); out['NE_lobe_group'] = axis_stats([P[i] for i in ne]); out['west_arm_incl_mid_top'] = axis_stats([P[west], P[top]])
out['whole'] = axis_stats(P)
# crest-core bearings (from cores.py, -1.2 m cores)
json.dump(out, open(R + 'work_angles_v2.json', 'w'), indent=1)
for k, v in out.items(): print(k, json.dumps(v))
b1 = out['west_arm_block']['pca_axis_true_bearing_deg']; b2 = out['south_long_arm']['pca_axis_true_bearing_deg']
print('angle between PCA axes (acute):', round(abs(((b1 - b2) + 90) % 180 - 90), 1))
