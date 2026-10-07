# UPDATE_PROTOCOL - bringing the page up to date (04_build, written 2026-10-07)

ONE command, from `04_build\`:  `python src\update_page.py`   (`--fast` no Chrome check, 7 s; `--full` + all 162 DOM QA checks and screenshots, ~6 min;
`--force-export` re-export every combined mesh; `--dry` only say what changed). Exit 1 = build or check failed (the old page is in
`QA\prev\last_update\`). It never writes to 07_scale, 03_images or 02_research. Read its SUMMARY: "changed since the last update" lists every
area / volume / key number / picture count that moved; "!" lines say what is still missing for a new model.

## What it does (in order)
detect (signature per model: viewer, model.js, docs.js, annotated/, shape.json, picture registry, card, its config entries) -> backup page ->
compile_data.py -> build.py (re-copy viewers + pictures, prune stale copies, photo-match transforms when shape.json / model.js / registry changed,
re-export ONLY the combined meshes whose signature changed, fill `{{tokens}}` in curated text from model.js, verify snippets) -> check.py -> summary.

## You do nothing except run it when
- a model agent re-delivered `07_scale\shapes\<slug>\3d\` (index.html, model.js, docs.js, annotated\): copied and re-exported; versions come from model.js;
- the picture registry `03_images\reefs\<slug>\images.json` or a reef card `02_research\reefs\<slug>.json` changed (cards also feed the gallery text);
- a trace changed in `shape.json` (photo-match buttons and residuals follow).

## You edit one file first when
| change | edit | why |
|---|---|---|
| NEW model (has 3d\index.html + model.js) | `data\models3d_combined.json` (copy a similar entry: frame note, polygon expression, crest, hand), `data\models3d_curated.json` (key numbers, state_short), `data\models3d_caveats.json` | listed automatically, but without these it is "not in comparison" / auto numbers only |
| model not finished yet | add the slug to `data\models3d_hold.json` ("Not yet modelled") | stops half-written folders reaching the page |
| a caveat is fixed | its row in `data\models3d_caveats.json` (status `resolved`, new numbers, `{{tokens}}`) | rows are text; tokens `{{path\|fmt}}` are read from model.js |
| photo-match tolerance / Navionics log | `src\photo_match.py` (NAV_LOGS, TOL_*) | a capture log is only used when complete |
Pending updates, exactly what to touch: **Mount Maunganui bed** (default -3.6 m CD, later -2.8) = nothing, every bed number is a token; once the 2007
survey is in, set the caveat "as-built bed (ASSUMPTION)" to resolved. **Borth offshore fix**: caveat "Offshore seabed (y > 335 m) deeper than the Fig 2
-4.0 m contour" and key number "Seabed seaward of the reef" -> resolved text (the 0.89 m figure is typed there, not a token). **Boscombe flattening**:
check the key-number row for the extended seabed and the caveat "offshore alongshore tilt".

## After a run
`--full` once per real model change: view `QA\update_*.png` downscaled (photomatch_*, combined_oblique, versions_*) and read the FAIL lines.
Then log in `QA\round11_3d_LOG.md` (or the next round's log) and add one line to `05_qa\00_STATUS.md`.
Troubleshooting: "not in the vendored bundle" = the viewer imports a three.js module missing from `3d\vendor` (README there); "unresolved token" =
a `{{path}}` is not in model.js; combined check red = open `QA\build_log.txt` (each check prints got / ref / tolerance).
