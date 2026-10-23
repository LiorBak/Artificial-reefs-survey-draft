import sys; sys.path.insert(0, '/home/user/artificial-reef-survey/08_paper/data/src')
from common import *
SL = 'prattes-reef-el-segundo'
SH = '07_scale/shapes/prattes-reef-el-segundo/'
AL = dict(GLOBAL_ALIASES, BorreroNelsen2003=r"Borrero, J\.C\. (&|and) Nelsen", Fontaine2008=r'Fontaine, Evan', Borrero2010=r'Borrero, J\.C\., Mead', NOAA=r'NOAA CO-OPS', Skelly=r'Skelly Engineering', WikiChevron=r'Chevron Reef', RWR=r"Raised Water Research\. \"Pratte")
def build():
    r = Reef(SL, AL)
    r.F('name', "Pratte's Reef (permit name Chevron Reef), El Segundo / Dockweiler Beach, California", 'text', 'S', 'BorreroNelsen2003', 'title / p.1')
    r.F('country', 'USA', 'text', 'S', 'Blacka2013', 'Appendix A.11 p.115')
    r.F('lat', 33.92058, 'deg N (WGS84)', 'D', 'BorreroNelsen2003', 'centre of the georeferenced survey window of the paper (METHODS_3D s1, s3.10); +-100-150 m', note='Page marks this position approximate (card lat/lon; page status approximate).')
    r.F('lon', -118.43335, 'deg E (WGS84)', 'D', 'BorreroNelsen2003', 'as lat')
    r.F('year_built', 2000, 'year (Phase I, 22 Sept 2000)', 'S', 'BorreroNelsen2003', 'p.2-3 (METHODS_3D s2.1); Phase II 23-24 April 2001 (+90 bags)', note='Blacka 2013 p.116-117 dates Phase 2 to 2000 (not supported by the primary text).')
    r.F('year_completed', 2001, 'year (Phase II)', 'S', 'BorreroNelsen2003', 'p.3: second installation 23-24 April 2001', note='Removed in two phases: fall 2008 and fall 2010 (first removal of a purpose-built surf reef).')
    r.F('purpose', 'surf', 'category', 'S', 'Blacka2013', 'A.11 p.115: coastal protection not an objective', note='Court/permit-mandated mitigation for a surf break lost to a 1984 Chevron rock groin; experimental, temporary 10-year permit.')
    r.F('material', 'sand-filled geotextile (polypropylene) bags, 110 bags of 3.0 x 2.1 x 1.2 m (~12.7-14 t filled, 7.9 m3 nominal) in Phase I; +90 bags in Phase II', 'text', 'S', 'Blacka2013+BorreroNelsen2003', 'Blacka A.11.2 p.115; B&N 2003 p.2')
    r.F('volume_m3', 1350, 'm3 (sand, Phase I + II)', 'S', 'MeadBorrero2011', 'p.3 (3.1.3): smallest MPR ever built, 1,350 m3',
        alts=[(869, '110 bags x 7.9 m3 nominal (Phase I)', 'D', 'BorreroNelsen2003', 'METHODS_3D KN "Volume"'), (443, 'modelled single course, state B', 'D', 'repo:' + SH + '3d/METHODS_3D.md KN', 'METHODS_3D'), (1500, 'card range 1,400-1,600 m3', 'S', 'RWR', 'card size field')])
    r.F('footprint_area_m2', 435.2, 'm2 (Phase I design layout)', 'D', 'repo:' + SH + 'shape.json canonical.area_m2 (Skelly Engineering design drawing, verified)', 'shape.json; Fig. 4 of Borrero & Nelsen 2003 reprints the drawing',
        alts=[(703, '110 bags x 6.39 m2 bag footprint', 'D', 'BorreroNelsen2003', 'METHODS_3D KN "Footprint"'), (1856, '64 x 29 m V envelope (rectangle)', 'D', 'Blacka2013', 'Table 4.2 p.65 (area of the rectangle, DERIVED)')])
    r.F('plan_length_alongshore_m', 58.0, 'm', 'D', 'repo:' + SH + 'shape.json canonical.bbox_m.alongshore', 'V axis assumed shore-normal', alts=[(64, 'published', 'S', 'Blacka2013', 'Table 4.2 p.65')])
    r.F('plan_length_crossshore_m', 28.6, 'm', 'D', 'repo:' + SH + 'shape.json canonical.bbox_m.crossshore', '', alts=[(29, 'published', 'S', 'Blacka2013', 'Table 4.2 p.65')])
    r.F('crest_depth_msl_m', 2.68, 'm below MSL (apex face, Phase I as installed)', 'D', 'BorreroNelsen2003+NOAA', 'B&N 2003 p.2: depth at the outermost point "approximately - 6 ft MLLW" = 1.829 m below MLLW; MLLW = -0.849 m MSL (NOAA 9410840, 1983-2001) -> 2.68 m below MSL',
        note='Only as-built crest number. Arm tips (model, constant 1.35 m thickness): 1.78 m below MSL. Design label "min depth -6 ft MSL" = 1.83 m below MSL (state A). Phase II crest: 1.76 m below MSL ("within 3 ft of MLLW"), then eroded by ~1.45 m by Sept 2002. Blacka p.115-117: crest 1.8 m below MLLW (design), 0.9 m after Phase 2, then dropped 1.5 m.',
        alts=[(1.78, 'arm tips, model state B', 'D', 'repo:' + SH + '3d/METHODS_3D.md KN', 'METHODS_3D s3.2'), (1.83, 'design minimum depth (Skelly label, MSL)', 'S', 'Skelly', 'METHODS_3D s3.2 state A')])
    r.F('crest_depth_lat_m', 1.21, 'm below LAT (apex)', 'D', 'NOAA', 'LAT -1.469 m MSL (NOAA 9410840, epoch 1983-2001); apex 2.678 - 1.469 = 1.21 m; arm tips 0.32 m below LAT (METHODS_3D s3.2)')
    r.F('seabed_depth_toe_m', 4.03, 'm below MSL (apex)', 'D', 'repo:' + SH + '3d/METHODS_3D.md KN "Seabed at the reef centre"', 'NOAA 1/3 arc-second DEM, slope 1:32; apex -4.03, tips -3.13, centre -3.67 m MSL',
        note='Six estimates of bed depth at the reef range 2.92 (CRM) to 5.00 m (RWR "about 5 m deep"): Navionics 3.02, B&N Fig 5 beds 3.73, CCC text "15 feet (MSL)" 4.57. Blacka: depth 3.0 m MLLW. Scour to ~4 m depth after construction (Blacka p.116).')
    r.F('seabed_depth_at_crest_m', 4.03, 'm below MSL (apex face)', 'D', 'repo:' + SH + '3d/METHODS_3D.md KN', 'crest at the apex = toe position for the as-installed crest point; bed at the tips 3.13 m')
    r.F('reef_height_m', 1.35, 'm (one 1.2 m bag course, 1.12 courses)', 'D', 'BorreroNelsen2003', 'bag height 1.2 m (4 ft), courses not stated; sigma_H +-0.85 m; after Phase II relief 2.12 m')
    r.F('distance_offshore_crest_m', 103.3, 'm from the MSL waterline (apex face)', 'D', 'repo:' + SH + '3d/METHODS_3D.md s3.2 (y_apex = 103.28 m)', 'model frame y from the MSL waterline; shape.json canonical.distance_offshore_m = 91.44 (reef centre)',
        alts=[(50, 'published distance to the undisturbed pre-construction shoreline', 'S', 'Blacka2013', 'Table 4.2 p.65')])
    sp = round(0.804 - (-0.849), 2); mean = round(0.579 - (-0.566), 2)
    r.F('tide_spring_range_m', sp, 'm (great diurnal range GT = MHHW-MLLW; NOT a spring range)', 'D', 'NOAA', 'NOAA CO-OPS 9410840 Santa Monica datums, epoch 1983-2001: GT 1.654 (MHHW 2.398 - MLLW 0.745 station datum); MHHW +0.804, MLLW -0.849 m MSL (METHODS_3D tide levels); mixed semidiurnal tide, so spring/neap planes are not published; HAT-LAT = 2.85 m')
    r.F('tide_mean_range_m', mean, 'm (mean range MN = MHW-MLW)', 'D', 'NOAA', 'NOAA MN 1.145 (MHW 2.173 - MLW 1.028 station datum); MHW +0.579, MLW -0.566 m MSL')
    r.U('swell_hs_m', 'm', 'no wave-height statement for Pratte\'s found in the repo sources; Santa Monica Bay is a low-energy, W-SW swell site. Surfline comment: reef broke only on a few large swells (card R7).')
    r.U('swell_tp_s', 's', 'not found in the repo.')
    r.F('swell_dir', 'predominant swell assumed along the V axis (arms ~45 deg to the predominant swell per the design); the V axis opens to 61 deg T on the 1996 concept sketch vs shore-normal 65-66 deg T', 'text', 'S', 'Skelly', 'shape.json angles (img6 concept bisector 61.1 deg; shoreline 155.5/335.5 deg)', note='Swell direction in degrees from measurements not confirmed.')
    r.F('design_wave', 'V-reef at 45 deg per arm to the wave direction (design drawing); water depth 3 m MLLW, crest 1.8 m MLLW (Blacka p.115)', 'text', 'S', 'Blacka2013', 'A.11.2 p.115; Fig A.17')
    r.F('arm_angle_to_shoreline_deg', [44.7, 44.4], 'deg (IF the V axis is shore-normal; V axis within ~4 deg of shore-normal)', 'D', 'repo:' + SH + 'shape.json angles', 'arm edges vs V axis: 44.7 and 44.4 deg; apex angle 89.1 deg; the 1996 concept orientation gives 41.2 deg (NNE arm) and other values (not the built design)')
    r.F('arm_angle_to_swell_deg', [44.7, 44.4], 'deg (to the drawing\'s wave-direction axis = V axis)', 'D', 'repo:' + SH + 'shape.json angles', 'same measurements', note='Equals the design assumption; real swell direction not confirmed.')
    r.F('surf_outcome', 'does not work', 'category', 'S', 'Blacka2013+Fontaine2008', 'Blacka A.11 p.117 (surfing "No"; after Stage 2 "near rideable waves that broke only briefly", then none after settlement); Table 4.1',
        note='Quotes: "it never produced a consistently surfable wave" and "as useless as useless gets" (Fontaine, Surfline 2008, card R7); "very little effect on the surfing conditions at Dockweiler Beach" (Wikipedia, card R1). Reason: crest too deep for the swell (apex ~6 ft below MLLW, Surfrider figure "8 feet at zero tide"), bags settled/scoured/disintegrated.')
    r.U('surfable_days_per_year', 'days/yr', 'none stated; no consistently surfable wave.')
    r.F('durability', 'bags moved, sank, buried by sand; black polypropylene deteriorated ("largely disintegrated" within ~2 years); seabed scoured to ~4 m depth soon after installation; crest dropped 1.5 m in the year after Phase II; removed 2008 and 2010: 142.5 containers removed, 1 left visible, 42.5 torn or buried', 'text', 'S', 'Blacka2013', 'A.11 p.116-119; card R4 (RWR) for "largely disintegrated"')
    r.F('sediment_shoreline_outcome', 'no discernible effect on bathymetry or beach (monthly profiles, quarterly ADCP/dive surveys)', 'text', 'S', 'Blacka2013', 'A.11 p.117')
    r.F('cost_local', 550000, 'USD', 'S', 'Blacka2013', 'A.11 p.116-117: build US$550,000 (US$300,000 initial + US$250,000 extra "in 2000"); removal US$551,000 (US$285,000 + US$266,000)', price_year=2000, currency='USD',
        note='Mead & Borrero 2011 p.3 give US$300,000 to build (Phase 1 only) and removal "more than twice that". Blacka Table 4.4: AUD 0.68 M (2013), AUD 504/m3.',
        alts=[(300000, 'Phase 1 only (M&B 2011)', 'S', 'MeadBorrero2011', 'p.3'), (551000, 'removal 2008-2010', 'S', 'Blacka2013', 'A.11 p.118-119')])
    r.F('shape_on_page', 'shown', 'category', 'S', None, '04_build/data/reefs.json footprint.display = True (read only)')
    r.F('model_3d', 'yes: Phase I as built (design layout); confidence LOW', 'text', 'S', None, SH + '3d/METHODS_3D.md s1, s6')
    r.F('depth_gap_m', 1.35, 'm', 'D', 'repo:' + SH + '3d/METHODS_3D.md s3.2 (apex top -2.678 m, bed -4.03 m MSL)', 'toe depth 4.03 - crest depth 2.68 at the apex face (= one bag course)', note='At the arm tips the gap is 1.35 m too (top follows the bed at constant thickness).')
    r.F('seaward_ramp_length_m', 1.35, 'm', 'A', 'repo:' + SH + '3d/METHODS_3D.md assumption A5', 'ASSUMED bag-stack side slope 1 H : 1 V (range 0.5-2.5 H per 1 V), so ramp = gap x 1.0 (0.7-3.4 m)', note='No section of the Phase I reef exists; the face of a 1.2 m bag course is the only "ramp".')
    r.F('mean_seaward_slope', 1.0, 'm/m', 'A', 'repo:' + SH + '3d/METHODS_3D.md assumption A5', 'ASSUMED 1:1 (range 1:0.5 to 1:2.5)')
    return r
