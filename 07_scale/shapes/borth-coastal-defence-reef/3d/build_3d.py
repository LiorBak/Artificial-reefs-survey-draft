"""build_3d.py - regenerate 3d/model.js, 3d/docs.js and 3d/src/build_metrics.json for borth-coastal-defence-reef.
Run from this folder:  python build_3d.py            (model.js + docs.js)
                       python build_3d.py --shape    (additionally write outline_versions / default_outline / versions_info into ../shape.json)
Inputs: ../shape.json, src/*.npz|json (LiDAR windows, design rings/crest, Fig 2 contours), SOURCES_3D.md, METHODS_3D.md,
        src/navionics_reading.json (optional, written by nav_read.py).
Frame: shape.json canonical (x south, y offshore/west, metres); z = 0 at MSL; z_MSL = z_ODN - 0.31 (+-0.15).
Written 2026-10-06 by the 3D agent (Sonnet 5.5)."""
import json, os, sys, base64, math, datetime
import numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union
from pyproj import Transformer
import b3d_lib as L, b3d_reef as R

HERE = L.HERE; SRC = L.SRC
ZOFF = L.ZOFF
BUILT = '2026-10-06'

# -------------------------------------------------------------------------------------------- tides (mODN)
TIDES_ODN = [('LAT', 'LAT = chart datum', -2.44, 'ref4 (NTSLF, Barmouth and Fishguard -2.44 m; Aberystwyth not listed) + ref3 MHWS 5.00 m CD; LiDAR sea surface -2.2..-2.4 mODN', True),
             ('MLWS', 'MLWS', -1.74, 'ref3 (West of Wales SMP2 p.4C.3, Aberystwyth) and printed on drawings 9V5090/1021', False),
             ('MLWN', 'MLWN', -0.64, 'ref3 (SMP2 p.4C.3, Aberystwyth)', False),
             ('MSL', 'MSL (model zero) = +0.31 mODN', 0.31, 'mean of the four ref3 levels (MLWS+MLWN+MHWN+MHWS)/4 = +0.31 mODN, +-0.15 m (estimate)', True),
             ('MHWN', 'MHWN', 1.06, 'ref3 (SMP2 p.4C.3, Aberystwyth)', False),
             ('MHWS', 'MHWS (slider top; HAT not found)', 2.56, 'ref3 and printed on drawings 9V5090/1021 (MHWS +2.56)', False)]
EXTRA_LEVELS_ODN = [('lidar_flight', 'LiDAR flight 19 Mar 2022, water edge (about)', -2.3, 'sea surface read at the rock edge in the Welsh Government DSM (-2.2..-2.4 mODN)', True),
                    ('photo_2024', 'Esri photo 17 Sep 2024, rock waterline (about)', -1.3, 'median LiDAR DSM height along the traced rock edge (N -1.25, S -1.36 mODN)', True)]


def b64(arr, dtype):
    return base64.b64encode(np.ascontiguousarray(arr.astype(dtype)).tobytes()).decode('ascii')


def poly_list(p):
    return [[round(float(x), 2), round(float(y), 2)] for x, y in np.array(p.exterior.coords)]


def to_latlon(frame, polys):
    tf = Transformer.from_crs('EPSG:27700', 'EPSG:4326', always_xy=True)
    out = []
    for p in polys:
        en = frame.can2bng(np.array(p.exterior.coords))
        ll = [tf.transform(e, n) for e, n in en]
        out.append([[round(lat, 7), round(lon, 7)] for lon, lat in ll])
    return out


def main(update_shape=False):
    shape = json.load(open(os.path.join(L.BASE, 'shape.json'), encoding='utf-8'))
    F = L.Frame(shape)
    alt = shape['canonical']['alt_outlines_m']
    poly_ex = [Polygon(alt['lidar_exposed_2022-03-19'][k]) for k in ('north', 'south')]
    poly_dg = [Polygon(alt['armour_foot_design']['north_surf_reef']), Polygon(alt['armour_foot_design']['south_reef'])]
    poly_sat = [Polygon(p) for p in shape['canonical']['polygons_m']]
    ex_union = unary_union(poly_ex)

    # --- design polygons and seabed -------------------------------------------------------------------
    dp = R.design_polys(F)
    mh, ax = dp['axis']
    tail = mh + ax * dp['s']['R3'] * 0.5 + ax * dp['s']['R2'] * 0.5      # mid-point of the tail ramp
    nodes = L.seabed_nodes(F, shape, os.path.join(SRC, 'lidar_beach_SN6089_2022-03-19.npz'), os.path.join(SRC, 'fig2_contours_canonical.json'),
                           ex_union, arm_axis=((float(tail[0]), float(tail[1])), (float(mh[0]), float(mh[1]))))
    sx, sy, Zodn, rbf = L.seabed_grid(nodes)
    # node-fit residuals (design nodes) for METHODS
    fit_res = {}
    for src in sorted(set(n['src'] for n in nodes)):
        ns = [n for n in nodes if n['src'] == src]
        P = np.array([[n['x'], n['y']] for n in ns]); V = np.array([n['z'] for n in ns])
        fit_res[src] = dict(n=len(ns), rms=round(float(np.sqrt(np.mean((rbf(P) - V) ** 2))), 2), mean=round(float(np.mean(rbf(P) - V)), 2))

    # --- fine grids and three surfaces ---------------------------------------------------------------------
    xs, ys, X, Y = R.grid(); zs = R.seabed_at((sx, sy, Zodn), X, Y)
    fl = L.lidar_sampler(F, os.path.join(SRC, 'lidar_window_SN6089_2022-03-19.npz'), 'dsm')
    dsm_s, dsm_raw = R.smooth_dsm(fl, X, Y)
    H1, Z1 = R.outline_surface(X, Y, zs, dsm_s, poly_ex, -2.3)
    H2, Z2 = R.design_surface(X, Y, zs, dp)
    H3, Z3 = R.outline_surface(X, Y, zs, dsm_s, poly_sat, -1.3)

    def metrics(H, Zn, polys, name):
        V = R.volume(H, zs)
        thick = np.where(Zn == 1, np.minimum(2.7, np.maximum(H - zs, 0.0)), 0.0)
        V4 = float(thick.sum())
        area_all = float(np.isfinite(H).sum())
        a = sum(p.area for p in polys)
        # seabed-uncertainty effect on volume: +-0.4 m bed level over the whole rock footprint (incl. toe)
        dV = 0.4 * area_all
        return dict(volume_m3=round(V), area_footprint_m2=round(a), area_incl_toe_m2=round(area_all),
                    volume_type4_layer_m3=round(V4), tonnes=round(V * R.RHO_BULK), tonnes_range=[round(V * 1.6), round(V * 1.8)],
                    tonnes_type4_layer=round(V4 * R.RHO_BULK), volume_unc_bed_m3=round(dV), max_crest_mODN=round(float(np.nanmax(H)), 2))
    M = {'lidar_2022': metrics(H1, Z1, poly_ex, 'lidar'), 'design_1020': metrics(H2, Z2, poly_dg, 'design'), 'sat_2024': metrics(H3, Z3, poly_sat, 'sat')}

    # crest statistics of the LiDAR DSM (for validation tables)
    crestN = dp['crest_N']; crestS = dp['crest_S']
    import shapely
    def inside(poly): return shapely.contains_xy(poly, X, Y)
    stats = {}
    mN = inside(crestN) & np.isfinite(dsm_raw); mS = inside(crestS) & np.isfinite(dsm_raw)
    stats['dsm_crestN_median'] = round(float(np.nanmedian(dsm_raw[mN])), 2); stats['dsm_crestN_p90'] = round(float(np.nanpercentile(dsm_raw[mN], 90)), 2)
    stats['dsm_crestS_median'] = round(float(np.nanmedian(dsm_raw[mS])), 2); stats['dsm_crestS_p90'] = round(float(np.nanpercentile(dsm_raw[mS], 90)), 2)
    stats['design_vs_lidar_above_-2.0'] = None
    mm = np.isfinite(H1) & np.isfinite(H2) & (H2 > -2.0)
    stats['lidar_minus_design_mean_m'] = round(float(np.mean(H1[mm] - H2[mm])), 2); stats['lidar_minus_design_std_m'] = round(float(np.std(H1[mm] - H2[mm])), 2)
    del stats['design_vs_lidar_above_-2.0']
    # seabed under the footprints (mean model seabed, mODN)
    mN_ring = shapely.contains_xy(dp['N'][4], X, Y); mS_ring = shapely.contains_xy(dp['S'][4], X, Y)
    stats['seabed_under_N_foot_mean_mODN'] = round(float(zs[mN_ring].mean()), 2); stats['seabed_under_N_foot_min_max'] = [round(float(zs[mN_ring].min()), 2), round(float(zs[mN_ring].max()), 2)]
    stats['seabed_under_S_foot_mean_mODN'] = round(float(zs[mS_ring].mean()), 2); stats['seabed_under_S_foot_min_max'] = [round(float(zs[mS_ring].min()), 2), round(float(zs[mS_ring].max()), 2)]
    # Fig 2 -3.0 contour crossing at the reef (check)
    for yy in (287.0,):
        stats['model_seabed_at_y287_x-60_x85'] = [round(float(L.bilinear(Zodn, sx[0], sy[0], 5.0, np.array([-60.0, 85.0]), np.array([yy, yy]))[i]), 2) for i in (0, 1)]
    # model minus the Fig 2 contour levels (traced points outside the reef zone) - validation of the seabed
    f2c = json.load(open(os.path.join(SRC, 'fig2_contours_canonical.json')))['contours_mODN']
    for kk in ('-2', '-3', '-4'):
        dd = [float(L.bilinear(Zodn, sx[0], sy[0], 5.0, np.array([px_]), np.array([min(py_, 519.0)]))[0]) - float(kk) for px_, py_ in f2c[kk] if -200 <= px_ <= 260 and not (-115 <= px_ <= 160)]
        stats['model_minus_fig2_%s' % kk] = [round(float(np.mean(dd)), 2), round(float(np.std(dd)), 2), len(dd)]
    # EMODnet comparison at y=368,440,513 (x=-30 axis) mODN
    emod = {368: -0.40, 440: -1.10, 513: -1.91}
    stats['emodnet_vs_model'] = {str(y): dict(emodnet_mODN=round(e - 2.44, 2), model_mODN=round(float(L.bilinear(Zodn, sx[0], sy[0], 5.0, np.array([-30.0]), np.array([float(y)]))[0]), 2)) for y, e in emod.items()}

    # --- Navionics reading (optional) -------------------------------------------------------------------
    nav = None
    pnav = os.path.join(SRC, 'navionics_reading.json')
    if os.path.exists(pnav): nav = json.load(open(pnav, encoding='utf-8'))

    # --- versions ----------------------------------------------------------------------------------------
    def grid_block(H, Zn):
        Hmsl = np.where(np.isfinite(H), H - ZOFF, np.nan)
        cm = np.where(np.isfinite(Hmsl), np.round(Hmsl * 100), -32768).astype(np.int16)
        return dict(x0=float(xs[0]), y0=float(ys[0]), step=R.WSTEP, nx=len(xs), ny=len(ys), h_cm_b64=b64(cm, np.int16), zone_b64=b64(Zn, np.uint8))

    ver_defs = [
        dict(id='lidar_2022', name='Laser survey edge (Welsh Government LiDAR, 19 Mar 2022)', date='2022-03-19', kind='laser_survey',
             source_ids=['lidar2022', 'drg1021', 'drg1022', 'drg1023'], polys=poly_ex, H=H1, Z=Z1, edge=-2.3,
             level='rock exposed at the water level during the flight (about -2.3 mODN)',
             method='1 m LiDAR DSM (lightly smoothed, sigma 0.8 m) inside the exposed-rock outline; below the water edge the Royal Haskoning toe-berm slopes (1:1.5), 2 m flat blanket and 1:1.5 blanket edge (drawings 1021-1023) down to the modelled seabed.',
             note='Default (Lior 2026-10-06: laser survey or rock layer are more accurate than a photo). DSM sees block tops, about 0.1-0.3 m above the design surface.'),
        dict(id='design_1020', name='Design rock-layer foot (Royal Haskoning drawing 9V5090/1020 rev C1, Jan 2011)', date='2011-01', kind='design_drawing',
             source_ids=['drg1020', 'drg1021', 'drg1022', 'drg1023'], polys=poly_dg, H=H2, Z=Z2, edge=R.Z_FOOT,
             level='foot of the Type 4 armour layer = top of the toe berm (about -2.15 mODN)',
             method='Design surface lofted from the crest outline (setting-out points R1-R15, crest levels +0.50 / +1.00 / +0.00 ramp / +1.50) down to the armour foot ring at -2.15 mODN, then the toe berm (1.35 m, 1:1.5), 2 m blanket apron and blanket edge rings of drawing 1020, onto the modelled seabed.',
             note='The as-designed rock layer; the as-built flanks are flatter and 8-10 m wider than the design (LiDAR).'),
        dict(id='sat_2024', name='Visible rock edge (Esri satellite photo, 17 Sep 2024)', date='2024-09-17', kind='photo_trace',
             source_ids=['sat2024', 'lidar2022'], polys=poly_sat, H=H3, Z=Z3, edge=-1.3,
             level='bare rock above the waterline in the photo (about -1.3 mODN from the DSM at the traced edge)',
             method='Traced rock edge (79 vertices) as the footprint; LiDAR DSM inside; design toe slopes below the edge (assumed 1:1.5 from the edge down to the bed, i.e. steeper than the real flanks).',
             note='Smallest footprint: the photo shows only the rock above the water at that tide, so it understates the structure; kept as the traceable photo outline.'),
    ]
    versions = []
    for v in ver_defs:
        m = M[v['id']]
        bbox = np.vstack([np.array(p.exterior.coords) for p in v['polys']])
        versions.append(dict(id=v['id'], name=v['name'], date=v['date'], kind=v['kind'], source_ids=v['source_ids'], method=v['method'], level=v['level'],
                             edge_level_mODN=v['edge'], edge_level_MSL=round(v['edge'] - ZOFF, 2), note=v['note'],
                             area_m2=m['area_footprint_m2'], area_incl_toe_m2=m['area_incl_toe_m2'], volume_m3=m['volume_m3'],
                             volume_unc_m3=m['volume_unc_bed_m3'], tonnes_est=m['tonnes'], tonnes_range=m['tonnes_range'],
                             volume_type4_layer_m3=m['volume_type4_layer_m3'], tonnes_type4_layer=m['tonnes_type4_layer'],
                             bbox_m=[round(float(np.ptp(bbox[:, 0])), 1), round(float(np.ptp(bbox[:, 1])), 1)],
                             outline_m=[poly_list(p) for p in v['polys']], grid=grid_block(v['H'], v['Z'])))
    versions_info = ('Three outlines of the same two rock mounds. Default: the laser-survey edge (Welsh Government LiDAR, flown 19 March 2022 at about the lowest spring tide): the rock exposed at water level, '
                     '8,675 m2, built from the LiDAR surface plus the design toe slopes (a measured surface is more accurate than a photo). Second: the design rock-layer foot of Royal Haskoning drawing 9V5090/1020 (Jan 2011), '
                     '6,989 m2. Third: the visible rock edge in the Esri photo of 17 Sep 2024, 5,743 m2, the outline that was traced first and is kept for traceability. '
                     'Areas differ because the three edges sit at different heights on the same sloping flanks, not because the structure moved.')

    # --- seabed block (MSL) ---------------------------------------------------------------------------------
    sb = dict(x0=float(sx[0]), y0=float(sy[0]), step=5.0, nx=len(sx), ny=len(sy), z=[[round(float(v - ZOFF), 2) for v in row] for row in Zodn])
    levels = [dict(id=i, name=n, z=round(z - ZOFF, 2), z_ODN=z, source=s, estimated=e) for i, n, z, s, e in TIDES_ODN]
    extra = [dict(id=i, name=n, z=round(z - ZOFF, 2), z_ODN=z, source=s, estimated=e) for i, n, z, s, e in EXTRA_LEVELS_ODN]

    # bearings of the frame (for the camera heading read-out and the north arrow)
    bx, by = 179.57, 269.57
    north = [round(math.cos(math.radians(0 - bx)), 5), round(math.cos(math.radians(0 - by)), 5)]   # north in (x,y) canonical components

    mt = (dp['sop']['R3'] + dp['sop']['R4']) / 2; mh0 = (dp['sop']['R1'] + dp['sop']['R10']) / 2
    arm60 = mh + ax * 60.0
    oc = poly_sat[1].centroid
    def cl(text, p, z_odn): return dict(text=text, x=round(float(p[0]), 1), y=round(float(p[1]), 1), z=round(z_odn - ZOFF, 2))
    crest_labels = [cl('head edge +0.00 mODN', mh0, 0.0), cl('arm crest +0.50 mODN (9 m wide)', arm60, 0.5), cl('tail crest +1.00 mODN', mt, 1.0),
                    cl('breakwater crest +1.50 mODN, 6 m wide', (oc.x, oc.y), 1.5)]
    axis_xy = dict(head=[round(float(mh0[0]), 1), round(float(mh0[1]), 1)], tail=[round(float(mt[0]), 1), round(float(mt[1]), 1)])
    prov = provenance(M, stats, nodes, fit_res, nav)
    conf = dict(level='medium', reason=('The plan shape is high-confidence, and the rock surface above the water edge is a 1 m laser survey that agrees with the design crests within about 0.3 m. '
                                        'The seabed is the weak link: the design drawings show a typical bed level of about -4.0 mODN (beds "vary"), the HRPP576 Fig 2 contours are read by eye (+-0.5 m), '
                                        'and the mean-sea-level offset of +0.31 mODN is a four-level estimate (+-0.15 m), so reef height above the bed is known to about +-0.5 m and volumes to about +-15 %.'))
    model = dict(slug='borth-coastal-defence-reef', name='Borth coastal defence reef (Phase 1, Ceredigion, Wales)', built=BUILT,
                 state=('As-built final layout of Phase 1 (completed 8 March 2012; Coflein ref7): northern boot-shaped SURF REEF (crest +0.50 mODN, tail +1.00, head edge +0.00) and southern oval = '
                        'SHORE-PARALLEL BREAKWATER (crest +1.50 mODN), not a surf reef. No later change, damage or removal was found in imagery 2012-2024 or in the 2022 LiDAR.'),
                 frame=dict(x='alongshore, + toward SOUTH (bearing %.2f deg)' % bx, y='offshore, + toward WEST (bearing %.2f deg)' % by, z='up, 0 = MSL', units='m',
                            origin='foot of the perpendicular from the centroid of both mounds on the defence line (back of the shingle beach, bearing 359.57 deg)',
                            bearing_x_deg=bx, bearing_y_deg=by, north_xy=north, shoreline_y=0.0),
                 datum=dict(zero='MSL', msl_mODN=ZOFF, msl_unc=0.15, equation='z_MSL = z_ODN - 0.31 ; z_MSL = e_LAT - 2.75', lat_mODN=-2.44),
                 levels=levels, extra_levels=extra, slider=dict(min_id='LAT', max_id='MHWS', note='HAT was not found at a primary source; the slider top is MHWS (+2.56 mODN = +2.25 m MSL).'),
                 seabed=sb, versions=versions, default_version='lidar_2022', versions_info=versions_info,
                 roles=dict(north=dict(label='SURF REEF (northern, boot-shaped)', centroid=[round(float(poly_sat[0].centroid.x), 1), round(float(poly_sat[0].centroid.y), 1)]),
                            south=dict(label='BREAKWATER (oval, not a surf reef)', centroid=[round(float(poly_sat[1].centroid.x), 1), round(float(poly_sat[1].centroid.y), 1)])),
                 zones={'1': 'armour / surveyed surface (Type 4 rock, 5-8 t)', '2': 'toe berm (Type 0 rock, 8 t)', '3': 'blanket and apron (Type 6 rock, 5-100 kg)'},
                 provenance=prov, confidence_3d=conf, validation=dict(stats=stats, volumes=M, seabed_fit=fit_res),
                 density_t_m3=R.RHO_BULK, nce_type4_t=42000, navionics=nav,
                 photo_match=True, crest_labels=crest_labels, axis_xy=axis_xy)
    with open(os.path.join(HERE, 'model.js'), 'w', encoding='utf-8') as f:
        f.write('/* Generated by build_3d.py (%s). z in metres above MSL; canonical frame x south, y offshore(west). */\nwindow.REEF_MODEL = ' % BUILT)
        json.dump(model, f, separators=(',', ':'))
        f.write(';\n')
    json.dump(dict(M=M, stats=stats, fit_res=fit_res, nodes_n=len(nodes), frame_fit=dict(rms=F.fit_rms, max=F.fit_max)), open(os.path.join(SRC, 'build_metrics.json'), 'w'), indent=1)
    print('model.js', os.path.getsize(os.path.join(HERE, 'model.js')) // 1024, 'kB')
    print(json.dumps(M, indent=0)[:900]); print(stats); print(fit_res)

    # --- docs.js -----------------------------------------------------------------------------------------
    docs = {}
    for key, fn in (('methods_md', 'METHODS_3D.md'), ('sources_md', 'SOURCES_3D.md')):
        p = os.path.join(HERE, fn)
        docs[key] = open(p, encoding='utf-8').read() if os.path.exists(p) else ''
    with open(os.path.join(HERE, 'docs.js'), 'w', encoding='utf-8') as f:
        f.write('window.REEF_DOCS = '); json.dump(docs, f, ensure_ascii=False); f.write(';\n')

    # --- shape.json: outline versions ------------------------------------------------------------------------
    if update_shape:
        shp = os.path.join(L.BASE, 'shape.json')
        shape = json.load(open(shp, encoding='utf-8'))
        ov = []
        for v, vm in zip(ver_defs, versions):
            ov.append(dict(id=v['id'], name=v['name'], date=v['date'], kind=v['kind'], source_ids=v['source_ids'], method=v['method'], level=v['level'],
                           area_m2=vm['area_m2'], bbox_m=vm['bbox_m'], polygons_m=vm['outline_m'], polygons_latlon=to_latlon(F, v['polys']) if v['id'] != 'sat_2024' else shape['geo']['polygons_latlon'],
                           volume_m3_model=vm['volume_m3'], note=v['note']))
        shape['outline_versions'] = ov
        shape['default_outline'] = 'lidar_2022'
        shape['versions_info'] = versions_info
        shape['outline_versions_chosen'] = 'Lior chose the LiDAR default on 2026-10-06 (laser survey or rock layer are more accurate than a photo); canonical.polygons_m stays the traced polygon.'
        json.dump(shape, open(shp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('shape.json updated with outline_versions')


def provenance(M, stats, nodes, fit_res, nav):
    P = []
    def add(parameter, value, unit, src, method, unc, est):
        P.append(dict(parameter=parameter, value=value, unit=unit, source_id=src, method=method, uncertainty=unc, estimated=est))
    add('plan outline, visible rock (version sat_2024)', '5,743 m2, 79 vertices', 'm2', 'sat2024', 'traced on Esri World Imagery 2024-09-17 (bare rock at low tide), frame of shape.json (verified)', '+-5 m position, +-2 m edge', False)
    add('plan outline, laser survey (version lidar_2022, DEFAULT)', '8,675 m2', 'm2', 'lidar2022', 'cells with a LiDAR return on 2022-03-19 (water edge -2.2..-2.4 mODN), 1 m cells, simplified 0.4 m', '+-2 m (1 m cell + Helmert +-2-5 m position)', False)
    add('plan outline, design rock-layer foot (version design_1020)', '6,989 m2', 'm2', 'drg1020', 'ring 4 of the concentric rings of drawing 9V5090/1020 rev C1 georeferenced by its 15 setting-out points (residual 0.02 m)', '+-0.5 m on the drawing; +-2-5 m absolute (OSGB36 to WGS84 Helmert)', False)
    add('crest, northern arm', '+0.50', 'mODN', 'drg1021', 'sections N1-N1, N3-N3 (crest level label)', 'LiDAR DSM in the crest strip: median %+.2f, p90 %+.2f (DSM sees block tops)' % (stats['dsm_crestN_median'], stats['dsm_crestN_p90']), False)
    add('crest, northern tail', '+1.00', 'mODN', 'drg1021', 'section N1-N1 (second): transition 15 m from SOP R2 to +1.00 at SOP R3', 'LiDAR p90 +1.0..+1.15', False)
    add('crest, northern head edge', '+0.00 rising to +0.50 over about 40 m', 'mODN', 'drg1021', 'section N1-N1 (first): SOP R1 +0.00, transition approx. 40 m', 'about 0.2 m', False)
    add('crest, southern oval (breakwater)', '+1.50 (flat top 6 m x 38 m)', 'mODN', 'drg1023', 'section S2 and plan 1020 (SOP R14-R15)', 'LiDAR DSM in the crest strip: median %+.2f, p90 %+.2f' % (stats['dsm_crestS_median'], stats['dsm_crestS_p90']), False)
    add('armour layer (Type 4, 5-8 t) and foot level', '2.7 m thick; foot / toe-berm top about -2.15', 'mODN', 'drg1021', 'section N3-N3 labels; foot = bed -4.0 + 0.5 blanket + 1.35 berm', '+-0.1 m (labels), +-0.05 m measured on a 300 dpi render', False)
    add('side slopes (design)', '1:3 arm and oval, 1:4 mid, 1:5 head, toe berm 1:1.5', 'H:V', 'drg1022', 'slope labels on plan 1020 and sections N4-N6', 'as labelled', False)
    add('side slopes (as built, LiDAR)', '1:4.4 (-1.5..-0.5 mODN), 1:5.3 (-0.5..+0.2) north; 1:4.1 / 1:4.0 oval', 'H:V', 'lidar2022', '5x5 smoothed DSM, median slope by level band (verification, VERIFY.md)', '+-0.5', False)
    add('toe berm and blanket (Type 0 and Type 6)', 'berm 1.35 m high x 3.0 m top, apron 2.0 m, blanket 0.5 m', 'm', 'drg1021', 'sections N1-N3 dimension labels (1350, 3000, 2000, 500)', 'as labelled', False)
    add('seabed under northern arm', '%.2f mean (%.1f..%.1f)' % (stats['seabed_under_N_foot_mean_mODN'], *stats['seabed_under_N_foot_min_max']), 'mODN', 'drg1021', 'drawn layer thicknesses below +0.50: 2.70 + 1.31 + 0.50 = -4.01 (N3); N4 about -3.8; bed lines in sections are schematic (note 4: bed levels vary); tail shallower (assumed)', '+-0.4 m (+-0.6 m at the tail)', True)
    add('seabed under southern oval', '%.2f mean (%.1f..%.1f)' % (stats['seabed_under_S_foot_mean_mODN'], *stats['seabed_under_S_foot_min_max']), 'mODN', 'drg1023', 'note on S2: bed -3.6 to -4.2 mODN (shoreward to seaward); HRPP576 text: C about -3.5', '+-0.4 m', True)
    add('seabed contours around the reefs', '-3.0 contour at about 287 m offshore; -2.0 at about 208 m; -4.0 at about 410-425 m', 'mODN', 'hrpp576f2', 'HRPP576 Fig 2 grey contours digitised and georeferenced via oval C and the 500 m bar; only -3.0 used as seabed node outside the reef zone; the -4.0 contour is not a node: the model is %.2f m deeper than it at its traced points (METHODS_3D 4)' % stats['model_minus_fig2_-4'][0], '+-0.5 m by eye; +-10 m horizontally', True)
    add('bed under the oval, derived from section S1-S1', '-3.4 (centreline)', 'mODN', 'drg1023', '+1.50 top; Type 4 underside -1.20, Type 5 underside -2.90 (labels); Type 6 0.5 m below: -3.4', 'printed range on S2-S2 is -4.2 to -3.6 mODN: derived value 0.2 m shallower', True)
    add('beach and lower foreshore', 'DTM down to the water edge at about -2.3 mODN', 'mODN', 'lidar2022', 'Welsh Government LiDAR DTM 2022-03-19 sampled on a 6 m grid (3,000 nodes), reef cells excluded', '+-0.1 m vertical (DTM); 12 years after the survey of Fig 2', False)
    add('seabed offshore gradient beyond 335 m', '-1.1 % (about 1:90)', '%', 'emodnet', 'EMODnet Bathymetry soundings (CDI 115084) y 368-652 m: -0.40..-3.36 m rel. LAT; used as gradient only, anchored on the design bed level at 335 m; z_MSL = e_LAT - 2.75', '+-0.3 % in slope; the absolute cell values are 1.0-1.4 m shallower than the design bed and are NOT used', True)
    add('datum zero (MSL) in mODN', '+0.31', 'mODN', 'ref3', '(MLWS + MLWN + MHWN + MHWS)/4 of the Aberystwyth row; z_MSL = z_ODN - 0.31', '+-0.15 m', True)
    add('chart datum (LAT) in mODN', '-2.44', 'mODN', 'ref4', 'NTSLF: Barmouth and Fishguard -2.44 m; MHWS 5.00 m CD; LiDAR sea surface at a spring low -2.2..-2.4', '+-0.1 m', True)
    add('MHWS / MHWN / MLWN / MLWS', '+2.56 / +1.06 / -0.64 / -1.74', 'mODN', 'ref3', 'West of Wales SMP2 p.4C.3, Aberystwyth; MHWS and MLWS also printed on drawing 9V5090/1021', 'tabulated', False)
    add('HAT', 'not found', '-', '-', 'not published at a primary source; slider top = MHWS', '-', True)
    add('LiDAR vertical datum', 'ODN assumed', '-', 'lidar2022', 'not stated in the tile; supported by agreement with design crests (oval p90 +1.5 vs +1.50) and the sea surface (-2.2..-2.4 vs LAT -2.44)', '+-0.15 m', True)
    add('rock volume (default version)', '%d m3 = about %d t at %.1f t/m3' % (M['lidar_2022']['volume_m3'], M['lidar_2022']['tonnes'], R.RHO_BULK), 'm3', 'model', 'integral of (surface - seabed) over the 1 m grid, both mounds, including toe berm and blanket', '+-%d m3 (bed level +-0.4 m); density 1.6-1.8 t/m3' % M['lidar_2022']['volume_unc_bed_m3'], True)
    add('stated rock quantity (whole Phase 1)', '275,000 t, of which Type 4 (6-10 t) 42,000 t', 't', 'ref6', 'NCE Borth\'s Big Dig 2011: covers breakwaters, groynes and revetment as well; no reef-only figure exists at a primary source', 'upper bound only', False)
    if nav:
        add('Navionics cross-check', nav.get('summary', ''), 'm', 'navionics', nav.get('method', ''), nav.get('uncertainty', ''), True)
    return P


if __name__ == '__main__':
    main(update_shape='--shape' in sys.argv)
