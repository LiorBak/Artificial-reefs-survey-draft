import sys; sys.path.insert(0, '/home/user/artificial-reef-survey/08_paper/data/src')
from common import *
SL = 'palm-beach-gold-coast'
SH = '07_scale/shapes/palm-beach-gold-coast/'
AL = dict(GLOBAL_ALIASES, Mortensen2015=r'Mortensen, S\.B\.', Swellnet0729=r'Nettle, S\., Swellnet \(2019-07-29\)', Swellnet0823=r'Nettle, S\., Swellnet \(2019-08-23\)', ABC2022=r'ABC News Australia \(2022-09-03\)', ICM2024=r'Aaron Salyer', RWR=r'Raised Water Research \(n\.d\.\)\. "Palm Beach Reef',
          Prenzler=r'Prenzler', Inertia=r'The Inertia \(n\.d\.\)', CityGC=r'City of Gold Coast Open Data, Artificial Reef feature layer', Bluecoast=r'Bluecoast Consulting Engineers \(c\. 2020\)', Nav=r'Garmin Navionics')
def build():
    r = Reef(SL, AL); t = tr(SL)
    r.F('name', 'Palm Beach Reef (Palm Beach Artificial Reef), 19th Avenue, Palm Beach, Gold Coast, Queensland', 'text', 'S', 'ICM2024', 'card R13')
    r.F('country', 'Australia', 'text', 'S', 'ICM2024', 'card R13')
    r.F('lat', -28.107334, 'deg N (WGS84)', 'D', 'repo:' + SH + 'shape.json geo.centroid_latlon', 'centroid of the council/aerial outline; page status ok')
    r.F('lon', 153.470913, 'deg E (WGS84)', 'D', 'repo:' + SH + 'shape.json geo.centroid_latlon', 'as lat')
    r.F('year_built', 2019, 'year (construction Apr/May - Oct 2019)', 'S', 'ICM2024', 'card year field (R1, R3, R5): concept 2013, detailed design 2013-14, construction 2019')
    r.F('year_completed', 2019, 'year (finalised and certified Sept 2019)', 'S', 'ICM2024', 'card year field')
    r.F('purpose', 'multi', 'category', 'S', 'RWR', 'card purpose: (1) coastal-erosion protection, (2) surf amenity (right-hand wave, explicit in the brief), (3) habitat')
    r.F('material', 'quarried basalt/greenstone boulders (~60,000 t) as a rock mound', 'text', 'S', 'ICM2024', 'card size field (R2, R4-R7, R13)')
    r.F('volume_m3', 25000, 'm3 (quarried rock, as stated)', 'S', 'ICM2024', 'card size field: ~25,000 m3 / ~60,000 t', note='Stated value; 60,000 t / 25,000 m3 = 2.4 t/m3, a solid-rock density rather than bulk placed rock (1.6-1.8 t/m3), so tonnage and volume do not both hold (50,000-60,000 t at 1.7 t/m3 = 29,000-35,000 m3; LG Focus 2019: 50,000 t). Model rock envelope 22,020 m3 (16,537-28,010 for bed +-0.5 m; voids included, inferred; 3D); council register VOLUME 33,000 (units unknown); concept design 53,319 m3 (not the built reef).',
        alts=[(22020, '3D envelope (inferred)', 'D', 'repo:' + SH + '3d/METHODS_3D.md KN "Volume"', 'METHODS_3D'), (33000, 'council register, units unknown', 'S', 'CityGC', 'attribute VOLUME')])
    r.F('footprint_area_m2', 11972, 'm2 (toe outline)', 'D', 'repo:' + SH + 'shape.json canonical.area_m2 (Bluecoast/Nearmap aerial with survey contours + council polygon; IoU 0.995)', 'shape.json; METHODS_3D KN "Footprint"', alts=[(11942, 'council asset polygon (160 x 80 m nominal)', 'S', 'CityGC', 'OBJECTID 4638'), (21394, 'concept design 175 x 144 m (not built)', 'S', 'Mortensen2015', 'METHODS_3D KN')])
    r.F('plan_length_alongshore_m', 136.7, 'm', 'D', 'repo:' + SH + 'shape.json canonical.bbox_m.alongshore', 'shore-aligned bbox; oriented rectangle 162.3 x 91.3 m', alts=[(160, 'City: 160 m long', 'S', 'CityGC', 'asset polygon nominal')])
    r.F('plan_length_crossshore_m', 149.2, 'm', 'D', 'repo:' + SH + 'shape.json canonical.bbox_m.crossshore', 'shore-aligned bbox', alts=[(80, 'City: 80 m wide', 'S', 'CityGC', 'asset polygon nominal')])
    r.F('reef_height_m', 3.89, 'm (at the crest; max 4.17)', 'D', 'repo:' + SH + '3d/METHODS_3D.md KN "Reef height"', 'inferred from Navionics seabed and contour lines; council register HEIGHT_M = 5 (unit/reference not stated); +-0.5 m')
    r.F('crest_depth_msl_m', 1.5, 'm below MSL', 'S', 'ICM2024+Prenzler', '"The crest of the reef is 1.5 m below mean sea level" (Prenzler et al. 2022, via card R13/R24); concept "-1.5 m AHD" (Mortensen 2015); Navionics label "FISH HAVEN 1.5MT"', note='Crest slot 59.2 x 5.9 m; AHD vs MSL differs by 0.12 m (MSQ).')
    r.F('crest_depth_lat_m', 0.62, 'm below LAT', 'D', 'MSQ2026', 'LAT -0.88 m MSL (MSQ Gold Coast Seaway planes); crest 1.5 m below MSL -> 0.62 m below LAT (card: 60 cm at LAT)')
    r.F('seabed_depth_toe_m', round(t['toe_depth'], 2), 'm below MSL', 'D', 'repo:' + SH + '3d/model.js reef grid + seabed grid (derive_others.py)', 'bed at the seaward-most reef cell on the crest transect (y = %.0f m)' % t['y_toe'],
        note='Seabed from the Garmin Navionics SonarChart (datum assumed LAT, tested) and aerial contour lines; model toe -4.0 (landward end) to -7.0 m MSL (seaward end) +-0.5 m; no surveyed depth read. Median over columns %.2f m.' % med(SL, 'toe_depth')[0])
    r.F('seabed_depth_at_crest_m', round(t['bed_at_crest_edge'], 2), 'm below MSL', 'D', 'repo:' + SH + '3d/model.js seabed grid (derive_others.py)', 'bed under the seaward crest edge (y = %.0f m)' % t['y_crest_edge'])
    r.F('distance_offshore_crest_m', round(PROFILES[SL]['crest_cell_xy'][1], 0), 'm from the Esri 2025-12-01 waterline (MSL assumed)', 'D', 'repo:' + SH + '3d/model.js reef grid (derive_others.py)', 'y of the shallowest crest cell; toe nearest edge 225 m, centroid 305 m, farthest 374 m',
        alts=[(270, '~270 m offshore (most sources)', 'S', 'RWR', 'card size field'), (330, 'Royal HaskoningDHV', 'S', 'repo:Royal HaskoningDHV (n.d.) Palm Beach Shoreline Protection Project (card R5)', 'card size field')])
    sp, ne, mean = tide_stats(dict(MHWS=0.65, MHWN=0.36, MLWN=-0.37, MLWS=-0.66))
    r.F('tide_spring_range_m', sp, 'm', 'D', 'MSQ2026', 'Gold Coast Seaway standard-port planes 2026: MHWS +0.65, MLWS -0.66 m MSL (METHODS_3D)')
    r.F('tide_mean_range_m', mean, 'm', 'D', 'MSQ2026', 'mean of spring and neap ranges (neap %.2f m)' % ne)
    r.U('swell_hs_m', 'm', 'no wave-climate value recorded for Palm Beach in the repo; first test July 2019: 4-5 ft waves (Swellnet); at least double-overhead SE swells handled (Swellnet 2019-08-23). Same coast as Narrowneck (Blacka 2013: Hs 1.0 m, longshore drift ~500,000 m3/yr).')
    r.U('swell_tp_s', 's', 'not found.')
    r.F('swell_dir', 'south-east (SE) swell', 'text', 'S', 'Swellnet0823', 'card outcome field (R6, R15, R17)')
    r.F('design_wave', 'right-hand wave explicit in the design brief; concept design (Mortensen et al. 2015): crest orientation 105 deg, side-slope labels 1/12 and 1/5 (Fig 3); design Hs/Tp not recorded', 'text', 'S', 'Mortensen2015', 'Fig 3 labels (METHODS_3D KN "Side slopes")')
    r.F('arm_angle_to_shoreline_deg', 44.7, 'deg (toe outline long axis; crest slot 49.5; ICCE schematic 43.5)', 'D', 'repo:' + SH + 'shape.json angles', 'oriented bounding rectangle of the toe outline vs shoreline 154.3 deg (334.3)', note='Single rock mound; long axis ~45 deg to the shore (concept crest orientation 105 deg true).')
    r.U('arm_angle_to_swell_deg', 'deg', 'SE swell direction not quantified in the repo; shore-normal 64.3 deg true.')
    r.F('surf_outcome', 'works', 'category', 'S', 'Swellnet0823+Swellnet0729+Inertia', 'Swellnet 2019-07-29: July 2019 (reef ~50% built) broke 4-5 ft with rides up to ~30 m; at completion a consistent right plus a short thick left on bigger swells, handling at least double-overhead SE swells; The Inertia: "modest, measurable improvements"',
        note='No systematic surfable-days measurement found. Not yet judged long-term.')
    r.U('surfable_days_per_year', 'days/yr', 'not stated.')
    r.F('durability', 'stable structure with no significant movement or settlement (ICCE 2022 monitoring abstract, Prenzler et al.; monitoring papers to 2023); no damage or removal found', 'text', 'S', 'Prenzler', 'card status_now (abstract page only read; DOI/pages not confirmed)')
    r.F('sediment_shoreline_outcome', 'about 550,000 m3 of sand retained over the reef\'s first two years of operation (ABC News 2022); Watterson: compares favourably with nourishment over 30 years (journalistic, not a monitoring report)', 'text', 'S', 'ABC2022', 'card outcome field')
    r.F('cost_local', 18200000, 'AUD', 'S', 'ICM2024', 'card cost field (R2, R4, R7-R9, R12, R13, R16): AU$18.2 M (ICM comparison: AU$18.3 M)', price_year=2019, note='Project value announced at the launch (May 2019, HC2 contract); a reef-only contract value is not published; the 2017 phase-1 nourishment (470,000 m3) is a separate phase and not included.')
    r.f['cost_local']['currency'] = 'AUD'
    r.F('shape_on_page', 'shown', 'category', 'S', None, '04_build/data/reefs.json footprint.display = True (read only)')
    r.F('model_3d', 'yes: as built 2019 (inferred seabed and rock surface); confidence MEDIUM', 'text', 'S', None, SH + '3d/METHODS_3D.md s1, s6')
    r.profile_fields(SL, crest_primary=None, version_note='Crest = shallowest cell of the rock-surface grid (-1.5 m MSL, sourced). The surface is INFERRED from the aerial contour lines (interval assumed 0.5 m) and the Navionics seabed.')
    return r
