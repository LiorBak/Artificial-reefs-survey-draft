import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
nd = json.load(open(os.path.join(HERE, 'navionics', 'nav_datum_test.json')))
iz = nd['implied_zero_mODN']; tb = nd['rms_table']
out = dict(
    summary=('Garmin Navionics web chart (SonarChart + Nautical Chart, metres, 2026-10-07): shore-parallel contours 0 (drying edge at y 385-430 m), 0.5, 1, 1.5, 2, 2.5 m; the rock mounds lie inside the uniform drying area and are not charted, '
             'so no crest/height cross-check is possible; datum not stated, assumed LAT (best of 7 candidates, RMS %.2f m vs Fig 2 -4.0, %.2f vs EMODnet); the chart is about %.1f m shallower than Fig 2 offshore -> used as a cross-check only, not for the seabed.' % (
                 tb['LAT (-2.44)']['fig2_m4'], tb['LAT (-2.44)']['emodnet'], abs(iz['fig2_minus4'][0] + 2.44))),
    method=('Pixel rows of 982 x 655 px screenshots (zoom 17, 0.730 m/px) -> Web Mercator -> WGS84 -> OS grid -> canonical frame; contour crossings counted outward from the green drying edge; implied chart zero = z_reference + depth; '
            'candidate datums LAT -2.44, MLWS -1.74, MLWN -0.64, MSL +0.31, ODN 0, MHWN +1.06, MHWS +2.56 mODN tested by RMS against the model seabed (n=%d), the HRPP576 Fig 2 -4.0 contour (n=%d) and EMODnet cells (n=%d). See METHODS_3D.md 3.6.' % (iz['model'][2], iz['fig2_minus4'][2], iz['emodnet'][2])),
    uncertainty='datum +-0.6 m; contour position +-2 m; chart depths 0.6-1.1 m shallower than the survey references offshore (SonarChart is partly interpolated; data dates not shown)',
    implied_zero_mODN=iz, rms_table=tb, files='src/navionics/ (44 screenshots, capture log, scripts), annotated/A9, A10')
json.dump(out, open(os.path.join(HERE, 'navionics_reading.json'), 'w'), indent=1)
print(out['summary'])
