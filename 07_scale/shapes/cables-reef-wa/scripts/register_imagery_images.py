"""cables-reef-wa: register the images of the 2026-10-10 imagery + bathymetry run (img-32..40) and refresh img-30/31 (previews overwritten).
Appends to 03_images/reefs/cables-reef-wa/images.json and IMAGES.md and 03_images/reefs/NEW_IMAGES_LOG.md. Run once."""
import json, hashlib, os
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')); SL = 'cables-reef-wa'
JS = ROOT + '/03_images/reefs/%s/images.json' % SL; rows = json.load(open(JS)); have = {r['id'] for r in rows}
def meta(rel):
    p = ROOT + '/' + rel; b = open(p, 'rb').read(); im = Image.open(p); return len(b), list(im.size), hashlib.sha256(b).hexdigest()
R = '07_scale/shapes/cables-reef-wa/'
ESRI = "Esri, Maxar, Earthstar Geographics, and the GIS User Community"
def sat(n, rel, title, citation_extra, url, date, shows, ann):
    by, px, sh = meta(rel)
    return {"id": "cables-reef-wa-img-%d" % n, "file": rel, "annotated_files": ann, "kind": "satellite", "title": title,
            "citation": "%s (2026). %s Esri. %s Accessed 2026-10-10." % (ESRI, citation_extra, url), "image_url": url, "source_page": "https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9 (World Imagery); Wayback: https://livingatlas.arcgis.com/wayback/",
            "page_or_figure": "zoom 19 tile mosaic, 0.25 m/px, 07_scale/tools/satellite.py fetch (sidecar .geo.json holds bounds and release id)", "image_date": date, "credit": ESRI, "license": "Esri / Maxar imagery terms, not cleared for redistribution", "retrieved": "2026-10-10",
            "shows": shows, "structure_visible": True, "state_shown": "as-built (reef built 1999; image years later)", "used_for": ["cross_check"],
            "how_used": "Independent check of the outline georeferenced from the DoT soundings (position, orientation, extent, south-arm extension): outline drawn on the image by scripts/make_imagery_figs.py; no image information entered the fit. Result in VERIFY.md and METHODS_3D 3.7.",
            "linked_records": [R + "VERIFY.md", R + "3d/METHODS_3D.md section 3.7", R + "3d/SOURCES_3D.md I16"], "bytes": by, "px": px, "sha256": sh,
            "rights_note": "Private research copy; reuse rights to be checked before any public release.", "display": True,
            "for_3d_check": {"pending": False, "what_to_check": "done 2026-10-10: outline coincides with the dark rock patch; extension triangle not distinguishable", "model_values_affected": ["planform"]}, "added_by": "cables imagery + bathymetry run, 2026-10-10"}
W = "https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/%s/19/{y}/{x}"
new = [
 sat(32, R + "src/imagery/esri_world_imagery_2025-12-06_z19.png", "Esri World Imagery (current), Cable Station reef site, zoom 19", "World Imagery current layer, tile mosaic around 32.0155 S 115.7478 E.", "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/19/{y}/{x}", "2025-12-06 (capture date from the service identify DATE field)", "Dark rock patch of the V-shaped reef 250 m off the beach in clear water, seagrass and sand around it; no waves breaking.", [R + "src/imagery/annotated/overlay_esri_world_imagery_2025-12-06_z19.png"]),
 sat(33, R + "src/imagery/esri_wayback_2020-03-23_z19.png", "Esri Wayback release 2020-03-23, Cable Station reef, zoom 19", "World Imagery Wayback release 2020-03-23 (release id 16062).", W % 16062, "release 2020-03-23; capture date not available (earlier than the release)", "Reef patch with a wave breaking on its north-east arm; clearest view of the structure in the series.", [R + "src/imagery/annotated/overlay_esri_wayback_2020-03-23_z19.png"]),
 sat(34, R + "src/imagery/esri_wayback_2022-06-08_z19.png", "Esri Wayback release 2022-06-08, Cable Station reef, zoom 19", "World Imagery Wayback release 2022-06-08 (release id 44710).", W % 44710, "release 2022-06-08; capture date not available", "Dark, sharp-edged reef patch; the best contrast between rock and the surrounding sand.", [R + "src/imagery/annotated/overlay_esri_wayback_2022-06-08_z19.png"]),
 sat(35, R + "src/imagery/esri_wayback_2014-12-03_z19.png", "Esri Wayback release 2014-12-03, Cable Station reef, zoom 19", "World Imagery Wayback release 2014-12-03 (release id 23383).", W % 23383, "release 2014-12-03; capture date not available", "Reef patch (dark, reddish in this version) on the seagrass terrace; oldest release at zoom 19.", [R + "src/imagery/annotated/overlay_esri_wayback_2014-12-03_z19.png"]),
 sat(36, R + "src/imagery/esri_wayback_2024-08-15_z19.png", "Esri Wayback release 2024-08-15, Cable Station reef, zoom 19", "World Imagery Wayback release 2024-08-15 (release id 32553).", W % 32553, "release 2024-08-15; capture date not available", "Dark water, reef patch faint; kept for completeness of the series.", [R + "src/imagery/annotated/overlay_esri_wayback_2024-08-15_z19.png"]),
]
def own(n, rel, kind, title, shows, used, how, linked, state):
    by, px, sh = meta(rel)
    return {"id": "cables-reef-wa-img-%d" % n, "file": rel, "annotated_files": [], "kind": kind, "title": title, "citation": "Own figure made for this project (cables-reef-wa imagery + bathymetry run, 2026-10-10), derived from the sources named in 3d/SOURCES_3D.md (Esri imagery; DoT WA bathymetry, CC BY 4.0).",
            "image_url": None, "source_page": R + "3d/SOURCES_3D.md (own figure)", "page_or_figure": "-", "image_date": "2026-10-10", "credit": "Claude agent for Lior (own work, derived from registered sources)", "license": "own work; derived from sources whose reuse rights are not cleared", "retrieved": "2026-10-10",
            "shows": shows, "structure_visible": True, "state_shown": state, "used_for": used, "how_used": how, "linked_records": linked, "bytes": by, "px": px, "sha256": sh,
            "rights_note": "Private research copy; reuse rights to be checked before any public release.", "display": True,
            "for_3d_check": {"pending": False, "what_to_check": "-", "model_values_affected": []}, "added_by": "cables imagery + bathymetry run, 2026-10-10"}
new += [
 own(37, R + "src/imagery/annotated/overlay_montage_4dates.png", "diagram", "Georeferenced outline on four Esri images (2014, 2020, 2022, 2025)", "Four contrast-stretched crops of the reef with the georeferenced original-plan outline (magenta) and the extension triangle (yellow).", ["cross_check"], "Visual verification of position, orientation and extent; the extension triangle is not distinguishable from the surroundings.", [R + "VERIFY.md", R + "scripts/make_imagery_figs.py"], "as-built (years after completion)"),
 own(38, R + "src/bathymetry/figures/survey_1999_thickness.png", "survey_plot", "DoT WA soundings Nov 1999: rock thickness over the 1998 bed, with the fitted outline", "840 soundings coloured by thickness above the pre-construction bed; the V of the reef with the fitted design outline.", ["plan_trace", "3d_crest", "3d_height_slopes"], "Georeference fit and default 3D surface (version survey_surface_1999_11); thickness values read as sounding minus bed.", [R + "scripts/georef_fit.py", R + "3d/METHODS_3D.md 3.2, 3.4"], "as-built (Nov 1999)"),
 own(39, R + "src/bathymetry/figures/survey_2002_thickness.png", "survey_plot", "DoT WA soundings Feb 2002: thickness over the 1998 bed, with the fitted outlines", "Singlebeam lines (about 5 m apart) coloured by thickness above the 1998 bed; the south-arm extension triangle (SE) shows little rock.", ["cross_check", "3d_height_slopes"], "Surveyed surface version survey_surface_2002_02; extension test (+0.43 m, n = 23).", [R + "3d/METHODS_3D.md 3.5"], "as-built (Feb 2002)"),
 own(40, R + "src/bathymetry/figures/bed_perth5m_contours.png", "survey_plot", "DoT WA composite surface Perth_5m around the reef (m AHD) with the reef outline", "Seabed contours every 1 m from the 0 m AHD shoreline to 9 m, with the reef as a smoothed shallow mound.", ["3d_seabed", "context"], "Seabed beyond the 1998 survey coverage; shoreline bearing (7.8 deg T) and offshore distance (254-263 m).", [R + "scripts/make_bed.py", R + "scripts/shore_and_datum.py"], "as-built (composite of mixed dates)"),
]
for r in new:
    assert r['id'] not in have, r['id']
    rows.append(r)
for r in rows:
    if r['id'] in ('cables-reef-wa-img-30', 'cables-reef-wa-img-31'):
        r['bytes'], r['px'], r['sha256'] = meta(r['file']); r['how_used'] += ' Regenerated 2026-10-10 after the survey rebuild (default = Nov 1999 surveyed surface).'
json.dump(rows, open(JS, 'w'), indent=1, ensure_ascii=False)
md = ROOT + '/03_images/reefs/%s/IMAGES.md' % SL
with open(md, 'a', encoding='utf-8') as f:
    f.write('\n\n## Added 2026-10-10 (imagery + bathymetry run)\n')
    for r in new:
        f.write('\n### %s - %s\n- file: %s\n- kind: %s; date: %s\n- citation: %s\n- licence: %s\n- shows: %s\n- how used for the model: %s\n' % (r['id'], r['title'], r['file'], r['kind'], r['image_date'], r['citation'], r['license'], r['shows'], r['how_used']))
with open(ROOT + '/03_images/reefs/NEW_IMAGES_LOG.md', 'a', encoding='utf-8') as f:
    for r in new:
        f.write('2026-10-10 | %s | %s | %s | %s | %s | %s\n' % (SL, r['id'], r['file'], r['shows'][:110], 'done (checked 2026-10-10)', r['added_by']))
print(len(rows), 'rows')
