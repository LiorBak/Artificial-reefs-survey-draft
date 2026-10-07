"""annotate_3d.py - draw on the source images to show what was read (writes ../3d/annotated/*.png).
Needs: contours_s7.json (contours_s7.py), build_3d.py (for the model numbers), ../src images, and (optionally) the MSQ tidal-plane PDF
(path in MSQ_PDF; fetch from the URL in SOURCES_3D.md)."""
import json, os, math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import build_3d

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'src')
OUT = os.path.join(HERE, 'annotated')
os.makedirs(OUT, exist_ok=True)
MSQ_PDF = os.environ.get('MSQ_PDF', os.path.join(HERE, '..', 'src', 'msq_tidal_planes_2026.pdf'))


def font(sz, bold=False):
    for n in (('arialbd.ttf' if bold else 'arial.ttf'), 'DejaVuSans.ttf'):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def tag(d, xy, text, fill=(255, 255, 255), bg=(10, 20, 28, 215), sz=22, bold=True, anchor='la'):
    f = font(sz, bold)
    bb = d.textbbox(xy, text, font=f, anchor=anchor)
    d.rectangle((bb[0] - 4, bb[1] - 3, bb[2] + 4, bb[3] + 3), fill=bg)
    d.text(xy, text, font=f, fill=fill, anchor=anchor)


def tagml(d, xy, lines, fill=(255, 255, 255), bg=(10, 20, 28, 225), sz=20, bold=False):
    f = font(sz, bold)
    w = max(d.textlength(l, font=f) for l in lines)
    h = sz * 1.3 * len(lines)
    d.rectangle((xy[0] - 6, xy[1] - 6, xy[0] + w + 8, xy[1] + h + 4), fill=bg)
    for i, l in enumerate(lines):
        d.text((xy[0], xy[1] + i * sz * 1.3), l, font=f, fill=fill)


RANK_COL = [(255, 64, 64), (255, 150, 40), (255, 235, 59), (76, 217, 100), (64, 224, 208), (66, 133, 244), (186, 104, 255), (255, 105, 180),
            (255, 255, 255), (170, 255, 170), (255, 170, 170), (170, 170, 255), (200, 200, 100), (100, 200, 200)]


def load():
    model, val, ex = build_3d.main()
    D = json.load(open(os.path.join(HERE, 'contours_s7.json')))
    N = json.load(open(os.path.join(HERE, 'navionics_isolines.json')))
    return model, val, ex, D, N


def px_of(D, xy):
    """canonical metres -> aerial pixels (inverse of the similarity fit stored in contours_s7.json)"""
    T = D['transform']
    R = np.array(T['R']); Pm = np.array(T['Pm']); Cm = np.array(T['Cm']); s = T['scale_m_per_px']
    return Pm + ((np.asarray(xy, float) - Cm) @ R) / s


def fan_alpha_mid(c):
    """index of the point of a fan chain closest to the crest axis (alpha = 0)"""
    a0, a1 = c['alpha_deg']
    n = len(c['px'])
    return int(round((0 - a0) / (a1 - a0) * (n - 1))) if a1 > a0 else 0


def a_ranked(model, val, ex, D, N):
    im = Image.open(os.path.join(SRC, 'bluecoast_AR_aerial_Nearmaps.jpg')).convert('RGBA')
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.polygon([tuple(p) for p in D['slot_px']], fill=(255, 64, 64, 90), outline=(255, 64, 64, 255))
    tp = [tuple(p) for p in D['toe_px']]
    d.line(tp + [tp[0]], fill=(255, 213, 79, 255), width=3)
    for c in D['chains']:
        col = RANK_COL[(c['rank'] - 1) % len(RANK_COL)] + (255,)
        pts = [tuple(p) for p in c['px']]
        for a, b in zip(pts[:-1], pts[1:]):
            if math.hypot(a[0] - b[0], a[1] - b[1]) < 140:
                d.line([a, b], fill=col, width=3)
    seen = set()
    for c in D['chains']:
        if not c['part'].startswith('BE'):
            continue
        k = c['rank']
        if k in seen:
            continue
        seen.add(k)
        j = fan_alpha_mid(c)
        p = c['px'][j]
        z = model['reef']['crest_z'] - model['reef']['contour_interval_m'] * k
        tag(d, (p[0] - 4, p[1] - 30), '%.1f' % z, fill=RANK_COL[(k - 1) % len(RANK_COL)] + (255,), sz=19, anchor='la')
    for c in D['chains']:
        if c['part'] == 'A' and c['rank'] in (1, 3, 5, 7) and c['px'][0][1] < 760:
            p = c['px'][len(c['px']) // 2]
            z = model['reef']['crest_z'] - model['reef']['contour_interval_m'] * c['rank']
            tag(d, (p[0], p[1] - 26), '%.1f' % z, fill=RANK_COL[(c['rank'] - 1) % len(RANK_COL)] + (255,), sz=17, anchor='la')
    tag(d, (640, 690), 'crest slot 59 x 6 m = -1.5 m (text: crest 1.5 m below MSL)', fill=(255, 140, 140, 255), sz=20)
    tag(d, (1460, 330), 'outer line = toe outline (= council polygon)', fill=(255, 224, 130, 255), sz=20)
    for x in (26, 239, 451):
        d.line([(x, 1105), (x, 1165)], fill=(255, 0, 255, 255), width=4)
    tag(d, (26, 1075), '0 m', fill=(255, 130, 255, 255), sz=20, anchor='lb')
    tag(d, (239, 1075), '25 m  (213 px)', fill=(255, 130, 255, 255), sz=20, anchor='lb')
    tag(d, (451, 1075), '50 m  (425 px) -> 8.50 px/m', fill=(255, 130, 255, 255), sz=20, anchor='lb')
    d.rectangle((150, 880, 270, 1075), outline=(0, 255, 255, 255), width=3)
    tag(d, (150, 860), 'north arrow vertical: N up', fill=(130, 255, 255, 255), sz=18, anchor='lb')
    tagml(d, (36, 36), ['SOURCE s7: Bluecoast / Nearmap aerial (private research copy). Coloured lines = contour lines I traced (unlabelled in the source).',
                        'Numbers = elevation m vs MSL ASSUMED as -1.5 - 0.5 k  (k = lines crossed outward from the crest slot, interval 0.5 m inferred).',
                        'Lines 1-5 close all round the slot; lines 6-10 peel off the toe outline toward the seaward (E) end.',
                        'Interval check against Navionics: toe depths imply %.2f m per line (METHODS_3D.md 4.2); 1.0 m would put the E toe 5 m too deep.' % val['interval_fit']['s_nav_m']], sz=18)
    Image.alpha_composite(im, ov).convert('RGB').save(os.path.join(OUT, 's7_contours_ranked_elevations.png'))


def b_toe(model, val, ex, D, N):
    im = Image.open(os.path.join(SRC, 'bluecoast_AR_aerial_Nearmaps.jpg')).convert('RGBA')
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    PX = px_of(D, ex['toe_xy'])
    Z = np.array(ex['toe_z'])
    zmin, zmax = -7.2, -3.8

    def col(z):
        t = max(0, min(1, (z - zmin) / (zmax - zmin)))
        return (int(40 + 215 * t), int(120 + 100 * t), int(255 - 205 * t), 255)
    tp = [tuple(p) for p in D['toe_px']]
    d.line(tp + [tp[0]], fill=(255, 255, 255, 120), width=2)
    for i, (p, z) in enumerate(zip(PX, Z)):
        d.ellipse((p[0] - 5, p[1] - 5, p[0] + 5, p[1] + 5), fill=col(z), outline=(0, 0, 0, 255))
        if i % 22 == 0:
            tag(d, (p[0] + 8, p[1] - 22), '%.1f' % z, fill=(255, 255, 255, 255), sz=18)
    tagml(d, (36, 36), ['SOURCE s7. Dots = points on the toe outline (every 1 m of outline; %d dots), coloured by the elevation of the toe.' % len(Z),
                        'Elevation = -1.5 - 0.5 (K + f): K = number of traced lines inside the outline at that point, f = fractional position of the outline',
                        'between line K and the next level (distance to line K / local line spacing, <= 1).  Range %.1f to %.1f m vs MSL.' % (Z.min(), Z.max()),
                        'Independent check: Garmin Navionics natural seabed at the same dots is %.2f m shallower on average (sd %.2f m) when its depths are taken from LAT.' % (-val['toe_vs_navionics']['mean_m'], val['toe_vs_navionics']['sd_m'])], sz=18)
    for i in range(300):
        t = i / 299
        d.rectangle((1700 + i, 1250, 1701 + i, 1280), fill=col(zmin + t * (zmax - zmin)))
    tag(d, (1700, 1240), '%.1f m (deep)' % zmin, sz=18, anchor='lb')
    tag(d, (2000, 1240), '%.1f m' % zmax, sz=18, anchor='rb')
    Image.alpha_composite(im, ov).convert('RGB').save(os.path.join(OUT, 's7_toe_depth_from_contour_rank.png'))


def c_slopes(model, val, ex, D, N):
    im = Image.open(os.path.join(SRC, 'bluecoast_AR_aerial_Nearmaps.jpg')).convert('RGBA')
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for c in D['chains']:
        pts = [tuple(p) for p in c['px']]
        for a, b in zip(pts[:-1], pts[1:]):
            if math.hypot(a[0] - b[0], a[1] - b[1]) < 140:
                d.line([a, b], fill=(255, 255, 255, 150), width=2)
    mpp = D['transform']['scale_m_per_px']
    A = {}
    for c in D['chains']:
        if c['part'] == 'A':
            A.setdefault(c['rank'], []).append(np.array(c['px']))
    specs = [('N flank', 3, 4, lambda p: p[:, 1] < 760), ('S flank', 3, 4, lambda p: p[:, 1] > 840)]
    for lab, k1, k2, sel in specs:
        c1 = [p for p in A.get(k1, []) if sel(p).mean() > 0.5]
        c2 = [p for p in A.get(k2, []) if sel(p).mean() > 0.5]
        if not c1 or not c2:
            continue
        q1, q2 = c1[0], c2[0]
        p1 = q1[len(q1) // 2]
        dd = np.hypot(*(q2 - p1).T)
        p2 = q2[int(np.argmin(dd))]
        d.line([tuple(p1), tuple(p2)], fill=(255, 235, 59, 255), width=5)
        for p in (p1, p2):
            d.ellipse((p[0] - 7, p[1] - 7, p[0] + 7, p[1] + 7), fill=(255, 235, 59, 255))
        m = float(val['side_slope_spacing_m']['N flank (long side, 6 m spacing)' if lab == 'N flank' else 'S flank (short side)'][0])
        mid = (p1 + p2) / 2
        tag(d, (mid[0] + 12, mid[1] - 12), '%s: %.2f m per 0.5 m = 1:%.1f' % (lab, m, m / 0.5), fill=(255, 235, 59, 255), sz=20)
    e = val['east_axis_spacing_m']
    tag(d, (1130, 560), 'E end on the crest axis: %.1f m (3 lines, near-crest platform) then %.1f m per 0.5 m = 1:%.0f then 1:%.0f' % (e[0], float(np.median(e[3:-1])), e[0] / 0.5, float(np.median(e[3:-1])) / 0.5), fill=(255, 180, 90, 255), sz=19)
    tagml(d, (36, 36), ['SOURCE s7. Yellow bars = perpendicular spacing between neighbouring traced contour lines (pixels x %.4f m/px).' % mpp,
                        'With a 0.5 m interval the slopes are 1:12 (N flank, outer E end) and 1:5 (S flank), the design slopes printed on the concept figure',
                        '(Mortensen et al. 2015 Fig 3: 1/12, 1/5; text "gradient of 1:12"), and a 1:25 platform near the E end of the crest.',
                        'A 1.0 m interval would give 1:6 / 1:2.5 and would put the E toe 5 m deeper than the Navionics seabed: rejected.'], sz=18)
    Image.alpha_composite(im, ov).convert('RGB').save(os.path.join(OUT, 's7_side_slopes_from_line_spacing.png'))


def d_sections(model, val, ex, D, N):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from scipy.interpolate import RegularGridInterpolator
    g = ex['grid']
    xs, ys = np.array(g['xs']), np.array(g['ys'])
    zr = np.array(g['zr'])
    sb, sbn = ex['sb'], ex['sb_nav']
    cr = np.array(D['slot_canon_m'])
    cxm, cym = cr.mean(0)
    fig, axs = plt.subplots(2, 1, figsize=(12, 9.5))
    ax = axs[0]
    yy = np.arange(0, 600, 1.0)
    ax.plot(yy, build_3d.seabed_at(sb, np.full_like(yy, cxm), yy), color='#a1887f', label='seabed used in the model (hybrid) at x = %.0f m' % cxm)
    ax.plot(yy, build_3d.seabed_at(sbn, np.full_like(yy, cxm), yy), color='#6d4c41', ls='--', label='Navionics-only natural seabed (chart datum = LAT)')
    i = int(np.argmin(np.abs(xs - cxm)))
    ok = np.array(g['inside'])[:, i]
    ax.plot(ys[ok], zr[:, i][ok], color='#37474f', lw=2.5, label='reef surface (model) at x = %.0f m' % cxm)
    for k, lab, c in (('LAT', 'LAT -0.88', '#1565c0'), ('MSL', 'MSL 0', '#00838f'), ('HAT', 'HAT +1.15', '#1565c0')):
        z = [l['z'] for l in model['water']['levels'] if l['key'] == k][0]
        ax.axhline(z, color=c, ls='--', lw=1)
        ax.text(590, z + 0.1, lab, ha='right', color=c, fontsize=9)
    ax.axhline(-1.5, color='#c62828', ls=':', lw=1)
    ax.text(590, -1.4, 'crest -1.5 m MSL (text)', ha='right', color='#c62828', fontsize=9)
    ax.plot([560], [-11.4], 'rv', ms=9, label='concept design anchor (NOT used): 11.4 m at "560 m offshore" (Mortensen 2015)')
    ax.plot([534], [-13.0], 'g^', ms=9, label='GEBCO 2024 cell, 450 m wide (-13 m), at y = 534 m')
    ax.plot([0], [0], 'ks', label='waterline y = 0 (Esri 2025-12-01), taken as MSL')
    ax.set_xlabel('y, offshore distance from the waterline (m)  ->  ENE')
    ax.set_ylabel('z vs MSL (m)')
    ax.set_title('Cross-shore section through the crest centre (vertical exaggeration x 10)')
    ax.set_ylim(-14, 2)
    ax.legend(fontsize=8, loc='lower left')
    ax.grid(alpha=.3)
    ax = axs[1]
    u = np.array(D['slot_canon_m'])
    P = u - u.mean(0)
    w, v = np.linalg.eigh(P.T @ P)
    ax_dir = v[:, 1]
    if ax_dir[0] > 0:            # point toward ESE (bearing about 105 deg): negative alongshore (x, NNW) component
        ax_dir = -ax_dir
    t = np.arange(-30, 100, 1.0)
    pts = np.array([cxm, cym]) + np.outer(t, ax_dir)
    zrg = np.where(np.array(g['inside']), zr, np.nan)
    rg = RegularGridInterpolator((ys, xs), zrg, bounds_error=False, fill_value=np.nan)
    sz = rg(np.c_[pts[:, 1], pts[:, 0]])
    bed = build_3d.seabed_at(sb, pts[:, 0], pts[:, 1])
    ax.fill_between(t, bed, np.where(np.isnan(sz), bed, np.maximum(sz, bed)), color='#546e7a', alpha=.85, label='reef (model)')
    ax.plot(t, bed, color='#a1887f', label='seabed (model)')
    ax.axhline(0, color='#00838f', ls='--', lw=1)
    ax.axhline(-0.88, color='#1565c0', ls='--', lw=1)
    hd = math.degrees(math.atan2(ax_dir[0] * math.sin(math.radians(334.3)) + ax_dir[1] * math.sin(math.radians(64.3)), ax_dir[0] * math.cos(math.radians(334.3)) + ax_dir[1] * math.cos(math.radians(64.3)))) % 360
    ax.set_title('Section along the crest axis (toward bearing %.0f deg, ESE at right; WNW end at left); vertical exaggeration x 3' % hd)
    ax.set_xlabel('distance along the crest axis from the crest centre (m)')
    ax.set_ylabel('z vs MSL (m)')
    ax.legend(fontsize=8)
    ax.grid(alpha=.3)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'model_sections.png'), dpi=110)
    plt.close(fig)


def j_navionics(model, val, ex, D, N):
    """Navionics: (1) SonarChart screenshot with the reef outline and the labels read; (2) nautical-chart 'FISH HAVEN 1.5MT' screenshot;
    (3) extracted iso-lines + toe residuals + datum test."""
    sys.path.insert(0, HERE)
    import navionics_isolines as NI
    geo = NI.Geo()
    z, K = 18, 2
    toe = D['toe_canon_m']
    slot = D['slot_canon_m']
    hand = N['hand_reads']
    for chart, shade, name in (('sonar', 0.0, 'nav_sonar_z18_labels_read_with_reef_outline.png'), ('naut', 0.0, 'nav_nautical_z18_fish_haven_label.png')):
        im = Image.open(os.path.join(SRC, 'navionics', '%s_z%d_shade%04.1f.png' % (chart, z, shade))).convert('RGBA')
        im = im.resize((im.width * K, im.height * K), Image.LANCZOS)
        ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        tp = [tuple(K * np.array(geo.canon2clip(x, y, z))) for x, y in toe]
        sp_ = [tuple(K * np.array(geo.canon2clip(x, y, z))) for x, y in slot]
        d.line(tp + [tp[0]], fill=(220, 0, 0, 255), width=4)
        d.line(sp_ + [sp_[0]], fill=(200, 0, 200, 255), width=4)
        if chart == 'sonar':
            for lab, (px, py) in hand['sonar_labels_z18'].items():
                d.rectangle((K * px - 14, K * py - 14, K * px + 26, K * py + 14), outline=(0, 140, 255, 255), width=3)
            tagml(d, (20, 70), ['SOURCE: Garmin Navionics SonarChart Maps (maps.garmin.com/en-US/marine), zoom 18 (%.3f m/px), depth units = Meters,' % geo.m_per_px(18),
                                'accessed 2026-10-05 14:22 (own headless Chrome). Not for navigation; private research copy.  Datum NOT stated by the app.',
                                'Blue boxes = the contour labels I read (1 ... 11 m, labelled every 0.5 m = the interval).  Red = reef toe outline, magenta = crest slot',
                                '(shape.json canonical polygons placed by their lat/lon). The chart draws NO crest contour over the reef; it shows only the 1.5 m fish haven.'], sz=19)
        else:
            fx, fy = hand['fish_haven_label']['px_z18']
            d.rectangle((K * (fx - 40), K * (fy - 18), K * (fx + 45), K * (fy + 30)), outline=(255, 160, 0, 255), width=4)
            fh = val['fish_haven']
            tagml(d, (20, 70), ['SOURCE: Garmin Navionics Nautical Charts (maps.garmin.com/en-US/marine), zoom 18, Meters, accessed 2026-10-05 14:22. Not for navigation.',
                                'Orange box: the charted label "FISH HAVEN 1.5MT" (artificial-reef symbol, least depth 1.5 m).  Red = reef toe, magenta = crest slot.',
                                'Design crest: 1.5 m below MSL = %.2f m below LAT.  If the chart datum is LAT (A5) the chart puts the top %.2f m deeper than the design;' % (fh['crest_depth_below_LAT_m'], fh['difference_m']),
                                'the number 1.5 equals the design figure "1.5 m below MSL" - possibly copied without a datum conversion (cannot be settled from the app).'], sz=19)
        Image.alpha_composite(im, ov).convert('RGB').save(os.path.join(OUT, name))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, figsize=(17, 8.2), gridspec_kw=dict(width_ratios=[1.25, 1]))
    ax = axs[0]
    cm = plt.cm.viridis
    for v, pieces in N['sonar']['17'].items():
        for Pc in pieces:
            if len(Pc) < 100:
                continue
            P = np.array(Pc)
            ax.plot(P[:, 0], P[:, 1], '-', color=cm(float(v) / 10), lw=1.2)
            ax.text(P[len(P) // 2, 0], P[len(P) // 2, 1] - 3, '%s m' % v, fontsize=8, color=cm(float(v) / 10))
    T = np.array(D['toe_canon_m'])
    S = np.array(D['slot_canon_m'])
    ax.plot(*np.vstack([T, T[:1]]).T, 'r-', lw=1.5)
    ax.plot(*np.vstack([S, S[:1]]).T, 'm-', lw=1.5)
    res = np.array(ex['toe_z']) - np.array(ex['zb_toe'])
    sc = ax.scatter(ex['toe_xy'][:, 0], ex['toe_xy'][:, 1], c=res, cmap='coolwarm', vmin=-1.2, vmax=1.2, s=10, zorder=5)
    plt.colorbar(sc, ax=ax, shrink=.7, label='toe z (aerial contours) - Navionics seabed (LAT), m')
    ax.set_aspect('equal')
    ax.set_xlim(-300, 300)
    ax.set_ylim(520, 0)
    ax.set_xlabel('x alongshore, NNW (m)')
    ax.set_ylabel('y offshore, ENE (m)  (drawn downward)')
    ax.set_title('SonarChart iso-depth lines (1 m) and the reef; dots = toe elevation minus chart seabed', fontsize=10)
    ax.grid(alpha=.25)
    ax = axs[1]
    names = [('LAT', 0.0), ('MLWS', 0.22), ('MLWN', 0.51), ('AHD*', 0.76), ('MSL', 0.88), ('MHWS', 1.53)]
    tz, zb_ = np.array(ex['toe_z']), np.array(ex['zb_toe'])
    rms = [float(np.sqrt(np.mean((tz - (zb_ + o)) ** 2))) for _, o in names]
    ax.bar([n for n, _ in names], rms, color=['#2e7d32' if i == 0 else '#9e9e9e' for i in range(len(names))])
    for i, r_ in enumerate(rms):
        ax.text(i, r_ + 0.03, '%.2f' % r_, ha='center')
    ax.set_ylabel('RMS of (toe elevation from aerial contours - Navionics seabed), m')
    ax.set_title('Datum test: chart datum = which tidal plane? (n = %d toe points; * AHD offset unverified)' % len(tz), fontsize=10)
    ax.grid(alpha=.3, axis='y')
    plt.tight_layout()
    fig.savefig(os.path.join(OUT, 'nav_isolines_and_datum_test.png'), dpi=100)
    plt.close(fig)


def e_msq():
    import fitz
    if not os.path.exists(MSQ_PDF):
        print('MSQ pdf not found, skipping', MSQ_PDF)
        return
    doc = fitz.open(MSQ_PDF)
    p = doc[0]
    pix = p.get_pixmap(matrix=fitz.Matrix(2.2, 2.2))
    im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples).convert('RGBA')
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    s = 2.2
    words = p.get_text('words')
    hit = p.search_for('Gold Coast Seaway')[0]
    row = [w for w in words if w[1] >= hit.y0 - 4 and w[3] <= hit.y1 + 4]
    x0 = min(w[0] for w in row); x1 = max(w[2] for w in row)
    d.rectangle((x0 * s - 6, (hit.y0 - 3) * s, x1 * s + 6, (hit.y1 + 3) * s), outline=(255, 0, 0, 255), width=4, fill=(255, 0, 0, 40))
    hdr = [w for w in words if w[4] in ('MHWS', 'MHWN', 'MLWN', 'MLWS', 'MSL', 'HAT') and w[1] < hit.y0 and w[1] > 150]
    for w in hdr:
        d.rectangle((w[0] * s - 3, w[1] * s - 3, w[2] * s + 3, w[3] * s + 3), outline=(0, 120, 255, 255), width=3)
    for w in row:
        if w[4] in ('1.53', '1.24', '0.51', '0.22', '0.88', '2.03'):
            d.rectangle((w[0] * s - 3, w[1] * s - 3, w[2] * s + 3, w[3] * s + 3), outline=(0, 160, 0, 255), width=3)
    note = [w for w in words if w[4] == 'Jumpinpin']
    for w in note:
        yy = w[1]
        rowy = [q for q in words if abs(q[1] - yy) < 3]
        d.rectangle((min(q[0] for q in rowy) * s - 4, (yy - 3) * s, max(q[2] for q in rowy) * s + 4, (yy + 13) * s), outline=(255, 140, 0, 255), width=4)
        tag(d, (min(q[0] for q in rowy) * s, (yy + 18) * s), 'ocean beaches (Palm Beach): tides 20 min earlier than Gold Coast Seaway -> Seaway is the reference', fill=(255, 190, 90, 255), sz=24)
    tag(d, (40, 40), 'SOURCE MSQ Semidiurnal Tidal Planes 2026 (m above LAT 1992). Red row = Gold Coast Seaway standard port.', sz=26)
    tag(d, (40, 80), 'Green = values used: MHWS 1.53, MHWN 1.24, MLWN 0.51, MLWS 0.22, MSL 0.88, HAT 2.03. In the model z = value - 0.88 (MSL = 0).', sz=26)
    Image.alpha_composite(im, ov).convert('RGB').save(os.path.join(OUT, 'msq_tidal_planes_2026_gold_coast_seaway.png'))


def f_mortensen():
    im = Image.open(os.path.join(SRC, 'mortensen2015_fig3_concept_SCS_B.png')).convert('RGBA')
    k = 3
    im = im.resize((im.width * k, im.height * k), Image.LANCZOS)
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    boxes = [((275, 125, 310, 147), '1/2'), ((415, 125, 455, 147), '1/15'), ((270, 182, 308, 203), '1/5'), ((470, 182, 510, 203), '1/12'), ((372, 273, 410, 294), '1/12'),
             ((5, 320, 175, 392), 'values read: Volume 53,319 m3, Footprint 21,394 m2, Average Depth 8.7 m, Crest Level -1.5 m, Orientation 105 deg')]
    for (x0, y0, x1, y1), lab in boxes[:-1]:
        d.rectangle((x0 * k - 4, y0 * k - 4, x1 * k + 4, y1 * k + 4), outline=(255, 0, 0, 255), width=4)
    (x0, y0, x1, y1), lab = boxes[-1]
    d.rectangle((x0 * k, y0 * k, x1 * k, y1 * k), outline=(0, 160, 255, 255), width=4)
    tagml(d, (20, 20), ['SOURCE Mortensen et al. (2015) Fig 3 - CONCEPT design SCS B (NOT built).', 'Red boxes: side-slope labels 1/2, 1/15, 1/5, 1/12, 1/12 (design slopes).',
                        'Blue box: Crest Level -1.5 m (also in text: "crest level ... -1.5 m AHD"), orientation 105 deg.',
                        'Used only to test the contour interval of the built reef (slopes 1:12 and 1:5 reproduced).'], sz=26)
    Image.alpha_composite(im, ov).convert('RGB').save(os.path.join(OUT, 'mortensen2015_fig3_slopes_crest_read.png'))


def g_epw():
    im = Image.open(os.path.join(SRC, 'bluecoast_EPW2020_pages50-51.png')).convert('RGBA')
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    boxes = [((252, 742, 440, 800), (255, 140, 0, 255), '270 m offshore'), ((252, 800, 440, 866), (255, 0, 0, 255), 'crest: 1.5 m below average water level, 160 x 80 m'),
             ((460, 538, 640, 626), (0, 160, 255, 255), 'rock classes: core 300-1000 kg, armour 1-8 t'), ((252, 884, 440, 918), (0, 200, 0, 255), '60,000 t')]
    for (x0, y0, x1, y1), c, lab in boxes:
        d.rectangle((x0, y0, x1, y1), outline=c, width=3, fill=c[:3] + (35,))
    tag(d, (270, 724), '270 m offshore', fill=(255, 190, 90, 255), sz=14, anchor='lb')
    tag(d, (100, 835), 'crest 1.5 m below water level >', fill=(255, 120, 120, 255), sz=14, anchor='lb') if False else None
    tag(d, (445, 835), '<- crest -1.5 m', fill=(255, 120, 120, 255), sz=14, anchor='lm')
    tag(d, (645, 580), '<- core 300-1000 kg; armour 1-8 t', fill=(130, 210, 255, 255), sz=14, anchor='lm')
    tag(d, (445, 900), '<- 60,000 t', fill=(130, 255, 130, 255), sz=14, anchor='lm')
    tagml(d, (10, 12), ['SOURCE s8: Engineering for Public Works (IPWEAQ) Sept 2020 pp.50-51; boxes = text used (not depths of a survey).'], sz=15)
    Image.alpha_composite(im, ov).convert('RGB').save(os.path.join(OUT, 's8_epw2020_text_used.png'))


def h_icce():
    im = Image.open(os.path.join(SRC, 'icce13024_fig1_location_orientation.jpeg')).convert('RGBA')
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rectangle((425, 440, 665, 520), outline=(255, 140, 0, 255), width=4)
    d.rectangle((640, 395, 800, 495), outline=(255, 235, 59, 255), width=4)
    d.rectangle((1395, 30, 1430, 125), outline=(0, 255, 255, 255), width=3)
    tagml(d, (30, 20), ['SOURCE s4: ICCE 2022 Fig 1 (Hunt et al.), CC BY 4.0.', 'Orange: "Approx. 270m" arrow (255 m on the control-point scale 1.016 m/px) - only a cross-check of distance offshore.',
                        'Yellow: reef icon (traced as a cross-check of the plan; area 12,017 m2 vs 11,972 m2).', 'Cyan: north arrow (north up).',
                        'Water colour deepens seaward (left to right): qualitative support for a seabed that deepens offshore; no depth values in this figure.'], sz=20)
    Image.alpha_composite(im, ov).convert('RGB').save(os.path.join(OUT, 's4_icce_fig1_distance_and_icon.png'))


def i_fig4():
    im = Image.open(os.path.join(SRC, 'icce13024_fig4_final_survey.png')).convert('RGBA')
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.polygon([(385, 300), (410, 245), (470, 190), (580, 165), (640, 215), (600, 290), (480, 335), (420, 335)], outline=(255, 255, 255, 255), width=3)
    d.line([(470, 480), (470, 340)], fill=(255, 235, 59, 255), width=4)
    d.line([(470, 340), (470, 150)], fill=(255, 235, 59, 120), width=2)
    tagml(d, (10, 8), ['SOURCE s5: ICCE 2022 Fig 4 "Final survey of the completed reef structure" (multibeam, colour ramp WITHOUT a scale).',
                       'NOT used for any depth value. Read only qualitatively: rounded-rectangle mound on a seabed that is shallower (red/orange) toward the beach',
                       '(top, breaking waves) and deeper (yellow/green) seaward (bottom); the reef top is the shallowest (white). Consistent with the contour reading.'], sz=15)
    tag(d, (480, 470), 'seaward: deeper', fill=(255, 235, 59, 255), sz=16, anchor='lb')
    tag(d, (480, 150), 'shoreward: shallower', fill=(255, 235, 59, 255), sz=16, anchor='lb')
    Image.alpha_composite(im, ov).convert('RGB').save(os.path.join(OUT, 's5_icce_fig4_qualitative_only.png'))


if __name__ == '__main__':
    model, val, ex, D, N = load()
    a_ranked(model, val, ex, D, N)
    b_toe(model, val, ex, D, N)
    c_slopes(model, val, ex, D, N)
    d_sections(model, val, ex, D, N)
    j_navionics(model, val, ex, D, N)
    e_msq()
    f_mortensen()
    g_epw()
    h_icce()
    i_fig4()
    print('annotated images written to', OUT)
