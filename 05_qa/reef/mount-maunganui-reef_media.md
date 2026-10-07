Status: verified 2026-09-24 — 5/5 images accepted, 1/1 video accepted, 1/1 frame accepted, 0 dropped

Adversarial media verification pass on `03_images/web/mount-maunganui-reef.json`, `02_research/videos/mount-maunganui-reef/videos.json`, and `03_images/video_frames/mount-maunganui-reef/`.

## Images

| # | URL | Verdict | Evidence | What I saw |
|---|---|---|---|---|
| 1 | raisedwaterresearch.com/.../Mount-Reef-Arial-1024x575.jpg | belongs | Source page is a dedicated Raised Water Research "spot" page for Mount Maunganui/Mount Reef, confirmed by WebFetch; image alt="Mount Reef Arial". curl -L 200, 84,545 bytes, JPEG 1024x575. Hotlink test (no referer): 200, image/jpeg. | Aerial photo of the Mount Maunganui / Mauao headland and curving beach with an arrow pointing to a spot offshore in the sea — geography (tombolo island connected to a sandy point, curving beach) matches Mount Maunganui exactly; arrow marks the reef's offshore location consistent with the dossier's "~250 m offshore" description. |
| 2 | raisedwaterresearch.com/.../Mount-Reef-Installed.jpg | belongs | Same source page; caption "The installed reef. Image: ASR" (ASR Ltd = the reef's own designer/contractor per dossier R2/R4). curl -L 200, 195,598 bytes, JPEG 570x519. Hotlink: 200, image/jpeg. | Yellow/olive-toned bathymetric or sonar-style image showing several long tubular shapes arranged in an angled cluster — matches the dossier's description of sand-filled geotextile containers/tubes forming a V-shaped or wedge structure. |
| 3 | raisedwaterresearch.com/.../Mount-Reef-Right-2-Mead-Borrero.jpg | belongs | Same source page; caption "Mount Reef Right. Image: Mead, Borrero" (Shaw Mead = ASR's own engineer quoted throughout the dossier). curl -L 200, 184,578 bytes, JPEG 548x411. Hotlink: 200, image/jpeg. | Sunset/golden-hour photo of a wave breaking with a surfer riding it, another person in the water beyond — generic surf-action photo; no landmark visible, but page context and named photo credit (Mead/Borrero, ASR-linked) tie it specifically to this reef rather than a stock/interchangeable wave shot. |
| 4 | raisedwaterresearch.com/.../Mount-Reef-Multibean-2007.jpg | belongs | Same source page; caption "Depth reading 2007, showing missing bag. Image: Scarf 2009" — a cited survey source specific to this reef. curl -L 200, 480,630 bytes, JPEG 637x752. Hotlink: 200, image/jpeg. | Colored bathymetric/multibeam survey with a north arrow, showing two rows of tubular structures in an angled arrangement consistent with the reef's geotextile containers, plus a scour depression to their west — matches dossier's "scour hole" and container-arrangement description. |
| 5 | raisedwaterresearch.com/.../Mount-Reef-Deflated-Bag.jpg | belongs | Same source page; caption "Damaged/deflated containers at the apex of the reef. Image: Dahm and Gibberd 2013" — matches dossier's cited 2013 condition survey. curl -L 200, 220,372 bytes, JPEG 541x471, hotlink: 200, image/jpeg. | Colored bathymetric scan of a similar tubular container cluster with an arrow pointing at the apex/junction — consistent with degradation documented in the dossier ("sand leaked from some bags"). |
| 6 (map) | google.com/maps/@-37.6471741,176.1986412,17z | belongs (map pin, not a photo) | Coordinates fall directly on the Tay St / Marine Parade stretch of Mount Maunganui Beach, matching the dossier's stated onshore reference point. Not fetched/downloaded (interactive map, not a static image file); kept as a map reference only, no hotlink/content-type test applicable. | N/A — map reference, not an image asset. |

All 5 photo/survey images: **belongs**. Confirmed by a dedicated WebFetch of the source page (raisedwaterresearch.com's Mount Maunganui spot page), which returned per-image alt text and captions naming "Mount Reef" and citing the same named surveys (Scarf 2009; Dahm and Gibberd 2013) and firm (ASR / Mead) that the verified dossier itself cites for these events. No image was dead, undersized, or mismatched in scene/geography. None dropped.

## Videos

| URL | Verdict | Evidence | What it shows |
|---|---|---|---|
| https://www.youtube.com/watch?v=QsyH6FEzDx4 | belongs | `python -m yt_dlp --dump-single-json --skip-download`: title "MOUNT REEF DREAM TURNS INTO REALITY!", uploader "fjsoto1", upload_date 2006-10-21, duration 346s. Description: "After a gruelling two week construction period installing the second half of the Mount Reef, the partially completed reef started to show its capabilities on Wednesday 4th October. A small 1.5 metre north-easterly swell generated awesome waves on the reef... fast hollow right hand barrels and up to 50 metre rides." Also links to the (now defunct) official project site mountreef.co.nz. | Title, description, and date (Oct 2006) directly match the dossier's construction timeline (second half of reef under construction through 2006, "nearly to specifications" by Oct 2006 per R2). No captions/subtitles exist on the video (music only, no dialogue), so transcript extraction is not possible — this is expected and does not affect the video-identity verdict, which rests on title/description/date. |

## Frames

| Path | Verdict | Evidence | What I saw |
|---|---|---|---|
| 03_images/video_frames/mount-maunganui-reef/QsyH6FEzDx4_0125.jpg | belongs | Frame extracted at 01:25 from the verified video above. | Low-resolution (428x240 source) frame showing open ocean, an overcast sky, a wave breaking in a line offshore, and one surfer/person waiting in the lineup near the wave. Matches the video's own description of surf breaking on the partially built reef structure — no landmark visible (expected for a wide-angle offshore surf shot), but frame content is consistent with (does not contradict) the confirmed video's subject matter. |

## Summary

- Images: 6 candidates in `03_images/web/mount-maunganui-reef.json` — 5 photo/survey images accepted (belongs), 1 Google Maps entry kept as a map reference (not a downloadable photo asset, not subject to the same image tests). 0 rejected.
- Videos: 1 candidate — accepted (belongs), full embed usable (not link-only).
- Frames: 1 candidate — accepted (belongs).
- Nothing moved to `images_rejected`; no frames deleted.
- Scratch copies (`img1.jpg`–`img5.jpg`, `vid.json`, `err.log`) downloaded to the session scratchpad for inspection and deleted afterward; none copied into the project folder.
