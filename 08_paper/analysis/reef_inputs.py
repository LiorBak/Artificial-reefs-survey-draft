#!/usr/bin/env python3
"""reef_inputs.py - assemble the per-reef inputs of the analysis, each with its source (writes inputs_used.json).

Geometry: 08_paper/data/profiles/<slug>.json (DERIVED by extract_profiles.py from the 3D models; lines crest_line,
centreline, second_crest_line at 1 m spacing, z m MSL). Tidal planes: same JSONs (field tidal_planes_m_above_msl; sources
in each JSON key_inputs). Outcome, volume, material: 08_paper/data/reefs.json (each field carries its own citation).
Wave climate and arm angles: SITE table below; each entry says SOURCED (with the source) or ASSUMPTION.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')

B13 = 'Blacka et al. (2013) Table 4.3 p.67-68 (PDF p.79-80)'
# Typical surfing conditions per site. H = typical significant wave height near the site; T = period used for the
# 'site' runs (all runs are repeated for T = 6, 8, 10, 12, 14 s as sensitivity). phi0 = angle between the incident crest
# at the reef and each arm / peel line (deg), for the peel-angle estimate.
SITE = {
    'narrowneck-gold-coast': dict(
        H=1.0, H_src='SOURCED: H ~1 m, ' + B13,
        T=10.0, T_src='ASSUMPTION: no Tp in the sources (reefs.json swell_tp_s unknown; Blacka 2013 A.2 p.100: actual waves shorter period than the design swell); 10 s used, 6-14 s sensitivity',
        phi0=[81.1, 81.1], phi0_src='ASSUMPTION: shore-normal swell at the reef; arms near shore-normal converging seaward by 17.8 deg (reefs.json arm_angle_to_shoreline_deg note) -> each arm 90 - 8.9 = 81.1 deg to the crest. If the SE swell arrived ~49 deg off shore-normal unrefracted (reefs.json gaps note), the angle would be ~41 deg (alt run).',
        phi0_alt=[41.0, 41.0], tide_kind='semidiurnal',
        swell_dir='SE (qualitative; reefs.json swell_dir)'),
    'palm-beach-gold-coast': dict(
        H=1.0, H_src='ASSUMPTION: Narrowneck value (same Gold Coast coast, ' + B13 + ') transferred; no site value in reefs.json',
        T=10.0, T_src='ASSUMPTION (as Narrowneck)',
        phi0=[44.7], phi0_src='ASSUMPTION: crest parallel to the shoreline at the reef; reef long axis 44.7 deg to the shoreline (reefs.json arm_angle_to_shoreline_deg, DERIVED from the toe outline)',
        tide_kind='semidiurnal', swell_dir='SE (reefs.json swell_dir)'),
    'cables-reef-wa': dict(
        H=1.5, H_src='SOURCED: H = 1-2 m summer, 1.5-2.5 m winter, ' + B13 + '; 1.5 m used',
        T=12.0, T_src='ASSUMPTION: no Tp in the sources (reefs.json swell_tp_s unknown); 12 s used for Indian Ocean swell, sensitivity 6-14 s',
        phi0=[45.0, 45.0], phi0_src='SOURCED design value: peel angle ~45 deg between each arm and the wave crest (reefs.json arm_angle_to_swell_deg, design_wave; Lyons 1992 via card R1/R2); the real swell direction is not confirmed',
        tide_kind='mixed', swell_dir='narrow window in the lee of Rottnest Island (reefs.json)'),
    'mount-maunganui-reef': dict(
        H=1.5, H_src='SOURCED: H ~1.5 m, ' + B13 + ' and A.3.1',
        T=11.0, T_src='SOURCED: T ~11 s, ' + B13,
        phi0=[50.1, 54.9], phi0_src='ASSUMPTION: shore-normal swell at the reef; arms 50.1 and 54.9 deg to the shoreline (reefs.json arm_angle_to_shoreline_deg, DERIVED)',
        tide_kind='semidiurnal', swell_dir='unknown (reefs.json)'),
    'prattes-reef-el-segundo': dict(
        H=1.2, H_src='SOURCED: H = 0.9 m summer, 1.5 m winter at El Segundo, ' + B13 + '; mean 1.2 m used',
        T=6.0, T_src='SOURCED: T = 6 s, ' + B13 + ' (probably a mean period; 12 s swell sensitivity)',
        phi0=[44.7, 44.4], phi0_src='DERIVED from the design drawing: arms 44.7 and 44.4 deg to the V axis = assumed swell direction (reefs.json arm_angle_to_swell_deg)',
        tide_kind='mixed', swell_dir='assumed along the V axis (reefs.json)'),
    'boscombe-surf-reef': dict(
        H=0.5, H_src='SOURCED: H ~0.5 m, ' + B13 + ' (typical, not the surf design wave)',
        T=8.0, T_src='ASSUMPTION for surfing swell: 8 s. ' + B13 + ' gives T ~4 s (typical local sea, not surf); both reported',
        T_alt=4.0,
        phi0=[72.9], phi0_src='DERIVED: reef long axis (28.1 deg) vs the crest line of the 191 deg design swell, ignores refraction (reefs.json arm_angle_to_swell_deg)',
        tide_kind='semidiurnal', swell_dir='191 deg design (Mead et al. 2010 via reefs.json)'),
    'borth-coastal-defence-reef': dict(
        H=1.0, H_src='ASSUMPTION: no wave statistics for Borth in the sources (reefs.json swell_hs_m unknown); 1.0 m used',
        T=8.0, T_src='ASSUMPTION: 8 s (Cardigan Bay)',
        phi0=[64.2], phi0_src='ASSUMPTION: shore-normal swell; reef axis 64.2 deg to the shoreline (reefs.json, DERIVED PCA)',
        tide_kind='semidiurnal', swell_dir='unknown'),
    'bunbury-airwave': dict(
        H=1.0, H_src='ASSUMPTION: no wave statistics in the sources; 1.0 m used',
        T=12.0, T_src='ASSUMPTION: 12 s',
        phi0=None, phi0_src='dome (spherical cap): peel angle varies along the circular contour; not computed',
        tide_kind='mixed', swell_dir='unknown'),
    'southern-ocean-surf-reef-albany': dict(
        H=1.0, H_src='SOURCED design range: 0.8-1.3 m wave faces (reefs.json design_wave, RHDHV 2015 via card); 1.0 m used',
        T=13.0, T_src='ASSUMPTION: 13 s Southern Ocean swell refracted into King George Sound',
        phi0=[71.2], phi0_src='ASSUMPTION: crest parallel to the beach at the reef; crest edge 71.2 deg to the shoreline (reefs.json, DERIVED). The real swell at the reef is likely oblique (refraction around the Sound), which would lower the angle.',
        tide_kind='mixed', swell_dir='unknown'),
}

# Israel / Haifa reference conditions
ISRAEL = dict(
    tide_spring_range_m=0.40, tide_neap_range_m=0.15,
    tide_src='Rosen (2001) GLOSS report (via 02_research/israel/israel-wave-climate-and-tides.md R1): ~0.4 m spring, ~0.15 m neap, semidiurnal',
    Hs_surf_min=(0.45, 0.60), Hmax_surf_min=(0.60, 0.80),
    Hs_src="Lior's Shikmona buoy field definition of the minimum surfable wave (LiorBuoy2025; 01_source_notes/lior_suggestions_and_swell_heights.md lines 44-53)",
    Tp_obs=(5.7, 6.2), Tp_forecast=(6.0, 8.0),
    Tp_src="Shikmona buoy readouts 2025-08-06 (Hs 0.69 m, Tp 6.20 s) and 2025-08-15 (Hs 0.81 m, Tp 5.70 s); 4Surfers forecast 6-8 s (LiorBuoy2025)",
    swell_dir_deg=(284, 294), dir_src='LiorBuoy2025 (WNW)',
    lior_break_depth=dict(low=dict(Hs=0.45, Hmax=0.6, no_break=1.45, break_depth=1.3, min_depth=1.15),
                          high=dict(Hs=0.6, Hmax=0.8, no_break=1.7, break_depth=1.5, min_depth=1.35),
                          src='LiorBuoy2025 page 1 depth bands (01_source_notes/lior_suggestions_and_swell_heights.md lines 57-61)'),
    storm=dict(Hs12=(3.0, 3.3), src='Zviely et al. (2009) via 02_research/israel/haifa-bay-sediment-budget.md line 92: breaker-zone Hs exceeded 12 h/yr, CAMERI buoys, used for the ~5 m closure depth'),
    storm_extreme=dict(Hs=5.0, T=15.0, src='Carmel, Inman & Golik (1985) Coastal Engineering 9 (abstract, via israel-wave-climate-and-tides.md R4): storm waves > 5 m Hs, periods up to 15 s'),
    closure_depth_m=5.0, closure_src='Zviely et al. (2009) via haifa-bay-sediment-budget.md line 72',
    lst_m3yr=(60000, 72000), lst_src='Zviely et al. (2007) via haifa-bay-sediment-budget.md line 16: net LST 60,000-72,000 m3/yr at the south Carmel coast before Haifa Bay',
    haifa_trap_m3yr=66000, haifa_trap_src='Zviely et al. (2007, 2009) via haifa-bay-sediment-budget.md line 17: ~5 million m3 trapped at the Haifa Port breakwater 1929-2004, ~66,000 m3/yr',
    seasonal_bed_change_m=1.0, seasonal_src="Lior's observation (PLAN.md insight h-B): about 1 m seasonal bed-level change at Haifa; not yet sourced (ASSUMPTION; 0.5-1.5 m sensitivity)",
)


def tide_model(planes, kind):
    """Spring / neap semidiurnal amplitudes from the tidal planes (m about MSL). ASSUMPTION: semidiurnal sinusoid with a
    linear spring-neap modulation of the amplitude; diurnal inequality and Poole Bay double high water ignored."""
    p = planes
    if 'MHWS' in p and 'MLWS' in p:
        As = (p['MHWS'] - p['MLWS']) / 2
        An = (p['MHWN'] - p['MLWN']) / 2 if 'MHWN' in p and 'MLWN' in p else 0.5 * As
        basis = 'MHWS/MLWS and MHWN/MLWN'
    elif 'ANN_HI' in p and 'ANN_LO' in p:
        As = (p['ANN_HI'] - p['ANN_LO']) / 2
        An = 0.5 * As
        basis = 'WA DoT 2026 predicted annual range (approx. LAT-HAT, centred on MSL) as the spring-amplitude proxy; neap = 0.5 spring (ASSUMPTION)'
    elif 'MHHW' in p and 'MLLW' in p:
        As = (p['MHHW'] - p['MLLW']) / 2
        if 'MHW' in p and 'MLW' in p:
            Am = (p['MHW'] - p['MLW']) / 2
            An = max(0.25 * As, 2 * Am - As)
            basis = 'MHHW/MLLW (spring proxy) and MHW/MLW (mean) -> neap = 2 mean - spring'
        else:
            An = 0.5 * As
            basis = 'MHHW/MLLW (spring proxy); neap = 0.5 spring (ASSUMPTION)'
    else:
        raise ValueError('no tidal planes')
    hi = max(p.get(k, -9) for k in ('HAT', 'MHWS', 'ANN_HI', 'MHHW'))
    lo = min(p.get(k, 9) for k in ('LAT', 'MLWS', 'ANN_LO', 'MLLW'))
    sh = p.get('MHWS', p.get('ANN_HI', p.get('MHHW')))
    sl = p.get('MLWS', p.get('ANN_LO', p.get('MLLW')))
    z0 = (sh + sl) / 2   # mean of the spring high/low planes (not exactly 0 at Bunbury and Albany)
    return dict(A_spring=round(As, 3), A_neap=round(An, 3), z0=round(z0, 3), basis=basis, kind=kind, extreme_hi=hi, extreme_lo=lo)


def tide_levels(planes):
    """Low / mid / high water levels for the scenario runs: MLWS (or ANN_LO / MLLW), MSL, MHWS (or ANN_HI / MHHW)."""
    lo = planes.get('MLWS', planes.get('ANN_LO', planes.get('MLLW')))
    hi = planes.get('MHWS', planes.get('ANN_HI', planes.get('MHHW')))
    return dict(low=lo, mid=0.0, high=hi)


def reef_record(r, slug):
    """Small dict of reefs.json fields used here: value + status + location (+source list)."""
    keys = ['name', 'country', 'year_built', 'purpose', 'material', 'volume_m3', 'surf_outcome', 'surfable_days_per_year',
            'durability', 'sediment_shoreline_outcome', 'tide_spring_range_m', 'cost_usd_2024', 'distance_offshore_crest_m',
            'arm_angle_to_shoreline_deg', 'arm_angle_to_swell_deg']
    out = {}
    for k in keys:
        v = r.get(k)
        if isinstance(v, dict):
            out[k] = dict(value=v.get('value'), status=v.get('status'), location=v.get('location'),
                          source=(v.get('source') or [None])[0] if isinstance(v.get('source'), list) else v.get('source'))
    return out


def load():
    reefs = {r['slug']: r for r in json.load(open(os.path.join(DATA, 'reefs.json')))}
    out = {}
    for slug, site in SITE.items():
        pj = json.load(open(os.path.join(DATA, 'profiles', slug + '.json')))
        planes = pj['tidal_planes_m_above_msl']
        tide_src = [ki for ki in pj.get('key_inputs', []) if 'tid' in json.dumps(ki).lower() or 'datum' in json.dumps(ki).lower()]
        out[slug] = dict(
            slug=slug, name=pj.get('name'), site=site, planes=planes, tide=tide_model(planes, site['tide_kind']),
            tide_levels=tide_levels(planes), tide_sources=tide_src, profile_json='08_paper/data/profiles/%s.json' % slug,
            version=pj.get('version'), datum=pj.get('datum'), shoreline_definition=pj.get('shoreline_definition'),
            lines=dict({k: dict(profile=v['profile'], metrics=v['metrics'], x_line_m=v.get('x_line_m')) for k, v in pj['lines'].items()},
                       **{'layer:' + lay['name'].split(' ')[0]: dict(profile=lay['lines']['own_crest_line']['profile'],
                                                                      metrics=lay['lines']['own_crest_line']['metrics'],
                                                                      x_line_m=lay['lines']['own_crest_line'].get('x_line_m'),
                                                                      layer_name=lay['name'], layer_note=lay.get('note'))
                          for lay in pj.get('extra_layers', []) if 'own_crest_line' in lay.get('lines', {})}),
            glob=pj.get('global'), reefs_json=reef_record(reefs.get(slug, {}), slug), confidence_3d=pj.get('confidence_3d'))
    return out


def dump(inputs, path=os.path.join(HERE, 'inputs_used.json')):
    slim = {}
    for s, d in inputs.items():
        slim[s] = {k: v for k, v in d.items() if k not in ('lines',)}
        slim[s]['line_metrics'] = {k: v['metrics'] for k, v in d['lines'].items()}
    slim['_israel'] = ISRAEL
    with open(path, 'w') as f:
        json.dump(slim, f, indent=1, default=str)


if __name__ == '__main__':
    inp = load()
    dump(inp)
    for s, d in inp.items():
        print(s, d['tide'], d['tide_levels'])
