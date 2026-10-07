# Media re-check — mexico-reef-2026-unnamed (Xala Reef, Costalegre, Mexico)

Re-check date: 2026-09-25
Card: `02_research/reefs/mexico-reef-2026-unnamed.json`
Dossier context used: reef is a submerged rock/boulder structure (3,000 truckloads of quarried boulders), not exposed at the surface; no aerial-of-footprint or construction imagery exists in any source found. Structure itself is therefore never expected to be visible in a photo — only its wave effect can be.

## Videos

None to check. `02_research/videos/mexico-reef-2026-unnamed/videos.json` = `[]`, and the reef card's `videos[]` field is also empty. No transcripts exist. Nothing was previously accepted, so there is nothing to reject.

## Frames

None to check. No folder exists at `03_images/video_frames/mexico-reef-2026-unnamed/` (consistent with there being zero videos to extract frames from).

## Images (2 accepted on the card)

| # | URL | Card's current framing | Downloaded & viewed | New classification | Evidence |
|---|-----|------------------------|----------------------|---------------------|----------|
| 1 | `raisedwaterresearch.com/.../Reef2.jpg` | "Header image ... consistent with the Xala reef story" | Yes (136 KB JPEG, 1280×853) | **site_context_only** | Ground-level shot of a surfer inside a barreling wave, open ocean, no reef structure, no identifying landmark, no aerial/footprint view. The source article (raisedwaterresearch.com/unveiling-the-new-reef-in-mexico/) uses this only as its generic lead/header image — it is **not** the image the article explicitly captions as the reef. Per rubric, a submerged-structure photo needs the caption/source page to place it at the reef for `reef_effect_visible`; this one carries no such caption, only the card's own hedge ("consistent with ... the story"). Downgraded from an implicit "reef photo" framing to a plain surf photo with no verified link to the Xala site. |
| 2 | `raisedwaterresearch.com/.../Reef1-1024x573.jpg` | "Explicitly captioned ... 'Mexico's first artificial surf reef at Xala' — aerial shot of a clean peeling wave with a surfer riding it" | Yes (68 KB JPEG, 1024×573) | **reef_effect_visible** (confirmed) | Aerial/drone photo: a clean, consistently peeling left-hander breaking at one spot, surfer riding it, drone/helicopter visible in frame. The source page's own caption ties this specific image to "Mexico's first artificial surf reef at Xala" [R1]. The rock reef itself is submerged and not visible (consistent with the dossier's construction description), but the wave's clean, repeatable peel at the reef's (undisclosed but implied) location, combined with the source's explicit caption, satisfies `reef_effect_visible`. This image was already correctly classified on the card — confirmed, no change. |

### Rejected image (already excluded, re-confirmed correct)

- Google Maps link (`google.com/maps/@19.71861,-105.23222,13z`) — not a photo (serves HTML, not an image); already correctly in `images_rejected[]` with the caveat that it's only an approximate area pin, not the confirmed reef location. No change needed.

## Recommended hero image

**`https://raisedwaterresearch.com/wp-content/uploads/2026/04/Reef1-1024x573.jpg`** (Reef1) — the only image on this card that the source itself explicitly ties to "Mexico's first artificial surf reef at Xala," showing the reef's wave effect (a clean, repeatable peeling break) rather than a generic surf shot.

## Recommended card change (not applied here — Gemini-style output only, per task instructions to not touch the verified card without separate action)

- Reef2.jpg's `depicts` field should be tightened from framing it as reef-related ("consistent with the Xala reef story") to a plain caption noting it is the article's generic header image with no explicit link to the reef, i.e. reclassify it as `site_context_only` in any future compile pass.

## Method / documentation of what was relied on

- Downloaded each image URL directly from the card with `curl -L -A "Mozilla/5.0"` to a session scratchpad, viewed each with the Read (image) tool, then deleted the scratch copies (both files removed after viewing; scratchpad now clean of these files).
- Classification used: (a) the rubric definitions in the task; (b) the dossier's own description of the structure (submerged rock/boulder reef, no exposed/emergent structure, no drone-of-footprint imagery ever located [R1][R3][R4]); (c) the source page's own captions, read from the card's `images[].depicts` field, which quotes/paraphrases the original raisedwaterresearch.com captions — Image 2's caption ("Mexico's first artificial surf reef at Xala") is the deciding evidence for `reef_effect_visible`; Image 1 has no equivalent caption tying it to the reef, hence `site_context_only`.
- No new photo/video searches were performed — both images were already on the verified card; only re-verification (download + view) was done, per task scope.
