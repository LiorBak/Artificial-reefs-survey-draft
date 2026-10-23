"""cables-reef-wa: build model.js + docs.js. Run from anywhere: python3 build_3d.py
Inputs: ../shape.json, ../scripts/computed.json, ../scripts/a2_trace.json, METHODS_3D.md, SOURCES_3D.md (docs). numpy/scipy/skimage/shapely only.
Frame of model.js: x = alongshore, + toward SOUTH (x_model = -x_canonical of shape.json) so that (x, y west, z up) is right-handed in three.js; y = offshore, + toward WEST;
z (reef/seabed grids) = metres AHD (taken as MSL, A12) under datum reading A (z_AHD = z_RL - 0.716, datum link of 2026-10-13); RL values are kept as z_RL in the contours and provenance."""
import base64, json, sys, datetime
import numpy as np
from scipy import ndimage as ndi
from scipy.optimize import brentq
from skimage import measure
sys.path.insert(0, __file__.rsplit('/', 1)[0]); import b3d_lib as L
HERE = L.HERE
DEFAULT_VERSION = "survey_surface_1999_11"   # decision X9 (2026-10-10): measured survey > design drawing (Lior rule 4); see METHODS_3D section 10
OFF_A = 0.716                      # AHD above the design / tide-gauge datum (Fremantle LWD): DNM TR12 Table 3, MSL 1966-68 = 2.350 ft = 0.716 m above gauge zero = AHD 0.000 (scripts/datum_link.py); +-0.04 m Perth metro zone. Until 2026-10-13: 0.78 (S1 p.3 mean tide level). z_AHD(= z_MSL, A12) = z_RL - 0.716 (reading A)
G_BED = 1 / 30.0                   # Pitt sketch: 1 m depth per ~28-33 m
V_TARGET = 5500.0                  # Blacka 2013 A.1.3
Y_REF = 270.0
SH, CO = L.SH, L.CO
vers_src = {v['id']: v for v in SH['outline_versions']}
# ---- design surface (RL) on the ramp
ramp, zr, om, im_ = L.ramp_distance_surface(CO['v_orig_m'], CO['ramp_m'])
zr_nan = zr.copy()
zr = np.where(ramp, zr, 0.0)
sil_a = L.raster(CO['v_asbuilt_m']); sil_o = L.raster(CO['v_orig_m'])
EXT = L.raster(CO['tri_m']) & ~L.raster(CO['v_orig_m'])          # extension triangle outside the original footprint
# ---- measured pre-construction bed (DoT WA 1998 singlebeam + Perth_5m, AHD), canonical frame; scripts/make_bed.py. Bed in RL = AHD + OFF_A (assumption A8: AHD = MSL)
from scipy import ndimage as _ndi
_BED = np.load(HERE + '/bed_measured_canonical.npz'); _bx, _by, _bz = _BED['x'], _BED['y'], _BED['z_AHD'].astype(float)
def bed_fn(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    return _ndi.map_coordinates(_bz, [((y - _by[0]) / (_by[1] - _by[0])).ravel(), ((x - _bx[0]) / (_bx[1] - _bx[0])).ravel()], order=1, mode='nearest').reshape(np.broadcast(x, y).shape) + OFF_A
def vol(sil, _unused=None):
    withext = bool((sil & EXT).any())
    xx, yy, bed, surf, band = L.surfaces(sil, ramp, zr, bed_fn, ext_mask=(EXT & sil) if withext else None, ext_volume=320.0 if withext else None)
    V, t = L.volume(surf, bed); return V, xx, yy, bed, surf, band, t
V_ORIG_MEAS = vol(sil_o)[0]; V_EXT_MEAS = vol(sil_a)[0]
print('volumes with measured bed: original %.0f, with extension %.0f (stated 5,500 / 5,000 / 3,500)' % (V_ORIG_MEAS, V_EXT_MEAS))
# old (first model, 2026-10-10): plane 1:30 fitted to 5,500 m3 -> D0 = 3.50 m RL at y = 270 (archive/pre_imagery_2026-10-10)
D0 = None
D0_by_volume = {}
BED_AT_270 = float(-bed_fn(0.0, 270.0))
# ---- per-version grids
def to_b64(a, dt): return base64.b64encode(a.astype(dt).tobytes()).decode()
def version_entry(vid, name, date, kind, srcs, method, level, key, note, sil):
    out = {"id": vid, "name": name, "date": date, "kind": kind, "source_ids": srcs, "method": method, "level": level, "note": note}
    poly_c = np.array(CO[key]); poly_m = [[round(-x, 2), round(y, 2)] for x, y in poly_c]
    out['outline_m'] = [poly_m]; out['area_m2'] = round(float(__import__('shapely.geometry', fromlist=['Polygon']).Polygon(poly_m).area), 0)
    b = np.array(poly_m); out['bbox_m'] = [round(float(np.ptp(b[:, 0])), 0), round(float(np.ptp(b[:, 1])), 0)]
    if sil is None:
        out['grid'] = None; out['volume_m3'] = None; out['volume_unc_m3'] = None; out['edge_level_MSL'] = round(float(np.mean(bed_fn(-b[:, 0], b[:, 1]))) - OFF_A, 2)
        return out
    V, xx, yy, bed, surf, band, t = vol(sil)
    zone = np.zeros(sil.shape, np.uint8); zone[sil & ramp] = 1; zone[band] = 2
    if vid == 'design_plan_plus_extension_1999':
        zone[EXT & band] = 3
    z_msl = surf - OFF_A
    hcm = np.where(np.isfinite(z_msl), np.round(z_msl * 100), -32768).astype(np.int16)
    # export at 0.5 m (d = 1; use d = 2 for 1 m), flip x to the model frame (x south)
    d = 1; hcm = hcm[::d, ::d]; zone = zone[::d, ::d]
    hcm = hcm[:, ::-1]; zone = zone[:, ::-1]
    out['grid'] = {"x0": -L.X1, "y0": L.Y0, "step": L.STEP * d, "nx": hcm.shape[1], "ny": hcm.shape[0], "h_cm_b64": to_b64(hcm, '<i2'), "zone_b64": to_b64(zone, np.uint8)}
    out['volume_m3'] = round(V, 0)
    out['volume_unc_m3'] = round(float(sil.sum() * L.STEP ** 2 * 0.3), 0)       # bed level +-0.3 m (see METHODS_3D 5)
    out['edge_level_MSL'] = round(float(np.mean(bed_fn(-b[:, 0], b[:, 1]))) - OFF_A, 2)
    out['crest_rl_m'] = -1.0; out['mean_thickness_m'] = round(V / float(sil.sum() * L.STEP ** 2), 2); out['max_thickness_m'] = round(float(np.nanmax(t)), 2)
    return out
V = []
for vid, key, sil in (('design_plan_plus_extension_1999', 'v_asbuilt_m', sil_a), ('design_plan_original_1999', 'v_orig_m', sil_o), ('paper_fig7_site_plan_1999', 'fig7_m', None), ('pitt_concept_sketch', 'pitt_m', None)):
    s = vers_src[vid]
    # shape.json (written by scripts/add_geo_to_shape.py before the survey versions existed) still labels the original plan "(default)"; since decision X2/X9 the default is
    # survey_surface_1999_11 and the viewer appends "[default]" itself (index.html), so the label is stripped here (fixed 2026-10-13).
    e = version_entry(vid, s['name'].replace(' (default)', ''), s['date'], s['kind'], s['source_ids'], s['method'], s['level'], key, s['note'], sil); V.append(e)
    print(vid, e['area_m2'], e['bbox_m'], e.get('volume_m3'))
# ---- design contours (RL) as polylines in the model frame, from the ramp surface
cont = []
zs = np.where(ramp, zr, np.nan)
for rl in (-2.5, -2.0, -1.5):
    lines = []
    for c in measure.find_contours(np.where(np.isfinite(zs), zs, -9.0), rl):
        if len(c) < 8: continue
        lines.append([[round(-(L.X0 + p[1] * L.STEP), 2), round(L.Y0 + p[0] * L.STEP, 2)] for p in c[::4]])
    cont.append({"rl": rl, "z_msl": round(rl - OFF_A, 2), "lines": lines})
# ---- seabed grid (measured, DoT WA 1998 survey + Perth_5m), model frame
SBX0, SBX1, SBY0, SBY1, SBS = -150.0, 150.0, 190.0, 420.0, 5.0
snx, sny = int((SBX1 - SBX0) / SBS) + 1, int((SBY1 - SBY0) / SBS) + 1
seabed_z = [[round(float(bed_fn(-(SBX0 + i * SBS), SBY0 + j * SBS)) - OFF_A, 2) for i in range(snx)] for j in range(sny)]   # x_model = -x_canonical; z = AHD (= MSL, A8)
# ---- validation numbers
s_px = CO['scale_px_per_m']; uc, vc = CO['centroid_px_asbuilt']
def zr_at(u, v):
    x = (u - uc) / s_px; y = 270 + (vc - v) / s_px; j = int(round((y - L.Y0) / L.STEP)); i = int(round((x - L.X0) / L.STEP)); return float(zr[j, i])
chk = []
for v, exp in ((154, -2.5), (221, -2.0), (286, -1.5)):
    chk.append({"drawn_row_px": v, "drawn_RL": exp, "model_RL": round(zr_at(560, v), 2), "diff_m": round(zr_at(560, v) - exp, 2)})
rms = round(float(np.sqrt(np.mean([c['diff_m'] ** 2 for c in chk]))), 2)
tchk = {}
for k, v in L.DRAWN_TRANSECT_CROSSINGS.items():
    mod = L.transect_crossings(zr_nan, v['p'][0], v['p'][1]); tchk[k] = {"drawn_m": v['drawn_m_from_outer_end'], "model_m": mod, "diff_m": [round(m - d, 1) if m is not None else None for m, d in zip(mod, v['drawn_m_from_outer_end'])]}
import json as _json
# ---- validation against the DoT WA soundings (Nov 1999 / Feb 2002, AHD) sampled on the model surface of the original plan
GEO = _json.load(open(HERE + '/../scripts/georef.json'))['transform']
def _soundings(fn, r=160):
    a = np.loadtxt(HERE + '/../src/bathymetry/FR_selected/' + fn, usecols=(0, 1, 2)); th = np.radians(GEO['theta_ccw_deg'])
    d = a[:, :2] - [GEO['anchor_E_MGA50_GDA94'], GEO['anchor_N_MGA50_GDA94']]; c, s_ = np.cos(-th), np.sin(-th)
    Ec = c * d[:, 0] - s_ * d[:, 1]; Nc = s_ * d[:, 0] + c * d[:, 1]
    xc = Nc + GEO['anchor_canonical_xy_m'][0]; yc = -Ec + GEO['anchor_canonical_xy_m'][1]
    m = (abs(xc) < 150) & (yc > 190) & (yc < 420); return xc[m], yc[m], a[m, 2]
_xo, _yo, _so, _bo, _so_s = None, None, None, None, None
_Vo, xx_o, yy_o, bed_o, surf_o, band_o, t_o = vol(sil_o)
svy = {}
for tag, fn in (('1999-11', 'FR19991122_Single.txt'), ('2002-02', 'FR20020201_Single.txt')):
    xs, ys, zs_ = _soundings(fn); j = np.round((ys - L.Y0) / L.STEP).astype(int); i = np.round((xs - L.X0) / L.STEP).astype(int)
    ok = (j >= 0) & (j < L.ny) & (i >= 0) & (i < L.nx); xs, ys, zs_, j, i = xs[ok], ys[ok], zs_[ok], j[ok], i[ok]
    inn = sil_o[j, i] & np.isfinite(surf_o[j, i]); zm = surf_o[j, i] - OFF_A            # model z in MSL(A) = AHD
    d = zs_[inn] - zm[inn]
    ramp_in = inn & ramp[j, i]
    top = lambda z: float(np.mean(np.sort(z)[-max(3, int(0.05 * len(z))):]))
    rr_ = ramp[j, i] & np.isfinite(zr_nan[j, i]); cfit = float(np.mean(zr_nan[j, i][rr_] - zs_[rr_])) if rr_.any() else None
    svy_off = {"n_ramp_soundings": int(rr_.sum()), "best_fit_RL_minus_AHD_m": round(cfit, 2), "sd_of_residual_m": round(float(np.std(zr_nan[j, i][rr_] - zs_[rr_])), 2)}
    svy[tag] = {"ramp_offset_fit": svy_off, "n_inside_original_footprint": int(inn.sum()), "survey_minus_model_mean_m": round(float(d.mean()), 2), "rms_m": round(float(np.sqrt((d ** 2).mean())), 2),
                "median_m": round(float(np.median(d)), 2), "survey_top5pct_mean_AHD": round(top(zs_[inn]), 2), "model_top5pct_mean_A": round(top(zm[inn]), 2),
                "model_top5pct_mean_if_reading_B": round(top(zm[inn]) + OFF_A, 2), "survey_max_AHD": round(float(zs_[inn].max()), 2)}
# ---- surveyed-surface versions: rock thickness from the DoT soundings (survey z - measured bed) interpolated linearly on the original-plan footprint (scripts/survey_volume.py logic)
from scipy.interpolate import LinearNDInterpolator as _LND, NearestNDInterpolator as _NND
from matplotlib.path import Path as _Path
from shapely.geometry import Polygon as _Poly
_foot = _Poly(CO['v_orig_m']); _buf = np.array(_foot.buffer(6).exterior.coords)
def survey_version(vid, name, date, fn, note, srcs):
    xs, ys, zs_ = _soundings(fn); t = zs_ - (bed_fn(xs, ys) - OFF_A)               # thickness above the measured bed (m); AHD = MSL (A8)
    sel = _Path(_buf).contains_points(np.c_[xs, ys]); f = _LND(np.c_[xs[sel], ys[sel]], t[sel]); fnn = _NND(np.c_[xs[sel], ys[sel]], t[sel])
    tt = f(xx_o, yy_o); tt = np.where(np.isnan(tt), fnn(xx_o, yy_o), tt); tt = np.maximum(tt, 0.0)
    w = ndi.gaussian_filter(sil_o.astype(float), 2.0); tt = np.where(sil_o, ndi.gaussian_filter(np.where(sil_o, tt, 0.0), 2.0) / np.maximum(w, 1e-9), 0.0)
    surf = np.where(sil_o, bed_o + tt, np.nan); Vs = float(np.nansum(tt[sil_o]) * L.STEP ** 2)
    out = {"id": vid, "name": name, "date": date, "kind": "survey_surface", "source_ids": srcs, "method": "rock thickness = DoT WA singlebeam sounding (AHD) minus the measured 1998 bed, interpolated linearly between sounding lines within the original-plan footprint + 6 m, Gaussian-smoothed 1 m; footprint = original plan georeferenced by the same soundings",
           "level": "outline of the original design plan (georeferenced by the soundings: %s %% of rock soundings inside); surface = surveyed" % _json.load(open(HERE + '/../scripts/georef.json'))['fit']['rock_soundings_inside_pct'], "note": note}
    poly_m = [[round(-x, 2), round(y, 2)] for x, y in CO['v_orig_m']]; out['outline_m'] = [poly_m]; out['area_m2'] = round(float(_foot.area), 0)
    b = np.array(poly_m); out['bbox_m'] = [round(float(np.ptp(b[:, 0])), 0), round(float(np.ptp(b[:, 1])), 0)]
    z_msl = surf - OFF_A; hcm = np.where(np.isfinite(z_msl), np.round(z_msl * 100), -32768).astype(np.int16)
    zone = np.zeros(sil_o.shape, np.uint8); zone[sil_o] = 1
    hcm = hcm[:, ::-1]; zone = zone[:, ::-1]
    out['grid'] = {"x0": -L.X1, "y0": L.Y0, "step": L.STEP, "nx": hcm.shape[1], "ny": hcm.shape[0], "h_cm_b64": to_b64(hcm, '<i2'), "zone_b64": to_b64(zone, np.uint8)}
    out['volume_m3'] = round(Vs, 0); out['volume_unc_m3'] = 1000.0
    out['edge_level_MSL'] = round(float(np.mean(bed_fn(-b[:, 0], b[:, 1]))) - OFF_A, 2)
    out['crest_rl_m'] = None; out['mean_thickness_m'] = round(Vs / float(sil_o.sum() * L.STEP ** 2), 2); out['max_thickness_m'] = round(float(tt.max()), 2)
    out['crest_AHD_m'] = round(float(np.nanmax(z_msl)), 2); return out
V.append(survey_version('survey_surface_1999_11', 'Surveyed surface, Nov 1999 (DoT WA singlebeam)', 'survey ending 22 Nov 1999 (FR19991122); construction Feb-Dec 1999', 'FR19991122_Single.txt',
        "Measured, 840 soundings; the nearest thing to the as-built reef at completion. Footprint = the original plan (the extension triangle has only 27 soundings and is not distinguishable). Rock thickness is interpolated between sounding lines; single-beam smooths narrow ridges.", ['DoT1999', 'DoT1998']))
V.append(survey_version('survey_surface_2002_02', 'Surveyed surface, Feb 2002 (DoT WA singlebeam)', 'survey ending 1 Feb 2002 (FR20020201)', 'FR20020201_Single.txt',
        "Measured, 5,143 soundings in the window (about 5 m line spacing), 2.2 years after completion; the south-arm extension triangle is covered (mean +0.43 m) but not distinguishable from the surrounding bed.", ['DoT2002', 'DoT1998']))
for v in V[-2:]: print(v['id'], v['area_m2'], v['volume_m3'], v['mean_thickness_m'], v['max_thickness_m'], v['crest_AHD_m'])
GEO = _json.load(open(HERE + '/../scripts/georef.json'))['transform']; GEO_FIT = _json.load(open(HERE + '/../scripts/georef.json'))['fit']; SV2 = _json.load(open(HERE + '/../scripts/georef.json'))['survey_2002_vs_1998']
SVOL = _json.load(open(HERE + '/../scripts/survey_volume.json')); SHDAT = _json.load(open(HERE + '/../scripts/shore_datum.json')); SHORE_BRG = SHDAT['shoreline_bearing_deg_T']
dflt = [v for v in V if v['id'] == DEFAULT_VERSION][0]; orig = V[1]
bed_range = [round(float(-bed_fn(0, y)), 2) for y in (min(p[1] for p in CO['v_asbuilt_m']), max(p[1] for p in CO['v_asbuilt_m']))]
_ob = np.array(CO['v_orig_m']); _bu = -bed_fn(_ob[:, 0], _ob[:, 1])
validation = {"bed": "measured: DoT WA singlebeam 30 Mar 1998 (pre-construction) + Perth_5m, AHD; replaces the fitted 1:30 plane (RL -3.50 at y = 270) of the first model",
  "bed_AHD_at_x0_y270": round(float(bed_fn(0.0, 270.0)) - OFF_A, 2),
  "bed_depth_at_outline_original_plan_RL_m": {"min": round(float(_bu.min()), 2), "max": round(float(_bu.max()), 2), "mean": round(float(_bu.mean()), 2), "note": "depth below RL 0 of the measured bed along the outline; add 0.716 for depth below AHD (= MSL, A12) under reading A"},
  "bed_depth_at_outline_original_plan_below_MSL_A_m": {"min": round(float(_bu.min()) + OFF_A, 2), "max": round(float(_bu.max()) + OFF_A, 2), "mean": round(float(_bu.mean()) + OFF_A, 2), "text_water_depth": "3.0-6.0 m (Blacka Table 4.2, RWR)"},
  "S1_7m_contour_at_350m_model_depth_RL": round(float(-bed_fn(0, 350.0)), 2),
  "contour_check_centreline": chk, "contour_check_rms_m": rms, "contour_check_transects": tchk,
  "bed_at_setout_line": {"AHD_m": round(float(np.mean([bed_fn(p[0], p[1]) for p in np.array(CO['v_orig_m'])[12:73]])) - OFF_A, 2), "note": "mean measured bed (m AHD) along the outer foot (vertices 12-72 of the traced outline). Not a datum test: the design outer line RL -3.0 is the top of the outer slope, the bed under the foot is deeper"},
  "survey_check": svy,
  "volumes": {"default_model": dflt['volume_m3'], "original_model": orig['volume_m3'], "volume_with_extension_model": V[0]['volume_m3'], "stated_Blacka_A13": 5500, "stated_P3_ICM": 5000, "stated_Wikipedia": 3500, "extension_text_m3": 320,
              "implied_density_t_m3_if_10000_t": round(10000 / dflt['volume_m3'], 2), "first_model_before_survey": {"default_with_extension": 5500.0, "original": None}},
  "mean_thickness_m": dflt['mean_thickness_m'], "max_thickness_m": dflt['max_thickness_m']}
sys.path.insert(0, HERE)
levels = [
 {"id": "DATUM", "name": "Design / tide-gauge datum (chart datum, low-water mark)", "z": -0.716, "rl": 0.0, "source": "DNM TR12 Table 3: Fremantle MSL 1966-68 = AHD 0.000 is 0.716 m above gauge zero (Fremantle LWD; +-0.04 m Perth metro zone); Pitt sketch note: 0.0 on the tide gauge", "estimated": False},
 {"id": "LWt", "name": "Typical low water (MSL - 0.4 m)", "z": -0.40, "rl": 0.32, "source": "Blacka 2013 Table 4.3: tide range 0.8 m; half range taken as +-0.4 m (estimate)", "estimated": True},
 {"id": "MSL", "name": "Mean sea level (= AHD, MSL 1966-68 at Fremantle; MSL 1992-2011 is +0.06 m)", "z": 0.0, "rl": 0.716, "source": "AHD 0.000 = MSL 1966-68 (GA; DNM TR12 Table 3); BoM Fremantle MSL 1992-2011 0.773 m above gauge zero = AHD +0.057; S1 p.3 mean tide level 0.78 m above datum", "estimated": False},
 {"id": "HWt", "name": "Typical high water (MSL + 0.4 m)", "z": 0.40, "rl": 1.12, "source": "Blacka 2013 Table 4.3: tide range 0.8 m (estimate)", "estimated": True},
]
M = {
 "slug": "cables-reef-wa", "name": "Cable Station artificial surfing reef (Cables Reef, Cottesloe / Leighton, Perth, Western Australia)", "built": datetime.date.today().isoformat(),
 "state": "Default: rock surface surveyed by DoT WA in Nov 1999 (the month before completion) on the georeferenced Lyons (1992) design footprint, on the measured pre-construction bed. Design-plan versions (with and without the south-arm extension) are drawn at their design levels (RL -1.0 crest to -3.0 outer edge). Later changes are notes only.",
 "frame": {"x": "alongshore, + toward SOUTH (x_model = -x_canonical)", "y": "offshore, + toward WEST", "z": "up, 0 = MSL (reading A)", "units": "m", "origin": "the design drawing frame (x along the reef axis, y offshore) rotated %.1f deg from true north by the georeference; origin = canonical origin, centroid of the original footprint at y = 271 m" % GEO['theta_ccw_deg'],
           "bearing_x_deg": round((GEO['canonical_plus_x_bearing_deg'] + 180.0) % 360, 1), "bearing_y_deg": GEO['canonical_plus_y_(offshore)_bearing_deg'], "north_xy": [round(-float(np.cos(np.radians(GEO['theta_ccw_deg']))), 4), round(-float(np.sin(np.radians(GEO['theta_ccw_deg']))), 4)], "shoreline_y": 0.0, "shoreline_bearing_deg": SHORE_BRG},
 "datum": {"zero": "MSL", "rl_minus_msl_A": OFF_A, "equation": "reading A (default): z_AHD (= z_MSL) = z_RL - 0.716 ; reading B (Blacka 2013 wording 'below MSL'): z_MSL = z_RL",
           "note": "The drawing's RL datum is not stated. Reading A: RL = tide-gauge / chart datum (Pitt note, S1 'datum'). Reading B: RL = MSL (Blacka 2013 A.1.1 'crest submergence of 1-2.5 m below MSL'). They differ by 0.716 m; the viewer has a switch. Since 2026-10-13 reading A is supported by the datum definition: AHD 0.000 = MSL 1966-68 at Fremantle = 0.716 m above the Fremantle gauge zero (LWD) (DNM TR12 Table 3), so the offset is 0.716 m (+-0.04 m, Perth metro zone), not the 0.78 m of the 1999 paper (a present-day mean tide level)."},
 "levels": levels, "extra_levels": [], "slider": {"min_id": "DATUM", "max_id": "HWt", "note": "HAT/LAT of Fremantle not found at a primary source; slider spans the tide-gauge datum to typical high water (range 0.8 m, Blacka 2013)."},
 "seabed": {"x0": SBX0, "y0": SBY0, "step": SBS, "nx": snx, "ny": sny, "x1": SBX1, "z": seabed_z},
 "versions": V, "default_version": DEFAULT_VERSION,
 # shape.json's versions_info (written before the survey versions) says the default outline is the design plan; since X2/X9 the default VERSION is the Nov 1999 surveyed surface on that footprint (fixed 2026-10-13)
 "versions_info": SH['versions_info'].replace('The default outline is the original construction design plan', 'The default version is the rock surface surveyed in Nov 1999 (DoT WA soundings), drawn on the footprint of the original construction design plan') + " Four versions are modelled in 3D: the two design-plan versions (design levels of the Lyons plan) and the Nov 1999 and Feb 2002 surveyed surfaces; the Fig 7 and Pitt outlines are plan-only.",
 "contours": cont,
 "roles": {"north": {"label": "North arm (shorter)", "centroid": [-30.0, 280.0]}, "south": {"label": "South arm (longer, extended)", "centroid": [38.0, 262.0]}},
 "crest_labels": [{"text": "crest line RL -1.0 (1.0 m below datum)", "x": 4.0, "y": 268.0, "z": -1.72}, {"text": "set-out line RL -3.0 (apex)", "x": -12.0, "y": 308.0, "z": -3.72}],
 "provenance": [], "confidence_3d": {}, "validation": validation, "photo_match": True,
 "axis_xy": {"head": [-12.0, 312.0], "tail": [60.0, 240.0]},
}
exec(open(HERE + '/provenance.py').read())              # fills M['provenance'], M['confidence_3d'], M['ui'], M['source_names']
js = "/* Generated by build_3d.py (%s). x south, y west (offshore), z in m AHD (taken as MSL) under datum reading A (z = z_RL - 0.716). */ window.REEF_MODEL = %s;\n" % (M['built'], json.dumps(M, separators=(',', ':')))
open(HERE + '/model.js', 'w', encoding='utf-8').write(js)
docs = {}
for k, f in (('methods_md', 'METHODS_3D.md'), ('sources_md', 'SOURCES_3D.md')):
    try: docs[k] = open(HERE + '/' + f, encoding='utf-8').read()
    except FileNotFoundError: pass
open(HERE + '/docs.js', 'w', encoding='utf-8').write("/* Generated by build_3d.py */ window.REEF_DOCS = %s;\n" % json.dumps(docs))
print('model.js bytes', len(js), 'docs keys', list(docs))
