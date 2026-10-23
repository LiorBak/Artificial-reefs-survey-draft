# FEASIBILITY - Opunake reef plan shape and 3D model (updated 2026-10-13, after TRC 2009-33 and NZ Geographic)

## Verdict 2026-10-13
- Can the reef's own SHAPE (bag outline) now be shown? NO. Confidence that it cannot: high. Neither upload draws the bag layout: TRC 2009-33 gives only a bounding size and a location figure, NZ Geographic has no Opunake figure.
- Can its POSITION and SIZE now be stated? YES.
  - Position: the reef lies inside the legal occupation area of Coastal Permit 6376-1 (31 May 2005): four published corner co-ordinates (Taranaki local circuit grid = NZGD49 Taranaki Circuit) = a 189 x 94 m rectangle (17,726 m2), long axis bearing 63 deg, centre lat -39.45943, lon 173.85163 (TRC 2009-33 Appendix I, PDF p. 39). Confidence medium-high: the corners close as a rectangle, agree with the consent's map reference P20:832-937, and with the white rectangle of TRC Figure 1 (georeference residual 0.3 m, independent boat-ramp check 0.7 m, pick error 5-10 m). One printed easting is a misprint (257484 for 267484), corrected and documented.
  - Size (design, consent stage): about 99 m long x 30 m wide x 3.5 m high, area about 2,970 m2 (= 99 x 30, a bounding rectangle, not the true footprint), volume about 4,900 m3 (TRC printed pp. 3-4). Built in 3.0 to 1.8 m water depth below chart datum (= LAT) with the shallowest contour at 0.0 m below chart datum. 27 bags in place as of April 2008, fine-tuning (filling) still planned for 2009/2010; the reef was "basically in place" in Sept 2009 (TRC pp. 4, 15).
  - Where the reef lies INSIDE the occupation area is unknown: +-47 m along the axis, +-32 m across, and the axis is assumed parallel to the long side (assumptions A7, A8). The imagery (LINZ 2011-12, 0.4 m) shows no structure.
- The 90 x 20 m versus 30 x 100 m conflict is resolved: 99 x 30 m (consent-stage design, TRC) equals Blacka et al. 30 x 100 m; 90 x 20 m is the 2004 concept quoted in The Daily News of 11 June 2004 (bags 1.5-2 m high), which Newsroom 2021, RWR and SurferToday repeat.
- 3D model: still NO. No bag layout, no per-bag crest levels, no surveyed seabed; only one design sentence on the crest datum. Not built.

## Recommendation for main (page; nothing was un-hidden)
1. Keep the reef hidden as a SHAPE (Lior's rule of 2026-10-10: do not show shapes we do not know). shape.json status is now "envelope_only", so even if the footprint flag were removed the compile step keeps it hidden.
2. Use the new facts on the card/page: lat/lon to the consent centre (-39.45943, 173.85163; the old -39.46, 173.86 is 720 m east), size 99 x 30 x 3.5 m, volume 4,900 m3, crest/bed depths with datum. The card (02_research/reefs/opunake-reef.json/.md) already carries them.
3. Optional, Lior's decision: show the consent occupation area only, labelled "Consent occupation area 2005, not the reef outline", with the (i) text in shape.json versions_info. To do that: status "traced" in shape.json and remove display:false from 07_scale/reefs/opunake-reef.footprint.json. The 99 x 30 m rectangle (assumed placement) should stay unshown.

## What we know now / what is still missing
| need | state 2026-10-13 | source |
|---|---|---|
| position | consent area, centre -39.45943, 173.85163, +-47 / +-32 m for the reef inside it | TRC App. I PDF p. 39; Fig 1 |
| size | 99 x 30 x 3.5 m, 2,970 m2 (bounding), 4,900 m3 | TRC printed p. 4 |
| crest level | shallowest contour 0.0 m below chart datum (LAT) | TRC printed p. 3 |
| seabed | 1.8-3.0 m below chart datum (thin sand on rock, no excavation) | TRC printed pp. 3-4; Blacka 2013 Table 4.2 |
| state | 27 bags by April 2008; not finished Sept 2009; works Feb 2007 - May 2008 per sign (last digit blurred) | TRC printed pp. 4, 15; Photograph 2 |
| cost | north reef about NZ$1.3 m (2006 plan); bond NZ$50,000 (consent 6377-1 cond. 18) | NZ Geographic; TRC printed p. 6 |
| bag layout / plan drawing | MISSING | - |
| as-built survey (+-5 m) | MISSING (consent condition 10 required it within 90 days of completion) | held by TRC, STDC, LINZ Hydrographic Office |
| post-construction dive survey | MISSING (recommended for 2009-10, TRC printed p. 18) | later TRC report |
| tide levels with datum | still to fetch (LINZ tide tables) | - |

## What would give the bag layout (in order of value)
1. TRC / South Taranaki District Council consent file (Official Information request, REQUESTS E11): the detailed design plan (consent 6377-1 condition 3), the engineer's as-built confirmation (condition 9), the survey map of the reef position (condition 10), structural-integrity reports (condition 15) and any later monitoring report (dive survey 2009-10).
2. Black, K. and Mead, S. (2006). Opunake Reef Construction Manual. ASR Limited for the Opunake Reef Trust (cited in TRC bibliography, printed p. 20; not found online 2026-10-13).
3. Black et al. (2004), Studies for Resource Consent (REQUESTS P9; ResearchGate login).
4. Google Earth Pro history 2007-2012 (REQUESTS G8) over the now-exact target: look inside the 189 x 94 m rectangle at the four corners given in consent_georef.json for a pale bag field.
5. LINZ nautical chart of Opunake (reef symbol / obstruction) via the Hydrographic Office.

---
# History: FEASIBILITY as of 2026-10-10 (kept for the record; the verdict and position items above supersede it)

Earlier verdict (2026-10-10, SUPERSEDED in part by the section above): NOT feasible with what we held. No plan shape drawn, no 3D model built.

## What we have
- Size, text only: bags "around 90 m long and 20 m wide" (Newsroom 2021, Raised Water Research, SurferToday - one lineage), 27 sand-filled geotextile bags by 2009, north reef only, designed for one right-hand wave (card R1-R4).
- Four Esri World Imagery frames (capture 2025-01-16, 0.115 m/px). Reef not visible (submerged bags, breaking waves and turbid water; frame mostly beach). overlays/search_frame_z20_no_structure.png.
- Rough site: "north side of the cove", township 39.450 S 173.850 E, surf break 39.46 S 173.86 E - position uncertain by several hundred metres.
- Tide hint: surf-forecast sample high 2.94 m / low 0.47 m (datum not stated).

## What is missing
| need | why | who/where |
|---|---|---|
| Plan drawing or as-built survey of the reef (position, outline, bearing) | no shape without it | Black et al. 2004 "Studies for Resource Consent: Opunake Surfing Reef" (ResearchGate 273133845), ASR Ltd design reports, South Taranaki District Council / Taranaki Regional Council consent files, NZ Geographic 078 figure |
| Aerial imagery when the reef was fresh and water clear (2008-2012) or a calm-day imagery | reef may show as a pale bag field | Esri Wayback releases, LINZ Basemaps / Taranaki aerial flights, Google Earth Pro history (Lior) |
| Crest level with a datum (design said wave height 1.8-2.5 m; crest depth not in any source) | 3D crest | consent report; LINZ chart datum / NZVD2016 |
| Seabed depth around the reef | 3D seabed | LINZ nautical chart (Opunake / Cape Egmont), LINZ bathymetry, Navionics app reading (Lior) |
| Tide levels (LINZ tide predictions, nearest port, with datum) | water levels | LINZ tide tables |
| Bag size / volume | volume | consent report |

## Needs network (container allows only package servers)
- https://basemaps.linz.govt.nz and https://data.linz.govt.nz (Taranaki aerial imagery, charts, bathymetry) - position/visibility, seabed.
- Esri Wayback releases for tiles around -39.457, 173.854, z18-20, any date 2008-2025 - structure visible when new / clear water.
- https://www.nzgeo.com/stories/artificial-surf-reefs-coming-to-a-beach-near-you/ (R3) - design figure/dimensions.
- https://www.researchgate.net/publication/273133845 - blocked by bot check (Lior in a browser).
- https://raisedwaterresearch.com/spot/artificial-reef/new-zealand/north-island/opunake/ gallery; southtaranaki.com Opunake pages; Taranaki Regional Council consent records.

## For Lior
Google Earth Pro: historical imagery 2007-2012 over lat -39.457, lon 173.853 (look for a pale rectangle ~90 x 20 m offshore; give date, lat/lon of both ends). Navionics: soundings along a line off the beach. Papers: Black et al. 2004. When any of this exists, re-run the trace (METHOD.md steps) then 3D.

## Checked in the second pass (2026-10-10)
- papers/ (all 5 PDFs, text layer): Opunake appears only in text and tables: Mead & Borrero 2011 p.1,3-4; Rendle 2016 thesis Table 2.1 (p.41) + references (p.298); Blacka et al. 2013 Tables 4.1-4.4 + references. No plan figure, no coordinates, no crest level. The 2007 Mount Maunganui paper is scanned (no text; not OCR'd) and is about Mount Maunganui.
- Gemini extracts: no confirmable original source; its Opunake dimensions are self-contradictory. Not used.
- WebSearch (9 queries, list in sources.md): only text (90 x 20 m, 27 bags, 1.5-2 m high bags). No plan, no coordinates, no survey, no aerial of the bags.
- Old wedge in 07_scale/reefs/opunake-reef.footprint.json is now flagged DO_NOT_DISPLAY inside the file (schematic analogy, not the reef's shape).
- Size values disagree and both are kept on the card: 90 x 20 m (news/RWR lineage) vs 30 m longshore x 100 m cross-shore, depth 1.8-3.0 m, ~300 m offshore, at LAT (Blacka Table 4.2).

## What would give a shape (documents, in order of value)
1. Taranaki Regional Council (2009). Opunake Artificial Reef Monitoring Programme 2005-2009. Technical Report 2009-33, Stratford, NZ. Monitoring surveys, probably bathymetry/bag positions. NOT in papers/. Ask TRC (public technical report) or Lior via a browser/library.
2. Black, K.P. et al. (2004). Studies for Resource Consent: Opunake Surfing Reef. ASR Ltd technical report for South Taranaki District Council (ResearchGate 273133845). NOT in papers/ (full author list and exact title to confirm from the page).
3. Mead, S.T. and Black, K. design report/dossier for Opunake (ASR Ltd, c.2005-06; Gemini cites "Mead & Black 2007 Design Dossier", unverified). NOT in papers/.
4. Moores, A. (2006). Artificial surf reefs - coming to a beach near you. New Zealand Geographic 078 (Mar-Apr). Pre-construction design figure possible. NOT in papers/ (web text only, figure not seen).
5. Dated imagery: Google Earth Pro history 2007-2012, LINZ/Taranaki aerials, Esri Wayback (networks blocked here).
Already in papers/ (no plan): Mead & Borrero 2011, Rendle 2016, Blacka et al. 2013.
Until one of 1-5 arrives: shape.json stays no_source, no outline anywhere (Lior 2026-10-10: do not show shapes of reefs we do not know).

## Why this reef is hidden on the page, what was checked, what is assumed (source audit 2026-10-10)
Rule (Lior, 2026-10-10): shapes we do not know are not shown. Opunake is hidden (footprint.json display:false / DO_NOT_DISPLAY; shape.json status no_source).
- Why: no plan figure, no survey, no reef coordinates, and the structure is not visible on the satellite frames we hold (bags are submerged, water is turbid). The only size is text, and two sources disagree: 90 m x 20 m (Newsroom 2021 / Raised Water Research / SurferToday, one lineage) vs 30 m longshore x 100 m cross-shore, depth 1.8-3.0 m, ~300 m offshore at LAT (Blacka et al. 2013, Table 4.2, printed p.65). Neither is drawn.
- Checked, with sources: Esri World Imagery 2025-01-16 (4 frames, 0.115 m/px); papers/ at the cited places (Mead and Borrero 2011 s.3.1.5; Rendle 2016 PhD thesis Table 2.1 p.41, refs p.298; Blacka et al. 2013 Tables 4.2-4.4); 10 web searches (TRC Technical Report 2009-33 and Black et al. 2004 not found online); Gemini extracts (self-contradictory, not used).
- Assumed (A1-A4 in shape.json): location only "north side of the cove" within a few hundred metres; not seeing the bags is not evidence of absence; the two sizes may measure different things; the built state is the unfinished north reef. Nothing numeric is assumed in a drawing because there is none.
- Confidence: plan none; position very low; size low; crest, seabed none; tides low. Full tables: SOURCE_AUDIT_2026-10-10.md.

## Network pass 2026-10-10 (verdict unchanged: no plan source)
Checked with network access: LINZ open aerials 2011-12 (0.4 m) and 2021-22 (0.25 m), tile BJ28_5000_0806, georeferenced crops in src/ (registry img-11, img-12); Esri Wayback 4 distinct versions 2015-2024 (img-13..16); RWR Opunake page text and gallery (already held). The reef is not visible in any: only breaking waves, no bag field or linear feature (no imagery from 2006-2010 exists at this tile in the open sets; LINZ 2000-2002 film is pre-construction, not fetched). Not reachable: NZ Geographic and trc.govt.nz (Cloudflare bot check, not bypassed), ResearchGate (login), TRC 2009-33 / Black et al. 2004 (not found openly), LINZ charts/bathymetry (login; open AWS buckets have none here). RWR text re-read: 1.8-2.5 m wave face, 100 m ride, 90 x 20 m bags, NZ$1.1 M allocated, over NZ$1.7 M spent by 2009. The size conflict (90 x 20 vs 30 x 100 m) remains. Shape stays no_source and hidden.
