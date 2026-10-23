# Sand fill, dredging and geotextile container costs, and Narrowneck 2018 renewal (checked 2026-10-20)

Scope: Q1 unit costs of hydraulic dredging, sand placement and sand-filled containers, and how they fall with volume; Q2 the Narrowneck 2017-18 renewal per m3. Read-only check; nothing in the repo was changed except this note.

Access: WebFetch could not resolve most hosts (DNS). Downloads through the agent proxy with curl worked for two government PDFs (saved in the session scratchpad, not the repo). Search-only items are marked. IADC, USACE, Deltares, CIRIA and the Linham et al. (2010) paper itself were NOT reached.

## 1. Unit costs

**Q1a. Large-project sand and dredging rates (Australian, reputable: government-commissioned review).**
- WRL Research Report 263, Carley and Cox (2017), *Guidelines for Sand Nourishment: Science and Synthesis for NSW*, Oct 2017, section 6.1.1. URL: https://www.environment.nsw.gov.au/sites/default/files/sand-nourishment-guidelines-science-synthesis-nsw.pdf (read via curl; text extracted).
  - Quote: "all-inclusive unit rates for placed nourishment sand range from $5 to $50 per cubic metre in Australia. If a single rate is required ... Dredging offshore: $20 per cubic metre (noting that costs could be as high as $50 cubic metre)." (AUD, 2017.)
  - Section 6.1.2, Moses and Ling (2010) for NSW projects, AUD/m3 by volume class: "Major: 60,000 m3: $10 to $13"; "Medium: 30,000 m3: $13 to $17"; "Minor: 20,000 m3: $15 to $20". Components: dredge and load barges $3/m3; deliver to stockpile $3/m3; final shaping $2/m3. These exclude some transport and placement costs.
  - Section 6.1.5, Linham et al. (2010), worldwide survey of ten developed countries: "2010 US$4.09 to US$7.40 per m3" as averages, i.e. 2016 AUD 6.40-11.50; individual actual costs ranged 2009 US$3.0 to US$73 per m3. IPCC CZMS (1990) rates converted to AUD 10-20/m3 (2016), per WRL.
  - Section 6.1.3 (mobilisation, Pro Dredging 2013, Gold Coast, from Singapore): small TSHD (475 m3 hopper) bottom dumping $60,000; medium TSHD (5,800 m3 hopper) $3.8 M bottom dumping or rainbowing, $4.9 M pump ashore; large TSHD (11,600 m3 hopper) $5.6-6.7 M. AECOM (2010) hypothetical Sydney: $15 M; PBP (2006) Byron Bay: $4 M. Hopper capacity, not project volume.
  - Section 6.1.4 lists CIRIA (1996) factors: "Project size and consequent economies of scale"; distance between dredge and site; dredger size from borrow-area bathymetry.
- Greater Taree City Council, *Coastline Management Study, Appendix C* (Oct 2010), concept cost estimates, base date April 2010, excludes GST, design and approvals. URL: https://www.midcoast.nsw.gov.au/files/assets/public/v/1/document-resources/environment-docs/coastal-management/manning/coastline-management-study-appendix-c-oct-2010.pdf (curl after redirect; text extracted; a concept estimate, not a contract).
  - Dredge sand and stockpile: "m3 ... $10.00" (base case, AUD 2010) and "$40.00" in other scenarios (Old Bar cases).
  - "Mobilisation and demobilisation of dredge: Lump Sum $100,000.00" (AUD 2010), a fixed item in each estimate.

**Conversions (Table 1 method: nominal USD = AUD / World Bank annual FX; USD 2024 = nominal x US CPI 2024/year; from `08_paper/data/fx_worldbank.json`).**
- AUD 10/m3 (2010) = USD 9.17 nominal, USD 13.2 (2024). AUD 50/m3 (2010, trucked external sand) = USD 66 (2024).
- WRL 2017 range AUD 5-50/m3 = USD 4.9-49 (2024); AUD 10-20 = USD 9.8-19.6 (2024).

**Q1b. Geotextile sand containers filled in place.**
- Same Appendix C, Old Bar and Diamond Beach estimates (2010 AUD, ex GST): "Supply and placement of geobags ... $400.00" per bag, with the note "Assume 0.75 m3 containers and 2 side vandal deterrent"; "Supply and placement of geobags ... No. 2,500 ... $160.00" (Diamond Beach, "Assume single layer 0.75 m3 containers"); "Supply sand for geobags (external source) m3 ... $50.00" against "Dredge sand for geobags m3 ... $10.00" (PBP internal).
  - Implied: AUD 533/m3 of bag (400 / 0.75) = USD 704/m3 (2024); AUD 213/m3 (160 / 0.75) = about USD 282/m3 (2024). Bag supply and placement dominate; dredged sand is about 2-5% of the bag cost.
  - These are revetment or training-wall bags, not reef containers. No reef-container unit rate per m3 found in a primary source.
- Search-only: the coastal wiki page on artificial reefs says the cost of GSC reefs is "usually greater ... because of the difficult placement" (not reached; search summary only; https://www.coastalwiki.org/wiki/Artificial_reefs).

**Q1c. Scale.**
- Fixed mobilisation over volume: the Appendix C dredge mobilisation of AUD 100,000 adds AUD 1/m3 at 100,000 m3 and AUD 5/m3 at 20,000 m3 on top of the AUD 10/m3 dredged rate. Matches the NSW classes: AUD 10-13/m3 for 60,000 m3 vs AUD 15-20/m3 for 20,000 m3 (WRL, section 6.1.2).
- WRL section 6.1.4 cites CIRIA (1996) on economies of scale; WRL 6.1.3 says a large international dredger's mobilisation "will be a significant component" and is saved by sharing across projects.
- Search-only: Ecoshape (Dutch Holland Coast cost indicator, 2009 prices) says larger volumes use more cost-effective dredgers (https://www.ecoshape.org/app/uploads/sites/2/2020/06/1200893-000-ZKS-0004-v1.0-m-Inclusion-of-a-costs-indicator-in-the-interactive-design-tool-for-the-Holland-Coast-1.pdf; not fetched, DNS). Search-only: Wikipedia beach nourishment table gives Miami Beach 2017 about US$33.7/m3 and Myrtle Beach 1976 about US$18.4/m3 (secondary; not checked against sources).
- Not found: a quantified USACE or IADC unit-rate curve against volume.

**Verdict on Lior's 5-25+ USD/m3.** Consistent with the reputable sources: WRL gives AUD 5-50 (USD 5-49 in 2024) for all-inclusive placed sand in Australia, and AUD 20 (USD ~20) as a typical offshore dredged rate. Large-volume dredging (60,000 m3) sits at the low end (AUD 10-13 in 2017, about USD 8-10 in 2024 after conversion). No source gives a USD/m3 for hydraulic fill in a large reclamation project.

## 2. Narrowneck 2017-18 renewal

**What was done.** A renewal, not repairs only: 84 containers were added. Sources:
- Wikipedia, "Narrow Neck, Queensland" (accessed 2026-09-24; tertiary): "84 additional mega sand containers placed on the reef from a split-hull barge", renewal works finished June 2018. https://en.wikipedia.org/wiki/Narrow_Neck,_Queensland
- Raised Water Research (search summary only, page not read, 2026): the council voted in 2017 "to add 84 new bags meant to restore the crest to its original design depth"; refurbishment "roughly $2.1m AUD". https://raisedwaterresearch.com/spot/artificial-reef/unlocation/narrowneck/
- Swellnet, 7 Nov 2017 (card R2, read in an earlier session): remedial work from late 2017 to mid-2018 with a split-hull barge. https://www.swellnet.com/news/swellnet-dispatch/2017/11/07/narrowneck-artificial-reef-nears-completion-updated
- Repo claim, not re-verified here: `08_paper/sections/03_survey.md` l.37 cites "84 containers were renewed in 2017-18 [@blacka2013, pp. 97-98; @corbett2023]". Blacka (2013) is dated before the renewal, so the page citation needs checking before use.

**Cost.** The Inertia, 8 Sept 2017 (headline "$2 Million on Gold Coast Reef Renovation"; card R10; quote from Mayor Tom Tate): approx. AUD 2 M. Seabreeze (search summary): "$2 million would go toward the bags", but within a wider beach programme. The sum is not split by item (containers, crest, removal, survey).

**Volume.** 84 x 147 m3 = 12,348 m3. The 147 m3 per container is not published; it is the project's derived value (60,000 m3 / 408 containers, Jackson et al. 2007 Table 2 and p.4; 07_scale/shapes/narrowneck-gold-coast/HANDOFF.md, assumption A12). A published container size (20 m long, 3-4.5 m diameter) gives this order of magnitude but not a verified m3.

**Per m3.** Price year 2018 (renewal completed June 2018; Table 1 convention uses the construction or completion year). FX 2018 = 1.33841 AUD per USD (World Bank, `fx_worldbank.json`). CPI 2018 = 115.157; CPI 2024 = 143.857 (ratio 1.2492).
- AUD 2,000,000 / 12,348 m3 = AUD 162 per m3 (2018).
- USD nominal = USD 121 per m3 (2018); USD 2024 = **USD 151 per m3**. Whole renewal: USD 1.49 M nominal, USD 1.87 M (2024).
- Caveats: the AUD 2 M is a press figure ("approx."); it may include crest work, survey, removal of damaged bags and contingency, so the rate is an upper bound for placed sand; if some of the 84 bags replaced existing ones, net added volume is less and the rate higher. Not an audited final account.
- For comparison, the 1999 build AUD 2.3 M for 70,000 m3 gives USD 2024 about 2.79 M and USD 40/m3 (sand-fill basis). The renewal is about 3-4 times the original rate per m3, which is consistent with a 2018 contract for a small addition with mobilisation spread over few bags, plus repair work.

## Open items
- Narrowneck renewal contract or council report (breakdown: bags, crest, removal). City of Gold Coast council minutes 2017 (not reached).
- USACE or IADC unit-rate tables and the Linham et al. (2010) paper, if the paper needs a USD/m3 benchmark for large reclamation (not reached).
- Geotextile reef-container unit rate for a reef project (not found in primary sources).
