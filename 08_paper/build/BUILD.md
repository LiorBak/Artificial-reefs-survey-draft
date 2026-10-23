# Build of paper.pdf (LaTeX, APA 7)

## Current build: LaTeX (xelatex + biber, biblatex-apa)
Rebuild (from `08_paper/build/`): `python3 build_latex.py` (about 1 minute; output `paper.pdf`; work files and logs in the scratchpad
`.../scratchpad/latex/`, override with env `LATEX_WORK`). Needs xelatex, biber, pandoc 3.1.3 and the LaTeX packages already installed.
- Steps in `build_latex.py`: concatenate `../sections/ORDER.txt` (no `10_references.md`) -> pandoc `--biblatex` with `template.latex`
  (pandoc default minus the automatic bibliography), `latex_header.tex` and the Lua filter `tables.lua` -> `xelatex`, `biber`, `xelatex` x2.
  Under one "References" heading two lists are inserted before Appendix A (see "Two reference lists" below); a `\clearpage` precedes each appendix.
- `references.bib` (143 entries + 3 `skipbib` secondary sources) is written by `python3 md2bib.py` from `../sections/10_references.md`
  (heuristic parser; hand fixes in `bib_overrides.py`; keys like `hutt2001`, `mead2001a`, `raisedwaterndb`; key table in `citekeys.json`).
  Rerun `md2bib.py` only after editing 10_references.md, then rebuild. The `[not read]`-type notes are kept in the `addendum` field.
- In-text citations in the section files are pandoc/biblatex markup, written once by `python3 md2cite.py` (idempotent; plain-text originals
  in `sections_plain_backup/`): `[@key, p. 4]`, `@key` (narrative), `[@a; @b]`; groups that hold other text keep their parentheses and use
  raw `` `\cite[p. 4]{key}`{=latex} `` / `\citeyear`. 7 odd spots were converted by hand (Hutt et al. Figure 5 caption, possessives, Esri/LINZ-style aliases).
  Result: 585 citation items converted automatically; every key exists in the bib; all 143 listed works are cited.
  Check: `grep` the `.tex` for keys vs `references.bib` (done: none missing), `paper.log` has no undefined citation.
- Style: A4, 11 pt Latin Modern, 2.5 cm margins, hyperref colored links (dark blue), citations link to the reference entry, DOIs/URLs
  clickable, hanging indent 1.27 cm, sentence-case titles kept as written (`\DeclareCaseLangs{}`). Headings keep their typed numbers
  ("1 Introduction", "A.1"), so no LaTeX numbering. Captions are the Markdown ones ("Figure N."). `tables.lua` sets column widths from content,
  small type for wide tables and landscape pages for 8+ column tables with long content (Appendix C, Tables C1 and C3).
- Result: `paper.pdf`, 89 pages A4 = title pp. 1, contents pp. 2-4, main text Sections 1-9 pp. 5-40 (36 pages), References pp. 41-52 (12 pages),
  Appendices A-F pp. 53-89 (37 pages; B 66, C 67, D 77, E 82, F 87). 14 figures, no "??" or undefined citations, no Missing character.
  Greek in text is only phi and the dagger (taken from the math font by `newunicodechar`); Hebrew occurs only in URLs (percent-encoded).
- Old HTML build kept: `paper_html.pdf` (50 pages) from `build.py`. It is now outdated: the sections contain `[@key]` markup and
  `10_references.md` is no longer in ORDER.txt (the file itself is kept as the source of the bib).

### Known issues (LaTeX build)
- 89 pages against 50 in the HTML version (11 pt, 2.5 cm margins, long captions, reference notes kept); the main text is 36 pages (15-20 target).
- Reference list is generated from heuristic parsing: web pages without italics in the Markdown list are typeset by biblatex-apa as
  online items; the bracket notes appear after the entry as in the Markdown list. Check against `REFERENCE_ISSUES.md` before submission.
- "As cited in" citations print `(Pitt, 2009, as cited in Raised Water Research, 2019a)` through raw `\cite`; Shand 2011, Weppe et al. 2007 and
  Geofabrics 2013 are cited but, as APA 7 requires, not listed (`skipbib`, no link).
- Tables C1 and C3 are on landscape pages and leave white space at the end of those pages. Three or four table cells overrun the margin by 6-7 pt.
- Harmless log warnings: microtype "Unknown slot number" (8), hyperref `colorlinks` already used.
- Moores (2006) month "March-April" is in a note, not the date (biber cannot sort a non-numeric month).

## Previous build: HTML (outdated, see above)

Rebuild (from `08_paper/build/`): `python3 build.py` (no longer matches the sections: no citeproc, no reference list)
- Concatenates the files in `../sections/ORDER.txt` into `paper.md` (page break before References and Appendix A).
- pandoc: `paper.md -s --mathml --toc --toc-depth=2 --resource-path .. -c paper.css --embed-resources -o paper.html`.
- python playwright (`pip install playwright`, uses `/opt/pw-browsers/chromium-1194/chrome-linux/chrome --no-sandbox`) prints A4 with a page-number footer (`footerTemplate`). The plain Chrome flag `--no-pdf-header-footer` would remove the numbers.
- Style: `paper.css`. Figure numbers come from the captions in the section files (Figures 1-12 in text order; `fig8_stability.png` = Figure 11, `fig9_haifa_envelope.png` = Figure 12; Figure B1 in Appendix B).

Result: `paper.pdf`, 50 pages A4 = title and contents pp. 1-3 (abstract on p. 3), main text Sections 1-9 pp. 3-28 (about 26 pages, over the 15-20 target; no cuts made), References pp. 29-35, Appendices A-D pp. 36-50. 13 figures embedded (12 + B1), no raw Markdown or LaTeX found in the text layer.

## To confirm (Lior)
- Course name: the title page says "Coastal Engineering course paper" (placeholder in `sections/00_front.md`, `subtitle:`). Add course name/number/instructor.
- Abstract appears after the contents list (pandoc order); move if the instructor wants it before.
- Other open points: `../sections/OPEN_ISSUES.md`; reference problems: `REFERENCE_ISSUES.md`.

## Known issues
- Some white space below figures (figures are not split across pages).
- Main text is longer than the 15-20 page target (OPEN_ISSUES item 2 lists cut candidates).

- 2026-10-19: `thesurf2023` (Palm Beach video comments) was added by hand to references.bib. If md2bib.py is re-run, add it again or add it to 10_references.md first.

- 2026-10-20: four references added to `10_references.md` (elezovich2026, governmentof2025, surfline2025, 4surfers2025; group `other` in
  `ref_groups_new.csv`) and `md2bib.py` re-run: 154 entries (thesurf2023 is now generated from 10_references.md, no hand entry needed).
- Table footnotes: Table 1 uses pandoc notes `^[...]` inside cells. pandoc writes `\footnote` inside the longtable and the template's
  `\makesavenoteenv{longtable}` (footnotehyper) prints them at the foot of the page that holds the marker; if the table breaks across pages,
  each page carries its own notes. Keep the notes short so that Table 1 stays on one page (checked: p. 9, all 9 notes on that page).
  Landscape tables (C1, C3) carry their qualifications in the cells and in the "Notes to Tables C1-C5" instead.
- `latex_header.tex` loads `needspace`; Appendix G uses a raw `\Needspace{10\baselineskip}` before Table G3 to keep it on one page.
- Result 2026-10-20: 105 pages, no undefined citations.

## Two reference lists (grouping)
- `ref_groups.csv` (`key,group`, group = `academic` | `other`) covers every key in `references.bib`; `ref_groups_new.csv` (same format, written by
  other agents for appended entries) is re-read at each build and overrides. Edit these CSVs, never `references.bib`, to move an entry.
- `build_latex.py` writes a work copy of the bib with `keywords = {academic|other}` added to each entry; the source bib stays unchanged.
  It stops with a list if any bib key has no group (or a group other than academic/other).
- Back matter: `\section*{References}` then `\printbibliography[keyword=academic,heading=subbibintoc,title={Scholarly and technical sources}]`
  and `[keyword=other,...,title={Media, web and other non-academic sources}]`. Citation links still point to the entries.
- Group 1 = papers, conference papers, books, theses, technical/government/council/consultancy reports, official data sets, tide tables, standards.
  Group 2 = news and trade press, websites/blogs, company pages, YouTube, forum/social media, personal communications.
- Counts (at 2026-10-19): 147 keys = 99 academic + 48 other; listed (3 `skipbib` not printed) = 97 + 47.
- Doubtful, placed in group 2: pitt2009, zalul2025 (NGO appeal), mccp2026 (agency project list), cityof2023 (council FAQ), cityofnd (council web page),
  garminnavionicsnd (app chart), alvarez2006 (trade magazine). Doubtful, in group 1: rcahmw2020 (Coflein record), esrind (imagery), nationaltidalnd, verhagen2012 (lecture notes).

- 2026-10-20 (later): table captions are now set BELOW the tables in footnote size (`tables.lua`: the "**Table N.**" paragraph that
  precedes a table in the Markdown is moved after it, inside `\begingroup\footnotesize ... \endgroup` with `\nopagebreak`); figure
  captions stay below in footnote size (`latex_header.tex`). In the Markdown the caption paragraph still goes ABOVE the table.
  Wide tables (10+ columns): widths follow the body cells only (header words may wrap), cell notes `^[...]` are not counted, long
  left-aligned columns get 1.4x weight. Landscape tables use `\tabcolsep` 3.5 pt, `\arraystretch` 1.0 and script-size cell notes.
  Table 1 (13 columns, landscape) now fits on one page (p. 10) with its caption and its 10 notes.
- References added to `10_references.md` (group `other`, `ref_groups_new.csv`): theinertia2017, governmentof2024, internationalcoastal2025,
  southwestern2019. The Surf Eye video is now 2022 (key `thesurf2022`; `ref_groups.csv` and 08_discussion.md updated).
- Fig 12 (`fig9_haifa_envelope`) regenerated with `python3 ../analysis/figures_results.py fig9` (box 1.0-1.2 m; legend: built reefs geometry only).
- Result: 109 pages, no undefined citations.

## Captions and cross-reference links (2026-10-20)
- Captions: all figure and table captions are `\footnotesize` (9 pt at 11 pt body), label bold, below the float (`latex_header.tex` `\captionsetup`; table captions are set by `tables.lua`). `tables.lua` `Figure()` now estimates caption height at 9 pt and lets images use up to 85 % of the text height (was 75 %).
- `xref.lua` (new Pandoc Lua filter, runs before `tables.lua`, added in `build_latex.py`): links "Appendix X", "Appendix X.n", "Section X.n" and "Appendices A to F" (every listed letter) to the appendix headings (found from headings "Appendix X." / "X.n ..."), and "Figure N" / "Table N" (also E1, G3, ...) to the caption that begins "**Figure N.**" / "**Table N.**" (a `\hypertarget` is inserted there). Source Markdown is untouched. Headings, existing links and the caption labels themselves are not linked. Check: in PyMuPDF the links are kind 4 (named destinations `appendix-...`, `cap-Figure-1`).
- Run with `LATEX_WORK=<dir>` to build in a private work directory (default dir is shared with other agents).
