# Adversarial verification — Boscombe Surf Reef (Gemini-sourced candidates)

Verified 2026-09-25. Method: fetched each candidate's implied source (or, where Gemini gave no URL, searched for and fetched the best-matching primary/secondary source) and checked the claim against the actual page text. Assume-wrong-until-proven throughout.

## Reviews

| item | verdict | evidence | URL |
|---|---|---|---|
| Dr. Mark Davidson quote: "The wave length is rather too intense and challenging, and it is not quite as consistent as it should be... It met only 4 of the 11 design objectives." (Gemini outlet: "University of Plymouth evaluation report", May 2010, no URL given) | **CONFIRMED** (verbatim, via secondary reporting — no online copy of the primary Plymouth report itself was found) | Wikipedia's "Boscombe Surf Reef" article states, attributed to Dr. Mark Davidson of Plymouth University, May 2010: *"The wave length is rather too intense and challenging [and it] is not quite as consistent as it should be"* and separately *"the reef had only fully achieved four out of eleven of its design objectives."* thebreaker.co.uk independently corroborates the "4 of 11" figure ("it only met four out of 11 objectives") though its extracted text did not surface the wave-length sentence verbatim. Note: the exact wording Gemini gives concatenates two separate Davidson statements (wave-quality sentence + objectives-met sentence) into one quote via "..." — both halves are independently confirmed, but treat it as a paraphrase-splice rather than one continuous sentence in the source. | https://en.wikipedia.org/wiki/Boscombe_Surf_Reef (already R1 on our card); corroborating: https://www.thebreaker.co.uk/the-boscombe-surf-reef-what-went-wrong/ (already R2) |

This review is not new information for our card (the same quote and the same 4-of-11 finding are already woven into our card's `outcome` field, cited [R1][R2]), but it was not previously listed as a standalone entry in the card's `reviews` array. Recommend adding it there, attributed to Dr. Mark Davidson (University of Plymouth), sourced to R1/R2 — no new reference number needed.

## References

None submitted by Gemini for this reef (`"refs":[]`) — nothing to verify.

## Facts

| item | verdict | evidence | URL |
|---|---|---|---|
| "Boscombe reef reportedly met only 4 of 11 original design objectives per Davidson, Reeve & Medina 2010 (Univ. of Plymouth)." | **PARTIALLY CONFIRMED** — the "4 of 11" figure is confirmed; the "Reeve, D. & Medina, R." co-authorship is **NOT confirmed / rejected** | The "4 of 11" number is directly confirmed on Wikipedia and thebreaker.co.uk, both of which credit the May 2010 interim evaluation solely to **Dr. Mark Davidson** of the University of Plymouth — neither source, nor any other source found in a targeted search for "Boscombe surf reef Reeve Medina evaluation," mentions co-authors named Reeve or Medina. The one academic paper actually findable online that pairs Davidson with a co-author is Rendle & Davidson (2012), "An evaluation of the physical impact and structural integrity of a geotextile surf reef" (ICCE Proceedings) — a different, later paper (about structural/geotextile degradation, not the 11 design objectives) with a different co-author (Emma Jane Rendle, not Reeve or Medina). No trace of a "Davidson, Reeve & Medina 2010" report was found anywhere. This matches a fabricated-citation pattern also visible in Gemini's own per-reef dossier, which cites "Davidson, M., Reeve, D., & Medina, R. (2010). *Boscombe Surf Reef: Post-Construction Performance Evaluation and Physical Monitoring Report.*" with no URL and no corroborating trace online. | https://en.wikipedia.org/wiki/Boscombe_Surf_Reef ; https://www.thebreaker.co.uk/the-boscombe-surf-reef-what-went-wrong/ ; https://icce-ojs-tamu.tdl.org/icce/index.php/icce/article/view/6794 (Rendle & Davidson 2012, shows real co-author is Rendle, not Reeve/Medina) |

Recommendation: our card's existing "4 of 11" fact stands as-is (already correctly sourced [R1][R2], with no author names attached in our card's prose — good, since we never claimed "Reeve & Medina"). Do not adopt Gemini's "Davidson, Reeve & Medina 2010" citation string anywhere.

## Contradictions

| item | verdict | evidence | URL |
|---|---|---|---|
| Attribution of "nearest thing to an Atlantic roller [this side of Cornwall]" quote — ours: Paul Clark; Gemini: unnamed "Carve Surfing Magazine" editorial | **OURS IS CORRECT.** Gemini's alternative attribution is unconfirmed and appears fabricated. | Great British Life's article states verbatim: *"The reef promises the nearest thing to an Atlantic roller this side of Cornwall," says Bournemouth Surfing Centre's Paul Clark.* This exactly matches our card. A targeted search for the Carve Surfing Magazine version (including likely surrounding phrasing "white elephant" and "Kamikaze bodyboarder," both present verbatim in Gemini's own per-reef dossier) found nothing on carvemag.com or anywhere else — including checking a plausible Carve retrospective article ("Viva Bosvegas," carvemag.com, Nov 2022) directly, which turned out to be an unrelated one-line surf-check post with no mention of the reef, the £3.2M figure, or any such quote. No URL was ever given by Gemini for this attribution either, in the candidate or in its own dossier. | https://www.greatbritishlife.co.uk/homes-and-gardens/places-to-live/22630248.discover-boscombes-exciting-new-surf-reef/ (already R10 on our card) |

Recommendation: keep the card's sole attribution to Paul Clark; do not add or dual-attribute to Carve Surfing Magazine.

## Blocked

None — every candidate had a reachable source (or a reachable best-effort search target) within this pass.

## Summary of Gemini-survey reliability signal (for this reef)

Two of Gemini's four candidates for this reef trace back to citations that could not be corroborated anywhere on the open web: the "Davidson, Reeve & Medina 2010" report authorship, and the "Carve Surfing Magazine" editorial quote. Both appear in Gemini's own per-reef dossier without a URL. This is consistent with fabricated/hallucinated secondary detail layered on top of otherwise-correct core facts (the 4-of-11 finding and the general Davidson quote are both real). Treat any Gemini claim lacking a URL as unverified by default, per project rules.
