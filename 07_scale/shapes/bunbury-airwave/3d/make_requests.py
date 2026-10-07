"""make_requests.py - writes REQUESTS_FOR_LIOR.md (called by build_3d.py): what could not be read, as tables for the Navionics app / Google Earth Pro,
with exact decimal lat/lon (WGS84) computed from the model frame, and the values the model predicts at each point so that Lior can compare."""
import math
import os

import numpy as np
from pyproj import Transformer


def model_to_latlon(frame, bx_true, by_true, conv, x, y):
    """model (x alongshore, y seaward) -> (lat, lon); frame['origin_mga50'] = MGA94 zone 50 (E, N) of the origin"""
    bgx, bgy = math.radians(bx_true - conv), math.radians(by_true - conv)
    E = frame["origin_mga50"][0] + x * math.sin(bgx) + y * math.sin(bgy)
    N = frame["origin_mga50"][1] + x * math.cos(bgx) + y * math.cos(bgy)
    lon, lat = Transformer.from_crs(28350, 4326, always_xy=True).transform(E, N)
    return lat, lon


def write(path, frame, sm, zb_ahd, nav_d_of_y, lat_ahd, comp):
    bx, by, conv = sm["bearings"]["x_true"], sm["bearings"]["y_true"], sm["bearings"]["conv"]
    ll = lambda x, y: model_to_latlon(frame, bx, by, conv, x, y)
    site = frame["site_point_latlon"]
    chk = ll(0.0, frame["site_point_offset_from_origin_m"][1])
    err = math.hypot((chk[0] - site[0]) * 111000, (chk[1] - site[1]) * 111000 * math.cos(math.radians(site[0])))
    assert err < 3.0, "model->lat/lon check failed: %.1f m from the site point" % err

    def pt(x, y):
        a, b = ll(x, y)
        return "%.5f, %.5f" % (a, b)

    def below_lat(y):
        return lat_ahd - zb_ahd(y)

    rows = []
    for tag, x, y, what in (("B1", 0, 0.0, "the model's y = 0 line (2009 0 m AHD contour)"), ("B2", 0, 12.0, "where Navionics draws its 0 m contour (green/blue edge)"),
                            ("B3", 0, 30.0, "near edge of the 30-50 m text range"), ("B4", 0, 37.9, "the site point = the model default reef centre (y 37.5 m)"),
                            ("B5", 0, 45.0, "far edge of the RWR range"), ("B6", 0, 50.0, "SurferToday distance; where the text-implied seabed is reached for H = 2.0 m"),
                            ("B7", 0, 60.0, "just seaward of the reef zone"), ("B8", 0, 100.0, "offshore, where the slope is well defined"),
                            ("B9", -60, 45.0, "alongshore check (hypothetical reef centre 60 m south)"), ("B10", 60, 45.0, "alongshore check (60 m north)")):
        zl = below_lat(y)
        exp_l = ("%.1f m (lidar 2009)" % zl) if zl > 0.1 else ("about %.1f m ABOVE LAT = drying (lidar 2009)" % (-zl))
        nav_s = "" if y < 12 else "; %.1f m (my Navionics contour reading)" % nav_d_of_y(y)
        rows.append("| %s | Navionics app | %s | depth at the point (tap it; SonarChart layer on) | %s%s | metres (say if the app is set to feet); whether the app says the depth is 'chart datum' or 'tide corrected'; time of day | %s |" % (
            tag, pt(x, y), exp_l, nav_s, what))
    b_tbl = "\n".join(rows)
    olat, olon = ll(0.0, 0.0)
    md = """# REQUESTS FOR LIOR - Bunbury Airwave (Bunbury Back Beach, WA), 3D model (2026-10-05)

What the model already has: tide planes (GHD 2021, checked against the DoT survey index), seabed (WA DoT 2009 airborne lidar, **checked against the Garmin Navionics SonarChart contours I counted myself from the web viewer**, RMS %(rms)s m once depths are read below LAT), plan outline (verified circle, 12 m), reef height and crest depth (text). The bladder was removed in December 2019, so Navionics shows no structure and was used for the seabed only.
What I could NOT read, and could not find anywhere online, is listed here. The model is already built with stated assumptions; each row says what it would change. **Neither tool can show the structure itself except Google Earth historical imagery, and only if an image from 9-20 December 2019 exists (the nearest imagery I found at the site is 2016 and 2025).**

All coordinates are decimal degrees, WGS84 (lat, lon). They are computed from the model frame (origin %(olat).5f, %(olon).5f = the 2009 0 m AHD contour; +x = %(bx).1f deg true alongshore, +y = %(by).1f deg true seaward). Points are on the model's alongshore line x = 0 through the site point unless stated; a depth reading at them is a valid seabed reading whatever the true reef position is.

## A. Where exactly was the bladder? (largest geometric unknown: +-100 m alongshore, +-10 m offshore)

| # | tool | exact lat/lon or place | what to read | datum / units to note | why it matters for the model |
|---|---|---|---|---|---|
| A1 | Google Earth Pro, historical imagery slider | Bunbury Back Beach, centred on %(site)s, 30-50 m seaward of the waterline, just south of the Bunbury SLSC building (-33.3271, 115.6298) | the date of every image from Dec 2019 to Jan 2020 (the bladder sat in the water about 9-16 Dec 2019 and was removed within about three days); if one shows the pale circle, drop a placemark on its centre and copy the lat/lon, note the image date and whether the tide looks low | WGS84 decimal degrees; image date (day) | fixes the position (now a text/satellite estimate, +-100 m alongshore, +-10 m offshore = +-0.4 m of seabed depth) |
| A2 | Google Earth Pro, ruler (path) | from the A1 placemark (or, if no image shows it, from %(site)s) to the water's edge in the SAME image, along the shore normal (bearing about 282 deg true) | distance in metres and the bearing the ruler shows | metres; image date and whether the sand is wet/dry at the edge | the distance offshore (text 30-45 m / 45 m from the low-tide mark / 50 m; each 10 m moves the seabed depth by 0.4 m) |
| A3 | Google Earth Pro, ruler | from the SLSC building corner (-33.3271, 115.6298) to the A1 placemark | distance (m) and compass direction | metres; degrees true | confirms "just to the south of Bunbury surf club" (Tracks 2019) and the model's alongshore position |
| A4 | Google Earth Pro, historical imagery | the point %(olat).5f, %(olon).5f (the model's 2009 0 m AHD contour) | in the imagery nearest 2009-2010 and in the 2025 image: ruler distance from this point to the water's edge along bearing 282 deg; the image date and tide state | metres; sign (+ seaward) | shows whether the 2009 shoreline (which defines y = 0 for every distance in the model) has moved (2025 Esri waterline is about 7 m from the 2009 contour at the site) |

## B. Seabed depth (cross-check of the 2009 lidar and of my contour counting)

Navionics app (phone/tablet, SonarChart layer ON, "Sonar Logging" and "Community Edits" as you normally have them; set depth units to metres and say so). Tap the point and read the depth label; if the app shows a date/time and a tide-correction note, copy it. The "expected" cell gives the 2009 lidar value and, where I have one, my contour reading from the Navionics web viewer (both as depth below LAT, in metres); if the app is on a different datum the difference tells us which.

| # | tool | exact lat/lon | what to read | expected (model) | datum / units to note | why it matters |
|---|---|---|---|---|---|---|
%(btbl)s
| B11 | Navionics app | anywhere on this stretch, same hour as the readings | the app's tide-station name and the predicted tide height at the time of reading (Settings > Tides & currents), and any statement of the chart datum | LAT is my inferred datum (RMS test, METHODS_3D.md 3.6) | m above chart datum | settles whether the app depths are tide corrected and which datum they use (MLLW would be 0.4 m shallower than LAT) |

## C. As-installed shape (not found anywhere)

| # | tool | place | what to read | datum / units | why |
|---|---|---|---|---|---|
| C1 | e-mail to Waveco (Troy Bottegal) / the City of Bunbury (Dec 2019 council papers) | the installation record: dive log, photographs with a scale, as-installed height and which flank was steep | the as-installed height (1.6 m or 2.0 m?), a cross-section, the fill level when the seam tore, the orientation of the "skateboard ramp" | metres; MLLW / LAT / AHD | the model draws a symmetric cap; this is the largest remaining unknown in the reef surface |
| C2 | e-mail to Raised Water Research (they published the drone photo and the Dec 2019 tear photos) | the original, un-cropped drone frame(s) or video with metadata | the date/time, altitude and any scale object | - | gives the plan scale independent of the 12 m text value |
| C3 | WA Department of Transport (bathymetry) | a survey of Back Beach after 2009 (the index lists only 2009 lidar at the open coast) | whether a newer grid exists | AHD or LAT | replaces the 10-year-old seabed |

## D. Not needed from you
Tide planes (GHD 2021 table, cross-checked with the DoT index), the lidar, the card dates (December 2019, not 2018): done. No Haifa / Israel tide preset (local tides only).
""" % {"rms": comp["nav_rms_lat"], "olat": olat, "olon": olon, "bx": bx, "by": by, "site": "%.4f, %.4f" % tuple(site), "btbl": b_tbl}
    open(path, "w", encoding="utf-8").write(md)
    return {"site_check_error_m": round(err, 2)}
