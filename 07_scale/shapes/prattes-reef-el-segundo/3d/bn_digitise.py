"""bn_digitise.py - reads the vector figures of Borrero & Nelsen (2003) straight from the PDF paths and writes
src/bn2003_digitised.json (Figs 5, 7, 9) plus the hand-read Fig. 8 table.

Input : ../src/borrero_nelsen_2003_prattes_monitoring_results.pdf (private research copy supplied by Lior 2026-10-05)
Method: PyMuPDF page.get_drawings() returns every stroked path in PDF points; the axes are calibrated from the tick-mark
        lines (not from label centres): linear map  value = v0 + (coordinate - c0) / pts_per_unit.
        Fig. 5 (page 4): x = distance from the dune base (m), z (m; zero line = 'Approx. Min Low Tide' drawn at 0, datum not stated)
        Fig. 7 (page 6, top): x same origin, z (m, datum not stated; see METHODS_3D.md 3.10)
        Fig. 8 (page 6, bottom) is a RASTER; its numbers are read by eye on the 969 x 560 px image (+-0.05 m, +-0.5 m)
        Fig. 9 (page 7): UTM grid ticks every 20 m: E = 367460 + (x - 216.1)/2.495 ; N = 3754240 + (309.5 - y)/2.485 (zone 11, datum not stated)
Run   : python bn_digitise.py
"""
import json
import math
import os

import fitz
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(os.path.dirname(HERE), "src", "borrero_nelsen_2003_prattes_monitoring_results.pdf")
OUT = os.path.join(HERE, "src", "bn2003_digitised.json")


def stroke_points(x):
    pts = []
    for it in x["items"]:
        if it[0] == "l":
            if not pts or abs(pts[-1][0] - it[1].x) > 0.01 or abs(pts[-1][1] - it[1].y) > 0.01:
                pts.append((it[1].x, it[1].y))
            pts.append((it[2].x, it[2].y))
    return pts


def fig5(doc):
    p = doc[3]
    xt = {0: 141.5, 50: 196.4, 100: 251.3, 150: 306.2, 200: 361.1, 250: 416.0, 300: 470.9}      # tick x (pt) of the distance axis (from the 5-tick groups)
    k_x = (xt[300] - xt[0]) / 300.0
    y0, k_y = 455.82, 8.6                                                                           # z = 0 tick; pt per m (ticks at 6 -> 404.2 ... -6 -> 507.6)
    prof = None
    lines = {}
    for x in p.get_drawings():
        c = x.get("color")
        pts = stroke_points(x)
        if c == (0.0, 0.0, 0.0) and len(x["items"]) == 18:
            prof = pts
        elif c == (0.0, 0.0, 1.0) and len(pts) == 2 and pts[0][0] > 200:
            lines["max_high_tide_z"] = round((y0 - pts[0][1]) / k_y, 2)
        elif c is not None and abs(c[1] - 0.905) < 0.01 and len(pts) == 2 and pts[0][0] > 200:
            lines["min_low_tide_z"] = round((y0 - pts[0][1]) / k_y, 2)
    return {"distance_m": [round((a - xt[0]) / k_x, 1) for a, b in prof], "z_m": [round((y0 - b) / k_y, 2) for a, b in prof], "tide_lines_z_m": lines,
            "calibration": {"x0_pt": xt[0], "pt_per_m_x": round(k_x, 4), "z0_pt": y0, "pt_per_m_z": k_y}}


def fig7(doc):
    p = doc[5]
    x0, k_x = 143.63, (438.8 - 143.63) / 250.0
    y0, k_y = 135.23, (170.63 - 82.19) / 10.0                                                      # z=0 tick 135.23; 6 -> 82.19; -4 -> 170.63
    out = {}
    names = {(1.0, 0.0, 0.0): "Nov 2000", (0.0, 0.0, 0.0): "Oct 2001", (0.0, 0.0, 1.0): "Oct 2002"}
    for x in p.get_drawings():
        c = x.get("color")
        if x.get("width") and x["width"] > 1.0 and len(x["items"]) > 2 and c in names:
            pts = stroke_points(x)
            out[names[c]] = {"distance_m": [round((a - x0) / k_x, 1) for a, b in pts], "z_m": [round((y0 - b) / k_y, 2) for a, b in pts]}
    return {"profiles": out, "calibration": {"x0_pt": x0, "pt_per_m_x": round(k_x, 4), "z0_pt": y0, "pt_per_m_z": round(k_y, 3)}}


def fig8_hand():
    # read by eye on the native 969 x 560 px raster (x: 180 at px 285.5, 11.05 px/m; z: -2.0 at px 84, 138 px/m)
    return {"note": "RASTER figure; peak positions read by eye on the 969 x 560 px image, +-0.05 m vertical, +-0.5 m horizontal; datum of the 'height (m)' axis not stated",
            "crest": {"May 2001": {"distance_m": 203.6, "z_m": -1.77}, "October 2001": {"distance_m": 202.7, "z_m": -1.94},
                      "February 2002": {"distance_m": 200.1, "z_m": -2.64}, "September 2002": {"distance_m": 202.6, "z_m": -3.22}},
            "bed_beside_reef": {"May 2001": {"landward": [186.0, -3.27]}, "October 2001": {"landward": [193.8, -4.05], "seaward": [223.3, -4.14]},
                                "February 2002": {"landward": [195.5, -3.60], "seaward": [231.0, -4.46]}, "September 2002": {"landward": [193.0, -3.64]}}}


def fig9(doc):
    p = doc[6]
    E = lambda x: 367460 + (x - 216.1) / 2.495
    N = lambda y: 3754240 + (309.5 - y) / 2.485
    labels = {(0.0, 1.0, 0.773): -4, (0.0, 0.81, 1.0): -3, (0.0, 0.333, 1.0): -2, (0.1, 0.0, 1.0): -1, (0.0, 1.0, 0.591): -4, (0.0, 0.905, 1.0): -3, (0.25, 0.0, 1.0): -1}
    cont = []
    for x in p.get_drawings():
        c, w = x.get("color"), x.get("width")
        if not (c and w and (abs(w - 1.794) < 0.01 or (0.8 < w < 1.0 and c != (0.0, 0.0, 0.0)))):
            continue
        if x["rect"].width < 30 and x["rect"].height < 2:
            continue
        key = tuple(round(v, 3) for v in c)
        lab = -2 if key == (0.0, 0.333, 1.0) else labels[key]
        pts = stroke_points(x)
        cont.append({"value_m": lab, "survey": "March 2001" if abs(w - 1.794) < 0.01 else "October 2000", "solid": abs(w - 1.794) < 0.01,
                     "easting_m": [round(E(a), 1) for a, b in pts], "northing_m": [round(N(b), 1) for a, b in pts]})
    return {"contours": cont, "utm": "zone 11 N (central meridian 117 W); horizontal datum not stated (NAD83/WGS84 assumed)",
            "window_E": [round(367460 + (188.8 - 216.1) / 2.495, 1), round(367460 + (467.7 - 216.1) / 2.495, 1)],
            "window_N": [round(3754240 + (309.5 - 311.3) / 2.485, 1), round(3754240 + (309.5 - 133.7) / 2.485, 1)]}


def fig9_vs_dem(f9):
    """mean (survey contour value - NOAA DEM z_MSL at the contour vertices), per survey; needs pyproj and the DEM export"""
    from pyproj import Transformer
    import reef3d_lib as L
    tr = Transformer.from_crs("EPSG:32611", "EPSG:4326", always_xy=True)
    A = L.load_dem()
    ds = L.load_datums("9410840")
    off = ds["MSL"] - ds["NAVD88"]
    out = {}
    for survey in ("October 2000", "March 2001"):
        diffs = []
        for c in f9["contours"]:
            if c["survey"] != survey:
                continue
            lo, la = tr.transform(np.array(c["easting_m"]), np.array(c["northing_m"]))
            z = np.array([L.sample(A, x, y) - off for x, y in zip(lo, la)])
            diffs.append((c["value_m"], float(np.nanmean(z)), c["value_m"] - float(np.nanmean(z))))
        out[survey] = {"mean_offset_m": round(float(np.mean([d[2] for d in diffs])), 2), "by_contour": [{"value_m": v, "dem_z_msl": round(z, 2), "offset_m": round(o, 2)} for v, z, o in diffs]}
    lo, la = tr.transform(367505.0, 3754275.0)
    out["window_centre_lat_lon"] = [round(float(la), 5), round(float(lo), 5)]
    # mean direction of the contours (total least squares inside the window), grid -> true bearing with the UTM convergence
    brg = []
    for c in f9["contours"]:
        E, Nn = np.array(c["easting_m"]), np.array(c["northing_m"])
        m = (Nn > 3754242) & (Nn < 3754308) & (E > 367452) & (E < 367558)
        if m.sum() < 4:
            continue
        X = np.c_[E[m] - E[m].mean(), Nn[m] - Nn[m].mean()]
        v = np.linalg.svd(X, full_matrices=False)[2][0]
        if v[1] > 0:
            v = -v
        brg.append((math.degrees(math.atan2(v[0], v[1])) + 360) % 360)
    gamma = (float(lo) + 117.0) * math.sin(math.radians(float(la)))
    out["contour_bearing"] = {"grid_deg": round(float(np.mean(brg)), 1), "sd_deg": round(float(np.std(brg)), 1), "n": len(brg), "convergence_deg": round(gamma, 2), "true_deg": round(float(np.mean(brg)) + gamma, 1)}
    return out


def derived(f5, f7):
    d, z = np.array(f7["profiles"]["Oct 2001"]["distance_m"]), np.array(f7["profiles"]["Oct 2001"]["z_m"])
    i = int(np.argmax(np.where((d > 150) & (d < 230), z, -99)))
    peak_d, peak_z = float(d[i]), float(z[i])
    # beds beside the reef: the lowest vertex landward (150-200 m) and the vertex seaward of the reef (> peak, lowest before the profile ends)
    land = [(dd, zz) for dd, zz in zip(d, z) if 150 < dd < peak_d]
    bed_land = min(land, key=lambda t: t[1])
    sea = [(dd, zz) for dd, zz in zip(d, z) if peak_d < dd < 232]
    bed_sea = min(sea, key=lambda t: t[1])
    # base: first point where the profile leaves the landward bed, last point of the seaward bed
    zero = None
    for k in range(len(d) - 1):
        if z[k] >= 0 > z[k + 1]:
            zero = d[k] + (0 - z[k]) / (z[k + 1] - z[k]) * (d[k + 1] - d[k])
    mid = 0.5 * (bed_land[0] + bed_sea[0])
    der = {"peak_distance_m": peak_d, "peak_z_m": peak_z, "bed_landward": [float(bed_land[0]), float(bed_land[1])], "bed_seaward": [float(bed_sea[0]), float(bed_sea[1])],
           "relief_above_landward_bed_m": round(peak_z - bed_land[1], 2), "relief_above_seaward_bed_m": round(peak_z - bed_sea[1], 2),
           "base_width_m": round(float(bed_sea[0] - bed_land[0]), 1), "zero_crossing_distance_m": None if zero is None else round(float(zero), 1)}
    if zero is not None:
        der["peak_from_zero_crossing_m"] = round(peak_d - float(zero), 1)
        der["base_midpoint_from_zero_crossing_m"] = round(mid - float(zero), 1)
    d5, z5 = np.array(f5["distance_m"]), np.array(f5["z_m"])
    i5 = int(np.argmax(np.where((d5 > 150) & (d5 < 230), z5, -99)))
    land5 = [(a, b) for a, b in zip(d5, z5) if 150 < a < d5[i5]]
    sea5 = [(a, b) for a, b in zip(d5, z5) if d5[i5] < a < 232]
    bl5, bs5 = min(land5, key=lambda t: t[1]), min(sea5, key=lambda t: t[1])
    zc = None
    for k in range(len(d5) - 1):
        if z5[k] >= 0.0 > z5[k + 1]:
            zc = d5[k] + (0 - z5[k]) / (z5[k + 1] - z5[k]) * (d5[k + 1] - d5[k])
    zm = None
    for k in range(len(d5) - 1):
        if z5[k] >= 0.849 > z5[k + 1]:
            zm = d5[k] + (0.849 - z5[k]) / (z5[k + 1] - z5[k]) * (d5[k + 1] - d5[k])
    der5 = {"peak_distance_m": float(d5[i5]), "peak_z_m": float(z5[i5]), "bed_landward": [float(bl5[0]), float(bl5[1])], "bed_seaward": [float(bs5[0]), float(bs5[1])],
            "relief_above_landward_bed_m": round(float(z5[i5] - bl5[1]), 2), "relief_above_seaward_bed_m": round(float(z5[i5] - bs5[1]), 2),
            "zero_line_crossing_distance_m": None if zc is None else round(float(zc), 1), "plus_0p849_crossing_distance_m": None if zm is None else round(float(zm), 1)}
    return der, der5


def main():
    doc = fitz.open(PDF)
    f5, f7, f9 = fig5(doc), fig7(doc), fig9(doc)
    der7, der5 = derived(f5, f7)
    out = {"source": "Borrero & Nelsen (2003), file src/borrero_nelsen_2003_prattes_monitoring_results.pdf (supplied by Lior 2026-10-05)", "fig5": f5, "fig5_derived": der5, "fig7": f7,
           "fig7_oct2001_derived": der7, "fig8": fig8_hand(), "fig9": f9, "fig9_vs_dem": fig9_vs_dem(f9),
           "offset_fig5_minus_fig7_m": round(der5["peak_z_m"] - der7["peak_z_m"], 2),
           "offset_fig5_minus_fig7_bed_m": round(der5["bed_landward"][1] - der7["bed_landward"][1], 2)}
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1)
    print(json.dumps({k: out[k] for k in ("fig5_derived", "fig7_oct2001_derived", "offset_fig5_minus_fig7_m", "offset_fig5_minus_fig7_bed_m")}, indent=1))
    return out


if __name__ == "__main__":
    main()
