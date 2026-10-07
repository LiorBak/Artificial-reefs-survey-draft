"""nav_annotate.py - bunbury-airwave: reads the Garmin Navionics (Marine Maps web viewer) screenshots in src/navionics/ and tests the lidar seabed with them.

Inputs : src/navionics/sonar_m_z18_dpr2.png (SonarChart layer, metres, zoom 18, 1970 x 1702 px = 0.2497 m/px),
         src/navionics/nautical_m_z17_dpr1.png and nautical_m_z18_dpr2.png (Nautical Charts layer, metres),
         data/lidar_clip_model_frame.csv + data/lidar_derived.json (the WA DoT 2009 lidar resampled into the model frame, stage 1).
Outputs: data/nav_transects.json  (read by build_3d.py)   annotated/N1..N4 (png)
Run    : python nav_annotate.py        (build_3d.py calls compute(); python build_3d.py --annotations also redraws the figures)

METHOD (METHODS_3D.md section 3.6)
  * the screenshot is the Leaflet map container, north up, Web-Mercator, centred on SITE; metres per image pixel
        res = 156543.03392 * cos(lat) / 2**zoom / dpr            (0.2497 m/px at zoom 18, dpr 2, lat -33.3276)
  * a model-frame point (x alongshore, y seaward) maps to the image by the true bearings of the model axes (x 12.318, y 282.318 deg):
        east = x sin(bx) + (y - y_site) sin(by),  north = x cos(bx) + (y - y_site) cos(by),   px = cx + east/res,  py = cy - north/res
  * transects run along +y (shore-normal) from the site point at alongshore offsets a = -120 ... +120 m. Along each, the image is sampled every
    0.25 m. Band boundaries (green drying -> dark blue -> light blue -> white) and thin dark contour lines are located; runs closer than 2.5 m
    are merged (digits of depth labels). Index n = 0 is the green/blue boundary (the 0 m contour), n = 1 the dark/light blue boundary, n = 2 the
    light blue/white boundary = the 1 m shallow-shading limit (app setting 'Shallow shading 1 m'), n >= 3 the thin lines. Contour interval
    0.5 m (inferred and checked against the printed labels 1, 1.5, 2, 3, 3.5 ... 8.5): depth d_n = 0.5 n m below the (unstated) chart datum.
  * for each crossing the lidar elevation z_AHD is read from the 5 m grid; the datum D (m relative to AHD) implied by that line is
        D_n = z_AHD,n + d_n          (a depth d below datum D means z_AHD = D - d)
    and for each candidate datum D_c the RMS of (z_AHD,n - (D_c - d_n)) is computed (lines with valid lidar only: y >= 30 m, not gap-filled).
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates

HERE = os.path.dirname(os.path.abspath(__file__))
NAV = os.path.join(HERE, "src", "navionics")
DATA = os.path.join(HERE, "data")
ANN = os.path.join(HERE, "annotated")

SITE = (-33.3276, 115.6284)
LAT0 = SITE[0]
RES18 = 156543.03392 * math.cos(math.radians(LAT0)) / 2 ** 18          # m per CSS px at zoom 18 (0.4994)
MSL_AHD = 0.10
# candidate chart datums, metres relative to AHD (GHD 2021 Table 1, source S_tide; LAT also from the DoT survey index S_DoTidx)
CANDIDATES = {"LAT": -0.60, "LAT (DoT index)": -0.57, "MLLW": -0.20, "MHLW": 0.0, "AHD": 0.0, "MSL": 0.10}
INTERVAL = 0.5

# nautical-chart soundings read by eye on nautical_m_z18_dpr2.png (image px of the centre of the digits) and values as printed
# (Navionics prints decimals as a subscript: 3_5 = 3.5 m; an underlined figure is a drying height above chart datum)
NAUT_Z18 = [("3.5", 927, 400, 3.5, "sounding"), ("3.5", 655, 1650, 3.5, "sounding"), ("8.2", 255, 790, 8.2, "sounding"),
            ("0.6 (drying)", 1260, 200, 0.6, "drying"), ("0.9 (underlined; sits in the blue band, so drying or depth is unclear)", 1003, 983, 0.9, "drying"), ("0.4 (drying)", 946, 1650, 0.4, "drying")]


def load_summary():
    d = json.load(open(os.path.join(DATA, "lidar_derived.json"), encoding="utf-8"))
    sm = d["summary"]
    return d, sm["bearings"]["x_true"], sm["bearings"]["y_true"], d["frame"]["site_point_offset_from_origin_m"][1]


def load_grid():
    rows = [ln.strip().split(",") for ln in open(os.path.join(DATA, "lidar_clip_model_frame.csv"), encoding="utf-8") if ln[0] != "#"][1:]
    a = np.array([[float(v) for v in r] for r in rows])
    xs, ys = np.unique(a[:, 0]), np.unique(a[:, 1])
    Z = np.full((len(ys), len(xs)), np.nan)
    F = np.zeros_like(Z)
    ix = np.searchsorted(xs, a[:, 0]); iy = np.searchsorted(ys, a[:, 1])
    Z[iy, ix] = a[:, 2]
    F[iy, ix] = a[:, 4]
    return xs, ys, Z, F


class Lidar:
    def __init__(self):
        self.xs, self.ys, self.Z, self.F = load_grid()

    def at(self, x, y):
        """bilinear lidar elevation (m AHD) and 'valid' (no gap-filled node among the 4 neighbours)"""
        fx = (np.asarray(x, float) - self.xs[0]) / (self.xs[1] - self.xs[0])
        fy = (np.asarray(y, float) - self.ys[0]) / (self.ys[1] - self.ys[0])
        z = map_coordinates(self.Z, [fy, fx], order=1, mode="nearest")
        f = map_coordinates(self.F, [fy, fx], order=1, mode="nearest")
        inside = (fx >= 0) & (fx <= len(self.xs) - 1) & (fy >= 0) & (fy <= len(self.ys) - 1)      # outside the 300 x 240 m grid the value is NOT lidar
        return z, (f < 1e-6) & inside


def px_of(x, y, y_site, bx, by, res, cx, cy):
    e = x * math.sin(math.radians(bx)) + (y - y_site) * math.sin(math.radians(by))
    n = x * math.cos(math.radians(bx)) + (y - y_site) * math.cos(math.radians(by))
    return cx + e / res, cy - n / res


def classify(p):
    r, g, b = int(p[0]), int(p[1]), int(p[2])
    if abs(r - 152) < 16 and abs(g - 200) < 16 and b < 50:
        return "G"                                    # green: drying area
    if r < 90 and g > 130 and b > 200:
        return "B"                                    # dark blue shallow shading
    if 120 < r < 200 and g > 190 and b > 225:
        return "b"                                    # light blue shallow shading
    if r > 235 and g > 235 and b > 235:
        return "."
    if r > 225 and g > 215 and b < 170:
        return "Y"                                    # land
    return "?"


def transect(img, a, y_site, bx, by, res, s0=-60.0, s1=210.0, step=0.25):
    """sample image along +y at alongshore offset a; returns dict with band boundaries and thin-line crossings (s in m from the site, +seaward)"""
    H, W = img.shape[:2]
    cx, cy = W / 2.0, H / 2.0
    ss = np.arange(s0, s1 + step / 2, step)
    pts = [px_of(a, y_site + s, y_site, bx, by, res, cx, cy) for s in ss]
    cl, lum = [], []
    for (px, py) in pts:
        xi, yi = int(round(px)), int(round(py))
        if 0 <= xi < W and 0 <= yi < H:
            p = img[yi, xi]
            cl.append(classify(p)); lum.append(float(p[:3].mean()))
        else:
            cl.append("X"); lum.append(255.0)
    cl = np.array(cl); lum = np.array(lum)
    # last green sample = seaward end of the drying band; last dark-blue; last light-blue
    def last(c):
        k = np.where(cl == c)[0]
        return None if len(k) == 0 else float(ss[k.max()] + step / 2)
    g_end, B_end, b_end = last("G"), last("B"), last("b")
    # thin lines: seaward of the light-blue/white boundary
    start = b_end if b_end is not None else (B_end if B_end is not None else g_end)
    thin = []
    if start is not None:
        in_run = False
        runs = []
        for i, s in enumerate(ss):
            ok = (s > start + 2.5) and cl[i] != "X" and lum[i] < 215 and cl[i] in ".?"      # darker than the white background (248)
            if ok and not in_run:
                st = s; in_run = True
            if (not ok) and in_run:
                runs.append((st, ss[i - 1])); in_run = False
        merged = []
        for r in runs:
            if merged and r[0] - merged[-1][1] < 2.5:
                merged[-1] = (merged[-1][0], r[1])
            else:
                merged.append(r)
        thin = [round(float((r[0] + r[1]) / 2), 2) for r in merged]
    bounds = [v for v in (g_end, B_end, b_end) if v is not None]
    return {"a": a, "s_green_end": g_end, "s_dark_end": B_end, "s_light_end": b_end, "s_thin": thin, "crossings_s": [round(v, 2) for v in bounds] + thin}


def compute(verbose=False):
    d, bx, by, y_site = load_summary()
    L = Lidar()
    img = np.array(Image.open(os.path.join(NAV, "sonar_m_z18_dpr2.png")).convert("RGB"))
    res = RES18 / 2.0
    offsets = [-120, -90, -60, -30, 0, 30, 60, 90, 120]
    out = {"method": "see nav_annotate.py docstring", "res_m_per_px": res, "interval_m": INTERVAL, "site": SITE, "y_site_m": y_site, "bearings_true": [bx, by], "transects": []}
    for a in offsets:
        t = transect(img, a, y_site, bx, by, res)
        cs = t["crossings_s"]
        t["depth_m"] = [INTERVAL * n for n in range(len(cs))]
        ys = np.array([y_site + s for s in cs]); xs = np.full_like(ys, a, dtype=float)
        z, valid = L.at(xs, ys)
        t["y_model_m"] = [round(float(v), 2) for v in ys]
        t["lidar_ahd"] = [round(float(v), 3) for v in z]
        t["lidar_valid"] = [bool(v) and bool(y >= 30.0) for v, y in zip(valid, ys)]
        t["implied_datum_ahd"] = [round(float(zi + dn), 3) for zi, dn in zip(z, t["depth_m"])]
        out["transects"].append(t)
        if verbose:
            print(a, len(cs), "g_end %.1f" % t["s_green_end"], cs[:6])
    # datum test: main transect (a = 0) and all transects, valid lidar lines only
    def test(ts):
        res_ = {}
        allD = []
        for t in ts:
            for D, v, dn, zi in zip(t["implied_datum_ahd"], t["lidar_valid"], t["depth_m"], t["lidar_ahd"]):
                if v:
                    allD.append((D, dn, zi))
        arr = np.array(allD)
        for k, Dc in CANDIDATES.items():
            r = arr[:, 2] - (Dc - arr[:, 1])            # lidar z - (Dc - d)
            res_[k] = {"datum_ahd": Dc, "rms_m": round(float(np.sqrt(np.mean(r ** 2))), 3), "bias_lidar_minus_nav_m": round(float(np.mean(r)), 3), "n": int(len(r))}
        res_["_implied_free_datum_ahd"] = {"mean": round(float(arr[:, 0].mean()), 3), "sd": round(float(arr[:, 0].std(ddof=1)), 3), "n": int(len(arr)),
                                          "sem": round(float(arr[:, 0].std(ddof=1) / math.sqrt(len(arr))), 3)}
        return res_
    out["datum_test_main"] = test([t for t in out["transects"] if t["a"] == 0])
    out["datum_test_all"] = test(out["transects"])
    # per-line summary (mean over transects) for the plot
    nmax = min(len(t["crossings_s"]) for t in out["transects"])
    out["n_lines_common"] = nmax
    # near-shore line (n = 0, 0 m contour): where is it relative to the lidar?
    g = [t["s_green_end"] for t in out["transects"]]
    out["zero_line_s_m"] = {"mean": round(float(np.mean(g)), 2), "sd": round(float(np.std(g, ddof=1)), 2)}
    z0 = [t["lidar_ahd"][0] for t in out["transects"]]
    out["zero_line_lidar_ahd"] = {"mean": round(float(np.mean(z0)), 3), "sd": round(float(np.std(z0, ddof=1)), 3), "note": "lidar elevation at the 0 m Navionics contour (surf-zone strip: lidar partly gap-filled, indicative only)"}
    # alongshore smoothness of the 3 m contour etc: spread of s for line n across transects (a measure of how straight the contours are)
    spread = {}
    for n in (4, 6, 8, 10, 12):
        v = [t["crossings_s"][n] for t in out["transects"] if len(t["crossings_s"]) > n]
        if len(v) > 3:
            spread[str(INTERVAL * n)] = {"mean_s": round(float(np.mean(v)), 1), "sd_m": round(float(np.std(v, ddof=1)), 1), "n": len(v)}
    out["contour_spread_across_transects"] = spread
    # nautical-chart spot soundings (z18 dpr2): implied datum from the lidar
    nt = []
    for lab, px, py, val, kind in NAUT_Z18:
        e = (px - 985.0) * res
        n_ = -(py - 851.0) * res
        bxr, byr = math.radians(bx), math.radians(by)
        xm = e * math.sin(bxr) + n_ * math.cos(bxr)               # component along +x (alongshore)
        ym = e * math.sin(byr) + n_ * math.cos(byr) + y_site      # component along +y (seaward) + site offset
        z, valid = L.at(np.array([xm]), np.array([ym]))
        z = float(z[0])
        D = z + val if kind == "sounding" else z - val            # drying height h above datum: z = D + h
        nt.append({"label": lab, "kind": kind, "value_m": val, "px": [px, py], "x_m": round(xm, 1), "y_m": round(ym, 1), "lidar_ahd": round(z, 3),
                   "lidar_valid": bool(valid[0]) and bool(ym >= 30.0), "implied_datum_ahd": round(D, 3)})
    out["nautical_soundings"] = nt
    sdg = [r["implied_datum_ahd"] for r in nt if r["kind"] == "sounding" and r["lidar_valid"]]
    out["nautical_sounding_datum"] = {"mean": round(float(np.mean(sdg)), 3), "n": len(sdg), "values": sdg,
                                      "note": "only soundings inside the 300 x 240 m lidar grid and y >= 30 m count; spot soundings outside it (x = -212 m, y = 219 m) and drying heights are listed but not used"}
    # nautical-chart contours 2 / 5 m along the main transect (z17 dpr1)
    try:
        im17 = np.array(Image.open(os.path.join(NAV, "nautical_m_z17_dpr1.png")).convert("RGB"))
        res17 = RES18 * 2.0
        t17 = transect(im17, 0, y_site, bx, by, res17, s0=-60, s1=330)
        out["nautical_z17_main"] = {"s_green_end": t17["s_green_end"], "s_dark_end": t17["s_dark_end"], "s_thin": t17["s_thin"], "crossings_s": t17["crossings_s"]}
        # Nautical Charts layer: contours 0, 2, 5, 10 m (no 0.5 m interval): 0 = green end, 2 = blue/white edge, then thin lines 5 and 10
        ncs = [(0.0, t17["s_green_end"]), (2.0, t17["s_dark_end"])] + list(zip((5.0, 10.0), t17["s_thin"]))
        rows = []
        for dep, sv in ncs:
            z, valid = L.at(np.array([0.0]), np.array([y_site + sv]))
            rows.append({"depth_m": dep, "s_m": round(float(sv), 2), "y_m": round(float(y_site + sv), 2), "lidar_ahd": round(float(z[0]), 3), "lidar_valid": bool(valid[0]) and bool(y_site + sv >= 30.0),
                         "implied_datum_ahd": round(float(z[0] + dep), 3)})
        out["nautical_contours_main"] = rows
    except Exception as ex:                                              # pragma: no cover
        out["nautical_z17_main"] = {"error": str(ex)}
    with open(os.path.join(DATA, "nav_transects.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    return out


if __name__ == "__main__":
    o = compute(verbose=True)
    print(json.dumps({k: o[k] for k in ("datum_test_main", "datum_test_all", "zero_line_s_m", "zero_line_lidar_ahd", "contour_spread_across_transects", "nautical_sounding_datum", "nautical_z17_main")}, indent=1))
    for r in o["nautical_soundings"]:
        print(r)
