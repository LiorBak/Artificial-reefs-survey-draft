"""build_3d.py - regenerate 3d/model.js, 3d/docs.js and 3d/src/build_metrics.json for southern-ocean-surf-reef-albany.
Run from this folder:  python -I build_3d.py
Inputs : ../shape.json (two outline versions, canonical frame), src/levels2_raw.json (contour crossings read off the RHDHV 2015 plan, scripts/read_contours.py),
         src/tides_derived.json (scripts/tides_from_dot.py), METHODS_3D.md, REGISTER_3D.md, SOURCES_3D.md.
Frame  : shape.json canonical (metres; +x alongshore toward NNE, bearing 30.26 deg true; +y offshore toward ESE, bearing 120.26 deg); z up, z = 0 at AHD (about MSL).
Model  : seabed = alongshore-uniform profile z_b(y) (contour crossings, see METHODS_3D 3.2); reef = loft between a crest ridge line (level z_c along the ridge) and the toe
         polygon (z = z_b), z = z_c + (z_b - z_c) * (d_c / (d_c + d_t))**N, N calibrated once so the DESIGN outline holds the stated 34,000 m3 (assumption A9).
Written 2026-10-10 by the 3D agent (Sonnet 5.5)."""
import json, os, math, datetime, base64
import numpy as np
import shapely
from shapely.geometry import Polygon, LineString
from scipy.ndimage import gaussian_filter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'src')
BASE = os.path.join(HERE, '..')
BUILT = '2026-10-10'
BETA = 30.26                       # bearing of +x (deg true), shape.json geo.shoreline_bearing_deg

# ---------------------------------------------------------------------------------------------- seabed profile (y from the beach-face line -> z m AHD)
# nodes -1..-7 from the contour crossings (src/levels2_raw.json, medians over 10 shore-normal transects, deeper ones adjusted by eye, see METHODS 3.2);
# landward of the -0.5 contour and seaward of -7: ASSUMED (A4, A5)
PROFILE = [(-60, 2.0), (-30, 1.0), (7, -0.5), (36, -1.0), (50, -1.5), (64, -2.0), (75, -2.5), (88, -3.0), (98, -3.5), (105, -4.0), (118, -4.5), (126, -5.0),
           (150, -6.0), (178, -7.0), (250, -7.5), (330, -8.0), (420, -8.3)]
PY = np.array([p[0] for p in PROFILE], float); PZ = np.array([p[1] for p in PROFILE], float)
BED_SHIFT = 0.0                    # + = bed deeper (sensitivity runs only)


def zb(y, shift=None):
    return np.interp(y, PY, PZ) - (BED_SHIFT if shift is None else shift)


# ---------------------------------------------------------------------------------------------- reef surface
CREST = dict(z_peak=-1.0, z_main=-2.0, peak_len=15.0, ramp_end=40.0, offset=9.0)     # A7: ridge levels measured from the EAST (offshore) end of the ridge


def ridge_line(pts, nchain, offset):
    P = Polygon(pts); L = LineString(pts[:nchain])
    for side in ('left', 'right'):
        Li = L.parallel_offset(offset, side)
        if Li.geom_type != 'LineString':
            Li = max(Li.geoms, key=lambda g: g.length)
        if P.contains(Li.interpolate(0.5, normalized=True)):
            return P, Li
    raise RuntimeError('ridge offset failed')


SLOPE_MAX = 0.5      # A8: no toe slope steeper than 1:2 (H <= 0.5 * distance to the toe line)


def reef_grid(pts, nchain, N, shift=0.0, crest=CREST, step=1.0, x0=-80.0, y0=50.0, nx=160, ny=200, smooth=1.2, slope_max=SLOPE_MAX):
    P, Li = ridge_line(pts, nchain, crest['offset'])
    Ls = Li.length
    xs = x0 + (np.arange(nx) + 0.5) * step; ys = y0 + (np.arange(ny) + 0.5) * step
    X, Y = np.meshgrid(xs, ys)
    inside = shapely.contains_xy(P, X, Y)
    pts_ = shapely.points(X[inside], Y[inside])
    dt = shapely.distance(P.exterior, pts_); dc = shapely.distance(Li, pts_)
    sd = np.array([Li.project(p) for p in pts_]); sE = Ls - sd
    zc = np.interp(sE, [0, crest['peak_len'], crest['ramp_end'], Ls + 1], [crest['z_peak'], crest['z_peak'], crest['z_main'], crest['z_main']])
    b = zb(Y[inside], shift)
    z = zc + (b - zc) * (dc / (dc + dt + 1e-9)) ** N
    z = np.maximum(z, b)
    hh = np.minimum(z - b, slope_max * dt) if slope_max else z - b
    H = np.zeros_like(X); H[inside] = hh            # height above bed
    if smooth:
        w = gaussian_filter(inside.astype(float), smooth); Hs = gaussian_filter(H, smooth) / np.maximum(w, 1e-6)
        H = np.where(inside, Hs, 0.0); H = np.minimum(H, np.where(inside, 99, 0))
    vol = float(H.sum() * step * step)
    Zs = np.where(inside, zb(Y, shift) + H, np.nan)
    return dict(xs=xs, ys=ys, H=H, inside=inside, vol=vol, area=float(P.area), Zs=Zs, ridge=np.array(Li.coords), Ls=Ls, P=P, hmax=float(H.max()), hmean=float(H[inside].mean()))


def calibrate_N(pts, nchain, target=34000.0):
    lo, hi = 0.8, 12.0
    for _ in range(40):
        mid = (lo + hi) / 2
        v = reef_grid(pts, nchain, mid)['vol']
        if v < target: lo = mid
        else: hi = mid
    return (lo + hi) / 2


def b64(a, dt):
    return base64.b64encode(np.ascontiguousarray(a.astype(dt)).tobytes()).decode('ascii')


def main():
    shape = json.load(open(os.path.join(BASE, 'shape.json'), encoding='utf-8'))
    ver = {v['id']: v for v in shape['outline_versions']}
    des = ver['design_bluecoast']['polygons_m'][0]; sat = ver['sat_2026']['polygons_m'][0]
    NCH = {'design_bluecoast': 8, 'sat_2026': 6}
    N = calibrate_N(des, NCH['design_bluecoast'])
    tides = json.load(open(os.path.join(SRC, 'tides_derived.json')))
    LAT = -round(tides['mean_all_m'], 2)                # z of LAT in m AHD (AHD assumed = MSL = LAT + mean of the extremes)
    HAT_pred = round(tides['max_m'] + LAT, 2)
    dens = 62800 / 34000.0

    metrics = {'N_shape_exponent': round(N, 3), 'density_t_m3': round(dens, 3), 'LAT_AHD': LAT, 'HAT_pred_AHD': HAT_pred}
    versions = []
    defs = [('design_bluecoast', 'Bluecoast final design, outer contour (design stage, volume on 2017 bathymetry)', 'design stage, before the March - June 2025 rock placement', ['design_plan', 'design_table', 'rhdhv2015', 'eia2018'],
             'Toe polygon = outermost contour of the Bluecoast plan (shape.json design_bluecoast). Seabed from the RHDHV 2015 contour profile. Crest ridge 9 m inside the steep shoreward edge, -1.0 m AHD at the offshore (east) end, -2.0 m AHD along the rest; surface lofted between crest and toe with exponent N calibrated so the volume is the stated 34,000 m3.'),
            ('sat_2026', 'Visible reef on Esri satellite 2026-01-20 (as seen from above)', '2026-01-20', ['sat2026', 'design_table', 'rhdhv2015', 'eia2018'],
             'Toe polygon = traced dark rock patch on the 2026-01-20 image (shape.json sat_2026). Same seabed, crest rule and exponent N as the design version (not re-fitted); volume is therefore a result, not a fit.')]
    for vid, name, date, srcs, method in defs:
        pts = ver[vid]['polygons_m'][0]; nch = NCH[vid]
        G = reef_grid(pts, nch, N)
        # sensitivities (no re-calibration)
        sens = {}
        for lab, kw in (('bed_deeper_1m', dict(shift=1.0)), ('bed_shallower_1m', dict(shift=-1.0)),
                        ('bed_deeper_0.74m_if_LAT', dict(shift=0.74)),
                        ('crest_all_-1.0', dict(crest=dict(CREST, z_main=-1.0))), ('crest_all_-2.0', dict(crest=dict(CREST, z_peak=-2.0))),
                        ('ridge_offset_5m', dict(crest=dict(CREST, offset=5.0))), ('ridge_offset_14m', dict(crest=dict(CREST, offset=14.0)))):
            sens[lab] = round(reef_grid(pts, nch, N, **kw)['vol'])
        G1 = reef_grid(pts, nch, 1.0)
        poly_o = [[round(float(x), 2), round(float(y), 2)] for x, y in pts]
        H = G['H']; Hcm = np.round(np.where(G['inside'], H, -327.68) * 100).astype(np.int16)
        Hcm[~G['inside']] = -32768
        vol = G['vol']; unc = max(abs(sens['bed_deeper_1m'] - vol), abs(sens['bed_shallower_1m'] - vol))
        # crest area above -2 m AHD (surface) as a check on the design table statement "110 m crest at -2 m"
        Z = G['Zs']; above2 = float(np.nansum(Z > -2.0) * 1.0)
        v = dict(id=vid, name=name, date=date, kind='design_drawing' if vid.startswith('design') else 'satellite_trace', source_ids=srcs, method=method,
                 level='toe = seabed (z_b); crest ridge -1.0 / -2.0 m AHD (design table)', edge_level_MSL=None, area_m2=round(G['area']), volume_m3=round(vol), volume_unc_m3=round(unc),
                 tonnes_est=round(vol * dens), tonnes_range=[round((vol - unc) * dens), round((vol + unc) * dens)], max_height_m=round(G['hmax'], 2), note=('DEFAULT. Design drawing of the built version; volume fitted to the stated 34,000 m3.' if vid.startswith('design') else 'Result, not a fit: same seabed, crest rule and exponent as the design version.'), mean_height_m=round(G['hmean'], 2),
                 volume_unfitted_loft_N1=round(G1['vol']), sensitivities_m3=sens, area_above_minus2_m2=round(above2),
                 ridge_xy=[[round(float(a), 2), round(float(b), 2)] for a, b in G['ridge']], ridge_length_m=round(G['Ls'], 1),
                 bbox_m=[round(float(np.ptp([p[0] for p in pts])), 1), round(float(np.ptp([p[1] for p in pts])), 1)], outline_m=[poly_o],
                 grid=dict(x0=-80.0, y0=50.0, step=1.0, nx=160, ny=200, h_cm_b64=b64(Hcm, np.int16), zone_b64=b64(np.where(G['inside'], 1, 0), np.uint8)))
        versions.append(v)
        if vid == 'design_bluecoast':   # 2026-10-13 sensitivity only (not in model.js): press/ABC quote 70,000 t; City design table 62,800 t
            N70 = calibrate_N(pts, nch, target=70000 / dens); G70 = reef_grid(pts, nch, N70)
            sens70 = dict(target_t=70000, target_m3=round(70000 / dens), N=round(N70, 2), volume_m3=round(G70['vol']), max_height_m=round(G70['hmax'], 2), mean_height_m=round(float(G70['hmean']), 2) if 'hmean' in G70 else None)
        metrics[vid] = {k: v[k] for k in ('area_m2', 'volume_m3', 'volume_unc_m3', 'tonnes_est', 'max_height_m', 'mean_height_m', 'volume_unfitted_loft_N1', 'sensitivities_m3', 'ridge_length_m', 'area_above_minus2_m2')}
        if vid == 'design_bluecoast': metrics[vid]['if_built_70000_t'] = sens70
        # bed depth at key points of the outline (m AHD)
        ys_ = np.array([p[1] for p in pts]); metrics[vid]['bed_at_outline_y_min_max'] = [round(float(zb(ys_.min())), 2), round(float(zb(ys_.max())), 2)]
    # ---- seabed grid
    x0, y0, step, nx, ny = -260.0, -60.0, 5.0, 105, 97
    sx = x0 + np.arange(nx) * step; sy = y0 + np.arange(ny) * step
    Zb = np.round(np.tile(zb(sy)[:, None], (1, nx)), 2)
    levels = [dict(id='LAT', name='LAT (chart datum), derived', z=LAT, source='dot_tides + assumption A2 (AHD = MSL = LAT + mean of 2024 predicted extremes %.2f m)' % tides['mean_all_m'], estimated=True),
              dict(id='MLLW', name='MLLW (City of Albany, from the crest statement)', z=-0.26, source='city_page: crest -1.0 m AHD = 0.74 m below MLLW', estimated=False),
              dict(id='MSL', name='AHD (model zero, taken as MSL)', z=0.0, source='assumption A2', estimated=True),
              dict(id='MHHW', name='MHHW (City of Albany, from the crest statement)', z=0.34, source='city_page: crest -1.0 m AHD = 1.34 m below MHHW', estimated=False),
              dict(id='HAT', name='highest PREDICTED tide of 2024 (HAT proxy; slider top)', z=HAT_pred, source='dot_tides: 2024 maximum predicted %.2f m above LAT; true HAT not found' % tides['max_m'], estimated=True)]
    prov = json.load(open(os.path.join(SRC, 'provenance.json'), encoding='utf-8')) if os.path.exists(os.path.join(SRC, 'provenance.json')) else []
    conf = json.load(open(os.path.join(SRC, 'confidence.json'), encoding='utf-8')) if os.path.exists(os.path.join(SRC, 'confidence.json')) else dict(level='low', reason='tbd')
    th = math.radians(BETA)
    # true north in canonical (x,y): north = e_N ; x axis = (sin b, cos b) in (E,N), y axis = (sin(b+90), cos(b+90))
    north_xy = [round(math.cos(th), 4), round(math.cos(th + math.pi / 2), 4)]
    ctr = Polygon(des).centroid
    model = dict(slug='southern-ocean-surf-reef-albany', name='Southern Ocean Surf Reef ("Midds Reef"), Middleton Beach, Albany WA', built=BUILT,
                 state='As built (rock placed 18 March - June 2025, opened 16 July 2025; a May 2025 storm moved some core rock before armouring and 18 high rocks were repositioned in late February 2026 = notes only). Plan = Bluecoast design outline (default) or the visible reef on Esri 2026-01-20; heights = design crest levels over a seabed read from 2015 design contours (LOW confidence, see Methods).',
                 frame=dict(x='alongshore, + toward NNE (bearing %.2f deg true)' % BETA, y='offshore, + toward ESE (bearing %.2f deg true)' % (BETA + 90), z='up, 0 = AHD (about MSL)', units='m',
                            origin='foot of the perpendicular from the traced reef centroid onto the beach-face line (edge of bright dry sand, Esri 2026-01-20); lat/lon -35.0172584, 117.919428',
                            bearing_x_deg=BETA, bearing_y_deg=BETA + 90, north_xy=north_xy, shoreline_y=0.0),
                 datum=dict(zero='AHD (taken as MSL)', msl_mODN=0.0, lat_AHD=LAT, equation='z_AHD = model z ; depth below LAT = -(z) + %.2f ; z_AHD = -(depth below CD) + %.2f if CD = LAT' % (LAT, LAT)),
                 levels=levels, extra_levels=[], slider=dict(min_id='LAT', max_id='HAT', note='HAT proper was not found; the slider top is the highest predicted tide of 2024. Storm surge adds 0.4-1.0 m (EIA 2018 s.5, from RHDHV 2015a).'),
                 seabed=dict(x0=x0, y0=y0, step=step, nx=nx, ny=ny, x1=x0 + (nx - 1) * step, y1=y0 + (ny - 1) * step, z=Zb.tolist(), profile=[list(p) for p in PROFILE]),
                 versions=versions, default_version='design_bluecoast',
                 versions_info='Two outlines of the same rock reef. Default: the Bluecoast final-design outer contour (13,104 m2, a design drawing of the built version, positioned on the satellite image; no measured as-built survey was found). Toggle: the dark rock patch visible on the Esri satellite image of 2026-01-20 (10,918 m2, about 17 % smaller because the soft toe edge is not visible from above). Heights are modelled the same way in both.',
                 roles=dict(main=dict(label='Southern Ocean Surf Reef', centroid=[round(ctr.x, 1), round(ctr.y, 1)])),
                 zones={'1': 'armour / surface rock (a single surface; belly D50 0.16 m, core 0.49 m, armour 0.94 m layers are not modelled separately)'},
                 provenance=prov, confidence_3d=conf, validation=metrics, density_t_m3=round(dens, 3), photo_match=True,
                 crest_labels=[dict(text='crest -1.0 m AHD (peak, design)', x=round(float(versions[0]['ridge_xy'][-1][0]), 1), y=round(float(versions[0]['ridge_xy'][-1][1]), 1), z=-1.0),
                               dict(text='crest -2.0 m AHD (110 m of crest, design)', x=round(float(versions[0]['ridge_xy'][len(versions[0]['ridge_xy']) // 2][0]), 1), y=round(float(versions[0]['ridge_xy'][len(versions[0]['ridge_xy']) // 2][1]), 1), z=-2.0)],
                 axis_xy=dict(head=[round(float(versions[0]['ridge_xy'][-1][0]), 1), round(float(versions[0]['ridge_xy'][-1][1]), 1)], tail=[round(float(versions[0]['ridge_xy'][0][0]), 1), round(float(versions[0]['ridge_xy'][0][1]), 1)]))
    open(os.path.join(HERE, 'model.js'), 'w', encoding='utf-8').write('window.REEF_MODEL = ' + json.dumps(model, separators=(',', ':')) + ';\n')
    json.dump(metrics, open(os.path.join(SRC, 'build_metrics.json'), 'w'), indent=1)
    # ---- docs.js
    docs = {}
    for key, fn in (('methods_md', 'METHODS_3D.md'), ('register_md', 'REGISTER_3D.md'), ('sources_md', 'SOURCES_3D.md')):
        p = os.path.join(HERE, fn)
        if os.path.exists(p): docs[key] = open(p, encoding='utf-8').read()
    open(os.path.join(HERE, 'docs.js'), 'w', encoding='utf-8').write('window.REEF_DOCS = ' + json.dumps(docs) + ';\n')
    print(json.dumps(metrics, indent=1)[:2500])


if __name__ == '__main__':
    main()
