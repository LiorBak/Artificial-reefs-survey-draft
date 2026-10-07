# Palm Beach Reef — web image index

5 candidates found and verified (HTTP 200 + correct content-type via `curl -sI`). No Wikimedia Commons file found for this specific structure (searched "Palm Beach artificial reef Gold Coast" on Commons — no results, matching the dossier's own note).

| # | Kind | Depicts | Source page | Direct URL |
|---|---|---|---|---|
| 1 | photo | Aerial view of completed reef, boat for scale | ABC News (2022-09-03), photo "Supplied: City of Gold Coast" | https://live-production.wcms.abc-cdn.net.au/45b719e6a29fdb237a75b4f095d83fbf |
| 2 | photo | Aerial view of benefited area | Cru Collective blog | https://www.crucollective.com.au/wp-content/uploads/2019/10/Palm-Beach-Artificial-Reef-Completion.jpg |
| 3 | photo | Section view / rock sizing | Cru Collective blog | https://www.crucollective.com.au/wp-content/uploads/2019/10/Palm-Beach-Artificial-Reef-Completion2.jpg |
| 4 | photo | 2017 sand-nourishment/sandbar activity | Bluecoast Consulting Engineers artificial reefs page | https://images.squarespace-cdn.com/content/v1/5bfcd059e2ccd1869cf36e40/1600916522672-D4UT1B7FEQEBOCBBOQRI/image-asset.jpeg |
| 5 | map | Approx. onshore reference point (19th Ave, Palm Beach) | Google Maps | https://www.google.com/maps?q=-28.1120958,153.4567092 |

Notes:
- The best photo (#1) is the official City of Gold Coast aerial supplied to ABC News — likely the strongest candidate for the dossier's lead image.
- #2/#3 are unattributed on Cru Collective's own blog (a coastal engineering consultancy blog, not a stock source); treated as link-only, all-rights-reserved.
- #4 is not itself a reef photo — it documents the *companion 2017 sand-nourishment phase* at the same beach, included because Lior's dossier treats nourishment + reef as one project.
- No precise lat/lon for the submerged reef structure was found in any source (dossier itself flags this as unresolved). The map pin (#5) uses the approximate onshore coordinate for 19th Avenue, Palm Beach (from a hotel listing at that address), NOT the reef's true offshore position (~270-330 m out). Flagged clearly in the JSON entry.
- Swellnet's own site (multiple construction-era photo articles, e.g. https://www.swellnet.com/news/swellnet-dispatch/2019/08/23/watch-palm-beach-artificial-reef) returned HTTP 403 to the fetch tool (likely bot-blocking) and could not be indexed with direct image URLs in this pass — a later agent with browser access could revisit these.
- Hall Contracting's project page returned only a lazy-loaded SVG placeholder to the fetch tool — no usable direct image URL extracted.
- SkyEpics aerial-photography listings (two Palm Beach reef construction photos found via search) returned HTTP 403 to WebFetch — stock aerial photography, likely paid/licensed, not pursued further.

## References
R1. ABC News Australia (2022-09-03). "Millions spent to protect Gold Coast beaches, but climate change poses a huge challenge." https://www.abc.net.au/news/2022-09-03/gold-coast-no-stranger-to-beach-erosion/101381812 — accessed 2026-09-24 — supports: image #1, its caption and City of Gold Coast credit.
R2. Cru Collective (n.d.). "Palm Beach Artificial Reef Completion." https://www.crucollective.com.au/blog/palm-beach-artificial-reef-completion/ — accessed 2026-09-24 — supports: images #2 and #3, their captions.
R3. Bluecoast Consulting Engineers (n.d.). "Artificial reefs for coastal protection and surfing." https://www.bluecoastconsulting.com.au/artificialreefs — accessed 2026-09-24 — supports: image #4 and its 2017-nourishment context.
