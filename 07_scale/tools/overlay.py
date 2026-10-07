#!/usr/bin/env python3
"""
overlay.py - draw traced polygons on top of a satellite/photo image for visual QA.
07_scale/tools/ (see 07_scale/tools/README.md for worked examples).

Subcommands:
    render  --image IMG --polys POLYS --out PNG [--grid N] [--labels] [--alpha 0.35]
            Semi-transparent fill + outline + numbered vertices for one set of polygons.
            --grid N draws a labelled pixel grid every N px (helps read coordinates).
            --labels numbers each vertex (0,1,2,...) next to the point; default on.

    zoom    --image IMG --box x0 y0 x1 y1 --scale K --grid N --out PNG
            Crop [x0,y0,x1,y1] (original pixel coords), enlarge by K, and draw grid
            lines + tick labels in ORIGINAL pixel coordinates, so an agent can read
            precise coordinates by eye off the enlarged image.

    compare --image IMG --polys A --polys2 B --out PNG
            Draw two polygon sets in two colours (A=red, B=cyan) on the same image,
            for comparing e.g. our trace vs. Gemini's footprint.

POLYS argument: a path to a JSON file, or a literal JSON string, holding a list of
polygons, each a list of [x, y] pixel points, e.g. [[[100,120],[180,120],[180,200]]].
"""
import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FILL_A = (255, 60, 60)
OUTLINE_A = (255, 0, 0)
FILL_B = (60, 220, 220)
OUTLINE_B = (0, 180, 180)
GRID_COLOR = (255, 255, 0)
GRID_TEXT_BG = (0, 0, 0)


def _font(size=14):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:  # noqa: BLE001
        return ImageFont.load_default()


def _load_polys(arg):
    p = Path(arg)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return json.loads(arg)


def _draw_polygon(base, draw, poly, fill_rgb, outline_rgb, alpha, labels, font):
    if len(poly) >= 2:
        fill_rgba = (*fill_rgb, int(255 * alpha))
        overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)
        pts = [tuple(pt) for pt in poly]
        if len(poly) >= 3:
            odraw.polygon(pts, fill=fill_rgba, outline=None)
        odraw.line(pts + [pts[0]], fill=(*outline_rgb, 255), width=2)
        base.alpha_composite(overlay)
        draw = ImageDraw.Draw(base)
    for i, (x, y) in enumerate(poly):
        r = 4
        draw.ellipse([x - r, y - r, x + r, y + r], fill=outline_rgb, outline=(255, 255, 255))
        if labels:
            draw.text((x + 6, y - 6), str(i), fill=(255, 255, 255), font=font,
                       stroke_width=2, stroke_fill=(0, 0, 0))


def _draw_grid(base, draw, step, font):
    w, h = base.size
    for x in range(0, w, step):
        draw.line([(x, 0), (x, h)], fill=GRID_COLOR, width=1)
        draw.text((x + 2, 2), str(x), fill=GRID_COLOR, font=font,
                   stroke_width=1, stroke_fill=GRID_TEXT_BG)
    for y in range(0, h, step):
        draw.line([(0, y), (w, y)], fill=GRID_COLOR, width=1)
        draw.text((2, y + 2), str(y), fill=GRID_COLOR, font=font,
                   stroke_width=1, stroke_fill=GRID_TEXT_BG)


def render(image_path, polys, out_path, grid=None, labels=True, alpha=0.35):
    img = Image.open(image_path).convert("RGBA")
    font = _font()
    for poly in polys:
        _draw_polygon(img, None, poly, FILL_A, OUTLINE_A, alpha, labels, font)
    draw = ImageDraw.Draw(img)
    if grid:
        _draw_grid(img, draw, grid, font)
    img.convert("RGB").save(out_path)


def zoom(image_path, box, scale, out_path, grid=None):
    img = Image.open(image_path).convert("RGB")
    x0, y0, x1, y1 = box
    crop = img.crop((x0, y0, x1, y1))
    new_size = (int(crop.width * scale), int(crop.height * scale))
    big = crop.resize(new_size, Image.LANCZOS).convert("RGBA")
    draw = ImageDraw.Draw(big)
    font = _font(max(10, int(12 * min(scale, 2))))
    if grid:
        # grid lines at multiples of `grid` in ORIGINAL coords; labels show original coords.
        first_x = x0 - (x0 % grid)
        gx = first_x
        while gx <= x1:
            if gx >= x0:
                bx = (gx - x0) * scale
                draw.line([(bx, 0), (bx, big.height)], fill=GRID_COLOR, width=1)
                draw.text((bx + 2, 2), str(gx), fill=GRID_COLOR, font=font,
                          stroke_width=1, stroke_fill=GRID_TEXT_BG)
            gx += grid
        first_y = y0 - (y0 % grid)
        gy = first_y
        while gy <= y1:
            if gy >= y0:
                by = (gy - y0) * scale
                draw.line([(0, by), (big.width, by)], fill=GRID_COLOR, width=1)
                draw.text((2, by + 2), str(gy), fill=GRID_COLOR, font=font,
                          stroke_width=1, stroke_fill=GRID_TEXT_BG)
            gy += grid
    big.convert("RGB").save(out_path)


def compare(image_path, polys_a, polys_b, out_path, alpha=0.30):
    img = Image.open(image_path).convert("RGBA")
    font = _font()
    for poly in polys_a:
        _draw_polygon(img, None, poly, FILL_A, OUTLINE_A, alpha, True, font)
    for poly in polys_b:
        _draw_polygon(img, None, poly, FILL_B, OUTLINE_B, alpha, True, font)
    img.convert("RGB").save(out_path)


def main():
    ap = argparse.ArgumentParser(prog="overlay.py", description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("render", help="draw one polygon set on an image")
    p.add_argument("--image", required=True)
    p.add_argument("--polys", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--grid", type=int, default=None)
    p.add_argument("--labels", action="store_true", default=True)
    p.add_argument("--no-labels", dest="labels", action="store_false")
    p.add_argument("--alpha", type=float, default=0.35)

    p = sub.add_parser("zoom", help="crop + enlarge a region with a labelled grid")
    p.add_argument("--image", required=True)
    p.add_argument("--box", required=True, nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1"))
    p.add_argument("--scale", required=True, type=float)
    p.add_argument("--grid", type=int, default=20)
    p.add_argument("--out", required=True)

    p = sub.add_parser("compare", help="draw two polygon sets in two colours")
    p.add_argument("--image", required=True)
    p.add_argument("--polys", required=True, help="set A (red)")
    p.add_argument("--polys2", required=True, help="set B (cyan)")
    p.add_argument("--out", required=True)
    p.add_argument("--alpha", type=float, default=0.30)

    args = ap.parse_args()

    if args.cmd == "render":
        polys = _load_polys(args.polys)
        render(args.image, polys, args.out, args.grid, args.labels, args.alpha)
        print(json.dumps({"ok": True, "out": args.out}))

    elif args.cmd == "zoom":
        zoom(args.image, args.box, args.scale, args.out, args.grid)
        print(json.dumps({"ok": True, "out": args.out}))

    elif args.cmd == "compare":
        a = _load_polys(args.polys)
        b = _load_polys(args.polys2)
        compare(args.image, a, b, args.out, args.alpha if hasattr(args, "alpha") else 0.30)
        print(json.dumps({"ok": True, "out": args.out}))

    else:
        ap.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
