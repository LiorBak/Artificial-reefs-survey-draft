"""Coordinate helpers for the Boscombe 3D model (run from any folder).

Canonical frame of shape.json: metres, +x alongshore (bearing 83.4 deg), +y offshore (bearing 173.4 deg),
origin = pixel (1509.7, 747.8) of the Esri Wayback 2011-09-28 image (img1).
m = M @ (p_px - O_PX),  M fitted to the 25 traced vertices (max residual 0.006 m).
"""
import json, math
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # .../shapes/boscombe-surf-reef
SHAPE = json.load(open(ROOT / "shape.json", encoding="utf-8"))
GEO1 = json.load(open(ROOT / "src" / "esri_wayback10_2011-09-28_z18_wide.png.geo.json", encoding="utf-8"))
O_PX = np.array(SHAPE["canonical"]["origin_px_img1"], float)
IMG1_PX = np.array(SHAPE["sources"][0]["pixel_polygons"][0], float)
CAN_POLY = np.array(SHAPE["canonical"]["polygons_m"][0], float)
# fit M
_P = IMG1_PX - O_PX
_A, *_ = np.linalg.lstsq(_P, CAN_POLY, rcond=None)
M = _A.T                      # 2x2, m = M @ (p - O)
Minv = np.linalg.inv(M)

R = 6378137.0
def _merc(lat, lon):
    x = R * math.radians(lon)
    y = R * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
    return x, y
_b = GEO1["bounds"]
_x0, _y1 = _merc(_b["north"], _b["west"])
_x1, _y0 = _merc(_b["south"], _b["east"])
_W, _H = GEO1["width"], GEO1["height"]

def ll2px(lat, lon):
    x, y = _merc(lat, lon)
    return (x - _x0) / (_x1 - _x0) * _W, (_y1 - y) / (_y1 - _y0) * _H

def px2ll(px, py):
    x = _x0 + px / _W * (_x1 - _x0)
    y = _y1 - py / _H * (_y1 - _y0)
    lon = math.degrees(x / R)
    lat = math.degrees(2 * math.atan(math.exp(y / R)) - math.pi / 2)
    return lat, lon

def px2can(p):
    p = np.asarray(p, float)
    return (p - O_PX) @ M.T

def can2px(m):
    m = np.asarray(m, float)
    return m @ Minv.T + O_PX

try:
    from pyproj import Transformer
    _t = Transformer.from_crs("EPSG:27700", "EPSG:4326", always_xy=True)
    _tinv = Transformer.from_crs("EPSG:4326", "EPSG:27700", always_xy=True)
except Exception:
    _t = _tinv = None

def osgb2can(E, N):
    """OSGB36 (E,N) -> canonical metres, via lat/lon and the img1 pixel grid (Helmert datum shift, ~+-5 m)."""
    E = np.asarray(E, float); N = np.asarray(N, float)
    lon, lat = _t.transform(E, N)
    out = np.zeros(E.shape + (2,))
    flat_lat = np.ravel(lat); flat_lon = np.ravel(lon)
    pts = np.array([ll2px(a, b) for a, b in zip(flat_lat, flat_lon)])
    can = px2can(pts)
    return can.reshape(E.shape + (2,))

def can2osgb(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    px = can2px(np.stack([np.ravel(x), np.ravel(y)], axis=-1))
    ll = np.array([px2ll(a, b) for a, b in px])
    E, N = _tinv.transform(ll[:, 1], ll[:, 0])
    return np.reshape(E, x.shape), np.reshape(N, x.shape)

if __name__ == "__main__":
    print("M =", M, " rot deg", math.degrees(math.atan2(M[1, 0], M[0, 0])), "scale", math.sqrt(abs(np.linalg.det(M))))
    print("resid max", np.abs(px2can(IMG1_PX) - CAN_POLY).max())
    c = CAN_POLY.mean(0)
    print("poly centroid-ish", c, can2osgb(*c))
    print("osgb round trip", osgb2can(*can2osgb(10.0, 220.0)))
