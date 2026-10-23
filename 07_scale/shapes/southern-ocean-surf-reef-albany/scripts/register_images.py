"""Updates 03_images/reefs/southern-ocean-surf-reef-albany/images.json + IMAGES.md with the planform-trace results (2026-10-10).
Re-reads both files right before writing (a papers-intake agent may add rows). Run from the repo root: python -I <this file>"""
import json, re, os, datetime
ROOT = '/home/user/artificial-reef-survey'; SLUG = 'southern-ocean-surf-reef-albany'
JS = f'{ROOT}/03_images/reefs/{SLUG}/images.json'; MD = f'{ROOT}/03_images/reefs/{SLUG}/IMAGES.md'; LOG = f'{ROOT}/03_images/reefs/NEW_IMAGES_LOG.md'
S = f'07_scale/shapes/{SLUG}'; TODAY = '2026-10-10'
O = f'{S}/overlays/'
U = {
 '10': dict(ann=[], pend=False, used=['plan_trace', 'cross_check', '3d_crest', 'context'], links=[S+'/sources.md design_table'],
   res="Table read again on the image: volume 34,000 m3 (NOT 54,000 m3 as an earlier text said), crest level -1.00 m AHD, crest length 110 m @ -2 m AHD, 140 m from landward toe, orientation curved 270N-305N. Volume consistent with 62,800 t / 1.85 t/m3. No as-built crest value found to compare with.",
   how="Values read into METHOD.md step 1/3 and shape.json dimensions_check (source id design_table). Correction: volume is 34,000 m3, not 54,000 m3."),
 '11': dict(ann=[O+'design_diagram_trace.png', O+'canonical_versions_m.png'], pend=False, used=['plan_trace', 'scale', 'cross_check'], links=[S+'/sources.md design_plan', S+'/shape.json outline design_bluecoast'],
   res="Outermost design contour traced (25 vertices); scale bar 1.52 px/m, north up (crest line 278 deg; free fit -3 deg); positioned on the satellite by translation (IoU 0.81). Area 13,104 m2, along-crest length 164.6 m (text 165 m). Faint seabed contours east of the reef carry no labels: no depth read.",
   how="TRACED 2026-10-10: planform -> shape.json source design_plan / default outline design_bluecoast (METHOD.md 2b)."),
 '13': dict(ann=[O+'sat2026-01-20_trace.png', O+'shoreline_fit.png', O+'before_after_2025-01-16_vs_2026-01-20.png'], pend=False, used=['plan_trace', 'scale', 'cross_check'], links=[S+'/sources.md sat2026', S+'/shape.json outline sat_2026'],
   res="Traced (20 vertices): area 10,918 m2; along-crest length 157 m (text 165 m, -4.7 %), across 117 m (text up to 110 m); crest edge bearing 281.5 deg (design 270-305). Nearest edge 71 m from the dry-sand beach-face line (about 150 m from the vegetation edge; text 140 m from landward toe, reference undefined). No depth information in the image.",
   how="TRACED 2026-10-10: source sat2026 (primary as-built visible outline), outline version sat_2026 (METHOD.md 2a)."),
 '12': dict(ann=[O+'before_after_2025-01-16_vs_2026-01-20.png'], pend=False, used=['cross_check', 'context'], links=[S+'/VERIFY.md'],
   res="Before/after: inside the traced polygon mean green 137 (2025) vs 129 offshore = no structure; 57 vs 68 in 2026. Confirms the dark wedge is the new reef. No depth information extractable from the RGB image.",
   how="Pre-construction control for the planform trace (VERIFY.md check 1)."),
 '05': dict(ann=[], pend=False, used=['context', 'cross_check'], links=[S+'/METHOD.md 2c'],
   res="Viewed: oblique aerial, no scale, berm only partly built (May 2025): not traceable. Qualitative only: elongated dark berm tapering seaward, consistent with the wedge planform. No depth value.",
   how="Context for the planform, not traced (METHOD.md 2c)."),
 '03': dict(ann=[], pend=False, used=['context'], links=[S+'/METHOD.md 2c'],
   res="Viewed: near-vertical drone view of barges over the partly built berm, no known-length scale reference: not traceable. Qualitative only.",
   how="Context only, not traced (METHOD.md 2c)."),
}
rows = json.load(open(JS, encoding='utf8')); t = open(MD, encoding='utf8').read()
for r in rows:
    k = r['id'][-2:]
    if k not in U: continue
    u = U[k]; rid = r['id']; f = r.setdefault('for_3d_check', {})
    if f.get('result', '').startswith(u['res'][:40]): continue          # already applied
    new_ann = [a for a in u['ann'] if a not in r['annotated_files']]
    f['pending'] = u['pend']; f['result'] = u['res']; r['annotated_files'] += new_ann
    r['used_for'] = [x for x in r['used_for'] if x != 'not_used'] + [x for x in u['used'] if x not in r['used_for']]
    r['how_used'] = (r.get('how_used', '') + ' ' + u['how']).strip(); r['linked_records'] += [l for l in u['links'] if l not in r['linked_records']]
    if k == '10': r['shows'] = r['shows'].replace('54,000 m3', '34,000 m3')
    m = re.search(r'(## %s - .*?)(?=\n## |\Z)' % re.escape(rid), t, re.S)
    if m:
        sec = m.group(1)
        if k == '10': sec = sec.replace('volume 54,000 m3', 'volume 34,000 m3').replace('54,000 m3', '34,000 m3 (corrected 2026-10-10)')
        sec = re.sub(r'- \*\*3D check pending\*\*: (YES|no)', '- **3D check pending**: no', sec, count=1)
        sec = sec.rstrip('\n') + '\n- **3D check result (%s)**: %s\n- **How used (update %s)**: %s\n' % (TODAY, u['res'], TODAY, u['how'])
        if new_ann: sec += '- **annotated versions (added %s)**: %s\n' % (TODAY, ', '.join(new_ann))
        t = t[:m.start(1)] + sec + t[m.end(1):]
tmp = JS + '.tmp'; json.dump(rows, open(tmp, 'w', encoding='utf8'), indent=1, ensure_ascii=False); os.replace(tmp, JS)
open(MD, 'w', encoding='utf8').write(t)
with open(LOG, 'a', encoding='utf8') as l:
    l.write('%s | %s | img-10..13,03,05 (annotated overlays, no new rows) | %s | planform trace overlays (satellite trace, design-plan trace, shoreline fit, before/after, canonical versions) | planform checked; no depth info; img-10 volume corrected to 34,000 m3 | shape agent queue item 9\n' % (TODAY, SLUG, O))
print('done', len(rows))
