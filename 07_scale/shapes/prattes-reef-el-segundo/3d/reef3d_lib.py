"""reef3d_lib.py - shared helpers for build_3d.py and make_annotations.py (Pratte's Reef 3D model).

Everything here is deterministic and reads only files under 3d/src/ and ../shape.json.
Frame: canonical frame of shape.json (metres; +x alongshore toward bearing X_BEARING, +y offshore toward
bearing Y_BEARING = X_BEARING + 90 deg, i.e. +x turned 90 deg clockwise), z up, z = 0 at MSL.
"""
import json
import math
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
SHAPE = os.path.join(os.path.dirname(HERE), "shape.json")

# ---- geographic hint for WHERE to sample the DEM.
# RUN 3 (2026-10-05): centre of the survey window of Borrero & Nelsen (2003) Fig. 9 (UTM 11N 367505 E, 3754275 N), which agrees with
# the paper's 'about 200 m south of the Hyperion 1-mile outfall' (+-60 m; see METHODS_3D.md 3.10). The OLD text-derived hint (CCC 1998:
# 300 yd north of the Grand Avenue jetty) is kept for the record; it lies 217 m away.
HINT_LAT, HINT_LON = 33.92058, -118.43335
OLD_HINT_LAT, OLD_HINT_LON = 33.9188, -118.4324
ALONG_BAND_M = 150.0          # alongshore half-width of the band averaged for the seabed profile

# ---- DEM export geometry (see src/PROVENANCE_3D.md): bbox of the exported rasters, 1/3 arc-second cells
DEM_W, DEM_S, DEM_E, DEM_N = -118.445, 33.905, -118.420, 33.925
DEM_CELL = 0.000092592

M_LAT = 111132.0              # metres per degree latitude (local, ~34 N)


def m_lon(lat):
    return 111320.0 * math.cos(math.radians(lat))


def load_dem(name="noaa_santa_monica_13as_navd88_export.tif"):
    return np.array(Image.open(os.path.join(SRC, name))).astype(float)


def sample(A, lon, lat, cell=DEM_CELL):
    """bilinear sample of a north-up raster whose top-left corner is (DEM_W, DEM_N)"""
    i = (DEM_N - lat) / cell - 0.5
    j = (lon - DEM_W) / cell - 0.5
    i0, j0 = int(math.floor(i)), int(math.floor(j))
    di, dj = i - i0, j - j0
    h, w = A.shape
    if i0 < 0 or j0 < 0 or i0 + 1 >= h or j0 + 1 >= w:
        return float("nan")
    return (A[i0, j0] * (1 - di) * (1 - dj) + A[i0 + 1, j0] * di * (1 - dj)
            + A[i0, j0 + 1] * (1 - di) * dj + A[i0 + 1, j0 + 1] * di * dj)


def canon_to_lonlat(x, y, x_bearing, lon0=HINT_LON, lat0=HINT_LAT):
    """canonical-frame offset (x alongshore, y offshore) from the hint point -> lon, lat.
    +x points to bearing x_bearing, +y to x_bearing + 90 (deg clockwise from north)."""
    a = math.radians(x_bearing)
    o = math.radians(x_bearing + 90.0)
    east = x * math.sin(a) + y * math.sin(o)
    north = x * math.cos(a) + y * math.cos(o)
    return lon0 + east / m_lon(lat0), lat0 + north / M_LAT


def load_datums(station="9410840"):
    d = json.load(open(os.path.join(SRC, "noaa_%s_datums.json" % station), encoding="utf-8"))
    v = {x["name"]: x["value"] for x in d["datums"]}
    v["LAT"] = d["LAT"]
    v["HAT"] = d["HAT"]
    v["_epoch"] = d["epoch"]
    return v


def datum_levels_msl(station="9410840"):
    """tidal datums as heights above MSL (m): z = station-datum value - MSL"""
    v = load_datums(station)
    msl = v["MSL"]
    out = {k: round(v[k] - msl, 3) for k in ("HAT", "MHHW", "MHW", "MTL", "MSL", "MLW", "MLLW", "LAT", "NAVD88")}
    return out, v


def seabed_profile(x_bearing, A=None, ymin=-60.0, ymax=300.0, dy=5.0, band=ALONG_BAND_M, dx=10.0,
                   navd_to_msl=None, cell=DEM_CELL):
    """Mean cross-shore seabed profile z_MSL(y) from the NOAA 1/3 arc-sec DEM.
    For each alongshore station x in [-band, band] (step dx) the profile is sampled along +y (bearing x_bearing+90)
    from the hint point; y is then measured from that station's own MSL waterline (the most seaward z=0 crossing,
    searching y < 150 m), so beach-width variations along the shore do not smear the profile.
    Returns dict with y, mean z, std z, n stations, waterline offsets."""
    if A is None:
        A = load_dem()
    ds = datum_levels_msl()[1]
    if navd_to_msl is None:
        navd_to_msl = ds["MSL"] - ds["NAVD88"]      # z_MSL = z_NAVD88 - (MSL - NAVD88); pass 0.0 for an MSL-datum raster
    ys = np.arange(ymin, ymax + dy / 2, dy)
    prof = []
    wl = []
    xs = np.arange(-band, band + dx / 2, dx)
    for x in xs:
        s_scan = np.arange(-300.0, 500.0, 1.0)
        z = np.array([sample(A, *canon_to_lonlat(x, s, x_bearing), cell=cell) - navd_to_msl for s in s_scan])
        idx = [i for i in range(len(s_scan) - 1) if z[i] >= 0 > z[i + 1] and s_scan[i] < 150]
        if not idx:
            continue
        i = idx[-1]
        sw = s_scan[i] + (0 - z[i]) / (z[i + 1] - z[i]) * (s_scan[i + 1] - s_scan[i])
        wl.append(sw)
        prof.append(np.interp(sw + ys, s_scan, z))
    prof = np.array(prof)
    return {"y": ys, "z_mean": prof.mean(0), "z_std": prof.std(0), "z_min": prof.min(0), "z_max": prof.max(0),
            "n": len(prof), "waterline_offsets": np.array(wl), "navd_to_msl": navd_to_msl}
