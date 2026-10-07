#!/usr/bin/env python3
"""
satellite.py - fetch Esri World Imagery (current or Wayback-archived) satellite tiles
for one reef site, stitched + cropped to a PNG with a .geo.json sidecar.
07_scale/tools/ (see 07_scale/tools/README.md for worked examples).

Subcommands:
    fetch         --lat LAT --lon LON --radius-m R --zoom Z --out PNG [--wayback RELEASE]
    wayback-list  [--near-date YYYY-MM-DD]
    pix2ll        --geo PNG.geo.json --x X --y Y
    ll2pix        --geo PNG.geo.json --lat LAT --lon LON

Tile sources:
    current : https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}
    wayback : https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/{release}/{z}/{y}/{x}
    wayback release list (id -> dated release): https://s3-us-west-2.amazonaws.com/config.maptiles.arcgis.com/waybackconfig.json

Capture date: queried from the Esri World_Imagery MapServer's "identify" operation (current
imagery), or from the matching Wayback release's own metadata layer (--wayback case). If no
date attribute comes back, the sidecar records "unknown" -- this is common for the low-res
fallback layer and for some remote areas.
"""
import argparse
import json
import math
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

import requests
from PIL import Image

TILE_SIZE = 256
CURRENT_TEMPLATE = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
WAYBACK_TEMPLATE = ("https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/"
                     "WMTS/1.0.0/default028mm/MapServer/tile/{release}/{z}/{y}/{x}")
WAYBACK_CONFIG_URL = "https://s3-us-west-2.amazonaws.com/config.maptiles.arcgis.com/waybackconfig.json"
IDENTIFY_URL = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/identify"
ATTRIBUTION = "Esri, Maxar, Earthstar Geographics, and the GIS User Community"
USER_AGENT = "artificial-reef-research/1.0 (private research use)"

_session = requests.Session()
_session.headers.update({"User-Agent": USER_AGENT})


# --------------------------------------------------------------------------- #
# Web Mercator / slippy-tile math
# --------------------------------------------------------------------------- #

def deg2num_frac(lat, lon, zoom):
    """lat/lon -> fractional (world-pixel-x, world-pixel-y) at this zoom, standard
    Web Mercator slippy-map convention (0,0 = top-left of the world, 256*2^zoom px square)."""
    n = 2 ** zoom
    world_px = TILE_SIZE * n
    x = (lon + 180.0) / 360.0 * world_px
    lat_rad = math.radians(lat)
    y = (1.0 - math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi) / 2.0 * world_px
    return x, y


def num2deg(px, py, zoom):
    """Inverse of deg2num_frac: world pixel coords at this zoom -> lat/lon."""
    n = 2 ** zoom
    world_px = TILE_SIZE * n
    lon = px / world_px * 360.0 - 180.0
    y_frac = 1.0 - 2.0 * py / world_px
    lat = math.degrees(math.atan(math.sinh(math.pi * y_frac)))
    return lat, lon


def ground_resolution_m_per_px(lat, zoom):
    """Standard Esri/Google Web Mercator ground resolution formula at a given latitude
    and zoom: metres per pixel on the ground at the image centre."""
    return 156543.03392804097 * math.cos(math.radians(lat)) / (2 ** zoom)


# Mercator-meters helpers for the .geo.json bounds-based pix2ll / ll2pix (these do not
# need the zoom or tile grid at all -- just the stored north/south/east/west bounds).
_EARTH_R = 6378137.0


def _merc_x(lon):
    return math.radians(lon) * _EARTH_R


def _merc_y(lat):
    return _EARTH_R * math.log(math.tan(math.pi / 4.0 + math.radians(lat) / 2.0))


def _inv_merc_x(x):
    return math.degrees(x / _EARTH_R)


def _inv_merc_y(y):
    return math.degrees(2.0 * math.atan(math.exp(y / _EARTH_R)) - math.pi / 2.0)


# --------------------------------------------------------------------------- #
# tile download
# --------------------------------------------------------------------------- #

def _fetch_tile(template, z, y, x, retries=3, backoff=1.5):
    url = template.format(z=z, y=y, x=x)
    last_exc = None
    for attempt in range(retries):
        try:
            r = _session.get(url, timeout=30)
            if r.status_code == 200 and r.content:
                return Image.open(__import__("io").BytesIO(r.content)).convert("RGB")
            last_exc = RuntimeError(f"HTTP {r.status_code} for {url}")
        except Exception as e:  # noqa: BLE001 - want to retry on anything transient
            last_exc = e
        time.sleep(backoff * (attempt + 1))
    raise RuntimeError(f"failed to fetch tile {z}/{y}/{x} from {template}: {last_exc}")


# --------------------------------------------------------------------------- #
# wayback release list
# --------------------------------------------------------------------------- #

def get_wayback_releases():
    """Returns list of dicts: {release, date, title, metadata_layer_url}, sorted newest first."""
    r = _session.get(WAYBACK_CONFIG_URL, timeout=30)
    r.raise_for_status()
    cfg = r.json()
    out = []
    for release_id, entry in cfg.items():
        title = entry.get("itemTitle", "")
        # itemTitle looks like "World Imagery (Wayback 2026-08-05)"
        date_str = None
        if "(" in title and ")" in title:
            inner = title[title.rfind("(") + 1: title.rfind(")")]
            date_str = inner.replace("Wayback", "").strip()
        out.append({
            "release": release_id,
            "date": date_str,
            "title": title,
            "metadata_layer_url": entry.get("metadataLayerUrl"),
        })
    out.sort(key=lambda e: e["date"] or "", reverse=True)
    return out


# --------------------------------------------------------------------------- #
# capture-date lookup
# --------------------------------------------------------------------------- #

def _parse_identify_date(payload):
    """Pull the best capture-date attribute out of an ArcGIS identify response."""
    try:
        results = payload.get("results", [])
    except AttributeError:
        return None, None
    # Prefer layerId 0 ("World Imagery", the actual high-res layer shown at close zoom).
    results = sorted(results, key=lambda r: r.get("layerId", 99))
    for res in results:
        attrs = res.get("attributes", {})
        for key in ("DATE (YYYYMMDD)", "DATE"):
            val = attrs.get(key)
            if val and str(val).lower() != "null":
                v = str(val)
                if v.isdigit() and len(v) == 8:
                    return f"{v[0:4]}-{v[4:6]}-{v[6:8]}", key
                return v, key
        val = attrs.get("SRC_DATE2")
        if val and str(val).lower() != "null":
            # MM/DD/YYYY -> YYYY-MM-DD
            try:
                m, d, y = val.split("/")
                return f"{y}-{int(m):02d}-{int(d):02d}", "SRC_DATE2"
            except Exception:  # noqa: BLE001
                return val, "SRC_DATE2"
    return None, None


def lookup_capture_date(lat, lon, identify_url, zoom):
    """Query an ArcGIS MapServer's identify operation at (lat, lon). Returns
    (date_str_or_None, source_field_or_None)."""
    half = 0.01  # degrees, generous map extent box around the point
    params = {
        "geometry": f"{lon},{lat}",
        "geometryType": "esriGeometryPoint",
        "sr": 4326,
        "layers": "visible",
        "tolerance": 2,
        "mapExtent": f"{lon - half},{lat - half},{lon + half},{lat + half}",
        "imageDisplay": "600,600,96",
        "returnGeometry": False,
        "f": "json",
    }
    try:
        r = _session.get(identify_url, params=params, timeout=30)
        r.raise_for_status()
        return _parse_identify_date(r.json())
    except Exception:  # noqa: BLE001 - capture date is best-effort
        return None, None


# --------------------------------------------------------------------------- #
# fetch
# --------------------------------------------------------------------------- #

def fetch(lat, lon, radius_m, zoom, out_path, wayback=None):
    out_path = Path(out_path)
    n = 2 ** zoom

    if wayback:
        template = WAYBACK_TEMPLATE.replace("{release}", str(wayback))
        template_record = WAYBACK_TEMPLATE
    else:
        template = CURRENT_TEMPLATE
        template_record = CURRENT_TEMPLATE

    center_x, center_y = deg2num_frac(lat, lon, zoom)
    mpp = ground_resolution_m_per_px(lat, zoom)
    pixel_radius = radius_m / mpp

    left = center_x - pixel_radius
    right = center_x + pixel_radius
    top = center_y - pixel_radius
    bottom = center_y + pixel_radius

    tx_min = max(0, int(math.floor(left / TILE_SIZE)))
    tx_max = min(n - 1, int(math.floor((right - 1e-6) / TILE_SIZE)))
    ty_min = max(0, int(math.floor(top / TILE_SIZE)))
    ty_max = min(n - 1, int(math.floor((bottom - 1e-6) / TILE_SIZE)))

    n_tiles = (tx_max - tx_min + 1) * (ty_max - ty_min + 1)
    if n_tiles > 400:
        raise ValueError(f"radius/zoom combination needs {n_tiles} tiles (>400) - reduce radius or zoom")

    canvas = Image.new("RGB", ((tx_max - tx_min + 1) * TILE_SIZE, (ty_max - ty_min + 1) * TILE_SIZE))
    for ty in range(ty_min, ty_max + 1):
        for tx in range(tx_min, tx_max + 1):
            tile = _fetch_tile(template, zoom, ty, tx)
            canvas.paste(tile, ((tx - tx_min) * TILE_SIZE, (ty - ty_min) * TILE_SIZE))

    origin_x = tx_min * TILE_SIZE
    origin_y = ty_min * TILE_SIZE
    crop_box = (
        int(round(left - origin_x)),
        int(round(top - origin_y)),
        int(round(right - origin_x)),
        int(round(bottom - origin_y)),
    )
    final = canvas.crop(crop_box)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    final.save(out_path)

    # exact bounds of the FINAL crop, in lat/lon (so the sidecar matches the saved pixels)
    final_left_world = origin_x + crop_box[0]
    final_top_world = origin_y + crop_box[1]
    final_right_world = origin_x + crop_box[2]
    final_bottom_world = origin_y + crop_box[3]
    north, west = num2deg(final_left_world, final_top_world, zoom)
    south, east = num2deg(final_right_world, final_bottom_world, zoom)

    # capture date: for a Wayback release, ask that release's own metadata layer;
    # for current imagery, ask the main MapServer.
    capture_date, date_field = None, None
    identify_url = IDENTIFY_URL
    if wayback:
        try:
            releases = get_wayback_releases()
            match = next((r for r in releases if r["release"] == str(wayback)), None)
            if match and match.get("metadata_layer_url"):
                identify_url = match["metadata_layer_url"] + "/identify"
        except Exception:  # noqa: BLE001
            pass
    capture_date, date_field = lookup_capture_date(lat, lon, identify_url, zoom)

    geo = {
        "image": out_path.name,
        "width": final.width,
        "height": final.height,
        "bounds": {"north": north, "south": south, "east": east, "west": west},
        "zoom": zoom,
        "m_per_px_center": mpp,
        "tile_template": template_record,
        "wayback_release": str(wayback) if wayback else None,
        "center": {"lat": lat, "lon": lon},
        "radius_m": radius_m,
        "attribution": ATTRIBUTION,
        "retrieved": date.today().isoformat(),
        "capture_date": capture_date or "unknown",
        "capture_date_field": date_field,
    }
    geo_path = out_path.with_suffix(out_path.suffix + ".geo.json")
    geo_path.write_text(json.dumps(geo, indent=2), encoding="utf-8")
    return geo


# --------------------------------------------------------------------------- #
# pix2ll / ll2pix (use only the .geo.json bounds; no network needed)
# --------------------------------------------------------------------------- #

def pix2ll(geo, x, y):
    b = geo["bounds"]
    w, h = geo["width"], geo["height"]
    x_west, x_east = _merc_x(b["west"]), _merc_x(b["east"])
    y_north, y_south = _merc_y(b["north"]), _merc_y(b["south"])
    fx = x / w
    fy = y / h
    mx = x_west + fx * (x_east - x_west)
    my = y_north + fy * (y_south - y_north)
    return _inv_merc_y(my), _inv_merc_x(mx)  # lat, lon


def ll2pix(geo, lat, lon):
    b = geo["bounds"]
    w, h = geo["width"], geo["height"]
    x_west, x_east = _merc_x(b["west"]), _merc_x(b["east"])
    y_north, y_south = _merc_y(b["north"]), _merc_y(b["south"])
    mx, my = _merc_x(lon), _merc_y(lat)
    fx = (mx - x_west) / (x_east - x_west)
    fy = (my - y_north) / (y_south - y_north)
    return fx * w, fy * h  # x_px, y_px


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main():
    ap = argparse.ArgumentParser(prog="satellite.py", description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("fetch", help="stitch tiles around a lat/lon into a PNG + .geo.json")
    p.add_argument("--lat", required=True, type=float)
    p.add_argument("--lon", required=True, type=float)
    p.add_argument("--radius-m", required=True, type=float)
    p.add_argument("--zoom", required=True, type=int)
    p.add_argument("--out", required=True)
    p.add_argument("--wayback", default=None, help="Wayback release id (see wayback-list)")

    sub.add_parser("wayback-list", help="print available Wayback releases (id + date)")

    p = sub.add_parser("pix2ll", help="pixel coords -> lat/lon using a .geo.json")
    p.add_argument("--geo", required=True)
    p.add_argument("--x", required=True, type=float)
    p.add_argument("--y", required=True, type=float)

    p = sub.add_parser("ll2pix", help="lat/lon -> pixel coords using a .geo.json")
    p.add_argument("--geo", required=True)
    p.add_argument("--lat", required=True, type=float)
    p.add_argument("--lon", required=True, type=float)

    args = ap.parse_args()

    if args.cmd == "fetch":
        geo = fetch(args.lat, args.lon, args.radius_m, args.zoom, args.out, args.wayback)
        print(json.dumps(geo, indent=2))

    elif args.cmd == "wayback-list":
        for r in get_wayback_releases():
            print(f"{r['release']:>8}  {r['date'] or '?':<12}  {r['title']}")

    elif args.cmd == "pix2ll":
        geo = json.loads(Path(args.geo).read_text(encoding="utf-8"))
        lat, lon = pix2ll(geo, args.x, args.y)
        print(json.dumps({"lat": lat, "lon": lon}, indent=2))

    elif args.cmd == "ll2pix":
        geo = json.loads(Path(args.geo).read_text(encoding="utf-8"))
        x, y = ll2pix(geo, args.lat, args.lon)
        print(json.dumps({"x": x, "y": y}, indent=2))

    else:
        ap.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
