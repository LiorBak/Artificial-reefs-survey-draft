# Brief: ADVERSARIAL VERIFICATION + FIX of ONE traced reef shape (slug given in your prompt)

Try to prove the tracing wrong. Files: 07_scale\shapes\<slug>\shape.json, METHOD.md, sources.md, src\, overlays\.
Tools: 07_scale\tools\. Spec + confidence rubric: 07_scale\SHAPE_SPEC.md.

## Checks
1. VIEW every overlay PNG, then RE-RENDER the overlays yourself from shape.json (overlay.py render) and view them. Does each outline
   follow the structure / drawn outline on that image? Zoom where it matters. Rate overlay_match good / approximate / poor, with specifics.
2. Design version: open the sources. Is the drawn version the as-built / latest? Is there a later redesign, extension, damage or removal
   that changes the footprint (e.g. Narrowneck 2017-18 renewal, Cables southern extension, Mount Maunganui partial collapse, Boscombe
   damage and closure, Pratte's removal)? State which state the drawing represents; the page must say so.
3. Scale: re-check each image's px_per_m evidence (scale-bar ends, georef metres-per-pixel, the known dimension used). Recompute area,
   bbox, max dimension and angles with geom.py and compare with shape.json.
   TOOL BUG (found 2026-10-05): geom.py make-canonical / px_to_m rotated by +phi instead of -phi before it was fixed, so a canonical
   block made with it is wrong whenever the alongshore direction was not exactly (1,0). Check METHOD.md for its use; if used, recompute
   the canonical polygon with the fixed tool (or an explicit rotation) and confirm one known point by hand.
4. Dimensions vs text: agree within the rubric's tolerance? If not, which is wrong and why?
5. Provenance: every source has url, page/figure, date, credit; every number in METHOD.md has a source or a method.
6. Gemini findings: re-fetch the Gemini sources the tracer judged (both "correct" and "wrong") and confirm or overturn each verdict.
7. Confidence level and reason honest per the rubric.

FIX shape.json, METHOD.md and overlays in place (never invent; lower confidence rather than guess). Set "status": "verified",
"verified_on": "2026-10-04", and a "verification" array [{check, verdict, evidence}]. Write 07_scale\shapes\<slug>\VERIFY.md.

## Final JSON
{"slug","confidence","confidence_reason","primary_source","design_version","geo_referenced":bool,"dims",
"corrections":["..."],"overlay_match","gemini_findings":["source - verdict - evidence"],"no_source":bool,
"no_source_detail":"if no usable image: what was searched, what Gemini used and whether it was wrong, what the drawing falls back to"}
