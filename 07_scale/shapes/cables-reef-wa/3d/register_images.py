"""Register this run's images in 03_images/reefs/cables-reef-wa/images.json (+ IMAGES.md, NEW_IMAGES_LOG.md). Re-reads images.json right before writing (other agents may append rows).
Idempotent by file path. Run from anywhere after the previews exist: python3 register_images.py"""
import json, hashlib, os, re
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
REG = ROOT + '/03_images/reefs/cables-reef-wa/images.json'
def rel(p): return os.path.relpath(p, ROOT).replace(os.sep, '/')
SH = ROOT + '/07_scale/shapes/cables-reef-wa'
NEW = [
 (SH + '/overlays/cables-reef-wa_versions_compare_m.png', 'diagram', 'Outline versions of the Cable Station reef compared in metres', 'The four outline versions (default design plan + extension, design plan, paper Fig 7 V, Pitt concept) plotted in the canonical frame.',
  ['plan_trace', 'cross_check'], 'Shows how the versions differ in size and shape; the Pitt concept is about 2.4 times the built footprint.', ['07_scale/shapes/cables-reef-wa/shape.json outline_versions']),
 (SH + '/3d/annotated/A2_centreline_section.png', 'diagram', 'Modelled section through the apex of the Cable Station reef', 'Section along the apex centreline: reef surface (RL -1.0 crest to -3.0 set-out), modelled bed and the water levels.',
  ['3d_crest', '3d_height_slopes', '3d_seabed'], 'Shows the modelled crest depth (1.78 m below MSL under reading A) and the thickness over the bed; a check, not a source.', ['07_scale/shapes/cables-reef-wa/3d/SOURCES_3D.md', '07_scale/shapes/cables-reef-wa/3d/METHODS_3D.md section 4']),
 (SH + '/3d/annotated/A3_bed_level_vs_volume.png', 'diagram', 'Bed level fitted to the stated rock volume (Cable Station reef)', 'Modelled rock volume versus the assumed bed depth, with the stated volumes 3,500 / 5,000 / 5,500 m3 and the bed depth each implies.',
  ['3d_seabed', '3d_height_slopes'], 'Documents the single free parameter of the model (bed level D0 = 3.50 m at y = 270 m).', ['07_scale/shapes/cables-reef-wa/3d/METHODS_3D.md section 3.4']),
 (SH + '/3d/preview_plan.png', 'diagram', 'Screenshot of the three.js viewer, plan view (Cable Station reef)', 'Plan view of the modelled reef on the modelled seabed with the 10 m grid and scale bars (north = left).',
  ['camera_match', 'context'], 'Preview of the delivered model viewer (index.html) for the page and for camera-match planning.', ['07_scale/shapes/cables-reef-wa/3d/index.html']),
 (SH + '/3d/preview_oblique.png', 'diagram', 'Screenshot of the three.js viewer, oblique view from the sea (Cable Station reef)', 'Oblique view from the sea of the modelled V-shaped reef under a translucent MSL water surface.',
  ['camera_match', 'context'], 'Preview of the delivered model viewer (index.html).', ['07_scale/shapes/cables-reef-wa/3d/index.html']),
]
ANN = {  # existing rows: annotated files to add
 'cables-reef-wa-img-26': ['07_scale/shapes/cables-reef-wa/overlays/cables-reef-wa-img-26_A2_outline_ramp_scale.png', '07_scale/shapes/cables-reef-wa/3d/annotated/A1_A2_scale_and_contours_read.png'],
 'cables-reef-wa-img-05': ['07_scale/shapes/cables-reef-wa/overlays/cables-reef-wa-img-05_retrace_outer_foot.png'],
 'cables-reef-wa-img-06': ['07_scale/shapes/cables-reef-wa/overlays/cables-reef-wa-img-06_extension_triangle.png'],
 'cables-reef-wa-img-20': ['07_scale/shapes/cables-reef-wa/overlays/cables-reef-wa-img-20_fig7_V_outline_rotated.png'],
 'cables-reef-wa-img-07': ['07_scale/shapes/cables-reef-wa/overlays/cables-reef-wa-img-07_pitt_concept_outline.png', '07_scale/shapes/cables-reef-wa/3d/annotated/A4_pitt_sketch_bed_gradient_read.png'],
}
RESULT = {
 'cables-reef-wa-img-26': 'USED (primary, plan + levels): printed dimensions give 6.51 px/m (+-3%); footprint 4,049 m2 (121 x 76 m); ramp RL -1.0 to -3.0; model contours within 0.14 m rms. 3D 2026-10-10.',
 'cables-reef-wa-img-05': 'Re-trace on this lower-resolution copy at an assumed 3.6 px/m: 4,209 m2, +4% vs img-26. Not the primary. 2026-10-10.',
 'cables-reef-wa-img-06': 'Extension triangle traced and registered on img-26: 347 m2; with the stated 320 m3 the mean fill is 0.92 m. Built extent still unverified. 2026-10-10.',
 'cables-reef-wa-img-07': 'Bed gradient read from the 3.0-7.0 m contour labels (1:28 left, 1:33 right, used 1:30); scale bar 171 px per 200 m. Concept outline (170 x 159 m) differs from the built design. 2026-10-10.',
 'cables-reef-wa-img-10': 'Qualitative section, no numbers: consistent with the modelled centreline section (gentle offshore ramp, steeper inner side). 2026-10-10.',
 'cables-reef-wa-img-17': 'Oblique, not traceable. Ride-length check inconclusive: crest-line arm lengths 49 m (south) and 52 m (north) vs ride 50-80 m / 30-40 m. 2026-10-10.',
 'cables-reef-wa-img-20': 'Apex offshore confirmed (INDIAN OCEAN label upright after rotating); V 122 x 76 m with an assumed 100 m grid agrees with img-26 (121 x 76 m); centroid 271 m from the shore line sets the 270 m offshore position. 2026-10-10.',
 'cables-reef-wa-img-23': 'Same as img-20 (upscale of the same raster). 2026-10-10.',
}
rows = json.load(open(REG, encoding='utf-8'))            # re-read immediately before writing
byid = {r['id']: r for r in rows}; have_files = {r['file'] for r in rows if r.get('file')}
for rid, files in ANN.items():
    r = byid[rid]; r['annotated_files'] = list(dict.fromkeys((r.get('annotated_files') or []) + files))
for rid, res in RESULT.items():
    r = byid.get(rid)
    if r and r.get('for_3d_check', {}).get('pending'):
        r['for_3d_check']['pending'] = False; r['for_3d_check']['result'] = res
    elif r and 'result' not in r.get('for_3d_check', {}): r.setdefault('for_3d_check', {})['result'] = res
nums = [int(re.search(r'(\d+)$', r['id']).group(1)) for r in rows]; nxt = max(nums) + 1; added = []
for path, kind, title, shows, used, how, linked in NEW:
    f = rel(path)
    if f in have_files: continue
    im = Image.open(path); raw = open(path, 'rb').read()
    row = {"id": "cables-reef-wa-img-%02d" % nxt, "file": f, "annotated_files": [], "kind": kind, "title": title,
           "citation": "Own figure made for this project (cables-reef-wa shape + 3D task, 2026-10-10), derived from the registered sources named in SOURCES_3D.md.", "image_url": None, "source_page": None,
           "page_or_figure": "-", "image_date": "2026-10-10", "credit": "Claude agent for Lior (own work, derived from registered sources)", "license": "own work; derived from sources whose reuse rights are not cleared", "retrieved": "2026-10-10",
           "shows": shows, "structure_visible": True, "state_shown": "design (model)", "used_for": used, "how_used": how, "linked_records": linked, "bytes": len(raw), "px": [im.width, im.height],
           "sha256": hashlib.sha256(raw).hexdigest(), "rights_note": "Private research copy; reuse rights to be checked before any public release.", "display": True,
           "for_3d_check": {"pending": False, "what_to_check": "-", "model_values_affected": []}, "added_by": "cables-reef-wa shape + 3D task, 2026-10-10"}
    rows.append(row); added.append(row); nxt += 1
json.dump(rows, open(REG, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
with open(ROOT + '/03_images/reefs/cables-reef-wa/IMAGES.md', 'a', encoding='utf-8') as f:
    for r in added:
        f.write("\n## %s - %s (own figure)\n\n![%s](../../../%s)\n\n- **file**: `%s`\n- **kind**: %s\n- **shows**: %s\n- **state shown**: design (model)\n- **image date**: 2026-10-10\n- **citation**: %s\n- **licence**: %s\n- **used for**: %s\n- **How used for the model**: %s\n- **rights**: Private research copy; reuse rights to be checked before any public release.\n- **display in HTML**: True\n- **added by**: %s\n" % (r['id'], r['title'], r['id'], r['file'], r['file'], r['kind'], r['shows'], r['citation'], r['license'], ', '.join(r['used_for']), r['how_used'], r['added_by']))
with open(ROOT + '/03_images/reefs/NEW_IMAGES_LOG.md', 'a', encoding='utf-8') as f:
    for r in added:
        f.write("2026-10-10 | cables-reef-wa | %s | %s | %s | no (own figure) | cables-reef-wa shape + 3D task\n" % (r['id'], r['file'], r['shows']))
print('added', [(r['id'], r['file']) for r in added]); print('updated rows', list(RESULT))
