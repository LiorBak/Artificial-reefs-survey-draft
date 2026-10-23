"""cables-reef-wa: annotated figures (own work) for the imagery + bathymetry verification of 2026-10-10.
Outputs: ../src/imagery/annotated/overlay_<image>.png (georeferenced outline on each Esri image; yellow = with extension, magenta = original plan),
../src/imagery/annotated/overlay_montage_4dates.png, ../src/bathymetry/figures/{survey_1999_thickness.png, survey_2002_thickness.png, bed_perth5m_contours.png}.
numpy, scipy, PIL, matplotlib, pyproj, shapely; satellite.py (07_scale/tools) for the Web-Mercator maths."""
import sys, json, numpy as np
HERE = __file__.rsplit('/', 1)[0]
sys.path.insert(0, HERE + '/../../../tools'); import satellite as S
exec(open(HERE + '/georef_fit.py').read().split("res = differential_evolution")[0])
G = json.load(open(HERE + '/georef.json'))['transform']; th, tx, ty = G['theta_ccw_deg'], G['anchor_E_MGA50_GDA94'] - CX, G['anchor_N_MGA50_GDA94'] - CY
Wo = world(poly0, th, tx, ty); We = world(poly_ext, th, tx, ty)
from PIL import Image, ImageDraw, ImageOps, ImageEnhance
IM = HERE + '/../src/imagery/'; OUT = IM + 'annotated/'
def px_poly(W, geo):
    z = geo['zoom']; b = geo['bounds']; x0, y0 = S.deg2num_frac(b['north'], b['west'], z)
    pts = []
    for x, y in W:
        lo, la = Ti.transform(CX + x, CY + y); a, c = S.deg2num_frac(la, lo, z); pts.append((a - x0, c - y0))
    return pts
names = {'esri_wayback_2014-12-03_z19': 'Wayback release 2014-12-03', 'esri_wayback_2020-03-23_z19': 'Wayback release 2020-03-23', 'esri_wayback_2022-06-08_z19': 'Wayback release 2022-06-08',
         'esri_wayback_2024-08-15_z19': 'Wayback release 2024-08-15', 'esri_world_imagery_2025-12-06_z19': 'World Imagery, captured 2025-12-06'}
crops = []
for n, lab in names.items():
    im = Image.open(IM + n + '.png').convert('RGB'); geo = json.load(open(IM + n + '.png.geo.json'))
    im = ImageOps.autocontrast(im, cutoff=0.5); im = ImageEnhance.Brightness(im).enhance(1.25)
    d = ImageDraw.Draw(im)
    for W, c in ((Wo, (255, 0, 255)), (We, (255, 255, 0))):
        pp = px_poly(W, geo); d.line(pp + [pp[0]], fill=c, width=3)
    pp = px_poly(Wo, geo); cxp = np.mean([p[0] for p in pp]); cyp = np.mean([p[1] for p in pp]); hw = 480
    cr = im.crop((int(cxp - hw), int(cyp - hw), int(cxp + hw), int(cyp + hw))).resize((900, 900), Image.LANCZOS)
    dd = ImageDraw.Draw(cr); dd.rectangle((0, 0, 560, 24), fill=(0, 0, 0)); dd.text((6, 6), lab + ' | contrast-stretched | outline = georeferenced design plan (magenta), + extension (yellow)', fill=(255, 255, 255))
    cr.save(OUT + 'overlay_' + n + '.png'); crops.append(cr.resize((600, 600), Image.LANCZOS))
sh = Image.new('RGB', (1200, 1200))
for i, k in enumerate((0, 1, 2, 4)): sh.paste(crops[k], ((i % 2) * 600, (i // 2) * 600))
sh.save(OUT + 'overlay_montage_4dates.png')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def thick_fig(arr, title, out, vmax=3):
    q = arr[:, :2] - [CX, CY]; t = arr[:, 2] - bed_at(arr[:, :2]); m = (abs(q[:, 0] - tx) < 100) & (abs(q[:, 1] - ty) < 100)
    fig, ax = plt.subplots(figsize=(8, 8)); sc = ax.scatter(q[m, 0] - tx, q[m, 1] - ty, c=t[m], s=8, cmap='RdYlBu_r', vmin=-0.5, vmax=vmax)
    for W, c in ((Wo, 'k'), (We, 'm')): ax.plot(*(np.r_[W, W[:1]] - [tx, ty]).T, c, lw=1.2)
    ax.set_aspect('equal'); ax.set_xlim(-70, 90); ax.set_ylim(-70, 90); ax.grid(alpha=.3); ax.set_xlabel('east of the anchor (m, MGA50)'); ax.set_ylabel('north of the anchor (m)')
    fig.colorbar(sc, shrink=.7, label='sounding minus 1998 bed (m)'); ax.set_title(title, fontsize=9); fig.tight_layout(); fig.savefig(out, dpi=110); plt.close(fig)
B2 = HERE + '/../src/bathymetry/figures/'
thick_fig(post, 'DoT WA soundings Nov 1999 (FR19991122), rock thickness over the 1998 bed.\nBlack = original design plan, magenta = with extension, georeferenced (scripts/georef_fit.py)', B2 + 'survey_1999_thickness.png', 4)
thick_fig(p02, 'DoT WA soundings Feb 2002 (FR20020201), thickness over the 1998 bed.\nBlack = original plan, magenta = with extension; the extension triangle (SE) shows little rock', B2 + 'survey_2002_thickness.png', 3)
z = np.load(HERE + '/../src/bathymetry/DoT_Perth_5m_clip_reef.npz'); a = z['z_AHD'].astype(float); a[a < -9000] = np.nan; xl, yt, px = float(z['x_left']), float(z['y_top']), float(z['pixel'])
E0, N0 = G['anchor_E_MGA50_GDA94'], G['anchor_N_MGA50_GDA94']
X = xl + (np.arange(a.shape[1]) + .5) * px - E0; Y = yt - (np.arange(a.shape[0]) + .5) * px - N0
fig, ax = plt.subplots(figsize=(8, 8)); im = ax.imshow(a, cmap='nipy_spectral', vmin=-9, vmax=0, extent=[X[0] - px / 2, X[-1] + px / 2, Y[-1] - px / 2, Y[0] + px / 2])
cs = ax.contour(X, Y[::-1], a[::-1], levels=np.arange(-9, 0.5, 1.0), colors='k', linewidths=.4); ax.clabel(cs, fontsize=6, fmt='%.0f')
for W, c in ((Wo, 'w'),): ax.plot(*(np.r_[W, W[:1]] - [tx, ty]).T, c, lw=1.2)
ax.set_xlim(-300, 350); ax.set_ylim(-350, 300); ax.set_xlabel('east of the anchor (m)'); ax.set_ylabel('north of the anchor (m)'); fig.colorbar(im, shrink=.7, label='m AHD')
ax.set_title('DoT WA composite surface Perth_5m (AHD), contours every 1 m. White = reef outline (original plan).\nThe composite includes the reef as a smoothed shallow mound (about -2 m AHD).', fontsize=9); fig.tight_layout(); fig.savefig(B2 + 'bed_perth5m_contours.png', dpi=110)
print('ok')
