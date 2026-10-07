#!/usr/bin/env python
"""build_3d.py - STAGE 2 of the bunbury-airwave 3D build: regenerates model.js, docs.js, METHODS_3D.md and computed.json.

Inputs (all inside the project, nothing is downloaded):
  ../shape.json                       verified plan outline (canonical frame)             [plan]
  ../../../../02_research/reefs/bunbury-airwave.json   the reef card (verdict, dates, developer account)  [state, chronology]
  data/lidar_clip_model_frame.csv     WA DoT 2009 lidar resampled to the model frame (5 m grid, filled flag)  [seabed]
  data/lidar_derived.json             frame, shoreline fit, native-resolution profile, summary of stage 1
  data/nav_transects.json             Navionics transects and datum test (written by nav_annotate.py)
  METHODS_3D.template.md              the methods note with {{placeholders}} (edit THIS, not METHODS_3D.md)
  SOURCES_3D.md, REQUESTS_FOR_LIOR.md, annotated/*.png   (copied / listed into docs.js)
Outputs: model.js (window.REEF_MODEL), docs.js (window.REEF_DOCS), METHODS_3D.md, computed.json, and an auto block at the end of SOURCES_3D.md.
Usage:   python build_3d.py                  (regenerate after a change of shape.json, the card or the template)
         python build_3d.py --annotations    (also re-run nav_annotate.py and nav_figures.py)
STAGE 1 (build_3d_lidar.py, needs the 67 MB BU2009TRBS_Lidar.bag, URL and md5 in SOURCES_3D.md) produced the lidar files; it is not needed here.
Everything numeric in the model is read from a file above or defined in the constants below with its source id; nothing is typed into the viewer.
Requires numpy, matplotlib (contours), scipy and Pillow (through nav_annotate).
"""
import datetime
import hashlib
import json
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SHAPE_DIR = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
CARD_PATH = os.path.join(ROOT, "02_research", "reefs", "bunbury-airwave.json")
DATA = os.path.join(HERE, "data")
TODAY = datetime.date.today().isoformat()
sys.path.insert(0, HERE)

# ------------------------------------------------------------------------------------------------ constants (source ids resolve in SOURCES below)
MSL_AHD = 0.10                                   # S_tide: MSL = +0.1 m AHD (GHD 2021 Table 1)
TIDES_AHD = {"HAT": 0.6, "MHHW": 0.2, "MLHW": 0.1, "MSL": 0.1, "MHLW": 0.0, "MLLW": -0.2, "LAT": -0.6}
TIDES_CD = {"HAT": 1.3, "MHHW": 0.9, "MLHW": 0.7, "MSL": 0.7, "MHLW": 0.6, "MLLW": 0.5, "LAT": 0.1}
LEVEL_ORDER = ["LAT", "MLLW", "MHLW", "MSL", "MLHW", "MHHW", "HAT"]
LEVEL_LABEL = {"HAT": "Highest Astronomical Tide", "MHHW": "Mean Higher High Water", "MLHW": "Mean Lower High Water", "MSL": "Mean Sea Level",
               "MHLW": "Mean Higher Low Water", "MLLW": "Mean Lower Low Water", "LAT": "Lowest Astronomical Tide (chart datum since 2009)"}
LAT_AHD_DOT = -0.57                              # S_DoTidx: LAT = AHD - 0.57 m at Bunbury
REEF_Y_DEFAULT = 37.5                            # shape.json canonical.distance_offshore_m (midpoint of the 30-45/50 m text range)
A_BASE = 6.0                                     # base radius (12 m diameter, text)
H_RANGE = (1.6, 2.0)                             # text: Tracks 2019 1.6 m; ABC/RWR 2 m
H_DEFAULT = 2.0
CREST_TEXT_M = 1.0                               # RWR: shallow point about 1 m under the surface at low tide
OFFSHORE_RANGE = (30.0, 50.0)
# uncertainty budget (1-sigma-like; the basis of each is given in METHODS_3D.md section 5)
SIG_LIDAR = 0.48                                 # BAG uncertainty layer at the reef zone (type 1-sigma / 95 % not stated: read as 1-sigma, conservative)
SIG_CHANGE = 0.30                                # assumed seabed change 2009 -> 2019 (no source; judgement)
SIG_TIDE_TRANSFER = 0.10                         # port gauge (3 km NE) -> Back Beach, plus 0.1 m rounding of the table
SIG_CREST_TEXT = 0.30                            # "about 1m"
FILL_MASS_T = (140.0, 150.0)                     # developer-only
BULK_DRY, BULK_SAT = 1.6, 2.0                    # t/m3 for beach sand (own assumption, section 4)
RNG_SEED = 20261005


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def fmt(v, d=2):
    return ("%." + str(d) + "f") % v


def sgn(v, d=2):
    return ("%+." + str(d) + "f") % v


def cap_vol(H, a=A_BASE):
    return math.pi * H * (3 * a * a + H * H) / 6.0


def cap_radius(H, a=A_BASE):
    return (a * a + H * H) / (2.0 * H)


def main(annotations=False):
    # ------------------------------------------------------------------------------------------ inputs
    shape_bytes = open(os.path.join(SHAPE_DIR, "shape.json"), "rb").read()
    shape = json.loads(shape_bytes.decode("utf-8"))
    card = json.load(open(CARD_PATH, encoding="utf-8"))
    ld = json.load(open(os.path.join(DATA, "lidar_derived.json"), encoding="utf-8"))
    import nav_annotate as NA
    navp = os.path.join(DATA, "nav_transects.json")
    if annotations or not os.path.exists(navp):
        NA.compute()
        import nav_figures
        if annotations:
            nav_figures.main()
    nav = json.load(open(navp, encoding="utf-8"))
    xs, ys, Zahd, F = NA.load_grid()
    sm = ld["summary"]
    fr = ld["frame"]
    prof = ld["profile"]
    can = shape["canonical"]
    poly = can["polygons_m"][0]
    assert shape["status"] == "verified", "shape.json status is %r" % shape["status"]

    # ------------------------------------------------------------------------------------------ seabed grid (model frame, z = AHD - MSL_AHD) and contours
    Zmsl = Zahd - MSL_AHD
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig_c, ax_c = plt.subplots()
    levels = [0, -1, -2, -3, -4, -5, -6, -7, -8]
    cs = ax_c.contour(xs, ys, Zahd, levels=sorted(levels))
    contours = []
    for lv, segs in zip(cs.levels, cs.allsegs):
        lines = [np.round(s, 1).tolist() for s in segs if len(s) > 1]
        contours.append({"ahd": float(lv), "z": round(float(lv) - MSL_AHD, 2), "polylines": lines})
    plt.close(fig_c)

    py = np.array(prof["y"], dtype=float)
    pz = np.array([np.nan if v is None else v for v in prof["median_ahd"]], dtype=float)
    ok = np.isfinite(pz)

    def zb(y):
        """median lidar seabed (m AHD) at y (5 m profile, linear)"""
        return float(np.interp(y, py[ok], pz[ok]))

    def zb_native(y):
        k = str(int(y)) if float(y).is_integer() else str(y)
        return float(sm["depths_ahd"][k]) if k in sm["depths_ahd"] else zb(y)

    def y_of_z(level):
        """seaward y where the median profile first falls to `level` (m AHD), searching y >= 15"""
        m = ok & (py >= 15)
        yy_, zz_ = py[m], pz[m]
        for i in range(len(yy_) - 1):
            if (zz_[i] - level) * (zz_[i + 1] - level) <= 0 and zz_[i] != zz_[i + 1]:
                return float(yy_[i] + (level - zz_[i]) * (yy_[i + 1] - yy_[i]) / (zz_[i + 1] - zz_[i]))
        return float("nan")

    slope = abs(sm["seabed_slope"])
    y_mllw = sm["y_of_level"]["-0.2"][0]
    y_lat = sm["y_of_level"]["-0.6"][0]
    y_msl = sm["y_of_level"]["0.0"][0]

    # ------------------------------------------------------------------------------------------ reef geometry numbers
    lat_z = TIDES_AHD["LAT"]
    mllw_z = TIDES_AHD["MLLW"]

    def crest_ahd(y, H):
        return zb_native(y) + H

    def below(level_ahd, zc):
        return level_ahd - zc            # positive = crest below that level

    reef_rows = {}
    for y in (30.0, 37.5, 45.0, 49.0, 50.0):
        for H in H_RANGE:
            zc = crest_ahd(y, H)
            reef_rows["%g_%g" % (y, H)] = {"seabed_ahd": round(zb_native(y), 2), "crest_ahd": round(zc, 2), "below_mllw": round(below(mllw_z, zc), 2),
                                           "below_lat": round(below(lat_z, zc), 2)}
    y_for_1m = {}
    for H in H_RANGE:
        y_for_1m["mllw_%g" % H] = round(y_of_z(mllw_z - CREST_TEXT_M - H), 1)
        y_for_1m["lat_%g" % H] = round(y_of_z(lat_z - CREST_TEXT_M - H), 1)
    y_tracks = round(y_mllw + 45.0, 1)               # "approximately 45 metres off the low tide mark"
    tracks = {H: {"seabed": round(zb(y_tracks), 2), "below_mllw": round(below(mllw_z, zb(y_tracks) + H), 2)} for H in H_RANGE}
    V = {H: cap_vol(H) for H in H_RANGE}
    V["1.8"] = cap_vol(1.8)
    area_traced = can["area_m2"]
    area_circle = math.pi * A_BASE ** 2
    mass_rows = []
    for m in FILL_MASS_T:
        lo, hi = m / BULK_SAT, m / BULK_DRY
        mass_rows.append({"mass_t": m, "vol_lo": lo, "vol_hi": hi, "share20": (lo / V[2.0], hi / V[2.0]), "share16": (lo / V[1.6], hi / V[1.6])})

    # ------------------------------------------------------------------------------------------ uncertainty (section 5)
    sig_y = (OFFSHORE_RANGE[1] - OFFSHORE_RANGE[0]) / math.sqrt(12)           # uniform over the text range
    sig_H = (H_RANGE[1] - H_RANGE[0]) / math.sqrt(12)
    sig_zb = math.sqrt(SIG_LIDAR ** 2 + (slope * sig_y) ** 2 + SIG_CHANGE ** 2)
    sig_zc = math.sqrt(sig_zb ** 2 + sig_H ** 2)
    sig_dc = math.sqrt(sig_zc ** 2 + SIG_TIDE_TRANSFER ** 2)
    sig_dc_lat = math.sqrt(sig_zc ** 2 + SIG_TIDE_TRANSFER ** 2)
    rng = np.random.default_rng(RNG_SEED)
    N = 40000
    y_s = rng.uniform(*OFFSHORE_RANGE, N)
    H_s = rng.uniform(*H_RANGE, N)
    zb_s = np.interp(y_s, py[ok], pz[ok]) + rng.normal(0, math.sqrt(SIG_LIDAR ** 2 + SIG_CHANGE ** 2), N)
    mllw_s = mllw_z + rng.normal(0, SIG_TIDE_TRANSFER, N)
    dc_s = mllw_s - (zb_s + H_s)
    mc = {"mean": float(dc_s.mean()), "sd": float(dc_s.std()), "p05": float(np.percentile(dc_s, 5)), "p50": float(np.percentile(dc_s, 50)), "p95": float(np.percentile(dc_s, 95)),
          "frac_ge_1": float((dc_s >= CREST_TEXT_M).mean()), "N": N}
    # the same with the position conditioned on the text 'about 1 m' (crest depth 1.0 +- 0.3 m): which y fit? (rejection on the crest depth)
    w = np.exp(-0.5 * ((dc_s - CREST_TEXT_M) / SIG_CREST_TEXT) ** 2)
    y_post = float(np.sum(w * y_s) / np.sum(w))
    y_post_sd = float(math.sqrt(np.sum(w * (y_s - y_post) ** 2) / np.sum(w)))
    z_default = (mllw_z - (zb_native(REEF_Y_DEFAULT) + H_DEFAULT) - CREST_TEXT_M) / math.sqrt(sig_dc ** 2 + SIG_CREST_TEXT ** 2)

    # ------------------------------------------------------------------------------------------ Navionics summaries
    D_LAT = TIDES_AHD["LAT"]
    ts = nav["transects"]
    nmin = min(len(t["crossings_s"]) for t in ts)
    nav_prof_y, nav_prof_z = [], []
    for n in range(nmin):
        nav_prof_y.append(float(np.mean([t["y_model_m"][n] for t in ts])))
        nav_prof_z.append(D_LAT - 0.5 * n)                       # m AHD under the LAT assumption
    nav_prof_y, nav_prof_z = np.array(nav_prof_y), np.array(nav_prof_z)
    nav_vs = {}
    for y in (30.0, 37.5, 45.0, 50.0, 60.0, 100.0, 150.0):
        zn = float(np.interp(y, nav_prof_y, nav_prof_z))
        nav_vs[str(y)] = {"nav_lat_ahd": round(zn, 2), "lidar_ahd": round(zb_native(y), 2), "diff_nav_minus_lidar": round(zn - zb_native(y), 2)}
    dm = [v["diff_nav_minus_lidar"] for k, v in nav_vs.items() if 30 <= float(k) <= 150]
    nav_mean_diff = float(np.mean(dm))
    # tilt of the Navionics 0 m line against the model x axis
    aa = np.array([t["a"] for t in ts], dtype=float)
    sg = np.array([t["s_green_end"] for t in ts], dtype=float)
    tilt = float(math.degrees(math.atan(np.polyfit(aa, sg, 1)[0])))
    nt = nav["datum_test_all"]
    nm = nav["datum_test_main"]

    # ------------------------------------------------------------------------------------------ card-derived state facts
    card_year = card["year"]
    verdict = card["verdict"]
    verdict_reason = card["verdict_reason"]
    dev = card["developer_account"]
    ref = {r["id"]: r for r in card["references"]}
    assert verdict == "failed", "card verdict is %r: the viewer text assumes FAILED" % verdict

    state_label = ("Installed bladder (installation attempted December 2019: began the week of 9 Dec, seam tear spotted Fri 13 Dec at about 90 % complete), "
                   "torn before completion - not a working reef")
    caption = ("<b>Installed bladder (December 2019: install week of 9 Dec, seam tear spotted Fri 13 Dec), torn before completion - not a working reef. Card verdict: FAILED.</b> "
               "Sand-slurry-ballasted Hypalon rubber, removed within days; no independent record of rideable waves. "
               "The developer's \"In 2018\" is contradicted by every dated 2019 report (Methods 2.1; this model uses December 2019). Shape drawn = symmetric-cap stand-in.")

    lifecycle = [
        {"date": "2018-08", "event": "Waveco's crowd-funding campaign (Kickstarter) fails; nothing deployed. The only 2018 events found.", "modelled": False, "source": "R3, R19"},
        {"date": "2019-06-13", "event": "ABC: the Airwave is set to be installed in November 2019.", "modelled": False, "source": "R2"},
        {"date": "2019-08-12", "event": "Tracks: first live trial planned for mid-November at about 45 m offshore; the crowd-funding was 'last year'.", "modelled": False, "source": "R23"},
        {"date": "2019-10-14", "event": "Raised Water Research: construction half-way.", "modelled": False, "source": "R4"},
        {"date": "2019-11-15", "event": "Tracks: 12 m diameter, 1.6 m tall at the highest point; live trial 'in the next couple of months'.", "modelled": False, "source": "R9"},
        {"date": "2019-12-07 to 12-13", "event": "Installation week (from Mon 9 Dec): slurry pump and hoses on the beach (7 Dec, forum observer); three divers and a boat.", "modelled": False, "source": "R9, R15, R1"},
        {"date": "2019-12-13 (Fri)", "event": "A diver spots the tear along a glued seam: bladder about 90 % complete, not fully anchored. THIS INSTALLED, TORN STATE IS WHAT THE MODEL SHOWS (geometry only).", "modelled": True, "source": "R1, R5, R7, R15"},
        {"date": "2019-12-16 (Mon)", "event": "Tear reported (ABC, RWR, The Inertia, SurferToday). Bottegal: unexpected deep swell and undertow.", "modelled": False, "source": "R1, R5, R6, R7"},
        {"date": "within about 3 days", "event": "Bladder removed from the water (reports range from about 5 hours to 3 days).", "modelled": False, "source": "R8, R18, R15"},
        {"date": "2020-07-09", "event": "Second prototype planned for December 2020 (about A$300,000 more needed); not confirmed built.", "modelled": False, "source": "R18"},
        {"date": "2021-10-08", "event": "Tracks: Bottegal 'readily admits' the first trial was a failure; sand pumped too heavily into one quadrant; redesign with welded compound, only tank-tested.", "modelled": False, "source": "R22"},
        {"date": "2022-03-22", "event": "Bunbury Mail: Bottegal says 'not a failure'; glued Hypalon seams; a lone 0.75 m wave seen (developer's account only); back in the water 'by Summer 2024'.", "modelled": False, "source": "R8"},
        {"date": "2025", "event": "Waveco's Bunbury proposal is a granite (rock) reef, not the rubber Airwave. The About page (last modified 2025-12-22) says 'In 2018 ... successfully created peeling waves ... wasn't a failure' (year contradicted, waves not independently supported).", "modelled": False, "source": "R20, R21"},
    ]

    # ------------------------------------------------------------------------------------------ sources
    def src(i, title, url, kind, quote=None, note=None, **kw):
        d = {"id": i, "title": title, "url": url, "kind": kind}
        if quote:
            d["quote"] = quote
        if note:
            d["note"] = note
        d.update(kw)
        return d

    sources = [
        src("S_shape", "Verified plan shape (shape.json): 29-vertex circle traced on the RWR drone photo img1", "07_scale/shapes/bunbury-airwave/shape.json (img1: https://raisedwaterresearch.com/wp-content/uploads/2019/12/Airwave-from-Above.jpg)", "image-derived"),
        src("S_card", "Reef card 02_research/reefs/bunbury-airwave.json (verified 2026-09-24; developer-account check 2026-10-05): verdict, install dates, material, references R1-R24", "02_research/reefs/bunbury-airwave.json", "card",
            note="verdict 'failed'; verdict_reason and developer_account quoted in METHODS_3D.md section 2.1"),
        src("S_RWR", "Raised Water Research, Bunbury Airwave profile page (R3)", "https://raisedwaterresearch.com/spot/artificial-reef/australia/western-australia/bunbury-airwave/", "text",
            quote="at low tide, the shallow point is about 1m under the surface of the water; rises about 2m off the sea floor at its highest point; 30-45 meters off the beach"),
        src("S_Tracks19", "Tracks Magazine 2019-11-15, Airwave set for live trial at Bunbury (R9)", "https://tracksmag.com.au/airwave-set-for-live-trial-at-bunbury-534049", "text",
            quote="twelve metres in diameter and 1.6m tall at the highest point; approximately 45 metres off the low tide mark"),
        src("S_ABC19", "ABC News 2019-12-16, Bunbury's Back Beach surfers deflated as artificial reef Airwave tears during installation (R1)", "https://www.abc.net.au/news/2019-12-16/word-first-surf-reef-tears-during-installation/11803228", "text", quote="two-metre-high, 12-metre-wide, dome-like bladder"),
        src("S_RWRtear", "Raised Water Research 2019-12-16, The Bunbury Airwave tears during installation (R5)", "https://raisedwaterresearch.com/the-bunbury-airwave-artificial-reef-tears-during-installation/", "text"),
        src("S_BunMail", "Bunbury Mail 2022-03-22, Airwave founder Troy Bottegal ... (R8)", "https://www.bunburymail.com.au/story/7667604/bunbury-still-set-to-become-surfing-destination/", "text", note="relays Bottegal: glued Hypalon seams, 140 t sand, removal within three days"),
        src("S_Tracks21", "Tracks Magazine 2021-10-08, The Airwave Pumps Again (R22)", "https://tracksmag.com.au/the-airwave-pumps-again", "text", quote="a bit of a skateboard ramp type thing happening ... now going for a more classic dome shape"),
        src("S_SWT20", "South Western Times 2020-07-09, Airwave back for second wave of Bunbury surf (R18)", "https://www.swtimes.com.au/news/south-western-times/airwave-back-for-second-wave-of-bunbury-surf-ng-b881601738z", "text"),
        src("S_Swellnet", "Swellnet forum thread 'Airwave inflatable reef' (R15, secondary: anonymous posts, dated 2019-12 observations)", "https://www.swellnet.com/forums/surfing-reef-designs/472884", "text"),
        src("S_Waveco", "Waveco Pty Ltd (developer) About page, 'The Bunbury Deployment' (R21): SELF-PUBLISHED, promotional, not independent", "https://www.waveco.com.au/about/", "developer claim",
            quote="In 2018, we deployed a 150-tonne sand-slurry bladder at Bunbury's Back Beach. While it successfully created peeling waves", note="accessed 2026-10-05; year contradicted by the independent record (December 2019); waves not independently supported"),
        src("S_Tradie", "The Tradie Magazine 2019-01-31, Creating the Perfect Wave (quote seen in search text only; page 403)", "https://www.tradiemagazine.com.au/creating-the-perfect-wave/", "text", quote="a very subtle, flattened dome with a steeply angled back"),
        src("S_Surfer", "SurferToday 2019-12-17, Ripped seam puts world's first inflatable surf reef on hold (R7; page 403 to scripts; figure seen via search text)", "https://www.surfertoday.com/surfing/ripped-seam-puts-worlds-first-inflatable-surf-reef-on-hold", "text", quote="50 meters from shore"),
        src("S_lidar", "WA Department of Transport bathymetry, Lidar2009TRBS ('Two Rocks - Naturaliste Lidar 2009'), 10 m grid, BAG", "https://dotazprdauegisextpubst01.blob.core.windows.net/transport-wa-public/bathymetry/rasters/BU2009TRBS_Lidar.bag", "data",
            note="survey index: https://services6.arcgis.com/67Ks15nDmWoIbK8b/arcgis/rest/services/Survey_index_linkedbagfiles/FeatureServer/0 ; DataRestri NO; metadata 'Approved for Public Release', 'Not to be used for navigation'; md5 a5742ce2217aef90670cee1426f76933"),
        src("S_tide", "GHD (2021) Tidal Inundation Monitoring and Modelling Report, Table 1 Tidal planes for Port of Bunbury (source cited there: Dept of Defence 2018)", "https://www.epa.wa.gov.au/sites/default/files/PER_documentation2/App%20B%20-%20Tidal%20innudation%20report.pdf", "table",
            quote="HAT +1.3 m CD / +0.6 m AHD ... MSL +0.7 / +0.1 ... LAT +0.1 / -0.6"),
        src("S_DoTidx", "WA DoT bathymetric survey index, Bunbury records: vertical datum LAT, AHD_Diff 0.57 BELOW", "https://services6.arcgis.com/67Ks15nDmWoIbK8b/arcgis/rest/services/Survey_index_linkedbagfiles/FeatureServer/0", "data", note="LAT = AHD - 0.57 m at Bunbury (consistent with -0.6 above)"),
        src("S_nav", "Garmin Navionics Marine Maps web viewer: SonarChart Maps and Nautical Charts layers, metres (webapp.navionics.com redirects here); accessed 2026-10-05", "https://maps.garmin.com/en-US/marine/", "data",
            note="(c) Garmin Navionics; private research copy; 'Not to be used for navigation'; no login or CAPTCHA; the app states no datum; screenshots in src/navionics/"),
        src("S_sat", "Esri World Imagery, Back Beach, 2025-08-30 (private research copy, rights not cleared)", "07_scale/shapes/bunbury-airwave/src/sat_backbeach_current.png", "image-derived",
            note="used only for the approximate reef location (waterline) and to draw the lidar contours over the beach"),
    ]

    # ------------------------------------------------------------------------------------------ provenance
    prov = []

    def P(parameter, value, unit, source_id, method, uncertainty, estimated=False):
        prov.append({"parameter": parameter, "value": value, "unit": unit, "source_id": source_id, "method": method, "uncertainty": uncertainty, "estimated": estimated})

    P("what the structure was", "Hypalon (synthetic-rubber) air/sand/water bladder, glued seams; NOT a rock reef, NOT a rigid shell", "-", "S_card, S_Tracks19, S_BunMail, S_RWR",
      "card type field; Tracks 2019 and Bunbury Mail 2022 (glued, not welded, Hypalon seams); material colour shown = pale grey (RWR drone photo / ABC frame show a pale bladder with a printed logo)",
      "colour is a rendering choice; the sources do not state one")
    P("fill", "sand slurry (washed coarse beach sand) + water + air; mass 140-150 t", "t", "S_Tracks19, S_BunMail, S_Tracks21, S_Waveco, S_Swellnet",
      "slurry corroborated independently (Tracks 2019, Bunbury Mail, RWR, forum observer); the MASS is developer-only (140 t Tracks 2021 / Bunbury Mail; 150 t Waveco page, forum summary); no anchors drawn",
      "mass +-7 % between the developer's own statements; no independent weighing; not used by the geometry")
    P("state modelled / date", "as installed: installation attempted December 2019 (week of 9 Dec; tear spotted Fri 13 Dec 2019); NOT 2018", "-", "S_card, S_ABC19, S_RWRtear, S_Swellnet",
      "card year and developer_account check: every dated 2019 report (ABC 2019-06-13, Tracks 2019-08-12 and 2019-11-15, RWR 2019-10-14 and 2019-12-16, ABC 2019-12-16) places the install in Dec 2019; Waveco's 'In 2018' is contradicted; the only 2018 events are a failed Kickstarter and a 'may be installed' preview",
      "day of the week of installation +-2 d; the geometry does not depend on it")
    P("verdict", "FAILED (card), kept", "-", "S_card, S_Waveco", "card verdict_reason; the developer's 'wasn't a failure' and 'successfully created peeling waves' were checked and do not change it", "-")
    P("reef plan outline", "circle, 12.0 m (traced 29-vertex polygon, %.1f m2)" % area_traced, "m", "S_shape", "ellipse fit of img1 outline, minor axis stretched; scale from the text-stated 12 m", "+-0.4 m outline reading; size from text, not measured")
    P("reef base diameter", 12.0, "m", "S_RWR, S_ABC19, S_Tracks19", "text, five sources agree", "none stated")
    P("reef height above seabed (default / range)", "2.0 (range 1.6-2.0)", "m", "S_RWR, S_ABC19 (2 m) vs S_Tracks19 (1.6 m)",
      "text; both are pre-install design figures reported by the developer; sources disagree, viewer slider covers both; no as-installed measurement exists", "0.4 m (the disagreement)")
    P("reef profile", "spherical cap (symmetric) by default; optional ramp asymmetry", "-", "S_Tracks21, S_Tradie",
      "ESTIMATE. Sources say 'dome', 'flattened dome with a steeply angled back', 'skateboard ramp'; the as-installed bladder was partly filled and torn; no cross-section or steep-side direction is published", "flank shape unknown; +-0.3 m locally", True)
    P("crest depth at low tide", CREST_TEXT_M, "m below water surface", "S_RWR", "text, design condition; 'low tide' level not defined (viewer assumes MLLW for the check)", "about 'about 1m'; +-%.1f m plus the undefined 'low tide' (MLLW vs LAT 0.4 m)" % SIG_CREST_TEXT)
    P("reef centre distance offshore (default)", REEF_Y_DEFAULT, "m seaward of the 0 m AHD contour", "S_shape; S_RWR 30-45, S_Tracks19 ~45 from low-tide mark, S_Surfer 50",
      "text midpoint kept from shape.json; presets 30 / 37.5 / 45 / %.0f / 50 m in the viewer. Measured from the 2009 0 m AHD contour (MSL waterline), the low-tide (MLLW) mark is %.1f m further out" % (y_tracks, y_mllw),
      "+-10 m (text range)", True)
    P("shoreline (y = 0)", "fitted 0 m AHD contour, 2009 lidar", "-", "S_lidar",
      "zero crossings along 201 rows (|north| <= 500 m), straight-line fit; rms scatter %.1f m" % ld["shoreline"]["rms_scatter_m"], "shoreline moves seasonally and over 10 years by tens of metres")
    P("seabed depth at the reef centre (y = 37.5)", round(zb_native(37.5), 2), "m AHD", "S_lidar", "median of bilinear samples |x| <= 100 m, 10 m grid",
      "BAG uncertainty layer %.2f m here; survey is 10 years before the install; alongshore p10-p90 +-0.15 m" % sm["uncertainty_layer_at_reef"][1])
    P("seabed depth, independent check", "Navionics SonarChart on LAT: %+.2f m vs lidar at 30-150 m (mean difference)" % nav_mean_diff, "m", "S_nav, S_lidar",
      "9 shore-normal transects, 0.5 m contours counted from the 0 m line, depths read below LAT (-0.60 m AHD); RMS %.2f m over %d lines" % (nt["LAT"]["rms_m"], nt["LAT"]["n"]), "contour counting +-0.5 m worst case; chart sources and dates not shown by the app")
    P("Navionics depth datum (inferred)", "LAT (-0.60 m AHD)", "-", "S_nav, S_lidar, S_tide, S_DoTidx",
      "app states none; RMS test on %d lines: LAT %.2f, MLLW %.2f, AHD %.2f, MSL %.2f m" % (nt["LAT"]["n"], nt["LAT"]["rms_m"], nt["MLLW"]["rms_m"], nt["AHD"]["rms_m"], nt["MSL"]["rms_m"]),
      "free-fit datum %+.2f m AHD (sd %.2f); MLLW disfavoured, not excluded" % (nt["_implied_free_datum_ahd"]["mean"], nt["_implied_free_datum_ahd"]["sd"]), True)
    P("structure visible in Navionics?", "no", "-", "S_nav", "no closed contour or 12 m anomaly at the default position or at +-60 m alongshore; the bladder was removed in Dec 2019", "lateral position unknown (+-100 m): weak check")
    P("seabed slope y = 30..100 m", round(slope, 4), "m/m (about 1:%.0f)" % (1 / slope), "S_lidar", "linear fit to the alongshore median profile", "smooth; no bar or trough within 200 m")
    P("seabed resolution", 10, "m cell", "S_lidar", "the 12 m reef covers only 1-2 cells; the seabed under the footprint is a sloping plane, not resolved detail", "natural rock/seagrass patches visible in the photos are not in the grid")
    n_filled = int(F.sum())
    P("seabed gap fill", "%d of %d 5 m nodes" % (n_filled, F.size), "-", "S_lidar", "no lidar return in the surf zone (y about -15..35): filled from the alongshore median profile (linear across the gap) + a smoothed per-column offset; shown tinted in the viewer", "+-0.3 m in the filled strip", True)
    P("vertical datum of lidar", "AHD", "-", "S_lidar, S_DoTidx", "DoT survey index says AHD; the BAG's own VERT_CS tag only says 'Instantaneous Water Level' (generic)", "datum label not independently verified; the 0 m contour falling at the MSL waterline supports AHD")
    P("tidal planes (HAT/MHHW/MLHW/MSL/MHLW/MLLW/LAT)", "+0.6 / +0.2 / +0.1 / +0.1 / 0.0 / -0.2 / -0.6", "m AHD", "S_tide, S_DoTidx", "table; LAT-AHD offset checked against the DoT index (0.57 m)", "rounded to 0.1 m; Bunbury Port inner-harbour gauge, assumed valid at Back Beach")
    P("model z reference", "z = AHD - 0.1", "m", "S_tide", "MSL = +0.1 m AHD", "+-0.05 m")
    P("frame orientation", "x = %.1f deg true, y (seaward) = %.1f deg true" % (fr["x_bearing_true"], fr["y_bearing_true"]), "deg", "S_lidar",
      "direction of the fitted 0 m AHD contour; grid convergence %.2f deg (pyproj); the Navionics 0 m line is tilted %+.1f deg against it" % (fr["grid_convergence_deg"], tilt), "+-2 deg (contour scatter)")
    P("site location", "%.4f, %.4f" % tuple(fr["site_point_latlon"]), "deg", "S_sat", "45 m seaward of the 2025 Esri waterline south of the Back Beach SLSC building; not traced (reef removed Dec 2019)", "+-100 m; the seabed is alongshore-uniform there, so lateral error barely matters", True)

    confidence = {
        "level": "medium",
        "reason_short": "Seabed (2009 lidar, cross-checked by Navionics, RMS %.2f m) and tides are sourced; reef height, crest depth and the installed shape are text-based or assumed, and the bladder never operated." % nt["LAT"]["rms_m"],
        "reason": ("MEDIUM, by the rubric in METHODS_3D.md section 6. The seabed comes from an airborne-lidar survey of this exact beach (smooth 1:%.0f slope), an independent Navionics chart agrees with it to %.2f m RMS once its depths are read below LAT, "
                   "and the tides are from a port table. The text-implied seabed (crest 1 m below low tide + 1.6-2 m height) is reached by the lidar at y = %.0f-%.0f m, inside the 30-50 m text range. Against that: the survey is from 2009, its 10 m cells cannot resolve the 12 m reef, "
                   "the offshore distance is a 30-50 m text range (+-0.4 m of depth), and the crest depth, height and flank shape are text or estimates. Crest depth below MLLW is %.2f +- %.2f m (Monte Carlo over the position and height ranges), against 'about 1 m' in the text. "
                   "The as-installed bladder was partly filled, unanchored and torn, so its true surface differs from the symmetric cap drawn." % (
                       1 / slope, nt["LAT"]["rms_m"], y_for_1m["mllw_1.6"], y_for_1m["mllw_2"], mc["mean"], mc["sd"])),
    }
    inputs_status = {
        "plan": "sourced - shape.json 29-vertex circle, 12 m from text (verified; plan confidence medium)",
        "crest": "sourced (text only) - RWR: about 1 m under the surface at low tide; 'low tide' datum undefined (MLLW assumed)",
        "height_slopes": "estimated - 1.6 or 2.0 m from text (pre-install design figures), profile shape assumed",
        "seabed": "sourced - WA DoT airborne lidar 2009 (10 m grid), cross-checked by Garmin Navionics SonarChart (LAT-referenced)",
        "tides": "sourced - port tidal-plane table (GHD 2021), checked against the DoT survey index",
        "state": "as installed (December 2019, torn before completion); later history in the caption and METHODS_3D.md only",
    }

    # ------------------------------------------------------------------------------------------ model.js
    def r2(a):
        return np.round(a, 2).tolist()

    water_levels = [{"id": k, "label": LEVEL_LABEL[k], "z": round(TIDES_AHD[k] - MSL_AHD, 2), "ahd": TIDES_AHD[k], "chart_datum_m": TIDES_CD[k], "source_id": "S_tide",
                     "note": "GHD 2021 Table 1, Port of Bunbury, rounded to 0.1 m"} for k in LEVEL_ORDER]
    sb = ld["seabed_meta"]
    model = {
        "meta": {"slug": "bunbury-airwave", "name": "Bunbury Airwave: sand-slurry-ballasted rubber (Hypalon) bladder, as installed Dec 2019 - torn, not a working reef", "built": TODAY, "units": "metres",
                 "generator": "3d/build_3d.py", "verdict": verdict, "verdict_reason": verdict_reason, "card_year": card_year, "state_label": state_label},
        "caption": caption,
        "lifecycle": lifecycle,
        "frame": {"description": "x alongshore (bearing %.1f deg true), y seaward from the fitted 0 m AHD contour (bearing %.1f deg true), z up, 0 = MSL = +0.1 m AHD. Same frame as shape.json canonical (x alongshore, y offshore)." % (fr["x_bearing_true"], fr["y_bearing_true"]),
                  "x_bearing_true": fr["x_bearing_true"], "y_bearing_true": fr["y_bearing_true"], "grid_convergence_deg": fr["grid_convergence_deg"], "north_xy": fr["north_xy"],
                  "origin_mga50": fr["origin_mga50"], "origin_latlon": fr["origin_latlon"], "site_point_latlon": fr["site_point_latlon"],
                  "site_point_offset_from_origin_m": fr["site_point_offset_from_origin_m"], "msl_ahd": MSL_AHD},
        "seabed": {"x0": float(xs[0]), "y0": float(ys[0]), "dx": sb["dx"], "dy": sb["dy"], "nx": int(len(xs)), "ny": int(len(ys)), "z": [r2(row) for row in Zmsl], "filled": [row.astype(int).tolist() for row in F],
                   "source_id": "S_lidar", "native_cell_m": sb["native_cell_m"], "vertical_uncertainty_m": sb["vertical_uncertainty_m"], "survey_year": sb["survey_year"], "note": sb["note"],
                   "contours": contours, "profile": prof,
                   "navionics": {"y": [round(float(v), 2) for v in nav_prof_y], "z_msl": [round(float(v) - MSL_AHD, 2) for v in nav_prof_z], "datum_assumed": "LAT (-0.60 m AHD)", "source_id": "S_nav",
                                 "note": "mean over 9 shore-normal transects of the SonarChart contour crossings (0.5 m interval, counted from the 0 m line), depths read below LAT; in the viewer it shifts the lidar surface by (Navionics - lidar median) per y; seabed CHECK, not the default"}},
        "shoreline": ld["shoreline"],
        "reef": {"toe_polygon_m": [[round(p[0], 3), round(p[1], 3)] for p in poly], "polygon_frame_note": "orientation of the traced polygon in x/y is arbitrary (circle); centred on its own ellipse centre",
                 "centre_default": [0.0, REEF_Y_DEFAULT], "offshore_range_text_m": list(OFFSHORE_RANGE),
                 "offshore_presets": [{"label": "30 m (RWR near)", "y": 30.0}, {"label": "37.5 m (shape.json)", "y": 37.5}, {"label": "45 m (RWR far)", "y": 45.0},
                                      {"label": "%.0f m (Tracks: 45 m off low-tide mark)" % y_tracks, "y": y_tracks}, {"label": "50 m (SurferToday)", "y": 50.0}],
                 "diameter_m": 12.0, "height_default_m": H_DEFAULT, "height_range_m": list(H_RANGE), "crest_depth_text_m": CREST_TEXT_M, "crest_depth_text_at": "low tide (MLLW assumed for the on-screen check)",
                 "material": {"label": "Hypalon (synthetic-rubber) bladder, sand-slurry + water + air fill, glued seams", "short": "sand-slurry-ballasted rubber bladder (not rock)",
                              "colour_hex": "#c8d0d4", "colour_note": "pale grey: the RWR drone photo and the ABC frame show a pale bladder with a printed logo; a rendering choice, no source states a colour",
                              "fill": "sand slurry (washed coarse beach sand), water and air", "fill_mass_t": list(FILL_MASS_T), "fill_mass_note": "developer-only (140 t Tracks 2021 / Bunbury Mail 2022; 150 t Waveco page / forum summary); no independent weighing",
                              "anchors": "none drawn (self-ballasted by its sand); installation was not fully anchored when it tore"},
                 "state": "as installed (December 2019), torn along a glued seam before completion; geometry = symmetric spherical-cap stand-in",
                 "profile": {"type": "spherical_cap", "asym_default": 0.0, "asym_max": 0.6, "steep_side_default_bearing_true": 0,
                             "note": "estimate: cap with base radius 6 m and height H; ramp asymmetry moves the apex towards the chosen side (steeper there), direction not published"}},
        "water_levels": water_levels,
        "water_default": "MSL",
        "north_arrow": {"north_xy": fr["north_xy"], "source": "grid convergence of MGA94 zone 50 at the site + fitted shoreline direction"},
        "navionics": {"reached": True, "url": "https://webapp.navionics.com/ -> https://maps.garmin.com/en-US/marine/", "layers": ["SonarChart Maps", "Nautical Charts"], "units": "metres",
                      "datum_stated": None, "datum_inferred": "LAT (-0.60 m AHD), by RMS test against the 2009 lidar", "contour_interval_m": 0.5, "accessed": "2026-10-05", "reef_visible": False,
                      "used_for": "seabed cross-check only (the bladder was removed in Dec 2019)", "blocked_or_login": "none (no login, CAPTCHA or consent dialog)",
                      "datum_test_all": nav["datum_test_all"], "datum_test_main": nav["datum_test_main"], "mean_diff_30_150_m": round(nav_mean_diff, 2)},
        "sources": sources,
        "provenance": prov,
        "confidence_3d": confidence,
        "inputs_status": inputs_status,
    }
    with open(os.path.join(HERE, "model.js"), "w", encoding="utf-8") as f:
        f.write("// generated by build_3d.py on %s - do not edit by hand. Frame/units: see REEF_MODEL.frame.\nwindow.REEF_MODEL = " % TODAY)
        json.dump(model, f, separators=(",", ":"))
        f.write(";\n")

    # ------------------------------------------------------------------------------------------ computed.json + METHODS_3D.md from the template
    lvl = {k: round(TIDES_AHD[k] - MSL_AHD, 2) for k in LEVEL_ORDER}
    r = reef_rows
    comp = {
        "build_date": TODAY, "card_year": card_year, "msl_ahd": MSL_AHD, "lat_ahd": TIDES_AHD["LAT"], "mllw_ahd": TIDES_AHD["MLLW"], "hat_ahd": TIDES_AHD["HAT"], "mhhw_ahd": TIDES_AHD["MHHW"],
        "lat_msl": lvl["LAT"], "mllw_msl": lvl["MLLW"], "mhhw_msl": lvl["MHHW"], "hat_msl": lvl["HAT"], "mhlw_msl": lvl["MHLW"], "mlhw_msl": lvl["MLHW"],
        "lat_dot": LAT_AHD_DOT, "lat_diff": round(abs(LAT_AHD_DOT - TIDES_AHD["LAT"]), 2), "range_hat_lat": round(TIDES_AHD["HAT"] - TIDES_AHD["LAT"], 2), "range_mhhw_mllw": round(TIDES_AHD["MHHW"] - TIDES_AHD["MLLW"], 2),
        "plan_status": shape["status"], "plan_verified_on": shape.get("verified_on"), "plan_conf": shape["confidence"]["level"], "plan_md5": hashlib.md5(shape_bytes).hexdigest(),
        "area_traced": area_traced, "area_circle": fmt(area_circle, 1), "area_diff_pct": fmt(100 * (area_traced / area_circle - 1), 1), "n_vertices": len(poly),
        "bx": fr["x_bearing_true"], "by": fr["y_bearing_true"], "conv": fr["grid_convergence_deg"], "shore_a_f": fmt(sm["fit"]["icpt_a_m"], 1), "shore_b_f": fmt(sm["fit"]["slope_b"], 4), "shore_rms": ld["shoreline"]["rms_scatter_m"],
        "site_dist": round(sm["fit"]["site_dist_to_line_m"], 1), "origin_e": fr["origin_mga50"][0], "origin_n": fr["origin_mga50"][1],
        "nx": len(xs), "ny": len(ys), "n_filled": n_filled, "n_nodes": int(F.size), "filled_pct": fmt(100 * n_filled / F.size, 1),
        "slope": fmt(slope, 4), "slope_inv": fmt(1 / slope, 1), "y_mllw": fmt(y_mllw, 1), "y_lat": fmt(y_lat, 1), "y_msl": fmt(y_msl, 1),
        "z20": fmt(zb_native(20), 2), "z30": fmt(zb_native(30), 2), "z375": fmt(zb_native(37.5), 2), "z40": fmt(zb_native(40), 2), "z45": fmt(zb_native(45), 2), "z49": fmt(zb_native(49), 2), "z50": fmt(zb_native(50), 2),
        "z60": fmt(zb_native(60), 2), "z100": fmt(zb_native(100), 2), "z150": fmt(zb_native(150), 2), "z200": fmt(zb_native(200), 2),
        "z375_msl": fmt(zb_native(37.5) - MSL_AHD, 2), "z375_mllw": fmt(mllw_z - zb_native(37.5), 2), "z375_lat": fmt(lat_z - zb_native(37.5), 2),
        "unc_layer": fmt(sm["uncertainty_layer_at_reef"][1], 2),
        "y_tracks": fmt(y_tracks, 1), "z_tracks": fmt(zb(y_tracks), 2),
        "cap20_375_crest_ahd": fmt(r["37.5_2"]["crest_ahd"], 2), "cap20_375_below_mllw": fmt(r["37.5_2"]["below_mllw"], 2), "cap20_375_below_lat": fmt(r["37.5_2"]["below_lat"], 2),
        "cap16_375_crest_ahd": fmt(r["37.5_1.6"]["crest_ahd"], 2), "cap16_375_below_mllw": fmt(r["37.5_1.6"]["below_mllw"], 2), "cap16_375_below_lat": fmt(r["37.5_1.6"]["below_lat"], 2),
        "cap20_30_below_mllw": fmt(r["30_2"]["below_mllw"], 2), "cap16_30_below_mllw": fmt(r["30_1.6"]["below_mllw"], 2),
        "cap20_45_below_mllw": fmt(r["45_2"]["below_mllw"], 2), "cap16_45_below_mllw": fmt(r["45_1.6"]["below_mllw"], 2),
        "cap20_50_below_mllw": fmt(r["50_2"]["below_mllw"], 2), "cap16_50_below_mllw": fmt(r["50_1.6"]["below_mllw"], 2),
        "tracks20_below_mllw": fmt(tracks[2.0]["below_mllw"], 2), "tracks16_below_mllw": fmt(tracks[1.6]["below_mllw"], 2),
        "y1_mllw_20": fmt(y_for_1m["mllw_2"], 1), "y1_mllw_16": fmt(y_for_1m["mllw_1.6"], 1), "y1_lat_20": fmt(y_for_1m["lat_2"], 1), "y1_lat_16": fmt(y_for_1m["lat_1.6"], 1),
        "zimp_mllw_20": fmt(mllw_z - CREST_TEXT_M - 2.0, 2), "zimp_mllw_16": fmt(mllw_z - CREST_TEXT_M - 1.6, 2), "zimp_lat_20": fmt(lat_z - CREST_TEXT_M - 2.0, 2), "zimp_lat_16": fmt(lat_z - CREST_TEXT_M - 1.6, 2),
        "diff_default_20": fmt(abs(zb_native(37.5) - (mllw_z - CREST_TEXT_M - 2.0)), 2), "diff_default_16": fmt(abs(zb_native(37.5) - (mllw_z - CREST_TEXT_M - 1.6)), 2),
        "rs20": fmt(cap_radius(2.0), 2), "rs16": fmt(cap_radius(1.6), 2), "theta20": fmt(math.degrees(math.asin(A_BASE / cap_radius(2.0))), 1), "theta16": fmt(math.degrees(math.asin(A_BASE / cap_radius(1.6))), 1),
        "vol20": fmt(V[2.0], 1), "vol16": fmt(V[1.6], 1), "vol18": fmt(V["1.8"], 1),
        "m140_lo": fmt(mass_rows[0]["vol_lo"], 0), "m140_hi": fmt(mass_rows[0]["vol_hi"], 0), "m150_lo": fmt(mass_rows[1]["vol_lo"], 0), "m150_hi": fmt(mass_rows[1]["vol_hi"], 0),
        "s140_20": "%.0f-%.0f" % tuple(100 * v for v in mass_rows[0]["share20"]), "s140_16": "%.0f-%.0f" % tuple(100 * v for v in mass_rows[0]["share16"]),
        "s150_20": "%.0f-%.0f" % tuple(100 * v for v in mass_rows[1]["share20"]), "s150_16": "%.0f-%.0f" % tuple(100 * v for v in mass_rows[1]["share16"]),
        "load_t_m2": fmt(150.0 / area_circle, 2), "load_kpa": fmt(150.0 / area_circle * 9.81, 0),
        "sig_lidar": fmt(SIG_LIDAR, 2), "sig_change": fmt(SIG_CHANGE, 2), "sig_tide": fmt(SIG_TIDE_TRANSFER, 2), "sig_crest_text": fmt(SIG_CREST_TEXT, 2), "sig_y": fmt(sig_y, 1), "sig_H": fmt(sig_H, 3),
        "slope_sig_y": fmt(slope * sig_y, 2), "sig_zb": fmt(sig_zb, 2), "sig_zc": fmt(sig_zc, 2), "sig_dc": fmt(sig_dc, 2), "sig_dc_lat": fmt(sig_dc_lat, 2),
        "mc_mean": fmt(mc["mean"], 2), "mc_sd": fmt(mc["sd"], 2), "mc_p05": fmt(mc["p05"], 2), "mc_p95": fmt(mc["p95"], 2), "mc_frac_ge1": fmt(100 * mc["frac_ge_1"], 0), "mc_n": mc["N"],
        "y_post": fmt(y_post, 1), "y_post_sd": fmt(y_post_sd, 1), "z_default": fmt(abs(z_default), 1),
        "ve5_h20": fmt(5 * 2.0, 1), "ve5_slope": fmt(1 / (5 * slope), 1), "ve5_angle20": fmt(math.degrees(math.atan(5 * math.tan(math.asin(A_BASE / cap_radius(2.0))))), 1),
        # navionics
        "nav_res": fmt(nav["res_m_per_px"], 4), "nav_ntr": len(ts), "nav_nlines": nmin, "nav_n_all": nt["LAT"]["n"], "nav_n_main": nm["LAT"]["n"],
        "nav_rms_lat": fmt(nt["LAT"]["rms_m"], 2), "nav_rms_lat_dot": fmt(nt["LAT (DoT index)"]["rms_m"], 2), "nav_rms_mllw": fmt(nt["MLLW"]["rms_m"], 2), "nav_rms_ahd": fmt(nt["AHD"]["rms_m"], 2), "nav_rms_msl": fmt(nt["MSL"]["rms_m"], 2),
        "nav_bias_lat": sgn(nt["LAT"]["bias_lidar_minus_nav_m"], 2), "nav_bias_mllw": sgn(nt["MLLW"]["bias_lidar_minus_nav_m"], 2),
        "navm_rms_lat": fmt(nm["LAT"]["rms_m"], 2), "navm_rms_mllw": fmt(nm["MLLW"]["rms_m"], 2), "navm_rms_ahd": fmt(nm["AHD"]["rms_m"], 2), "navm_rms_msl": fmt(nm["MSL"]["rms_m"], 2),
        "nav_free": sgn(nt["_implied_free_datum_ahd"]["mean"], 2), "nav_free_sd": fmt(nt["_implied_free_datum_ahd"]["sd"], 2), "nav_free_sem": fmt(nt["_implied_free_datum_ahd"]["sem"], 3),
        "navm_free": sgn(nm["_implied_free_datum_ahd"]["mean"], 2),
        "nav_zero_s": fmt(nav["zero_line_s_m"]["mean"], 1), "nav_zero_sd": fmt(nav["zero_line_s_m"]["sd"], 1), "nav_zero_z": sgn(nav["zero_line_lidar_ahd"]["mean"], 2), "nav_zero_z_sd": fmt(nav["zero_line_lidar_ahd"]["sd"], 2),
        "nav_tilt": sgn(tilt, 1), "nav_mean_diff": sgn(nav_mean_diff, 2),
        "nav_d30": sgn(nav_vs["30.0"]["diff_nav_minus_lidar"], 2), "nav_d375": sgn(nav_vs["37.5"]["diff_nav_minus_lidar"], 2), "nav_d45": sgn(nav_vs["45.0"]["diff_nav_minus_lidar"], 2), "nav_d50": sgn(nav_vs["50.0"]["diff_nav_minus_lidar"], 2),
        "nav_d60": sgn(nav_vs["60.0"]["diff_nav_minus_lidar"], 2), "nav_d100": sgn(nav_vs["100.0"]["diff_nav_minus_lidar"], 2), "nav_d150": sgn(nav_vs["150.0"]["diff_nav_minus_lidar"], 2),
        "nav_z375": sgn(nav_vs["37.5"]["nav_lat_ahd"], 2), "nav_z50": sgn(nav_vs["50.0"]["nav_lat_ahd"], 2),
        "nav_sound_z": sgn(nav["nautical_soundings"][0]["lidar_ahd"], 2), "nav_sound_d": sgn(nav["nautical_sounding_datum"]["mean"], 2), "nav_sound_x": nav["nautical_soundings"][0]["x_m"], "nav_sound_y": nav["nautical_soundings"][0]["y_m"],
        "nav_c2_d": sgn(nav["nautical_contours_main"][1]["implied_datum_ahd"], 2), "nav_c5_d": sgn(nav["nautical_contours_main"][2]["implied_datum_ahd"], 2),
        "nav_c2_s": fmt(nav["nautical_contours_main"][1]["s_m"], 1), "nav_c5_s": fmt(nav["nautical_contours_main"][2]["s_m"], 1),
        "slope_pm10": fmt(slope * 10.0, 2), "nav_sc2_s": fmt([t for t in ts if t["a"] == 0][0]["crossings_s"][4], 1), "nav_sc5_s": fmt([t for t in ts if t["a"] == 0][0]["crossings_s"][10], 1),
        "nav_sp2": fmt(nav["contour_spread_across_transects"]["2.0"]["sd_m"], 1), "nav_sp5": fmt(nav["contour_spread_across_transects"]["5.0"]["sd_m"], 1),
        "nav_table_md": "\n".join(["| y (m) | Navionics on LAT (m AHD) | lidar median (m AHD) | Navionics - lidar (m) |", "|---|---|---|---|"] +
                                  ["| %g | %+.2f | %+.2f | %+.2f |" % (float(k), v["nav_lat_ahd"], v["lidar_ahd"], v["diff_nav_minus_lidar"]) for k, v in nav_vs.items()]),
        "datum_table_md": "\n".join(["| candidate datum | z (m AHD) | RMS, 9 transects (n=%d) | bias lidar - Navionics | RMS, main transect (n=%d) |" % (nt["LAT"]["n"], nm["LAT"]["n"]), "|---|---|---|---|---|"] +
                                    ["| %s | %+.2f | %.2f | %+.2f | %.2f |" % (k, nt[k]["datum_ahd"], nt[k]["rms_m"], nt[k]["bias_lidar_minus_nav_m"], nm[k]["rms_m"]) for k in ("LAT", "LAT (DoT index)", "MLLW", "MHLW", "AHD", "MSL")]),
        "crest_table_md": "\n".join(["| reef centre y (m) | seabed (m AHD) | crest H = 1.6 m: below MLLW / LAT (m) | crest H = 2.0 m: below MLLW / LAT (m) |", "|---|---|---|---|"] +
                                    ["| %g | %+.2f | %.2f / %.2f | %.2f / %.2f |" % (y, r["%g_1.6" % y]["seabed_ahd"], r["%g_1.6" % y]["below_mllw"], r["%g_1.6" % y]["below_lat"], r["%g_2" % y]["below_mllw"], r["%g_2" % y]["below_lat"]) for y in (30.0, 37.5, 45.0, 49.0, 50.0)]),
        "mass_table_md": "\n".join(["| sand mass | settled volume (%.1f-%.1f t/m3) | share of cap, H = 2.0 m (%s m3) | share of cap, H = 1.6 m (%s m3) |" % (BULK_DRY, BULK_SAT, fmt(V[2.0], 1), fmt(V[1.6], 1)), "|---|---|---|---|"] +
                                   ["| %g t | %.0f-%.0f m3 | %s %% | %s %% |" % (m["mass_t"], m["vol_lo"], m["vol_hi"], "%.0f-%.0f" % tuple(100 * v for v in m["share20"]), "%.0f-%.0f" % tuple(100 * v for v in m["share16"])) for m in mass_rows]),
        "lifecycle_md": "\n".join(["| date | event | in the model? | source (card refs) |", "|---|---|---|---|"] +
                                  ["| %s | %s | %s | %s |" % (e["date"], e["event"], "**yes (geometry)**" if e["modelled"] else "no (caption/methods only)", e["source"]) for e in lifecycle]),
        "verdict_reason": verdict_reason, "dev_quote": dev["quote"], "dev_overall": dev["overall"],
        "n_dev_checks": len(dev["checks"]),
        "ref_ids": ", ".join(sorted(ref.keys(), key=lambda s: int(s[1:]))),
    }
    json.dump(comp, open(os.path.join(HERE, "computed.json"), "w", encoding="utf-8"), indent=1)
    methods = open(os.path.join(HERE, "METHODS_3D.template.md"), encoding="utf-8").read()

    def sub(m):
        k = m.group(1)
        if k not in comp:
            raise KeyError("placeholder {{%s}} not computed" % k)
        return str(comp[k])

    methods = re.sub(r"\{\{(\w+)\}\}", sub, methods)
    open(os.path.join(HERE, "METHODS_3D.md"), "w", encoding="utf-8").write(methods)

    # ------------------------------------------------------------------------------------------ auto block in SOURCES_3D.md
    sp = os.path.join(HERE, "SOURCES_3D.md")
    s_txt = open(sp, encoding="utf-8").read()
    block = ("<!-- BUILD-AUTO-START -->\n## Build state (written by build_3d.py on %s)\n"
             "- shape.json status = **%s**, verified_on = %s, plan confidence = %s, md5 %s; outline %d vertices, area %.1f m2.\n"
             "- Reef card verdict = **%s**; card year field: %s\n"
             "- Seabed: %d x %d nodes (5 m), %d gap-filled; Navionics datum test (lines with valid lidar): LAT %.2f m RMS, MLLW %.2f, AHD %.2f, MSL %.2f (n = %d).\n"
             "- confidence_3d = %s; crest depth below MLLW %.2f +- %.2f m (Monte Carlo over the position and height ranges) vs text 'about 1 m'.\n<!-- BUILD-AUTO-END -->" % (
                 TODAY, shape["status"], shape.get("verified_on"), shape["confidence"]["level"], hashlib.md5(shape_bytes).hexdigest(), len(poly), area_traced, verdict, card_year,
                 len(xs), len(ys), n_filled, nt["LAT"]["rms_m"], nt["MLLW"]["rms_m"], nt["AHD"]["rms_m"], nt["MSL"]["rms_m"], nt["LAT"]["n"], confidence["level"].upper(), mc["mean"], mc["sd"]))
    if "<!-- BUILD-AUTO-START -->" in s_txt:
        s_txt = re.sub(r"<!-- BUILD-AUTO-START -->.*?<!-- BUILD-AUTO-END -->", lambda m: block, s_txt, flags=re.S)
    else:
        s_txt = s_txt.rstrip() + "\n\n" + block + "\n"
    open(sp, "w", encoding="utf-8").write(s_txt)

    # ------------------------------------------------------------------------------------------ REQUESTS_FOR_LIOR.md (lat/lon computed from the model frame)
    import make_requests
    req_path = os.path.join(HERE, "REQUESTS_FOR_LIOR.md")
    nav_depth_of_y = lambda y: float(np.interp(y, nav_prof_y, 0.5 * np.arange(len(nav_prof_y))))
    make_requests.write(req_path, fr, sm, zb, nav_depth_of_y, TIDES_AHD["LAT"], comp)

    # ------------------------------------------------------------------------------------------ docs.js (methods + sources + requests markdown for the viewer)
    ann_dir = os.path.join(HERE, "annotated")
    docs = {"methods_md": methods, "sources_md": s_txt, "requests_md": open(req_path, encoding="utf-8").read() if os.path.exists(req_path) else "", "built": TODAY,
            "annotated": sorted(f for f in os.listdir(ann_dir) if f.lower().endswith(".png")) if os.path.isdir(ann_dir) else []}
    with open(os.path.join(HERE, "docs.js"), "w", encoding="utf-8") as f:
        f.write("// generated by build_3d.py on %s - do not edit by hand\nwindow.REEF_DOCS = " % TODAY)
        json.dump(docs, f, indent=1)
        f.write(";\n")
    print("built: model.js, docs.js, METHODS_3D.md, computed.json; plan", shape["status"], "verdict", verdict, "confidence", confidence["level"])
    return comp


if __name__ == "__main__":
    main(annotations="--annotations" in sys.argv)
