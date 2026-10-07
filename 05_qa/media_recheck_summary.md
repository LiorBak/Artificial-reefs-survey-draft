# Media re-check summary — 2026-09-25

Source data: `05_qa/reef/<slug>_media_recheck.json` (+ matching `.md` report) for all 13
built artificial surf reefs, and the consolidated changes log
`05_qa/media_recheck_changes.md` (119 logged rows: kept/annotated/moved/hero-set actions
across images, videos, and video frames).

## Totals by verdict

**Images (68 checked across 13 reefs):**

| Verdict | Count |
|---|---|
| structure_visible | 34 |
| reef_effect_visible | 12 |
| site_context_only | 12 |
| unrelated_or_wrong_site (moved to `images_rejected`) | 7 |
| could_not_load | 3 |
| **Total** | **68** |

10 images were moved out of the rendered set entirely (`images_rejected`) per
`media_recheck_changes.md` — all 10 are the Kovalam Reef India batch that turned out, on
re-fetch, to be a different subject (Burkitts Reef petition sketch, an excavator on a
basalt boulder beach, and generic surfer shots with no tie to Kovalam's geotextile
mound).

**Videos (29 checked across 13 reefs):**

| Verdict | Count |
|---|---|
| about_the_reef | 11 |
| mentions_reef_briefly | 3 |
| unknown / embed_ok=False (not independently re-classifiable this pass) | 2 |
| unlabeled in the recheck JSON (see individual `.md` reports for the reasoning) | 13 |
| **Total** | **29** |

No videos were removed from the page; flagged ones render as link-only with a
"site context only" / "mentions briefly" label instead of an embedded player (per the
`04_build` "media labels" rule — see `04_build/README.md`).

## Images labelled "site context only" (12) — for Lior's review

These render on the page (not rejected) but are tagged as not showing the structure or
its effect — worth a quick look to confirm the label is fair:

1. **Borth coastal defence reef** — `geograph.org.uk/.../2554717...jpg` (construction-site fence sign, no reef visible)
2. **Bunbury Airwave** — `abc-cdn.net.au/0db449946b7b75c45d5bd9c51901a510` (pre-installation beach aerial, no bladder)
3. **Burkitts Reef (Bargara)** — a Google Maps *search* URL (not a real photo)
4. **Cables Reef (WA)** — `surfingdownsouth.com.au/.../1948-Surfing-Cable-Station...jpg` (1948 B&W photo, pre-reef)
5. **Cables Reef (WA)** — `surfingdownsouth.com.au/.../1957-City-Beach-BC-crew...jpg` (1957 B&W beach photo, no water)
6. **Kovalam Reef (India)** — `raisedwaterresearch.com/.../Kovalam-Overview-Good...jpg` (plausible but unconfirmed — flagged as possibly mislabeled given 4 sibling URLs on the same domain proved wrong-subject)
7. **Kovalam Reef (India)** — a Google Maps satellite-tile link (no reef annotation)
8. **Xala Reef (Mexico, 2026)** — `raisedwaterresearch.com/.../Reef2.jpg`
9. **Narrowneck Reef (Gold Coast)** — Wikimedia lifeguard-sign photo (matches card's own description, just not the structure)
10. **Opunake Surf Reef** — Wikimedia `Opunake_Beach.JPG` (general beach shot)
11. **Palm Beach Reef (Gold Coast)** — Squarespace CDN image (site/context)
12. **Pratte's Reef (El Segundo)** — `raisedwaterresearch.com/.../Prattes-Removal.jpg`

## Videos flagged (not "about_the_reef") — for Lior's review

18 videos across 10 reefs are flagged as briefly-mentions / unlabeled / unknown rather
than squarely about the reef (full reasoning for each is in the matching
`05_qa/reef/<slug>_media_recheck.md`):

| Reef | Video | Flag |
|---|---|---|
| Borth coastal defence reef | `youtube.com/watch?v=QUB6s_F9dZc` | mentions_reef_briefly |
| Borth coastal defence reef | `youtube.com/watch?v=dQieZVQUDEI` | mentions_reef_briefly |
| Boscombe Surf Reef | `youtube.com/watch?v=F0PslWKkbf4` | unlabeled (see report) |
| Boscombe Surf Reef | `youtube.com/watch?v=HeiYPXt85LM` | unlabeled — reclassified to "mentions_reef_briefly" on re-check (about the town's regeneration, not the structure) |
| Boscombe Surf Reef | `youtube.com/watch?v=7xMwL09a1TI` | unlabeled (metadata-only classification, medium confidence) |
| Boscombe Surf Reef | `youtube.com/watch?v=eceOTU06Dts` | unlabeled (metadata-only classification) |
| Bunbury Airwave | `abc.net.au/news/2019-12-16/11804314` | unlabeled (report classifies as about_the_reef; JSON field name mismatch — see note below) |
| Burkitts Reef (Bargara) | `youtube.com/watch?v=wuJ__7Js-cY` | unlabeled — frame already in `rejected/`, re-confirmed correctly excluded |
| Burkitts Reef (Bargara) | `youtube.com/watch?v=O3bEn8029XQ` | unlabeled |
| Kovalam Reef (India) | `youtube.com/watch?v=E2_03-CkwGY` | mentions_reef_briefly (text-only mention in description) |
| Kovalam Reef (India) | `youtube.com/watch?v=X3NqayC1Iqc` | embed_ok=False, unconfirmed tie to the reef |
| Kovalam Reef (India) | `youtube.com/watch?v=6eSOn_m5Oz8` | unlabeled |
| Narrowneck Reef (Gold Coast) | `youtube.com/shorts/xCLnKjvJ9r4` | unknown |
| Opunake Surf Reef | `youtube.com/watch?v=-xWlsZlffZY` | unlabeled — site-context-only, link-only rendering confirmed in round 6 QA |
| Opunake Surf Reef | `youtube.com/watch?v=cfiQvzgdGn0` | unlabeled |
| Opunake Surf Reef | `youtube.com/watch?v=GXYYCbZtz_s` | unlabeled |
| Palm Beach Reef (Gold Coast) | `youtube.com/watch?v=xWPl70kPFug` | mentions_reef_briefly |
| Southern Ocean Surf Reef (Albany) | `youtube.com/watch?v=6kwDBzf67EU` | unknown |

Note: most reefs' JSON uses the field `about` with values `about_the_reef` /
`mentions_reef_briefly`; a few entries have no `about` value set even where the matching
`.md` report gives a clear classification (e.g. Bunbury's ABC News clip is written up as
"about_the_reef" in prose but the JSON field is empty) — worth a small script pass to
backfill those JSON fields for consistency, flagged here rather than fixed silently.

## Changes already applied

`05_qa/media_recheck_changes.md` (119 rows) records every action taken during the
recheck: images kept with a shows= label, images moved to `images_rejected` (10, all
Kovalam), hero-image recommendations set per reef, videos kept/reclassified, and
individual video frames annotated (including two already-`rejected/` Burkitts frames
re-confirmed as correctly excluded). Applied to the cards via
`05_qa/apply_media_recheck.py`.

## What still needs Lior's eyes

- The 12 "site context only" images above (rendered but not showing the structure/effect
  — confirm the labels read right, especially #6, which is flagged as possibly the wrong
  photo).
- The 18 flagged videos above, particularly the ones with no clear `about` classification
  in the JSON (Boscombe ×3, Burkitts ×2, Kovalam ×2, Opunake ×2) — worth a listen/watch
  if time allows, since these render as plain links on the page either way and no
  further automated re-check will change that.
- No images or videos were permanently deleted from disk; `images_rejected` entries stay
  in the card JSON (excluded from rendering, not erased) so they can be re-reviewed.
