import sys; sys.path.insert(0, '/home/user/artificial-reef-survey/08_paper/data/src')
from common import *
SL = 'borth-coastal-defence-reef'
SH = '07_scale/shapes/borth-coastal-defence-reef/'
AL = dict(GLOBAL_ALIASES, Haskoning=r'9V5090', LiDAR2022=r'Welsh Government \(2022\)', SMP2=r'West of Wales Shoreline Management Plan', NCE2011=r'Hansford', Coflein=r'Coflein', BorreroMead2010=r'Borrero, J\.C\. and Mead, S\.T\. \(2010\)', Stormrider=r'Stormrider', DailyPost=r'North Wales Live')
def build():
    r = Reef(SL, AL); t = tr(SL)
    r.F('name', 'Borth coastal defence reef (Phase 1: northern surf reef + southern oval breakwater, incl. Wallog headland), Ceredigion, Wales', 'text', 'S', 'Blacka2013', 'Table 4.2 p.66; Fig 4.1 p.72')
    r.F('country', 'United Kingdom (Wales)', 'text', 'S', 'Coflein', 'record NPRN 424699')
    r.F('lat', 52.483243, 'deg N (WGS84)', 'D', 'repo:' + SH + '3d/METHODS_3D.md / 04_build/data/reefs.json location (centre of the traced outline)', 'centre of the traced outline (Esri 2024 / LiDAR 2022); the page shows status ok')
    r.F('lon', -4.056157, 'deg E (WGS84)', 'D', 'repo:' + SH + '3d/METHODS_3D.md / 04_build/data/reefs.json location', 'as lat')
    r.F('year_built', 2011, 'year (construction start Jan 2011)', 'S', 'NCE2011', 'card year field (R1): construction started Jan 2011')
    r.F('year_completed', 2012, 'year (Phase 1 completed 8 March 2012)', 'S', 'Coflein+Blacka2013', 'Coflein NPRN 424699; Blacka p.70 (completed 2012)')
    r.F('purpose', 'multi', 'category', 'S', 'NCE2011', 'card purpose: primary flood/erosion protection of Borth village, secondary surf amenity (community rejected a sea wall)', note='Only the northern boot-shaped mound is shaped as a surf reef; the southern oval is a shore-parallel breakwater (METHODS_3D s1).')
    r.F('material', 'quarry rock armour: Type 4 (6-10 t) 42,000 t, Type 1 (3-6 t) 16,200 t, Type 3 (0.3-1 t) 18,500 t, Type 6 (5-100 kg) 500 t for the whole Phase 1 (275,000 t material incl. 84,500 t shingle); rock density 1.7 t/m3 in the model', 'text', 'S', 'NCE2011', 'card size field (R1)')
    r.F('volume_m3', 30119, 'm3 (rock, laser-survey edge, 3D default)', 'D', 'LiDAR2022+Haskoning', 'model rock volume +-4,600 m3 for 0.4 m bed error (METHODS_3D KN "Rock volume"); design foot 28,919 m3, photo edge 25,504 m3',
        note='No reef-only quantity at a primary source; 51,200 t at 1.7 t/m3 (+-15 %).', alts=[(28919, 'design rock foot (drawing 1020)', 'D', 'Haskoning', 'METHODS_3D KN'), (25504, 'visible rock edge in the Esri photo 17 Sep 2024', 'D', 'repo:' + SH + '3d/METHODS_3D.md KN', 'METHODS_3D KN')])
    r.F('footprint_area_m2', 5742.7, 'm2 (visible rock edge, Esri 17 Sep 2024; shape.json canonical)', 'D', 'repo:' + SH + 'shape.json canonical.area_m2', 'both mounds, canonical outline',
        alts=[(8675, 'laser-survey edge (LiDAR 19 Mar 2022, about -2.3 mODN), 3D default', 'D', 'LiDAR2022', 'METHODS_3D s1'), (6989, 'design rock foot (drawing 9V5090/1020)', 'D', 'Haskoning', 'METHODS_3D s1'),
              (12240, 'published 72 x 170 m (north) + 85 x 45 m (south) rectangles (DERIVED)', 'D', 'Blacka2013', 'Table 4.2 p.66')])
    r.F('plan_length_alongshore_m', 195.5, 'm (both mounds)', 'D', 'repo:' + SH + 'shape.json canonical.bbox_m.alongshore', 'x range -74.2..121.3 m', alts=[(170, 'north reef published "width" 170 m', 'S', 'Blacka2013', 'Table 4.2 p.66')])
    r.F('plan_length_crossshore_m', 140.0, 'm (both mounds)', 'D', 'repo:' + SH + 'shape.json canonical.bbox_m.crossshore', 'y range 257..397 m', alts=[(72, 'north reef published "length" 72 m', 'S', 'Blacka2013', 'Table 4.2 p.66')])
    r.F('reef_height_m', 4.5, 'm (north arm; oval about 5.5 m, +-0.5)', 'D', 'Haskoning', 'METHODS_3D KN "Height above the seabed": crest minus the modelled seabed')
    r.F('crest_depth_msl_m', -0.19, 'm below MSL (NEGATIVE = above MSL, emergent)', 'D', 'Haskoning', 'design drawings 1020-1023 rev C1: north arm crest +0.50 mODN; z_MSL = z_ODN - 0.31 (MSL = +0.31 mODN +-0.15, 4-level mean; METHODS_3D) -> +0.19 m above MSL',
        note='Tail +1.00 mODN (0.69 m above MSL); head edge 0.00 rising to +0.50 over ~40 m; oval breakwater +1.50 mODN (1.19 m above MSL). LiDAR DSM crest strips: north arm median +0.58 mODN, oval +1.55 mODN (LiDAR minus design +0.14 +-0.28 m). Blacka Table 4.2: submergence "at MSL".',
        alts=[(-0.69, 'north-arm tail +1.00 mODN', 'D', 'Haskoning', 'METHODS_3D KN'), (-1.19, 'oval breakwater +1.50 mODN', 'D', 'Haskoning', 'METHODS_3D KN')])
    r.F('crest_depth_lat_m', -2.94, 'm below LAT (NEGATIVE = above LAT)', 'D', 'SMP2', 'LAT -2.44 mODN (Barmouth, Fishguard; West of Wales SMP2); north arm crest +0.50 mODN is 2.94 m above LAT; drying at all but the high-water half of the tide')
    r.F('seabed_depth_toe_m', round(t['toe_depth'], 2), 'm below MSL', 'D', 'repo:' + SH + '3d/model.js seabed + default outline (derive_profiles.py)', 'bed at the seaward-most cell of the north mound on the crest transect',
        note='Design bed about -4.0 mODN under the north arm (beds "vary"); north foot -3.86 mODN mean (-4.05 to -2.51) = 3.55 m below MSL at the mean; seabed seaward of the reef follows the HRPP576 Fig 2 -4.0 m contour. Blacka: depth 4.0 m at MSL.')
    r.F('seabed_depth_at_crest_m', round(t['bed_at_crest_edge'], 2), 'm below MSL', 'D', 'repo:' + SH + '3d/model.js seabed (derive_profiles.py)', 'bed at the crest edge of the transect')
    r.F('distance_offshore_crest_m', 330.5, 'm (centroid of both mounds, from the defence line = back of the shingle beach)', 'D', 'repo:' + SH + 'shape.json canonical.distance_offshore_m / METHODS_3D KN', 'centroid 330.5 m; nearest edge 257 m, farthest 397 m; Esri +-5 m',
        note='Reference line is the defence line at the back of the shingle beach, NOT the MSL waterline.', alts=[(300, 'Coflein', 'S', 'Coflein', 'NPRN 424699'), (400, 'contractor (NCE 2011)', 'S', 'NCE2011', 'card size field'), (110, 'Blacka (north reef; probably to the undisturbed shoreline)', 'S', 'Blacka2013', 'Table 4.2 p.66')])
    r.F('tide_spring_range_m', 4.30, 'm', 'D', 'SMP2', 'MHWS +2.56 - MLWS -1.74 mODN (Aberystwyth, West of Wales SMP2 water-level table, p.4C.3); neap range 1.70 m', note='Card: spring range 4.7-4.8 m, high springs 5.4 m (tide-forecast site, tertiary); Blacka Table 4.3: "typical" 6.0 m (undefined).')
    r.F('tide_mean_range_m', 3.0, 'm', 'D', 'SMP2', 'mean of spring 4.30 and neap 1.70 ranges: ((MHWS+MHWN)-(MLWS+MLWN))/2 with MHWN +1.06, MLWN -0.64 mODN')
    r.U('swell_hs_m', 'm', 'no wave-climate value for Borth recorded in the repo sources read (Borrero & Mead 2010 surfing assessment report and HRPP576 not obtained).')
    r.U('swell_tp_s', 's', 'not found.')
    r.U('swell_dir', 'text', 'not found; west-facing bay (shore-normal bearing 269.6 deg true).')
    r.F('design_wave', 'surfing assessment by Borrero & Mead (2010) for Ceredigion CC; armour sized with HR Wallingford 3D physical modelling (NCE 2011); Rigden et al. 2013 (Surf reefs - physical modelling) is a related card reference, content not read', 'text', 'S', 'NCE2011', 'card R15, R17 (reports not obtained)')
    r.F('arm_angle_to_shoreline_deg', 64.2, 'deg (north mound long axis; head part 67.8, tail part 76.9; design plan 60.9)', 'D', 'repo:' + SH + 'shape.json angles', 'PCA of the polygon vs shoreline bearing 359.57 deg; the south (oval) mound is parallel to the shore (0.18 deg)')
    r.U('arm_angle_to_swell_deg', 'deg', 'swell direction not available; the north mound axis is 25.8 deg off shore-normal.')
    r.F('surf_outcome', 'unknown', 'category', 'S', 'Blacka2013+Stormrider', 'Blacka Table 4.1 (protection and surfing "Unknown (insufficient monitoring)"); Stormrider guide still calls it a "proposed" artificial reef site; Surf-Forecast 3.0/5 beginner, no first-hand reviews',
        note='No wave-height, ride-length or surfable-days measurement found. Crest above MSL at design means the surf reef only works on the rising/falling tide with cover (not analysed).')
    r.U('surfable_days_per_year', 'days/yr', 'not stated.')
    r.F('durability', 'no damage, deflation or removal found (imagery 2012-2024, LiDAR 2022); rock armour designed with 3D physical modelling; defences withstood December 2011 storms', 'text', 'S', 'DailyPost', 'METHODS_3D s1; card outcome (R2, R3)')
    r.F('sediment_shoreline_outcome', 'flood protection reported effective from Dec 2011; scheme combines reef + groynes + breakwater with beach nourishment (84,500 t shingle); no quantified shoreline response found; Blacka: performance "yet to be determined"', 'text', 'S', 'DailyPost+Blacka2013', 'card outcome; Blacka p.70, Table 4.1')
    r.F('cost_local', 13000000, 'GBP', 'S', 'Coflein', 'record NPRN 424699: completed reef/coastal-defence works GBP 13 M (whole Phase 1 defence scheme, not the reef alone)', price_year=2012, currency='GBP',
        note='Other values: GBP 7 M funding envelope; GBP 13.5 M (2009); BAM Nuttall tender GBP 11.5 M; GBP 12 M (Wikipedia, 2011-15); GBP 29 M full phased scheme. Price year ASSUMED 2012 (completion). Not reef-only: WHOLE PHASE 1 SCHEME (275,000 t incl. 84,500 t shingle; all breakwaters and groynes); excluded from any cost-per-volume or cost-outcome comparison. RHDHV (search only): about GBP 14 M, completed March 2015.')
    r.F('shape_on_page', 'shown', 'category', 'S', None, '04_build/data/reefs.json footprint.display = True (read only)')
    r.F('model_3d', 'yes: laser-survey (LiDAR 2022) default; confidence MEDIUM', 'text', 'S', None, SH + '3d/METHODS_3D.md s1, s6')
    r.profile_fields(SL, crest_primary=-0.19, use_median=True, version_note='North mound only (x < 15 m of the model frame); crest = LiDAR-surface maximum; the reef is a long diagonal mound (axis 64 deg to the shore), so the median over columns is used as primary.')
    return r
