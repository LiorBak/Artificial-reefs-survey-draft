"""cables-reef-wa: build model.js + docs.js. Run from anywhere: python3 build_3d.py
Inputs: ../shape.json, ../scripts/computed.json, ../scripts/a2_trace.json, METHODS_3D.md, SOURCES_3D.md (docs). numpy/scipy/skimage/shapely only.
Frame of model.js: x = alongshore, + toward SOUTH (x_model = -x_canonical of shape.json) so that (x, y west, z up) is right-handed in three.js; y = offshore, + toward WEST;
z (reef/seabed grids) = metres relative to MSL under datum reading A (z_MSL = z_RL - 0.78); RL values are kept as z_RL in the contours and provenance."""
import base64, json, sys, datetime
import numpy as np
from scipy import ndimage as ndi
from scipy.optimize import brentq
from skimage import measure
sys.path.insert(0, __file__.rsplit('/', 1)[0]); import b3d_lib as L
HERE = L.HERE
OFF_A = 0.78                       # S1 p.3: mean tide level 0.78 m above datum -> z_MSL = z_RL - 0.78 (reading A)
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
def vol(sil, D0):
    bed_fn = lambda x, y: -(D0 + (y - Y_REF) * G_BED)
    withext = bool((sil & EXT).any())
    xx, yy, bed, surf, band = L.surfaces(sil, ramp, zr, bed_fn, ext_mask=(EXT & sil) if withext else None, ext_volume=320.0 if withext else None)
    V, t = L.volume(surf, bed); return V, xx, yy, bed, surf, band, t
D0 = brentq(lambda d: vol(sil_a, d)[0] - V_TARGET, 2.0, 6.0)
D0_by_volume = {str(v): round(brentq(lambda d: vol(sil_a, d)[0] - v, 1.5, 7.0), 2) for v in (3500, 5000, 5500)}
print('D0', round(D0, 3), D0_by_volume)
bed_fn = lambda x, y: -(D0 + (y - Y_REF) * G_BED)
# ---- per-version grids
def to_b64(a, dt): return base64.b64encode(a.astype(dt).tobytes()).decode()
def version_entry(vid, name, date, kind, srcs, method, level, key, note, sil):
    out = {"id": vid, "name": name, "date": date, "kind": kind, "source_ids": srcs, "method": method, "level": level, "note": note}
    poly_c = np.array(CO[key]); poly_m = [[round(-x, 2), round(y, 2)] for x, y in poly_c]
    out['outline_m'] = [poly_m]; out['area_m2'] = round(float(__import__('shapely.geometry', fromlist=['Polygon']).Polygon(poly_m).area), 0)
    b = np.array(poly_m); out['bbox_m'] = [round(float(np.ptp(b[:, 0])), 0), round(float(np.ptp(b[:, 1])), 0)]
    if sil is None:
        out['grid'] = None; out['volume_m3'] = None; out['volume_unc_m3'] = None; out['edge_level_MSL'] = round(float(np.mean([bed_fn(0, y) for y in b[:, 1]])) - OFF_A, 2)
        return out
    V, xx, yy, bed, surf, band, t = vol(sil, D0)
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
    out['edge_level_MSL'] = round(float(np.mean([bed_fn(0, y) for y in b[:, 1]])) - OFF_A, 2)
    out['crest_rl_m'] = -1.0; out['mean_thickness_m'] = round(V / float(sil.sum() * L.STEP ** 2), 2); out['max_thickness_m'] = round(float(np.nanmax(t)), 2)
    return out
V = []
for vid, key, sil in (('design_plan_plus_extension_1999', 'v_asbuilt_m', sil_a), ('design_plan_original_1999', 'v_orig_m', sil_o), ('paper_fig7_site_plan_1999', 'fig7_m', None), ('pitt_concept_sketch', 'pitt_m', None)):
    s = vers_src[vid]
    e = version_entry(vid, s['name'], s['date'], s['kind'], s['source_ids'], s['method'], s['level'], key, s['note'], sil); V.append(e)
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
# ---- seabed grid (plane), model frame
SBX0, SBX1, SBY0, SBY1, SBS = -150.0, 150.0, 190.0, 420.0, 5.0
snx, sny = int((SBX1 - SBX0) / SBS) + 1, int((SBY1 - SBY0) / SBS) + 1
seabed_z = [[round(float(bed_fn(0, SBY0 + j * SBS)) - OFF_A, 2) for i in range(snx)] for j in range(sny)]
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
dflt = V[0]; orig = V[1]
bed_range = [round(float(-bed_fn(0, y)), 2) for y in (CO['v_asbuilt_m'] and [min(p[1] for p in CO['v_asbuilt_m']), max(p[1] for p in CO['v_asbuilt_m'])])]
validation = {"D0_bed_depth_at_y270_RL": round(D0, 3), "D0_for_stated_volumes": D0_by_volume, "bed_gradient": "1:30 (Pitt sketch 1:28-1:33)",
  "bed_depth_under_footprint_RL_m": {"shoreward_edge_y": bed_range[0], "offshore_edge_y": bed_range[1], "text_water_depth": "3.0-6.0 m (Blacka Table 4.2, RWR)", "water_depth_at_MSL_reading_A": [round(bed_range[0] + OFF_A, 2), round(bed_range[1] + OFF_A, 2)], "water_depth_at_MSL_reading_B": [bed_range[0], bed_range[1]]},
  "S1_7m_contour_at_350m_model_depth_RL": round(float(-bed_fn(0, 350.0)), 2),
  "contour_check_centreline": chk, "contour_check_rms_m": rms, "contour_check_transects": tchk,
  "volumes": {"default_model": dflt['volume_m3'], "original_model": orig['volume_m3'], "stated_Blacka_A13": 5500, "stated_P3_ICM": 5000, "stated_Wikipedia": 3500, "extension_text_m3": 320,
              "implied_density_t_m3_if_10000_t": round(10000 / dflt['volume_m3'], 2)},
  "mean_thickness_m": dflt['mean_thickness_m'], "max_thickness_m": dflt['max_thickness_m']}
sys.path.insert(0, HERE)
levels = [
 {"id": "DATUM", "name": "Design / tide-gauge datum (chart datum, low-water mark)", "z": -0.78, "rl": 0.0, "source": "S1 p.3: wave-basin sea level 'mean tide level of 0.78 m above datum'; Pitt sketch note: 0.0 on the tide gauge", "estimated": False},
 {"id": "LWt", "name": "Typical low water (MSL - 0.4 m)", "z": -0.40, "rl": 0.38, "source": "Blacka 2013 Table 4.3: tide range 0.8 m; half range taken as +-0.4 m (estimate)", "estimated": True},
 {"id": "MSL", "name": "Mean sea level (mean tide level 0.78 m above datum)", "z": 0.0, "rl": 0.78, "source": "S1 p.3 (MTL taken as MSL)", "estimated": False},
 {"id": "HWt", "name": "Typical high water (MSL + 0.4 m)", "z": 0.40, "rl": 1.18, "source": "Blacka 2013 Table 4.3: tide range 0.8 m (estimate)", "estimated": True},
]
M = {
 "slug": "cables-reef-wa", "name": "Cable Station artificial surfing reef (Cables Reef, Cottesloe / Leighton, Perth, Western Australia)", "built": datetime.date.today().isoformat(),
 "state": "Design state of the 1999 reef: Lyons (1992) design plan with the southern-arm extension, drawn at its design levels (RL -1.0 crest to -3.0 outer edge). No survey of the built reef was found; later changes are notes only.",
 "frame": {"x": "alongshore, + toward SOUTH (x_model = -x_canonical)", "y": "offshore, + toward WEST", "z": "up, 0 = MSL (reading A)", "units": "m", "origin": "shoreline point nearest the reef centroid; shoreline assumed N-S; centroid of the default footprint 270 m offshore",
           "bearing_x_deg": 180.0, "bearing_y_deg": 270.0, "north_xy": [-1.0, 0.0], "shoreline_y": 0.0},
 "datum": {"zero": "MSL", "rl_minus_msl_A": OFF_A, "equation": "reading A (default): z_MSL = z_RL - 0.78 ; reading B (Blacka 2013 wording 'below MSL'): z_MSL = z_RL",
           "note": "The drawing's RL datum is not stated. Reading A: RL = tide-gauge / chart datum (Pitt note, S1 'datum'). Reading B: RL = MSL (Blacka 2013 A.1.1 'crest submergence of 1-2.5 m below MSL'). They differ by 0.78 m; the viewer has a switch."},
 "levels": levels, "extra_levels": [], "slider": {"min_id": "DATUM", "max_id": "HWt", "note": "HAT/LAT of Fremantle not found at a primary source; slider spans the tide-gauge datum to typical high water (range 0.8 m, Blacka 2013)."},
 "seabed": {"x0": SBX0, "y0": SBY0, "step": SBS, "nx": snx, "ny": sny, "x1": SBX1, "z": seabed_z},
 "versions": V, "default_version": "design_plan_plus_extension_1999", "versions_info": SH['versions_info'] + " Only the first two are modelled in 3D (they carry the design levels of the Lyons plan); the Fig 7 and Pitt outlines are plan-only.",
 "contours": cont,
 "roles": {"north": {"label": "North arm (shorter)", "centroid": [-30.0, 280.0]}, "south": {"label": "South arm (longer, extended)", "centroid": [38.0, 262.0]}},
 "crest_labels": [{"text": "crest line RL -1.0 (1.0 m below datum)", "x": 4.0, "y": 268.0, "z": -1.78}, {"text": "set-out line RL -3.0 (apex)", "x": -12.0, "y": 308.0, "z": -3.78}],
 "provenance": [], "confidence_3d": {}, "validation": validation, "photo_match": True,
 "axis_xy": {"head": [-12.0, 312.0], "tail": [60.0, 240.0]},
}
exec(open(HERE + '/provenance.py').read())              # fills M['provenance'], M['confidence_3d'], M['ui'], M['source_names']
js = "/* Generated by build_3d.py (%s). x south, y west (offshore), z in m relative to MSL under datum reading A (z_MSL = z_RL - 0.78). */ window.REEF_MODEL = %s;\n" % (M['built'], json.dumps(M, separators=(',', ':')))
open(HERE + '/model.js', 'w', encoding='utf-8').write(js)
docs = {}
for k, f in (('methods_md', 'METHODS_3D.md'), ('sources_md', 'SOURCES_3D.md')):
    try: docs[k] = open(HERE + '/' + f, encoding='utf-8').read()
    except FileNotFoundError: pass
open(HERE + '/docs.js', 'w', encoding='utf-8').write("/* Generated by build_3d.py */ window.REEF_DOCS = %s;\n" % json.dumps(docs))
print('model.js bytes', len(js), 'docs keys', list(docs))
