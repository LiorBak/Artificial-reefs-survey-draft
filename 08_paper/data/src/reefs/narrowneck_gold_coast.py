import sys; sys.path.insert(0, '/home/user/artificial-reef-survey/08_paper/data/src')
from common import *
SL = 'narrowneck-gold-coast'
SH = '07_scale/shapes/narrowneck-gold-coast/'
AL = dict(GLOBAL_ALIASES, Swellnet2017=r'Nettle.*2017-11-07', Swellnet2019=r'Nettle.*2019-08-19', EcoShape=r'EcoShape \(accessed', Inertia2017=r'Haro, Alexander',
          ICM=r'Building Artificial Surf Reefs', RaisedWater=r'Raised Water Research.*Narrowneck', CityGC2020=r'City of Gold Coast \(2020\)', Garmin=r'Garmin Navionics')
def build():
    r = Reef(SL, AL); t = tr(SL); m = med(SL, 'ramp')
    r.F('name', 'Narrowneck Reef (Gold Coast Reef), Gold Coast, Queensland', 'text', 'S', 'Blacka2013', 'Appendix A.2 p.94')
    r.F('country', 'Australia', 'text', 'S', 'Blacka2013', 'Appendix A.2 p.94')
    r.F('lat', -27.986629, 'deg N (WGS84)', 'D', 'repo:' + SH + 'shape.json geo.centroid_latlon', 'centroid of the traced container field (Esri Wayback r9812, 8 Aug 2020); same point as the page and the card',
        note='Position +-5 m (Esri); page status ok (not approximate).')
    r.F('lon', 153.434052, 'deg E (WGS84)', 'D', 'repo:' + SH + 'shape.json geo.centroid_latlon', 'as lat')
    r.F('year_built', 1999, 'year (construction start)', 'S', 'Blacka2013', 'A.2.1 p.94: construction began Aug 1999')
    r.F('year_completed', 2000, 'year (main phase)', 'S', 'Blacka2013', 'A.2.1 p.94: major phase complete Dec 2000; crest raise/trim 2001, 2002, 2004, 2006',
        note='Renewed June 2018 (84 containers added, Option 2 layout only partly built on the south reef): 07_scale METHODS_3D s1; Corbett 2023; Swellnet 2017.')
    r.F('purpose', 'multi', 'category', 'S', 'MeadBorrero2011', 'p.2 (3.1.2): first MPR designed primarily for coastal protection, surfing secondary',
        note='Primary: protect the Narrowneck isthmus/Gold Coast beaches (sand bypass of ~500,000 m3/yr drift); secondary: surf; tertiary (unplanned): habitat.')
    r.F('material', 'geotextile sand-filled containers (Terrafix); initial ~400, 534 placed by 2018; each ~20 m long, 3-4.5 m diameter, 160-300 t', 'text', 'S', 'Blacka2013', 'A.2.5 p.97',
        note='Sand per container about 147 m3 (METHODS_3D s3/KN; 534 x 147 = ~78,500 m3 placed).')
    r.F('volume_m3', 70000, 'm3 (sand fill of the containers, literature; about 60,000 placed by 2000, 78,500 by 2018; exposed mound 13,495 m3 in the 3D model)', 'S', 'MeadBorrero2011', 'p.2 (3.1.2): "largest yet built (some 70,000 m3)" citing Jackson 2007',
        note='Fill volume, 1999-2000 build. The visible/exposed mound is only 17-27 % of the placed sand.',
        alts=[(78500, '534 containers x ~147 m3 sand (placed to 2018)', 'D', 'repo:' + SH + '3d/METHODS_3D.md s1/KN "Mound envelope volume"', 'stated line "534 containers x about 147 m3"'),
              (13495, 'mound envelope of the default 3D outline (photo 8 Aug 2020), +-3,100 m3 for 0.5 m bed error', 'D', 'repo:' + SH + '3d/model.js versions[photo_2020-08-08].volume_m3', 'model.js'),
              (21271, 'mound envelope, Option 2 renewal design 2017', 'D', 'repo:' + SH + '3d/model.js versions[design_option2_2017].volume_m3', 'model.js')])
    r.F('footprint_area_m2', 6239, 'm2 (plan, visible container field)', 'D', 'repo:' + SH + 'shape.json canonical.area_m2 (photo trace of Esri Wayback r9812, 8 Aug 2020)', 'shape.json canonical.area_m2; METHODS_3D s1',
        note='LOWER BOUND: the deeper toe is not visible on the photo. Default outline decided by Lior 2026-10-10 (D7).',
        alts=[(13941, 'Option 2 renewal design envelope (2017)', 'D', 'Corbett2023+Jackson2012', 'shape.json outline_versions; METHODS_3D s4.1'),
              (13631, '2004 revised design (to -6 m contour)', 'D', 'Jackson2012', 'shape.json outline_versions'),
              (34409, 'council asset polygon OBJECTID 4637 (loose envelope)', 'S', 'repo:City of Gold Coast Open Data, Artificial Reef layer OBJECTID 4637 (card R28)', 'shape.json dimensions_check')])
    r.F('plan_length_alongshore_m', 113.3, 'm', 'D', 'repo:' + SH + 'shape.json canonical.bbox_m.alongshore', 'bbox of all 7 traced polygons in the shore-aligned frame',
        alts=[(170, 'V-shape maximum longshore dimension (published)', 'S', 'Blacka2013', 'Table 4.2 p.65')])
    r.F('plan_length_crossshore_m', 157.4, 'm', 'D', 'repo:' + SH + 'shape.json canonical.bbox_m.crossshore', 'bbox of all 7 traced polygons',
        alts=[(280, 'V-shape maximum cross-shore dimension (published)', 'S', 'Blacka2013', 'Table 4.2 p.65')])
    r.F('crest_depth_msl_m', 2.32, 'm below MSL', 'D', 'VieiraDaSilva2021+MSQ2026', 'crest -2.2 m AHD measured after the 2018 renewal (V. da Silva 2021 p.5); AHD to MSL: z_MSL = z_AHD - 0.12 (MSQ Gold Coast Seaway, METHODS_3D s3.1)',
        note='Shallowest container top in the 3D model: -1.8 m AHD = 1.92 m below MSL (isolated wing container). Design crest -2.5 m AHD = 2.62 m below MSL. Original 1999 design -1.0 m AHD (Blacka 2013 p.94), built at -1.5 m AHD, lowered; then settled 1-2 m locally.',
        alts=[(1.92, 'shallowest mesh top (isolated wing container)', 'D', 'Corbett2023', 'METHODS_3D s3.1, 4.3'), (2.62, 'design crest -2.5 m AHD', 'D', 'Jackson2007+MSQ2026', 'METHODS_3D s3.1')])
    r.F('crest_depth_lat_m', 1.44, 'm below LAT', 'D', 'VieiraDaSilva2021+MSQ2026', 'METHODS_3D s3.1: measured -2.2 m AHD = 1.44 m below LAT with MSQ AHD = LAT + 0.760',
        note='1.20 m below LAT with the papers\' rule (AHD = LAT + 1.00); the 0.24 m datum difference is an open issue (ask City / MSQ).')
    r.F('seabed_depth_toe_m', round(t['toe_depth'], 2), 'm below MSL', 'D', 'repo:' + SH + '3d/model.js seabed + default outline (08_paper/data/src/derive_profiles.py)', 'bed at the seaward-most cell of the grid column through the crest (x = 50 m, y = 283 m of the model frame)',
        note='Bed profile from the 2017 pre-works multibeam read off Corbett 2023 Fig 3 colour scale (+-0.4 m, placed to +-10 m) and Navionics labels; the outline edge is the -6 m contour (photo outline = lower bound). Design toe about -7 m AHD (7.1 m below MSL). Median over reef columns %.2f m.' % med(SL, 'toe_depth')[0],
        alts=[(7.12, 'seabed at the toe, -7 m AHD, read from the multibeam colour figure (+-0.4 m)', 'D', 'Corbett2023+VieiraDaSilva2021', 'Corbett 2023 Fig 3; METHODS_3D s3.3, KN "Seabed"')])
    r.F('seabed_depth_at_crest_m', round(t['bed_at_crest_edge'], 2), 'm below MSL', 'D', 'repo:' + SH + '3d/model.js seabed (derive_profiles.py)', 'bed under the seaward crest edge on the same transect (y = %.0f m)' % t['y_crest_edge'],
        note='Bed under the reef ranges %.2f-%.2f m below MSL (mean %.2f) under the 6,239 m2 footprint.' % (PROFILES[SL]['bed_depth_under_footprint_m']['min'], PROFILES[SL]['bed_depth_under_footprint_m']['max'], PROFILES[SL]['bed_depth_under_footprint_m']['mean']))
    r.F('reef_height_m', 2.2, 'm (mean; max 3.9)', 'D', 'Corbett2023', 'METHODS_3D KN "Reef height above the seabed": mean 2.2 m, max 3.9 m (default); 2-2.5 m at the crest wedge, 1-1.5 m at the toe; +-1 m')
    r.F('distance_offshore_crest_m', round(PROFILES[SL]['crest_cell_xy'][1], 0), 'm from the 8 Aug 2020 waterline (MSL line proxy)', 'D', 'repo:' + SH + '3d/model.js frame (shoreline_y = 0) (derive_profiles.py)', 'y of the shallowest crest cell',
        note='Centroid of the traced field is %.0f m offshore; nearest edge 212 m (shape.json canonical.distance_offshore_m = 369.1 m; its definition is not stated in the file). Published: 100-600 m offshore (Blacka Table 4.2).' % 288,
        alts=[(369.1, 'shape.json canonical.distance_offshore_m', 'D', 'repo:' + SH + 'shape.json canonical.distance_offshore_m', 'shape.json'),
              (288, 'centroid of the traced field', 'D', 'repo:' + SH + 'shape.json dimensions_check "earlier text-derived schematic" row', 'shape.json dimensions_check')])
    # tide
    sp, ne, mean = tide_stats(dict(MHWS=0.65, MHWN=0.36, MLWN=-0.37, MLWS=-0.66))
    r.F('tide_spring_range_m', sp, 'm', 'D', 'MSQ2026', 'MHWS +0.65 - MLWS -0.66 m MSL (Gold Coast Seaway planes above LAT: MLWS 0.22, MHWS 1.53); METHODS_3D s3.1',
        note='Semidiurnal, micro-tidal. Blacka 2013 Table 4.3 p.67 lists "tide range 2 m" (definition not stated, probably the maximum range); HAT-LAT = 2.03 m.',
        alts=[(2.0, 'tide range as listed in the NSW review (definition not stated)', 'S', 'Blacka2013', 'Table 4.3 p.67 / A.2.1')])
    r.F('tide_mean_range_m', mean, 'm', 'D', 'MSQ2026', 'mean of spring and neap ranges: ((MHWS+MHWN)-(MLWS+MLWN))/2 with MHWS +0.65, MHWN +0.36, MLWN -0.37, MLWS -0.66; neap range %.2f m' % ne)
    r.F('swell_hs_m', 1.0, 'm (typical; basis not stated)', 'S', 'Blacka2013', 'Table 4.3 p.67 and A.2.1 "Hs 1.0 m"; longshore drift ~500,000 m3/yr to the north',
        note='Dominant swell: south-east (Swellnet 2017 quote: "clean south-east swell"). Reef needs "long period, clean swell" (2007 monitoring report, via Swellnet 2017). Hs distribution/Tp not confirmed in the repo sources; design Tp not confirmed.')
    r.F('swell_tp_s', None, 's', 'U', None, '', note='no Tp for the Narrowneck design/typical surf found in the repo; Blacka 2013 A.2 p.100: actual Gold Coast waves are shorter period than the modelled long-period clean swell (value not stated).')
    r.F('swell_dir', 'SE (south-east) for the surfable swell (qualitative)', 'text', 'S', 'Swellnet2017', 'quote of Stu Nettle 7 Nov 2017 (R2)', note='Direction in degrees not confirmed.')
    r.F('design_wave', 'design basis: Burleigh Heads and Kirra surfing parameters (Mead 2000, via Mead & Borrero 2011); designers\' 1:50 physical model at UNSW WRL with the ORIGINAL -1.0 m AHD crest; wave transmission 0.5 over the crest, 0.9 at the shoreline', 'text', 'S', 'MeadBorrero2011+Blacka2013', 'M&B p.2-3; Blacka A.2.2-A.2.4 p.95-96',
        note='Design wave height/period not confirmed.')
    r.F('arm_angle_to_shoreline_deg', 72.2, 'deg (north arm; south arm 90.0)', 'D', 'repo:' + SH + 'shape.json angles', 'north arm axis vs shoreline (acute): 72.2 deg (min-rectangle 82.2); south arm 90.0; arms converge seaward by 17.8 +-5 deg',
        note='Narrowneck is a V/chevron with two nearly shore-normal arms and a weir, not a peel-angle ramp in the Mead/Black sense.')
    r.U('arm_angle_to_swell_deg', 'deg', 'not computed: dominant SE swell direction is given only qualitatively; with shore-normal bearing 86.2 deg true and a SE swell (~135 deg) the swell arrives about 49 deg off shore-normal before refraction (ASSUMPTION of 135 deg).')
    r.F('surf_outcome', 'works rarely', 'category', 'S', 'Swellnet2017+Swellnet2019+Blacka2013', 'Swellnet 2017/2019; Blacka Table 4.1 (surfing "Minor")',
        note='Reason: crest lowered from -1.0 to -1.5 m AHD by the council before construction (Blacka p.94; Swellnet says "1 m") so that the reef is too deep for consistent breaking; non-uniform container placement; reef lives only in long-period clean swell at low tide. Quotes: "disappointing in its secondary objective to improve surfing" (Wikipedia, card R9); "surfers seldom surf the reef" (Swellnet 2019, card R14); "the change would have no effect on sand accretion but was terminal to Narrowneck becoming a good surfing reef" (Swellnet 2017). Reef broke waves "roughly 50% of the time", faces 0.7-2.0 m, average ride 150-200 m / 30 s, "fun, but not hollow" (EcoShape via card R6); rides up to 60 s onto the adjacent sandbars (Corbett 2010a via Mead & Borrero 2011 p.3).')
    r.U('surfable_days_per_year', 'days/yr', 'not stated for Narrowneck; EcoShape (card R6) says the reef broke waves about 50 % of the time (basis unknown).')
    r.F('durability', 'containers stable to 8-10 m waves; nine storms with H>5 m by 2002; settlement 1-2 m locally (weir containers up to 2 m); damage by anchors, spears, knives, boards; composite geotextile used in later bags; renewal 2017-18 (84 containers); Cyclone Oma Feb 2019 erosion (beach)', 'text', 'S', 'Blacka2013+Corbett2023', 'Blacka A.2.5 p.97-98; METHODS_3D s1 (history); Swellnet 2019',
        note='Reef still in place and monitored in 2019-2026.')
    r.F('sediment_shoreline_outcome', 'Mixed/disputed. Published 20-50 m salient; Blacka 2013 (p.98-100) reads it as a likely misreading (arbitrary dune reference line); Turner (2005) ~20 m accretion within 1000 m of the reef 2001-2003; shoreline receded 2.8 m/yr north/south and 4.3 m/yr in the lee over 8 yr (Blacka et al. 2008); sand increases mostly in offshore bars (City 2019). NSW review rating: coastal protection "Minor".', 'text', 'S', 'Blacka2013+MeadBorrero2011+Swellnet2019', 'Blacka A.2.6-A.2.7 p.98-100; Mead & Borrero p.4 (30-50 m); Swellnet 2019')
    r.F('cost_local', 2800000, 'AUD', 'S', 'Blacka2013', 'A.2.7 p.101: "total cost of the reef was $2.8 million (including top up and maintenance)" (Jackson & Corbett 2007) = about AUD 3.9 M in 2013 AUD; original 1999-2000 build AUD 2.3 M (ICM, card R3)', price_year=2000, currency='AUD',
        note='Price year ASSUMED 2000 (completion of the main phase; the top-ups ran to about 2006, so the 2024 value is a lower bound). Excludes the 2017-18 renewal (about AUD 2 M, mayor quoted by The Inertia 2017; Seabreeze: AUD 2 M of an AUD 18 M beach budget) and the beach nourishment. Other values: AUD 2.3 M original build (ICM); AUD 2.1 M over 10 yr (Raised Water Research, card R5); total AUD 2.8 M incl. top-ups and maintenance (Jackson & Corbett 2007, via Blacka 2013 A.2.7 p.101) = AUD 3.9 M in 2013 AUD (AUD 56/m3); 2017-18 renewal about AUD 2 M (The Inertia 2017, card R10). Lior\'s notes give "$2.5 M" with currency unstated (not used).',
        alts=[(2300000, 'original 1999-2000 build (ICM, ~AUD 30/m3)', 'S', 'ICM', 'ICM web page (card R3)'), (2000000, '2017-18 renewal (mayor quote, press)', 'S', 'Inertia2017', 'press article 2017-09-08')])
    r.F('shape_on_page', 'shown', 'category', 'S', None, '04_build/data/reefs.json footprint.display = True (read only)')
    r.F('model_3d', 'yes: default = visible container field 8 Aug 2020; confidence MEDIUM', 'text', 'S', None, '07_scale/shapes/narrowneck-gold-coast/3d/METHODS_3D.md s1, s6')
    r.profile_fields(SL, crest_primary=2.32, version_note='Model crest = shallowest container top (1.92 m); the measured 2018 crest level is 2.32 m (see crest_depth_msl_m).')
    r.F('reef_arm_note', 'two shore-normal arms + weir (chevron)', 'text', 'S', 'repo:' + SH + 'shape.json canonical.polygon_labels', 'north arm, south arm, shoreward patches, weirs')
    return r
