"""cables-reef-wa: write the georeference, verification and decisions of the imagery + bathymetry run (2026-10-10) into ../shape.json.
Original shape.json archived (run once on the archived file; not idempotent) in 3d/archive/pre_imagery_2026-10-10/. Run after georef_fit.py, survey_volume.py, shore_and_datum.py."""
import json
HERE = __file__.rsplit('/', 1)[0]
d = json.load(open(HERE + '/../shape.json')); G = json.load(open(HERE + '/georef.json')); SV = json.load(open(HERE + '/survey_volume.json')); SD = json.load(open(HERE + '/shore_datum.json'))
t = G['transform']; f = G['fit']; s2 = G['survey_2002_vs_1998']
d['geo'] = {"crs": "EPSG:28350 GDA94 / MGA zone 50 (soundings); WGS84 lon/lat given for the anchor", "anchor_canonical_xy_m": t['anchor_canonical_xy_m'], "anchor_lon": t['anchor_lon'], "anchor_lat": t['anchor_lat'],
            "anchor_E": t['anchor_E_MGA50_GDA94'], "anchor_N": t['anchor_N_MGA50_GDA94'], "theta_ccw_deg": t['theta_ccw_deg'], "canonical_plus_x_bearing_deg_T": t['canonical_plus_x_bearing_deg'],
            "apex_direction_bearing_deg_T": t['canonical_plus_y_(offshore)_bearing_deg'], "transform": t['note'], "shoreline_bearing_deg_T": SD['shoreline_bearing_deg_T'],
            "anchor_to_0m_AHD_line_m": SD['anchor_to_0mAHD_m_by_bearing_deg'],
            "method": "rigid fit (rotation + shift, scale fixed) of the traced original-plan outline to the DoT WA soundings of Nov 1999 (scripts/georef_fit.py); free-scale run gives 0.979; independent check on four Esri images (VERIFY.md)",
            "fit": f, "source_ids": ["DoT1999", "DoT1998", "SAT"]}
for v in d['outline_versions']:
    if v['id'] == 'design_plan_original_1999':
        v['name'] = 'Design plan footprint (Lyons 1992 / Blacka 2013 Fig A.2), georeferenced and confirmed by DoT soundings (default)'
        v['note'] = v['note'] + ' Georeferenced and confirmed 2026-10-10: %s %% of the Nov 1999 rock soundings lie inside, scale within 2 %%; the dark rock patch on four Esri images coincides with it.' % f['rock_soundings_inside_pct']
    if v['id'] == 'design_plan_plus_extension_1999':
        v['name'] = 'Design plan + drawn southern-arm extension (not confirmed by soundings or imagery)'
        v['note'] = v['note'] + ' NOT CONFIRMED (2026-10-10): Feb 2002 soundings in the triangle show %.2f m of rock (n=%d) against %.2f m inside the original plan and %.2f m in the 25 m ring outside; the triangle is not darker than its surroundings on Esri imagery.' % (s2['extension_triangle_mean_thickness_m'], s2['n_extension'], s2['mean_rock_thickness_inside_original_footprint_m'], s2['ring_0_25m_outside_mean_thickness_m'])
d['default_outline'] = 'design_plan_original_1999'
d['versions_info'] = ("The default outline is the original construction design plan (outer foot of the rock mound, traced on Blacka et al. 2013 Fig A.2 after Lyons 1992, scaled from its printed dimensions), "
    "georeferenced by fitting it to the DoT WA soundings of Nov 1999 (91 % of the rock soundings inside, scale within 2 %) and checked on Esri satellite images (the dark rock patch coincides with it). "
    "The drawn southern-arm extension (320 m3) is kept as a separate version because neither the 2002 soundings nor the imagery confirm it. The V printed on the paper's site plan (Fig 7) and an early concept sketch are shown for comparison.")
d['confidence'] = {"level": "high", "reason": "Footprint position, orientation and scale are confirmed by an as-built-era survey with coordinates (DoT WA soundings, Nov 1999: %s %% of rock soundings inside the outline, free scale fit 0.979) and by four georeferenced Esri images on which the rock patch coincides with the outline. Dimensions 121 x 76 m differ from the text 140 x 70 m by -13 %% / +9 %%; the survey and the printed dimensions agree with each other, the text is rounded. The south-arm extension is NOT confirmed (low confidence, separate version)." % f['rock_soundings_inside_pct'],
    "factors": ["DoT WA singlebeam soundings Nov 1999 (840) and Feb 2002 (5,143 in the window) over the 1998 pre-construction bed", "rigid fit; scale freed gives 0.979", "Esri World Imagery and Wayback z19, 4 dates, outline on the dark rock patch", "scale from four printed dimensions of the design plan, sd 0.7 %", "extension: 23 soundings, +0.43 m mean, image not darker: not confirmed"]}
for k in d['dimensions_check']:
    if k['quantity'].startswith('offshore distance'):
        k['drawing_value'] = '%d m (due east) to %d m (080/100 deg) from the georeferenced centroid anchor to the 0 m AHD line (DoT Perth_5m)' % (SD['anchor_to_0mAHD_m_by_bearing_deg']['90'], SD['anchor_to_0mAHD_m_by_bearing_deg']['80'])
        k['comment'] = 'measured on DoT data (independent of the drawing); closest to S1 250 m'
d['angles'].append({"what": "arm bearings after georeferencing (true): north arm %.0f, south arm %.0f deg; relative to the shoreline bearing %.0f deg: north arm %.0f, south arm %.0f deg" % (44.7 - t['theta_ccw_deg'], 137.3 - t['theta_ccw_deg'], SD['shoreline_bearing_deg_T'], abs(44.7 - t['theta_ccw_deg'] - SD['shoreline_bearing_deg_T']), 188 - (137.3 - t['theta_ccw_deg'])), "deg": None, "method": "canonical arm angles 42.7 / 44.7 deg to the frame axis rotated by the fitted theta; shoreline from the 0 m AHD contour; the frame axis is NOT shore-normal (the first model assumed N-S)"})
d['verified_on'] = '2026-10-10'; d['status'] = 'verified'; d['checked_without_network'] = False
d['verification'] = [
 {"check": "overlay vs structure on georeferenced imagery", "verdict": "good", "evidence": "outline coincides with the dark rock patch on Esri Wayback 2014-12-03, 2020-03-23, 2022-06-08, 2024-08-15 and World Imagery 2025-12-06; waves break on the patch in 2020-03-23 (src/imagery/annotated/overlay_*.png)"},
 {"check": "position, orientation, scale against soundings", "verdict": "good", "evidence": "%s %% of rock soundings (>0.6 m over the 1998 bed) inside, %s %% of bed soundings inside; theta %.1f deg ccw; free scale 0.979" % (f['rock_soundings_inside_pct'], f['bed_soundings_inside_pct'], t['theta_ccw_deg'])},
 {"check": "southern-arm extension", "verdict": "not confirmed", "evidence": "2002 soundings in the triangle: +%.2f m (n=%d) vs +%.2f m outside; imagery brightness inside the triangle equals the surroundings (edge.py brightness ratio 1.1-2.9 vs rock interior)" % (s2['extension_triangle_mean_thickness_m'], s2['n_extension'], s2['ring_0_25m_outside_mean_thickness_m'])},
 {"check": "dimensions vs text", "verdict": "ok with note", "evidence": "121 x 76 m traced and soundings fit vs text 140 x 70 m (-13 % / +9 %); the text is approximate"},
 {"check": "rock volume", "verdict": "design surface low", "evidence": "design surface on the measured bed: 3,920 m3 (original plan); soundings: %d (Nov 1999) to %d m3 (Feb 2002); stated 3,500-5,500" % (SV['original_plan']['1999-11']['volume_m3'], SV['original_plan']['2002-02']['volume_m3'])},
 {"check": "datum", "verdict": "A nearer than B", "evidence": "survey-implied RL minus AHD about 0.5-0.6 m on the design ramp vs 0.78 (A) and 0 (B)"}]
d['updated'] = '2026-10-10'
json.dump(d, open(HERE + '/../shape.json', 'w'), indent=1, ensure_ascii=False); print('shape.json updated; status', d['status'])
