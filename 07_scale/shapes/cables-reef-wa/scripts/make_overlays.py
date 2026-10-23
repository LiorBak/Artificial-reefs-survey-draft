"""Render overlays from computed.json / a2_trace.json. Run from the shape folder: python3 scripts/make_overlays.py"""
import json, numpy as np
from PIL import Image, ImageDraw
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
R = '../../../03_images/reefs/cables-reef-wa/'
C = json.load(open('scripts/computed.json')); T = json.load(open('scripts/a2_trace.json'))
RED, BLUE, GRN, ORG, MAG = (230, 0, 0), (0, 70, 220), (0, 150, 60), (255, 130, 0), (200, 0, 200)
def draw(img, scale, polys, out, pts=(), lines=(), labels=(), rot=0, crop=None):
    im = Image.open(img).convert('RGB')
    if rot: im = im.rotate(rot, expand=True)
    im = im.resize((int(im.width*scale), int(im.height*scale)), Image.LANCZOS); d = ImageDraw.Draw(im, 'RGBA')
    for poly, col, fill in polys:
        q = [(x*scale, y*scale) for x, y in poly]
        if fill: d.polygon(q, fill=col+(fill,))
        d.line(q+[q[0]], fill=col+(255,), width=2)
    for (p0, p1), t, col in lines:
        d.line([(p0[0]*scale, p0[1]*scale), (p1[0]*scale, p1[1]*scale)], fill=col+(255,), width=3); d.text((p1[0]*scale+6, p1[1]*scale-6), t, fill=col)
    for (x, y), t, col in pts:
        d.ellipse((x*scale-4, y*scale-4, x*scale+4, y*scale+4), outline=col, width=2); d.text((x*scale+6, y*scale-12), t, fill=col)
    for (x, y), t, col in labels: d.text((x, y), t, fill=col)
    im.save(out)
E=T['scale_evidence']
# A2 (primary): silhouette, ramp polygon, extension triangle, scale-evidence lines
draw(R+'cables-reef-wa_p8-figA2-design-lyons-1992_1992.png', 1.3,
     [([tuple(p) for p in T['silhouette_px']], RED, 30), ([tuple(p) for p in T['ramp_px']], GRN, 0), ([tuple(p) for p in C['tri_px_A2']], ORG, 90)],
     'overlays/cables-reef-wa-img-26_A2_outline_ramp_scale.png',
     lines=[(tuple(map(tuple, E['transect_left_26.0m']['px'])), '26.0 m = %.0f px (%.2f px/m)' % (E['transect_left_26.0m']['len_px'], E['transect_left_26.0m']['px_per_m']), BLUE),
            (tuple(map(tuple, E['transect_right_30.0m']['px'])), '30.0 m = %.0f px (%.2f px/m)' % (E['transect_right_30.0m']['len_px'], E['transect_right_30.0m']['px_per_m']), BLUE),
            (((560, 91), (560, 349.5)), '40.0 m = 258 px (6.46 px/m)', MAG)],
     pts=[((560, y), t, MAG) for y, t in zip(E['centreline_x560_rows_used'], ['-3.0 set-out', '-2.5', '-2.0', '-1.5', '-1.0 crest'])],
     labels=[((10, 6), 'RED = outer foot (interface line) traced; GREEN = design ramp (set-out line RL -3.0 .. crest line RL -1.0); ORANGE = extension triangle (img-06)', RED),
             ((10, 20), 'BLUE / MAGENTA = printed dimensions used for scale: mean %.2f px/m (sd %.2f), 4 readings' % (E['scale_mean_px_per_m'], E['scale_sd']), BLUE)])
# img-05 re-trace at assumed scale
draw(R+'cables-reef-wa_rwr-original-design-plan_1990s.jpg', 2.5, [([tuple(p) for p in json.load(open('scripts/p05_toe_pixels.json'))['polys'][0]], RED, 40)],
     'overlays/cables-reef-wa-img-05_retrace_outer_foot.png',
     labels=[((10, 6), 'img-05 (RWR copy of the same drawing, 478 px wide): independent re-trace; no legible scale (3.6 px/m assumed: area %.0f m2 vs %.0f m2 on A2)' % (C['v_img05']['area_m2'], C['v_orig']['area_m2']), RED)])
# img-06: triangle
draw(R+'cables-reef-wa_rwr-additional-fill-area-plan_1990s.jpg', 2.5, [([(76.7, 190), (165, 212.7), (111.7, 248.3)], ORG, 90)], 'overlays/cables-reef-wa-img-06_extension_triangle.png',
     pts=[((76.7, 190), 'P2 (reg.)', BLUE), ((165, 212.7), 'P1 (reg.)', BLUE), ((111.7, 248.3), 'N', BLUE)])
draw(R+'cables-reef-wa_pattiaratchi1999-fig7-geographic-location_1999.png', 3.2, [([tuple(p) for p in C['fig7_px']], RED, 40)], 'overlays/cables-reef-wa-img-20_fig7_V_outline_rotated.png', rot=-90)
draw(R+'cables-reef-wa_rwr-pitt-sketch-plan_1990s.jpg', 2.5, [([tuple(p) for p in C['pitt_px']], BLUE, 30)], 'overlays/cables-reef-wa-img-07_pitt_concept_outline.png')
# comparison in metres
fig, ax = plt.subplots(figsize=(9, 6.5))
cols = {'v_asbuilt_m': ('#d62728', 'default: design plan + extension (A2 trace, 6.51 px/m)', 1.8), 'v_orig_m': ('#ff7f0e', 'design plan without extension (A2)', 1.2), 'v_img05_m': ('#9467bd', 'img-05 re-trace (assumed 3.6 px/m)', 1.0), 'fig7_m': ('#2ca02c', 'paper Fig 7 V outline (assumed 100 m grid)', 1.2), 'pitt_m': ('#1f77b4', 'Pitt concept sketch (proposal, centroid aligned)', 1.2)}
for k, (c, l, w) in cols.items():
    p = np.array(C[k]); ax.plot(*np.vstack([p, p[:1]]).T, color=c, lw=w, label=l)
ax.set_aspect('equal'); ax.grid(alpha=.3); ax.legend(fontsize=8, loc='lower left')
ax.set_xlabel('alongshore, m (+ = north)'); ax.set_ylabel('offshore, m from the shore line (+ = west); centroids placed at 270 m')
ax.set_title('cables-reef-wa outline versions in metres', fontsize=10); fig.tight_layout(); fig.savefig('overlays/cables-reef-wa_versions_compare_m.png', dpi=110)
