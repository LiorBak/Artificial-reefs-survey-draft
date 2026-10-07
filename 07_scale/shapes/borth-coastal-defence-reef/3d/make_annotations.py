"""make_annotations.py - annotated copies of the source images used for the Borth 3D model (3d/annotated/).

Run from this folder:  python make_annotations.py [fig2] [drg1020] [drg1021] [drg1022] [drg1023] [lidar] [seabed]   (no argument = all)
Every picture marks exactly what was read off the source (see SOURCES_3D.md "Annotated images" for the captions).
Positions of the callouts on the drawings 1021-1023 are pixel positions read by eye on a 1400 px wide view of the 3643 px PNG
(factor K = 3643/1400); the drawings' text is vector outlines, not a text layer, so it cannot be searched.
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import b3d_lib as L
import b3d_reef as R

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'annotated')
SRC = os.path.join(HERE, 'src')
PROJ = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
SHP = L.BASE
FIG2 = os.path.join(PROJ, '03_images', 'reefs', 'borth-coastal-defence-reef', 'borth-coastal-defence-reef_hrpp576-fig2-layout-contours_2013.png')
DRG = {k: os.path.join(SHP, 'src', 'borth_rh-drg-9V5090-%s.png' % v) for k, v in {
    '1020': '1020_multipurpose-reef-plan_2010', '1021': '1021_northern-reef-sections-1_2010',
    '1022': '1022_northern-reef-sections-2_2010', '1023': '1023_southern-reef-sections_2010'}.items()}
K = 3643 / 1400.0


def font(sz, bold=False):
    for n in (('arialbd.ttf' if bold else 'arial.ttf'), 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def tag(d, xy, text, fill=(255, 255, 255, 235), ink=(0, 0, 0), sz=22, bold=False, anchor='la', border=None):
    f = font(sz, bold)
    bb = d.textbbox(xy, text, font=f, anchor=anchor)
    d.rectangle((bb[0] - 3, bb[1] - 2, bb[2] + 3, bb[3] + 2), fill=fill, outline=border)
    d.text(xy, text, font=f, fill=ink, anchor=anchor)


def wrap(lines, f, width):
    out = []
    for t in lines:
        words, cur = t.split(' '), ''
        for w in words:
            tt = (cur + ' ' + w).strip()
            if f.getlength(tt) > width and cur:
                out.append(cur); cur = w
            else:
                cur = tt
        out.append(cur)
    return out


def with_caption(im, lines, sz=22, pad=10):
    f = font(sz)
    lines = wrap(lines, f, im.width - 2 * pad)
    h = len(lines) * (sz + 6) + 2 * pad
    out = Image.new('RGB', (im.width, im.height + h), (255, 255, 255))
    out.paste(im.convert('RGB'), (0, 0)); d = ImageDraw.Draw(out)
    for i, t in enumerate(lines):
        d.text((pad, im.height + pad + i * (sz + 6)), t, font=f, fill=(0, 0, 0))
    return out


def save(im, name):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name); im.save(p, optimize=True); print('wrote', name, im.size, os.path.getsize(p) // 1024, 'kB')


# ------------------------------------------------------------------------------------------------ Fig 2 (HRPP576)
def fig2():
    c = json.load(open(os.path.join(SRC, 'fig2_contours_canonical.json')))
    cal = c['calibration']; s = cal['m_per_px']; pcx, pcy = cal['oval_centre_px']; cx, cy = cal['oval_centroid_canonical_m']
    S = 2
    im = Image.open(FIG2).convert('RGB'); im = im.resize((im.width * S, im.height * S), Image.LANCZOS)
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    col = {'-2': (220, 40, 40, 255), '-3': (20, 110, 230, 255), '-4': (20, 150, 60, 255)}
    for k, pts in c['contours_mODN'].items():
        P = [((pcx + (x - cx) / s) * S, (pcy + (y - cy) / s) * S) for x, y in pts]
        d.line(P, fill=col[k], width=3)
    # label boxes (printed contour labels on the left), pixel rows read by eye
    for lab, row in (('+0.0', 62), ('-1.0', 97), ('-2.0', 135), ('-3.0', 178), ('-4.0', 236), ('-5.0', 325)):
        d.rectangle((6 * S, (row - 9) * S, 96 * S, (row + 9) * S), outline=(255, 140, 0, 255), width=3)
    # column-330 tracking: where the grey contour lines cross the column used for the first reading
    xcol = 330 * S
    d.line((xcol, 100, xcol, 330 * S), fill=(120, 120, 120, 170), width=1)
    for k, row in (('-2.0', 139.0), ('-3.0', 191.0), ('-4.0', 262.5)):
        y = row * S; d.ellipse((xcol - 8, y - 8, xcol + 8, y + 8), outline=(0, 0, 0, 255), width=3)
        tag(d, (xcol + 14, y - 12), 'column 330: %s mODN at row %.1f' % (k, row), sz=20)
    # georeferencing: oval C centre and the 500 m bar
    ox, oy = pcx * S, pcy * S
    d.line((ox - 18, oy, ox + 18, oy), fill=(200, 0, 200, 255), width=3); d.line((ox, oy - 18, ox, oy + 18), fill=(200, 0, 200, 255), width=3)
    tag(d, (ox + 24, oy + 14), 'oval C centre = canonical (+85.3, +325.7) m', sz=20, border=(200, 0, 200))
    # the 500 m bar: dark horizontal run near the bottom (rows 322-334)
    a = np.asarray(Image.open(FIG2).convert('L')).astype(int); band = a[329:331, :]          # bar = rows 329-330, columns 153..434 (checked)
    cols = np.where((band < 100).sum(axis=0) >= 2)[0]; cols = cols[cols < 480]
    if len(cols):
        b0, b1 = int(cols.min()), int(cols.max())
        d.line((b0 * S, 316 * S, b1 * S, 316 * S), fill=(0, 160, 160, 255), width=4)
        for xx in (b0, b1):
            d.line((xx * S, 310 * S, xx * S, 322 * S), fill=(0, 160, 160, 255), width=4)
        tag(d, (((b0 + b1) // 2) * S, 300 * S), 'bar read: %d px = 500 m -> %.3f m/px' % (b1 - b0, 500.0 / (b1 - b0)), sz=20, anchor='ma', border=(0, 160, 160))
    # reef zone of the model (x -100..150 m, y 265..405 m)
    pa = ((pcx + (-100 - cx) / s) * S, (pcy + (265 - cy) / s) * S); pb = ((pcx + (150 - cx) / s) * S, (pcy + (405 - cy) / s) * S)
    x0, y0, x1, y1 = pa[0], pa[1], pb[0], pb[1]
    d.rectangle((x0, y0, x1, y1), outline=(255, 0, 120, 255), width=2)
    tag(d, (x0, y0 - 24), 'zone of the two mounds in the model (x -100..+150, y 265..405 m)', sz=18, border=(255, 0, 120))
    out = Image.alpha_composite(im.convert('RGBA'), ov)
    out = with_caption(out, ['HRPP576 (Wallingford/Cardiff 2013) Fig 2, 849 x 349 px shown at x2. Up = landward, right = south, left labels are mODN (Ordnance Datum Newlyn).',
                             'Red / blue / green lines = the -2 / -3 / -4 mODN contours as traced by eye (98 / 94 / 51 points, canonical frame, +-10 m). Orange boxes = printed contour labels read.',
                             'Black rings = the column-330 read-out (-2.0 at row 139, -3.0 at row 191, -4.0 at row 262.5). Scale: 500 m bar and oval C (the only structure in the figure that is built) give 1.776 m/px.',
                             'Used: -3.0 contour (y about 287 m offshore at the reef) as seabed control outside the reef zone; -2 and -4 for checking only. Private research copy.'], sz=20)
    save(out, 'A1_fig2_contours_read.png')


# ------------------------------------------------------------------------------------------------ drawing 1020 (plan)
def bng2png(en):
    f = json.load(open(os.path.join(SRC, 'design1020_pdf_to_bng_fit.json')))
    Rm = np.array(f['R']); sm = np.array(f['sm_bng']); dm = np.array(f['dm_pdf']); s = f['scale_pt_per_m']
    en = np.asarray(en, float)
    pdf = s * (en - sm) @ Rm.T + dm
    return pdf * (3643 / 2384.0)


def drg1020():
    F = L.Frame(json.load(open(os.path.join(SHP, 'shape.json'), encoding='utf-8')))
    im = Image.open(DRG['1020']).convert('RGB')
    rings = json.load(open(os.path.join(SRC, 'design1020_rings_bng.json')))
    cp = json.load(open(os.path.join(SRC, 'design1020_crest_paths_bng.json')))['paths']
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    cols = [(160, 160, 160), (120, 200, 120), (60, 170, 230), (30, 90, 230), (230, 30, 30)]
    allp = []
    for k in 'NS':
        for i, r in enumerate(rings[k]):
            P = bng2png(r); allp.append(P)
            d.line([tuple(p) for p in P] + [tuple(P[0])], fill=cols[i] + (255,), width=4)
    for pid, v in cp.items():
        P = bng2png(v['bng']); allp.append(P); d.line([tuple(p) for p in P], fill=(255, 140, 0, 255), width=6)
    dp = R.design_polys(F)
    for name, xy in dp['sop'].items():
        en = F.can2bng(np.array([xy]))[0]; p = bng2png([en])[0]
        d.ellipse((p[0] - 9, p[1] - 9, p[0] + 9, p[1] + 9), fill=(255, 0, 255, 255))
        tag(d, (p[0] + 12, p[1] - 12), name, sz=26, bold=True, fill=(255, 255, 255, 220))
    A = np.vstack(allp); x0, y0 = A.min(0) - 120; x1, y1 = A.max(0) + 120
    out = Image.alpha_composite(im.convert('RGBA'), ov).crop((int(x0), int(y0), int(x1), int(y1)))
    d2 = ImageDraw.Draw(out)
    lx, ly = 30, 30
    for i, t in enumerate(['ring 0  apron outer edge (seabed)', 'ring 1  blanket (Type 6) top edge', 'ring 2  apron / berm foot', 'ring 3  toe-berm (Type 0) top outer edge', 'ring 4  FOOT OF THE TYPE 4 ARMOUR = design outline (-2.15 mODN)']):
        d2.rectangle((lx, ly + i * 36, lx + 30, ly + i * 36 + 24), fill=cols[i]); tag(d2, (lx + 40, ly + i * 36 - 2), t, sz=24)
    d2.rectangle((lx, ly + 180, lx + 30, ly + 204), fill=(255, 140, 0)); tag(d2, (lx + 40, ly + 178), 'crest outline paths read from the vector PDF (R1-R6, R2-R3-R4-R5)', sz=24)
    d2.ellipse((lx + 3, ly + 218, lx + 27, ly + 242), fill=(255, 0, 255)); tag(d2, (lx + 40, ly + 214), 'setting-out points (SOP) R1-R15 from the drawing table', sz=24)
    out = with_caption(out, ['Royal Haskoning drawing 9V5090/1020 rev C1 (Jan 2011), plan of both reefs; crop of the 3643 px render, plan drawn with north to the RIGHT. Overlay = the vector geometry of the PDF re-projected with the fitted PDF<->OS-grid transform (max residual 0.12 pt = 0.02 m).',
                            'Crest levels read on the drawing: arm +0.50 mODN (9 m strip), tail +1.00 (strip R2/R5-R3/R4, 26.6 m), head lens +0.00 rising over "TRANSITION APPROX. 40 m", oval +1.50 (6 m flat top, R14-R15). Ring 4 = the "design rock-layer foot" outline (6,989 m2).',
                            'Private research copy of a public Ceredigion CC / Haskoning drawing; reuse rights to be checked.'], sz=26)
    save(out, 'A2_drg1020_rings_and_sop_read.png')


# ------------------------------------------------------------------------------------------------ drawings 1021-1023 (sections)
def callouts(key, items, title_lines, name):
    """items: (x, y, label, kind) in 1400-px view coordinates; kind 'v' = value read, 'd' = dimension / slope, 'w' = water level"""
    im = Image.open(DRG[key]).convert('RGB')
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    colk = {'v': (230, 30, 30), 'd': (30, 90, 230), 'w': (0, 150, 90), 's': (160, 0, 200)}
    for i, (x, y, lab, kind) in enumerate(items, 1):
        X, Y = x * K, y * K; c = colk[kind]
        d.ellipse((X - 48, Y - 22, X + 48, Y + 22), outline=c + (255,), width=6)
        tag(d, (X, Y - 30), '%d' % i, sz=34, bold=True, fill=c + (255,), ink=(255, 255, 255), anchor='ms')
    out = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')
    cap = list(title_lines) + [''] + ['%d  %s' % (i, lab) for i, (_, _, lab, _) in enumerate(items, 1)]
    out = with_caption(out, cap, sz=30, pad=14)
    # shrink the huge page a little to keep the file reasonable
    out = out.resize((out.width * 3 // 4, out.height * 3 // 4), Image.LANCZOS)
    save(out, name)


def drg1021():
    items = [
        (403, 133, '+0.00 mODN = top of the rock at SOP R1 (head edge)', 'v'),
        (405, 156, '-2.70 = underside of the Type 4 layer at the head (+0.00 - 2.70)', 'v'),
        (1043, 129, '+0.50 mODN = arm crest (N1-N1 first section, 40 m from R1)', 'v'),
        (1043, 152, '-2.20 = underside of Type 4 at the arm (+0.50 - 2.70); Type 5 + Type 6 below it', 'v'),
        (590, 123, '"TRANSITION APPROX. 40m": head lens rises from +0.00 to +0.50', 'd'),
        (222, 112, 'MHWS +2.56 mODN (printed)', 'w'), (188, 148, 'MLWS -1.74 mODN (printed)', 'w'),
        (298, 184, 'toe berm: 1350 mm high, 1:1.5 slopes, 3000 wide top; apron 2000; blanket 500', 'd'),
        (246, 349, '+0.50 mODN arm crest (N1-N1 second section)', 'v'), (246, 371, '-2.20 underside of Type 4 at the arm', 'v'),
        (598, 334, '"TRANSITION APPROX. 15m" from SOP R2 (+0.50) to SOP R3 (+1.00)', 'd'),
        (693, 345, '+1.00 mODN tail crest at SOP R3', 'v'), (693, 368, '-1.70 underside of Type 4 at the tail (+1.00 - 2.70)', 'v'),
        (771, 370, 'tail end slope 1:3 down to the toe berm (layer 2700 mm thick)', 'd'),
        (599, 772, '+0.50 mODN crest, N3-N3 cross-section', 'v'), (599, 797, '-2.20; with Type 5 1.31 + Type 6 0.5 m below: bed -4.0 mODN (derived)', 'v'),
        (210, 171, 'EXISTING SEABED VARIES (note 4: BED LEVELS VARY): flat schematic ground line, no bed level printed', 's'),
    ]
    callouts('1021', items, ['Royal Haskoning drawing 9V5090/1021 rev C1 (Jan 2011), Northern reef sections sheet 1 of 2. Red = crest / underside levels read (mODN), blue = dimensions and slopes, green = tide levels printed on the drawing.',
                             'Used: crest +0.50 / +1.00 / +0.00, ramps 40 m and 15 m, layer thickness 2.70 m, toe berm; the bed level -4.0 mODN under the arm is DERIVED (2.70 + 1.31 + 0.5 below +0.50 = -4.01), not printed. Private research copy.'],
             'A3_drg1021_sections_read.png')


def drg1022():
    items = [
        (623, 243, '+0.50 mODN crest of the developed section N4-N4 (arm between "setting out curve" and "change of direction")', 'v'),
        (563, 265, '-2.20 underside of Type 4 (2.70 m thick; Type 5 and Type 6 below)', 'v'),
        (465, 258, 'flank slope 1:4 (N4-N4); layer thickness 2700 mm measured normal to the slope', 'd'),
        (522, 209, '"SETTING OUT CURVE" / (665,209) "CHANGE OF DIRECTION": the +0.50 crest is flat between them', 'd'),
        (338, 229, 'MHWS +2.56 mODN (printed)', 'w'), (306, 263, 'MLWS -1.74 mODN (printed)', 'w'),
        (405, 297, 'toe berm (Type 0) 1350 mm high, 3000 wide top, apron 2000, blanket 500 (same as 1021)', 'd'),
        (734, 461, 'N5-N5: +0.00 mODN at SOP R1 (head edge)', 'v'), (734, 483, 'N5-N5: -2.70 underside of Type 4 at the head', 'v'),
        (498, 663, 'N6-N6: +0.00 mODN at SOP R10', 'v'), (498, 685, 'N6-N6: -2.70 underside of Type 4', 'v'),
        (540, 560, 'N5 head slope rises from the toe berm to +0.00 at R1 (about 1:5 as printed on drawing 1021 / the plan)', 'd'),
    ]
    callouts('1022', items, ['Royal Haskoning drawing 9V5090/1022 rev C1 (Jan 2011), Northern reef sections sheet 2 of 2: developed section N4-N4 (arm) and head sections N5-N5, N6-N6.',
                             'Red = levels read (mODN), blue = dimensions/slopes, green = printed tide levels. Confirms the model arm crest +0.50, head +0.00, flank 1:4, layer 2.70 m. Private research copy.'],
             'A4_drg1022_sections_read.png')


def drg1023():
    items = [
        (364, 172, 'SOP R15 (end of the oval flat top); (737,172) SOP R14', 'd'),
        (590, 184, '23000 + 23000 mm on S1-S1 = 46 m between SOP R15 and R14; the SOP table of drawing 1020 gives 38 m (unresolved; the model uses 38 m)', 'd'),
        (456, 198, '+1.50 mODN oval crest (S1-S1, flat)', 'v'),
        (456, 221, '-1.20 underside of Type 4 (+1.50 - 2.70)', 'v'),
        (456, 235, '-2.90 underside of Type 5 (-1.20 - 1.70); Type 6 0.5 m below gives the bed -3.4 mODN under the centreline (derived)', 'v'),
        (336, 206, 'end slope 1:3', 'd'),
        (150, 189, 'MHWS +2.56 mODN (printed)', 'w'), (147, 226, 'MLWS -1.74 mODN (printed)', 'w'),
        (526, 526, 'S2-S2: +1.50 mODN crest', 'v'), (536, 514, 'crest 3000 + 3000 = 6 m wide at the top (flat top 6 m)', 'd'),
        (586, 552, 'flank slope 1:3, layer 2700 mm', 'd'), (580, 570, 'Type 5 layer 1700 mm', 'd'),
        (774, 571, 'EXISTING SEABED VARIES -4.2 TO -3.6m AOD: the only printed bed levels (note on S2-S2); model uses -3.6 shoreward and -4.2 seaward', 's'),
    ]
    callouts('1023', items, ['Royal Haskoning drawing 9V5090/1023 rev C1 (Jan 2011), Southern reef (oval) sections S1-S1 and S2-S2.',
                             'Red = levels read (mODN), blue = dimensions, green = tide levels, purple = the printed bed-level range. Crest +1.50 mODN, flat top 6 m, flanks 1:3. Derived bed under the centreline (-3.4) is 0.2 m above the printed range. Private research copy.'],
             'A5_drg1023_sections_read.png')


# ------------------------------------------------------------------------------------------------ LiDAR crest check, beach, seabed zones
def _model():
    t = open(os.path.join(HERE, 'model.js'), encoding='utf-8').read()
    return json.loads(t[t.index('{'):t.rindex('}') + 1])


def lidar():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    shape = json.load(open(os.path.join(SHP, 'shape.json'), encoding='utf-8'))
    F = L.Frame(shape); dp = R.design_polys(F); M = _model()
    fl = L.lidar_sampler(F, os.path.join(SRC, 'lidar_beach_SN6089_2022-03-19.npz'), 'dsm')
    xs = np.arange(-140, 181, 1.0); ys = np.arange(190, 441, 1.0); X, Y = np.meshgrid(xs, ys); Z = fl(X, Y)
    fig = plt.figure(figsize=(15, 9.5)); gs = fig.add_gridspec(2, 2, height_ratios=[1.25, 1], hspace=0.34, wspace=0.18)
    ax = fig.add_subplot(gs[0, :])
    im = ax.imshow(Z, extent=(xs[0] - .5, xs[-1] + .5, ys[0] - .5, ys[-1] + .5), origin='lower', cmap='terrain', vmin=-2.6, vmax=2.0, interpolation='nearest')
    cs = ax.contour(X, Y, np.nan_to_num(Z, nan=-9), levels=[0.0, 0.5, 1.0, 1.5], colors=['k'], linewidths=0.6)
    ax.clabel(cs, fmt='%.1f', fontsize=7)
    for v, col, lab in zip(M['versions'], ['#d62728', '#1f77b4', '#ff7f0e'], ['LiDAR edge (default) 8,675 m2', 'design foot 6,989 m2', 'photo edge 5,743 m2']):
        for k, ring in enumerate(v['outline_m']):
            ax.plot(*np.array(ring + [ring[0]]).T, color=col, lw=1.6, label=lab if k == 0 else None)
    for key in ('crest_N', 'crest_S'):
        ax.plot(*np.array(dp[key].exterior.coords).T, color='white', lw=1.2, ls='--', label='design crest outline (1020)' if key == 'crest_N' else None)
    ax.set_aspect('equal'); ax.set_xlabel('x alongshore, + south (m)'); ax.set_ylabel('y offshore, + west (m)')
    ax.set_title('Welsh Government LiDAR DSM 1 m, flown 19 Mar 2022 (mODN), the two rock mounds; colour = surface height, sea = blank')
    st = M['validation']['stats']
    fig.text(0.5, 0.485, 'DSM inside the design crest strips:  N arm (design +0.50) median %+.2f, p90 %+.2f m;   oval (design +1.50) median %+.2f, p90 %+.2f m;   LiDAR minus design above -2.0 mODN: mean %+.2f, sd %.2f m' % (
        st['dsm_crestN_median'], st['dsm_crestN_p90'], st['dsm_crestS_median'], st['dsm_crestS_p90'], st['lidar_minus_design_mean_m'], st['lidar_minus_design_std_m']), fontsize=10, ha='center', bbox=dict(fc='w', ec='k'))
    ax.legend(loc='lower left', fontsize=8); plt.colorbar(im, ax=ax, shrink=0.7, label='mODN')
    # profile along the arm axis
    mh, axv = dp['axis']; nrm = np.array([-axv[1], axv[0]]); ss = np.arange(-25, 135, 1.0)
    mx = []; mdn = []; des = []
    for sv in ss:
        pts = np.array([mh + axv * sv + nrm * o for o in np.arange(-6, 6.1, 1.0)]); z = fl(pts[:, 0], pts[:, 1])
        mx.append(np.nanmax(z) if np.isfinite(z).any() else np.nan); mdn.append(np.nanmedian(z) if np.isfinite(z).any() else np.nan)
        c = mh + axv * sv; des.append(float(R.crest_height_N(np.array([c[0]]), np.array([c[1]]), dp)[0]))
    a2 = fig.add_subplot(gs[1, 0])
    a2.plot(ss, mx, color='#d62728', label='LiDAR DSM, max within +-6 m of the axis'); a2.plot(ss, mdn, color='#e8a0a0', label='LiDAR DSM, median within +-6 m')
    a2.plot(ss, des, color='k', ls='--', label='design crest (+0.00 -> +0.50 over 40 m, +0.50 -> +1.00 over 15 m)')
    for k in ('R1', 'R2', 'R3'):
        a2.axvline(dp['s'][k], color='grey', lw=0.6); a2.text(dp['s'][k], 1.75, 'SOP ' + k, fontsize=8, ha='center')
    a2.set_xlabel('distance along the head-tail axis from the head edge (m)'); a2.set_ylabel('mODN'); a2.set_ylim(-2.6, 2.0); a2.grid(alpha=.3); a2.legend(fontsize=7, loc='lower right')
    a2.set_title('Northern surf reef: crest profile, LiDAR vs design')
    # section across the oval
    S = dp['sop']; a_, b_ = S['R14'], S['R15']; u = (b_ - a_) / np.linalg.norm(b_ - a_); v = np.array([-u[1], u[0]]); cen = (a_ + b_) / 2
    tt = np.arange(-35, 35.1, 1.0); zz = []
    for t in tt:
        pts = np.array([cen + v * t + u * o for o in np.arange(-10, 10.1, 2.0)]); z = fl(pts[:, 0], pts[:, 1]); zz.append(np.nanmean(z) if np.isfinite(z).any() else np.nan)
    a3 = fig.add_subplot(gs[1, 1]); a3.plot(tt, zz, color='#d62728', label='LiDAR DSM, mean over 20 m along the crest (section S2-S2 position)')
    des = np.where(np.abs(tt) <= 3, 1.5, 1.5 - (np.abs(tt) - 3) / 3.0); a3.plot(tt, np.maximum(des, -2.3), 'k--', label='design: +1.50 flat top 6 m, flanks 1:3 (drawing 1023)')
    a3.axhline(-2.3, color='b', lw=0.6); a3.text(-34, -2.2, 'sea level at the flight (about -2.3 mODN)', fontsize=7, color='b')
    a3.set_xlabel('distance across the oval from its centreline (m)'); a3.set_ylabel('mODN'); a3.set_ylim(-2.6, 2.0); a3.grid(alpha=.3); a3.legend(fontsize=7, loc='upper right')
    a3.set_title('Southern breakwater (oval): cross-section, LiDAR vs design')
    fig.suptitle('Borth: LiDAR crest and shape check (source: Welsh Government LiDAR 2022-03-19, DSM; design: Royal Haskoning 9V5090/1020-1023 rev C1). Not for navigation.', fontsize=11)
    os.makedirs(OUT, exist_ok=True); fig.savefig(os.path.join(OUT, 'A6_lidar_crest_check.png'), dpi=110, bbox_inches='tight'); plt.close(fig); print('wrote A6_lidar_crest_check.png')

    # beach: LiDAR DTM contours vs Fig 2 contours
    dtm = L.lidar_sampler(F, os.path.join(SRC, 'lidar_beach_SN6089_2022-03-19.npz'), 'dtm')
    xs = np.arange(-260, 321, 2.0); ys = np.arange(0, 330, 2.0); X, Y = np.meshgrid(xs, ys); Zt = dtm(X, Y)
    f2 = json.load(open(os.path.join(SRC, 'fig2_contours_canonical.json')))['contours_mODN']
    fig, ax = plt.subplots(figsize=(14, 6.5))
    im = ax.imshow(Zt, extent=(xs[0] - 1, xs[-1] + 1, ys[0] - 1, ys[-1] + 1), origin='lower', cmap='terrain', vmin=-2.6, vmax=3.0, interpolation='nearest')
    cs = ax.contour(X, Y, np.nan_to_num(Zt, nan=-9), levels=[-2.0, -1.5, -1.0, -0.5, 0.0], colors='k', linewidths=0.6); ax.clabel(cs, fmt='%.1f', fontsize=7)
    for k, col in (('-2', 'red'), ('-3', 'blue')):
        P = np.array(f2[k]); ax.plot(P[:, 0], P[:, 1], color=col, lw=2.2, label='HRPP576 Fig 2 contour %s mODN (traced, +-10 m)' % k)
    for ring in M['versions'][0]['outline_m']:
        ax.plot(*np.array(ring + [ring[0]]).T, color='m', lw=1.2)
    ax.axhline(0, color='r', lw=0.8); ax.text(300, 4, 'defence line y = 0', fontsize=8, color='r', ha='right')
    ax.set_xlim(-260, 320); ax.set_ylim(0, 330); ax.set_aspect('equal'); ax.legend(loc='lower right', fontsize=8); plt.colorbar(im, ax=ax, shrink=0.8, label='LiDAR DTM mODN')
    ax.set_title('Beach in the 2022 LiDAR DTM (colour, black contours -2.0...0 mODN, blank = water at the flight) vs the pre-construction Fig 2 contours -2 / -3 mODN (HRPP576)')
    ax.text(-250, 14, 'Behind the mounds (x -20..+100) the 2022 beach contours lie further offshore (salient) than Fig 2 shows;\nthe model uses the measured 2022 DTM there and the Fig 2 -3.0 contour only outside the reef zone.', fontsize=9, bbox=dict(fc='w', ec='k'))
    ax.set_xlabel('x alongshore, + south (m)'); ax.set_ylabel('y offshore (m)')
    fig.savefig(os.path.join(OUT, 'A7_lidar_beach_vs_fig2.png'), dpi=110, bbox_inches='tight'); plt.close(fig); print('wrote A7_lidar_beach_vs_fig2.png')


def seabed():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    shape = json.load(open(os.path.join(SHP, 'shape.json'), encoding='utf-8'))
    F = L.Frame(shape); alt = shape['canonical']['alt_outlines_m']
    ex_union = unary_union([Polygon(alt['lidar_exposed_2022-03-19'][k]) for k in ('north', 'south')])
    dp = R.design_polys(F); mh, axv = dp['axis']; tail = mh + axv * dp['s']['R3'] * 0.5 + axv * dp['s']['R2'] * 0.5
    nodes = L.seabed_nodes(F, shape, os.path.join(SRC, 'lidar_beach_SN6089_2022-03-19.npz'), os.path.join(SRC, 'fig2_contours_canonical.json'), ex_union,
                           arm_axis=((float(tail[0]), float(tail[1])), (float(mh[0]), float(mh[1]))))
    sx, sy, Z, rbf = L.seabed_grid(nodes); M = _model()
    fig, ax = plt.subplots(figsize=(14, 10))
    im = ax.pcolormesh(sx, sy, Z, cmap='Blues_r', vmin=-7, vmax=0, shading='auto')
    cs = ax.contour(sx, sy, Z, levels=np.arange(-7, 0.1, 0.5), colors='k', linewidths=0.5); ax.clabel(cs, fmt='%.1f', fontsize=7)
    sty = {'lidar_dtm_2022': ('#2ca02c', 3, 'LiDAR DTM 19 Mar 2022 beach (y < 255, rock buffered out)'), 'fig2_-3.0': ('#d62728', 40, 'HRPP576 Fig 2 -3.0 mODN contour (outside the reef zone)'),
           'design_N3_arm': ('#ff7f0e', 40, 'design bed under the north arm -4.0 (drawing 1021 N3, derived)'), 'design_N4': ('#ff7f0e', 40, None), 'assumed_tail': ('#ffbb78', 40, 'ASSUMED bed under the tail (-3.0 ... -3.4)'),
           'design_S2_shoreward': ('#9467bd', 40, 'printed bed range under the oval -3.6 / -4.2 (drawing 1023 note)'), 'design_S2_seaward': ('#9467bd', 40, None), 'anchor_335': ('k', 40, 'ASSUMED anchor -4.0 at y = 335 outside the reef (design bed level)')}
    for k, (c, sz, lab) in sty.items():
        P = np.array([[n['x'], n['y']] for n in nodes if n['src'] == k])
        if len(P):
            ax.scatter(P[:, 0], P[:, 1], s=sz, c=c, edgecolors='w', linewidths=0.4, label=lab)
    for ring in M['versions'][0]['outline_m']:
        ax.plot(*np.array(ring + [ring[0]]).T, color='m', lw=1.5)
    ax.axhline(335, color='k', ls=':', lw=0.8); ax.text(-195, 340, 'y = 335 m: beyond this the EMODnet gradient -1.1 % is applied to the modelled level', fontsize=9)
    ax.text(-195, 10, 'LiDAR beach zone', fontsize=9); ax.text(-195, 470, 'no control data: EMODnet gradient only', fontsize=9, bbox=dict(fc='w', alpha=.7))
    ax.set_aspect('equal'); ax.set_xlim(-200, 260); ax.set_ylim(0, 520); ax.set_xlabel('x alongshore, + south (m)'); ax.set_ylabel('y offshore, + west (m)')
    ax.legend(loc='lower right', fontsize=8); plt.colorbar(im, ax=ax, shrink=0.6, label='seabed mODN (thin-plate RBF through the nodes)')
    ax.set_title('Borth seabed: where each part of the modelled seabed comes from (control nodes by source; magenta = LiDAR-edge outline of the mounds)')
    fig.savefig(os.path.join(OUT, 'A8_seabed_source_zones.png'), dpi=100, bbox_inches='tight'); plt.close(fig); print('wrote A8_seabed_source_zones.png')


if __name__ == '__main__':
    todo = sys.argv[1:] or ['fig2', 'drg1020', 'drg1021', 'drg1022', 'drg1023', 'lidar', 'seabed']
    for t in todo:
        globals()[t]()
