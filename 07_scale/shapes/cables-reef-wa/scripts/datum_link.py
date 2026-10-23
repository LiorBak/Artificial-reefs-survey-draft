"""cables-reef-wa: Fremantle chart datum (LWD) -> AHD link (assumption A12 / A1).  Run: python3 datum_link.py  -> datum_link.json
Inputs (all in ../src/datum/, copies of the sources listed in the json):
  DNM_TR12_Roelse_1975_excerpt_*.pdf   Table 3 (report p.36): Fremantle MSL 1966-68 above zero of staff gauge = 2.350 ft  (typed here; read off the page image 2026-10-13, text layer agrees)
  PSMSL_111_Fremantle_rlr_annual_*.txt annual RLR values (mm); data are relative to tide-gauge zero + 6.000 m (PSMSL RLR diagram text)
  ../scripts/shore_datum.json          BoM Fremantle MSL 1992-2011 (0.773 m above gauge zero), extremes
  ../3d/model.js                       validation.survey_check (RL minus AHD fitted on the design ramp, highest soundings)
"""
import json, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
FT = 0.3048                                                    # international foot, m
msl_6668_ft = 2.350                                            # DNM TR12 Table 3, Fremantle, NMV/F/6, epoch 1.1.1966-31.12.1968
msl_6668 = msl_6668_ft * FT                                    # m above staff-gauge zero = AHD 0.000 at this gauge
psmsl = {}
for l in open(HERE + '/../src/datum/PSMSL_111_Fremantle_rlr_annual_2026-10-13.txt'):
    a = l.split(';')
    if len(a) >= 2 and int(a[1]) != -99999: psmsl[int(a[0])] = (int(a[1]) - 6000) / 1000.0     # m above tide-gauge zero (RLR = TGZ + 6.000 m)
mean = lambda a, b: sum(psmsl[y] for y in range(a, b + 1) if y in psmsl) / len([y for y in range(a, b + 1) if y in psmsl])
SD = json.load(open(HERE + '/shore_datum.json'))
bom_msl = SD['BoM_Fremantle_MSL_above_gauge_zero_mean_of_annual_means_1992_2011_m']
js = open(HERE + '/../3d/model.js').read(); M = json.loads(js[js.index('window.REEF_MODEL = ') + len('window.REEF_MODEL = '):].rstrip().rstrip(';'))
sc = M['validation']['survey_check']
LWD_AHD = -msl_6668                                            # tide-gauge zero (= Fremantle LWD) in m AHD, national adjustment
METRO = 0.040                                                  # Landgate: Fremantle 1966-68 MSL vs 'State MSL' (1948), sign not known to us
out = {
 "about": "Fremantle Low Water Datum (LWD = tide-gauge zero) relative to AHD, from the datum definition itself (AHD 0.000 = MSL 1966-68 at 30 gauges incl. Fremantle).",
 "dnm_tr12_table3": {"station": "Fremantle", "tide_gauge_bench_mark": "NMV/F/6", "msl_1966_68_above_staff_gauge_zero_ft": msl_6668_ft, "msl_1966_68_above_staff_gauge_zero_m": round(msl_6668, 4), "bm_above_msl_ft": 10.659,
                     "epoch": "1 Jan 1966 - 31 Dec 1968", "location": "Roelse, Granger and Graham (1975) DNM Technical Report 12, 2nd ed., Table 3, report p.36 (PDF p.40); text 4.5.4 p.35"},
 "psmsl_check": {"definition": "PSMSL RLR = tide-gauge zero + 6.000 m (psmsl.org rlr.diagrams/111.php, 'Add 6.000m to all data values to refer to RLR')",
                 "annual_msl_above_TGZ_m": {str(y): round(psmsl[y], 3) for y in (1966, 1968) if y in psmsl}, "mean_1966_1968_available_years_m": round(mean(1966, 1968), 4),
                 "mean_1992_2011_m": round(mean(1992, 2011), 4), "bom_mean_1992_2011_m": bom_msl, "diff_1966_68_vs_DNM_m": round(mean(1966, 1968) - msl_6668, 4),
                 "reading": "staff-gauge zero of the 1966-68 survey = tide-gauge zero (= LWD) within 0.005 m; PSMSL and BoM 1992-2011 means agree within 0.002 m"},
 "result": {"LWD_in_m_AHD": round(LWD_AHD, 3), "AHD_above_LWD_m": round(msl_6668, 3), "metro_zone_ambiguity_m": METRO,
            "AHD_above_LWD_range_m": [round(msl_6668 - METRO, 3), round(msl_6668 + METRO, 3)],
            "present_MSL_1992_2011_minus_AHD_m": round(bom_msl - msl_6668, 3), "present_MSL_PSMSL_minus_AHD_m": round(mean(1992, 2011) - msl_6668, 3),
            "highest_recorded_m_AHD": round(SD['BoM_page_max_recorded_m'] - msl_6668, 3), "lowest_recorded_m_AHD": round(SD['BoM_page_min_recorded_m'] - msl_6668, 3),
            "highest_recorded_when": SD['BoM_page_max_when'], "lowest_recorded_when": SD['BoM_page_min_when']},
 "design_vs_survey": {k: {"fitted_RL_minus_AHD_m": sc[k]['ramp_offset_fit']['best_fit_RL_minus_AHD_m'], "sd_m": sc[k]['ramp_offset_fit']['sd_of_residual_m'], "n": sc[k]['ramp_offset_fit']['n_ramp_soundings'],
                          "official_minus_fitted_m": round(msl_6668 - sc[k]['ramp_offset_fit']['best_fit_RL_minus_AHD_m'], 3), "highest_sounding_AHD_m": sc[k]['survey_max_AHD'],
                          "design_crest_RL_-1.0_in_AHD_m": round(-1.0 - msl_6668, 3), "highest_sounding_above_design_crest_m": round(sc[k]['survey_max_AHD'] - (-1.0 - msl_6668), 3)} for k in sc},
 "reading_A_offset_old_m": 0.78, "reading_A_offset_new_m": round(msl_6668, 3),
 "old_0.78_source": "Pattiaratchi (1999) p.3: wave-basin 'mean tide level of 0.78 m above datum' (a present-day MSL, cf. BoM 1992-2011 0.773)",
}
json.dump(out, open(HERE + '/datum_link.json', 'w'), indent=1)
print(json.dumps(out['result'], indent=1)); print(json.dumps(out['design_vs_survey'], indent=1)); print(out['psmsl_check']['annual_msl_above_TGZ_m'], out['psmsl_check']['mean_1992_2011_m'], out['psmsl_check']['diff_1966_68_vs_DNM_m'])
