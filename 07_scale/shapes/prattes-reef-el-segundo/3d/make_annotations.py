"""make_annotations.py - regenerates every annotated source image in 3d/annotated/ (STEP 2 of the brief).

Reads: ../src/img1_skelly_diagram.png, ../src/img6_ccc_exhibit3_concept_plan.png (private research copies),
       src/ccc_W5a-10-1998_staff_report.pdf, src/icce2010_borrero_mead_moores_SFC.pdf, src/*.tif, src/noaa_*.json.
Writes: annotated/*.png
Run:  python make_annotations.py
"""
import json
import math
import os

import fitz  # PyMuPDF
import matplotlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import reef3d_lib as L  # noqa: E402

HERE = L.HERE
SRC = L.SRC
OUT = os.path.join(HERE, "annotated")
SHAPEDIR = os.path.dirname(HERE)
os.makedirs(OUT, exist_ok=True)

RED = (220, 30, 30)
BLUE = (30, 90, 220)
GREEN = (20, 140, 60)
ORANGE = (240, 130, 0)


def font(size):
    for f in ("arial.ttf", "C:/Windows/Fonts/arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            continue
    return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def caption_canvas(img, caption_lines, margin_w=0, pad=10, fsize=16, bottom=True):
    """put img on a white canvas with a caption block below it"""
    fnt = font(fsize)
    W = img.width + margin_w
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    lines = []
    for c in caption_lines:
        lines += wrap(tmp, c, fnt, W - 2 * pad) + [""]
    h = len(lines) * (fsize + 4) + 2 * pad
    canvas = Image.new("RGB", (W, img.height + h), (255, 255, 255))
    canvas.paste(img, (0, 0))
    d = ImageDraw.Draw(canvas)
    y = img.height + pad
    for ln in lines:
        d.text((pad, y), ln, fill=(0, 0, 0), font=fnt)
        y += fsize + 4
    return canvas


def box(draw, xy, color, width=3, label=None, fnt=None, label_xy=None):
    draw.rectangle(xy, outline=color, width=width)
    if label:
        draw.text(label_xy or (xy[0], xy[1] - 20), label, fill=color, font=fnt or font(16))


# ---------------------------------------------------------------------------------------------------
def fig_skelly_crest_labels():
    """A1: the two 'TOP OF BAG MIN DEPTH -6' MSL' call-outs and the scale bar on the Skelly design drawing (img1)."""
    im = Image.open(os.path.join(SHAPEDIR, "src", "img1_skelly_diagram.png")).convert("RGB")
    k = 4
    big = im.resize((im.width * k, im.height * k), Image.LANCZOS)
    d = ImageDraw.Draw(big)
    f = font(20)
    # call-out 1 (upper arm tip) and call-out 2 (lower arm tip); coordinates read on the 308 x 385 original
    for (x0, y0, x1, y1, lab) in ((236, 20, 308, 64, "1"), (228, 262, 308, 292, "2")):
        d.rectangle((x0 * k, y0 * k, x1 * k, y1 * k), outline=RED, width=4)
        d.text((x0 * k - 26, y0 * k - 2), lab, fill=RED, font=font(26))
    # scale bar ticks (x px from the run-length scan in METHOD.md): 15, 30, 60, 90 ft at y 329-337
    for xt, lab in ((20.5, "15'"), (44.0, "30'"), (91.5, "60'"), (138.0, "90'")):
        d.line((xt * k, 322 * k, xt * k, 342 * k), fill=BLUE, width=3)
        d.text((xt * k - 14, 343 * k), lab, fill=BLUE, font=f)
    d.text((6 * k, 306 * k), "scale-bar ticks used", fill=BLUE, font=f)
    cap = [
        "Source: Skelly Engineering plan-view design drawing 'PRATTE'S REEF' (undated, fall 2000 Phase I design; 110 bags + 30 optional) "
        "via Raised Water Research, https://raisedwaterresearch.com/wp-content/uploads/2019/07/Pratts-Reef-Diagram.png (private copy, 308 x 385 px, shown 4x).",
        "RED boxes 1 and 2: the two call-outs at the arm tips read 'TOP OF BAG MIN DEPTH -6' MSL' (the right edge of the scan cuts the words 'BAG' and 'DEPTH'). "
        "Reading: top of bag no shallower than 6 ft = 1.829 m below MEAN SEA LEVEL (design minimum depth, not a survey). With the NOAA Santa Monica datums "
        "(MSL - MLLW = 0.849 m) this is 0.98 m below MLLW. Used as crest state A.",
        "BLUE ticks: the printed scale bar (0-15-30-60-90 ft); least-squares fit 1.5712 px/ft, i.e. 5.155 px/m (METHOD.md, shape.json), which fixes the plan size, not the depth.",
    ]
    out = caption_canvas(big, cap)
    out.save(os.path.join(OUT, "A1_skelly_drawing_crest_labels_and_scale.png"))


def render_page(pdf, pno, dpi):
    d = fitz.open(pdf)
    pix = d[pno].get_pixmap(dpi=dpi)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    return img, d[pno]


def fig_ccc_exhibit2():
    """A2: CCC Exhibit 2 (Skelly, June 1997 cross-section): datum labels and top of reef."""
    img, _ = render_page(os.path.join(SRC, "ccc_W5a-10-1998_staff_report.pdf"), 29, 150)
    s = 150 / 110.0
    d = ImageDraw.Draw(img)
    f = font(22)
    boxes = [
        ((795, 235, 905, 275), "MHHW +2.6 ft MSL", GREEN),
        ((795, 380, 905, 420), "MSL (0)", GREEN),
        ((795, 530, 905, 572), "MLLW -2.8 ft", GREEN),
        ((790, 755, 915, 795), "TOP OF REEF -7 ft MSL", RED),
        ((245, 733, 445, 762), "bag 12 ft wide", BLUE),
        ((140, 830, 185, 900), "3 ft", BLUE),
    ]
    for (x0, y0, x1, y1), lab, col in boxes:
        d.rectangle((x0 * s, y0 * s, x1 * s, y1 * s), outline=col, width=4)
        d.text((x0 * s - (95 if x0 > 700 else 0), y1 * s + 2 if x0 < 700 else y0 * s - 26), lab, fill=col, font=f)
    cap = [
        "Source: California Coastal Commission staff report W5a, application E-98-15 (Surfrider Foundation - Pratte's Reef), hearing 13 Oct 1998, Exhibit 2 'Reef design profile view' "
        "(Skelly Engineering, June 1997 - the 1996-98 CONCEPT of about 30 large bags, not the built design). https://documents.coastal.ca.gov/reports/1998/10/W5a-10-1998.pdf, PDF p.30 (rendered 150 dpi).",
        "GREEN: the three datum labels printed on the drawing: MHHW +2.6 ft MSL (0.79 m), MLLW -2.8 ft (-0.85 m). NOAA station 9410840 gives +0.804 m and -0.849 m: agreement within 0.015 m, "
        "which confirms that 'MSL' on Skelly's drawings is the NOAA Santa Monica/LA epoch MSL and that MLLW lies 0.85 m BELOW MSL.",
        "RED: 'TOP OF REEF -7 MSL' (-2.13 m MSL) of the 1997 concept. BLUE: bag 12 ft wide x 3 ft high (concept bags; schematic - the drawing is not to scale). "
        "Used only as a cross-check of the datum (the concept crest was 1 ft deeper than the later -6 ft design minimum).",
    ]
    caption_canvas(img, cap).save(os.path.join(OUT, "A2_ccc_exhibit2_profile_datums.png"))


def fig_ccc_exhibit3_contours():
    """A3: CCC Exhibit 3 plan view (July 1996 concept, depth contours in ft MSL): section A-A and contour crossings."""
    im = Image.open(os.path.join(SHAPEDIR, "src", "img6_ccc_exhibit3_concept_plan.png")).convert("RGB")
    c = np.array([763.37, 996.83])
    dv = np.array([0.91802, -0.39653])
    nv = np.array([-dv[1], dv[0]])
    d = ImageDraw.Draw(im)
    f = font(34)
    # section line A-A (fitted by PCA on the thick stroke; bearing 66.6 deg)
    d.line([tuple(c + dv * -600), tuple(c + dv * 600)], fill=GREEN, width=3)
    # contour crossings read along A-A (t in px along A-A from the line centre; -ve = seaward/WSW)
    cross = [(-351, "-15 ft", "read", None), (-185, "-10 ft", "interpolated under the bags (+-20 px)", None),
             (-28, "-5 ft", "interpolated under the bags (+-20 px)", None), (46, "0 ft", "read", None),
             (353, "+5 ft", "read", None)]
    for t, lab, how, _ in cross:
        p = c + dv * t
        d.ellipse((p[0] - 14, p[1] - 14, p[0] + 14, p[1] + 14), outline=RED, width=5)
        q = p + nv * (70 if lab in ("-10 ft", "0 ft") else -70)
        d.text((q[0] - 40, q[1] - 18), lab + ("*" if how != "read" else ""), fill=RED, font=f)
    d.text((620, 1500), "RED circles = contour crossings of A-A (* = interpolated through the drawn bags)", fill=RED, font=font(30))
    cap = [
        "Source: California Coastal Commission staff report W5a, application E-98-15, Exhibit 3 'Reef design plan view' (Skelly Engineering, July 1996 CONCEPT: about 30 large bags, two 150 ft wings; "
        "'depth contours in feet, MSL'; north arrow up), PDF p.31 raster, private copy. https://documents.coastal.ca.gov/reports/1998/10/W5a-10-1998.pdf",
        "GREEN: cross-shore section line A-A, fitted to the thick stroke (bearing 66.6 deg, WSW to ENE). RED: the five contour crossings read along A-A at -15, -10, -5, 0, +5 ft MSL "
        "(spacing 166, 157, 74, 307 px; the two '150 ft' dimension lines of this sketch measure 237 and 279 px, so the sketch is NOT to scale).",
        "Use: QUALITATIVE cross-check only. The contours are shore-parallel (155/335 deg) and deepen seaward as in the NOAA DEM; the reef sketch straddles the -10 and -5 ft contours "
        "(1.5-3 m), i.e. SHALLOWER than the 15 ft (4.6 m) stated in the same report's text. No number of the 3D model is taken from this figure.",
    ]
    out = caption_canvas(im.resize((im.width // 2, im.height // 2), Image.LANCZOS), cap)
    out.save(os.path.join(OUT, "A3_ccc_exhibit3_contours_section_AA.png"))


def highlight_pdf(pdf, pno, phrases, out_name, caption, dpi=130, clip=None):
    doc = fitz.open(pdf)
    page = doc[pno]
    n = 0
    for ph in phrases:
        rects = page.search_for(ph, clip=clip) if clip else page.search_for(ph)
        for r in rects:
            page.add_highlight_annot(r)
            n += 1
    pix = page.get_pixmap(dpi=dpi, clip=clip)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    caption_canvas(img, caption, fsize=15).save(os.path.join(OUT, out_name))
    return n


def fig_pdf_highlights():
    icce = os.path.join(SRC, "icce2010_borrero_mead_moores_SFC.pdf")
    ccc = os.path.join(SRC, "ccc_W5a-10-1998_staff_report.pdf")
    # ICCE p.7: Pratte's paragraph (page index 6)
    n1 = highlight_pdf(
        icce, 6,
        ["110 sand filled geotextile containers", "7.9 m", "between 80 and 90%", "outermost point", "approximately 1.8 m", "below MLLW",
         "made shallower", "within 1 m of MLLW", "placed directly over", "Ninety new bags", "increasing the", "reef volume by 80%"],
        "A4_icce2010_p7_pratte_text_highlighted.png",
        ["Source: Borrero, J.C., Mead, S.T. & Moores, A. (2010). Stability considerations and case studies of submerged structures constructed from large, sand filled, geotextile containers. "
         "Coastal Engineering Proceedings 1(32), structures.60, p.7 (doi:10.9753/icce.v32.structures.60; CC BY 4.0).",
         "Highlighted (yellow): 110 containers of max 7.9 m3 filled to 80-90%; 'after the initial installation, the depth at the outermost point of the reef was approximately 1.8 m below MLLW' "
         "(= -2.65 m MSL, crest state B); April 2001 +90 bags, volume +80%, 'crest ... widened and made shallower, to within 1 m of MLLW' (crest state C, later change, not modelled); new bags 'placed directly over the phase 1 bags'."],
        dpi=120)
    # ICCE p.2: Figure 1 (Pratte's bag 3 m x 1.2 m)
    doc = fitz.open(icce)
    page = doc[1]
    clip = fitz.Rect(60, 80, 560, 330)
    pix = page.get_pixmap(dpi=140, clip=clip)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    d = ImageDraw.Draw(img)
    sc = 140 / 72.0
    # box around the top row (Pratte's bag): PDF points approx x 120-420, y 52-100 -> clip-relative
    x0, y0, x1, y1 = (140 - clip.x0) * sc, (96 - clip.y0) * sc, (415 - clip.x0) * sc, (132 - clip.y0) * sc
    d.rectangle((x0, y0, x1, y1), outline=RED, width=4)
    caption_canvas(img, [
        "Source: Borrero, Mead & Moores (2010), ICCE, Fig. 1 on p.2 'Size comparison between sand filled geotextile containers'. RED box: 'A Pratte's Reef bag' = 3 m long x 1.2 m high "
        "(the max volume 7.9 m3 stated on p.7 then implies a plan width of about 2.2 m). Used for bag height (layer thickness 1.2 m) and bag length."], fsize=15).save(
        os.path.join(OUT, "A5_icce2010_fig1_pratte_bag_size.png"))
    # CCC p.11: project description (page index 10)
    n3 = highlight_pdf(
        ccc, 10,
        ["100 yards", "150 feet long", "7 feet high", "15 feet of water", "9,000 square feet", "300 yards north"],
        "A6_ccc_p11_project_description_highlighted.png",
        ["Source: California Coastal Commission staff report W5a, application E-98-15 (13 Oct 1998), section 4.2 Project Description, p.11 (PDF p.11). "
         "Highlighted: 'The proposed project site is 300 yards north of the Grand Avenue jetty and 100 yards offshore ... each wing approximately 150 feet long and 7 feet high ... located in 15 feet of water (MSL)'. "
         "This is the 1996-98 CONCEPT (about 30 large bags). It supports the seabed depth at the site (15 ft = 4.57 m MSL at ~100 yd offshore) and the site position hint (north of the jetty); "
         "the later 110-bag design is smaller."],
        dpi=120)
    return n1, n3


# ---------------------------------------------------------------------------------------------------
def fig_dem(shape):
    """A7: NOAA DEM map + shore-normal profile with the reef, crest states, datums and the text depth statements."""
    xb = shape["canonical"].get("alongshore_bearing_deg", 155.0)
    A = L.load_dem()
    ds_lev, ds = L.datum_levels_msl()
    off = ds["MSL"] - ds["NAVD88"]
    prof = L.seabed_profile(xb, A=A)
    C = L.load_dem("noaa_socal_crm_1as_export.tif")
    prof_c = L.seabed_profile(xb, A=C, navd_to_msl=0.0, cell=1 / 3600.0)
    poly = np.array(shape["canonical"]["polygons_m"][0])
    ymin_p, ymax_p = poly[:, 1].min(), poly[:, 1].max()
    yc = shape["canonical"]["distance_offshore_m"]

    fig = plt.figure(figsize=(15, 8.2))
    ax = fig.add_axes([0.04, 0.10, 0.40, 0.84])
    ny, nx = A.shape
    lon = np.linspace(L.DEM_W + L.DEM_CELL / 2, L.DEM_E - L.DEM_CELL / 2, nx)
    lat = np.linspace(L.DEM_N - L.DEM_CELL / 2, L.DEM_S + L.DEM_CELL / 2, ny)
    Z = A - off
    asp = 1 / math.cos(math.radians(33.918))
    im = ax.imshow(np.clip(Z, -12, 4), extent=[L.DEM_W, L.DEM_E, L.DEM_S, L.DEM_N], cmap="GnBu_r", vmin=-12, vmax=4, aspect=asp)
    cs = ax.contour(lon, lat, Z, levels=[-8, -7, -6, -5, -4, -3, -2, -1, 0], colors="k", linewidths=0.6)
    ax.clabel(cs, fmt="%d m", fontsize=7)
    cs0 = ax.contour(lon, lat, Z, levels=[0], colors="red", linewidths=1.6)
    ax.set_xlim(-118.4385, -118.4265)
    ax.set_ylim(33.9105, 33.9250)
    # band rectangle (alongshore +-150 m, offshore -120..+320 m) around the hint
    corners = []
    for (x, y) in ((-L.ALONG_BAND_M, -120), (L.ALONG_BAND_M, -120), (L.ALONG_BAND_M, 320), (-L.ALONG_BAND_M, 320), (-L.ALONG_BAND_M, -120)):
        corners.append(L.canon_to_lonlat(x, y, xb))
    corners = np.array(corners)
    ax.plot(corners[:, 0], corners[:, 1], "-", color="orange", lw=2, label="sampled band: +-150 m alongshore")
    lo, la = L.canon_to_lonlat(0, 0, xb)
    ax.plot([lo], [la], "*", color="yellow", mec="k", ms=14, label="reef position hint (33.92058, -118.43335; B&N 2003 Fig. 9 window centre, +-100 m)")
    # reef outline at the hint, y measured from the waterline: shift so reef centroid y=yc from MSL waterline (mean waterline offset at the hint)
    wl_mean = float(np.mean(prof["waterline_offsets"]))
    # polygon placed so that the reef centroid sits at y = yc from the MSL waterline; hint is at s=0 where the waterline is at s=wl_mean
    pl = np.array([L.canon_to_lonlat(px, py + wl_mean, xb) for px, py in poly])
    ax.fill(pl[:, 0], pl[:, 1], color="red", alpha=0.8, label="reef outline (435 m2, shape.json) at 91 m from the MSL waterline")
    # north arrow
    ax.annotate("N", xy=(-118.4275, 33.9248), xytext=(-118.4275, 33.9225), arrowprops=dict(arrowstyle="->", lw=2), ha="center", fontsize=12)
    # 100 m scale bar
    x0 = -118.4380
    y0 = 33.9112
    ax.plot([x0, x0 + 100 / L.m_lon(33.918)], [y0, y0], "k-", lw=4)
    ax.text(x0, y0 + 0.0003, "100 m", fontsize=9)
    ax.legend(loc="upper left", fontsize=7.5)
    ax.set_title("NOAA/NGDC Santa Monica 1/3 arc-sec DEM (2010), z in m rel. MSL (z_NAVD88 - %.3f)\nred line = MSL waterline (0 m); no reef is visible in the DEM" % off, fontsize=9)
    ax.set_xlabel("longitude")
    ax.set_ylabel("latitude")
    ax.tick_params(labelsize=7)

    ax2 = fig.add_axes([0.52, 0.10, 0.46, 0.84])
    y = prof["y"]
    ax2.fill_between(y, prof["z_min"], prof["z_max"], color="0.85", label="min-max of %d alongshore stations" % prof["n"])
    ax2.fill_between(y, prof["z_mean"] - prof["z_std"], prof["z_mean"] + prof["z_std"], color="0.65", label="+-1 sd")
    ax2.plot(y, prof["z_mean"], "k-", lw=2, label="seabed used: mean profile (NOAA Santa Monica DEM)")
    ax2.plot(prof_c["y"], prof_c["z_mean"], "b--", lw=1.4, label="check: NOAA Coastal Relief Model SoCal 1 arc-sec (MSL)")
    navp = os.path.join(SRC, "navionics", "nav_transect.json")
    if os.path.exists(navp):
        nv = json.load(open(navp, encoding="utf-8"))
        yh = -float(prof["waterline_offsets"].mean())
        ax2.plot(yh + np.array(nv["profile"]["s_m"]), nv["profile"]["z_nav_msl_assumed_mllw"], "o-", color="tab:green", ms=3, lw=1,
                 label="check: Navionics SonarChart 1 ft contours (datum assumed MLLW; seabed only)")
    ax2.axvspan(ymin_p, ymax_p, color="red", alpha=0.18, label="reef y-extent %.0f-%.0f m (shape.json)" % (ymin_p, ymax_p))
    ax2.axvline(yc, color="red", lw=1)
    zc = {"A  -6 ft MSL (design, Skelly drawing; modelled alternative)": -1.829, "B  6 ft (1.83 m) below MLLW (Borrero & Nelsen 2003; ICCE: 1.8 m; as installed, Phase I; MODELLED default)": -6 * 0.3048 + ds_lev["MLLW"],
          "C  3 ft (0.91 m) below MLLW (B&N 2003: after Phase II; NOT modelled)": -3 * 0.3048 + ds_lev["MLLW"]}
    cols = {"A": "red", "B": "darkorange", "C": "purple"}
    for lab, z in zc.items():
        ax2.axhline(z, color=cols[lab[0]], ls="--", lw=1.2)
        dz = -0.30 if lab[0] == "A" else 0.10
        ax2.text(298, z + dz, "crest %s: %.2f m MSL" % (lab, z), ha="right", fontsize=7.5, color=cols[lab[0]])
    for nm in ("HAT", "MHHW", "MSL", "MLLW", "LAT"):
        ax2.axhline(ds_lev[nm], color="teal", lw=0.8, ls=":")
        ax2.text(-58, ds_lev[nm] + 0.05, "%s %+.2f m" % (nm, ds_lev[nm]), fontsize=7.5, color="teal")
    # text depth statements at the reef
    zs91 = float(np.interp(yc, y, prof["z_mean"]))
    ax2.plot([yc], [zs91], "ko", ms=7)
    ax2.annotate("DEM at %.0f m: %.2f m" % (yc, zs91), (yc, zs91), (yc + 30, zs91 + 0.55), arrowprops=dict(arrowstyle="->"), fontsize=8)
    ax2.plot([yc, yc], [-15 * 0.3048 - 0.0, -15 * 0.3048], "ms", ms=8)
    ax2.annotate("CCC 1998 text: '15 feet of water (MSL)' = -4.57 m", (yc, -4.57), (yc + 20, -5.6), arrowprops=dict(arrowstyle="->", color="m"), fontsize=8, color="m")
    ax2.plot([yc + 2], [-5.0], "g^", ms=8)
    ax2.annotate("RWR text: 'rose from about 5 m deep' (datum not stated)", (yc + 2, -5.0), (yc + 35, -6.6), arrowprops=dict(arrowstyle="->", color="g"), fontsize=8, color="g")
    ax2.set_xlim(-60, 300)
    ax2.set_ylim(-9.5, 4.5)
    ax2.set_xlabel("distance offshore of the MSL waterline, y (m)  [canonical frame, +y toward 245 deg]")
    ax2.set_ylabel("height above MSL (m)")
    ax2.set_title("Cross-shore seabed profile used (NOAA DEM), sourced depth statements, crest states A-C, tidal datums", fontsize=9)
    ax2.legend(loc="lower left", fontsize=7.5)
    ax2.grid(alpha=0.3)
    fig.text(0.04, 0.012, "How depth was estimated: for 31 alongshore stations (-150..+150 m, 10 m apart, along the shoreline bearing %.0f deg) the DEM was sampled bilinearly along +y; each profile was shifted so y = 0 at its own MSL waterline; "
             "the mean was kept (5 m steps). Source: NOAA NGDC (2010) Santa Monica CA 1/3 arc-second NAVD88 DEM, retrieved 2026-10-05; conversion z_MSL = z_NAVD88 - %.3f m (NOAA 9410840: MSL 1.594 m, NAVD88 0.802 m above station datum)." % (xb, off), fontsize=7.5, wrap=True)
    fig.savefig(os.path.join(OUT, "A7_noaa_dem_map_and_seabed_profile.png"), dpi=110)
    plt.close(fig)
    return prof, prof_c


def fig_datums():
    """A8: NOAA datum ladder (Santa Monica 9410840) in m rel. MSL and ft, with the CCC Exhibit 2 labels for comparison."""
    lev, ds = L.datum_levels_msl()
    lev_la, dsl = L.datum_levels_msl("9410660")
    fig, ax = plt.subplots(figsize=(9, 6.5))
    order = ["HAT", "MHHW", "MHW", "MSL", "MLW", "MLLW", "LAT"]
    for i, nm in enumerate(order):
        ax.hlines(lev[nm], 0, 1, color="teal", lw=2)
        ax.text(1.02, lev[nm], "%s  %+.3f m  (%+.2f ft)" % (nm, lev[nm], lev[nm] / 0.3048), va="center", fontsize=9)
        ax.hlines(lev_la[nm], 1.55, 2.0, color="gray", lw=1.5, ls="--")
    ax.text(1.57, 1.55, "LA Outer Harbor 9410660\n(dashed, same epoch)", fontsize=8, color="gray")
    ax.hlines(lev["NAVD88"], 0, 1, color="brown", lw=1.5, ls=":")
    ax.text(-0.02, lev["NAVD88"] + 0.06, "NAVD88 %+.3f m (datum of the DEM)" % lev["NAVD88"], ha="right", fontsize=8, color="brown")
    ax.hlines(-2.6 * 0 + 2.6 * 0.3048, 0, 1, color="m", lw=1, ls="-.")
    ax.text(-0.02, 2.6 * 0.3048 + 0.04, "CCC Exh. 2: MHHW +2.6 ft", ha="right", fontsize=8, color="m")
    ax.text(-0.02, -2.8 * 0.3048 - 0.1, "CCC Exh. 2: MLLW -2.8 ft", ha="right", fontsize=8, color="m")
    for lab, z, c in (("A  design -6 ft MSL (alternative)", -1.829, "red"), ("B  as installed (6 ft below MLLW, B&N 2003) - modelled", -6 * 0.3048 + lev["MLLW"], "darkorange"), ("C  after Phase II (3 ft below MLLW) - NOT modelled", -3 * 0.3048 + lev["MLLW"], "purple")):
        ax.hlines(z, 0, 1, color=c, lw=2.5, ls="--")
        ax.text(-0.02, z, "crest " + lab + "  %.2f m MSL" % z, ha="right", va="center", fontsize=8.5, color=c)
    ax.set_xlim(-3.2, 2.9)
    ax.set_ylim(-3.0, 1.8)
    ax.set_xticks([])
    ax.set_ylabel("height above MSL (m)")
    ax.set_title("Tidal datums at Santa Monica (NOAA 9410840, epoch %s) relative to MSL, with the three crest-depth readings" % ds["_epoch"], fontsize=8.5)
    ax.grid(axis="y", alpha=0.3)
    fig.text(0.01, 0.012, "z_MSL = (datum on station datum) - 1.594 m.  Source: NOAA CO-OPS API, stations/9410840/datums.json?units=metric (retrieved 2026-10-05).  "
             "Dashed = the three crest-depth readings (A: Skelly drawing, label MSL; B, C: Borrero & Nelsen 2003, 6 ft and 3 ft below MLLW, converted with MLLW = -0.849 m MSL).", fontsize=7, wrap=True)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(OUT, "A8_noaa_tidal_datums_and_crest_states.png"), dpi=110)
    plt.close(fig)


if __name__ == "__main__":
    shape = json.load(open(L.SHAPE, encoding="utf-8"))
    fig_skelly_crest_labels()
    fig_ccc_exhibit2()
    fig_ccc_exhibit3_contours()
    print("pdf highlights:", fig_pdf_highlights())
    fig_dem(shape)
    fig_datums()
    print("done")
