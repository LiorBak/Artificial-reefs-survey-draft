# Project status — 2026-09-25 update

## 2026-09-25 additions (on top of the 2026-09-24 state below)
- **Media re-checked**: all 13 built reefs' images/videos re-verified (68 images, 29
  videos). 10 images moved to `images_rejected` (all Kovalam Reef India — wrong subject
  on re-fetch); everything else kept, each with a "shows=" label. 12 images and 18
  videos are labelled site-context-only / briefly-mentions and flagged for Lior's
  review. Full totals and the review list: `05_qa/media_recheck_summary.md`; every
  individual action: `05_qa/media_recheck_changes.md`.
- **Scale tab built**: a footprint scale-comparison view added to
  `04_build/artificial_reefs.html` for all 13 reefs (own build, `07_scale/`), checked
  against — but not copied from — a second AI's (Gemini's) independent attempt. Method,
  confidence levels and a per-reef summary table: `07_scale/README.md`.
- **QA round 6** (`04_build/QA/round6_browser.md`): Scale tab, media labels and a smoke
  test all pass; one non-blocking defect found (comparison table doesn't sort — see
  `04_build/README.md`). **Round 7** (re-test after the sort fix) has not run yet.

---

# Project status — 2026-09-24 (ALL AGENTS PAUSED on Lior's request; reef batch was mid-run — see per-item table for what finished)

## Decisions
- Focus for now: the 13 built artificial SURF reefs (section 1 of the page). Israel topics (section 2) and the 13 geotube/submerged-breakwater cases are PAUSED, not abandoned; everything researched so far stays on disk and the per-item chain is skip-aware, so resuming costs only the missing stages.
- Blocked/paywalled sources Lior can fetch by hand: `05_qa/blocked_sources.md` (heuristic scan; the explicit 'Blocked sources' sections in the dossiers are the reliable rows).

## Per-item state (what exists on disk)

| slug | kind | dossier | first line | claims QA | media QA | images idx | videos | frames | card json |
|---|---|---|---|---|---|---|---|---|---|
| al-aqah-beach-geotube-uae | reef | yes | # Al Aqah Beach Geotube Beach Nourishment — Al Aqah Beach, Fujairah, United Arab Emirates | - | - | - | - | 0 | unverified draft |
| al-yasat-aali-island-uae | reef | yes | # Al Yasat Aali Island coastal works (ICM) — Al Yasat / Aali Island, United Arab Emirates | - | - | - | - | 0 | unverified draft |
| borth-coastal-defence-reef | reef | yes | # Borth coastal defence reef (incl. Wallog headland) — Borth, Ceredigion, Wales, United Ki | - | - | - | - | 0 | unverified draft |
| boscombe-surf-reef | reef | yes | # Boscombe Surf Reef — Boscombe, Bournemouth, Dorset, United Kingdom | - | - | - | - | 0 | unverified draft |
| bunbury-airwave | reef | yes | # Bunbury Airwave — Bunbury Back Beach, Western Australia, Australia | - | - | - | - | 0 | - |
| burkitts-reef-bargara | reef | yes | # Burkitts Reef (Burkitt's Reef / "Greg's Reef") — Bargara, Queensland, Australia | - | - | - | - | 0 | unverified draft |
| cables-reef-wa | reef | yes | # Cable Station Reef (Cables Reef) — Leighton/Cottesloe, Perth, Western Australia, Austral | - | - | - | - | 0 | unverified draft |
| icm-california-headlands-unnamed | reef | yes | # Living Speed Bumps (RE:BEACH Oceanside pilot) — South Oceanside, California, USA | - | - | - | - | 0 | unverified draft |
| icm-queensland-sandbag-cliff | reef | yes | # Queensland clay-cliff "rock-look" sandbag wall (ICM transcript) vs. Scarborough Cliffs S | - | - | - | - | 0 | unverified draft |
| icm-uae-submerged-reef | reef | yes | # Fairmont Ajman Beach Stabilisation (ICM submerged reef) — Ajman, United Arab Emirates | - | - | - | - | 0 | unverified draft |
| japanese-artificial-reef-program | reef | yes | # Japanese 人工リーフ (Artificial Reef) Submerged Breakwater Programme — Multiple sites, Japan | - | - | - | - | 0 | unverified draft |
| kovalam-reef-india | reef | yes | # Kovalam Reef (Lighthouse Beach) — Kovalam, India | - | - | - | - | 0 | unverified draft |
| mexico-reef-2026-unnamed | reef | yes | # Xala Reef (Costalegre artificial surf reef) — Costalegre, Jalisco, Mexico | - | - | - | - | 0 | unverified draft |
| mount-maunganui-reef | reef | yes | # Mount Maunganui Beach Reef ("Mount Reef") — Mount Maunganui, New Zealand | - | - | - | - | 0 | unverified draft |
| narrowneck-gold-coast | reef | yes | # Narrowneck Reef (Gold Coast Reef) — Narrowneck, Gold Coast, Queensland, Australia | - | - | - | - | 0 | unverified draft |
| opunake-reef | reef | yes | # Opunake Surf Reef — Opunake, Taranaki, New Zealand | - | - | - | - | 0 | unverified draft |
| palm-beach-gold-coast | reef | yes | # Palm Beach Reef — Palm Beach, Gold Coast, Queensland, Australia | - | - | - | - | 0 | unverified draft |
| prattes-reef-el-segundo | reef | yes | # Pratte's Reef — El Segundo / Dockweiler State Beach, California, USA | - | - | - | - | 0 | unverified draft |
| sigandu-beach-breakwaters-indonesia | reef | yes | # Sigandu Beach low-crested breakwaters — Sigandu Beach, Central Java, Indonesia | - | - | - | - | 0 | unverified draft |
| southern-ocean-surf-reef-albany | reef | yes | # Southern Ocean Surf Reef ("Midds Reef") — Middleton Beach, Albany, Western Australia, Au | - | - | - | - | 0 | unverified draft |
| walkable-geotube-breakwater-unnamed | reef | yes | # Walkable geotube breakwater (unnamed) — location not stated, country not stated (ICM por | - | - | - | - | 0 | unverified draft |
| young-jin-beach-geotube-korea | reef | yes | # Young-Jin Beach Geotube Detached Breakwater — Young-Jin (Yeongjin) Beach, Gangneung, Sou | - | - | - | - | 0 | unverified draft |
| yucatan-geotube-mexico | reef | yes | # Yucatan Geotube submerged breakwater — Yucatan, Mexico | - | - | - | - | 0 | unverified draft |
| ashdod-sand-and-breakwater | israel | yes | Status: verified 2026-09-24 — 23 refs checked, 15 claims ok, 6 fixed, 2 dropped | yes | - | yes | - | 0 | - |
| ashkelon-geotubes-2018 | israel | yes | Status: verified 2026-09-24 — 23 refs checked, 16 claims ok, 6 fixed, 3 dropped | yes | - | - | - | 2 | - |
| econcrete-armoring-israel | israel | yes | Status: researched 2026-09-24 | - | - | - | - | 0 | unverified draft |
| haifa-bay-sediment-budget | israel | yes | Status: researched 2026-09-24 | - | - | - | - | 0 | unverified draft |
| haifa-port-sand-bypass | israel | yes | Status: researched 2026-09-24 | - | - | - | - | 0 | - |
| herzliya-marina-sand | israel | yes | Status: verified 2026-09-24 — 18 refs checked, 22 claims ok, 9 fixed, 0 dropped | - | - | - | - | 0 | - |
| israel-coastal-protection-audit-reports | israel | yes | Status: researched 2026-09-24 | - | - | - | - | 0 | unverified draft |
| israel-geotubes-other-sites | israel | yes | Status: verified 2026-09-24 — 10 refs checked, 16 claims ok, 3 fixed, 0 dropped | yes | - | yes | yes | 2 | unverified draft |
| israel-wave-climate-and-tides | israel | yes | Status: verified 2026-09-24 — 23 refs checked, 16 claims ok, 7 fixed, 2 dropped | yes | - | yes | yes | 2 | - |
| michmoret-ecological-reef-pilot | israel | yes | Status: verified 2026-09-24 — 17 refs checked, 33 claims ok, 1 fixed, 0 dropped | yes | - | - | - | 0 | - |
| netanya-cliff-protection | israel | yes | Status: researched 2026-09-24 | - | - | - | - | 0 | unverified draft |
| tel-aviv-detached-breakwaters | israel | yes | Status: verified 2026-09-24 — 18 refs checked, 12 claims ok, 5 fixed, 2 dropped | - | - | yes | yes | 1 | - |

## Pipeline per item
research → (media ∥ claims verify+fix) → media verify + card JSON. Script: reef-item-chain (Workflow), args {kind, slugs, done_research}.

## Next
1. Section 1 (13 world artificial surf reefs) built 2026-09-25: `04_build/artificial_reefs.html`. Two rounds of QA done (`04_build/QA/round1_browser.md`, `round1_content.md`, `round2_browser.md`); both round-1 blockers (hover overlay, modal reopen) confirmed fixed in round 2. See `04_build/README.md` for full summary.
1b. Section 1 enriched 2026-09-25 against a second AI's (Gemini's) independent attempt at the same task (`C:\Users\lior\Documents\Gemini\AG\artifical reef`, read-only, untouched): added reference pop-ups anchored to `[R#]` markers, surfer reviews as their own quote-card block, an at-a-glance strip + accordion (replacing tabs), and nav-label counts. 8 of 13 reefs had Gemini candidates checked by verification agents (fetch-and-confirm against the actual source); 0 new reference numbers were minted — accepted items slot into existing R6/R7/R11 or need no new one — while several Gemini quotes were rejected as fabricated/unverifiable (Opunake x3, Kovalam, Boscombe partial, Cables, Albany, Palm Beach partial). Full per-reef results: `06_gemini_compare/verified/*.md`; summary: `06_gemini_compare/README.md`. Two rounds of QA on the new UI (`04_build/QA/round3_browser.md`, `round4_browser.md`) both PASS, no blockers. Burkitts Reef's two video-frame images were removed (QA confirmed they don't show the reef) and moved to `04_build/QA/removed_assets/`; media review (videos/photos generally) is left to Lior, no new media was sourced.
2. Israel batch (kind=israel) and the geotube cases (kind=reef, P2 slugs) remain PAUSED on Lior's request.
3. Sections 2 (Israel sediment transfer) and 3 (Haifa conclusions) are placeholders pending Lior's go-ahead to resume that research.

## 2026-10-04 — paused at usage limit
Done: agent briefs in _agent_briefs\ (common, trace_shape, verify_shape, video_review, build_shapes_videos, qa_browser, wrap_report);
shape spec 07_scale\SHAPE_SPEC.md; tracing tools 07_scale\tools\ (tested); transcription tools 02_research\videos\tools\ (tested);
Gemini video extract 02_research\videos\00_gemini_video_extract.* (Gemini has no real transcripts; its video list was built from our folder).
In flight when paused: 13 shape-tracing agents (writing only to 07_scale\shapes\<slug>\; may be partial - check each shape.json "status").
Stopped: 7 video agents (Narrowneck, Cables, Pratte's, Mount Maunganui, Opunake, Boscombe, Kovalam) - re-run them; 6 never started
(Borth, Palm Beach, Albany, Burkitts, Bunbury, Xala) because of the 20-agent concurrency cap.
Next: finish/redo tracing where shape.json is missing -> verify_shape per reef -> video_review per reef (max 20 agents at once) ->
build_shapes_videos -> qa_browser -> wrap_report.

## 2026-10-04 (later) — video transcription paused on Lior's request
Video review packs finished: mount-maunganui-reef, prattes-reef-el-segundo, boscombe-surf-reef.
Stopped mid-run (re-run video_review.md for these when resumed): narrowneck, cables, opunake, kovalam, borth, palm-beach, albany.
Never started: burkitts, bunbury (verify Gemini's second ABC clip 11802958), xala.
Shape tracing continues for all 13 reefs.

## 2026-10-05 (evening) - 3D phase relaunched after the session-limit cut-off
- Lior's decisions:
  - model the as-built state, with later changes as notes;
  - no Haifa tide preset;
  - agents try the Navionics web chart themselves and add it as a source (reef cross-check only where the structure still exists);
  - whatever they cannot read goes to 3d\REQUESTS_FOR_LIOR.md (Navionics app + Google Earth Pro);
  - run 3 agents at a time.
  These decisions are recorded in _agent_briefs\model_3d.md.
- Running (Sonnet 5.5): 3D Pratte's (resume), 3D Palm Beach (resume), 3D Boscombe (resume).
- Queued next: Bunbury 3D docs retrofit (Step 6 + Navionics + relabel as sand-ballasted bladder), Mount Maunganui trace -> verify -> 3D.

## 2026-10-05 (late) - 3D batch results
- 3D DONE, Step 6 docs included:
  - Bunbury: medium; Hypalon rubber bladder; FAILED.
  - Boscombe: medium; as-built 2009.
  - Palm Beach: medium; as-built 2019.
  - Pratte's: low; Phase I 2000.
- Each reef has 3d\REQUESTS_FOR_LIOR.md (Navionics app points + Google Earth Pro).
- Navionics web chart (maps.garmin.com/en-US/marine) works without login; the datum is unstated, so it was inferred by an RMS test per reef.
- Pending Lior decision: download the 4.1 GB City of Gold Coast DTM (data.gov.au, CC BY 2.5 AU) for Palm Beach + Narrowneck seabed.
- Session limit (resets 12am) cut off the following; resume from their METHOD.md / SOURCES_3D.md:
  - Narrowneck trace: groundwork in METHOD.md, NEXT STEPS listed; scratch in %TEMP%\nn_trace.
  - Mount Maunganui trace.
  - Pratte's Borrero & Nelsen 2003 update.
- Build brief: three.js must be vendored locally into 04_build\3d\vendor\ (CDN unreachable from this machine).

## 2026-10-06 - Lior's decisions and new agents
- Lior said NO to downloading the 4.1 GB Gold Coast DTM (probably land only, too big). Agents must keep every download under ~50 MB.
- Pratte's: the 3D model was updated from Borrero & Nelsen 2003. That paper was supplied by Lior and is stored at shapes\prattes-reef-el-segundo\src\.
  - Confidence stays low.
  - Position hint moved about 217 m NNW to 33.92058, -118.43335 (±100 m).
  - Volume gap unresolved (443 vs 695-782 m3).
  - Shape flagged PENDING RE-VERIFICATION. The verifier must check the extra edits to shape.json.
- Running:
  - EMODnet bathymetry check: output to 07_scale\bathymetry\emodnet\.
  - Gold Coast government reports and depth check: output to 07_scale\bathymetry\gold_coast\.
  - Mount Maunganui trace: restarted.
- Next:
  - Narrowneck trace resume, using the gold_coast report.
  - Integrate EMODnet into Boscombe 3D and the gov depths into Palm Beach 3D.
  - Re-verify Pratte's shape.
  - Mount Maunganui verify, then its 3D model.

## 2026-10-06 (later) - Image rule; Mount Maunganui traced
- LIOR: "any image showing a reef should be in our folders and displayed in the html" (with full citation, link and how it was used for the model).
  New brief _agent_briefs\image_registry.md + common.md rule 6: every reef image is SAVED in our folders and REGISTERED in
  03_images\reefs\<slug>\images.json + IMAGES.md. This replaces the old link-only policy of 03_images\web\.
  build_shapes_videos.md gains section 3b: an Images gallery per reef + an Images tab driven by the registry ("Used for the model" line, full citation, annotated toggle).
- The Gold Coast and EMODnet agents were told to save and register their images. The image-registry backfill agent was started (all 13 reefs; Gold Coast reefs last).
- Mount Maunganui trace DONE (medium).
  - As-built delta-wing "7": 67.9 x 60.4 m, 1,071 m2 at the -2.0 m CD contour; toe outline 73.9 x 62.5 m, 1,424 m2.
  - Primary source: BoPRC Fig 3, 2013 multibeam survey; LINZ 2010-11 aerial agrees to ~2 m.
  - The survey footprint is 8-15% smaller than the BoPRC text. Partly removed in 2014.
  - 3D inputs are in METHOD.md (MVD-53 = CD + 0.9622 m).
  - Next: verify_shape, then 3D.
- Lior asked that new Gold Coast images be saved per reef as they are found, reported, and accounted for in the 3D checks:
  - Registry gains a "for_3d_check" field {pending, what_to_check, model_values_affected}.
  - New inbox 03_images\reefs\NEW_IMAGES_LOG.md (one line per new image) drives the page rebuild and the 3D re-checks.
  - model_3d.md gains STEP 0: view every pending image, confirm or contradict the model value, document it in METHODS_3D section 4, and clear the flag. A re-check run of an already-built model does only STEP 0 and the documentation.
  - After the Gold Coast agent finishes: Palm Beach 3D re-check run (STEP 0) on its pending images.

## 2026-10-06 (night) - EMODnet and Gold Coast reports done
- Agents' Write calls for REPORT.md were refused by the harness ("subagents should return findings as text"). The orchestrator saved both reports from the hand-backs:
  - 07_scale\bathymetry\emodnet\REPORT.md (+ agent_final_report.json.md);
  - 07_scale\bathymetry\gold_coast\REPORT.md.
  For future report-type deliverables, expect the same: save them from the hand-back.
- EMODnet:
  - Coverage: Boscombe and Borth only. DTM 2024, LAT, cells about 116 x 73 m; Haifa is interpolated cells only.
  - Boscombe: the reef is not visible. EMODnet is 1.8 +- 0.7 m deeper than the model seabed, and the offset is not constant. Take only the offshore slope beyond y = 380 m (-1.41 %), plus a validation row.
  - Borth: reef cells are GEBCO interpolation; surveyed cells start 335 m offshore (-1.1 %).
  - Lior requests: 07_scale\bathymetry\emodnet\REQUESTS_FOR_LIOR.md (CDI pages behind a bot check).
- Gold Coast:
  - The DTM has NO underwater cells at either reef (Q1 = no).
  - Palm Beach: crest -1.5 m MSL confirmed by 3 sources. The Mortensen 2015 pre-reef survey vs Navionics gives RMS 0.29 m after LAT->AHD, supporting LAT. PBO3 buoy depth is 11.75 m.
  - Narrowneck:
    - The built renewal is the AMENDED shape, with "minor changes".
    - The ~20 m seaward shift is unverified (Corbett 2023 is blocked).
    - The renewed crest is -2.2 m AHD (multibeam after 2018).
  - 51 images registered (Narrowneck img-01..36, Palm Beach img-01..15); Lior's four named images are registered.
  - Pending 3D checks are listed in the registry.
- Running: image backfill, Mount Maunganui verify, Borth verify.
- Queue (3D first):
  1. Mount Maunganui 3D
  2. Borth 3D
  3. Narrowneck trace resume (uses gold_coast REPORT section 6.5)
  4. Palm Beach 3D re-check (STEP 0 + REPORT section 5.3)
  5. Boscombe EMODnet integration (REPORT 9.1)
  6. Pratte's re-verify
  7. Trace the remaining 6 reefs

## 2026-10-06 (later) - Image registry backfill DONE (all 13 reefs)
- Registry: 03_images\reefs\<slug>\images.json + IMAGES.md for every reef; convention and counts in 03_images\reefs\README.md; check script 03_images\reefs\check_registry.py (run: PASSED, 0 errors, 0 warnings).
- 264 rows (205 by the backfill, 51 Gold Coast reports, 8 EMODnet): 259 display:true, 0 dead links, 122 used for a model/shape value, 64 with a pending 3D check.
  Per reef (registered / displayed): Narrowneck 44/44, Cables 23/22, Pratte's 32/32, Mount Maunganui 18/18, Opunake 10/10, Boscombe 29/29, Kovalam 14/14, Borth 16/16,
  Palm Beach 34/34, Albany 13/11, Burkitts 8/6, Bunbury 21/21, Mexico 2/2.
- Every hotlinked image was downloaded from its original URL; figures of PDFs were extracted (Mount Maunganui BoPRC Figs 1, 2, 5; Kovalam ASR brochure; Cables Pattiaratchi 1999 Figs 1-7);
  images > 10 MB also have a <=3000 px copy (Opunake, Burkitts, Palm Beach context). Several reefs gained images not on their cards (Albany RWR construction photos, Cables RWR drawings/tables,
  Kovalam brochure composite, Narrowneck ICM photos, Lior's image29 + YouTube screenshot).
- Every row has for_3d_check; one line per backfilled image is in 03_images\reefs\NEW_IMAGES_LOG.md. Pending 3D checks worth scheduling first: Albany (as-built berm on the 2026-01-20 Esri image vs design 110 m / -1.0 m AHD; design plan diagram to trace),
  Cables (original-design plan + Pattiaratchi Fig 7 apex/outline), Kovalam (stepped break-line vs smooth crescent), Mount Maunganui (BoPRC Fig 5 / 'Installed' depths), Boscombe (Raised Water / Echo aerials), Prattes (Fig 2 aerial position).
- Lior's four named images are registered: Palm Beach and Narrowneck DTM coverage overlays (palm-beach img-11, narrowneck img-22) and Jackson 2012 pages 3-4 (narrowneck img-01, img-02; 200 dpi renders in shapes\narrowneck-gold-coast\src\gov, the %TEMP% j12_p3/j12_p4 are lower-resolution scratch copies).
- Decisions for Lior/QA (listed in the README): Opunake and Kovalam images that the 2026-09-25 recheck rejected look genuine on re-view (registered with a note); Burkitts dive frames and Albany quarry/vessel-track images registered with display:false.
- Excluded on purpose: image26 and its RWR original, the Gemini folder, 3d\preview_*.png model screenshots, 07_scale\drawings, PDFs/GeoTIFFs (referenced through source_pdf).
- sources.md / SOURCES_3D.md of the reefs with shape or 3D work got a "Registry ids" note (no other edits; shape.json and model.js untouched).
- Image registry backfill DONE:
  - 264 rows across 13 reefs (259 display:true, 0 dead); check_registry.py passes.
  - Judgement calls for Lior:
    - Opunake/Kovalam RWR images rejected in the 09-25 recheck are kept as site context (display true);
    - Lior's image29 shows a webinar presenter's webcam thumbnail (privacy flag);
    - image26 and its RWR original are not registered.
  - Many new pending_3d_checks (Albany, Cables, Kovalam, Mount Maunganui, Boscombe, Pratte's, Burkitts, Palm Beach, Narrowneck, Mexico): every 3D or trace run must clear them (model_3d STEP 0).
- Started: Narrowneck trace resume (state = renewed June 2018; primary = Esri Wayback post-2018; design prior = Jackson 2012 Fig 7).

## 2026-10-07 (morning) - limit reset; 3D tab
- Resumed after the 10am limit: Mount Maunganui verify, Borth verify, Narrowneck trace.
- LIOR asked for a new "3D models" tab:
  - each model's viewer, with the pictures used to construct it below it;
  - hover shows how each picture was used and its source;
  - at the bottom: methods, texts relied on, caveats (e.g. model vs reported volume) and references.
  Brief: _agent_briefs\build_3d_tab.md (data-driven; vendored three.js; lazy iframes; caveats table in 04_build\data\models3d_caveats.json). Builder agent started.
- 4 agents are running (one above the 3 cap), because Lior asked to keep the three going AND to spawn one for the tab.

## 2026-10-06 (10:30 system time, after the limit reset) - Mount Maunganui shape VERIFIED
- Adversarial verification of 07_scale\shapes\mount-maunganui-reef\ finished: shape.json status "verified", verified_on 2026-10-06; VERIFY.md has checks 1-7 and the "3D inputs check".
- Confirmed: Fig 3 ticks (5.45 px/m), area 1,071.0 m2, 67.9 x 60.4 m, canonical frame (no make-canonical rotation bug); second raster of the same survey (BoPRC Fig 5) gives 1,074 m2 under -2.0 m, IoU 0.93; LINZ aerial position within 2 m. Overlays good (img1, img2) / approximate (img3). Confidence stays MEDIUM (outline 14-15 % below the 80 x 70 m text; area definition spread 1,071-2,400 m2).
- Survey-over-aerial as primary: justified (reef under 3-4.5 m of water, soft aerial edges); the outline is the lower-bound footprint, the toe outline (73.9 x 62.5 m, +-6 % now) is the as-built one.
- Corrections: removal ended over the weekend of 8-9 Nov 2014 (10 Nov = SunLive posting date; all bags above the seabed removed); consent lapse year 2010 is from NZ Herald, not BoPRC; "buried base bags" is BoPRC inference; Installed-image scale uncertainty +-6 %; Fig 5 added as ctx9.
- 3D INPUTS (METHOD.md annotated): MVD-53 = CD + 0.9622 m CONFIRMED (but present MSL is CD + 1.13 m, so label z = 0 as MVD-53); crest 0.8-1.0 m below CD CONFIRMED for 2013 (Installed legend is clipped at -1.8 m, not independent support); bed -4.5 m CD is the deep end, use -4.0 +-0.5 m (range -3.0 to -4.5); height 3.5 m is the DESIGN maximum (Moores 2006), use about 3 m +-0.5 (2013 exposed relief 1.5-2 m). New figures found in Scarfe 2008 p282: reef area 2,400 m2, crest -1.25 m MSL (max).
- Gemini: all six tracer verdicts confirmed after re-fetching the originals; added BoPRC "Decommissioning Report" (no such title), Wikimedia caption, SunLive / NZ Herald 2023 (correct, with Gemini errors listed), probable origin of 95 x 75 m (Moores 2006 design dims).
- Registry: no new rows (the backfill rows img-01..18 stand); img-04 (Fig 5) gained the verify overlay and results, img-06/-08/-09/-10 carry verifier results; img-08 and -09 pending false; img-04, -06, -10 stay pending for the 3D agent. check_registry.py passed. NEW_IMAGES_LOG line added. The RWR comparison graphic is not stored (README policy).
- Open items: Mead, Black & Moores (2007) "Amalgamating Design and the Constraints of Construction" and Mead (2011) may hold an as-built plan with a scale (no PDF found); the 3D agent should use the toe outline and the ranges above.
- LIOR (usage): subagents cannot be /compacted.
  - common.md rule 7 LEAN CONTEXT.
  - Rule 8 HANDOFF FILES: read only common.md + the brief + the folder's HANDOFF.md; ask the orchestrator (SendMessage "main" / NEEDS_CLARIFICATION) instead of reading everything; write a HANDOFF.md of max ~150 lines before finishing.
  - Large agents are restarted fresh from checkpoints rather than resumed.
  - Running agents were told to write HANDOFF.md: mount-maunganui, borth, narrowneck, 04_build.
  - QUEUED: one small agent to write HANDOFF.md for the reefs already done (prattes, boscombe, bunbury, palm-beach) and for bathymetry\emodnet and bathymetry\gold_coast, from their METHOD/METHODS_3D/REPORT files.

## 2026-10-06 (after the limit reset) - Borth shape VERIFIED, 3D inputs prepared
- shape.json status verified, confidence HIGH (reason rewritten; the tracer had left it "(provisional)" with design_version, dimensions_check, gemini and references empty). Files: 07_scale\shapes\borth-coastal-defence-reef\VERIFY.md (checks 1-7 + "3D inputs"), HANDOFF.md, METHOD.md step 4, scripts_verify\.
- Design version: the drawing is the BUILT final layout (Phase 1 completed 8 March 2012). HR Wallingford HRPP576 (2013): the original two surfable reefs became ONE surfable northern reef (boot) + a shore-parallel breakwater (the oval). No later extension, damage or removal found; imagery 2012-2024 and the 2022 LiDAR show the same two mounds.
- New primary sources: Royal Haskoning "For Construction" drawings 9V5090/1001, 1020-1023 (plan 1:500 georeferenced by 15 OS-grid setting-out points, residual 0.02 m; sections with levels in mODN), HRPP576, Welsh Government LiDAR tile SN6089 flown 2022-03-19 at about LAT, West of Wales SMP2 water levels, NTSLF datum table.
- Agreement: design armour foot vs trace IoU 0.79 N / 0.86 S, centroids within 4 m; lengths -4 % / +0.4 %; but drawn area 5,743 m2 is the visible rock edge (design foot 6,989, LiDAR exposed 8,675 m2). Footprint alternatives stored in canonical.alt_outlines_m.
- FIX: canonical frame was mirror-handed (+x north); now +x south, +y west (clockwise rule like the other shapes). The tracer had not used the buggy geom.py path; recomputed independently (0.005 m) and with fixed geom.py (0.014 m).
- 3D inputs (mODN; MSL +0.31 est., LAT -2.44, MHWS +2.56, MLWS -1.74): crest N arm +0.50, tail +1.00, head +0.00 rising to +0.50, oval +1.50; seabed about -4.0 (oval -3.6..-4.2); design slopes 1:3/1:4/1:5, as built 1:4-1:5; height 4.5 m (N) / 5.1-5.7 m (S). Gemini's crest -1.5 m CD, seabed -6.8 m, 200 m offshore, 200 x 65 m, Halcrow, 025 deg all wrong.
- Registry: img-17..25 added (HRPP576 Figs 2-3, five drawings, LiDAR figure, design/LiDAR overlay); rows 01-16 got for_3d_check results; EMODnet rows carry the verified MSL-LAT = 2.75 m (the -2.25 m web value is unsupported). check_registry.py passes for Borth; NEW_IMAGES_LOG lines added.
- Open: Aberystwyth chart datum/MSL/HAT not at a primary tide source (UKHO/EasyTide would close it); LiDAR datum assumed ODN; footprint level to choose for the 3D model; rows 14-17 and 20-24 pending for the 3D agent.

## 2026-10-06 - Narrowneck shape TRACED (resume run), 3D inputs prepared
- shape.json status traced, confidence MEDIUM (visible container field traced on sharp georeferenced imagery and confirmed three ways; the deeper toe is not visible, the renewal option built is unverified). Files: 07_scale\shapes\narrowneck-gold-coast\ (METHOD.md ends with "INPUTS FOR 3D", HANDOFF.md, shape.json, overlays\, scripts\).
- State drawn: the renewed reef as left in June 2018. PRIMARY = Esri Wayback 2020-08-08 (release 9812, z19, 0.2637 m/px), the sharpest post-renewal image (2019-06-18 is blurry, 2021 blurry, 2022+ dark but resolved, 2025 featureless). Both arms resolve into individual 20 m containers; 7 polygons: north arm 134 x 54 m (3,678 m2), south arm 111 x 40 m (2,269 m2), two NW shoreward patches, three channel containers (two faint). All polygons 6,239 m2, bbox 113 x 157 m, reef y = 212-369 m offshore of the 2020 waterline; shoreline bearing 356.2 deg; arms converge seaward by ~18 deg; channel gap 20.7 m.
- Checks: s4 (2022 tile set) co-registered to 0.2 m; the Garmin Navionics SonarChart shows the arms as closed 4.0 / 4.5 m shoal loops (centre assumed = reef centroid, match within ~20 m); council polygon (171 x 262 m, 34.6k m2) contains 100 % of the trace (loose envelope); arm length vs the design drawing within 10 %. geom.py (fixed 2026-10-05) used; one canonical point confirmed by hand (0.001 m).
- DESIGN PRIOR: Jackson 2012 Fig 7/6b georeferenced to Esri (same photo, Fig 7 = 1.75 x Fig 6b; scale 0.21 m/px +-10 % from Jackson 2007 Fig 13's 100 m bar = 4.275 px/m and from dark-patch matching; placement +-15 m). The 2020 trace lies inside the 2004 design envelope; ends differ by +15 m (N tip), -4 m (S tip), ~22 m at the shoreward wall: the unverified "20 m seaward" amended shape is neither confirmed nor excluded. Finding: the visible field corresponds to the design out to about the -6 m contour; the -2.5 m crest wedge covers only the shoreward ~60 m of each arm.
- INPUTS FOR 3D (METHOD.md): crest measured -2.2 m AHD (Vieira 2021 AM p.5) = -1.44 m LAT = -2.32 m MSL; target RL -2.5 m AHD (Jackson 2007 p.7); seabed -4/-5, -6 to -8, -9/-10 m AHD (Vieira Fig 3, +-1 m) and Navionics 4.0-4.5 over arms, 5.5-6 around (LAT assumed); containers 20 m x 3-4.5 m, 450 by 2006 + 84 in 2018, crest layer T2 on two T4 (Jackson 2012 Fig 9); tides z=0 at MSL: LAT -0.88, AHD -0.12, HAT +1.15 (MSQ, REPORT section 3).
- Gemini: topology (inshore/offshore lobes) and 400 x 220 m wrong; sources judged (Black & Mead unverifiable; Jackson 2012 wrong_design_version; ICM dimension_not_in_source; Swellnet correct as a depth quote).
- Registry: img-45..53 added (4 Esri Wayback tile sets, z17 shoreline context, 4 Navionics rows incl. two 9-image series); the 16 pending rows got planform results (pending false for 02, 03, 05, 08, 09, 10, 23, 26, 27, 36, 43; still pending for the 3D agent: 01, 04 (crest/datum), 14 (height), 24 (crest), 31 (seabed), 50, 51 (Navionics crest/seabed)). check_registry.py passes.
- Open: which renewal option was built (Corbett et al. 2023 not obtained, REPORT 8 request 1); identity of the three channel containers; Navionics '0.9' spot depth (older crest state?) - ask Lior to read the app label at -27.9866, 153.4341; AHD offset ambiguity 0.24 m (ICM 1.00 vs MSQ 0.76).
- Mount Maunganui VERIFIED (medium). 3D inputs corrected: bed -4.0 +- 0.5 m CD; height ~3 +- 0.5 m; present MSL = CD + 1.13 vs MVD-53 = CD + 0.9622. Removal finished 8-9 Nov 2014.
- Borth VERIFIED (high, with a footprint-definition caveat).
  - Canonical frame was mirror-handed and is flipped (+x south): any cached drawing must be rebuilt.
  - Built final layout = boot-shaped surf reef (crest +0.50 mODN) + oval shore-parallel BREAKWATER (crest +1.50 mODN); the page must label the oval as a breakwater.
  - Footprints: visible rock 5,743 / design armour foot 6,989 / LiDAR exposed 8,675 m2.
  - Tides (mODN): LAT -2.44, MLWS -1.74, MSL ~+0.31, MHWS +2.56.
  - Seabed about -4.0 mODN.
  - Royal Haskoning drawings 9V5090/1020-1023 are georeferenced.
- Started: Mount Maunganui 3D (fresh agent; reads only common + model_3d + HANDOFF).
- Next slot: Borth 3D.
- Narrowneck TRACED (medium). Renewed reef as left in June 2018.
  - Primary: Esri Wayback r9812, 2020-08-08, z19; individual 20 m containers visible.
  - 7 polygons, 6,239 m2: N arm 134 x 54 m, S arm 111 x 40 m. 212-369 m offshore. Arms converge seaward ~18 deg.
  - Navionics SonarChart 4.0/4.5 m shoal loops agree within ~20 m.
  - The 2020 field sits inside the 2004 design envelope; the "20 m seaward" renewal option is neither confirmed nor excluded.
  - Crest -2.2 m AHD = -2.32 m MSL (Vieira 2021). The crest wedge covers only the shoreward ~60 m of each arm (do not model a flat crest).
  - Next: verify_shape.
- Started: Borth 3D (design sections + design armour-foot toe; LiDAR 2022 and visible-rock trace as validation; oval labelled breakwater).
- Running: Mount Maunganui 3D, Borth 3D, 3D tab.
- Queue:
  1. Narrowneck verify -> 3D
  2. HANDOFF writer for older reefs
  3. Palm Beach 3D re-check
  4. Boscombe EMODnet integration
  5. Pratte's re-verify
  6. Trace the remaining 6
- LIOR (Borth edge): default = laser survey (LiDAR 2022, 8,675 m2); toggleable versions: design rock-layer foot (RH drawing 1020, Jan 2011, 6,989 m2) and visible rock in a photo (Esri 2024-09-17, 5,743 m2). Keep confidence HIGH.
  - Rule: measured survey > design drawing > photo for the default edge.
  - SHAPE_SPEC.md gains "Outline versions" (outline_versions, default_outline, versions_info).
  - The (i) pop-up explaining versions is required in the viewers, the Shapes tab and the 3D tab: model_3d.md, build_shapes_videos.md 1f, build_3d_tab.md 2b.
  - Borth 3D, Mount Maunganui 3D and the tab agent were told.
- LIOR: agents self-summarise and stop near limits. common.md rule 9 HANDOFF_STOP (~300k tokens / ~60 tool calls / usage warning). The 3D-tab agent is exempt.
- CORRECTION (Lior): rule 9 was a misunderstanding and is DELETED from common.md. "Limit" meant Lior's 5-hour usage limit, not agent context size. With that limit near, the Mount Maunganui 3D and Borth 3D agents were asked to checkpoint (HANDOFF + SOURCES_3D) and stop; fresh agents will continue later. The 3D-tab agent keeps going.

## 2026-10-07 - after the 3:20pm limit
- All three agents were cut off by Lior's usage limit: Mount Maunganui 3D, Borth 3D, 3D tab.
- LIOR: "only html for now; wait for my go with resuming the other agents". Mount Maunganui 3D and Borth 3D are PAUSED; their folders may lack a final HANDOFF.
- 3D tab continued by a FRESH agent from 04_build\QA\round9_3d_LOG.md + HANDOFF.md.
  - Done so far: 4 models, 93 picture tiles, tooltips, lightbox, viewer loads from file:// via a vendored three bundle.
  - Remaining: versions toggle + (i) dialog, keyboard tooltip fix, check.py, docs, QA.

## 2026-10-06 (agent system clock; follows the entry above) - 3D models tab FINISHED (fresh agent, from the checkpoint)
- Done: outline/model versions feature (toggle with names + dates, (i) dialog with versions_info + table name | date | source | footprint | volume, iframe switched by #version=<id> and postMessage {type:"m3d-version", version}, key numbers per version, automatic caveat rows for version differences). Tested ONLY with a synthetic model in a temp sandbox (`04_build\src\qa_versions_synth.py`, 26/26 PASS); the real Borth / Mount Maunganui models with versions are not built (paused until Lior says go). Nothing was created or edited in 07_scale.
- Fixed: "keyboard focus shows the tooltip" (focus() scrolled the tile into view and the scroll listener hid the tooltip).
- check.py: new [3D] block (sections vs discovered models, viewer copies, vendored three.js, no CDN/import map, gallery files, tooltip content, mandated caveat rows, evidence verified, versions contract, DOM checks in own Chrome) + page-size WARN above 15 MB + assets-path regex no longer trips on reference URLs. Result: 0 failures. qa_models3d.py: all PASS.
- Docs: README.md section "3D models tab", data\SCHEMA.md section "models3d.json", 04_build\HANDOFF.md finalised (185 lines: status, commands, module map, data flow, decisions, versions contract, checks, next steps for build_shapes_videos.md).
- Numbers: 4 models (Prattes LOW, Boscombe/Bunbury/Palm Beach MEDIUM), 93 pictures, 23 curated caveat rows, 76 merged references, page 1.7 MB (+ assets ~30 MB, 3d ~16 MB).
- Screenshots (viewed): 04_build\QA\round9_3d_{overview,gallery_tooltip,viewer_loaded,keynumbers,lightbox,caveats,methods,mobile,dark}.png and round9_3d_versions_{toggle_viewer,dialog,caveats}.png (synthetic). Log: 04_build\QA\round9_3d_LOG.md.
- Open for Lior: picture reuse rights are not cleared (private research copies); go-ahead to resume the Borth and Mount Maunganui 3D agents (then rebuild the page: the tab picks them up and shows their versions).

## 2026-10-07 (agent system clock) - 3D models tab ROUND 10 (Lior's four review requests) DONE
- Lior's requests: (1) enable exit from full screen + easy way back to the main page / other tabs from every page; (2) photos right beside the 3D model, text later; (3) less text at the top, more behind (i) or in an appendix; (4) reef selector at the top, one model at a time + "All (compare)" with all models in one scene.
- (1) Full screen = the whole stage (viewer + photo panel) through the Fullscreen API with a red "Exit full screen" button top-right (always on top), Esc, and a CSS fallback (iPhone). Sticky top bar (brand link + the five tabs) on every tab, "Top" button on long views, visible close buttons + Esc on every dialog/lightbox. The standalone viewer pages ("Own page") got a slim top bar "<- Back to the page" + the five tabs (injected into the COPY at build time, hidden when framed).
- (2)+(3) Per model: compact header (one-line confidence reason + state, full texts behind (i)) -> viewer (~60 %) next to the photo panel (~40 %; stacked on phones, photos directly under the viewer): large picture, original/annotated toggle, arrows, caption, (i) with how used + source, thumbnail strip by role; clicking a thumbnail shows it beside the model (hover/focus tooltip kept; "Enlarge" = lightbox with the full record). Key numbers, methods documents, references below; the project-wide methods / texts relied on / caveats / references are an "Appendix" at the bottom (parts open on demand, "read more" links). Page intro and tab intro are 1-2 lines with an (i) pop-over (hover / focus / click / Esc); the long site header is hidden on the 3D tab.
- (4) Selector (sticky, one button per reef with its 3D-confidence dot + "All (compare)"), hash #view/models3d/<slug|all> (Back works), default = first model, its viewer starts by itself. "All (compare)" = ONE three.js scene (3d/combined/index.html): all models at the same scale side by side along a shared shoreline, z = 0 at each site's MSL, labels with name + confidence, vertical-exaggeration slider (default 1x, always shown), water toggle, metre grid 10/50 m, 50 m + 100 m scale bars, plan / oblique / cross-shore presets, per-reef toggles + fly-to, and an Overlay mode (all reefs on one origin).
- Method of the combined scene: geometry is read from each model's own viewer at build time (src/export_combined.py: own headless Chrome, THREE.Scene hook, no viewer file changed), rotated so offshore = +z (pure rotation), written to 3d/combined/<slug>.js (2.2 MB, works from file://). Checks vs model.js, all PASS: footprint area (+0.1 % Bunbury, +4.7 % Palm Beach, +9.9 % Prattes, +20 % Boscombe; tolerance 25 %: meshes include side slopes), footprint centroid <= 0.27 m, crest level <= 0.145 m (tolerance 0.2 m), shoreline <= 0.52 m, slope direction <= 4.4 deg. Export status: 4/4 models exported (boscombe-surf-reef, bunbury-airwave, palm-beach-gold-coast, prattes-reef-el-segundo); a model without an entry in data\models3d_combined.json is listed as "not in comparison" with the reason.
- Finding: the viewers were built for >= 1100 px windows; framed next to the photo panel they squeezed the canvas, so the COPIES hide their side panels when framed (< 1100 px; originals untouched; "Own page" has the full UI).
- Checks: python src\build.py OK; python src\check.py 0 failures; python src\qa_models3d.py --prefix round10_3d 79 checks PASS; python src\qa_versions_synth.py 27/27 PASS; python src\qa_shots.py PASS (other tabs unchanged). Screenshots (viewed downscaled): 04_build\QA\round10_3d_{overview,model_with_photos,thumb_tooltip,panel_annotated,lightbox,info_popover,caveats,methods,fullscreen,all_stage,all_method,combined_oblique,combined_plan,combined_overlay,combined_overlay_side,sticky_nav,gallery_header,standalone_bar,mobile,dark}.png and round10_3d_versions_*.png. Page 1.73 MB; backup of the previous page + sources: 04_build\QA\prev\round9\. Log: 04_build\QA\round10_3d_LOG.md.
- Docs: README.md "3D models tab" rewritten, data\SCHEMA.md ("models3d.json" combined block, "models3d_combined.json"), 04_build\HANDOFF.md (185 lines), data\models3d_text\combined_method.md.
- Not built: the optional "camera hint" (button that sets a viewer to the view of a picture; needs a view field in the registry + a message contract). Nothing in 07_scale or 03_images was created or edited; nothing downloaded.
- Open for Lior: look at the tab once in his own browser (tuned in headless Chrome 1440 x 900 and 390 x 844); picture reuse rights still not cleared; go-ahead to resume Borth / Mount Maunganui 3D (then rebuild: the tab picks them up; add each a line in data\models3d_combined.json for the comparison).

## 2026-10-07 (later) - 3D tab round 2 done; agents resumed (Lior's go)
- 3D tab round 2 DONE:
  - full screen with an exit button; sticky navigation; back bar on standalone viewers;
  - photos beside the viewer; text below; Appendix;
  - reef selector + "All (compare)" combined scene + overlay mode (meshes exported from each viewer at build time).
  - Checks: build 0 failures, QA 79/79.
- LIOR asked for:
  - a "match this photo" button, but only where the camera is already documented. Plan-view traced images (shape.json pixel_polygons + georef) and logged Navionics captures qualify; oblique photos are left to the human eye. Brief written: _agent_briefs\build_3d_tab_r3.md (QUEUED until the 3D agents finish).
  - Boscombe 3D: extend the seabed to the shoreline (CCO beach profiles / 2011 survey / Navionics) and offshore with the EMODnet slope (REPORT 9.1), keeping the reef unchanged.
  - Resume the other reefs.
- Running (fresh agents from checkpoints):
  - Mount Maunganui 3D
  - Borth 3D (LiDAR default + versions)
  - Boscombe extension (also writes its HANDOFF.md)
- Queue:
  1. 3D tab round 3 (photo match + add Mount Maunganui/Borth + rebuild "All")
  2. Narrowneck verify -> 3D
  3. HANDOFF writer for Pratte's, Bunbury and Palm Beach, plus the bathymetry folders
  4. Palm Beach 3D re-check (STEP 0 + gold_coast REPORT 5.3)
  5. Pratte's re-verify
  6. Trace the remaining 6
- 2026-10-07 evening: limit reset.
  - The three agents were resumed directly by mistake; Lior: they were ~300k tokens each. They were stopped (TaskStop) and replaced by FRESH agents.
  - Each fresh agent reads only common.md, the needed brief sections and the checkpoint TO DO:
    - Mount Maunganui 3D: CHECKPOINT 3 TO DO (docs/previews/registry/HANDOFF);
    - Borth 3D: viewer fixes, Navionics, annotated, METHODS_3D, registry, HANDOFF;
    - Boscombe extension: Navionics checks, figures, STEP 0, METHODS_3D, HANDOFF.
- 2026-10-07: Mount Maunganui 3D FINISHED (fresh agent, from checkpoint 3): 07_scale\shapes\mount-maunganui-reef\3d\ (index.html viewer, model.js, docs.js, METHODS_3D.md, REQUESTS_FOR_LIOR.md, SOURCES_3D.md, annotated\, preview_*.png) + HANDOFF.md rewritten (90 lines).
  - Confidence 3D MEDIUM: plan (2013 survey -2.0 m outline 1,071 m2, default; ASR as-built toe 1,424 m2, version 2), crest -0.9 m CD and tides (LINZ Tauranga, z = 0 present MSL = CD + 1.13) are sourced; the as-built bed (-4.0 +-0.5 m CD, orchestrator decision) and so the 3 m height and flank shape are NOT.
  - Volume finding (METHODS_3D.md 4.3): at bed -4.0 the model holds 3,212 m3 (toe loft, +15 %) / 3,620 m3 (survey outline + 1:1 skirt, +29 %) vs the stated 2,800 m3; 2,800 is reproduced at bed -3.66 / -3.51 m CD (-3.91 even with vertical flanks). Every later source is shallower (2013 survey -2.4..-3.3, Navionics 2026 -2.76). DECISION for Lior: keep -4.0 or use about -3.6 (REQUESTS_FOR_LIOR.md no. 1).
  - Registry: 22 rows; annotated/mmr_model_checks.png attached to img-04; check_registry.py has no error for this reef but FAILS for other reefs (9 unregistered files: boscombe-surf-reef 3d/annotated x5, borth-coastal-defence-reef 3d/src/navionics x4).
  - Viewer fixes this run: Plan view now fits the reef into the visible canvas; hash parameter find=<heading> for the Methods panel. Page (04_build) not touched.
- Mount Maunganui 3D DONE (medium). Fresh agent, 173k tokens.
  - Versions: 2013 multibeam outline (default) and the 2008 as-built toe.
  - Bed decision for Lior: -4.0 m CD gives +15..+29 % over the stated 2,800 m3. About -3.5..-3.66 CD reproduces it, and all later evidence reads shallower.
  - Not yet in the page (round 3).
- Started: Narrowneck verify. Outline versions follow the rule survey > design > photo; Navionics SonarChart is a candidate "survey" version.
- check_registry.py flags 9 errors (Boscombe annotated, Borth navionics); the running agents were told to register those files.
- 2026-10-07: Boscombe 3D seabed extension FINISHED (fresh agent after the usage-limit stop): 07_scale\shapes\boscombe-surf-reef\ (3d\model.js, docs.js, METHODS_3D.md, SOURCES_3D.md, annotated\, preview_*.png) + HANDOFF.md (new, 121 lines).
  - Model enlarged so the shoreline is visible: seabed grid 161 x 359 cells, 2 m, x -160..160, y -66..650 m (was y 0..380). Zones: CCO beach profiles of 2010-04-20 (11 lines, OGL v3, y -66..~40 m, +-0.36 m), blend to the Fig. 9 survey, EMODnet-slope offshore rows y 380-650 m (+-1.2 m, extrapolated). Reef, survey and under-reef cells byte-identical; scene structure unchanged; 04_build not touched.
  - Checks: CCO datum test supports chart datum for the Fig. 9 zero (+0.03 m, sd 0.30, n 11; -1.37 m if ODN). Navionics z16 nearshore: chart HW / CD / CD-1 m lines at model +0.96 / -1.66 / -2.53 m MSL (expected +0.81 / -1.40 / -2.40). Navionics z16 offshore: r.m.s. 1.2 m, organised alongshore trend -1.2 m per 100 m of x (model copies a spline row at y 380); flattening that row would give 0.5 m (not applied, open issue 1 for Lior).
  - STEP 0 registry views done: img-01 is a dry sand heap, NOT an exposed reef (registry corrected; card 02_research json, media_recheck json and the page caption still carry the old wording); img-02/03 consistent with shape.json / survey crest zones; img-07 not georeferenceable. New rows img-30/31/32, Navionics z16 annotations on img-14, img-25..29 resolved; check_registry.py: no Boscombe error (it still fails for borth-coastal-defence-reef files of another agent).
  - Confidence 3D stays MEDIUM. Open: alongshore tilt decision, CDI 117452 metadata, page integration (new grid size y0 -66, ny 359).
- Boscombe extension DONE.
  - Seabed: x -160..160, y -66..650.
  - Beach from CCO profiles of 2010-04-20; offshore from the EMODnet slope.
  - Reef and survey cells unchanged.
  - CCO datum test supports ACD (+0.03 m).
  - Registry img-01 description corrected.
  - Open for Lior: flatten the offshore row alongshore (Navionics rms 1.2 -> 0.5 m)?
- Started: 3D tab round 3, with priorities:
  1. Boscombe shoreline in the page
  2. "All" label/scale fixes
  3. Mount Maunganui
  4. Photo match
  5. Borth (after its 3D agent finishes)
- Running: Borth 3D, Narrowneck verify, page round 3.
- LIOR (2026-10-07):
  - Root REQUESTS_FOR_LIOR.md written (index of all open requests: papers with citations, e-mails, browser pages, Navionics/GE readings, decisions, media review). common.md rule 9 keeps it current.
  - Mount Maunganui bed: default -3.6 m CD (ASSUMPTION), plus a "later seabed" option at -2.8 m CD (2013 survey / Navionics; crest must stay below the water line). QUEUED (small 3D re-check agent).
  - Page round-3 agent also does:
    - collapsible full-screen side panels (open by default);
    - a fast update protocol: src\update_page.py + UPDATE_PROTOCOL.md.
  - QUEUED: complete the incomplete citations P3 (Mead 2011), P5 (Rendle thesis title/year), P6 (Black & Mead 2001 title).

## 2026-10-07 - Borth 3D model FINISHED (3D agent, Sonnet 5.5, finish run)
- Viewer 07_scale\shapes\borth-coastal-defence-reef\3d\index.html: fixed header wrapping/overflow, label declutter, version selector (3 outlines with names + dates) with the (i) pop-up (versions_info + table name | date | source | footprint | volume), #version=<id> / #water / #ve / #view / #tab / #info hash parameters, the oval labelled BREAKWATER (not a surf reef), tide slider LAT -> MHWS with the reason stated (HAT not found at a primary source). Previews rendered in own headless Chrome (random port, fresh profile): preview_plan.png, preview_oblique.png, preview_methods_panel.png.
- Data: default = LiDAR 2022 edge (Lior 2026-10-06): 8,675 m2, 31,300 m3, about 53,000 t at 1.7 t/m3 (+-15 %); design_1020 6,989 m2 / 30,100 m3; sat_2024 5,743 m2 / 26,400 m3; Type 4 layer 26-37 kt, below NCE's 42,000 t for the whole Phase 1. shape.json outline_versions / default_outline "lidar_2022" / versions_info written (canonical.polygons_m unchanged); VERIFY.md line "Lior chose the LiDAR default, 2026-10-06".
- Navionics (Garmin Marine Maps web viewer, own headless Chrome, no login/CAPTCHA): datum not stated, LAT best of 7 candidates by RMS (1.15 m vs Fig 2 -4.0, 0.64 vs EMODnet, 2.30 vs the model) but the chart is 0.6-1.1 m shallower than the references offshore; the reef is NOT charted (inside a uniform drying area), so no crest/height cross-check; seabed cross-check only. Annotated A9, A10.
- NEW FINDING: the modelled sea floor seaward of the reef is 0.9 m deeper than the HRPP576 Fig 2 -4.0 contour (n 13), Navionics and EMODnet shallower still; volumes under the rock unaffected. Not changed (orchestrator's -4.0 anchor); proposed fix and decision D6 are in the root REQUESTS_FOR_LIOR.md.
- Annotated images A1-A10 in 3d\annotated\ (Fig 2 contours, drawings 1020-1023 readings, LiDAR crest check, beach vs Fig 2, seabed source zones, Navionics). METHODS_3D.md (8 sections; section 4 compares the 3 versions), REQUESTS_FOR_LIOR.md (7 rows; indexed at the project root), HANDOFF.md rewritten.
- Registry: new rows img-26..29 (Navionics series) and img-30 (seabed source map); img-14..17, 20..24 closed with result lines; check_registry.py exit 0 (Borth 30 registered, pending_3d 0).
- confidence_3d MEDIUM. Open: root REQUESTS D6 (offshore seabed fix), Navionics-app / Google Earth readings, Aberystwyth Z0 / HAT.
- LIOR supplied papers in papers\:
  - Corbett et al. 2023 (P1, Narrowneck renewal) -> sent to the Narrowneck verifier now.
  - Mead, Black & Moores 2007 (P2, Mount Maunganui; Fig 3 = design 6,500 m3 vs as-built survey 2,800 m3).
  - Mead & Borrero 2011 (P3, "MPRs - a decade of applications").
  - Rendle 2016 PhD thesis (P5, Boscombe, 343 pp).
  - Blacka et al. 2013 UNSW WRL TR 1012/08 (P8, review of artificial reefs, NSW).
  - P6 dropped (not needed); P7 not public (via the City e-mail only). Root REQUESTS_FOR_LIOR.md updated.
- QUEUE (3D first, as slots free):
  1. Mount Maunganui update: P2 Fig 3 as-built survey (possible measured default version and bed level) + Lior's bed decision (-3.6 assumption, -2.8 later option) + P3.
  2. Boscombe update from the Rendle thesis (bag layout as built, crest levels, survey datum).
  3. Papers intake (P3 + P8): per-reef facts and figures into HANDOFFs and the registry for all 13 reefs (helps the untraced ones).
  4. Then: Palm Beach re-check, Pratte's re-verify, trace the remaining 6.
- Borth 3D DONE (3D medium).
  - Versions: LiDAR 2022 default 31,336 m3; design 1020 30,091 m3; photo 2024 26,400 m3. All Type 4 tonnages are below NCE's 42 kt.
  - LiDAR crest minus design: +0.14 +- 0.28 m.
  - Navionics: the reef is not charted (drying area), so no crest check; LAT is the best datum by RMS.
  - Open: offshore seabed 0.9 m deeper than the Fig 2 -4.0 contour (D6, fix recommended); oval 38 vs 46 m.
  - Page round-3 agent was given the go-ahead for Borth.
- Started: Mount Maunganui update (P2 2007 as-built survey, P3, Lior's bed decision -3.6 assumption / -2.8 later option).
- Next slot: "seabed fixes" (Borth D6 offshore contour nodes; Boscombe D2 flatten the offshore row) -> then update_page.py.
- 2026-10-07 late: Lior's 5-hour limit near.
  - Mount Maunganui update and Narrowneck verify were told to checkpoint (SOURCES_3D.md / VERIFY.md CHECKPOINT section + HANDOFF.md) and stop with HANDOFF_STOP.
  - The page round-3 agent is the priority: checkpoint in 04_build\QA\round11_3d_LOG.md now, then continue.
- RESTART PLAN after the reset (FRESH agents only, from those checkpoints):
  1. page round 3 (if unfinished)
  2. Mount Maunganui update
  3. Narrowneck verify
  4. Seabed fixes (Borth D6, Boscombe D2)
  5. Boscombe from the Rendle thesis
  6. Papers intake (P3, P8)
  7. Palm Beach re-check
  8. Pratte's re-verify
  9. Trace the remaining 6
- Mount Maunganui update STOPPED (HANDOFF_STOP): nothing applied yet. The 2007 PDF is scanned (no text layer); OCR tool 07_scale\tools\ocr_windows.ps1 (Windows OCR). Checkpoint with a 6-step TO DO in 3d\SOURCES_3D.md; HANDOFF section 0 'PENDING UPDATE'.
- Narrowneck verify STOPPED (HANDOFF_STOP). Checks 1-3 done; VERIFY.md CHECKPOINT has a 10-step TO DO.
  - Frame and scale confirmed. The trace is a lower bound (seaward edge limited by detection; 20 faint patches beyond the north tip).
  - Corbett 2023: Option 2 was BUILT (crest -2.5 m AHD = -1.5 m LAT, crest 20 m seaward, south reef rotated 5 deg). North reef nearly complete; south reef and bridge only partly built. No post-renewal survey is in the paper.
  - Orchestrator decision: default stays the 2020 photo trace. Toggles: Corbett Option 2 design (built, partly), 2004 design (pre-renewal), 2011 survey relief (pre-renewal), Navionics (indicative).
  - First fix for the next agent: the scale discrepancy between Corbett Fig 2 (crest loops ~85-90 m) and the Jackson Fig 7 chain (60-62 m).
  - Root REQUESTS P1 still to be marked "used" by the next agent.

## 2026-10-07 (agent system clock, later) - 3D models tab ROUND 11 DONE (round 3 of the 3D tab; two agents, second one finished from the checkpoint)
- Models: 6 on the tab, 6/6 in "All (compare)": Borth coastal defence reef (3 outline versions, default LiDAR 2022: 8,675 m2 / 31,336 m3; design 30,091 m3; photo 26,400 m3; the oval is a BREAKWATER), Boscombe (seabed now extended to the beach and offshore: beach strip + shoreline show in "All"), Bunbury, Mount Maunganui (2 versions; bed level is an ASSUMPTION, every bed number is a {{token}} read from model.js), Palm Beach, Prattes. Borth data: hold entry removed, combined entry, 9 key numbers, 9 caveats (versions volumes, offshore seabed 0.89 m deeper than the Fig 2 -4.0 m contour (fix pending), oval 38 m vs 46 m, tide slider LAT..MHWS (no HAT), oval = breakwater).
- "All (compare)" fixes (Lior's screenshot): ONE shared scale bar; reef labels in screen space with collision avoidance + leader lines, inside the canvas (default / plan / overlay, also 1000 x 700); Boscombe shoreline + beach visible.
- Collapsible panels (combined layout panel, every viewer's side panel, the page's photo / reefs panel), open by default, state kept through full screen.
- "Match this photo" (src\photo_match.py -> 04_build\data\photo_match.json; receiver injected into the build copies only): 30 eligible plan-view pictures (Borth 8, Boscombe 6, Bunbury 1, Mount Maunganui 7, Palm Beach 6, Prattes 2), max trace residual 3.25 m (Borth sat2012; tolerance 2 m, 10 % of the length for reefs < 40 m, 4 m for georeferenced pictures); button in the photo panel, overlay with an opacity slider, Reset view; Navionics screenshots only where the capture log is complete (Borth, Mount Maunganui, Palm Beach, Boscombe). Excluded: oblique (Bunbury img4), uncalibrated (Bunbury img5), residual too large (Boscombe img2/img3, Palm s2, Prattes img6). Geometry test: for all 30 pictures the overlay corners coincide (<= 3 px) with the picture corners projected by the viewer's camera.
- BUG FOUND AND FIXED: the outline-versions toggle never switched the 3D model of the real viewers (they read #version= only at start; the round-10 test used a synthetic viewer). The page now re-loads the live viewer with the new version; QA reads the viewer's own selector after every switch.
- One-command refresh: python src\update_page.py [--fast|--full|--dry|--force-export] (detect changed models, backup, compile_data, build, check, summary of changed numbers) + 04_build\UPDATE_PROTOCOL.md; tested end to end including a real change. compile_data.py no longer moves the 3D picture copies to QA\removed_assets on every run (every build re-encoded all pictures, 55 s).
- 02_research\reefs\boscombe-surf-reef.json images[0] (Flickr 'cornerhouse', img-01): depicts / shows corrected to the registry row (dry sand heap behind the beach fence with the 'Surf reef' sign, no sea or reef in view; 'site context only').
- Checks: build OK (verify 119 snippets, 0 failed); check.py 0 failures; qa_models3d.py --prefix round11_3d 162/162 PASS (79 old + 83 round-11); qa_versions_synth.py 27/27. Screenshots 04_build\QA\round11_3d_*.png (41, viewed downscaled). Page 2.1 MB.
- Docs: 04_build\README.md ("3D models tab", "How to rebuild"), data\SCHEMA.md ("Round 11 additions"), HANDOFF.md (181 lines), UPDATE_PROTOCOL.md (34 lines), QA\round11_3d_LOG.md. Nothing in 07_scale or 03_images was edited; one edit in 02_research (the Boscombe card above).
- Open for Lior: pending model updates (Mount Maunganui bed + 2007 survey, Borth offshore fix, Boscombe flattening) come in with update_page.py; look at the tab once in his own browser; the 4 m tolerance for georeferenced pictures is my decision (the residual there measures the edge definition); 04_build\QA\removed_assets (39 MB of old picture copies) can be deleted.
