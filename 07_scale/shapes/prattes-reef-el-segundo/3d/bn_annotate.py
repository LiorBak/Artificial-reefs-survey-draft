"""bn_annotate.py - annotated copies of the pages / figures of Borrero & Nelsen (2003) that the 3D model uses (annotated/A12-A17).

Input : ../src/borrero_nelsen_2003_prattes_monitoring_results.pdf (private research copy supplied by Lior), src/bn2003_digitised.json (bn_digitise.py),
        ../src/img1_skelly_diagram.png, src/navionics/nav_transect.json, NOAA DEM export
Run   : python bn_annotate.py           (called by build_3d.py --annotations)
"""
import json
import math
import os

import fitz
import matplotlib
import numpy as np
from PIL import Image, ImageDraw

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import make_annotations as MA  # noqa: E402
import reef3d_lib as L  # noqa: E402

HERE = L.HERE
OUT = os.path.join(HERE, "annotated")
PDF = os.path.join(os.path.dirname(HERE), "src", "borrero_nelsen_2003_prattes_monitoring_results.pdf")
DIG = json.load(open(os.path.join(L.SRC, "bn2003_digitised.json"), encoding="utf-8"))
CITE = "Borrero, J.C. & Nelsen, C. (2003). Results of a comprehensive monitoring program at Pratte's Reef (16-page PDF supplied by Lior on 2026-10-05; venue and year are not printed in the file; private research copy)"


def page_img(doc, pn, dpi=110, clip=None):
    pm = doc[pn].get_pixmap(dpi=dpi, clip=clip)
    return Image.frombytes("RGB", (pm.width, pm.height), pm.samples)


def highlight(doc, pn, phrases, color=(1, 0.9, 0.1)):
    page = doc[pn]
    n = 0
    for ph in phrases:
        for r in page.search_for(ph):
            a = page.add_highlight_annot(r)
            a.set_colors(stroke=color)
            a.update()
            n += 1
    return n


def fig_text_pages():
    doc = fitz.open(PDF)
    ph1 = ["approximately 200 m south", "Hyperion Sewage", "1-mile outfall", "within 500 m of two", "Grand Street Jetty"]
    ph2 = ["110 sand filled geotextile bags", "4’ x 7’ x 10’", "280 ft", "7.9 m", "between 80 and 90%", "September 22", "apex", "pointing offshore", "approximately - 6 ft MLLW", "Figure 4 shows the design placement"]
    ph3 = ["April 23rd and 24th 2001", "Ninety new bags", "increased the reef volume by 80%", "within 3ft of MLLW", "placed directly", "over the phase 1 bags"]
    for pn, ph in ((0, ph1), (1, ph2), (2, ph3)):
        n = highlight(doc, pn, ph)
        print("highlighted", n, "phrases on page", pn + 1)
    imgs = [page_img(doc, pn, 100) for pn in (0, 1, 2)]
    W = sum(i.width for i in imgs)
    H = max(i.height for i in imgs)
    canvas = Image.new("RGB", (W, H), "white")
    x = 0
    for i in imgs:
        canvas.paste(i, (x, 0))
        x += i.width
    cap = [CITE + ". Pages 1, 2 and 3.",
           "Highlighted (yellow): p.1 - the reef is 'approximately 200 m south of the Hyperion Sewage Treatment Plant's 1-mile outfall' and 'within 500 m' of the outfall and the Grand Street Jetty (position). "
           "p.2 - 110 sand-filled geotextile bags, 4' x 7' x 10', maximum volume 280 ft3 (7.9 m3), filled 80-90 %, installed 22 Sept 2000, V with the apex pointing offshore, "
           "'After the initial installation, the depth at the outermost point of the reef was approximately - 6 ft MLLW' (Phase I crest, datum MLLW). p.3 - Phase II on 23-24 April 2001: 90 new bags, +80 % volume, crest widened and made shallower 'to within 3ft of MLLW', placed directly over the Phase I bags.",
           "Used for: bag size and count (primary source, replaces the web summary), Phase I and II dates, crest datum and values (6 ft MLLW = 1.829 m; 3 ft MLLW = 0.914 m), site position text. NOT given anywhere in the paper: stack height / number of courses, a plan of the built reef."]
    MA.caption_canvas(canvas, cap, fsize=15).save(os.path.join(OUT, "A12_bn2003_p1-3_text_highlighted.png"))


def fig_fig4_vs_img1():
    doc = fitz.open(PDF)
    pm = doc[2]
    xref = [im[0] for im in pm.get_images(full=True)][0]       # Fig. 4 raster (371 x 468 px)
    pix = fitz.Pixmap(doc, xref)
    if pix.n >= 4:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    f4 = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    i1 = Image.open(os.path.join(os.path.dirname(HERE), "src", "img1_skelly_diagram.png")).convert("RGB")
    s = 3
    f4b = f4.resize((f4.width * s, f4.height * s), Image.LANCZOS)
    i1b = i1.resize((int(i1.width * (f4b.height / i1.height)), f4b.height), Image.LANCZOS)
    W = f4b.width + i1b.width + 30
    canvas = Image.new("RGB", (W, f4b.height + 40), "white")
    canvas.paste(f4b, (0, 40))
    canvas.paste(i1b, (f4b.width + 30, 40))
    d = ImageDraw.Draw(canvas)
    f = MA.font(20)
    d.text((10, 8), "Borrero & Nelsen (2003) Fig. 4 'The design layout of Pratte's Reef' (371 x 468 px, shown 3x)", fill=(200, 0, 0), font=f)
    d.text((f4b.width + 40, 8), "img1: Skelly drawing used for the traced outline (308 x 385 px, scaled to the same height)", fill=(0, 0, 200), font=f)
    cap = [CITE + ". Fig. 4 on p.3 (embedded raster).",
           "Result: Fig. 4 is the SAME Skelly Engineering drawing as img1 (same BAG COUNT 110, OPTIONAL BAGS 30, scale bar 0-15-30-60-90 ft, '45 deg' and 'WAVE DIRECTION' marks, TOP OF BAG MIN DEPTH -6' MSL call-outs at both arm tips, title block): "
           "it is a third reproduction of the DESIGN layout, captioned 'The design layout of Pratte's Reef'. The paper contains no as-built plan and no bag-position survey, so the verified outline in shape.json is not re-traced or changed."]
    MA.caption_canvas(canvas, cap, fsize=16).save(os.path.join(OUT, "A13_bn2003_fig4_vs_skelly_img1.png"))


def fig_fig2():
    doc = fitz.open(PDF)
    xref = [im[0] for im in doc[1].get_images(full=True)][0]       # Fig. 2 aerial (432 x 231 px)
    pix = fitz.Pixmap(doc, xref)
    if pix.n >= 4:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    s = 3
    big = im.resize((im.width * s, im.height * s), Image.LANCZOS).convert("RGBA")
    d = ImageDraw.Draw(big, "RGBA")
    f12, f14 = MA.font(15), MA.font(17)
    rl = [270, 310, 337, 376, 424, 532]                      # range-line x (px of the 3x image), read by eye
    chev = (340, 462)
    outfall_x, grand_x, es_x = 185, 660, 1090
    m_per_px3 = 550.0 / (rl[-1] - rl[0])
    for k, x in enumerate(rl):
        d.line([(x, 345), (x, 462)], fill=(255, 60, 60, 255), width=2)
        MA.ImageDraw.Draw(big).text((x - 8, 322), str(k + 1), fill=(255, 220, 0, 255), font=f14)
    d.line([(rl[0], 335), (rl[-1], 335)], fill=(255, 220, 0, 255), width=3)
    MA.ImageDraw.Draw(big).text((rl[0] + 20, 306), "6 range lines span about 550 m (text, p.4): %.2f m per 3x px" % m_per_px3, fill=(255, 255, 0, 255), font=f12)
    d.ellipse([chev[0] - 14, chev[1] - 14, chev[0] + 14, chev[1] + 14], outline=(0, 255, 255, 255), width=3)
    MA.ImageDraw.Draw(big).text((chev[0] - 70, chev[1] + 22), "reef chevron (on range line 3)", fill=(0, 255, 255, 255), font=f14)
    for x, lab in ((outfall_x, "1-mile outfall"), (grand_x, "Grand Street jetty (arrow tip)"), (es_x, "El Segundo jetty")):
        d.line([(x, 440), (x, 500)], fill=(255, 140, 0, 255), width=3)
    # distances
    y_line = 520
    for x0, x1, col in ((outfall_x, chev[0], (255, 140, 0, 255)), (chev[0], grand_x, (255, 140, 0, 255))):
        d.line([(x0, y_line), (x1, y_line)], fill=col, width=3)
        d.line([(x0, y_line - 8), (x0, y_line + 8)], fill=col, width=3)
        d.line([(x1, y_line - 8), (x1, y_line + 8)], fill=col, width=3)
        MA.ImageDraw.Draw(big).text(((x0 + x1) / 2 - 28, y_line + 8), "%.0f m" % ((x1 - x0) * m_per_px3), fill=(255, 200, 120, 255), font=f14)
    MA.ImageDraw.Draw(big).text((20, 40), "Fig. 2 north is to the LEFT (the 1-mile outfall, which lies north of the reef, is on the left); sea at the bottom", fill=(255, 255, 255, 255), font=f12)
    cap = [CITE + ". Fig. 2 on p.2 (embedded 432 x 231 px raster, shown 3x); caption: 'A section of an aerial photograph showing the location of the reef relative to other coastal structures. The black lines crossing the beach correspond to range lines used in shoreline profile monitoring.'",
           "Read: RED = the six range lines (the reef chevron sits on line 3 = the profile line 'Line 3' of Figs 5-8); YELLOW bar = 550 m between lines 1 and 6 (text p.4) = scale %.2f m per 3x px (cross-check: Grand Street jetty to El Segundo jetty then spans %.0f m, "
           "matching the roughly 0.9 km between the Navionics/satellite positions); ORANGE = the 1-mile outfall (faint pipe in the surf), the Grand Street jetty arrow and the El Segundo jetty. Reef to outfall: %.0f m (text p.1: 'approximately 200 m'); reef to Grand Street jetty: %.0f m (text: 'within 500 m'). "
           "The aerial gives the reef position only along the beach, to about +-60 m; no outline is drawn." % (m_per_px3, (es_x - grand_x) * m_per_px3, (chev[0] - outfall_x) * m_per_px3, (grand_x - chev[0]) * m_per_px3),
           "Position derived (see METHODS_3D.md 3.10): outfall landfall read on the Navionics chart (33.9231 N, 118.4337 W) + 200-320 m south along 155 deg + 91 m offshore = 33.9202-33.9211 N, 118.4332-118.4337 W; centre of the Fig. 9 survey window 33.92058 N, 118.43335 W; Grand-Street-jetty-based estimate (660 m north of 33.91685 N, 118.43030 W) 33.9219 N, 118.4342 W."]
    MA.caption_canvas(big.convert("RGB"), cap, fsize=15).save(os.path.join(OUT, "A14_bn2003_fig2_aerial_position.png"))


def fig_profiles():
    f5, f7, f8 = DIG["fig5"], DIG["fig7"], DIG["fig8"]
    d7, d5 = DIG["fig7_oct2001_derived"], DIG["fig5_derived"]
    fig, ax = plt.subplots(2, 2, figsize=(15, 9.5), gridspec_kw={"height_ratios": [1.3, 1]})
    a = ax[0, 0]
    d, z = np.array(f5["distance_m"]), np.array(f5["z_m"])
    a.plot(d, z, "k-o", ms=3, label="Fig. 5: centreline profile, Oct 2001 (digitised from the PDF path)")
    a.axhline(0, color="c", lw=1)
    a.axhline(f5["tide_lines_z_m"]["max_high_tide_z"], color="b", lw=1)
    a.text(2, 0.1, "'Approx. Min Low Tide' = 0 (read as MLLW)", color="c", fontsize=8)
    a.text(2, f5["tide_lines_z_m"]["max_high_tide_z"] + 0.1, "'Approx. Max High Tide' = +%.2f m (6.0 ft)" % f5["tide_lines_z_m"]["max_high_tide_z"], color="b", fontsize=8)
    a.axhline(0.849, color="g", ls=":", lw=1)
    a.text(2, 0.95, "MSL = MLLW + 0.849 m", color="g", fontsize=8)
    a.plot([d5["peak_distance_m"]], [d5["peak_z_m"]], "r^", ms=10)
    a.annotate("crest %.2f m\nrelief %.1f m above landward bed" % (d5["peak_z_m"], d5["relief_above_landward_bed_m"]), (d5["peak_distance_m"], d5["peak_z_m"]), xytext=(95, -1.2), arrowprops=dict(arrowstyle="->", color="r"), color="r", fontsize=9)
    a.plot([d5["bed_landward"][0], d5["bed_seaward"][0]], [d5["bed_landward"][1], d5["bed_seaward"][1]], "bs", ms=7)
    a.set_xlim(0, 300)
    a.set_ylim(-5, 7.5)
    a.set_xlabel("distance from the dune base (m)")
    a.set_ylabel("z (m), Fig. 5 axis")
    a.set_title("Fig. 5 (p.4): profile along the reef centreline\n(range line 3), Oct 2001, after Phase II", fontsize=9.5)
    a.grid(alpha=0.3)
    a.legend(fontsize=8, loc="lower left")
    b = ax[0, 1]
    for nm, col in (("Nov 2000", "red"), ("Oct 2001", "black"), ("Oct 2002", "blue")):
        p = f7["profiles"][nm]
        b.plot(p["distance_m"], p["z_m"], "-o", color=col, ms=3, label="Fig. 7: " + nm)
    b.plot([d7["peak_distance_m"]], [d7["peak_z_m"]], "r^", ms=10)
    b.annotate("Oct 2001 crest %.2f m at d = %.1f m\n(%.1f m from the z = 0 crossing at d = %.1f m)\nbase width %.1f m, relief %.1f m" % (d7["peak_z_m"], d7["peak_distance_m"], d7["peak_from_zero_crossing_m"], d7["zero_crossing_distance_m"], d7["base_width_m"], d7["relief_above_landward_bed_m"]),
               (d7["peak_distance_m"], d7["peak_z_m"]), xytext=(20, -2.6), arrowprops=dict(arrowstyle="->", color="r"), color="r", fontsize=8, bbox=dict(boxstyle="round", fc="w", alpha=0.9))
    b.axhline(0, color="gray", lw=0.8)
    b.set_xlim(0, 260)
    b.set_ylim(-5.5, 6.5)
    b.set_xlabel("distance from the dune base (m)")
    b.set_ylabel("z (m), Fig. 7 axis (datum not stated)")
    b.set_title("Fig. 7 (p.6): the same line, Nov 2000 (stops at 109 m,\ndoes not reach the reef), Oct 2001, Oct 2002", fontsize=9.5)
    b.grid(alpha=0.3)
    b.legend(fontsize=8, loc="lower left")
    c = ax[1, 0]
    names = list(f8["crest"].keys())
    zc = [f8["crest"][k]["z_m"] for k in names]
    c.plot(range(len(names)), zc, "r-o")
    for i, k in enumerate(names):
        c.annotate("%.2f m" % zc[i], (i, zc[i]), xytext=(4, 6), textcoords="offset points", fontsize=9)
    c.set_xticks(range(len(names)))
    c.set_xticklabels(names)
    c.set_ylabel("crest z (m), Fig. 8 axis")
    c.set_title("Fig. 8 (p.6, raster 'Year 2 Reef Closeup'): crest eroded\nabout %.1f m in 16 months (read by eye, +-0.05 m)" % (zc[0] - zc[-1]), fontsize=9.5)
    c.grid(alpha=0.3)
    e = ax[1, 1]
    e.axis("off")
    import textwrap
    txt = ("What was read (all after Phase II, April 2001; Phase I profile NOT available):\n"
           "- Fig. 5 and Fig. 7/8 are the same data: Fig. 5 = Fig. 7 + %.2f m vertically (peak and bed both) and 5.5 m horizontally.\n"
           "- Fig. 5 zero line is labelled 'Approx. Min Low Tide' and the high-tide line sits at +%.2f m (6 ft): read as MLLW-referenced.\n"
           "- Fig. 7/8 axis = Fig. 5 axis + 1.44 m = MHW - MLLW (1.43 m) or MSL - LAT (1.47 m): datum ambiguous, not stated.\n"
           "- Oct 2001 crest: %.2f m (Fig. 5) / %.2f m (Fig. 7); relief %.1f m above the landward bed, %.1f m above the seaward bed;\n  base width %.1f m (design apex block: 10.6 m).\n"
           "- Beds beside the reef: %.2f / %.2f m (Fig. 5 axis), i.e. %.2f / %.2f m MSL if the axis is MLLW; DEM at y = 91 m: -3.75 m MSL.\n"
           "- Crest distance from the MSL waterline (MLLW reading of Fig. 5: z = 0.849 m at d = %.1f m): %.1f m (centre of the base: %.1f m);\n  text distance 91.44 m (100 yd).\n"
           "- May 2001 crest %.2f m on the Fig. 8 axis = %.2f m on the Fig. 5 axis: 'within 3 ft (0.91 m) of MLLW' (p.3) holds." % (
               DIG["offset_fig5_minus_fig7_m"], f5["tide_lines_z_m"]["max_high_tide_z"], d5["peak_z_m"], d7["peak_z_m"], d7["relief_above_landward_bed_m"], d7["relief_above_seaward_bed_m"], d7["base_width_m"],
               d5["bed_landward"][1], d5["bed_seaward"][1], d5["bed_landward"][1] - 0.849, d5["bed_seaward"][1] - 0.849,
               d5["plus_0p849_crossing_distance_m"], d5["peak_distance_m"] - d5["plus_0p849_crossing_distance_m"], 0.5 * (d5["bed_landward"][0] + d5["bed_seaward"][0]) - d5["plus_0p849_crossing_distance_m"],
               f8["crest"]["May 2001"]["z_m"], f8["crest"]["May 2001"]["z_m"] + DIG["offset_fig5_minus_fig7_m"]))
    e.text(0, 1.0, "\n".join(textwrap.fill(par, 92, subsequent_indent="    ") for par in txt.split("\n")), va="top", fontsize=8.2, family="monospace")
    fig.text(0.01, 0.005, CITE + ". Figs 5 and 7 are vector graphics: the curves were read from the PDF paths (bn_digitise.py), axes calibrated on the tick marks. Fig. 8 is a raster read by eye.", fontsize=7.5)
    fig.tight_layout(rect=(0, 0.02, 1, 1), h_pad=3)
    fig.savefig(os.path.join(OUT, "A15_bn2003_fig5-8_reef_profiles_digitised.png"), dpi=110)
    plt.close(fig)


def fig_fig9():
    from pyproj import Transformer
    f9 = DIG["fig9"]
    to_ll = Transformer.from_crs("EPSG:32611", "EPSG:4326", always_xy=True)
    E0, N0 = 367505.0, 3754275.0
    A = L.load_dem()
    ds = L.load_datums("9410840")
    off = ds["MSL"] - ds["NAVD88"]
    bx, by = math.radians(155), math.radians(245)
    fig, ax = plt.subplots(1, 2, figsize=(15, 7.2), gridspec_kw={"width_ratios": [1.15, 1]})
    cols = {-4: "#00cc99", -3: "#00aaff", -2: "#2a55ff", -1: "#4a00ff"}
    a = ax[0]
    for c in f9["contours"]:
        a.plot(np.array(c["easting_m"]) - E0, np.array(c["northing_m"]) - N0, "-" if c["solid"] else "--", color=cols[c["value_m"]], lw=2.2 if c["solid"] else 1.2)
    for v, col in cols.items():
        a.plot([], [], color=col, label="%d m" % v)
    a.plot([], [], "k-", label="March 2001 (winter profile)")
    a.plot([], [], "k--", label="October 2000 (summer, 4 weeks after Phase I)")
    # reef outline at the window centre, rotated into E/N (grid north ~ true north - 0.8 deg ignored)
    shape = json.load(open(L.SHAPE, encoding="utf-8"))
    poly = np.array(shape["canonical"]["polygons_m"][0])
    yc = shape["canonical"]["distance_offshore_m"]
    px, py = poly[:, 0], poly[:, 1] - yc
    e = px * math.sin(bx) + py * math.sin(by)
    n = px * math.cos(bx) + py * math.cos(by)
    a.fill(e, n, color="m", alpha=0.35, label="Phase I design outline (435 m2) centred on the window")
    a.plot(0, 0, "y*", ms=14, mec="k", label="window centre = position hint")
    a.set_aspect("equal")
    a.set_xlim(f9["window_E"][0] - E0, f9["window_E"][1] - E0)
    a.set_ylim(f9["window_N"][0] - N0, f9["window_N"][1] - N0)
    a.set_xlabel("easting - 367505 m (UTM 11N)")
    a.set_ylabel("northing - 3754275 m")
    a.set_title("Borrero & Nelsen (2003) Fig. 9 (p.7) re-drawn from the PDF paths on its UTM axes\n(contour values in m, datum not stated)", fontsize=10)
    a.grid(alpha=0.3)
    a.legend(fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=3)
    b = ax[1]
    # contour offsets vs DEM and DEM contour overlay
    Eg = np.arange(f9["window_E"][0], f9["window_E"][1], 2.0)
    Ng = np.arange(f9["window_N"][0], f9["window_N"][1], 2.0)
    EE, NN = np.meshgrid(Eg, Ng)
    lon, lat = to_ll.transform(EE, NN)
    Z = np.array([[L.sample(A, lo, la) - off for lo, la in zip(r1, r2)] for r1, r2 in zip(lon, lat)])
    lev_msl = [-5.5, -5.0, -4.5, -4.0, -3.5, -3.0, -2.5, -2.0]
    cs = b.contour(EE - E0, NN - N0, Z, levels=lev_msl, colors="0.45", linewidths=0.9)
    b.clabel(cs, fmt=lambda v: "%.1f" % v, fontsize=7)
    rows = []
    for c in f9["contours"]:
        en = np.array([c["easting_m"], c["northing_m"]]).T
        lo, la = to_ll.transform(en[:, 0], en[:, 1])
        zd = np.array([L.sample(A, x, y) - off for x, y in zip(lo, la)])
        rows.append((c["value_m"], c["solid"], float(np.nanmean(zd))))
        b.plot(en[:, 0] - E0, en[:, 1] - N0, "-" if c["solid"] else "--", color=cols[c["value_m"]], lw=2.0 if c["solid"] else 1.1)
    b.set_aspect("equal")
    b.set_xlim(f9["window_E"][0] - E0, f9["window_E"][1] - E0)
    b.set_ylim(f9["window_N"][0] - N0, f9["window_N"][1] - N0)
    b.set_xlabel("easting - 367505 m")
    b.set_title("same contours over the NOAA DEM contours (grey, m rel. MSL)", fontsize=9)
    b.grid(alpha=0.3)
    mean_off = {"Oct 2000": np.mean([v - z for v, s, z in rows if not s]), "Mar 2001": np.mean([v - z for v, s, z in rows if s])}
    fig.text(0.01, 0.01, CITE + ". Fig. 9 is a vector graphic: the eight contours were read from the PDF paths; axes calibrated on the tick marks (E = 367460 + (x - 216.1)/2.495 pt/m, N = 3754240 + (309.5 - y)/2.485); UTM zone 11, horizontal datum not stated (NAD83/WGS84 assumed).\n"
             "Read: the window (about 112 x 71 m) is centred on 33.92058 N, 118.43335 W; contours run along 155 deg (shore bearing confirmed); no bag signature is visible and the reef outline is not drawn; the reef (58 x 29 m) fits inside the window. "
             "Mean (survey contour value - NOAA DEM z_MSL at the same points): Oct 2000 %+.2f m, Mar 2001 %+.2f m (MLLW would give +0.85 m): datum of Fig. 9 not stated; seasonal change and the DEM's 10 m cells contribute." % (mean_off["Oct 2000"], mean_off["Mar 2001"]), fontsize=7.5)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(os.path.join(OUT, "A16_bn2003_fig9_bathymetry_utm.png"), dpi=110)
    plt.close(fig)
    return mean_off


def fig_p14_p16():
    doc = fitz.open(PDF)
    highlight(doc, 13, ["Narrowneck is 70 times bigger", "Pratte’s only extends 30", "Narrowneck extends"])
    highlight(doc, 15, ["approximately 1600 cubic meters", "200", "geotextile bags", "mostly level with the sand"])
    highlight(doc, 13, ["200 meters north of Pratte"])
    imgs = [page_img(doc, 13, 100), page_img(doc, 15, 100)]
    canvas = Image.new("RGB", (imgs[0].width + imgs[1].width, max(i.height for i in imgs)), "white")
    canvas.paste(imgs[0], (0, 0))
    canvas.paste(imgs[1], (imgs[0].width, 0))
    cap = [CITE + ". Pages 14 and 16.",
           "Highlighted: p.14 - Narrowneck is 70 times bigger in volume; 'Pratte's only extends 30' m cross-shore (the V's cross-shore extent: 28.6 m in the traced outline); the outfall is 200 m north of the reef. p.16 - 'approximately 1600 cubic meters of sand contained in 200 geotextile bags' "
           "= 200 x 7.9 m3 = 1580 m3, i.e. the NOMINAL bag volume (not the 80-90 % filled volume); 'The reef bags are mostly level with the sand' (end state). No stack height is given."]
    MA.caption_canvas(canvas, cap, fsize=15).save(os.path.join(OUT, "A17_bn2003_p14_p16_text_highlighted.png"))


def main():
    fig_text_pages()
    fig_fig4_vs_img1()
    fig_fig2()
    fig_profiles()
    mo = fig_fig9()
    fig_p14_p16()
    print("A12-A17 written; Fig. 9 mean offsets", mo)
    return mo


if __name__ == "__main__":
    main()
