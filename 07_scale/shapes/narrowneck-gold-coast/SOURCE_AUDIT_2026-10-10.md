# SOURCE AUDIT 2026-10-10 - narrowneck-gold-coast (shape files, VERIFY.md, 3d/ model and viewer, image registry)

Auditor: fresh agent (Sonnet 5.5), standard in `_agent_briefs/task_source_audit.md`. Scope: `shape.json`, `HANDOFF.md`, `VERIFY.md`, `sources.md`, `3d/METHODS_3D.md`, `3d/SOURCES_3D.md`, `3d/model.js` / `docs.js` / `index.html`, `3d/MAIN_TYPED_TEXTS.json`, registry `03_images/reefs/narrowneck-gold-coast/`. The reef card was read, not edited.
Method: claims were traced to the saved PDFs / images by short text searches (pymupdf, `-I`), not by re-reading the sources. No model value was changed. `model.js` was regenerated and compared field by field with a build of the unmodified script (only `versions_info` and `confidence_3d.reason` text differ). Status: ok = traced and consistent; fixed = corrected or completed in place; missing = no source reachable (listed in REQUESTS); mismatch = values differ between files (recorded, not changed).
Abbreviations: cor23 Corbett et al. 2023; vds21 Vieira da Silva et al. 2021 (Accepted Manuscript, AM); jack12 Jackson et al. 2012 (ICCE, PDF page n); jack07 Jackson et al. 2007 (repository copy, "Page n" printed on it); msq Maritime Safety Queensland.

## Table 1 - statements and numbers
| # | statement / number | source | location | how used | status |
|---|---|---|---|---|---|
| 1 | Corbett 2023: authors, title, conference, pp. 663-669 | PDF in papers/ | printed page numbers 663..669 on PDF pages 1..7 (checked); publisher/venue wording | citation | fixed (pages confirmed; venue = Australasian Coasts & Ports 2023, Sunshine Coast, 15-18 Aug 2023, as printed on page 1) |
| 2 | Option 2 was built; north reef almost fully achieved; south reef and bridge only partly | cor23 | PDF p.3 ("north reef design shape was almost fully achieved ... only partial completion of the south reef and the bridge"), Sec 4.2.6 PDF p.5 | state drawn; version 2 note | ok |
| 3 | Design crest -2.5 m AHD = -1.5 m LAT | cor23 PDF pp.2-3; jack07 Page 7 (printed) and Page 10; council TOP_REDUCED_LEVEL | quote | crest target | ok |
| 4 | Measured crest -2.2 m AHD after the 2018 top-up | vds21 AM p.5, lines 137-138 | quote checked | crest of default surface (A16) | ok |
| 5 | AHD "equivalent to mean sea level" in vds21 | vds21 AM p.5 line 123 | new finding, supports a small AHD-MSL offset (here 0.12 m) | context for A10 | fixed (added to A10) |
| 6 | Design reef between the -2 m AHD and -10.4 m AHD contours; extent 200-350 m alongshore, 400-500 m cross-shore | vds21 AM p.5, lines 123-126 | quote checked (cites Black 1999; Jackson and Hornsey 2002) | context; envelope sizes not used as outline | ok |
| 7 | Survey date of vds21 Fig 3 (survey 1) = 19 Jul 2018 | vds21 AM p.8 line 176; p.12 line 312 | build_3d.py text said 18 Jul 2018 | caption of seabed check | mismatch -> fixed (build_3d.py, model.js `confidence_3d.reason`; METHODS and SOURCES already said 19 Jul) |
| 8 | Seabed -4/-5 inner, -6..-8 under the reef, -9/-10 seaward (+-1 m) | vds21 Fig 3 (img-31), read by eye once (annotation A3) | | check of the bed profile; seaward bed | ok |
| 9 | 408 geotextile bags, 20 m long, 3-4.5 m diameter | jack07 Page 4 (PDF p.5) | quote checked | container facts | ok |
| 10 | 450 containers placed since 1999, 42 of them in three maintenance campaigns | jack12 p.3 | quote checked | count (A13) | ok |
| 11 | 8 of 42 maintenance containers damaged or missing, 6 buried | jack12 p.6 | quote checked | A13 caveat | ok (added to A13) |
| 12 | +84 containers June 2018 around the existing structure | City of Gold Coast 2020 archived page; cor23 abstract | | count; state | ok |
| 13 | 534 containers = 450 + 84 | derived | | cross-check only | ok (A13: none assumed lost) |
| 14 | 60,000 m3 of sand for Narrowneck; 147 m3 per container (60,000/408) | jack07 Table 2, Page 13 | Narrowneck column of the comparison table (checked) | volume cross-check (4.5) | fixed (cited to Table 2; assumption A12 added; applying 147 m3 to the later 126 containers is an assumption) |
| 15 | Placed sand 78,500 m3 = 534 x 147; mound envelope 13,495-21,271 m3 = 17-27 % | build_3d.py, model.js `validation.volumes` | 13,495/78,498 = 0.17; 21,271/78,498 = 0.27 | cross-check | ok |
| 16 | Datum: AHD = LAT + 0.760 (Seaway); MSL 0.88, MLWS 0.22, MLWN 0.51, MHWN 1.24, MHWS 1.53, HAT 2.03 above LAT | msq 2014 / 2026 | 07_scale/bathymetry/gold_coast/REPORT.md section 3 (lines 62-67, quoted) | tide planes, z_MSL = z_AHD - 0.12 | ok (original MSQ pages not re-opened; REPORT quotes them) |
| 17 | z_MSL levels in model.js: LAT -0.88, MLWS -0.66, MLWN -0.37, MHWN +0.36, MHWS +0.65, HAT +1.15; AHD offset 0.12 | model.js `levels`, `datum` | recomputed from row 16 | viewer | ok |
| 18 | Papers' rule AHD = LAT + 1.00 (0.24 m difference) | jack07 Page 7; cor23 p.3; REPORT remark (ii) | | viewer switch; open question to City | ok (decision N4, assumption A10) |
| 19 | Crest below LAT: 1.44 m (MSQ) / 1.20 m (papers); design 1.74 / 1.50 | build_3d.py `stats.crest_below_LAT_m` | arithmetic on rows 4, 3, 16, 18 | caption | ok |
| 20 | Plan: 7 polygons, 6,239 m2 (arms 5,948), N arm 3,678, S arm 2,269 | shape.json canonical; trace_s3.py; s3 = img-45 | recomputed values equal shape.json `outline_versions[0].area_m2`, model.js, METHODS 4.1, HANDOFF 3a | default outline | ok |
| 21 | Scale 0.263665 m/px, shoreline bearing 356.21 deg, frame origin lat -27.986800 lon 153.431127 | shape.json; HANDOFF 3a | Web-Mercator z19; waterline of s7 | frame | ok |
| 22 | Areas of the other versions 13,941 / 13,631 / 4,922 / 537 m2 | shape.json outline_versions == model.js versions | identical | versions | ok |
| 23 | Volumes 13,495 / 21,271 / 13,603 / 6,856 m3 and uncertainties +-3,120 / 6,969 / 6,818 / 2,461 (bed +-0.5 m) | model.js == METHODS 4.1 == MAIN_TYPED_TEXTS tokens | identical | validation | ok |
| 24 | Design surface vs 53 multibeam blocks: mean +0.26 m, sd 0.66 m, r 0.76 | build_3d.py stats; METHODS 4.2 | | A4 check | ok |
| 25 | Corbett Fig 3 scale 0.4651 m/px, colour bar fit, registration (-5, 290) m +-10 m | prep_multibeam.py, SOURCES_3D step 0 | script re-runnable | seabed | ok (assumptions A1-A3) |
| 26 | Corbett Fig 2 bar 97 px = 50 m; no scale conflict with Jackson Fig 7 | VERIFY.md step 1 | chamfer fit s = 1.504, 0.65 px | version 2 scale | ok |
| 27 | Jackson 2007 Fig 13 bar 100 m = 428 px | img-27, VERIFY | 4.275 px/m +-1 % | design scale | ok |
| 28 | Navionics labels 7/8/9/10 m at y 402/411/474/514 m (+-20 m), LAT assumed | img-50 annotation A2; METHODS 3.3 | map centre = reef centroid | seaward bed only | fixed (centre-of-map assumption now A11; datum A6) |
| 29 | Navionics '0.9' label and nearshore contours not used | METHODS 3.3; REQUESTS | | none | ok (decision N6) |
| 30 | Nearshore bed 0 / -1.8 / -2.1 m AHD at y 0 / 100 / 190 | assumed | | visual only | ok (A7; flagged `estimated` in provenance) |
| 31 | Side slope 1.5:1, min. height 1.0 m, isolated container 1.8 m | assumed | | default surface | ok (A5; effect "not quantified" stated honestly) |
| 32 | Stage-1 height estimate 4-6 m at the toe | earlier agent estimate (HANDOFF 6) | refuted by multibeam relief 1-1.5 m (METHODS 4.3) | not used | fixed (HANDOFF marks it SUPERSEDED) |
| 33 | Gemini: two lobes, 400 x 220 m, 75,000 m2 | Gemini folder (read-only) | shape.json `gemini`; HANDOFF 9 | rejected | ok (now stated in METHODS 2b / 3.7) |
| 34 | Black and Mead 2001 (JCR SI 29, pp. 115-130), design crest -0.67 m AHD | quoted in vds21 AM p.5 only | web search found no matching record | history note only | missing -> REQUESTS (recorded "not confirmed") |
| 35 | Jackson et al. 2012: DOI 10.9753/icce.v33.structures.54 | | article URL icce-ojs-tamu.tdl.org/icce/article/view/6956 confirmed; DOI not confirmed | citation | missing -> "not confirmed" in METHODS 2; REQUESTS |
| 36 | Jackson et al. 2007: Shore & Beach 75(4), Fall 2007; pages 67-79 | repository PDF (Page 1-13); one citing paper gives 67-79 | author order on the repository copy: Jackson, Corbett, McGrath, Tomlinson, Stuart (the citing paper swaps McGrath/Tomlinson) | citation | fixed (Fall 2007 added; journal pages marked not confirmed) |
| 37 | Vieira da Silva et al. 2021: authors and DOI | AM title page | five authors, Coastal Engineering 171, 104027, AM from Griffith (CC BY-NC-ND) | citation | ok (AM page numbers used, stated) |
| 38 | Blacka et al. 2013: full citation | registry img-69 | WRL Technical Report 2012/08; doi:10.4225/53/58e1dc7368c7a; accessed 2026-10-07 | validation only | fixed (full citation added to METHODS 2 / 8) |
| 39 | Default outline = 2020 photo trace is Lior's decision D7 | root REQUESTS_FOR_LIOR.md, "Decisions taken" | 2026-10-10 | default_version | fixed (recorded in METHODS 3.8, shape.json `default_outline_decision` and `versions_info`, model.js `versions_info`, HANDOFF, VERIFY, registry img-45; stale "D7 open" removed) |
| 40 | Source ids differ: model ids (s3, cor23, vds21...) vs sources.md s1-s12 | | | traceability | fixed (crosswalk in METHODS 2b) |
| 41 | Registry: 78 rows, all files present, citation / url / licence / date / shows / how_used non-empty in every row, no row pending | images.json | script check | image rule | ok |
| 42 | HANDOFF "65 rows", "img-55 PENDING" | HANDOFF lines 7, 10, 24, 95 | registry has 78 rows, img-55 closed | consistency | fixed |
| 43 | Viewer shows source list with provenance (Sources tab), methods, assumptions, decisions | index.html, docs.js | before: methods only inside METHODS_3D.md (assumption table without effect, no decisions list) | rule 8 | fixed (three new chips; smoke test: 5 chips, tables render, no console errors) |
| 44 | Per-element confidence | METHODS section 6 | before: one overall paragraph | rule 6 | fixed (table) |
| 45 | Card says crest lowered 1 m before construction, about 1.5 m below low-tide waterline [R2][R3] | card `size`, `as_built_vs_design` | papers: designed -0.67 AHD (Black and Mead), Waikato -1.0 AHD, adopted -1.5 AHD for the 1999 contract (jack07 Page 4; vds21 p.5), later lowered to -2.5 AHD | | mismatch (wording; card not edited) |
| 46 | Card: about 70,000 m3 of sand, about 400 containers, A$30/m3 | card `size`, `cost` | jack07 Table 2: 60,000 m3, A$54/m3 (Narrowneck column); jack12: 450 containers by 2012, 534 after 2018 | | mismatch (card not edited; both sets are sourced, the card should show the disagreement) |
| 47 | Card footprint 350 x 600 m (R9) and 450 x 250 m (R8) | card | model: visible field 113 x 157 m, design envelopes about 13,900 m2, council polygon 171 x 262 m; vds21 gives 200-350 x 400-500 m | | mismatch (different definitions; stated in shape.json confidence factors) |

## Table 2 - the standard, item by item
| rule | finding | action |
|---|---|---|
| 1 every statement has a source | all numbers in rows 1-47 trace; three citation details unconfirmed (rows 34-36) | recorded, REQUESTS |
| 2 each source says how used | METHODS 2 listed contributions only | section 2b added (what, how, accuracy, element, role) |
| 3 methods explicit | scripts and numerical methods were spread over METHOD.md, SOURCES_3D, build_3d.py | METHODS 3.7 collects them; AI involvement stated |
| 4 assumptions labelled | A1-A10 without sensitivity or replacement | A1-A16 with effect and replacement (sensitivities taken from stored numbers: bed +-0.5 m = +-3,120 m3 (23 %), crest +-0.25 m = +-1,500 m3 (11 %), A4 sd 0.66 m); A5 effect honestly "not quantified" |
| 5 decisions logged | no list | METHODS 3.8: D7 (Lior) and N1-N14 (agent) with options, who, date, reason; Lior's own reason for D7 is not recorded and is not invented |
| 6 confidence per element | overall only | table in section 6 |
| 7 consistency | numbers equal across shape.json, model.js, METHODS, MAIN_TYPED_TEXTS (rows 20-23); mismatches: row 7 (fixed), 42 (fixed), 45-47 (card) | see rows |
| 8 viewer shows it | see row 43 | done |

## Values that look wrong (for main)
None in the model. Two points to watch, both documented: (1) the card's Narrowneck numbers differ from Jackson 2007 / 2012 (rows 45-47); (2) CLAUDE.md rule 4 ranks "design drawing of the built version" above "photo trace"; D7 deliberately chooses the photo, so the page's (i) text should say it is Lior's decision.

## Page text edits for main (04_build/data, NOT edited)
- `models3d_curated.json` models["narrowneck-gold-coast"].state_short: append " Default outline = Lior's decision D7 (2026-10-10)." after "(default; a lower bound)". Equivalent change is already in `3d/MAIN_TYPED_TEXTS.json` only if main copies the new sentence.
- The same file's `relied` / key_numbers `ids` use the model ids (s3, cor23, vds21, jack12, jack07, msq): keep; the crosswalk to the reference list is METHODS_3D 2b.
- No other old -> new changes: the volume and area tokens come from model.js and are unchanged.

## Files changed by this audit
`3d/METHODS_3D.md`, `3d/SOURCES_3D.md`, `3d/build_3d.py`, `3d/model.js` (text only), `3d/docs.js`, `3d/index.html` (chip list), `3d/REQUESTS_FOR_LIOR.md`, `shape.json` (text: `versions_info`, new key `default_outline_decision`), `HANDOFF.md`, `VERIFY.md` (appended; CRLF kept), registry `images.json` + `IMAGES.md` (img-45 how_used sentence), root `REQUESTS_FOR_LIOR.md` and `05_qa/00_STATUS.md` (appended).
