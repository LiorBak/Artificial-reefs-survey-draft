"""Renders overlays/ from polys_px.json + build_out.json (re-runnable). python -I make_overlays.py"""
import json, math, numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
H = '..'; P = json.load(open('polys_px.json')); O = json.load(open('build_out.json'))
def font(sz):
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', sz)
    except Exception: return ImageFont.load_default()
# 1 satellite trace
im = Image.open(f'{H}/src/esri_current_2026-01-20_z18.png').convert('RGB')
box = (300, 330, 800, 700); sc = 2
c = im.crop(box).resize(((box[2]-box[0])*sc, (box[3]-box[1])*sc), Image.LANCZOS); d = ImageDraw.Draw(c, 'RGBA')
T = lambda p: ((p[0]-box[0])*sc, (p[1]-box[1])*sc)
mask = json.load(open('mask30_px.json'))
d.line([T(p) for p in mask] + [T(mask[0])], fill=(0, 255, 255, 255), width=2)
poly = [T(p) for p in P['sat2026_trace']]; d.polygon(poly, fill=(255, 0, 0, 40)); d.line(poly + [poly[0]], fill=(255, 40, 40, 255), width=3)
for i, p in enumerate(poly): d.ellipse([p[0]-4, p[1]-4, p[0]+4, p[1]+4], fill=(255, 255, 0, 255))
# scale bar 50 m
mpp = O['mpp']; L = 50/mpp*sc; x0, y0 = 20, c.size[1]-30; d.line([(x0, y0), (x0+L, y0)], fill=(255, 255, 255, 255), width=4); d.text((x0, y0-22), '50 m (0.489 m/px, z18)', fill=(255, 255, 255, 255), font=font(14))
d.text((10, 8), 'Esri World Imagery, captured 2026-01-20 | red = traced outline (20 vertices) | cyan = objective dark-patch mask (green<30)', fill=(255, 255, 255, 255), font=font(13))
c.save(f'{H}/overlays/sat2026-01-20_trace.png')
# 2 design diagram
im = Image.open(f'{H}/src/rwr_bluecoast_design_diagram.png').convert('RGB'); sc = 2
box = (440, 230, 820, 702)
c = im.crop(box).resize(((box[2]-box[0])*sc, (box[3]-box[1])*sc), Image.LANCZOS); d = ImageDraw.Draw(c, 'RGBA')
T = lambda p: ((p[0]-box[0])*sc, (p[1]-box[1])*sc)
poly = [T(p) for p in P['design_diagram_trace']]; d.polygon(poly, fill=(255, 0, 0, 30)); d.line(poly + [poly[0]], fill=(255, 0, 0, 255), width=3)
for x, lab in ((493.5, '0'), (569.5, '50 m'), (645.5, '100 m')):
    X, Y = T((x, 678)); d.line([(X, Y-24), (X, Y+24)], fill=(255, 0, 255, 255), width=3); d.text((X-14, Y+26), lab, fill=(255, 0, 255, 255), font=font(14))
d.line([T((520, 300)), T((765, 335))], fill=(0, 160, 255, 255), width=2)
d.text((8, 6), 'Bluecoast final-design plan (north up): red = outermost design contour; magenta = scale-bar ticks 493.5/569.5/645.5 px; blue = dashed crest line', fill=(0, 0, 0, 255), font=font(12))
c.save(f'{H}/overlays/design_diagram_trace.png')
# 3 canonical frame comparison
fig, ax = plt.subplots(figsize=(8.5, 7))
s = np.array(O['sat']['polygon_m']); g = np.array(O['design']['polygon_m'])
ax.fill(g[:, 0], g[:, 1], color='tab:orange', alpha=.35, label=f"Design outline (Bluecoast, outermost contour) {O['design']['area_m2']:.0f} m2")
ax.fill(s[:, 0], s[:, 1], color='tab:blue', alpha=.35, label=f"Satellite trace 2026-01-20 {O['sat']['area_m2']:.0f} m2")
ax.axhline(0, color='goldenrod', lw=3, label='beach-face line (dry-sand edge, 2026-01-20 image) y=0')
ax.plot([0], [0], 'k+'); ax.set_aspect('equal'); ax.invert_yaxis(); ax.set_xlabel('x alongshore (m, toward NNE %.0f deg true)' % O['shoreline']['bearing_deg']); ax.set_ylabel('y offshore (m, toward %.0f deg true)' % O['shoreline']['shore_normal_bearing_deg'])
ax.set_ylim(300, -10); ax.set_xlim(-110, 110); ax.grid(alpha=.3); ax.legend(loc='lower left', fontsize=8)
ax.set_title('southern-ocean-surf-reef-albany: outline versions in the canonical frame (y down = offshore)', fontsize=10)
fig.tight_layout(); fig.savefig(f'{H}/overlays/canonical_versions_m.png', dpi=110)
# 4 shoreline fit
im = Image.open(f'{H}/src/esri_current_2026-01-20_z18.png').convert('RGB'); d = ImageDraw.Draw(im, 'RGBA')
for x, y in O['shoreline']['points_px']: d.ellipse([x-4, y-4, x+4, y+4], fill=(255, 255, 0, 255))
b = math.radians(O['shoreline']['bearing_deg']); ox, oy = O['origin_enu_from_centre']
# shoreline line through foot point (east,north metres from centre)
fx, fy = 511 + ox/mpp, 511 - oy/mpp; dx, dy = math.sin(b)/mpp, -math.cos(b)/mpp
d.line([(fx-600*dx/ (abs(dy)+abs(dx)), fy-600*dy/(abs(dy)+abs(dx))), (fx+600*dx/(abs(dy)+abs(dx)), fy+600*dy/(abs(dy)+abs(dx)))], fill=(255, 0, 0, 255), width=3)
pg = [tuple(p) for p in P['sat2026_trace']]; d.line(pg+[pg[0]], fill=(0, 255, 255, 255), width=2)
d.text((10, 10), 'yellow = beach-face (dry-sand edge) points (rows 40-320, 440-720); red = Theil-Sen line, rows 440-720, bearing %.1f deg' % O['shoreline']['bearing_deg'], fill=(255, 255, 255, 255), font=font(14))
im.resize((800, 800), Image.LANCZOS).save(f'{H}/overlays/shoreline_fit.png')
# 5 before/after
a = Image.open(f'{H}/src/esri_wayback13192_2025-01-16_z18.png').convert('RGB').crop((340, 340, 800, 700)); b2 = Image.open(f'{H}/src/esri_current_2026-01-20_z18.png').convert('RGB').crop((340, 340, 800, 700))
w = Image.new('RGB', (920, 380), 'white'); w.paste(a, (0, 20)); w.paste(b2, (460, 20)); d = ImageDraw.Draw(w); d.text((6, 3), 'Esri Wayback 13192, captured 2025-01-16 (before construction)', fill=(0, 0, 0), font=font(12)); d.text((466, 3), 'Esri current, captured 2026-01-20 (reef built)', fill=(0, 0, 0), font=font(12))
w.save(f'{H}/overlays/before_after_2025-01-16_vs_2026-01-20.png')
print('ok')
