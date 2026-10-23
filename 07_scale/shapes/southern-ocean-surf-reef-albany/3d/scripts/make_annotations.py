"""make_annotations.py - annotated copies of the source images showing exactly what was read (3d/annotated/A1..A3)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import geo as g
from pyproj import Transformer
from scipy.ndimage import map_coordinates
OUT = os.path.join(HERE, '..', 'annotated'); os.makedirs(OUT, exist_ok=True)
shape = json.load(open(os.path.join(g.SRC, '..', 'shape.json'), encoding='utf-8'))
ver = {v['id']: v for v in shape['outline_versions']}
lv = json.load(open(os.path.join(g.SRC3, 'levels2_raw.json')))
try: FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15); FS = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
except Exception: FONT = FS = ImageFont.load_default()
COL = {-1: (0, 0, 0), -1.5: (200, 220, 60), -2: (80, 220, 80), -2.5: (40, 190, 110), -3: (30, 190, 160), -3.5: (40, 170, 200), -4: (60, 140, 230), -4.5: (60, 90, 240), -5: (30, 30, 255), -6: (130, 40, 220), -7: (170, 40, 160)}


def caption(img, lines, fs=FONT):
    W = img.width; h = 20 * len(lines) + 12
    c = Image.new('RGB', (W, img.height + h), (16, 22, 30)); c.paste(img, (0, 0)); d = ImageDraw.Draw(c)
    for i, l in enumerate(lines): d.text((8, img.height + 6 + 20 * i), l, fill=(230, 236, 242), font=fs)
    return c


# ---------------------------------------------------------------- A1: RHDHV 2015 plan - how the contours were read
m = Image.open(os.path.join(g.SRC, 'rwr_images', 'rwr_RHDHV_optionB_contours_plan_2015.jpg')).convert('RGB'); K = 2
o = m.resize((m.width * K, m.height * K), Image.LANCZOS); d = ImageDraw.Draw(o)
def P(x, y): return tuple(K * c for c in g.xy_to_m2(x, y))
for x in range(-160, 41, 20):
    d.line([P(x, 0), P(x, 215)], fill=(255, 255, 255), width=1)
for L, col in COL.items():
    for xs, r in lv.items():
        if r and r.get(str(L)) is not None and int(xs) % 40 == 0:
            p = P(int(xs), r[str(L)]); d.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], outline=(255, 255, 255), fill=col)
x = -40
for L in COL:
    r = lv.get(str(x))
    if r and r.get(str(L)) is not None:
        p = P(x, r[str(L)]); d.text((p[0] + 6, p[1] - 8), '%g' % L, fill=(255, 255, 0), font=FS)
for vid, col in (('design_bluecoast', (255, 60, 60)), ('sat_2026', (255, 255, 255))):
    pts = [P(a, b) for a, b in ver[vid]['polygons_m'][0]]; d.line(pts + [pts[0]], fill=col, width=3)
d.line([P(-200, 0), P(200, 0)], fill=(255, 0, 255), width=2)
for i, (nx, ny) in enumerate([(85, 218), (110, 218.3), (110, 240.7), (75, 255)]):
    p = tuple(K * c for c in (nx, ny)); d.rectangle([p[0] - 6, p[1] - 6, p[0] + 6, p[1] + 6], outline=(0, 255, 255), width=2); d.text((p[0] + 8, p[1] - 6), 'GCP%d' % (i + 1), fill=(0, 255, 255), font=FS)
img = caption(o, ['A1  Royal HaskoningDHV 2015 "Option B" plan (via Raised Water Research, registry img-16): how the seabed depths were read. Contour colours follow the plan legend (-0.5 ... -8 m, datum not stated; assumed AHD, A3).',
                  'White lines = 10 shore-normal transects (x = -160 ... +40 m, 20 m apart, canonical frame). Dots = contour crossings found by colour (every 40 m; labels = depth in m at x = -40). Magenta = beach-face line (y = 0).',
                  'Red outline = Bluecoast design toe; white outline = satellite 2026 patch. Cyan squares GCP1-4 = ground control points used to georeference this plan on the Esri 2025-01-16 image (similarity fit, residual up to 5 m).',
                  'The structure drawn in this plan is the 2015 concept (Option B, crest -0.75 m, 46,620 m3), NOT the built reef; only its seabed contours were used.'], FS)
img.save(os.path.join(OUT, 'A1_rhdhv_2015_contours_read_on_plan.png'))

# ---------------------------------------------------------------- A3: BMT Fig 6.9 overlay
t = Transformer.from_crs(4326, 28350, always_xy=True)
def xy2r(x, y):
    la, lo = g.en2ll(*g.xy2en(x, y)); E, N = t.transform(lo, la); return 230 + (E - 583500) * 0.538, 265.5 - (N - 6124500) * 0.540
b = Image.open(os.path.join(g.SRC, 'epa', 'EIA_fig6-9_embedded_raster.png')).convert('RGB'); K = 2
o = b.resize((b.width * K, b.height * K), Image.LANCZOS); d = ImageDraw.Draw(o)
for vid, col in (('design_bluecoast', (255, 255, 0)), ('sat_2026', (255, 255, 255))):
    pts = [tuple(K * c for c in xy2r(a, bb)) for a, bb in ver[vid]['polygons_m'][0]]; d.line(pts + [pts[0]], fill=col, width=3)
d.line([tuple(K * c for c in xy2r(x, 0)) for x in (-150, 150)], fill=(255, 0, 255), width=2)
sound = {'2.7': (436, 214), '8.4': (633.5, 180.5), '5 (line label)': (526.5, 130), '3.4': (366, 396), '5 (line label) S': (380, 536), '7.2': (587.5, 423), '7.3': (830, 340), '5.7': (549, 600)}
for k, (rx, ry) in sound.items():
    p = (K * rx, K * ry); d.ellipse([p[0] - 5, p[1] - 5, p[0] + 5, p[1] + 5], outline=(255, 60, 60), width=2)
img = caption(o.crop((500, 100, 1650, 1250)), ['A3  BMT (2018) EIA Fig 6.9 (registry img-14): spot soundings "m CD" read at the printed labels (red rings; label centre = position, +-6 px = +-11 m) and georeferenced with the UTM50/GDA94 grid labels.',
                  'Yellow outline = Bluecoast design toe, white = satellite 2026 patch (both placed through UTM -> lat/lon -> canonical frame). Magenta = beach-face line. Soundings: 2.7 m at (x -53, y 32); 8.4 m at (188, 315); 7.2 m (-243, 472); 7.3 m (120, 780); 5.7 m (-562, 579); 3.4 m (-410, 93).',
                  'Use: far-field check only (8.4 m CD at y = 315 agrees with the -8 m AHD contour read at A1). The near-shore 2.7 m (y = 32) is about 1.6 m deeper than the A1 contours (-1.1 m): UNRESOLVED, see Methods 4.'], FS)
img.save(os.path.join(OUT, 'A3_bmt2018_fig6-9_soundings_georeferenced.png'))

# ---------------------------------------------------------------- A2: profile figure
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(HERE, '..'))
import build_3d as B
fig, ax = plt.subplots(1, 2, figsize=(14, 5.2), gridspec_kw={'width_ratios': [1.25, 1]})
a = ax[0]
ys = np.linspace(-60, 420, 400); a.plot(ys, B.zb(ys), 'k-', lw=2, label='seabed profile used (alongshore uniform)')
for L in COL:
    v = [r[str(L)] for r in lv.values() if r and r.get(str(L)) is not None]
    if v: a.errorbar([np.median(v)], [L], xerr=[[np.median(v) - np.percentile(v, 25)], [np.percentile(v, 75) - np.median(v)]], fmt='o', color='tab:blue', ms=4, capsize=3)
a.plot([], [], 'o', color='tab:blue', label='contour crossings: median and IQR over 10 transects (A1)')
a.plot([32], [-2.7], 'rs', label='BMT 2018 sounding 2.7 m CD (x -53): if CD = AHD')
a.plot([32], [-2.7 - 0.74], 'r^', label='  ... if CD = LAT (z = -2.7 - 0.74)')
a.plot([315], [-8.4], 'rs'); a.plot([315], [-8.4 - 0.74], 'r^')
a.axhline(0, color='c', lw=0.8); a.text(-55, 0.1, 'AHD (model zero)', color='c', fontsize=8)
a.axhline(-0.74, color='gray', lw=0.6, ls='--'); a.text(-55, -0.6, 'LAT (derived)', color='gray', fontsize=8)
a.axvspan(67, 234, color='orange', alpha=0.15, label='reef footprint, y = 67 ... 234 m')
a.set_xlabel('y offshore from the beach-face line (m)'); a.set_ylabel('z (m AHD)'); a.set_title('Seabed profile: contours read from the RHDHV 2015 plan vs BMT 2018 soundings'); a.legend(fontsize=7.5, loc='lower left'); a.grid(alpha=0.3)
a = ax[1]
G = B.reef_grid(ver['design_bluecoast']['polygons_m'][0], 8, json.load(open(os.path.join(HERE, '..', 'src', 'build_metrics.json')))['N_shape_exponent'])
rid = G['ridge']; s = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(rid, axis=0).T))]); sE = s[-1] - s
zc = np.interp(sE, [0, 15, 40, s[-1] + 1], [-1, -1, -2, -2]); bed = B.zb(rid[:, 1])
a.plot(sE, zc, 'r-', lw=2, label='crest ridge level (design table, assumption A7)'); a.plot(sE, bed, 'k-', lw=2, label='seabed under the ridge'); a.fill_between(sE, bed, zc, color='tab:orange', alpha=0.3)
a.set_xlabel('distance along the crest ridge from its offshore (east) end (m)'); a.set_ylabel('z (m AHD)'); a.set_title('Section along the crest ridge (design outline)'); a.legend(fontsize=8); a.grid(alpha=0.3)
fig.text(0.01, 0.005, 'A2  Seabed profile and crest section. Sources: RHDHV 2015 Option B plan (registry img-16), BMT 2018 Fig 6.9 (img-14), City of Albany design table (img-10). Crest levels are design values; the bed under the ridge is read from the profile (+-1 m). Private research figure.', fontsize=7.5)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(OUT, 'A2_seabed_profile_and_crest_section.png'), dpi=110)
print('ok')
