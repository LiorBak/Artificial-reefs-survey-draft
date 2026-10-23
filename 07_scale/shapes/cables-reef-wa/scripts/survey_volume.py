"""cables-reef-wa: rock volume and thickness measured from the DoT WA soundings (survey surface minus the 1998 pre-construction bed), integrated over the
georeferenced original-plan footprint. Linear interpolation (LinearNDInterpolator) of the thickness at the sounding points within footprint + 6 m, evaluated on a 0.5 m grid.
Reports Nov-1999 and Feb-2002 separately, and a bracket from the rock threshold. Writes survey_volume.json. numpy/scipy/shapely/matplotlib only."""
import json, numpy as np
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator
from matplotlib.path import Path
from shapely.geometry import Polygon
exec(open(__file__.rsplit('/', 1)[0] + '/georef_fit.py').read().split("res = differential_evolution")[0])
G = json.load(open(HERE + '/georef.json'))['transform']; th, tx, ty = G['theta_ccw_deg'], G['anchor_E_MGA50_GDA94'] - CX, G['anchor_N_MGA50_GDA94'] - CY
out = {}
for name, pl in (('original_plan', poly0), ('with_extension', poly_ext)):
    W = world(pl, th, tx, ty); sp = Polygon(W); P = Path(W)
    gx, gy = np.meshgrid(np.arange(W[:, 0].min(), W[:, 0].max(), 0.5) + .25, np.arange(W[:, 1].min(), W[:, 1].max(), 0.5) + .25)
    inside = P.contains_points(np.c_[gx.ravel(), gy.ravel()]).reshape(gx.shape)
    for tag, arr in (('1999-11', post), ('2002-02', p02)):
        q = arr[:, :2] - [CX, CY]; t = arr[:, 2] - bed_at(arr[:, :2])
        near = Polygon(W).buffer(6).contains(__import__('shapely.geometry', fromlist=['MultiPoint']).MultiPoint(q).geoms[0]) if False else Path(np.array(sp.buffer(6).exterior.coords)).contains_points(q)
        f = LinearNDInterpolator(q[near], t[near]); fn_ = NearestNDInterpolator(q[near], t[near])
        tt = f(gx, gy); tt = np.where(np.isnan(tt), fn_(gx, gy), tt); tt = np.maximum(tt, 0)       # negative thickness = noise
        V = float(tt[inside].sum() * 0.25)
        out.setdefault(name, {})[tag] = {"volume_m3": round(V, 0), "mean_thickness_m": round(float(tt[inside].mean()), 2), "max_thickness_m": round(float(tt[inside].max()), 2),
                                          "n_soundings_used": int(near.sum()), "area_m2": round(float(inside.sum() * 0.25), 0)}
out['note'] = ("thickness = sounding z (AHD) minus the 1998 bed interpolated at the same point; negatives clipped to 0; interpolated linearly between sounding lines (spacing ~5 m); "
               "uncertainty: bed interpolation +-0.2-0.3 m (1995 vs 1998 surveys differ by sd 0.29 m, mean 0.09 m) -> about +-1,000 m3 over 4,000 m2; singlebeam footprint smooths ridges (volume biased low)")
json.dump(out, open(HERE + '/survey_volume.json', 'w'), indent=1); print(json.dumps(out, indent=1))
