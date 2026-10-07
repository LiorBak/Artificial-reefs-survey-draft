#!/usr/bin/env python
"""
build_3d_lidar.py - STAGE 1 of the bunbury-airwave 3D build (this file is the original Step 3-5 build_3d.py of 2026-10-05, renamed).

Reads the WA Department of Transport airborne-lidar bathymetry grid BU2009TRBS_Lidar.bag (public download, see SOURCES_3D.md),
resamples it into the reef's model frame, fills surf-zone gaps, writes:
  data/lidar_stage_model.js     (the model as it was before Step 6; NOT the viewer's model.js any more)
  data/lidar_clip_model_frame.csv
  data/build_summary.json
  annotated/lidar_*.png, seabed_profile_with_tides.png, img1_trace_axes_scale.png
Run:  python build_3d_lidar.py --bag <path to BU2009TRBS_Lidar.bag>
Requires numpy scipy h5py pyproj matplotlib pillow.   The raw .bag (67 MB) is NOT stored in the project.

STAGE 2 = build_3d.py: reads data/lidar_clip_model_frame.csv, data/lidar_derived.json (frame, shoreline fit, native-resolution profile,
extracted from this stage's output on 2026-10-05) and the Navionics analysis, and writes model.js, docs.js and METHODS_3D.md. Stage 1 did NOT
have to be re-run for Step 6 (the .bag was not re-downloaded); apart from the output name of the model file below it is unchanged.

MODEL FRAME (metres)
  origin O  = foot of the perpendicular from the card-derived site point (-33.3276, 115.6284) on the fitted 0 m AHD contour
  +x        = alongshore, bearing 12.3 deg TRUE (NNE)   [grid bearing 11.56 deg, MGA94 z50]
  +y        = seaward, bearing 282.4 deg TRUE (WNW)     (x rotated 90 deg anticlockwise -> right-handed with z up)
  z         = up, 0 = MSL; MSL = +0.1 m AHD (GHD 2021 Table 1), so z = AHD - 0.1
"""
import argparse, json, math, os, sys
import numpy as np
import h5py
from pyproj import Transformer, Proj
from scipy.ndimage import map_coordinates
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon as MplPolygon
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SHAPE_DIR = os.path.dirname(HERE)
ap = argparse.ArgumentParser()
ap.add_argument("--bag", required=True)
args = ap.parse_args()

# ------------------------------------------------------------------ constants (each is traced in SOURCES_3D.md / provenance)
SITE_LL = (-33.3276, 115.6284)          # shape.json location_note.approx_centre_latlon (+-100 m)
MSL_AHD = 0.1                           # GHD 2021 Table 1, MSL +0.1 m AHD
TIDES_AHD = {"HAT": 0.6, "MHHW": 0.2, "MLHW": 0.1, "MSL": 0.1, "MHLW": 0.0, "MLLW": -0.2, "LAT": -0.6}
TIDES_CD = {"HAT": 1.3, "MHHW": 0.9, "MLHW": 0.7, "MSL": 0.7, "MHLW": 0.6, "MLLW": 0.5, "LAT": 0.1}
REEF_Y_DEFAULT = 37.5                   # shape.json canonical.distance_offshore_m (text midpoint 30-45/50 m)
X0G, Y0G = 361415.0, 6305610.0          # BAG cornerPoints: SW cell centre, MGA94 zone 50
CELL = 10.0

# ------------------------------------------------------------------ read BAG
f = h5py.File(args.bag, "r")
E = f["BAG_root/elevation"][:].astype(float)
U = f["BAG_root/uncertainty"][:].astype(float)
E = np.where(E >= 1e5, np.nan, E)
U = np.where(U >= 1e5, np.nan, U)
tr = Transformer.from_crs(4326, 28350, always_xy=True)
tr_inv = Transformer.from_crs(28350, 4326, always_xy=True)
XS, YS = tr.transform(SITE_LL[1], SITE_LL[0])
conv = Proj(28350).get_factors(SITE_LL[1], SITE_LL[0]).meridian_convergence   # +0.754 deg: true bearing = grid bearing + conv

# ------------------------------------------------------------------ fit the 0 m AHD contour near the site -> model frame
r0 = int(round((YS - Y0G) / CELL)); c0 = int(round((XS - X0G) / CELL))
R = 100
sub = E[r0 - R:r0 + R + 1, c0 - R:c0 + R + 1]
xs_e = (np.arange(c0 - R, c0 + R + 1)) * CELL + X0G - XS
ys_n = (np.arange(r0 - R, r0 + R + 1)) * CELL + Y0G - YS
pts = []
for i, yy in enumerate(ys_n):
    row = sub[i]
    for j in range(len(row) - 1):
        a, b = row[j], row[j + 1]
        if np.isfinite(a) and np.isfinite(b) and a < 0 <= b:
            pts.append((xs_e[j] + CELL * (0 - a) / (b - a), yy)); break
pts = np.array(pts)
m = np.abs(pts[:, 1]) <= 500
slope_b, icpt_a = np.polyfit(pts[m, 1], pts[m, 0], 1)           # east = a + b*north  (relative to site)
rms_contour = float(np.sqrt(np.mean((pts[m, 0] - (icpt_a + slope_b * pts[m, 1])) ** 2)))
tvec = np.array([slope_b, 1.0]); tvec /= np.linalg.norm(tvec)    # +x alongshore (grid E,N components)
nvec = np.array([-tvec[1], tvec[0]])                              # +y seaward
s_ = -icpt_a * slope_b / (1 + slope_b ** 2)
P = np.array([icpt_a + slope_b * s_, s_])
OX, OY = XS + P[0], YS + P[1]
dist_site_to_line = float(np.hypot(*P))
bear_x_grid = math.degrees(math.atan2(tvec[0], tvec[1])) % 360
bear_y_grid = math.degrees(math.atan2(nvec[0], nvec[1])) % 360
bear_x_true = (bear_x_grid + conv) % 360
bear_y_true = (bear_y_grid + conv) % 360
# north (true) as a vector in model (x,y)
def true_bearing_to_xy(b_true):
    b = math.radians((b_true - conv) % 360)                 # grid bearing
    e, n = math.sin(b), math.cos(b)
    return (e * tvec[0] + n * tvec[1], e * nvec[0] + n * nvec[1])
north_xy = true_bearing_to_xy(0.0)

def to_grid(x, y):
    return OX + x * tvec[0] + y * nvec[0], OY + x * tvec[1] + y * nvec[1]

def from_grid(gx, gy):
    dx, dy = gx - OX, gy - OY
    return dx * tvec[0] + dy * tvec[1], dx * nvec[0] + dy * nvec[1]

def sample(x, y, arr=E, order=1):
    gx, gy = to_grid(x, y)
    cc = (gx - X0G) / CELL; rr = (gy - Y0G) / CELL
    msk = np.isfinite(arr).astype(float); az = np.where(np.isfinite(arr), arr, 0.0)
    v = map_coordinates(az, [rr, cc], order=order, mode="nearest")
    w = map_coordinates(msk, [rr, cc], order=order, mode="nearest")
    return np.where(w > 0.999, v / np.where(w > 0, w, 1), np.nan)

# ------------------------------------------------------------------ seabed grid in model frame (5 m) + gap fill
GX = np.arange(-150, 150.1, 5.0); GY = np.arange(-40, 200.1, 5.0)
XX, YY = np.meshgrid(GX, GY)
Z_raw = sample(XX, YY)                                        # m AHD, NaN where no lidar return
valid = np.isfinite(Z_raw)
Pm = np.full(len(GY), np.nan)
for j in range(len(GY)):
    if valid[j].sum() >= 30:
        Pm[j] = np.nanmedian(Z_raw[j])
good = np.isfinite(Pm)
Pm_f = np.interp(GY, GY[good], Pm[good])                      # linear across the surf-zone rows
resid = Z_raw - Pm_f[:, None]
off = np.array([np.nanmedian(resid[(GY >= -40) & (GY <= 80), i]) if np.isfinite(resid[(GY >= -40) & (GY <= 80), i]).any() else 0.0
                for i in range(len(GX))])
k = 5
off_s = np.convolve(np.pad(off, (k // 2, k // 2), mode="edge"), np.ones(k) / k, mode="valid")
Z_ahd = np.where(valid, Z_raw, Pm_f[:, None] + off_s[None, :])
filled = (~valid).astype(int)
Z_msl = Z_ahd - MSL_AHD

# profile statistics for |x|<=100 (native-resolution sampling, step 2.5 m in y)
yy_p = np.arange(-40, 200.1, 2.5); xx_p = np.arange(-100, 100.1, 10.0)
Zp = sample(*np.meshgrid(xx_p, yy_p))
prof_med = np.nanmedian(Zp, axis=1)
with np.errstate(all="ignore"):
    prof_p10 = np.nanpercentile(Zp, 10, axis=1); prof_p90 = np.nanpercentile(Zp, 90, axis=1)
nvalid = np.isfinite(Zp).sum(axis=1)

def y_at_level(level):
    out = []
    for j in range(len(yy_p) - 1):
        a, b = prof_med[j], prof_med[j + 1]
        if np.isfinite(a) and np.isfinite(b) and (a - level) * (b - level) <= 0 and a != b:
            out.append(float(yy_p[j] + 2.5 * (level - a) / (b - a)))
    return out

def depth_at_y(y):
    return float(np.interp(y, yy_p[nvalid >= 10], prof_med[nvalid >= 10]))

mask_fit = (yy_p >= 30) & (yy_p <= 100)
slope_seabed = float(np.polyfit(yy_p[mask_fit], prof_med[mask_fit], 1)[0])

# ------------------------------------------------------------------ contours (from the filled 5 m grid)
levels_ahd = [0, -1, -2, -3, -4, -5, -6, -7, -8]
fig_c, ax_c = plt.subplots()
cs = ax_c.contour(GX, GY, Z_ahd, levels=sorted(levels_ahd))
contours = []
for lv, segs in zip(cs.levels, cs.allsegs):
    lines = [np.round(s, 1).tolist() for s in segs if len(s) > 1]
    contours.append({"ahd": float(lv), "z": round(float(lv) - MSL_AHD, 2), "polylines": lines})
plt.close(fig_c)

# ------------------------------------------------------------------ shape.json -> toe polygon
shape = json.load(open(os.path.join(SHAPE_DIR, "shape.json"), encoding="utf8"))
poly = shape["canonical"]["polygons_m"][0]
reef_info = {
    "diameter_text_m": 12.0, "area_m2_traced": shape["canonical"]["area_m2"], "bbox_m": shape["canonical"]["bbox_m"],
}

# ------------------------------------------------------------------ outputs: CSV
os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
os.makedirs(os.path.join(HERE, "annotated"), exist_ok=True)
with open(os.path.join(HERE, "data", "lidar_clip_model_frame.csv"), "w", encoding="utf8") as fh:
    fh.write("# WA DoT Lidar2009TRBS (BU2009TRBS_Lidar.bag) bilinear-resampled to the bunbury-airwave model frame, 5 m spacing.\n")
    fh.write("# x_m alongshore (+NNE, bearing %.1f true), y_m seaward from the fitted 0 m AHD contour (bearing %.1f true). Origin MGA94 z50 E%.1f N%.1f.\n" % (bear_x_true, bear_y_true, OX, OY))
    fh.write("# ahd_m = metres relative to AHD (source datum per DoT index); z_msl_m = ahd_m - %.2f; filled=1 where no lidar return (interpolated, see SOURCES_3D.md)\n" % MSL_AHD)
    fh.write("x_m,y_m,ahd_m,z_msl_m,filled\n")
    for j, yv in enumerate(GY):
        for i, xv in enumerate(GX):
            fh.write("%.0f,%.0f,%.3f,%.3f,%d\n" % (xv, yv, Z_ahd[j, i], Z_msl[j, i], filled[j, i]))

# ------------------------------------------------------------------ model.js
def r2(a): return np.round(a, 2).tolist()
water_levels = []
labels = {"HAT": "Highest Astronomical Tide", "MHHW": "Mean Higher High Water", "MLHW": "Mean Lower High Water", "MSL": "Mean Sea Level",
          "MHLW": "Mean Higher Low Water", "MLLW": "Mean Lower Low Water", "LAT": "Lowest Astronomical Tide (chart datum since 2009)"}
for key in ("LAT", "MLLW", "MHLW", "MSL", "MLHW", "MHHW", "HAT"):
    water_levels.append({"id": key, "label": labels[key], "z": round(TIDES_AHD[key] - MSL_AHD, 2), "ahd": TIDES_AHD[key],
                         "chart_datum_m": TIDES_CD[key], "source_id": "S_tide",
                         "note": "GHD 2021 Table 1, Port of Bunbury, rounded to 0.1 m"})
sources = [
    {"id": "S_shape", "title": "Verified plan shape (shape.json) - 29-vertex circle traced on the RWR drone photo img1", "url": "07_scale/shapes/bunbury-airwave/shape.json (img1: https://raisedwaterresearch.com/wp-content/uploads/2019/12/Airwave-from-Above.jpg)", "kind": "image-derived"},
    {"id": "S_RWR", "title": "Raised Water Research, Bunbury Airwave profile page", "url": "https://raisedwaterresearch.com/spot/artificial-reef/australia/western-australia/bunbury-airwave/", "kind": "text",
     "quote": "at low tide, the shallow point is about 1m under the surface of the water; rises about 2m off the sea floor at its highest point; 30-45 meters off the beach"},
    {"id": "S_Tracks19", "title": "Tracks Magazine 2019-11-15, Airwave set for live trial at Bunbury", "url": "https://tracksmag.com.au/airwave-set-for-live-trial-at-bunbury-534049", "kind": "text",
     "quote": "twelve metres in diameter and 1.6m tall at the highest point; approximately 45 metres off the low tide mark"},
    {"id": "S_ABC19", "title": "ABC News 2019-12-16, Bunbury's Back Beach surfers deflated", "url": "https://www.abc.net.au/news/2019-12-16/word-first-surf-reef-tears-during-installation/11803228", "kind": "text", "quote": "two-metre-high, 12-metre-wide, dome-like bladder"},
    {"id": "S_Tracks21", "title": "Tracks Magazine 2021-10-08, The Airwave Pumps Again", "url": "https://tracksmag.com.au/the-airwave-pumps-again", "kind": "text",
     "quote": "a bit of a skateboard ramp type thing happening ... now going for a more classic dome shape"},
    {"id": "S_Tradie", "title": "The Tradie Magazine 2019-01-31, Creating the Perfect Wave (quote seen in search text only; page 403)", "url": "https://www.tradiemagazine.com.au/creating-the-perfect-wave/", "kind": "text",
     "quote": "a very subtle, flattened dome with a steeply angled back"},
    {"id": "S_Surfer", "title": "SurferToday 2019-12-17, Ripped seam puts world's first inflatable surf reef on hold (page 403 to scripts; figure seen via search text)", "url": "https://www.surfertoday.com/surfing/ripped-seam-puts-worlds-first-inflatable-surf-reef-on-hold", "kind": "text", "quote": "50 meters from shore"},
    {"id": "S_lidar", "title": "WA Department of Transport bathymetry, Lidar2009TRBS ('Two Rocks - Naturaliste Lidar 2009'), 10 m grid, BAG", "url": "https://dotazprdauegisextpubst01.blob.core.windows.net/transport-wa-public/bathymetry/rasters/BU2009TRBS_Lidar.bag", "kind": "data",
     "note": "survey index: https://services6.arcgis.com/67Ks15nDmWoIbK8b/arcgis/rest/services/Survey_index_linkedbagfiles/FeatureServer/0 ; DataRestri NO; metadata 'Approved for Public Release', 'Not to be used for navigation'; md5 a5742ce2217aef90670cee1426f76933"},
    {"id": "S_tide", "title": "GHD (2021) Tidal Inundation Monitoring and Modelling Report, Table 1 Tidal planes for Port of Bunbury (source cited there: Dept of Defence 2018)", "url": "https://www.epa.wa.gov.au/sites/default/files/PER_documentation2/App%20B%20-%20Tidal%20innudation%20report.pdf", "kind": "table",
     "quote": "HAT +1.3 m CD / +0.6 m AHD ... MSL +0.7 / +0.1 ... LAT +0.1 / -0.6"},
    {"id": "S_DoTidx", "title": "WA DoT bathymetric survey index, Bunbury records: vertical datum LAT, AHD_Diff 0.57 BELOW", "url": "https://services6.arcgis.com/67Ks15nDmWoIbK8b/arcgis/rest/services/Survey_index_linkedbagfiles/FeatureServer/0", "kind": "data", "note": "LAT = AHD - 0.57 m at Bunbury (consistent with -0.6 above)"},
    {"id": "S_sat", "title": "Esri World Imagery, Back Beach, 2025-08-30 (private research copy, rights not cleared)", "url": "07_scale/shapes/bunbury-airwave/src/sat_backbeach_current.png", "kind": "image-derived", "note": "used only for the approximate reef location (waterline) and to draw the lidar contours over the beach"},
]
prov = [
    {"parameter": "reef plan outline", "value": "circle, 12.0 m (traced 29-vertex polygon, 112.1 m2)", "unit": "m", "source_id": "S_shape", "method": "ellipse fit of img1 outline, minor axis stretched; scale from the text-stated 12 m", "uncertainty": "+-0.4 m outline reading; size from text, not measured", "estimated": False},
    {"parameter": "reef base diameter", "value": 12.0, "unit": "m", "source_id": "S_RWR, S_ABC19, S_Tracks19", "method": "text, five sources agree", "uncertainty": "none stated", "estimated": False},
    {"parameter": "reef height above seabed (default / range)", "value": "2.0 (range 1.6-2.0)", "unit": "m", "source_id": "S_RWR, S_ABC19 (2 m) vs S_Tracks19 (1.6 m)", "method": "text; sources disagree, viewer slider covers both", "uncertainty": "0.4 m (the disagreement)", "estimated": False},
    {"parameter": "reef profile", "value": "spherical cap (symmetric) by default; optional ramp asymmetry", "unit": "-", "source_id": "S_Tracks21, S_Tradie", "method": "ESTIMATE. Sources say 'dome', 'flattened dome with a steeply angled back', 'skateboard ramp'; no cross-section or the direction of the steep side is published", "uncertainty": "flank shape unknown; +-0.3 m locally", "estimated": True},
    {"parameter": "crest depth at low tide", "value": 1.0, "unit": "m below water surface", "source_id": "S_RWR", "method": "text, design condition; 'low tide' level not defined (viewer assumes MLLW for the check)", "uncertainty": "about 'about 1m'; +-0.3 m plus the undefined 'low tide'", "estimated": False},
    {"parameter": "reef centre distance offshore (default)", "value": REEF_Y_DEFAULT, "unit": "m seaward of the 0 m AHD contour", "source_id": "S_shape; S_RWR 30-45, S_Tracks19 ~45 from low-tide mark, S_Surfer 50", "method": "text midpoint kept from shape.json; presets 30 / 37.5 / 45 / 49 / 50 m in the viewer. Measured from the 2009 0 m AHD contour (MSL waterline), the low-tide mark is about %.0f m further out" % (y_at_level(-0.2)[0] if y_at_level(-0.2) else 4), "uncertainty": "+-10 m (text range)", "estimated": True},
    {"parameter": "shoreline (y = 0)", "value": "fitted 0 m AHD contour, 2009 lidar", "unit": "-", "source_id": "S_lidar", "method": "zero crossings along 201 rows (|north| <= 500 m), straight-line fit; rms scatter %.1f m" % rms_contour, "uncertainty": "shoreline moves seasonally and over 10 years by tens of metres", "estimated": False},
    {"parameter": "seabed depth at the reef centre (y = 37.5)", "value": round(depth_at_y(37.5), 2), "unit": "m AHD", "source_id": "S_lidar", "method": "median of bilinear samples |x| <= 100 m, 10 m grid", "uncertainty": "BAG uncertainty layer 0.47-0.49 m here; survey is 10 years before the install; alongshore p10-p90 +-0.15 m", "estimated": False},
    {"parameter": "seabed slope y = 30..100 m", "value": round(abs(slope_seabed), 4), "unit": "m/m (about 1:%.0f)" % (1 / abs(slope_seabed)), "source_id": "S_lidar", "method": "linear fit to the alongshore median profile", "uncertainty": "smooth; no bar or trough within 200 m", "estimated": False},
    {"parameter": "seabed resolution", "value": 10, "unit": "m cell", "source_id": "S_lidar", "method": "the 12 m reef covers only 1-2 cells; the seabed under the footprint is a sloping plane, not resolved detail", "uncertainty": "natural rock/seagrass patches visible in the photos are not in the grid", "estimated": False},
    {"parameter": "seabed gap fill", "value": "%d of %d 5 m nodes" % (int(filled.sum()), filled.size), "unit": "-", "source_id": "S_lidar", "method": "no lidar return in the surf zone (y about -15..35): filled from the alongshore median profile (linear across the gap) + a smoothed per-column offset; shown hatched in the viewer", "uncertainty": "+-0.3 m in the filled strip", "estimated": True},
    {"parameter": "vertical datum of lidar", "value": "AHD", "unit": "-", "source_id": "S_lidar, S_DoTidx", "method": "DoT survey index says AHD; the BAG's own VERT_CS tag only says 'Instantaneous Water Level' (generic)", "uncertainty": "datum label not independently verified; the 0 m contour falling at the MSL waterline supports AHD", "estimated": False},
    {"parameter": "tidal planes (HAT/MHHW/MLHW/MSL/MHLW/MLLW/LAT)", "value": "+0.6 / +0.2 / +0.1 / +0.1 / 0.0 / -0.2 / -0.6", "unit": "m AHD", "source_id": "S_tide, S_DoTidx", "method": "table; LAT-AHD offset checked against the DoT index (0.57 m)", "uncertainty": "rounded to 0.1 m; Bunbury Port inner-harbour gauge, assumed valid at Back Beach", "estimated": False},
    {"parameter": "model z reference", "value": "z = AHD - 0.1", "unit": "m", "source_id": "S_tide", "method": "MSL = +0.1 m AHD", "uncertainty": "+-0.05 m", "estimated": False},
    {"parameter": "frame orientation", "value": "x = %.1f deg true, y (seaward) = %.1f deg true" % (bear_x_true, bear_y_true), "unit": "deg", "source_id": "S_lidar", "method": "direction of the fitted 0 m AHD contour; grid convergence %.2f deg (pyproj)" % conv, "uncertainty": "+-2 deg (contour scatter)", "estimated": False},
    {"parameter": "site location", "value": "%.4f, %.4f" % SITE_LL, "unit": "deg", "source_id": "S_sat", "method": "45 m seaward of the 2025 Esri waterline south of the Back Beach SLSC building; not traced (reef removed Dec 2019)", "uncertainty": "+-100 m; the seabed is alongshore-uniform there, so lateral error barely matters", "estimated": True},
]
confidence = {"level": "medium",
              "reason": "The seabed comes from a real airborne-lidar survey of this exact beach (smooth, uniform 1:24 slope; it also agrees with the depth implied by the 1 m crest depth plus 1.6-2 m height), and the tides are from a port table. But the survey is from 2009, its 10 m cells cannot resolve the 12 m reef, the offshore distance is a 30-50 m text range, and the crest depth, height and asymmetric flank shape are text or estimates."}
model = {
    "meta": {"slug": "bunbury-airwave", "name": "Bunbury Airwave (inflatable bladder, as installed Dec 2019)", "built": "2026-10-05", "units": "metres",
             "generator": "3d/build_3d.py"},
    "frame": {"description": "x alongshore (bearing %.1f deg true), y seaward from the fitted 0 m AHD contour (bearing %.1f deg true), z up, 0 = MSL = +0.1 m AHD. Same frame as shape.json canonical (x alongshore, y offshore)." % (bear_x_true, bear_y_true),
              "x_bearing_true": round(bear_x_true, 2), "y_bearing_true": round(bear_y_true, 2), "grid_convergence_deg": round(conv, 3),
              "north_xy": [round(north_xy[0], 4), round(north_xy[1], 4)],
              "origin_mga50": [round(OX, 1), round(OY, 1)], "origin_latlon": [round(v, 6) for v in tr_inv.transform(OX, OY)[::-1]],
              "site_point_latlon": list(SITE_LL), "site_point_offset_from_origin_m": [round(v, 1) for v in from_grid(XS, YS)],
              "msl_ahd": MSL_AHD},
    "seabed": {"x0": float(GX[0]), "y0": float(GY[0]), "dx": 5.0, "dy": 5.0, "nx": int(len(GX)), "ny": int(len(GY)),
               "z": [r2(row) for row in Z_msl], "filled": [row.tolist() for row in filled],
               "source_id": "S_lidar", "native_cell_m": 10, "vertical_uncertainty_m": 0.5,
               "survey_year": 2009, "note": "bilinear resample of the 10 m grid; hatched/lighter cells = gap-filled (no lidar return)",
               "contours": contours,
               "profile": {"y": [float(v) for v in yy_p[::2]], "median_ahd": r2(prof_med[::2]), "p10_ahd": r2(prof_p10[::2]), "p90_ahd": r2(prof_p90[::2])}},
    "shoreline": {"y": 0.0, "definition": "fitted 0 m AHD contour of the 2009 lidar (about the MSL waterline; MSL = +0.1 AHD)", "rms_scatter_m": round(rms_contour, 1)},
    "reef": {"toe_polygon_m": [[round(p[0], 3), round(p[1], 3)] for p in poly], "polygon_frame_note": "orientation of the traced polygon in x/y is arbitrary (circle); centred on its own ellipse centre",
             "centre_default": [0.0, REEF_Y_DEFAULT], "offshore_range_text_m": [30, 50],
             "offshore_presets": [{"label": "30 m (RWR near)", "y": 30.0}, {"label": "37.5 m (shape.json)", "y": 37.5}, {"label": "45 m (RWR far)", "y": 45.0},
                                   {"label": "49 m (Tracks: 45 m off low-tide mark)", "y": round(4.1 + 45, 1)}, {"label": "50 m (SurferToday)", "y": 50.0}],
             "diameter_m": 12.0, "height_default_m": 2.0, "height_range_m": [1.6, 2.0],
             "crest_depth_text_m": 1.0, "crest_depth_text_at": "low tide (MLLW assumed for the on-screen check)",
             "profile": {"type": "spherical_cap", "asym_default": 0.0, "asym_max": 0.6, "steep_side_default_bearing_true": 0,
                         "note": "estimate: cap with base radius 6 m and height H; ramp asymmetry moves the apex towards the chosen side (steeper there), direction not published"}},
    "water_levels": water_levels,
    "water_default": "MSL",
    "north_arrow": {"north_xy": [round(north_xy[0], 4), round(north_xy[1], 4)], "source": "grid convergence of MGA94 zone 50 at the site + fitted shoreline direction"},
    "sources": sources,
    "provenance": prov,
    "confidence_3d": confidence,
    "inputs_status": {"plan": "sourced - shape.json 29-vertex circle, 12 m from text", "crest": "sourced - text, RWR 1 m under the surface at low tide (datum of 'low tide' undefined)",
                      "height_slopes": "estimated - 1.6 or 2.0 m from text, profile shape assumed", "seabed": "sourced - WA DoT airborne lidar 2009, 10 m grid", "tides": "sourced - port tidal-plane table"},
}
with open(os.path.join(HERE, "data", "lidar_stage_model.js"), "w", encoding="utf8") as fh:
    fh.write("// bunbury-airwave 3D model data (stage 1, pre-Step-6), generated by build_3d_lidar.py. Frame/units: see REEF_MODEL.frame.\nwindow.REEF_MODEL = ")
    json.dump(model, fh, separators=(",", ":"))
    fh.write(";\n")
print("data/lidar_stage_model.js written", os.path.getsize(os.path.join(HERE, "data", "lidar_stage_model.js")), "bytes")

# ================================================================== annotated figures
# ---- helpers for the satellite overlay (Web-Mercator linear mapping, as satellite.py does)
geo = json.load(open(os.path.join(SHAPE_DIR, "src", "sat_backbeach_current.png.geo.json")))
sat = Image.open(os.path.join(SHAPE_DIR, "src", "sat_backbeach_current.png")).convert("RGB")
t3857 = Transformer.from_crs(4326, 3857, always_xy=True)
wx0, wy0 = t3857.transform(geo["bounds"]["west"], geo["bounds"]["north"])
wx1, wy1 = t3857.transform(geo["bounds"]["east"], geo["bounds"]["south"])
def grid_to_px(gx, gy):
    lon, lat = tr_inv.transform(gx, gy)
    X, Y = t3857.transform(lon, lat)
    return (X - wx0) / (wx1 - wx0) * geo["width"], (Y - wy0) / (wy1 - wy0) * geo["height"]
def model_to_px(x, y):
    return grid_to_px(*to_grid(np.asarray(x), np.asarray(y)))

# ---- Figure 1: lidar contours (native 10 m grid, unfilled) over the Esri image
cx, cy = model_to_px(0, 40)
half = 260.0 / geo["m_per_px_center"] * 1.0
fig, ax = plt.subplots(figsize=(11, 9.2), dpi=110)
ax.imshow(sat)
# native cells window for contouring
rr0 = int((OY - Y0G) / CELL); cc0 = int((OX - X0G) / CELL)
Wn = 60
Esub = E[rr0 - Wn:rr0 + Wn + 1, cc0 - Wn:cc0 + Wn + 1]
Xn = (np.arange(cc0 - Wn, cc0 + Wn + 1)) * CELL + X0G
Yn = (np.arange(rr0 - Wn, rr0 + Wn + 1)) * CELL + Y0G
Xm, Ym = np.meshgrid(Xn, Yn)
Epx, Epy = grid_to_px(Xm, Ym)
cmap = plt.get_cmap("viridis_r")
for lv in [-1, -2, -3, -4, -5, -6, -7]:
    cs = plt.figure().add_subplot().contour(Xm, Ym, np.ma.masked_invalid(Esub), levels=[lv])
    plt.close("all")
    best = None
    for seg in cs.allsegs[0]:
        px, py = grid_to_px(seg[:, 0], seg[:, 1])
        ax.plot(px, py, color=cmap((-lv - 1) / 6.0), lw=1.6)
        inside = (np.abs(px - cx) < half * 0.9) & (np.abs(py - cy) < half * 0.9)
        if inside.sum() > 0 and (best is None or inside.sum() > best[0]):
            k_ = np.where(inside)[0]; k_ = k_[np.argmin(np.abs(py[k_] - (cy - 0.35 * half)))]
            best = (inside.sum(), px[k_], py[k_])
    if best:
        ax.text(best[1], best[2], "%d m" % lv, color="white", fontsize=9, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.15", fc=cmap((-lv - 1) / 6.0), ec="none", alpha=0.95))
cs0 = plt.figure().add_subplot().contour(Xm, Ym, np.ma.masked_invalid(Esub), levels=[0])
plt.close("all")
for seg in cs0.allsegs[0]:
    px, py = grid_to_px(seg[:, 0], seg[:, 1]); ax.plot(px, py, color="red", lw=1.2, alpha=0.7)
# fitted shoreline and frame axes
lx = np.array([-250, 250.0]); lpx, lpy = model_to_px(lx, np.zeros(2))
ax.plot(lpx, lpy, color="red", lw=2.2, ls="--", label="fitted 0 m AHD contour = model y = 0 (shoreline)")
o_px, o_py = model_to_px(0, 0)
ax_px, ax_py = model_to_px(30, 0); ay_px, ay_py = model_to_px(0, 30)
ax.annotate("", xy=(ax_px, ax_py), xytext=(o_px, o_py), arrowprops=dict(arrowstyle="->", color="yellow", lw=2))
ax.annotate("", xy=(ay_px, ay_py), xytext=(o_px, o_py), arrowprops=dict(arrowstyle="->", color="yellow", lw=2))
ax.text(ax_px, ax_py - 8, "+x alongshore (%.0f deg true)" % bear_x_true, color="yellow", fontsize=9)
ax.text(ay_px - 10, ay_py + 22, "+y seaward (%.0f deg true)" % bear_y_true, color="yellow", fontsize=9, ha="right")
# 30-50 m band + reef circle at 37.5
band = [model_to_px(-60, 30), model_to_px(60, 30), model_to_px(60, 50), model_to_px(-60, 50)]
ax.add_patch(MplPolygon(np.array(band), closed=True, fc="orange", ec="orange", alpha=0.25, label="text range for the reef centre, 30-50 m offshore"))
th = np.linspace(0, 2 * np.pi, 120)
cxm, cym = model_to_px(6 * np.cos(th), REEF_Y_DEFAULT + 6 * np.sin(th))
ax.plot(cxm, cym, color="magenta", lw=2.2, label="reef, 12 m circle, centre y = 37.5 m (model default)")
# profile strip
strip = [model_to_px(-100, -10), model_to_px(100, -10), model_to_px(100, 200), model_to_px(-100, 200)]
ax.add_patch(MplPolygon(np.array(strip), closed=True, fc="none", ec="cyan", lw=1.2, ls=":", label="strip used for the depth profile (|x| <= 100 m, y -10..200 m)"))
# site point and SLSC
sx, sy = grid_to_px(XS, YS); ax.plot(sx, sy, "x", color="white", ms=9, mew=2)
ax.text(sx - 12, sy - 14, "site point -33.3276, 115.6284 (text-derived, +-100 m)", color="white", fontsize=8, ha="right", va="bottom")
lonl, latl = 115.6298, -33.3271
X_, Y_ = t3857.transform(lonl, latl); px_, py_ = (X_ - wx0) / (wx1 - wx0) * geo["width"], (Y_ - wy0) / (wy1 - wy0) * geo["height"]
ax.plot(px_, py_, "s", color="white", ms=7); ax.text(px_ + 8, py_ - 6, "Back Beach SLSC (Esri image)", color="white", fontsize=8)
# scale bar 50 m and north arrow
mpp = geo["m_per_px_center"]
bx, by = cx - half + 30, cy + half - 30
ax.plot([bx, bx + 50 / mpp], [by, by], color="white", lw=5); ax.plot([bx, bx + 50 / mpp], [by, by], color="black", lw=1.5)
ax.text(bx, by - 12, "50 m bar (image scale %.3f m/px)" % mpp, color="white", ha="left", fontsize=9)
nx_, ny_ = bx + 20, by - 80
dnx, dny = model_to_px(north_xy[0] * 40, north_xy[1] * 40); onx, ony = model_to_px(0, 0)
vx, vy = (dnx - onx), (dny - ony); L = math.hypot(vx, vy); vx, vy = vx / L * 45, vy / L * 45
ax.annotate("", xy=(nx_ + vx, ny_ + vy), xytext=(nx_, ny_), arrowprops=dict(arrowstyle="-|>", color="white", lw=2.5))
ax.text(nx_ + vx * 1.25, ny_ + vy * 1.25, "N (true)", color="white", fontsize=10, ha="center", va="center", fontweight="bold")
ax.set_xlim(cx - half, cx + half); ax.set_ylim(cy + half, cy - half); ax.set_axis_off()
ax.legend(loc="upper right", fontsize=8, framealpha=0.85)
ax.set_title("bunbury-airwave: WA DoT 2009 lidar depth contours (m AHD, native 10 m grid, no gap fill) over Esri World Imagery 2025-08-30\n"
             "contours read from BU2009TRBS_Lidar.bag; the reef is NOT in this image (removed Dec 2019); circle = model default position", fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "annotated", "lidar_contours_on_satellite.png")); plt.close(fig)

# ---- Figure 2: native cells around the reef with values
fig, ax = plt.subplots(figsize=(10, 6.6), dpi=110)
rng = 90
sub_x = np.arange(-rng, rng + 0.1, 10.0)
# native cell centres inside the window, in model frame
cells = []
for r in range(rr0 - 20, rr0 + 21):
    for c in range(cc0 - 20, cc0 + 21):
        x_, y_ = from_grid(X0G + c * CELL, Y0G + r * CELL)
        if -rng <= x_ <= rng and -20 <= y_ <= 80:
            cells.append((x_, y_, E[r, c], U[r, c]))
cells = np.array(cells)
okc = np.isfinite(cells[:, 2])
sc = ax.scatter(cells[okc, 0], cells[okc, 1], c=cells[okc, 2], cmap="viridis", vmin=-6, vmax=1.5, s=330, marker="s", edgecolors="none")
ax.scatter(cells[~okc, 0], cells[~okc, 1], s=330, marker="s", facecolors="none", edgecolors="red", hatch="///", linewidths=0.6)
for x_, y_, v, u in cells[okc]:
    if abs(x_) <= 60:
        ax.text(x_, y_, "%.1f" % v, ha="center", va="center", fontsize=6.5, color="white" if v < -2 else "black")
cb = fig.colorbar(sc, ax=ax, shrink=0.8); cb.set_label("lidar elevation, m AHD (native 10 m cells, rotated into the model frame)")
ax.add_patch(Circle((0, REEF_Y_DEFAULT), 6.0, fc="none", ec="magenta", lw=2.2, label="reef 12 m (default y = 37.5)"))
ax.add_patch(Rectangle((-90, 30), 180, 20, fc="orange", alpha=0.18, label="30-50 m text range"))
ax.axhline(0, color="red", ls="--", lw=1.5, label="y = 0: fitted 0 m AHD contour")
ax.set_xlim(-rng, rng); ax.set_ylim(-20, 80); ax.set_aspect("equal")
ax.set_xlabel("x alongshore (m, %.0f deg true)" % bear_x_true); ax.set_ylabel("y seaward of the 0 m AHD contour (m)")
ax.set_title("Lidar cells read around the reef site: each square is one 10 m cell, number = elevation m AHD (red hatch = no return)\n"
             "the 12 m reef spans only 1-2 cells; seabed under it = sloping plane, about -2.1 (y=30) to -3.2 (y=50) m AHD", fontsize=9)
ax.legend(loc="upper left", fontsize=8, framealpha=0.9)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "annotated", "lidar_cells_at_reef.png")); plt.close(fig)

# ---- Figure 3: depth profile
fig, ax = plt.subplots(figsize=(11, 5.6), dpi=110)
okp = nvalid >= 10
ax.fill_between(yy_p[okp], prof_p10[okp], prof_p90[okp], color="tab:blue", alpha=0.25, label="10th-90th percentile across |x| <= 100 m")
ax.plot(yy_p[okp], prof_med[okp], color="tab:blue", lw=2.2, label="median seabed, 2009 lidar (m AHD)")
colors = {"HAT": "tab:red", "MSL": "tab:green", "MLLW": "tab:orange", "LAT": "tab:purple"}
for k_, c_ in colors.items():
    ax.axhline(TIDES_AHD[k_], color=c_, lw=1.2, ls="--")
    ax.text({"HAT": 198, "MSL": 160, "MLLW": 125, "LAT": 198}[k_], TIDES_AHD[k_] + (0.08 if k_ != "LAT" else -0.35), "%s %+.1f m AHD" % (k_, TIDES_AHD[k_]), color=c_, ha="right", fontsize=8)
ax.axvspan(30, 50, color="orange", alpha=0.18, label="reef centre, text range 30-50 m")
ax.axvline(REEF_Y_DEFAULT, color="magenta", lw=1.6, label="model default centre 37.5 m")
d375 = depth_at_y(37.5)
ax.plot([37.5], [d375], "o", color="magenta")
ax.annotate(("seabed %.2f m AHD at y = 37.5" + chr(10) + "= %.2f m below MLLW, %.2f m below LAT") % (d375, TIDES_AHD["MLLW"] - d375, TIDES_AHD["LAT"] - d375), xy=(37.5, d375), xytext=(58, d375 + 1.9),
            arrowprops=dict(arrowstyle="->"), fontsize=8)
# text-derived seabed: low tide (MLLW) - 1.0 m crest - H
for H, ls_ in ((2.0, "-"), (1.6, ":")):
    zt = TIDES_AHD["MLLW"] - 1.0 - H
    ax.axhline(zt, color="black", lw=1.0, ls=ls_)
    ax.text(2, zt - 0.28, "text-implied seabed: MLLW %.1f - crest 1.0 - height %.1f = %.1f m AHD" % (TIDES_AHD["MLLW"], H, zt), fontsize=7.5)
# shaded reef silhouette at 37.5 with H=2
yy_r = np.linspace(31.5, 43.5, 60); dome = np.sqrt(100 - (yy_r - 37.5) ** 2) - 8
base = np.interp(yy_r, yy_p[okp], prof_med[okp])
ax.fill_between(yy_r, base, base + dome, color="magenta", alpha=0.7, label="reef cross-section (H = 2.0 m cap) at 37.5 m")
ax.set_xlim(-30, 200); ax.set_ylim(-9.2, 3.0)
ax.set_xlabel("y: metres seaward of the fitted 0 m AHD contour (2009)"); ax.set_ylabel("elevation, m AHD")
ax.grid(alpha=0.3); ax.legend(loc="lower left", fontsize=8)
ax.set_title("bunbury-airwave: cross-shore seabed profile from the WA DoT 2009 airborne lidar, vertical scale exaggerated about 8x", fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "annotated", "seabed_profile_with_tides.png")); plt.close(fig)

# ---- Figure 4: img1 with the trace, fitted ellipse axes and the text-derived 12 m scale
img1 = Image.open(os.path.join(SHAPE_DIR, "src", "img1_airwave-from-above.jpg")).convert("RGB")
d = ImageDraw.Draw(img1, "RGBA")
src1 = [s for s in shape["sources"] if s["id"] == "img1"][0]
pp = src1["pixel_polygons"]
if isinstance(pp, str): pp = json.loads(pp)
pol = [tuple(p) for p in pp[0]]
d.polygon(pol, fill=(255, 140, 0, 50)); d.line(pol + [pol[0]], fill=(255, 140, 0, 255), width=2)
cxy = (446.4, 334.9); a_, b_ = 153.55, 137.39; ang = math.radians(-156.0)
ux, uy = math.cos(ang), math.sin(ang); vx_, vy_ = -uy, ux
def pt(s, t): return (cxy[0] + s * ux + t * vx_, cxy[1] + s * uy + t * vy_)
d.line([pt(-a_, 0), pt(a_, 0)], fill=(255, 0, 255, 255), width=3)
d.line([pt(0, -b_), pt(0, b_)], fill=(0, 255, 255, 255), width=2)
for s_end in (-a_, a_):
    d.line([pt(s_end, -8), pt(s_end, 8)], fill=(255, 0, 255, 255), width=3)
d.text((10, 8), "img1 (RWR drone photo, 16 Dec 2019). Orange = traced outline (29 vertices). Magenta = fitted major axis 307.1 px = 12.0 m (SCALE FROM TEXT, 25.59 px/m).", fill=(255, 255, 255, 255))
d.text((10, 22), "Cyan = minor axis 274.8 px (foreshortened by the camera tilt, 137.4/153.6 = 0.895 -> ~26 deg off nadir). Stretching it by 1.118 gives the circle used in shape.json.", fill=(255, 255, 255, 255))
d.text((10, 36), "Photo has no scale bar and no geo-reference; reuse rights not cleared (private research copy).", fill=(255, 255, 255, 255))
img1.save(os.path.join(HERE, "annotated", "img1_trace_axes_scale.png"))
print("annotated figures written")

summary = {
    "fit": {"icpt_a_m": icpt_a, "slope_b": slope_b, "rms_contour_m": rms_contour, "site_dist_to_line_m": dist_site_to_line},
    "bearings": {"x_true": bear_x_true, "y_true": bear_y_true, "conv": conv},
    "depths_ahd": {str(y): depth_at_y(y) for y in (20, 30, 37.5, 40, 45, 49, 50, 60, 100, 150, 200)},
    "y_of_level": {str(l): y_at_level(l) for l in (0.0, -0.2, -0.6, -1.0, -2.0, -2.5, -2.8, -3.0, -3.2, -3.3)},
    "seabed_slope": slope_seabed, "filled_nodes": int(filled.sum()), "total_nodes": int(filled.size),
    "uncertainty_layer_at_reef": [float(sample(np.array([0.0]), np.array([y]), arr=U, order=0)[0]) for y in (30, 37.5, 45, 50)],
}
json.dump(summary, open(os.path.join(HERE, "data", "build_summary.json"), "w"), indent=1)
print(json.dumps(summary, indent=1))

# what stage 2 (build_3d.py) reads, so that the .bag need not be fetched again (same content as the lidar_derived.json extracted by hand on 2026-10-05)
json.dump({"_about": "Stage-1 results needed by build_3d.py; written by build_3d_lidar.py",
           "frame": model["frame"], "shoreline": model["shoreline"],
           "seabed_meta": {k: model["seabed"][k] for k in ("x0", "y0", "dx", "dy", "nx", "ny", "source_id", "native_cell_m", "vertical_uncertainty_m", "survey_year", "note")},
           "profile": model["seabed"]["profile"], "summary": summary,
           "grid_csv": "data/lidar_clip_model_frame.csv (5 m resample, all nodes, filled flag; z_msl_m = ahd_m - 0.10)"},
          open(os.path.join(HERE, "data", "lidar_derived.json"), "w"), indent=1)
