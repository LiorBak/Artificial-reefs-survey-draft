"""build_3d.py - regenerate 3d/model.js, 3d/docs.js and 3d/src/build_metrics.json for narrowneck-gold-coast.
Run from this folder:  python prep_multibeam.py   (once; Corbett Fig 3 -> src/multibeam_fig3.npz)
                       python build_3d.py          (model.js + docs.js)
Inputs: ../shape.json (outline_versions, canonical polygons), src/multibeam_fig3.npz, METHODS_3D.md, SOURCES_3D.md.
Frame: shape.json canonical (x alongshore bearing 356.2, y offshore bearing 86.2, metres); z = 0 at MSL; z_MSL = z_AHD - 0.12 (MSQ, +-0.25 datum ambiguity).
Written 2026-10-10 by the stage-2 3D agent (Sonnet 5.5)."""
import json, os, sys, base64, math
import numpy as np
from shapely.geometry import Polygon
from scipy import ndimage as ndi
import nn_lib as L

HERE = L.HERE; SRC = L.SRC
BUILT = '2026-10-10'
A_MSQ = 0.12            # MSL = AHD + 0.12 (MSQ: AHD = LAT + 0.760, MSL = LAT + 0.88)
LEVELS = [('LAT', 'LAT = chart datum', -0.88, 'MSQ 2026 Semidiurnal tidal planes, Gold Coast Seaway: MSL = LAT + 0.88', False),
          ('MLWS', 'MLWS', -0.66, 'MSQ 2026: LAT + 0.22', False), ('MLWN', 'MLWN', -0.37, 'MSQ 2026: LAT + 0.51', False),
          ('MSL', 'MSL (model zero)', 0.0, 'MSQ 2026: LAT + 0.88', False), ('MHWN', 'MHWN', 0.36, 'MSQ 2026: LAT + 1.24', False),
          ('MHWS', 'MHWS', 0.65, 'MSQ 2026: LAT + 1.53', False), ('HAT', 'HAT', 1.15, 'MSQ 2026: LAT + 2.03', False)]
EXTRA = [('AHD', 'AHD zero (MSQ: LAT + 0.76)', -0.12, 'MSQ 2014 Standard port datum levels, Gold Coast Seaway: AHD = LAT + 0.760 (papers imply LAT + 1.00: see METHODS 3.1)', False)]
CREST_AS_BUILT = -2.2   # m AHD, measured shallowest crest after the 2018 renewal (Vieira da Silva 2021 AM p.5)
CREST_DESIGN = -2.5     # m AHD, design crest (Jackson 2007; Corbett 2023 p.3)
H_MIN_VISIBLE = 1.0     # m, minimum height of a visible container above the bed (multibeam relief, METHODS 3.2; estimated)
TOP_CAP = -1.8         # m AHD, shallowest container top in the 2017 multibeam (south arm; north arm -2.5)
H_SINGLE = 1.8          # m, isolated single container (channel containers, wing patches): multibeam relief p99 1.7 m (estimated)


def b64(a, dt): return base64.b64encode(np.ascontiguousarray(a.astype(dt)).tobytes()).decode('ascii')
def pl(p): return [[round(float(x), 2), round(float(y), 2)] for x, y in np.array(p.exterior.coords)]


def load_mb(xs, ys):
    Z = np.load(os.path.join(SRC, 'multibeam_fig3.npz')); out = {}
    for k in ('D', 'R', 'bed'):
        A = np.full((len(ys), len(xs)), np.nan)
        i0 = int(round(Z['xs'][0] - xs[0])); j0 = int(round(Z['ys'][0] - ys[0]))
        A[j0:j0 + len(Z['ys']), i0:i0 + len(Z['xs'])] = Z[k]; out[k] = A
    out['ys'] = Z['ys']; out['xs'] = Z['xs']; out['bed_win'] = Z['bed']
    return out


def seabed(mb):
    """5 m grid x -250..250, y -40..520 (m AHD): alongshore-uniform profile b(y) blended with the multibeam bed inside its window."""
    sx = np.arange(-250, 251, 5.0); sy = np.arange(-40, 521, 5.0); SX, SY = np.meshgrid(sx, sy)
    prof, ctrl = L.seabed_profile(dict(ys=mb['ys'], bed=mb['bed_win']))
    base = prof(SY)
    Z = np.load(os.path.join(SRC, 'multibeam_fig3.npz'))
    bed = Z['bed'].astype(float); xs_w, ys_w = Z['xs'], Z['ys']
    from scipy.ndimage import map_coordinates
    ok = np.isfinite(bed)
    idx = ndi.distance_transform_edt(~ok, return_distances=False, return_indices=True)
    bedf = ndi.gaussian_filter(bed[tuple(idx)], 3)                       # NaN cells filled by the nearest valid cell before smoothing
    dist_in = ndi.distance_transform_edt(ok)                             # distance to the edge of the valid map area (px = m)
    u = (SX - xs_w[0]); v = (SY - ys_w[0])
    uu = np.clip(np.round(u).astype(int), 0, len(xs_w) - 1); vv = np.clip(np.round(v).astype(int), 0, len(ys_w) - 1)
    inside = (u >= 0) & (u <= len(xs_w) - 1) & (v >= 0) & (v <= len(ys_w) - 1) & ok[vv, uu]
    w = np.clip(dist_in[vv, uu] / 15.0, 0, 1) * inside
    s = map_coordinates(bedf, [np.clip(v, 0, len(ys_w) - 1), np.clip(u, 0, len(xs_w) - 1)], order=1)
    Zs = np.where(inside, w * s + (1 - w) * base, base)
    return sx, sy, Zs, prof, ctrl


def bil(sx, sy, Z, x, y):
    return ndi.map_coordinates(Z, [(np.asarray(y) - sy[0]) / (sy[1] - sy[0]), (np.asarray(x) - sx[0]) / (sx[1] - sx[0])], order=1, mode='nearest')


def main():
    shape = json.load(open(os.path.join(L.BASE, 'shape.json'), encoding='utf-8'))
    xs, ys, X, Y = L.grid(); mb = load_mb(xs, ys)
    sx, sy, Zs, prof, ctrl = seabed(mb)
    Sg = bil(sx, sy, Zs, X, Y)                       # seabed on the reef grid, m AHD
    V = {v['id']: v for v in shape['outline_versions']}
    P = lambda vid, key='polygons_m': [Polygon(p) for p in V[vid][key]]

    def surface(vid, crest, loops_from, kind):
        polys = P(vid)
        m = L.mask_of(polys, X, Y)
        loops = P(loops_from, 'crest_loops_m'); env = P(loops_from)
        Zc, _ = L.design_top(loops, env, X, Y)
        Zc = Zc + (crest - L.Z_CREST)                # shift the whole surface to the crest level of this version
        top = Zc.copy()
        if kind == 'photo':                          # visible containers: at least one layer above the bed; isolated ones = one layer
            top = np.maximum(top, Sg + H_MIN_VISIBLE)
            iso = L.mask_of(polys[2:], X, Y)
            top = np.where(iso, Sg + H_SINGLE, top)
            top = np.minimum(top, TOP_CAP)               # no container top shallower than the shallowest multibeam top
        d_edge = ndi.distance_transform_edt(m) * L.GSTEP
        zt = np.minimum(top, Sg + L.FLANK * d_edge + 0.3)
        H = np.where(m, np.maximum(Sg, zt), np.nan)
        return H, m, Zc, loops, env

    # ---------------------------------------------------------------- the five versions
    defs = []
    H1, m1, Zc1, lp1, ev1 = surface('photo_2020-08-08', CREST_AS_BUILT, 'design_option2_2017', 'photo')
    H2, m2, Zc2, lp2, ev2 = surface('design_option2_2017', CREST_DESIGN, 'design_option2_2017', 'design')
    H3, m3, Zc3, lp3, ev3 = surface('design_2004_revised', CREST_DESIGN, 'design_2004_revised', 'design')
    H4, m4, Zc4, lp4, ev4 = surface('survey_2011-06-09', CREST_DESIGN, 'design_2004_revised', 'design')
    surf = {'photo_2020-08-08': H1, 'design_option2_2017': H2, 'design_2004_revised': H3, 'survey_2011-06-09': H4}

    def metrics(H):
        h = np.where(np.isfinite(H), H - Sg, 0.0)
        return dict(volume_m3=int(round(float(h.sum()) * L.GSTEP ** 2)), area_m2=int(round(float(np.isfinite(H).sum()))),
                    mean_height_m=round(float(h[np.isfinite(H)].mean()), 2), max_height_m=round(float(h.max()), 2),
                    crest_max_AHD=round(float(np.nanmax(H)), 2), crest_min_AHD=round(float(np.nanmin(H)), 2),
                    volume_unc_bed_m3=int(round(0.5 * float(np.isfinite(H).sum()))))      # +-0.5 m bed level over the footprint
    M = {k: metrics(H) for k, H in surf.items()}
    # container-count cross-check
    n_cont, v_cont = 534, 147.0
    M['_containers'] = dict(n=n_cont, sand_m3_each=v_cont, total_m3=int(n_cont * v_cont))

    def gblock(H):
        Hm = np.where(np.isfinite(H), H - A_MSQ, np.nan)
        cm = np.where(np.isfinite(Hm), np.round(Hm * 100), -32768).astype(np.int16)
        return dict(x0=float(xs[0]), y0=float(ys[0]), step=L.GSTEP, nx=len(xs), ny=len(ys), h_cm_b64=b64(cm, np.int16))

    meta = {
        'photo_2020-08-08': dict(name='Renewed reef as seen on the 2020 aerial photo (visible container field, 8 Aug 2020)', kind='photo_trace', edge=-6.0,
            source_ids=['s3', 'cor23', 'vds21', 'jack12'], loops=lp2, env=ev2,
            method='Plan = traced container field (7 polygons). Top = design crest surface of Option 2 (crest loops -2.5 AHD, -6 AHD envelope), lowered to the measured crest -2.2 AHD, at least 1.0 m above the bed (visible containers), 1.8 m for the isolated containers; flanks 1.5:1 from the polygon edge; bed from the 2017 multibeam.',
            level='visible container field after the 2017-18 renewal (about the -6 m contour; the deeper toe is not visible, so a LOWER BOUND)'),
        'design_option2_2017': dict(name='Renewal design Option 2 (2017, the layout the 2017-18 works followed), -6 m AHD envelope', kind='design_drawing', edge=-6.0,
            source_ids=['cor23', 'jack12'], loops=lp2, env=ev2,
            method='Design surface: -2.5 AHD inside the crest loops, falling linearly with distance rank to -6 AHD at the envelope (Corbett Fig 2 right); bed as in the default version.',
            level='-6 m AHD design contour envelope; crest -2.5 AHD'),
        'design_2004_revised': dict(name='2004 revised design, -6 m AHD envelope (before the 2017-18 renewal)', kind='design_drawing', edge=-6.0,
            source_ids=['jack12', 'jack07', 'cor23'], loops=lp3, env=ev3,
            method='Same surface rule as Option 2 with the 2004 crest loops and envelope (Jackson 2012 Fig 2 right). Validated against the 2017 multibeam tops (mean offset +0.26 m, sd 0.66 m).',
            level='-6 m design contour envelope; crest -2.5 AHD'),
        'survey_2011-06-09': dict(name='Surveyed relief zone, bathymetric survey of 9 Jun 2011 (before the 2017-18 renewal)', kind='multibeam_survey', edge=-6.0,
            source_ids=['jack12'], loops=lp4, env=ev4,
            method='Footprint = zone of strong relief in Jackson 2012 Fig 5a (no depth legend); surface = 2004 design surface cut to that zone (assumption); low confidence.',
            level='relief zone of the 2011 survey (threshold-dependent: 3,000-7,000 m2)'),
    }
    versions = []
    for vid in ('photo_2020-08-08', 'design_option2_2017', 'design_2004_revised', 'survey_2011-06-09', 'navionics_4.0m_shoals'):
        sv = V[vid]; mt = meta.get(vid); polys = P(vid)
        d = dict(id=vid, name=(mt or sv)['name'], date=sv['date'], kind=sv['kind'], source_ids=(mt or sv)['source_ids'] if mt else ['s12'],
                 method=(mt or sv)['method'], level=(mt or sv)['level'] if mt else sv['level'], note=sv['note'], area_m2=sv['area_m2'], bbox_m=sv['bbox_m'],
                 outline_m=[pl(p) for p in polys], solid=bool(mt))
        if mt:
            m = M[vid]; d.update(volume_m3=m['volume_m3'], volume_unc_m3=m['volume_unc_bed_m3'], mean_height_m=m['mean_height_m'], max_height_m=m['max_height_m'],
                                 crest_shallowest_AHD=m['crest_max_AHD'], grid=gblock(surf[vid]), edge_level_MSL=round(mt['edge'] - A_MSQ, 2),
                                 crest_loops_m=[pl(p) for p in mt['loops']] if vid != 'photo_2020-08-08' else None)
            if vid == 'photo_2020-08-08': d['design_loops_m'] = [pl(p) for p in mt['loops']]
        else:
            d.update(volume_m3=None, volume_unc_m3=None, edge_level_MSL=round(-4.0 - 0.76 - A_MSQ, 2))
        versions.append(d)
    versions_info = ('Five outlines are stored; the first is the DEFAULT. (1) The renewed reef as it is on the Esri aerial photo of 8 Aug 2020 (the visible container field, 6,239 m2): no post-renewal survey or as-built drawing exists, so the photo is the only evidence of the state actually built; it is a LOWER BOUND because the deeper toe is not visible. '
                     '(2) Renewal design Option 2 (2017; Corbett et al. 2023 Fig 2): the layout the 2017-18 works followed, drawn to the -6 m AHD contour (13,941 m2); the north reef was almost fully achieved, the south reef and the bridge only partly. '
                     '(3) The 2004 revised design (13,631 m2): the reef BEFORE the 84 containers of 2017-18. (4) The 2011 survey relief zone (4,922 m2; Jackson et al. 2012): also pre-renewal, no depth legend. '
                     '(5) Navionics chart shoals shallower than 4.0 m (537 m2): indicative position check only, not a footprint, no solid is drawn. Design outlines are placed to +-15 m and are envelopes larger than the container field. '
                     'Default = decision D7 by Lior, 2026-10-10 (photo trace; Option 2 stays a toggle).')

    # ------------------------------------------------------------------ validation numbers
    stats = {}
    mx, my = mb['xs'], mb['ys']
    # (a) design surface vs multibeam tops, 8 m blocks, 2004 design surface (pre-works structure)
    D, R, B = mb['D'], mb['R'], mb['bed']
    Zc, men = L.design_top(lp3, ev3, X, Y)
    res = []
    for j in range(0, D.shape[0] - 8, 8):
        for i in range(0, D.shape[1] - 8, 8):
            d = D[j:j + 8, i:i + 8]; r = R[j:j + 8, i:i + 8]; mm = men[j:j + 8, i:i + 8]
            if np.isfinite(d).sum() < 60 or not mm.all() or (r > 0.8).sum() < 8: continue
            res.append((np.nanpercentile(d, 90), Zc[j + 4, i + 4]))
    a = np.array(res); stats['design2004_vs_multibeam_tops'] = dict(n=len(a), mean_offset_m=round(float(np.mean(a[:, 1] - a[:, 0])), 2), sd_m=round(float(np.std(a[:, 1] - a[:, 0])), 2), corr=round(float(np.corrcoef(a[:, 0], a[:, 1])[0, 1]), 2))
    # (b) multibeam shallowest tops inside the traced arms
    from shapely import contains_xy
    for nm, i in (('north_arm', 0), ('south_arm', 1)):
        mk = contains_xy(Polygon(shape['canonical']['polygons_m'][i]).buffer(2), X, Y) & np.isfinite(D)
        stats['multibeam_' + nm] = dict(shallowest_AHD=round(float(np.nanmax(D[mk])), 2), p99_AHD=round(float(np.nanpercentile(D[mk], 99)), 2), relief_p90_m=round(float(np.nanpercentile(R[mk], 90)), 2), relief_p99_m=round(float(np.nanpercentile(R[mk], 99)), 2), bed_median_AHD=round(float(np.nanmedian(B[mk])), 2))
    stats['bed_profile_AHD'] = {str(y): round(float(prof(y)), 2) for y in (0, 100, 190, 210, 235, 265, 300, 340, 370, 400, 460, 500)}
    # (c) bed under the footprints (model), height above bed per version
    for vid, H in surf.items():
        mk = np.isfinite(H); stats['bed_under_' + vid] = [round(float(Sg[mk].min()), 2), round(float(Sg[mk].mean()), 2), round(float(Sg[mk].max()), 2)]
    # (d) packing: volume / (534 x 147)
    stats['packing_photo_vs_containers'] = round(M['photo_2020-08-08']['volume_m3'] / M['_containers']['total_m3'], 2)
    stats['packing_option2_vs_containers'] = round(M['design_option2_2017']['volume_m3'] / M['_containers']['total_m3'], 2)
    # (e) crest datum sensitivity: crest depth below LAT
    stats['crest_below_LAT_m'] = dict(measured_msq=round(-(CREST_AS_BUILT + 0.76), 2), measured_icm=round(-(CREST_AS_BUILT + 1.00), 2), design_msq=round(-(CREST_DESIGN + 0.76), 2), design_icm=round(-(CREST_DESIGN + 1.00), 2))

    # ------------------------------------------------------------------ assemble
    sb = dict(x0=float(sx[0]), y0=float(sy[0]), step=5.0, nx=len(sx), ny=len(sy), z=[[round(float(v - A_MSQ), 2) for v in row] for row in Zs])
    levels = [dict(id=i, name=n, z=z, source=s, estimated=e) for i, n, z, s, e in LEVELS]
    extra = [dict(id=i, name=n, z=z, source=s, estimated=e) for i, n, z, s, e in EXTRA]
    faint = [[[round(a, 2), round(b, 2)] for a, b in q['canonical_m']] for q in shape['faint_seaward_patches']['patches'] if len(q.get('canonical_m', [])) > 2]
    nx_, ny_ = math.cos(math.radians(356.21)), math.cos(math.radians(86.21))
    cen = lambda p: (round(p.centroid.x, 1), round(p.centroid.y, 1))
    n_loop = lp2[0] if lp2[0].centroid.x > 0 else lp2[1]; s_loop = lp2[1] if lp2[0].centroid.x > 0 else lp2[0]
    crest_labels = [dict(text='N arm crest -2.2 AHD (measured, shallowest)', x=cen(n_loop)[0], y=cen(n_loop)[1], z=round(CREST_AS_BUILT - A_MSQ, 2)),
                    dict(text='S arm crest (design -2.5 AHD)', x=cen(s_loop)[0], y=cen(s_loop)[1], z=round(CREST_DESIGN - A_MSQ, 2)),
                    dict(text='toe: surface meets bed at about -6 to -7 AHD', x=20.0, y=352.0, z=round(-6.5 - A_MSQ, 2))]
    prov = provenance(M, stats)
    conf = dict(level='medium', reason=('The container field is a georeferenced 2020 photo trace and the crest (-2.2 m AHD, multibeam) and seabed (2017 multibeam, 19 Jul 2018 survey, Vieira da Silva 2021 Fig 3) are measured, but the 2017 multibeam is read from a colour figure (+-0.4 m, placed to +-10 m), '
                                        'no post-renewal plan or survey exists, the toe below about -6 m is not visible, and the crest datum differs by 0.24 m between sources; reef height is known to about +-1 m and volume only as a lower bound.'))
    model = dict(slug='narrowneck-gold-coast', name='Narrowneck Reef, Gold Coast (Queensland, Australia)', built=BUILT,
                 state=('Renewed reef as left in June 2018 (84 containers added around the 2004-revised structure; about 534 containers placed since 1999), shown by the visible container field of 8 Aug 2020. '
                        'History is not modelled: 1999-2000 build, 2004 weir and flared wings, 2017-18 renewal (Option 2 only partly built on the south reef); no later change is documented.'),
                 frame=dict(x='alongshore, + toward NORTH (bearing 356.21 deg)', y='offshore, + toward EAST (bearing 86.21 deg)', z='up, 0 = MSL', units='m',
                            origin='waterline of the 2020-08-08 Esri image nearest the reef centroid (-27.986800, 153.431127)', bearing_x_deg=356.21, bearing_y_deg=86.21,
                            north_xy=[round(nx_, 5), round(ny_, 5)], shoreline_y=0.0),
                 datum=dict(zero='MSL', ahd_msl_msq=A_MSQ, equation='z_MSL = z_AHD - 0.12 (MSQ default); alternative (papers: AHD = LAT - 1.00): z_MSL = z_AHD + 0.12', unc=0.25,
                            alt=[dict(id='msq', label='MSQ: AHD = LAT + 0.760 (default)', geom_shift=0.0), dict(id='icm', label='Papers: RL -2.5 AHD = -1.5 LAT (AHD = LAT + 1.00)', geom_shift=0.24)]),
                 levels=levels, extra_levels=extra, slider=dict(min_id='LAT', max_id='HAT', note='Gold Coast Seaway planes (MSQ 2026); LAT to HAT.'),
                 seabed=sb, versions=versions, default_version='photo_2020-08-08', versions_info=versions_info,
                 faint_patches_m=faint, provenance=prov, confidence_3d=conf, validation=dict(stats=stats, volumes=M),
                 photo_match=True, crest_labels=crest_labels, container=dict(n=534, length_m=20, diameter_m='3-4.5', sand_m3_each=147))
    with open(os.path.join(HERE, 'model.js'), 'w', encoding='utf-8') as f:
        f.write('/* Generated by build_3d.py (%s). z in metres above MSL (z_MSL = z_AHD - 0.12); canonical frame x north-ish, y offshore (east). */\nwindow.REEF_MODEL = ' % BUILT)
        json.dump(model, f, separators=(',', ':')); f.write(';\n')
    json.dump(dict(M=M, stats=stats), open(os.path.join(SRC, 'build_metrics.json'), 'w'), indent=1)
    print('model.js', os.path.getsize(os.path.join(HERE, 'model.js')) // 1024, 'kB'); print(json.dumps(M)); print(json.dumps(stats))
    docs = {}
    for key, fn in (('methods_md', 'METHODS_3D.md'), ('sources_md', 'SOURCES_3D.md')):
        p = os.path.join(HERE, fn); docs[key] = open(p, encoding='utf-8').read() if os.path.exists(p) else ''
    # sections of METHODS_3D.md shown as their own tabs in the viewer (source audit 2026-10-10)
    import re as _re
    for key, head in (('sources_use_md', '### 2b.'), ('assumptions_md', '### 3.6 '), ('decisions_md', '### 3.8 ')):
        m_ = docs['methods_md']; i_ = m_.find(head)
        if i_ >= 0:
            j_ = _re.search(r'\n#{2,3} ', m_[i_ + 4:]); docs[key] = m_[i_:i_ + 4 + j_.start()] if j_ else m_[i_:]
    with open(os.path.join(HERE, 'docs.js'), 'w', encoding='utf-8') as f:
        f.write('window.REEF_DOCS = '); json.dump(docs, f, ensure_ascii=False); f.write(';\n')


def provenance(M, st):
    P = []
    def add(parameter, value, unit, src, method, unc, est): P.append(dict(parameter=parameter, value=value, unit=unit, source_id=src, method=method, uncertainty=unc, estimated=est))
    add('plan outline, photo (version photo_2020-08-08, DEFAULT)', '6,239 m2, 7 polygons', 'm2', 's3', 'dark container patches thresholded on Esri Wayback r9812 (8 Aug 2020), closed 3.7 m, georeferenced by tile bounds (shape.json, verified)', 'edges +-1 m; waterline distance +-15 m; visible field only = lower bound', False)
    add('plan outlines of the other four versions', '13,941 / 13,631 / 4,922 / 537 m2', 'm2', 'cor23, jack12, s12', 'VERIFY.md steps 2-5 (design drawings placed on the 2020 image; relief zone of the 2011 survey; Navionics 4.0 m loops)', '+-15 m placement; scale +-3 % (Option 2) / +-10 % (2004)', False)
    add('crest, as built (shallowest)', '-2.2 m AHD = %.2f m below LAT (MSQ) or %.2f (papers)' % (st['crest_below_LAT_m']['measured_msq'], st['crest_below_LAT_m']['measured_icm']), 'm AHD', 'vds21', 'quote: multibeam survey indicates the reef crest is currently at -2.2 m AHD (accepted manuscript p.5)', '+-0.2 m; which part of the crest is not stated; 0.24 m datum ambiguity for the LAT value', False)
    add('crest, design target', '-2.5 m AHD (= -1.5 m LAT by the papers; -1.74 m LAT by MSQ)', 'm AHD', 'jack07, cor23', 'Jackson 2007 printed p.7; Corbett 2023 p.3; council layer TOP_REDUCED_LEVEL -2.5', 'design value; settlement 1-2 m locally', False)
    add('crest variation along the arms', '-2.5 over the shoreward wedge, falling to -6 at the envelope (surface rule: linear in distance rank between crest loop and envelope)', 'm AHD', 'jack12, cor23', 'contours -2.5/-3/-3.5/-4/-4.5/-5/-6 (Jackson 2012 Fig 2 right, Corbett Fig 2); NOT digitised contour by contour: crest loops and envelope only. Check vs 2017 multibeam tops: mean offset %+.2f m, sd %.2f m, r = %.2f (n = %d)' % (st['design2004_vs_multibeam_tops']['mean_offset_m'], st['design2004_vs_multibeam_tops']['sd_m'], st['design2004_vs_multibeam_tops']['corr'], st['design2004_vs_multibeam_tops']['n']), '+-0.7 m', True)
    add('seabed in and around the reef window (164 x 145 m)', 'about -4 (shoreward ends) to -7 (seaward), -2 at the window edge y 205', 'm AHD', 'cor23', 'Corbett Fig 3 pre-works multibeam (registry img-55): hue -> depth through the colour bar (4 tick labels), grey opening (r 4.65 m) removes the containers, Gaussian 6 px; placed by overlap with the traced arms (+-10 m)', '+-0.4 m colour reading; assumed AHD (not stated); +-10 m position', False)
    add('seabed seaward and shoreward of the window', 'to -7.8 at y 402, -8.8 at 411, -9.8 at 474, -10.8 at 514; shoreward 0 at y 0, -1.8 at y 100, -2.1 at y 190', 'm AHD', 'vds21, s12', 'Navionics SonarChart labels 7/8/9/10 (LAT assumed, AHD = -(depth) - 0.76) read on img-50 at +-20 m (map centre = reef centroid assumed), consistent with Vieira da Silva Fig 3 (-9/-10 seaward); shoreward part ASSUMED (Navionics land edge does not match the 2020 waterline, METHODS 4.4)', '+-1 m offshore; +-1 m nearshore (unsurveyed)', True)
    add('reef height above the bed', 'multibeam relief p90 %.1f-%.1f m, p99 %.1f-%.1f m (single container layer 1-2 m); crest wedge 2-3 m' % (st['multibeam_north_arm']['relief_p90_m'], st['multibeam_south_arm']['relief_p90_m'], st['multibeam_north_arm']['relief_p99_m'], st['multibeam_south_arm']['relief_p99_m']), 'm', 'cor23', 'relief = multibeam surface minus opened bed (img-55)', '+-0.5 m; opening leaves wide stacks in the bed (heights biased low)', True)
    add('side slope of the mound', '1.5 H : 1 V from the footprint edge', 'H:V', 'estimate', 'rounded 3-4.5 m diameter containers; no published section', 'unknown; +-0.5 slope', True)
    add('container size and count', '20 m x 3-4.5 m; 408 (1999-2000) + 42 + 84 (2018) = 534 placed, 70-80 visible', 'n', 'jack07, jack12, city20', 'Jackson 2007 p.4; Jackson 2012 p.3; City of Gold Coast renewal page 2020', 'count by sum of campaigns', False)
    add('tide planes (z = 0 at MSL)', 'LAT -0.88, MLWS -0.66, MLWN -0.37, MHWN +0.36, MHWS +0.65, HAT +1.15; AHD -0.12', 'm MSL', 'msq', 'Maritime Safety Queensland 2014 (standard port datum levels) and 2026 (semidiurnal tidal planes), Gold Coast Seaway row (4 km from the reef)', '+-0.05 m; AHD offset ambiguity 0.24 m (METHODS 3.1)', False)
    add('volume (default version, photo)', '%d m3' % M['photo_2020-08-08']['volume_m3'], 'm3', 'model', 'sum of (surface - bed) over the 1 m grid; envelope incl. voids between containers', '+-%d m3 (bed level +-0.5 m); lower bound' % M['photo_2020-08-08']['volume_unc_bed_m3'], True)
    return P


if __name__ == '__main__':
    main()
