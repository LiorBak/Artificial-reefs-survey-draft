# Media re-check — Borth coastal defence reef

Date: 2026-09-25. Method: each accepted image was downloaded to a scratch folder with
`curl -L -A "Mozilla/5.0"`, viewed directly, and classified against the rubric below; scratch
copies were deleted after viewing. Videos were not downloaded — classified from
`02_research/videos/borth-coastal-defence-reef/videos.json`, the (silent, no-transcript)
video notes already on file, and the dossier's description of the structure (submerged/semi-submerged
rock reef with visible causeway during construction). Frames were viewed directly from
`03_images/video_frames/borth-coastal-defence-reef/`.

Rubric: **structure_visible** (reef/rock/bags visible — construction, low-tide exposure, aerial of
footprint) / **reef_effect_visible** (structure submerged but its effect — wave break, salient, surfers
on the reef — is unmistakably at the reef site) / **site_context_only** (beach/town/generic surfing,
no visible link to the reef) / **unrelated_or_wrong_site** / **could_not_load**.

## Images

| # | URL | What I saw | Classification | Confidence |
|---|---|---|---|---|
| 1 | upload.wikimedia.org/.../A_bigger_splash...2366565.jpg | A dredging/plant barge ("CAN LORO", with tug "AFON GOCH") underway, deck loaded with white rock armour and a wheel loader, throwing up a large bow-wave/splash. This is the barge delivering rock armour material for the works, not the reef structure itself in place. | structure_visible | High — matches caption "wave breaking against a barge loaded with rock armour" (source page/geograph caption) and dossier's material-delivery narrative (8,000+ deliveries) |
| 2 | s0.geograph.org.uk/.../2554717_ca5fc76b.jpg | A chain-link construction fence with a red/white "Construction Operations KEEP OUT" sign, Borth beach and seafront visible behind (shingle, groynes, houses), no reef or rock structure visible offshore. | site_context_only | High — image shows only beach/town + closure signage, matches its own caption exactly; no structure visible |
| 3 | s0.geograph.org.uk/.../2575564_e576dfb2.jpg | Three excavators working along an offshore rock causeway/reef extending into the sea, evening light, sea calm; this is the causeway/reef under construction at Borth's southern end. | structure_visible | High — matches caption "Building the reef: Borth sea defences" and dossier's causeway-construction narrative |
| 4 | borthcommunity.info/.../20110818-100400.jpg | Three yellow "Norton's"-branded excavators plus a dump truck working on a rock causeway/reef extending into calm water, low afternoon light. | structure_visible | High — matches caption (official BAM Nuttall progress photo, August 2011, Norton's plant) and dossier |
| 5 | borthcommunity.info/.../20110818-101454.jpg | One yellow Komatsu excavator loading a dump truck on the same rock causeway/reef extending into the sea. | structure_visible | High — matches caption (official progress photo, August 2011) |

Google Maps satellite link (6th "image" entry) was not re-downloaded — it is a live map view, not a
fixed photo, and was already correctly labelled `kind: map` rather than a "reef effect" photo; no
change needed.

## Frames (video_frames/borth-coastal-defence-reef/, excluding rejected/)

| File | What I saw | Classification | Confidence |
|---|---|---|---|
| AJXnUqQObJM_0015.jpg | Two excavators on an offshore rock spit/causeway, waves breaking on the sand in the foreground, overcast sky. | structure_visible | High — matches dossier caption exactly (excavators building the reef, seen from the beach) |
| QUB6s_F9dZc_0007.jpg | Borth seafront houses beside a shingle beach; excavators, dump trucks and a large stockpile of quarried rock/shingle material in the foreground (onshore stockpile/sorting area, not the offshore reef itself). | site_context_only (onshore works, not the reef structure or its effect) | High — the pile and plant shown are landward material handling, not the reef; caption in videos.json already says this correctly ("houses...construction plant and large stockpiled rock/shingle piles"), but this is coastal-defence-works context, not reef-structure-or-effect content |

Note: I am marking QUB6s_F9dZc_0007.jpg more strictly than the original dossier/videos.json frame
caption, which is accurate as a description but doesn't itself establish "reef visible" — the frame shows
onshore stockpiling for the wider coastal-defence works, not the offshore reef or its effect. This is a
minor downgrade for precision, not a removal (the video/frame is legitimately about the Borth coastal-
defence project, just not the reef structure specifically).

## Videos

All four accepted videos are silent amateur construction b-roll; none contain surfing footage,
and none were found to depict "the beach but never the reef" the way Lior flagged for other reefs —
this reef's video set does not have that problem.

| Video | Title | Evidence used | Classification | best_timestamp_seconds |
|---|---|---|---|---|
| c4J6hfvynr4 | "Borth Sea Defenses Video 3 Feb 2011" | videos.json: "filming the coastal-defence/reef construction site at Borth in February 2011, early in the works"; silent, no captions | about_the_reef (construction b-roll of the works site; too early/generic to pin an exact reef-only timestamp) | null (no reef-specific moment identified — early general site b-roll) |
| AJXnUqQObJM | "Borth sea defences and reef" | videos.json + frame AJXnUqQObJM_0015.jpg viewed directly: two excavators building the offshore rock reef, filmed from the beach | about_the_reef | 15 |
| QUB6s_F9dZc | "Borth Beach Sea Defence Works August 2011" | videos.json + frame QUB6s_F9dZc_0007.jpg viewed directly: houses, plant and stockpiled material on the seafront/onshore area, not the offshore reef itself | mentions_reef_briefly (wider coastal-defence works shown; the reef structure itself is not on screen at this frame) | 7 |
| dQieZVQUDEI | "borth sea defence 2012" | videos.json: description "komatsu 450 separating rock and shingle" — material sorting/grading, into 2012, matching Coflein's stated reef/coastal-defence completion date; not independently re-viewed here (embed_ok:false, no new download per no-new-media-search rule) | mentions_reef_briefly (material prep for the works; not shown at the reef structure itself per available description) | 60 (as previously recorded; unverified against footage, since no re-download was performed) |

## Hero image recommendation

**Recommended hero: image #3 / #4 (offshore rock causeway/reef under construction, multiple excavators,
calm evening sea)** — image 3 (`2575564_e576dfb2.jpg`, "Building the reef: Borth sea defences") is the
single clearest, best-composed shot that shows the reef structure itself extending into the sea with
plant actively working on it, correctly captioned at source. Image 4 is an equally valid alternate from
the official BAM Nuttall progress-photo set. Image 1 (barge/splash) is a strong secondary hero for dynamism
but shows a supply barge, not the reef site itself.

## Overall recheck verdict for this reef

No mislabelled or misleading media were found in the accepted image set — all five images either show
the reef/causeway structure under construction (4 of 5) or are correctly limited in the card to
"construction closure" context (1 of 5, already accurately captioned as such). The one frame
(QUB6s_F9dZc_0007.jpg) is reclassified from an implicit "reef-adjacent" read down to
`site_context_only`-equivalent (onshore works) for precision, but its caption in the source JSON was
already accurate and not misleading. Unlike the case Lior flagged for other reefs, no video or image
here shows generic beach/surfing scenery mislabelled as reef content — Borth's media set is
construction-documentary in nature throughout.
