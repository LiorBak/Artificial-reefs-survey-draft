"""build_3d.py - regenerates model.js, docs.js, METHODS_3D.md and computed.json for Pratte's Reef (El Segundo).

Inputs  : ../shape.json (verified plan outline, canonical frame), src/noaa_*.json (tidal datums),
          src/noaa_*.tif (DEM exports), METHODS_3D.template.md, SOURCES_3D.md
Outputs : model.js  (window.REEF_MODEL)   docs.js (window.REEF_DOCS)   METHODS_3D.md   computed.json
          and an auto block in SOURCES_3D.md (plan shape status at build time)
Usage   : python build_3d.py            (re-run whenever shape.json changes; add --annotations to also redraw annotated/*.png)
Everything numeric in the model is either read from a source file here or defined in the SOURCES table below with
its source id; nothing is typed into the viewer.
"""
import datetime
import hashlib
import json
import math
import os
import re
import sys

import numpy as np
import shapely
from shapely.geometry import Polygon

import reef3d_lib as L

HERE = L.HERE
TODAY = datetime.date.today().isoformat()

# ------------------------------------------------------------------------------------------------ constants
BAG = {"length_m": 3.0, "width_m": 2.13, "height_m": 1.2, "volume_max_m3": 7.9, "fill_min": 0.80, "fill_max": 0.90}
SLOPE_RUN_DEFAULT = 1.0           # A5: horizontal metres per metre of rise of the stacked-bag side slope
SLOPE_RUN_RANGE = [0.5, 2.5]
MIN_HEIGHT_M = BAG["height_m"]    # A6: a bag course is at least one bag high
CELL = 0.25                       # m, reef height-field grid for the Python volume check (viewer uses 0.25 m too)
N_BAGS_PHASE1 = 110
N_BAGS_FINAL = 200
Y_NOMINAL = None                  # filled from shape.json (distance_offshore_m = 91.44)

LEVELS_ORDER = ["LAT", "MLLW", "MLW", "MSL", "MHW", "MHHW", "HAT"]
LEVEL_LABEL = {"LAT": "LAT (lowest astronomical tide)", "MLLW": "MLLW (mean lower low water)", "MLW": "MLW",
               "MSL": "MSL (mean sea level) = model zero", "MHW": "MHW", "MHHW": "MHHW (mean higher high water)",
               "HAT": "HAT (highest astronomical tide)"}


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def reef_height_field(poly, seabed_fn, state, slope_run, min_h=MIN_HEIGHT_M, cell=CELL, y_shift=0.0, thick_override=None):
    """Reef height above the seabed on a regular grid.
         level mode     : h_top(y) = max(z_c - z_bed(y), min_h)                      (crest at a fixed elevation z_c)
         thickness mode : h_top     = max(z_ref - z_bed(y_ref + shift), min_h)       (top parallel to the bed; z_ref at the offshore face)
         h(x,y) = max(0, min(h_top, d_in(x,y) / s)),  d_in = distance inside the toe outline (0 on the outline), s = slope_run.
       Returns (X, Y, H, inside, Htop)."""
    b = poly.bounds
    xs = np.arange(b[0] - 1 + cell / 2, b[2] + 1, cell)
    ys = np.arange(b[1] - 1 + cell / 2, b[3] + 1, cell)
    X, Y = np.meshgrid(xs, ys)
    inside = shapely.contains_xy(poly, X, Y)
    d = np.zeros_like(X)
    pts = shapely.points(X[inside], Y[inside])
    d[inside] = shapely.distance(pts, poly.exterior)
    zb = seabed_fn(Y + y_shift)
    if state["mode"] == "level":
        Htop = np.maximum(state["z_msl"] - zb, min_h)
    else:
        t = thick_override if thick_override is not None else max(state["z_ref_msl"] - float(seabed_fn(state["y_ref_m"] + y_shift)), min_h)
        Htop = np.full_like(zb, t)
    H = np.where(inside, np.minimum(Htop, d / slope_run), 0.0)
    return X, Y, H, inside, Htop


def main(annotations=False):
    # ---------------------------------------------------------------- plan shape (re-read at build time)
    shape_bytes = open(L.SHAPE, "rb").read()
    shape = json.loads(shape_bytes.decode("utf-8"))
    can = shape["canonical"]
    poly_xy = can["polygons_m"][0]
    poly = Polygon(poly_xy)
    assert poly.is_valid, "outline polygon invalid"
    x_bearing = 155.0                                   # canonical +x bearing (shape.json frame text: '~155 deg')
    y_bearing = float(can.get("shore_normal_bearing_deg", 245))
    assert abs(y_bearing - (x_bearing + 90)) < 1e-6
    y_nom = float(can["distance_offshore_m"])
    plan = {
        "status": shape["status"], "verified_on": shape.get("verified_on"), "shape_json_updated": shape.get("updated"),
        "shape_json_md5": hashlib.md5(shape_bytes).hexdigest(), "shape_json_mtime": datetime.datetime.fromtimestamp(
            os.path.getmtime(L.SHAPE)).isoformat(timespec="seconds"),
        "confidence_plan": shape["confidence"]["level"], "area_m2": can["area_m2"], "bbox_m": can["bbox_m"],
        "max_dim_m": can["max_dim_m"], "distance_offshore_m": y_nom, "n_vertices": len(poly_xy),
        "polygon_xy_m": [[round(p[0], 3), round(p[1], 3)] for p in poly_xy],
        "polygon_area_check_m2": round(poly.area, 2),
        "drawn": shape["design_version"]["drawn"], "geo": shape.get("geo"),
        "y_range_m": [round(poly.bounds[1], 2), round(poly.bounds[3], 2)],
        "x_range_m": [round(poly.bounds[0], 2), round(poly.bounds[2], 2)],
    }
    if shape["status"] != "verified":
        print("WARNING: shape.json status is %r (not 'verified')" % shape["status"])

    # ---------------------------------------------------------------- tides / datums
    lev, ds = L.datum_levels_msl("9410840")
    lev_la, ds_la = L.datum_levels_msl("9410660")
    msl_mllw = round(ds["MSL"] - ds["MLLW"], 3)            # 0.849
    msl_mllw_la = round(ds_la["MSL"] - ds_la["MLLW"], 3)   # 0.861
    water_levels = [{"id": k, "z": lev[k], "label": LEVEL_LABEL[k],
                     "source": "NOAA CO-OPS 9410840 Santa Monica, epoch %s (LAT/HAT: station record, HAT predicted 2040-07-24)" % ds["_epoch"]}
                    for k in LEVELS_ORDER]

    # ---------------------------------------------------------------- seabed: NOAA DEM profile (primary), CRM (check), Navionics (check / alternative)
    A = L.load_dem()
    prof = L.seabed_profile(x_bearing, A=A)
    y_prof = prof["y"]
    z_prof = prof["z_mean"]
    C = L.load_dem("noaa_socal_crm_1as_export.tif")
    prof_c = L.seabed_profile(x_bearing, A=C, navd_to_msl=0.0, cell=1 / 3600.0)

    def seabed_fn(y):
        return np.interp(y, y_prof, z_prof)

    def at(yv):
        return float(np.interp(yv, y_prof, z_prof))

    y_tips, y_apex = plan["y_range_m"]
    seabed_checks = {
        "dem_z_at_nominal_m": round(at(y_nom), 2), "dem_sd_at_nominal_m": round(float(np.interp(y_nom, y_prof, prof["z_std"])), 2),
        "dem_z_at_tips_m": round(at(y_tips), 2), "dem_z_at_apex_m": round(at(y_apex), 2),
        "crm_z_at_nominal_m": round(float(np.interp(y_nom, prof_c["y"], prof_c["z_mean"])), 2),
        "y_at_15ft_m": round(float(np.interp(-15 * 0.3048, z_prof[::-1], y_prof[::-1])), 1),
        "slope_1_in": round(1.0 / abs((at(y_apex) - at(y_tips)) / (y_apex - y_tips)), 1),
        "n_stations": prof["n"], "waterline_offset_mean_m": round(float(prof["waterline_offsets"].mean()), 1),
        "waterline_offset_sd_m": round(float(prof["waterline_offsets"].std()), 1),
        "navd88_to_msl_m": round(prof["navd_to_msl"], 3),
    }
    y_hint = round(-float(prof["waterline_offsets"].mean()), 1)          # distance of the hint point from the DEM's MSL waterline (101.2 m)

    # ---- Navionics SonarChart transect through the hint (src/navionics/nav_transect.json, made by nav_annotate.py)
    navp = os.path.join(L.SRC, "navionics", "nav_transect.json")
    if not os.path.exists(navp):
        import nav_annotate
        nav_annotate.compute()
    nav = json.load(open(navp, encoding="utf-8"))
    nav_s = np.array(nav["crossings_s_m"], float)
    nav_n = np.arange(len(nav_s))
    nav_y = y_hint + nav_s
    nav_z = -(nav_n * 0.3048) - msl_mllw                                   # z_MSL = -(n ft) - (MSL - MLLW), chart datum assumed MLLW

    def nav_fn(y):
        return np.interp(y, nav_y, nav_z, left=np.nan, right=np.nan)

    def seabed_nav_fn(y):                                                  # Navionics where it has contours, DEM elsewhere
        v = nav_fn(y)
        return np.where(np.isnan(v), seabed_fn(y), v)

    nav_on_grid = [None if np.isnan(v) else round(float(v), 3) for v in nav_fn(y_prof)]
    seabed = {
        "kind": "alongshore-uniform cross-shore profile z(y); y from the MSL waterline",
        "extent": {"x": [-150, 150], "y": [float(y_prof[0]), float(y_prof[-1])]},
        "profile_y_m": [round(float(v), 1) for v in y_prof],
        "profile_z_m": [round(float(v), 3) for v in z_prof],
        "profile_sd_m": [round(float(v), 3) for v in prof["z_std"]],
        "profile_zmin_m": [round(float(v), 3) for v in prof["z_min"]],
        "profile_zmax_m": [round(float(v), 3) for v in prof["z_max"]],
        "crm_check_z_m": [round(float(np.interp(v, prof_c["y"], prof_c["z_mean"])), 3) for v in y_prof],
        "navionics": {"y_m": [round(float(v), 2) for v in nav_y], "z_m": [round(float(v), 3) for v in nav_z], "profile_z_m": nav_on_grid,
                      "y_hint_m": y_hint, "valid_y_m": [round(float(nav_y[0]), 1), round(float(nav_y[-1]), 1)],
                      "layer": "Garmin Navionics SonarChart Maps (Marine Maps web viewer), depth units feet, zoom 18, 1 ft contours counted along 245 deg through %.5f N %.5f W" % (L.HINT_LAT, -L.HINT_LON),
                      "datum_assumed": "MLLW (not stated by the app; test: RMS vs DEM %.3f m MLLW, %.3f m NAVD88, %.3f m LAT, %.3f m MSL)" % (
                          nav["datum_test"]["MLLW"]["rms_m"], nav["datum_test"]["NAVD88"]["rms_m"], nav["datum_test"]["LAT"]["rms_m"], nav["datum_test"]["MSL"]["rms_m"]),
                      "accessed": "2026-10-05", "n_contours": len(nav_s)},
        "shoreline_y_m": 0.0,
        "nominal_reef_y_m": y_nom,
        "reef_offset_range_m": [60.0, 130.0],
        "datum": "z_MSL = z_NAVD88 - %.3f" % prof["navd_to_msl"],
        "source": "NOAA NGDC (2010) Santa Monica CA 1/3 arc-second NAVD88 Coastal DEM; mean of %d alongshore stations (+-%d m) about %.5f N %.5f W" % (prof["n"], L.ALONG_BAND_M, L.HINT_LAT, -L.HINT_LON),
        "checks": seabed_checks,
    }

    # ---------------------------------------------------------------- Borrero & Nelsen (2003): digitised profile figures (bn_digitise.py)
    if not os.path.exists(os.path.join(L.SRC, "bn2003_digitised.json")):
        import bn_digitise
        bn_digitise.main()
    dig = json.load(open(os.path.join(L.SRC, "bn2003_digitised.json"), encoding="utf-8"))
    d5, d7, f8 = dig["fig5_derived"], dig["fig7_oct2001_derived"], dig["fig8"]
    bed5_msl = [d5["bed_landward"][1] - msl_mllw, d5["bed_seaward"][1] - msl_mllw]             # Fig. 5 axis read as MLLW
    bed5_mean_msl = float(np.mean(bed5_msl))

    # ---------------------------------------------------------------- crest scenarios (z_MSL).  Only the as-built Phase I is modelled (Lior, 2026-10-05).
    z_A = round(-6 * 0.3048, 3)
    z_B = round(-6 * 0.3048 - msl_mllw, 3)          # Borrero & Nelsen (2003) p.2: 'approximately - 6 ft MLLW' (ICCE 2010 rounds it to 1.8 m)
    z_C = round(-3 * 0.3048 - msl_mllw, 3)          # Borrero & Nelsen (2003) p.3: Phase II crest 'within 3ft of MLLW' (ICCE 2010: 1 m; RWR: 0.9 m)
    crest_states = [
        {"id": "B", "mode": "thickness", "label": "B  Phase I as installed (Sept 2000): outermost point approximately 6 ft below MLLW (Borrero & Nelsen 2003 p.2); top follows the seabed",
         "short": "B: as installed (6 ft MLLW), top parallel to bed", "z_ref_msl": z_B, "y_ref_m": round(y_apex, 2), "datum_stated": "MLLW", "value_stated": "approximately - 6 ft MLLW (= 1.829 m; ICCE 2010: 1.8 m)",
         "source_id": "S10 Borrero & Nelsen 2003 p.2 (primary; ICCE 2010 S2 repeats it as 1.8 m)", "applies": "the outermost point (offshore face of the V apex block); carried along the reef at constant thickness above the bed (assumption A4)",
         "uncertainty_m": 0.3,
         "note": "The only as-built number found. Thickness = z_ref - seabed(apex) (>= one 1.2 m bag course)."},
        {"id": "A", "mode": "level", "label": "A  Phase I design: top of bag min depth -6 ft MSL (Skelly drawing), level crest",
         "short": "A: design level, -6 ft MSL", "z_msl": z_A, "datum_stated": "MSL", "value_stated": "-6 ft MSL",
         "source_id": "P1/img1 Skelly Engineering drawing, call-outs at both arm tips", "applies": "design minimum depth of the bag tops (not a survey); level crest assumed wherever the stack can reach it",
         "uncertainty_m": 0.15, "note": "The drawing prints the SAME number (6 ft) with the datum label MSL; the paper prints '- 6 ft MLLW' for the as-installed outermost point. A and B differ by exactly MSL - MLLW (0.85 m): one number, two datum labels. Which label is right is not stated anywhere; A is also close to the Phase II crest (-1.76 m MSL)."},
    ]
    not_modelled = [
        {"id": "C", "label": "C  After Phase II (23-24 April 2001, +90 bags placed over Phase I; crest widened and made shallower): 'within 3 ft of MLLW'", "z_msl": z_C, "value_stated": "within 3 ft (0.914 m) of MLLW (ICCE 2010: 1 m; RWR: 0.9 m)",
         "source_id": "S10 Borrero & Nelsen 2003 p.3 (primary); S2; S3", "reason": "later change of the structure (not the as-built Phase I); plan extent after widening not drawn anywhere"},
        {"id": "R7", "label": "Surfline 2008 comment ('8 feet deep at zero tide')", "z_msl": -3.29, "value_stated": "8 ft at zero tide (if zero tide = MLLW)", "source_id": "card R7 (Cloudflare, not re-fetched)",
         "reason": "anonymous comment, datum and date unclear; shown only as the deep bound of the crest-depth range"},
    ]

    def thick_of(c, seabed_f=seabed_fn):
        return max(c["z_ref_msl"] - float(seabed_f(c["y_ref_m"])), MIN_HEIGHT_M)

    def htop_at(c, y, seabed_f=seabed_fn):
        if c["mode"] == "level":
            return max(c["z_msl"] - float(seabed_f(y)), MIN_HEIGHT_M)
        return thick_of(c, seabed_f)

    def vol(c, s, y_shift=0.0, seabed_f=seabed_fn, thick=None):
        X, Y, H, ins, Ht = reef_height_field(poly, seabed_f, c, s, y_shift=y_shift, thick_override=thick)
        return float(H.sum() * CELL * CELL)

    stats = {}
    vol_table = {}
    for c in crest_states:
        if c["mode"] == "thickness":
            c["thickness_m"] = round(thick_of(c), 3)
        vol_table[c["id"]] = {str(s): round(vol(c, s), 0) for s in (0.5, 0.75, 1.0, 1.5, 2.0)}
        X, Y, H, ins, Ht = reef_height_field(poly, seabed_fn, c, SLOPE_RUN_DEFAULT)
        Hi = H[ins]
        plateau = (H >= Ht - 1e-9) & ins
        h_apex, h_tips = htop_at(c, y_apex), htop_at(c, y_tips)
        z_apex, z_tips = at(y_apex) + h_apex, at(y_tips) + h_tips
        stats[c["id"]] = {
            "volume_m3": round(float(H.sum() * CELL * CELL), 0), "h_max_m": round(float(Hi.max()), 2), "h_mean_m": round(float(Hi.mean()), 2),
            "plateau_area_m2": round(float(plateau.sum() * CELL * CELL), 1),
            "crest_h_apex_m": round(h_apex, 2), "crest_h_tips_m": round(h_tips, 2), "top_z_apex_msl_m": round(z_apex, 3), "top_z_tips_msl_m": round(z_tips, 3),
            "top_apex_below_mllw_m": round(-z_apex - msl_mllw, 2), "top_tips_below_mllw_m": round(-z_tips - msl_mllw, 2),
            "top_apex_below_lat_m": round(lev["LAT"] - z_apex, 2), "top_tips_below_lat_m": round(lev["LAT"] - z_tips, 2),
            "courses_apex": round(h_apex / BAG["height_m"], 2),
        }
        c.update(stats[c["id"]])
        if c["mode"] == "level":
            c["depth_below_msl_m"] = round(-c["z_msl"], 3)
            c["depth_below_mllw_m"] = round(-(c["z_msl"] + msl_mllw), 3)
            c["depth_below_lat_m"] = round(lev["LAT"] - c["z_msl"], 3)
        else:
            c["depth_below_msl_m"] = round(-c["z_ref_msl"], 3)
            c["depth_below_mllw_m"] = round(-(c["z_ref_msl"] + msl_mllw), 3)
            c["depth_below_lat_m"] = round(lev["LAT"] - c["z_ref_msl"], 3)
    for c in not_modelled:
        c["depth_below_mllw_m"] = round(-(c["z_msl"] + msl_mllw), 3)
        c["depth_below_lat_m"] = round(lev["LAT"] - c["z_msl"], 3)
    cB, cA = crest_states[0], crest_states[1]

    # ---------------------------------------------------------------- validation numbers
    bag_vol_lo = N_BAGS_PHASE1 * BAG["volume_max_m3"] * BAG["fill_min"]
    bag_vol_hi = N_BAGS_PHASE1 * BAG["volume_max_m3"] * BAG["fill_max"]
    vol_final_bag_lo = N_BAGS_FINAL * BAG["volume_max_m3"] * BAG["fill_min"]
    vol_final_bag_hi = N_BAGS_FINAL * BAG["volume_max_m3"] * BAG["fill_max"]
    # tip check: one bag course on the DEM seabed at the arm tips vs the drawing's "top of bag min depth"
    tip_single_course_top = at(y_tips) + BAG["height_m"]
    tip_diff_A = tip_single_course_top - z_A
    tipB_top = stats["B"]["top_z_tips_msl_m"]
    # sensitivities (state B and A) -> volume uncertainty
    h0 = cB["thickness_m"]
    dV_B_thick = (vol(cB, 1.0, thick=h0 + 0.3) - vol(cB, 1.0, thick=max(h0 - 0.3, MIN_HEIGHT_M))) / 2
    dV_B_y = (vol(cB, 1.0, y_shift=25.0) - vol(cB, 1.0, y_shift=-25.0)) / 2
    dV_B_s = (vol(cB, 0.5) - vol(cB, 2.0)) / 2
    sig_V_B = math.sqrt(dV_B_thick ** 2 + dV_B_y ** 2 + dV_B_s ** 2)
    dV_A_zc = (vol({**cA, "z_msl": cA["z_msl"] + 0.15}, 1.0) - vol({**cA, "z_msl": cA["z_msl"] - 0.15}, 1.0)) / 2
    dV_A_y = (vol(cA, 1.0, y_shift=25.0) - vol(cA, 1.0, y_shift=-25.0)) / 2
    dV_A_s = (vol(cA, 0.5) - vol(cA, 2.0)) / 2
    sig_V_A = math.sqrt(dV_A_zc ** 2 + dV_A_y ** 2 + dV_A_s ** 2)
    vol_nav_B = vol(cB, 1.0, seabed_f=seabed_nav_fn)
    thick_nav_B = thick_of(cB, seabed_nav_fn)
    # sensitivity of reef height to the seabed position (+-25 m along the profile)
    sens = {}
    for dy in (-25, 0, 25, 40):
        zb = at(y_nom + dy)
        sens[str(dy)] = {"seabed_z_m": round(zb, 2), "thickness_B_m": round(max(z_B - at(y_apex + dy), MIN_HEIGHT_M), 2), "crest_height_A_m": round(z_A - zb, 2)}

    # ---------------------------------------------------------------- uncertainty propagation numbers
    sea_estimates = {"NOAA DEM at y = 91.44 m": at(y_nom), "NOAA CRM 1 arc-sec at y = 91.44 m": seabed_checks["crm_z_at_nominal_m"],
                     "CCC 1998 text '15 feet (MSL)'": -15 * 0.3048, "RWR text 'about 5 m deep' (datum not stated)": -5.0}
    sea_estimates["B&N 2003 Fig. 5: beds either side of the reef, Oct 2001 (axis read as MLLW)"] = bed5_mean_msl
    nav_ref = nav.get("reef_centre_if_91m_from_chart_coastline", {}).get("z_msl_assumed_mllw")
    if nav_ref is not None:
        sea_estimates["Navionics SonarChart 91.44 m from the chart coastline (MLLW assumed)"] = nav_ref
    est_vals = np.array(list(sea_estimates.values()), float)
    sd_est = float(est_vals.std(ddof=1))
    slope = 1.0 / seabed_checks["slope_1_in"]
    sig_y = 25.0
    sig_pos = slope * sig_y
    sig_zc = 0.30           # reading of the crest state (assumed; A: +-0.15 m rounding of the drawn foot, B: 'approximately')
    sig_zb = round(max(sd_est, 0.0), 1)
    sig_H = math.sqrt(sig_zc ** 2 + sig_zb ** 2)
    unc = {"sig_zc_m": sig_zc, "sig_zb_m": sig_zb, "sig_H_m": round(sig_H, 2), "sd_estimates_m": round(sd_est, 2), "sig_pos_m": round(sig_pos, 2), "sig_y_m": sig_y,
           "estimates": {k: round(float(v), 2) for k, v in sea_estimates.items()}}

    # ---------------------------------------------------------------- provenance array
    P = []

    def prov(parameter, value, unit, source_id, method, uncertainty, estimated):
        P.append({"parameter": parameter, "value": value, "unit": unit, "source_id": source_id, "method": method,
                  "uncertainty": uncertainty, "estimated": estimated})

    prov("plan outline (toe polygon)", "%d vertices, %.1f m2, %.1f x %.1f m" % (len(poly_xy), can["area_m2"], can["bbox_m"]["alongshore"], can["bbox_m"]["crossshore"]),
         "m", "P1 shape.json (img1 Skelly drawing)", "outline of the solid-outline bags traced on the scaled design drawing (scale bar 0-90 ft), canonical frame of shape.json",
         "+-0.2 m on the outline (+-4 % area); scale bar +-3-5 %", False)
    prov("state modelled", "Phase I as built, Sept 2000: footprint = Skelly design layout (110 solid bags), top = ICCE as-installed depth", "-", "P1 / S2 / VERIFY.md check 2",
         "no as-built plan exists; Phase II (Apr 2001) and the removal (fall 2008 / fall 2010) are in the caption only, not modelled", "design vs real structure differ by metres (bags moved, sank, buried)", False)
    prov("frame orientation", "+x toward 155 deg, +y (offshore) toward 245 deg", "deg", "P1 shape.json angles; img4 shoreline fit; img6 north arrow",
         "present shoreline fitted on Esri 2026-01-09 image (155.5 deg); concept plan bisector 61 deg; SonarChart 0 ft line trend gives 158 deg", "+-5 deg (drawing has no north arrow)", True)
    prov("position (lat/lon)", "%.5f N, %.5f W (inferred hint; not surveyed)" % (L.HINT_LAT, -L.HINT_LON), "deg", "S10 Borrero & Nelsen 2003 Fig. 9 (UTM window) + p.1 text + Fig. 2; Navionics outfall landfall",
         "centre of the Fig. 9 survey window (UTM 11N 367505 E, 3754275 N); agrees to <= 35 m with 'about 200 m south of the 1-mile outfall' (outfall landfall read on the Navionics chart) + 91 m offshore; Fig. 2 scale gives 320 m instead of 200 m; the earlier text hint (CCC 1998: 300 yd north of the Grand Avenue jetty, 33.9188 N 118.4324 W) is 217 m away and superseded",
         "+-100 m alongshore (window half-length 56 m; outfall- and jetty-based estimates span 190 m); no effect on depths (bed uniform alongshore)", True)
    prov("crest B: top of the reef at the offshore face, Phase I as installed (MODELLED, default)", "%.3f (stated %s)" % (z_B, cB["value_stated"]), "m rel. MSL", cB["source_id"],
         "z_MSL = -(6 ft x 0.3048 + (MSL - MLLW)) = -(1.829 + %.3f); carried along the reef at constant thickness %.2f m above the DEM seabed" % (msl_mllw, cB["thickness_m"]),
         "+-%.2f m (reading 'approximately', single point, as-built variation); datum MLLW now confirmed in the primary paper" % cB["uncertainty_m"], False)
    prov("crest A: design minimum depth of the bag tops (MODELLED alternative)", "%.3f (stated %s)" % (z_A, cA["value_stated"]), "m rel. MSL", "P1/img1 call-outs at both arm tips",
         "6 ft x 0.3048 m/ft; datum label MSL as printed (the paper prints the same 6 ft as MLLW); level crest", "+-%.2f m (foot rounding); %.2f m above crest B = MSL - MLLW" % (cA["uncertainty_m"], z_A - z_B), False)
    prov("crest C: after Phase II (NOT modelled)", "%.3f (stated %s)" % (z_C, not_modelled[0]["value_stated"]), "m rel. MSL", not_modelled[0]["source_id"],
         "z_MSL = -(3 ft x 0.3048 + %.3f); Fig. 8 gives the May 2001 crest as %.2f m on its axis (datum not stated) and %.1f m of erosion by Sept 2002" % (msl_mllw, f8["crest"]["May 2001"]["z_m"], f8["crest"]["May 2001"]["z_m"] - f8["crest"]["September 2002"]["z_m"]), "later change: shown for the record only", False)
    prov("reef after Phase II (NOT modelled): centreline relief and width", "relief %.1f m above the beds, base width %.0f m, crest %.1f m from the z = 0 crossing (Oct 2001)" % (d7["relief_above_landward_bed_m"], d7["base_width_m"], d7["peak_from_zero_crossing_m"]), "m",
         "S10 Borrero & Nelsen 2003 Figs 5, 7, 8 (profile along range line 3, vector paths digitised)", "bn_digitise.py: peak minus the lowest vertex landward and seaward of the peak; the design apex block is only 10.6 m wide at the centreline", "+-0.2 m vertical; axis datum not stated (Fig. 7/8 = Fig. 5 + 1.44 m)", False)
    prov("bag size", "4 x 7 x 10 ft = 1.2 x 2.1 x 3.0 m, maximum 280 ft3 = 7.9 m3, filled 80-90 %, about 14 t", "m", "S10 Borrero & Nelsen 2003 p.2 (primary); S2 ICCE 2010 Fig.1 & p.7",
         "stated in the paper; 3.0 x 2.13 x 1.2 m rectangular = 7.67 m3 (3 % below the stated maximum); consistent with the drawing grid pitch 6.9 x 9.5 ft", "+-3 % (bag shape)", False)
    prov("bag counts and dates", "Phase I: 110 bags, installed 22 Sept 2000; Phase II: 90 bags, 23-24 April 2001 (+80 % volume); total 200 bags, 'approximately 1600 m3'", "-", "S10 Borrero & Nelsen 2003 pp.2-3, 16",
         "1600 m3 = 200 x 7.9 m3 (NOMINAL volume, not the 80-90 % filled volume); 90/110 = 0.82 vs '+80 %'", "stated; stack height / number of courses NOT stated", False)
    prov("side slope of the bag stack", "%.1f H : 1 V (range %.1f-%.1f)" % (SLOPE_RUN_DEFAULT, SLOPE_RUN_RANGE[0], SLOPE_RUN_RANGE[1]), "-", "none (assumption A5)",
         "bag edge of a 1.2-1.5 m course; volume sensitivity in METHODS_3D.md section 5", "0.5-2.5", True)
    prov("reef thickness (state B)", "%.2f m = %.2f bag courses (apex), %.2f m at the tips" % (stats["B"]["crest_h_apex_m"], stats["B"]["courses_apex"], stats["B"]["crest_h_tips_m"]), "m", "derived: crest B minus DEM seabed at the apex",
         "thickness = z_B - z_seabed(y_apex), applied as a constant over the reef (top parallel to the bed)", "+-%.1f m (propagation of crest and seabed uncertainty)" % unc["sig_H_m"], True)
    prov("seabed profile (primary)", "z(91.4 m) = %.2f m MSL, slope 1:%.0f over the reef" % (seabed_checks["dem_z_at_nominal_m"], seabed_checks["slope_1_in"]), "m rel. MSL",
         "S5 NOAA NGDC Santa Monica 1/3 arc-sec NAVD88 DEM (2010)", "mean of %d alongshore profiles, each aligned on its MSL waterline; z_MSL = z_NAVD88 - %.3f" % (prof["n"], prof["navd_to_msl"]),
         "+-%.1f m (SD of %d independent depth estimates %.2f m; position +-25 m x slope = %.2f m; alongshore sd %.2f m)" % (unc["sig_zb_m"], len(est_vals), sd_est, sig_pos, seabed_checks["dem_sd_at_nominal_m"]), False)
    prov("seabed profile (independent check, selectable in the viewer)", "z(hint) = %.2f m MSL (%.1f ft below chart datum); DEM %.2f m" % (nav["hint_z_msl_assumed_mllw"], nav["hint_depth_ft"], nav["dem_z_msl_at_hint"]), "m rel. MSL",
         "S7 Garmin Navionics SonarChart (Marine Maps web viewer), accessed 2026-10-05", "%d 1 ft contours counted along 245 deg through the hint (nav_annotate.py); chart datum assumed MLLW: z_MSL = -(n x 0.3048) - %.3f; seabed only (reef removed)" % (len(nav_s), msl_mllw),
         "+-0.3 m in the reef zone (mean diff to DEM %+.2f m, max %.2f m); datum assumed; +-1 ft counting error" % (nav["profile"]["stat_reef_zone_-17_to_12"]["mean_diff_m"], nav["profile"]["stat_reef_zone_-17_to_12"]["max_abs_diff_m"]), True)
    prov("reef distance from the MSL waterline", "%.2f m (centroid)" % y_nom, "m", "P1 (text: 100 yd offshore, CCC E-98-15 p.11; Wikipedia; RWR 'roughly 100 meters')",
         "text value; the waterline is the MSL contour of the DEM; hint-based position gives %.1f m; B&N 2003 Fig. 5 (axis read as MLLW, MSL = +0.849 m) puts the Oct 2001 crest %.1f m and the centre of the base %.1f m from the MSL line (Fig. 7 axis read as MSL: %.1f / %.1f m)" % (y_hint, d5["peak_distance_m"] - d5["plus_0p849_crossing_distance_m"], 0.5 * (d5["bed_landward"][0] + d5["bed_seaward"][0]) - d5["plus_0p849_crossing_distance_m"], d7["peak_from_zero_crossing_m"], d7["base_midpoint_from_zero_crossing_m"]), "+-25 m (-> +-%.1f m seabed depth)" % sig_pos, True)
    prov("shoreline", "y = 0 at the MSL waterline", "m", "S5 DEM", "z_MSL = 0 contour of the seabed profile; beach face 1:10 to 1:30", "+-10 m (alongshore sd of waterline %.1f m, seasonal berm changes; the Navionics 0 ft line lies 40 m seaward of the DEM's MLLW line)" % seabed_checks["waterline_offset_sd_m"], False)
    for k in LEVELS_ORDER:
        prov("tidal datum " + k, "%+.3f" % lev[k], "m rel. MSL", "S4 NOAA CO-OPS 9410840 (epoch %s)" % ds["_epoch"], "station-datum value minus MSL (1.594 m)",
             "+-0.03 m transfer to El Segundo (12.5 km); LA Outer Harbor MSL-MLLW differs by %.3f m" % abs(msl_mllw_la - msl_mllw), False)
    prov("north direction", "(-0.906, -0.423) in (x, y)", "-", "P1 frame", "bearing 0 deg = x-bearing 155 deg rotated by -155 deg", "+-5 deg", True)

    sources = [
        {"id": "P1", "citation": "shape.json of this reef (07_scale/shapes/prattes-reef-el-segundo/shape.json), traced on img1 = Skelly Engineering (c. 2000) plan drawing 'PRATTE'S REEF' via Raised Water Research; verified 2026-10-04", "url": "https://raisedwaterresearch.com/wp-content/uploads/2019/07/Pratts-Reef-Diagram.png"},
        {"id": "S1", "citation": "California Coastal Commission (1998). Staff report W5a, application E-98-15 (Surfrider Foundation - Pratte's Reef), hearing 13 Oct 1998; Exhibits 2 and 3 by Skelly Engineering (1997, 1996)", "url": "https://documents.coastal.ca.gov/reports/1998/10/W5a-10-1998.pdf"},
        {"id": "S2", "citation": "Borrero, J.C., Mead, S.T. & Moores, A. (2010). Stability considerations and case studies of submerged structures constructed from large, sand filled, geotextile containers. Coastal Engineering Proceedings 1(32), structures.60", "url": "https://doi.org/10.9753/icce.v32.structures.60"},
        {"id": "S3", "citation": "Raised Water Research (n.d.). Pratte's Reef. accessed 2026-10-05", "url": "https://raisedwaterresearch.com/spot/artificial-reef/us/california/prattes-reef/"},
        {"id": "S4", "citation": "NOAA CO-OPS (2026). Tidal datums, station 9410840 Santa Monica, CA, epoch 1983-2001 (cross-check 9410660 Los Angeles)", "url": "https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/9410840/datums.json?units=metric"},
        {"id": "S5", "citation": "NOAA National Geophysical Data Center (2010). Santa Monica, California 1/3 arc-second NAVD 88 Coastal Digital Elevation Model", "url": "https://www.ngdc.noaa.gov/metaview/page?xml=NOAA/NESDIS/NGDC/MGG/DEM/iso/xml/726.xml&view=getDataView&header=none"},
        {"id": "S6", "citation": "NOAA National Geophysical Data Center (2012/2013). U.S. Coastal Relief Model - Southern California v2 (1 arc-second), doi:10.7289/V5V985ZM", "url": "https://www.ngdc.noaa.gov/metaview/page?xml=NOAA/NESDIS/NGDC/MGG/DEM/iso/xml/4970.xml&view=getDataView&header=none"},
        {"id": "S7", "citation": "Garmin Navionics (2026). Marine Maps web viewer (SonarChart Maps and Nautical Charts layers), reached via webapp.navionics.com; accessed 2026-10-05; screenshots private research copies, not for navigation", "url": "https://maps.garmin.com/en-US/marine/"},
        {"id": "S8", "citation": "NOAA CO-OPS (2026). Tidal datums, station 9410660 Los Angeles Outer Harbor, CA, epoch 1983-2001 (cross-check of MSL-MLLW)", "url": "https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/9410660/datums.json?units=metric"},
        {"id": "S10", "citation": "Borrero, J.C. & Nelsen, C. (2003). Results of a comprehensive monitoring program at Pratte's Reef. In: Black, K. & Mead, S. (eds), Proceedings of the 3rd International Surfing Reef Symposium, Raglan, New Zealand (venue and year as cited in R23; the 16-page PDF supplied by Lior on 2026-10-05 prints neither). Private research copy.", "url": "src/borrero_nelsen_2003_prattes_monitoring_results.pdf (local copy; original URL unknown)"},
        {"id": "S9", "citation": "Reef card 02_research/reefs/prattes-reef-el-segundo.json (verified 2026-09-25): removal dates (Phase I removal 30 Sept-17 Oct 2008, remaining bags fall 2010) from Surfrider Foundation news, Coastal Frontiers Corp. case study and Surfline (2008); not re-fetched in this run", "url": "https://www.coastalfrontiers.com/removal-of-prattes-reef"},
    ]

    conf = {"level": "low",
            "reason": ("Every input has a source, and the 2003 monitoring paper now confirms the datum of the as-installed crest (about 6 ft below MLLW), the bag size, the dates and, through a georeferenced survey window, the position to about +-100 m; "
                       "the tide datums and the seabed (NOAA DEM and Navionics agree within 0.3 m in the reef zone) are well supported. But there is still no as-built plan (the paper's Fig. 4 is the design layout), "
                       "the stack height is not stated and the single-course model holds only %d m3 against %d-%d m3 for 110 bags, the Phase I crest is one point that differs by %.1f m from the design reading, "
                       "and the vertical uncertainty (+-%.2f m) is more than half the reef height (%.1f m)." % (round(stats["B"]["volume_m3"]), round(bag_vol_lo), round(bag_vol_hi), abs(z_A - z_B), unc["sig_H_m"], stats["B"]["crest_h_apex_m"])),
            "reason_short": "LOW: all inputs sourced and the 2003 paper fixes datum, bag size, dates and position (+-100 m), but no as-built plan, stack height unknown (volume gap %d-%d m3), crest readings differ by %.1f m; vertical error (+-%.2f m) is over half the %.1f m reef height." % (
                round(bag_vol_lo - stats["B"]["volume_m3"]), round(bag_vol_hi * 1.0 - stats["B"]["volume_m3"] + 0), abs(z_A - z_B), unc["sig_H_m"], stats["B"]["crest_h_apex_m"])}
    inputs_status = {
        "plan": "sourced - verified outline of the Phase I design layout (435.2 m2, 58.0 x 28.6 m); the 2003 paper's Fig. 4 is the same design drawing, so no as-built plan exists",
        "crest": "sourced - Phase I outermost point approximately 6 ft below MLLW (Borrero & Nelsen 2003 p.2; datum MLLW now confirmed) = %.2f m MSL, default; Skelly design minimum -6 ft MSL = %.2f m MSL (same number, other datum label) as alternative; variation along the crest assumed" % (z_B, z_A),
        "height_slopes": "estimated - bag size 4 x 7 x 10 ft now primary; number of courses NOT stated by any source; one course (thickness %.2f m from crest B minus the DEM seabed) assumed; side slope 1H:1V assumed; the 110-bag volume check fails (%d vs %d-%d m3)" % (h0, round(stats["B"]["volume_m3"]), round(bag_vol_lo), round(bag_vol_hi)),
        "seabed": "sourced - NOAA 1/3 arc-sec DEM (primary), Navionics SonarChart (check) and the 2003 paper's profiles (beds beside the reef %.2f m MSL if the axis is MLLW): DEM %.2f vs Navionics %.2f m MSL at the hint; reef distance +-25 m -> +-%.1f m" % (bed5_mean_msl, nav["dem_z_msl_at_hint"], nav["hint_z_msl_assumed_mllw"], sig_pos),
        "position": "inferred - Borrero & Nelsen (2003) Fig. 9 survey window centre %.5f N, %.5f W, consistent with '200 m south of the 1-mile outfall'; +-100 m; not surveyed, no georeferenced outline" % (L.HINT_LAT, -L.HINT_LON),
        "tides": "sourced - NOAA CO-OPS 9410840 Santa Monica (cross-check 9410660); MSL-MLLW = %.3f m" % msl_mllw,
    }
    lifecycle = [
        {"date": "1996-1998", "event": "concept of about 30 large bags (150 ft wings); CCC permit E-98-15 heard 13 Oct 1998", "source": "S1"},
        {"date": "22 Sept 2000", "event": "Phase I installed: 110 sand-filled geotextile bags (4 x 7 x 10 ft, 7.9 m3 max each, 80-90 % filled, about 14 t) filled at the Port of Los Angeles and placed by barge crane in a V with the apex offshore; outermost point approximately 6 ft below MLLW. THE STATE MODELLED HERE", "source": "S10 p.2"},
        {"date": "Oct 2000", "event": "first bathymetric survey (Fig. 9 contours, georeferenced); November 2000 profile taken before any significant swell", "source": "S10"},
        {"date": "winter 2000-01", "event": "Phase I bags largely covered by sand that moved offshore", "source": "S10 p.3"},
        {"date": "23-24 Apr 2001", "event": "Phase II: 90 more bags placed directly over Phase I, volume +80 %, crest widened and made shallower to within 3 ft of MLLW (NOT modelled)", "source": "S10 p.3"},
        {"date": "May 2001 - Sept 2002", "event": "crest of the widened reef eroded by about 1.5 m (Fig. 8); by Oct 2002 the bags were mostly level with the sand", "source": "S10 Fig. 8, p.16"},
        {"date": "Aug 2002", "event": "dive survey: several bags ripped and losing fill (polypropylene black bags worse than polyester white bags)", "source": "S10 p.8-9; S2"},
        {"date": "fall 2008", "event": "removal begun (30 Sept-17 Oct 2008): mostly buried remnants", "source": "S2, S9"},
        {"date": "fall 2010", "event": "removal completed (end of the 10-year permit); first removal of a purpose-built surfing reef", "source": "S9"},
    ]
    caption = ("Pratte's Reef (permit name Chevron Reef), El Segundo / Dockweiler Beach, California. MODELLED: Phase I as built (22 Sept 2000) - footprint = Skelly Engineering design layout of 110 bags "
               "(no as-built plan exists; the 2003 monitoring paper reprints the same design drawing), top at the as-installed depth of about 6 ft below MLLW. NOT MODELLED: Phase II (23-24 April 2001, +90 bags, crest widened and raised, "
               "eroded again by 2002) and the removal (fall 2008 and fall 2010). Seabed = NOAA DEM, checked against Navionics and the paper's profiles. Position inferred from the paper's survey window (+-100 m).")

    model = {
        "slug": "prattes-reef-el-segundo", "name": "Pratte's Reef (permit name: Chevron Reef), El Segundo / Dockweiler Beach, California",
        "generated": TODAY, "caption": caption, "lifecycle": lifecycle,
        "state_label": "Phase I as built (22 Sept 2000): footprint = Skelly Engineering design layout (110 solid-outline bags; no as-built plan exists), top = as-installed depth of about 6 ft below MLLW (Borrero & Nelsen 2003); Phase II and the removal are not modelled",
        "frame": {"units": "m", "x": "alongshore toward 155 deg (SSE)", "y": "offshore toward 245 deg (WSW) = x turned 90 deg clockwise", "z": "up, 0 = MSL (NOAA 9410840, epoch 1983-2001)",
                  "x_bearing_deg": x_bearing, "y_bearing_deg": y_bearing,
                  "north_xy": [round(math.cos(math.radians(-x_bearing)), 4), round(math.sin(math.radians(-x_bearing)), 4)],
                  "handedness_note": "(x, y, z-up) is left-handed (y = x turned CLOCKWISE); the viewer maps model (x, y, z) to three.js (X = x, Y = z, Z = y), which is mirror-free"},
        "plan": plan,
        "seabed": seabed,
        "reef": {"toe_polygon_xy_m": plan["polygon_xy_m"], "states": crest_states, "not_modelled": not_modelled, "default_state": "B",
                 "bag": BAG, "slope_run_default": SLOPE_RUN_DEFAULT, "slope_run_range": SLOPE_RUN_RANGE, "min_height_m": MIN_HEIGHT_M,
                 "y_apex_m": round(y_apex, 2), "y_tips_m": round(y_tips, 2),
                 "rule": "h(x,y) = max(0, min(h_top, d_in(x,y) / slope_run)); h_top = z_c - z_seabed(y) (state A, level crest) or z_ref - z_seabed(y_apex) (state B, constant thickness); both >= min_height; d_in = distance inside the toe outline; surface z = z_seabed + h",
                 "offshore_presets": [{"label": "text: 100 yd from the waterline", "y": y_nom}, {"label": "hint %.5f N, %.5f W" % (L.HINT_LAT, -L.HINT_LON), "y": y_hint}, {"label": "CCC '15 ft (MSL)' depth", "y": seabed_checks["y_at_15ft_m"]}],
                 "volume_check": {"model_volume_by_state_slope_m3": vol_table, "bags_110_80_90pct_m3": [round(bag_vol_lo), round(bag_vol_hi)], "bags_110_max_m3": round(110 * 7.9),
                                  "bags_200_80_90pct_m3": [round(vol_final_bag_lo), round(vol_final_bag_hi)], "stated_final_volume_m3": [1400, 1600]},
                 "sensitivity_seabed_position": sens, "uncertainty": unc},
        "water": {"levels": water_levels, "default": "MSL", "datum_note": "z in m above MSL; MSL - MLLW = %.3f m (LA Outer Harbor %.3f)" % (msl_mllw, msl_mllw_la)},
        "shoreline": {"y_m": 0.0, "definition": "MSL waterline (z = 0 contour of the seabed profile)"},
        "north": {"xy": [round(math.cos(math.radians(-x_bearing)), 4), round(math.sin(math.radians(-x_bearing)), 4)], "bearing_deg": 0},
        "position_hint": {"lat": L.HINT_LAT, "lon": L.HINT_LON, "uncertainty_m": 100, "utm11n": [367505.0, 3754275.0],
                          "note": "inferred: centre of the Borrero & Nelsen (2003) Fig. 9 survey window, consistent with 'about 200 m south of the 1-mile outfall'; shape.json geo = null (no georeferenced outline)",
                          "superseded_text_hint": {"lat": L.OLD_HINT_LAT, "lon": L.OLD_HINT_LON, "basis": "CCC 1998: 300 yd north of the Grand Avenue jetty, 100 yd offshore", "distance_to_new_hint_m": 217}},
        "provenance": P, "sources": sources, "confidence_3d": conf, "inputs_status": inputs_status,
        "stats": stats,
    }

    # ---------------------------------------------------------------- write model.js
    with open(os.path.join(HERE, "model.js"), "w", encoding="utf-8") as f:
        f.write("// generated by build_3d.py on %s - do not edit by hand\nwindow.REEF_MODEL = " % TODAY)
        json.dump(model, f, indent=1)
        f.write(";\n")

    # ---------------------------------------------------------------- computed.json + METHODS_3D.md from template
    def f2(v, d=2):
        return ("%." + str(d) + "f") % v

    comp = {
        "plan_status": plan["status"], "plan_verified_on": plan["verified_on"], "plan_md5": plan["shape_json_md5"], "plan_mtime": plan["shape_json_mtime"],
        "area_m2": can["area_m2"], "bbox_alongshore": can["bbox_m"]["alongshore"], "bbox_crossshore": can["bbox_m"]["crossshore"], "n_vertices": len(poly_xy),
        "y_min": plan["y_range_m"][0], "y_max": plan["y_range_m"][1], "y_nom": y_nom, "confidence_plan": plan["confidence_plan"], "y_hint": y_hint,
        "msl_mllw": msl_mllw, "msl_mllw_la": msl_mllw_la, "msl_mllw_diff": round(abs(msl_mllw - msl_mllw_la), 3),
        "navd88_to_msl": seabed_checks["navd88_to_msl_m"],
        "lat": lev["LAT"], "hat": lev["HAT"], "mhhw": lev["MHHW"], "mllw": lev["MLLW"], "mhw": lev["MHW"], "mlw": lev["MLW"],
        "tidal_range_mhhw_mllw": round(lev["MHHW"] - lev["MLLW"], 3),
        "z_dem_nom": seabed_checks["dem_z_at_nominal_m"], "sd_dem_nom": seabed_checks["dem_sd_at_nominal_m"],
        "z_dem_tips": seabed_checks["dem_z_at_tips_m"], "z_dem_apex": seabed_checks["dem_z_at_apex_m"], "z_crm_nom": seabed_checks["crm_z_at_nominal_m"],
        "dem_crm_diff": round(seabed_checks["dem_z_at_nominal_m"] - seabed_checks["crm_z_at_nominal_m"], 2),
        "y_15ft": seabed_checks["y_at_15ft_m"], "slope_1_in": seabed_checks["slope_1_in"], "n_stations": prof["n"],
        "wl_mean": seabed_checks["waterline_offset_mean_m"], "wl_sd": seabed_checks["waterline_offset_sd_m"],
        "zA": z_A, "zB": z_B, "zC": z_C, "zAB_diff": round(z_A - z_B, 3),
        "zA_mllw": round(z_A + msl_mllw, 3), "zB_mllw": round(z_B + msl_mllw, 3), "zC_mllw": round(z_C + msl_mllw, 3),
        "zA_lat": round(lev["LAT"] - z_A, 3), "zB_lat": round(lev["LAT"] - z_B, 3), "zC_lat": round(lev["LAT"] - z_C, 3),
        "zA_mllw_la": round(-z_A - msl_mllw_la, 3),
        "thickB": cB["thickness_m"], "coursesB": f2(cB["thickness_m"] / BAG["height_m"]),
        "hB_apex": stats["B"]["crest_h_apex_m"], "hB_tips": stats["B"]["crest_h_tips_m"], "hB_max": stats["B"]["h_max_m"], "hB_mean": stats["B"]["h_mean_m"],
        "topB_apex": stats["B"]["top_z_apex_msl_m"], "topB_tips": stats["B"]["top_z_tips_msl_m"],
        "topB_apex_mllw": stats["B"]["top_apex_below_mllw_m"], "topB_tips_mllw": stats["B"]["top_tips_below_mllw_m"],
        "topB_apex_lat": stats["B"]["top_apex_below_lat_m"], "topB_tips_lat": stats["B"]["top_tips_below_lat_m"],
        "hA_apex": stats["A"]["crest_h_apex_m"], "hA_tips": stats["A"]["crest_h_tips_m"], "hA_max": stats["A"]["h_max_m"], "hA_mean": stats["A"]["h_mean_m"],
        "topA_apex_lat": stats["A"]["top_apex_below_lat_m"], "coursesA_apex": stats["A"]["courses_apex"],
        "volA": int(stats["A"]["volume_m3"]), "volB": int(stats["B"]["volume_m3"]), "plateauA": stats["A"]["plateau_area_m2"], "plateauB": stats["B"]["plateau_area_m2"],
        "vol_bag_lo": round(bag_vol_lo), "vol_bag_hi": round(bag_vol_hi), "vol_bag_max": round(110 * 7.9),
        "vol_final_lo": round(vol_final_bag_lo), "vol_final_hi": round(vol_final_bag_hi),
        "ratioB_lo": f2(stats["B"]["volume_m3"] / bag_vol_hi), "ratioB_hi": f2(stats["B"]["volume_m3"] / bag_vol_lo),
        "ratioA_lo": f2(stats["A"]["volume_m3"] / bag_vol_hi), "ratioA_hi": f2(stats["A"]["volume_m3"] / bag_vol_lo),
        "missing_vol_lo": round(bag_vol_lo - stats["B"]["volume_m3"]), "missing_vol_hi": round(bag_vol_hi - stats["B"]["volume_m3"]),
        "missing_bags_lo": round((bag_vol_lo - stats["B"]["volume_m3"]) / (BAG["volume_max_m3"] * 0.85)), "missing_bags_hi": round((bag_vol_hi - stats["B"]["volume_m3"]) / (BAG["volume_max_m3"] * 0.85)),
        "bag_foot_m2": f2(BAG["length_m"] * BAG["width_m"]), "bag_foot_total_m2": round(110 * BAG["length_m"] * BAG["width_m"]), "bag_rect_vol": f2(BAG["length_m"] * BAG["width_m"] * BAG["height_m"]),
        "bag_rect_vs_stated_pct": f2(100 * (BAG["length_m"] * BAG["width_m"] * BAG["height_m"] / BAG["volume_max_m3"] - 1), 1),
        "bag_ratio_phase2": f2(90 / 110), "bag_mean_courses": f2(110 * BAG["length_m"] * BAG["width_m"] / can["area_m2"]),
        "tip_single_course_top": round(tip_single_course_top, 2), "tip_diff_A": round(tip_diff_A, 2), "tipB_top": tipB_top, "tipB_diff_A": round(tipB_top - z_A, 2),
        "sig_zc": sig_zc, "sig_zb": sig_zb, "sig_H": unc["sig_H_m"], "sd_est": f2(sd_est), "sig_pos": f2(sig_pos), "sig_y": sig_y, "slope_inv": f2(1 / slope, 1),
        "sig_V_B": round(sig_V_B), "dV_B_thick": round(dV_B_thick), "dV_B_y": round(dV_B_y), "dV_B_s": round(dV_B_s),
        "sig_V_A": round(sig_V_A), "dV_A_zc": round(dV_A_zc), "dV_A_y": round(dV_A_y), "dV_A_s": round(dV_A_s),
        "vol_nav_B": int(round(vol_nav_B)), "thick_nav_B": f2(thick_nav_B),
        "sig_D_lat_B": f2(math.sqrt(sig_zc ** 2 + 0.05 ** 2)), "sig_D_lat_A": f2(math.sqrt(0.15 ** 2 + 0.05 ** 2)),
        "ve5_apex": f2(5 * stats["B"]["crest_h_apex_m"], 1), "ve5_slope_inv": f2(seabed_checks["slope_1_in"] / 5, 1),
        "est_table_md": "\n".join(["| estimate of the seabed depth at the nominal reef position | z (m MSL) |", "|---|---|"] + ["| %s | %.2f |" % (k, v) for k, v in sea_estimates.items()]),
        "vol_table_md": "\n".join(
            ["| state | s = 0.5 | 0.75 | **1.0** | 1.5 | 2.0 |", "|---|---|---|---|---|---|"] +
            ["| %s | %s |" % (k, " | ".join("%d" % vol_table[k][str(s)] for s in (0.5, 0.75, 1.0, 1.5, 2.0))) for k in "BA"]),
        "sens_md": "\n".join(["| reef moved by (m) | seabed z under the centre (m MSL) | thickness state B (m) | crest height state A (m) |", "|---|---|---|---|"] +
                             ["| %+d | %.2f | %.2f | %.2f |" % (int(k), v["seabed_z_m"], v["thickness_B_m"], v["crest_height_A_m"]) for k, v in sens.items()]),
        # Navionics
        "nav_n": len(nav_s), "nav_hint_ft": nav["hint_depth_ft"], "nav_hint_m": f2(nav["hint_depth_ft"] * 0.3048), "nav_hint_z": nav["hint_z_msl_assumed_mllw"], "dem_hint_z": nav["dem_z_msl_at_hint"],
        "nav_green_end": nav["green_end_m"], "nav_coast": nav["chart_coastline_s_m"], "nav_last_s": nav["crossings_s_m"][-1],
        "nav_anchor_off": abs(nav["nautical_anchor"]["offset_m"]), "nav_anchor_x": nav["nautical_anchor"]["x_m"], "nav_anchor_s": nav["nautical_anchor"]["s_m"], "nav_s15": nav["nautical_anchor"]["sonar_crossing_15_s_m"],
        "nav_rms_mllw": nav["datum_test"]["MLLW"]["rms_m"], "nav_rms_navd": nav["datum_test"]["NAVD88"]["rms_m"], "nav_rms_lat": nav["datum_test"]["LAT"]["rms_m"], "nav_rms_msl": nav["datum_test"]["MSL"]["rms_m"],
        "nav_bias_mllw": nav["datum_test"]["MLLW"]["bias_nav_minus_dem_m"], "nav_npts": nav["datum_test"]["MLLW"]["n_points"],
        "nav_d_reef": "%+.2f" % nav["profile"]["stat_reef_zone_-17_to_12"]["mean_diff_m"], "nav_d_reef_abs": "%.2f" % abs(nav["profile"]["stat_reef_zone_-17_to_12"]["mean_diff_m"]),
        "nav_dmax_reef": "%.2f" % nav["profile"]["stat_reef_zone_-17_to_12"]["max_abs_diff_m"],
        "nav_d_0_40": "%+.2f" % nav["profile"]["stat_s_0_to_40"]["mean_diff_m"], "nav_d_surf": "%+.2f" % nav["profile"]["stat_surf_zone_-50_to_-17"]["mean_diff_m"],
        "nav_dmax_surf": "%.2f" % nav["profile"]["stat_surf_zone_-50_to_-17"]["max_abs_diff_m"],
        "nav_d_40_150": "%+.2f" % nav["profile"]["stat_s_40_to_150"]["mean_diff_m"], "nav_d_far": "%+.2f" % nav["profile"]["stat_s_150_to_260"]["mean_diff_m"],
        "nav_green_end_abs": abs(nav["green_end_m"]), "nav_coast_abs": abs(nav["chart_coastline_s_m"]), "nav_y0": round(float(nav_y[0]), 1),
        "water_apex_lat": f2(stats["B"]["top_apex_below_lat_m"]),
        "water_apex_hat": f2(lev["HAT"] - stats["B"]["top_z_apex_msl_m"]), "water_tips_lat": f2(stats["B"]["top_tips_below_lat_m"]), "water_tips_hat": f2(lev["HAT"] - stats["B"]["top_z_tips_msl_m"]),
        "range_mhhw_lat": f2(lev["MHHW"] - lev["LAT"]), "lvlB_tips_h": f2(z_B - at(y_tips)),
        "nav_al_mean": nav["alongshore_summary"]["depth_ft_at_s0_mean"], "nav_al_sd": nav["alongshore_summary"]["sd_ft"], "nav_al_sd_m": nav["alongshore_summary"]["sd_m"],
        "nav_al_min": nav["alongshore_summary"]["min_ft"], "nav_al_max": nav["alongshore_summary"]["max_ft"],
        "nav_reef_ft": nav["reef_centre_if_91m_from_chart_coastline"]["depth_ft"], "nav_reef_z": nav["reef_centre_if_91m_from_chart_coastline"]["z_msl_assumed_mllw"],
        "nav_m_per_px": round(nav["m_per_px"], 4),
        # ---- Borrero & Nelsen (2003)
        "hint_lat": "%.5f" % L.HINT_LAT, "hint_lon": "%.5f" % -L.HINT_LON, "old_hint_lat": "%.4f" % L.OLD_HINT_LAT, "old_hint_lon": "%.4f" % -L.OLD_HINT_LON,
        "bn_zB_mllw_ft": 6, "bn_zC_ft": 3, "zB_icce": round(-1.8 - msl_mllw, 3), "zB_diff_icce": round(z_B - (-1.8 - msl_mllw), 3),
        "bn_peak5": d5["peak_z_m"], "bn_peak7": d7["peak_z_m"], "bn_peak_d7": d7["peak_distance_m"], "bn_peak_d5": d5["peak_distance_m"],
        "bn_relief": d7["relief_above_landward_bed_m"], "bn_relief_sea": d7["relief_above_seaward_bed_m"], "bn_base_w": d7["base_width_m"],
        "bn_bed5_land": d5["bed_landward"][1], "bn_bed5_sea": d5["bed_seaward"][1], "bn_bed5_land_msl": round(bed5_msl[0], 2), "bn_bed5_sea_msl": round(bed5_msl[1], 2), "bn_bed5_mean_msl": round(bed5_mean_msl, 2),
        "bn_bed7_land": d7["bed_landward"][1], "bn_bed7_sea": d7["bed_seaward"][1],
        "bn_zero7": d7["zero_crossing_distance_m"], "bn_peak_from_zero7": d7["peak_from_zero_crossing_m"], "bn_mid_from_zero7": d7["base_midpoint_from_zero_crossing_m"],
        "bn_msl5": d5["plus_0p849_crossing_distance_m"], "bn_peak_from_msl5": round(d5["peak_distance_m"] - d5["plus_0p849_crossing_distance_m"], 1),
        "bn_mid_from_msl5": round(0.5 * (d5["bed_landward"][0] + d5["bed_seaward"][0]) - d5["plus_0p849_crossing_distance_m"], 1),
        "bn_offset57": dig["offset_fig5_minus_fig7_m"], "bn_maxhigh5": dig["fig5"]["tide_lines_z_m"]["max_high_tide_z"],
        "bn_may01": f8["crest"]["May 2001"]["z_m"], "bn_oct01": f8["crest"]["October 2001"]["z_m"], "bn_feb02": f8["crest"]["February 2002"]["z_m"], "bn_sep02": f8["crest"]["September 2002"]["z_m"],
        "bn_erosion": round(f8["crest"]["May 2001"]["z_m"] - f8["crest"]["September 2002"]["z_m"], 2), "bn_may01_5": round(f8["crest"]["May 2001"]["z_m"] + dig["offset_fig5_minus_fig7_m"], 2),
        "bn_may01_mllw_if_msl": round(f8["crest"]["May 2001"]["z_m"] + msl_mllw, 2), "bn_3ft_m": round(3 * 0.3048, 3),
        "vol_bag_nom": round(N_BAGS_PHASE1 * BAG["volume_max_m3"]), "vol_total_nom": round(N_BAGS_FINAL * BAG["volume_max_m3"]),
        "ratioB_nom": f2(stats["B"]["volume_m3"] / (N_BAGS_PHASE1 * BAG["volume_max_m3"])), "ratioA_nom": f2(stats["A"]["volume_m3"] / (N_BAGS_PHASE1 * BAG["volume_max_m3"])),
        "missing_nom": round(N_BAGS_PHASE1 * BAG["volume_max_m3"] - stats["B"]["volume_m3"]),
        "dist_hint_old_m": 217, "sig_x": 100, "volB_p1": round(stats["B"]["volume_m3"] + sig_V_B), "volB_p2": round(stats["B"]["volume_m3"] + 2 * sig_V_B), "volB_p3": round(stats["B"]["volume_m3"] + 3 * sig_V_B),
        "nav_label_n": nav["label_check"]["n"], "nav_label_match": nav["label_check"]["n_match"],
        "nav_lab_n_all": nav["label_datum_test"]["n"], "nav_lab_n_reef": nav["label_datum_test"]["zones"]["reef_zone"]["n"],
        "nav_lab_surf_mllw": nav["label_datum_test"]["zones"]["surf_zone_lt_8ft"]["datums"]["MLLW"]["bias_nav_minus_dem_m"],
        "nav_lab_off_mllw": nav["label_datum_test"]["zones"]["offshore_gt_18ft"]["datums"]["MLLW"]["bias_nav_minus_dem_m"],
        "nav_lab_all_mllw": nav["label_datum_test"]["zones"]["all"]["datums"]["MLLW"]["bias_nav_minus_dem_m"],
        "nav_bias_navd": nav["datum_test"]["NAVD88"]["bias_nav_minus_dem_m"], "nav_bias_lat": nav["datum_test"]["LAT"]["bias_nav_minus_dem_m"], "nav_bias_msl": nav["datum_test"]["MSL"]["bias_nav_minus_dem_m"],
        "fig9_off_oct": dig["fig9_vs_dem"]["October 2000"]["mean_offset_m"], "fig9_off_mar": dig["fig9_vs_dem"]["March 2001"]["mean_offset_m"], "fig9_bearing": dig["fig9_vs_dem"]["contour_bearing"]["true_deg"], "fig9_bearing_sd": dig["fig9_vs_dem"]["contour_bearing"]["sd_deg"], "y15_diff": round(seabed_checks["y_at_15ft_m"] - y_nom, 1), "fig9_win_e": "%d-%d" % tuple(dig["fig9"]["window_E"]), "fig9_win_n": "%d-%d" % tuple(dig["fig9"]["window_N"]),
        "build_date": TODAY,
    }
    json.dump(comp, open(os.path.join(HERE, "computed.json"), "w", encoding="utf-8"), indent=1)
    tpl_path = os.path.join(HERE, "METHODS_3D.template.md")
    methods = open(tpl_path, encoding="utf-8").read()

    def sub(m):
        k = m.group(1)
        if k not in comp:
            raise KeyError("placeholder {{%s}} not computed" % k)
        return str(comp[k])

    methods = re.sub(r"\{\{(\w+)\}\}", sub, methods)
    open(os.path.join(HERE, "METHODS_3D.md"), "w", encoding="utf-8").write(methods)

    # ---------------------------------------------------------------- auto block in SOURCES_3D.md
    sp = os.path.join(HERE, "SOURCES_3D.md")
    src = open(sp, encoding="utf-8").read()
    block = ("<!-- BUILD-AUTO-START -->\n## Plan shape at build time (written by build_3d.py on %s)\n"
             "- shape.json status = **%s**, verified_on = %s, updated = %s, plan confidence = %s; file md5 %s, modified %s.\n"
             "- Outline used: %d vertices, area %.1f m2, bbox %.1f x %.1f m (alongshore x cross-shore), y from %.1f to %.1f m, centroid distance offshore %.2f m. geo = %s.\n"
             "- Drawn state: %s\n<!-- BUILD-AUTO-END -->" % (
                 TODAY, plan["status"], plan["verified_on"], plan["shape_json_updated"], plan["confidence_plan"], plan["shape_json_md5"], plan["shape_json_mtime"],
                 len(poly_xy), can["area_m2"], can["bbox_m"]["alongshore"], can["bbox_m"]["crossshore"], plan["y_range_m"][0], plan["y_range_m"][1], y_nom,
                 "null" if plan["geo"] is None else "set", plan["drawn"]))
    if "<!-- BUILD-AUTO-START -->" in src:
        src = re.sub(r"<!-- BUILD-AUTO-START -->.*?<!-- BUILD-AUTO-END -->", lambda m: block, src, flags=re.S)
    else:
        src = src.rstrip() + "\n\n" + block + "\n"
    open(sp, "w", encoding="utf-8").write(src)

    # ---------------------------------------------------------------- docs.js (methods + sources markdown for the viewer)
    req_path = os.path.join(HERE, "REQUESTS_FOR_LIOR.md")
    docs = {"methods_md": methods, "sources_md": src, "requests_md": open(req_path, encoding="utf-8").read() if os.path.exists(req_path) else "", "built": TODAY,
            "annotated": sorted(f for f in os.listdir(os.path.join(HERE, "annotated")) if f.lower().endswith(".png")) if os.path.isdir(os.path.join(HERE, "annotated")) else []}
    with open(os.path.join(HERE, "docs.js"), "w", encoding="utf-8") as f:
        f.write("// generated by build_3d.py on %s - do not edit by hand\nwindow.REEF_DOCS = " % TODAY)
        json.dump(docs, f, indent=1)
        f.write(";\n")
    print("built: model.js, docs.js, METHODS_3D.md, computed.json; plan status", plan["status"], "area", can["area_m2"])
    if annotations:
        import make_annotations as MA
        import nav_annotate as NA
        MA.fig_skelly_crest_labels(); MA.fig_ccc_exhibit2(); MA.fig_ccc_exhibit3_contours(); MA.fig_pdf_highlights(); MA.fig_dem(shape); MA.fig_datums()
        NA.main()
        import bn_annotate as BA
        BA.main()
        print("annotations redrawn")
    return comp


if __name__ == "__main__":
    main(annotations="--annotations" in sys.argv)
