# Adversarial verification — Kovalam Reef (India) — Gemini-sourced candidate

Verified 2026-09-25. Assumption: guilty until the source proves otherwise.

## Reviews

| item | verdict | evidence | URL |
|---|---|---|---|
| Unnamed Kovalam fisherman quote: "We were told the reef would bring thousands of fish. Instead, our nets are torn to pieces on the plastic bags. We pull up shredded black plastic instead of fish." (outlet: "local Malayalam news report", 2012) | **REJECTED — fabricated/unverifiable citation** | The harness candidate carried no URL. Checked Gemini's own source files for a citation: Gemini's per-reef dossier (`02_world_reefs_data\kovalam-reef-india.md`, lines 99-100) attributes it only to "Kovalam artisanal fisherman, local Malayalam news report (2012)" — again no link. Gemini's structured data file (`02_world_reefs_data\world_reefs_master.json`, the `real_people_reviews` array for `kovalam-reef-india`) does carry a `url` field, but it resolves to `https://www.thehindu.com` — the bare homepage of The Hindu newspaper, not a specific article — paired with an invented `apa_citation`: "Artisanal Fisherman. (2012-08-14). Net snagging hazards on submerged Kovalam geotextiles. The Hindu." This is a fabricated-looking citation pattern (also seen on the same reef's other two reviews in that file, which cite bare `https://www.surfer.com` and `https://kovalamsurfclub.com` instead of specific article URLs — the latter site is a live Wix site, checked by HTTP HEAD, but nothing on it was findable for this quote either). Multiple targeted web searches (exact quote text, "Malayalam news" + reef + fishermen + 2012, "The Hindu" + "Net snagging hazards" + Kovalam, site:thehindu.com queries) returned no matching article, no Malayalam-press piece, and no independent source using this quote or attribution. No real, checkable source could be located anywhere on the open web. | none found (candidate URL empty; Gemini's own file points to `https://www.thehindu.com`, a non-specific homepage that does not contain this quote) |

## Refs
None supplied (candidate list was empty).

## Facts
None supplied (candidate list was empty).

## Contradictions
None supplied (candidate list was empty).

## Conclusion
The one candidate review does not survive verification and must **not** be added to our card. It traces back to a citation in Gemini's own `world_reefs_master.json` that names a real outlet (The Hindu) but links only to its homepage and supplies an invented-sounding article title/APA citation — a classic hallucinated-citation pattern, not a verifiable source. No independent trace of this quote exists elsewhere online. Our existing card's fisherman-related content ("local fishermen reported recovering damaged portions of the artificial reef rather than more fish," sourced to Raised Water Research [R1]) already covers the same real-world claim (nets/community harm) with a verified source, and is unaffected by this rejection — nothing changes on `kovalam-reef-india.json`.

No new references were appended (nothing to add with the next free R#), consistent with rejecting the only candidate.
