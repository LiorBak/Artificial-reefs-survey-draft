"""Annotated copies of the Garmin Navionics screenshots -> ../annotated/navionics_*.png  (run after build_3d.py; reads ../model.js).
Marks: reef outline of shape.json, canonical 25 m grid, scale bar, north arrow, the colour fills that were measured (drying / <0.5 m / <1 m),
the survey (Rendle & Davidson Fig. 9) zones for comparison, centroid markers, and the soundings that were read."""
import json, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import canon
import navionics as nv

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "annotated"
M = json.loads((HERE.parent / "model.js").read_text(encoding="utf-8").split("=", 1)[1].strip().rstrip(";"))
NAVM = M["navionics"]
FONT = lambda sz: ImageFont.truetype("C:/Windows/Fonts/arial.ttf", sz)
FONTB = lambda sz: ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", sz)
MAG, CYAN, YEL, ORG, WHITE, BLK = (255, 0, 200), (0, 220, 255), (255, 235, 90), (255, 140, 0), (255, 255, 255), (0, 0, 0)
HDR_H, FOOT_H = 70, 96


def label(d, xy, text, font, fill=BLK, bg=(255, 255, 225), pad=3, anchor="la"):
    x, y = xy
    bb = d.textbbox((x, y), text, font=font, anchor=anchor)
    d.rectangle([bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad], fill=bg)
    d.text((x, y), text, font=font, fill=fill, anchor=anchor)


def wrap(text, font, width):
    words = text.split(); lines = []; cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.getlength(t) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def frame(img, header, footer):
    W, H = img.size
    fh, ff = FONT(15), FONT(14)
    hl = [(l, i) for i, t in enumerate(header) for l in wrap(t, fh, W - 16)]
    fl = [(l, i) for i, t in enumerate(footer) for l in wrap(t, ff, W - 16)]
    hh, fo = 8 + 19 * len(hl), 10 + 18 * len(fl)
    out = Image.new("RGB", (W, H + hh + fo), (30, 30, 30))
    out.paste(img, (0, hh))
    d = ImageDraw.Draw(out)
    for k, (t, i) in enumerate(hl):
        d.text((8, 5 + k * 19), t, font=fh, fill=(255, 255, 255) if i == 0 else (255, 235, 90))
    for k, (t, i) in enumerate(fl):
        d.text((8, hh + H + 6 + k * 18), t, font=ff, fill=(255, 255, 255) if i % 2 == 0 else (150, 255, 170))
    return out


class View:
    """screenshot crop (x0,y0,x1,y1) enlarged by k, with a canonical-metre overlay"""
    def __init__(self, kind, z, box, k):
        self.mp = nv.Mapper(z); self.box = box; self.k = k
        im = nv.Image.open(nv.SRC / nv.FILES[(kind, z)]).convert("RGB").crop(box)
        self.img = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
        self.d = ImageDraw.Draw(self.img, "RGBA")

    def px(self, X, Y):
        return ((X - self.box[0]) * self.k, (Y - self.box[1]) * self.k)

    def can(self, x, y):
        p = self.mp.can2px(x, y)
        return [self.px(a, b) for a, b in p]

    def poly(self, pts_can, fill=None, outline=MAG, width=3, close=True):
        P = self.can([p[0] for p in pts_can], [p[1] for p in pts_can])
        if close:
            P = P + [P[0]]
        self.d.line(P, fill=outline, width=width)

    def grid(self, step=25, rng=((-100, 100), (150, 300))):
        for x in range(rng[0][0], rng[0][1] + 1, step):
            P = self.can([x, x], [rng[1][0], rng[1][1]]); self.d.line(P, fill=(0, 120, 255, 70), width=1)
            label(self.d, (P[0][0], P[0][1] - 2), "x%d" % x, FONT(12), fill=(0, 60, 160), bg=(255, 255, 255, 190), pad=1, anchor="mb")
        for y in range(rng[1][0], rng[1][1] + 1, step):
            P = self.can([rng[0][0], rng[0][1]], [y, y]); self.d.line(P, fill=(0, 120, 255, 70), width=1)
            label(self.d, (P[0][0] + 2, P[0][1]), "y%d" % y, FONT(12), fill=(0, 60, 160), bg=(255, 255, 255, 190), pad=1, anchor="lm")

    def scalebar(self, L=50, at=(30, None)):
        y = self.img.height - 30 if at[1] is None else at[1]
        w = L / self.mp.mpp * self.k
        self.d.rectangle([at[0], y, at[0] + w, y + 6], fill=BLK)
        self.d.rectangle([at[0] + w / 2, y, at[0] + w, y + 6], fill=WHITE, outline=BLK)
        label(self.d, (at[0], y - 4), "%d m (ground, from the zoom level)" % L, FONT(13), anchor="lb")

    def north(self, at):
        # true north in canonical (x, y): bearing 0 -> direction (cos(0-83.4), sin(0-83.4)) in (x,y)
        ang = math.radians(-83.4); dx, dy = math.cos(ang), math.sin(ang)
        p0 = np.array(self.can([0], [200])[0]); p1 = np.array(self.can([40 * dx], [200 + 40 * dy])[0])
        v = (p1 - p0); v = v / np.linalg.norm(v) * 46
        x0, y0 = at
        self.d.line([(x0, y0 + 0), (x0 + v[0], y0 + v[1])], fill=(220, 0, 0), width=4)
        self.d.polygon([(x0 + v[0], y0 + v[1]), (x0 + v[0] * 0.78 - v[1] * 0.14, y0 + v[1] * 0.78 + v[0] * 0.14), (x0 + v[0] * 0.78 + v[1] * 0.14, y0 + v[1] * 0.78 - v[0] * 0.14)], fill=(220, 0, 0))
        label(self.d, (x0 + v[0] * 1.25, y0 + v[1] * 1.25), "N", FONTB(16), fill=(200, 0, 0), anchor="mm")


def reef_outline():
    return json.loads((canon.ROOT / "shape.json").read_text(encoding="utf-8"))["canonical"]["polygons_m"][0]


def zone_loops(level):
    for z in M["reef"]["crest_zones"]:
        if abs(z["level_acd"] - level) < 1e-6:
            return z["loops"]
    return []


def fig_sonar():
    v = View("sonar", 18, (690, 250, 1170, 640), 2.4)
    d = v.d
    v.grid(25, ((-75, 75), (150, 300)))
    v.poly(reef_outline(), outline=MAG, width=3)
    for lvl, col in ((0.0, (255, 0, 0, 255)), (-0.5, (255, 140, 0, 255)), (-1.0, (230, 200, 0, 255))):
        for lp in zone_loops(lvl):
            v.poly(lp, outline=col, width=2)
    L = NAVM["outlines_xy"]
    for key, col, w in (("sonar|drying", (0, 90, 0, 255), 3), ("sonar|depth_lt_0.5m", (0, 70, 170, 255), 3), ("sonar|depth_lt_1m", (0, 140, 255, 255), 3)):
        v.poly(L[key], outline=col, width=w)
    sh = NAVM["shapes"]
    for key, col, txt in (("sonar|drying", (0, 90, 0), "drying (green)"), ):
        c = sh[key]["centroid_xy"]; P = v.can([c[0]], [c[1]])[0]
        d.ellipse([P[0] - 6, P[1] - 6, P[0] + 6, P[1] + 6], fill=(255, 255, 255, 255), outline=(0, 90, 0), width=3)
    c0 = M["navionics"]["comparison"]["centroid_xy_drying"]["survey_zone_0m"]
    P = v.can([c0[0]], [c0[1]])[0]
    d.polygon([(P[0], P[1] - 8), (P[0] + 8, P[1]), (P[0], P[1] + 8), (P[0] - 8, P[1])], fill=(255, 0, 0, 255), outline=WHITE)
    v.scalebar(50); v.north((v.img.width - 60, 70))
    # labels of what was read (contour labels printed on the chart, positions read by eye)
    reads = [("0.5 m contour (dark/light blue edge)", (944, 392), (20, 20)), ("1 m contour (outer edge of blue)", (876, 520), (-5, 40)),
             ("1.5 m", (978, 357), (80, -5)), ("2 m", (986, 340), (80, -34)), ("3 m", (895, 566), (-140, 10)), ("4 m", (743, 586), (-20, 30))]
    for txt, (X, Y), (dx, dy) in reads:
        P = v.px(X, Y)
        d.line([P, (P[0] + dx, P[1] + dy)], fill=BLK, width=1)
        label(d, (P[0] + dx, P[1] + dy), txt, FONT(14), anchor="lm" if dx >= 0 else "rm")
    # legend
    lx, ly = 10, 10
    d.rectangle([lx, ly, lx + 345, ly + 138], fill=(255, 255, 255, 225), outline=BLK)
    leg = [(MAG, "reef outline (shape.json, 2011-09-28 image)"), ((0, 90, 0), "Navionics drying patch (green): %d m2" % sh["sonar|drying"]["area_m2"]),
           ((0, 70, 170), "Navionics depth < 0.5 m: %d m2" % sh["sonar|depth_lt_0.5m"]["area_m2"]), ((0, 140, 255), "Navionics depth < 1 m: %d m2" % sh["sonar|depth_lt_1m"]["area_m2"]),
           ((255, 0, 0), "survey (Fig. 9, Apr 2011) >0 / >-0.5 / >-1 m ACD zones:"), ((255, 140, 0), "   %d / %d / %d m2" % tuple(M["stats"]["crest_zone_area_m2"][k] for k in ("0.0", "-0.5", "-1.0")))]
    for i, (col, t) in enumerate(leg):
        d.line([(lx + 8, ly + 14 + i * 21), (lx + 38, ly + 14 + i * 21)], fill=col + (255,), width=4)
        d.text((lx + 46, ly + 14 + i * 21), t, font=FONT(13), fill=BLK, anchor="lm")
    cmp_ = NAVM["comparison"]["area_m2"]
    hdr = ["ANNOTATED COPY of Garmin Navionics SonarChart (metres, shallow shading 1 m), zoom 18 (0.378 m/px), screenshot 2026-10-05. Garmin Navionics, not for navigation; private research copy.",
           "Marked: reef outline (magenta), canonical 25 m grid (x alongshore, y offshore), the colour fills measured (green drying / dark blue <0.5 m / light blue <1 m), contour labels read, survey zones from Fig. 9 for comparison."]
    foot = ["Areas (m2) Navionics vs April 2011 survey:  drying/>0 m ACD  %d vs %d;   <0.5 m  %d vs %d;   <1 m  %d vs %d.   Centroid of drying patch (white dot) is %.0f m from the survey >0 m zone (red diamond)." % (
                cmp_["drying_above_0m_acd"]["sonarchart"], cmp_["drying_above_0m_acd"]["survey_april2011"], cmp_["shallower_than_0.5m"]["sonarchart"], cmp_["shallower_than_0.5m"]["survey_april2011"],
                cmp_["shallower_than_1m"]["sonarchart"], cmp_["shallower_than_1m"]["survey_april2011"],
                math.hypot(sh["sonar|drying"]["centroid_xy"][0] - c0[0], sh["sonar|drying"]["centroid_xy"][1] - c0[1])),
            "Reading: the structure still shows as a shoal (bags damaged but present); its crest reaches above chart datum (drying) at the shoreward-east half; the 2-4 m contours hug the SW flank (toe ~3-4 m).",
            "Datum: not stated by the viewer; assumed chart datum (agreement with the survey zones at 0.5 and 1 m supports it). Navionics survey date: unknown."]
    out = frame(v.img, hdr, foot)
    p = OUT / "navionics_sonarchart_z18_annotated.png"; out.save(p); print("saved", p)


def fig_nautical():
    v = View("nautical", 18, (690, 250, 1170, 640), 2.4)
    d = v.d
    v.grid(25, ((-75, 75), (150, 300)))
    v.poly(reef_outline(), outline=MAG, width=3)
    L = NAVM["outlines_xy"]; sh = NAVM["shapes"]
    v.poly(L["nautical|drying"], outline=(0, 90, 0, 255), width=3)
    v.poly(L["nautical|depth_lt_1m"], outline=(0, 140, 255, 255), width=3)
    for lvl, col in ((0.0, (255, 0, 0, 255)), (-1.0, (230, 200, 0, 255))):
        for lp in zone_loops(lvl):
            v.poly(lp, outline=col, width=2)
    v.scalebar(50); v.north((v.img.width - 60, 70))
    reads = [("1 m contour = edge of blue", (892, 504), (-20, 45)), ("1.6 m sounding", (976.7, 410), (60, -20)), ("2.2 m", (842.3, 402.7), (-60, -25))]
    # z18 soundings seen in this crop (printed): 1.6 at (1055,331) 2.2 at (787,318) 2.3 at (799,493) 3.3 at (1095,507) 2.3 at (558,411)->outside
    z18_read = [("1.6", 1055, 331), ("2.2", 787, 318), ("2.3", 799, 493), ("3.3", 1095, 507), ("1.4", 1175, 226), ("1.2", 626, 251), ("4.4", 559, 601)]
    for t, X, Y in z18_read:
        if v.box[0] <= X <= v.box[2] and v.box[1] <= Y <= v.box[3]:
            P = v.px(X, Y); d.ellipse([P[0] - 4, P[1] - 4, P[0] + 4, P[1] + 4], outline=(200, 0, 0), width=2)
            label(d, (P[0] + 8, P[1]), t + " m", FONTB(14), fill=(160, 0, 0), anchor="lm")
    P = v.px(892, 504); d.line([P, (P[0] - 20, P[1] + 45)], fill=BLK, width=1); label(d, (P[0] - 20, P[1] + 45), "1 m contour = outer edge of the blue", FONT(14), anchor="rm")
    lx, ly = 10, 10
    d.rectangle([lx, ly, lx + 380, ly + 116], fill=(255, 255, 255, 225), outline=BLK)
    leg = [(MAG, "reef outline (shape.json, 2011-09-28 image)"), ((0, 90, 0), "Navionics drying patch (green): %d m2" % sh["nautical|drying"]["area_m2"]),
           ((0, 140, 255), "Navionics depth < 1 m (green + blue): %d m2" % sh["nautical|depth_lt_1m"]["area_m2"]),
           ((255, 0, 0), "survey (Fig. 9, Apr 2011) >0 m ACD zone: %d m2" % M["stats"]["crest_zone_area_m2"]["0.0"]), ((230, 200, 0), "survey >-1 m ACD zone: %d m2" % M["stats"]["crest_zone_area_m2"]["-1.0"])]
    for i, (col, t) in enumerate(leg):
        d.line([(lx + 8, ly + 14 + i * 21), (lx + 38, ly + 14 + i * 21)], fill=col + (255,), width=4)
        d.text((lx + 46, ly + 14 + i * 21), t, font=FONT(13), fill=BLK, anchor="lm")
    hdr = ["ANNOTATED COPY of Garmin Navionics Nautical Chart (metres, shallow shading 1 m), zoom 18 (0.378 m/px), screenshot 2026-10-05. Garmin Navionics, not for navigation; private research copy.",
           "Marked: reef outline (magenta), canonical 25 m grid, green drying patch and blue (< 1 m) fills measured, spot soundings read (red circles), survey zones from Fig. 9 for comparison."]
    foot = ["The Nautical Chart (contours at 1 m, spot soundings to 0.1 m) draws a drying patch of %d m2 and a < 1 m area of %d m2 (the SonarChart layer: %d / %d m2)." % (
                sh["nautical|drying"]["area_m2"], sh["nautical|depth_lt_1m"]["area_m2"], sh["sonar|drying"]["area_m2"], sh["sonar|depth_lt_1m"]["area_m2"]),
            "No drying height is printed, so the crest is only bounded: >= 0 m above chart datum; the survey (Fig. 9) peak is +0.68 m ACD (April 2011).",
            "Not read from this view (see REQUESTS_FOR_LIOR.md): drying heights, survey date of the chart, vertical datum statement."]
    out = frame(v.img, hdr, foot)
    p = OUT / "navionics_nauticalchart_z18_annotated.png"; out.save(p); print("saved", p)


def fig_soundings():
    v = View("nautical", 17, (400, 330, 1400, 700), 1.4)
    d = v.d
    v.grid(50, ((-300, 150), (100, 350)))
    v.poly(reef_outline(), outline=MAG, width=3)
    # survey area outline
    ext = M["survey_extent"]
    v.poly(ext, outline=(255, 190, 0, 255), width=2)
    rows = NAVM["soundings"]
    n = 0
    for r in rows:
        P = v.px(r["px"], r["py"])
        n += 1
        col = (200, 0, 0) if r["used"] else (120, 120, 120)
        d.ellipse([P[0] - 11, P[1] - 11, P[0] + 11, P[1] + 11], outline=col, width=2)
        d.text((P[0], P[1]), str(n), font=FONTB(12), fill=col, anchor="mm")
    # table
    W = v.img.width
    tab_h = 14 + 17 * 12
    hdr = ["ANNOTATED COPY of Garmin Navionics Nautical Chart, zoom 17 (0.756 m/px), metres, screenshot 2026-10-05. Garmin Navionics, not for navigation; private research copy.",
           "Marked: spot soundings and contour labels read by eye (numbered), reef outline (magenta), the extent of the Fig. 9 depth survey (orange); table: Navionics depth vs model seabed at the same point."]
    img = v.img
    out = Image.new("RGB", (W, img.height + 6 + 15 * 12), (255, 255, 255))
    out.paste(img, (0, 0)); dd = ImageDraw.Draw(out)
    y0 = img.height + 4
    cols = 3; per = math.ceil(len(rows) / cols)
    for c in range(cols):
        for i in range(per):
            k = c * per + i
            if k >= len(rows):
                break
            r = rows[k]
            md = "n/a (outside model grid)" if r["model_depth_m"] is None else ("%.2f m  (diff %+.2f)%s" % (r["model_depth_m"], r["diff_model_minus_nav_m"], "" if r["used"] else "  [on reef: not used]"))
            dd.text((8 + c * (W // cols), y0 + i * 13), "%2d  Nav %.1f m  | model %s" % (k + 1, r["depth_m"], md), font=FONT(11), fill=(0, 0, 0))
    cm = NAVM["comparison"]["soundings_all"]
    foot = ["Model seabed - Navionics sounding (the %d soundings that fall on seabed inside the model grid): mean %+.2f m, sd %.2f m, rms %.2f m. Positions read to about +-1 m, depths to 0.1 m." % (cm["n"], cm["mean"], cm["sd"], cm["rms"]),
            "Soundings inside the Fig. 9 survey area test the survey seabed; those outside test the thin-plate-spline extrapolation (an independent check); datum of Navionics not stated (assumed chart datum)."]
    res = frame(out, hdr, foot)
    p = OUT / "navionics_nauticalchart_z17_soundings_annotated.png"; res.save(p); print("saved", p)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    fig_sonar(); fig_nautical(); fig_soundings()
