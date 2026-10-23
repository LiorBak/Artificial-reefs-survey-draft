"""Assemble 08_paper/data/reefs.json, reefs_table.csv, gaps.md from the per-reef modules in reefs/.
Run: python3 -I build_reefs.py     (read-only access to the repo sources; writes only inside 08_paper/data)"""
import sys, os, json, csv, importlib.util, glob, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from common import ROOT
D = f'{ROOT}/08_paper/data'
SLUGS = ['narrowneck-gold-coast', 'cables-reef-wa', 'prattes-reef-el-segundo', 'mount-maunganui-reef', 'opunake-reef', 'boscombe-surf-reef', 'kovalam-reef-india',
         'borth-coastal-defence-reef', 'palm-beach-gold-coast', 'southern-ocean-surf-reef-albany', 'burkitts-reef-bargara', 'bunbury-airwave', 'mexico-reef-2026-unnamed']
ORDER = ['name', 'country', 'lat', 'lon', 'year_built', 'year_completed', 'purpose', 'material', 'volume_m3', 'footprint_area_m2', 'plan_length_alongshore_m', 'plan_length_crossshore_m', 'reef_height_m',
         'crest_depth_msl_m', 'crest_depth_lat_m', 'seabed_depth_toe_m', 'seabed_depth_at_crest_m', 'depth_gap_m', 'seaward_ramp_length_m', 'mean_seaward_slope', 'distance_offshore_crest_m',
         'tide_spring_range_m', 'tide_mean_range_m', 'tide_range_type', 'tide_source', 'swell_hs_m', 'swell_tp_s', 'swell_dir', 'design_wave', 'arm_angle_to_shoreline_deg', 'arm_angle_to_swell_deg', 'surf_outcome', 'surfable_days_per_year',
         'durability', 'sediment_shoreline_outcome', 'cost_local', 'cost_usd', 'cost_usd_2024', 'shape_on_page', 'model_3d']
FX = json.load(open(f'{D}/fx_worldbank.json'))
WB = 'World Bank, World Development Indicators: PA.NUS.FCRF "Official exchange rate (LCU per US$, period average)" and FP.CPI.TOTL "Consumer price index (2010 = 100)", USA; https://api.worldbank.org/v2 ; fetched 2026-10-15'

def load_module(slug):
    p = f'{os.path.dirname(os.path.abspath(__file__))}/reefs/{slug.replace("-", "_")}.py'
    if not os.path.exists(p): return None
    spec = importlib.util.spec_from_file_location(slug.replace('-', '_'), p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def add_usd(r):
    c = r.f.get('cost_local')
    if not c or c.get('value') is None: r.U('cost_usd', 'USD', 'no local cost value'); r.U('cost_usd_2024', 'USD', 'no local cost value'); return
    cur, yr = c['currency'], str(c['price_year'])
    fx = FX['fx'][cur].get(yr)
    if fx is None: r.U('cost_usd', 'USD', f'no FX for {cur} {yr}'); r.U('cost_usd_2024', 'USD', 'no FX'); return
    nominal = c['value'] / fx
    cpi_b = FX['cpi_usa'].get('2024'); cpi_y = FX['cpi_usa'].get(yr) or cpi_b
    r.F('cost_usd', round(nominal, -3), f'USD (nominal, {yr})', 'D', 'repo:' + WB, f'cost_local {c["value"]:,} {cur} ({yr}) / {fx:.4f} {cur} per USD (period average {yr})',
        note=f'DERIVED = local amount / World Bank annual-average official exchange rate. ASSUMPTION: the price year of cost_local ({yr}) is the year of the FX rate (see the note of cost_local). Not inflation adjusted.')
    r.F('cost_usd_2024', round(nominal * cpi_b / cpi_y, -3), 'USD (2024 prices)', 'D', 'repo:' + WB, f'nominal USD x CPI_USA(2024) {cpi_b:.2f} / CPI_USA({yr}) {cpi_y:.2f}',
        note='DERIVED; US CPI (World Bank FP.CPI.TOTL, 2010 = 100) used as the deflator; 2025 CPI was not yet published by the source.')

# What the field tide_spring_range_m holds for each reef (its name is kept for the pipeline) and the official source (tides_check.md, 2026-10-19)
_SPR = 'spring range (MHWS - MLWS)'
_ANN = 'predicted annual range (approx. LAT-HAT), WA DoT 2026; not a spring range'
_DOT = 'WA DoT / BoM Tide Predictions by Location WA 2026 (heights above LAT)'
TIDE_META = {
    'narrowneck-gold-coast': (_SPR, 'MSQ Semidiurnal Tidal Planes 2026, Gold Coast Seaway'),
    'palm-beach-gold-coast': (_SPR, 'MSQ Semidiurnal Tidal Planes 2026, Gold Coast Seaway'),
    'cables-reef-wa': (_ANN, _DOT + ', Fremantle (+0.30 to +1.44 m)'),
    'prattes-reef-el-segundo': ('great diurnal range GT (MHHW - MLLW); mean = MN; not a spring range', 'NOAA CO-OPS datums, station 9410840 Santa Monica (GT 1.654, MN 1.145)'),
    'mount-maunganui-reef': (_SPR, 'LINZ Standard port tidal levels 2026-27, Tauranga'),
    'opunake-reef': (_SPR + ', Port Taranaki', 'LINZ Standard port tidal levels 2026-27, Port Taranaki (MHWS 3.56, MLWS 0.40)'),
    'boscombe-surf-reef': (_SPR, 'Mead et al. 2010 Table 1 (Bournemouth gauge); Admiralty value not retrieved'),
    'kovalam-reef-india': ('undefined "tide range" (Blacka 2013 Table 4.3)', 'Blacka et al. 2013 Table 4.3 p.68 (approx.); no official source reached'),
    'borth-coastal-defence-reef': (_SPR, 'West of Wales SMP2 water-level table p.4C.3 (Aberystwyth)'),
    'southern-ocean-surf-reef-albany': (_ANN, _DOT + ', Albany (+0.09 to +1.47 m)'),
    'burkitts-reef-bargara': (_SPR + ', Burnett Heads', 'MSQ Semidiurnal Tidal Planes 2026, Burnett Heads (not independently verified)'),
    'bunbury-airwave': (_ANN, _DOT + ', Bunbury (+0.10 to +1.30 m)'),
    'mexico-reef-2026-unnamed': (None, None),
}

def add_tide_meta(r, slug):
    t, s = TIDE_META[slug]
    if t is None:
        r.U('tide_range_type', 'text', 'no tide value recorded'); r.U('tide_source', 'text', 'no tide value recorded'); return
    r.F('tide_range_type', t, 'text', 'S', None, 'what tide_spring_range_m holds for this reef (see unit of that field)')
    r.F('tide_source', s, 'text', 'S', None, 'full citations are in the source list of tide_spring_range_m')

def short_src(rec):
    keys = rec.get('src_keys', '')
    s = (keys if not keys.startswith('repo:') else 'repo: ' + keys[5:90]) + (' | ' + rec['location'] if rec.get('location') else '')
    return re.sub(r'\s+', ' ', s)[:230]

def flat(v):
    if isinstance(v, list): return '; '.join(str(x) for x in v)
    return '' if v is None else str(v)

def main():
    reefs = []; refs_all = {}
    for slug in SLUGS:
        m = load_module(slug)
        if m is None: print('MISSING MODULE', slug); continue
        r = m.build()
        add_usd(r)
        add_tide_meta(r, slug)
        for f in ORDER:
            if f not in r.f and f != 'slug': r.U(f, '', 'not recorded in this dataset version')
        obj = {'slug': slug}
        for f in ORDER + [k for k in r.f if k not in ORDER]: obj[f] = r.f[f]
        obj['_references'] = r.used
        obj['_status_counts'] = {s: sum(1 for k, f in r.f.items() if f['status'] == s and k not in ('tide_range_type', 'tide_source')) for s in ('sourced', 'derived', 'assumed', 'unknown')}
        reefs.append(obj)
    json.dump(reefs, open(f'{D}/reefs.json', 'w'), indent=1, ensure_ascii=False)
    cols = ['slug']
    for f in ORDER: cols += [f, f + '__unit', f + '__status', f + '__src']
    with open(f'{D}/reefs_table.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh); w.writerow(cols)
        for o in reefs:
            row = [o['slug']]
            for f in ORDER:
                rec = o[f]; row += [flat(rec['value']), rec.get('unit', ''), rec['status'], short_src(rec)]
            w.writerow(row)
    # core numeric table (one number per cell, for plots and regressions)
    def num(v):
        try: return float(v) if not isinstance(v, bool) and v is not None and not isinstance(v, (list, str)) else ('' if isinstance(v, (list,)) else (float(v) if re.fullmatch(r'-?\d+(\.\d+)?', str(v)) else ''))
        except Exception: return ''
    core = ['lat', 'lon', 'year_built', 'volume_m3', 'footprint_area_m2', 'plan_length_alongshore_m', 'plan_length_crossshore_m', 'reef_height_m', 'crest_depth_msl_m', 'crest_depth_lat_m', 'seabed_depth_toe_m', 'seabed_depth_at_crest_m',
            'depth_gap_m', 'seaward_ramp_length_m', 'mean_seaward_slope', 'distance_offshore_crest_m', 'tide_spring_range_m', 'tide_mean_range_m', 'surfable_days_per_year', 'cost_usd', 'cost_usd_2024']
    with open(f'{D}/reefs_core.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh); w.writerow(['slug', 'name', 'country', 'purpose', 'surf_outcome', 'shape_on_page', 'model_3d_yes'] + sum([[c, c + '_status'] for c in core], []) + ['cost_local_amount', 'cost_local_currency', 'cost_local_price_year'])
        for o in reefs:
            row = [o['slug'], o['name']['value'], o['country']['value'], o['purpose']['value'], o['surf_outcome']['value'], o['shape_on_page']['value'], 'yes' if str(o['model_3d']['value']).startswith('yes') else 'no']
            for c in core: row += [num(o[c]['value']), o[c]['status']]
            cl = o['cost_local']; row += [cl['value'] if cl['value'] is not None else '', cl.get('currency', ''), cl.get('price_year', '')]
            w.writerow(row)
    # gaps
    out = ['# Gaps per reef (what is unknown, assumed or weak) - generated by src/build_reefs.py + manual notes in src/gaps_manual.py', '']
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import gaps_manual; GM = gaps_manual.GAPS
    except Exception as e: GM = {}; print('no gaps_manual', e)
    for o in reefs:
        out.append(f'## {o["slug"]} - {o["name"]["value"]}')
        out.append(f'Status counts: {o["_status_counts"]}')
        un = [f for f in ORDER if o[f]['status'] == 'unknown']; asm = [f for f in ORDER if o[f]['status'] == 'assumed']
        out.append('- UNKNOWN fields: ' + (', '.join(un) if un else 'none'))
        for f in un:
            if o[f].get('note'): out.append(f'  - {f}: {o[f]["note"]}')
        out.append('- ASSUMED fields: ' + (', '.join(asm) if asm else 'none'))
        for f in asm:
            out.append(f'  - {f}: {o[f]["location"] if o[f].get("location") else ""} {o[f].get("note", "")}'.rstrip())
        for g in GM.get(o['slug'], []): out.append('- ' + g)
        out.append('')
    open(f'{D}/gaps.md', 'w', encoding='utf-8').write('\n'.join(out))
    json.dump(sorted(set(common.WARN)), open('/tmp/claude-0/paper/data/warn.json', 'w'))
    print('reefs', len(reefs), 'warnings', common.WARN)
    tot = {s: sum(o['_status_counts'][s] for o in reefs) for s in ('sourced', 'derived', 'assumed', 'unknown')}; print(tot)

if __name__ == '__main__': main()
