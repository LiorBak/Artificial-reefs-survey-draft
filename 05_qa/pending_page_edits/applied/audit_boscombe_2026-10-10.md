# Boscombe source audit 2026-10-10: page edits for the page agent (04_build/data)
Exact old -> new: 07_scale/shapes/boscombe-surf-reef/SOURCE_AUDIT_2026-10-10.md section 3:
models3d_curated.json /models/boscombe-surf-reef/state_short, confidence_short, key_numbers/0/note; models3d_caveats.json /rows/10/ev/0.
Card (cards agent): "about 1 ha" and "220 m" vs traced 4,042 m2 and 181-276 m; card images[0] and 05_qa/reef/boscombe-surf-reef_media_recheck.json describe img-01 as an exposed mound (it shows a sand heap).
Open: local MSL 1.66 m ODN (Rendle p.70) vs 1.40 (NTSLF) - default 1.40 kept.

# Other audit notes for the cards agent / page agent (added by main 2026-10-10)
- Borth card: `size` quotes Blacka's dimensions of the superseded two-reef design; final layout north mound 144.9 m, south oval 71.8 x 31.0 m (07_scale/shapes/borth-coastal-defence-reef/SOURCE_AUDIT_2026-10-10.md).
- Cables: page texts = 07_scale/shapes/cables-reef-wa/3d/PAGE_TEXTS_FOR_MAIN.json (revised by the audit).
- Albany: shape.json `canonical` = satellite trace (10,918 m2) but `default_outline` = design (13,104 m2): the page must draw the default (design) outline. Card: ~70,000 t vs 62,800 t.
- Kovalam: H35 bbox 43x24 (shape.json) vs 38x29 (rectify_result.json); volumes 4,000 / 4,300 (Rendle Table 2.1) / 4,800 / 4,017.
- Burkitts: card treats a "9 m dive depth" site as this headland, but the registry rejected that video as another place: remove or qualify on the card.
- Opunake: check the next page build shows no wedge.
