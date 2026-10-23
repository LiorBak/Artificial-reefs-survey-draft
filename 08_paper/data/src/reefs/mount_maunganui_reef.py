import sys; sys.path.insert(0, '/home/user/artificial-reef-survey/08_paper/data/src')
from common import *
SL = 'mount-maunganui-reef'
SH = '07_scale/shapes/mount-maunganui-reef/'
AL = dict(GLOBAL_ALIASES, Focus2014=r'Focus Resource Management Group', Scarfe2008=r'Scarfe, B\.E\. \(2008\)', MeadBlackMoores2007=r'Mead, S\.T\., Black, K\.P\. and Moores, A\. \(2007\)', LINZ=r'Land Information New Zealand',
          RWR=r'Raised Water Research\. "Mount Maunganui', NZHerald_DeadZone=r"Stuck with a 'Dead Zone", Weppe=r'Weppe', MeadBlack1999=r'Mead, S\. and Black, K\. \(1999\)')
def build():
    r = Reef(SL, AL)
    r.F('name', 'Mount Maunganui Reef (Mount Reef), Mount Maunganui main beach, Bay of Plenty', 'text', 'S', 'Blacka2013', 'Appendix A.3 p.101')
    r.F('country', 'New Zealand', 'text', 'S', 'Blacka2013', 'Appendix A.3 p.101')
    r.F('lat', -37.644783, 'deg N (WGS84)', 'D', 'repo:' + SH + 'shape.json geo.centroid_latlon', 'centroid of the -2.0 m CD contour outline of the 18 Jul 2013 multibeam survey; same as the page')
    r.F('lon', 176.202591, 'deg E (WGS84)', 'D', 'repo:' + SH + 'shape.json geo.centroid_latlon', 'as lat')
    r.F('year_built', 2005, 'year (construction start)', 'S', 'Blacka2013', 'A.3.1 p.101: construction began 2005 (Nov 2005 per M&B p.3; card: Feb/Nov 2005, sources disagree)')
    r.F('year_completed', 2008, 'year (June 2008)', 'S', 'Blacka2013', 'A.3.1 p.101', note='Removed 25 Sep - Nov 2014 (resource consent lapsed 2010); remnant fabric still ashore Jan 2023 (card R12).')
    r.F('purpose', 'multi', 'category', 'S', 'MeadBlack1999', 'card R13 (surf primary, per designer) + Blacka Table 4.1 (protection secondary)', note='Surf primary per designer; coastal protection and amenity hoped for.')
    r.F('material', 'sand-filled geotextile containers (SFC), 24 containers built in two halves by the RAD method, filled sizes 30 x 1.5 x 1.0 m to 50 x 7.2 x 3.2 m', 'text', 'S', 'Blacka2013', 'A.3.3 p.102')
    r.F('volume_m3', 2800, 'm3 (as built)', 'S', 'MeadBorrero2011', 'p.3 Fig 3 (as-built survey 2,800 m3); repeated by Focus/BoPRC 2013 p.28', note='Design volume 6,500 m3 (M&B Fig 3 top; card 5,000-6,000). Model default: 2,945 m3 (outline) / 2,727 m3 (toe loft) at the assumed bed -3.6 m CD.',
        alts=[(6500, 'design volume (M&B 2011 Fig 3 top)', 'S', 'MeadBorrero2011', 'p.3'), (2945, '3D default version (assumed bed)', 'D', 'repo:' + SH + '3d/METHODS_3D.md KN', 'METHODS_3D')])
    r.F('footprint_area_m2', 1071, 'm2 (default: -2.0 m CD contour, 2013 multibeam)', 'D', 'repo:' + SH + 'shape.json canonical.area_m2 (-2.0 m CD contour of the 18 Jul 2013 multibeam survey, 5 bag polygons)', 'shape.json; METHODS_3D s1',
        alts=[(1424, 'as-built toe outline (ASR "Installed" survey image, 2008)', 'D', 'repo:' + SH + 'shape.json outline_versions', 'METHODS_3D s1'), (2400, '79 x 67 m at 70 % complete (Scarfe 2008; definition unstated)', 'S', 'Scarfe2008', 'METHODS_3D KN "Footprint"')])
    r.F('plan_length_alongshore_m', 67.9, 'm', 'D', 'repo:' + SH + 'shape.json canonical.bbox_m.alongshore', '', alts=[(90, 'published maximum longshore dimension', 'S', 'Blacka2013', 'Table 4.2 p.65')])
    r.F('plan_length_crossshore_m', 60.4, 'm', 'D', 'repo:' + SH + 'shape.json canonical.bbox_m.crossshore', '', alts=[(70, 'published maximum cross-shore dimension', 'S', 'Blacka2013', 'Table 4.2 p.65')])
    r.F('crest_depth_msl_m', 2.03, 'm below present MSL', 'D', 'Focus2014+LINZ', 'main bags 0.8-1.0 m below Chart Datum (BoPRC/Focus p6, p21); crest -0.9 m CD; z_MSL = z_CD - 1.13 (LINZ Tauranga) -> 2.03 m below MSL (METHODS_3D s3.1)',
        note='Deflated apex bags by 2013: -2.0 to -2.4 m CD (3.1-3.5 m below MSL). Blacka Table 4.2 submergence 0.4 m (datum not stated; may be as-built).',
        alts=[(1.93, 'crest -0.8 m CD', 'D', 'Focus2014+LINZ', 'METHODS_3D s3.2 crest options'), (2.13, 'crest -1.0 m CD', 'D', 'Focus2014+LINZ', 'METHODS_3D s3.2')])
    r.F('crest_depth_lat_m', 0.87, 'm below LAT', 'D', 'LINZ', 'LAT -1.16 m MSL (LINZ Tauranga standard port levels); crest 2.03 m below MSL -> 0.87 m below LAT')
    r.F('seabed_depth_toe_m', 4.73, 'm below MSL', 'A', 'Focus2014+MeadBlackMoores2007', 'ASSUMED as-built bed at the reef centre -3.6 m CD (= 4.73 m below MSL), Lior decision D1 2026-10-07; chosen to reproduce the stated 2,800 m3',
        note='No source states the 2008-09 bed. Evidence range: Oct 2006 survey beside the unfinished reef 2.0-3.7 m (CD assumed); BoPRC p23 3.0-4.0 m in 2008; ASR Installed ring -4.46 m CD; consent depth 3.7-4.6 m; 2013 survey -2.4 to -3.3 m CD; Navionics 2026 -2.76 m CD. Alternative "later seabed" -2.8 m CD = 3.93 m below MSL; Blacka depth 3.0-4.5 m. Bed slope 1:64 (Navionics 3-5 m).',
        alts=[(3.93, 'later seabed -2.8 m CD', 'A', 'repo:' + SH + '3d/METHODS_3D.md s3.3', 'METHODS_3D s3.3')])
    r.F('seabed_depth_at_crest_m', 4.73, 'm below MSL', 'A', 'Focus2014', 'same assumed bed (alongshore-uniform profile; the bed varies by < 0.1 m across the 5 m between toe and crest)')
    r.F('reef_height_m', 2.7, 'm (assumed bed -3.6 m CD; 1.9 m at -2.8 m CD)', 'A', 'repo:' + SH + '3d/METHODS_3D.md s1/KN', 'METHODS_3D KN "Reef height above the bed": maximum 2.85 m default version; Moores 2006 largest bags 3.5 m high x 50 m long')
    r.F('distance_offshore_crest_m', 307.7, 'm from the wet/dry-sand shoreline (Esri 2011-01-15)', 'D', 'repo:' + SH + '3d/METHODS_3D.md KN "Distance from the shoreline"', 'reef centroid 307.7 m; shoreline bearing 136.15 deg T',
        alts=[(257, 'Scarfe 2008 Table 8-3 (from the MSL line): 257-324 m', 'S', 'Scarfe2008', 'Table 8-3'), (250, 'published', 'S', 'Blacka2013', 'Table 4.2 p.65')])
    r.F('tide_spring_range_m', 1.75, 'm', 'D', 'LINZ', 'MHWS +0.83 - MLWS -0.92 m MSL (LINZ Tauranga; METHODS_3D s3.1 check "spring range 1.75")', alts=[(2.0, 'tide range as listed', 'S', 'Blacka2013', 'Table 4.3 p.67 (definition not stated)')])
    r.F('tide_mean_range_m', 1.42, 'm', 'D', 'LINZ', 'mean of spring (1.75) and neap (1.09) ranges: ((MHWS+MHWN)-(MLWS+MLWN))/2, MHWN +0.53, MLWN -0.56')
    r.F('swell_hs_m', 1.5, 'm (typical; basis not stated)', 'S', 'Blacka2013', 'Table 4.3 p.67 and A.3.1: H ~1.5 m, T ~11 s; longshore drift 60,000-80,000 m3/yr (variable direction)')
    r.F('swell_tp_s', 11, 's (typical)', 'S', 'Blacka2013', 'Table 4.3 p.67 / A.3.1')
    r.U('swell_dir', 'text', 'swell direction not confirmed in the sources read (open ocean beach, Bay of Plenty).')
    r.F('design_wave', 'designed with WBEND/3DD numerical models then a physical model; symmetrical "delta" with a wave-focusing zone (shallower gradient) and a wave-breaking zone (steeper gradient) for a single peaking wave', 'text', 'S', 'Blacka2013', 'A.3.2 p.102')
    r.F('arm_angle_to_shoreline_deg', [50.1, 54.9], 'deg (west/northern arm, south/long arm)', 'D', 'repo:' + SH + 'shape.json angles', 'west arm axis 86 deg T, south arm 11 deg T vs shoreline 136.15 deg T; apex angle 75 +-5 deg; V bisector within 2 deg of shore-normal')
    r.U('arm_angle_to_swell_deg', 'deg', 'swell direction not confirmed.')
    r.F('surf_outcome', 'works rarely', 'category', 'S', 'NZHerald_DeadZone+MeadBorrero2011+Blacka2013', 'M&B p.3; Blacka Table 4.1 (surfing "No", construction incomplete); card R7',
        note='Partly built reef (right-hander, late Oct 2006) "produced very good hollow waves" (M&B p.3), ride 20-40 m, but "three or four times since the surf reef was completed" (local surfer Derek Winter, NZ Herald, "pretty pathetic"); designer Shaw Mead: "over-sold and under-delivered". Reasons: incomplete construction (ruptured containers, unsealed ports, damaged container slump ~1 m lower crest), built ~50 m closer to shore than design, apex deflation.')
    r.U('surfable_days_per_year', 'days/yr', 'not stated; "three or four times" since completion (local surfer, ~2010).')
    r.F('durability', 'ruptured containers and sand loss during filling; one of the largest containers damaged beyond repair (gap 60 x 6 m, replaced ~9 months later; adjacent container slumped, crest ~1 m lower at offshore end); apex bags deflated to -2.0 to -2.4 m CD by 2013; buried base bags; reef removed 25 Sep - Nov 2014 (resource consent lapsed 2010)', 'text', 'S', 'MeadBorrero2011+Focus2014', 'M&B p.3; Blacka p.72; BoPRC/Focus 2013; METHODS_3D s1')
    r.F('sediment_shoreline_outcome', 'weak/disputed: Weppe et al. 2009 report ~25 m widening, influence ~150 m SE (via M&B p.5); the NSW review reads the same data as subtle (30 m accretion 100-200 m NW, no noticeable salient, maybe a slight groyne effect +-200 m) and rates protection "Negligible"', 'text', 'S', 'MeadBorrero2011+Blacka2013', 'M&B p.5; Blacka A.3.4 p.103; Table 4.1')
    r.F('cost_local', 1500000, 'NZD', 'S', 'RWR', 'card cost field (R2, R6, R7, R12): NZ$1.5 M', price_year=2008, currency='NZD', note='Price year ASSUMED 2008 (completion); sources do not state it. Blacka Table 4.4: AUD 1.53 M in 2013 AUD (AUD 545/m3).', alts=[(87000, 'removal cost (RWR); other sources ~NZ$60,000', 'S', 'RWR', 'card cost field')])
    r.F('shape_on_page', 'shown', 'category', 'S', None, '04_build/data/reefs.json footprint.display = True (read only)')
    r.F('model_3d', 'yes: as-built reef (2013 multibeam outline, assumed bed); confidence MEDIUM', 'text', 'S', None, SH + '3d/METHODS_3D.md s1, s6')
    r.F('depth_gap_m', 2.70, 'm', 'D', 'repo:' + SH + '3d/METHODS_3D.md s3.2-3.3', 'toe depth 4.73 (assumed bed) - crest depth 2.03 = 2.70 m (1.90 m at the "later seabed" option)')
    r.F('seaward_ramp_length_m', 5.1, 'm', 'D', 'repo:' + SH + '3d/METHODS_3D.md s3.2', 'ASSUMED 1:1 skirt from the bed (-3.6 m CD) to the -2.0 m CD contour = 1.6 m, plus the DEM-shaped rise from the contour to the crest -0.9 m CD over 3.5 m (RISE table, 2013 DEM) = 5.1 m',
        note='The DEM flanks are near vertical over the last 0.5-1 m (steeper than the 1:1 skirt). Hand calculation from the METHODS rules, not a grid extraction.')
    r.F('mean_seaward_slope', 0.53, 'm/m', 'D', 'repo:' + SH + '3d/METHODS_3D.md s3.2-3.3', '= 2.70 / 5.1 (1:1.9)')
    DEM = 'repo:' + SH + '3d/model.js survey2013 (18 Jul 2013 multibeam DEM, 1 m grid, m MSL) sampled by hand along x = -29 m (08_paper/data: transect printed in README s6)'
    for nm, v, lab in (('seabed_depth_toe_m', 4.26, 'bed 2013 (DEM) at y = 306 m on the transect x = -29 m, just seaward of the reef edge (2013 deflated state; bed y = 320-350 m: 3.9-4.3 m below MSL)'),
                       ('depth_gap_m', 2.95, '2013 DEM transect x = -29 m: toe 4.26 - highest DEM cell 1.29 m below MSL'), ('seaward_ramp_length_m', 12.0, '2013 DEM: crest at y = 294 m, bed reached at y = 306 m'), ('mean_seaward_slope', 0.25, '2013 DEM transect')):
        r.f[nm].setdefault('alternatives', []).append({'value': v, 'label': lab, 'status': 'derived', 'source': r.src(DEM), 'location': 'survey2013 grid x0 -75, y0 249, step 1 m'})
    return r
