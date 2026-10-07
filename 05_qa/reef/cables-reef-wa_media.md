Status: verified 2026-09-24

Adversarial media verification of `03_images/web/cables-reef-wa.json` and `02_research/videos/cables-reef-wa/videos.json` for **Cable Station Reef (Cables Reef)**, Leighton/Cottesloe, Perth, WA, Australia.

Inputs: 6 candidate web images, 0 videos, 0 extracted video frames (videos.json is empty — no video leads were found for this site during research). Lior's `from_lior` figure index was also checked for anything belonging to this slug.

## Images

| # | URL | Verdict | Evidence | What I saw |
|---|---|---|---|---|
| 1 | raisedwaterresearch.com/.../Cables-Reef.jpg | **belongs** | Source page (live WebFetch) confirms this is the header/main photo on the dedicated "Cables Reef" spot page, which the page identifies as "an artificial surfing reef off Cable Station in Perth, Western Australia." Downloaded via curl: 44,756 bytes, JPEG 700×394, HTTP 200, Content-Type: image/jpeg. Hotlink test (no Referer): HTTP 200, image/jpeg ⇒ hotlink_ok. | A wide ocean/coast shot: a clean left-breaking wave with several surfers paddling/sitting in the lineup and one rider on the wave face. Consistent with a surf-reef break; no landmark text visible but matches the page's own framing of this as the Cables Reef break. |
| 2 | raisedwaterresearch.com/.../cabletopturn.jpg | **belongs** | Same source page (live). WebFetch confirms this file depicts "a surfer executing a turn on the reef." Downloaded: 27,618 bytes, JPEG 501×301, HTTP 200, image/jpeg. Hotlink: HTTP 200, image/jpeg ⇒ hotlink_ok. | A surfer performing a top turn on a breaking wave, another surfer sitting in the water nearby. Generic surf action shot, plausible as Cables Reef and directly hosted on the page dedicated to this exact break; filename itself ("cabletopturn") matches the page's own image set. |
| 3 | raisedwaterresearch.com/.../Cables-Side-View.jpg | **belongs** | Same source page (live). WebFetch confirms this is captioned "Side view of Cables Reef" on the page. Downloaded: 26,874 bytes, JPEG 573×226, HTTP 200, image/jpeg. Hotlink: HTTP 200, image/jpeg ⇒ hotlink_ok. | A simple line-drawing cross-section diagram: sea surface, a raised bump labelled "PROPOSED ENHANCEMENT" over the "EXISTING SEA BED." This is a schematic engineering profile, exactly matching a reef-design cross-section (consistent with the dossier's description of physical-model design studies for the reef shape). Not a photo, but correctly labelled and hosted on the reef-specific page. |
| 4 | surfingdownsouth.com.au/.../1948-Surfing-Cable-Station...jpg | **belongs** | Source page (live WebFetch) confirms caption: "1948 Surfers at Cable Station reef riding canvas covered stand up boards and a toothpick surfboard. Water photo by Don Bancroft." Downloaded: 97,706 bytes, JPEG 800×450, HTTP 200, image/jpeg. Hotlink: HTTP 200, image/jpeg ⇒ hotlink_ok. | A black-and-white water-level photo showing three surfers riding a wave on early wooden/canvas boards, with the bow of the photographer's paddle craft in the foreground. Matches the caption exactly — pre-reef natural break at the same site, dated 1948. |
| 5 | i0.wp.com/surfingdownsouth.com.au/.../1957-City-Beach-BC-crew...jpg | **belongs** | Source page (live WebFetch) confirms caption: "1957 Brian Cole (second from right) and his City Beach surfing mates heading to Cables Station reef for a surf... Morris 10 sedan is loaded with plywood toothpick surfboards." Downloaded: 207,914 bytes, JPEG 800×513, HTTP 200, image/jpeg (Content-Length matched exactly). Hotlink: HTTP 200, image/jpeg ⇒ hotlink_ok. | Black-and-white group photo: five young men holding paddles, posing beside a small car with surfboards/paddles strapped to the roof, on a sandy street/verge. Matches the caption — a car loaded with vintage boards heading to Cable Station, dated 1957. |
| 6 | google.com/maps/@-32.0157,115.7497,17z (satellite link) | **dropped — does not belong as an image asset** | This is a live Google Maps HTML page, not a static image file: `curl -sI` returns HTTP 200 but Content-Type: text/html, not image/*. It fails the "download + content-type image/*" test outright — there is no fixed image to fetch, view or hotlink. Even setting that aside, the dossier's own entry for this candidate already notes "the reef structure itself is submerged and may not be clearly resolved in satellite imagery," so it could not be visually confirmed to show the reef even if treated as a map/screenshot lead. | N/A — no image file exists at this URL to view. |

## Videos

None. `02_research/videos/cables-reef-wa/videos.json` is `[]` — the research stage explicitly reported no YouTube/Vimeo leads found for this site (dossier's own "Video leads" section: "Not found"). No video verification was possible or needed; `videos: []` in the output card.

## Video frames

None. `03_images/video_frames/cables-reef-wa/` does not exist (no videos were found, so no frames were ever extracted). Nothing to verify or drop.

## Lior's own figures (from_lior)

Checked `03_images/from_lior/` (goldcoast_pptx, suggestions, surf_route, and the two standalone PNGs) for anything belonging to this slug. One relevant item found:

- **`03_images/from_lior/goldcoast_pptx/image26.png`** — per its own INDEX.md, a "4-panel satellite comparison: Narrowneck / Cables / Mount Reef / Pratte's Reef, with 'bags falling apart' caption," flagged in the index itself as "Key reference image — but third-party/copyrighted, flag before reuse." The dossier's own text (see its "Correcting a source-file caption" passage) already establishes that the "bags falling apart" caption describes the geotextile-bag reefs (Narrowneck/Mount Reef/Pratte's), **not** Cables, since Cables was built from granite/limestone rock, not bags. Included in the card's `lior_images` with a caption carrying that caveat, so the HTML builder doesn't present the "bags falling apart" text as describing Cables itself. Flagged copyright status (third-party satellite/comparison graphic) is preserved in the caption for the builder's awareness.

## Summary

- 6 candidate images reviewed: **5 accepted** (all hosted directly on the two source pages already tied to this exact site, captions confirmed live, all downloaded successfully >5KB with image/jpeg content-type, all pass hotlink test), **1 dropped** (Google Maps link — not a static image asset, fails the content-type test, and the dossier itself flags the submerged structure as not clearly visible in satellite imagery anyway).
- 0 videos, 0 frames — none exist for this slug.
- 1 Lior figure identified as relevant (image26.png, 4-panel comparison graphic) and included with a corrective caption.
- No web images were copied into the project folder; all accepted images remain link-only per project rules. Scratch downloads used for verification were deleted after inspection.
