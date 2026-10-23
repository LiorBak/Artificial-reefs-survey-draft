"""Helpers for the paper master dataset (08_paper/data). Read-only access to the repo sources; writes only inside 08_paper/data.
F(...) builds one field record {value, unit, status, source, location, note}. Sources are given as short aliases that are resolved
to FULL citation strings found in the repo (METHODS_3D.md section 8, card references, shape.json references, models3d.json references)
so that no citation detail is typed by hand."""
import json, re, os
ROOT = '/home/user/artificial-reef-survey'
STATUS = {'S': 'sourced', 'D': 'derived', 'A': 'assumed', 'U': 'unknown'}
_cache = {}

def _lines_for(slug):
    """all candidate citation lines for a reef, own files first"""
    if slug in _cache: return _cache[slug]
    out = []
    md = f'{ROOT}/07_scale/shapes/{slug}/3d/METHODS_3D.md'
    if os.path.exists(md):
        t = open(md, encoding='utf8').read()
        i = t.find('## 8. References')
        if i >= 0:
            for ln in t[i:].splitlines()[1:]:
                if ln.startswith('## ') and not ln.startswith('## 8'): break
                if ln.startswith('- '): out.append((ln[2:].strip(), f'METHODS_3D.md s8 ({slug})'))
                elif re.match(r'^\d+\. ', ln): out.append((re.sub(r'^\d+\. ', '', ln).strip(), f'METHODS_3D.md s8 ({slug})'))
        for ln in t.splitlines():
            if ln.startswith('| ') and len(ln) > 60: out.append((ln.strip(), f'METHODS_3D.md source table ({slug})'))
    sp = f'{ROOT}/07_scale/shapes/{slug}/shape.json'
    if os.path.exists(sp):
        s = json.load(open(sp, encoding='utf8'))
        for r in s.get('references') or []:
            c = r.get('citation') or r.get('text') or ''
            u = r.get('url') or ''
            out.append((c + (f' {u}' if u and u not in c else ''), f'shape.json references {r.get("id")} ({slug})'))
    cp = f'{ROOT}/02_research/reefs/{slug}.json'
    if os.path.exists(cp):
        c = json.load(open(cp, encoding='utf8'))
        for r in c.get('references') or []:
            ci = r.get('citation') or r.get('text') or ''
            u = r.get('url') or ''
            out.append((ci + (f' {u}' if u and u not in ci else ''), f'card references {r.get("id")} ({slug})'))
    _cache[slug] = out
    return out

_global = None
def _all_lines():
    global _global
    if _global is None:
        _global = []
        d = json.load(open(f'{ROOT}/04_build/data/models3d.json', encoding='utf8'))
        for r in d['references']:
            _global.append((r['text'] + (f' {r["url"]}' if r.get('url') and r['url'] not in r['text'] else ''), 'models3d.json references'))
        for s in os.listdir(f'{ROOT}/07_scale/shapes'):
            _global += _lines_for(s)
    return _global

WARN = []
def cite(slug, pat):
    """first line matching regex pat: own reef first, then every reef"""
    rx = re.compile(pat, re.I | re.S)
    for ln, where in _lines_for(slug) + _all_lines():
        if rx.search(ln): return ln
    WARN.append(f'NO CITATION for {slug}: {pat}')
    return f'[citation not found in repo for /{pat}/ - not confirmed]'

class Reef:
    def __init__(self, slug, aliases):
        self.slug = slug; self.al = aliases; self.f = {}; self.used = {}
    def src(self, key):
        """key = 'a+b' aliases joined by +; 'repo:...' free text for repository files"""
        out = []
        for k in ([key] if key.startswith('repo:') else key.split('+')):
            if k.startswith('repo:'): out.append(k[5:])
            elif k in self.al:
                c = cite(self.slug, self.al[k]); out.append(c); self.used[k] = c
            else: raise KeyError(f'{self.slug}: unknown alias {k}')
        return out
    def F(self, name, value, unit, st, src, loc, note=None, alts=None, **extra):
        if st not in STATUS: raise ValueError(st)
        rec = {'value': value, 'unit': unit, 'status': STATUS[st], 'source': self.src(src) if src else [], 'location': loc, 'src_keys': src or ''}
        if note: rec['note'] = note
        rec.update(extra)
        if alts:
            rec['alternatives'] = [{'value': a[0], 'label': a[1], 'status': STATUS[a[2]], 'source': self.src(a[3]) if a[3] else [], 'location': a[4]} for a in alts]
        self.f[name] = rec
        return rec
    def U(self, name, unit, note):
        self.f[name] = {'value': None, 'unit': unit, 'status': 'unknown', 'source': [], 'location': '', 'note': note}

# ---- shared aliases (regexes that pick ONE citation line out of the repo's reference lists) ----
GLOBAL_ALIASES = {
    'Blacka2013': r'Blacka, M\.J.*A Review of Artificial Reefs',
    'MeadBorrero2011': r'Mead, S\.T\. and Borrero, J\.C\. \(2011\)',
    'Jackson2007': r'Jackson, L\.A\., Corbett.*2007\).*Narrowneck Reef',
    'Jackson2012': r'Jackson, A\., Tomlinson.*Long.term performance',
    'Corbett2023': r'Corbett.*Narrowneck Artificial Reef Renewal',
    'VieiraDaSilva2021': r'Vieira da Silva.*Sediment pathways',
    'MSQ2026': r'Maritime Safety Queensland \(2026\).*tidal planes',
}
import math
def tide_stats(lv):
    """lv = dict of plane -> z (m MSL). Returns (spring_range, neap_range, mean_range, formula) from MHWS/MHWN/MLWN/MLWS (semidiurnal)"""
    sp = lv['MHWS'] - lv['MLWS']; ne = lv['MHWN'] - lv['MLWN']
    mean = ((lv['MHWS'] + lv['MHWN']) - (lv['MLWS'] + lv['MLWN'])) / 2
    return round(sp, 2), round(ne, 2), round(mean, 2)

PROFILES = json.load(open(f'{ROOT}/08_paper/data/profiles_derived.json')) if os.path.exists(f'{ROOT}/08_paper/data/profiles_derived.json') else {}
def tr(slug, tol='0.25'):
    return PROFILES[slug]['transect_at_crest'][tol]
def med(slug, k):
    p = PROFILES[slug]; return p[f'median_over_columns_{k}'], p[f'p10_{k}'], p[f'p90_{k}']

def _profile_fields(self, slug, crest_primary=None, version_note='', skip_ramp=False, use_median=False):
    """Adds depth_gap_m, seaward_ramp_length_m, mean_seaward_slope DERIVED from the model grid (derive_profiles.py)."""
    P = PROFILES[slug]; t = P['transect_at_crest']['0.25']; ta, tb = P['transect_at_crest']['0.1'], P['transect_at_crest']['0.5']
    srcm = f'repo:07_scale/shapes/{slug}/3d/model.js (default version {P["version"]}) processed by 08_paper/data/src/derive_profiles.py -> 08_paper/data/profiles_derived.json'
    ramp = t['ramp']; gap_model = t['gap']
    gap = (t['toe_depth'] - crest_primary) if crest_primary is not None else gap_model      # primary: toe depth - SOURCED crest depth when one exists
    slope = gap / ramp if ramp else None
    locm = f'transect at the alongshore position x = {t["x"]:.1f} m of the shallowest cell; toe at y = {t["y_toe"]:.0f} m (outline edge), crest edge at y = {t["y_crest_edge"]:.0f} m (seaward-most cell within 0.25 m of the column maximum)'
    mg, mg10, mg90 = med(slug, 'gap'); mr, mr10, mr90 = med(slug, 'ramp'); ms, ms10, ms90 = med(slug, 'slope')
    sens = f'ramp {ta["ramp"]:.1f} m (tol 0.10 m) / {t["ramp"]:.1f} m (0.25) / {tb["ramp"]:.1f} m (0.50)'
    alt = lambda lab, v, loc: (v, lab, 'D', srcm, loc)
    basis = (f'DEPTH GAP = seabed depth at the seaward toe ({t["toe_depth"]:.2f}) - sourced crest depth ({crest_primary:.2f}) on the crest transect' if crest_primary is not None else f'DEPTH GAP = seabed depth at the seaward toe ({t["toe_depth"]:.2f}) - model crest depth ({t["crest_depth"]:.2f}) on the crest transect')
    alts_g = [alt('median over reef columns (p10-p90 %.2f-%.2f)' % (mg10, mg90), round(mg, 2), f'{P["n_columns"]} columns with >= 5 valid cells')]
    if crest_primary is not None: alts_g.insert(0, alt(f'with the model crest depth {t["crest_depth"]:.2f} m (shallowest grid cell)', round(gap_model, 2), 'model.js grid'))
    self.F('depth_gap_m', round(gap, 2), 'm', 'D', srcm, locm, note=f'{basis}. {version_note}', alts=alts_g)
    if not skip_ramp:
        self.F('seaward_ramp_length_m', round(ramp, 1), 'm', 'D', srcm, locm, note=f'Horizontal distance toe -> crest edge. Sensitivity to the crest tolerance: {sens}.',
               alts=[alt('median over reef columns (p10-p90 %.1f-%.1f)' % (mr10, mr90), round(mr, 1), f'{P["n_columns"]} columns')])
        self.F('mean_seaward_slope', round(slope, 3), 'm/m (gap / ramp)', 'D', srcm, locm, note=f'= 1:{1/slope:.1f}. Grid step {P["grid_step_m"]} m. ' + (f'Uses the sourced crest depth {crest_primary} m; with the model crest {t["crest_depth"]:.2f} m the slope is {gap_model/ramp:.3f}.' if crest_primary is not None else ''),
               alts=[alt('median over reef columns (p10-p90 %.3f-%.3f)' % (ms10, ms90), round(ms, 3), f'{P["n_columns"]} columns')])
_pf_orig = _profile_fields
def _pf(self, slug, crest_primary=None, version_note='', skip_ramp=False, use_median=False):
    _pf_orig(self, slug, crest_primary, version_note, skip_ramp)
    if not use_median: return
    # swap: primary = median over reef columns, the crest-transect value becomes the alternative
    for name, k in (('depth_gap_m', 'gap'), ('seaward_ramp_length_m', 'ramp'), ('mean_seaward_slope', 'slope')):
        rec = self.f[name]; mv = med(slug, k)[0]; alt = rec['alternatives'][0]
        old = {'value': rec['value'], 'label': 'crest-transect value (through the single shallowest cell)', 'status': rec['status'], 'source': rec['source'], 'location': rec['location']}
        rec['value'] = round(mv, 3 if k == 'slope' else 2); rec['alternatives'] = [old]
        rec['location'] = f'median over {PROFILES[slug]["n_columns"]} reef columns (p10-p90 in note); the crest-transect is kept as alternative because the reef is a long diagonal mound for which one shore-normal transect is not representative'
        rec['note'] = (rec.get('note') or '') + f' [primary = median over columns: p10 {med(slug, k)[1]:.3f}, p90 {med(slug, k)[2]:.3f}]'
Reef.profile_fields = _pf
