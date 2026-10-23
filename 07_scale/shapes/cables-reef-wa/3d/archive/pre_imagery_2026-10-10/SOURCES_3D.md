# SOURCES_3D - cables-reef-wa

Run started 2026-10-10 (network blocked all run: only repo files used). Registry: 03_images/reefs/cables-reef-wa/images.json (ids below). All images are private research copies; reuse rights not cleared.

## Inputs and where each came from
| id | model input | value | source (registry id) | what was read / quote (<= 25 words) | method |
|---|---|---|---|---|---|
| I1 | plan outline | 4,049 m2 (121 x 76 m); +347 m2 extension | Blacka et al. (2013) WRL TR 2012/08, Fig A.2 p.93 [cables-reef-wa-img-26]; extension img-06 | outline of the drawn structure (interface line); 'ADDITIONAL FILL AREA' triangle | silhouette trace; triangle registered on P2, P1 (../METHOD.md) |
| I2 | scale | 6.51 px/m (sd 0.05) | img-26 printed dimensions | '26.0 m', '30.0 m', '40.0 m', contours every 0.5 m at '1:20' | four readings, annotated/A1 |
| I3 | crest line | RL -1.00 | img-26 label 'RL -1.00'; S1 p.3 | 'a 1:20 slope was constructed up to the 1 m contour of the existing reef' | label read; inner edge of the ramp |
| I4 | outer (set-out) edge | RL -3.00 | img-26 ('40.0 m' at 1:20); S1 p.3 | 'the existing 3 m depth contour was extended offshore' | 2.0 m x 20 = 40 m |
| I5 | ramp contours | RL -2.5, -2.0, -1.5; slopes 1:20 / 1:15 / ~1:13 | img-26 labels and slope marks | 'RL -2.50', 'RL -2.00', 'RL -1.50' | model vs drawn: rms 0.14 m, annotated/A1 |
| I6 | datum | z_MSL = RL - 0.78 (A) or RL (B) | S1 p.3 (img-15..23 paper); Blacka A.1.1; Pitt note (img-07) | 'mean tide level of 0.78 m above datum'; Blacka: 'crest submergence of 1 - 2.5 m below MSL' | two readings, switch in the viewer |
| I7 | bed gradient | 1:30 | img-07 Pitt sketch contours 3.0-7.0 m | label rows read, 28-33 m per m of depth | annotated/A4 |
| I8 | bed level | RL -3.50 m at y = 270 m | Blacka A.1.3 (5,500 m3); P3/ICM 5,000; card 3,500 | 'constructed using 5,500 m3 of 1.5 t and 3.0 t grade granite boulders' | fitted, annotated/A3 |
| I9 | tides | range 0.8 m; MTL +0.78 m above datum | Blacka Table 4.3 p.67; S1 p.3 | 'tide range 0.8 m' | typical HW/LW = MSL +-0.4 m (estimate) |
| I10 | position | centroid 270 m offshore | img-20 Fig 7 measurement; S1 '250 m'; Blacka/RWR 275 m | centroid-to-shore line on Fig 7 | assumed 100 m grid |
| I11 | water depth (check) | 3.0-6.0 m | Blacka Table 4.2 p.65; RWR | - | compared with modelled bed in METHODS_3D 4 |

## Annotated images (3d/annotated/) and overlays (../overlays/)
| file | caption | registered as |
|---|---|---|
| annotated/A1_A2_scale_and_contours_read.png | Fig A.2 with the four printed dimensions used for scale (blue / magenta) and the model's RL -2.5 / -2.0 / -1.5 contours (orange) over the drawn ones | annotated_files of cables-reef-wa-img-26 |
| annotated/A2_centreline_section.png | modelled section through the apex: reef surface, bed, water levels | cables-reef-wa-img-28 |
| annotated/A3_bed_level_vs_volume.png | bed level fitted to the stated volumes (3,500 / 5,000 / 5,500 m3) | cables-reef-wa-img-29 |
| annotated/A4_pitt_sketch_bed_gradient_read.png | Pitt sketch with the contour rows read for the bed gradient and the scale bar | annotated_files of cables-reef-wa-img-07 |
| ../overlays/cables-reef-wa-img-26_A2_outline_ramp_scale.png | traced outline (red), ramp polygon (green), extension (orange), scale lines | annotated_files of img-26 |
| ../overlays/cables-reef-wa-img-05_retrace_outer_foot.png | independent re-trace on the RWR copy (assumed scale) | annotated_files of img-05 |
| ../overlays/cables-reef-wa-img-06_extension_triangle.png | extension triangle | annotated_files of img-06 |
| ../overlays/cables-reef-wa-img-20_fig7_V_outline_rotated.png | Fig 7 V outline on the rotated figure (north up) | annotated_files of img-20 |
| ../overlays/cables-reef-wa-img-07_pitt_concept_outline.png | Pitt concept outline | annotated_files of img-07 |
| ../overlays/cables-reef-wa_versions_compare_m.png | the four outline versions in metres | cables-reef-wa-img-27 |
| preview_plan.png, preview_oblique.png | screenshots of index.html (own headless Chrome, vendored three.js) | cables-reef-wa-img-30, -31 |

## Registry results (for_3d_check) written 2026-10-10
img-26: used (primary, plan + levels). img-05: re-trace, area +4% vs img-26 at the assumed scale. img-06: extension triangle 347 m2, 0.92 m mean fill vs the 320 m3 text. img-07: bed gradient and scale bar read; concept outline differs from the built design. img-20: orientation and the 270 m offshore position; V 122 x 76 m (assumed 100 m grid) agrees with img-26. img-23: same as img-20 (upscale). img-17: oblique, not traceable; ride-length check inconclusive (crest arms 49 / 52 m). img-10: qualitative section, consistent with the modelled centreline section (gentle ramp on the offshore side, steeper inner side), no numbers.

## Sources and how each was used (audit 2026-10-10)
| source | location | used for | how | accuracy | status |
|---|---|---|---|---|---|
| Blacka et al. (2013) WRL TR 2012/08, https://doi.org/10.4225/53/58e1dc7368c7a (Lior's copy, papers/) | Fig A.2 p.93 (PDF p.105) [img-26] | plan, scale, crest and set-out levels, contours, slopes | silhouette traced by hand-picked vertices; scale from four printed dimensions; labels read by eye | scale +-3 %, area +-6 % | primary |
| same | A.1.1-A.1.5 p.92-93, Tables 4.2-4.4 p.65-69 | 140 x 70 m, 275 m, 3.0-6.0 m depth, crest 1.0-2.5 m below MSL, 5,500 m3, tide range 0.8 m | read from text; compared with the traced model (validation) and 5,500 m3 used to fit the bed (A3) | 'approximately' | validation + one fitted input |
| Pattiaratchi (1999) CWR UWA ED1483CP, http://joas.free.fr/studies/bei/g2s/reefdesign.pdf (mirror, accessed 2026-10-05) | p.2-4, Fig 1, 3-7 [img-15..23] | MTL 0.78 m above datum, 3 m contour extension, 1:20 slope to the 1 m contour, 250 m offshore, 45 deg peel angle, Fig 7 plan | text read; Fig 7 V outline traced (18 vertices, 100 m grid assumed A8) | Fig 7 +-1 grid cell | datum + cross-check |
| Raised Water Research (2019) Cables Reef, https://raisedwaterresearch.com/spot/artificial-reef/australia/western-australia/cables-reef/ (accessed 2026-10-06) | 'original design' [img-05], 'additional fill area' 320 m3 [img-06], Pitt 'Cables Drawing' [img-07], side view [img-10], stats images [img-11..13] | img-05 re-trace check; img-06 extension; img-07 bed gradient 1:30 and concept version; img-10 qualitative section check; img-11..13 context only | img-06 triangle registered on P2, P1; img-07 contour rows read with printed scale bar | extension +-30 % | secondary |
| Mead and Borrero (2011) Coasts and Ports 2011, https://search.informit.org/doi/10.3316/informit.715072832934166 (Lior's copy) | p.2 | 5,000 m3 (sensitivity of the bed fit) | text read | - | comparison only; it says limestone, Blacka says granite (unresolved) |
| Wikipedia, Multi-purpose reef (accessed 2026-09-24) | card R1 | 3,500 m3 (sensitivity of the bed fit) | read | weak secondary | comparison only |
| Reef card 02_research/reefs/cables-reef-wa.json | R2, R5 | '> 10,000 t' (density check 1.82 t/m3), Pitt 2009 'crest ~1.5 m below lowest tide' | read | R5 was blocked, second-hand | validation only |
| Pitt, A. (2009) assessment, via the card (SurfingRamps.com.au) | card dossier | crest depth cross-check | second-hand, original not read | - | context only |
| Lyons (1992) UWA design report | via Blacka Fig A.2 | origin of the design drawing | not read | citation details not confirmed | cited via Blacka |
| Ranasinghe et al. (2001); Pattiaratchi et al. (2003) COPEDEC VI Colombo 15-19 Sep 2003; Bancroft (1999) UWA thesis | cited by Blacka / dossier | nothing in the model | not read | - | wanted for as-built levels (REQUESTS_FOR_LIOR.md) |
| Gemini folder | - | not used (not in this repo) | - | - | rejected by rule 2 |
| Own scripts ../scripts/ (trace_a2.py, compute_shape.py, make_overlays.py, make_shape_json.py) and build_3d.py | - | every derived number | python (numpy, scipy, skimage, shapely) | - | reproducible |
Assumptions A1-A11 and decisions X1-X8 are listed in METHODS_3D.md sections 9 and 10.
