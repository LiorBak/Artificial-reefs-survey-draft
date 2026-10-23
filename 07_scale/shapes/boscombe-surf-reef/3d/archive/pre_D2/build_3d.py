#!/usr/bin/env python
"""build_3d.py - regenerate 3d/model.js, 3d/docs.js and 3d/model_stats.json for the Boscombe Surf Reef viewer.

    python build_3d.py            (from anywhere; needs numpy scipy matplotlib pillow opencv-python pyproj)

Inputs (all inside this reef's folder):
    ../shape.json                          verified plan outline (canonical metres)
    ../src/rendle_davidson_2012_fig9_bathymetry_apr2011_native.png   survey plot (private research copy)
    ../src/esri_wayback10_2011-09-28_z18_wide.png.geo.json           georeference of the satellite image (canonical frame origin)
    ../src/navionics_garmin_*_2026-10-05.png + scripts/navionics_reads.json   Garmin Navionics screenshots + soundings read by eye
    METHODS_3D.md, SOURCES_3D.md, REQUESTS_FOR_LIOR.md   notes embedded in the viewer via docs.js
    ../src/cco_profiles/*.txt              (added 2026-10-07) Channel Coastal Observatory beach-profile surveys (scripts/cco_fetch.py downloads them)
Outputs:
    model.js   window.REEF_MODEL = {...}   (seabed + reef height fields, outlines, water levels, provenance, confidence)
    docs.js    window.REEF_DOCS  = {...}   (METHODS_3D.md + SOURCES_3D.md text for the 'Methods & sources' panel)
If shape.json's canonical polygon changes, re-run this script: the toe outline, the survey registration test, the relief
statistics and the idealised loft are all recomputed from it.  Constants that come from text sources (tide levels, datum offset,
design crest) are in scripts/fields.py (CONSTANTS) with their source lines in SOURCES_3D.md.
"""
import json, math, sys, datetime
from pathlib import Path
import numpy as np
from scipy import ndimage as ndi

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "scripts"))
import fields as fl                                   # noqa: E402
import navionics as nv                                # noqa: E402
import extend_seabed as ex                            # noqa: E402  (2026-10-07: shoreward CCO beach + offshore EMODnet-slope extension)
from canon import CAN_POLY, SHAPE, can2osgb, px2ll, O_PX   # noqa: E402

CM = 100.0
BUILT = "2026-10-05"
REVISED = "2026-10-07"      # seabed extended to the shoreline / beach (CCO) and to y = 650 m (EMODnet slope)


def to_msl(z_survey):
    return z_survey + fl.SURVEY_ZERO_IN_MSL


def cm_list(a, nodata=-32768):
    out = np.where(np.isfinite(a), np.rint(a * CM), nodata).astype(int)
    return out.ravel().tolist()


def contour_loops(xs, ys, Z, level, min_len=25.0):
    import contourpy
    gen = contourpy.contour_generator(xs, ys, np.where(np.isfinite(Z), Z, -99.0), line_type=contourpy.LineType.Separate)
    loops = []
    for ln in gen.lines(level):
        if len(ln) < 4:
            continue
        L = np.hypot(*np.diff(ln, axis=0).T).sum()
        if L >= min_len:
            loops.append(ln)
    return loops


def simplify(ln, tol=1.0):
    from shapely.geometry import LineString
    s = LineString(ln).simplify(tol)
    return np.asarray(s.coords)


def main():
    F = fl.build()
    xs, ys = F["xs"], F["ys"]
    S, Zreef, rel, code = F["S"], F["Zreef"], F["relief"], F["code"]
    ideal = F["ideal_rel"]; inside = F["inside"]; valid = F["valid"]; Zs = F["Zs"]
    XX, YY = F["XX"], F["YY"]
    off = fl.SURVEY_ZERO_IN_MSL

    # ---------- seabed grid (2 m) in MSL frame, cm integers
    # Original grid x -160..160, y 0..380 (survey / spline / under reef) is kept cell for cell; rows are ADDED shoreward (y -66..-2, CCO beach
    # profiles) and offshore (y 382..650, EMODnet slope); y 0..~80 non-survey cells get the CCO offset (see scripts/extend_seabed.py).
    k = int(round(fl.SEABED["step"] / fl.FINE))
    S2 = S[::k, ::k]; code2 = code[::k, ::k]
    xs2, ys2 = xs[::k], ys[::k]
    EXT = ex.extend(xs2, to_msl(S2), code2)
    ys_ext = EXT["ys"]
    dw10 = np.rint(EXT["dw"] * 10).astype(int)
    seabed = {
        "x0": float(xs2[0]), "y0": float(ys_ext[0]), "dx": fl.SEABED["step"], "dy": fl.SEABED["step"], "nx": int(len(xs2)), "ny": int(len(ys_ext)),
        "order": "row-major: index = j*nx + i, i along +x, j along +y (offshore)",
        "unit": "cm", "z_cm": cm_list(EXT["z"]),
        "code": "".join(str(int(c)) for c in EXT["code"].ravel()),
        "code_key": {"0": "SURVEY value (Rendle & Davidson 2012 Fig 9 colour read, April 2011, light smoothing)",
                     "1": "EXTRAPOLATED outside the plotted survey area (thin-plate spline through the survey seabed) - no data; checked against Navionics soundings (mean -0.05 m, sd 0.47 m, n = 12)",
                     "2": "INTERPOLATED under the reef (thin-plate spline across the reef footprint) - pre-reef seabed estimate",
                     "3": "CCO BEACH PROFILE (Channel Coastal Observatory, survey of %s, m ODN): measured at the 11 profile lines, linearly interpolated alongshore between lines; y -66 m to the seaward end of the lines (y about 21-38 m)" % ex.CCO_DATE,
                     "4": "INTERPOLATION between the seaward end of the CCO profiles and the survey: spline extrapolation + the CCO offset decaying over %d m" % ex.BLEND_L,
                     "5": "EMODnet SLOPE EXTRAPOLATION y > 380 m: z(y) = z_model(x, 380) - %.4f (y - 380), EMODnet DTM 2024 slope, +-%.1f m; no local data" % (ex.EMODNET_SLOPE, ex.EMODNET_UNC)},
        "datum_w": "".join(chr(48 + int(v)) for v in dw10.ravel()),
        "datum_w_key": "one character per cell: chr(48 + round(10 * w)), w in 0..1 = fraction of the 'survey zero = ODN' switch (+1.40 m) applied to the cell; the CCO beach (ODN-referenced) has w = 0",
        "survey_valid_area_m2": int(valid.sum()),
        "extension": {"original_grid": {"x": [-160.0, 160.0], "y": [0.0, 380.0]}, "extended_grid": {"x": [-160.0, 160.0], "y": [float(ys_ext[0]), float(ys_ext[-1])]},
                      "cco_date": ex.CCO_DATE, "cco_lines": [d["pid"] for d in EXT["diag"]], "cco_blend_m": ex.BLEND_L,
                      "emodnet_slope": ex.EMODNET_SLOPE, "emodnet_unc_m": ex.EMODNET_UNC,
                      "cco_end_y_by_x": {"x0": float(xs2[0]), "dx": fl.SEABED["step"], "y_end": [round(float(v), 1) for v in EXT["y_end_by_x"]]},
                      "survey_y_range_m": [100.0, 312.0]},
    }
    cco_delta = np.array([d["delta_cco_minus_base"] for d in EXT["diag"]])
    cco_var = ex.beach_validation(EXT["lines"])
    zi = np.array([np.interp(0.0, ys_ext, EXT["z"][:, i]) for i in range(EXT["z"].shape[1])])
    seabed["extension"]["cco_vs_base"] = {"lines": EXT["diag"], "delta_mean_m": round(float(cco_delta.mean()), 3), "delta_sd_m": round(float(cco_delta.std()), 3),
                                          "delta_if_survey_zero_were_ODN_m": round(float(cco_delta.mean() - fl.MSL_ABOVE_CD), 3), "date_variability": cco_var,
                                          "z_msl_at_y0_mean_m": round(float(zi.mean()), 3), "z_msl_at_y0_range_m": [round(float(zi.min()), 3), round(float(zi.max()), 3)]}

    # ---------- reef grid (1 m) bounding box around reef mask + idealised loft
    rm = F["reef_mask"] | (ideal > 0)
    jj, ii = np.where(rm)
    pad = 2
    j0, j1, i0, i1 = jj.min() - pad, jj.max() + pad + 1, ii.min() - pad, ii.max() + pad + 1
    sl = (slice(j0, j1), slice(i0, i1))
    relief_s = rel[sl]; ideal_s = ideal[sl]; S_s = S[sl]
    surf_survey = np.where(relief_s > 0.10, to_msl(S_s + relief_s), np.nan)
    surf_ideal = np.where(ideal_s > 0.10, to_msl(S_s + ideal_s), np.nan)
    reef_grid = {
        "x0": float(xs[i0]), "y0": float(ys[j0]), "dx": 1.0, "dy": 1.0, "nx": int(i1 - i0), "ny": int(j1 - j0),
        "unit": "cm", "nodata": -32768,
        "surveyed_z_cm": cm_list(surf_survey),
        "idealised_z_cm": cm_list(surf_ideal),
        "seabed_under_z_cm": cm_list(to_msl(S_s)),
        "idealised_ramp_cm": cm_list(np.where(F["ideal_ramp"][sl] > 0, F["ideal_ramp"][sl], np.nan)),
        "note": "surveyed = April 2011 DGPS surface (colour read) where it stands >0.10 m above the estimated seabed; "
                "idealised = intact-reef loft of the verified outline (see reef.idealised_rule); idealised_ramp = relief 1 + phi/m before the crest cap (the viewer re-applies the cap when the datum switch is used); nodata = no reef here",
    }

    # ---------- statistics
    area_poly = float(inside.sum())
    stats = {
        "poly_area_m2": round(area_poly, 1),
        "survey_relief_volume_m3": round(float(rel.sum()), 0),
        "idealised_volume_m3": round(float(ideal.sum()), 0),
        "area_relief_gt": {str(t): int((rel > t).sum()) for t in (0.5, 1.0, 1.5, 2.0, 3.0)},
        "relief_inside_outline_pct_5_25_50_75_95_max": [round(float(v), 2) for v in np.percentile(rel[inside], [5, 25, 50, 75, 95, 100])],
        "tps_fit_rms_m": round(F["fit_rms"], 3),
    }
    zin = Zreef[inside]
    stats["crest_z_acd_inside_outline_pct_5_25_50_75_95_max"] = [round(float(v), 2) for v in np.percentile(zin, [5, 25, 50, 75, 95, 100])]
    iy, ix = np.unravel_index(np.argmax(np.where(inside, Zreef, -9)), Zreef.shape)
    stats["crest_max"] = {"z_acd": round(float(Zreef[iy, ix]), 2), "x": float(xs[ix]), "y": float(ys[iy])}
    stats["seabed_under_outline_acd_mean_min_max"] = [round(float(S[inside].mean()), 2), round(float(S[inside].min()), 2), round(float(S[inside].max()), 2)]
    gy, gx = np.gradient(Zreef, 1.0); g = np.hypot(gx, gy)
    sel = (rel > 1.0) & (rel < 2.5)
    stats["flank_gradient_median_survey"] = round(float(np.median(g[sel])), 3)

    # ---------- reef axis (PCA of the relief>1 m cells) and crest profile along it
    core = (rel > 1.0)
    cx, cy = XX[core].mean(), YY[core].mean()
    C = np.cov(np.vstack([XX[core] - cx, YY[core] - cy]))
    w, V = np.linalg.eigh(C); ax = V[:, np.argmax(w)]
    if ax[1] < 0:
        ax = -ax                                       # point offshore
    nrm = np.array([-ax[1], ax[0]])
    s_all = (XX - cx) * ax[0] + (YY - cy) * ax[1]
    t_all = (XX - cx) * nrm[0] + (YY - cy) * nrm[1]
    smin, smax = s_all[core].min(), s_all[core].max()
    prof = []
    for s in np.arange(math.ceil(smin / 5) * 5, smax, 5.0):
        m = core & (np.abs(s_all - s) < 2.5)
        if m.sum() < 8:
            continue
        zz = np.where(m, Zreef, -99); j, i = np.unravel_index(np.argmax(zz), zz.shape)
        prof.append({"s_m": float(s), "x": float(xs[i]), "y": float(ys[j]), "crest_z_acd": round(float(Zreef[j, i]), 2),
                     "crest_z_msl": round(float(to_msl(Zreef[j, i])), 2), "seabed_z_acd": round(float(S[j, i]), 2),
                     "relief_m": round(float(rel[j, i]), 2)})
    axis_bearing = (83.4 + math.degrees(math.atan2(ax[1], ax[0]))) % 360
    stats["axis"] = {"centre_xy": [round(float(cx), 1), round(float(cy), 1)], "unit_xy_offshore_end": [round(float(ax[0]), 4), round(float(ax[1]), 4)],
                     "bearing_to_offshore_end_deg": round(axis_bearing, 1), "length_core_m": round(float(smax - smin), 1)}

    # ---------- crest zones (contours of the surveyed surface inside the reef footprint)
    Zc = np.where(F["reef_mask"], Zreef, np.nan)
    Zc = ndi.gaussian_filter(np.nan_to_num(Zc, nan=-9.0), 1.2)
    zones = []
    for lev in (-1.0, -0.5, 0.0):
        loops = []
        for ln in contour_loops(xs, ys, np.where(F["reef_mask"], Zc, -9.0), lev):
            sp = simplify(ln, 1.0)
            loops.append([[round(float(a), 1), round(float(b), 1)] for a, b in sp])
        area = float(((Zc > lev) & F["reef_mask"]).sum())
        zones.append({"level_acd": lev, "level_msl": round(lev + off, 2), "area_m2": round(area), "loops": loops})
    stats["crest_zone_area_m2"] = {str(z["level_acd"]): z["area_m2"] for z in zones}

    # ---------- Navionics (Garmin) shoal outlines + soundings vs this model (assumed same datum, chart datum)
    NAV = nv.derive()
    nav_rows, nav_cmp = nv.compare(NAV, F, stats, zones)
    NAV_OUT = {
        "access": {"date": "2026-10-05", "viewer": "https://maps.garmin.com/en-US/marine (old webapp.navionics.com redirects here)", "layers": ["Nautical Charts", "SonarChart Maps"],
                   "units": "metres", "shallow_shading_m": 1, "zoom_used": "16/17/18 (18 = max, 0.378 m/px)", "datum": "NOT stated by the viewer; assumed chart datum",
                   "credit": "Garmin Navionics, not for navigation; private research copy; reuse not cleared"},
        "outlines_xy": {k + "|" + n: d["outline_xy"] for k, v in NAV["layers"].items() for n, d in v.items()},
        "shapes": {k + "|" + n: {a: b for a, b in d.items() if a != "outline_xy"} for k, v in NAV["layers"].items() for n, d in v.items()},
        "soundings": nav_rows, "comparison": nav_cmp,
        "outline_note": "outline_xy = canonical metres; layer|level: drying = above chart datum (green), depth_lt_0.5m / depth_lt_1m = blue shallow shading; draw at z_MSL = -depth_below_CD - 1.40 (drying: -1.40 + 0)",
    }

    # ---------- toe polygon with z at each vertex
    from matplotlib.path import Path as MP
    def samp(A, x, y):
        return float(A[int(round(y - ys[0])), int(round(x - xs[0]))])
    toe = []
    for x, y in CAN_POLY:
        sb = samp(S, x, y); rf = samp(Zreef, x, y)
        toe.append([round(float(x), 2), round(float(y), 2), round(float(to_msl(sb)), 2), round(float(to_msl(rf)), 2)])

    # ---------- survey extent outline
    from skimage import measure
    cs = measure.find_contours(valid.astype(float), 0.5)
    big = max(cs, key=len)
    ext = simplify(np.c_[xs[0] + big[:, 1], ys[0] + big[:, 0]], 2.0)
    survey_extent = [[round(float(a), 1), round(float(b), 1)] for a, b in ext]

    # ---------- origin
    lat0, lon0 = px2ll(*O_PX)
    E0, N0 = can2osgb(0.0, 0.0)

    # ---------- water levels (MSL frame)
    TD = fl.TIDES_ACD
    names = {
        "HAT": "Highest Astronomical Tide", "MHWS": "Mean High Water Springs", "MHWN": "Mean High Water Neaps",
        "MLWN": "Mean Low Water Neaps", "MLWS": "Mean Low Water Springs", "LAT": "Lowest Astronomical Tide (= chart datum within 0.06 m)",
    }
    water = [{"key": "MSL", "label": "Mean Sea Level (model zero)", "z": 0.0, "acd": fl.MSL_ABOVE_CD, "source_id": "S4",
              "note": "estimated: Ordnance Datum is 1.40 m above chart datum at Bournemouth (NTSLF); ODN ~ MSL; mean of the four mean levels in Mead Table 1 = 1.375 m ACD"}]
    for k_ in ("HAT", "MHWS", "MHWN", "MLWN", "MLWS", "LAT"):
        water.append({"key": k_, "label": names[k_], "z": round(TD[k_] - fl.MSL_ABOVE_CD, 2), "acd": TD[k_], "source_id": "S3",
                      "note": "Mead et al. (2010) Table 1 'Water levels at Boscombe (m, ACD)', Bournemouth Pier gauge"})
    water.sort(key=lambda d: -d["z"])

    sources = [
        {"id": "S1", "short": "Esri Wayback 2011-09-28 (plan outline)", "citation": "Esri, Maxar, Earthstar Geographics, and the GIS User Community (2011) World Imagery Wayback release 10, tiles of 2011-09-28. https://livingatlas.arcgis.com/wayback/ (retrieved 2026-10-04). Licence: Esri/Maxar terms, private research copy only.", "kind": "image"},
        {"id": "S2", "short": "Rendle & Davidson 2012, Fig. 9", "citation": "Rendle, E. & Davidson, M. (2012) An evaluation of the physical impact and structural integrity of a geotextile surf reef. Coastal Engineering Proceedings 33 (ICCE 2012), article 6794, Fig. 9; survey data Channel Coastal Observatory / Bournemouth Borough Council, April 2011. https://icce-ojs-tamu.tdl.org/icce/article/view/6794 (accessed 2026-10-05). Licence: authors' copyright, research copy.", "kind": "image"},
        {"id": "S3", "short": "Mead et al. 2010 (design crest, tides, Fig. 3a)", "citation": "Mead, S., Blenkinsopp, C., Moores, A. & Borrero, J. (2010) Design and construction of the Boscombe multi-purpose reef. Coastal Engineering Proceedings 32 (ICCE 2010), article 1352. https://icce-ojs-tamu.tdl.org/icce/article/view/1352 (accessed 2026-10-05).", "kind": "text+image"},
        {"id": "S4", "short": "NTSLF chart datum / ordnance datum table", "citation": "National Tidal and Sea Level Facility (n.d.) Chart datum and ordnance datum (table of offsets by port; Bournemouth -1.40 m). https://ntslf.org/tides/datum (accessed 2026-10-05).", "kind": "text"},
        {"id": "S5", "short": "EMODnet Bathymetry (datum plausibility check)", "citation": "EMODnet Bathymetry Consortium (2026) EMODnet Digital Bathymetry (DTM), WMS GetFeatureInfo, layer emodnet:mean. https://ows.emodnet-bathymetry.eu/wms (queried 2026-10-05). Depths relative to LAT, ~115 m cells.", "kind": "data"},
        {"id": "S6", "short": "Herbert et al. 2017 (exposure at low springs)", "citation": "Herbert, R.J.H., Collins, K., Mallinson, J., Hall, A.E., Pegg, J., Ross, K., Clarke, L. & Clements, T. (2017) Epibenthic and mobile species colonisation of a geotextile artificial surf reef on the south coast of England. PLoS ONE 12(9): e0184100. https://pmc.ncbi.nlm.nih.gov/articles/PMC5604948/ (accessed 2026-10-05).", "kind": "text"},
        {"id": "S7", "short": "shape.json (verified plan outline)", "citation": "This project (2026) 07_scale/shapes/boscombe-surf-reef/shape.json, status 'verified' 2026-10-05, canonical frame derived from S1.", "kind": "project"},
        {"id": "S8", "short": "riverlevels.uk Bournemouth (MSL ~ ODN check)", "citation": "riverlevels.uk (n.d.) Tide at Bournemouth: usual range -1.08 m to +1.11 m above Ordnance Datum. https://riverlevels.uk/tide-bournemouth (accessed 2026-10-05).", "kind": "text"},
        {"id": "S9", "short": "Garmin Navionics web viewer (Nautical Chart + SonarChart)", "citation": "Garmin Ltd / Navionics (2026) Marine Maps viewer, Nautical Charts and SonarChart Maps layers, depths in metres, shallow shading 1 m; screenshots of 2026-10-05 at zoom 16-18 centred on 50.71753 N, 1.83891 W. https://maps.garmin.com/en-US/marine (the former webapp.navionics.com redirects here). Not for navigation; vertical datum not stated by the viewer (assumed chart datum). Private research copy; reuse rights not cleared.", "kind": "image"},
        {"id": "S10", "short": "Liverpool Univ. page on SonarChart datum / drying areas", "citation": "University of Liverpool (n.d.) Depth surveys; crowd sourced charts (Navionics SonarChart, TeamSurv). https://www.liverpool.ac.uk/~cmi//mag/survey_h.html (accessed 2026-10-05): later SonarChart versions keep the drying areas as given by the Hydrographic Office and add extra contours by interpolation.", "kind": "text"},
        {"id": "S11", "short": "Solent Forum (double high water, tidal range gradient)", "citation": "Solent Forum (n.d.) Waves and tides. https://solentforum.org/solent/our_coastal_zone/waves_and_tides/ (accessed 2026-10-05): tidal range 1.2 m in Christchurch Bay rising to 3.0 m in Chichester Harbour; double high water in this part of the Channel. Context only, no number from it is used in the model.", "kind": "text"},
        {"id": "S12", "short": "History of the reef (closure, damage, liquidation, re-branding)", "citation": "Wikipedia (2026) Boscombe Surf Reef (accessed 2026-09-24 and via the project dossier 02_research/reefs/boscombe-surf-reef.md refs R1, R4, R6, R8): opening 19 Nov 2009, inspection 23 Mar 2011, closure 31 Mar 2011, ASR repairs Aug 2011 never completed, ASR liquidation Sept 2012, insurance settlement 2013, re-branding as Coastal Activity Park April 2014 / 2017, debris ashore 26 Dec 2017. Leisure Opportunities (2012) 'Future of Boscombe surf reef in doubt'; Newsroom.co.nz (2021) 'The Kiwi scientist and the failed surf breaks'.", "kind": "text"},
    ]

    for s_ in sources:
        if s_["id"] == "S5":
            s_["short"] = "EMODnet Bathymetry DTM 2024 (far-field slope, datum plausibility check)"
            s_["citation"] = ("EMODnet Bathymetry Consortium (2024) EMODnet Digital Bathymetry (DTM 2024). https://doi.org/10.12770/cf51df64-56f9-4a99-b1aa-36b8d7b743a1 (accessed 2026-10-06; "
                              "queried via WMS/ERDDAP/REST, see 07_scale/bathymetry/emodnet/REPORT.md). Vertical reference LAT (model LAT = -1.46 m MSL); 1/16 arc-minute cells, 115.8 m N-S x 73.4 m E-W at Boscombe; "
                              "source survey CDI 117452, EDMO 2607 (OceanWise Limited), quality index horizontal 3 / vertical 4 / age 1 / purpose 3. CC BY 4.0; not for navigation.")
    sources += [
        {"id": "S13", "short": "Channel Coastal Observatory beach profiles (Southeast Regional Coastal Monitoring Programme)",
         "citation": ("Channel Coastal Observatory / Southeast Regional Coastal Monitoring Programme (2026) Topographic beach profile surveys, profile lines 5f00424 to 5f00429 (incl. A lines), Poole Bay SU11 "
                      "(Easting, Northing, Elevation_OD in m ODN, chainage), survey dates 2004-2026; model uses %s. https://coastalmonitoring.org/ (profile API https://coastalmonitoring.org/cco/profiles/api.php and "
                      "WFS layer national_profiles, accessed 2026-10-06). Licence: Open Government Licence v3.0; source to be acknowledged; hydrographic data not for navigation. "
                      "Raw copies: ../src/cco_profiles/.") % ex.CCO_DATE, "kind": "data"},
        {"id": "S14", "short": "Project EMODnet feasibility report (integration plan 9.1, comparison 6)",
         "citation": "This project (2026) 07_scale/bathymetry/emodnet/REPORT.md, sections 6 (comparison with the Boscombe model) and 9.1 (integration plan: far-field slope -1.41 % +-0.10 %).", "kind": "project"},
    ]

    A_ = lambda a: float(a)
    prov = [
        {"parameter": "Reef toe outline (plan)", "value": f"25-vertex polygon, {area_poly:.0f} m2", "unit": "m", "source_id": "S7/S1",
         "method": "Outer edge of the dark bag field traced on Esri Wayback 2011-09-28; converted to the canonical frame (x alongshore, y offshore); drawn state = reef after the April 2011 damage",
         "uncertainty": "+-1 m on W/E/S edges, +-1.1 m on the shoreward edge; survey relief>1 m footprint is within 1-5% of the outline area (IoU 0.90, no shift)", "estimated": False},
        {"parameter": "Seabed and reef surface heights", "value": f"grid {seabed['nx']}x{seabed['ny']} at 2 m; reef 1 m", "unit": "m", "source_id": "S2",
         "method": "Colour of each pixel of Fig. 9 (left map) -> nearest colour of the printed bar (+0.9 .. -5.3 m); map axes (OSGB36 gridlines) -> canonical frame via lat/lon and the S1 georeference; gaussian 1 m smoothing",
         "uncertainty": "+-0.2 m colour read; plot is itself an interpolated surface of DGPS lines (finer than ~3-5 m not trustworthy)", "estimated": False},
        {"parameter": "Vertical datum of the survey plot", "value": "Chart Datum (ACD) assumed", "unit": "-", "source_id": "S2/S3/S6/S5",
         "method": "Crest and depth values agree with the designers' ACD figures; Rendle's text calls the zero 'MSL ... Chart Datum, Newlyn' (garbled); EMODnet check. Viewer switch shows the alternative (survey zero = ODN ~ MSL)",
         "uncertainty": "+-1.4 m on ALL absolute heights if the alternative is true (relief unaffected)", "estimated": True},
        {"parameter": "MSL above chart datum", "value": fl.MSL_ABOVE_CD, "unit": "m", "source_id": "S4/S3/S8",
         "method": "Bournemouth chart datum is 1.40 m below Ordnance Datum (NTSLF); ODN ~ MSL; Mead Table 1 mean of four mean levels 1.375 m; gauge usual range centred +0.02 m ODN",
         "uncertainty": "+-0.1 m", "estimated": True},
        {"parameter": "Tide levels HAT/MHWS/MHWN/MLWN/MLWS/LAT (ACD)", "value": "2.59 / 2.21 / 1.67 / 1.17 / 0.45 / -0.06", "unit": "m ACD", "source_id": "S3",
         "method": "Mead et al. (2010) Table 1; converted to the model frame by subtracting 1.40", "uncertainty": "+-0.05 m (table precision); tide gauge on Bournemouth Pier, ~1.5 km W of the reef", "estimated": False},
        {"parameter": "Design crest height", "value": "+0.5 m ACD (= -0.90 m MSL)", "unit": "m", "source_id": "S3",
         "method": "Quote: 'The design has a crest height of 0.5 m above chart datum'; settlement 0.5 m or less", "uncertainty": "design value; as-built/settled crest differs (see survey)", "estimated": False},
        {"parameter": "Surveyed crest (April 2011)", "value": f"max {stats['crest_max']['z_acd']:+.2f} m ACD at x={stats['crest_max']['x']:.0f}, y={stats['crest_max']['y']:.0f}; median inside outline {stats['crest_z_acd_inside_outline_pct_5_25_50_75_95_max'][2]:+.2f}", "unit": "m ACD", "source_id": "S2",
         "method": "Highest survey value along the reef axis every 5 m (crest_profile); damaged 70 m container gives a -1.2..-2 m trough (Fig. 9 profiles)",
         "uncertainty": "+-0.2 m colour read; peaks smoothed by the plot interpolation", "estimated": False},
        {"parameter": "Reef height above seabed", "value": f"median {stats['relief_inside_outline_pct_5_25_50_75_95_max'][2]:.1f} m, max {stats['relief_inside_outline_pct_5_25_50_75_95_max'][5]:.1f} m (survey); loft crest {fl.DESIGN_CREST_ACD} - seabed", "unit": "m", "source_id": "S2/S3",
         "method": "relief = surveyed surface minus thin-plate-spline seabed fitted to survey cells outside the reef", "uncertainty": "+-0.3 m (seabed under the reef is interpolated)", "estimated": True},
        {"parameter": "Side slope (idealised loft)", "value": f"1:{fl.SLOPE_RUN_PER_RISE}", "unit": "run:rise", "source_id": "S2",
         "method": "Fig. 9 across-reef section (62.2 m line): SW flank rises 2.0 m over 6-8 m (1:3 .. 1:4, steepest 2 m window 1:1.5); NE side 1:5 .. 1:7; map-derived median gradient is gentler (1:%.1f) because the plot is smoothed" % (1 / stats["flank_gradient_median_survey"]),
         "uncertainty": "+-30%", "estimated": True},
        {"parameter": "Seabed beyond the survey (corners, y 100-312 outside the plot, y 312-380)", "value": "thin-plate-spline extrapolation (code 1)", "unit": "m", "source_id": "S2/S9",
         "method": "TPS through the survey seabed; checked against 12 Navionics soundings in the extrapolated area (model - Navionics mean -0.05 m, sd 0.47 m) and EMODnet cells (see the EMODnet cross-check row)",
         "uncertainty": "+-0.5 m within ~100 m of the survey edge, growing beyond", "estimated": True},
        {"parameter": "Beach and nearshore seabed y -66 .. ~30 m (zone 'CCO profile', code 3)", "value": "11 profile lines, survey %s, Elevation_OD (m ODN) = z_MSL (A4)" % ex.CCO_DATE, "unit": "m", "source_id": "S13",
         "method": "Channel Coastal Observatory profile lines 5f00424..5f00429 (x -220..+222 m): Easting/Northing -> canonical (x, y) with the same chain as Fig. 9 (OSGB36 -> WGS84 -> S1 pixel -> canonical); heights taken as m ODN = m MSL (A4); each profile as a polyline in y, linear interpolation alongshore between lines; "
                   "back of beach z about +3.3 m ODN at y = -66 m; z reaches about -1.0 m ODN at the seaward end of the lines (y 21..38 m). Survey date %s = nearest date at which all 11 lines near the reef exist (2009-09-22 / 2009-11-30 exist on 1-2 lines only)" % ex.CCO_DATE,
         "uncertainty": "+-0.1 m survey; +-0.3 m between survey dates (rms of 2011-03 minus 2010-04 over 11 lines = %.2f m); +-5 m position (OSGB -> frame); +-0.1 m ODN = MSL; alongshore interpolation between lines 40-60 m apart" % (cco_var[[d["date"] for d in cco_var].index("2011-03-23")]["rms"] if cco_var else float("nan")), "estimated": False},
        {"parameter": "Transition CCO beach -> survey (y ~30 .. ~80 m, code 4)", "value": "spline extrapolation + CCO offset decaying over %d m" % ex.BLEND_L, "unit": "m", "source_id": "S13/S2",
         "method": "Z = base spline seabed + R, R = offset (CCO - base) at the seaward end of each profile line, interpolated alongshore and decaying to 0 over %d m (smoothstep); cells with survey or under-reef code are never changed" % ex.BLEND_L,
         "uncertainty": "+-0.5 m (no data between y ~35 and 100 m except the spline)", "estimated": True},
        {"parameter": "CCO beach vs Fig. 9 spline at the seaward end of the profiles (datum test of A3)", "value": "CCO (m ODN) minus spline seabed read as ACD: mean %+.2f m, sd %.2f m (n = 11 lines); if the Fig. 9 zero were ODN: %+.2f m" % (cco_delta.mean(), cco_delta.std(), cco_delta.mean() - fl.MSL_ABOVE_CD),
         "unit": "m", "source_id": "S13/S2", "method": "z_CCO(x_l, y_end) - z_model(x_l, y_end), y_end = last measured point of each line (y 21..38 m), model value = spline extrapolation 65-80 m beyond the plotted survey edge. Independent of EMODnet and Navionics: supports A3 (chart datum) and shows the extrapolation is good to ~0.3 m here",
         "uncertainty": "+-0.3 m (sd over lines); not a measurement of the survey itself", "estimated": False},
        {"parameter": "Shoreline y = 0 (surf line of 28 Sep 2011)", "value": "y = 0; model beach surface there z = %+.2f m MSL (range %+.2f..%+.2f over x)" % (seabed["extension"]["cco_vs_base"]["z_msl_at_y0_mean_m"], seabed["extension"]["cco_vs_base"]["z_msl_at_y0_range_m"][0], seabed["extension"]["cco_vs_base"]["z_msl_at_y0_range_m"][1]), "unit": "m", "source_id": "S7/S1/S13",
         "method": "surf line of the 2011-09-28 image between px (1300,772) and (1750,720); tide state at that moment unknown. With the CCO beach the surface at y = 0 is about -0.2 m ODN (~MLWN -0.23 m): the line is NOT the MSL waterline (MSL contour lies ~8 m landward, y about -8) and moves with the tide; the viewer also draws the waterline of the selected level",
         "uncertainty": "+-5 m (georeference); tide state unknown", "estimated": False},
        {"parameter": "North direction", "value": "x axis = bearing 83.4 deg, y axis = 173.4 deg", "unit": "deg true", "source_id": "S7/S1",
         "method": "shape.json geo.shoreline_bearing_deg 83.4 from the georeferenced image (north-up Web-Mercator)", "uncertainty": "+-0.5 deg", "estimated": False},
        {"parameter": "Imagery state vs survey state", "value": "survey April 2011; image 2011-09-28", "unit": "-", "source_id": "S1/S2",
         "method": "both after the April 2011 container failure; repairs began Aug 2011 inside the envelope (shape.json)", "uncertainty": "bag-field changes between April and Sept 2011 not resolved", "estimated": False},
    ]

    c_ = nav_cmp
    prov += [
        {"parameter": "State drawn (default)", "value": "AS-BUILT 2009, intact (idealised loft of the verified outline; crest +0.5 m ACD)", "unit": "-", "source_id": "S3/S2/S7",
         "method": "Lior's rule (2026-10-05): model the as-built state; later damage is NOT a second state. Loft: crest = design +0.5 m ACD (Oct 2009 DGPS crest +0.45..+0.65 m, Rendle & Davidson Fig. 9 lower panels), flanks 1:3 from the outline placed on the 1 m relief contour. The April 2011 survey surface (post-damage) is kept only as an evidence layer",
         "uncertainty": "crest +-0.3 m (design +0.5 vs Oct 2009 profile tops +0.05..+0.65, typical +0.2..+0.3), flank +-30%, flat crest idealised (design had a 'focus' and a 'wedge' section whose heights are not published)", "estimated": True},
        {"parameter": "Navionics shoal vs survey (cross-check)", "value": "drying patch %d m2 (SonarChart) / %d m2 (Nautical) vs survey >0 m ACD %d m2; 0.5 m contour %d vs %d m2; 1 m contour %d vs %d m2" % (
            c_["area_m2"]["drying_above_0m_acd"]["sonarchart"], c_["area_m2"]["drying_above_0m_acd"]["nautical_chart"], c_["area_m2"]["drying_above_0m_acd"]["survey_april2011"],
            c_["area_m2"]["shallower_than_0.5m"]["sonarchart"], c_["area_m2"]["shallower_than_0.5m"]["survey_april2011"],
            c_["area_m2"]["shallower_than_1m"]["sonarchart"], c_["area_m2"]["shallower_than_1m"]["survey_april2011"]), "unit": "m2", "source_id": "S9/S2/S10",
         "method": "Colour fills of the Garmin Navionics screenshots (green drying, blue < 1 m) converted to canonical metres; compared with the zones of the April 2011 survey surface. Navionics shows the structure as it is now (damaged, not removed). Agreement at 0.5 and 1 m is within 1-2 %, so the same datum (chart datum) is very probable; it may also mean both come from the same survey (the viewer gives no survey date)",
         "uncertainty": "area +-10 % (pixel read, 0.38 m/px); datum of Navionics not stated; independence from Fig. 9 not proven", "estimated": False},
        {"parameter": "Navionics soundings vs model seabed", "value": "%d soundings: mean difference model - Navionics %+.2f m, sd %.2f m (in the survey area n=%d: %+.2f m; extrapolated area n=%d: %+.2f m)" % (
            c_["soundings_all"]["n"], c_["soundings_all"]["mean"], c_["soundings_all"]["sd"], c_["soundings_in_survey_area"]["n"], c_["soundings_in_survey_area"].get("mean", float("nan")),
            c_["soundings_in_extrapolated_area"]["n"], c_["soundings_in_extrapolated_area"].get("mean", float("nan"))), "unit": "m", "source_id": "S9",
         "method": "27 spot soundings + 6 contour labels of the Nautical Chart (z17) read by eye (scripts/navionics_reads.json), pixel -> lat/lon -> canonical; model seabed (ACD) sampled at the same point",
         "uncertainty": "read +-0.05 m (printed to 0.1 m) and +-1 m in position; Navionics data date unknown", "estimated": False},
        {"parameter": "Tide model at the site", "value": "semi-diurnal with double high water; MHWS-MLWS 1.76 m, max spring range 1.96 m", "unit": "m", "source_id": "S3/S2/S11",
         "method": "Water level slider LAT..HAT uses the six Table-1 levels (Bournemouth Pier gauge); heights above chart datum converted with z_MSL = z_ACD - 1.40. The double high water (stand) is not modelled: the slider is a static level, not a time series",
         "uncertainty": "+-0.05 m (table precision); actual level also moves by surge (+-0.5 m) and wave set-up", "estimated": False},
    ]

    i0 = int(np.argmin(np.abs(xs2 - 0.0)))
    def zx0(y):
        return float(np.interp(y, ys_ext, EXT["z"][:, i0]))
    emo_cells = [(380, -8.51), (445, -9.98), (505, -10.56), (605, -11.63)]          # EMODnet cell means at x = 0, m MSL (REPORT 9.1: LAT values - 1.46)
    emo_tie = [(y, round(zx0(y), 2), z, round(zx0(y) - z, 2)) for y, z in emo_cells]
    seabed["extension"]["emodnet_tie_x0"] = {"rows": [{"y": a, "model_z_msl": b, "emodnet_z_msl": c, "model_minus_emodnet": d} for a, b, c, d in emo_tie],
                                             "note": "EMODnet cell means at the centres y = 380 / 445 / 505 / 605 m (REPORT 9.1; LAT -> MSL with 1.46 m); model = extension at x = 0"}
    prov += [
        {"parameter": "Seabed y 380-650 m (zone 'EMODnet slope', code 5)", "value": "z(y) = z_model(x, 380) - 0.0141 (y - 380); z(x=0, y=650) = %.2f m MSL" % zx0(650.0), "unit": "m", "source_id": "S5/S14",
         "method": "EMODnet DTM 2024 slope -1.41 % (+-0.10 %) from the four full cells beyond the model grid, applied from the model's own y = 380 row (column by column, so the alongshore pattern of the spline row continues); EXTRAPOLATED, no local data. Ties to EMODnet cell means within 0.8-1.4 m (model shallower): " +
                   "; ".join("y %d: model %+.2f vs EMODnet %+.2f (%+.2f)" % r for r in emo_tie),
         "uncertainty": "+-1.2 m (REPORT 9.1 gave +-1.0 m; Navionics z16 check of 11 soundings: rms 1.2 m, model deeper at x<0 and shallower at x>0, about -1.2 m per 100 m of x); EMODnet absolute levels themselves carry +-1.5 m datum/sampling uncertainty at Boscombe", "estimated": True},
        {"parameter": "EMODnet cross-check of the model seabed (validation, not a model value)", "value": "reef-centre cell (ki34288/kj32794, n = 12): EMODnet -5.62 m LAT = -7.08 m MSL; model minus EMODnet = +1.39 m; seven cells fully inside the grid: mean +1.80 m, sd 0.66 m (range +1.14 .. +3.05)", "unit": "m", "source_id": "S5/S14",
         "method": "EMODnet cell means vs the model averaged over the same cell footprints (z_LAT = z_MSL + 1.46); not a constant offset (smallest where best sampled), so not a datum shift (REPORT 6.2); the DTM shows no reef; EMODnet is not used for the reef, toe, beach or the seabed around the reef",
         "uncertainty": "+-1.5 m datum and sampling (REPORT 6.2)", "estimated": False},
    ]

    conf = {"level": "medium",
            "reason": "Outline (2011 satellite), seabed (April 2011 DGPS plot, +-0.2 m colour read) and the as-built crest (designers +0.5 m ACD, Oct 2009 survey +0.45..0.65) are all sourced and agree, and Garmin Navionics shows the same shoal; but the zero of the survey plot (chart datum) is assumed (+-1.4 m if wrong), the as-built flanks and flat crest are an idealised loft, and the ground under the reef and the strip between the beach profiles and the survey (y ~35-100 m) are interpolated. From 2026-10-07 the beach is a measured profile (Channel Coastal Observatory, April 2010) and it also supports the chart-datum reading (CCO minus model = +0.03 m, sd 0.30 m); the seabed beyond y = 380 m is an EMODnet-slope extrapolation (+-1 m)."}

    history = [
        {"date": "2008-06", "event": "Construction starts (lower container layer placed in 2008)", "source_id": "S3/S12"},
        {"date": "2009-09/10", "event": "Upper layer finished; as-built DGPS survey Oct 2009 (crest +0.45 to +0.65 m ACD) - THE STATE MODELLED", "source_id": "S3/S2"},
        {"date": "2009-11-19", "event": "Official opening", "source_id": "S12"},
        {"date": "2011-03-23", "event": "Council inspection finds 'substantial changes' in the reef profile", "source_id": "S12"},
        {"date": "2011-03-31", "event": "Closed for safety", "source_id": "S12"},
        {"date": "2011-04", "event": "DGPS survey: one 70 m container lost about 80 t of sand, 4 m gap, 2 m crest dip (probably a boat propeller)", "source_id": "S2/S12"},
        {"date": "2011-08", "event": "Repairs by ASR begin; suspended for the winter and never completed", "source_id": "S12"},
        {"date": "2011-09-28", "event": "Satellite image used for the plan outline (structure still clearly visible)", "source_id": "S1"},
        {"date": "2012", "event": "Adjacent container lost; gap up to 10 m (Rendle & Davidson 2012)", "source_id": "S2"},
        {"date": "2012-09", "event": "ASR Ltd in liquidation; council insurance settlement 2013", "source_id": "S12"},
        {"date": "2014-04", "event": "Site re-branded as a 'Coastal Activity Park' (diving, snorkelling, kite/windsurfing); surfing dropped; again 2017", "source_id": "S12"},
        {"date": "2017-12-26", "event": "Debris from the decaying bags still washing ashore", "source_id": "S12"},
        {"date": "2026-10-05", "event": "Garmin Navionics charts still show a shoal with a drying patch at the site: damaged, not removed", "source_id": "S9"},
    ]
    caption = ("AS-BUILT 2009 state (intact reef). Later: containers failed from March-April 2011 (one 70 m bag lost ~80 t of sand, 2 m crest dip), "
               "closed 31 Mar 2011, repairs never completed, ASR liquidated Sept 2012, site re-branded for diving/snorkelling 2014/2017; the bags still lie on the "
               "seabed in damaged form and still show as a shoal on the Navionics chart. Not modelled as a second state.")

    M = {
        "schema": 1, "slug": "boscombe-surf-reef", "name": "Boscombe Surf Reef (Bournemouth, UK)", "built": BUILT, "revised": REVISED,
        "state_drawn": "AS-BUILT 2009 (intact, finished Sept-Oct 2009): idealised loft of the verified outline with the design crest +0.5 m ACD. Evidence layer: April 2011 DGPS surface (after the container failure).",
        "caption": caption, "history": history, "default_reef_mode": "idealised",
        "frame": {
            "units": "m", "x_axis": "alongshore, true bearing 83.4 deg (towards the east; Boscombe Pier lies at negative x)", "y_axis": "offshore, true bearing 173.4 deg (shore normal, towards SSE)",
            "z_axis": "up, 0 = mean sea level (MSL)", "threejs_mapping": "X = x, Y = z, Z = y (right-handed, not mirrored: from above the shore is at the top, +x to the right, like a north-up map)",
            "bearing_x_deg": 83.4, "bearing_y_deg": 173.4, "heading_formula": "compass bearing of a canonical direction (dx,dy) = 83.4 + atan2(dy, dx) in degrees",
            "origin_latlon_wgs84": [round(lat0, 6), round(lon0, 6)], "origin_osgb36_EN": [round(float(E0), 1), round(float(N0), 1)],
            "origin_note": "point on the 2011-09-28 surf line nearest the reef centroid (canonical frame of shape.json)",
        },
        "north": {"dir_xy": [round(math.cos(math.radians(83.4)), 4), round(-0.0 + math.cos(math.radians(173.4)), 4)],
                  "note": "unit vector of true north in canonical (x, y): components are cos(bearing of axis); north is mostly towards -y (towards the beach)"},
        "datum": {
            "survey_datum": "Chart Datum (ACD) - ASSUMED (see provenance)", "msl_above_cd_m": fl.MSL_ABOVE_CD,
            "survey_zero_in_msl_m": fl.SURVEY_ZERO_IN_MSL, "z_msl_equals": "z_survey + survey_zero_in_msl_m",
            "alt_datum": {"label": "survey zero = Ordnance Datum Newlyn (~ MSL)", "shift_to_add_to_all_survey_heights_m": fl.ALT_DATUM_SHIFT},
            "lat_acd_m": fl.TIDES_ACD["LAT"],
        },
        "water_levels": water,
        "shoreline": {"y": 0.0, "x_range": [-160.0, 160.0], "label": "surf line in the 2011-09-28 image (tide state unknown)",
                      "z_msl_at_line_mean": seabed["extension"]["cco_vs_base"]["z_msl_at_y0_mean_m"],
                      "note": "since 2026-10-07 the seabed grid includes the beach (CCO profiles); the y = 0 line lies about 8 m seaward of the MSL waterline (z = -0.2 m); the viewer also draws the waterline of the selected level"},
        "seabed": seabed,
        "survey_extent": survey_extent,
        "reef": {
            "toe_polygon_xyzz": toe,
            "toe_polygon_note": "[x, y, z_seabed_MSL, z_surveyed_surface_MSL] per vertex; polygon = outer edge of the visible bag field, which lies on the ~1 m relief contour of the survey",
            "crest_zones": zones, "crest_zones_note": "contours of the surveyed surface (Gaussian 1.2 m) inside the footprint at the stated survey levels (ACD) and the same in MSL; area = cells above the level",
            "crest_profile": prof, "crest_profile_note": "highest surveyed point in each 5 m station along the reef axis (offshore end first at the largest s); 's' measured from the footprint centre",
            "axis": stats["axis"],
            "grid": reef_grid,
            "design": {"crest_acd_m": fl.DESIGN_CREST_ACD, "crest_msl_m": round(fl.DESIGN_CREST_ACD + off, 2), "source_id": "S3",
                       "settlement_m": "<= 0.5 (Mead et al. 2010)", "layers": "two layers of geotextile sand containers (lower layer 2008, upper layer 2009)",
                       "containers": "54 (Mead 2010; 32 in Rendle 2012), diameters 1-5 m, lengths 15-70 m, ~13,000 m3 sand"},
            "idealised_rule": f"relief = clip(1 + phi / {fl.SLOPE_RUN_PER_RISE}, 0, crest - seabed), phi = signed distance from the verified outline (+ inside, m); crest = design +{fl.DESIGN_CREST_ACD} m ACD; the outline is placed on the 1 m relief contour",
            "slope_run_per_rise": fl.SLOPE_RUN_PER_RISE,
        },
        "stats": stats, "navionics": NAV_OUT,
        "tides": {"gauge": "Bournemouth Pier (Mead et al. 2010)", "mhws_mlws_range_m": 1.76, "max_spring_range_m": 1.96, "double_high_water": True,
                  "note": "Poole Bay has a small range and a double high water (stand); the viewer uses static levels only", "source_id": "S3/S2/S11",
                  "acd_minus_odn_m": fl.MSL_ABOVE_CD},
        "provenance": prov, "sources": sources, "confidence_3d": conf,
    }
    js = "window.REEF_MODEL = " + json.dumps(M, separators=(",", ":")) + ";\n"
    (HERE / "model.js").write_text(js, encoding="utf-8")
    (HERE / "model_stats.json").write_text(json.dumps(stats, indent=1), encoding="utf-8")

    # ---------- docs.js
    docs = {"built": BUILT}
    for key, fn in (("methods_md", "METHODS_3D.md"), ("sources_md", "SOURCES_3D.md"), ("requests_md", "REQUESTS_FOR_LIOR.md")):
        p = HERE / fn
        docs[key] = p.read_text(encoding="utf-8") if p.exists() else f"({fn} not written yet)"
    (HERE / "docs.js").write_text("window.REEF_DOCS = " + json.dumps(docs, ensure_ascii=False) + ";\n", encoding="utf-8")
    print("model.js %.0f KB, docs.js %.0f KB" % ((HERE / "model.js").stat().st_size / 1024, (HERE / "docs.js").stat().st_size / 1024))
    print(json.dumps(stats, indent=1))
    print("crest profile (s, crest_z_acd, relief):", [(p["s_m"], p["crest_z_acd"], p["relief_m"]) for p in prof])


if __name__ == "__main__":
    main()
