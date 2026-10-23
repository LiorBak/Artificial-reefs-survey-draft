# SOURCE_AUDIT 2026-10-10 - mount-maunganui-reef (3D model, shape files, image registry)

Standard: `_agent_briefs/task_source_audit.md`. Scope: `3d/METHODS_3D.template.md` (-> METHODS_3D.md, docs.js), `3d/mmr_text.py` (model.js sources/provenance), `3d/SOURCES_3D.md`, `shape.json`, `HANDOFF.md`, `03_images/reefs/mount-maunganui-reef/`. No model value was changed; model.js was rebuilt and compared with a rebuild from the old text: only 4 `sources[].citation` strings differ. BoPRC report page numbers re-checked against `src/boprc_report.pdf` (printed page = PDF page - 1). Status: ok / fixed / missing / mismatch.

## A. Statement table
| statement / number | source | location | how used | status |
|---|---|---|---|---|
| Completed mid-2008 | Dahm & Gibberd (Focus) 2013, Focus Report 131 (BoPRC) | printed p6 | state drawn (A1) | ok (text confirmed) |
| 80 x 70 m built size | same | p6 (footnote: Scarfe p271, 79 x 67 m) | compared only | ok |
| Consent depth 3.7-4.6 m (pre-reef) | same | p6 | bed evidence | ok; earlier notes lacked the page, now cited |
| Crest 0.8-1.0 m below CD | same | p21 (PDF 22), p6 | crest -0.9 (A3) | ok |
| Main-bag crest not changed 2008-2013 | same | p23 | crest | ok |
| Bed beside north arm 3.0-4.0 m (2008), 2.25-2.75 m (2013) | same | p23 | bed evidence | ok |
| Bed fluctuates > 1 m | same | p29 (PDF 30) | uncertainty | ok |
| 2,800 m3 built vs 6,500 m3 design; crest 0.5-1 m below design | same, citing "Mead (2011)" | p28 | volume check | ok; **text said "BoPRC, RWR and Mead&Borrero" as if independent: fixed, one origin (A11)** |
| Outline -2.0 m CD, 1,071.0 m2, 67.9 x 60.4 m | Fig 3 (img-08) | PDF p23 | plan | ok (re-computed by verifier; method now listed with scripts) |
| Fig 3 depth legend is Chart Datum | Fig 3 title block | | datum of 2013 bed | ok |
| Toe outline 1,424 m2, 73.9 x 62.5 m, scale 5.96 px/m +-6 % | ASR Installed (img-10) | registration `scripts/installed_toe.py` | plan v2 | ok; area effect of scale (+-12 %) added (A10); METHOD.md says +-4 %, verifier +-6 %: +-6 % used everywhere |
| Crest percentiles, RISE profile | Fig 5 (img-04) | hue decode | A4 | ok |
| MVD-53 = CD + 0.9622 m | NIWA HAM2006-133 s1 | | datum | ok; **authors were wrong ("Bell, Goring et al.") -> Bell & Lewis (web search; not confirmed on the PDF)** |
| HAT..LAT above CD, MSL 1.13 | LINZ standard port levels, Tauranga | row | tides | ok |
| Navionics datum = CD (RMS 0.30 m) | N1 vs Fig 5 | `nav_profile.py` | A5 | ok |
| Shoreline bearing 136.15-136.27 deg | Esri 2011-01-15 | Theil-Sen, 116 profiles | frame | ok; the template now states the method (A12) |
| Reef 257-324 m from MSL line; 2,400 m2; 79 x 67 m; surge 0.2-0.6 m; scour hole 7,500 m2 | Scarfe 2008 | p275, p282, p271-272, p264 | comparison | ok as recorded in METHOD.md; thesis not in repo, pages not re-opened |
| Moores 3.5 m x 50 m bags, 4.5 m | Moores 2006 NZ Geographic 78 | article | design only | ok; issue date not confirmed (REQUESTS) |
| Oct 2006 bed 2.0-3.7 m | Mead et al. 2007 Fig 12 | img-37 | bed evidence | ok; datum assumed CD (A13) |
| 2,800 of 6,500 m3 "in place"; 50 m closer to shore; 9 months 1 m low | Mead & Borrero 2011 | s3.1.4, s4.1.2, Fig 3 | notes | ok |
| P3 Fig 3 bottom fits toe outline IoU 0.87 | `fig3_asbuilt_check.py/.json` | | corroboration | ok |
| Removal 25 Sep-8/9 Nov 2014, NZ$87,000 | SunLive 10 Nov 2014 | | caption | ok (not re-fetched) |
| Consent "Aug/Sep 2000", 5 years | BoPRC p2/p5 say August 2000, p8 says September 2000 | | caption | ok; internal inconsistency of the report noted |
| Summary: "decision -4.0 +-0.5 m CD ... 3 m height" | METHODS_3D template s1 | | | **mismatch (stale after D1): fixed to -3.6 ASSUMPTION, 2.7 m (1.9 m at -2.8)** |
| BoPRC citation "Focus Resource Management Group (2013/14)" | report p2 | | | **fixed: Dahm & Gibberd, Focus Report No. 131, Dec 2013** (methods, model.js, registry) |
| Registry header "38 images" | images.json has 41 | IMAGES.md | | **fixed 41 / 13 used** |
| img-10 note "use -4.0 +-0.5" | superseded by D1 | images.json | | fixed (marked superseded) |
| HANDOFF "registry 38 rows / 22 images" | | | | fixed |
| Assumptions list without why/effect/replacement | | methods 3.5 | | fixed (A1-A14 table) |
| No decisions list; no per-source "how used" | | | | fixed (3.6 Decisions M1-M15; 2.1 table) |
| Confidence per element missing | | methods 6 | | fixed (table) |
| Viewer had Methods, Sources log, Requests only | | index.html | | fixed: tabs "Sources & how used", "Assumptions", "Decisions" (docs.js keys srcuse_md, assump_md, decis_md; rendered, no page errors) |

Counts: 31 statement rows checked; 20 ok unchanged, 11 fixed (of which 4 were text mismatches), 0 open missing except the citation items in REQUESTS_FOR_LIOR.md.

## B. For main: values and page texts (nothing edited in 04_build/ or the card)
1. No model value looks wrong. Note A11: the 2,800 m3 is one origin (Mead 2011), and -3.6 m was chosen to match it, so the volume does not validate the bed.
2. `04_build/data/models3d_curated.json` /models/mount-maunganui-reef/key_numbers/4/stated: "about 3 m (BoPRC text); 3.5 m = design maximum ..." -> "about 3 m (verifier's estimate, VERIFY.md item 4; not stated in BoPRC); 3.5 m = design maximum of the largest bags (Moores 2006)".
3. key_numbers/1/stated "2,800 m3 built volume (Raised Water Research, BoPRC p28)" -> "2,800 m3 in place (Mead & Borrero 2011 Fig 3 and s3.1.4; repeated by BoPRC 2013 p28 and Raised Water Research: one origin)".
4. key_numbers/2/stated "consent depth 3.7-4.6 m" -> add "(BoPRC p6, pre-reef)"; "Scarfe 2007 about 2.8-3.0 m" has no page: add the thesis page or "METHOD.md".
5. Source ids: the page uses the model's ids (R1 = BoPRC, R3 = RWR, R4 = Scarfe), the reef card uses R1 = Wikipedia, R2 = RWR...: two id spaces, state "model source id" in the 3D panel.
6. Reef card (do not edit; for main): `gaps`/`size` text "No crest-depth figure ... found in any source fetched" conflicts with BoPRC p6/p21 (0.8-1.0 m below CD); card still has no Dahm & Gibberd (2013) or NIWA entry as its own reference (BoPRC is cited only through the images).
7. models3d_caveats rows for this slug were not checked line by line (only the curated key_numbers).
