#!/usr/bin/env python3
"""extract_profiles.py - cross-shore depth profiles of the surf-reef 3D models, for the review paper (08_paper).

Run:   python3 08_paper/analysis/extract_profiles.py [--plots /tmp/some_dir] [--only <slug>]
Reads: 07_scale/shapes/<slug>/3d/model.js (READ ONLY) for the nine reefs that have a 3D model; default version only.
Writes: 08_paper/data/profiles/<slug>.json, _no_3d_model.json and SUMMARY.md.
Needs: numpy, scipy, shapely (Prattes polygon distance), matplotlib (optional, --plots).

Frame of every model: x alongshore, y offshore (away from the model shoreline y = 0), z up, z = 0 at MSL.
Each reef's frame, datum and shoreline definition are recorded in its JSON (read from the model's own metadata and from
build_3d.py / index.html). Reef-surface rules that the viewers evaluate at run time (Prattes, Bunbury, Mount Maunganui,
Albany) are re-implemented in the adapters below, line by line from the viewer / build code (cited in each JSON, "method").
Every number written is DERIVED from the model data; assumptions are named in the JSON.
Primary cut ('crest_line') = constant model x through the shallowest crest cell, except where CUT_OVERRIDES (Lior's
review 2026-10-19) sets a surf cut through the surfed part of the reef, perpendicular to the shoreline (Albany, Cables, Borth).
Sections of this file: (1) per-reef adapters, (2) profile/metric core, (3) main (driver, summary, non-3D records).
"""

import base64
import json
import math
import os

import numpy as np
from scipy import ndimage as ndi

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SHAPES = os.path.join(REPO, '07_scale', 'shapes')


def load_model(slug):
    p = os.path.join(SHAPES, slug, '3d', 'model.js')
    t = open(p, encoding='utf-8').read()
    i = t.index('window.REEF_MODEL')
    j = t.index('=', i) + 1
    s = t[j:].strip()
    if s.endswith(';'):
        s = s[:-1]
    return json.loads(s), p


def b64_i16(s, ny, nx):
    a = np.frombuffer(base64.b64decode(s), dtype='<i2').reshape(ny, nx).astype(float)
    a[a == -32768] = np.nan
    return a / 100.0


def b64_u8(s, ny, nx):
    return np.frombuffer(base64.b64decode(s), dtype=np.uint8).reshape(ny, nx)


class GridFn:
    """Bilinear interpolation on a regular grid Z[j, i] (j along y, i along x); NaN outside the grid."""

    def __init__(self, x0, y0, dx, dy, Z):
        self.x0, self.y0, self.dx, self.dy = float(x0), float(y0), float(dx), float(dy)
        self.Z = np.asarray(Z, float)
        self.ny, self.nx = self.Z.shape

    def __call__(self, x, y):
        x = np.asarray(x, float)
        y = np.asarray(y, float)
        x, y = np.broadcast_arrays(x, y)
        fx = (x - self.x0) / self.dx
        fy = (y - self.y0) / self.dy
        out = ndi.map_coordinates(self.Z, [fy.ravel(), fx.ravel()], order=1, mode='nearest').reshape(x.shape)
        bad = (fx < -1e-9) | (fx > self.nx - 1 + 1e-9) | (fy < -1e-9) | (fy > self.ny - 1 + 1e-9)
        return np.where(bad, np.nan, out)

    @property
    def x_range(self):
        return (self.x0, self.x0 + (self.nx - 1) * self.dx)

    @property
    def y_range(self):
        return (self.y0, self.y0 + (self.ny - 1) * self.dy)


def rows_grid(sb):
    """model.js seabed {x0,y0,step|dx,z:[rows of y][cols of x]} -> GridFn"""
    dx = sb.get('step', sb.get('dx'))
    dy = sb.get('step', sb.get('dy', dx))
    return GridFn(sb['x0'], sb['y0'], dx, dy, np.array(sb['z'], float))


def flat_grid(sb, key='z_cm', dx_key='dx'):
    nx, ny = sb['nx'], sb['ny']
    Z = np.array(sb[key], float).reshape(ny, nx) / 100.0
    return GridFn(sb['x0'], sb['y0'], sb[dx_key], sb.get('dy', sb[dx_key]), Z)


def ax(x0, step, n):
    return x0 + step * np.arange(n)


# ---------------------------------------------------------------------------------------------------------- Borth
def borth(m, mp):
    ver = next(v for v in m['versions'] if v['id'] == m['default_version'])
    g = ver['grid']
    RZ = b64_i16(g['h_cm_b64'], g['ny'], g['nx'])
    Zn = b64_u8(g['zone_b64'], g['ny'], g['nx'])
    sb = rows_grid(m['seabed'])
    return dict(
        seabed=sb, rx=ax(g['x0'], g['step'], g['nx']), ry=ax(g['y0'], g['step'], g['ny']), RZ=RZ, zone=Zn,
        mask=lambda X, Y: X < 30.0,
        secondary=dict(name='southern oval = shore-parallel breakwater (crest +1.50 mODN, NOT a surf reef)', mask=lambda X, Y: X >= 30.0),
        meta=dict(
            version_id=ver['id'], version_name=ver['name'], version_date=ver['date'],
            datum='z = metres above MSL; MSL = +0.31 mODN (+-0.15, estimate); z_MSL = z_ODN - 0.31 (model.js datum.equation)',
            frame='x alongshore (+ toward SOUTH, bearing 179.57 deg T); y offshore (+ toward WEST, bearing 269.57 deg T); origin = foot of the perpendicular from the centroid of both mounds on the defence line',
            shoreline_def='y = 0 is the DEFENCE LINE (back of the shingle beach, z about +4.9 m MSL), NOT the MSL waterline. The MSL waterline is where the modelled natural seabed crosses z = 0 (computed per line, key y_msl_crossing_m).',
            reef_surface_def='model.js versions[lidar_2022].grid.h_cm_b64 (int16 cm, z_MSL, 1 m cells, rows = y, cols = x): 1 m LiDAR DSM (Welsh Government, flown 19 Mar 2022, lightly smoothed) inside the exposed-rock outline, plus the Royal Haskoning toe berm / blanket slopes (drawings 9V5090/1021-1023) down to the modelled seabed. Zones: 1 armour, 2 toe berm, 3 blanket/apron.',
            seabed_def='model.js seabed (5 m grid, z_MSL): thin-plate/RBF fit to the Royal Haskoning drawing nodes + Fig. 2 contours (build_3d.py seabed_grid).',
            source_files=['07_scale/shapes/borth-coastal-defence-reef/3d/model.js', '07_scale/shapes/borth-coastal-defence-reef/3d/build_3d.py (lines 62-130)', '07_scale/shapes/borth-coastal-defence-reef/3d/METHODS_3D.md'],
            caveats=['The 1 m LiDAR DSM sees block tops, about 0.1-0.3 m above the design surface (model.js versions[0].note).',
                     'The default 3D confidence is MEDIUM; bed under the reef is interpolated from design drawings, Fig. 2 contours and checked against Navionics (datum +-0.6 m).',
                     'The model has TWO structures: northern boot-shaped surf reef (crest +0.50 mODN) and southern oval shore-parallel breakwater (crest +1.50 mODN) which is NOT a surf reef. Reef metrics below are for the whole footprint incl. both unless a mask is given; the surf reef is the northern one (x < 0).'],
            region_masks={'surf_reef_north': 'x < 0 (model.js roles.north centroid x = -38.9)', 'breakwater_south': 'x > 0 (roles.south centroid x = 85.3)'},
        ))


# -------------------------------------------------------------------------------------------------------- Boscombe
def boscombe(m, mp):
    sb = m['seabed']
    Zsb = np.array(sb['z_cm'], float).reshape(sb['ny'], sb['nx']) / 100.0
    seabed = GridFn(sb['x0'], sb['y0'], sb['dx'], sb['dy'], Zsb)
    code = np.frombuffer(sb['code'].encode(), dtype=np.uint8).reshape(sb['ny'], sb['nx']) - 48
    rg = m['reef']['grid']
    nodata = rg['nodata']
    Z = np.array(rg['idealised_z_cm'], float).reshape(rg['ny'], rg['nx'])
    Z[Z == nodata] = np.nan
    Z /= 100.0
    surveyed = np.array(rg['surveyed_z_cm'], float).reshape(rg['ny'], rg['nx'])
    surveyed[surveyed == nodata] = np.nan
    surveyed /= 100.0
    return dict(
        seabed=seabed, rx=ax(rg['x0'], rg['dx'], rg['nx']), ry=ax(rg['y0'], rg['dy'], rg['ny']), RZ=Z,
        seabed_code=GridFn(sb['x0'], sb['y0'], sb['dx'], sb['dy'], code.astype(float)),
        extra_layers=[dict(name='surveyed_surface_2011-04', RZ=surveyed, note='April 2011 DGPS surface (Rendle and Davidson 2012 Fig. 9, colour read; reef.grid.surveyed_z_cm) AFTER the container failure (March-April 2011); evidence layer, not the default; datum assumption as for the default (ACD, MSL = ACD + 1.40 m)')],
        meta=dict(
            version_id='idealised', version_name='AS-BUILT 2009 (intact): idealised loft of the verified outline, design crest +0.5 m ACD', version_date='2009 (Sept-Oct 2009 completion)',
            datum='z = metres above MSL; model assumes the survey zero is Admiralty Chart Datum (ACD) with MSL = ACD + 1.40 m (Ordnance Datum - 1.40 m at Bournemouth, NTSLF), so z_MSL = z_ACD - 1.40; the alternative reading (survey zero = ODN) shifts survey heights by +1.40 m',
            frame='x alongshore (true bearing 83.4 deg, toward the east; Boscombe Pier at negative x); y offshore (true bearing 173.4 deg); origin on the 2011-09-28 surf line nearest the reef centroid',
            shoreline_def='y = 0 is the surf line visible in the 2011-09-28 Esri image (tide state unknown); it lies about 8 m SEAWARD of the modelled MSL waterline (z = -0.2 m at the line) (model.js shoreline.note). The MSL crossing is computed per line (y_msl_crossing_m).',
            reef_surface_def='model.js reef.grid.idealised_z_cm (1 m cells, z_MSL): relief = clip(1 + phi/3.0, 0, crest - seabed), phi = signed distance from the verified outline (m, + inside), crest = design +0.5 m ACD = -0.9 m MSL (flat), outline on the 1 m relief contour (reef.idealised_rule). The viewer re-applies the same cap; with datumShift = 0 (default) the stored grid is what is drawn.',
            seabed_def='model.js seabed.z_cm (2 m grid, z_MSL): April 2011 DGPS plot colour read (Rendle and Davidson 2012 Fig. 9) in the survey area; thin-plate-spline infill under the reef; CCO beach profiles (2010-04-20) landward; EMODnet-slope extrapolation y > 380 m (seabed_source_code: 0 survey, 1 extrapolated, 2 interpolated under reef, 3 CCO beach, 4 CCO-survey blend, 5 EMODnet slope).',
            source_files=['07_scale/shapes/boscombe-surf-reef/3d/model.js', '07_scale/shapes/boscombe-surf-reef/3d/index.html (lines 195-262)', '07_scale/shapes/boscombe-surf-reef/3d/build_3d.py (lines 105-135, 405-410)'],
            caveats=['The default reef surface is an idealised flat-crest loft (crest level = design value +0.5 m ACD), not a survey: the real Oct 2009 profile tops were +0.05..+0.65 m ACD (model.js provenance).',
                     'Slope of the loft flanks (1:3) is an assumption (SLOPE_RUN_PER_RISE = 3.0, source S2); real flanks of the April 2011 DGPS surface have median gradient 0.172 (about 1:5.8) (stats.flank_gradient_median_survey).',
                     'Survey datum is assumed to be chart datum (ACD) - not stated in the source; a +1.4 m alternative exists.'],
        ))


# --------------------------------------------------------------------------------------------------------- Bunbury
def bunbury(m, mp):
    sb = m['seabed']
    seabed = GridFn(sb['x0'], sb['y0'], sb['dx'], sb['dy'], np.array(sb['z'], float))
    R = m['reef']
    cx, cy = R['centre_default']
    H = R['height_default_m']
    poly = np.array(R['toe_polygon_m'], float)
    # radial function of the traced polygon about its own centre (index.html RAD_R: ray/segment intersection)
    NR = 720
    rad = np.full(NR, np.nan)
    for mm in range(NR):
        th = 2 * math.pi * mm / NR
        dxr, dyr = math.cos(th), math.sin(th)
        best = np.inf
        for k in range(len(poly)):
            a, b = poly[k], poly[(k + 1) % len(poly)]
            ex, ey = b[0] - a[0], b[1] - a[1]
            den = dxr * ey - dyr * ex
            if abs(den) < 1e-12:
                continue
            t = (a[0] * ey - a[1] * ex) / den
            u = (a[0] * dyr - a[1] * dxr) / den
            if t > 0 and 0 <= u <= 1 and t < best:
                best = t
        rad[mm] = best
    step = 0.25
    rx = np.arange(cx - 8, cx + 8 + 1e-9, step)
    ry = np.arange(cy - 8, cy + 8 + 1e-9, step)
    X, Y = np.meshgrid(rx, ry)
    dxx, dyy = X - cx, Y - cy
    r = np.hypot(dxx, dyy)
    th = np.mod(np.arctan2(dyy, dxx), 2 * math.pi)
    R_th = np.interp(th, np.append(2 * math.pi * np.arange(NR) / NR, 2 * math.pi), np.append(rad, rad[0]))
    s = r / R_th
    a0 = 6.0
    Rs = (a0 * a0 + H * H) / (2 * H)
    cap = np.sqrt(np.maximum(Rs * Rs - (a0 * s) ** 2, 0.0)) - (Rs - H)
    RZ = np.where(s <= 1.0, seabed(X, Y) + cap, np.nan)
    return dict(
        seabed=seabed, rx=rx, ry=ry, RZ=RZ,
        meta=dict(
            version_id='installed_Dec2019_spherical_cap', version_name='Installed bladder, December 2019 (torn before completion): symmetric spherical-cap stand-in, 12 m diameter, H = 2.0 m', version_date='2019-12-09..13',
            datum='z = metres above MSL; MSL = +0.1 m AHD (GHD 2021 Table 1, Port of Bunbury, rounded 0.1 m); z_MSL = z_AHD - 0.1',
            frame='x alongshore (true bearing 12.32 deg), y seaward from the fitted 0 m AHD contour of the 2009 lidar (bearing 282.32 deg), z up',
            shoreline_def='y = 0 is the fitted 0 m AHD contour of the 2009 lidar (about the MSL waterline, MSL = +0.1 m AHD; rms scatter 8.4 m) (model.js shoreline.definition).',
            reef_surface_def='z = lidar seabed(x, y) + capZ(s, H) with s = r / R_rim(theta) (rim from the traced 29-vertex polygon), capZ(t, H) = sqrt(Rs^2 - (6t)^2) - (Rs - H), Rs = (36 + H^2) / (2H) (index.html function capZ, buildReef with asymmetry 0). The viewer adds a +0.03 m rendering lift which is NOT included here. Default centre y = 37.5 m, H = 2.0 m (reef.height_default_m; text range 1.6-2.0 m).',
            seabed_def='model.js seabed (5 m grid resampled from the 10 m 2009 WA DoT airborne-lidar grid, z_MSL = AHD - 0.1; gap-filled cells flagged), vertical uncertainty +-0.5 m; default bed = lidar (state.bed = lidar).',
            source_files=['07_scale/shapes/bunbury-airwave/3d/model.js', '07_scale/shapes/bunbury-airwave/3d/index.html (lines 199-217, 382-425)'],
            caveats=['NOT a working reef: the bladder tore along a glued seam during installation (13 Dec 2019) and was removed; geometry is an idealised cap stand-in with height 1.6-2.0 m from pre-installation text, profile shape ASSUMED.',
                     'Offshore position 37.5 m from shoreline is the shape.json value; texts give 30-50 m (reef.offshore_presets).',
                     'Crest depth stated in text: about 1 m below surface at low tide (RWR, datum undefined) - compare with the modelled crest.'],
        ))


# ---------------------------------------------------------------------------------------------------------- Cables
def cables(m, mp):
    ver = next(v for v in m['versions'] if v['id'] == m['default_version'])
    g = ver['grid']
    RZ = b64_i16(g['h_cm_b64'], g['ny'], g['nx'])
    sb = rows_grid(m['seabed'])
    dv = next(v for v in m['versions'] if v['id'] == 'design_plan_original_1999')
    gd = dv['grid']
    return dict(
        seabed=sb, rx=ax(g['x0'], g['step'], g['nx']), ry=ax(g['y0'], g['step'], g['ny']), RZ=RZ,
        extra_layers=[dict(name='design_plan_original_1999 (datum reading A)', RZ=b64_i16(gd['h_cm_b64'], gd['ny'], gd['nx']),
                           note='Design surface on the measured bed, original-plan footprint (Lyons 1992 / Blacka 2013 Fig. A.2), crest RL -1.0 = -1.72 m AHD (reading A, offset 0.716 m); grid versions[design_plan_original_1999].grid. Not the default; included because the surveyed default surface stops at the design outline with 1.5-2.6 m of rock still standing at the outer edge, so its seaward slopes are not toe-to-crest slopes.')],
        true_shoreline=dict(
            # DERIVED, see extract_profiles.py: fitted 0 m AHD line bearing 7.8 deg T, 254 m due east of the anchor (centroid of original plan, canonical x 3.738, y 271.446 => model x -3.738)
            anchor_model=(-3.738, 271.446), x_bearing=170.3, y_bearing=260.3, shore_bearing=7.8, dist_east_m=254.0),
        meta=dict(
            version_id=ver['id'], version_name=ver['name'], version_date=ver['date'],
            datum='z = metres above MSL, MSL taken = AHD (A12). Surveyed versions are in AHD directly. Design versions: reading A (default for design) z_MSL = z_RL - 0.716 (Fremantle LWD to AHD, DNM TR12 Table 3, +-0.04 m); reading B: z_MSL = z_RL.',
            frame='x alongshore (+ toward SOUTH, bearing 170.3 deg T; x_model = -x_canonical); y offshore (+ toward WEST, bearing 260.3 deg T). The frame is the design-drawing frame rotated 9.74 deg ccw from true north: it is NOT shore-normal (fitted shoreline bearing 7.8 deg T, i.e. the y axis is about 17.5 deg off the shore normal).',
            shoreline_def='y = 0 is the NOMINAL origin line of the design frame (centroid of the original footprint at y = 271 m, Pattiaratchi 1999 / Blacka 2013), not the surveyed shoreline. The surveyed 0 m AHD line (fitted line, bearing 7.8 deg T) lies 254 m due east of the anchor (centroid) (shore_and_datum.py); y_true_shoreline is DERIVED from that (see derived_true_shoreline). The seabed grid starts at y = 190 m, so the MSL crossing is not in the model.',
            reef_surface_def='model.js versions[survey_surface_1999_11].grid.h_cm_b64 (int16 cm, z_MSL=AHD, 0.5 m cells, x already flipped to the model frame): rock thickness = DoT WA singlebeam soundings of 22 Nov 1999 (840 soundings, AHD) minus the measured 30 Mar 1998 pre-construction bed, linearly interpolated between sounding lines inside the original-plan footprint + 6 m, Gaussian-smoothed 1 m; footprint = the georeferenced Lyons (1992) original-plan outline (4,049 m2).',
            seabed_def='model.js seabed (5 m grid, y 190-420 m, x -150..150 m): DoT WA singlebeam of 30 Mar 1998 (pre-construction) inside the survey, Perth_5m composite elsewhere; AHD = MSL.',
            source_files=['07_scale/shapes/cables-reef-wa/3d/model.js', '07_scale/shapes/cables-reef-wa/3d/build_3d.py (lines 30-62, 120-140)', '07_scale/shapes/cables-reef-wa/3d/index.html (lines 148-175)', '07_scale/shapes/cables-reef-wa/HANDOFF.md', '07_scale/shapes/cables-reef-wa/3d/METHODS_3D.md section 3.6'],
            caveats=['Default surface is a MEASURED single-beam survey (+-0.3 m, interpolated between ~5 m sounding lines, smoothed 1 m) of the month before completion (Nov 1999): crest top -1.55 m AHD, highest sounding -1.40 m. Feb 2002 survey: -1.71 / -1.67 m.',
                     'Footprint is the original design outline; the drawn south-arm extension is NOT confirmed (23 soundings).',
                     'Footprint edge cells keep a non-zero rock thickness (survey interpolation within the outline), so the surface does not taper to zero at the toe.',
                     'Design crest RL -1.0 = -1.72 m AHD (reading A) or -1.00 m (B); the surveyed surface is 0.13-0.22 m higher than reading A (physical/survey, not datum).'],
        ))


# ----------------------------------------------------------------------------------------------------- Mount Maunganui
def mount_maunganui(m, mp):
    MSL = m['datum']['msl_above_cd_m']
    SB = m['seabed']
    R = m['reef']
    GR = R['grid']
    ZC = R['zc_cd']
    YC = SB['y_ref']
    KY = np.array([k[0] for k in SB['knots_cd']], float)
    KZ = np.array([k[1] for k in SB['knots_cd']], float)

    def pnav(y):
        y = np.asarray(y, float)
        out = np.interp(y, KY, KZ)
        out = np.where(y >= KY[-1], KZ[-1] + (y - KY[-1]) * (KZ[-1] - KZ[-2]) / (KY[-1] - KY[-2]), out)
        out = np.where(y < 0, MSL - y / SB['beach_run_per_rise'], out)
        return out

    ZREF = float(pnav(YC))
    bed = SB['bed_default_cd']       # -3.6 m CD (ASSUMPTION, Lior decision D1)

    def bedCD(y):
        w = np.clip((np.asarray(y, float) - SB['w_y0']) / (YC - SB['w_y0']), 0, 1)
        return pnav(y) + (bed - ZREF) * w

    def seabed(x, y):
        x = np.asarray(x, float)
        y = np.asarray(y, float)
        x, y = np.broadcast_arrays(x, y)
        ext = SB['extent']
        z = bedCD(y) - MSL
        bad = (y < ext['y'][0]) | (y > ext['y'][1]) | (x < ext['x'][0]) | (x > ext['x'][1])
        return np.where(bad, np.nan, z)
    ver = next(v for v in m['versions'] if v['id'] == m['default_version'])
    nx, ny = GR['nx'], GR['ny']
    inner = np.array(R['inner_per_mille'], float).reshape(ny, nx)
    flank = np.array(ver['flank'], float).reshape(ny, nx)
    crest = R['crest_cd']['default']
    run = ver.get('run_default', 1.0)
    rxs = ax(GR['x0'], GR['dx'], nx)
    rys = ax(GR['y0'], GR['dx'], ny)
    S = np.repeat(bedCD(rys)[:, None], nx, axis=1)
    Z = S.copy()
    msk = inner >= 0
    Z[msk] = ZC + inner[msk] / 1000.0 * (crest - ZC)
    mf = (~msk) & (flank >= 0)
    if ver['rule'] == 'skirt':
        Z[mf] = np.maximum(S[mf], ZC - flank[mf] / 100.0 / run)
    else:
        Z[mf] = np.maximum(S[mf], S[mf] + (ZC - S[mf]) * flank[mf] / 1000.0)
    Hh = np.maximum(0, Z - S)
    RZ = np.where(Hh > 0.005, Z - MSL, np.nan)
    ev = m['survey2013']
    g2 = ev['grid']
    ZZ = np.array(ev['z_msl_cm'], float).reshape(g2['ny'], g2['nx'])
    ZZ[ZZ == ev['nodata']] = np.nan
    ZZ /= 100.0
    return dict(
        seabed=seabed, rx=rxs, ry=rys, RZ=RZ,
        extra_layers=[dict(name='multibeam_2013-07-18_DEM_from_BoPRC_Fig5', rx=ax(g2['x0'], g2['dx'], g2['nx']), ry=ax(g2['y0'], g2['dy'] if 'dy' in g2 else g2['dx'], g2['ny']), RZ=ZZ,
                      note='18 Jul 2013 multibeam DEM decoded from the hue of BoPRC Fig. 5 (colour-read, see model.js survey2013.note; z_MSL cm); evidence layer, 5 years after completion, not the default. The survey grid is 1 m and covers only the surveyed part.')],
        meta=dict(
            version_id=ver['id'], version_name=ver['name'], version_date=ver['date'],
            datum='z = metres above present MSL; MSL = Chart Datum + 1.13 m (LINZ Tauranga 2026-27 standard port levels); z_MSL = z_CD - 1.13; MVD-53 = CD + 0.9622 m (NIWA 2006)',
            frame='x alongshore (true bearing 316.15 deg, toward NW / Mauao side); y offshore (true bearing 46.15 deg, shore-normal, toward NE); origin = point on the wet/dry-sand shoreline (Esri 2011-01-15) nearest the survey-outline centroid',
            shoreline_def='y = 0 is the wet/dry-sand boundary of the Esri 2011-01-15 image; the seabed rule starts at y = 0 with z = MSL (first knot (0, 1.13 m CD)), so y = 0 is also the MSL line of the modelled profile by construction. Landward (y < 0) a schematic 1:15 beach (not sourced).',
            reef_surface_def='Re-implementation of index.html computeField(): inside the -2.0 m CD polygons of the 18 Jul 2013 multibeam survey z_CD = ZC + r/1000 (crest - ZC) with ZC = -2.0 m CD, crest = -0.9 m CD (reef.crest_cd.default), r from reef.inner_per_mille (2013 DEM median rise table scaled to 1.10 m); outside: skirt z_CD = max(S, ZC - dout/run), run 1.0 (H:V = 1:1, ASSUMPTION), dout = distance from the -2.0 m contour (versions[].flank, cm); z_MSL = z_CD - 1.13. Grid 0.5 m. Reef cells = height above local bed > 0.005 m.',
            seabed_def='Alongshore-UNIFORM cross-shore profile (no x dependence): S(y) = Pnav(y) + (bed - Pnav(y_ref)) * clamp((y - 111.2)/(y_ref - 111.2), 0, 1) in m CD, Pnav = Navionics SonarChart 2026 contour crossings (knots_cd), bed at the reef = -3.6 m CD = -4.73 m MSL (ASSUMPTION, Lior decision D1 2026-10-07; chart datum assumed, RMS 0.30 m against the 2013 multibeam).',
            source_files=['07_scale/shapes/mount-maunganui-reef/3d/model.js', '07_scale/shapes/mount-maunganui-reef/3d/index.html (lines 193-245, 366-400)'],
            caveats=['As-built seabed under the reef is an ASSUMPTION (-3.6 m CD; stated volume 2,800 m3 gives -3.51 m); the later seabed (Navionics 2026) is -2.76 m CD, which would give a reef 0.84 m lower in height. Reef HEIGHT and slopes therefore depend on this assumption; the crest level (-0.9 m CD = -2.03 m MSL, BoPRC p6/p21) is sourced.',
                     'Flank (skirt) 1:1 below the -2.0 m CD contour is an ASSUMPTION; inside the contour the rise follows the 2013 DEM median rise table.',
                     'Seabed is alongshore uniform; no x dependence.'],
        ))


# ------------------------------------------------------------------------------------------------------- Narrowneck
def narrowneck(m, mp):
    ver = next(v for v in m['versions'] if v['id'] == m['default_version'])
    g = ver['grid']
    RZ = b64_i16(g['h_cm_b64'], g['ny'], g['nx'])
    sb = rows_grid(m['seabed'])
    return dict(
        seabed=sb, rx=ax(g['x0'], g['step'], g['nx']), ry=ax(g['y0'], g['step'], g['ny']), RZ=RZ,
        meta=dict(
            version_id=ver['id'], version_name=ver['name'], version_date=ver['date'],
            datum='z = metres above MSL; z_MSL = z_AHD - 0.12 (MSQ 2026 Gold Coast Seaway planes: AHD = LAT + 0.76, MSL = LAT + 0.88, uncertainty +-0.25 m); alternative from the papers: AHD = LAT + 1.00 shifts geometry by +0.24 m',
            frame='x alongshore (+ toward NORTH, bearing 356.21 deg T); y offshore (+ toward EAST, bearing 86.21 deg T); origin = waterline of the 2020-08-08 Esri image nearest the reef centroid',
            shoreline_def='y = 0 is the waterline of the Esri World Imagery of 8 Aug 2020 (tide stage unknown); the seabed profile there is 0.0 m AHD = -0.12 m MSL (validation.stats.bed_profile_AHD), so the MSL crossing is within a few metres of y = 0.',
            reef_surface_def='model.js versions[photo_2020-08-08].grid.h_cm_b64 (int16 cm, z_MSL, 1 m cells): plan = 7 traced container-field polygons of the 8 Aug 2020 aerial; surface = design crest surface of renewal Option 2 (crest loops -2.5 m AHD, falling linearly with distance rank to the -6 m AHD envelope), lowered to the measured shallowest crest -2.2/-1.8 m AHD (build_3d.py surface()).',
            seabed_def='model.js seabed (5 m grid, z_MSL): 2017 multibeam (19 Jul 2017) + Navionics labels; offshore profile AHD: 0 at y 0, -1.8 at y 100, -2.1 at y 190, -5.1 at y 265, -6.76 at y 340 (validation.stats.bed_profile_AHD).',
            source_files=['07_scale/shapes/narrowneck-gold-coast/3d/model.js', '07_scale/shapes/narrowneck-gold-coast/3d/build_3d.py (lines 90-115)', '07_scale/shapes/narrowneck-gold-coast/3d/index.html (lines 154-165)'],
            caveats=['Plan is a photo trace of the VISIBLE container field (a lower bound of the footprint; deeper toe not visible); the top surface is a design-rule surface, not a survey; confidence MEDIUM.',
                     'The reef has two arms (north and south) plus channel containers; the cross-shore centreline x_c is the mid-point of the whole footprint (the gap between the arms), so the centreline profile crosses only low, discontinuous container patches. The main crest line (x = 46 m) clips the shoreward tip of the north arm (1-2 m of reef at the crest), so its ramp metrics are not representative; the second crest line (south arm, x = -40 m) and the crest labels in model.js (north-arm crest -2.32 m MSL at x = 30.7, y = 279.9) describe the arms better.',
                     'History (1999-2000 build, 2004 weir and flared wings, 2017-18 renewal) is not modelled; this is the state after the June 2018 renewal.'],
        ))


# ----------------------------------------------------------------------------------------------------------- Palm Beach
def palm_beach(m, mp):
    sb = m['seabed']
    seabed = GridFn(sb['x0'], sb['y0'], sb['dx'], sb['dx'], np.array(sb['z_cm'], float).reshape(sb['ny'], sb['nx']) / 100.0)
    g = m['reef']['grid']
    Z = np.array(g['z_cm'], float).reshape(g['ny'], g['nx'])
    Z[Z == g['nodata']] = np.nan
    Z /= 100.0
    return dict(
        seabed=seabed, rx=ax(g['x0'], g['dx'], g['nx']), ry=ax(g['y0'], g['dx'], g['ny']), RZ=Z,
        meta=dict(
            version_id='as_built_2019', version_name='As built (rock placed May-Sept 2019, certified Sept 2019); contours from Bluecoast/Nearmap aerial of the completed reef', version_date='2019-09 (aerial undated, Sept 2019 - Sept 2020)',
            datum='z = metres above MSL; MSL = LAT + 0.88 m (MSQ 2026 Gold Coast Seaway); seabed Navionics depths taken as depth below LAT (assumption A5): z_MSL = -d - 0.88',
            frame='x alongshore (toward 334.3 deg T, NNW); y offshore (toward 64.3 deg T, ENE); origin on the waterline of Esri World Imagery 2025-12-01',
            shoreline_def='y = 0 is the waterline fitted to Esri World Imagery 2025-12-01 and taken as z = 0 (MSL) (assumption A7, tide stage of the image unknown). Landward (y < 0) a visual beach face rises at 1:15 (not surveyed).',
            reef_surface_def='model.js reef.grid.z_cm (1 m cells, z_MSL): linear (Delaunay) interpolation between survey contour lines read off the aerial, each at z = -1.5 - 0.5 k m (k = lines crossed outward from the 59 x 6 m crest outline at -1.5 m MSL), toe outline at the next 0.5 m level by fractional position; edge ramped (2.5 m) onto the seabed (reef.side_slope_rule).',
            seabed_def='model.js seabed.z_cm (4 m grid, z_MSL): thin-plate spline through Garmin Navionics SonarChart iso-depth lines (1 m interval, outside a 25 m buffer round the reef) plus toe elevations read from the aerial contours (hybrid); under the reef and seaward of the 10 m line interpolated / extrapolated; chart datum assumed LAT (rms residual 0.08 m).',
            source_files=['07_scale/shapes/palm-beach-gold-coast/3d/model.js', '07_scale/shapes/palm-beach-gold-coast/3d/index.html (lines 160-190)'],
            caveats=['Crest at -1.5 m MSL is from the contour reading of an undated aerial (chart/lidar datum of the contour lines assumed); height above the seabed is sensitive to the Navionics datum assumption (volume 12,000-34,000 m3 for a +-1 m seabed offset).',
                     'Seabed under the reef is interpolated (reef height 3.9 m at the crest from an interpolated bed of -5.4 m MSL, hybrid; Navionics-only bed -5.0 m).'],
        ))


# ------------------------------------------------------------------------------------------------------------- Prattes
def prattes(m, mp):
    S = m['seabed']
    yp = np.array(S['profile_y_m'], float)
    zp = np.array(S['profile_z_m'], float)    # default bed = NOAA DEM mean profile (state.bed = 'dem')

    def seabed(x, y):
        x = np.asarray(x, float)
        y = np.asarray(y, float)
        x, y = np.broadcast_arrays(x, y)
        z = np.interp(y, yp, zp)
        return np.where((y < yp[0]) | (y > yp[-1]), np.nan, z)
    R = m['reef']
    import shapely
    from shapely.geometry import Polygon
    poly = Polygon(R['toe_polygon_xy_m'])
    st = next(s for s in R['states'] if s['id'] == R['default_state'])
    slope_run = R['slope_run_default']
    min_h = R['min_height_m']
    cell = 0.25
    b = poly.bounds
    xs = np.arange(b[0] - 1 + cell / 2, b[2] + 1, cell)
    ys = np.arange(b[1] - 1 + cell / 2, b[3] + 1, cell)
    X, Y = np.meshgrid(xs, ys)
    inside = shapely.contains_xy(poly, X, Y)
    d = np.zeros_like(X)
    pts = shapely.points(X[inside], Y[inside])
    d[inside] = shapely.distance(pts, poly.exterior)
    zb = seabed(X, Y)
    if st['mode'] == 'level':
        Htop = np.maximum(st['z_msl'] - zb, min_h)
    else:
        t = max(st['z_ref_msl'] - float(seabed(0.0, st['y_ref_m'])), min_h)
        Htop = np.full_like(zb, t)
    H = np.where(inside, np.minimum(Htop, d / slope_run), 0.0)
    RZ = np.where(inside & (H > 0), zb + H, np.nan)
    return dict(
        seabed=seabed, rx=xs, ry=ys, RZ=RZ,
        meta=dict(
            version_id='state_' + st['id'], version_name=st['label'], version_date='Phase I, 22 Sept 2000 (as installed)',
            datum='z = metres above MSL (NOAA 9410840 Santa Monica, epoch 1983-2001); MSL - MLLW = 0.849 m; z_MSL = z_NAVD88 - 0.792 (DEM); LAT = -1.469 m MSL; MLLW = -0.849 m MSL',
            frame='x alongshore (toward 155 deg T, SSE); y offshore (toward 245 deg T, WSW); origin on the MSL waterline (alongshore-uniform profile)',
            shoreline_def='y = 0 is the MSL waterline: the z = 0 contour of the NOAA DEM mean cross-shore profile (model.js seabed.shoreline_y_m = 0, definition: "MSL waterline (z = 0 contour of the seabed profile)").',
            reef_surface_def='Re-implementation of build_3d.py reef_height_field(): h(x,y) = max(0, min(h_top, d_in/slope_run)), d_in = distance inside the toe outline (76-vertex Skelly Engineering design layout of 110 bags, no as-built plan exists), slope_run = 1.0 (ASSUMPTION A5), h_top = constant thickness z_ref - z_seabed(y_ref) = %.3f m (state B: outermost point approx. 6 ft = 1.829 m below MLLW = -2.678 m MSL at the apex, Borrero and Nelsen 2003 p.2; assumption A4: top follows the seabed at constant thickness), >= one 1.2 m bag course; z = z_seabed(y) + h; 0.25 m grid.' % (float(t) if st['mode'] != 'level' else float('nan')),
            seabed_def='model.js seabed.profile_z_m (5 m spacing, NOAA NGDC 2010 Santa Monica 1/3 arc-second NAVD88 DEM, mean of 31 alongshore stations +-150 m, z_MSL = z_NAVD88 - 0.792); alongshore-UNIFORM (no x dependence). Position of the reef on the profile is nominal (100 yd = 91.44 m from the waterline; +-25 m uncertainty, reef_offset_range_m).',
            source_files=['07_scale/shapes/prattes-reef-el-segundo/3d/model.js', '07_scale/shapes/prattes-reef-el-segundo/3d/build_3d.py (lines 48-72, 205-216)'],
            caveats=['Plan is the DESIGN layout (no as-built plan); crest level is a single sourced number (-6 ft MLLW at the apex); the top is assumed parallel to the seabed (state B), so the highest point is at the shoreward tips (-1.78 m MSL) and the V is shallower shoreward.',
                     'State A (top of bag -6 ft MSL = -1.829 m, level crest, Skelly drawing) is the alternative; both are the same number with two datum labels.',
                     'Reef is a V of geotextile sand bags ~1.2-1.35 m high (3.0 x 2.13 x 1.2 m bags); hence slopes are bag-stack flanks (1:1 assumed), not designed wave-transformation ramps.',
                     'The V arms are oblique to the model y axis and narrow (about 10-15 m), so any constant-x line crosses an arm over a few metres only: the crest-line ramp (1-2 m) is a tip artefact; the centreline crosses the apex block (ramp about 5 m). Use the stack height (1.35 m) and the 1:1 flank assumption instead of the line slopes.',
                     'Confidence in the 3D model is LOW (model.js confidence_3d).'],
        ))


# ---------------------------------------------------------------------------------------------------------- Albany
def albany(m, mp):
    sbg = rows_grid(m['seabed'])
    prof = np.array(m['seabed']['profile'], float)      # [[y, z_AHD], ...] the definition of the (alongshore-uniform) seabed

    def sb(x, y):
        x = np.asarray(x, float)
        y = np.asarray(y, float)
        x, y = np.broadcast_arrays(x, y)
        z = np.interp(y, prof[:, 0], prof[:, 1])
        xr, yr = sbg.x_range, sbg.y_range
        return np.where((y < yr[0]) | (y > yr[1]) | (x < xr[0]) | (x > xr[1]), np.nan, z)
    ver = next(v for v in m['versions'] if v['id'] == m['default_version'])
    g = ver['grid']
    H = b64_i16(g['h_cm_b64'], g['ny'], g['nx'])         # height above the seabed (m), NaN outside the footprint
    rx = ax(g['x0'], g['step'], g['nx'])
    ry = ax(g['y0'], g['step'], g['ny'])
    X, Y = np.meshgrid(rx, ry)
    RZ = np.where(np.isfinite(H), sb(X, Y) + H, np.nan)
    return dict(
        seabed=sb, rx=rx, ry=ry, RZ=RZ,
        meta=dict(
            version_id=ver['id'], version_name=ver['name'], version_date=ver['date'],
            datum='z = metres above AHD, taken as MSL (assumption A2); LAT = -0.74 m AHD (derived: LAT + mean of 2024 predicted extremes), MHHW = +0.34, MLLW = -0.26 (City of Albany crest statement)',
            frame='x alongshore (+ toward NNE, bearing 30.26 deg T); y offshore (+ toward ESE, bearing 120.26 deg T); origin = foot of the perpendicular from the traced reef centroid onto the beach-face line (edge of bright dry sand, Esri 2026-01-20)',
            shoreline_def='y = 0 is the beach-face line (edge of bright dry sand) of the Esri 2026-01-20 image, NOT the MSL line. The modelled seabed (seabed.profile: z = +1.0 m at y -30, -0.5 m at y +7) crosses z = 0 (AHD = MSL) about 5 m LANDWARD of y = 0 (y_msl_crossing_m, interpolated).',
            reef_surface_def='model.js versions[design_bluecoast].grid.h_cm_b64 = reef HEIGHT above the seabed (int16 cm, 1 m cells); z = seabed(x, y) + h with the bilinear 5 m seabed (index.html buildReef: z = seaAt(x,y) + h). Height rule (build_3d.py reef_grid): crest ridge 9 m inside the steep shoreward edge, -1.0 m AHD at the offshore (east) end and -2.0 m AHD along the rest (City design table), flanks fall to the seabed with shape exponent N = 2.734, volume fitted to the stated 34,000 m3.',
            seabed_def='model.js seabed.profile (17 knots y -> z AHD=MSL, linearly interpolated; the 5 m seabed.z grid reproduces it within 0.04 m): medians of the RHDHV 2015 design-report contour crossings over 10 shore-normal transects (nodes -1 to -7 m), deeper nodes adjusted by eye, landward of -0.5 m and seaward of -7 m ASSUMED (build_3d.py PROFILE, A4/A5). Alongshore-UNIFORM (no x dependence). LOW confidence.',
            source_files=['07_scale/shapes/southern-ocean-surf-reef-albany/3d/model.js', '07_scale/shapes/southern-ocean-surf-reef-albany/3d/build_3d.py (lines 100-130)', '07_scale/shapes/southern-ocean-surf-reef-albany/3d/index.html (lines 123-170)'],
            caveats=['3D confidence is LOW: the plan outline is high-confidence and the crest levels are City DESIGN values, but the seabed under the reef (hence heights and flank slopes) is read from 2015 design contours; the reef shape between toe and ridge is a fitted rule (exponent N) not a survey.',
                     'Default version is the Bluecoast design outline (13,104 m2); the visible-reef version (Esri 2026-01-20) has 10,919 m2.',
                     'Slopes of the flanks follow from the fitted exponent and the volume fit to 34,000 m3 (design) and are therefore model results, not measurements.'],
        ))


ADAPTERS = {
    'borth-coastal-defence-reef': borth,
    'boscombe-surf-reef': boscombe,
    'bunbury-airwave': bunbury,
    'cables-reef-wa': cables,
    'mount-maunganui-reef': mount_maunganui,
    'narrowneck-gold-coast': narrowneck,
    'palm-beach-gold-coast': palm_beach,
    'prattes-reef-el-segundo': prattes,
    'southern-ocean-surf-reef-albany': albany,
}


# =====================================================================================================================
#                                      (2) PROFILE SAMPLING AND METRICS
# =====================================================================================================================


STEP = 1.0            # m, profile sampling step (task: every 1-2 m)
THK_MIN = 0.10        # m, a reef cell belongs to the footprint if reef surface - natural seabed >= THK_MIN (ASSUMPTION, documented)
CREST_TOL = 0.10      # m, crest zone = contiguous points within CREST_TOL of the line's highest reef point (ASSUMPTION)
TIE_TOL = 0.02        # m, cells within TIE_TOL of the global maximum are 'equally shallowest'; the one nearest the footprint centroid is used
SLOPE_HALF = 1.0      # m, max slope = central difference over +-SLOPE_HALF (2 m baseline)
PAD_SEA = 150.0       # m, profile extends this far seaward of the most offshore reef toe (or to the end of the seabed domain)
LAND_LIMIT = -50.0    # m, profile starts at most this far landward of the model shoreline y = 0
GAP_BRIDGE = 12.0     # m, gaps in the reef along a line up to this length are bridged when the reef run is formed (discrete containers / arms; ASSUMPTION)
HYPSO_LEVELS = [0.5, 0.0, -0.5, -1.0, -1.5, -2.0, -2.5, -3.0, -4.0, -5.0]   # m MSL, for the alongshore-extent table

# ---- per-reef override of the PRIMARY cut ('crest_line'), after Lior's figure review of 2026-10-19 ------------------
# The automatic rule (constant model x through the shallowest crest cell) is kept for every other reef. For the reefs
# below the automatic line does not cross the part of the reef where the wave breaks and is surfed, or is not
# perpendicular to the local shoreline. The override line is given by an anchor point (model x, y) and the direction of
# the offshore shore normal; the profile is sampled along that line by the same bilinear interpolation on the model
# grids (seabed and reef surface). The automatic line is kept in the JSON as lines.crest_line_auto (not used downstream).
#   anchor: (x, y) in the model frame, or 'centroid' = area centroid of the reef footprint
#   normal: 'model_y' = the model +y axis (the model frame is shore-normal for these reefs), or
#           ('shore_bearing', deg T) = perpendicular to a shoreline of that bearing (offshore side), converted with the
#           model axis bearings x_bearing / y_bearing of the adapter's true_shoreline record
CUT_OVERRIDES = {
    'southern-ocean-surf-reef-albany': dict(
        anchor=(17.0, 118.0), normal='model_y',
        reason='Lior 2026-10-19: the automatic crest line (x = 48 m, through the -1.0 m AHD take-off plateau at the offshore '
               'end) lies on the short offshore part of the reef, not where the wave is ridden. The cut is moved to the middle '
               'of the long -2.0 m AHD ridge ("crest 110 m @ -2 m AHD", City of Albany / Bluecoast design table, '
               'SOURCE_AUDIT_2026-10-10 design_table): the ridge cells of the model (row-wise maximum of the reef surface, '
               'z > -2.15 m) run from (x 3, y 68) to (x 38, y 168); the middle of that -2 m ridge is about (x 17, y 118). '
               'Cut perpendicular to the shoreline (model x = 17 m constant; the Albany frame is shore-normal). '
               'Built reef is a left-hander with the take-off at the offshore (east) end and the ride along this ridge '
               '(design table "left-hander, peel 60 deg, rides to 100 m"; 07_scale/shapes/southern-ocean-surf-reef-albany/'
               'HANDOFF.md, 3d/REGISTER_3D.md A7).'),
    'cables-reef-wa': dict(
        anchor='centroid', normal=('shore_bearing', 7.8),
        reason='Lior 2026-10-19: the automatic crest line followed the design-frame y axis, which is about 17.5 deg off the '
               'shore normal, and passed through the west arm. The cut now goes through the middle of the reef (area '
               'centroid of the footprint) and is perpendicular to the local shoreline: fitted 0 m AHD line, bearing 7.8 deg T '
               '(07_scale/shapes/cables-reef-wa/HANDOFF.md, shore_and_datum.py), so the cut runs offshore at bearing '
               '277.8 deg T. Check: the mean down-slope direction of the model seabed over the reef area '
               '(x -80..80 m, y 200..330 m) is 17.9 deg from the model +y axis, the same side and within 0.4 deg.'),
    'borth-coastal-defence-reef': dict(
        anchor=(-43.5, 338.0), normal='model_y',
        reason='Lior 2026-10-19: move the cut a little to the right in the plan of Figure 1 (looking seaward), i.e. 10 m '
               'south (model x -33.5 -> -43.5 m), so that it crosses the middle of the main ridge of the northern (boot) '
               'surf reef instead of its northern shoulder. No source locates the surf break at Borth (reef card: no '
               'ride or break position found), so the position is a judgement on the plan. Cut perpendicular to the shoreline '
               '(model x constant; the Borth frame is shore-normal).'),
}


def rnd(a, nd=3):
    a = np.asarray(a, float)
    return [None if not np.isfinite(v) else round(float(v), nd) for v in a]


def sample_reef(rx, ry, RZ, x, y):
    """Normalised bilinear sample of the reef surface (NaN-aware); NaN where fewer than half of the 4 neighbours exist."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    x, y = np.broadcast_arrays(x, y)
    fx = (x - rx[0]) / (rx[1] - rx[0])
    fy = (y - ry[0]) / (ry[1] - ry[0])
    fin = np.isfinite(RZ)
    num = ndi.map_coordinates(np.where(fin, RZ, 0.0), [fy.ravel(), fx.ravel()], order=1, mode='constant', cval=0.0)
    den = ndi.map_coordinates(fin.astype(float), [fy.ravel(), fx.ravel()], order=1, mode='constant', cval=0.0)
    with np.errstate(invalid='ignore', divide='ignore'):
        out = np.where(den >= 0.5, num / den, np.nan)
    return out.reshape(x.shape)


def footprint(rx, ry, RZ, seabed, mask=None):
    X, Y = np.meshgrid(rx, ry)
    SB = seabed(X, Y)
    TH = RZ - SB
    foot = np.isfinite(RZ) & (TH >= THK_MIN)
    if mask is not None:
        foot &= mask(X, Y)
    return X, Y, SB, TH, foot


def crest_and_centre(rx, ry, RZ, X, Y, foot):
    zmax = float(np.nanmax(np.where(foot, RZ, np.nan)))
    cand = foot & (RZ >= zmax - TIE_TOL)
    cx, cy = X[foot].mean(), Y[foot].mean()          # area centroid of the footprint
    d = np.hypot(X[cand] - X[cand].mean(), Y[cand] - Y[cand].mean())
    # tie-break: candidate cell nearest the centroid of the candidate set (the 'middle' of the shallowest plateau)
    k = int(np.argmin(d))
    xc, yc = float(X[cand][k]), float(Y[cand][k])
    cols = np.where(foot.any(axis=0))[0]
    x_lo, x_hi = float(rx[cols[0]]), float(rx[cols[-1]])
    rows = np.where(foot.any(axis=1))[0]
    y_lo, y_hi = float(ry[rows[0]]), float(ry[rows[-1]])
    dx = float(rx[1] - rx[0])
    return dict(zmax=zmax, x_crest=xc, y_crest=yc, x_centre=0.5 * (x_lo + x_hi), x_centroid=float(cx), y_centroid=float(cy),
                x_range=[x_lo, x_hi], y_range=[y_lo, y_hi], area_m2=float(foot.sum() * dx * (ry[1] - ry[0])), dx=dx)


def crest_cell(X, Y, RZ, sel):
    """shallowest reef cell inside the boolean selection `sel` (ties within TIE_TOL: the cell nearest the middle of the tied set)"""
    if not sel.any():
        return None
    zmax = float(np.nanmax(np.where(sel, RZ, np.nan)))
    cand = sel & (RZ >= zmax - TIE_TOL)
    d = np.hypot(X[cand] - X[cand].mean(), Y[cand] - Y[cand].mean())
    k = int(np.argmin(d))
    return float(X[cand][k]), float(Y[cand][k]), zmax


def alongshore_length(rx, RZ, foot, level):
    """Alongshore extent (model x) of the part of the footprint whose surface is at or above `level` (m MSL):
    span = x_max - x_min of such cells; union = (number of x-columns containing such a cell) * dx."""
    sel = foot & (RZ >= level)
    if not sel.any():
        return dict(level_msl_m=round(float(level), 3), span_m=None, union_m=None, note='no reef cell at or above this level')
    cols = np.where(sel.any(axis=0))[0]
    dx = float(rx[1] - rx[0])
    return dict(level_msl_m=round(float(level), 3), span_m=round(float((cols[-1] - cols[0]) * dx + dx), 2), union_m=round(float(len(cols) * dx), 2),
                x_min_m=round(float(rx[cols[0]]), 2), x_max_m=round(float(rx[cols[-1]]), 2))


def msl_crossing(y, zs):
    """First downward crossing of z = 0 (MSL) moving offshore along the natural-seabed profile (linear interpolation)."""
    ok = np.isfinite(zs)
    for k in range(len(y) - 1):
        if ok[k] and ok[k + 1] and zs[k] > 0 >= zs[k + 1]:
            return float(y[k] + (0 - zs[k]) * (y[k + 1] - y[k]) / (zs[k + 1] - zs[k]))
    return None


def runs(inrun):
    out = []
    k = 0
    n = len(inrun)
    while k < n:
        if inrun[k]:
            j = k
            while j + 1 < n and inrun[j + 1]:
                j += 1
            out.append((k, j))
            k = j + 1
        else:
            k += 1
    return out


def slope_stats(y, z, k0, k1):
    """max slope (positive = deeper seaward, i.e. surface falls with increasing y) by central difference +-SLOPE_HALF between indices k0..k1"""
    h = int(round(SLOPE_HALF / (y[1] - y[0])))
    best, kb = None, None
    for k in range(max(k0, h), min(k1, len(y) - 1 - h) + 1):
        a, b = z[k - h], z[k + h]
        if np.isfinite(a) and np.isfinite(b):
            s = (a - b) / (y[k + h] - y[k - h])
            if best is None or s > best:
                best, kb = s, k
    return best, kb


def fmt_slope(s):
    if s is None or not np.isfinite(s) or s <= 0:
        return dict(tan=None, deg=None, one_in=None)
    return dict(tan=round(float(s), 4), deg=round(math.degrees(math.atan(s)), 2), one_in=round(1.0 / s, 2))


def line_metrics(y, zs, zr):
    th = zr - zs
    inrun = np.isfinite(zr) & (th >= THK_MIN)
    if not inrun.any():
        return dict(reef_on_line=False)
    raw_segs = runs(inrun)
    kmax = int(np.nanargmax(np.where(inrun, zr, -np.inf)))
    # merge segments separated by gaps <= GAP_BRIDGE
    gmax = int(round(GAP_BRIDGE / (y[1] - y[0])))
    merged = [list(raw_segs[0])]
    bridged = []
    for a, b in raw_segs[1:]:
        if a - merged[-1][1] - 1 <= gmax:
            bridged.append(dict(y_from_m=round(float(y[merged[-1][1] + 1]), 2), y_to_m=round(float(y[a - 1]), 2)))
            merged[-1][1] = b
        else:
            merged.append([a, b])
    segs = [tuple(s) for s in merged]
    seg = next(s for s in segs if s[0] <= kmax <= s[1])
    i0, i1 = seg
    # crest zone: contiguous around kmax within CREST_TOL of the max
    zmax = float(zr[kmax])
    c0 = kmax
    while c0 - 1 >= i0 and zr[c0 - 1] >= zmax - CREST_TOL:
        c0 -= 1
    c1 = kmax
    while c1 + 1 <= i1 and zr[c1 + 1] >= zmax - CREST_TOL:
        c1 += 1
    step = float(y[1] - y[0])
    ramp_len = float(y[i1] - y[c1])
    rise = float(zr[c1] - zr[i1])
    msl = msl_crossing(y, zs)
    smax, ksm = slope_stats(y, zr, c1, i1)
    # shoreward face
    sh_len = float(y[c0] - y[i0])
    sh_rise = float(zr[c0] - zr[i0])
    out = dict(
        reef_on_line=True,
        crest_z_msl_m=round(zmax, 3), crest_y_m=round(float(y[kmax]), 2), crest_depth_below_msl_m=round(-zmax, 3),
        crest_seabed_z_msl_m=round(float(zs[kmax]), 3), crest_height_above_seabed_m=round(float(zr[kmax] - zs[kmax]), 3),
        crest_zone_y_m=[round(float(y[c0]), 2), round(float(y[c1]), 2)], crest_zone_width_m=round(float(y[c1] - y[c0] + step), 2),
        seaward_toe_y_m=round(float(y[i1]), 2), seaward_toe_reef_z_msl_m=round(float(zr[i1]), 3), seaward_toe_seabed_z_msl_m=round(float(zs[i1]), 3),
        seaward_toe_thickness_m=round(float(zr[i1] - zs[i1]), 3),
        ramp_length_m=round(ramp_len, 2), ramp_rise_m=round(rise, 3),
        crest_to_toe_drop_m=round(float(zmax - zr[i1]), 3), crest_to_toe_seabed_drop_m=round(float(zmax - zs[i1]), 3),
        mean_seaward_slope=fmt_slope(rise / ramp_len) if ramp_len > 0 else fmt_slope(None),
        max_seaward_slope=fmt_slope(smax), max_seaward_slope_at_y_m=None if ksm is None else round(float(y[ksm]), 2),
        shoreward_toe_y_m=round(float(y[i0]), 2), shoreward_toe_reef_z_msl_m=round(float(zr[i0]), 3), shoreward_toe_seabed_z_msl_m=round(float(zs[i0]), 3),
        shoreward_ramp_length_m=round(sh_len, 2), shoreward_ramp_rise_m=round(sh_rise, 3),
        mean_shoreward_slope=fmt_slope(sh_rise / sh_len) if sh_len > 0 else fmt_slope(None),
        reef_cross_shore_extent_m=round(float(y[i1] - y[i0] + step), 2),
        max_thickness_on_line_m=round(float(np.nanmax(np.where(inrun, th, np.nan))), 3),
        y_msl_crossing_m=None if msl is None else round(msl, 2),
        segments=[dict(y_from_m=round(float(y[a]), 2), y_to_m=round(float(y[b]), 2), max_z_msl_m=round(float(np.nanmax(zr[a:b + 1])), 3)) for a, b in segs],
        bridged_gaps=bridged,
        seabed_mean_slope_under_reef=fmt_slope((float(zs[i0]) - float(zs[i1])) / (float(y[i1]) - float(y[i0]))) if i1 > i0 else fmt_slope(None),
    )
    if msl is not None:
        out['crest_distance_from_msl_line_m'] = round(float(y[kmax]) - msl, 2)
        out['seaward_toe_distance_from_msl_line_m'] = round(float(y[i1]) - msl, 2)
        out['shoreward_toe_distance_from_msl_line_m'] = round(float(y[i0]) - msl, 2)
        if y[i1] > msl:
            out['seabed_mean_slope_msl_line_to_seaward_toe'] = fmt_slope((0.0 - float(zs[i1])) / (float(y[i1]) - msl))
        if y[i0] > msl:
            out['seabed_mean_slope_msl_line_to_shoreward_toe'] = fmt_slope((0.0 - float(zs[i0])) / (float(y[i0]) - msl))
    # natural seabed slope seaward of the reef (toe -> toe + 100 m)
    yt = float(y[i1])
    j = int(np.argmin(np.abs(y - (yt + 100.0))))
    if abs(y[j] - (yt + 100.0)) < 1e-6 and np.isfinite(zs[j]):
        out['seabed_mean_slope_seaward_of_toe_100m'] = fmt_slope((float(zs[i1]) - float(zs[j])) / 100.0)
    return out


def alongshore_by_level(rx, RZ, foot, levels=HYPSO_LEVELS):
    return [alongshore_length(rx, RZ, foot, L) for L in levels]


# =====================================================================================================================
#                                                       MAIN
# =====================================================================================================================
import argparse
import datetime
import re
import sys

SLUGS_3D = list(ADAPTERS.keys())

# ---- which published sources each profile depends on (ids as used in the model's own provenance / METHODS_3D.md) -------
KEY_INPUTS = {
    'borth-coastal-defence-reef': [
        ('reef surface (exposed rock, LiDAR DSM) and water edge', ['lidar2022']),
        ('toe berm / blanket / armour design (crest +0.50/+1.00/+1.50 mODN, slopes 1:3-1:5, berm 1.35 m 1:1.5)', ['drg1020-1023']),
        ('seabed contours around the reefs (Fig. 2) and offshore gradient', ['hrpp576f2', 'emodnet']),
        ('datum / tide levels (MSL = +0.31 mODN estimate; LAT = -2.44 mODN)', ['ref3', 'ref4'])],
    'boscombe-surf-reef': [
        ('plan outline (2011-09-28 image) ', ['S1', 'S7']),
        ('survey plot: seabed and surveyed reef surface (Apr 2011), flank gradient', ['S2']),
        ('design crest +0.5 m ACD, tide levels (ACD), settlement', ['S3']),
        ('MSL above chart datum (1.40 m), Ordnance Datum link', ['S4']),
        ('beach profiles (landward seabed)', ['S13']),
        ('EMODnet slope extrapolation (y > 380 m)', ['S5', 'S14'])],
    'bunbury-airwave': [
        ('seabed: WA DoT 2009 airborne lidar, 10 m grid', ['S_lidar']),
        ('plan outline / position (shape.json trace)', ['S_shape']),
        ('base diameter 12 m, height 2.0 m, crest 1 m below surface at low tide', ['S_RWR', 'S_ABC19', 'S_Tracks19']),
        ('tidal planes and MSL = +0.1 m AHD', ['S_tide']),
        ('Navionics SonarChart seabed check', ['S_nav'])],
    'cables-reef-wa': [
        ('plan outline / design (Lyons 1992 design plan, Fig. A.2)', ['B2013']),
        ('Nov 1999 rock surface (840 soundings, AHD), 1998 pre-construction bed', ['DoT_FR']),
        ('seabed outside the survey (Perth_5m, AHD) and shoreline (0 m AHD contour)', ['DoT_5m']),
        ('datum: AHD = MSL 1966-68 = 0.716 m above Fremantle gauge zero', ['Roelse1975'])],
    'mount-maunganui-reef': [
        ('outline (-2.0 m CD contour, 18 Jul 2013 multibeam), crest -0.9 m CD, bed, volume 2,800 m3', ['R1', 'img1', 'ctx9']),
        ('chart datum / MSL / tide levels (LINZ Tauranga)', ['R6']),
        ('MVD-53 link', ['R5']),
        ('seabed profile outside the reef (Navionics SonarChart 2026)', ['N1'])],
    'narrowneck-gold-coast': [
        ('container field (2020-08-08 Esri aerial trace)', ['s3']),
        ('2017 multibeam seabed, Option 2 / 2004 designs, crest loops and -6 m envelope', ['cor23', 'jack12']),
        ('measured crest -2.2 m AHD (2017-18 renewal works), seabed labels', ['vds21']),
        ('tide planes (MSL = LAT + 0.88 m), AHD link', ['msq']),
        ('Navionics shoals (position check only)', ['s12'])],
    'palm-beach-gold-coast': [
        ('plan outline and survey contour lines read off the Bluecoast/Nearmap aerial', ['s7', 's1']),
        ('crest level -1.5 m (certified design/as-built)', ['p1']),
        ('Navionics SonarChart seabed iso-depth lines', ['n1']),
        ('tide planes (MSL = LAT + 0.88 m)', ['t1']),
        ('pre-reef City survey seabed check', ['s6'])],
    'prattes-reef-el-segundo': [
        ('plan outline (Skelly Engineering design drawing, 110 bags)', ['P1']),
        ('as-installed crest depth (-6 ft MLLW), bag size, dates', ['S10']),
        ('seabed: NOAA NGDC Santa Monica 1/3 arc-second NAVD88 DEM', ['S5']),
        ('tidal datums NOAA CO-OPS 9410840', ['S4'])],
    'southern-ocean-surf-reef-albany': [
        ('plan outline: Bluecoast final design (toe polygon)', ['design_plan']),
        ('crest levels -1.0 / -2.0 m AHD, volume 34,000 m3, rock layers', ['design_table', 'city_page']),
        ('seabed profile (design contours)', ['rhdhv2015', 'eia2018']),
        ('tides (LAT, MLLW, MHHW)', ['dot_tides', 'city_page'])],
}

STATIC_CITATIONS = {
    'cables-reef-wa': {
        'B2013': 'Blacka, M.J., Shand, T.D., Carley, J.T. and Mariani, A. (2013) A Review of Artificial Reefs for Coastal Protection in NSW. WRL Technical Report 2012/08 (final, 11 June 2013), UNSW Water Research Laboratory, for the NSW Office of Environment and Heritage. https://doi.org/10.4225/53/58e1dc7368c7a (Fig. A.2 p.93 reproduces Lyons (1992) design plan; Table 4.3 p.67 tide range 0.8 m). Read in Lior\'s copy in papers/ (intake note 05_qa/papers_intake/P8_blacka_2013.md); cited per 07_scale/shapes/cables-reef-wa/3d/METHODS_3D.md reference 1.',
        'DoT_FR': 'Department of Transport, Western Australia, Coastal Information Branch (file dated 2020-11-11) Bathymetry point data, Fremantle (FR) package, FR.zip: FR19980330_Reef_Single.txt (30 Mar 1998), FR19991122_Single.txt (22 Nov 1999), FR20020201_Single.txt (1 Feb 2002); single-beam, GDA94 / MGA 50, m AHD; licence CC BY 4.0. https://s3-ap-southeast-2.amazonaws.com/transport.wa/Bathymetry/PointData/FR.zip ; catalogue https://catalogue.data.wa.gov.au/dataset/dot-bathy ; accessed 2026-10-10 (per cables-reef-wa/3d/METHODS_3D.md reference 9).',
        'DoT_5m': 'Department of Transport, Western Australia (file dated 2020-11-11) Composite surface Perth_5m.tif (WA Bathymetry, 5 m cells, AHD); licence CC BY 4.0. https://s3-ap-southeast-2.amazonaws.com/transport.wa/Bathymetry/Rasters/Perth_5m.tif ; dataset https://catalogue.data.wa.gov.au/dataset/composite-surfaces-index ; accessed 2026-10-10 (per cables-reef-wa/3d/METHODS_3D.md reference 10).',
        'Roelse1975': 'Roelse, A., Granger, H.W. and Graham, J.W. (1975) The Adjustment of the Australian Levelling Survey 1970-1971. Division of National Mapping, Department of Minerals and Energy, Technical Report 12, 2nd edition, Canberra. Table 3 (Fremantle MSL 1966-68 = AHD 0.000 is 0.716 m above gauge zero). https://d28rz98at9flks.cloudfront.net/69874/Tech_Rep_DNM_012.pdf ; accessed 2026-10-13 (per cables-reef-wa/3d/METHODS_3D.md reference 13).'},
    'southern-ocean-surf-reef-albany': {
        'design_plan': 'Bluecoast Consulting Engineers (c. 2019). Southern Ocean Surf Reef design plan, via Raised Water Research. https://raisedwaterresearch.com/wp-content/uploads/2019/12/Souther-Ocean-Surf-Reef-Design-by-Bluecoast.png (registry img-11); per southern-ocean-surf-reef-albany/3d/METHODS_3D.md section 8.',
        'design_table': 'Bluecoast Consulting Engineers / City of Albany (n.d., c. 2020). Final Reef Design table. https://www.albany.wa.gov.au/Profiles/albany/Assets/ClientData/Surf_Reef/design.jpg (registry img-10); per METHODS_3D.md section 8.',
        'city_page': 'City of Albany (2026). Southern Ocean Surf Reef (SOSR), completed project page ("Design Aspects"). https://www.albany.wa.gov.au/council/projects/completed-projects/southern-ocean-surf-reef-sosr.aspx ; per METHODS_3D.md section 8.',
        'rhdhv2015': 'Royal HaskoningDHV (2015). Albany Artificial Surf Reef Feasibility Study, Middleton Beach, executive summary, 13 July 2015, report PA1039_RP150622, 2 pp. https://www.albany.wa.gov.au/documents/435/albany-artificial-surf-reef-feasibility-study-middleton-beach ; and Royal HaskoningDHV (2015) Option B "Long Right" reef design with depth contours, as reproduced by Raised Water Research, https://raisedwaterresearch.com/wp-content/uploads/2019/12/Albany-Model2.jpg (img-16); per METHODS_3D.md section 8.',
        'eia2018': 'BMT Western Australia Pty Ltd (2018). Middleton Beach Artificial Surf Reef Environmental Impact Assessment. Report 1345_001/1_Rev2, September 2018, for the City of Albany, 160 pp. https://epa.wa.gov.au/sites/default/files/Referral_Documentation/Environmental%20Impact%20Assessment_0.pdf (Fig 6.9 p.32; tides s.5 p.13); per METHODS_3D.md section 8.',
        'dot_tides': 'Western Australia Department of Transport and Bureau of Meteorology (2024). Tide Predictions by Location WA 2024, Albany (35 02 S 117 53 E, datum LAT). https://transport.wa.gov.au/mediaFiles/marine/MAR_P_2024_Tide_Predictions_by_Location_WA.PDF ; per METHODS_3D.md section 8.'},
}


def parse_md_tables(path):
    d = {}
    for line in open(path, encoding='utf-8'):
        if line.startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if len(cells) >= 2 and cells[0] and not set(cells[0]) <= set('-: '):
                d.setdefault(cells[0].strip('`*'), cells[1])
    return d


def resolve_citations(slug, m, ids):
    tbl = {}
    p = os.path.join(SHAPES, slug, '3d', 'METHODS_3D.md')
    if os.path.exists(p):
        tbl = parse_md_tables(p)
    ms = {}
    if isinstance(m.get('sources'), list):
        for s in m['sources']:
            c = s.get('citation') or s.get('title')
            if s.get('url') and c and s['url'] not in c:
                c = c + ' ' + s['url']
            ms[s['id']] = c
    out = {}
    for i in ids:
        c = STATIC_CITATIONS.get(slug, {}).get(i) or tbl.get(i) or ms.get(i)
        out[i] = c if c else 'citation not confirmed (id %s: see 07_scale/shapes/%s/3d/METHODS_3D.md and SOURCES_3D.md)' % (i, slug)
    return out


ANNUAL_RANGE_HALF = {'southern-ocean-surf-reef-albany': 0.69, 'bunbury-airwave': 0.60, 'cables-reef-wa': 0.57}   # half of the WA DoT/BoM 2026 predicted annual range (1.38, 1.20, 1.14 m), centred on MSL (08_paper/notes/tides_check.md)


def apply_annual_range(slug, planes):
    if slug in ANNUAL_RANGE_HALF:
        planes.pop('LWt', None); planes.pop('HWt', None)
        planes['ANN_LO'], planes['ANN_HI'] = -ANNUAL_RANGE_HALF[slug], ANNUAL_RANGE_HALF[slug]
    return planes


def tidal_planes(m):
    lst = None
    for key in ('levels', 'water_levels'):
        if isinstance(m.get(key), list):
            lst = m[key]
    if lst is None and isinstance(m.get('water'), dict):
        lst = m['water'].get('levels')
    out = {}
    for r in lst or []:
        k = r.get('id') or r.get('key')
        if k is not None and 'z' in r:
            out[k] = r['z']
    return out


def cables_true_shoreline_fn(ts):
    bx, by = math.radians(ts['x_bearing']), math.radians(ts['y_bearing'])
    ux = np.array([math.sin(bx), math.cos(bx)])      # east, north components of the model +x unit vector
    uy = np.array([math.sin(by), math.cos(by)])
    Ps = np.array([ts['dist_east_m'], 0.0])           # point on the 0 m AHD line, east of the anchor
    ds = np.array([math.sin(math.radians(ts['shore_bearing'])), math.cos(math.radians(ts['shore_bearing']))])
    ax0, ay0 = ts['anchor_model']
    xs, ys = Ps @ ux, Ps @ uy
    dxs, dys = ds @ ux, ds @ uy

    def f(x):
        x = np.asarray(x, float)
        return ay0 + ys + (x - ax0 - xs) / dxs * dys
    return f


def profile_range(seabed, x, y_lo_model, y_reef_hi):
    yy = np.arange(-300.0, 1000.0 + 1e-9, STEP)
    zs = seabed(np.full_like(yy, x), yy)
    ok = np.isfinite(zs)
    if not ok.any():
        raise RuntimeError('no seabed on line x=%s' % x)
    lo = max(float(yy[ok][0]), LAND_LIMIT)
    hi = min(float(yy[ok][-1]), y_reef_hi + PAD_SEA)
    return lo, hi


def line_points(s, x, y_anchor, d):
    """model (x, y) of the points at line coordinate s. Constant-x lines: d = None, s = model y. Oblique lines:
    point = (x, y_anchor) + (s - y_anchor) * d with d the unit offshore direction, so s is a true distance along the line
    that equals the model y at the anchor."""
    s = np.asarray(s, float)
    if d is None:
        return np.full_like(s, x), s
    return x + (s - y_anchor) * d[0], y_anchor + (s - y_anchor) * d[1]


def profile_range_dir(seabed, x, y_anchor, d, y_reef_hi):
    ss = np.arange(-300.0, 1000.0 + 1e-9, STEP)
    zs = seabed(*line_points(ss, x, y_anchor, d))
    ok = np.isfinite(zs)
    if not ok.any():
        raise RuntimeError('no seabed on line through x=%s' % x)
    return max(float(ss[ok][0]), LAND_LIMIT), min(float(ss[ok][-1]), y_reef_hi + PAD_SEA)


def line_block(label, x, layer, seabed, y_reef_hi, true_shore_fn=None, defn='', y_anchor=None, direction=None):
    """direction = None: constant-x line (model y axis). direction = (dx, dy) unit vector (offshore, dy > 0): oblique line
    through (x, y_anchor); 'offshore_m' is then the distance along the line, equal to the model y at the anchor."""
    rx, ry, RZf = layer['rx'], layer['ry'], layer['RZf']
    d = None if direction is None else np.asarray(direction, float) / np.hypot(*direction)
    if d is None:
        lo, hi = profile_range(seabed, x, 0.0, y_reef_hi)
    else:
        lo, hi = profile_range_dir(seabed, x, y_anchor, d, y_reef_hi)
    y = np.arange(math.ceil(lo), math.floor(hi) + 1e-9, STEP)
    xs_, ys_ = line_points(y, x, y_anchor, d)
    zs = seabed(xs_, ys_)
    zr = sample_reef(rx, ry, RZf, xs_, ys_)
    zr = np.where(np.isfinite(zs) & (zr - zs >= THK_MIN), zr, np.nan)
    met = line_metrics(y, zs, zr)
    blk = dict(definition=defn, x_line_m=round(float(x), 2), metrics=met)
    if d is not None:
        blk['oblique'] = dict(anchor_xy_m=[round(float(x), 2), round(float(y_anchor), 2)], direction_xy=[round(float(d[0]), 5), round(float(d[1]), 5)],
                              angle_from_model_y_deg=round(math.degrees(math.atan2(d[0], d[1])), 2),
                              note='offshore_m = distance along this line (m), equal to the model y at the anchor; x_line_m = anchor x')
    if met.get('reef_on_line'):
        pa = line_points([met['shoreward_toe_y_m'], met['seaward_toe_y_m']], x, y_anchor, d)
        blk['reef_run_xy_m'] = [[round(float(pa[0][k]), 2), round(float(pa[1][k]), 2)] for k in (0, 1)]
    prof = dict(offshore_m=[round(float(v), 2) for v in y], seabed_msl_m=rnd(zs), reef_msl_m=rnd(zr))
    if met.get('y_msl_crossing_m') is not None:
        prof['offshore_from_msl_line_m'] = [round(float(v) - met['y_msl_crossing_m'], 2) for v in y]
    if true_shore_fn is not None and d is not None:
        # line coordinate s where the line meets the derived shoreline y = f(x) (f is linear in x)
        g = [float(line_points(t, x, y_anchor, d)[1] - true_shore_fn(line_points(t, x, y_anchor, d)[0])) for t in (0.0, 1.0)]
        ysh = -g[0] / (g[1] - g[0])
        blk['derived_true_shoreline_y_at_line_m'] = round(ysh, 2)
        blk['derived_true_shoreline_note'] = 'line coordinate s (offshore_m) at which this line meets the fitted 0 m AHD line; distances along the line from it are shore-normal distances'
        prof['offshore_from_true_shoreline_m'] = [round(float(v) - ysh, 2) for v in y]
        if met.get('reef_on_line'):
            met['crest_distance_from_true_shoreline_m'] = round(met['crest_y_m'] - ysh, 2)
            met['seaward_toe_distance_from_true_shoreline_m'] = round(met['seaward_toe_y_m'] - ysh, 2)
    elif true_shore_fn is not None:
        ysh = float(true_shore_fn(x))
        blk['derived_true_shoreline_y_at_line_m'] = round(ysh, 2)
        prof['offshore_from_true_shoreline_m'] = [round(float(v) - ysh, 2) for v in y]
        if met.get('reef_on_line'):
            met['crest_distance_from_true_shoreline_m'] = round(met['crest_y_m'] - ysh, 2)
            met['seaward_toe_distance_from_true_shoreline_m'] = round(met['seaward_toe_y_m'] - ysh, 2)
    blk['profile'] = prof
    return blk


def layer_from(rx, ry, RZ, seabed, mask=None):
    X, Y, SB, TH, foot = footprint(rx, ry, RZ, seabed, mask)
    return dict(rx=rx, ry=ry, RZ=RZ, X=X, Y=Y, SB=SB, TH=TH, foot=foot, RZf=np.where(foot, RZ, np.nan))


def global_block(layer):
    cc = crest_and_centre(layer['rx'], layer['ry'], layer['RZ'], layer['X'], layer['Y'], layer['foot'])
    g = dict(
        crest_z_msl_m=round(cc['zmax'], 3), crest_x_m=round(cc['x_crest'], 2), crest_y_m=round(cc['y_crest'], 2),
        crest_height_above_seabed_m=round(float((layer['RZ'] - layer['SB'])[np.isclose(layer['X'], cc['x_crest']) & np.isclose(layer['Y'], cc['y_crest'])][0]), 3),
        crest_depth_below_msl_m=round(-cc['zmax'], 3),
        footprint_x_range_m=[round(v, 2) for v in cc['x_range']], footprint_y_range_m=[round(v, 2) for v in cc['y_range']],
        footprint_alongshore_span_m=round(cc['x_range'][1] - cc['x_range'][0] + cc['dx'], 2),
        footprint_cross_shore_span_m=round(cc['y_range'][1] - cc['y_range'][0] + cc['dx'], 2),
        footprint_area_m2_thickness_ge_0p10=round(cc['area_m2'], 1),
        footprint_centroid_xy_m=[round(cc['x_centroid'], 2), round(cc['y_centroid'], 2)],
        centreline_x_m=round(cc['x_centre'], 2),
        alongshore_length_z_ge_minus0p5_m_msl=alongshore_length(layer['rx'], layer['RZ'], layer['foot'], -0.5),
        alongshore_length_z_ge_crest_minus0p5=alongshore_length(layer['rx'], layer['RZ'], layer['foot'], cc['zmax'] - 0.5),
        alongshore_extent_by_level=alongshore_by_level(layer['rx'], layer['RZ'], layer['foot']),
    )
    return cc, g


def stated_volume(slug, m):
    """volume stated by the model for the default version (m3) and where it was read"""
    try:
        if slug == 'borth-coastal-defence-reef':
            v = next(v for v in m['versions'] if v['id'] == m['default_version'])
            return v['volume_m3'], 'model.js versions[lidar_2022].volume_m3 (both structures incl. toe berm and blanket)'
        if slug == 'boscombe-surf-reef':
            return m['stats']['idealised_volume_m3'], 'model.js stats.idealised_volume_m3'
        if slug == 'cables-reef-wa':
            v = next(v for v in m['versions'] if v['id'] == m['default_version'])
            return v['volume_m3'], 'model.js versions[survey_surface_1999_11].volume_m3'
        if slug == 'mount-maunganui-reef':
            v = next(v for v in m['versions'] if v['id'] == m['default_version'])
            return v['volume_m3_default'], 'model.js versions[multibeam_2013_m2p0].volume_m3_default (bed -3.6 m CD)'
        if slug == 'narrowneck-gold-coast':
            v = next(v for v in m['versions'] if v['id'] == m['default_version'])
            return v['volume_m3'], 'model.js versions[photo_2020-08-08].volume_m3'
        if slug == 'palm-beach-gold-coast':
            return m['reef']['stats']['volume_m3'], 'model.js reef.stats.volume_m3'
        if slug == 'prattes-reef-el-segundo':
            return m['stats'][m['reef']['default_state']]['volume_m3'], 'model.js stats[B].volume_m3'
        if slug == 'southern-ocean-surf-reef-albany':
            v = next(v for v in m['versions'] if v['id'] == m['default_version'])
            return v['volume_m3'], 'model.js versions[design_bluecoast].volume_m3 (fitted to the stated 34,000 m3)'
        if slug == 'bunbury-airwave':
            H, a0 = m['reef']['height_default_m'], 6.0
            return round(math.pi * H * (3 * a0 * a0 + H * H) / 6.0, 1), 'DERIVED analytic spherical-cap volume pi*H*(3a^2+H^2)/6 with a = 6 m, H = 2.0 m (no volume stated in the model)'
    except Exception as e:
        return None, 'not available (%s)' % e
    return None, 'not available'


def process(slug):
    m, mp = load_model(slug)
    a = ADAPTERS[slug](m, mp)
    seabed, rx, ry, RZ, meta = a['seabed'], a['rx'], a['ry'], a['RZ'], a['meta']
    layer = layer_from(rx, ry, RZ, seabed, a.get('mask'))
    cc, glob = global_block(layer)
    ts_fn = cables_true_shoreline_fn(a['true_shoreline']) if a.get('true_shoreline') else None
    lines = {
        'centreline': line_block('centreline', cc['x_centre'], layer, seabed, cc['y_range'][1], ts_fn,
                                 'cross-shore line (constant model x) at the alongshore mid-point of the reef footprint bounding box'),
        'crest_line': line_block('crest_line', cc['x_crest'], layer, seabed, cc['y_range'][1], ts_fn,
                                 'cross-shore line (constant model x) through the shallowest crest cell of the reef surface (ties within %.2f m: the cell nearest the middle of the shallowest plateau)' % TIE_TOL),
    }
    side_main_left = cc['x_crest'] < cc['x_centre']
    other = (layer['X'] >= cc['x_centre']) if side_main_left else (layer['X'] < cc['x_centre'])
    c2 = crest_cell(layer['X'], layer['Y'], layer['RZ'], layer['foot'] & other)
    if c2 is not None:
        lines['second_crest_line'] = line_block('second_crest_line', c2[0], layer, seabed, cc['y_range'][1], ts_fn,
                                                'cross-shore line through the shallowest reef cell on the OTHER side of the centreline than the main crest line (for two-arm reefs: the other arm); crest cell z = %.2f m MSL' % c2[2])
    ov = CUT_OVERRIDES.get(slug)
    if ov:
        if ov['anchor'] == 'centroid':
            xa, ya = cc['x_centroid'], cc['y_centroid']
        else:
            xa, ya = ov['anchor']
        if ov['normal'] == 'model_y':
            dvec = None
            ang = 0.0
        else:
            ts = a['true_shoreline']
            ob = None
            for b in (ov['normal'][1] - 90.0, ov['normal'][1] + 90.0):   # offshore side = positive model-y component
                v = (math.cos(math.radians(b - ts['x_bearing'])), math.cos(math.radians(b - ts['y_bearing'])))
                if v[1] > 0:
                    dvec, ob = v, b % 360
            ang = math.degrees(math.atan2(dvec[0], dvec[1]))
        lines['crest_line_auto'] = lines['crest_line']
        lines['crest_line_auto']['definition'] += ' [AUTOMATIC RULE, superseded for this reef by the override in crest_line; kept for reference, not used downstream]'
        nb = line_block('crest_line', xa, layer, seabed, cc['y_range'][1], ts_fn,
                        'SURF CUT (per-reef override of the automatic crest line): cross-shore line through (x %.1f, y %.1f) m, %s. Reason: %s' % (
                            xa, ya, 'along the model y axis (perpendicular to the shoreline)' if dvec is None else
                            'perpendicular to the shoreline (offshore bearing %.1f deg T, %.1f deg from the model y axis)' % (ob, ang), ov['reason']),
                        y_anchor=ya if dvec is not None else None, direction=dvec)
        nb['override'] = dict(reason=ov['reason'], anchor_xy_m=[round(float(xa), 2), round(float(ya), 2)],
                              angle_from_model_y_deg=round(ang, 2), offshore_bearing_deg_T=None if dvec is None else round(ob, 1),
                              automatic_line_x_m=lines['crest_line_auto']['x_line_m'])
        lines['crest_line'] = nb
    out = dict(
        slug=slug, name=m.get('name') or m.get('meta', {}).get('name'),
        generated=datetime.date.today().isoformat(),
        script='08_paper/analysis/extract_profiles.py',
        status='DERIVED: every number in "global", "lines" and "extra_layers" is computed by the script from the published 3D-model data (no new measurement); the model inputs and their sources are in "key_inputs" and in the model METHODS_3D.md.',
        version=dict(id=meta['version_id'], name=meta['version_name'], date=meta['version_date'], is_default_version=True),
        frame=meta['frame'], datum=meta['datum'], shoreline_definition=meta['shoreline_def'],
        units='metres; offshore_m = model y (distance from the model shoreline y = 0, positive offshore); elevations in metres above MSL (z up); x = alongshore model axis',
        method=dict(
            reef_surface=meta['reef_surface_def'], seabed=meta['seabed_def'],
            sampling=dict(step_m=STEP, interpolation='seabed: bilinear on the model grid / analytic profile; reef surface: NaN-aware (normalised) bilinear on the reef grid; profiles at constant model x',
                          footprint_rule='a reef cell belongs to the footprint if (reef surface - natural seabed) >= %.2f m (ASSUMPTION, avoids zero-thickness tapers)' % THK_MIN,
                          centreline='x = (x_min + x_max)/2 of the footprint', crest_line='x of the shallowest reef-surface cell',
                          crest_zone='contiguous points on the line within %.2f m of the line maximum (ASSUMPTION)' % CREST_TOL,
                          ramp='seaward ramp = from the seaward edge of the crest zone to the seaward end of the reef run (the toe); ramp_length = horizontal distance, ramp_rise = reef-surface drop over it, mean_seaward_slope = rise/length',
                          max_seaward_slope='maximum over the ramp of (z[y-%.0f m] - z[y+%.0f m]) / %.0f m (central difference, %.0f m baseline), tan, degrees and 1:n' % (SLOPE_HALF, SLOPE_HALF, 2 * SLOPE_HALF, 2 * SLOPE_HALF),
                          toe='seaward toe = most offshore point of the reef run (reef surface still >= %.2f m above the seabed); the reef elevation, seabed elevation and thickness there are reported (thickness > 0.5 m means the model surface is cut at its outline, not at the seabed)' % THK_MIN,
                          gap_bridging='gaps up to %.0f m along a line are bridged when forming the reef run (ASSUMPTION; only Narrowneck is affected)' % GAP_BRIDGE,
                          alongshore_length='span = x_max - x_min of footprint cells with reef surface >= level; union = number of x-columns containing such a cell * dx. Two levels are reported because "crest -0.5 m" is ambiguous: (a) z >= -0.5 m MSL and (b) z >= crest - 0.5 m',
                          offshore_distance='offshore_m is measured from the model shoreline y = 0 (definition in shoreline_definition); offshore_from_msl_line_m uses the first downward crossing of z = 0 (MSL) of the modelled natural seabed on the same line'),
        ),
        source_files=meta['source_files'] + ['08_paper/analysis/extract_profiles.py (this script, re-runnable: python3 extract_profiles.py)'],
        key_inputs=[dict(input=role, sources={i: c for i, c in resolve_citations(slug, m, ids).items()}) for role, ids in KEY_INPUTS[slug]],
        read_from='07_scale/shapes/%s/3d/model.js (read only)' % slug,
        caveats=meta['caveats'],
        tidal_planes_m_above_msl=apply_annual_range(slug, tidal_planes(m)),
        confidence_3d=m.get('confidence_3d', {}).get('level') if isinstance(m.get('confidence_3d'), dict) else None,
        global_=glob, lines=lines,
    )
    if ov:
        out['method']['sampling']['crest_line'] += ' -- OVERRIDDEN for this reef by a per-reef SURF CUT (CUT_OVERRIDES, Lior 2026-10-19); definition and reason in lines.crest_line.definition / .override; the automatic line is lines.crest_line_auto'
    if 'region_masks' in meta:
        out['region_masks'] = meta['region_masks']
    SBg = layer['SB']
    dxg = float(rx[1] - rx[0])
    dyg = float(ry[1] - ry[0])
    vol = float(np.nansum(np.clip(RZ - SBg, 0, None)) * dxg * dyg)
    sv, svsrc = stated_volume(slug, m)
    out['reconstruction_check'] = dict(
        what='volume of the reef grid read here (sum of max(reef - seabed, 0) over all finite reef cells, no thickness threshold, seabed from this script) against the volume stated by the model for the same version; a check that the surface was reconstructed as the viewer draws it',
        volume_recomputed_m3=round(vol, 0), volume_stated_m3=sv, stated_source=svsrc,
        ratio_recomputed_to_stated=None if not sv else round(vol / sv, 3),
        max_reef_z_msl_m=round(float(np.nanmax(RZ)), 3))
    if a.get('secondary'):
        sec = a['secondary']
        lay2 = layer_from(rx, ry, RZ, seabed, sec['mask'])
        cc2, g2 = global_block(lay2)
        out['secondary_structure'] = dict(name=sec['name'], global_=g2, crest_line=line_block('crest_line', cc2['x_crest'], lay2, seabed, cc2['y_range'][1], None, 'cross-shore line through the highest cell of the secondary structure'))
    # extra layers (evidence / alternative surfaces), same lines
    extras = []
    for ex in a.get('extra_layers', []):
        exrx = ex.get('rx', rx)
        exry = ex.get('ry', ry)
        lay = layer_from(exrx, exry, ex['RZ'], seabed, a.get('mask'))
        if not lay['foot'].any():
            continue
        cc_e, g_e = global_block(lay)
        blk = dict(name=ex['name'], note=ex['note'], is_default_version=False, global_=g_e, lines={})
        for nm, xl in (('centreline', cc['x_centre']), ('crest_line', cc['x_crest']), ('own_crest_line', cc_e['x_crest'])):
            if nm == 'own_crest_line' and abs(cc_e['x_crest'] - cc['x_crest']) < 0.51:
                continue
            blk['lines'][nm] = line_block(nm, xl, lay, seabed, cc_e['y_range'][1], ts_fn, 'same definition as the default layer' if nm != 'own_crest_line' else 'cross-shore line through the shallowest crest cell of THIS layer')
        extras.append(blk)
    if extras:
        out['extra_layers'] = extras
    out['global'] = out.pop('global_')
    return out, layer


def fix_keys(o):
    """json: rename 'global_' keys (used to avoid the keyword) to 'global'"""
    if isinstance(o, dict):
        return {('global' if k == 'global_' else k): fix_keys(v) for k, v in o.items()}
    if isinstance(o, list):
        return [fix_keys(v) for v in o]
    return o


def jdefault(o):
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(type(o))


# ---- reefs without a 3D model: what the cards / FEASIBILITY give ---------------------------------------------------
def non3d_records():
    P = 'Taranaki Regional Council (2009). Opunake Artificial Reef Monitoring Programme 2005-2009. Technical Report 2009-33 (ISSN 0114-8184; document 631513). Stratford, NZ, September 2009, 58 pp. (Lior\'s copy: new uploads from lior/Opunake Artificial Reef monitoring programme 2005-2009.pdf)'
    BL = 'Blacka, M.J., Shand, T.D., Carley, J.T. and Mariani, A. (2013). A Review of Artificial Reefs for Coastal Protection in NSW. WRL Technical Report 2012/08, UNSW Water Research Laboratory, for NSW Office of Environment and Heritage. https://doi.org/10.4225/53/58e1dc7368c7a (report page = PDF page - 12)'
    MB = 'Mead, S.T. and Borrero, J.C. (2011). Multi-Purpose Reefs - A Decade of Applications. Proc. 20th Australasian Coastal and Ocean Engineering Conference (Coasts and Ports 2011), ASR Ltd. https://search.informit.org/doi/10.3316/informit.715072832934166'
    return {
        'kovalam-reef-india': dict(
            name='Kovalam Reef (Lighthouse Beach, Kerala, India)', has_3d_model=False,
            crest_depth='unknown as a located value. Range only: "submergence 0.2-3.4 m", datum not stated, not tied to any position on the reef (Blacka et al. 2013, Table 4.2, report p.66)',
            toe_depth='unknown. Water depth at the reef "1.3-3.7 m" (a range, datum not stated) (Blacka et al. 2013, Table 4.2, report p.66)',
            size='plan 65 m longshore x 85 m cross-shore, 90 m offshore (Blacka et al. 2013, Table 4.2 p.66); volume 4,000 m3 (Mead and Borrero 2011, p.4), 4,300 m3 (Rendle 2016 Table 2.1 p.41), 4,800 m3 (RWR / ICM); 30 m long sand-container units. Project trace of the oblique photo: 59 x 41 m default, 546-1,681 m2 depending on the assumed camera height (LOW confidence; 07_scale/shapes/kovalam-reef-india/FEASIBILITY.md)',
            ramp_slope='unknown', alongshore_length='65 m (Blacka et al. 2013 Table 4.2: longshore dimension); trace 59 m (LOW)',
            tide='tide range about 1.0 m (Blacka et al. 2013 Table 4.3 p.68)',
            sources=[BL, MB, 'Rendle, E.J. (2016). The Environmental, Social and Economic Impacts of an Artificial Surf Reef - The UK Experience. PhD thesis, University of Plymouth, Table 2.1 printed p.41 (Lior\'s copy in papers/)'],
            read_from='07_scale/shapes/kovalam-reef-india/FEASIBILITY.md; 02_research/reefs/kovalam-reef-india.json (size, references R13, R14, R15)',
            why_no_profile='3D model not built: crest and seabed are single unlocated ranges without datum, plan scale only estimated (FEASIBILITY.md 2026-10-10). Structure later sank and deflated.'),
        'opunake-reef': dict(
            name='Opunake Reef (north reef, Taranaki, New Zealand)', has_3d_model=False,
            crest_depth='shallowest contour 0.0 m below chart datum (chart datum = LAT) (design, consent stage; TRC 2009 printed p.3). Relative to MSL: not converted (no tide level with datum fetched; Blacka 2013 Table 4.3 tide range > 3.0 m)',
            toe_depth='built in 3.0 to 1.8 m of water below chart datum (LAT) on a thin sand layer over rock, no excavation (TRC 2009 printed pp.3-4; Blacka 2013 Table 4.2 p.65: depth 1.8-3.0 m)',
            size='design about 99 m long x 30 m wide x 3.5 m high, plan area about 2,970 m2 (a bounding rectangle 99 x 30, not the true footprint), volume about 4,900 m3 (TRC 2009 printed p.4); Blacka 2013 Table 4.2: 30 m longshore x 100 m cross-shore, ~300 m offshore; 27 bags in place by April 2008, structure not completed (Sept 2009)',
            ramp_slope='unknown (no cross-section)', alongshore_length='design long axis 99 m, bearing 63 deg (occupation area 189 x 94 m rectangle); true footprint unknown',
            tide='tide range > 3.0 m (Blacka et al. 2013 Table 4.3)',
            sources=[P, BL],
            read_from='07_scale/shapes/opunake-reef/FEASIBILITY.md; 02_research/reefs/opunake-reef.json (size, references R18, R14)',
            why_no_profile='3D model not built: no bag layout, no per-bag crest levels, no surveyed seabed (FEASIBILITY.md 2026-10-13).'),
        'burkitts-reef-bargara': dict(
            name='Burkitts Reef (Bargara, Queensland, Australia)', has_3d_model=False,
            crest_depth='unknown (no crest or minimum-depth figure found; natural basalt platform awash/exposed on satellite at unknown tide)',
            toe_depth='unknown (dive-site depth "to ~9 m" is a site-wide maximum, not a profile; not used)',
            size='about 300 m3 of rock moved, at least 12 large basalt boulders relocated (RWR Burkitts Reef page; Swellnet comment 2022); traced natural basalt platform 31,485 m2 minimum (321 x 377 m, Esri 2025-09-05, LOW confidence) which is NOT the reshaped zone; Redgard Phase 3 work-zone ellipse about 1,750 m2 (43 x 52 m, +-20-30 m, LOW)',
            ramp_slope='unknown', alongshore_length='unknown (reef zone not located)',
            tide='about 2.5 m swing (no datum); MSQ 2026 planes Burnett Heads: MHWS 2.94, MHWN 2.35, MLWN 1.20, MLWS 0.61, MSL 1.78, HAT 3.68 m above LAT',
            sources=['Raised Water Research (n.d.). "Burkitts Reef" [spot page, artificial-reef database]. https://raisedwaterresearch.com/spot/artificial-reef/australia/queensland/burkitts-reef/ (accessed 2026-09-24)', 'Swellnet comment thread, user truebluebasher, 2022-06-02. https://www.swellnet.com/comments/get/540429'],
            read_from='07_scale/shapes/burkitts-reef-bargara/FEASIBILITY.md; 02_research/reefs/burkitts-reef-bargara.json (size; references R4, R8)',
            why_no_profile='3D model not built: only a low-confidence outline of the natural platform exists; crest and seabed are missing (FEASIBILITY.md 2026-10-10). Natural boulder headland reshaped in place, not an engineered structure.'),
        'mexico-reef-2026-unnamed': dict(
            name='Xala Reef (Costalegre, Jalisco, Mexico; card name "Mexico reef 2026")', has_3d_model=False,
            crest_depth='unknown (not disclosed in any source)', toe_depth='unknown',
            size='not disclosed; "3,000 truckloads" of quarried boulders (Hollywood Reporter 2025-04-22). The 160 x 80 m analogy envelope in 07_scale/reefs/ and Gemini\'s ~140 x 75 m are unsourced and not used',
            ramp_slope='unknown', alongshore_length='unknown', tide='unknown (Manzanillo/Cuyutlan tide not fetched)',
            sources=['Romeyn, K. (2025-04-22). With Xala, Richard Gere has Co-Founded a Luxury Mexican Paradise. The Hollywood Reporter. https://www.hollywoodreporter.com/lifestyle/lifestyle-news/xala-richard-gere-luxury-mexican-paradise-1236192415/', 'Indelicato, P. (2026-03-31). Unveiling the new reef in Mexico. Raised Water Research (announcement). https://raisedwaterresearch.com/unveiling-the-new-reef-in-mexico/'],
            read_from='07_scale/shapes/mexico-reef-2026-unnamed/FEASIBILITY.md; 02_research/reefs/mexico-reef-2026-unnamed.json (size; references R1, R3)',
            why_no_profile='no plan, no coordinates, no dimensions, no image of the structure (FEASIBILITY.md 2026-10-10).'),
    }


def fmt(v, nd=2, none='n/a'):
    return none if v is None else (('%.' + str(nd) + 'f') % v)


def summary_rows(results):
    rows = []
    for slug, r in results.items():
        g = r['global']
        for ln in ('crest_line', 'centreline'):
            L = r['lines'][ln]['metrics']
            if not L.get('reef_on_line'):
                continue
        L = r['lines']['crest_line']['metrics']
        C = r['lines']['centreline']['metrics']
        rows.append((slug, r, g, L, C))
    return rows


def slope_txt(s, deg=True):
    if not s or not s.get('one_in'):
        return 'n/a'
    return ('1:%.1f (%.1f deg)' % (s['one_in'], s['deg'])) if deg else ('1:%.1f' % s['one_in'])


SHORELINE_TXT = {
    'borth-coastal-defence-reef': 'defence line (back of shingle beach), not the MSL line',
    'boscombe-surf-reef': 'surf line of 2011-09-28 (about 8 m seaward of the MSL line)',
    'bunbury-airwave': 'fitted 0 m AHD contour (about MSL)',
    'cables-reef-wa': 'nominal design-frame origin, NOT the shoreline (fitted 0 m AHD line about 254 m E of the reef centroid; derived distance given)',
    'mount-maunganui-reef': 'wet/dry sand line = MSL line of the model',
    'narrowneck-gold-coast': 'waterline of Esri 2020-08-08 image',
    'palm-beach-gold-coast': 'waterline of Esri 2025-12-01 taken as MSL',
    'prattes-reef-el-segundo': 'MSL waterline (z = 0 of the DEM profile)',
    'southern-ocean-surf-reef-albany': 'beach-face line (edge of dry sand); MSL line 5 m landward'}


def write_summary(results, non3d, path):
    t = []
    A = t.append
    A('# Cross-shore profiles of the reefs - SUMMARY\n')
    A('Generated %s by `08_paper/analysis/extract_profiles.py` (re-runnable) from the DEFAULT version of each 3D model in `07_scale/shapes/<slug>/3d/model.js` (read only). One JSON per reef with a 3D model: `08_paper/data/profiles/<slug>.json` (metadata, datum, shoreline definition, profiles every %.0f m on two or three lines, metrics, sources, caveats); the four reefs without a 3D model: `08_paper/data/profiles/_no_3d_model.json`.\n' % (datetime.date.today().isoformat(), STEP))
    A('Every number for the nine modelled reefs is **DERIVED** from the model grids by the method stated here and in each JSON (not a new measurement). The inputs behind each model and their sources are cited in the JSON field `key_inputs` and in `07_scale/shapes/<slug>/3d/METHODS_3D.md`. The re-implemented reef surfaces reproduce the volumes stated by the models to within 1 % (JSON `reconstruction_check`). z = metres above MSL (each model\'s datum link is in the JSON field `datum`); y = offshore distance from the model shoreline y = 0 (defined differently per reef, see section 2).\n')
    A('## 1. Master table, all reefs (default version; crest-line profile)\n')
    A('Crest line = cross-shore line (constant model x) through the shallowest crest cell, EXCEPT for the reefs in section 1a, where a per-reef SURF CUT replaces it (Lior 2026-10-19). Ramp = seaward face from the seaward edge of the crest zone (points within 0.10 m of the line maximum) to the seaward toe (last point where the reef is at least 0.10 m above the natural seabed). Mean slope = ramp drop / ramp length; max slope = steepest 2 m central difference on the ramp. Crest depth below MSL is negative where the crest is above MSL (Borth). "(cut)" = the model surface stops at its outline with more than 0.5 m of reef still standing, so the toe is not where the surface meets the seabed. Alongshore length = x-span of reef cells at or above the level: (a) -0.5 m MSL, (b) 0.5 m below the crest (the request "at crest -0.5 m" is ambiguous, both given).\n')
    A('| Reef | Version / basis | Crest z (m MSL) | Crest depth below MSL (m) | Crest height above bed (m) | Crest distance offshore (m) | Toe z reef / bed (m MSL) | Drop crest to toe, on reef / to bed (m) | Ramp length (m) | Mean seaward slope | Max seaward slope | Alongshore length (a) z>=-0.5 m / (b) z>=crest-0.5 m (m) |')
    A('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for slug, r, g, L, C in summary_rows(results):
        if not L.get('reef_on_line'):
            A('| %s | %s | no reef on line |' % (slug, r['version']['id']))
            continue
        al_abs = g['alongshore_length_z_ge_minus0p5_m_msl']['span_m']
        al_rel = g['alongshore_length_z_ge_crest_minus0p5']['span_m']
        if L.get('crest_distance_from_msl_line_m') is not None:
            dist = '%.0f from MSL line (y=%.0f)' % (L['crest_distance_from_msl_line_m'], L['crest_y_m'])
        elif L.get('crest_distance_from_true_shoreline_m') is not None:
            dist = '~%.0f from fitted shoreline (derived; y=%.0f)' % (L['crest_distance_from_true_shoreline_m'], L['crest_y_m'])
        else:
            dist = 'y=%.0f' % L['crest_y_m']
        cut = ' (cut)' if L['seaward_toe_thickness_m'] > 0.5 else ''
        A('| **%s** | %s | %s | %s | %s | %s | %s / %s%s | %s / %s | %s | %s | %s | %s / %s |' % (
            slug, r['version']['id'], fmt(L['crest_z_msl_m']), fmt(L['crest_depth_below_msl_m']), fmt(L['crest_height_above_seabed_m']), dist,
            fmt(L['seaward_toe_reef_z_msl_m']), fmt(L['seaward_toe_seabed_z_msl_m']), cut, fmt(L['crest_to_toe_drop_m']), fmt(L['crest_to_toe_seabed_drop_m']), fmt(L['ramp_length_m'], 0),
            slope_txt(L['mean_seaward_slope']), slope_txt(L['max_seaward_slope']),
            'none' if al_abs is None else '%.0f' % al_abs, 'n/a' if al_rel is None else '%.0f' % al_rel))
    for slug, d in non3d.items():
        A('| **%s** | no 3D model (card / FEASIBILITY) | unknown as a located value | %s | unknown | unknown | toe/bed: %s | unknown | unknown | unknown | unknown | %s |' % (
            slug, d['crest_depth'], d['toe_depth'], d['alongshore_length']))
    A('\n### 1a. Per-reef surf cuts (override of the automatic crest line; Lior 2026-10-19)\n')
    A('For these reefs the automatic crest line does not cross the part of the reef where the wave breaks and is surfed, or is not perpendicular to the local shoreline. The row above (and `lines.crest_line` in the JSON, used by every downstream script) is the SURF CUT: a line through the stated anchor, perpendicular to the shoreline, sampled every %.0f m by the same bilinear interpolation on the model grids. The automatic line stays in the JSON as `lines.crest_line_auto` (reference only).\n' % STEP)
    A('| Reef | Automatic line x (m) | Surf cut anchor (x, y) (m) | Cut direction | Reason |')
    A('|---|---|---|---|---|')
    for slug, r in results.items():
        o = r['lines']['crest_line'].get('override')
        if not o:
            continue
        dtxt = 'model y axis (shore-normal frame)' if o['offshore_bearing_deg_T'] is None else 'offshore bearing %.1f deg T (%.1f deg from model y)' % (o['offshore_bearing_deg_T'], o['angle_from_model_y_deg'])
        A('| %s | %.1f | %.1f, %.1f | %s | %s |' % (slug, o['automatic_line_x_m'], o['anchor_xy_m'][0], o['anchor_xy_m'][1], dtxt, o['reason']))
    A('\nSizes of the four reefs without a 3D model (card / FEASIBILITY values, full citations in `_no_3d_model.json`):\n')
    for slug, d in non3d.items():
        A('* **%s**: %s. Read in: %s.' % (slug, d['size'], d['read_from']))
    A('\n## 2. Datum and shoreline definition per reef (what "offshore distance" is measured from)\n')
    A('| Reef | y = 0 (model shoreline) is | z = 0 is | Seabed under the reef |')
    A('|---|---|---|---|')
    for slug, r in results.items():
        A('| %s | %s | %s | %s |' % (slug, SHORELINE_TXT[slug], r['datum'].split(';')[0], r['method']['seabed'].split(':')[0][:120]))
    A('\nFull wording of datum, frame, shoreline, reef-surface rule and seabed per reef: JSON fields `datum`, `frame`, `shoreline_definition`, `method.reef_surface`, `method.seabed`, `caveats`.\n')
    A('## 3. Centreline (x at the alongshore mid-point of the footprint) and second crest line\n')
    A('| Reef | Line | x (m) | crest z (m MSL) | crest y (m) | seaward toe y (m) | toe z reef / bed (m MSL) | thickness at toe (m) | ramp length (m) | mean seaward slope | max seaward slope | seabed slope MSL line to seaward toe | seabed slope under reef |')
    A('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for slug, r, g, L, C in summary_rows(results):
        for ln in ('centreline', 'second_crest_line'):
            S = r['lines'].get(ln)
            if not S:
                continue
            M2 = S['metrics']
            if not M2.get('reef_on_line'):
                A('| %s | %s | %s | no reef on line | | | | | | | | | |' % (slug, ln, fmt(S['x_line_m'], 1)))
                continue
            sl = M2.get('seabed_mean_slope_msl_line_to_seaward_toe')
            su = M2.get('seabed_mean_slope_under_reef')
            A('| %s | %s | %s | %s | %s | %s | %s / %s | %s | %s | %s | %s | %s | %s |' % (
                slug, ln, fmt(S['x_line_m'], 1), fmt(M2['crest_z_msl_m']), fmt(M2['crest_y_m'], 0), fmt(M2['seaward_toe_y_m'], 0), fmt(M2['seaward_toe_reef_z_msl_m']), fmt(M2['seaward_toe_seabed_z_msl_m']),
                fmt(M2['seaward_toe_thickness_m']), fmt(M2['ramp_length_m'], 0), slope_txt(M2['mean_seaward_slope'], False), slope_txt(M2['max_seaward_slope'], False),
                ('1:%.0f' % sl['one_in']) if sl and sl.get('one_in') else 'n/a', ('1:%.0f' % su['one_in']) if su and su.get('one_in') else 'n/a'))
    A('\nFor two-arm reefs (Cables, Mount Maunganui, Narrowneck, Prattes) the centreline passes through the apex block or the gap between the arms and the second crest line is the other arm; for single-body reefs the second crest line lies next to the centreline. See JSON `caveats`.\n')
    A('## 4. Alongshore extent of the reef above given levels (union length of x-columns, m)\n')
    lv = HYPSO_LEVELS
    A('| Reef | ' + ' | '.join('z>=%+.1f' % v for v in lv) + ' |')
    A('|---|' + '---|' * len(lv))
    for slug, r, g, L, C in summary_rows(results):
        A('| %s | ' % slug + ' | '.join(('-' if e['union_m'] is None else '%.0f' % e['union_m']) for e in g['alongshore_extent_by_level']) + ' |')
    A('\nLevels are metres above MSL; "-" = no reef cell that shallow. Borth counts the northern surf reef only (the southern oval is a shore-parallel breakwater, reported separately in its JSON under `secondary_structure`). Both readings of "alongshore length at crest -0.5 m" are in each JSON: `global.alongshore_length_z_ge_minus0p5_m_msl` and `global.alongshore_length_z_ge_crest_minus0p5` (span and union).\n')
    A('## 5. Evidence layers and alternative surfaces (not the default; own crest line)\n')
    A('| Reef | Layer | crest z (m MSL) | crest height above bed (m) | seaward toe thickness (m) | ramp length (m) | mean seaward slope | max seaward slope | note |')
    A('|---|---|---|---|---|---|---|---|---|')
    for slug, r in results.items():
        for ex in r.get('extra_layers', []):
            S = ex['lines'].get('own_crest_line') or ex['lines'].get('crest_line')
            M2 = S['metrics']
            if not M2.get('reef_on_line'):
                continue
            A('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (slug, ex['name'], fmt(M2['crest_z_msl_m']), fmt(M2['crest_height_above_seabed_m']), fmt(M2['seaward_toe_thickness_m']), fmt(M2['ramp_length_m'], 0),
                  slope_txt(M2['mean_seaward_slope'], False), slope_txt(M2['max_seaward_slope'], False), ex['note'][:160]))
    A('\n## 6. Reading guide and caveats common to all reefs\n')
    A('* **What is survey and what is a rule**: Cables (Nov 1999 sounding surface), Borth (2022 LiDAR DSM) and Mount Maunganui (rise inside the -2.0 m CD contour from the 2013 DEM) carry survey information; Boscombe (flat crest, 1:3 flanks), Prattes (constant 1.35 m stack, 1:1 flanks), Bunbury (spherical cap), Palm Beach (contour interpolation), Narrowneck and Albany (design-surface rules) are idealised. Ramp lengths and slopes are model results and inherit these assumptions; the surfaces were not re-measured.')
    A('* **Seabed**: the natural seabed under each reef is interpolated (a pre-construction survey exists only for Cables, 1998). Mount Maunganui uses an ASSUMED as-built bed of -3.6 m CD; Palm Beach and Narrowneck rely on Navionics/multibeam with datum assumptions. Crest HEIGHT and ramp slopes depend on these; crest LEVEL is sourced for Mount Maunganui, Boscombe, Palm Beach, Prattes and Albany (design or stated values), surveyed for Cables and Borth.')
    A('* **Slopes are along the model y axis** (the cross-shore direction of the model frame). For oblique ridges (Albany, Boscombe, Borth boot) the slope normal to the crest differs; for Cables the frame axis is about 17.5 deg off the shore normal, so the Cables surf cut (crest_line) is turned 17.5 deg to the shore normal and its distances are along that line; the centreline and second crest line of Cables still follow the frame axis.')
    A('* **Tidal planes** (m above MSL, small-tide sites): JSON field `tidal_planes_m_above_msl`.')
    A('* **JSON layout**: `lines.<name>.profile.{offshore_m, seabed_msl_m, reef_msl_m}` are equal-length arrays at 1 m spacing (`null` = no reef / no data); `lines.<name>.metrics` are the numbers above; `global` holds crest, footprint and alongshore extents; `extra_layers` holds the evidence layers; `reconstruction_check` the volume test.')
    open(path, 'w', encoding='utf-8').write('\n'.join(t) + '\n')


def check_plots(results, outdir):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except Exception as e:                       # plots are optional
        print('matplotlib unavailable, no check plots:', e)
        return
    os.makedirs(outdir, exist_ok=True)
    for slug, r in results.items():
        fig, axs = plt.subplots(1, 2, figsize=(13, 3.6), sharey=True)
        for axx, ln in zip(axs, ('centreline', 'crest_line')):
            L = r['lines'][ln]
            p = L['profile']
            y = np.array(p['offshore_m'], float)
            zs = np.array([np.nan if v is None else v for v in p['seabed_msl_m']])
            zr = np.array([np.nan if v is None else v for v in p['reef_msl_m']])
            axx.plot(y, zs, color='saddlebrown', lw=1.2, label='natural seabed')
            axx.plot(y, zr, color='crimson', lw=1.8, label='reef surface')
            axx.axhline(0, color='teal', lw=0.6)
            met = L['metrics']
            if met.get('reef_on_line'):
                axx.plot([met['crest_y_m']], [met['crest_z_msl_m']], 'k^')
                axx.plot([met['seaward_toe_y_m']], [met['seaward_toe_reef_z_msl_m']], 'kv')
                lo, hi = met['shoreward_toe_y_m'] - 60, met['seaward_toe_y_m'] + 60
                axx.set_xlim(max(lo, y[0]), min(hi, y[-1]))
            axx.set_title('%s: %s x=%.1f m' % (slug, ln, L['x_line_m']), fontsize=8)
            axx.set_xlabel('offshore y (m)')
            axx.grid(alpha=0.3)
        axs[0].set_ylabel('z (m MSL)')
        axs[0].legend(fontsize=7)
        fig.tight_layout()
        fig.savefig(os.path.join(outdir, 'check_%s.png' % slug), dpi=70)
        plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__ if __doc__ else None)
    ap.add_argument('--out', default=os.path.join(REPO, '08_paper', 'data', 'profiles'))
    ap.add_argument('--plots', default=None, help='directory for quick-check PNGs (use a temp dir, not the repo)')
    ap.add_argument('--only', default=None)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    results = {}
    for slug in SLUGS_3D:
        if args.only and slug != args.only:
            continue
        r, _ = process(slug)
        r = fix_keys(r)
        results[slug] = r
        json.dump(r, open(os.path.join(args.out, slug + '.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=jdefault)
        L = r['lines']['crest_line']['metrics']
        print('%-34s crest %+.2f m MSL at y=%.0f; toe y=%.0f; ramp %.0f m' % (slug, L['crest_z_msl_m'], L['crest_y_m'], L['seaward_toe_y_m'], L['ramp_length_m']))
    non3d = non3d_records()
    json.dump(dict(generated=datetime.date.today().isoformat(), note='Reefs without a 3D model: only what the reef cards and FEASIBILITY files give; "unknown" where no source gives a value. No profile arrays.', reefs=non3d),
              open(os.path.join(args.out, '_no_3d_model.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    if not args.only:
        write_summary(results, non3d, os.path.join(args.out, 'SUMMARY.md'))
    if args.plots:
        check_plots(results, args.plots)


if __name__ == '__main__':
    main()
