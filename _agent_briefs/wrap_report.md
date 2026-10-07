# Brief: documentation and the per-reef source report

1. 07_scale\SOURCES_AND_GEMINI_REPORT.md - per reef (all 13): primary source (kind, title, date, link), design version drawn and why,
   confidence + reason, overlay match, geo-referenced or not, and Gemini's sources with our verdict per source (correct / wrong site /
   wrong design version / number not in source / dead) and the evidence. A dedicated section "Reefs with no usable shape source" giving,
   per reef: what was searched, what Gemini used and whether it was wrong, and what the page shows instead.
   Read every 07_scale\shapes\<slug>\shape.json, METHOD.md and VERIFY.md.
2. Update 07_scale\README.md (new method: traced on real images, the tools, the spec, the confidence rubric, how to re-trace a reef) and
   07_scale\tools\README.md if needed.
3. 02_research\videos\INDEX.md - every video per reef with relevance, origin, transcript source, segment count, and the review workflow
   (Videos tab -> Export -> save media_decisions.json into 04_build\data\ -> rebuild).
4. Update 04_build\README.md and 05_qa\00_STATUS.md (2026-10-04: shapes traced on source images; Videos review tab; QA results from
   04_build\QA\round8_browser.md and round9 if present). Also list _agent_briefs\ in the root README.md as the record of agent instructions.

5. 07_scale\METHODS.md - a project-wide methods paper at academic level (added 2026-10-05 at Lior's request): Introduction and aims;
   Data (source types, provenance and licensing policy, Gemini handling - nothing used unless re-verified at source); Plan-shape
   reconstruction (image acquisition incl. Esri Wayback, tracing protocol with render-view-adjust, scale establishment, geo-referencing
   and the canonical frame with its equations, the geom.py rotation bug and its fix, cross-checks such as IoU and Hausdorff distance);
   Verification protocol (adversarial verifier, checks list); Confidence rubric and how each level was assigned; 3D modelling
   (bathymetry sources, datum handling with equations, reef surface construction, uncertainty propagation); Results summary table
   (all reefs: shape, dimensions, confidence and reason, 3D status); Limitations and unknowns (per reef, what is missing and what would
   resolve it); References (author-year). The page's Methods tab renders this file.

## Final answer (plain text, not JSON)
For EACH reef one line: slug | confidence | reason | primary source | Gemini verdict summary.
Then a "NO SOURCE" block with the full per-reef detail. Then video totals (by relevance and by origin).
