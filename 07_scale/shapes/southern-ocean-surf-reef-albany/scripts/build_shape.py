"""Builds the canonical frame + metric results for southern-ocean-surf-reef-albany. Run: python -I build_shape.py
Inputs: src/esri_current_2026-01-20_z18.png(+.geo.json), polys_px.json (traced polygons), src/rwr_bluecoast_design_diagram.png.
Output: build_out.json (all numbers quoted in METHOD.md / shape.json)."""
import json, math
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from shapely.geometry import Polygon
from shapely import affinity
H = '..'
geo = json.load(open(f'{H}/src/esri_current_2026-01-20_z18.png.geo.json'))
mpp = geo['m_per_px_center']; cx = cy = 511.0   # image centre px = (lat -35.018, lon 117.9207) (checked with satellite.py pix2ll)
P = json.load(open('polys_px.json'))
sat = np.array(P['sat2026_trace']); des = np.array(P['design_diagram_trace'])
def enu(px):  # px -> east, north metres about image centre
    px = np.asarray(px, float); return np.c_[(px[:,0]-cx)*mpp, -(px[:,1]-cy)*mpp]
# ---- shoreline (swash/dry-sand edge): seaward end of the first bright (R>165) dry-sand run = 'beach-face line' (the true swash line is ~10-15 m further seaward, foam makes it unmeasurable by threshold), rows 40-320 and 440-720
a = np.asarray(Image.open(f'{H}/src/esri_current_2026-01-20_z18.png').convert('RGB')).astype(float)
R = gaussian_filter(a[...,0], 2); pts = []
for y in list(range(40, 321, 20)) + list(range(440, 721, 20)):
    xs = np.where(R[y] > 165)[0]; run = xs[0]
    for x in xs[1:]:
        if x - run > 6: break
        run = x
    pts.append((run, y))
pts = np.array(pts, float); E = enu(pts)
# robust (Theil-Sen) fit east = k*north + c on the section beside the reef (rows 440-720); whole-beach and northern-section bearings kept for the uncertainty
from scipy.stats import theilslopes
n1 = len(list(range(40,321,20)))
def ts(sel):
    s_, i_, lo_, hi_ = theilslopes(E[sel,0], E[sel,1]); return s_, i_, math.degrees(math.atan(s_)), math.degrees(math.atan(lo_)), math.degrees(math.atan(hi_))
k, c, beta, blo, bhi = ts(slice(n1, None))
beta_all = ts(slice(None))[2]; beta_n = ts(slice(0, n1))[2]; beta_s = beta
res = E[n1:,0] - (k*E[n1:,1] + c)
beta = beta % 360
u_al = np.array([math.sin(math.radians(beta)), math.cos(math.radians(beta))])      # +x alongshore (east,north)
u_of = np.array([math.sin(math.radians(beta+90)), math.cos(math.radians(beta+90))]) # +y offshore
# shoreline point: line through (east=c, north=0) direction u_al
def to_frame(e, origin):
    d = e - origin; return np.c_[d@u_al, d@u_of]
S = enu(sat); cen = np.array(Polygon(S).centroid.coords[0])
p0 = np.array([c, 0.0])
foot = p0 + ((cen-p0)@u_al)*u_al   # foot of perpendicular from reef centroid onto the shoreline
sat_m = to_frame(S, foot)
def stats(m):
    pg = Polygon(m); b = pg.bounds
    return dict(area_m2=round(pg.area,1), x_range=[round(b[0],1), round(b[2],1)], y_range=[round(b[1],1), round(b[3],1)],
                alongshore=round(b[2]-b[0],1), crossshore=round(b[3]-b[1],1),
                centroid=[round(pg.centroid.x,1), round(pg.centroid.y,1)])
out = dict(mpp=mpp, shoreline=dict(points_px=pts.tolist(), bearing_deg=round(beta,2), bearing_north_section_rows40_320=round(beta_n,2), bearing_whole_beach=round(beta_all,2), bearing_ci95_rows440_720=[round(blo,1),round(bhi,1)], resid_rms_m=round(float(np.sqrt((res**2).mean())),2), resid_median_abs_m=round(float(np.median(abs(res))),2),
           shore_normal_bearing_deg=round((beta+90)%360,2)),
           origin_enu_from_centre=foot.tolist())
out['sat'] = stats(sat_m); out['sat']['polygon_m'] = np.round(sat_m,2).tolist()
mx = max(((i,j) for i in range(len(sat_m)) for j in range(i)), key=lambda t: np.linalg.norm(sat_m[t[0]]-sat_m[t[1]]))
out['sat']['max_dim_m'] = round(float(np.linalg.norm(sat_m[mx[0]]-sat_m[mx[1]])),1)
out['sat']['nearest_edge_from_shoreline_m'] = round(float(sat_m[:,1].min()),1)
# ---- design diagram: 1.52 px/m (scale bar ticks 493.5 / 569.5 / 645.5 px = 0 / 50 / 100 m), north up (verified by crest bearing)
ppm = (645.5-493.5)/100.0
D = np.c_[des[:,0]/ppm, -des[:,1]/ppm]          # east, north (north-up)
D_fr = to_frame(D, np.zeros(2))                 # frame axes, arbitrary origin; translation found next
dpg = Polygon(D_fr); spg = Polygon(sat_m)
best = None
for dx in np.arange(-120, 120.1, 1.0):
    pass
# translation fit by maximising IoU (coarse then fine)
def iou(t):
    q = affinity.translate(dpg, t[0], t[1]); return q.intersection(spg).area / q.union(spg).area
cx0 = np.array(spg.centroid.coords[0]) - np.array(dpg.centroid.coords[0]); t = cx0.copy(); bi = iou(t)
for step in (8, 4, 2, 1, .5):
    imp = True
    while imp:
        imp = False
        for d in ((step,0),(-step,0),(0,step),(0,-step)):
            tt = t + d; v = iou(tt)
            if v > bi + 1e-6: t, bi, imp = tt, v, True
des_m = D_fr + t
out['design'] = stats(des_m); out['design']['polygon_m'] = np.round(des_m,2).tolist()
out['design']['scale_px_per_m'] = ppm; out['design']['translation_fit_m'] = np.round(t,1).tolist()
out['design']['iou_vs_sat_after_translation'] = round(bi,3); out['design']['iou_centroid_aligned'] = round(iou(cx0),3)
# free similarity check (rotation + scale) to confirm north-up and scale bar
best = (bi, 0, 1.0)
for rot in np.arange(-15, 15.1, 1.0):
    for sc in np.arange(0.8, 1.21, 0.02):
        q0 = affinity.scale(affinity.rotate(dpg, rot, origin='centroid'), sc, sc, origin='centroid')
        t0 = np.array(spg.centroid.coords[0]) - np.array(q0.centroid.coords[0])
        q = affinity.translate(q0, *t0); v = q.intersection(spg).area/q.union(spg).area
        if v > best[0]: best = (v, rot, sc)
out['design']['free_fit'] = dict(iou=round(best[0],3), rot_deg=best[1], scale=round(best[2],2))
# IoU of mask-trace vs manual trace is computed in verify step
json.dump(out, open('build_out.json','w'), indent=1)
print(json.dumps({k:out[k] for k in ('shoreline',)}))
for k in ('sat','design'): print(k, {kk:v for kk,v in out[k].items() if kk!='polygon_m'})
