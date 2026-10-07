"""Assemble ../shape.json (status 'traced') from the work_*.json files and the facts recorded in METHOD.md. Re-run after any change.
python build_shape_json.py"""
import json, math, sys
sys.path.insert(0, '.')
from geo_tools import *
can = json.load(open(ROOT + 'work_canonical_v2.json'))
ang = json.load(open(ROOT + 'work_angles_v2.json'))
pp = json.load(open(ROOT + 'work_pixel_polygons.json'))
reg = json.load(open(ROOT + 'work_installed_reg.json'))
r1 = lambda poly: [[round(x, 1), round(y, 1)] for x, y in poly]
S = can['survey']; T = can['toe_installed_T-4.2']

# Fig 3 full-image bounds (BOPTM -> lat/lon)
corners = [(0, 0), (899, 0), (899, 1063), (0, 1063)]
ll = [T_boptm_to_ll.transform(*f3_en(x, y)) for x, y in corners]
f3_bounds = dict(north=round(max(p[1] for p in ll), 6), south=round(min(p[1] for p in ll), 6), east=round(max(p[0] for p in ll), 6), west=round(min(p[0] for p in ll), 6))
lz_side = json.load(open(ROOT + 'src/linz_aerial_2010-11_BD37_1000_1314_crop.png.geo.json'))
lzc = [(0, 0), (1099, 0), (1099, 1099), (0, 1099)]
lzll = [T_boptm_to_ll.transform(*T_nztm_to_boptm.transform(*lz_px_to_nztm(i, j))) for i, j in lzc]
lz_bounds = dict(north=round(max(p[1] for p in lzll), 6), south=round(min(p[1] for p in lzll), 6), east=round(max(p[0] for p in lzll), 6), west=round(min(p[0] for p in lzll), 6))

BOPRC = 'https://www.boprc.govt.nz/media/558385/mount-maunganui-reef-assessment-of-management-options.pdf'
RWR = 'https://raisedwaterresearch.com/spot/artificial-reef/new-zealand/north-island/mount-maunganui/'
ESRI_T = 'https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/{release}/{z}/{y}/{x}'
src_dir = '07_scale/shapes/mount-maunganui-reef/src/'

sources = [
 dict(id='img1', kind='as_built_survey', title='Figure 3 "Most recent survey of Mount Reef conducted on 18 July 2013" - multibeam plan, colour-coded depth (Chart Datum), NZ-grid axes; survey by University of Waikato & Discovery Marine Ltd',
      url=BOPRC, source_page=BOPRC, page_or_figure='PDF page 23 (printed p22), Figure 3, embedded raster xref 53, 900 x 1064 px native', image_date='2013-07-18 (survey)',
      credit='University of Waikato & Discovery Marine Ltd (DML), via Focus Resource Management Group / Bay of Plenty Regional Council', license='not stated (council report) - check before public reuse',
      local_file=src_dir + 'boprc_fig3_2013_survey.png', image_size=[900, 1064],
      georef=dict(provider='NZGD2000 Bay of Plenty Circuit 2000 (EPSG:2106) axis tick labels printed on the figure', zoom=None, bounds=f3_bounds,
                  tile_template='E = 376680 + (x-109)/5.45 ; N = 812960 - (y-82)/5.45 (x,y = native pixels; ticks at x=109..872 and y=82..845, 109 px per 20 m)',
                  imagery_date='2013-07-18', attribution='University of Waikato & Discovery Marine Ltd'),
      scale=dict(px_per_m=5.45, method='georeferenced', evidence='bottom axis ticks at x = 109, 218, 327, 436, 545, 654, 763, 872 px labelled 376680 ... 376820 (20 m step); left axis ticks at y = 82, 191, ... 845 px labelled 812960 ... 812820; 109 px per 20 m in both axes (square pixels, no shear). Grid confirmed by the outlines falling on the reef in img2.', uncertainty_pct=1.0),
      pixel_polygons=[r1(p) for p in pp['img1']],
      traced_what='-2.0 m Chart Datum contour of the bag field: nearest-legend-colour classification of the native raster (26 swatches), mask = shallower than -2.0 m, closing x2 + hole fill, components > 300 px, contour at the mask edge, Douglas-Peucker 1 px. Five polygons: west (northern) arm 3-bag block 467.1 m2, mid-top bag 61.0, NE small bag 20.5, NE lobe (2 bags) 107.5, south (long) arm 415.0 m2.',
      match_notes='Outline follows the red/orange bag fields and the black -2 contour line (overlays/img1_boprc_fig3_2013.png). It is a mid-height (about half-relief) outline: the bag sides are near vertical on the north side (0.5 m red -> green) and less steep on the scour side (1-1.5 m), so the true toe lies ~0.3-1.5 m outside it. The small north-arm base bags are buried in 2013 and absent; the apex bags are deflated (BoPRC printed p23).',
      role='primary'),
 dict(id='img2', kind='aerial_photo', title='Bay of Plenty 0.125m Urban Aerial Photos (2010-2011), tile BD37_1000_1314 (1100 x 1100 px crop around the reef)',
      url='https://nz-imagery.s3.ap-southeast-2.amazonaws.com/bay-of-plenty/bay-of-plenty_2010-2011_0.125m/rgb/2193/BD37_1000_1314.tiff', source_page='https://nz-imagery.s3.ap-southeast-2.amazonaws.com/catalog.json (LINZ open data, STAC collection bay-of-plenty_2010-2011_0.125m)',
      page_or_figure='tile BD37_1000_1314 (E 1882240-1882720, N 5828640-5829360 NZTM); crop offset px 2067,4175', image_date='2010-12-28 .. 2011-03-31 (flight window; exact day not stated)',
      credit='LINZ (host/processor), New Zealand Aerial Mapping (producer), BOPLASS and Gisborne District Council (licensors)', license='CC BY 4.0',
      local_file=src_dir + 'linz_aerial_2010-11_BD37_1000_1314_crop.png', image_size=[1100, 1100],
      georef=dict(provider='LINZ Bay of Plenty 0.125m Urban Aerial Photos (2010-2011), NZTM2000 EPSG:2193', zoom=None, bounds=lz_bounds,
                  tile_template=lz_side['source_tiff'] + ' ; pixel (i,j) upper-left corner = E %.3f + 0.125 i, N %.3f - 0.125 j' % (LZ_E0, LZ_N0), imagery_date='2010-12-28..2011-03-31',
                  attribution='Source: LINZ Data Service, Bay of Plenty 0.125m Urban Aerial Photos (2010-2011), CC BY 4.0'),
      scale=dict(px_per_m=8.0, method='georeferenced', evidence='GeoTIFF ModelPixelScale 0.125 m (EPSG:2193); 1100 px = 137.5 m', uncertainty_pct=0.5),
      pixel_polygons=[r1(p) for p in pp['img2']],
      traced_what='NOT an independent hand trace: the img1 -2.0 m outlines projected onto the aerial (BOPTM -> NZTM) to test them. The reef shows as a dark red-brown "7"; separately an automatic visible-mass outline (red-excess threshold) gives 1723 m2, 71.3 x 64.9 m alongshore x cross-shore, used as an upper bound (aerial edges are soft and include shadow).',
      match_notes='Best-fit shift of the survey outline against the aerial red mass: 0.5 m W and 1.75 m S (correlation 0.86 vs 0.83 unshifted; Esri 2011 coarse copy gave 0.2 m E-W, 1.7 m N-S): the grid-tick georeference of img1 agrees with the aerial to about 2 m (includes real bag movement 2011-2013). The mass extends 1-2 m beyond the survey outline on the S and E sides (extra east-side bag of the south arm, junction fill: buried by 2013).',
      role='cross_check'),
 dict(id='img3', kind='other', title='"Mount Reef Installed" - colour-coded bathymetry of the completed reef (ASR image on Raised Water Research; legend -1.8 to -7.4 m, datum not stated, axes 100-700 unlabelled)',
      url='https://raisedwaterresearch.com/wp-content/uploads/2019/11/Mount-Reef-Installed.jpg', source_page=RWR, page_or_figure='image caption on page: "The installed reef. Image: ASR"; 570 x 519 px',
      image_date='undated; after Aug 2008 (shows the replaced split top-row bag and the apex "focus" bags)', credit='ASR Ltd via Raised Water Research', license='all rights reserved (link only; no licence stated)',
      local_file=src_dir + 'mount-reef-installed.jpg', image_size=[570, 519], georef=None,
      scale=dict(px_per_m=round(5.45 * reg['s'], 3), method='known dimension (registration to img1)',
                 evidence='no scale bar. Similarity transform onto img1 fitted by maximising the correlation of its depth > -3.8 m mask (image rotated 90 deg clockwise to north-up) with the img1 -2.0 m mask: scale %.4f Installed px per img1 px, rotation %.2f deg, correlation %.3f, IoU %.2f (see METHOD Step 1e). Cross-checks: axis ticks give 0.106 m/unit; implied volume above the ambient bed inside the toe outline 2,835-2,861 m3 vs 2,800 m3 stated as-built.' % (reg['s'], reg['theta_deg'], reg['corr'], reg['iou']),
                 uncertainty_pct=4.0),
      pixel_polygons=[r1(p) for p in pp['img3']],
      traced_what='toe-level outline of the completed reef: registered mask of depth shallower than -4.2 m (legend units), 3 polygons, 1424 m2 (original image pixel frame; north is to the LEFT in this image).',
      match_notes='Outline follows the bags in all three arms including the small north-side base bags, the east-side bag of the south arm and the junction fill; img1 outlines sit inside it (overlays/img3_asr_installed.png). Edges are soft (smoothed DEM) so the outline is +-1-2 m. Registration, not a scale bar, fixes the scale.',
      role='cross_check'),
 dict(id='ctx1', kind='paper_figure', title='Figure 4 "multibeam survey conducted in January 2007, when the reef was 70 % complete (from Scarfe, 2009)" - shaded relief, north arrow only', url=BOPRC, source_page=BOPRC,
      page_or_figure='PDF page 26 (printed p25), raster xref 60, 815 x 953 px', image_date='2007-01', credit='Scarfe (2009) via BoPRC / Focus RMG', license='not stated', local_file=src_dir + 'boprc_fig4_2007_multibeam.png', image_size=[815, 953], georef=None, scale=None, pixel_polygons=[],
      traced_what='nothing (context)', match_notes='Layout at 70 % complete: north arm bag block, south arm, NE bags; "missing bag" on the northern arm replaced in 2008; smaller lower bags on the northern arm visible (buried in 2013). No scale.', role='context'),
 dict(id='ctx2', kind='paper_figure', title='"Mount Reef Multibeam 2007" (RWR copy of ctx1)', url='https://raisedwaterresearch.com/wp-content/uploads/2019/11/Mount-Reef-Multibean-2007.jpg', source_page=RWR, page_or_figure='n/a; 637 x 752 px', image_date='2007-01',
      credit='Scarfe 2009 via Raised Water Research', license='all rights reserved', local_file=src_dir + 'mount-reef-multibeam-2007.jpg', image_size=[637, 752], georef=None, scale=None, pixel_polygons=[], traced_what='nothing (context)', match_notes='duplicate of ctx1', role='context'),
 dict(id='ctx3', kind='design_drawing', title='"Mount Reef" CAD render (2005 delta-wing design, symmetric two-arm layout, no scale)', url='https://raisedwaterresearch.com/wp-content/uploads/2019/11/Mount-Reef.jpg', source_page=RWR, page_or_figure='n/a; 581 x 438 px',
      image_date='design stage 2005', credit='ASR via Raised Water Research', license='all rights reserved', local_file=src_dir + 'mount-reef-cad-design.jpg', image_size=[581, 438], georef=None, scale=None, pixel_polygons=[],
      traced_what='nothing (context)', match_notes='Design topology only (symmetric interleaved V); superseded by the as-built surveys.', role='context'),
 dict(id='ctx4', kind='aerial_photo', title='"Mount Reef Arial" - wide aerial with the reef arrowed (too small to measure)', url='https://raisedwaterresearch.com/wp-content/uploads/2019/11/Mount-Reef-Arial-1024x575.jpg?v=1573519132', source_page=RWR, page_or_figure='n/a; 1024 x 575 px', image_date='undated',
      credit='Raised Water Research', license='all rights reserved', local_file=src_dir + 'mount-reef-arial.jpg', image_size=[1024, 575], georef=None, scale=None, pixel_polygons=[], traced_what='nothing (context)', match_notes='location only', role='context'),
 dict(id='ctx5', kind='satellite', title='Esri World Imagery Wayback release 3630, z18, 700 m radius (shoreline fit; reef visible)', url=ESRI_T.replace('{release}', '3630'), source_page='Esri Wayback', page_or_figure='n/a',
      image_date='2011-01-15 (Esri SRC_DATE2)', credit='Esri, Maxar, Earthstar Geographics, GIS User Community', license='Esri terms - private research copy', local_file=src_dir + 'esri_wayback_2011-01-15_z18_wide.png', image_size=[2961, 2961],
      georef=dict(provider='Esri World Imagery Wayback', zoom=18, bounds=json.load(open(ROOT + 'src/esri_wayback_2011-01-15_z18_wide.png.geo.json'))['bounds'], tile_template=ESRI_T.replace('{release}', '3630'), imagery_date='2011-01-15', attribution='Esri, Maxar, Earthstar Geographics, and the GIS User Community'),
      scale=dict(px_per_m=round(1 / 0.4728420391858986, 4), method='georeferenced', evidence='0.4728 m/px at the centre (z18 Web Mercator, sidecar)', uncertainty_pct=1.0), pixel_polygons=[],
      traced_what='nothing traced on the reef; used to fit the shoreline (wet/dry-sand boundary, 116 shore-normal profiles, Theil-Sen bearing 136.27 deg, MAD 1.8 m)', match_notes='shoreline bearing 136.15 deg true after grid convergence', role='context'),
 dict(id='ctx6', kind='satellite', title='Esri Wayback release 3630, z19, 200 m radius (first registration test)', url=ESRI_T.replace('{release}', '3630'), source_page='Esri Wayback', page_or_figure='n/a', image_date='2011-01-15', credit='Esri', license='Esri terms - private research copy',
      local_file=src_dir + 'esri_wayback_2011-01-15_z19.png', image_size=[1692, 1692], georef=None, scale=None, pixel_polygons=[], traced_what='nothing (context)', match_notes='survey vs satellite shift 0.2 m E-W, 1.7 m N-S; superseded by img2', role='context'),
 dict(id='ctx7', kind='satellite', title='Esri Wayback release 10, z17, 250 m radius', url=ESRI_T.replace('{release}', '10'), source_page='Esri Wayback', page_or_figure='n/a', image_date='2010-03-03', credit='Esri', license='Esri terms - private research copy',
      local_file=src_dir + 'esri_wayback_2010-03-03_z17.png', image_size=[529, 529], georef=None, scale=None, pixel_polygons=[], traced_what='nothing (context)', match_notes='reef visible as a dark "7" 21 months after completion; 0.95 m/px, too coarse to trace', role='context'),
]

def cpoly(p): return [[round(x, 2), round(y, 2)] for x, y in p]
canonical = dict(
    frame='metres; origin = point on the shoreline (wet/dry-sand boundary, Esri 2011-01-15) nearest the survey-outline centroid (lat %.7f, lon %.7f); +x alongshore toward true bearing %.2f deg (NW); +y offshore toward true bearing %.2f deg (NE)' % (can['origin_latlon'][0], can['origin_latlon'][1], can['alongshore_x_true_bearing_deg'], can['offshore_y_true_bearing_deg']),
    derived_from='img1', polygons_m=can['survey_polygons_m'],
    polygon_labels=['west (northern) arm, 3-bag block', 'west arm, mid-top bag', 'NE small bag (focus)', 'NE lobe, 2 bags (focus)', 'south (long) arm, 2 bags'],
    area_m2=S['area_m2'], bbox_m=dict(alongshore=S['bbox_alongshore_m'], crossshore=S['bbox_crossshore_m']), max_dim_m=S['max_dim_m'],
    distance_offshore_m=round(can['dist_survey_centroid_to_shoreline_m'], 1),
    distance_offshore_note='centroid to the wet/dry-sand shoreline line; nearest reef point %.1f m, farthest %.1f m (y range of the polygons). Scarfe 2008 Table 8-3 gives 257 m (MSL shoreline) to the inshore edge and 324 m to the offshore edge (70 %% complete reef); text: ~250 m.' % (S['y_range'][0], S['y_range'][1]),
    shore_normal_bearing_deg=round(can['offshore_y_true_bearing_deg'], 2), shoreline_true_bearing_deg=round(can['shoreline_true_bearing_deg'], 2),
    outline_definition='-2.0 m Chart Datum contour of the 18 Jul 2013 multibeam survey (mid-height outline of the large bags); see toe_polygons_m for the larger as-built toe-level outline',
    min_rotated_rectangle_m=S['min_rot_rect_m'], centroid_m=S['centroid_m'],
    toe_polygons_m=can['toe_polygons_m'], toe_derived_from='img3', toe_area_m2=T['area_m2'], toe_bbox_m=dict(alongshore=T['bbox_alongshore_m'], crossshore=T['bbox_crossshore_m']), toe_max_dim_m=T['max_dim_m'],
    toe_note='as-built toe-level outline from the ASR "Installed" image registered onto img1 (area +33 % vs the survey outline; includes the north-side base bags, the east-side bag of the south arm and the junction fill that are buried or below -2.0 m in 2013). Scale from registration (+-4 %); volume check 2,835-2,861 m3 vs 2,800 m3 stated.')

geo = dict(polygons_latlon=can['survey_polygons_latlon'], toe_polygons_latlon=can['toe_polygons_latlon'], shoreline_bearing_deg=round(can['shoreline_true_bearing_deg'], 2),
           method='Fig 3 pixels -> NZ-grid E,N (tick calibration) -> WGS84 with pyproj (EPSG:2106 -> 4326); shoreline = wet/dry-sand boundary fitted on the Esri 2011-01-15 image (grid bearing 135.98 deg + convergence); checked against the LINZ 2010-11 aerial to ~2 m (0.5 m W, 1.75 m S best fit)',
           source_id='img1', origin_latlon=can['origin_latlon'], centroid_latlon=can['survey_centroid_latlon'], grid_convergence_deg=round(can['true_north_in_grid_deg'], 3))

W, Sg, Mt, NE, WI = ang['west_arm_incl_mid_top'], ang['south_long_arm'], ang['mid_top_bag'], ang['NE_lobe_group'], ang['west_arm_block']
angles = [
 dict(what='west (northern) arm axis, true bearing', deg=86.0, method='mean of the crest-core axes of the three west-arm bags at -1.2 m CD (84.7, 85.4, 86.9 deg) and minimum-rectangle long side of the arm incl. mid-top bag (87.8 deg); +-3 deg'),
 dict(what='west (northern) arm vs shoreline (acute angle)', deg=round(abs(((86.0 % 180) - (can['shoreline_true_bearing_deg'] % 180) + 90) % 180 - 90), 1), method='86 deg axis vs shoreline 136.15 deg true (both undirected); +-3 deg, plus +-2 deg for the shoreline definition'),
 dict(what='south (long) arm axis, true bearing', deg=11.0, method='PCA axis %.1f deg, minimum-rectangle %.1f deg, crest cores 7.3-16.3 deg (-1.0/-1.2/-1.4 m); +-4 deg' % (Sg['pca_axis_true_bearing_deg'], Sg['mrr_long_side_true_bearing_deg'])),
 dict(what='south (long) arm vs shoreline (acute angle)', deg=round(abs(((11.0 % 180) - (can['shoreline_true_bearing_deg'] % 180) + 90) % 180 - 90), 1), method='11 deg axis vs shoreline 136.15 deg; +-4 deg, plus +-2 deg shoreline definition'),
 dict(what='angle between the two arm axes (apex angle at the junction)', deg=75.0, method='86 - 11 deg; +-5 deg'),
 dict(what='bisector of the V (pointing at the junction) vs shore-normal bearing 46.15 deg', deg=2.0, method='arm directions from the junction 266 and 191 deg -> bisector 228.5 -> apex bearing 48.5 deg true; offset ~2 deg: the V is symmetric about the shore normal'),
 dict(what='NE lobe (focus bags) axis, true bearing', deg=18.0, method='PCA %.1f deg, minimum rectangle %.1f deg of the two NE bags (range 13-23); roughly parallel to the south arm' % (NE['pca_axis_true_bearing_deg'], NE['mrr_long_side_true_bearing_deg'])),
 dict(what='shoreline true bearing (SE direction)', deg=round(can['shoreline_true_bearing_deg'], 2), method='Theil-Sen fit of the wet/dry-sand boundary, 116 shore-normal profiles on the Esri 2011-01-15 image, grid bearing 135.98 deg + convergence 0.161 deg; the dune-toe line gives 135.9 deg, whole-beach geometry on current Esri 133.6-134 deg; +-2 deg depending on definition/date'),
]
dimensions_check = [
 dict(quantity='overall shore-parallel (alongshore) length', text_value='80 m (BoPRC 2014 printed p6 "as finally built"); 79 m (Scarfe 2008 p272/275, 70 % complete)', text_ref='card S1 / footprint file S1', drawing_value='%.1f m (survey outline, img1); %.1f m (toe-level outline, img3); 71.3 m (aerial visible-mass upper bound)' % (S['bbox_alongshore_m'], T['bbox_alongshore_m']), diff_pct=round((S['bbox_alongshore_m'] / 80 - 1) * 100, 1),
      comment='diff_pct is for the survey outline; the toe-level outline is %.0f %% below 80 m. The text values are rounded "approximately" figures whose measurement frame is not stated; no accessible source reproduces them.' % abs((T['bbox_alongshore_m'] / 80 - 1) * 100)),
 dict(quantity='overall cross-shore width', text_value='70 m (BoPRC); 67 m (Scarfe 2008, = 324 m - 257 m in Table 8-3, 70 % complete)', text_ref='card S1', drawing_value='%.1f m (survey); %.1f m (toe); 64.9 m (aerial visible mass)' % (S['bbox_crossshore_m'], T['bbox_crossshore_m']), diff_pct=round((S['bbox_crossshore_m'] / 70 - 1) * 100, 1),
      comment='diff_pct is for the survey outline; the toe-level outline is %.0f %% below 70 m.' % abs((T['bbox_crossshore_m'] / 70 - 1) * 100)),
 dict(quantity='footprint area', text_value='2,497 m2 (earlier text-derived two-rectangle schematic); Gemini 4,800 m2 gross / 2,455 m2 net', text_ref='07_scale/reefs/mount-maunganui-reef.footprint.json; 00_gemini_footprints_extract', drawing_value='%.0f m2 survey; %.0f m2 toe-level; 1,723 m2 aerial visible-mass upper bound' % (S['area_m2'], T['area_m2']), diff_pct=round((S['area_m2'] / 2497 - 1) * 100, 1),
      comment='vs the earlier 2,497 m2 schematic (modelled from 25 m-wide rectangles, not traced); toe-level is %.0f %% below it. Gemini footprints rejected.' % abs((T['area_m2'] / 2497 - 1) * 100)),
 dict(quantity='arm length', text_value='"around 80 m" each (Scarfe 2008 Fig 4.22 caption, 70 % complete); 70 m x 30 m each (NZ Herald Nov 2005, design stage); bags 50 m long (Moores 2006, designer)', text_ref='card R8, S4', drawing_value='west arm 47.6 m x 19.3 m; south arm 45.1 m x 12.0 m; longest bag ~45-48 m', diff_pct=-41.0,
      comment='diff_pct vs 80 m (mean of 47.6 and 45.1 = 46.4 m). Measured arm length agrees with the 50 m bag length (-7 %); the 80 m arm and 70 x 30 m figures are not reproduced by any survey or the aerial.'),
 dict(quantity='distance offshore', text_value='~250 m (card R12, S1); 250-300 m (consent); Scarfe 2008: 257-324 m from the MSL shoreline', text_ref='card S1', drawing_value='%.1f m centroid, %.1f m nearest point, %.1f m farthest, to the wet/dry-sand line' % (can['dist_survey_centroid_to_shoreline_m'], S['y_range'][0], S['y_range'][1]), diff_pct=round((S['y_range'][0] / 250 - 1) * 100, 1),
      comment='diff_pct = nearest reef point vs 250 m; our shoreline is the wet/dry-sand boundary, landward of MSL by ~20-30 m on this flat beach, so this agrees with Scarfe (257 / 324 m).'),
 dict(quantity='crest depth (majority)', text_value='0.8-1.0 m below Chart Datum; highest point 0.2-0.4 m below CD (BoPRC 2014 printed p6, p21)', text_ref='card S1', drawing_value='Fig 3 colours: median -1.3 m (west block) / -1.5 m (south arm), 90th percentile -0.7 / -0.5 m, red cores -0.6..-1.0 m; Installed legend brightest -1.8 m MVD-53 = -0.84 m CD', diff_pct=None, comment='consistent (colour steps 0.2 m); not a length so no percentage'),
 dict(quantity='as-built volume', text_value='2,800 m3 (RWR; BoPRC printed p28); design 6,000-6,500 m3', text_ref='card R2/S1', drawing_value='2,835-2,861 m3 above the ambient bed inside the toe outline (img3); 1,588 m3 above the 2013 bed inside the -2.0 m outline (img1)', diff_pct=1.5,
      comment='diff_pct is for img3 and validates its registered scale; the 2013 value is lower because bags have settled and sand has aggraded.'),
]
gemini = dict(values=dict(length_m=95.0, width_m=75.0, area_m2=4800.0, crest_depth_m=2.2, distance_offshore_m=250.0, ambient_seabed_depth_m=6.2, shape='Swept-Wing Inverted Y / Chevron with Central Ridge', coordinates='-37.6331, 176.1864 (footprints/satellite) ; -37.6597, 176.2147 (dossier)', shoreline_orientation_deg=125, tidal_range_m=2.1),
  sources_used=[
   dict(url=RWR, what_gemini_said='cited as the basis of the Mount Reef description (wedge, 2,800 m3, 250 m offshore)', our_check='dimension_not_in_source', evidence='re-fetched 2026-10-05 with a browser User-Agent: confirms the wedge -> delta-wing change, 2,800 m3 built, 250 m / 300 m siting; contains no 95 x 75 m, no 2.2 m crest, no 6.2 m bed.'),
   dict(url='https://raisedwaterresearch.com/wp-content/uploads/2019/07/Artificial-Reef-Comparison.jpg', what_gemini_said='source of the footprint outline (source_crops/mount_maunganui_source.png = crop of this graphic: white "Y" outline over an aerial, 200 m bar)', our_check='wrong_design_version', evidence='schematic design-intent outline, not a survey; surveys and the 2010-11 aerial show an asymmetric "7" (arms 86 and 11 deg true, 75 deg apart) and no stem on the V axis.'),
   dict(url='https://doi.org/10.1080/089207599263767', what_gemini_said='"Black, S.M. & Kerry, A. (1999). Multipurpose Artificial Reef. Coastal Manag. 27:355-365."', our_check='wrong_design_version', evidence='Real paper: Mead & Black (1999), "A Multipurpose, Artificial Reef at Mount Maunganui Beach, New Zealand", Coastal Management 27(4):355-365 (Crossref, first author listed Black). Authors/title garbled by Gemini; 1999 pre-construction design paper (full text not accessible, publisher 403): cannot support as-built 95 x 75 m.'),
   dict(url='(no URL given by Gemini)', what_gemini_said='"Mead, S. et al. (2007). Mount Maunganui Reef Monitoring Report. ASR Ltd."', our_check='unverifiable', evidence='not found online; nearest real items: Black & Mead (2007) Shore & Beach 75(4):55-66 and Mead (2011), both cited in BoPRC / Scarfe but not accessible.'),
   dict(url='(no URL given by Gemini)', what_gemini_said='"Tauranga City Council: Tay Street Reef Removal Dossier (2014)."', our_check='dead', evidence='no such document found; the partial removal was a Bay of Plenty Regional Council decision (announced 16 Apr 2014; BoPRC report).'),
   dict(url='-37.6331,176.1864 and -37.6597,176.2147', what_gemini_said='reef coordinates', our_check='wrong_site', evidence='1.93 km NW and 1.97 km SE of the reef at -37.6448, 176.2026 (reef visible there on LINZ 2010-11 and Esri 2010/2011 imagery).')],
  summary='Gemini footprint rejected: wrong coordinates (about 2 km off), a Y-shaped polygon traced from a schematic graphic, 95 x 75 m / 2.2 m crest / 6.2 m bed unsupported by any accessible source (BoPRC survey: crest 0.8-1.0 m below CD, bed 3-5 m MSL). Only the 250 m offshore figure and the general V family agree.')
references = [
 dict(id='R1', citation='Focus Resource Management Group (2013/14). Mount Maunganui Reef - Assessment of Management Options. Report for Bay of Plenty Regional Council.', url=BOPRC, accessed='2026-10-05', supports='Fig 3 survey (img1), Fig 4, dimensions, depths, history, bag damage'),
 dict(id='R2', citation='LINZ (2010-11). Bay of Plenty 0.125m Urban Aerial Photos (2010-2011), CC BY 4.0, tile BD37_1000_1314.', url='https://nz-imagery.s3.ap-southeast-2.amazonaws.com/bay-of-plenty/bay-of-plenty_2010-2011_0.125m/rgb/2193/collection.json', accessed='2026-10-05', supports='img2'),
 dict(id='R3', citation='Raised Water Research. Mount Maunganui (page with ASR "Installed" image and Scarfe 2009 multibeam).', url=RWR, accessed='2026-10-05', supports='img3, ctx1-4, as-built volume 2,800 m3'),
 dict(id='R4', citation='Scarfe, B.E. (2008). Oceanographic considerations for the management and protection of surfing breaks. PhD thesis, University of Waikato.', url='https://hdl.handle.net/10289/2668', accessed='2026-10-05', supports='datum MVD-53, 79 x 67 m, offshore distances (Table 8-3), construction stages (Table 8-1), coast orientation 132 deg'),
 dict(id='R5', citation='NIWA (2006). MHWS level for the Bay of Plenty. Client report HAM2006-133 (Bell, Goring et al.).', url='https://www.boprc.govt.nz/media/32572/NIWA-091119-MHWSlevelforBOP.pdf', accessed='2026-10-05', supports='MVD-53 = Chart Datum + 0.9622 m (Tauranga); MLOS vs MVD-53'),
 dict(id='R6', citation='LINZ. Standard port tidal levels (Tauranga).', url='https://www.linz.govt.nz/guidance/marine-information/tide-prediction-guidance/standard-port-tidal-levels', accessed='2026-10-05', supports='MHWS/MHWN/MLWN/MLWS 2026-27, HAT/LAT 2000-2018 (Chart Datum)'),
 dict(id='R7', citation='LINZ. Notes about the Moturiki Annual Mean Sea Level Data (updated 16 Feb 2023).', url='https://www.linz.govt.nz/sites/default/files/data/Moturiki_Readme.pdf', accessed='2026-10-05', supports='gauge zero 1.487 m below MVD-53; chart datum 4.103 m below BM BC84'),
 dict(id='R8', citation='Mead, S. and Black, K. (1999). A multipurpose, artificial reef at Mount Maunganui Beach, New Zealand. Coastal Management 27(4): 355-365.', url='https://doi.org/10.1080/089207599263767', accessed='2026-10-05', supports='Gemini source G3 (metadata only; full text not accessible)'),
 dict(id='R9', citation='Moores, A. (2006). Artificial surf reefs - coming to a beach near you. New Zealand Geographic 78.', url='https://www.nzgeo.com/stories/artificial-surf-reefs-coming-to-a-beach-near-you/', accessed='2026-09-25 (card)', supports='design: 24 bags, largest 3.5 m high x 50 m long, 660 m3 each, 4.5 m depth, 250 m offshore'),
]
design_version = dict(
 drawn='As-built bag field of the completed reef (construction finished mid-2008): img1 outlines the large bags at the -2.0 m CD contour as surveyed 18 Jul 2013; the as-built toe-level outline (ASR image, after Aug 2008) is given separately as toe_polygons_m. State drawn is the built delta-wing "7": west (northern) arm of three bags + a top-row bag, south (long) arm of two bags, and two NE "focus" bags.',
 why_this_one='The reef was built Nov 2005 - mid 2008 to the 2005 delta-wing consent, never to the original 50 x 100 m wedge or the symmetric 70 x 30 m V. No as-built plan with a scale exists in accessible sources, so the 2013 georeferenced multibeam is the measured source (BoPRC: crest levels of the main bags "have not changed significantly" since 2008) and the ASR post-construction image shows the completed state. Later changes are notes: apex bag deflation (2008, worse by 2013), north-arm base bags buried by 2013, partial removal 25 Sep - 10 Nov 2014, consent lapsed 2010, fabric washing ashore Jan 2023.',
 alternatives_seen=[
  dict(what='original wedge design, 50 m wide x <100 m long', source_id='doc0', why_not_used='abandoned in 2005 before construction (BoPRC printed p6)'),
  dict(what='2005 design: symmetric V of two 70 m x 30 m arms, 240 m offshore (NZ Herald Nov 2005); CAD render', source_id='ctx3', why_not_used='design intent; built layout is asymmetric with arms 75 deg apart and ~50 m long bags'),
  dict(what='Jan 2007 multibeam, 70 % complete (missing bag on the northern arm)', source_id='ctx1', why_not_used='incomplete state; no scale'),
  dict(what='Y-shaped schematic outline in the RWR comparison graphic (used by Gemini)', source_id='(RWR Artificial-Reef-Comparison.jpg)', why_not_used='schematic, not a survey'),
  dict(what='2013 state: apex bags more deflated, north-arm base bags buried', source_id='img1', why_not_used='drawn, with the differences recorded as notes and the toe-level as-built outline given separately'),
  dict(what='post-2014 state (partly removed)', source_id='ctx8 (not saved)', why_not_used='not visible on 2025 Esri imagery; as-built rule')])
confidence = dict(level='medium',
  reason='The outline is traced on a georeferenced 2013 multibeam survey (NZ-grid ticks, validated against a 0.125 m 2010-11 aerial to about 2 m) and a second as-built image reproduces the stated 2,800 m3 volume, so shape, arm angles and lengths are well fixed; but the surveyed footprint (68 x 60 m at -2 m CD, 74 x 62 m at the toe) is 8-15 % smaller than the 80 x 70 m in the BoPRC text, and the 2013 survey postdates completion by five years (small north-arm base bags buried).',
  factors=['georeferenced multibeam plan (NZ-grid ticks) with 5.45 px/m scale, +-2 m position check against a 0.125 m aerial', 'structure clearly visible on the LINZ 2010-11 aerial', 'dimensions 8-15 % below the text values (medium band per rubric)', 'survey is 2013, not the as-built state: buried base bags and apex deflation',
           'toe-level outline scale comes from registration (+-4 %), validated by volume 2,835-2,861 vs 2,800 m3', 'Gemini footprint rejected'])
shape = dict(slug='mount-maunganui-reef', name='Mount Maunganui Beach Reef ("Mount Reef")', status='traced', updated='2026-10-06', confidence=confidence, design_version=design_version, sources=sources,
             canonical=canonical, geo=geo, angles=angles, dimensions_check=dimensions_check, gemini=gemini, no_source=None, references=references, verified_on='(set by verifier)', verification=[])
json.dump(shape, open(ROOT + 'shape.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('shape.json written', len(json.dumps(shape)), 'bytes')
