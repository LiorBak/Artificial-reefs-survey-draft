#!/usr/bin/env python3
"""build_consent_georef.py - Opunake: consent occupation area (RMA coastal permit 6376-1) -> lat/lon, georeference of TRC 2009-33 Figure 1.

Run:  python3 -I build_consent_georef.py   (needs numpy, scipy, pyproj, PIL; reads src/ images and the LINZ/Esri crops in src/)
Writes: consent_georef.json (all numbers), src/trc2009-33_fig1_p9_reef_location.png.geo.json,
        overlays/*.png (checks).  Provenance of every input is in sources.md (ids c6376, fig1, fig2, trc_text) and METHOD.md (2026-10-13).
Nothing here is a measurement of the reef itself: the polygon is the LEGAL occupation area, the envelope is an ASSUMED placement.
"""
import json, math, sys
from pathlib import Path
import numpy as np
import pyproj
from pyproj import Transformer, Geod
from PIL import Image, ImageDraw
from scipy.ndimage import map_coordinates
Image.MAX_IMAGE_PIXELS = None

HERE = Path(__file__).resolve().parent.parent          # 07_scale/shapes/opunake-reef
pyproj.datadir.append_data_dir(str(HERE / "scripts" / "proj_grid"))   # LINZ nz_linz_nzgd2kgrid0005.tif (NZGD49 -> NZGD2000, 0.2 m)
SRC = HERE / "src"; OV = HERE / "overlays"

# ---- INPUT 1: consent 6376-1 corners as printed (TRC 2009-33 Appendix I, PDF p.39, scan; Taranaki local circuit grid = NZGD49 / Taranaki Circuit, EPSG:27209)
PRINTED = {"A": (257484, 663800), "B": (267650, 663887), "C": (267696, 663803), "D": (267525, 663718)}
# printed corner A reads 257484E; corrected to 267484E (typo: 10 km west of the bay, breaks the rectangle, contradicts GR P20:832-937)
CONS = {"A": (267484, 663800), "B": (267650, 663887), "C": (267696, 663803), "D": (267525, 663718)}

# ---- INPUT 2: pixel readings on TRC 2009-33 Fig 1 (embedded image 417 x 273 px), read by eye on 10x grids (+-0.5 px)
WHITE = {"A": (191.2, 134.0), "B": (227.5, 114.8), "C": (237.8, 133.8), "D": (200.2, 152.8)}   # white rectangle "Proposed location of surf reef" = consent area
ORANGE = {"A": (175.8, 127.5), "B": (239.5, 93.5), "C": (259.0, 134.2), "D": (193.0, 167.2)}   # orange "Area of water to be used during the construction process"
RAMP_FIG1 = (155.0, 125.5)      # light square at headland tip = "boat ramp and concrete hard-standing"
SCALEBAR_TICKS_PX = [9.5, 26.3, 42.2, 74.2]   # 0 / X / 2X / 4X ticks (labels illegible; 4X read as 300 m -> X = 75 m)

# ---- INPUT 3: independent landmark pick in Esri World Imagery 2025-01-16 (z18 frame fetched 2026-10-13, scratch): hardstanding at tip of headland
RAMP_ESRI_LONLAT = (173.8484984636307, -39.45910893659767)

to_ll = Transformer.from_crs(27209, 4326, always_xy=True)
to_nztm = Transformer.from_crs(27209, 2193, always_xy=True)
ll_to_c = Transformer.from_crs(4326, 27209, always_xy=True)
to_nzmg = Transformer.from_crs(27209, 27200, always_xy=True)
geod = Geod(ellps="WGS84")

def fit_affine(src, dst):
    A, b = [], []
    for (x, y), (E, N) in zip(src, dst):
        A += [[x, y, 1, 0, 0, 0], [0, 0, 0, x, y, 1]]; b += [E, N]
    p = np.linalg.lstsq(np.array(A, float), np.array(b, float), rcond=None)[0]
    return np.array([[p[0], p[1], p[2]], [p[3], p[4], p[5]]])
def apply(M, pt): return M @ np.array([pt[0], pt[1], 1.0])
def bearing(p, q): return math.degrees(math.atan2(q[0]-p[0], q[1]-p[1])) % 360
def dist(p, q): return math.hypot(q[0]-p[0], q[1]-p[1])
def shoelace(P):
    return 0.5*abs(sum(P[i][0]*P[(i+1) % len(P)][1]-P[(i+1) % len(P)][0]*P[i][1] for i in range(len(P))))

keys = "ABCD"
M = fit_affine([WHITE[k] for k in keys], [CONS[k] for k in keys])        # pixel -> circuit E,N
resid = {k: (apply(M, WHITE[k]) - np.array(CONS[k])).round(2).tolist() for k in keys}
sx = float(np.hypot(M[0, 0], M[1, 0])); sy = float(np.hypot(M[0, 1], M[1, 1]))
rot = math.degrees(math.atan2(M[1, 0], M[0, 0]))          # north-up image: pixel-x axis points east (rot ~ 0)
orange_c = {k: apply(M, ORANGE[k]).round(1).tolist() for k in keys}
ramp_c = apply(M, RAMP_FIG1)
ramp_ll = to_ll.transform(*ramp_c)
ramp_off_m = geod.inv(ramp_ll[0], ramp_ll[1], *RAMP_ESRI_LONLAT)[2]
bar_px = SCALEBAR_TICKS_PX[3]-SCALEBAR_TICKS_PX[0]

# ---- consent polygon facts
P = [CONS[k] for k in keys]
cen = (sum(p[0] for p in P)/4, sum(p[1] for p in P)/4)
long1, long2 = dist(P[0], P[1]), dist(P[3], P[2]); short1, short2 = dist(P[1], P[2]), dist(P[0], P[3])
b_long = (bearing(P[0], P[1]) + bearing(P[3], P[2]))/2          # grid bearing of the long sides (WSW-ENE)
b_short = (bearing(P[1], P[2]) + bearing(P[0], P[3]) + 360 if False else 0)
angles_at_corners = []
for i in range(4):
    a, b_, c = P[i-1], P[i], P[(i+1) % 4]
    v1 = (a[0]-b_[0], a[1]-b_[1]); v2 = (c[0]-b_[0], c[1]-b_[1])
    angles_at_corners.append(round(math.degrees(math.acos((v1[0]*v2[0]+v1[1]*v2[1])/(math.hypot(*v1)*math.hypot(*v2)))), 1))
ll = {k: to_ll.transform(*CONS[k]) for k in keys}
nztm = {k: to_nztm.transform(*CONS[k]) for k in keys}
nzmg = {k: to_nzmg.transform(*CONS[k]) for k in keys}
cen_ll = to_ll.transform(*cen); cen_nzmg = to_nzmg.transform(*cen)
# true azimuth of long axis (grid convergence)
az = geod.inv(ll["A"][0], ll["A"][1], ll["B"][0], ll["B"][1])[0] % 360
az2 = geod.inv(ll["D"][0], ll["D"][1], ll["C"][0], ll["C"][1])[0] % 360
az_true_long = (az+az2)/2
# ---- ASSUMED envelope: TRC 2009-33 p.4 'approximately 30 m wide, 3.5 m high, 99 m long' as a rectangle centred in the consent area, long axis // consent long axis
L_ENV, W_ENV = 99.0, 30.0
u = (math.sin(math.radians(b_long)), math.cos(math.radians(b_long)))     # unit vector along long axis (E,N), toward ENE
v = (-u[1], u[0])                                                        # 90 deg anticlockwise (toward NNW)
env = [(cen[0]+sx_*u[0]*L_ENV/2+sy_*v[0]*W_ENV/2, cen[1]+sx_*u[1]*L_ENV/2+sy_*v[1]*W_ENV/2) for sx_, sy_ in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
env_ll = [to_ll.transform(*p) for p in env]
# canonical local frame: origin = consent centre; +y = along long axis toward WSW (away from Opunake Beach = 'offshore' direction); +x = +y rotated 90 deg clockwise
by = (b_long+180) % 360                                                 # bearing of +y
def to_local(p):
    dE, dN = p[0]-cen[0], p[1]-cen[1]
    ey = (math.sin(math.radians(by)), math.cos(math.radians(by))); ex = (math.sin(math.radians(by+90)), math.cos(math.radians(by+90)))
    return [round(dE*ex[0]+dN*ex[1], 2), round(dE*ey[0]+dN*ey[1], 2)]
cons_local = [to_local(p) for p in P]; env_local = [to_local(p) for p in env]

out = {
 "generated": "2026-10-13", "script": "07_scale/shapes/opunake-reef/scripts/build_consent_georef.py",
 "crs_note": "Taranaki local circuit grid = NZGD49 / Taranaki Circuit (EPSG:27209; TM, origin 39 08 08.7 S 174 13 40.8 E, FE 300000, FN 700000). Converted to NZGD2000 (~WGS84) with the LINZ NZGD49->NZGD2000 grid nz_linz_nzgd2kgrid0005.tif (0.2 m; scripts/proj_grid/), verified against PROJ 7-parameter fallback (differs ~3.7 m).",
 "consent_printed_corners_E_N": PRINTED, "consent_used_corners_E_N": CONS, "typo_note": "Corner A printed 257484E; used 267484E (see sources.md c6376, METHOD.md 2026-10-13).",
 "consent_corners_lonlat_wgs84": {k: [round(ll[k][0], 7), round(ll[k][1], 7)] for k in keys},
 "consent_corners_nztm_E_N": {k: [round(nztm[k][0], 2), round(nztm[k][1], 2)] for k in keys},
 "consent_corners_nzmg_E_N": {k: [round(nzmg[k][0], 1), round(nzmg[k][1], 1)] for k in keys},
 "consent_centre": {"circuit_E_N": [round(cen[0], 1), round(cen[1], 1)], "lat": round(cen_ll[1], 6), "lon": round(cen_ll[0], 6), "nzmg_E_N": [round(cen_nzmg[0], 1), round(cen_nzmg[1], 1)]},
 "gr_check": "Consent text GR P20:832-937 (NZMS 260 sheet P20, 100 m) -> NZMG E 2583200 N 6193700; polygon corners lie at NZMG E 2583212-2583424 N 6193565-6193732 (corner A = 832-936): consistent, ~100 m rounding.",
 "consent_polygon": {"sides_m": {"A-B": round(long1, 1), "D-C": round(long2, 1), "B-C": round(short1, 1), "A-D": round(short2, 1)},
     "mean_long_m": round((long1+long2)/2, 1), "mean_short_m": round((short1+short2)/2, 1), "corner_angles_deg": angles_at_corners,
     "area_m2": round(shoelace(P), 0), "long_axis_grid_bearing_deg": round(b_long, 1), "long_axis_true_azimuth_deg": round(az_true_long, 1)},
 "fig1_georef": {"image": "src/trc2009-33_fig1_p9_reef_location.png", "px": [417, 273], "gcps": "4 corners of the white rectangle <-> 4 consent corners (affine, 6 parameters, 2 degrees of freedom check)",
     "gcp_pixels": WHITE, "gcp_circuit_E_N": CONS, "residuals_m": resid,
     "affine_pixel_to_circuitEN": M.round(5).tolist(), "m_per_px_x": round(sx, 3), "m_per_px_y": round(sy, 3), "image_rotation_deg_from_north_up": round(rot, 2),
     "scalebar": {"bar_px_0_to_4X": round(bar_px, 1), "m_per_px_if_4X_equals_300m": round(300/bar_px, 3), "labels": "illegible at 417 px width; tick spacing 1:1:2 and 3-character labels at ticks 3 and 4 -> 0/75/150/300 m inferred; matches the consent-derived 4.4-4.5 m/px within 3-5 %"},
     "orange_corners_circuit_E_N": orange_c,
     "orange_note": "orange rectangle = 'Area of water to be used during the construction process' (not a consent boundary in the text we hold)",
     "landmark_check": {"boat_ramp_pixel": RAMP_FIG1, "predicted_lonlat": [round(ramp_ll[0], 6), round(ramp_ll[1], 6)], "esri_2025_pick_lonlat": [round(RAMP_ESRI_LONLAT[0], 6), round(RAMP_ESRI_LONLAT[1], 6)],
         "offset_m": round(ramp_off_m, 1), "pick_uncertainty_m": "5-10 (hardstanding picked by eye in both images)", "meaning": "independent of the 4 GCPs: confirms white rectangle = consent area, figure north-up at ~4.5 m/px"}},
 "envelope_assumed": {"what": "99 m x 30 m rectangle (TRC 2009-33 p.4), centred on the consent centre, long axis parallel to the consent long axis (ASSUMPTION: orientation and centring; 99 m cannot fit across the 94 m short side, so it lies within ~47 deg of the long axis)",
     "corners_circuit_E_N": [[round(p[0], 1), round(p[1], 1)] for p in env], "corners_lonlat": [[round(p[0], 7), round(p[1], 7)] for p in env_ll], "area_m2": round(L_ENV*W_ENV, 0)},
 "canonical_frame": {"frame": "metres; origin = consent-area centre (no single shoreline point: headland rock shore ~90 m NW of the polygon, Opunake Beach 300+ m E-SE); +y along the consent long axis toward bearing %.1f deg grid (WSW, away from the beach); +x = +y rotated 90 deg clockwise (bearing %.1f)" % (by, (by+90) % 360),
     "consent_polygon_m": cons_local, "envelope_m": env_local},
}
(HERE / "consent_georef.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
# sidecar for the Fig 1 image
side = {"image": "trc2009-33_fig1_p9_reef_location.png", "width": 417, "height": 273, "crs": "EPSG:27209 (NZGD49 / Taranaki Circuit), E,N metres",
        "affine_pixel_to_EN": M.round(5).tolist(), "m_per_px": [round(sx, 3), round(sy, 3)], "method": "4 GCPs = consent 6376-1 corners; see consent_georef.json",
        "residuals_m": resid, "accuracy": "+-0.5 px reading = +-2.2 m; landmark check offset %.1f m" % ramp_off_m,
        "source": "TRC Technical Report 2009-33 (Sept 2009), p.9 Figure 1", "retrieved": "2026-10-13 from new uploads from lior/ PDF"}
(SRC / "trc2009-33_fig1_p9_reef_location.png.geo.json").write_text(json.dumps(side, indent=1), encoding="utf-8")
print(json.dumps({k: out[k] for k in ("consent_centre", "consent_polygon")}, indent=0))
print("fig1 m/px", round(sx, 3), round(sy, 3), "rot", round(rot, 2), "resid", resid, "ramp offset m", round(ramp_off_m, 1))
print("envelope circuit", [[round(p[0], 1), round(p[1], 1)] for p in env]); print("local cons", cons_local, "env", env_local)

# ---------------- overlays ----------------
def circuit_grid(E0, E1, N0, N1, step):
    Es = np.arange(E0, E1, step); Ns = np.arange(N1, N0, -step)
    EE, NN = np.meshgrid(Es, Ns); return EE, NN
def sample_esri(EE, NN):
    g = json.loads((Path("/tmp/claude-0/opunake/esri_z18_wide.png.geo.json")).read_text()); b = g["bounds"]; W, H = g["width"], g["height"]
    t3857 = Transformer.from_crs(4326, 3857, always_xy=True)
    x0, y1 = t3857.transform(b["west"], b["north"]); x1, y0 = t3857.transform(b["east"], b["south"])
    lon, lat = to_ll.transform(EE.ravel(), NN.ravel()); X, Y = t3857.transform(lon, lat)
    px = (X-x0)/(x1-x0)*W; py = (y1-Y)/(y1-y0)*H
    im = np.array(Image.open("/tmp/claude-0/opunake/esri_z18_wide.png").convert("RGB")).astype(float)
    ch = [map_coordinates(im[..., c], [py, px], order=1).reshape(EE.shape) for c in range(3)]
    return np.stack(ch, -1).astype(np.uint8)
if "--overlays" in sys.argv:
    OV.mkdir(exist_ok=True)
    E0, E1, N0, N1, st = 267050, 267950, 663450, 664150, 0.8
    EE, NN = circuit_grid(E0, E1, N0, N1, st)
    base = Image.fromarray(sample_esri(EE, NN)).convert("RGB")
    # warp Fig 1 into the same frame (inverse affine)
    Minv = np.linalg.inv(np.vstack([M, [0, 0, 1]]))
    xy = Minv @ np.vstack([EE.ravel(), NN.ravel(), np.ones(EE.size)]); fx, fy = xy[0].reshape(EE.shape), xy[1].reshape(EE.shape)
    f1 = np.array(Image.open(SRC / "trc2009-33_fig1_p9_reef_location.png").convert("RGB")).astype(float)
    warped = np.stack([map_coordinates(f1[..., c], [fy, fx], order=1, cval=-1) for c in range(3)], -1)
    mask = (fx >= 0) & (fx <= 416) & (fy >= 0) & (fy <= 272)
    bl = np.array(base).astype(float); bl[mask] = 0.5*bl[mask]+0.5*warped[mask]
    img = Image.fromarray(bl.astype(np.uint8)); d = ImageDraw.Draw(img)
    pxf = lambda p: ((p[0]-E0)/st, (N1-p[1])/st)
    d.polygon([pxf(p) for p in P], outline=(255, 255, 0), width=2)
    d.text((8, 8), "Fig 1 of TRC 2009-33 (50 percent) warped onto Esri 2025-01-16; yellow = consent 6376-1 polygon from printed coordinates", fill=(255, 255, 0))
    img.thumbnail((1200, 1200)); img.save(OV / "fig1_georef_check_on_esri2025.png"); print("wrote overlay 1", img.size)
    # overlay 2: consent polygon + envelope on LINZ 2011-12 (0.4 m, EPSG:2193) and Esri
    lg = json.loads((SRC / "linz_aerial_2011-12_0.4m_crop.png.geo.json").read_text())
    li = Image.open(SRC / "linz_aerial_2011-12_0.4m_crop.png").convert("RGB"); d = ImageDraw.Draw(li)
    tp = lambda p: ((to_nztm.transform(*p)[0]-lg["x_left"])/lg["px_m"], (lg["y_top"]-to_nztm.transform(*p)[1])/lg["px_m"])
    d.polygon([tp(p) for p in P], outline=(255, 255, 0), width=5)
    d.polygon([tp(p) for p in env], outline=(255, 60, 60), width=5)
    c = tp(cen); li = li.crop((int(c[0]-650), int(c[1]-450), int(c[0]+650), int(c[1]+450))); li.thumbnail((1200, 1200)); li.save(OV / "consent_area_and_envelope_on_linz2011-12.png"); print("wrote overlay 2", li.size)
