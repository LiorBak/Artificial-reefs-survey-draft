"""build_3d.py - regenerates model.js, docs.js, computed.json (and METHODS_3D.md from METHODS_3D.template.md) for mount-maunganui-reef.
Inputs: ../shape.json (outline_versions, default_outline, canonical, geo), navionics_profile.json (nav_profile.py), ../src/boprc Fig 5 DEM (via mmr_lib, registry img-04),
SOURCES_3D.md.  Rules are in mmr_model.py (the viewer implements the same rules on the grids written here).   Usage:  python build_3d.py
(2026-10-06, 3D agent.  model.js is a JS file so the viewer works from file://; docs.js carries the methods and sources as markdown.)"""
import datetime, json, math, os, re, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mmr_lib as L
import mmr_model as M

HERE = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today().isoformat()
MSL, MVD = M.MSL, M.MVD
BX, BY = 316.15, 46.15
STATED_VOLUME = 2800.0
VER_IDS = ['multibeam_2013_m2p0', 'asr_installed_toe_2008']


def cm(a):
    return [int(v) for v in np.round(np.asarray(a).ravel() * 100)]


def build():
    sh = json.load(open(os.path.join(HERE, '..', 'shape.json'), encoding='utf-8'))
    nav = json.load(open(os.path.join(HERE, 'navionics_profile.json')))
    G = M.make_grid(); ny, nx = G['shape']
    ovs = {v['id']: v for v in sh['outline_versions']}
    # ---------------------------------------------------------------- 2013 survey surface (evidence layer, hue-decoded Fig 5 DEM, 1 m grid)
    dep, filled, valid, _ = L.load_fig5()
    sx0, sx1, sy0, sy1, sd = -75.0, 102.0, 249.0, 396.0, 1.0
    Zs, sxs, sys_ = L.fig5_to_grid(dep, valid, sx0, sx1, sy0, sy1, sd)
    survey_cm = np.where(np.isfinite(Zs), np.round((Zs - MSL) * 100), -32768).astype(int)
    # ---------------------------------------------------------------- reef versions
    comp = {'versions': {}, 'bed_for_2800': {}}
    versions = []
    for vid in VER_IDS:
        o = ovs[vid]; rule = 'skirt' if vid == VER_IDS[0] else 'loft'
        vol_by_bed = {}
        for b in M.BEDS + [None]:
            s = M.stats(G, vid, b); vol_by_bed['nav' if b is None else '%.1f' % b] = {k: round(v, 2) for k, v in s.items()}
        b2800 = M.solve_bed(G, vid)
        s_def = M.stats(G, vid, M.BED_DEFAULT)
        comp['versions'][vid] = dict(volume_by_bed=vol_by_bed, bed_for_2800=round(b2800, 3), area_m2=o['area_m2'])
        comp['bed_for_2800'][vid] = round(b2800, 3)
        for crest in (-0.8, -1.0):
            comp['versions'][vid]['volume_bed-4.0_crest%.1f' % crest] = round(M.stats(G, vid, -4.0, crest=crest)['volume_m3'], 1)
        if rule == 'skirt':
            comp['versions'][vid]['volume_bed-4.0_by_run'] = {str(r): round(M.stats(G, vid, -4.0, run=r)['volume_m3'], 1) for r in (0.25, 0.5, 1.0, 1.5, 2.0)}
            z, S = M.surface(G, vid, M.BED_DEFAULT); inn = G['inner'] >= 0
            comp['versions'][vid]['volume_above_contour_m3'] = round(float(((z - M.ZC)[inn]).sum() * M.DX ** 2), 1)
            comp['versions'][vid]['vertical_wall_minimum_volume_bed-4.0_m3'] = round(float(M.REGION.area * (M.ZC - (-4.0)) + comp['versions'][vid]['volume_above_contour_m3']), 0)
        versions.append({
            'id': vid, 'name': o['name'], 'date': o['date'], 'kind': o['kind'], 'source_ids': o['source_ids'], 'method': o['method'], 'level': o['level'],
            'area_m2': o['area_m2'], 'bbox_m': o['bbox_m'], 'note': o['note'], 'rule': rule, 'run_default': 1.0,
            'flank_unit': 'cm distance from the -2.0 m contour (outside it); -1 = none' if rule == 'skirt' else 'per-mille loft fraction t (0 at the toe, 1000 at the -2.0 m contour); -1 = none',
            'flank': [int(v) for v in (G['skirt'] if rule == 'skirt' else G['loft']).ravel()],
            'polygons_m': [[[round(float(a), 2), round(float(b), 2)] for a, b in p] for p in (M.P2 if rule == 'skirt' else M.PT)],
            'volume_m3_default': round(s_def['volume_m3'], 0), 'footprint_at_bed_m2_default': round(s_def['footprint_area_m2'], 0),
            'h_max_m_default': round(s_def['h_max_m'], 2), 'volume_by_bed': vol_by_bed, 'bed_for_2800_m3': round(b2800, 2),
        })
    # ---------------------------------------------------------------- water levels (z in m above present MSL = CD + 1.13)
    LV = [('HAT', 2.20, 'Highest Astronomical Tide'), ('MHWS', 1.96, 'Mean High Water Springs'), ('MHWN', 1.66, 'Mean High Water Neaps'), ('MSL', 1.13, 'Mean Sea Level (2006-2025 observations)'),
          ('MLWN', 0.57, 'Mean Low Water Neaps'), ('MLWS', 0.21, 'Mean Low Water Springs'), ('LAT', -0.03, 'Lowest Astronomical Tide')]
    levels = [{'id': i, 'label': l, 'z': round(c - MSL, 3), 'above_cd': c, 'source': 'R6 LINZ standard port tidal levels, Tauranga (page updated 8 Jun 2026; MHWS..MLWS predicted 1 Jul 2026-30 Jun 2027, HAT/LAT 2000-2018, MSL observed 2006-2025)'} for i, c, l in LV]
    datum_lines = [
        {'id': 'MVD-53', 'label': 'Moturiki Vertical Datum 1953 (Scarfe / ASR "MSL 1953") = CD + 0.9622 m', 'z': round(MVD - MSL, 4), 'above_cd': MVD, 'source': 'R5 NIWA 2006 (Bell, Goring et al.), Tauranga: MVD-53 = Chart Datum + 0.9622 m; present MSL is 0.17 m above it'},
        {'id': 'CD', 'label': 'Chart Datum (the datum of every BoPRC / DML survey depth)', 'z': round(-MSL, 3), 'above_cd': 0.0, 'source': 'R6 LINZ (CD = zero of the tidal predictions); R7: chart datum 4.103 m below BM BC84'}]
    # ---------------------------------------------------------------- navionics knots
    knots = nav['profile_y_zCD']
    from shapely.geometry import Polygon as _P
    def arm(poly):
        r = _P(poly).minimum_rotated_rectangle; c = list(r.exterior.coords)[:4]
        e = [(np.hypot(c[(i + 1) % 4][0] - c[i][0], c[(i + 1) % 4][1] - c[i][1]), i) for i in range(4)]
        L_, i = max(e); a = np.array(c[i]); b = np.array(c[(i + 1) % 4]); a2 = np.array(c[(i + 3) % 4]); b2 = np.array(c[(i + 2) % 4])
        p0 = (a + a2) / 2; p1 = (b + b2) / 2
        return [[round(float(p0[0]), 1), round(float(p0[1]), 1)], [round(float(p1[0]), 1), round(float(p1[1]), 1)]]
    arms = {'west_block': arm(M.P2[0]), 'south_arm': arm(M.P2[4])}
    model = {
        'schema': 2, 'slug': 'mount-maunganui-reef', 'name': 'Mount Maunganui Beach Reef ("Mount Reef"), New Zealand', 'built': TODAY,
        'state_label': 'AS-BUILT reef, completed mid-2008 (geotextile sand-bag delta wing), idealised loft of the verified outline; evidence layer: 18 Jul 2013 multibeam surface',
        'caption': ('AS-BUILT state (reef completed mid-2008), drawn from the 18 Jul 2013 multibeam outline (default) or the 2008 "Installed" toe outline. z = 0 is present mean sea level (MSL = Chart Datum + 1.13 m); '
                    'the depth datum of the surveys, Chart Datum, and MVD-53 (CD + 0.96 m) are drawn as labelled datum lines. LATER CHANGES (not modelled): by 13 Jul 2013 the apex bags were deflated to -2.0 .. -2.4 m CD '
                    'and the small north-arm base bags were probably buried; the five-year consent lapsed in 2010; the bags were removed from 25 Sep 2014 to the weekend of 8-9 Nov 2014 (all bags above the seabed, NZ$87,000); '
                    'fabric washed ashore on 18 Jan 2023. The reef no longer exists. The seabed outside the reef is the Garmin Navionics SonarChart of 2026 (not for navigation) shifted to the selected as-built bed level.'),
        'history': [
            {'date': '2000 Aug/Sep', 'event': 'five-year resource consent granted (lapsed 2010)', 'source': 'R11 NZ Herald; R1'},
            {'date': 'Jan-May 2007', 'event': 'reef about 70 % complete: 79 x 67 m, reef area 2,400 m2 (definition unstated), highest bag -1.25 m MSL (MVD-53)', 'source': 'R4 Scarfe 2008'},
            {'date': 'mid-2008', 'event': 'reef completed as built (volume about 2,800 m3, crest 0.8-1.0 m below CD)  <-- STATE MODELLED', 'source': 'R1 p6, p28; R3'},
            {'date': '18 Jul 2013', 'event': 'multibeam survey (BoPRC Fig 3 / Fig 5): crest -0.8 .. -1.0 m CD unchanged on the main bags; apex bags deflated (-2.0 .. -2.4 m CD)', 'source': 'R1 p23; img-04 / img-08'},
            {'date': '25 Sep - 8/9 Nov 2014', 'event': 'bags removed above the seabed (NZ$87,000)', 'source': 'R10 SunLive'},
            {'date': '18 Jan 2023', 'event': 'geotextile fabric washed ashore (Sutherland Ave)', 'source': 'R11'}],
        'frame': {'units': 'm', 'x_axis': 'alongshore, true bearing 316.15 deg (towards the NW, Mauao side)', 'y_axis': 'offshore, true bearing 046.15 deg (shore normal, towards the NE)',
                  'z_axis': 'up, 0 = present mean sea level (MSL = Chart Datum + 1.13 m, LINZ Tauranga 2026-27); z_MSL = z_CD - 1.13',
                  'threejs_mapping': 'X = x, Y = z, Z = y (right-handed, not mirrored: (x, y, z-up) is left-handed because y is x turned 90 deg clockwise)',
                  'bearing_x_deg': BX, 'bearing_y_deg': BY,
                  'heading_formula': 'compass bearing of a canonical direction (dx, dy) = atan2(dx sin(BX) + dy sin(BY), dx cos(BX) + dy cos(BY))',
                  'origin_latlon_wgs84': [-37.6467041, 176.2000765], 'origin_note': 'point on the wet/dry-sand shoreline (Esri 2011-01-15) nearest the survey-outline centroid; NZ grid EPSG:2106 E 376521.85 N 812664.84',
                  'reef_centroid_latlon_wgs84': sh['geo']['centroid_latlon'], 'reef_centroid_xy_m': [round(float(M.XC), 2), round(float(M.YC), 2)]},
        'north': {'dir_xy': [round(math.cos(math.radians(BX)), 4), round(-math.sin(math.radians(BX)), 4)], 'note': 'unit vector of true north in canonical (x, y)'},
        'datum': {'msl_above_cd_m': MSL, 'mvd53_above_cd_m': MVD, 'z_msl_equals': 'z_CD - 1.13', 'cd_z': round(-MSL, 3), 'mvd53_z': round(MVD - MSL, 4), 'sources': 'R5, R6, R7'},
        'water_levels': levels, 'water_default': 'MSL', 'datum_lines': datum_lines,
        'shoreline': {'y': 0.0, 'label': 'shoreline y = 0 (wet/dry sand boundary, Esri World Imagery 2011-01-15)', 'bearing_deg': 136.15},
        'seabed': {
            'kind': 'alongshore-uniform cross-shore profile z(y) (m CD) = Pnav(y) + (bed - Pnav(y_ref)) * w(y)',
            'knots_cd': [[round(a, 1), round(b, 2)] for a, b in knots], 'extrapolation': 'last slope continued seaward of the last knot; schematic 1:15 dry beach for y < 0 (not sourced)',
            'beach_run_per_rise': 15.0, 'y_ref': float(M.YC), 'w_y0': M.W_Y0, 'z_nav_at_reef_cd': nav['z_cd_at_reef_centroid'],
            'bed_options_cd': M.BEDS, 'bed_default_cd': M.BED_DEFAULT, 'bed_note': 'bed = seabed elevation (m CD) at the reef centroid, y = 307.7 m; "nav" = the Navionics profile as it is',
            'extent': {'x': [-220.0, 220.0], 'y': [-30.0, 560.0]},
            'navionics': {'accessed': '2026-10-06', 'viewer': 'Garmin Marine Maps (maps.garmin.com/en-US/marine; successor of webapp.navionics.com)', 'layers': ['SonarChart Maps', 'Nautical Charts'], 'units': 'metres',
                          'datum': 'not stated by the viewer; chart datum (CD) assumed and tested against the 2013 multibeam bed (RMS 0.30 m as CD, 0.78 as MVD-53, 0.95 as MSL)',
                          'credit': 'Garmin Navionics, not for navigation; private research copy', 'registry_ids': ['mount-maunganui-reef-img-19', '-img-20', '-img-21', '-img-22'],
                          'depth_at_reef_centroid_m': round(-nav['z_cd_at_reef_centroid'], 2), 'contours_y_median_m': {k: v['y_median_m'] for k, v in nav['contours'].items()},
                          'datum_test': nav['datum_test_vs_2013_dem']['results']},
            'rule_in_viewer': 'S(y) = Pnav(y) + (bed - Pnav(y_ref)) * clamp((y - w_y0) / (y_ref - w_y0), 0, 1)'},
        'reef': {
            'grid': {'x0': M.X0, 'y0': M.Y0, 'dx': M.DX, 'nx': int(nx), 'ny': int(ny), 'order': 'row-major, index = j*nx + i, i along +x, j along +y'},
            'zc_cd': M.ZC, 'crest_cd': {'default': M.CREST_CD, 'options': [-0.8, -0.9, -1.0], 'note': 'main-bag crest 0.8-1.0 m below CD (BoPRC p6, p21); Fig 3 / Fig 5 confirm'},
            'rise_table': {'d2_m': M.RISE_D, 'rise_m': M.RISE_Z, 'rise_max_m': M.RISE_MAX, 'note': 'rise above the -2.0 m contour vs distance inside it, 2013 DEM medians (west block + south arm) scaled to the 1.10 m between the contour and the crest -0.9 CD'},
            'inner_per_mille': [int(v) for v in G['inner'].ravel()], 'inner_note': 'r = RISE(d2) / 1.10 * 1000 inside the -2.0 m polygons, -1 outside; z = zc + r/1000 * (crest - zc)',
            'rule': ('inside the -2.0 m CD polygons z = zc + r (crest - zc); outside: version rule "skirt" z = max(S, zc - dout / run) (run = H:V, default 1) or "loft" z = S + (zc - S) t. S = local seabed. '
                     'Reef height h = z - S (>= 0); volume = sum(h) dx dy')},
        'versions': versions, 'default_version': sh['default_outline'], 'versions_info': sh['versions_info'], 'versions_optional': sh['outline_versions_optional'],
        'stated_volume_m3': STATED_VOLUME, 'arms_xy': arms,
        'survey2013': {'grid': {'x0': sx0, 'y0': sy0, 'dx': sd, 'nx': len(sxs), 'ny': len(sys_)}, 'z_msl_cm': [int(v) for v in survey_cm.ravel()], 'nodata': -32768,
                       'note': 'evidence layer: 18 Jul 2013 multibeam DEM decoded from the hue of BoPRC Fig 5 (registry mount-maunganui-reef-img-04) with its colour bar, 1 m grid, m CD converted to m MSL; +-0.15 m (colour decoding), not the as-built state'},
        'stats': comp,
    }
    import mmr_text
    model = mmr_text.add_text(model, comp, nav)
    return model, comp, G


def write_model_js(model):
    txt = '// generated by build_3d.py on %s - do not edit by hand' % TODAY + chr(10) + 'window.REEF_MODEL = ' + json.dumps(model, separators=(',', ':')) + ';' + chr(10)
    open(os.path.join(HERE, 'model.js'), 'w', encoding='utf-8').write(txt)
    return len(txt)


# ------------------------------------------------------------------------------------------------------------------ documentation
def sg(v, d=2):
    """signed number with a plain minus (m MSL values)"""
    s = ('%.' + str(d) + 'f') % v
    return ('+' + s) if v > 0 else s


def _vol(c, bed):
    return c['volume_by_bed'][bed]['volume_m3']


def fill_methods(model, comp, nav, chk):
    """Fills METHODS_3D.template.md (the {{...}} placeholders) from the computed numbers -> markdown text."""
    cs = comp['versions'][VER_IDS[0]]; ct = comp['versions'][VER_IDS[1]]
    lv = {l['id']: l['z'] for l in model['water_levels']}
    dt = nav['datum_test_vs_2013_dem']['results']
    dk = {k.split(' ')[0]: v for k, v in dt.items()}
    v_t = _vol(ct, '-4.0'); v_s = _vol(cs, '-4.0')
    dv_bed = (_vol(ct, '-4.5') - _vol(ct, '-3.5')) / 2.0
    cbeds = ['-3.0', '-3.5', '-4.0', '-4.5']
    ver_by_id = {v['id']: v for v in model['versions']}
    rows = ['| version (rule) | date | source ids | footprint at the outline (m2) | vol. at bed -3.0 | vol. at bed -3.5 | **vol. at bed -4.0 (default)** | vol. at bed -4.5 | Navionics bed as is | bed that gives 2,800 m3 | footprint at bed -4.0 (m2) |',
            '|---|---|---|---|---|---|---|---|---|---|---|']
    for vid, c in ((VER_IDS[0], cs), (VER_IDS[1], ct)):
        v = ver_by_id[vid]
        vols = ['{:,.0f}'.format(_vol(c, b)) for b in cbeds]
        rows.append('| %s (%s) | %s | %s | %s | %s | %s | **%s** | %s | %s | %s m CD | %s |' % (
            v['name'], 'outline + 1:1 skirt' if v['rule'] == 'skirt' else 'toe loft', v['date'], ', '.join(v['source_ids']), '{:,.0f}'.format(v['area_m2']),
            vols[0], vols[1], vols[2], vols[3], '{:,.0f}'.format(_vol(c, 'nav')), '%.2f' % c['bed_for_2800'], '{:,.0f}'.format(c['volume_by_bed']['-4.0']['footprint_area_m2'])))
    rows.append('')
    rows.append('Volumes in m3, crest -0.9 m CD, sum(h) dx dy on a 0.5 m grid (`mmr_model.py`); stated volume 2,800 m3 (BoPRC p28, Raised Water Research). The bed is the seabed level at the reef centre; '
                '"Navionics bed as is" uses the 2026 SonarChart without shifting it (%.2f m CD at the reef centre).' % nav['z_cd_at_reef_centroid'])
    ver_table = '\n'.join(rows)
    bands = ['| y band (m from shoreline) | cells | 2013 multibeam median (m CD) | Navionics 2026 (m CD) | Navionics minus 2013 (m) |', '|---|---|---|---|---|']
    for b in nav['datum_test_vs_2013_dem']['by_y_band']:
        bands.append('| %d to %d | %d | %.2f | %.2f | %+.2f |' % (b['y_from'], b['y_to'], b['n'], b['dem_2013_zCD_median'], b['nav_zCD'], b['nav_zCD'] - b['dem_2013_zCD_median']))
    nav_tab = ', '.join('%d m: y = %.0f' % (int(k), c['y_median_m']) for k, c in sorted(nav['contours'].items(), key=lambda kv: int(kv[0]))) + ' (m from the shoreline)'
    fp1 = chk['run_for_toe_area']
    rep = {
        'TODAY': TODAY, 'CREST_MSL': '%.2f' % (M.CREST_CD - MSL),
        'HAT': sg(lv['HAT']), 'MHWS': sg(lv['MHWS']), 'MHWN': sg(lv['MHWN']), 'MLWN': sg(lv['MLWN']), 'MLWS': sg(lv['MLWS']), 'LAT': sg(lv['LAT']),
        'Z_NAV': '%.2f' % nav['z_cd_at_reef_centroid'],
        'DT_CD_MEAN': '%.2f' % dk['CD']['mean_diff_m'], 'DT_CD_RMS': '%.2f' % dk['CD']['rms_m'], 'DT_LAT_RMS': '%.2f' % dk['LAT']['rms_m'],
        'DT_MVD_RMS': '%.2f' % dk['MVD-53']['rms_m'], 'DT_MSL_RMS': '%.2f' % dk['MSL']['rms_m'],
        'NAV_TABLE': nav_tab, 'DT_BANDS': '\n'.join(bands), 'VER_TABLE': ver_table,
        'WALL_MIN': '{:,.0f}'.format(cs['vertical_wall_minimum_volume_bed-4.0_m3']), 'ABOVE_CONTOUR': '{:,.0f}'.format(cs['volume_above_contour_m3']),
        'AREA_S': '{:,.0f}'.format(cs['area_m2']), 'AREA_T': '{:,.0f}'.format(ct['area_m2']),
        'FP_S_RUN1': '{:,.0f}'.format(fp1['1.0']), 'FP_S_RUN05': '{:,.0f}'.format(fp1['0.5']),
        'V_S_RUN05': '{:,.0f}'.format(cs['volume_bed-4.0_by_run']['0.5']), 'V_RUN025': '{:,.0f}'.format(cs['volume_bed-4.0_by_run']['0.25']), 'V_RUN2': '{:,.0f}'.format(cs['volume_bed-4.0_by_run']['2.0']),
        'V_T': '{:,.0f}'.format(v_t), 'V_S': '{:,.0f}'.format(v_s),
        'V_T_PCT': '%.0f' % ((v_t / STATED_VOLUME - 1) * 100), 'V_S_PCT': '%.0f' % ((v_s / STATED_VOLUME - 1) * 100),
        'BED2800_T': '%.2f' % ct['bed_for_2800'], 'BED2800_S': '%.2f' % cs['bed_for_2800'],
        'BED_VERT': '%.2f' % (M.ZC - (STATED_VOLUME - cs['volume_above_contour_m3']) / cs['area_m2']), 'DV_BED': '{:,.0f}'.format(dv_bed), 'DV_BED_PCT': '%.0f' % (dv_bed / v_t * 100),
        'DV_CREST_P': '{:,.0f}'.format(ct['volume_bed-4.0_crest-0.8'] - v_t), 'DV_CREST_M': '{:,.0f}'.format(v_t - ct['volume_bed-4.0_crest-1.0']),
    }
    t = open(os.path.join(HERE, 'METHODS_3D.template.md'), encoding='utf-8').read()
    for k, v in rep.items():
        t = t.replace('{{%s}}' % k, v)
    left = re.findall(r'\{\{[A-Z_0-9]+\}\}', t)
    if left:
        raise SystemExit('unfilled placeholders: %s' % sorted(set(left)))
    return t


REQUESTS = [
    ('DECISION', 'As-built bed level at the reef centre (the one number that sets the 3 m height and the volume).',
     'The model default is -4.0 m CD (orchestrator decision of 2026-10-06; BoPRC p23 bed 3.0-4.0 m beside the north arm in 2008, ASR Installed ring about -4.5 m CD if its datum is MVD-53). '
     'But the stated 2,800 m3 is reproduced only at -3.51 m CD (survey outline, 1:1 skirt) or -3.66 m CD (toe outline), and every later source reads the bed shallower (2013 survey -2.4 to -3.3, Navionics 2026 -2.76). '
     'Keep -4.0, or switch the default to about -3.6 m CD? (The viewer already has a bed selector -3.0 / -3.5 / -4.0 / -4.5 / Navionics.)'),
    ('FILE', 'Mead, Black and Moores (2007) and Mead (2011): an as-built plan or section of the Mount Reef.',
     'No PDF could be found without a login. A scaled section would fix the flank slope and the bed level and would replace two assumptions (flank shape, bed). Do you have access (university library, ASR, Raised Water Research)?'),
    ('ASK', 'Datum of the ASR "Mount Reef Installed" bathymetry image (legend -1.8 to -7.4 m).',
     'It is read as MVD-53 here; the same reading as CD would move the toe-level ring from -4.46 to -5.4 m CD. A one-line answer from ASR / Raised Water Research settles whether the 2008 seabed was about -4.5 m CD.'),
    ('LOOK', 'Google Earth historical imagery 2008-2010 over -37.6448, 176.2026.',
     'If the reef bags are visible (calm, clear day) they confirm the as-built footprint and the north-arm base bags that the 2013 survey no longer shows. Note the imagery date; no download needed.'),
    ('LOOK', 'Navionics phone app: depth at the reef centre and the 2.4 m sounding at about 36 m along the shore and 345 m out.',
     'A second reading of the same 2026 SonarChart in the app (with its stated datum) would check the web-viewer reading used for the seabed (-2.76 m CD at the centre).'),
    ('LEGAL', 'Reuse rights of the private research copies before any public release.',
     'The BoPRC / Focus RMG report figures, the ASR image, Esri Wayback tiles and Garmin Navionics screenshots are private copies (07_scale/shapes/mount-maunganui-reef/src/ and 3d/src/); none is embedded in the viewer. Only the LINZ aerial (CC BY 4.0) is open-licensed.'),
]


def requests_md():
    out = ['# Requests for Lior - Mount Maunganui Beach Reef 3D model (%s)' % TODAY, '',
           'Nothing blocks the model; each item below would improve it. Ordered by effect on the model. Reasons: METHODS_3D.md sections 4 and 7.', '']
    for i, (k, title, body) in enumerate(REQUESTS, 1):
        out += ['%d. **[%s] %s**' % (i, k, title), '   %s' % body, '']
    return '\n'.join(out)


def write_docs(model, comp, nav):
    chk = json.load(open(os.path.join(HERE, 'checks.json')))
    methods = fill_methods(model, comp, nav, chk)
    open(os.path.join(HERE, 'METHODS_3D.md'), 'w', encoding='utf-8').write(methods)
    req = requests_md()
    open(os.path.join(HERE, 'REQUESTS_FOR_LIOR.md'), 'w', encoding='utf-8').write(req)
    src = open(os.path.join(HERE, 'SOURCES_3D.md'), encoding='utf-8').read()
    ann = sorted(f for f in os.listdir(os.path.join(HERE, 'annotated')) if f.lower().endswith(('.png', '.jpg')))
    docs = {'methods_md': methods, 'sources_md': src, 'requests_md': req, 'annotated': ann, 'built': TODAY}
    txt = '// generated by build_3d.py on %s - do not edit by hand' % TODAY + chr(10) + 'window.REEF_DOCS = ' + json.dumps(docs, ensure_ascii=False, separators=(',', ':')) + ';' + chr(10)
    open(os.path.join(HERE, 'docs.js'), 'w', encoding='utf-8').write(txt)
    return len(methods), len(src), len(txt)


if __name__ == '__main__':
    model, comp, G = build()
    json.dump(comp, open(os.path.join(HERE, 'computed.json'), 'w'), indent=1)
    n = write_model_js(model)
    nm, ns, nd = write_docs(model, comp, json.load(open(os.path.join(HERE, 'navionics_profile.json'))))
    print('METHODS_3D.md chars', nm, '| SOURCES chars', ns, '| docs.js bytes', nd)
    print('model.js bytes', n, '| versions', [(v['id'], v['volume_m3_default'], v['bed_for_2800_m3']) for v in model['versions']])
