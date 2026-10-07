# Boscombe Surf Reef — strict media re-check (2026-09-25)

Method: every accepted image was downloaded to a scratch temp dir (`curl -L -A "Mozilla/5.0"`), viewed directly, classified against the dossier's structure description, and the scratch copy deleted afterward. Videos were not downloaded — classified from `videos.json`, the two saved transcripts (read in full), and `yt-dlp --dump-single-json --skip-download` metadata for the two untranscribed videos. Both accepted frame files (outside `rejected/`) were viewed directly.

## Images

| # | URL | Classification | Evidence relied on |
|---|---|---|---|
| 1 | wavelengthmag.com/.../bournemouth-surf-reef.jpg | **structure_visible** | Viewed: sand-covered mound exposed above water behind beach fence, with the site's own "Surf reef" safety sign. Matches dossier's exposed-mound description. |
| 2 | raisedwaterresearch.com/.../Boscombe-Arial-1024x683.jpg | **structure_visible** | Viewed: aerial of pier/beach with a distinct dark rectangular submerged shape offshore, at the ~220–240 m distance and ~1 ha size the dossier states. |
| 3 | raisedwaterresearch.com/.../Boscombe-Exposed-1024x683.jpg | **structure_visible** | Viewed: two parallel rows of dark rounded humps (individual geotextile bags) breaking the surface with whitewater — matches dossier's 55-bag, 2–3 m-high, 60 m-long description. |
| 4 | raisedwaterresearch.com/.../Boscombe-Propeller-Damage-1024x768.jpg | **structure_visible** | Viewed: close-up of a torn geotextile bag edge with a hand touching it — matches the documented 2011 boat-propeller strike/torn-fabric narrative (R1, R9). |
| 5 | commons.wikimedia.org/.../Boscombe_Surf_Reef.jpg | **structure_visible** | Viewed: schematic cross-section diagram of stacked bags forming an angled ramp under breaking waves — matches "design_as_planned" description. |

**Result: all 5 accepted images confirmed structure_visible. No mis-tagged or off-site images found.**

## Videos

| Video | Classification | Best timestamp | Evidence |
|---|---|---|---|
| F0PslWKkbf4 — "Boscombe Surf Reef - The Story" | **about_the_reef** | 83s (01:23) | Full transcript read. Detailed construction narration: "made from a base layer a top layer and a ramp... webbing base and huge geotextile bags... largest bags were 70m long 2m high and 6m wide"; mechanism quote at 02:59 "it does not work like a wave machine... it mimics a natural reef by acting as a ramp." |
| HeiYPXt85LM — "Boscombe Surf Reef - the regeneration of Boscombe" | **mentions_reef_briefly** (downgraded) | 128s (02:08) | Full transcript read. This is a regeneration/interview piece about the town (rundown history, Overstrand development, beach pods, pier refit); the reef is repeatedly credited as catalyst ("it was a catalyst for all of this investment") but the structure itself is never described or shown. Downgraded from the card's implicit "about the reef" framing. |
| 7xMwL09a1TI — "the construction story so far" | **about_the_reef** (medium confidence) | 0s | Not transcribed; no saved frames. `yt-dlp` metadata: title only ("Boscombe Surf Reef the construction story so far"), description empty. Classification rests on the title alone. |
| eceOTU06Dts — "Boscombe Surf Reef in action November 2009" | **about_the_reef** | 8s | Not transcribed (no speech). `yt-dlp` description: "A few clips of the Bournemouth Surf Reef being used by body boarders one day after the official press launch... one of the biggest fiascos ever... wasting millions on a white elephant." Explicitly places the footage at the reef. |

## Frames

| Frame | Classification | Evidence |
|---|---|---|
| F0PslWKkbf4_0045.jpg | **site_context_only** (downgraded from card caption) | Viewed directly: this is the documentary's on-screen-labelled **"Before"** shot near the pier pilings — one surfer in calm water, unremarkable wave. Because it's explicitly the pre-reef baseline comparison frame, it cannot show reef effect by definition. Card caption should be corrected to note the "Before" label. |
| eceOTU06Dts_0018.jpg | **reef_effect_visible** (medium confidence) | Viewed directly: wave breaking with two figures near a pink and a yellow marker buoy. Classified on the strength of the video's own description ("Bournemouth Surf Reef being used by body boarders... one day after the official press launch"), not on visible landmarks in the frame alone — the frame by itself (wave + buoys) would not be identifiable as the reef without that source description. |

## Hero image recommendation

**raisedwaterresearch.com Boscombe-Arial-1024x683.jpg** — best single image for a reader unfamiliar with the site: pier, beach, town and the reef's submerged rectangular footprint all visible together at the correct scale/offshore distance. **Boscombe-Exposed-1024x683.jpg** (close-up bag rows) is a strong second choice for showing the physical structure itself.

## Summary

- All 5 images: confirmed clean (structure_visible), no changes needed.
- Videos: 1 confirmed about_the_reef with strong evidence; 1 downgraded to mentions_reef_briefly (was more about town regeneration than the structure); 2 remain about_the_reef but only on title/description metadata (not transcribed, limited/no frames) — flagged medium confidence, could be tightened later by transcribing or pulling more frames.
- Frames: 1 downgraded to site_context_only (it's the pre-reef "Before" shot, mislabeled by implication in the existing caption); 1 confirmed reef_effect_visible but only via the video description, not the frame's own visual content.

No unrelated_or_wrong_site or could_not_load items were found in this card's media.
