"""cables-reef-wa: trace of Blacka et al. (2013) Fig A.2 (Lyons 1992 design plan), registry cables-reef-wa-img-26.
Produces scripts/a2_trace.json: outer silhouette (interface line), design-ramp polygon (set-out line + crest line), scale evidence.
Run from the shape folder: python3 scripts/trace_a2.py   (numpy, scipy, skimage, shapely, PIL only)"""
import json, numpy as np
from PIL import Image
from scipy import ndimage as ndi
from skimage import measure
from shapely.geometry import Polygon
A2 = '../../../03_images/reefs/cables-reef-wa/cables-reef-wa_p8-figA2-design-lyons-1992_1992.png'
a = np.array(Image.open(A2).convert('L')).astype(float)
H, W = a.shape
# --- 1. silhouette of the drawn structure = outer foot ('interface line')
m = a < 215; m[620:, :] = False                    # rows >= 620 hold the caption
m = ndi.binary_closing(m, structure=np.ones((5, 5)))
lab, n = ndi.label(m); s = ndi.sum(m, lab, range(1, n + 1)); mm = ndi.binary_fill_holes(lab == 1 + int(np.argmax(s)))
mo = ndi.binary_opening(mm, structure=np.ones((11, 11)))
lab, n = ndi.label(mo); s = ndi.sum(mo, lab, range(1, n + 1)); sil = lab == 1 + int(np.argmax(s))
sil = ndi.binary_erosion(sil, iterations=1)         # undo ~1 px of outward bias of the closing
# --- 2. ramp region = silhouette minus the densely hatched rock bands
dens = ndi.uniform_filter((a < 200).astype(float), size=11)
band = ndi.binary_closing((dens > 0.22) & sil, structure=np.ones((7, 7)))
ramp = ndi.binary_opening(sil & ~band, structure=np.ones((9, 9)))
lab, n = ndi.label(ramp); s = ndi.sum(ramp, lab, range(1, n + 1)); ramp = lab == 1 + int(np.argmax(s))
ramp = ndi.binary_closing(ramp, structure=np.ones((25, 25)))      # label text / leaders notch the edge: close them
ramp = ndi.binary_fill_holes(ramp)
def contour_poly(mask, tol):
    c = max(measure.find_contours(mask.astype(float), 0.5), key=len)
    return Polygon([(float(x) + 0.5, float(y) + 0.5) for y, x in c]).simplify(tol)
P_sil = contour_poly(sil, 0.8); P_ramp = contour_poly(ramp, 0.8)
# --- 3. scale evidence (px per metre, native px of the 917 x 682 raster)
ev = {
 "transect_left_26.0m": {"px": [[257, 360], [355, 500]], "label_m": 26.0},
 "transect_right_30.0m": {"px": [[767, 268], [652, 425]], "label_m": 30.0},
}
for k, v in ev.items():
    (x0, y0), (x1, y1) = v['px']; v['len_px'] = round(float(np.hypot(x1 - x0, y1 - y0)), 1); v['px_per_m'] = round(v['len_px'] / v['label_m'], 3)
# centreline x=560 : dark-line rows (set-out inner band edge, RL -2.5, -2.0, -1.5, crest edge RL -1.0)
col = a[:, 560]; rows = [y for y in range(1, H - 1) if col[y] < 200 and col[y] <= col[y - 1] and col[y] <= col[y + 1]]
g = []
for y in rows:
    if g and y - g[-1][-1] <= 3: g[-1].append(y)
    else: g.append([y])
cl_all = [round(float(np.mean(t)), 1) for t in g if 80 < np.mean(t) < 360]
ev['centreline_x560_rows_all_dark_minima'] = cl_all
cl = [91.0, 154.0, 221.0, 286.0, 349.5]   # picked by eye from cl_all: set-out edge (RL -3.0), RL -2.5, -2.0, -1.5, crest edge (RL -1.0); 87, 260, 358 are hatch / label lines
ev['centreline_x560_rows_used'] = cl
sp = np.diff(cl[1:5])      # RL -2.5 -> -2.0 -> -1.5 -> -1.0 (3 intervals)
ev['contour_spacing_px_mean'] = round(float(np.mean(sp)), 2)
ev['contour_spacing_px_per_m_if_1in20_0.5m'] = round(float(np.mean(sp)) / 10.0, 3)
ev['dim_40.0m_from_to_rows'] = [cl[0], cl[-1]]; ev['dim_40.0m_px_per_m'] = round((cl[-1] - cl[0]) / 40.0, 3)   # 1:20 over 2 m (RL -3.0 to -1.0) = 40 m, matches the printed 40.0 m
vals = [ev['transect_left_26.0m']['px_per_m'], ev['transect_right_30.0m']['px_per_m'], ev['contour_spacing_px_per_m_if_1in20_0.5m'], ev['dim_40.0m_px_per_m']]
ev['scale_mean_px_per_m'] = round(float(np.mean(vals)), 3); ev['scale_sd'] = round(float(np.std(vals, ddof=1)), 3)
out = {"image": A2.split('/')[-1], "image_size": [W, H], "silhouette_px": [list(map(float, p)) for p in list(P_sil.exterior.coords)[:-1]],
       "ramp_px": [list(map(float, p)) for p in list(P_ramp.exterior.coords)[:-1]], "scale_evidence": ev,
       "silhouette_area_px2": P_sil.area, "ramp_area_px2": P_ramp.area, "silhouette_bounds_px": P_sil.bounds}
json.dump(out, open('scripts/a2_trace.json', 'w'))
print(len(out['silhouette_px']), len(out['ramp_px']), P_sil.bounds, round(P_sil.area), round(P_ramp.area))
print(json.dumps({k: v for k, v in ev.items()}, indent=0)[:900])
