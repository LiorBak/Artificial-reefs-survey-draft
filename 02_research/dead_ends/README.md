# Dead ends: sources checked that gave nothing useful (Lior, 2026-10-10)

One file per reef: `<slug>.json`. Purpose: future agents do not repeat a search that already failed.
These are NOT references; they never go into a card's `references` list. The page shows them per reef in a collapsed
"Checked, nothing useful (N)" section at the end of the reef dialog (closed by default).

Agents: append only (read the file, add your entries, write it back in one step). Before searching for something,
check this file first. Check `papers/` (Lior's PDFs) before any web search for a paper.

Format:
```json
{
  "slug": "opunake-reef",
  "entries": [
    {
      "what": "Black et al. 2004, Opunake reef resource-consent design study (ASR)",
      "kind": "paper | report | web page | imagery | chart | database | video | e-mail contact | search",
      "where": "URL, or the exact search string, or 'papers/ folder'",
      "checked": "2026-10-10",
      "by": "agent: Opunake with imagery (cloud)",
      "result": "not found | paywalled | login needed | bot check (not bypassed) | no plan or figure | imagery shows no structure | wrong site | broken link | other: ...",
      "detail": "one or two sentences: what exactly was looked at and why it did not help",
      "might_work": "what could still work (e.g. Lior via browser, e-mail to X, Google Earth Pro history) or ''"
    }
  ]
}
```
Partial yields (a source that gave one fact but not the needed one) are references for that fact; add a dead-end entry
only for the part that failed, and say so in `detail`.
