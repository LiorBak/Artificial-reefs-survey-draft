"""nav_annotate.py - reads the Navionics (Garmin Marine Maps) screenshots saved in src/navionics/, extracts the
SonarChart contour crossings along the shore-normal transect through the position hint (Borrero & Nelsen 2003 Fig. 9 window centre), compares them with the
NOAA DEM, writes src/navionics/nav_transect.json and the annotated images A9, A10, A11 in annotated/.

Run:  python nav_annotate.py        (called by build_3d.py --annotations; build_3d.py only reads nav_transect.json)
Method (see METHODS_3D.md section 3.5):
  * screenshot = Leaflet map container, north up, Web-Mercator, 256 px tiles; metres per pixel
        res = 156543.03392 * cos(lat) / 2**zoom      (0.4955 m/px at z18, 33.9206 N)
  * transect: from the screenshot centre (= hint, 33.92058 N 118.43335 W) along bearing 245 deg (shore-normal, +y of the model
    frame) in 0.25 px steps; dark pixels (max RGB < 110) are contour lines / text; runs closer than 0.8 m are merged.
  * index 0 = the first dark run within 3 m of the seaward end of the green (drying) band = the 0 ft contour; index n = n ft
    (1 ft interval, verified: the 0-6 ft contours bound the 6 ft shallow-shading band; the 15th contour coincides (3 m) with the
    nautical-layer spot sounding "15").
  * depth below chart datum d_ft = n; z_MSL = -(n * 0.3048) - delta, delta = MSL - chart datum (0.849 m if MLLW, assumed)
"""
import json
import math
import os
import sys

import matplotlib
import numpy as np
from PIL import Image, ImageDraw

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import reef3d_lib as L  # noqa: E402
import make_annotations as MA  # noqa: E402

NAV = os.path.join(L.SRC, "navionics")
sys.path.insert(0, NAV)
import transect_lib as T  # noqa: E402

OUT = os.path.join(L.HERE, "annotated")
LAT0, LON0, ZOOM = L.HINT_LAT, L.HINT_LON, 18
FT = 0.3048
BEARING_Y = 245.0
BEARING_X = 155.0
ALONG_OFFSETS = (-150, -100, -50, 0, 50, 100, 150)
SONAR = os.path.join(NAV, "sonar_ft_z18_map.png")
NAUT = os.path.join(NAV, "nautical_ft_z18_map.png")
NAUT_SOUNDING_PX = (340, 379)          # "15" (ft) read by eye on nautical_ft_z18_map.png (container pixels)
NAUT_SOUNDING_FT = 15.0


def tag(d, xy, text, fill, fnt, bg=(255, 255, 255, 225)):
    """text on a semi-opaque white box (keeps labels readable over contour lines)"""
    w = d.textlength(text, font=fnt)
    d.rectangle([xy[0] - 2, xy[1] - 1, xy[0] + w + 2, xy[1] + fnt.size + 3], fill=bg)
    d.text(xy, text, fill=fill, font=fnt)


def res_m_per_px(lat=LAT0, z=ZOOM):
    return 156543.03392 * math.cos(math.radians(lat)) / 2 ** z


def px_to_offsets(px, py, W, H, res):
    """container pixel -> (x alongshore, s offshore) metres relative to the hint (screen centre)"""
    e = (px - W / 2) * res
    n = -(py - H / 2) * res
    ax, ay = math.radians(BEARING_X), math.radians(BEARING_Y)
    return e * math.sin(ax) + n * math.cos(ax), e * math.sin(ay) + n * math.cos(ay)


def offsets_to_px(x, s, W, H, res):
    ax, ay = math.radians(BEARING_X), math.radians(BEARING_Y)
    e = x * math.sin(ax) + s * math.sin(ay)
    n = x * math.cos(ax) + s * math.cos(ay)
    return W / 2 + e / res, H / 2 - n / res


def dem_along(A, s_list, x_list=(-10, -5, 0, 5, 10), off=None):
    ds = L.load_datums("9410840")
    if off is None:
        off = ds["MSL"] - ds["NAVD88"]
    out = []
    for s in s_list:
        v = []
        for x in x_list:
            lon, lat = L.canon_to_lonlat(x, s, BEARING_X)
            v.append(L.sample(A, lon, lat) - off)
        out.append(float(np.mean(v)))
    return np.array(out)


_MASK = None
DARK_THR = 175      # anti-aliased 1 px contour lines on the light-blue shading are brighter than 110


def clean_mask():
    """dark pixels (max RGB < 110) belonging to LONG connected components only (contour lines, coastline): drops depth-label glyphs and the
    small magenta/black chart symbols that otherwise create false contour crossings (their components are shorter than 30 px)"""
    global _MASK
    if _MASK is None:
        from scipy import ndimage as ndi
        im = np.array(Image.open(SONAR).convert("RGB")).astype(int)
        dark = im.max(axis=2) < DARK_THR
        lab, nl = ndi.label(dark, structure=np.ones((3, 3)))
        keep = np.zeros_like(dark)
        for i, sl in enumerate(ndi.find_objects(lab)):
            if max(sl[0].stop - sl[0].start, sl[1].stop - sl[1].start) >= 30:
                keep |= lab == i + 1
        _MASK = keep
    return _MASK


def clean_profile(cx, cy, bearing=BEARING_Y, s0=-300, s1=600, res=None):
    """(green_end_m, contour crossing positions s (m, from the screenshot point (cx, cy) along `bearing`), index of the 0 ft line)"""
    res = res or res_m_per_px()
    m = clean_mask()
    H, W = m.shape
    b = math.radians(bearing)
    dx, dy = math.sin(b), -math.cos(b)
    run, runs = None, []
    for s in np.arange(s0, s1, 0.25):
        x, y = cx + dx * s / res, cy + dy * s / res
        xi, yi = int(round(x)), int(round(y))
        on = 0 <= xi < W and 0 <= yi < H and bool(m[max(yi - 0, 0):yi + 1, max(xi - 0, 0):xi + 1].any())
        if on:
            run = [s, s] if run is None else [run[0], s]
        elif run is not None:
            runs.append(run)
            run = None
    if run:
        runs.append(run)
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] < 0.8:
            merged[-1][1] = r[1]
        else:
            merged.append(r)
    pos = [0.5 * (r[0] + r[1]) for r in merged]
    pts = T.transect(SONAR, ZOOM, LAT0, bearing, cx, cy, s0 / res, s1 / res)[1]
    ge = T.green_end(pts)
    k0 = None
    if ge is not None:
        for i, q in enumerate(pos):
            if abs(q - ge) <= 3.0:
                k0 = i
                break
    return ge, pos, k0


SONAR_LABELS = [(1, (551, 257)), (4, (493, 237)), (5, (467, 222)), (12, (366, 169)), (13, (333, 188)), (15, (258, 196)), (16, (210, 179)),
                (17, (208, 221)), (19, (57, 118)), (22, (167, 380)), (23, (258, 556)), (24, (47, 321))]   # contour depth labels (ft) read by eye on sonar_ft_z18_map.png


def verify_labels(W, H, res):
    """check the contour counting against the printed depth labels: a shore-normal line through (but 7 px beside) each label crosses the contour of that label;
    its index counted from the 0 ft line must equal the label value"""
    ax = math.radians(BEARING_X)
    ux, uy = math.sin(ax), -math.cos(ax)                 # unit vector alongshore (+x) in screen (px) coordinates
    rows = []
    for val, (px, py) in SONAR_LABELS:
        best = None
        for side in (-1, 1):
            cx, cy = px + side * 7 * ux, py + side * 7 * uy
            ge, pos, k0 = clean_profile(cx, cy)
            if k0 is None:
                continue
            p = pos[k0:]
            # position of the label along this transect (s of the label point projected on the 245 deg line through (cx, cy))
            sl = ((px - cx) * math.sin(math.radians(BEARING_Y)) + (-(py - cy)) * math.cos(math.radians(BEARING_Y))) * res
            j = int(np.argmin([abs(q - sl) for q in p]))
            cand = (abs(p[j] - sl), j)
            if best is None or cand < best:
                best = cand
        rows.append({"label_ft": val, "px": [px, py], "counted_index": None if best is None else best[1], "distance_to_line_m": None if best is None else round(best[0], 1)})
    ok = sum(1 for r in rows if r["counted_index"] == r["label_ft"])
    return {"rows": rows, "n_match": ok, "n": len(rows)}


# ---- depth labels read by eye (feet) on the screenshots: container pixel positions (985 x 751 images)
OLD_DIR = os.path.join(NAV, "hint1_33.9188_-118.4324")
LABEL_SETS = [   # (image, centre lat, lon, [(value_ft, (px, py), kind)])
    (os.path.join(NAV, "sonar_ft_z18_map.png"), L.HINT_LAT, L.HINT_LON,
     [(1, (551, 257), "sonar"), (4, (493, 237), "sonar"), (5, (467, 222), "sonar"), (12, (366, 169), "sonar"), (13, (333, 188), "sonar"), (15, (258, 196), "sonar"),
      (16, (210, 179), "sonar"), (17, (208, 221), "sonar"), (19, (57, 118), "sonar"), (22, (167, 380), "sonar"), (23, (258, 556), "sonar"), (24, (47, 321), "sonar")]),
    (os.path.join(NAV, "nautical_ft_z18_map.png"), L.HINT_LAT, L.HINT_LON,
     [(15, (340, 379), "sounding"), (23, (212, 594), "sounding"), (19, (357, 594), "sounding"), (3, (611, 405), "sounding")]),
    (os.path.join(OLD_DIR, "sonar_ft_z18_map.png"), L.OLD_HINT_LAT, L.OLD_HINT_LON,
     [(23, (81, 157), "sonar"), (21, (316, 544), "sonar"), (20, (356, 646), "sonar"), (19, (390, 673), "sonar")]),
    (os.path.join(OLD_DIR, "nautical_ft_z18_map.png"), L.OLD_HINT_LAT, L.OLD_HINT_LON,
     [(15, (404, 355), "sounding"), (21, (272, 660), "sounding"), (23, (35, 195), "sounding"), (3, (433, 6), "sounding")]),
]


def label_datum_test():
    """compare every depth label / spot sounding (feet) with the NOAA DEM at the same ground point, for four candidate chart datums.
    No contour counting is involved: the label value is read directly."""
    lev, _ = L.datum_levels_msl("9410840")
    deltas = {"MLLW": -lev["MLLW"], "NAVD88": -lev["NAVD88"], "LAT": -lev["LAT"], "MSL": 0.0}     # delta = MSL - datum (m)
    A = L.load_dem()
    ds = L.load_datums("9410840")
    off = ds["MSL"] - ds["NAVD88"]
    res = res_m_per_px()
    pts = []
    for img, lat0, lon0, labs in LABEL_SETS:
        W, H = Image.open(img).size
        for val, (px, py), kind in labs:
            e, n = (px - W / 2) * res, -(py - H / 2) * res
            lon, lat = lon0 + e / L.m_lon(lat0), lat0 + n / L.M_LAT
            zd = L.sample(A, lon, lat) - off
            if np.isnan(zd):
                continue
            pts.append({"value_ft": val, "kind": kind, "image": os.path.basename(os.path.dirname(img)) if "hint1" in img else "new", "lat": round(lat, 5), "lon": round(lon, 5), "dem_z_msl": round(float(zd), 2)})
    out = {"n": len(pts), "points": pts, "datums": {}, "zones": {}, "reef_zone_ft": [8, 18]}
    for zone, sel in (("all", lambda p: True), ("reef_zone", lambda p: 8 <= p["value_ft"] <= 18), ("surf_zone_lt_8ft", lambda p: p["value_ft"] < 8), ("offshore_gt_18ft", lambda p: p["value_ft"] > 18)):
        sub = [p for p in pts if sel(p)]
        out["zones"][zone] = {"n": len(sub), "datums": {}}
        for k, dl in deltas.items():
            d = np.array([-(p["value_ft"] * FT) - dl - p["dem_z_msl"] for p in sub])
            out["zones"][zone]["datums"][k] = {"bias_nav_minus_dem_m": round(float(d.mean()), 3), "sd_m": round(float(d.std()), 3), "rms_m": round(float(np.sqrt((d ** 2).mean())), 3)}
    for k, dl in deltas.items():
        z = out["zones"]["reef_zone"]["datums"][k]
        out["datums"][k] = {"delta_msl_minus_datum_m": round(dl, 3), **z}
    return out


def compute():
    ds = L.load_datums("9410840")
    msl = ds["MSL"]
    lev, _ = L.datum_levels_msl("9410840")
    deltas = {"MLLW": -lev["MLLW"], "MSL": 0.0, "NAVD88": -lev["NAVD88"], "LAT": -lev["LAT"]}   # delta = MSL - datum (m)
    img = Image.open(SONAR)
    W, H = img.size
    res = res_m_per_px()
    # ---- hint transect
    ge, pos, k0 = clean_profile(W / 2, H / 2)
    p = pos[k0:]
    n = np.arange(len(p))
    s = np.array(p, float)
    A = L.load_dem()
    z_dem = dem_along(A, s)
    out = {"capture": json.load(open(os.path.join(NAV, "session_state.json"), encoding="utf-8")),
           "map_px": [W, H], "m_per_px": res, "zoom": ZOOM, "hint": [LAT0, LON0], "transect_bearing_deg": BEARING_Y,
           "green_end_m": round(float(ge), 2), "crossings_s_m": [round(float(v), 2) for v in s], "n_ft": n.tolist()}
    # ---- alignment of crossings with the nautical spot sounding
    x_s, s_s = px_to_offsets(*NAUT_SOUNDING_PX, W, H, res)
    out["nautical_anchor"] = {"sounding_ft": NAUT_SOUNDING_FT, "container_px": list(NAUT_SOUNDING_PX), "x_m": round(x_s, 1), "s_m": round(s_s, 1),
                              "sonar_crossing_15_s_m": round(float(s[15]), 1), "offset_m": round(float(s[15] - s_s), 1)}
    # ---- datum test: the s range 0..40 m (beyond the surf zone, inside the DEM's best-resolved zone)
    sel = (s >= 0) & (s <= 40)
    out["datum_test"] = {}
    for k, dl in deltas.items():
        zn = -(n * FT) - dl
        d = (zn - z_dem)[sel]
        out["datum_test"][k] = {"delta_msl_minus_datum_m": round(dl, 3), "n_points": int(sel.sum()), "bias_nav_minus_dem_m": round(float(d.mean()), 3),
                                "rms_m": round(float(np.sqrt((d ** 2).mean())), 3)}
    zn = -(n * FT) - deltas["MLLW"]
    out["profile"] = {"s_m": [round(float(v), 2) for v in s], "z_nav_msl_assumed_mllw": [round(float(v), 3) for v in zn], "z_dem_msl": [round(float(v), 3) for v in z_dem],
                      "diff_nav_minus_dem": [round(float(v), 3) for v in (zn - z_dem)]}
    for name, lo, hi in (("reef_zone_-17_to_12", -17.0, 12.0), ("s_0_to_40", 0.0, 40.0), ("s_40_to_150", 40.0, 150.0), ("s_150_to_260", 150.0, 260.0), ("surf_zone_-50_to_-17", -50.0, -17.0)):
        m = (s >= lo) & (s <= hi)
        d = (zn - z_dem)[m]
        out["profile"]["stat_" + name] = {"n": int(m.sum()), "mean_diff_m": round(float(d.mean()), 3), "max_abs_diff_m": round(float(np.abs(d).max()), 3)}
    # ---- alongshore transects (each aligned on its own 0 ft line)
    al = []
    for xo in ALONG_OFFSETS:
        cx, cy = offsets_to_px(xo, 0.0, W, H, res)
        g_, ps, k = clean_profile(cx, cy)
        if k is None:
            continue
        q = ps[k:]
        n0 = float(np.interp(0.0, q, range(len(q)))) if q[0] < 0 < q[-1] else None
        al.append({"x_m": xo, "zero_ft_line_s_m": round(q[0], 1), "six_ft_s_m": round(q[6], 1) if len(q) > 6 else None, "depth_ft_at_s0": None if n0 is None else round(n0, 1),
                   "n_crossings": len(q)})
    out["alongshore"] = al
    d0 = [a["depth_ft_at_s0"] for a in al if a["depth_ft_at_s0"] is not None]
    out["alongshore_summary"] = {"depth_ft_at_s0_mean": round(float(np.mean(d0)), 2), "sd_ft": round(float(np.std(d0)), 2), "min_ft": min(d0), "max_ft": max(d0),
                                 "sd_m": round(float(np.std(d0)) * FT, 2), "n": len(d0)}
    # depth ft at the hint and at the reef centre if the reef sits 91.44 m seaward of the chart coastline (land/green boundary)
    land_line = None
    pts = T.transect(SONAR, ZOOM, LAT0, BEARING_Y, W / 2, H / 2, -400, 100)[1]
    yel = [d for d, mx, pp in pts if abs(pp[0] - 248) < 6 and abs(pp[1] - 232) < 6 and abs(pp[2] - 112) < 12]
    if yel:
        land_line = max(yel)
    out["chart_coastline_s_m"] = None if land_line is None else round(float(land_line), 1)
    if land_line is not None:
        s91 = land_line + 91.44
        nn = float(np.interp(s91, s, n))
        out["reef_centre_if_91m_from_chart_coastline"] = {"s_m": round(s91, 1), "depth_ft": round(nn, 2), "z_msl_assumed_mllw": round(-(nn * FT) - deltas["MLLW"], 2)}
    out["label_check"] = verify_labels(W, H, res)
    out["transect_datum_test"] = out["datum_test"]
    out["label_datum_test"] = label_datum_test()
    out["datum_test"] = {k: {"delta_msl_minus_datum_m": v["delta_msl_minus_datum_m"], "n_points": out["label_datum_test"]["zones"]["reef_zone"]["n"], "bias_nav_minus_dem_m": v["bias_nav_minus_dem_m"], "rms_m": v["rms_m"]}
                         for k, v in out["label_datum_test"]["datums"].items()}
    out["hint_depth_ft"] = round(float(np.interp(0.0, s, n)), 2)
    out["hint_z_msl_assumed_mllw"] = round(-(out["hint_depth_ft"] * FT) - deltas["MLLW"], 2)
    out["dem_z_msl_at_hint"] = round(float(dem_along(A, [0.0])[0]), 2)
    json.dump(out, open(os.path.join(NAV, "nav_transect.json"), "w", encoding="utf-8"), indent=1)
    return out


def _poly_px(W, H, res):
    shape = json.load(open(L.SHAPE, encoding="utf-8"))
    poly = shape["canonical"]["polygons_m"][0]
    yc = float(shape["canonical"]["distance_offshore_m"])
    return [offsets_to_px(x, y - yc, W, H, res) for x, y in poly]


def fig_sonar(nav):
    img = Image.open(SONAR).convert("RGB")
    W, H = img.size
    res = nav["m_per_px"]
    d = ImageDraw.Draw(img, "RGBA")
    f12, f14 = MA.font(12), MA.font(14)
    # reef outline at the hint
    poly = _poly_px(W, H, res)
    d.polygon(poly, fill=(220, 30, 200, 70), outline=(220, 30, 200, 255))
    d.line(poly + [poly[0]], fill=(220, 30, 200, 255), width=2)
    # transect
    p0, p1 = offsets_to_px(0, -70, W, H, res), offsets_to_px(0, 175, W, H, res)
    d.line([p0, p1], fill=(255, 140, 0, 255), width=2)
    for sv in range(-70, 176, 10):
        a = offsets_to_px(0, sv, W, H, res)
        e = offsets_to_px(5 if sv % 50 == 0 else 2.5, sv, W, H, res)
        d.line([a, e], fill=(255, 140, 0, 255), width=2)
        if sv % 50 == 0 and sv not in (0,):
            tag(d, (e[0] + 4, e[1] - 6), "s=%+d m" % sv, (200, 90, 0, 255), f12)
    # contour crossings
    for k, sv in enumerate(nav["crossings_s_m"]):
        a = offsets_to_px(0, sv, W, H, res)
        d.ellipse([a[0] - 3, a[1] - 3, a[0] + 3, a[1] + 3], outline=(230, 20, 20, 255), width=2)
        if k in (0, 6, 15, 20, 24):
            tag(d, (a[0] - 44, a[1] + 6), "%d ft" % k, (200, 0, 0, 255), f14)
    # hint star + label with leader
    cx, cy = W / 2, H / 2
    d.polygon([(cx, cy - 9), (cx + 3, cy - 3), (cx + 9, cy - 3), (cx + 4, cy + 2), (cx + 6, cy + 9), (cx, cy + 5), (cx - 6, cy + 9), (cx - 4, cy + 2), (cx - 9, cy - 3), (cx - 3, cy - 3)], fill=(255, 230, 0, 255), outline=(0, 0, 0, 255))
    d.line([(cx - 8, cy - 6), (330, 250)], fill=(0, 0, 0, 255), width=1)
    tag(d, (150, 238), "hint %.5f N, %.5f W = s 0 (depth there %.1f ft)" % (LAT0, -LON0, nav["hint_depth_ft"]), (0, 0, 0, 255), f14)
    # nautical anchor
    x_s, s_s = nav["nautical_anchor"]["x_m"], nav["nautical_anchor"]["s_m"]
    a = offsets_to_px(x_s, s_s, W, H, res)
    d.rectangle([a[0] - 12, a[1] - 9, a[0] + 12, a[1] + 9], outline=(0, 120, 255, 255), width=2)
    tag(d, (a[0] - 190, a[1] + 14), "spot sounding 15 ft (Nautical layer)", (0, 90, 220, 255), f12)
    # 0 ft / coastline notes
    ge = nav["green_end_m"]
    a = offsets_to_px(0, ge, W, H, res)
    d.line([(a[0] + 2, a[1] + 2), (640, 440)], fill=(20, 100, 20, 255), width=1)
    tag(d, (560, 442), "0 ft line = seaward edge of the green band (s = %.1f m)" % ge, (20, 100, 20, 255), f12)
    if nav.get("chart_coastline_s_m") is not None:
        a = offsets_to_px(0, nav["chart_coastline_s_m"], W, H, res)
        d.line([(a[0] + 2, a[1] + 2), (700, 250)], fill=(90, 70, 0, 255), width=1)
        tag(d, (610, 232), "chart coastline (green/yellow edge), s = %.1f m" % nav["chart_coastline_s_m"], (90, 70, 0, 255), f12)
    # scale bar 50 m and north arrow
    bx, by = 40, H - 40
    L50 = 50 / res
    d.line([(bx, by), (bx + L50, by)], fill=(0, 0, 0, 255), width=4)
    for t in (0, 10, 20, 30, 40, 50):
        d.line([(bx + t / res, by - 5), (bx + t / res, by + 5)], fill=(0, 0, 0, 255), width=2)
    d.text((bx, by - 22), "50 m (%.4f m/px)" % res, fill=(0, 0, 0, 255), font=f14)
    d.line([(W - 40, 70), (W - 40, 30)], fill=(0, 0, 0, 255), width=3)
    d.polygon([(W - 40, 22), (W - 46, 36), (W - 34, 36)], fill=(0, 0, 0, 255))
    d.text((W - 46, 74), "N", fill=(0, 0, 0, 255), font=f14)
    dt = nav["datum_test"]
    lc = nav["label_check"]
    cap = [
        "Source: Garmin Navionics (c) Garmin, 'Marine Maps' web viewer https://maps.garmin.com/en-US/marine/ (reached via https://webapp.navionics.com/), accessed 2026-10-05; layer SonarChart Maps, depth units feet, shallow shading 6 ft, zoom 18 (max), "
        "centre = position hint of the removed reef (centre of the Borrero & Nelsen 2003 Fig. 9 survey window; +-60 m). Private research copy; 'Not to be used for navigation'; reuse not cleared. The page states neither the depth datum nor the contour interval.",
        "Read: ORANGE line = shore-normal transect (bearing 245 deg) through the hint; RED circles = the %d contour lines crossed, counted from the 0 ft line (index n = n ft; 1 ft interval checked: 7 lines bound the 6 ft blue shading band). "
        "Depth at the hint = %.1f ft = %.2f m below the (assumed MLLW) chart datum = %.2f m MSL; NOAA DEM at the same point %.2f m MSL." % (len(nav["crossings_s_m"]), nav["hint_depth_ft"], nav["hint_depth_ft"] * FT, nav["hint_z_msl_assumed_mllw"], nav["dem_z_msl_at_hint"]),
        "MAGENTA = the Phase I design outline (435 m2) placed with its centroid on the hint (position uncertain by +-60 m). The reef was removed in 2008-2010 and is not visible in any contour: this chart is used for the SEABED only. "
        "BLUE box = the nautical-layer spot sounding 15 ft read on nautical_ft_z18_map.png; it lies %.1f m from the 15th contour crossing (anchor of the counting)." % abs(nav["nautical_anchor"]["offset_m"]),
        "Datum test (no counting involved): the %d depth labels / spot soundings of the 8-18 ft zone, read directly, compared with the NOAA DEM at the same ground points: bias (Navionics - DEM) %+.2f m if the depths are below MLLW, %+.2f NAVD88, %+.2f LAT, %+.2f MSL (RMS %.2f / %.2f / %.2f / %.2f m). MSL and LAT are rejected; MLLW and NAVD88 (0.06 m apart) cannot be separated: MLLW is an assumption. "
        "Counting check: the 24 contour lines of the transect reproduce the labels 1, 4 and 5 ft exactly but only %d of %d labels overall (deeper labels differ by 1-3 lines), so the contour count carries +-2 lines (+-0.6 m) beyond 6 ft."
        % (dt["MLLW"]["n_points"], dt["MLLW"]["bias_nav_minus_dem_m"], dt["NAVD88"]["bias_nav_minus_dem_m"], dt["LAT"]["bias_nav_minus_dem_m"], dt["MSL"]["bias_nav_minus_dem_m"], dt["MLLW"]["rms_m"], dt["NAVD88"]["rms_m"], dt["LAT"]["rms_m"], dt["MSL"]["rms_m"], lc["n_match"], lc["n"]),
    ]
    out = MA.caption_canvas(img, cap, fsize=14)
    out.save(os.path.join(OUT, "A9_navionics_sonarchart_contours_transect.png"))


def fig_nautical(nav):
    img = Image.open(NAUT).convert("RGB")
    W, H = img.size
    res = nav["m_per_px"]
    d = ImageDraw.Draw(img, "RGBA")
    f12, f14 = MA.font(12), MA.font(14)
    poly = _poly_px(W, H, res)
    d.line(poly + [poly[0]], fill=(220, 30, 200, 255), width=2)
    p0, p1 = offsets_to_px(0, -70, W, H, res), offsets_to_px(0, 175, W, H, res)
    d.line([p0, p1], fill=(255, 140, 0, 255), width=2)
    cx, cy = W / 2, H / 2
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 230, 0, 255), outline=(0, 0, 0, 255))
    d.text((cx + 8, cy - 22), "hint (s = 0)", fill=(0, 0, 0, 255), font=f14)
    marks = [((340, 379), "15 ft"), ((212, 594), "23 ft"), ((357, 594), "19 ft"), ((611, 405), "3 ft")]
    for (px, py), lab in marks:
        d.ellipse([px - 14, py - 11, px + 14, py + 11], outline=(0, 120, 255, 255), width=2)
        x_, s_ = px_to_offsets(px, py, W, H, res)
        d.text((px + 16, py + 8), "%s  (x %+.0f, s %+.0f m)" % (lab, x_, s_), fill=(0, 70, 200, 255), font=f12)
    d.text((560, 470), "blue band = 0-6 ft shading", fill=(0, 60, 160, 255), font=f12)
    d.text((640, 330), "green = drying (above chart datum)", fill=(30, 100, 20, 255), font=f12)
    d.text((780, 300), "yellow = land", fill=(110, 90, 0, 255), font=f12)
    bx, by = 40, H - 40
    L50 = 50 / res
    d.line([(bx, by), (bx + L50, by)], fill=(0, 0, 0, 255), width=4)
    d.text((bx, by - 22), "50 m", fill=(0, 0, 0, 255), font=f14)
    cap = [
        "Source: Garmin Navionics (c) Garmin, Marine Maps web viewer https://maps.garmin.com/en-US/marine/, accessed 2026-10-05; layer Nautical Charts, depth units feet, zoom 18, centre = text position hint. Private research copy; 'Not to be used for navigation'.",
        "Read: spot soundings (BLUE rings, value in feet, position given as x alongshore / s offshore metres from the hint) and the 0-6 ft shading band. The sounding '15' lies %.1f m from the 15th SonarChart contour on the transect (anchor of the contour counting, see A9). "
        "The coarse contour lines of this layer are not used." % abs(nav["nautical_anchor"]["offset_m"]),
        "MAGENTA = Phase I design outline placed on the hint (position +-60 m); no reef is drawn on the chart (removed 2008-2010).",
    ]
    MA.caption_canvas(img, cap, fsize=14).save(os.path.join(OUT, "A10_navionics_nautical_chart_soundings.png"))


def fig_profile(nav):
    pr = nav["profile"]
    s = np.array(pr["s_m"])
    zn = np.array(pr["z_nav_msl_assumed_mllw"])
    zd = np.array(pr["z_dem_msl"])
    fig, ax = plt.subplots(1, 2, figsize=(14, 5.6), gridspec_kw={"width_ratios": [2.2, 1]})
    a = ax[0]
    a.axvspan(-17, 12, color="m", alpha=0.12, label="reef extent if its centre is at the hint (+-14 m)")
    a.plot(s, zd, "k-", lw=2, label="NOAA DEM at the same ground transect (z_NAVD88 - 0.792)")
    a.plot(s, zn, "o-", color="tab:red", ms=4, lw=1, label="Navionics SonarChart contours, n ft below chart datum assumed MLLW (z = -n x 0.3048 - 0.849)")
    zm = -(np.arange(len(s)) * FT)
    a.plot(s, zm, "x:", color="gray", ms=4, lw=1, label="same contours if the datum were MSL (rejected)")
    a.set_xlabel("distance seaward of the hint along 245 deg, s (m)")
    a.set_ylabel("z (m rel. MSL)")
    a.set_title("Seabed profile: Navionics SonarChart vs NOAA DEM (private research copy of the chart; seabed only, reef removed)")
    a.grid(alpha=0.3)
    a.legend(fontsize=8, loc="lower left")
    st = pr["stat_s_0_to_40"]
    a.annotate("s = 0-40 m: mean (Navionics - DEM) = %+.2f m\nreef zone: %+.2f m; surf zone s < -17 m: %+.2f m; s > 150 m: %+.2f m" % (st["mean_diff_m"], pr["stat_reef_zone_-17_to_12"]["mean_diff_m"], pr["stat_surf_zone_-50_to_-17"]["mean_diff_m"], pr["stat_s_150_to_260"]["mean_diff_m"]),
               xy=(0.02, 0.97), xycoords="axes fraction", va="top", fontsize=9, bbox=dict(boxstyle="round", fc="w", alpha=0.85))
    b = ax[1]
    dt = nav["datum_test"]
    names = ["MLLW", "NAVD88", "MSL", "LAT"]
    vals = [dt[k]["rms_m"] for k in names]
    b.bar(names, vals, color=["tab:red" if k == "MLLW" else "gray" for k in names])
    for i, v in enumerate(vals):
        b.text(i, v + 0.02, "%.2f m" % v, ha="center", fontsize=9)
    b.set_ylabel("RMS (Navionics - DEM), m")
    b.set_title("Which datum are the chart depths below?\n(depth labels 8-18 ft vs DEM, n = %d)" % dt["MLLW"]["n_points"])
    b.grid(alpha=0.3, axis="y")
    fig.text(0.01, 0.01, "Method: contour lines counted along the transect in src/navionics/sonar_ft_z18_map.png (1 ft interval from the 0-6 ft shading band; labels 1, 4, 5 ft reproduced exactly, deeper labels +-1-3 lines).\nChart datum not stated by the app: MLLW is an assumption; the right-hand test uses depth labels (not counting), cannot separate MLLW from NAVD88 (0.06 m) but rejects MSL and LAT.",
             fontsize=8)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(os.path.join(OUT, "A11_navionics_vs_noaa_dem_profile.png"), dpi=110)
    plt.close(fig)


def main():
    nav = compute()
    fig_sonar(nav)
    fig_nautical(nav)
    fig_profile(nav)
    print("nav_transect.json + A9, A10, A11 written")
    return nav


if __name__ == "__main__":
    main()
