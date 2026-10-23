# Lior's uploads "new uploads from lior/", intake index (2026-10-19)

Scope: every file in `new uploads from lior/` (his folder; nothing moved or renamed there). Compared with `papers/` and `05_qa/papers_intake/` by SHA-256, and PDFs by page count, metadata, first- and last-page text, and full-text word 8-gram overlap.

## 1. Duplicates

- Deleted: none. No file's SHA-256 matches another file in the upload folder, `papers/` or `05_qa/papers_intake/`.
- Kept as two versions (not a true duplicate): `DesigningaPreliminaryMultifunctionalArtificialReef.pdf` (11 pp., publisher-style Journal of Coastal Research copy) and `Voorde-DesigningPreliminaryMultifunctional-2009.pdf` (12 pp., JSTOR download copy). Same paper (ten Voorde et al. 2009, pp. 69-79). Page counts differ (11 vs 12), page-1 front matter differs, and about 78% of 8-word sequences are shared. Both are kept; the JSTOR copy is the one with Figure 14 on its p. 11 (journal p. 78).
- Not compared as PDFs (no PDF twin exists in the repo): the Albany and Raised Water Research web prints and the New Zealand Geographic print have OCR text in `albany_rwr_pdfs_ocr.md` and `nzgeo_moores_2006_artificial_surf_reefs_ocr.md`. These are derived text, not duplicates, so the PDFs are kept.

## 2. Identification, text layer and text files

| Upload file | Citation (APA) | Text layer | Text file |
|---|---|---|---|
| 105_Coastal_Structures_2019.pdf | Marrone, J., Zhou, S., Brashear, P., Howe, B., & Baker, S. (2019). Numerical and physical modeling to inform design of the LivingBreakwaters project, Staten Island, New York. In N. Goseberg & T. Schlurmann (Eds.), *Coastal Structures 2019* (pp. 1044-1054). Bundesanstalt fur Wasserbau. doi:10.18451/978-3-939230-64-9_105 | Yes, 12/12 pp. | `marrone_2019_livingbreakwaters_text.md` |
| Albany-Artificial-Surf-Reef-Community-Update-and-FAQs.pdf | Raised Water Research / Albany project team (2023, May). *Albany Artificial Surf Reef: Community update and FAQs* [project information sheet, 4 pp.]. No formal author line. | Yes, 4/4 pp. | `albany_asr_community_faq_2023_text.md` |
| Beach Profile Changes Due to Low Crested Breakwaters at Sigandu Beach.pdf | Sulaiman, D. M., Bachtiar, H., Taufiq, A., & Hermanto (2015). Beach profile changes due to low crested breakwaters at Sigandu Beach. *Procedia Engineering, 116*, 510-519. doi:10.1016/j.proeng.2015.08.320 | Yes, 10/10 pp. | `sulaiman_2015_sigandu_text.md` |
| Dabir_2020_IOP_Conf._Ser.__Earth_Environ._Sci._527_012004.pdf | Dabir, V., et al. (2020). Permeability of a composite seawall: Effect of the orientation of gaps in the structure. *IOP Conference Series: Earth and Environmental Science, 527*, 012004. doi:10.1088/1755-1315/527/1/012004 | Yes, 9/9 pp. | `dabir_2020_composite_seawall_text.md` |
| DesigningaPreliminaryMultifunctionalArtificialReef.pdf | ten Voorde, M., Antunes do Carmo, J. S., & Neves, M. G. (2009). Designing a preliminary multifunctional artificial reef to protect the Portuguese coast. *Journal of Coastal Research, 25*(1), 69-79. doi:10.2112/07-0827.1 | Yes, 11/11 pp. | `ten_voorde_2009_jcr_text.md` |
| Voorde-DesigningPreliminaryMultifunctional-2009.pdf | Same paper (JSTOR copy). Figure 14 is on p. 11 of this file. | Yes, 12/12 pp. | `ten_voorde_2009_jstor_text.md` |
| The multifunctional artificial reef and its role in the defence of the.pdf | López, I., Tinoco, H., Aragonés, L., & García-Barba, J. (2016). The multifunctional artificial reef and its role in the defence of the Mediterranean coast. *Science of the Total Environment, 550*, 910-923. doi:10.1016/j.scitotenv.2016.01.180 | Yes, 14/14 pp. | `lopez_2016_mediterranean_mfar_text.md` |
| Using Submerged Geotextile Tubes in the Protection of the E. Korean Shore.pdf | Oh, Y. I., & Shin, E. C. (2006). Using submerged geotextile tubes in the protection of the E. Korean shore. *Coastal Engineering, 53*, 879-895. doi:10.1016/j.coastaleng.2006.06.005 | Yes, 17/17 pp. | `oh_shin_2006_korea_geotube_text.md` |
| Opunake Artificial Reef monitoring programme 2005-2009.pdf | Taranaki Regional Council (2009). *Opunake Artificial Reef Monitoring Programme 2005-2009* (Technical Report 2009-33, Doc. 631513). Stratford: TRC. | Yes for 39/58 pp.; 11 image-only pages OCRed (tesseract, 200 dpi); 8 blank pages | `opunake_trc_2009_33_monitoring_text.md` |
| New Zyland Geographic.pdf | Moores, A. (2006). Artificial surf reefs: Coming to a beach near you. *New Zealand Geographic* (issue shown as Mar-Apr 2006 per card R3). | No (print of a web page). Already OCRed. | existing `05_qa/papers_intake/nzgeo_moores_2006_artificial_surf_reefs_ocr.md` (not redone) |
| 3 x https_*raisedwaterresearch / aisedwaterresearch PDFs (Albany) | Raised Water Research web pages (Midds Reef; Detailed design starts; More waves). Undated print-outs. | No (browser prints). Already OCRed. | existing `05_qa/papers_intake/albany_rwr_pdfs_ocr.md` (not redone) |
| WhatsApp Image 2026-10-08 at 14.28.06.jpeg | Not a paper. See section 4. | n/a | none (image registration pending) |

No OCR was needed beyond the Opunake image pages. Tesseract was already installed.

## 3. Five-line relevance summary per paper

1. **Marrone et al. (2019), LivingBreakwaters.** Cited in Bar and Drimer (2023) as [7]; now available. Partly submerged armour-stone and concrete breakwaters with habitat and wave attenuation goals; numerical and physical modelling of the design. Relevant to multifunction structures, not to surf-quality crests.
2. **Albany ASR FAQ (2023).** Community information sheet for the Albany (WA) artificial surf reef: why it is needed, what is planned. Useful for the community and consent side; not a technical paper.
3. **Sulaiman et al. (2015), Sigandu beach.** Cited as [23]; now available. Low-crested geotube breakwaters installed from 2014 at Sigandu (Central Java) after erosion caused by a port jetty; beach-profile changes measured. A geotube low-crested breakwater case, not a surf reef.
4. **Dabir et al. (2020), composite seawall.** Not cited in Bar and Drimer (2023); came up in the Chien DOI search. Study of the permeability of a composite seawall with gaps (per abstract). Not a reef; no relevance to surf reefs or geotubes beyond general porous-structure hydraulics. Noted only.
5. **ten Voorde et al. (2009), Portuguese coast.** Cited as [15]; now available in two versions. Designs a multifunctional submerged delta-shaped reef for surfing and shore protection; sets rules for shoreline response (Sa/SZW > 1.5), wave rays and slope. The main Haifa-relevant design paper in the upload set; Figure 14 read in section 5.
6. **López et al. (2016), Mediterranean MFAR.** Cited as [16]; now available. Multipurpose surfing reef at Babilonia beach, Guardamar (Spain), with sand accretion and shore defence goals; design and wave-climate study. Directly on the surf-reef topic.
7. **Oh and Shin (2006), E. Korea geotubes.** Cited as [21]; now available. Submerged double-lined geotube detached breakwaters for shore protection, with measured shoreline advance and later re-erosion. Lior judges it not a surf reef: keep as a geotube example in Appendix D.
8. **Taranaki Regional Council (2009), Opunake.** Not in Bar and Drimer (2023). Monitoring of the Opunake (NZ) surf reef, 2005-2009 (marine ecology, sediment, surf and consent conditions). Strong source for surf-reef monitoring design and outcomes.
9. **New Zealand Geographic (Moores 2006) and Raised Water Research prints (Albany).** Not PDFs with a text layer; OCR texts already exist in the intake folder. Popular and project-web sources; treat as secondary.
10. **WhatsApp image.** Not a paper. See section 4.

## 4. WhatsApp image (not moved)

`new uploads from lior/WhatsApp Image 2026-10-08 at 14.28.06.jpeg` (816 x 1056 px) is one page (p. 2-8) of a DRAFT report, "Western Australia, Reef Enhancement Modeling Study", Integral Consulting Inc., August 2022. It shows Figure 12, an artist's schematic of proposed reef modifications at Clam Reef, WA: a submerged new rock reef edge added to an existing reef, with the expected wave actions (new left- and right-hand waves, wave lines, "stand-up" zones and a previous break pattern). Credit on the figure: "shown by Roy Bothgal & Matt Jamieson, 2022". It is a surf-reef enhancement scheme, so it falls under the image rule: it must be registered in `_agent_briefs/image_registry.md` terms with citation, licence and use before it is shown on the page. Not done in this task.

## 5. Figure 14, ten Voorde et al. (2009)

- Location: JSTOR copy, PDF p. 11 = journal p. 78. Explanatory text on PDF p. 10 = journal p. 77 (section "Horizontal Dimensions").
- Exact caption: "Figure 14. Erosion for distance apex structure-coast of 100 m (left) and accretion for distance apex structure-coast of 250 m (right; Ranasinghe and Turner, 2006)."
- Parameters stated: distance from the apex of the structure to the shore, 100 m (erosion) and 250 m (accretion); test waves, peak period 10 s and significant wave height 1.5 m; model: numerical modelling (credited to Ranasinghe and Turner 2006); the paper gives no crest depth for this figure. Current arrows scale 1 m/s; depth bands from -1 m to below -9 m.
- Figure saved: `08_paper/lit/figs/ten_voorde_2009_fig14.png` (200 dpi crop, 1429 x 862 px).
- What it shows (read once): two plan views of depth bands with depth-averaged current vectors. Left (100 m): return-current cells at the structure carry flow offshore, away from the shore. Right (250 m): the return cells turn toward the shore, with a sheltered zone behind the apex where flow points at the shoreline. The paper's own text is about the mode of shoreline response (erosion vs accretion) set by Sa/SZW > 1.5, where Sa is the apex-to-shore distance and SZW the surf-zone width; the figure shows flow only, not sediment transport.
- Against Lior's reading (larger distance from shore keeps sand on the shore): the figure is consistent with it for the flow pattern, and the paper states the same for the shoreline response. The figure does not show sand volumes, so it supports the reading qualitatively only.
- Text for the Figure 14 paragraph is in `05_qa/papers_intake/ten_voorde_2009_jstor_text.md` (journal p. 77).

## 6. Open items

- Dabir et al. (2020) needs no action; it is not a Bar and Drimer citation.
- Two Bar and Drimer references remain unavailable: [8] Chien et al. (2014) and [24] Gouaud (2016). See `08_paper/notes/bar_drimer_cited_papers.md`.
- The WhatsApp image needs registration (section 4) if it is used on the page.
