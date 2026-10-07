"""Compare the Mortensen et al. (2015) Fig 6a pre-construction depth profile (read by eye, y=3050 m, datum unstated)
with the Navionics SonarChart depths below LAT used in the Palm Beach 3D model (read-only values from
07_scale/shapes/palm-beach-gold-coast/3d/validation_3d.json, anchors.sonar_depth_below_LAT_at_y_(mean of x=+-150 m)).
Unknowns: shift s (m) between the figure's x and the distance offshore y of the 3D frame (x = y + s) and, optionally, a vertical offset c (m).
Test: chart depth below AHD = depth below LAT + 0.76 (MSQ 2014), or below MSL = + 0.88 (MSQ 2026), or no conversion (LAT)."""
import numpy as np
M = np.array([[394,2.0],[406,2.5],[425,3.0],[443,3.5],[540,4.5],[572,5.0],[596,5.5],[620,6.0],[639,6.5],[660,7.0],[718,8.0],[730,8.5],[767,9.5],[782,10.0],[800,10.5],[836,11.5],[852,12.0]])
C = np.array([[150,2.22],[225,3.86],[260,4.39],[300,4.93],[340,5.58],[374,6.31],[450,8.81]])
sel = (M[:,1] >= 3.5) & (M[:,1] <= 11.5)           # fixed comparison set (3.5-11.5 m); chart extended linearly beyond 450 m
Mx, Md = M[sel,0], M[sel,1]
def chart(y):
    d = np.interp(y, C[:,0], C[:,1])
    slope = (C[-1,1]-C[-2,1])/(C[-1,0]-C[-2,0])
    return np.where(y > C[-1,0], C[-1,1] + slope*(y - C[-1,0]), d)
print("comparison points: %d of the Mortensen labels (%.1f-%.1f m)" % (sel.sum(), Md.min(), Md.max()))
for name, ds in [("LAT (no conversion)", 0.0), ("AHD = LAT + 0.76 (MSQ 2014)", 0.76), ("MSL = LAT + 0.88 (MSQ 2026)", 0.88)]:
    best = {}
    for fit_c in (False, True):
        res = []
        for s in np.arange(200, 400.5, 0.5):
            r = chart(Mx - s) + ds - Md
            c = -r.mean() if fit_c else 0.0
            rr = r + c
            res.append((float(np.sqrt(np.mean(rr**2))), float(s), float(c)))
        rms, s, c = min(res)
        best[fit_c] = (rms, s, c)
        print("%-30s vertical offset %-9s: shift s = %5.1f m, c = %+5.2f m, RMS = %.2f m" % (name, "fitted" if fit_c else "fixed 0", s, c, rms))
