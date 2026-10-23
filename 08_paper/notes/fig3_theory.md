# Figure 3 theory check: surface landward of the break, and breaker shapes

Scope: checks the sketch in `08_paper/figures/fig3_wave_sketch.png` (code `08_paper/analysis/figures_wave.py`). Citations DOIs were checked against Crossref on 2026-10-19 unless marked "unverified".

## 1. Water surface landward of the break

**Instantaneous surface.** A breaking wave is peaked at the crest and flat in the trough. Near breaking, the crest stands about 0.6–0.65 H above still water and the trough about 0.35–0.4 H below it (second-order Stokes / cnoidal shape; Dean & Dalrymple 1991, ch. 4). So the trough behind the crest should dip to roughly -0.35 to -0.4 H_b below MSL, then rise again to the next crest or to the bore front. The current sketch's trough (about -0.6 m, i.e. about -0.4 H_b with H_b = 1.39 m) has the right depth, but it stays flat all the way to the shore. That is the error.

**Mean level (set-down and set-up).**
- Seaward of the break, radiation stress gives set-down. Longuet-Higgins & Stewart (1964) in the shallow-water limit give η̄_b ≈ -γ H_b/16 at the break point, i.e. about -0.05 H_b for γ ≈ 0.78. This is a few centimetres here, not the -0.6 m trough.
- Landward of the break, the mean level rises (set-up). Bowen, Inman & Simmons (1968) confirm set-down and set-up with measurements. Lior's estimate of a shoreline set-up of 0.2–0.3 H_b is the right order for a plane beach. **Unverified:** the exact coefficient; check Longuet-Higgins & Stewart (1964) before quoting a number.
- Over a submerged reef crest the mean level drops at the crest and then rises on the reef flat. Gourlay (1996) gives the reef-flat set-up. **Unverified:** the exact coefficients; read the paper before quoting.

**What a correct snapshot shows landward of the break:** (i) a trough about 0.35–0.4 H_b below MSL just behind the crest; (ii) the next crest or bore front, whose top sits above MSL; (iii) a mean level that dips slightly at the break (about -0.05 H_b) and then rises toward the shore, ending above 0 (set-up) at the shoreline. A single flat line at the trough level down to the shore is wrong.

## 2. Breaker shapes (Galvin 1968; Battjes 1974)

- **Surf similarity:** ξ = tanβ / √(H/L0). Battjes (1974) gives approximate limits: spilling below about 0.4, plunging about 0.4–2, surging/collapsing above about 2–3. Galvin (1968) classified the same breaker types from laboratory beaches. The figure's ξ_b = 0.56 (plunging) and 3.0 (collapsing) fall in the right classes.
- **Plunging (panel a):** The crest steepens, the front goes near-vertical, then the crest tip overturns into a thin lip that projects forward and falls into the trough ahead, trapping an air pocket. Lip thickness is a small fraction of H, roughly 0.1–0.2 H at its root (Peregrine 1983, review; **the 0.1–0.2 H figure is a typical range, not a measured value for this case**).
  - Onset (t0): crest sharpened and tilted forward, front near-vertical, lip beginning to curl, no foam yet.
  - t0 + 1 s: lip has reached the trough ahead, air pocket enclosed, white water at the impact point. For T = 10 s, 1 s is about T/10, so the impact is still in the early stage.
- **Surging / collapsing (panel b):** The front steepens but the crest does not overturn into a free jet. Surging: the base runs up the slope and little or no white water forms. Collapsing: the crest and front fall down the face from the bottom up, with a short or absent lip and only a small amount of foam. Both fit ξ above about 2.
  - Onset (t0): steep front, rounded crest, no overturning.
  - t0 + 1 s: the base has surged up the face, the crest is still a rounded hump, and the surface behind is a thin run-up sheet. Little or no lip.

## Sketch spec

- **Landward of the break, instantaneous surface:** the trough dips to about -0.35 to -0.4 H_b below MSL directly behind the crest (not a flat line). After it, the next crest or bore front rises above MSL. Keep the bore front about 0.2–0.4 H_b above the trough.
- **Landward, mean level:** dip about -0.05 H_b at the break, then rise steadily toward the shore; end above MSL (set-up, about 0.2–0.3 H_b on a plane beach; state "order-of-magnitude, unverified coefficient" in the caption).
- **Plunging lip thickness:** about 0.1–0.2 H_b at the root, tapering to a point at the tip.
- **Panel (a), two time steps:** t0 onset (crest sharpened, front near-vertical, lip starting) and t0 + 1 s (lip thrown into the trough ahead, air pocket, white water at impact).
- **Panel (b), two time steps:** t0 onset (steep front, no overturn) and t0 + 1 s (base surged up the face, no lip or a very short one, thin run-up sheet).
- **Caption:** say the mean-level shape is from set-down/set-up theory, and the lip shapes are schematic.

## References

- Bowen, A. J., Inman, D. L., & Simmons, V. P. (1968). Wave "set-down" and set-up. *Journal of Geophysical Research*, 73(8), 2569–2577. https://doi.org/10.1029/JB073i008p02569
- Battjes, J. A. (1974). Surf similarity. *Proceedings of the 14th International Conference on Coastal Engineering*, 466–480. https://doi.org/10.1061/9780872621138.029
- Dean, R. G., & Dalrymple, R. A. (1991). *Water wave mechanics for engineers and scientists*. World Scientific. https://doi.org/10.1142/1232
- Galvin, C. J. (1968). Breaker type classification on three laboratory beaches. *Journal of Geophysical Research*, 73(12), 3651–3659. https://doi.org/10.1029/JB073i012p03651
- Gourlay, M. R. (1996). Wave set-up on coral reefs. 1. Set-up and wave-generated flow on an idealised two dimensional horizontal reef. *Coastal Engineering*, 27(3–4), 161–193. https://doi.org/10.1016/0378-3839(96)00008-7
- Longuet-Higgins, M. S., & Stewart, R. W. (1964). Radiation stresses in water waves; a physical discussion, with applications. *Deep-Sea Research*, 11(4), 529–562. https://doi.org/10.1016/0011-7471(64)90001-4
- Longuet-Higgins, M. S., & Stewart, R. W. (1962). Radiation stress and mass transport in gravity waves, with application to "surf beats". *Journal of Fluid Mechanics*, 13(4), 481–504. https://doi.org/10.1017/S0022112062000877
- Peregrine, D. H. (1983). Breaking waves on beaches. *Annual Review of Fluid Mechanics*, 15, 149–178. https://doi.org/10.1146/annurev.fl.15.010183.001053
