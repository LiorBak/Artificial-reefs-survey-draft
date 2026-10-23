# Paper: resume point (2026-10-19 ~14:45 UTC) - read this first after compaction

Goal: Lior's course paper (English, academic, ~15-20 pp + appendices, PDF). Plan and all decisions: `08_paper/PLAN.md`.
No revision round (Lior). No public web page now (Lior). Orchestrator commits and pushes; agents never run git.

## Done (committed)
- Data `08_paper/data/` (reefs.json, profiles/), literature `08_paper/lit/`, notes `08_paper/notes/` (israel, Netanya check = Ashkelon,
  Drimer model = Bar & Drimer 2023 only (2026 paper not found), sediment, materials, surf_outcomes, insights_in_literature).
- Analysis `08_paper/analysis/` (run_all.py; RESULTS.md, FINDINGS.md, SEABED_SEDIMENT.md, FIGURE_SPECS.md).
- Figures `08_paper/figures/` fig1-fig9 + figB + fig_sediment_* (png/pdf/caption.md).
- Sections `08_paper/sections/` 01-07 (+ .refs.md) and appendices A, C, D, appendix_refs_pending.md.

## Running now (Haiku agents, started 14:40 UTC)
1. Tide check -> `08_paper/notes/tides_check.md` (Lior suspects Bunbury/Cables/Albany/Narrowneck tide ranges in fig1 are wrong;
   note SW WA really is microtidal). If values WRONG: fix in 08_paper/data + profiles + figures_survey.py, re-run figure scripts.
2. Bar & Drimer cited papers download/OCR -> `05_qa/papers_intake/bar_drimer_cited/`, `08_paper/notes/bar_drimer_cited_papers.md`;
   its "Not downloadable - for Lior" list must be given to Lior in chat (full citations).
3. Rating evidence -> `08_paper/notes/rating_evidence.md`.

## Next steps (in order)
1. When 3 is done: propose to Lior a 3-criteria rating per reef for his review: (A) surf quality (shape/depth), (B) safety + longevity
   (materials, tears, injuries e.g. Albany), (C) other effects (sediment, storm protection). Lior's view: Albany is basically the only
   truly surfable (great quality, some injuries). After his OK, write it into the paper (table in section 3 or 8, and use it as the
   outcome measure in section 4 / FINDINGS where "outcome" ranks appear).
2. Run `_agent_briefs/workflows/paper_all_rest.js` from phase 'Assemble' (assemble = Opus: 08_discussion, 09_conclusions, 00_front,
   10_references merge, ORDER.txt, appendix_B_3d), then refcheck x2 (Haiku), then build-pdf (Sonnet) -> `08_paper/build/paper.pdf`.
   (Edit the script to skip the 'Figures' and 'Write' phases, which are done.) Include the rating and tide fixes before assembly.
3. Send Lior the PDF; commit/push.
Known small issues: FINDINGS item 4 needs the Borth H0=3 m exception (61.9 deg); refs missing in references.json (Rosen 2001,
van Steeg 2011, Mead 2000, Hudson 1959, Verhagen 2012, Barlow 2013); Appendix A.0 mentions AI agents - Lior to confirm.
