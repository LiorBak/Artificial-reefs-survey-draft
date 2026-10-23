# FEASIBILITY - 3D model of kovalam-reef-india (2026-10-10)

Decision: **3D NOT built.** Plain-language reason and what would change it.

## What we have, per model input (brief model_3d.md STEP 1)
| input | what the sources give | source | verdict |
|---|---|---|---|
| a. plan shape | 5-6 sand-container strips fanning out, seen only in an OBLIQUE photo (no scale, no georeference). Outline traced in photo pixels; metric version is a camera-model estimate (see METHOD.md, VERIFY.md), LOW confidence | ASR aerial (img-07 / WRL Fig 4.5 = img-16) | weak |
| b. crest depth | "Submergence 0.2-3.4 m", datum not stated, probably a range across the reef, not tied to any position on it | WRL TR 2012/08 Table 4.2 p.66 (Blacka et al. 2013) | range only, unlocated, no datum |
| c. height, slopes | tubes about 30 m long (ASR via card R1); no height, no cross-section | card | missing |
| d. seabed | "Water depth 1.3-3.7 m" at the reef, "90 m offshore" to the pre-reef shoreline; no profile, no contours, no datum | same table | one range, no profile |
| e. tides | tide range about 1.0 m (Table 4.3 p.68); no MSL/LAT/MHWS levels, no gauge | same | range only |
Rule in the brief: build if plan, crest and seabed are sourced. Here crest and seabed are single ranges without position or datum and the plan scale is estimated; a model would be mostly assumption, and a 0.2 m crest next to a 3.4 m crest cannot be turned into a reef height without inventing which end is which. The structure also later sank and deflated (card; Rendle pers. comm. 2013 in Blacka et al. p.70), so there is no as-built survey to calibrate against.

## What is missing (in order of value; the first two are what Lior can do)
1. **Navionics / SonarChart readings** (Garmin Navionics, not for navigation) around the lighthouse end of Lighthouse Beach: depth at 5 points along a line from the shoreline at about 8.3875 N, 76.9750 E straight out to 250 m offshore, note datum. Gives the seabed profile (input d).
2. **Google Earth Pro historical imagery**, Feb 2010 - 2012 (Maxar): the reef strips may be visible from above, which would give the plan with a scale bar (input a). Note dates and the lat/lon of both ends of the strips and of the tombolo rock tip.
3. Esri Wayback z19 tiles for the 2011-02-28 capture (listed in HANDOFF.md section 7): the container strips are about 1 m wide features at 0.3 m/px; if visible, they give a georeferenced trace directly.
4. ASR Ltd technical report "Kovalam coastal protection" (ASR 2010a, cited in the reference list of Rendle (2016) PhD thesis, Univ. Plymouth, PDF p.279) or the CESS (Centre for Earth Science Studies) morphological assessment: design plan, crest levels, container dimensions.
5. A published Kerala tide table (Vizhinjam) for MSL, LAT, HHWL levels.

## What a future 3D could be
If 1 and 2 arrive, build with the Borth pipeline (07_scale/shapes/borth-coastal-defence-reef/3d/build_3d.py): strips as extruded tubes on a sloping seabed. Until then the model is held off the page ("Not yet modelled").

## Why this reef is hidden on the page, what was checked, what is assumed (source audit 2026-10-10)
Rule (Lior, 2026-10-10): shapes we do not know are not shown. Kovalam is hidden (footprint.json display:false).
- Why: the only picture of the structure is one oblique, unscaled ASR photo; it cannot fix the camera height, so the traced strips cover 546 to 1,681 m2 (versions H35 / H60 / H80). WRL Table 4.2 says 65 x 85 m; the default trace is 59 x 41 m (cross-shore -52 %). The true size and position are unknown.
- Checked, with sources: camera fit on the Esri 2011-02-28 frame (rms 2.2-2.8 px for H 30-80 m, rectify_result.json); Blacka, Shand, Carley and Mariani (2013) WRL TR 2012/08 Tables 4.2-4.4 (printed pp.66, 68, 69) and p.70; Mead and Borrero (2011) s.3.1.7 and 4.1.4 (4,000 m3, late Feb 2010, monitoring from the lighthouse platform); Esri frames 2011 and 2026 (reef not visible); RWR Kovalam Outline (foam line only); Gemini (unfetchable, not used).
- Assumed (ASSUMPTION, A1-A7 in shape.json): sea plane; pinhole camera; camera height 60 m by lens plausibility and WRL's 90 m (circular); 2011 swash line = 2010 beach; strips = whole reef.
- Confidence: plan LOW, position LOW-MEDIUM (+-20 m), crest/seabed none (unlocated ranges, no datum), tides LOW (range ~1.0 m). Full tables: SOURCE_AUDIT_2026-10-10.md.

## Network pass 2026-10-10 (result)
Still NOT built, still hidden. Checked: all Esri Wayback releases (no z19 before 2022; z17 1.19 m/px shows no strips in 2011-2020), surfingindia/Vimeo/RWR (no vertical image), searches for ASR 2010a and CESS (no open copy), web.archive.org unreachable here, surfer.com 403, Navionics needs a browser (none installed). Missing inputs unchanged: items 1, 2, 4, 5 above (Navionics readings, Google Earth Pro Feb 2010-2012 imagery, ASR/CESS report, Vizhinjam tide table). Details: METHOD.md section 6.
