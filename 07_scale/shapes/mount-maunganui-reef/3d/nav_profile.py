"""nav_profile.py - Navionics SonarChart contours (navionics_isolines.json, from nav_isolines.py) -> cross-shore depth profile at the reef, datum test
against the 2013 multibeam DEM (Fig 5, mmr_lib), and the annotated figures in annotated/.  Run:  python nav_profile.py
Outputs: navionics_profile.json, annotated/nav_sonar_z17_profile.png, annotated/nav_naut_z17_check.png, annotated/nav_datum_test.png
(Garmin Navionics, not for navigation; private research copy.  Replaces the earlier navionics_profile_sonar_z17.json, a straight-line fit that was wrong
because the contours curve towards Mauao.)"""
import json, os, sys, math
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import unary_union
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mmr_lib as L
import nav_isolines as N
HERE = os.path.dirname(os.path.abspath(__file__)); ANN = os.path.join(HERE, 'annotated'); os.makedirs(ANN, exist_ok=True)
D = json.load(open(os.path.join(HERE, 'navionics_isolines.json')))
sh, P2, PT = L.load_shape()
U2 = unary_union([Polygon(p) for p in P2]); UT = unary_union([Polygon(p) for p in PT])
XC, YC = U2.centroid.coords[0]
TRANSECTS = (-100, -50, 0, 50, 100)


def cross(lines, x0, ymin=20):
    ys = []
    for l in lines:
        a = np.array(l)
        for i in range(len(a) - 1):
            (xa, ya), (xb, yb) = a[i], a[i + 1]
            if (xa - x0) * (xb - x0) < 0:
                y = ya + (yb - ya) * (x0 - xa) / (xb - xa)
                if y > ymin: ys.append(float(y))
    return sorted(ys)


# ------------------------------------------------------------------ 1. profile (SonarChart z17 + z18 check)
prof = {}
for v in range(1, 10):
    row = {'depth_m': v, 'transects': {}, 'z18': {}}
    for chart, zz, key in (('sonar', '17', 'transects'), ('sonar', '18', 'z18')):
        for x0 in TRANSECTS:
            ys = cross(D[chart][zz][str(v)], x0)
            if len(ys) == 1: row[key][str(x0)] = round(ys[0], 1)
            elif len(ys) > 1: row[key][str(x0)] = [round(y, 1) for y in ys]
    vals = [y for y in row['transects'].values() if not isinstance(y, list)]
    row['n'] = len(vals)
    row['y_median_m'] = round(float(np.median(vals)), 1) if vals else None
    row['y_at_x0_m'] = row['transects'].get('0')
    z18 = [y for y in row['z18'].values() if not isinstance(y, list)]
    row['z18_median_m'] = round(float(np.median(z18)), 1) if z18 else None
    prof[str(v)] = row
use = [(prof[k]['y_median_m'], -float(k)) for k in prof if prof[k]['n'] >= 3]       # (y, z_CD) needs >= 3 of 5 transects
# shoreline anchor: wet/dry sand line y = 0 is taken as the MSL line of the 2011-01-15 image => z_CD = +1.13 (assumption A-shore)
anchor = (0.0, L.MSL_ABOVE_CD)
pts = [anchor] + use
ys_p, zs_p = zip(*pts)
z_at_reef = float(np.interp(YC, ys_p, zs_p))
slopes = [(round((pts[i + 1][0] - pts[i][0]) / abs(pts[i + 1][1] - pts[i][1]), 0)) for i in range(len(pts) - 1)]
out = {'method': 'median over transects x = %s m of the y where the SonarChart z17 shade-v edge (= v-m contour) crosses the line x = const; contours extracted by nav_isolines.py' % (TRANSECTS,),
       'datum_assumed': 'chart datum (CD); the viewer states no datum', 'access': '2026-10-06', 'contours': prof,
       'profile_y_zCD': [[round(a, 1), round(b, 2)] for a, b in pts], 'run_per_rise_m': slopes, 'reef_centroid_xy': [round(XC, 2), round(YC, 2)],
       'z_cd_at_reef_centroid': round(z_at_reef, 2)}
print('profile (y, z_CD):', out['profile_y_zCD']); print('run per 1 m rise:', slopes); print('z_CD at reef centroid %.2f (depth %.2f m)' % (z_at_reef, -z_at_reef))
for k, r in prof.items(): print(k, r['y_median_m'], r['n'], 'z18', r['z18_median_m'], r['transects'])

# ------------------------------------------------------------------ 2. nautical chart (2 m and 5 m contours + sounding 2.4 m)
naut = {}
for v in (2, 5):
    naut[str(v)] = {str(x0): [round(y, 1) for y in cross(D['naut']['17'][str(v)], x0)] for x0 in TRANSECTS}
snd = {'label': '2.4', 'pixel_z17': [493, 273]}
snd['xy'] = [round(c, 1) for c in N.clip2canon(493, 273, 17)]
snd['sonar_profile_depth_m_there'] = round(-float(np.interp(snd['xy'][1], ys_p, zs_p)), 2)
snd['distance_to_toe_outline_m'] = round(float(UT.distance(Point(*snd['xy']))), 1)
out['nautical_chart'] = {'contours_y_by_transect': naut, 'sounding_2.4': snd,
                         'note': 'Nautical Charts z17 show only the 2 m and 5 m contours (coarse); the 2.4 sounding lies at the NE (seaward) tip of the reef footprint; SonarChart interpolation there is %.2f m' % snd['sonar_profile_depth_m_there']}
print('naut', naut, snd)

# ------------------------------------------------------------------ 3. datum test against the 2013 multibeam DEM (CD) on cells away from the reef and its scour hole
dep, filled, valid, _ = L.load_fig5()
Z, xs, ys = L.fig5_to_grid(dep, valid, -80, 105, 245, 400, 1.0)
XX, YY = np.meshgrid(xs, ys)
from shapely import vectorized
zone = unary_union([UT, U2]).convex_hull.buffer(12)
inz = vectorized.contains(zone, XX, YY)
ok = np.isfinite(Z) & ~inz
nav_z = np.interp(YY, ys_p, zs_p)
bias = {}
for name, shift in (('CD (as read)', 0.0), ('LAT (z_CD = z_LAT - 0.03)', -0.03), ('MVD-53 (z_CD = z_MVD + 0.9622)', 0.9622), ('MSL (z_CD = z_MSL + 1.13)', 1.13)):
    r = Z[ok] - (nav_z[ok] + shift)
    bias[name] = dict(shift_m=shift, n=int(ok.sum()), mean_diff_m=round(float(r.mean()), 2), rms_m=round(float(np.sqrt((r ** 2).mean())), 2))
rows = []
for y0 in range(250, 400, 25):
    m = ok & (YY >= y0) & (YY < y0 + 25)
    if m.sum() > 20: rows.append(dict(y_from=y0, y_to=y0 + 25, n=int(m.sum()), dem_2013_zCD_median=round(float(np.median(Z[m])), 2), nav_zCD=round(float(np.median(nav_z[m])), 2)))
out['datum_test_vs_2013_dem'] = {'cells': 'Fig 5 DEM 1 m grid, x -80..105, y 245..400, valid and outside the convex hull of the reef + toe buffered by 12 m (no reef, no scour hole)', 'results': bias, 'by_y_band': rows}
print(json.dumps(bias, indent=1)); print(rows)
json.dump(out, open(os.path.join(HERE, 'navionics_profile.json'), 'w'), indent=1)

# ------------------------------------------------------------------ 4. annotated figures
def font(sz, bold=False):
    for f in ('arialbd.ttf' if bold else 'arial.ttf', 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'):
        try: return ImageFont.truetype(f, sz)
        except Exception: pass
    return ImageFont.load_default()
F10, F12, F14B = font(11), font(13), font(15, True)
COL = {1: (230, 25, 75), 2: (245, 130, 48), 3: (210, 170, 0), 4: (60, 180, 75), 5: (0, 130, 200), 6: (145, 30, 180), 7: (240, 50, 230), 8: (128, 128, 0), 9: (0, 128, 128)}


def clip_xy(x, y, z=17):
    a, b = N.canon2clip(np.atleast_1d(x), np.atleast_1d(y), z); return list(zip(a.tolist(), b.tolist()))


def draw_common(im, z=17):
    dr = ImageDraw.Draw(im, 'RGBA')
    for P, col in ((PT, (255, 140, 0, 255)), (P2, (255, 0, 0, 255))):
        for p in P:
            q = clip_xy(p[:, 0], p[:, 1], z); dr.line(q + [q[0]], fill=col, width=2)
    c = clip_xy(XC, YC, z)[0]; dr.line([(c[0] - 8, c[1]), (c[0] + 8, c[1])], fill=(0, 0, 0, 255), width=2); dr.line([(c[0], c[1] - 8), (c[0], c[1] + 8)], fill=(0, 0, 0, 255), width=2)
    # frame axes: shoreline y = 0 and transect x = 0
    sl = clip_xy(np.array([-300, 500]), np.array([0, 0]), z); dr.line(sl, fill=(200, 0, 0, 255), width=2)
    return dr, c


def label(dr, xy, text, fnt=F12, fill=(0, 0, 0, 255), bg=(255, 255, 255, 215)):
    w, h = dr.textbbox((0, 0), text, font=fnt)[2:]; x, y = xy
    dr.rectangle([x - 2, y - 1, x + w + 2, y + h + 1], fill=bg); dr.text((x, y), text, font=fnt, fill=fill)


# 4a SonarChart z17 with the extracted contours, transects and the profile
im = Image.open(os.path.join(N.SRC, 'sonar_z17_shade00.0.png')).convert('RGB')
dr, c = draw_common(im)
for v in range(1, 10):
    for l in D['sonar']['17'][str(v)]:
        if np.median(np.array(l)[:, 1]) < 60: continue          # beach-edge artefact
        q = clip_xy(np.array(l)[:, 0], np.array(l)[:, 1]); q = [p for p in q if 0 <= p[0] < 982 and 0 <= p[1] < 655]
        if len(q) > 1: dr.line(q, fill=COL[v] + (255,), width=3)
for x0 in TRANSECTS:
    q = clip_xy(np.array([x0, x0]), np.array([0, 820])); dr.line(q, fill=(0, 0, 0, 255) if x0 == 0 else (90, 90, 90, 255), width=1)
    for v in range(1, 10):
        yv = prof[str(v)]['transects'].get(str(x0))
        if isinstance(yv, float):
            p = clip_xy(x0, yv)[0]
            if 0 <= p[0] < 982 and 0 <= p[1] < 655: dr.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], fill=COL[v] + (255,), outline=(0, 0, 0, 255))
for v in range(1, 10):
    yv = prof[str(v)]['transects'].get('0')
    if isinstance(yv, float):
        p = clip_xy(0, yv)[0]
        if 0 <= p[0] < 982 and 0 <= p[1] < 655: label(dr, (p[0] + 6, p[1] - 8), '%d m  y=%d' % (v, round(yv)), F10, COL[v] + (255,))
label(dr, (c[0] + 10, c[1] + 4), 'reef centroid y=%.0f m: chart depth %.2f m' % (YC, -z_at_reef), F12, (180, 0, 0, 255))
def strip(im, lines, h=130):
    big = Image.new('RGB', (im.width, im.height + h), (255, 255, 255)); big.paste(im, (0, 0)); d2 = ImageDraw.Draw(big)
    for i, t in enumerate(lines): d2.text((6, im.height + 4 + 14 * i), t, font=F10, fill=(0, 0, 0))
    return big, d2
im, dr2 = strip(im, ['Garmin Navionics SonarChart (maps.garmin.com/en-US/marine), zoom 17, accessed 2026-10-06 - NOT FOR NAVIGATION; private research copy.',
                     'Coloured lines = contours read from the Shallow-shading edge (1..9 m; the viewer states no datum: chart datum assumed, tested in nav_datum_test.png).',
                     'Dots = crossings on the 5 transects x = -100, -50, 0, 50, 100 m (black lines); table (right) = median y of each contour. Red outline = -2.0 m CD survey outline',
                     '(2013), orange = as-built toe, red line = shoreline y = 0 (Esri 2011-01-15). Reef REMOVED Sep-Nov 2014: Navionics used for the SEABED only.',
                     'The 3 m contour bulges 12-17 m seaward at x = 0..50 right at the reef (3 m at y 339-346 vs 327-329 at x = -100, -50, 100): possible residual of the removed reef; not used.'])
tx, ty = 6, 655 + 80
for i, v in enumerate(range(1, 10)):
    r = prof[str(v)]; cx_, cy_ = tx + 190 * (i % 5) - 330, ty + 14 * (i // 5)
    dr2.rectangle([cx_ + 330, cy_ + 2, cx_ + 340, cy_ + 11], fill=COL[v])
    dr2.text((cx_ + 344, cy_), '%d m: y = %s (n=%d)' % (v, r['y_median_m'], r['n']), font=F10, fill=(0, 0, 0))
im.save(os.path.join(ANN, 'nav_sonar_z17_profile.png'))

# 4b nautical chart z17: 2 m and 5 m contours, sounding 2.4 and the reef
im = Image.open(os.path.join(N.SRC, 'naut_z17_shade00.0.png')).convert('RGB')
dr, c = draw_common(im)
for v in (2, 5):
    for l in D['naut']['17'][str(v)]:
        if np.median(np.array(l)[:, 1]) < 60: continue          # beach-edge artefact
        q = clip_xy(np.array(l)[:, 0], np.array(l)[:, 1]); q = [p for p in q if 0 <= p[0] < 982 and 0 <= p[1] < 655]
        if len(q) > 1: dr.line(q, fill=COL[v] + (255,), width=3)
p = (493, 273); dr.ellipse([p[0] - 7, p[1] - 7, p[0] + 7, p[1] + 7], outline=(0, 0, 255, 255), width=3)
label(dr, (p[0] + 12, p[1] - 22), 'sounding 2.4 m at (x %.0f, y %.0f): NE tip of the reef footprint; SonarChart interpolation %.2f m' % (snd['xy'][0], snd['xy'][1], snd['sonar_profile_depth_m_there']), F10, (0, 0, 200, 255))
im, _ = strip(im, ['Garmin Navionics Nautical Charts (maps.garmin.com/en-US/marine), zoom 17, accessed 2026-10-06 - NOT FOR NAVIGATION; private research copy.',
                   'Only the 2 m (orange) and 5 m (blue) contours are drawn on this layer; small figures are spot soundings in m with the decimetre as subscript (2_4 = 2.4 m).',
                   'Red outline = -2.0 m CD survey outline (2013), orange = as-built toe, red line = shoreline y = 0. Sounding 2.4 m (blue ring) lies at the NE tip of the footprint.',
                   'The other soundings (0.9 m at x 352, y 235; 0.3 m at x -187, y 213) are 150-350 m alongshore of the reef transect: not used.'], 70)
im.save(os.path.join(ANN, 'nav_naut_z17_check.png'))

# 4c datum test figure: Navionics profile vs the 2013 DEM bed (cells outside the reef zone), y band medians
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8.5, 4.6))
yy = np.arange(0, 560, 2.0); ax.plot(yy, np.interp(yy, ys_p, zs_p), 'k-', lw=2, label='Navionics SonarChart 2026 (read as CD)')
sc = ax.scatter(YY[ok][::7], Z[ok][::7], c=XX[ok][::7], s=4, cmap='viridis', label='2013 multibeam DEM (Fig 5, CD), outside reef zone')
for nm, sft, col in (('MVD-53 reading (+0.96)', 0.9622, 'tab:red'), ('MSL reading (+1.13)', 1.13, 'tab:orange')):
    ax.plot(yy, np.interp(yy, ys_p, zs_p) + sft, '--', color=col, lw=1, label='Navionics if datum = ' + nm)
ax.axhline(-0.9, color='m', lw=1); ax.text(5, -0.82, 'crest -0.9 m CD', color='m', fontsize=8)
ax.axhline(-4.0, color='b', lw=1, ls=':'); ax.text(5, -3.92, 'as-built bed decision -4.0 m CD', color='b', fontsize=8)
ax.axvspan(YC - 30, YC + 30, color='orange', alpha=.15); ax.set_xlim(0, 560); ax.set_ylim(-7, 2)
ax.set_xlabel('y offshore of the shoreline (m)'); ax.set_ylabel('seabed elevation (m, CD)'); ax.grid(alpha=.3); ax.legend(fontsize=7, loc='lower left')
ax.set_title('mount-maunganui-reef: Navionics profile vs 2013 survey bed (colour = x alongshore); orange band = reef', fontsize=9)
fig.colorbar(sc, ax=ax, label='x (m)'); fig.tight_layout(); fig.savefig(os.path.join(ANN, 'nav_datum_test.png'), dpi=130)
print('figures written')
