"""Annotated copies of the sources showing what was read (3d/annotated/). Run from anywhere: python3 make_annotations.py"""
import json, sys, numpy as np
from PIL import Image, ImageDraw
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
HERE = __file__.rsplit('/', 1)[0]; sys.path.insert(0, HERE); import b3d_lib as L
R = HERE + '/../../../../03_images/reefs/cables-reef-wa/'; OUT = HERE + '/annotated/'
CO, T = L.CO, json.load(open(HERE + '/../scripts/a2_trace.json')); M = json.loads(open(HERE + '/model.js').read().split('window.REEF_MODEL =', 1)[1].rsplit(';', 1)[0])
s = CO['scale_px_per_m']; uc, vc = CO['centroid_px_asbuilt']
def px(x_model, y):         # model (x south, y west) -> A2 px
    xc = -x_model; return (uc + xc * s, vc - (y - 270.0) * s)
# A1: A2 with the printed dimensions used for scale and the MODEL contours drawn over the DRAWN ones
im = Image.open(R + 'cables-reef-wa_p8-figA2-design-lyons-1992_1992.png').convert('RGB'); d = ImageDraw.Draw(im, 'RGBA'); E = T['scale_evidence']
for k, col in (('transect_left_26.0m', (0, 70, 220)), ('transect_right_30.0m', (0, 70, 220))):
    p0, p1 = E[k]['px']; d.line([tuple(p0), tuple(p1)], fill=col + (255,), width=3); d.text((p1[0] + 6, p1[1] - 4), '%s = %.0f px -> %.2f px/m' % (k.split('_')[-1], E[k]['len_px'], E[k]['px_per_m']), fill=col)
d.line([(560, 91), (560, 349.5)], fill=(200, 0, 200, 255), width=3); d.text((566, 200), 'printed 40.0 m = 258 px -> 6.46 px/m', fill=(200, 0, 200))
for y, t in zip(E['centreline_x560_rows_used'], ['RL -3.0 (set-out edge)', '-2.5', '-2.0', '-1.5', '-1.0 (crest edge)']):
    d.ellipse((556, y - 3, 564, y + 3), outline=(200, 0, 200), width=2); d.text((470, y - 6), t, fill=(200, 0, 200))
for c in M['contours']:
    for ln in c['lines']:
        q = [px(p[0], p[1]) for p in ln]; d.line(q, fill=(255, 120, 0, 255), width=2)
d.text((10, 6), 'A1  Blacka et al. (2013) Fig A.2 (cables-reef-wa-img-26): BLUE/MAGENTA = printed dimensions read for the scale (mean 6.51 px/m);', fill=(0, 0, 0))
d.text((10, 20), 'ORANGE = model contours RL -2.5 / -2.0 / -1.5 (distance-ratio surface) drawn over the printed contours (rms 0.16 m on the centreline)', fill=(255, 100, 0))
im.save(OUT + 'A1_A2_scale_and_contours_read.png')
# A2: centreline profile (model frame x = -11.9 m i.e. canonical +11.9 m) bed / surface / water
dflt = M['versions'][0]; G = dflt['grid']; import base64
H = np.frombuffer(base64.b64decode(G['h_cm_b64']), dtype='<i2').reshape(G['ny'], G['nx']).astype(float) / 100
xc = 11.9; xm = -xc; ix = int(round((xm - G['x0']) / G['step']))
ys = G['y0'] + np.arange(G['ny']) * G['step']; surf = np.where(H[:, ix] == -327.68, np.nan, H[:, ix])
bed = np.array([-(M['validation']['D0_bed_depth_at_y270_RL'] + (y - 270.0) / 30.0) - 0.78 for y in ys])
fig, ax = plt.subplots(figsize=(10, 4.5)); ax.plot(ys, bed, color='#8a6d3b', label='modelled existing bed (plane 1:30, RL -%.2f m at y=270)' % M['validation']['D0_bed_depth_at_y270_RL'])
ax.plot(ys, surf, color='#444', lw=2, label='reef surface on the centreline x = %.1f m (design RL -1.0 crest to -3.0 set-out)' % xm)
for lv in M['levels']: ax.axhline(lv['z'], color='#4aa3df', lw=0.8, ls='--'); ax.text(ys[0] + 1, lv['z'] + 0.04, lv['id'] + ' ' + ('%+.2f' % lv['z']), fontsize=8, color='#2a6f9f')
ax.set_xlabel('y offshore (west), m'); ax.set_ylabel('z, m relative to MSL (reading A: z = RL - 0.78)'); ax.legend(fontsize=8, loc='lower left'); ax.grid(alpha=.3)
ax.set_title('A2  Centreline section through the apex (heights exaggerated about 5x)', fontsize=10); fig.tight_layout(); fig.savefig(OUT + 'A2_centreline_section.png', dpi=110)
# A3: bed calibration
Dv = np.linspace(2.0, 5.0, 25); Vv = []
sil_a = L.raster(CO['v_asbuilt_m']); ramp, zr, om, im_ = L.ramp_distance_surface(CO['v_orig_m'], CO['ramp_m']); zr = np.where(ramp, zr, 0.0)
EXT = L.raster(CO['tri_m']) & ~L.raster(CO['v_orig_m'])
for D in Dv:
    bf = lambda x, y, D=D: -(D + (y - 270.0) / 30.0); xx, yy, bed_, sf, band = L.surfaces(sil_a, ramp, zr, bf, ext_mask=EXT & sil_a, ext_volume=320.0); Vv.append(L.volume(sf, bed_)[0])
fig, ax = plt.subplots(figsize=(7.5, 4.5)); ax.plot(Dv, Vv, color='#222', lw=2)
for v, c, n in ((5500, '#d62728', 'Blacka 2013 A.1.3'), (5000, '#ff7f0e', 'Mead & Borrero 2011 / ICM'), (3500, '#2ca02c', 'Wikipedia')):
    D = M['validation']['D0_for_stated_volumes'][str(v)]; ax.axhline(v, color=c, ls='--', lw=1); ax.plot([D], [v], 'o', color=c); ax.text(2.02, v + 120, '%s: %d m3 -> bed %.2f m' % (n, v, D), fontsize=8, color=c)
ax.set_xlabel('bed depth below the datum at y = 270 m (RL, m)'); ax.set_ylabel('modelled rock volume, m3'); ax.grid(alpha=.3)
ax.set_title('A3  Bed level fitted to the stated rock volume (free parameter)', fontsize=10); fig.tight_layout(); fig.savefig(OUT + 'A3_bed_level_vs_volume.png', dpi=110)
# A4: Pitt sketch contour rows read (bed gradient)
im = Image.open(R + 'cables-reef-wa_rwr-pitt-sketch-plan_1990s.jpg').convert('RGB'); S = 3.0; im = im.resize((int(im.width * S), int(im.height * S)), Image.LANCZOS); d = ImageDraw.Draw(im, 'RGBA')
left = [(7, 115), (6, 139), (5, 159), (4, 193), (3, 212)]; right = [(7, 139), (6, 166), (5, 195.6)]
for dep, y in left: d.line([(40 * S, y * S), (110 * S, y * S)], fill=(220, 0, 0, 255), width=2); d.text((30 * S, y * S - 10), '%d.0' % dep, fill=(220, 0, 0))
for dep, y in right: d.line([(215 * S, y * S), (265 * S, y * S)], fill=(0, 0, 220, 255), width=2); d.text((268 * S, y * S - 10), '%d.0' % dep, fill=(0, 0, 220))
sc0, sc1 = 74, 245; d.line([(sc0 * S, 296 * S), (sc1 * S, 296 * S)], fill=(0, 140, 0, 255), width=3); d.text((sc0 * S, 296 * S + 6), 'scale bar 0-200 m = 171 px (0.855 px/m)', fill=(0, 140, 0))
d.text((8, 8), 'A4  Pitt sketch (cables-reef-wa-img-07): contour label rows read on the left (red) and right (blue);', fill=(0, 0, 0)); d.text((8, 22), 'left 24.3 px/m of depth = 28 m per m (1:28); right 28.3 px/m = 33 m per m (1:33); used 1:30', fill=(0, 0, 0))
im.save(OUT + 'A4_pitt_sketch_bed_gradient_read.png')
print('annotated done')
