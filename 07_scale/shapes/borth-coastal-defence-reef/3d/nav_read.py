"""nav_read.py - read the Garmin Navionics screenshots (src/navionics) along shore-normal rows and compare with the model seabed.

Method (METHODS_3D.md 3.6):
  * the screenshot is the Leaflet container (982 x 655 px, north up, Web Mercator); the centre pixel (491, 327) is lat 52.483453 N, 4.056205 W
    (nav_geometry.json, read from the page itself); Mercator metres per pixel = 156543.03392 / 2**zoom.
  * pixel -> Mercator metres -> WGS84 -> OS grid (EPSG:27700, pyproj) -> canonical frame (b3d_lib.Frame).
  * along a pixel row, thin dark runs are chart contour lines; the 0 m line is the edge of the green 'drying' area.  The depth of each line is
    counted outward (0, 0.5, 1, 1.5, 2, 2.5 m: the printed labels 1, 1.5, 2, 2.5 and 0.5 confirm the 0.5 m interval) .
  * for candidate chart datums (depth below datum d -> z_ODN = z0 - d) the offset to the model seabed along the same ground points is evaluated.
Writes src/navionics_reading.json (read by build_3d.py) and src/navionics/nav_lines.json.
"""
import json, os, sys, math
import numpy as np
from PIL import Image
from pyproj import Transformer
import b3d_lib as L

HERE = os.path.dirname(os.path.abspath(__file__)); NAV = os.path.join(HERE, 'src', 'navionics')
CEN = (52.483453, -4.056205); CPX = (491.0, 327.0)
shape = json.load(open(os.path.join(L.BASE, 'shape.json'), encoding='utf-8')); F = L.Frame(shape)
T_ll2m = Transformer.from_crs('EPSG:4326', 'EPSG:3857', always_xy=True); T_m2ll = Transformer.from_crs('EPSG:3857', 'EPSG:4326', always_xy=True)
T_ll2bng = Transformer.from_crs('EPSG:4326', 'EPSG:27700', always_xy=True)
cm = T_ll2m.transform(CEN[1], CEN[0])


def px2can(col, row, zoom):
    r = 156543.03392 / 2 ** zoom
    lon, lat = T_m2ll.transform(cm[0] + (np.asarray(col) - CPX[0]) * r, cm[1] - (np.asarray(row) - CPX[1]) * r)
    e, n = T_ll2bng.transform(lon, lat)
    return F.bng2can(np.c_[np.ravel(e), np.ravel(n)])


def runs(mask1d, gap=2):
    cols = np.where(mask1d)[0]; cl = []
    for c in cols:
        if cl and c - cl[-1][-1] <= gap: cl[-1].append(c)
        else: cl.append([c])
    return [float(np.mean(c)) for c in cl]


def read_lines(fn, zoom, rows, xmax=900):
    im = np.asarray(Image.open(os.path.join(NAV, fn)).convert('RGB')).astype(int)
    dark = im.max(axis=2) < 120
    green = (abs(im[:, :, 0] - 152) < 14) & (abs(im[:, :, 1] - 200) < 16) & (im[:, :, 2] < 40)
    out = []
    for row in rows:
        cs = [c for c in runs(dark[row, :xmax]) if c < 800]
        g = np.where(green[row])[0]; edge = float(g.min()) if len(g) else None
        # the line that coincides with the green edge is the 0 m line
        cs = sorted(cs, reverse=True)
        if edge is not None:
            cs = [c for c in cs if c <= edge + 4]
        out.append(dict(row=row, cols=cs, green_edge=edge))
    return out


if __name__ == '__main__':
    z = L.lidar_sampler  # noqa
    import b3d_reef as R
    t = open(os.path.join(HERE, 'model.js'), encoding='utf-8').read(); M = json.loads(t[t.index('{'):t.rindex('}') + 1])
    sb = M['seabed']; Zm = np.array(sb['z']) + 0.31          # mODN
    def seabed(x, y): return float(L.bilinear(Zm, sb['x0'], sb['y0'], sb['step'], np.array([x]), np.array([y]))[0])
    res = {}
    rows = [60, 120, 200, 250, 450, 500, 560, 600]
    allp = []
    for fn, zoom, chart in (('sonar_z17_shade00.0.png', 17, 'SonarChart'), ('naut_z17_shade00.0.png', 17, 'Nautical Chart')):
        L_ = read_lines(fn, zoom, rows)
        for rr in L_:
            cols = rr['cols']
            xy = px2can(cols, [rr['row']] * len(cols), zoom) if cols else np.zeros((0, 2))
            rr['xy'] = xy.round(1).tolist()
        res[chart] = L_
    json.dump(res, open(os.path.join(NAV, 'nav_lines.json'), 'w'), indent=0)
    # ---- model-implied chart zero per line (SonarChart, lines 0, 0.5, ..., 2.5 m) -------------------------------------------------------
    depths = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
    pts = []                                          # (row, x, y, d, z_model)
    for rr in res['SonarChart']:
        for k, ((x, y), c) in enumerate(zip(rr['xy'], rr['cols'])):
            if k < len(depths): pts.append((rr['row'], x, y, depths[k], seabed(x, y)))
    P = np.array(pts)
    P = P[P[:, 2] <= 515.0]                           # the model grid ends at y = 520 (clamped beyond): lines farther offshore are not comparable
    imp = P[:, 4] + P[:, 3]                           # z_model + d = chart zero level (mODN) implied if the model is right
    print('model-implied chart zero (mODN) by depth:', {d: (round(float(np.mean(imp[P[:, 3] == d])), 2), round(float(np.std(imp[P[:, 3] == d])), 2)) for d in depths if (P[:, 3] == d).any()})
    cands = {'LAT (-2.44)': -2.44, 'MLWS (-1.74)': -1.74, 'MLWN (-0.64)': -0.64, 'MSL (+0.31)': 0.31, 'ODN (0.00)': 0.0, 'MHWN (+1.06)': 1.06, 'MHWS (+2.56)': 2.56}
    rms = {k: round(float(np.sqrt(np.mean((imp - v) ** 2))), 2) for k, v in cands.items()}
    print('RMS vs model (all lines):', rms, ' best offset', round(float(imp.mean()), 2), 'sd', round(float(imp.std()), 2))
    # ---- other independent references --------------------------------------------------------------------------------------------------
    f2 = json.load(open(os.path.join(HERE, 'src', 'fig2_contours_canonical.json')))['contours_mODN']
    # depth of the chart as function of y along rows (linear), used at the Fig 2 contour crossing of the same x
    def chart_depth(row_res, y):
        ys = np.array([q[1] for q in row_res['xy']][:6]); d = np.array(depths[:len(ys)])
        return float(np.interp(y, ys, d, left=np.nan, right=np.nan)) if ys[0] < y < ys[-1] else float('nan')
    ref = []
    for rr in res['SonarChart']:
        x = rr['xy'][0][0]
        for k, lev in (('-2', -2.0), ('-3', -3.0), ('-4', -4.0)):
            C = np.array(f2[k]); o = np.argsort(C[:, 0]); yc = float(np.interp(x, C[o, 0], C[o, 1], left=np.nan, right=np.nan))
            if np.isfinite(yc):
                d = chart_depth(rr, yc)
                if np.isfinite(d): ref.append(('Fig2 %s' % k, x, yc, d, lev + d))
    print('Fig 2 contour vs chart depth at the same point (x, y, chart depth d, implied zero):')
    for r_ in ref: print('  ', r_[0], round(r_[1]), round(r_[2]), round(r_[3], 2), round(r_[4], 2))
    # EMODnet cells at x = -30 (REPORT.md of the EMODnet extract): y 368 -> -2.84, 440 -> -3.54, 513 -> -4.35 mODN
    r285 = read_lines('sonar_z17_shade00.0.png', 17, [285])[0]; r285['xy'] = px2can(r285['cols'], [285] * len(r285['cols']), 17).tolist()
    emo = []
    for y, zz in ((368, -2.84), (440, -3.54), (513, -4.35)):
        d = chart_depth(r285, y)
        # beyond the 0 m line the chart is 'drying' (d < 0): extrapolate linearly with the 0 -> 0.5 m slope
        if not np.isfinite(d):
            ys = [q[1] for q in r285['xy']][:2]; d = 0.5 * (y - ys[0]) / (ys[1] - ys[0])
        emo.append(('EMODnet y=%d' % y, -30.6, y, round(d, 2), round(zz + d, 2)))
    print('EMODnet vs chart:', emo)
    imp_f2 = np.array([r_[4] for r_ in ref]); imp_em = np.array([r_[4] for r_ in emo])
    tab = {}
    for k, v in cands.items():
        tab[k] = dict(model=round(float(np.sqrt(np.mean((imp - v) ** 2))), 2), fig2_m4=round(float(np.sqrt(np.mean((imp_f2 - v) ** 2))), 2), emodnet=round(float(np.sqrt(np.mean((imp_em - v) ** 2))), 2))
    print('RMS table', tab)
    print('implied zero: model %.2f+-%.2f (n=%d) | Fig2 -4.0 %.2f+-%.2f (n=%d) | EMODnet %.2f+-%.2f (n=%d)' % (imp.mean(), imp.std(), len(imp), imp_f2.mean(), imp_f2.std(), len(imp_f2), imp_em.mean(), imp_em.std(), len(imp_em)))
    out = dict(model_implied_zero_by_depth={str(d): [round(float(np.mean(imp[P[:, 3] == d])), 2), round(float(np.std(imp[P[:, 3] == d])), 2)] for d in depths if (P[:, 3] == d).any()}, rms_table=tab,
               implied_zero_mODN=dict(model=[round(float(imp.mean()), 2), round(float(imp.std()), 2), len(imp)], fig2_minus4=[round(float(imp_f2.mean()), 2), round(float(imp_f2.std()), 2), len(imp_f2)],
                                      emodnet=[round(float(imp_em.mean()), 2), round(float(imp_em.std()), 2), len(imp_em)]),
               fig2=[[r_[0], round(r_[1]), round(r_[2]), round(r_[3], 2), round(r_[4], 2)] for r_ in ref], emodnet=emo, rows=rows, lines_n=int(len(P)))
    json.dump(out, open(os.path.join(NAV, 'nav_datum_test.json'), 'w'), indent=1)


# ------------------------------------------------------------------------------------------------ annotated screenshots
def can2px(xy, zoom):
    bng = F.can2bng(np.asarray(xy, float).reshape(-1, 2))
    lon, lat = Transformer.from_crs('EPSG:27700', 'EPSG:4326', always_xy=True).transform(bng[:, 0], bng[:, 1])
    mx, my = T_ll2m.transform(lon, lat); r = 156543.03392 / 2 ** zoom
    return np.c_[CPX[0] + (mx - cm[0]) / r, CPX[1] - (my - cm[1]) / r]


def annotate():
    from PIL import ImageDraw
    import make_annotations as MA
    t = open(os.path.join(HERE, 'model.js'), encoding='utf-8').read(); M = json.loads(t[t.index('{'):t.rindex('}') + 1])
    f2 = json.load(open(os.path.join(HERE, 'src', 'fig2_contours_canonical.json')))['contours_mODN']
    nd = json.load(open(os.path.join(NAV, 'nav_datum_test.json'))); lines = json.load(open(os.path.join(NAV, 'nav_lines.json')))
    for fn, zoom, chart, name in (('sonar_z17_shade05.0.png', 17, 'SonarChart', 'A9_navionics_sonarchart_z17_annotated.png'),
                                  ('naut_z18_shade00.0.png', 18, 'Nautical Chart', 'A10_navionics_nautical_z18_reef_outline.png')):
        im = Image.open(os.path.join(NAV, fn)).convert('RGBA'); S = 2 if zoom == 17 else 1
        im = im.resize((im.width * S, im.height * S), Image.LANCZOS); ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        for x in range(-150, 251, 50):
            P = can2px([(x, 150), (x, 700)], zoom) * S; d.line([tuple(q) for q in P], fill=(255, 255, 255, 110), width=1)
            q = can2px([(x, 205 if zoom == 17 else 330)], zoom)[0] * S
            if 0 < q[1] < im.height - 20 and 0 < q[0] < im.width:
                MA.tag(d, (q[0], q[1] + 6), 'x %d' % x, sz=15, fill=(255, 255, 255, 190))
        for y in range(200, 701, 50):
            P = can2px([(-250, y), (300, y)], zoom) * S; d.line([tuple(q) for q in P], fill=(255, 255, 255, 110), width=1)
            q = can2px([(-150 if zoom == 17 else -100, y)], zoom)[0] * S
            if 0 < q[0] < im.width - 60 and 0 < q[1] < im.height:
                MA.tag(d, (q[0] + 4, q[1] - 8), 'y %d' % y, sz=15, fill=(255, 255, 255, 190))
        for vi, col in ((0, (255, 0, 255, 255)), (2, (255, 230, 0, 255))):
            for ring in M['versions'][vi]['outline_m']:
                P = can2px(ring + [ring[0]], zoom) * S; d.line([tuple(q) for q in P], fill=col, width=3)
        for k, col in (('-2', (220, 40, 40, 255)), ('-3', (20, 90, 220, 255)), ('-4', (0, 120, 40, 255))):
            P = can2px(f2[k], zoom) * S; d.line([tuple(q) for q in P], fill=col, width=3)
            q = P[len(P) // 2]; MA.tag(d, (q[0] - 20, q[1] - 24), 'Fig 2 %s mODN' % k, sz=16, fill=col[:3] + (255,), ink=(255, 255, 255))
        if zoom == 17:
            depths = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
            for rr in lines[chart]:
                for k, c in enumerate(rr['cols'][:6]):
                    x, y = c * S, rr['row'] * S
                    d.ellipse((x - 6, y - 6, x + 6, y + 6), outline=(0, 0, 0, 255), fill=(255, 255, 255, 255), width=2)
                    if rr['row'] in (60, 250, 500):
                        MA.tag(d, (x + 8, y - 22), '%g' % depths[k], sz=17, fill=(255, 255, 255, 235), border=(0, 0, 0))
                d.line((0, rr['row'] * S, 900 * S, rr['row'] * S), fill=(0, 0, 0, 60), width=1)
            q = can2px([(37, 405)], zoom)[0] * S; d.ellipse((q[0] - 34, q[1] - 34, q[0] + 34, q[1] + 34), outline=(255, 128, 0, 255), width=4)
            MA.tag(d, (q[0] - 170, q[1] + 40), 'charted shoal 0.5-1 m, 35 m off the rock: not the reef', sz=17, fill=(255, 235, 200, 245), border=(255, 128, 0))
            q = can2px([(-108.5, 248.2)], zoom)[0] * S; d.ellipse((q[0] - 22, q[1] - 22, q[0] + 22, q[1] + 22), outline=(0, 0, 0, 255), width=3)
            MA.tag(d, (q[0] - 120, q[1] + 28), 'drying height 0.2 m (nautical chart label)', sz=17, fill=(255, 255, 255, 245), border=(0, 0, 0))
        else:
            MA.tag(d, (14, 70), 'Nautical Chart z18 (0.364 m/px): no raised feature at the rock; the drying (green) area is uniform', sz=17, fill=(255, 255, 255, 235), border=(0, 0, 0))
        out = Image.alpha_composite(im, ov).convert('RGB')
        tb = nd['rms_table']; iz = nd['implied_zero_mODN']
        if zoom == 17:
            cap = ['Garmin Navionics web chart (maps.garmin.com/marine, SonarChart Maps layer, Depth units = metres, Shallow shading = 5 m), zoom 17 (0.730 m/px), centre 52.483453 N 4.056205 W, captured 2026-10-07. "Not to be used for navigation"; private research copy, reuse not cleared.',
                   'Overlay: canonical grid (x alongshore + south, y offshore, 50 m); magenta = LiDAR-edge outline of the two mounds (default), yellow = visible-rock edge 2024; red / blue / green lines = HRPP576 Fig 2 contours -2 / -3 / -4 mODN. White dots = chart contour crossings read along 8 pixel rows parallel to the shore (labels = depth below chart datum in m, rows 60, 250, 500): the green edge is the 0 m line (y about 385-430 m), then 0.5, 1, 1.5, 2, 2.5 m.',
                   'Datum test (zero level of the chart in mODN, implied if the reference is right): model seabed %.2f +- %.2f (n=%d); Fig 2 -4.0 contour %.2f +- %.2f (n=%d); EMODnet cells %.2f +- %.2f (n=%d). RMS of candidate datums vs Fig 2 -4.0: LAT %.2f, MLWS %.2f, MSL %.2f, ODN %.2f m: LAT is the best standard datum (assumed), but even LAT leaves the chart about 1.1 m shallower than Fig 2 offshore.' % (
                       iz['model'][0], iz['model'][1], iz['model'][2], iz['fig2_minus4'][0], iz['fig2_minus4'][1], iz['fig2_minus4'][2], iz['emodnet'][0], iz['emodnet'][1], iz['emodnet'][2],
                       tb['LAT (-2.44)']['fig2_m4'], tb['MLWS (-1.74)']['fig2_m4'], tb['MSL (+0.31)']['fig2_m4'], tb['ODN (0.00)']['fig2_m4']),
                   'Reef: the rock mounds (0 to +1.5 mODN, 2.4-4 m above LAT) lie inside the uniformly green drying area; the chart shows no raised feature and no reef symbol, so it gives no crest or height. The only charted shoal (0.5-1 m) is 35 m off the north mound head.']
        else:
            cap = ['Garmin Navionics web chart, Nautical Chart layer, zoom 18 (0.365 m/px), Depth units = metres, shading 0, centre 52.483453 N 4.056205 W, captured 2026-10-07. Not for navigation; private research copy.',
                   'Magenta = LiDAR-edge outline, yellow = visible-rock edge 2024, canonical grid 50 m. The rock mounds lie inside the green drying area with no separate feature; the 0.5 / 1 m loops lie outside the structure.']
        out = MA.with_caption(out, cap, sz=19)
        MA.save(out, name)


if __name__ == '__main__' and 'annotate' in sys.argv:
    annotate()
