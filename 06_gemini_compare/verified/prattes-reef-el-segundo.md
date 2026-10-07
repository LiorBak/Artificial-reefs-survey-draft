# Adversarial verification — Pratte's Reef / Chevron Reef (El Segundo)

Source of candidates: Gemini survey (see harness task). Verified 2026-09-25.
Method: fetched the cited URL directly; Surfline blocks WebFetch/curl with a 403 (confirmed again below), and the Wayback Machine returns the capture as robots-excluded (404) even though its CDX index lists a 200 snapshot from 2023-06-04 — so the page was read live through the Claude Browser pane instead (same method our own card's `blocked_sources` note already used for this exact URL).

## Reviews

| item | verdict | evidence | URL |
|---|---|---|---|
| Review by "evan" — "Sounds like Surfrider should hire a new team of engineers, not a bunch of pencil pushers that don't know the first thing about surfing slabs." (Surfline comment thread, 2008) | **ACCEPT** (quote confirmed, minor wording fix, date/URL corrected) | Comment thread on the live Surfline article "SANDBAGGED" (fetched via browser pane) shows, verbatim: `evan 10/13/2008 04:36 PM — sounds like surfrider should hire a new team of engineers, not a bunch of pencil pushers that don't know the first thing about surfing slabs.` This is about Pratte's Reef specifically — it sits directly under the article's discussion of the reef's removal/failure, alongside the "Andrew" and "Randy Wright" comments already in our card. Gemini's version capitalizes "Sounds"; the page's actual text is lowercase "sounds" — use the page's wording. Gemini's candidate also mis-cited the outlet URL as bare `https://www.surfline.com` (homepage) instead of the specific article; the correct URL and exact date (2008-10-13, not just "2008") are below. | https://www.surfline.com/templates/article_html.cfm?n=2&id=19261&p=1 |

**Recommendation:** Add "evan" as a ninth entry in the card's `reviews` array (same style as the existing "Andrew"/"Randy Wright"/etc. Surfline-commenter rows), citing the existing **R7** reference (Fontaine, Evan, "SANDBAGGED," Surfline.com, 2008-10-11) — this is the same page as R7, not a new source, so no new reference number is needed. Suggested entry:

```json
{"who": "\"evan\"", "role": "Surfline commenter", "quote_or_summary": "\"sounds like surfrider should hire a new team of engineers, not a bunch of pencil pushers that don't know the first thing about surfing slabs.\"", "outlet": "Surfline.com comment thread", "date": "2008-10-13", "url": "https://www.surfline.com/templates/article_html.cfm?n=2&id=19261&p=1"}
```

(Per the harness's provenance convention, if this row is added it should be marked as originating "via Gemini survey, verified 2026-09-25.")

## Refs
None submitted for this reef in this batch.

## Facts
None submitted for this reef in this batch.

## Contradictions
None submitted for this reef in this batch.

## Notes on access
- Live fetch of `https://www.surfline.com/templates/article_html.cfm?n=2&id=19261&p=1` via WebFetch: **403 Forbidden** (consistent with the card's existing `blocked_sources` note for R7).
- Wayback Machine: CDX API confirms one snapshot (`20230604221124`, HTTP 200 at capture time), but every retrieval attempt (`/web/<ts>/…`, `/web/<ts>id_/…`, and the harness-suggested `/web/2026/…` redirect form) returned **404** with `exclusion.robots.policy` timing present in the response headers — i.e., Internet Archive is now honoring a robots.txt exclusion for this URL, so the archived copy is not servable even though it exists.
- Successfully read the live page content via the Claude Browser pane (renders client-side past whatever blocks WebFetch/curl), which is how the quote above was confirmed directly against the article's comment section (59 comments total, "evan"'s comment timestamped 10/13/2008 04:36 PM, positioned among the other named commenters already cited in the card as R7).
