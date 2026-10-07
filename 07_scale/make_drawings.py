#!/usr/bin/env python3
"""make_drawings.py -- documentation copies of the Scale-tab drawings.

Renders, for each of the 13 verified footprints (07_scale/reefs/<slug>.footprint.json):
  drawings/<slug>.svg  (+ .png)   one reef in plan, 1 px = 1 m, same rules as the page's Scale view
and for all of them together:
  drawings/overlay.svg (+ .png)            all reefs on one frame, true distance offshore, shared shoreline,
                                           centred alongshore on each centroid, football pitch for reference
  drawings/overlay_centroid.svg (+ .png)   the same, every centroid on one point
  drawings/sheet.svg (+ .png)              all 13 plan drawings side by side on one shared shoreline and one
                                           100 m scale bar (the layout of Lior's reference graphic, with our
                                           schematic outlines instead of aerial photos)

Geometry: this is a line-by-line port of 04_build/src/scale.js (panelFrame / panelSVG / overlaySVG);
area, bbox and centroid come from the SAME function the page compiler uses
(04_build/src/compile_data.py: geometry_of). Keep the two in step if either changes.

PNG: cairosvg if it can load the cairo library; otherwise headless Chrome/Edge (as used by
04_build/src/qa_shots.py); otherwise SVG only.

Run:  python "07_scale/make_drawings.py"
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "drawings"
sys.path.insert(0, str(ROOT / "04_build" / "src"))
import compile_data as cd  # noqa: E402  (same geometry + verdict code path as the page)

# --- constants: identical to scale.js -------------------------------------------------------
PITCH_L, PITCH_W = 105, 68                      # FIFA recommendation, Wikipedia "Football pitch"
G = dict(ML=16, MR=16, MT=30, BEACH=24, MB=34, PAD_M=15, MIN_HALF_M=75, BAR_M=100)
PALETTE = ['#4e79a7', '#e15759', '#59a14f', '#f28e2b', '#b07aa1', '#9c755f', '#ff9da7',
           '#76b7b2', '#edc948', '#bab0ac', '#1f9fd4', '#d37295', '#8cd17d']
# light-theme values of the page's CSS tokens
C = dict(sea="#e6f1f7", sand="#efe3c4", shore="#7a6a45", line="#1b1f24", dim="#3d5a73",
         text="#1b1f24", muted="#5a626d", surface="#ffffff")
VERDICT_FILL = {"worked": "#1e7a46", "partly worked": "#9fd6a8", "mixed": "#c98a12", "failed": "#9b1c1c", "n-a": "#e4e5e8"}
FONT = "Inter, Segoe UI, Arial, sans-serif"


def fmt(n, d=None):
    if d is None:
        d = 1 if abs(n) < 10 else 0
    s = f"{n:,.{d}f}"
    return s.rstrip("0").rstrip(".") if "." in s else s


def load():
    reefs = []
    for slug in cd.SLUGS:
        fp = json.loads((HERE / "reefs" / f"{slug}.footprint.json").read_text(encoding="utf-8"))
        card = json.loads((ROOT / "02_research" / "reefs" / f"{slug}.json").read_text(encoding="utf-8"))
        polys = fp.get("polygons_m") or [fp["polygon_m"]]
        reefs.append(dict(slug=slug, name=card.get("name") or fp.get("name"), verdict=cd.normalize_verdict(card.get("verdict")),
                          polys=polys, geom=cd.geometry_of(polys), area=fp.get("area_m2"), bbox_m=fp.get("bbox_m") or {},
                          confidence=cd.confidence_level(fp.get("confidence"))))
    order = sorted(reefs, key=lambda r: -r["area"])
    for i, r in enumerate(order):
        r["color"] = PALETTE[i % len(PALETTE)]
    return reefs


# --- one panel (port of scale.js panelFrame + panelSVG) --------------------------------------
def panel_frame(r, s):
    b = r["geom"]["bbox"]
    cx = (b["minx"] + b["maxx"]) / 2
    half = max((b["maxx"] - b["minx"]) / 2 + G["PAD_M"], G["MIN_HALF_M"])
    top = max(b["maxy"], 0) + G["PAD_M"]
    W = G["ML"] + 2 * half * s + G["MR"]
    H = G["MT"] + top * s + G["BEACH"] + G["MB"]
    return dict(W=round(W), H=round(H), top=top,
                tx=lambda x: G["ML"] + (x - (cx - half)) * s,
                ty=lambda y: G["MT"] + (top - y) * s)


def ring_path(ring, tx, ty):
    return "".join(("L" if i else "M") + f"{tx(p[0]):.1f} {ty(p[1]):.1f}" for i, p in enumerate(ring)) + "Z"


def panel_body(r, s, fr):
    """SVG elements of one panel (without the <svg> wrapper), in the frame fr."""
    tx, ty, W, H = fr["tx"], fr["ty"], fr["W"], fr["H"]
    y0, o = ty(0), []
    o.append(f'<rect x="0" y="0" width="{W}" height="{y0:.1f}" fill="{C["sea"]}"/>')
    o.append(f'<rect x="0" y="{y0:.1f}" width="{W}" height="{G["BEACH"]}" fill="{C["sand"]}"/>')
    o.append(f'<line x1="0" x2="{W}" y1="{y0:.1f}" y2="{y0:.1f}" stroke="{C["shore"]}" stroke-width="1.5"/>')
    o.append(f'<text x="{W - G["MR"]}" y="{y0 + 15:.1f}" text-anchor="end" fill="{C["muted"]}">beach · shoreline (y = 0)</text>')
    a_len = max(10, min(36, y0 - G["MT"] + 6))
    o.append(f'<line x1="{G["ML"] + 4}" x2="{G["ML"] + 4}" y1="{y0 - 4:.1f}" y2="{y0 - 4 - a_len:.1f}" stroke="{C["dim"]}" stroke-width="1.5"/>'
             f'<path d="M{G["ML"]} {y0 - a_len:.1f}l4 -7l4 7z" fill="{C["dim"]}"/>')
    o.append(f'<text x="{G["ML"]}" y="{G["MT"] - 12}" fill="{C["muted"]}">↑ offshore (sea)</text>')
    fill = VERDICT_FILL.get(r["verdict"], VERDICT_FILL["n-a"])
    o.append(f'<g fill="{fill}" fill-opacity=".9" stroke="{C["line"]}" stroke-width="1" stroke-linejoin="round">' +
             "".join(f'<path d="{ring_path(rg, tx, ty)}"/>' for rg in r["polys"]) + "</g>")
    np_ = min((p for rg in r["polys"] for p in rg), key=lambda p: p[1])
    if np_[1] * s >= 10:
        x = tx(np_[0])
        o.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{y0:.1f}" y2="{ty(np_[1]):.1f}" stroke="{C["dim"]}" stroke-dasharray="3 3"/>'
                 f'<text x="{x + 4:.1f}" y="{(y0 + ty(np_[1])) / 2 + 4:.1f}" fill="{C["text"]}">{fmt(np_[1], 0)} m</text>')
    bl, bx1 = G["BAR_M"] * s, W - G["MR"]
    bx0, by = bx1 - bl, H - 12
    o.append(f'<rect x="{bx0:.1f}" y="{by - 5}" width="{bl / 2:.1f}" height="5" fill="{C["text"]}"/>'
             f'<rect x="{bx0 + bl / 2:.1f}" y="{by - 5}" width="{bl / 2:.1f}" height="5" fill="{C["surface"]}" stroke="{C["text"]}" stroke-width=".8"/>'
             f'<text x="{bx0:.1f}" y="{by - 9}" fill="{C["text"]}">0</text><text x="{bx1}" y="{by - 9}" text-anchor="end" fill="{C["text"]}">100 m</text>')
    o.append(f'<text x="{G["ML"]}" y="{H - 7}" fill="{C["muted"]}">1 px = {fmt(1 / s, 3)} m</text>')
    return o


def caption(r):
    b = r["bbox_m"]
    return (f'{fmt(b.get("length_alongshore") or 0)} × {fmt(b.get("width_crossshore") or 0)} m · '
            f'{fmt(r["area"])} m² · {r["confidence"]} confidence')


def svg_doc(W, H, body, font_size=11):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'font-family="{FONT}" font-size="{font_size}">\n<rect width="100%" height="100%" fill="{C["surface"]}"/>\n' + "\n".join(body) + "\n</svg>\n")


TITLE_H = 40


def panel_svg(r, s=1.0):
    """Documentation copy of one panel: a 40 px title band (the page shows the title in HTML)
    above exactly the page's drawing. Returns (W, H, body)."""
    fr = panel_frame(r, s)
    W = max(fr["W"], 300)
    body = [f'<text x="8" y="16" font-weight="600" font-size="13" fill="{C["text"]}">{escape(r["name"])}</text>',
            f'<text x="8" y="32" fill="{C["muted"]}">{escape(caption(r))}</text>',
            f'<g transform="translate(0,{TITLE_H})">'] + panel_body(r, s, fr) + ["</g>"]
    return W, fr["H"] + TITLE_H, body


# --- overlay (port of scale.js overlaySVG) ---------------------------------------------------
def nice_bar(span):
    best = 5
    for x in (5, 10, 20, 25, 50, 100, 200, 250, 500, 1000):
        if x <= span / 5:
            best = x
    return best


def overlay_svg(reefs, align="shore", pitch=True, px_width=1400):
    def off(r):
        c = r["geom"]["centroid"]
        return (-c[0], -c[1]) if align == "centroid" else (-c[0], 0)
    mins = [float("inf"), float("-inf"), float("inf"), float("-inf")]

    def ext(x0, x1, y0, y1):
        mins[0], mins[1], mins[2], mins[3] = min(mins[0], x0), max(mins[1], x1), min(mins[2], y0), max(mins[3], y1)
    for r in reefs:
        b, d = r["geom"]["bbox"], off(r)
        ext(b["minx"] + d[0], b["maxx"] + d[0], b["miny"] + d[1], b["maxy"] + d[1])
    pitch_y = 0 if align == "centroid" else PITCH_W / 2 + 6
    if pitch:
        ext(-PITCH_L / 2, PITCH_L / 2, pitch_y - PITCH_W / 2, pitch_y + PITCH_W / 2)
    if align == "shore":
        ext(mins[0], mins[1], 0, mins[3])
    minx, maxx, miny, maxy = mins
    w0, h0 = maxx - minx, maxy - miny
    half = max(w0, h0 * 1.25, 120) / 2 * 1.12
    cx = (minx + maxx) / 2
    fw = 2 * half
    fh = max(h0 * 1.14, fw * 0.62)
    fy1 = maxy + (fh - h0) * 0.6
    fy0 = fy1 - fh
    beach = max(fh * 0.07, 6) if align == "shore" else 0
    if align == "shore":
        fy0 = min(fy0, -beach)
    fh = fy1 - fy0
    X = lambda x: x - (cx - half)  # noqa: E731
    Y = lambda y: fy1 - y          # noqa: E731
    fs = fw / 55
    nss = 'vector-effect="non-scaling-stroke"'
    o = []
    if align == "shore":
        o.append(f'<rect x="0" y="0" width="{fw:.2f}" height="{Y(0):.2f}" fill="{C["sea"]}"/>')
        o.append(f'<rect x="0" y="{Y(0):.2f}" width="{fw:.2f}" height="{fh - Y(0):.2f}" fill="{C["sand"]}"/>')
        o.append(f'<line {nss} x1="0" x2="{fw:.2f}" y1="{Y(0):.2f}" y2="{Y(0):.2f}" stroke="{C["shore"]}" stroke-width="1.5"/>')
        o.append(f'<text x="{fs:.2f}" y="{Y(0) + fs * 1.3:.2f}" fill="{C["muted"]}">shared shoreline (y = 0) · beach</text>')
        o.append(f'<text x="{fs:.2f}" y="{fs * 1.4:.2f}" fill="{C["muted"]}">↑ offshore · each reef at its drawn distance from the shore, centred alongshore</text>')
    else:
        o.append(f'<rect x="0" y="0" width="{fw:.2f}" height="{fh:.2f}" fill="{C["sea"]}"/>')
        o.append(f'<line {nss} x1="{X(0):.2f}" x2="{X(0):.2f}" y1="0" y2="{fh:.2f}" stroke="{C["muted"]}" stroke-dasharray="4 4" opacity=".6"/>'
                 f'<line {nss} x1="0" x2="{fw:.2f}" y1="{Y(0):.2f}" y2="{Y(0):.2f}" stroke="{C["muted"]}" stroke-dasharray="4 4" opacity=".6"/>')
        o.append(f'<text x="{fs:.2f}" y="{fs * 1.4:.2f}" fill="{C["muted"]}">↑ offshore · all centroids on one point (shoreline not shown)</text>')
    if pitch:
        o.append(f'<g fill="none" stroke="{C["text"]}" stroke-width="1.2" stroke-dasharray="6 4" opacity=".75">'
                 f'<rect {nss} x="{X(-PITCH_L / 2):.2f}" y="{Y(pitch_y + PITCH_W / 2):.2f}" width="{PITCH_L}" height="{PITCH_W}"/>'
                 f'<line {nss} x1="{X(0):.2f}" x2="{X(0):.2f}" y1="{Y(pitch_y + PITCH_W / 2):.2f}" y2="{Y(pitch_y - PITCH_W / 2):.2f}"/></g>'
                 f'<text x="{X(-PITCH_L / 2 + 2):.2f}" y="{Y(pitch_y + PITCH_W / 2) - fs * 0.4:.2f}" fill="{C["text"]}">football pitch 105 × 68 m</text>')
    for r in sorted(reefs, key=lambda r: -r["area"]):
        d = off(r)
        paths = "".join('<path {} d="{}Z"/>'.format(nss, "".join(("L" if i else "M") + f"{X(p[0] + d[0]):.2f} {Y(p[1] + d[1]):.2f}" for i, p in enumerate(rg))) for rg in r["polys"])
        o.append(f'<g fill="{r["color"]}" fill-opacity=".28" stroke="{r["color"]}" stroke-width="1.6"><title>{escape(r["name"])}</title>{paths}</g>')
    bar = nice_bar(fw)
    bx1 = fw - fs
    bx0, by = bx1 - bar, fh - fs * 0.8
    o.append(f'<rect x="{bx0:.2f}" y="{by - fs * 0.45:.2f}" width="{bar / 2:.2f}" height="{fs * 0.45:.2f}" fill="{C["text"]}"/>'
             f'<rect x="{bx0 + bar / 2:.2f}" y="{by - fs * 0.45:.2f}" width="{bar / 2:.2f}" height="{fs * 0.45:.2f}" fill="{C["surface"]}" stroke="{C["text"]}" stroke-width=".8" {nss}/>'
             f'<text x="{bx0:.2f}" y="{by - fs * 0.7:.2f}" fill="{C["text"]}">0</text>'
             f'<text x="{bx1:.2f}" y="{by - fs * 0.7:.2f}" text-anchor="end" fill="{C["text"]}">{bar} m</text>')
    # legend (documentation copy only; on the page it is an HTML list with toggles)
    k = px_width / fw
    leg_w = 440
    W, H = round(px_width + leg_w), round(max(fh * k, 26 * len(reefs) + 40))
    legend = [f'<text x="{px_width + 14}" y="24" font-weight="600" fill="{C["text"]}">Reefs (area)</text>']
    for i, r in enumerate(sorted(reefs, key=lambda r: -r["area"])):
        y = 44 + 26 * i
        legend.append(f'<rect x="{px_width + 14}" y="{y - 11}" width="14" height="14" rx="3" fill="{r["color"]}"/>'
                      f'<text x="{px_width + 36}" y="{y}" fill="{C["text"]}">{escape(r["name"][:38])} · {fmt(r["area"])} m²</text>')
    body = [f'<svg x="0" y="0" width="{px_width}" height="{fh * k:.1f}" viewBox="0 0 {fw:.2f} {fh:.2f}" font-size="{fs:.2f}">'] + o + ["</svg>"] + legend
    return W, H, body


# --- sheet: every panel side by side on one shared shoreline (image26-style layout) ------------
def sheet_svg(reefs, s=1.0):
    frames = [(r, panel_frame(r, s)) for r in sorted(reefs, key=lambda r: -r["area"])]
    top_max = max(fr["top"] for _, fr in frames)
    gap, x, parts = 10, 10, []
    base = G["MT"] + top_max * s + G["BEACH"] + G["MB"] + 20     # bottom of every panel
    H = round(base + 44)
    for r, fr in frames:
        dy = (top_max - fr["top"]) * s + 20          # align every shoreline on one line
        parts.append(f'<g transform="translate({x},{dy:.1f})">' + "".join(panel_body(r, s, fr)) + "</g>")
        parts.append(f'<text x="{x + 4}" y="{base + 16:.0f}" font-weight="600" fill="{C["text"]}">{escape(r["name"][:34])}</text>'
                     f'<text x="{x + 4}" y="{base + 32:.0f}" fill="{C["muted"]}">{escape(caption(r))}</text>')
        x += max(fr["W"], 200) + gap
    W = x
    parts.append(f'<text x="10" y="14" fill="{C["muted"]}">All 13 verified footprints, 1 px = {fmt(1 / s, 3)} m, shorelines aligned; '
                 f'every panel carries its own 100 m bar. Schematic outlines, not surveys: see 07_scale/reefs/&lt;slug&gt;.md.</text>')
    return W, H, parts


# --- PNG ------------------------------------------------------------------------------------------
def chrome():
    for c in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"):
        if Path(c).exists():
            return c
    return shutil.which("chrome") or shutil.which("msedge")


def to_png(svg_path: Path, W: int, H: int, how: dict):
    png = svg_path.with_suffix(".png")
    if how.get("cairo") is not False:
        try:
            import cairosvg  # noqa: PLC0415
            cairosvg.svg2png(url=str(svg_path), write_to=str(png))
            how["cairo"] = True
            return "cairosvg"
        except Exception:  # noqa: BLE001  (no cairo DLL on this machine)
            how["cairo"] = False
    exe = chrome()
    if not exe:
        return "svg only"
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as prof:
        subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                        f"--user-data-dir={prof}", f"--window-size={W},{H}", f"--screenshot={png}",
                        svg_path.as_uri()], capture_output=True, timeout=90)
    return "headless Chrome" if png.exists() and png.stat().st_size > 1000 else "svg only (png failed)"


def main():
    OUT.mkdir(exist_ok=True)
    reefs = load()
    how, log = {}, []
    for r in reefs:
        W, H, body = panel_svg(r, 1.0)
        p = OUT / f"{r['slug']}.svg"
        p.write_text(svg_doc(W, H, body), encoding="utf-8")
        log.append((p.name, W, H, to_png(p, W, H, how)))
    for name, align in (("overlay", "shore"), ("overlay_centroid", "centroid")):
        W, H, body = overlay_svg(reefs, align=align)
        p = OUT / f"{name}.svg"
        p.write_text(svg_doc(W, H, body, font_size=14), encoding="utf-8")
        log.append((p.name, W, H, to_png(p, W, H, how)))
    W, H, body = sheet_svg(reefs, 1.0)
    p = OUT / "sheet.svg"
    p.write_text(svg_doc(W, H, body), encoding="utf-8")
    log.append((p.name, W, H, to_png(p, W, H, how)))
    for row in log:
        print(f"{row[0]:<48} {row[1]:>5} x {row[2]:<5} png: {row[3]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
