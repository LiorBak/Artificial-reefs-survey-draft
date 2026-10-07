# Adversarial verification — narrowneck-gold-coast (vs. Gemini survey)

Scope for this pass: **contradictions** only (Gemini candidates lists were empty for reviews/refs/facts — nothing else to check this round).

## Contradictions

| item | verdict | evidence | URL |
|---|---|---|---|
| "1971 study institution": ours = "Delft University of Technology" vs. Gemini = "Delft Hydraulics Laboratory (Netherlands)" | **OURS RIGHT — Gemini's claim is not supported by its own cited source.** Gemini cites `en.wikipedia.org/wiki/Narrow_Neck,_Queensland` as saying "Delft Hydraulics Laboratory." I fetched that exact page (both via WebFetch and raw `curl`, text extracted from the live HTML) and it does **not** say that anywhere. It says: *"In 1971 the Dutch University Delft completed a report for the Queensland Government recommending the construction of a groyne at Narrow Neck."* "Dutch University Delft" is the (slightly awkward, Dutch-word-order) English name for **Delft University of Technology** (TU Delft) — a university, not the separate Netherlands research institute "Delft Hydraulics" (WL \| Delft Hydraulics, now part of Deltares). Our card's existing reference R13 (`en.wikipedia.org/wiki/Gold_Coast_Shoreline_Management_Plan`) was also re-checked and contains the identical sentence/attribution ("Dutch University Delft"), confirming our card's wording, not Gemini's. | Live: https://en.wikipedia.org/wiki/Narrow_Neck,_Queensland ; https://en.wikipedia.org/wiki/Gold_Coast_Shoreline_Management_Plan (both fetched 2026-09-25) |

### Verbatim evidence (exact text pulled from the live Wikipedia page, raw HTML, stripped of tags)

> "...A 'mega sand container' at Narrow Neck in 1999. In 1971 the Dutch University Delft completed a report for the Queensland Government recommending the construction of a groyne at Narrow Neck. The Gold Coast City Council examined the idea of a groyne and instead constructed an artificial reef to stabilise the foreshore at Narrow Neck. So far the reef has worked well as a coastal control point, but has been disappointing in its secondary objective to improve..."

Same sentence (word-for-word) appears on the Gold Coast Shoreline Management Plan Wikipedia page.

No mention of "Delft Hydraulics," "Delft Hydraulics Laboratory," or "WL Delft Hydraulics" appears anywhere on either page. Gemini's contradiction candidate is rejected.

## Disposition

- **No change to our card.** `02_research/reefs/narrowneck-gold-coast.json` already says "1971 Delft University of Technology report" in the `motivation` field with references [R9][R13] — this is confirmed correct as written. No edit needed, no new reference number required (both R9 and R13 already exist and were re-verified against live sources).
- Gemini's competing claim ("Delft Hydraulics Laboratory (Netherlands)") is not supported by the very Wikipedia article it cites for that claim, and is not adopted.

## Candidates not actioned (none supplied this round)

- Reviews: none supplied by the harness for this reef in this pass.
- Refs: none supplied.
- Facts: none supplied.
- Blocked: none — both sources fetched live successfully, no archive.org fallback needed.

## Method note

Fetched `https://en.wikipedia.org/wiki/Narrow_Neck,_Queensland` twice, independently: (1) via WebFetch tool with a targeted extraction prompt, and (2) via raw `curl` to a local scratch file with HTML tags stripped and the surrounding ~550 characters printed directly, to rule out any summarization artifact from the WebFetch pass. Both methods returned the identical sentence. Also independently re-fetched `https://en.wikipedia.org/wiki/Gold_Coast_Shoreline_Management_Plan` (our own existing R13) via WebFetch and confirmed the same attribution.
