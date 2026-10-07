"""Step 4 (screenshots): EMODnet Map Viewer screenshots (own headless Chrome) annotated with the DTM cell grid, reef outline, points and shore-normal profile.
Usage: python make_viewer_figures.py [slug ...]      Output: viewer/<slug>_viewer_<variant>_annotated.png (+ the raw screenshot and calibration json)"""
import asyncio, json, math, os, sys
import numpy as np, pandas as pd
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
import viewer_lib as V
import extract_site as E

DATA, OUT = E.DATA, E.OUT
VIEW = os.path.join(OUT, "viewer"); os.makedirs(VIEW, exist_ok=True)
FONT = "C:/Windows/Fonts/arial.ttf"; FONTB = "C:/Windows/Fonts/arialbd.ttf"
ACCESSED = "2026-10-06"
CROP_BOTTOM = 1128          # the cookie banner (left untouched) covers the lowest ~120 px of the 1250 px window

VARIANTS = {
    "dtm": dict(layers=[14159], opacities=[50], basemap="esri-imagery", label="Mean depth, natural colour (DTM 2024, layer 14159) at 50 % over Esri World Imagery"),
    "sources": dict(layers=[13012], opacities=[55], basemap="esri-imagery", label="Source references of the DTM (layer 13012, V2024) at 55 % over Esri World Imagery"),
}
SITES = {
    "boscombe-surf-reef": dict(half_w=600, half_h=360, centre_xy=(0, 255), profile_y=(0, 500), short="Boscombe"),
    "borth-coastal-defence-reef": dict(half_w=520, half_h=330, centre_xy=(0, 300), profile_y=(0, 600), short="Borth"),
}


def font(sz, bold=False): return ImageFont.truetype(FONTB if bold else FONT, sz)


def project(cal, lat, lon):
    X, Y = V.merc(lat, lon); sx, ox, sy, oy = cal; return sx * X + ox, sy * Y + oy


def annotate(slug, variant, raw_png, cal, out_png):
    S = E.site_def(slug); fr = S["frame"]; cfg = SITES[slug]
    img = Image.open(raw_png).convert("RGBA"); W, H = img.size
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    f11, f12, f13, f15 = font(11), font(12), font(13), font(15, True)
    # --- DTM cells (grid + value)
    cells = pd.read_csv(f"{DATA}/{slug}_cells_dtm2024_erddap.csv")
    h = 0.5 / 960
    for r in cells.itertuples():
        x0, y0 = project(cal, r.latitude + h, r.longitude - h); x1, y1 = project(cal, r.latitude - h, r.longitude + h)
        if x1 < 0 or y1 < 60 or x0 > W or y0 > CROP_BOTTOM: continue
        d.rectangle([x0, y0, x1, y1], outline=(255, 255, 255, 120 if not np.isnan(r.elevation) else 50), width=1)
        if not np.isnan(r.elevation):
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            if 20 < cx < W - 80 and 80 < cy < CROP_BOTTOM - 10:
                tag = f"{r.elevation:.1f}" + ("i" if getattr(r, "interpolation_flag", 0) == 1 else "")
                d.text((cx, cy), tag, font=f12, fill=(255, 255, 255, 255), anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0, 255))
    # --- reef outline(s)
    for poly in S["shape"]["geo"]["polygons_latlon"]:
        pts = [project(cal, la, lo) for la, lo in poly]; d.line(pts + [pts[0]], fill=(255, 235, 0, 255), width=3)
    # --- shore-normal profile through the reef centre
    xp = S["centre_xy"][0]; y0p, y1p = cfg["profile_y"]
    a = project(cal, *fr.xy2ll(xp, y0p)); b = project(cal, *fr.xy2ll(xp, y1p))
    d.line([a, b], fill=(0, 255, 255, 255), width=3)
    for yy in range(y0p, y1p + 1, 100):
        p = project(cal, *fr.xy2ll(xp, yy)); d.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], fill=(0, 255, 255, 255), outline=(0, 0, 0, 255))
        d.text((p[0] - 10, p[1]), f"{yy} m", font=f12, fill=(0, 255, 255, 255), anchor="rm", stroke_width=2, stroke_fill=(0, 0, 0, 255))
    # --- named points
    P = pd.read_csv(f"{DATA}/{slug}_points_emodnet.csv"); legend = []
    for i, r in enumerate(P.itertuples(), 1):
        p = project(cal, r.lat, r.lon)
        if r.role.startswith("reef") or r.role.startswith("mound"): col = (255, 60, 60, 255)
        elif r.role in ("toe",): col = (255, 160, 0, 255)
        elif r.role in ("seabed",): col = (80, 255, 80, 255)
        else: col = (255, 120, 255, 255)
        d.ellipse([p[0] - 6, p[1] - 6, p[0] + 6, p[1] + 6], outline=col, width=2)
        d.text((p[0] + 8, p[1] - 14), str(i), font=f13, fill=col, stroke_width=2, stroke_fill=(0, 0, 0, 255))
        legend.append((i, r.point, r.role, r.elev_LAT_m, col))
    # --- legend box (bottom-left), two columns when long
    ncol = 2 if len(legend) > 12 else 1; per = math.ceil(len(legend) / ncol); lh = 16; colw = 330
    box_w = max(10 + ncol * colw, 600); box_h = lh * (per + 2) + 14
    d.rectangle([8, CROP_BOTTOM - box_h - 8, 8 + box_w, CROP_BOTTOM - 8], fill=(0, 0, 0, 185))
    yb = CROP_BOTTOM - box_h - 2
    d.text((16, yb), "points = EMODnet DTM 2024 cell mean, m rel. LAT (white numbers on the map = cell mean; i = interpolated cell)", font=f11, fill=(255, 255, 255, 255))
    for k, (i, nme, role, v, col) in enumerate(legend):
        c_, r_ = divmod(k, per)
        d.text((16 + c_ * colw, yb + lh * (r_ + 1)), f"{i:>2}  {nme}  [{role.split(' (')[0]}]  {v:.2f} m", font=f11, fill=col)
    d.text((16, yb + lh * (per + 1)), "yellow = reef outline (project shape.json)   cyan = shore-normal profile (m offshore of the frame origin)", font=f11, fill=(255, 255, 255, 255))
    title = [f"EMODnet Map Viewer (https://emodnet.ec.europa.eu/geoviewer/), accessed {ACCESSED} - {VARIANTS[variant]['label']}",
             "Annotations added by this project: white cell grid = EMODnet DTM cells (1/16 arc-min), numbers = depth m rel. LAT (negative = below LAT).",
             "(c) EMODnet Bathymetry Consortium (2024) EMODnet Digital Bathymetry (DTM 2024), DOI 10.12770/cf51df64-56f9-4a99-b1aa-36b8d7b743a1, CC BY 4.0; basemap (c) Esri, Maxar, Earthstar Geographics. Private research copy. Not for navigation."]
    d.rectangle([8, 66, 1330, 66 + 18 * len(title) + 6], fill=(0, 0, 0, 175))
    for k, t in enumerate(title): d.text((14, 70 + 18 * k), t, font=f12, fill=(255, 255, 255, 255))
    # scale bar 100 m
    f = 1 / math.cos(math.radians(S["centre_ll"][0])); sx = cal[0]; L = 100 * f * sx
    x0b, y0b = W - 160 - L - 20, CROP_BOTTOM - 40
    d.rectangle([x0b - 8, y0b - 22, x0b + L + 8, y0b + 12], fill=(0, 0, 0, 175)); d.line([(x0b, y0b), (x0b + L, y0b)], fill=(255, 255, 255, 255), width=3)
    d.text((x0b, y0b - 16), "100 m", font=f12, fill=(255, 255, 255, 255))
    d.text((x0b + L + 30, y0b - 8), "N up", font=f13, fill=(255, 255, 255, 255), anchor="lm", stroke_width=2, stroke_fill=(0, 0, 0, 255))
    out = Image.alpha_composite(img, ov).convert("RGB").crop((0, 0, W, CROP_BOTTOM)); out.save(out_png, optimize=True)
    return out.size


async def main(slugs):
    for slug in slugs:
        S = E.site_def(slug); cfg = SITES[slug]; fr = S["frame"]
        lat_c, lon_c = fr.xy2ll(*cfg["centre_xy"])
        for variant, v in VARIANTS.items():
            raw = f"{VIEW}/{slug}_viewer_{variant}_raw.png"
            if os.environ.get("ANNOTATE_ONLY") and os.path.exists(raw):
                info = json.load(open(f"{VIEW}/{slug}_viewer_{variant}_calibration.json"))
                print("  annotated", annotate(slug, variant, raw, info["cal"], f"{VIEW}/{slug}_viewer_{variant}_annotated.png")); continue
            info = await V.capture(f"{cfg['short']}_{variant}", lat_c, lon_c, cfg["half_w"], cfg["half_h"], v["layers"], v["basemap"], v["opacities"], raw)
            json.dump(info, open(f"{VIEW}/{slug}_viewer_{variant}_calibration.json", "w"), indent=1)
            print(slug, variant, "calibration residual px", info["spread"], "scale px/m", info["cal"][0])
            print("  annotated", annotate(slug, variant, raw, info["cal"], f"{VIEW}/{slug}_viewer_{variant}_annotated.png"))


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:] or list(SITES)))
