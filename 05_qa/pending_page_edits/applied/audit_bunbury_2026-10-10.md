# Bunbury source audit 2026-10-10: page edits for the page agent (04_build/data) and a card fix
Details: 07_scale/shapes/bunbury-airwave/SOURCE_AUDIT_2026-10-10.md.
- models3d_curated.json /models/bunbury-airwave/state_short:
  old: "As installed, December 2019: 12 m sand-slurry bladder, torn along a glued seam before completion (card verdict FAILED). Geometry only; it never operated as a reef. Removal, redesign and the 2025 granite proposal are not modelled."
  new (orchestrator, adds Troy's account; "never operated" conflicts with it): "As installed, December 2019: 12 m rubber bladder with a sand-slurry fill (press also mentions air; the developer says the final design used sand instead of air), failed along a glued seam (card verdict FAILED). The developer reports perfect waves for a couple of days before the seam opened; no independent confirmation. Geometry only. Removal, redesign and the 2025 granite / concrete plans are not modelled."
- models3d_caveats.json, new optional row: "Fill type: sources disagree (ABC 'air'; Tracks 'sand + air'; developer interview 'sand instead of air'); the model draws no fill. See METHODS_3D 2.2."
- CARD FIX (also affects the Google Maps link): card lat/lon (-33.31, 115.64) is ~2 km from the traced site (-33.3276, 115.6284; 07_scale/shapes/bunbury-airwave). Use the traced site for the Maps link and correct the card (cards agent / main).
