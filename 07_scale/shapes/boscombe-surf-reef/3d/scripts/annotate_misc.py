"""More annotated sources for the Boscombe 3D model (private research copies):
 -> annotated/mead_fig3a_design_read.png     designers' depth plan: colour bar ticks, soundings, outline
 -> annotated/sat2011_model_frame.png        2011-09-28 satellite image with the model frame, survey extent, grid, sections
 -> annotated/datum_check_emodnet.png        chart: EMODnet cell depths vs survey seabed (ACD / ODN readings)
 -> annotated/text_*.png                     page crops of the two papers with the quoted sentences highlighted
"""
import sys, json, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from canon import CAN_POLY, SHAPE, can2px, px2can, can2osgb, O_PX
from annotate_fig9 import label, dashed_line, circled, FONT, FB, OUT
ROOT = HERE.parents[1]
SRCDIR = ROOT / "src"


# ------------------------------------------------------------------ Mead Fig 3a
def mead_fig():
    S = 1.6
    im0 = Image.open(SRCDIR / "mead_et_al_2010_fig3a_design_bathymetry.png").convert("RGB")
    arr = np.array(im0).astype(float)
    bar = arr[107:482, 835:841, :].mean(axis=1)                     # colour bar rows
    bar_val = -(np.arange(107, 482) - 107) / 51.3
    def read(px, py, r=2):
        patch = arr[int(py) - r:int(py) + r + 1, int(px) - r:int(px) + r + 1].reshape(-1, 3).mean(axis=0)
        j = ((bar - patch) ** 2).sum(axis=1).argmin()
        return float(bar_val[j])
    X0, XS, Y0, YS = 98.0, 1.9635, 40.0, 1.9635                      # model m -> px (x: px = 98 + (x-140)*s ; y: px = 40 + (560-y)*s)
    mp = lambda x, y: (X0 + (x - 140) * 1.969, Y0 + (560 - y) * 1.958)
    im = im0.resize((int(im0.width * S), int(im0.height * S)), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    P = lambda x, y: (x * S, y * S)
    f9, f11, fb = FONT(int(8.5 * S)), FONT(int(10 * S)), FB(int(10 * S))
    # colour bar ticks
    d.rectangle([P(823, 106), P(852, 482)], outline=(255, 255, 255), width=3); d.rectangle([P(823, 106), P(852, 482)], outline=(0, 0, 0), width=1)
    for k in range(8):
        y = 107 + 51.3 * k
        d.line([P(815, y), P(860, y)], fill=(0, 0, 0), width=2)
        label(d, P(862, y - 8), f"{-k} m", f11, anchor="la", bg=(255, 255, 200))
    label(d, P(852, 490), "bar y=107 px = 0 m ... y=481 px = -7.3 m (51.3 px/m)", f9, anchor="ra", bg=(255, 255, 200))
    # footprint trace from shape.json (img3)
    src3 = [s for s in SHAPE["sources"] if s["id"] == "img3"][0]
    poly = np.array(src3["pixel_polygons"][0], float)
    pts = [P(a, b) for a, b in poly]
    d.line(pts + [pts[0]], fill=(255, 0, 255), width=3)
    label(d, (pts[0][0] - 220, pts[0][1] - 110), "traced design footprint (shape.json img3, ~-2.5 m contour)", f9, fg=(255, 255, 255), bg=(160, 0, 160), anchor="la")
    # soundings
    sites = [("A crest", 330, 440), ("B crest", 345, 427), ("C seabed W", 240, 440), ("D seabed E (shoreward)", 395, 440),
             ("E seabed (y=520)", 320, 520), ("F seabed (y=365)", 320, 365)]
    res = {}
    for name, mx, my in sites:
        px, py = mp(mx, my)
        z = read(px, py)
        res[name] = z
        d.ellipse([P(px - 4, py - 4), P(px + 4, py + 4)], outline=(0, 0, 0), fill=(255, 255, 255), width=2)
        label(d, P(px + 6, py), f"{name[0]}: {z:+.1f} m", f11, anchor="lm", bg=(255, 255, 255))
    # x/y axis anchors
    for x_m in (140, 460):
        px, _ = mp(x_m, 0); dashed_line(d, P(px, 40), P(px, 510), (0, 0, 0), 2)
        label(d, P(px, 36), f"x = {x_m} m (px {px:.0f})", f9, anchor="ms", bg=(255, 255, 160))
    for y_m in (560, 320):
        _, py = mp(0, y_m); dashed_line(d, P(98, py), P(728, py), (0, 0, 0), 2)
        label(d, P(100, py - 2), f"y = {y_m} m (px {py:.0f})", f9, anchor="lb", bg=(255, 255, 160))
    strip = Image.new("RGB", (im.width, 62), (30, 30, 30)); sd = ImageDraw.Draw(strip)
    sd.text((8, 4), "ANNOTATED COPY of Mead, Blenkinsopp, Moores & Borrero (2010) ICCE, Fig. 3(a): numerical-model depth plan of the DESIGN. Private research copy.", font=FONT(15), fill=(255, 255, 255))
    sd.text((8, 24), "Marked: colour-bar ticks, axis anchors (x 140-460 m, y 320-560 m), traced footprint, soundings A-F read by nearest bar colour (+-0.2 m). Model zero is not stated (crest drawn at ~0 m).", font=FONT(15), fill=(255, 255, 160))
    sd.text((8, 44), "Text: 'The design has a crest height of 0.5 m above chart datum'; 'set in water depths of 3-5 m (CD)'. Design relief read here: crest ~0 m vs surrounding seabed -3.3 .. -5.0 m.", font=FONT(15), fill=(160, 255, 160))
    out = Image.new("RGB", (im.width, im.height + 62)); out.paste(strip, (0, 0)); out.paste(im, (0, 62))
    out.save(OUT / "mead_fig3a_design_read.png", optimize=True)
    return res


# ------------------------------------------------------------------ satellite frame
def sat_frame():
    sh = SHAPE["sources"][0]
    sat = Image.open(SRCDIR / "esri_wayback10_2011-09-28_z18_wide.png").convert("RGB")
    # survey extent (from the model grid) and shore line
    sys.path.insert(0, str(HERE.parent))
    ext = None
    try:
        txt = (HERE.parent / "model.js").read_text(encoding="utf-8")
        ext = json.loads(txt[txt.index("=") + 1:].rstrip().rstrip(";"))["survey_extent"]
    except Exception as e:                                          # model.js not built yet
        print("no model.js yet", e)
    # crop window in px around the canonical domain
    corners = np.array([[-160, 0], [160, 0], [160, 380], [-160, 380]], float)
    cp = can2px(corners)
    x0, y0 = cp.min(axis=0) - 30; x1, y1 = cp.max(axis=0) + 30
    x0, y0 = max(0, int(x0)), max(0, int(y0)); x1, y1 = min(sat.width, int(x1)), min(sat.height, int(y1))
    crop = sat.crop((x0, y0, x1, y1))
    S = 1.0 if crop.width <= 1700 else 1700.0 / crop.width
    crop = crop.resize((int(crop.width * S), int(crop.height * S)), Image.LANCZOS)
    d = ImageDraw.Draw(crop, "RGBA")
    P = lambda p: ((p[0] - x0) * S, (p[1] - y0) * S)
    f10, f12 = FONT(14), FB(15)
    # canonical grid every 50 m
    for x in range(-150, 151, 50):
        a, b = P(can2px([[x, 0]])[0]), P(can2px([[x, 380]])[0])
        d.line([a, b], fill=(255, 255, 255, 110), width=1)
        label(d, a, f"x={x}", f10, anchor="ma", bg=(255, 255, 255), pad=1)
    for y in range(0, 381, 50):
        a, b = P(can2px([[-160, y]])[0]), P(can2px([[160, y]])[0])
        d.line([a, b], fill=(255, 255, 255, 110) if y else (0, 255, 255, 255), width=1 if y else 3)
        label(d, b, f"y={y}", f10, anchor="lm", bg=(255, 255, 255), pad=1)
    label(d, P(can2px([[-150, 0]])[0]), "y = 0: surf line of 28 Sep 2011 (tide state unknown)", f12, anchor="la", bg=(0, 200, 200), fg=(0, 0, 0))
    # survey extent
    if ext:
        pts = [P(p) for p in can2px(np.array(ext))]
        d.line(pts + [pts[0]], fill=(255, 220, 0, 255), width=3)
        label(d, pts[len(pts) // 2], "area of the April 2011 depth survey (Fig. 9) in this frame", f12, anchor="la", bg=(255, 220, 0))
    # outline
    pts = [P(p) for p in can2px(CAN_POLY)]
    d.line(pts + [pts[0]], fill=(255, 0, 255, 255), width=3)
    # section lines
    for (c0, c1, nm, col) in (((0, 90), (0, 330), "section S1 (shore normal x=0)", (0, 255, 120, 255)),):
        a, b = P(can2px([c0])[0]), P(can2px([c1])[0])
        d.line([a, b], fill=col, width=3); label(d, b, nm, f12, anchor="la", bg=(0, 200, 90))
    # axis (crest profile) line: from centre along the reef axis
    # origin and axes arrows
    o = P(can2px([[0, 0]])[0]); ax = P(can2px([[40, 0]])[0]); ay = P(can2px([[0, 40]])[0])
    d.line([o, ax], fill=(255, 80, 80, 255), width=4); d.line([o, ay], fill=(80, 160, 255, 255), width=4)
    label(d, ax, "+x (bearing 83.4)", f12, anchor="la", bg=(255, 80, 80)); label(d, ay, "+y offshore (173.4)", f12, anchor="la", bg=(80, 160, 255))
    # north arrow
    nx, ny = math.cos(math.radians(83.4)), math.cos(math.radians(173.4))
    n0 = can2px([[-120, 60]])[0]; n1 = can2px([[-120 + 40 * nx, 60 + 40 * ny]])[0]
    d.line([P(n0), P(n1)], fill=(255, 255, 255, 255), width=5); label(d, P(n1), "N", FB(20), anchor="mb", bg=(0, 0, 0), fg=(255, 255, 255))
    strip = Image.new("RGB", (crop.width, 46), (30, 30, 30)); sd = ImageDraw.Draw(strip)
    sd.text((8, 4), "ANNOTATED COPY of Esri World Imagery Wayback (release 10), capture 2011-09-28 (Esri, Maxar, Earthstar Geographics). Private research copy; reuse rights not cleared.", font=FONT(15), fill=(255, 255, 255))
    sd.text((8, 24), "Marked: 3D model frame (50 m grid, origin and axes, north), traced reef outline (magenta), area of the April 2011 survey (yellow), shore-normal section S1. Scale 0.378 m/px at native size.", font=FONT(15), fill=(255, 255, 160))
    out = Image.new("RGB", (crop.width, crop.height + 46)); out.paste(strip, (0, 0)); out.paste(crop, (0, 46))
    out.save(OUT / "sat2011_model_frame.png", optimize=True)
    return out.size


# ------------------------------------------------------------------ EMODnet chart
def emodnet_chart():
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    prof = json.load(open(HERE / "_emodnet_profile.json"))
    ys = np.array([p[1] for p in prof]); zs = np.array([p[4] for p in prof])
    sys.path.insert(0, str(HERE.parent))
    txt = (HERE.parent / "model.js").read_text(encoding="utf-8")
    M = json.loads(txt[txt.index("=") + 1:].rstrip().rstrip(";"))
    sb = M["seabed"]
    Z = np.array(sb["z_cm"], float).reshape(sb["ny"], sb["nx"]) / 100.0 - M["datum"]["survey_zero_in_msl_m"]   # back to survey (ACD) datum
    i0 = int(round((0 - sb["x0"]) / sb["dx"]))
    yy = sb["y0"] + np.arange(sb["ny"]) * sb["dy"]
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.step(ys, zs, where="mid", color="k", lw=2, label="EMODnet DTM cell values (LAT datum, ~115 m cells), line x = 0")
    ax.plot(yy, Z[:, i0], color="tab:blue", lw=2, label="April 2011 survey seabed (+ model extrapolation), read as Chart Datum (default reading)")
    ax.plot(yy, Z[:, i0] + 1.40, color="tab:red", lw=2, ls="--", label="same survey read as ODN: 1.40 m higher in chart-datum / LAT terms (alternative reading)")
    ax.set_ylim(-9, 1.5); ax.set_xlim(-20, 440)
    ax.axvspan(181, 276, color="magenta", alpha=0.12, label="reef (shore-normal extent)")
    ax.axvspan(100, 305, color="gold", alpha=0.10, label="surveyed y range")
    ax.set_xlabel("distance offshore y along x = 0 (m)"); ax.set_ylabel("depth / height (m) relative to LAT or chart datum")
    ax.set_title("Boscombe: EMODnet depth cells vs the survey seabed (datum plausibility check)")
    ax.grid(alpha=.3); ax.legend(loc="lower left", fontsize=8)
    import textwrap
    fig.text(0.01, 0.005, textwrap.fill("Survey as Chart Datum: EMODnet is deeper by ~1.3-1.7 m (older / smoothed data likely). Survey as ODN: the survey would be 1.40 m shallower in LAT terms and the gap would be ~3 m. "
             "The default (chart datum) reading is therefore the closer one; EMODnet is only a coarse plausibility check.", 170), fontsize=7)
    fig.subplots_adjust(bottom=0.17)
    fig.savefig(OUT / "datum_check_emodnet.png", dpi=110); plt.close(fig)


if __name__ == "__main__":
    print(mead_fig())
    print(sat_frame())
