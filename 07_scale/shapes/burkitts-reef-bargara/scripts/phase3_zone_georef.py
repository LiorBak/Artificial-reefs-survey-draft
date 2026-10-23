"""Georeference the 'Bargara Reef Phase 3' work-zone annotations (Redgard, via Jackson & Corbett 2007 Fig. 1)
from the oblique aerial onto the Esri Wayback frame (image date 2016-07-31). Run: python -I phase3_zone_georef.py <shape folder>
Affine map from 3 ground control points (GCP): outer tip of rock wall B, root (south end) of wall B, outer tip of groyne A.
Oblique pixel coords are in the 1100x1100 grid of the photo crop (obl_grid, 2x of the 550 px photo at 300 dpi page render).
Sat pixel coords are in the 1180x1180 grid = 2x upscale of src/wayback/..._z18_north.png (591 px, 0.542 m/px)."""
import sys, json, math, numpy as np, pyproj
from pathlib import Path
root = Path(sys.argv[1]); geo = json.load(open(root/'src/wayback/burkitts_esri_wayback-rel23264_img2016-07-31_z18_north.png.geo.json'))
OBL = {'B_tip': (850, 172), 'B_root': (115, 165), 'A_tip': (640, 72)}
SAT = {'B_tip': (272, 298), 'B_root': (155, 600), 'A_tip': (122, 285)}
ELLIPSE = dict(c=(573, 386), a=225, b=52, tilt_deg=3.5)      # drawn ellipse in the oblique
ARROWS = {'Reprofile several surface rocks': (650, 250), 'Remove to lengthen break (arrow tip at ellipse end)': (815, 405),
          'Improve shore break': (880, 610), 'Reprofile dangerous rocks': (985, 905)}
def merc_y(l): return math.log(math.tan(math.pi/4+math.radians(l)/2))
def inv_y(m): return math.degrees(2*math.atan(math.exp(m))-math.pi/2)
def pix2ll(x, y):
    b = geo['bounds']; w, h = geo['width'], geo['height']
    lon = b['west']+(b['east']-b['west'])*x/w
    my = merc_y(b['north'])+(merc_y(b['south'])-merc_y(b['north']))*y/h
    return inv_y(my), lon
def fit(o, s):
    ks = list(o); A = np.array([[*o[k], 1] for k in ks], float)
    return np.linalg.solve(A, [s[k][0] for k in ks]), np.linalg.solve(A, [s[k][1] for k in ks])
px, py = fit(OBL, SAT); f = lambda u, v: (px@[u, v, 1], py@[u, v, 1])
tog = lambda p: pix2ll(p[0]*geo['width']/1180, p[1]*geo['height']/1180)
th = math.radians(ELLIPSE['tilt_deg']); c = ELLIPSE['c']; pts = []
for i in range(72):
    t = 2*math.pi*i/72; x = ELLIPSE['a']*math.cos(t); y = ELLIPSE['b']*math.sin(t)
    pts.append((c[0]+x*math.cos(th)-y*math.sin(th), c[1]+x*math.sin(th)+y*math.cos(th)))
ell_sat = [f(*p) for p in pts]; ell_ll = [tog(p) for p in ell_sat]
T = pyproj.Transformer.from_crs(4326, 32756, always_xy=True)
xy = np.array([T.transform(lo, la) for la, lo in ell_ll]); x, y = xy[:, 0], xy[:, 1]
area = 0.5*abs(np.dot(x, np.roll(y, -1))-np.dot(y, np.roll(x, -1)))
rng = np.random.default_rng(1); cs = []
for _ in range(2000):
    o = {k: (v[0]+rng.normal(0, 10), v[1]+rng.normal(0, 10)) for k, v in OBL.items()}
    s = {k: (v[0]+rng.normal(0, 8), v[1]+rng.normal(0, 8)) for k, v in SAT.items()}
    a, b = fit(o, s); cs.append((a@[*c, 1], b@[*c, 1]))
sd = (np.array(cs).std(0)*0.2710).round(1).tolist()   # grid px -> m (0.271 m per 1180-grid px)
res = {'what': 'Phase 3 work zones, georeferenced from oblique aerial (J&C 2007 Fig 1)', 'gcp_oblique': OBL, 'gcp_sat_grid': SAT,
       'affine_x': px.tolist(), 'affine_y': py.tolist(), 'ellipse_polygon_latlon': ell_ll,
       'ellipse_area_m2_utm56': round(area), 'ellipse_extent_EW_NS_m': [round(float(np.ptp(x))), round(float(np.ptp(y)))],
       'ellipse_centroid_latlon': [float(np.mean([p[0] for p in ell_ll])), float(np.mean([p[1] for p in ell_ll]))],
       'arrow_tips_latlon': {k: tog(f(*v)) for k, v in ARROWS.items()}, 'centre_sd_from_gcp_pick_noise_m': sd,
       'gcp_pick_noise': 'oblique 10 px, sat 8 grid px (1 sigma), Monte Carlo n=2000'}
json.dump(res, open(root/'scripts/phase3_zone_v1.json', 'w'), indent=1)
print(res['ellipse_area_m2_utm56'], res['ellipse_extent_EW_NS_m'], res['ellipse_centroid_latlon'], sd)
