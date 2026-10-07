"""trace_s3.py - reproduces the primary trace of Narrowneck Reef on src/wayback/nn_wayback_2020-08-08_r9812_z19.png (s3)
and the shoreline frame from src/wayback/nn_wayback_2020-08-08_r9812_z17_shoreline_context.png (s7).
Run:  python trace_s3.py   (writes trace_s3_out.json next to it).  Written 2026-10-06; needs numpy, opencv-python, pillow, shapely.
Method (see METHOD.md Steps 2a, 2b): green channel, blur 1 px, threshold < 49; closing radius 14 px per arm; Douglas-Peucker 3 px.
"""
import numpy as np, cv2, json, math, os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
im = np.asarray(Image.open(HERE + "/src/wayback/nn_wayback_2020-08-08_r9812_z19.png").convert("RGB"))
g = cv2.GaussianBlur(im[:, :, 1].astype(np.float32), (0, 0), 1.0)
m = (g < 49).astype(np.uint8)
win = np.zeros_like(m); win[500:1020, 240:880] = 1
m *= win
n, lab, st, cen = cv2.connectedComponentsWithStats(m, 8)
keep = np.zeros_like(m)
for i in range(1, n):
    if st[i, cv2.CC_STAT_AREA] >= 60: keep[lab == i] = 1
box = (378, 950, 415, 992)                       # SW container of the south arm: looser threshold in one box
add = np.zeros_like(keep); add[box[1]:box[3], box[0]:box[2]] = (g[box[1]:box[3], box[0]:box[2]] < 53)
keep = np.maximum(keep, add)
n, lab, st, cen = cv2.connectedComponentsWithStats(keep, 8)
reps = {'n_main': (600, 680), 'n_leg': (454, 705), 'n_top1': (456, 558), 'n_top2': (454, 571),
        's_main': (606, 896), 's_15': (436, 886), 's_14': (521, 849), 's_13': (436, 831), 's_17': (399, 879),
        's_19': (386, 922), 's_20': (443, 945), 's_21': (616, 949), 's_sw': (393, 972),
        'wing_a1': (331, 581), 'wing_a2': (382, 547), 'wing_b1': (328, 662), 'wing_b2': (340, 630)}
ids = {k: int(lab[y, x]) for k, (x, y) in reps.items()}
def comps(keys):
    out = np.zeros_like(keep)
    for k in keys: out[lab == ids[k]] = 1
    return out
def envelope(mk, r):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    pad = np.pad(mk, r + 2); c = cv2.morphologyEx(pad, cv2.MORPH_CLOSE, k)[r + 2:-(r + 2), r + 2:-(r + 2)]
    n2, l2, s2, c2 = cv2.connectedComponentsWithStats(c, 8)
    mm = np.zeros_like(c)
    for j in range(1, n2):
        if mk[l2 == j].any(): mm[l2 == j] = 1
    return mm
def contour(mk, eps):
    cs, _ = cv2.findContours(mk, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return cv2.approxPolyDP(max(cs, key=cv2.contourArea), eps, True)[:, 0, :].tolist()
spec = {'north_arm': (['n_main', 'n_leg', 'n_top1', 'n_top2'], 14),
        'south_arm': (['s_main', 's_15', 's_14', 's_13', 's_17', 's_19', 's_20', 's_21', 's_sw'], 14),
        'wing_patch_NW_a': (['wing_a1', 'wing_a2'], 10), 'wing_patch_NW_b': (['wing_b1', 'wing_b2'], 10)}
polys = {k: contour(envelope(comps(keys), r), 3.0) for k, (keys, r) in spec.items()}
polys['weir_1'] = [[426, 767], [488, 772], [485, 776], [455, 777], [429, 773]]                       # read by eye (6x zoom)
polys['weir_2_faint'] = [[421, 790], [430, 786], [448, 787], [455, 788], [470, 787], [472, 791], [462, 793], [440, 793], [425, 793]]
polys['weir_3_faint'] = [[452, 808], [460, 806], [468, 806], [478, 810], [490, 812], [488, 815], [475, 813], [462, 813], [452, 811]]
extras = {k: contour((lab == lab[y, x]).astype(np.uint8), 2.0) for k, (x, y) in
          {'sea_patch_1': (794, 555), 'sea_patch_7': (839, 633), 'sea_patch_9': (875, 652)}.items() if lab[y, x] > 0}
# shoreline from the z17 image: eastmost sand pixel (R-B > 8 after blur) on every 10th row, x = a*y + b
z = np.asarray(Image.open(HERE + "/src/wayback/nn_wayback_2020-08-08_r9812_z17_shoreline_context.png").convert("RGB")).astype(np.float32)
d = cv2.GaussianBlur(z[:, :, 0] - z[:, :, 2], (0, 0), 2)
pts = []
for y in range(0, z.shape[0], 10):
    xs = np.where(d[y, 900:1500] > 8)[0]
    if len(xs): pts.append((900 + xs.max(), y))
pts = np.array(pts, float); a, b = np.polyfit(pts[:, 1], pts[:, 0], 1)
bearing_north_heading = (180 - math.degrees(math.atan(a)) + 180) % 360
json.dump({'polygons_px': polys, 'extras_px': extras, 'component_ids': ids, 'waterline_slope_a_z17': a,
           'shoreline_bearing_north_heading_deg': bearing_north_heading, 'n_waterline_rows': len(pts)},
          open(HERE + "/trace_s3_out.json", "w"))
print({k: len(v) for k, v in polys.items()}, 'shoreline bearing', round(bearing_north_heading, 2))
