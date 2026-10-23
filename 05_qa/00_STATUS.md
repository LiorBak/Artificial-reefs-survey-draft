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

## 2026-10-07 (orchestrator) - project made handoff-ready (git, cloud)
- Local git repo at the project root (branch main, first commit 97a8766; 2,565 files, .git 597 MB; largest file 28 MB). Not pushed yet: waits for Lior to create a PRIVATE GitHub repo.
- New: CLAUDE.md (read-first rules for every session/agent, path mapping), _agent_briefs/orchestrator.md (orchestrator playbook, cloud/Linux notes, Lior's decisions, ordered work queue), requirements.txt, .gitignore (excludes 04_build/QA/prev and QA/removed_assets), .gitattributes (no line-ending conversion). common.md: root path maps to the repo root in the cloud.
- 04_build/src/qa_cdp.py + qa_shots.py: Chrome lookup also honours CHROME_PATH, chromium on PATH and Playwright's Chromium (Linux); still finds Windows Chrome locally.

## 2026-10-07 (orchestrator) - Lior's go: queue items 1-3 started (3 fresh Sonnet agents, PC)
- Mount Maunganui update (_agent_briefs/task_mm_update.md), Narrowneck verification stage 1 (task_narrowneck_verify.md), Borth D6 + Boscombe D2 seabed fixes (task_seabed_fixes.md; applied as recommended, reversible via 3d/archive/pre_D6, pre_D2).
- Live table of running agents + PC->cloud transfer protocol: _agent_briefs/orchestrator.md sections 7-8 (CLAUDE.md rule 10 points there). Agents never run git; the orchestrator commits.

## 2026-10-07 (seabed-fix agent) - Borth D6 DONE, Boscombe D2 NOT started (stopped on the 5-hour limit)
- Borth (07_scale/shapes/borth-coastal-defence-reef/3d): seabed fixed. Fig 2 -4.0 contour is now a node set (13 traced + 6 assumed bridge + 3 assumed east nodes); anchor -4.0 at y = 335 removed; EMODnet gradient starts on the contour. Model minus contour -4.0: -0.89 -> 0.00 m; -3.0 0.00; -2.0 -0.14 (unchanged); vs EMODnet cells 1.5-1.6 -> 0.7-1.2 m deeper; Navionics-implied zero -4.73 -> -3.75 (RMS vs LAT 2.30 -> 1.33 m).
- Bug found: the old fit clamped y to 335, ignoring the design bed nodes at y 360/385 (bed under the arm head -4.7, design -4.0). Option B (faithful fix) approved by the coordinator; volumes 31,336 / 30,091 / 26,400 -> 30,119 / 28,919 / 25,504 m3 (tonnes 53,271 / 51,154 / 44,880 -> 51,203 / 49,162 / 43,357); Type 4 layer of the default 36,646 -> 36,074 t.
- Files: model.js, docs.js, shape.json (volume_m3_model), METHODS_3D.md, SOURCES_3D.md, viewer note in index.html, annotated A1/A7-A10, previews, registry (img-17, img-30 refreshed), HANDOFF.md, root REQUESTS D6. Pre-fix copies: 3d/archive/pre_D6/. State is consistent (fully new). 04_build not touched: main must refresh the page and edit the typed texts (list in the agent's final report).
- Boscombe D2: not started; see Borth HANDOFF section 7 and the brief task_seabed_fixes.md.

## 2026-10-07 (Mount Maunganui update agent) - P2/P3 analysed, D1 NOT yet applied (stopped on the 5-hour limit)
- The "Fig. 3, design 6,500 m3 vs as-built survey 2,800 m3" is in P3 (Mead & Borrero 2011), not P2 (Mead, Black & Moores 2007; P2 has no as-built outline, bed or datum). main was told.
- P3 Fig 3 bottom (205 px, unlabelled grid ticks): fits the ASR toe outline (IoU 0.87, grid about 10 m, bag-top area 1,436 vs toe 1,424 m2) -> corroborates the toe version; not traced as a new version; default stays the 2013 multibeam outline. P2 Fig 12 top (Oct 2006, unfinished reef): bed beside the reef 2.0-3.7 m, reef parts 0.33-1.5 m below an unstated datum (CD assumed) -> shallower than -3.6 (reported only).
- Saved 16 figure files in 07_scale/shapes/mount-maunganui-reef/3d/src/ (not yet registered, ids 23-38 planned) and two check scripts in 3d/. Nothing else changed (model.js, shape.json, images.json, REQUESTS untouched; 04_build untouched).
- Continue from 3d/SOURCES_3D.md "CHECKPOINT (2026-10-07 b ...)" and HANDOFF.md section 0.

## 2026-10-10 (cloud orchestrator) - Borth page refresh done (D6 texts); page build runs in the cloud
- Borth typed texts updated for D6 (option B): models3d_caveats.json rows 32-33 (Type 4 about 36,100 t, outline spread up to 15 %; "Offshore seabed" row now resolved, 0.00 m vs the Fig 2 -4.0 contour, new ev snippet from METHODS_3D 4.4) and models3d_curated.json key numbers (Rock volume, Seabed under the rock -3.86 (-4.05 to -2.51), Seabed seaward of the reef). The D6 agent's own report was not available in the cloud; the texts were written from METHODS_3D.md 3.3 and HANDOFF section 7.
- `python src/update_page.py --full`: all checks pass, state saved; Borth is back in "All (compare)" (area 11,793 m2).
- Cloud fixes in 04_build/src (no effect on Lior's PC): Chrome gets --no-sandbox when run as root and a desktop-mouse setting on Linux (hover tooltips); the cloud Chromium path /opt/pw-browsers is found; QA ignores two cloud-only console messages (proxy-blocked remote pictures, the iframe fullscreen policy notice).
- Side effect: re-encoded image copies in 04_build/assets and 04_build/3d/*/annotated (same pictures, other bytes) and Linux paths in images_manifest.json. Harmless; a PC rebuild writes Windows paths again.

## 2026-10-10 (Narrowneck verify agent, stage 1) - Narrowneck VERIFIED (with issues); stage 2 (3D) not started
- Resumed after a usage-limit cut-off (partial work: 4 exploratory step2_*.py scripts without outputs: discarded; everything else consistent).
- Scale conflict resolved: none (Corbett Fig 2 bar: crest loops 71 m; same CAD design as Jackson Fig 2). Option 2 built (Corbett 2023); placed in the frame (13,941 m2 envelope, 96.6 % of the traced arms inside).
- shape.json: status "verified with issues", 5 outline versions (default = 2020 photo trace, 6,239 m2; Option 2 design; 2004 design; 2011 survey relief zone; Navionics 4.0 m shoals, indicative), versions_info, faint patches (24, 663 m2).
- Registry img-54..65 (Corbett 2023 figures; Fig 3 multibeam pending 3D check); 5 new overlays; check_registry: Narrowneck passes. 3D plan in 07_scale/shapes/narrowneck-gold-coast/HANDOFF.md.
- Not done: Gemini re-fetch (no network to the hosts); Navionics "0.9" reading (Lior); D7 open (recommendation: keep photo).

## 2026-10-10 (Mount Maunganui update, agent 3) - D1 applied, P2/P3 registered and used (previews re-rendered; page refresh by main still to do)
- D1 in code: default as-built bed -3.6 m CD labelled ASSUMPTION, option "later seabed" -2.8 m CD, sensitivity -3.0/-3.5/-4.0/-4.5/Navionics; model.js bed_scenarios + default_bed, seabed-scenario selector with (i) pop-up and #bed=<id> in 3d/index.html; METHODS_3D.md, docs.js, REQUESTS rebuilt (build_3d.py). Crest -0.9 / highest cell -0.8 m CD stays 0.77+ m below LAT in every bed option (nothing clipped).
- Volumes (m3): -3.6 default 2,945 (2013 outline + skirt, +5 % vs 2,800) / 2,727 (toe loft, -3 %); -2.8 later seabed 1,752 / 1,756; full table in METHODS_3D.md 4.3 and shape.json volume_table_3d.
- Papers: the 6,500 vs 2,800 m3 figure is Mead & Borrero 2011 Fig 3 (P3), not P2. Bottom picture fits the ASR toe outline (IoU 0.87), not traced, default outline unchanged; D8 (toe as default) is open. Oct 2006 bed 2.0-3.7 m (P2 Fig 12) supports the -2.8 option.
- 16 figures registered (mount-maunganui-reef-img-23..38, NEW_IMAGES_LOG.md); card gets R16/R17 with the P2/P3 facts; HANDOFF section 0 rewritten. 04_build untouched: main must refresh the page and re-type the texts that quote -4.0 (see the task's final JSON).

## 2026-10-10 (Boscombe D2 agent) - D2 applied: offshore seabed (row y = 380 and seaward) flat alongshore
- extend_seabed.py (flag OFFSHORE_FLATTEN): row 380 = its alongshore mean (-7.78 m MSL), EMODnet cross-shore gradient 0.0141 kept; zone-5 uncertainty +-1.2 -> +-0.5 m. model.js, docs.js, shape.json (identical), METHODS_3D.md (3.4 block D2, validation 12, A16, tables), SOURCES_3D.md, zone map and Navionics offshore figure re-made, 4 previews re-rendered, registry img-14/30/31/32 updated.
- Navionics offshore r.m.s. 1.20 -> 0.51 m; zone-5 alongshore trend +0.76 -> 0.00 m per 100 m of x. Reef, survey, beach, codes, datum weights, stats byte-identical (21,779 cells changed, all at y >= 380). Known: 1.13 m step between rows 378 and 380 at the x edges; soundings still show -0.44 m per 100 m of x.
- Pre-D2 copies in 07_scale/shapes/boscombe-surf-reef/3d/archive/pre_D2/. 04_build untouched: main refreshes the page and re-types the Boscombe caveat texts (see the agent's final JSON). REQUESTS D2 = applied.

## 2026-10-10 (Boscombe P5 agent, queue item 4) - Rendle 2016 thesis read; no model change
- Read only the relevant pages of P5 (PDF 60-106, 109, 121-130, 139, 145-147; printed page = PDF - 3). No as-built plan exists in P5: Fig. 5.3 is the ASR Ltd DESIGN bag layout (18 Dec 2006; footprint 4,474 m2, bags 10,450 + fill 1,750 m3, crest 0.3 m CD); text says 32 containers built; built crest about +0.5 m CD (design 0 m CD, Table 4.4); four council surveys Oct 2009 - Apr 2011 (Figs. 5.6-5.8, April 2011 plan with OS-grid axes), 2012 survey withheld.
- Comparison table (18 rows) in 07_scale/shapes/boscombe-surf-reef/P5_RENDLE2016_NOTES.md: every P5 number is inside the model's stated uncertainty (footprint +10.7 % vs trace, volume 11,900-12,200 vs loft 13,119, Oct 2009 crest tops within 0.15 m). Proposed: re-label the +0.5 m crest as BUILT (not design); datum A3 gets a third supporting argument; open question 1.66 m (Rendle) vs 1.40 m (NTSLF) CD-to-MSL.
- 8 figures registered (boscombe-surf-reef-img-33..40; 4 flagged for 3D check), logged in NEW_IMAGES_LOG.md; card gets R17 and facts (dates, cost history, failure volumes, lessons) with pages; discrepancies noted (32 / 46 / 54-55 bags; start 30 Aug 2008 vs June 2008). check_registry.py PASSED. 04_build and the 3D model untouched.

## 2026-10-10 (cloud orchestrator) - Lior: no agent cap in the cloud; drop the Map and Scale tabs
- Done today: Borth D6 page texts; Narrowneck stage 1; Boscombe D2; Mount Maunganui D1 (page refreshed, all checks pass); Boscombe P5 notes.
- Running (12 agents): Narrowneck 3D; page agent (remove Map + Scale tabs, small fixes); Palm Beach 3D re-check + HANDOFF; Pratte's re-verify + HANDOFF; Bunbury/bathymetry HANDOFFs + Boscombe wording; papers intake P3/P8; trace/verify/3D for Cables, Opunake, Kovalam, Albany, Burkitts, Mexico.
- New models are held off the page (04_build/data/models3d_hold.json) until their agents finish.
- The cloud environment's network reaches package servers only (websites, map tiles, EMODnet, Navionics blocked): reef agents work from local files and list what needs the network.

## 2026-10-10 (mexico-reef-2026-unnamed, queue item 9) - FEASIBILITY only
- No image shows the structure, no dimensions/coordinates exist (card gaps, 2 context images); raisedwaterresearch.com 403 from the container. No trace, verify or 3D made.
- Wrote 07_scale/shapes/mexico-reef-2026-unnamed/FEASIBILITY.md + HANDOFF.md (needs-network list in section 7). Registry unchanged.

## 2026-10-10 (opunake-reef agent, queue item 9) - feasibility only, no shape, no 3D
- No plan figure, no position, reef not visible on Esri 2025-01-16 z20 (viewed once); only text 90 x 20 m, 27 bags. shape.json status no_source (LOW), FEASIBILITY.md lists what is missing; old wedge schematic not used; 3 undocumented overlays archived. Esri/LINZ/nzgeo refused by proxy (needs-network list in HANDOFF.md). img-10 annotated overlay registered. 04_build untouched.

## 2026-10-10 - housekeeping run (queue item 8 + Boscombe wording)
- Written: 07_scale/shapes/bunbury-airwave/HANDOFF.md (verdict FAILED kept, developer's "2018 / not a failure" claim recorded as contradicted); 07_scale/bathymetry/emodnet/HANDOFF.md and 07_scale/bathymetry/gold_coast/HANDOFF.md. emodnet/REPORT.md exists (403 lines, sections 0-11, appears complete).
- Boscombe: 3d/METHODS_3D.md relabels the +0.5 m CD crest as the BUILT crest (Rendle 2016 p70) in A6/E10, adds P5 footprint/volume/bag-count/MSL 1.66-vs-1.40 notes to validation 2-4; provenance-row label in 3d/build_3d.py changed (no rebuild, no value change, model.js/shape.json/04_build untouched). Boscombe HANDOFF section 11 added.
- Open: rebuild/copy Boscombe docs.js into 04_build at the next page update.

## 2026-10-10 (burkitts-reef-bargara, queue item 9) - traced + self-verified (LOW), 3D feasibility only
- 07_scale/shapes/burkitts-reef-bargara/: shape.json, METHOD.md, sources.md, VERIFY.md, FEASIBILITY.md, HANDOFF.md, overlays/, scripts/. Outline = visible basalt rock platform on Esri 2025-09-05 (img-08), 31,485 m2 in frame (south edge cut by the frame), 321 x 377 m bbox, confidence LOW: the reshaped boulder zone (the real reef) is located by no source.
- 3D not built: no crest, seabed, datum, reef height (only ~2.5 m tide swing, ~300 m3 moved). Network blocked: needs-network list in HANDOFF section 7. Registry img-08/img-01 updated; no new images. 04_build untouched; slug should go on models3d_hold.json.

## 2026-10-10 (palm-beach-gold-coast, queue items 6 + 8) - 3D re-check, no geometry change; HANDOFF written
- 9 images flagged "needs 3D check" (img-03, 04, 05, 09, 12, 13, 14, 15, 16) re-checked against the model: crest (img-14/12) 0 to 0.12 m, seabed profile vs Mortensen 2015 Fig 6a RMS 0.33 m, orientation 102-109 deg vs 109.6 deg, footprint vs council polygon 0.55 m; PBO3 buoy (img-05) marginal +0.62 m on an extrapolated seabed. Table: 3d/METHODS_3D.md 4.9, 07_scale/shapes/palm-beach-gold-coast/HANDOFF.md 3.5.
- No change to model geometry or volumes (22,020 m3, crest height 3.89 m). Rebuilt with build_3d.py: new provenance rows (crest pages, PBO3, Mortensen profile, AHD-MSL 0.12 m now verified), sources c1/d1/t2, validation key recheck_2026_10_10. Pre-change files in 3d/archive/pre_recheck_2026-10-10/. 3d/REQUESTS C2 closed.
- Registry: 9 rows set pending=false with result; NEW_IMAGES_LOG lines marked CHECKED; new annotated figure 3d/annotated/recheck_orientation_img04_img15.png. Written: 07_scale/shapes/palm-beach-gold-coast/HANDOFF.md.
- Open for main: update 04_build/data/models3d_curated.json + models3d_caveats.json Palm Beach rows (texts in the agent's summary), copy docs.js/model.js at the next page update. Viewer not re-rendered (Chrome script is Windows-only, CDN blocked). No decision for Lior.

## 2026-10-10 (Pratte's Reef, queue items 7 + 8) - re-verified, HANDOFF written
- Re-verified the `pending_reverification` items of prattes-reef-el-segundo against the supplied Borrero & Nelsen (2003) PDF: pp.1-3, 14, 16 quotes confirmed; Fig. 4 is the same drawing as img1 (and img5 is the same raster as Fig. 4); the "30" cross-shore statement agrees (Fig. 20 re-measured 29.0 x 58.5 m vs outline 28.6 x 58.0 m). Polygons, canonical frame, design version and confidence (medium) unchanged; block removed, `reverified_on` 2026-10-10.
- New finding: the paper's text (reef 200 m from the outfall, within 500 m of both structures) disagrees with its Fig. 2 (about 340 m / 670 m); position hint may be +-150 m. Crest datum ambiguity (drawing MSL vs paper MLLW, 0.849 m) and volume gap (443 vs 695-782 m3) stay open as judgement calls.
- 3D model rebuilt (stamps only; volumes 443 / 550 m3 identical). Registry: -img-37, -img-38 added (Fig. 4 + outline, Fig. 20 + scale check). VERIFY.md, METHOD.md, sources.md, 3d/METHODS_3D.template.md (note in 3.10) updated; HANDOFF.md written; root REQUESTS E1 extended. Archive: 07_scale/shapes/prattes-reef-el-segundo/archive/pre_reverify_2026-10-10/. Main still has to update models3d_caveats.json (position row) and models3d_curated.json (footprint row), optional text only.

## 2026-10-10 (papers intake P3 + P8, queue item 5) - per-reef facts extracted, 25 figures registered
- Read P3 (Mead & Borrero 2011, 6 pp) in full and P8 (Blacka et al. 2013, 131 pp: Tables 4.1-4.4, Section 4, Appendix A.1-A.4, A.11, figure list; text layers fine, no OCR). Notes: 05_qa/papers_intake/P3_mead_borrero_2011.md and P8_blacka_2013.md (per-reef facts with page/figure, card status HAS/LACKS/CONTRADICTS, ready-to-apply "card additions per slug"). Reef cards NOT edited.
- Covered: cables, narrowneck, prattes, mount-maunganui, opunake, boscombe, kovalam (both papers); borth (P8 tables only, P3 reference only). Nothing in either paper for palm-beach-gold-coast, southern-ocean-surf-reef-albany, burkitts-reef-bargara, bunbury-airwave, mexico-reef-2026-unnamed.
- Main contradictions with cards: Narrowneck crest lowered 0.5 m (-1.0 to -1.5 m AHD, P8) vs card "1 m"; Narrowneck 20-50 m salient called a misreading of an arbitrary reference line (P8); Boscombe 7 of 11 criteria met (P3) vs card 4 of 11; Kovalam volume 4,000 m3 (P3, P8 cost-rate) vs card 4,800; Mount Maunganui design volume 6,500 m3 (P3); Cables built 1998 (P3) vs 1999 and volume 5,500 m3 (P8); Prattes Phase 2 dated 2000 (P8) vs card spring 2001; Borth offshore distance 110-140 m (P8) vs card 300-400 m; Opunake footprint 30 x 100 m (P8) vs card 90 x 20 m.
- Images: 25 registered (boscombe 41-43, narrowneck 66-74, cables 24-26, prattes 33-36, mount-maunganui 39-41, borth 31, kovalam 15-16) in 03_images/reefs/<slug>/ + IMAGES.md + NEW_IMAGES_LOG.md; "needs 3D check": narrowneck-img-69 (crest depth), cables-img-26, prattes-img-35, borth-img-31, kovalam-img-16. P3 Mount Maunganui Figs 3-4 were already img-23..25 (skipped).
- REQUESTS_FOR_LIOR.md P3 and P8 rows updated (P8 report number is 2012/08, not 1012/08). Main still has to apply the card additions from both notes files.

## 2026-10-10 (narrowneck-gold-coast, stage 2) - 3D model built (confidence MEDIUM); main must add it to the page
- 07_scale/shapes/narrowneck-gold-coast/3d/: model.js, docs.js, index.html, METHODS_3D.md, SOURCES_3D.md, annotated/A1-A6, previews, MAIN_TYPED_TEXTS.json. Default = photo 2020-08-08 (D7 still open); four more outlines selectable (Option 2 2017, 2004 design, 2011 survey zone, Navionics shoals outline only).
- Seabed and container relief from Corbett 2023 Fig 3 (pre-works multibeam, digitised by hue; +-0.4 m, placed +-10 m, AHD assumed); crest -2.2 m AHD measured; datum default MSQ (AHD = LAT + 0.760), the papers' LAT + 1.00 as a viewer switch (0.24 m). Mound envelope volumes: photo 13.5k, Option 2 21.3k, 2004 13.6k, 2011 zone 6.9k m3 = 17-27 % of the 78.5k m3 of sand placed (534 containers). Stage-1 toe height estimate (4-6 m) not supported: multibeam relief 1-1.5 m at the toe.
- Registry: pending rows closed (img-01, 04, 14, 24, 31, 50, 51, 55, 69); new img-75..78. REQUESTS: Navionics 0.9 + nearshore points + City datum offset / as-built (root file row updated). Not run: update_page.py (main's job).

## 2026-10-10 - P3 (Mead & Borrero 2011) and P8 (Blacka 2013) applied to 5 cards
Slugs: borth-coastal-defence-reef, boscombe-surf-reef, mount-maunganui-reef, opunake-reef, prattes-reef-el-segundo (cards .json + .md). New refs: Borth R14 (P8) + R15 (Borrero & Mead 2010, not seen); Boscombe R18 (P3) + R19 (P8); Mount Maunganui R18 (P8; P3 already R17); Opunake R13 (P3) + R14 (P8); Prattes R18 (P3) + R19 (P8). Disagreements kept side by side with "SOURCES DISAGREE" notes (MM volume 5,000/6,000/6,500; Boscombe 4 vs 7 of 11, P3 authors designed the reef; Borth offshore 300-400 vs 110-140 m; Opunake 90x20 vs 30x100 m; Prattes phase 2 2000 vs 2001, build/removal totals, bag size). Gaps only partly filled (Borth footprint/crest; MM crest) or left open (Prattes crest/bag weight). Not touched: narrowneck, cables, kovalam. JSON parse OK; no card-only check exists (check.py runs on the built page); update_page.py not run. md: fields whose text did not match are in an "Additions 2026-10-10" section before References; new refs appended at the end of each md.

## 2026-10-10 (southern-ocean-surf-reef-albany, item 9) - shape traced + verified (HIGH), 3D NOT built (feasibility only)
- 07_scale/shapes/southern-ocean-surf-reef-albany/: shape.json (2 outline versions: default Bluecoast final-design outline 13,104 m2; toggle visible reef on Esri 2026-01-20, 10,918 m2), METHOD/sources/VERIFY, overlays/ (5), scripts/, HANDOFF.md, FEASIBILITY.md.
- Findings: reef is a wedge whose crest runs ~280 deg true (about 13 deg off the shore normal); length along crest 157 m (sat) / 165 m (design) vs text 165 m; width 117/121 vs "up to 110"; 71 m from the dry-sand edge (about 150 m from the vegetation edge) vs text "140 m from landward toe" (reference undefined). Before/after Esri (2025-01-16 vs 2026-01-20) confirms the dark patch is the new reef. Design-figure arrows (110/140 m) are not to the bar's scale.
- Registry: img-10 volume corrected 54,000 -> 34,000 m3 (table reads 34,000); img-03/05/10/11/12/13 results written, annotated overlays added. No new image rows.
- 3D blocked: no seabed depth / pile height / slope in local sources; network blocked (City report, Navionics, AusSeabed). Crest -1.0 m AHD and tides (MLLW -0.26, MHHW +0.34 m AHD) are sourced. Lior reading table in FEASIBILITY.md. Slug belongs in 04_build/data/models3d_hold.json. update_page.py not run.

## 2026-10-10 - narrowneck-gold-coast card: P3 + P8 facts applied
- 02_research/reefs/narrowneck-gold-coast.json/.md: added R22 (Mead & Borrero 2011), R23 (Blacka et al. 2013), R24 (internal 3D stage-2 report); fields extended (motivation, design_as_planned, size, as_built_vs_design, outcome, why_worked_or_failed, cost, year, 2 gaps); md "Additions 2026-10-10" section before References.
- Disagreements recorded (both values kept): crest lowering 1 m vs 0.5 m (-1.0 to -1.5 m AHD, P8 p.94), measured crest -2.2 m AHD (3D); footprint 170 x 280 m vs 350 x 600 / 450 x 250 m; salient 20-50 m / 30-50 m vs P8 p.98 reference-line misreading; 70,000 vs 78,500 m3 placed (17-27 % exposed).
- JSON validated. Notes files P3/P8 marked narrowneck applied.

## 2026-10-10 - PAGE agent: Map and Scale tabs removed (Lior's decision)
- Top nav now Gallery, Table, 3D models; #view/map and #view/scale fall back to the gallery; viewer top bars (incl. combined) list the three tabs; meta description updated; Leaflet/map tiles and scale.js no longer loaded.
- Rule 1 kept: reef dialog section "Footprint & how we drew it" (derivation, images relied on, verification, provenance md) stays for all 13 reefs via slim src/footprint.js; 3D tab keeps outline versions and methods. Lost only the 2D all-reefs overlay/comparison.
- Archived (restorable): archive/04_build_removed_2026-10-10/ (scale.js + pre-change src files + old page); restore steps in 04_build/HANDOFF.md section 0.
- Checks: Map/Scale checks in check.py, qa_models3d.py, qa_shots.py replaced by retired-route and no-leftover checks; update_page.py --full: all pass, state saved.
- Fixes: Palm Beach labels in match view (pm_receiver.js), compact version block (Borth viewer higher at 900 px), photo_match.py skips held models (it had silently dropped all Match-photo buttons because of Narrowneck).

## 2026-10-10 - kovalam-reef-india, queue item 9 (shape; 3D withheld)
- Traced the container strips on the ASR aerial (img-07 = WRL Fig 4.5), rectified through a camera fitted to the 2011-02-28 Esri swash line. Result LOW confidence: area 1,216 m2, 59 x 41 m at an assumed camera height of 60 m; the photo cannot fix the scale (546-1,681 m2 for 30-80 m), so 3 versions (35/60/80 m) in shape.json. Status verified (self-check), VERIFY.md, METHOD.md, sources.md, HANDOFF.md in 07_scale/shapes/kovalam-reef-india/.
- 3D not built: FEASIBILITY.md (crest/depth from WRL Table 4.2 are unlocated ranges without datum; no seabed profile; tides only a ~1 m range). Main: add slug to models3d_hold.json.
- Images: registry rows img-07/-08/-09/-16 updated, planform pendings closed; check_registry passes for kovalam. Needs network list in HANDOFF section 7 (Esri Wayback z19 2010-14, Navionics, surfer.com/surfingindia pages).

## 2026-10-10 - Airwave founder interview added to Bunbury and Albany cards
- New personal-communication source (Lior's Zoom interview with Troy, Airwave founder, 8 Oct 2026; notes as reported by Lior). Bunbury card: R25, fill = sand not air in final design, seam opened a couple of days after installation, "perfect waves" before that (founder claim), future = concrete; `sources_disagree` (4 items) and `interview_2026_10_10` added; verdict label unchanged (failed), verdict_reason made fairer. Albany card: R19 plus a review (waves look bad from outside; not surfed; developer of a different reef). .md in step ("Additions 2026-10-10" sections); both JSON parse. HANDOFF section 8 appended for bunbury-airwave. 04_build not touched and the page not rebuilt (new keys `sources_disagree`, `interview_2026_10_10` are not yet used by the pipeline).

## 2026-10-10 - opunake-reef, item 9b (local papers + Gemini extracts + web search)
- papers/ text-layer grep: Opunake only in text/tables (Mead & Borrero 2011; Rendle 2016 Table 2.1 + refs; Blacka 2013 Tables 4.1-4.4). No plan figure, coordinates or datum. Gemini extracts: nothing confirmable. 9 WebSearches: text only (90 x 20 m, 27 bags). Log in 07_scale/shapes/opunake-reef/sources.md.
- Result: still no plan source. shape.json stays no_source; FEASIBILITY.md updated with what is needed (TRC 2009 Tech. Report 2009-33, Black et al. 2004, design report, NZ Geographic figure, dated imagery).
- 07_scale/reefs/opunake-reef.footprint.json now carries DO_NOT_DISPLAY / display:false (file kept). 04_build/src/compile_data.py load_footprint still reads it and does not honour the flag: main please check the page does not show the wedge, and add opunake-reef to models3d_hold.json.
- Card: R15 added (Rendle 2016 Table 2.1: 4,800 m3, A$760,000), TRC report lead. No new images.

## 2026-10-10 - REQUESTS_FOR_LIOR.md rewritten into one to-do file
- Old file archived: archive/REQUESTS_FOR_LIOR_before_2026-10-10.md. New layout: Do next; 1 Papers (full citations); 2 E-mails with contact + draft (E1-E13); 3 Web searches (W1-W11); 4 Google Earth captures (G1-G11, precise links); 5 Later app readings (links per point); 6 Decisions open (D3, D4, D5, D8, D9); 7 Decided/done.
- Lior's answers applied: D7 agreed (keep photo trace); Pratte's J1 decided (MLLW); J2 closed as decided by us (+-150 m; noted in prattes HANDOFF section 5 for the model agent).
- Papers: already in papers/ = P1, P2, P3, P5, P8 (asking agents should be told); missing = P4, P7, P9-P16 (P10 and P16 have free online copies).
- Contacts confirmed by web search: City of Gold Coast beaches@, City of Albany staff@ (general), BCP Council (Matt Hosey), CCO cco@channelcoast.org, City of Bunbury info@, WA DoT cdc@, TRC consents@, STDC phone/form, Bundaberg council general. Not confirmed: DETSI, Bluecoast, Borrero/Nelsen, Coastal Frontiers, Waveco, RWR, ASR/CESS.

## 2026-10-10 - kovalam-reef-india card: P3/P8 facts applied
Added R13 (Mead & Borrero 2011) and R14 (Blacka et al. 2013) to the .json and .md. Size: P8 Table 4.2 geometry (65 x 85 m, 1.3-3.7 m, 90 m offshore, submergence 0.2-3.4 m, datum not stated), tide/wave climate (Table 4.3). Outcome: beach 10-15 m / up to 30 m wider (P3 p.5 Fig. 7), why surfing worked, P8 p.70 verdict, CESS assessment pending, 2013 damage note. Volume sources disagree and are kept side by side: 4,000 m3 (P3), ~4,017 m3 implied (P8 cost rate), 4,800 m3 (R1/R10); the shape HANDOFF also uses 4,000. JSON validated; md kept CRLF.

## 2026-10-10 - cables-reef-wa trace + verify (partial) + 3D DONE (queue item 9, fresh agent)
- Trace: primary = Blacka et al. 2013 Fig A.2 (Lyons 1992 design plan, registry img-26, legible labels); scale from four printed dimensions 6.51 px/m (+-3%). Default outline = design plan + drawn southern extension 4,355 m2 (121 x 89 m); original plan 4,049 m2 (121 x 76 m); Fig 7 V and Pitt concept as extra versions. Shape confidence MEDIUM. shape.json status traced; VERIFY.md partial (no network: no satellite / aerial / bathymetry).
- cables-reef-wa 3D DONE (07_scale/shapes/cables-reef-wa/3d/): design ramp RL -1.0 crest to -3.0 set-out from the printed contours, bed plane 1:30 fitted to the stated 5,500 m3, datum reading A/B switch (RL datum unstated, 0.78 m). 3D confidence LOW. Previews rendered with own headless Chrome and vendored three.js.
- Registry: 8 rows got results / annotated files, 5 own figures added (img-27..31), NEW_IMAGES_LOG updated. HANDOFF has the needs-network list. Main: remove cables-reef-wa from 04_build/data/models3d_hold.json, add the combined / curated / caveat entries, run update_page.py.

## 2026-10-10 - cables-reef-wa card: papers P3 + P8 applied (fresh agent)
- 02_research/reefs/cables-reef-wa.json + .md: added R17 (Mead & Borrero 2011) and R18 (Blacka et al. 2013). Facts: 1998 build year (P3), 5,000 m3 limestone, 50 m right-hand breaker aim, surfable days 5-7 to 142/yr, Rottnest shelter, negative public reaction; P8 geometry 140 x 70 m / 275 m offshore / 3-6 m, crest 1.0-2.5 m below MSL, 5,500 m3 granite 1.5 t / 3.0 t, design chain (UWA/DMH WA, Ranasinghe 2001, Lyons 1992 Fig A.2), cost A$1.51-1.8 M nominal / A$2.5 M 2013 / A$457 per m3, tide range 0.8 m, wave climate, performance caveats, verdict "partially". .md has an "Additions 2026-10-10" section before References.
- Contradictions kept with both values and a "sources disagree" note: year 1999 vs 1998; volume 3,500 / 5,000 / 5,500 m3; crest 1-3 m vs 1.0-2.5 m; granite vs limestone; RL datum 0.78 m noted. Also added to the card gaps list. JSON validated (parses, CRLF kept). Both intake notes marked cables applied.

## 2026-10-10 - palm-beach-gold-coast source audit (fresh agent)
- 07_scale/shapes/palm-beach-gold-coast/SOURCE_AUDIT_2026-10-10.md written. METHODS_3D.md: per-source "how used" table (2.2), assumptions A12-A14, decisions DEC1-DEC15 (3.9), tools/AI statement (3.10), references c1, d1, t2 added; docs.js regenerated (model.js byte-identical; no value changed). IMAGES.md stale pending-3D lines fixed (registry otherwise complete).
- Unconfirmed: Prenzler 2022 DOI/pages (REQUESTS). Mismatches listed for main: card volume 25,000 vs model 22,000 vs register 33,000; card offshore 270/330 m vs model 225-374 m.

## 2026-10-10 - Pratte's Reef source audit (agent)
Audit in 07_scale/shapes/prattes-reef-el-segundo/SOURCE_AUDIT_2026-10-10.md. Applied J1 (MLLW kept, decision D6) and J2 (+-150 m position uncertainty, text only; model unchanged). METHODS_3D gained source "how used" table, decisions D1-D10, per-element confidence; viewer got sub-tabs. Open: S10 venue/year unconfirmed; card V size 64 m vs our 58.0 m (not edited).

## 2026-10-10 - bunbury-airwave source audit (fresh agent)
- SOURCE_AUDIT_2026-10-10.md in 07_scale/shapes/bunbury-airwave/: 29 rows, 22 ok, 6 fixed, 1 mismatch (card lat/lon ~2 km off, card read-only). Registry (21 ids) checked: files present, sha256 match, no empty fields.
- 3d/METHODS_3D template + docs.js: added 2.2 fill disagreement (ABC "air", Tracks sand+air, Troy interview R25 "sand instead of air"; unresolved, no value changed), 2.3 how each source was used, A14, DEC1-DEC12, L12, Bakalo (2026) reference, S_Troy in viewer sources. Rebuilt for docs only; model.js changed in text fields only (checked as JSON diff).
- Page text proposals for main (not applied): models3d_curated.json bunbury-airwave/state_short, see audit section 6. Request E5b added.

## 2026-10-10 - Boscombe source audit (agent)
Result: `07_scale/shapes/boscombe-surf-reef/SOURCE_AUDIT_2026-10-10.md`. METHODS_3D.md: stale zone-5 uncertainty (1.2 -> 0.5 m since D2) fixed; Rendle 2016 added as S15 (validation only) and S14 row added; Mead / Rendle-Davidson citation forms completed (DOIs not confirmed); new section 9 (source use by element, assumption register with sensitivities, decision register BD1-BD12, confidence per element, methods/AI statement). build_3d.py gets source S15; model.js/docs.js rebuilt (text only; reef, stats, levels identical; seabed = D2 state). Page text edits and card mismatches listed for main in the audit file section 3. No model value changed.

## 2026-10-10 - cables-reef-wa source audit
SOURCE_AUDIT_2026-10-10.md written; METHODS_3D/SOURCES_3D extended (assumptions A1-A11, decisions X1-X8, how-used table), docs.js rebuilt, PAGE_TEXTS_FOR_MAIN.json texts sourced. No model values changed. Open: citations for Bancroft 1999, Pattiaratchi 2003, Ranasinghe 2001, Lyons 1992 (REQUESTS_FOR_LIOR.md).

## 2026-10-10 - borth-coastal-defence-reef source audit (fresh agent)
- 07_scale/shapes/borth-coastal-defence-reef/SOURCE_AUDIT_2026-10-10.md: 34 statements, 19 ok, 10 fixed, 2 open, 3 mismatches explained (2 are card wording about the superseded two-reef design). No model value changed; 3d/model.js byte-identical after rebuild.
- New 3d/REGISTER_3D.md (sources with how-used, methods, assumptions A1-A14, decisions DEC1-DEC14, confidence) built into docs.js and shown in the viewer Methods tab; METHODS_3D.md pointer + Blacka reference; shape.json ref6 "Hansford, Mark"; registry img-24 note (LiDAR mask). Registry has 31 rows (HANDOFF said 30). Viewer logic tested with node only (no Chrome).
- Page text edits for main: none needed. Card (not edited): `size` quotes Blacka's superseded-design dimensions.

## 2026-10-10 - mount-maunganui-reef source audit (fresh agent)
- SOURCE_AUDIT_2026-10-10.md in 07_scale/shapes/mount-maunganui-reef/. METHODS_3D template: sources table with how used, assumptions A1-A14 (why/effect/replacement), decisions M1-M15, scripts/AI note, confidence per element; stale summary text (-4.0, 3 m) fixed. BoPRC citation corrected (Dahm & Gibberd, Focus Report 131, Dec 2013) in methods, model.js sources and registry; NIWA authors Bell & Lewis; 2,800 m3 shown as one origin (Mead 2011). Viewer: tabs Sources & how used / Assumptions / Decisions (render checked, no page errors). model.js: only 4 citation strings changed. Registry header 41 images. For main: page-text edits listed in the audit file section B.

## 2026-10-10 - Narrowneck source audit (fresh agent, documentation only)
- 07_scale/shapes/narrowneck-gold-coast/SOURCE_AUDIT_2026-10-10.md: 47 statements traced (29 ok, 13 fixed, 2 missing = Black & Mead 2001 and Jackson 2012 DOI/2007 journal pages not confirmed, 3 mismatches in the reef card only, not edited). No model value changed; model.js differs from the previous build only in versions_info and confidence_3d.reason text.
- D7 recorded (Lior, 2026-10-10: default = 2020 photo trace) in METHODS_3D 3.8, shape.json, HANDOFF, VERIFY, registry img-45. METHODS_3D gained 2b (how each source was used), A1-A16 assumptions with effects, 3.7 methods/AI, 3.8 decisions, per-element confidence; viewer has chips Sources: how used / Assumptions / Decisions (smoke test passed).
- Fixed: vds21 survey date 18 -> 19 Jul 2018 in the model text; stale HANDOFF counts. REQUESTS_FOR_LIOR.md appended (citations not confirmed).

## 2026-10-10 - source audit (agent: Albany, Burkitts, Kovalam, Opunake, Mexico shapes)
SOURCE_AUDIT_2026-10-10.md written in each of the 5 folders. Added to FEASIBILITY.md (all 5) and shape.json (4; Mexico has none by design): why hidden / what was checked with sources / assumptions A# / decisions D# / page_status. Citations completed: Blacka, Shand, Carley, Mariani 2013 (WRL TR 2012/08, DOI 10.4225/53/58e1dc7368c7a); Mead and Borrero 2011 authors; Rendle 2016 PhD (Plymouth), Table 2.1 corroborates Burkitts (300 m3, AUS$10,000) and gives a 4th Kovalam volume (4,300 m3). Fixed: Rendle year (2012/2013 -> 2016), WRL authors in Kovalam sources.md, Albany R18 citation, build dates wording. Open for main: Albany shape.json canonical = sat2026 while default_outline = design_bluecoast; card Burkitts lat sign (+24.8205) and dive-site identity vs registry; Kovalam H35 bbox 43x24 vs sweep 38x29. No model values changed.

## 2026-10-10 - source audit of 7 reef cards, group A (fresh agent)
- Cards: borth-coastal-defence-reef, boscombe-surf-reef, bunbury-airwave, mount-maunganui-reef, palm-beach-gold-coast, prattes-reef-el-segundo, narrowneck-gold-coast (.json + .md in step). Table: 05_qa/source_audit/cards_group_A_2026-10-10.md.
- Added: verdict_reason (who decided / why) on all 7; LOCATION notes and tertiary / not-citable labels on references; model facts with sources (crest, tides, traced outlines); lat/lon filled or corrected on Bunbury, Mount Maunganui, Palm Beach, Narrowneck (from the traced shapes). Prattes lat/lon kept (model has no fix; 600 m from the hint). Borth USD conversion corrected. Mount Maunganui design-paper citation corrected (Mead & Black 1999). Prattes Phase 2 date resolved to April 2001 from Borrero & Nelsen 2003 p.3.
- Open: web-page authors/dates ("n.d." pages), Prenzler 2022 DOI/pages, Jackson 2007 pages, FX rates (see REQUESTS_FOR_LIOR.md, appended).

## 2026-10-10 - citations audit of all 13 reef cards (fresh agent)
Report: 05_qa/source_audit/cards_citations_2026-10-10.md. Scan of every narrative sentence without [R#]: 174 flagged, about 90 tagged, 11 marked DERIVED with the internal document, about 45 labelled (negative finding / inference / unsourced), none removed except 31 Opunake [R4] tags (R4 marked NOT READ) and the Burkitts dive-site claim (qualified: rejected video is another place). New refs: Cables R21, Borth R21, Burkitts R18.
- Corrected: lat/lon on Boscombe, Borth, Kovalam, Albany, Burkitts, Prattes (hint +-150 m), Cables (weak listing, unconfirmed); Opunake unverified; Kovalam cost_usd_approx 1,100,000 -> 1,580,000 (Rs 75 M / 47.44, FY2009-10 average, secondary source); Albany 6-8 s attribution (forecast site; buoy 5.7-6.2 s) and tonnage 62,800 t vs ~70,000 t; Mexico "unveiled 16 April 2026" reworded (also shapes/mexico HANDOFF); Mead et al. 2007 = 18th ACOEC (card right; mount-maunganui shape.json fixed); Borth Blacka dimensions marked superseded design; Bunbury stale coordinates text.
- Open: see report section "Items left unsourced or unconfirmed". Page build not run (04_build untouched): refresh needed to show the new lat/lon, Kovalam cost and wording.

## 2026-10-10 - kovalam-reef-india network pass (fresh agent)
Fetched Esri Wayback (197 releases; z19 blank before 2022, z17 shows no strips 2011-2020), surfingindia/Vimeo/RWR pages, searched for ASR 2010a and CESS reports: no vertical or scaled image, no design plan. Wayback web and ASR site unreachable from the sandbox, surfer.com 403, Navionics needs a browser (none here). Registered 4 images (img-17 to -20). Shape stays hidden, LOW, no 3D. Files: 07_scale/shapes/kovalam-reef-india/METHOD.md s.6, FEASIBILITY.md, HANDOFF.md s.10.

## 2026-10-10 - opunake-reef network pass (fresh agent)
Network works for curl (not WebFetch DNS). Fetched LINZ open aerials 2011-12 (0.4 m) and 2021-22 (0.25 m) from the public AWS bucket (crops only; tiles are 73/208 MB), Esri Wayback (197 releases, 4 distinct versions 2015-2024), RWR Opunake page text. Reef NOT visible in any image: no plan source; shape stays no_source and hidden. Blocked by bot checks (not bypassed): NZ Geographic, trc.govt.nz; TRC 2009-33 and Black et al. 2004 not found openly. 6 images registered (opunake-reef-img-11..16), card got R16/R17 + md section, FEASIBILITY/HANDOFF/sources/METHOD updated. No bathymetry for Opunake in open LINZ buckets; LINZ chart layers need login.

## 2026-10-10 - 04_build page agent: hidden shapes, Google Maps links, interview cards (Lior's decisions of the day)
- Outline drawn only from a real plan source (shape.json traced/verified). Hidden (no polygon in page data, text "Shape not drawn ... see FEASIBILITY" + reason + text-only size + FEASIBILITY.md link): Mexico, Opunake, Burkitts, Kovalam. Data-driven: footprint.json display:false / DO_NOT_DISPLAY (flags added to Burkitts, Kovalam, Mexico; Opunake honoured), no shape.json, or shape.json status not traced/verified.
- Finding: the dialog drew the old text-derived footprint.json polygons (e.g. Narrowneck 114,950 m2 envelope vs 6,239 m2 traced). All shown outlines now come from shape.json canonical (9 reefs, Albany high); "Outline source" block added; old derivation table relabelled "earlier text-based estimate".
- Location link per reef (dialog, gallery tile, new table column): shape.json geo > shape location_note > card lat/lon; approximate flagged; Mexico "not published". Card lat/lon problems for card owners: Burkitts lat sign (+24.82), Albany 0.9 km, Kovalam 1.5 km off.
- Cards: "Sources disagree" accordion (Bunbury), personal-communication reviews linked to their reference, "personal communication, unpublished - no URL" wording. Hold reasons -> "Not yet modelled" for 5 reefs (Cables unchanged).
- check.py: hidden set, no outline leak, Maps URL format, DOM of all 13 dialogs + table. Two stale 3D snippets (Prattes position +-150 m, Mount Maunganui bag text) re-synced to the changed 3D docs; qa_models3d tolerates ERR_BLOCKED_BY_ORB for remote hotlinks (cloud proxy). update_page --full: state saved. Details: 04_build/HANDOFF.md section 0b.

## 2026-10-10 - cables-reef-wa imagery + bathymetry pass (fresh agent, network open)
Found: the reef is at 32.0156 S 115.7485 E (the brief's box 32.01-31.99 S missed it by 1 km). DoT WA open bathymetry (CC BY 4.0: FR.zip point surveys 1995/1998/1999-11/2002-02 in AHD, Perth_5m composite) and Esri Wayback z19 tiles fetched. The traced original design plan, moved and rotated only (theta 9.7 deg ccw), contains 91 % of the Nov 1999 rock soundings (free scale 0.979) and coincides with the dark rock patch on 5 Esri images: shape.json now verified, plan confidence high. The drawn south-arm extension is NOT confirmed (2002 soundings +0.43 m, n 23; image shows no contrast). Model rebuilt (first-run files archived in 3d/archive/pre_imagery_2026-10-10/): measured 1998 seabed replaces the plane fitted to 5,500 m3; default = Nov 1999 surveyed surface (4,671 m3; Feb 2002 5,219 m3); design surface on the measured bed 3,920 / 4,249 m3; datum: survey-implied RL-AHD 0.5-0.6 m (A 0.78, B 0): A kept. Also: shoreline 7.8 deg T, 254-263 m offshore, Fremantle MSL 0.773 m above LWD (BoM). Registry img-32..40; METHODS_3D A1-A17, X1-X13; source audit Addendum 1; PAGE_TEXTS_FOR_MAIN.json revised (old_to_new). Dead ends logged (02_research/dead_ends/cables-reef-wa.json, 11 entries): papers (403), Transport WA tide pages, RWR originals identical. Open: Fremantle CD-AHD offset, papers, post-2002 survey. Main: update page data (default version changed) and the card (275 m, 5,500 m3, coordinates).

## 2026-10-10 - Burkitts Reef (Bargara) + Mexico/Xala network pass (fresh agent, network open)
Burkitts: the reshaped zone is now LOCATED, low confidence, in the only form a source gives it: Redgard's Phase 3 work zones, marked on an oblique aerial in Jackson and Corbett (2007) Fig. 1 (same photo on the RWR page). Georeferenced with 3 ground control points onto Esri Wayback imagery of 2016-07-31: the "remove to lengthen break" ellipse is about 1,750 m2 (43 x 52 m) on the inner rock flat just seaward of the rock pool, +-20-30 m; three more marks are arrows (surface rocks at the pool, shore break at the NE platform edge, dangerous rocks on the east flank edge). This is the later designed Phase 3 plan, NOT the Feb 1997 first works (still unlocated). shape.json: reef_zone (displayable low, only as a labelled secondary layer; footprint.json display left false for main/Lior), outline version phase3_work_zone_ellipse_esri2016, assumptions A9-A13, decisions D6-D8, references R19-R22. Also: MSQ 2026 tidal planes for Burnett Heads retrieved (MHWS 2.94, MHWN 2.35, MLWN 1.20, MLWS 0.61, MSL 1.78, HAT 3.68 m above LAT; matches J&C 2.5 m spring and 3.7 m Table 1); Esri Wayback 197 releases scanned (6 distinct z18 images 2016-2025 plus 2010 z17; nothing older); BRC 2016 1 m LiDAR DEM has NoData over the whole platform (lowest valid 0.58 m); QImagery archive needs a token (not bypassed); ABC/RWR/Swellnet/Bundaberg Region pages saved. 12 images registered (img-09..20). 3D still not buildable (crest, seabed missing). Platform outline not re-traced on the larger south frame.
Mexico/Xala: nothing new that allows a trace. RWR post fetched (announcement only), RWR search, xala.com pages, Hollywood Reporter, WSCC bio, DHI, SEMARNAT search (gaceta host unreachable), Esri imagery of the coast (no visible works): no plan, coordinates or size. Context only: Xala has ~5 miles of coast near the Xola-Paraman lagoon, 10 min from the Costalegre airport. FEASIBILITY section 6 written; 2 imagery rows registered display:false. Dead ends logged: 02_research/dead_ends/burkitts-reef-bargara.json (+15), mexico-reef-2026-unnamed.json (+10). Cards: references/notes appended (Burkitts R19-R22, Mexico R13), one write per card. Docs and data are in the two reef folders (src/docs, src/web_text, src/wayback, src/dem, src/imagery).

## 2026-10-10 - dead-ends files for all 13 reefs (agent: dead-ends compilation, cloud)
- Built `02_research/dead_ends/<slug>.json` for all 13 reefs (format: `02_research/dead_ends/README.md`; rule 11 in `_agent_briefs/common.md`): every source or search that was checked and gave nothing useful, with date, agent/run, result, detail and "might_work" (REQUESTS_FOR_LIOR ids P/E/W/G/D where they exist). 181 entries in total (Narrowneck 15, Cables 19, Pratte's 12, Mount Maunganui 8, Opunake 16, Boscombe 12, Kovalam 12, Borth 10, Palm Beach 11, Albany 14, Burkitts 23, Bunbury 12, Mexico 17). Cards were NOT edited; dead ends are not references. Nothing in 04_build/ or papers/ touched; no git.
- Mined (grep, no dumps): shape-folder sources.md / FEASIBILITY / METHOD / VERIFY / HANDOFF / SOURCE_AUDIT / REPORT_* / 3d/*.md, `07_scale/verified/<slug>.md`, `05_qa/reef/<slug>_media_recheck.*`, card `blocked_sources` / `gaps` / `images_rejected` / `videos_rejected`, `05_qa/blocked_sources.md`, `05_qa/source_audit/*`, images.json (`used_for` not_used / display false), STATUS, REQUESTS (both versions), plus `07_scale/bathymetry/gold_coast` and `07_scale/bathymetry/emodnet` (shared dead ends).
- papers/ (PyMuPDF, 5 PDFs): "papers/ folder" entries only where no paper helped: Albany (no mention), Bunbury (no mention), Mexico (only the Yucatan geotextile reefs and Mortensen 2010 in references), Palm Beach (all 'Palm Beach' hits are Palm Beach, Florida: wrong site), Burkitts (only the Rendle Table 2.1 row; entry written by the Burkitts+Mexico agent). Partial-yield entries (paper helped for facts but not for the plan) for Opunake, Boscombe (Rendle thesis: no as-built plan) and Mount Maunganui (P2/P3: no as-built plan with scale/datum). The Mount Maunganui 2007 PDF has no text layer (image pages; tesseract not installed, no installs), so it could not be text-searched for any reef.
- Shared entries added to several reefs: EMODnet DTM 2024 "no coverage (HTTP 204)" for the 11 non-European reefs; Gold Coast DTM / Contours / State bathymetry survey not public for Narrowneck and Palm Beach.
- Merged with entries other agents wrote in parallel (Cables imagery+bathymetry, Burkitts+Mexico network pass; Albany 3D agent was still running when this finished): their entries kept; own entries made stale by their later reads were removed or merged (Burkitts: Jackson and Corbett 2007 is now read; Mexico: RWR post fetched fine in the network pass). Four Albany dead ends were taken from the Albany 3D agent's SOURCES_3D.md / METHODS_3D.md: if that agent appends its own, check for duplicates.
- Runs that disagree are kept side by side in `detail` (e.g. SurferToday R4/R5 read vs blocked; RWR Opunake/Kovalam images rejected by the 09-25 recheck vs re-viewed genuine; Surfline R7; Black and Mead 2001 record; Vimeo 11274816; Kovalam surfer.com read via Wayback vs web.archive.org unreachable).
- New small facts found while compiling: Cables Bancroft 1999 thesis URL at data-ww3.ifremer.fr returns HTTP 403 from the origin ("Server unable to read htaccess file"); not a bot check.

## 2026-10-10 - Albany (southern-ocean-surf-reef-albany): network run, 3D model built (LOW confidence)
- Fetched (network FULL): City of Albany project page + 8 documents (only a 5-page executive summary of the Detailed Design Report is public; no depths), EPA WA referral incl. BMT 2018 EIA (Fig 6.9 spot soundings m CD), Raised Water Research gallery (RHDHV 2015 Option B plan with seabed contours -0.5...-8 m), DoT/BoM 2024 tide predictions, Esri Wayback (19 releases: only 3 captures exist, 2022-12-19 / 2025-01-16 / 2026-01-20, no construction image). Navionics viewer rendered no map in headless Chrome (nothing bypassed); AusSeabed/GA 403. All saved under shapes/<slug>/src/ (city_docs, epa, rwr_images, tides).
- Built `07_scale/shapes/southern-ocean-surf-reef-albany/3d/` (viewer, model.js, docs.js, METHODS_3D, REGISTER_3D with sources/assumptions A1-A12/decisions D1-D10, annotated A1-A3, previews). Seabed profile read from the 2015 contours (georeferenced on Esri, datum assumed AHD); crest -1.0/-2.0 m AHD (City); LAT -0.74 m AHD derived. Design outline 13,104 m2, volume fitted to 34,000 m3 (unfitted loft 20,826 m3), satellite outline 30,273 m3; pile mean 2.6 m, max 6.0 m, +-1 m. Unresolved: BMT near-shore sounding 1.6 m deeper than the contours. 3D confidence LOW.
- Registry: 15 images added (img-14...28), check_registry PASSED. Dead ends: 11 entries appended to 02_research/dead_ends/southern-ocean-surf-reef-albany.json. papers/ checked first: nothing on Albany.
- For main: `3d/PAGE_TEXTS_FOR_MAIN.json` (combined / curated / caveats), remove slug from models3d_hold.json, run update_page.py. 04_build and papers/ not touched.

## 2026-10-10 - final page agent: pending edits, Cables + Albany on the 3D tab, dead-ends section (agent: final page agent, cloud)
- Outcome: page rebuilt with `update_page.py --full`, "state saved"; check 247 PASS / 0 FAIL, qa_models3d 191 PASS / 0 FAIL; 9 models on the 3D tab (+ Cables, Albany), combined scene 9/9 OK; hidden outlines still 4 (Mexico, Opunake, Burkitts, Kovalam; Burkitts `reef_zone` is not read by the hiding logic).
- Applied the pending edits (Boscombe incl. Rendle p.70 crest, Bunbury fill-type caveat + state, Mount Maunganui key numbers 1/2/4, Narrowneck D7, Palm Beach volume quantities + A12-A14 pointer, Prattes +-150 m); files moved to `05_qa/pending_page_edits/applied/`. Card notes of those audits were already in the cards (Kovalam Rendle 4,300 m3 / bbox 43x24 vs 38x29 still missing).
- Cables: curated + caveats (6 rows) + combined (`shore_mode:"none"`) merged, removed from the hold list; card lat/lon -32.0156, 115.7485, size text and new ref R22 (DoT WA bathymetry). Albany: entries merged (LOW stated plainly), removed from hold; card refs R20 (BMT 2018 EIA), R21 (RHDHV 2015 plan via RWR), R22 (DoT/BoM 2024 tides), City table 34,000 m3 verified on design.jpg.
- Albany viewer defect (reef drawn at z = height above seabed, up to +6 m MSL): fixed in the page copy only (`compile_models3d.py VIEWER_FIXES`); the 3D agent must fix `07_scale/shapes/southern-ocean-surf-reef-albany/3d/index.html` (`z = seaAt(x, y) + hv / 100`).
- Dead ends: new last section of every reef dialog "Checked, nothing useful (N)", closed by default, not in References (196 entries); check.py tests it for all 13.
- Also fixed: combined labels overlapped with 9 reefs (placeLabels free-area scan), Cables version buttons covered by an overflowing date (models3d.css), 3D key-number header "Model source ids", 3D references fallback for METHODS_3D files whose References section is a pointer.
- Screenshots viewed (3): 3D tab list, Albany 3D entry, Albany dead-ends section at 390 px. Details: `04_build/HANDOFF.md` section 0c.

## 2026-10-13 - Opunake: TRC Technical Report 2009-33 and NZ Geographic read; reef position found (agent: Opunake TRC/NZGeo task, cloud)
- Outcome: the reef POSITION and design SIZE are now documented, the bag layout is not. TRC 2009-33 (Lior's upload P15): Coastal Permit 6376-1 (31 May 2005) publishes the 4 corner co-ordinates of the occupation area (Taranaki circuit grid = NZGD49): 189 x 94 m, centre -39.45943, 173.85163, long axis 63 deg (first easting misprinted 257484 = 267484; rectangle closure + GR P20:832-937 confirm). TRC Fig 1 georeferenced on those corners (residual 0.3 m; boat ramp check 0.7 m): its 'Proposed location of surf reef' rectangle is the consent area, not the reef. Design size 99 x 30 x 3.5 m, volume about 4,900 m3 (area 2,970 = 99 x 30, a bounding rectangle), 3.0-1.8 m below chart datum, shallowest contour 0.0 m below chart datum (LAT); 27 bags April 2008, not finished Sept 2009. Size conflict resolved: 90 x 20 m is the 2004 concept (Daily News 11 Jun 2004), 99 x 30 = Blacka 100 x 30. NZ Geographic (P16): text only, no Opunake figure.
- Verdict: reef shape NO (no source draws the bags); position/size YES. shape.json status envelope_only (consent area = default outline, assumed 99 x 30 m rectangle optional, LOW); page stays hidden, no 3D. Recommendation for main in `07_scale/shapes/opunake-reef/FEASIBILITY.md`: card lat/lon -> -39.4594, 173.8516 (done in the card), optional Lior decision to show the consent area only.
- Files: `07_scale/shapes/opunake-reef/` (FEASIBILITY, HANDOFF, METHOD, VERIFY, sources, shape.json, consent_georef.json, scripts/, overlays/, src/ +9 images); card `02_research/reefs/opunake-reef.json/.md` (R18-R20); registry img-17..25 (check_registry PASSED); dead ends +5; OCR files in `05_qa/papers_intake/` (2); LINZ grid nz_linz_nzgd2kgrid0005.tif kept in scripts/proj_grid/ (197 KB).
- Requests: P15 and P16 DONE; new items (consent file documents, G8 target) appended to REQUESTS_FOR_LIOR.md. 04_build, papers/ and `new uploads from lior/` untouched.

## 2026-10-13 - Albany: Lior's four uploads read; 3D unchanged in geometry; card, registry, dead ends, W8 (agent: Albany uploads task, cloud; resumed after the usage-limit stop)
- Outcome: no as-built level, crest, section, seabed depth or rock-size table in any of the four uploads or the live Raised Water Research pages, so the Albany 3D geometry stays as it was (LOW; RHDHV 2015 contours, datum assumed AHD, 1.6 m conflict with BMT 2018 open). What changed is the timeline and the notes. FAQ PDF = byte-identical to our copy. None of the 3 RWR pages is another reef (spot page title "Midds Reef").
- Facts (all with locations in `07_scale/shapes/southern-ocean-surf-reef-albany/3d/REGISTER_3D.md` S15-S23 and METHODS_3D.md 3.4 / 8 / 9): first rock 18 Mar 2025 (card said Oct 2024 - Mar 2025 placement); two-thirds complete 16 May; storm Mon 26 May 2025 moved some core rock shoreward; opened 16 Jul 2025 after four months; 13 M AUD. Moved rocks 2026: about 18 high rocks, two days late Feb 2026, divers + local vessel + Albany Boardriders, "more than $20,000" / "about $24,000" (paywalled article metadata, D12). Conflicts recorded, not resolved: funding split (City vs WA Government/RWR), 140 vs 120 m offshore, 62,800 vs 70,000 t.
- 3D: build_3d.py text strings (state, design-version date) + sensitivity `if_built_70000_t` (design outline 37,898 m3, mean height 2.89 m); rebuilt, model.js differs only in those; viewer reloaded headless with no JS error; METHODS_3D.md has a full References list (section 8) and a before/after (section 9); `3d/PAGE_TEXTS_FOR_MAIN.json` key `_update_2026-10-13` has the exact old -> new for main.
- W8: GA portal and services give 403 / scripts as HTML (not bypassed); `3d/W8_how_to.png` (registry img-30) with lat -35.018005, lon 117.920991 and 5 steps + the 5-line text in `3d/REQUESTS_FOR_LIOR.md`; lead: WA DoT "Middleton Bay & Oyster Harbour" multibeam/laser surveys from GA's 2021 holdings list (42 MB; the 69 MB 2019 zip was not downloaded).
- Card `02_research/reefs/southern-ocean-surf-reef-albany.json/.md`: year, as_built_vs_design, status_now, unexpected_results, financed_by (conflict flagged), size, gaps updated; R10/R11/R18 extended; R23-R33 added; moved-rocks photo added to images. Registry img-29, img-30 (check_registry: no Albany errors; the 8 errors are Boscombe/Borth files of another agent). Dead ends +5. OCR: `05_qa/papers_intake/albany_rwr_pdfs_ocr.md`.
- Not touched: 04_build/, papers/, new uploads from lior/. Note for main/Mexico: RWR image `Reef2.jpg` (upload 2026/03, a barrel) seen on the RWR sidebar belongs to RWR's "Unveiling the new reef in Mexico" post, not Albany; not saved.

## 2026-10-13 - Cables: default label fixed, References list, Fremantle datum link (agent: Cables fixes + datum, cloud, resumed after the usage-limit stop)
- Outcome: (1) model.js no longer labels the original design plan "(default)"; the default is the Nov 1999 surveyed surface (`survey_surface_1999_11`). Compared with the pre-WIP model.js (commit 3ca8da5): surveyed versions, seabed, outlines identical; only the design versions, datum, water-level labels and texts changed, because of (3). (2) METHODS_3D section 8 is a numbered full-citation list (items 1-20). (3) A12 closed: AHD 0.000 = Fremantle LWD + 0.716 m (Roelse, Granger and Graham 1975, DNM Technical Report 12, Table 3: 2.350 ft; cross-checks PSMSL 111, BODC GLOSS 53, GA AHD page; copies in `07_scale/shapes/cables-reef-wa/src/datum/`). Reading A holds, B (RL = MSL) is 0.5-0.6 m off the soundings; the remaining 0.13-0.22 m gap to the soundings is physical or survey, not datum. HAT / LAT of Fremantle NOT found.
- Numbers changed (old -> new): reading A offset 0.78 -> 0.716 m; design crest -1.78 -> -1.72 m AHD; datum level -0.78 -> -0.716; design-surface volume 3,920 / 4,249 -> 4,136 / 4,465 m3 (original / with extension); mean thickness 0.97 -> 1.02 m; design vs surveyed volume -16 / -25 % -> -11 / -21 %; survey minus design (Nov 1999) +0.31 -> +0.25 m. Unchanged: surveyed volumes 4,671 / 5,219 m3, crest -1.55 / -1.71 m, seabed, outlines. Full before/after table: `3d/METHODS_3D.md` section 12.
- Files: `07_scale/shapes/cables-reef-wa/3d/METHODS_3D.md`, `3d/PAGE_TEXTS_FOR_MAIN.json` (new key `page_edits_2026_10_13`: exact old -> new for models3d_curated / combined / caveats), `3d/REQUESTS_FOR_LIOR.md`, `HANDOFF.md` (section 8 CHECKPOINT), `03_images/reefs/cables-reef-wa/images.json` (img-30 / 31 hashes refreshed; check_registry passes for cables), `02_research/dead_ends/cables-reef-wa.json` (+6 entries). Earlier today (previous agent, WIP commit): build_3d.py, provenance.py, model.js, docs.js, index.html, SOURCES_3D.md, `scripts/datum_link.*`, `src/datum/`.
- For main: apply `page_edits_2026_10_13` to `04_build/data/models3d_curated.json`, `models3d_combined.json`, `models3d_caveats.json` (the old caveat 'ev' "unresolved gap 0.2-0.3 m (A12)" and "thickness 0.97 m modelled vs 1.15-1.29 m surveyed" no longer exist in METHODS_3D, so the page check would fail until replaced), then `update_page.py --full`.
- For Lior: E7 partly done (offset found); HAT / LAT still open, contact Tides@transport.wa.gov.au and a draft e-mail are in REQUESTS_FOR_LIOR.md ('Cables update 2026-10-13'). Optional: save the Landgate AHD71 Perth PDF in a browser.
- Noted, not changed: two surveyed-volume figures coexist (grid 4,671 / 5,219 m3 on the page; point-based 4,751 / 5,201 m3 in model.js provenance and confidence text); documented in METHODS_3D 3.4.

## 2026-10-13 - SeaDataNet CDI records for Boscombe and Borth (W1/W2) and Kovalam retries (agent: W1/W2 SeaDataNet + Kovalam, cloud, resumed after the usage-limit stop)
- What: finished W1/W2 (the first agent had made the evidence files, SOURCES_3D sections and figures; this agent added the missing REQUESTS lines, registry rows, dead ends, HANDOFF checkpoints and a second probe of the endpoints) and did the Kovalam part (Wayback, Navionics, card fix).
- W1/W2 result: CDI 117452 = global 1982230 "Poole Bay, Blocks 14-17", survey 2011-08-26 to 2012-04-06, UKHO / OceanWise, access "by negotiation", instrument unknown (probably MCA survey HI1366); CDI 115084 = global 1981385 "CARDIGAN BAY", survey 1969-03-11 to 1969-05-25, single-beam echosounders. Vertical and horizontal datum and resolution NOT obtained (record pages behind a bot check, not bypassed; no public CSW or API; the BGS ISO record of HI1366 gives only EPSG:4326). Lior's 5 lines and figures are in REQUESTS_FOR_LIOR.md.
- Values that may be wrong (documentation only, models untouched): Boscombe METHODS_3D line 175 calls the EMODnet grid "older" (it is NEWER than the April 2011 survey; wording fix for main); Borth METHODS_3D lines 21 and 180 do not state that the EMODnet cells behind the gradient and the 0.7-1.2 m offset are a 1969 single-beam survey with unknown reduction datum.
- Kovalam: card R15 added (Rendle 2016 Table 2.1, PDF p.41: 4,300 m3 SFC, checked in papers/), volume list now 3,000 / 4,000 / 4,300 / 4,800, bbox mismatch noted (43 x 24 m in shape.json = axis-aligned extent in the canonical frame, 38 x 29 m in rectify_result.json from the sweep script's own frame; same shape, areas agree). Surfer article re-read via `web.archive.org/web/2/<url>`: no plan or dimensions. Archived asrltd.com pages: none usable. Navionics/Garmin viewer: no map in the cloud headless Chrome (geohash URL format `https://maps.garmin.com/en-US/marine?maps=another-brand&overlay=false&key=<geohash12>`; Kovalam geohash t9qxxwgbpf4n). Kovalam stays hidden.
- Registry: boscombe-surf-reef-img-44/45, borth-coastal-defence-reef-img-32/33 (CDI base maps and click-point figures); check_registry.py PASSED. Dead ends added: Boscombe 1, Borth 1, Kovalam 3.
- Files: 07_scale/shapes/{boscombe-surf-reef,borth-coastal-defence-reef,kovalam-reef-india}/HANDOFF.md, boscombe 3d/SOURCES_3D.md + src/cdi_2026-10-13/, borth 3d/SOURCES_3D.md, 02_research/reefs/kovalam-reef-india.json/.md, 02_research/dead_ends/{boscombe-surf-reef,borth-coastal-defence-reef,kovalam-reef-india}.json, 03_images/reefs/{boscombe-surf-reef,borth-coastal-defence-reef}/{images.json,IMAGES.md}, 03_images/reefs/NEW_IMAGES_LOG.md, REQUESTS_FOR_LIOR.md.

## 2026-10-13 (page agent, map links) - "Open location in..." block
- Done: coordinates (5 decimals + degrees-decimal-minutes) with a Copy button, Google Maps, satellite, Google Earth (web), and a per-reef KML for Google Earth Pro (placemark + note + confidence; the traced outline only for reefs whose outline is shown, never for Opunake, Kovalam, Mexico, Burkitts) in the reef dialog, each gallery tile (a menu that does not open the dialog) and each 3D tab model header; "All reefs (KML)" button in the gallery controls. Files: 04_build/src/compile_data.py, app.js, models3d.js, styles.css, template.html, check.py; 04_build/HANDOFF.md section 0d.
- Tested: Navionics web app has no centred URL (it redirects to a Garmin page), so the page says "paste the copied coordinates into its search box" and has no Navionics link.
- NOT done (deadline 00:04 UTC): EMODnet (Boscombe, Borth) and GEBCO viewer links: URL formats not tested, so none added. Next agent: see HANDOFF 0d.

## 2026-10-13 (late, 23:45-00:00 UTC) - P2 Mount Maunganui 2007 OCR (Haiku)
- Done: OCR of papers/Mount Maunganui Reef-amalgamating design and the constraints 2007.pdf (6 pages, 300 dpi, tesseract 5.3.4 eng psm 3, single-threaded). Files: 05_qa/papers_intake/P2_mead_black_moores_2007_ocr.md (full text, cleaned lightly) and P2_mead_black_moores_2007.md (citation, quality, numbers with pages).
- Quality: medium; p.1 two-column interleaving; figures image-only; digits not proof-read on image.
- Open: place of conference and DOI not confirmed; container volume 900 m3 and "30 x 1.5 m" need image check; no costs or crest/CD datum in text. No model or card changed.

## 2026-10-19 (08_paper, tide corrections) - tides_check.md applied
- Done: Albany 1.38, Bunbury 1.20, Cables 1.14 m = WA DoT/BoM 2026 predicted annual range (about LAT-HAT, centred on MSL, lower bounds; NOT spring ranges); Opunake spring 3.16 / mean 2.35 (LINZ Port Taranaki 2026-27); Burkitts 2.33 / 1.74 (MSQ Burnett Heads); Pratte's relabelled great diurnal (GT 1.654, MN 1.145). New fields tide_range_type, tide_source in 08_paper/data/reefs.json and reefs_table.csv (rebuilt with data/src/build_reefs.py from src/reefs/*.py). Profile planes ANN_LO/ANN_HI added for the three WA reefs (Cables LWt/HWt +-0.4 removed); extract_profiles.py, figures_survey.tide_band and reef_inputs.py read them.
- Re-run: analysis/run_all.py, figures_survey/results/wave.py (png+pdf regenerated; fig1 legend and caption, fig7 axis and caption updated). Result changes: Albany surfable 0.59 -> 0.62, Cables 0.65 -> 0.63, Bunbury 0 -> 0.01; Spearman surfable fraction vs outcome (best line) 0.74 (p_perm 0.049) -> 0.69 (0.075), not quoted in the text; Israeli-tide comparison now 66 % of cases within 0.05 (old 75 % could not be reproduced exactly); built-reef crest-load range 1.0-3.4 -> 0.9-3.4 m.
- Text fixed: sections 01, 03, 04 (Table 2, tide paragraph, Fig 7 caption), 05 (Kt rows), 07, appendix C (Tables C3, C5, tide note), RESULTS.md, FINDINGS.md, data/README.md; refs added to 03_survey.refs.md and appendix_refs_pending.md. SW WA kept as micro-tidal (<2 m).
- Open: WA values are lower bounds (3 of 4 quarterly blocks parsed; a column-aware parser would give MHHW/MLLW and a typical daily range); Bunbury mean 0.25 and Cables mean 0.80 probably too small, not recomputed; MSQ/LINZ rows read from search extracts only; Port Taranaki as reference for Opunake unchecked; fig3/fig7 other reefs unchanged.

## 2026-10-19 (page agent) - paper-review additions on the page
- Added from 08_paper: Pratte's surfer testimony (6 reviews, grade D), reef rating A/B/C (Table column, Quick facts row, (i) note), corrected tide ranges as card text (Albany, Bunbury, Cables, Opunake, Burkitts, Prattes), "Paper figures" section (fig1-9). Fixed Albany image label and Cables 'Crest level' quote; applied Albany/Cables text-only PAGE_TEXTS. 3D untouched; 3D tide proposals listed in REQUESTS_FOR_LIOR.md (item T1). Details: 04_build/HANDOFF.md 0e.

## 2026-10-19 (08_paper, recut agent) - surf cuts Albany/Cables/Borth + figure fixes (Lior's figure review)
- `08_paper/analysis/extract_profiles.py`: per-reef CUT_OVERRIDES (surf cut through the surfed part, shore-normal; oblique sampling by bilinear interpolation); old line kept as `crest_line_auto`. Pipeline (`run_all.py`) and all figure scripts re-run; 3D models untouched.
- Figures: colour = reef with coloured name labels; marker shape = outcome class (unknown hollow) with legends; Fig. 4 axes/bands explained; Fig. 5 Hutt 2001 + Walker 1975, no personal names; Fig. 3 redrawn per `notes/fig3_theory.md` (two time steps, set-down/set-up, bores). Captions updated.
- RESULTS.md / FINDINGS.md edited in place (old values kept). Old/new numbers and writer to-do: `08_paper/analysis/RECUT_NOTES.md`. Albany's collapsing-band position in Fig. 4 resolved (mean face 1:4.0, Y 1.08 -> 1:19.8, Y 2.11). Sections text not edited.

## 2026-10-19 (page agent) - Palm Beach video 8Ebp7VNAGEY + viewer comment
- Added the wave-pocket-tracking video (title/channel from oEmbed, reef confirmed by title; video not watched) and the grade-D comment to the Palm Beach card; full update "state saved", check.py 0 failures. Details: 04_build/HANDOFF.md 0f.

## 2026-10-20 (page agent) - Opunake photo localised; testimony check
- Opunake Wikimedia photo (CC BY-SA 3.0) now served from `assets/opunake-reef/` via new generic `local` field (compile_data.py + app.js); same for other CC images already registered. Other hot-links left (rights not cleared). Pratte's/Palm Beach comments, videos and A/B/C rating confirmed in dialogs and Table. Full update "state saved", check.py 0 failures.
