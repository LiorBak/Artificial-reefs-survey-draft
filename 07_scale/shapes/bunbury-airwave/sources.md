# Bunbury Airwave - shape-tracing sources

Re-done 2026-10-05 (resume run; the 2026-10-04 draft was treated as unverified notes). Every file in `src/` is listed here.
All images are private research copies (common.md rule 3). **Reuse rights are not cleared for any of them** - check with the rights holder before any public release.

| id | kind | title | url | source page | page/fig | image date | credit | license | retrieved | role |
|---|---|---|---|---|---|---|---|---|---|---|
| img1 | aerial_photo | Airwave-from-Above.jpg - near-nadir drone photo of the inflated bladder on the seabed | https://raisedwaterresearch.com/wp-content/uploads/2019/12/Airwave-from-Above.jpg?v=1576553483 | https://raisedwaterresearch.com/the-bunbury-airwave-artificial-reef-tears-during-installation/ (RWR tear post, 16 Dec 2019; the profile page serves a different, similarly named file) | header image of the tear post | taken during the Dec 2019 install week (tear spotted Fri 13 Dec; post 16 Dec; file upload `?v=` decodes to 2019-12-17 03:31 UTC); exact capture day not stated | Raised Water Research (photographer not stated) | not stated - NOT cleared | 2026-10-04 (md5 re-verified 2026-10-05) | primary |
| img4 | aerial_photo | ABC News video frame 11804314_0005.jpg ('Dream on hold for Bunbury surfers', ~00:03-00:05), oblique drone shot | https://abcmedia.akamaized.net/news/video/201912/airwave_high.mp4 | https://www.abc.net.au/news/2019-12-16/11804314 | video ~00:03-00:05; byte-identical to `03_images/video_frames/bunbury-airwave/11804314_0005.jpg` | 2019-12-16 | ABC News (Australia) | copyrighted news footage - NOT cleared | pre-existing in project | cross_check |
| img5 | design_drawing | ReefTopView.png - plan-view concept graphic: circle with concentric seam rings over a stock beach aerial, arrow labelled "30m" (NOT to scale) | https://raisedwaterresearch.com/wp-content/uploads/2019/09/ReefTopView.png | https://raisedwaterresearch.com/spot/artificial-reef/australia/western-australia/bunbury-airwave/ (also /progress-update-on-the-bunbury-airwave/) | gallery image | 2019-09-10 upload timestamp (`?v=1568074661` = 2019-09-10 00:17 UTC); pre-install concept | RWR profile page caption: 'Image: Unofficial Networks' (other diagrams there are captioned 'Image: Waveco') | not stated - NOT cleared | 2026-10-05 | cross_check |
| img2 | design_drawing | AirwaveDiagram2.jpg - oblique 3D concept render (no plan view, no scale) | https://raisedwaterresearch.com/wp-content/uploads/2019/09/AirwaveDiagram2.jpg?v=1568073278 | same RWR profile page | standalone render | 2019-09-09 upload timestamp (23:54 UTC) | Waveco via Raised Water Research | not stated - NOT cleared | 2026-10-04 (md5 re-verified 2026-10-05) | context |
| sat1 | satellite | Esri World Imagery at the card's coordinates (-33.31, 115.64), zoom 17 | https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer | n/a | n/a | 2025-08-30 (Esri identify) | Esri, Maxar, Earthstar Geographics, GIS User Community | Esri World Imagery terms | 2026-10-04 | context - shows the card coordinates are wrong (Bunbury boat-harbour groyne / Koombana Bay, ~2.2 km NE of the real site) |
| sat2 | satellite | Esri World Imagery, Bunbury Back Beach SLSC (-33.327276, 115.629902), zoom 18, r = 400 m | same | n/a | n/a | 2025-08-30 (Esri identify) | Esri, Maxar, Earthstar Geographics, GIS User Community | Esri World Imagery terms | 2026-10-04 | context - real site; used to estimate the approximate centre; no trace of the reef (expected: removed Dec 2019) |

Removed from `src/` on 2026-10-05 (not used): `img3` Airwave-Tear.jpg (underwater close-up of the torn seam, no plan information; https://raisedwaterresearch.com/wp-content/uploads/2019/12/Airwave-Tear.jpg) and `sat3` Esri Wayback release 4756 (2019-12-12) tile, whose imagery at this spot dates from 2016-03-03, i.e. before the reef existed; the next release (2020-01-08) postdates removal. No satellite imagery can show this reef.

## Design version
Only one version was ever built: the single 12 m inflatable bladder installed (about 90% complete) and torn (seam tear spotted by a diver on Fri 13 Dec 2019, reported by ABC on Mon 16 Dec). Its profile was asymmetric ('skateboard ramp', Bottegal in Tracks 2021) on a circular base. The planned redesign has only been tank-tested, never installed. `img5` and `img2` are pre-install concept graphics of the same circular dome, not alternatives. See `shape.json` -> `design_version`.

## Gemini checks (originals fetched by us, 2026-10-05; nothing from Gemini used)
| citation / url | verdict | evidence |
|---|---|---|
| https://www.abc.net.au/news/2019-12-16/airwave-artificial-surf-reef-bursts-bunbury-back-beach/11802958 (Gemini dossier) | wrong_site | HTTP 200 but the ID is an unrelated ABC Listen item (Townsville floods). Real article: .../word-first-surf-reef-tears-during-installation/11803228 |
| https://www.abc.net.au/news/image/airwave-torn-bladder-bunbury-2019.jpg (Gemini images_provenance.json) | dead | HTTP 404 |
| commons.wikimedia.org File:Back_Beach,_Bunbury,_January_2021_01.jpg / _02 / OIC_bunbury_back_beach_looking_N.jpg | dimension_not_in_source | Generic beach photos (_01/_02 25 Jan 2021 by Calistemon CC BY-SA 4.0; OIC photo 19 Oct 2006 by Orderinchaos), long after / before the reef; do not mention Airwave, 12 m or 38 m; show no structure |
| Bottegal, T. (2019) 'The Airwave Artificial Reef Project Brief' | unverifiable | no such document found online |
| Surfer Magazine 'The Bunbury Airwave Trial Review (2020)' | unverifiable | no such article found; the magazine was on hiatus 2020 to Aug 2024 |
| The Inertia 2019-12-18 'The Inflatable Artificial Reef in Australia Popped During Installation' | unverifiable | site returns 403 to scripts; real Inertia article has a different title |
| Gemini's own shape (reef_footprints.json id 'bunbury') | formula, not a trace | regular 24-gon R = 6.0 m centred 38 m from an invented origin; its coordinates (-33.3362, 115.6261) are ~1 km south of the real site. Other Gemini claims (helical screw anchors, 130 t, crest 1.8 m, 'Airwave Ltd', hemispherical dome, zero refraction) contradicted by sources, see `shape.json` -> `gemini.other_claims_checked` |

## Notes
- `img1` and `img4` show the same scene (same buoy, tether line and ring/valve mark): corroborating, not independent, evidence.
- Neither carries a scale bar or geo-reference; the 12 m scale comes from text (ABC, Raised Water Research, Bunbury Mail), so size agreement with the text is by construction. See `METHOD.md`.

## Verification additions (2026-10-05)
- Text sources added to `shape.json` references: R5 (RWR tear post, host of img1), R9 (Tracks 2021-10-08, profile and redesign), R10a (Tracks 2019-11-15, 12 m / 1.6 m / ~45 m off low-tide mark), R10b (Tradie 2019-01-31, circular base; seen in search-result text only, page 403 to scripts).
- A fifth RWR image (profile-page hero `uploads/2019/09/Airwave-From-Above.jpg`, 700x467 oblique) was looked at but is not in `src/` and is not used for any number.
- All four image sources re-downloaded and md5-matched on 2026-10-05 (img4 matches the project video frame; the ABC video page is live).

## Registry ids (added 2026-10-06, image registry backfill)

Every image is registered (citation + 'how used') in 03_images/reefs/bunbury-airwave/images.json (IMAGES.md).

| source id | registry id |
|---|---|
| img1 | bunbury-airwave-img-06 |
| img4 | bunbury-airwave-img-08 |
| img5 | bunbury-airwave-img-10 |
| img2 | bunbury-airwave-img-07 |
| sat1 | bunbury-airwave-img-11 |
| sat2 | bunbury-airwave-img-12 |
