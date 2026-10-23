"""make_annotations.py - annotated copies of the sources and the check figures -> annotated/ (A1..A6). Run after build_3d.py."""
import os, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MP
HERE = os.path.dirname(os.path.abspath(__file__)); BASE = os.path.dirname(HERE); ANN = os.path.join(HERE, 'annotated'); SRC = os.path.join(HERE, 'src')
GOV = os.path.join(BASE, 'src', 'gov')
shape = json.load(open(os.path.join(BASE, 'shape.json'), encoding='utf-8'))
M = json.loads(open(os.path.join(HERE, 'model.js'), encoding='utf-8').read().split('window.REEF_MODEL = ', 1)[1].rstrip().rstrip(';'))
mb = np.load(os.path.join(SRC, 'multibeam_fig3.npz')); st = json.load(open(os.path.join(SRC, 'multibeam_fig3.json')))
V = {v['id']: v for v in M['versions']}
A = 0.12


def font(sz):
    for f in ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
        if os.path.exists(f): return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


def tag(d, xy, text, fill=(255, 255, 255), bg=(0, 0, 0), sz=15):
    f = font(sz); b = d.textbbox(xy, text, font=f); d.rectangle((b[0] - 3, b[1] - 2, b[2] + 3, b[3] + 2), fill=bg); d.text(xy, text, fill=fill, font=f)


def a1():
    im = np.array(Image.open(os.path.join(GOV, 'corbett2023_extracted', 'p3_x86.png')).convert('RGB'))
    fig, ax = plt.subplots(1, 2, figsize=(15, 5.6), gridspec_kw=dict(width_ratios=[1.35, 1]))
    ax[0].imshow(im); ax[0].set_title('Corbett et al. 2023 Fig 3 (img-55): what was read', fontsize=10)
    for x, lab in ((274, '0 m'), (295, '10 m'), (317, '20 m')):
        ax[0].plot([x, x], [290, 300], color='red', lw=1.5); ax[0].text(x, 287, lab, color='red', fontsize=8, ha='center', va='bottom', fontweight='bold')
    ax[0].text(296, 311, 'bar ticks: 21.5 px = 10 m -> 0.4651 m/px', color='red', fontsize=7.5, ha='center', va='bottom')
    for y, v in ((140, -1), (198, -4), (253, -6), (305, -9)):
        ax[0].plot([380, 432], [y, y], color='black', lw=1); ax[0].text(383, y - 3, 'tick label %d at y=%d px' % (v, y), color='black', fontsize=6.5, va='bottom')
    ax[0].text(405, 128, 'depth = -0.0472 y + 5.58 (m)\nresiduals 0.03/-0.23/0.37/-0.17', fontsize=6.5, ha='center', va='bottom', color='black')
    # registered polygons
    s = st['scale_m_per_px']; tx, ty = st['tx'], st['ty']; W, H = st['map_px']
    xh = (-math.sin(math.radians(3.8)), math.cos(math.radians(3.8))); yh = (math.sin(math.radians(86.2)), math.cos(math.radians(86.2)))
    def px(x, y):
        dx, dy = x - tx, y - ty; E = dx * xh[0] + dy * yh[0]; N = dx * xh[1] + dy * yh[1]; return E / s + W / 2, -N / s + H / 2
    for p in V['photo_2020-08-08']['outline_m'][:2]:
        q = np.array([px(*c) for c in p]); ax[0].plot(q[:, 0], q[:, 1], color='white', lw=1.4)
    for p in V['photo_2020-08-08']['design_loops_m']:
        q = np.array([px(*c) for c in p]); ax[0].plot(q[:, 0], q[:, 1], color='magenta', lw=1.4)
    ax[0].text(8, 304, 'white = traced 2020 arms (shape.json), magenta = Option 2 crest loops (-2.5 AHD)\nplaced at centre (x -5, y 290) m, rotation 0, +-10 m', color='white', fontsize=7, va='bottom', bbox=dict(fc='black', alpha=.6, lw=0))
    ax[0].set_xlim(0, 460); ax[0].set_ylim(312, 100 if False else 0); ax[0].set_xticks([]); ax[0].set_yticks([])
    xs, ys = mb['xs'], mb['ys']; B = mb['bed']; R = mb['R']
    im2 = ax[1].imshow(B, extent=(xs[0], xs[-1], ys[-1], ys[0]), cmap='turbo_r', vmin=-8, vmax=-1.5, aspect='equal')
    ax[1].contour(xs, ys, np.nan_to_num(R, nan=0), levels=[0.8], colors='k', linewidths=0.6)
    for p in V['photo_2020-08-08']['outline_m'][:2]:
        q = np.array(p); ax[1].plot(q[:, 0], q[:, 1], color='white', lw=1)
    ax[1].set_title('derived bed (containers removed by grey opening), m AHD;\nblack = relief > 0.8 m; canonical x (north) / y (offshore) m', fontsize=9)
    ax[1].set_xlabel('x alongshore (m)'); ax[1].set_ylabel('y offshore (m)'); plt.colorbar(im2, ax=ax[1], shrink=0.8, label='bed, m AHD (datum assumed)')
    fig.tight_layout(); fig.savefig(os.path.join(ANN, 'A1_corbett_fig3_digitised.png'), dpi=110); plt.close(fig)


def a2():
    f = os.path.join(BASE, 'overlays', 'navionics_sonar_z18_shade0_with_trace_and_readings.png'); im = Image.open(f).convert('RGB'); k = im.width / 1200.0; d = ImageDraw.Draw(im)
    pts = [((845, 112), '7 -> AHD -7.76, y ~402'), ((876, 256), '8 -> -8.76, y ~411'), ((1015, 130), '9 -> -9.76, y ~474'), ((1105, 96), '10 -> -10.76, y ~514'),
           ((632, 350), '4.0 over N arm: smoothed shoal (crest -2.2 AHD) - not used for the crest'), ((340, 365), '5.5 around arms (not used)'), ((500, 490), '0.9 obstruction label: older crest state, NOT used'),
           ((135, 275), '0.5: chart land edge is ~80 m seaward of our 2020 waterline -> nearshore contours NOT used')]
    for (x, y), t in pts:
        X, Y = x * k, y * k; d.ellipse((X - 14, Y - 14, X + 14, Y + 14), outline=(255, 0, 0), width=4); tag(d, (X + 18, Y - 28), t, fill=(255, 255, 0), sz=22)
    tag(d, (30, im.height - 120), 'Used (red): seabed y 400-515 m = LAT depth + 0.76 below AHD (LAT assumed, MSQ), +-20 m (map centre = reef centroid). img-50, Garmin Navionics, accessed 2026-10-06, not for navigation.', fill=(255, 255, 255), sz=22)
    im.save(os.path.join(ANN, 'A2_navionics_readings_used.png'))


def a3():
    im = Image.open(os.path.join(GOV, 'narrowneck-gold-coast_vieira_da_silva2021_fig3_ten_topo_bathymetric_surveys_2018-2020_native.jpeg')).convert('RGB')
    cr = im.crop((0, 20, 275, 680)).resize((550, 1320), Image.LANCZOS); d = ImageDraw.Draw(cr)
    tag(d, (10, 10), 'Vieira da Silva 2021 Fig 3, survey 1 (19 Jul 2018), m AHD', sz=18)
    d.ellipse((280, 440, 440, 545), outline=(255, 255, 255), width=4)
    tag(d, (12, 600), 'MPAR circle = reef: bed cyan, about -4 to -6 m', fill=(255, 255, 0), sz=18)
    tag(d, (250, 700), 'seaward: blue -7 to -9', fill=(255, 255, 0), sz=18)
    tag(d, (12, 800), 'nearshore within ~100 m of beach:\nyellow-green -1 to -2', fill=(255, 255, 0), sz=18)
    tag(d, (12, 1260), 'read by eye (+-1 m); consistent with Corbett Fig 3 bed -4 .. -7', fill=(255, 255, 255), sz=16)
    cr.save(os.path.join(ANN, 'A3_vieira_fig3_reef_bed_read.png'))


def a4():
    im = Image.open(os.path.join(GOV, 'narrowneck-gold-coast_jackson2012_fig2_reef_levels_original_and_revised_design_300dpi_crop.png')).convert('RGB'); k = im.width / 1200.0; d = ImageDraw.Draw(im)
    for (x, y), t, dx in (((835, 100), 'crest wedge -2.50', 16), ((880, 150), '-3.0 to -5.0 dense', 16), ((1000, 80), 'envelope -6.00', -20), ((1130, 185), 'outer -8.00', -230)):
        X, Y = x * k, y * k; d.ellipse((X - 12, Y - 12, X + 12, Y + 12), outline=(255, 0, 0), width=4); tag(d, (X + dx, Y - 36), t, fill=(255, 255, 0), sz=24)
    tag(d, (20, im.height - 50), 'Fig 2 right (img-04) contour labels read; datum not printed (AHD in the papers)', sz=22)
    im.save(os.path.join(ANN, 'A4_jackson2012_fig2_contours_read.png'))


def decode(g):
    h = np.frombuffer(__import__('base64').b64decode(g['h_cm_b64']), dtype='<i2').reshape(g['ny'], g['nx']).astype(float) / 100
    h[h < -300] = np.nan; return h


def a5():
    sy = np.arange(-40, 521, 5.0); sx = np.arange(-250, 251, 5.0); SB = np.array(M['seabed']['z']) + A
    fig, ax = plt.subplots(figsize=(11, 5.2))
    ys = mb['ys']; B = mb['bed']; med = np.nanmedian(B, axis=1); lo = np.nanpercentile(B, 10, axis=1); hi = np.nanpercentile(B, 90, axis=1)
    ax.fill_between(ys, lo, hi, color='tab:blue', alpha=.25, label='multibeam bed, p10-p90 over x (Corbett Fig 3)'); ax.plot(ys, med, color='tab:blue', lw=1, label='multibeam bed, median')
    D = mb['D']; top = np.array([np.nanmax(r) if np.isfinite(r).any() else np.nan for r in D]); ax.plot(ys, top, color='tab:red', lw=.8, label='shallowest multibeam top (pre-works)')
    ax.plot(sy, SB[:, np.argmin(abs(sx))], 'k', lw=2, label='model seabed (x = 0)')
    g = V['photo_2020-08-08']['grid']; H = decode(g) + A; yy = g['y0'] + np.arange(g['ny'])
    ax.plot(yy, np.nanmax(H, axis=1), color='tab:orange', lw=1.5, label='model reef top, default version (max over x)')
    ax.errorbar([402, 411, 474, 514], [-7.76, -8.76, -9.76, -10.76], xerr=20, yerr=1, fmt='s', color='tab:green', label='Navionics labels 7-10 (LAT assumed, -0.76), +-20 m / +-1 m')
    ax.add_patch(plt.Rectangle((300, -8), 70, 2, fill=False, ec='purple', ls='--', label='Vieira 2021: under reef -6 to -8')); ax.add_patch(plt.Rectangle((440, -10), 80, 1, fill=False, ec='m', ls=':', label='Vieira 2021: seaward -9/-10'))
    ax.add_patch(plt.Rectangle((225, -5), 40, 1, fill=False, ec='brown', ls='--', label='Vieira 2021: inner edge -4/-5'))
    for lab, z in (('LAT', -0.76), ('MSL', 0.12), ('HAT', 1.27)):
        ax.axhline(z, color='gray', ls=':', lw=.8); ax.text(545, z + .05, lab, fontsize=7, ha='right')
    ax.axhline(-2.2, color='tab:orange', ls='--', lw=.8); ax.text(545, -2.15, 'measured crest -2.2 AHD', fontsize=7, ha='right', color='tab:orange')
    ax.set_xlabel('y offshore of the 2020-08-08 waterline (m)'); ax.set_ylabel('m AHD'); ax.set_xlim(-40, 550); ax.set_ylim(-11.5, 2)
    ax.set_title('Narrowneck: model seabed and reef top vs the sources, along the shore-normal (tide planes in AHD, MSQ)', fontsize=10); ax.legend(fontsize=6.5, loc='lower left', ncol=2)
    fig.tight_layout(); fig.savefig(os.path.join(ANN, 'A5_profile_model_vs_sources.png'), dpi=110); plt.close(fig)


def a6():
    sy = np.arange(-40, 521, 5.0); sx = np.arange(-250, 251, 5.0); SB = np.array(M['seabed']['z']) + A
    fig, ax = plt.subplots(figsize=(9, 8))
    im = ax.imshow(SB, extent=(sx[0] - 2.5, sx[-1] + 2.5, sy[-1] + 2.5, sy[0] - 2.5), cmap='YlGnBu_r', vmin=-11, vmax=0, aspect='equal')
    cols = {'photo_2020-08-08': 'gold', 'design_option2_2017': 'tab:red', 'design_2004_revised': 'tab:cyan', 'survey_2011-06-09': 'tab:purple', 'navionics_4.0m_shoals': 'lime'}
    for vid, v in V.items():
        for i, p in enumerate(v['outline_m']):
            q = np.array(p); ax.plot(q[:, 0], q[:, 1], color=cols[vid], lw=1.6 if vid.startswith('photo') else 1, label=(v['name'].split(' (')[0][:58] + ' (%s)' % v['date']) if i == 0 else None)
    for p in M['faint_patches_m']:
        q = np.array(p); ax.plot(q[:, 0], q[:, 1], color='magenta', lw=.6)
    ax.plot([-90, 85, 85, -90, -90], [190, 190, 390, 390, 190], 'w--', lw=.8, label='multibeam window (Fig 3)')
    ax.set_xlim(-130, 130); ax.set_ylim(420, 170); ax.set_xlabel('x alongshore (m, + north)'); ax.set_ylabel('y offshore (m, + east)')
    ax.set_title('The five outline versions on the model seabed (m AHD); pink = 24 faint patches', fontsize=10); ax.legend(fontsize=6.5, loc='upper right'); plt.colorbar(im, ax=ax, shrink=.6, label='model seabed, m AHD')
    fig.tight_layout(); fig.savefig(os.path.join(ANN, 'A6_versions_on_seabed.png'), dpi=110); plt.close(fig)


if __name__ == '__main__':
    a1(); a2(); a3(); a4(); a5(); a6(); print('annotated done', sorted(os.listdir(ANN)))
