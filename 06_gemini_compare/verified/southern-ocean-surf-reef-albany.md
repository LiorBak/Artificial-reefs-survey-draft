# Adversarial verification — Southern Ocean Surf Reef, Albany (Gemini candidates)

Verified 2026-09-25. Assume-wrong-until-proven default applied to every candidate. Gemini's folder was only read, never modified: `C:\Users\lior\Documents\Gemini\AG\artifical reef\02_world_reefs_data\southern-ocean-surf-reef-albany.md`.

## Reviews

Gemini's candidate list passed to this task had `"reviews": []` — nothing to verify here from the harness payload.

However, Gemini's own per-reef markdown file (read for context) contains a "Real people & surfers reviews" section with a review that was **not** included in the harness's candidate list but is directly relevant to the contradiction below, so it is checked anyway:

| item | verdict | evidence | URL |
|---|---|---|---|
| Quote: "The Australian and WA governments backing this project with over $9 million showed incredible vision..." — attributed to "Albany Boardriders Club spokesperson (2025)" | **REJECTED — unverifiable / likely fabricated** | Gemini's own file gives **no URL** for this quote (unlike every other reference in the same file, which carries a live link). Two targeted web searches ("Albany Boardriders spokesperson over $9 million", and a general search for "$9 million" + Albany reef) turned up no outlet, transcript, or press release containing this sentence or anything close to it attributed to a Boardriders spokesperson. The only "$9 million" figure findable anywhere is an unrelated USD currency conversion of the AUD $13M total cost on a third-party site, not a government-funding figure and not a quote. Do not add this quote or attribute it to anyone. | none provided by Gemini; searches found no matching source |

## References

| item | verdict | evidence | URL |
|---|---|---|---|
| Albany Advertiser: "Eighteen rocks of Southern Ocean Surf Reef repositioned in successful bid to reduce user injuries" | **ACCEPTED (partial — headline/byline/date only; body still paywalled)** | Direct `curl` fetch (HTTP 200) and a Wayback Machine snapshot (`web.archive.org/web/20260517181036/...`, HTTP 200) both load the real page. Headline matches Gemini's citation verbatim: "Eighteen rocks of Southern Ocean Surf Reef repositioned in successful bid to reduce user injuries." Byline: Melissa Sheil, Albany Advertiser, **Wed, 11 March 2026, 4:00PM**. Full body is behind "Premium" subscriber paywall in both the live page and the archived snapshot — no article text, no cost figure, no cause detail beyond the headline itself is retrievable from any version. This matches (does not exceed) what our card's [R11] already states — no new facts to add beyond confirming the article is live, real, and correctly dated. | https://www.albanyadvertiser.com.au/news/albany-advertiser/eighteen-rocks-of-southern-ocean-surf-reef-repositioned-in-successful-bid-to-reduce-user-injuries-c-21896905 (archived: https://web.archive.org/web/20260517181036/https://www.albanyadvertiser.com.au/news/albany-advertiser/eighteen-rocks-of-southern-ocean-surf-reef-repositioned-in-successful-bid-to-reduce-user-injuries-c-21896905) |

## Facts

Harness candidate list passed `"facts": []` — nothing to verify.

## Contradictions

| item | verdict | evidence | URL |
|---|---|---|---|
| Total project cost/funding: our card's "AUD $11.75 million Total Committed Funds" vs. Gemini's review-quote claim of "over $9 million" government backing | **RESOLVED — not a real contradiction; the $9M figure comes from an unsourced/unverifiable quote, not a competing source.** Our $11.75M figure is directly from the City of Albany's own project page and is the sum of named tranches: Commonwealth $4.75M + WA State (DPIRD) $5M + City of Albany $1.995M + Albany Boardriders Club $5,000 = $11.75M. Web search independently corroborates the $4.75M (Cook/WA State) + $5M (Albanese/Federal) tranches. Combined *federal+state government* funding alone is $9.75M — so "over $9 million" would be arithmetically consistent **if** it referred only to federal+state contributions (excluding the City of Albany's own $1.995M, which is also government money, just local). But since the specific quote making this claim has no traceable source (see Reviews table above) and could not be found anywhere outside Gemini's own file, it should not be treated as a second, competing source at all — it is not corroborated, so there is nothing to "dispute." Recommendation: keep our card's sourced $11.75M / $13M range as-is; do not add the "$9 million" figure or attribute it to any government or Boardriders statement. | https://www.albany.wa.gov.au/council/projects/completed-projects/southern-ocean-surf-reef-sosr.aspx (our [R3]); cross-check search results citing $5M Federal + $4.75M WA State (e.g. https://www.wa.gov.au/government/media-statements/Cook%20Labor%20Government/-Albany-artificial-reef-project-making-waves-20250114 , https://minister.infrastructure.gov.au/c-king/media-release/albany-artificial-reef-makes-splash) |

## Net effect on our card

**No changes recommended to `02_research/reefs/southern-ocean-surf-reef-albany.json`.** Nothing from Gemini's survey for this reef clears the verification bar:

- The one REF candidate (Albany Advertiser 18-rocks article) is already in our card as [R11], with the same "body paywalled" caveat — confirmed live and correctly dated, but adds no new information.
- The review quote behind the "$9 million" contradiction could not be verified anywhere and should be treated as likely fabricated/hallucinated by Gemini — it is not appended as a new reference and the [R#] reference list is unchanged.
- No new [R#] references were added.
