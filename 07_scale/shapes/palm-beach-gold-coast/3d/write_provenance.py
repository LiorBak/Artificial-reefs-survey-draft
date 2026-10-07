"""write_provenance.py - writes provenance_3d.json (provenance rows, source list, confidence_3d) from validation_3d.json so the numbers in the viewer
stay in step with the model. Run by build_3d.py; can be run alone after build_3d.py has produced validation_3d.json."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))


def build(val):
    dt, itv = val['datum_test'], val['interval_fit']
    nv = val['navionics_only']
    tv = val['toe_vs_navionics']
    sig = val['anchors']['navionics_reef_signature']['lines']
    fh = val['fish_haven']

    def row(parameter, value, unit, source_id, method, uncertainty, estimated):
        return dict(parameter=parameter, value=value, unit=unit, source_id=source_id, method=method, uncertainty=uncertainty, estimated=estimated)

    P = [
        row('Plan outline (toe polygon, 47 vertices)', '11,972 m2; 162.3 x 91.3 m; long axis 109.6 deg true', '', 's7 + s1',
            'traced on the scaled Bluecoast/Nearmap aerial (8.50 px/m, north arrow) and equal to the City of Gold Coast asset polygon (IoU 0.995, Hausdorff 0.55 m)', '+-1-2 m', False),
        row('Crest outline (slot)', '59.2 x 5.9 m, axis 104.8 deg', '', 's7',
            'innermost contour line, 8 vertices read by hand on 3x zooms; equals the concept crest (60 m at 105 deg, s6)', '+-0.5 m', False),
        row('Crest level', -1.5, 'm vs MSL', 'p1; s8; p2',
            '"The crest of the reef is 1.5m below mean sea level"; "1.5 metres below the average water level at its highest point"; "minimum freeboard of 1.5m at mean sea level, equating to 60cm at the lowest astronomical low tide"',
            '+-0.2 m (rounded figure; MSL vs AHD differ by about 0.1 m); applied uniformly over the 59 x 6 m crest, apex/arm variation not published', False),
        row('Crest depth below LAT', round(-1.5 + 0.88, 2), 'm (negative = below LAT)', 'p1; t1',
            'z_LAT = z_MSL + (MSL - LAT) = -1.5 + 0.88; the Swellnet pair gives 0.60 m below LAT (MSL - LAT = 0.90)', '+-0.22 m (sqrt(0.2^2 + 0.1^2))', False),
        row('Tide planes at the Gold Coast Seaway (MSL = 0)', 'LAT -0.88, MLWS -0.66, MLWN -0.37, MHWN +0.36, MHWS +0.65, HAT +1.15', 'm vs MSL', 't1',
            'MSQ Semidiurnal Tidal Planes 2026 (epoch 2010-2029), row Gold Coast Seaway standard port: MHWS 1.53, MHWN 1.24, MLWN 0.51, MLWS 0.22, MSL 0.88, HAT 2.03 m above LAT; heights minus 0.88; ocean beaches Jumpinpin to Snapper Rocks tide 20 min earlier than the Seaway',
            '+-0.1 m (Palm Beach is not a listed place)', False),
        row('Contour interval of the aerial\'s survey lines', 0.5, 'm per line', 's7; n1; s6',
            'NOT labelled in the source. Assumed 0.5 m (A3): Navionics seabed at the toe implies %.2f m (bands %.2f / %.2f / %.2f); the spacing then gives the concept design slopes 1:12 and 1:5; 1.0 m would put the seaward toe at %.1f m'
            % (itv['s_nav_m'], itv['by_rank_band']['4-6']['s_m'], itv['by_rank_band']['6-8']['s_m'], itv['by_rank_band']['8-11']['s_m'], itv['e_toe_if_1m_interval']),
            '+-0.05 m per line (+-10 %): +-0.5 m at the seaward toe (10 lines)', True),
        row('Side slopes', '1:12 (N flank and outer E end), 1:5 (S flank), 1:25 near-crest platform at the E end', '', 's7; s6',
            'perpendicular spacing of the traced lines (6.0, 2.47, 12.3 m) / 0.5 m; the concept figure labels 1/12 and 1/5', '+-10 % (interval)', True),
        row('Toe elevation of the rock', '%.1f (landward end) to %.1f (seaward end)' % (val['toe_depth_range_m'][1], val['toe_depth_range_m'][0]), 'm vs MSL', 's7',
            'z = -1.5 - 0.5 (K + f) on the toe outline (A4); the next-level fraction f is the outline\'s relative position between lines', '+-0.5 m', True),
        row('Seabed around and under the reef', 'toe -4.3 to -7.0; far field 1 m to 10 m below LAT (z = -d - 0.88)', 'm vs MSL', 'n1; s7',
            'thin-plate-spline surface through the SonarChart 1 m iso-lines (outside a 25 m buffer) plus the toe elevations; chart datum = LAT (A5, tested by RMS: LAT %.2f, MSL %.2f m)'
            % (dt['LAT']['rms_m'], dt['MSL']['rms_m']), '+-0.5 m under the reef (datum +-0.25, interpolation +-0.35, line quantisation +-0.15)', True),
        row('Navionics seabed vs toe elevations', '%.2f (sd %.2f)' % (tv['mean_m'], tv['sd_m']), 'm (toe - chart seabed)', 'n1; s7',
            'independent check: 427 points on the toe outline; rock toe lies %.2f m deeper than the chart seabed on average (scour/apron or interpolation under the reef)' % (-tv['mean_m']), '', False),
        row('Reef height at the crest above the seabed', round(val['height_at_crest_m'], 2), 'm', 'n1; s7',
            'crest -1.5 m minus the model seabed under the crest slot (%.2f m); with the Navionics-only seabed %.2f m' % (val['crest_mean_bed_z'], nv['height_at_crest_m']),
            '+-0.54 m (sqrt(0.2^2 + 0.5^2)); council HEIGHT_M = 5 (unit/reference not stated) is 1.1 m higher', True),
        row('Maximum reef height', round(val['max_height_m'], 2), 'm', 'n1; s7', 'maximum of (reef surface - seabed) on the 1 m grid, at x, y = %.0f, %.0f m' % tuple(val['max_height_at_xy']), '+-0.6 m', True),
        row('Rock envelope volume', round(val['volume_envelope_m3'], -2), 'm3', 'n1; s7',
            'integral of (reef surface - seabed) over the toe outline, 1 m grid; Navionics-only seabed %.0f m3; a seabed 1.0 m deeper gives %.0f m3; council VOLUME = 33,000 (units not stated), card 25,000 m3, 60,000 t'
            % (nv['volume_envelope_m3'], val['volume_sensitivity_by_seabed_offset_m']['-1.0']), '+-6,000 m3 per +-0.5 m of seabed level; 33 % below the register', True),
        row('Reef visible in the SonarChart?', 'yes, as a seaward bulge of the 4-6 m contours', '', 'n1',
            'max deviation from the chord: 4 m line %+.0f m, 5 m %+.0f m, 6 m %+.0f m; touches the toe outline; no contour closes over the crest' % (sig['4']['max_dev_m'], sig['5']['max_dev_m'], sig['6']['max_dev_m']), '', False),
        row('Charted crest depth ("FISH HAVEN 1.5MT")', 1.5, 'm below chart datum', 'n2',
            'label on the nautical chart; design crest = %.2f m below LAT; difference %.2f m if the datum is LAT (A5); equals the design number if read as MSL' % (fh['crest_depth_below_LAT_m'], fh['difference_m']),
            'datum not stated by the app', True),
        row('Waterline (y = 0) = MSL', 0.0, 'm', 's3',
            'waterline fitted to Esri World Imagery 2025-12-01; tide stage of the image unknown (A7); beach face landward of it is a visual 1:15 slope, not surveyed', '+-0.3 m', True),
        row('GEBCO check', '-13 (450 m cell at y = 534 m)', 'm', 'g1', 'GetFeatureInfo; Navionics seabed there is %.1f m MSL (1.1 m apart); not used' % val['gebco']['navionics_z_msl'], 'cell too coarse', False),
        row('Rock layers', 'core 300-1000 kg; armour 1-8 t, crest 6-8 t', '', 's8; p1', 'text only; layer thicknesses not published, so one rock surface is drawn', '', False),
    ]
    S = [
        dict(id='s1', citation='City of Gold Coast (2026) Artificial Reef feature layer, OBJECTID 4638. City of Gold Coast Open Data (ArcGIS Hub), CC BY 3.0. https://data-goldcoast.opendata.arcgis.com/datasets/c9d0b521374740cc9e9561b04c453736_0. Accessed 2026-10-05.', used_for='plan outline; HEIGHT_M / VOLUME cross-check'),
        dict(id='s3', citation='Esri (2025) World Imagery (Maxar), zoom 18, capture 2025-12-01, fetched 2026-10-04. https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9', used_for='waterline, shoreline bearing, state check'),
        dict(id='s4', citation='Hunt, S., Britton, G., Messiter, D., Prenzler, P., Knight, S. and Watterson, E. (2022) Palm Beach Shoreline Project: Innovative Coastal Management Solution. Coastal Engineering Proceedings 37, DOI 10.9753/icce.v37.management.66 (CC BY 4.0).', used_for='plan cross-check (Fig 1), construction 2019, survey (Fig 4 qualitative)'),
        dict(id='s6', citation='Mortensen, S.B., Hibberd, S., Kaergaard, K., Kristensen, S.E., Deigaard, R. and Hunt, S. (2015) Concept design of a multipurpose submerged control structure for Palm Beach, Gold Coast. Australasian Coasts & Ports Conference 2015. https://www.dhigroup.com/upload/publications/coastsea/Mortensen_2015.pdf', used_for='concept slopes 1/12, 1/5, crest orientation 105 deg, 60 m crest (context; the concept was NOT built)'),
        dict(id='s7', citation='Bluecoast Consulting Engineers (c. 2020) Palm Beach artificial reef, Nearmap aerial with survey contour lines (AR_aerial_Nearmaps.jpg). https://www.bluecoastconsulting.com.au/artificialreefs (private research copy; reuse rights unchecked).', used_for='plan outline, crest slot, contour lines (reef surface)'),
        dict(id='s8', citation='Engineering for Public Works (2020) Issue 19, September, IPWEAQ, pp. 50-51, Palm Beach Artificial Reef (page image hosted by Bluecoast).', used_for='crest 1.5 m below average water level; rock classes; 60,000 t'),
        dict(id='p1', citation='Prenzler, P. et al. (2022) Monitoring of the Palm Beach Artificial Reef. Coastal Engineering Proceedings 37 (abstract 12921). https://icce-ojs-tamu.tdl.org/icce/article/view/12921', used_for='crest 1.5 m below mean sea level, 6-8 t rocks, stable (no settlement)'),
        dict(id='p2', citation='Nettle, S. (2019) First impressions at the Palm Beach Artificial Reef. Swellnet, 29 July 2019. https://www.swellnet.com/news/swellnet-dispatch/2019/07/29/first-impressions-palm-beach-artificial-reef', used_for='freeboard 1.5 m at MSL = 60 cm at LAT'),
        dict(id='t1', citation='Maritime Safety Queensland (2026) Semidiurnal Tidal Planes - 2026, height above Queensland Port Datum (LAT 1992). https://www.msq.qld.gov.au/_/media/tmronline/msqinternet/msqfiles/home/tides/tidal-planes/2026-semidiurnal-tidal-planes.pdf. Accessed 2026-10-05.', used_for='MSL, LAT, MHWS, MHWN, MLWN, MLWS, HAT'),
        dict(id='n1', citation='Garmin Navionics (2026) SonarChart Maps, web viewer https://maps.garmin.com/en-US/marine, depth units metres, zoom 17-18, accessed 2026-10-05 14:22-14:35 local. Not for navigation; private research copy; datum not stated by the app (assumed LAT, tested by RMS).', used_for='natural seabed (iso-depth lines 1-10 m), reef signature'),
        dict(id='n2', citation='Garmin Navionics (2026) Nautical Charts layer, same viewer and date; label "FISH HAVEN 1.5MT". Not for navigation; private research copy.', used_for='charted crest depth cross-check'),
        dict(id='g1', citation='GEBCO Compilation Group (2024) GEBCO 2024 Grid, WMS GetFeatureInfo https://wms.gebco.net/mapserv (GEBCO_LATEST_2), queried 2026-10-05.', used_for='coarse check of the offshore depth (not used)'),
    ]
    conf = dict(level='medium',
                reason=('Plan, crest level (-1.5 m MSL) and tide planes are sourced; seabed depth and reef height are inferred (no surveyed value read) from the Garmin Navionics chart and the aerial\'s unlabelled contour lines, '
                        'which agree to %.2f m on average (sd %.2f m) - but the council register gives a taller reef (5 m, 33,000 m3) than the model (%.1f m, %.0f m3).'
                        % (-tv['mean_m'], tv['sd_m'], val['height_at_crest_m'], round(val['volume_envelope_m3'], -2))))
    return dict(provenance=P, sources=S, confidence_3d=conf)


if __name__ == '__main__':
    val = json.load(open(os.path.join(HERE, 'validation_3d.json'), encoding='utf8'))
    out = build(val)
    json.dump(out, open(os.path.join(HERE, 'provenance_3d.json'), 'w', encoding='utf8'), indent=1)
    print('provenance_3d.json written:', len(out['provenance']), 'rows,', len(out['sources']), 'sources;', out['confidence_3d']['level'])
