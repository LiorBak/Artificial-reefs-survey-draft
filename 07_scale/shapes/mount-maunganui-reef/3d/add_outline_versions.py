"""add_outline_versions.py - writes outline_versions / default_outline / versions_info (+ outline_versions_optional) into ../shape.json (2026-10-06, Lior's
outline-versions decision, 07_scale/SHAPE_SPEC.md 'Outline versions').  Edits the JSON in place (CRLF, indent 1, same key order); canonical.polygons_m /
polygon_m are NOT changed; build_shape_json.py is NOT re-run.  Idempotent: re-running replaces the three keys."""
import json, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shape.json')
t = open(P, 'rb').read().decode('utf-8'); sh = json.loads(t); c = sh['canonical']; g = sh['geo']
versions = [
 {"id": "multibeam_2013_m2p0", "name": "Multibeam survey outline (-2.0 m CD, 18 Jul 2013)", "date": "2013-07-18", "kind": "multibeam_survey",
  "source_ids": ["img1", "ctx9"],
  "method": "Outline of the -2.0 m Chart Datum contour on the georeferenced BoPRC Fig 3 (University of Waikato / Discovery Marine Ltd multibeam), re-checked on Fig 5 (IoU 0.93).",
  "level": "-2.0 m CD contour of the 2013 DEM = the exposed (mid-height) outline of the large bags; a lower bound of the footprint, the bags continue below it to the seabed",
  "area_m2": c['area_m2'], "bbox_m": [c['bbox_m']['alongshore'], c['bbox_m']['crossshore']],
  "polygons_m": c['polygons_m'], "polygon_labels": c['polygon_labels'], "polygons_latlon": g['polygons_latlon'],
  "note": "Survey is 5 years after completion (apex bags deflated, small north-arm base bags probably buried). The 3D model lofts the as-built reef from this contour: crest at -0.9 m CD, 1:1 skirt from the contour to the seabed (assumption)."},
 {"id": "asr_installed_toe_2008", "name": "As-built toe outline (ASR 'Installed' survey image, 2008)", "date": "2008 (undated image, after Aug 2008)", "kind": "multibeam_survey",
  "source_ids": ["img3", "img1"],
  "method": "Toe-level outline of the colour-coded 'Mount Reef Installed' bathymetry (ASR, on Raised Water Research) registered onto Fig 3 (scale +-6 %).",
  "level": "base (toe) of the bags as built, before settlement and burial; includes the north-side base bags, the east-side bag of the south arm and the junction fill that are buried or below -2.0 m in 2013",
  "area_m2": c['toe_area_m2'], "bbox_m": [c['toe_bbox_m']['alongshore'], c['toe_bbox_m']['crossshore']],
  "polygons_m": c['toe_polygons_m'], "polygons_latlon": g['toe_polygons_latlon'],
  "note": "Datum of the Installed image not stated (read as MVD-53); scale from registration. The 3D model lofts from the toe at the seabed through the -2.0 m contour of the 2013 survey to the crest."},
]
optional = [
 {"id": "aerial_dark_mass_2010", "name": "Aerial dark-mass outline (LINZ 0.125 m aerial, Dec 2010 - Mar 2011)", "date": "2010-12-28 .. 2011-03-31", "kind": "photo_trace",
  "source_ids": ["img2"], "area_m2": c['footprint_definitions_m2']['aerial_visible_mass_upper_bound'], "bbox_m": [71.3, 64.9], "polygons_m": None,
  "note": "Not stored as a polygon and not built in 3D (Lior 2026-10-06): the dark mass includes shadow and scour-hole darkening, so only its area is kept as an upper bound (threshold +-2 units gives 1,308-2,073 m2). Optional: could be re-traced from src/linz_aerial_2010-11_BD37_1000_1314_crop.png."}]
info = ("Two outlines of the same built reef are stored. DEFAULT: the -2.0 m Chart Datum contour of the 18 Jul 2013 multibeam survey (BoPRC Fig 3; 1,071 m2, 67.9 x 60.4 m), "
        "the best measured edge but a mid-height, lower-bound footprint measured 5 years after completion. SECOND: the as-built toe outline read from the ASR 'Installed' survey image "
        "(2008; 1,424 m2, 73.9 x 62.5 m), registered onto the 2013 survey, which includes bags that are buried or below -2.0 m by 2013. A third footprint, the dark mass on the 2010-11 aerial "
        "(about 1,723 m2), is kept only as an area (optional, not drawn).")
for k in ('outline_versions', 'default_outline', 'versions_info', 'outline_versions_optional'): sh.pop(k, None)
sh['outline_versions'] = versions; sh['default_outline'] = versions[0]['id']; sh['versions_info'] = info; sh['outline_versions_optional'] = optional
open(P, 'wb').write(json.dumps(sh, indent=1).replace('\n', '\r\n').encode('utf-8'))
print('written', [(v['id'], v['area_m2']) for v in versions], 'canonical.polygons_m unchanged:', sh['canonical']['polygons_m'] == c['polygons_m'])
