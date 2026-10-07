# Media re-check — Kovalam Reef (Lighthouse Beach), India

Checked on 2026-09-25 against `02_research/reefs/kovalam-reef-india.json`.

**Headline finding:** all four raisedwaterresearch.com photo URLs that the card describes as showing the reef, its construction, or an underwater view of the structure actually serve **unrelated content** when opened. Lior's suspicion about the videos was correct, and it turns out to be worse for the images: none of the accepted media for this reef shows the structure or an unmistakable reef effect.

## Images

| # | URL | Card says it shows | What it actually shows | Verdict |
|---|-----|--------------------|-------------------------|---------|
| 1 | `Kovalam-Geomat-1024x543.jpg` | Workers handling a geotextile mat, construction-phase | A hand-drawn 1980 ink sketch titled "PETITION FOR ROCK REMOVAL" for an unrelated site called "Burkitts Reef" | **unrelated_or_wrong_site** |
| 2 | `Kovalam-Reef-Underwater1.jpg` | Underwater view of the submerged reef mound | An excavator and a man on a dark volcanic-boulder beach (dry land, not underwater) | **unrelated_or_wrong_site** |
| 3 | `Kovalam-Reef-Underwater2.jpg` | Underwater view with fish schooling over the mound | A backlit surfer riding a wave on a light-blue board; no water/fish/mound visible | **unrelated_or_wrong_site** |
| 4 | `ASR-beach-widening-1024x784.jpg` | ASR Ltd's Aug 2009 vs Aug 2010 before/after aerial beach-widening photos | A backlit surfer doing an aerial maneuver at sunset; no before/after or aerial-map content | **unrelated_or_wrong_site** |
| 5 | `Kovalam-Overview-Good-1024x512.jpg` | Aerial overview of the crescent beach, rocky headland, resort front | Aerial/drone shot of a crescent beach with a rocky point, resort buildings, swimmers, and one ambiguous whitewater patch offshore | **site_context_only** (plausible location match, but no confirmed reef-specific content; treat with reduced confidence since 4/5 sibling URLs on the same domain were mismatched) |
| 6 | Google Maps link | Satellite/map view near the reef's coordinates | Generic map/satellite tile, no reef annotation | **site_context_only** |

Method: each URL was downloaded with `curl -L -A "Mozilla/5.0"` into the session scratchpad, opened and viewed directly, then deleted. Image 1 initially failed to decode (corrupted/odd dimensions from the raw download); re-saving through PIL fixed the decode and revealed the actual (unrelated) sketch content.

### Follow-up flag
The dossier's `outcome` field states "the beach 'remained wider' in both monsoon and non-monsoon seasons after installation," attributed to the reef's own monitoring and illustrated by image #4. Since image #4 does not show any before/after or beach-widening content, this claim's image support is gone — the text claim itself should be re-checked directly against source R1's page text (not from the image) before the card is finalized.

## Videos

No videos were re-downloaded; classification is drawn from `02_research/videos/kovalam-reef-india/videos.json` and `videos.md`, which already record each video's title/description in full (no transcripts exist — `--write-auto-subs` was blocked by YouTube 429s per that file).

| Video | Title | Verdict | Evidence |
|---|---|---|---|
| E2_03-CkwGY | Surfing Kovalam Beach, South Indian Small, Fun Waves - GoPro Footage | **mentions_reef_briefly** | Uploader's own description: *"there is an artificial reef that really goes off when the swell is big enough."* But the 22s clip itself is silent GoPro selfie/whitewash footage with no visible structure — the reef is named only in text, never shown. **This is the video Lior flagged.** |
| X3NqayC1Iqc | Kovalam Surf Club social video | **site_only** | Thumbnail reads "MEET JELLE RIGOLE FROM BELGIUM" (ties to a named dossier source), but the clip itself is a generic social video with no confirmed reef footage or dialogue. **This is the second video Lior flagged.** |
| 6eSOn_m5Oz8 | Surfing - Water Sports in Kovalam, Kerala | **site_only** | Official Kerala tourism promo describing general wave heights/surf infrastructure; no mention of the reef structure. |

## Frames

`03_images/video_frames/kovalam-reef-india/` is empty. Per `videos.md`, one test frame extraction was done and deliberately discarded (showed only a surfer selfie and whitewash, not the reef). Nothing to classify.

## Hero recommendation

**None.** Nothing in the accepted media clears `structure_visible` or `reef_effect_visible`. If a hero image is still needed for scene-setting only, `Kovalam-Overview-Good-1024x512.jpg` is the least-bad option as generic beach context — but it must not be captioned as showing the reef, and its authenticity is itself only moderately confident given that 4 of the 5 sibling URLs on the same domain turned out to serve wrong content entirely.

## Recommended changes to the card

1. Remove images #1–4 above from `images[]` in `kovalam-reef-india.json`.
2. Re-caption image #5 as generic beach context only.
3. Re-verify the beach-widening claim in `outcome` directly from source R1's text (its image support is invalid).
4. Note in the reef's media/QA notes that no verified image or video shows the structure itself or an unmistakable reef effect — only the surrounding beach/surf site.

## Note on scope

This session's assigned task was the strict media re-check for `kovalam-reef-india` only. The separate request to check Gemini's scale-comparison figures (per `image26.png` style, in `C:\Users\lior\Documents\Gemini\AG\artifical reef\`) across all reefs was not addressed in this run — it is a distinct, larger task that was not part of the computed task text handed to this subagent.
