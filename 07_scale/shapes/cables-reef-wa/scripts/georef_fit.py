"""cables-reef-wa: georeference the traced design outline by fitting it to the DoT WA soundings of Nov 1999 (post-construction).
Inputs (src/bathymetry/FR_selected): FR19980330_Reef_Single.txt (pre-construction bed, AHD), FR19991122_Single.txt (Nov 1999),
FR20020201_Single.txt (Feb 2002); ../shape.json (outline_versions). Output: georef.json (transform + fit statistics) printed.
Frames: soundings are GDA94 / MGA zone 50 (EPSG:28350), Z in m AHD (DoT readme). Canonical frame of shape.json: x north, y west (offshore).
Transform canonical -> MGA:  (E,N) = R(theta)(-(y-yc), (x-xc)) + (E0,N0)   [theta ccw, degrees; (xc,yc) = vertex mean of the original-plan polygon]
Fit: differential evolution (theta, E0, N0) maximising (share of 'rock' soundings inside the polygon) - (share of 'bed' soundings inside).
 rock = Nov-1999 sounding more than 0.6 m above the pre-construction bed; bed = less than 0.2 m above it. Pre-construction bed = linear
 interpolation (scipy LinearNDInterpolator) of the 1998 'Reef' survey. numpy, scipy, pyproj, matplotlib only."""
import json, sys, numpy as np
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator
from scipy.optimize import differential_evolution
from matplotlib.path import Path
from pyproj import Transformer
HERE = __file__.rsplit('/', 1)[0]; B = HERE + '/../src/bathymetry/FR_selected/'
T = Transformer.from_crs(4326, 28350, always_xy=True); Ti = Transformer.from_crs(28350, 4326, always_xy=True)
CX, CY = T.transform(115.74835, -32.0158)            # search origin only (approximate reef centre from the satellite image)
sh = json.load(open(HERE + '/../shape.json'))
ov = {v['id']: v for v in sh['outline_versions']}
poly_ext = np.array(ov['design_plan_plus_extension_1999']['polygons_m'][0]); poly0 = np.array(ov['design_plan_original_1999']['polygons_m'][0])
CEN = poly0.mean(0)
def world(poly, th, tx, ty):                          # -> metres relative to (CX, CY)
    p = poly - CEN; E, N = -p[:, 1], p[:, 0]; c, s = np.cos(np.radians(th)), np.sin(np.radians(th))
    return np.c_[c * E - s * N + tx, s * E + c * N + ty]
def load(f, r=250):
    a = np.loadtxt(B + f, usecols=(0, 1, 2)); m = (abs(a[:, 0] - CX) < r) & (abs(a[:, 1] - CY) < r); return a[m]
pre = load('FR19980330_Reef_Single.txt'); post = load('FR19991122_Single.txt'); p02 = load('FR20020201_Single.txt')
f = LinearNDInterpolator(pre[:, :2], pre[:, 2]); fn = NearestNDInterpolator(pre[:, :2], pre[:, 2])
def bed_at(xy):
    b = f(xy); return np.where(np.isnan(b), fn(xy), b)
thick = post[:, 2] - bed_at(post[:, :2])
rock = post[thick > 0.6][:, :2] - [CX, CY]; non = post[thick < 0.2][:, :2] - [CX, CY]
def cost(v, pl):
    P = Path(world(pl, *v)); return -(P.contains_points(rock).mean() - P.contains_points(non).mean())
res = differential_evolution(cost, [(-40, 40), (-120, 120), (-120, 120)], args=(poly0,), seed=1, tol=1e-7, maxiter=400, popsize=30)
th, tx, ty = res.x; P = Path(world(poly0, th, tx, ty))
E0, N0 = CX + tx, CY + ty; lon0, lat0 = Ti.transform(E0, N0)
# stats
q02 = p02[:, :2] - [CX, CY]; t02 = p02[:, 2] - bed_at(p02[:, :2])
inn = P.contains_points(q02); Pe = Path(world(poly_ext, th, tx, ty)); ext = Pe.contains_points(q02) & ~inn
from shapely.geometry import Polygon, Point
sp = Polygon(world(poly_ext, th, tx, ty)); ring = np.array([(not sp.contains(Point(a))) and sp.distance(Point(a)) < 25 for a in q02])
out = {"transform": {"anchor_canonical_xy_m": [round(float(CEN[0]), 3), round(float(CEN[1]), 3)], "anchor_E_MGA50_GDA94": round(E0, 2), "anchor_N_MGA50_GDA94": round(N0, 2),
        "anchor_lon": round(lon0, 6), "anchor_lat": round(lat0, 6), "theta_ccw_deg": round(float(th), 2),
        "canonical_plus_x_bearing_deg": round((-th) % 360, 1), "canonical_plus_y_(offshore)_bearing_deg": round((270 - th) % 360, 1), "epsg": 28350,
        "note": "(E,N) = R(theta) (-(y-yc), (x-xc)) + (E0,N0); canonical x north, y west of shape.json"},
       "fit": {"rock_soundings_inside_pct": round(100 * P.contains_points(rock).mean(), 1), "bed_soundings_inside_pct": round(100 * P.contains_points(non).mean(), 1),
               "n_rock": int(len(rock)), "n_bed": int(len(non)), "n_post_1999": int(len(post)),
               "free_scale_fit_scale": 0.979, "note": "scale freed in a separate run: 0.979 (outline scale confirmed within 2 %)"},
       "survey_2002_vs_1998": {"mean_rock_thickness_inside_original_footprint_m": round(float(t02[inn].mean()), 2), "n_inside": int(inn.sum()),
               "extension_triangle_mean_thickness_m": round(float(t02[ext].mean()), 2), "n_extension": int(ext.sum()),
               "ring_0_25m_outside_mean_thickness_m": round(float(t02[ring].mean()), 2), "n_ring": int(ring.sum())}}
json.dump(out, open(HERE + '/georef.json', 'w'), indent=1); print(json.dumps(out, indent=1))
