import sys; sys.path.insert(0, '/home/user/artificial-reef-survey/08_paper/data/src')
from common import *
SL = 'mexico-reef-2026-unnamed'
SH = '07_scale/shapes/mexico-reef-2026-unnamed/'
AL = dict(GLOBAL_ALIASES, RWR=r'Raised Water Research', THR=r'Hollywood Reporter')
def build():
    r = Reef(SL, AL)
    r.F('name', 'Xala Reef (Costalegre artificial surf reef), Jalisco, Mexico', 'text', 'S', 'THR', 'card name/place fields')
    r.F('country', 'Mexico', 'text', 'S', 'THR', 'card place field: Xala development, Costalegre coast, Jalisco')
    r.U('lat', 'deg N', 'location undisclosed; the area pin 19.71861, -105.23222 in the repo is NOT the reef (HANDOFF s3).')
    r.U('lon', 'deg E', 'as lat.')
    r.F('year_built', 2025, 'year (boulder surf break reported built by April 2025; "newly completed" 31 Mar 2026)', 'S', 'THR', 'card year field (R3, R4, R1)', note='Construction timeline unresolved (2025 vs 2026).')
    r.U('year_completed', 'year', 'described as "newly completed" in an announcement of 31 Mar 2026 (source framing, not verified).')
    r.F('purpose', 'multi', 'category', 'S', 'THR', 'card purpose: private surf break + coastal protection/beach restoration ("restore the beach, not flatten it")')
    r.F('material', 'quarried rock boulders ("3,000 truckloads")', 'text', 'S', 'THR', 'Hollywood Reporter 2025-04-22 (card R3)')
    for f, u in (('volume_m3', 'm3'), ('footprint_area_m2', 'm2'), ('plan_length_alongshore_m', 'm'), ('plan_length_crossshore_m', 'm'), ('reef_height_m', 'm'), ('crest_depth_msl_m', 'm below MSL'), ('crest_depth_lat_m', 'm below LAT'),
                 ('seabed_depth_toe_m', 'm below MSL'), ('seabed_depth_at_crest_m', 'm below MSL'), ('depth_gap_m', 'm'), ('seaward_ramp_length_m', 'm'), ('mean_seaward_slope', 'm/m'), ('distance_offshore_crest_m', 'm'),
                 ('tide_spring_range_m', 'm'), ('tide_mean_range_m', 'm'), ('swell_hs_m', 'm'), ('swell_tp_s', 's'), ('swell_dir', 'text'), ('arm_angle_to_shoreline_deg', 'deg'), ('arm_angle_to_swell_deg', 'deg'), ('surfable_days_per_year', 'days/yr'), ('sediment_shoreline_outcome', 'text')):
        r.U(f, u, 'not disclosed in any source found (no length, width, crest depth, volume, coordinates; no monitoring). Tides for Manzanillo (NOAA/UNAM) were not fetched.')
    r.F('design_wave', 'designed by S. B. Mortensen (DHI Seaport) for a high-performance surf break; no design parameters published', 'text', 'S', 'RWR', 'RWR announcement 2026-03-31 (card R1)')
    r.F('surf_outcome', 'unknown', 'category', 'S', 'RWR', 'card outcome field: no independent surf report or measurement; the location was withheld until a reveal event billed for 16 Apr 2026')
    r.F('durability', 'unknown: only announced March-April 2026', 'text', 'S', 'RWR', 'card outcome field')
    r.U('cost_local', 'local currency', 'not disclosed.')
    r.F('shape_on_page', 'hidden', 'category', 'S', None, '04_build/data/reefs.json footprint.display = False (read only); no shape.json (trace not possible)')
    r.F('model_3d', 'no', 'text', 'S', None, SH + 'HANDOFF.md / FEASIBILITY.md')
    return r
