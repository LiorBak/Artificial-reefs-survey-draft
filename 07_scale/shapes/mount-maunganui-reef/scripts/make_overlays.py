"""Final overlays + pixel polygons for the three traced images (img1 Fig 3, img2 LINZ aerial, img3 ASR Installed).
Writes ../overlays/img1_boprc_fig3_2013.png, img2_linz_aerial_2010-11.png, img3_asr_installed.png and ../work_pixel_polygons.json."""
import json, math, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi
sys.path.insert(0, '.')
from geo_tools import *
os.makedirs(ROOT + 'overlays', exist_ok=True)
surv = json.load(open(ROOT + 'work_polys_fig3_m20_v2.json'))
toe = json.load(open(ROOT + 'work_installed_toe_fig3px.json'))['-4.2']
reg = json.load(open(ROOT + 'work_installed_reg.json'))
s, th, tx, ty = reg['s'], reg['theta_deg'], reg['tx'], reg['ty']
c, sn = math.cos(math.radians(th)), math.sin(math.radians(th))
H_I = 519
def f3_to_inst(x, y):        # Fig 3 px -> Installed ORIGINAL px
    dx, dy = x - tx, y - ty
    xr = s * (c * dx + sn * dy); yr = s * (-sn * dx + c * dy)      # rotated (CW 90) Installed px
    return (yr, H_I - 1 - xr)
inst_toe = [[f3_to_inst(x, y) for x, y in p] for p in toe]
inst_surv = [[f3_to_inst(x, y) for x, y in p] for p in surv]
lz_surv = [[f3_to_lz(x, y) for x, y in p] for p in surv]
lz_toe = [[f3_to_lz(x, y) for x, y in p] for p in toe]
try: F = ImageFont.truetype('arial.ttf', 16); Fs = ImageFont.truetype('arial.ttf', 13)
except Exception: F = Fs = ImageFont.load_default()
def poly(d, p, col, w=2, close=True):
    pts = [tuple(q) for q in p]; d.line(pts + ([pts[0]] if close else []), fill=col, width=w)
def scalebar(d, x, y, px_per_m, metres, label=None):
    L = px_per_m * metres; d.rectangle([x - 4, y - 24, x + L + 70, y + 10], fill=(0, 0, 0, 160) if False else (0, 0, 0))
    d.line([(x, y), (x + L, y)], fill=(255, 255, 255), width=3); d.line([(x, y - 6), (x, y + 6)], fill=(255, 255, 255), width=2); d.line([(x + L, y - 6), (x + L, y + 6)], fill=(255, 255, 255), width=2)
    d.text((x + L + 6, y - 9), label or f'{metres} m', fill=(255, 255, 255), font=F)
def legend(d, x, y, items):
    d.rectangle([x - 6, y - 6, x + 520, y + 22 * len(items) + 2], fill=(0, 0, 0))
    for i, (col, txt) in enumerate(items):
        d.line([(x, y + 22 * i + 9), (x + 28, y + 22 * i + 9)], fill=col, width=3); d.text((x + 36, y + 22 * i), txt, fill=(255, 255, 255), font=Fs)
YEL, MAG, WHT, CYA = (255, 235, 0), (255, 0, 255), (255, 255, 255), (0, 255, 255)
# ---------- overlay 1: Fig 3
im = Image.open(ROOT + 'src/boprc_fig3_2013_survey.png').convert('RGB'); k = 2
box = (200, 340, 700, 780)
c1 = im.crop(box).resize(((box[2]-box[0]) * k, (box[3]-box[1]) * k), Image.LANCZOS); d = ImageDraw.Draw(c1)
sh = lambda p: [((x - box[0]) * k, (y - box[1]) * k) for x, y in p]
for p in toe: poly(d, sh(p), MAG, 2)
for p in surv: poly(d, sh(p), YEL, 3)
scalebar(d, 30, c1.height - 30, F3_PXM * k, 20)
legend(d, 20, 20, [(YEL, 'img1 outlines: -2.0 m CD contour of the 2013-07-18 multibeam (5 polygons, 1071 m2)'), (MAG, 'ASR "Installed" toe-level outline registered onto this survey (img3)')])
d.text((c1.width - 330, c1.height - 28), 'BoPRC 2014 Fig 3; px/m = 5.45 (NZ-grid ticks); north up', fill=WHT, font=Fs)
c1.save(ROOT + 'overlays/img1_boprc_fig3_2013.png')
# ---------- overlay 2: LINZ aerial (contrast-stretched copy)
a = np.array(Image.open(ROOT + 'src/linz_aerial_2010-11_BD37_1000_1314_crop.png').convert('RGB')).astype(float)
lo = np.percentile(a, 1, axis=(0, 1)); hi = np.percentile(a, 99.5, axis=(0, 1))
b = Image.fromarray((((a - lo) / (hi - lo)).clip(0, 1) ** 0.8 * 255).astype(np.uint8))
box2 = (250, 300, 900, 950); k2 = 1.5
c2 = b.crop(box2).resize((int((box2[2]-box2[0]) * k2), int((box2[3]-box2[1]) * k2)), Image.LANCZOS); d = ImageDraw.Draw(c2)
sh2 = lambda p: [((x - box2[0]) * k2, (y - box2[1]) * k2) for x, y in p]
for p in lz_toe: poly(d, sh2(p), MAG, 2)
for p in lz_surv: poly(d, sh2(p), YEL, 3)
scalebar(d, 30, c2.height - 30, 8.0 * k2, 20)
legend(d, 20, 20, [(YEL, 'img1 -2.0 m CD survey outlines projected via BOPTM -> NZTM (no shift applied)'), (MAG, 'ASR "Installed" toe-level outline (img3), same projection'),
                  (WHT, 'best-fit shift of survey vs aerial red mass: 0.5 m W, 1.75 m S (see METHOD)')])
d.text((c2.width - 560, c2.height - 28), 'LINZ Bay of Plenty 0.125 m aerial, flown 2010-12-28..2011-03-31, CC BY 4.0; contrast-stretched', fill=WHT, font=Fs)
c2.save(ROOT + 'overlays/img2_linz_aerial_2010-11.png')
# ---------- overlay 3: ASR Installed (original orientation)
im3 = Image.open(ROOT + 'src/mount-reef-installed.jpg').convert('RGB'); k3 = 2
c3 = im3.resize((im3.width * k3, im3.height * k3), Image.LANCZOS); d = ImageDraw.Draw(c3)
sh3 = lambda p: [(x * k3 + k3 / 2, y * k3 + k3 / 2) for x, y in p]
for p in inst_surv: poly(d, sh3(p), YEL, 2)
for p in inst_toe: poly(d, sh3(p), MAG, 3)
ppm_I = 5.45 * s
scalebar(d, 40, c3.height - 30, ppm_I * k3, 20)
legend(d, 40, 22, [(MAG, 'toe-level outline: depth shallower than -4.2 m (legend datum), area 1424 m2'), (YEL, 'img1 -2.0 m CD survey outlines mapped into this image')])
d.text((40, c3.height - 60), 'ASR "Installed" (RWR): scale 5.96 px/m from registration to img1 (+-6 %; axis ticks would give 6.27); north is to the LEFT', fill=WHT, font=Fs)
c3.save(ROOT + 'overlays/img3_asr_installed.png')
json.dump(dict(img1=surv, img2=lz_surv, img3=inst_toe, img3_survey_outlines=inst_surv, img2_toe=lz_toe), open(ROOT + 'work_pixel_polygons.json', 'w'))
print('ok', c1.size, c2.size, c3.size)
