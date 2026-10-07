"""Annotated copies of Rendle & Davidson (2012) Fig. 9 showing exactly what was read (private research copies).
 -> annotated/fig9_depth_read_map.png   (colour bar ticks, axis anchors, read area, contours, sample soundings, reef outline)
 -> annotated/fig9_profiles_read.png    (lower profile panels: crest / trough / toe levels and flank slopes read)
"""
import sys, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import survey_read2 as sr
from canon import CAN_POLY, can2osgb

OUT = HERE.parent / "annotated"; OUT.mkdir(exist_ok=True)
SRC = sr.SRC
FONT = lambda s: ImageFont.truetype("arial.ttf", s)
FB = lambda s: ImageFont.truetype("arialbd.ttf", s)


def label(d, xy, text, font, fg=(0, 0, 0), bg=(255, 255, 255), pad=2, anchor="la"):
    x, y = xy
    l, t, r, b = d.textbbox((x, y), text, font=font, anchor=anchor)
    d.rectangle([l - pad, t - pad, r + pad, b + pad], fill=bg)
    d.text((x, y), text, font=font, fill=fg, anchor=anchor)


def dashed_line(d, p0, p1, fill, width=1, dash=8, gap=5):
    x0, y0 = p0; x1, y1 = p1
    L = math.hypot(x1 - x0, y1 - y0)
    if L == 0:
        return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    t = 0.0
    while t < L:
        e = min(t + dash, L)
        d.line([(x0 + ux * t, y0 + uy * t), (x0 + ux * e, y0 + uy * e)], fill=fill, width=width)
        t += dash + gap


def map_figure():
    S = 2.0                                              # upscale factor
    im = Image.open(SRC).convert("RGB")
    crop = (0, 0, 998, 290)
    im = im.crop(crop).resize((int(998 * S), int(290 * S)), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    P = lambda x, y: (x * S, y * S)
    f9, f11, f13 = FONT(int(8 * S)), FONT(int(10 * S)), FB(int(11 * S))

    # --- colour bar
    d.rectangle([P(934, 19), P(946, 257)], outline=(255, 255, 255), width=3)
    d.rectangle([P(934, 19), P(946, 257)], outline=(0, 0, 0), width=1)
    for ty, tv in zip(sr.TICK_Y, sr.TICK_V):
        d.line([P(926, ty), P(950, ty)], fill=(0, 0, 0), width=2)
        label(d, P(953, ty), f"{tv:+.0f} m" if tv else "0 m", f11, anchor="lm", bg=(255, 255, 200))
    label(d, P(953, 20), f"top {sr.bar_value(20):+.2f} m", f9, anchor="lm", bg=(255, 255, 200))
    label(d, P(953, 255), f"bottom {sr.bar_value(255):.2f} m", f9, anchor="lm", bg=(255, 255, 200))
    # --- axis anchors of the left map
    for E, x in ((411400, sr.X_E0), (411550, 433.5)):
        dashed_line(d, P(x, 20), P(x, 255), (0, 0, 0), 2)
        label(d, P(x, 16), f"E {E}  (x={x:.1f}px)", f9, anchor="ms", bg=(255, 255, 160))
    for N, y in ((91000, sr.Y_N0), (90820, 235.3)):
        dashed_line(d, P(73, y), P(478, y), (0, 0, 0), 2)
        label(d, P(76, y - 1), f"N {N}  (y={y:.1f}px)", f9, anchor="lb", bg=(255, 255, 160))
    label(d, P(478, 22), "scale 1.908 px/m (E), 1.0909 px/m (N)", f9, anchor="ra", bg=(255, 255, 160))

    # --- read area
    dashed_line(d, P(73, 20), P(478, 20), (255, 255, 255), 2); dashed_line(d, P(478, 20), P(478, 255), (255, 255, 255), 2)
    dashed_line(d, P(478, 255), P(73, 255), (255, 255, 255), 2); dashed_line(d, P(73, 255), P(73, 20), (255, 255, 255), 2)
    label(d, P(75, 255), "area read (x 73-478, y 20-255 px)", f9, anchor="lb", bg=(255, 255, 255))

    # --- depth contours of the colour read
    val, dist, still, take = sr.depth_image()
    v = np.where(np.isfinite(val), val, np.nan)
    vf = ndi.gaussian_filter(np.nan_to_num(v, nan=-5.3), 1.2)
    import contourpy
    gen = contourpy.contour_generator(np.arange(vf.shape[1]), np.arange(vf.shape[0]), np.where(np.isfinite(v), vf, -9))
    cols = {0.0: (255, 255, 255), -1.0: (0, 0, 0), -2.0: (0, 0, 0), -3.0: (0, 0, 0), -4.0: (255, 255, 255)}
    for lev, col in cols.items():
        for ln in gen.lines(lev):
            if len(ln) < 20:
                continue
            pts = [P(x, y) for x, y in ln]
            d.line(pts, fill=col, width=1)
            k = len(ln) // 2
            label(d, P(*ln[k]), f"{lev:+.0f}" if lev else "0", f9, bg=(255, 255, 0), pad=1, anchor="mm")

    # --- reef outline (shape.json canonical -> OSGB -> figure px)
    E, N = can2osgb(CAN_POLY[:, 0], CAN_POLY[:, 1])
    px, py = sr.osgb2px(E, N)
    pts = [P(a, b) for a, b in zip(px, py)]
    d.line(pts + [pts[0]], fill=(255, 0, 255), width=3)
    label(d, (pts[0][0] + 8, pts[0][1] - 40), "reef outline (shape.json, from the 2011-09-28 satellite image)", f9, fg=(255, 255, 255), bg=(160, 0, 160), anchor="la")

    # --- sample soundings
    sites = [("A crest max", 20, 193), ("B seabed shoreward", 0, 125), ("C seabed offshore", 0, 292),
             ("D seabed W", -80, 235), ("E seabed E", 65, 215), ("F under 25 m NW flank", -20, 248)]
    vs = ndi.gaussian_filter(np.nan_to_num(v, nan=-9), 1.5)
    for name, cx, cy in sites:
        e, n = can2osgb(cx, cy)
        x, y = sr.osgb2px(e, n)
        x = float(np.ravel(x)[0]); y = float(np.ravel(y)[0])
        z = float(vs[int(round(y)), int(round(x))])
        d.ellipse([P(x - 3, y - 3), P(x + 3, y + 3)], outline=(0, 0, 0), fill=(255, 255, 255), width=2)
        label(d, P(x + 5, y), f"{name[0]}: {z:+.2f} m", f11, anchor="lm", bg=(255, 255, 255))
        print("sounding", name, "canonical (%g,%g)" % (cx, cy), "px (%.0f,%.0f)" % (x, y), "z=%.2f" % z)

    # --- cross-section lines (used in section_profiles.png): shore normal through reef centre, and the reef axis
    for (c0, c1, nm) in (((0, 100), (0, 305), "S1 shore normal x=0"),):
        pp = []
        for cx, cy in (c0, c1):
            e, n = can2osgb(cx, cy); x, y = sr.osgb2px(e, n); pp.append(P(float(np.ravel(x)[0]), float(np.ravel(y)[0])))
        d.line(pp, fill=(0, 255, 255), width=3)
        label(d, (pp[1][0] + 6, pp[1][1] - 4), nm, f9, anchor="lm", bg=(0, 200, 200))

    # --- title strip
    strip = Image.new("RGB", (im.width, 46), (30, 30, 30)); sd = ImageDraw.Draw(strip)
    sd.text((8, 4), "ANNOTATED COPY of Rendle & Davidson (2012) ICCE, Fig. 9 (left map), April 2011 DGPS bathymetry, Channel Coastal Observatory / Bournemouth BC. Private research copy.", font=FONT(15), fill=(255, 255, 255))
    sd.text((8, 24), "Marked: colour-bar ticks, OSGB gridline anchors, read area, depth contours of the colour read (0,-1,-2,-3,-4 m), reef outline, sample soundings A-F, section S1. Datum assumed Chart Datum.", font=FONT(15), fill=(255, 255, 160))
    foot = Image.new("RGB", (im.width, 50), (30, 30, 30)); fd = ImageDraw.Draw(foot)
    fd.text((8, 4), "Colour bar (right): tick rows y = 55, 93, 131, 168, 206, 244 px read as 0 .. -5 m, linear fit %.4f m/px (top +0.93 m, bottom -5.30 m); every map pixel -> nearest bar colour (RGB distance)." % sr._slope, font=FONT(15), fill=(255, 255, 255))
    fd.text((8, 26), "Gridlines E 411400 / 411550 and N 91000 / 90820 anchor the OSGB36 axes (1.908 px/m E, 1.0909 px/m N). Contours and soundings A-F are computed from the read, not printed in the paper.", font=FONT(15), fill=(255, 255, 160))
    out = Image.new("RGB", (im.width, im.height + 46 + 50)); out.paste(strip, (0, 0)); out.paste(im, (0, 46)); out.paste(foot, (0, 46 + im.height))
    out.save(OUT / "fig9_depth_read_map.png", optimize=True)
    return out.size


def circled(d, xy, n, font, col=(0, 0, 0), fill=(255, 255, 255), r=13):
    x, y = xy
    d.ellipse([x - r, y - r, x + r, y + r], fill=fill, outline=col, width=3)
    d.text((x, y), str(n), font=font, fill=col, anchor="mm")


def profile_figure():
    S = 3.0
    raw = Image.open(SRC).convert("RGB")
    y0 = 285
    def y_left(v): return y0 + (220 - 160.0 * v) / 3.0          # native px for value v (left profile panel)
    def y_right(v): return y0 + (62 + 118.8 * (1 - v)) / 3.0     # right profile panel
    fnum, fkey = FB(int(8 * S)), FONT(int(8.5 * S))
    GREEN, BLUE, RED, MAG, ORG = (0, 130, 0), (0, 0, 220), (220, 0, 0), (170, 0, 170), (255, 120, 0)
    panels = []
    for side, (x0, x1), yf, (xl, xr) in (("left", (0, 500), y_left, (105, 475)), ("right", (500, 998), y_right, (545, 950))):
        c = raw.crop((x0, y0, x1, 580)).resize((int((x1 - x0) * S), int((580 - y0) * S)), Image.LANCZOS)
        d = ImageDraw.Draw(c)
        Pp = lambda x, y: ((x - x0) * S, (y - y0) * S)
        def hline(v, n, col):
            y = yf(v)
            dashed_line(d, Pp(xl, y), Pp(xr, y), col, 3)
            circled(d, Pp(xr + 12, y), n, fnum, col)
        def mark(x, v, n, col, dx=0, dy=-16):
            px, py = Pp(x, yf(v))
            d.ellipse([px - 7, py - 7, px + 7, py + 7], outline=col, width=3)
            circled(d, (px + dx * S, py + dy * S), n, fnum, col)
        if side == "left":
            key = ["1  design crest +0.5 m ACD (Mead et al. 2010, p.2) - dashed green line",
                   "2  Oct 2009 (dark blue) crest tops +0.05 .. +0.45 m; circle = highest, +0.45 m",
                   "3  Apr 2011 (red) dip to -1.95 m = the lost 70 m container ('depression in crest height of 2 m')",
                   "4  seabed W of the reef -3.0 m (Oct 2009) .. -3.3 m (Apr 2011, scour ~0.25 m)",
                   "5  SW flank (orange): 2.0 m rise (-2.7 -> -0.7 m) over 6-8 m = 1:3 .. 1:4; steepest 2 m window 1:1.5 (x scale from the 62 m section line on the map)"]
            hline(0.5, 1, GREEN); hline(-3.0, 4, MAG)
            mark(302, 0.45, 2, BLUE, dx=0, dy=-12)
            mark(270, -1.95, 3, RED, dx=-12, dy=0)
            p0 = Pp(190, yf(-2.95)); p1 = Pp(206, yf(-0.45)); d.line([p0, p1], fill=ORG, width=4); circled(d, (p0[0] - 18, (p0[1] + p1[1]) / 2), 5, fnum, ORG)
        else:
            key = ["1  design crest +0.5 m ACD (Mead et al. 2010, p.2) - dashed green line",
                   "2  Oct 2009 (dark blue) crest +0.1 .. +0.65 m along the axis; circle = highest +0.65 m",
                   "3  Apr 2011 (red) along-axis trough -1.1 .. -2.2 m over about half the section (damaged 70 m container)",
                   "4  NE end (orange): drops 3.85 m (+0.6 -> -3.25 m) - horizontal scale of this panel not usable (axis labels inconsistent)",
                   "5  toe at the NE end -3.2 .. -3.9 m (dashed magenta at -3.2 m)"]
            hline(0.5, 1, GREEN); hline(-3.2, 5, MAG)
            mark(837, 0.64, 2, BLUE, dx=0, dy=-12)
            d.rectangle([Pp(693, yf(-1.0)), Pp(842, yf(-2.3))], outline=RED, width=4); circled(d, Pp(767, yf(-2.3) + 14), 3, fnum, RED)
            p0 = Pp(836, yf(0.6)); p1 = Pp(868, yf(-3.25)); d.line([p0, p1], fill=ORG, width=4); circled(d, (p1[0] - 22, (p0[1] + p1[1]) / 2), 4, fnum, ORG)
        kb = Image.new("RGB", (c.width, 175), (255, 255, 255)); kd = ImageDraw.Draw(kb)
        for i, line in enumerate(key):
            kd.text((10, 8 + i * 32), line, font=fkey, fill=(0, 0, 0))
        panel = Image.new("RGB", (c.width, c.height + 175)); panel.paste(c, (0, 0)); panel.paste(kb, (0, c.height))
        panels.append(panel)
    W = panels[0].width + panels[1].width + 8
    out = Image.new("RGB", (W, panels[0].height + 56), (30, 30, 30)); sd = ImageDraw.Draw(out)
    sd.text((8, 4), "ANNOTATED COPY of Rendle & Davidson (2012) ICCE, Fig. 9 lower panels: bathymetry cross-sections from four Channel Coastal Observatory surveys. Private research copy.", font=FONT(17), fill=(255, 255, 255))
    sd.text((8, 28), "Levels read from the printed Depth (m) axes (vertical ticks calibrated per panel: 53.3 px/m left, 39.6 px/m right in the native figure; left horizontal scale 5.84 px/m from the 62.2 m section line). Left: section across the reef. Right: section along the reef axis.", font=FONT(17), fill=(255, 255, 160))
    out.paste(panels[0], (0, 56)); out.paste(panels[1], (panels[0].width + 8, 56))
    out.save(OUT / "fig9_profiles_read.png", optimize=True)
    return out.size


if __name__ == "__main__":
    print(map_figure()); print(profile_figure())
