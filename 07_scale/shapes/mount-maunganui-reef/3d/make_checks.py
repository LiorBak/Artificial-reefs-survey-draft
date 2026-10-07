"""make_checks.py - validation figure of the loft against the 2013 survey and the stated volume: annotated/mmr_model_checks.png and checks.json.
(a) plan: -2.0 m outline, as-built toe, skirt footprint at bed -4.0 for run 1.0 and 0.5;  (b) two sections (south arm x = -20, west block x = +20): model reef vs the 2013 DEM (Fig 5, img-04);
(c) volume vs bed for both versions against the stated 2,800 m3 (RWR / BoPRC p28)."""
import json, os, sys
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mmr_lib as L, mmr_model as M
HERE = os.path.dirname(os.path.abspath(__file__))
G = M.make_grid(); xs, ys = G['xs'], G['ys']
dep, filled, valid, _ = L.load_fig5(); Zs, sxs, sys_ = L.fig5_to_grid(dep, valid, -45, 42, 276, 352, 0.5)
fig, ax = plt.subplots(2, 2, figsize=(13, 9))
a = ax[0, 0]
for p in M.P2: a.plot(p[:, 0], p[:, 1], 'r-', lw=1.5, label='-2.0 m CD outline (2013)' if p is M.P2[0] else None)
for p in M.PT: a.plot(p[:, 0], p[:, 1], color='orange', lw=1.5, label='as-built toe (2008)' if p is M.PT[0] else None)
for run, col in ((1.0, 'tab:blue'), (0.5, 'tab:green')):
    z, S = M.surface(G, 'multibeam_2013_m2p0', -4.0, run=run); h = np.where(np.isfinite(z), z - S, 0); a.contour(xs, ys, (h > 0.02).astype(float), [0.5], colors=col, linewidths=1.2)
    a.plot([], [], color=col, label='skirt footprint at bed -4.0, run %.1f (%.0f m2)' % (run, M.stats(G, 'multibeam_2013_m2p0', -4.0, run=run)['footprint_area_m2']))
a.set_aspect('equal'); a.set_title('(a) outlines and skirt footprints'); a.legend(fontsize=7); a.set_xlabel('x (m, NW)'); a.set_ylabel('y (m, offshore)'); a.grid(alpha=.3)
for k, (xsec, nm) in enumerate(((-20.0, 'south arm'), (20.0, 'west block'))):
    a = ax[0, 1] if k == 0 else ax[1, 0]
    i = int(round((xsec - xs[0]) / M.DX)); j2 = int(round((xsec - sxs[0]) / 0.5))
    for ver, col in (('multibeam_2013_m2p0', 'tab:blue'), ('asr_installed_toe_2008', 'tab:orange')):
        z, S = M.surface(G, ver, -4.0); zz = np.where(np.isfinite(z[:, i]) & (z[:, i] > S[:, i] + 0.02), z[:, i], np.nan)
        a.plot(ys, zz - M.MSL, color=col, lw=1.8, label='model (%s), bed -4.0' % ('survey outline, skirt 1:1' if ver.startswith('multi') else 'toe loft'))
    z, S = M.surface(G, 'multibeam_2013_m2p0', -4.0); a.plot(ys, S[:, i] - M.MSL, 'k-', lw=1, label='model bed -4.0 CD')
    a.plot(sys_, Zs[:, j2] - M.MSL, color='tab:purple', lw=1.2, label='2013 DEM (Fig 5, img-04)')
    a.axhline(-0.9 - M.MSL, color='m', lw=0.8, ls='--'); a.text(278, -0.9 - M.MSL + 0.05, 'crest -0.9 CD', color='m', fontsize=8)
    a.axhline(M.ZC - M.MSL, color='r', lw=0.8, ls=':'); a.text(278, M.ZC - M.MSL + 0.05, '-2.0 CD contour', color='r', fontsize=8)
    a.set_xlim(276, 352); a.set_ylim(-6.8, -1.2); a.set_title('(%s) section x = %+.0f m (%s), z in m MSL' % ('b' if k == 0 else 'c', xsec, nm)); a.grid(alpha=.3); a.legend(fontsize=7, loc='lower right'); a.set_xlabel('y (m)')
a = ax[1, 1]
beds = np.arange(-4.8, -2.6, 0.1)
for ver, col, nm in (('multibeam_2013_m2p0', 'tab:blue', 'survey outline, skirt 1:1'), ('asr_installed_toe_2008', 'tab:orange', 'toe loft')):
    a.plot(beds, [M.stats(G, ver, b)['volume_m3'] for b in beds], color=col, label=nm)
a.plot(beds, [M.stats(G, 'multibeam_2013_m2p0', b, run=0.5)['volume_m3'] for b in beds], color='tab:green', ls='--', label='survey outline, skirt 1:0.5')
a.axhline(2800, color='k', ls=':'); a.text(-4.75, 2830, 'stated 2,800 m3 (RWR / BoPRC p28); Installed grid 2,835-2,861', fontsize=8)
a.axvline(-4.0, color='b', ls=':'); a.text(-3.98, 4300, 'decision -4.0', color='b', fontsize=8, rotation=90)
a.set_xlabel('bed at the reef centre (m CD)'); a.set_ylabel('model volume above the bed (m3)'); a.set_title('(d) volume vs bed level'); a.grid(alpha=.3); a.legend(fontsize=8)
fig.suptitle('mount-maunganui-reef: model checks (crest -0.9 m CD; Navionics-based seabed profile shifted to the bed level)', fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'annotated', 'mmr_model_checks.png'), dpi=110)
out = {'run_for_toe_area': {str(r): M.stats(G, 'multibeam_2013_m2p0', -4.0, run=r)['footprint_area_m2'] for r in (0.25, 0.5, 0.75, 1.0, 1.5)},
       'toe_area_m2': float(M.TOE.area), 'region_area_m2': float(M.REGION.area)}
json.dump(out, open(os.path.join(HERE, 'checks.json'), 'w'), indent=1); print(out)
