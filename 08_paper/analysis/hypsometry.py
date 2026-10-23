#!/usr/bin/env python3
"""hypsometry.py - plan area and volume of each modelled reef above given levels (the 'active' part that shapes breaking).

Run:    python3 08_paper/analysis/hypsometry.py
Reads:  07_scale/shapes/<slug>/3d/model.js (READ ONLY) through the adapters of extract_profiles.py (same folder; imported,
        not modified), default model version, footprint rule (reef - seabed >= 0.10 m) as in extract_profiles.py.
Writes: 08_paper/analysis/results_hypsometry.json
Method (DERIVED): on the reef grid, area(level) = number of footprint cells with reef surface >= level x cell area;
volume_above(level) = sum over footprint cells of max(reef - max(level, seabed), 0) x cell area; levels relative to the
crest (crest, crest-0.25, ..., crest-3 m) and absolute (m MSL). Cell area from the grid step.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import extract_profiles as ep  # noqa: E402  (read-only reuse of the model adapters)

REL_LEVELS = [0.0, -0.25, -0.5, -1.0, -1.5, -2.0, -3.0]
ABS_LEVELS = [0.0, -0.5, -1.0, -1.5, -2.0, -2.5, -3.0, -4.0]


def one(slug):
    m, mp = ep.load_model(slug)
    a = ep.ADAPTERS[slug](m, mp)
    layer = ep.layer_from(a['rx'], a['ry'], a['RZ'], a['seabed'], a.get('mask'))
    rx, ry = np.asarray(layer['rx']), np.asarray(layer['ry'])
    dx = float(abs(rx[1] - rx[0]))
    dy = float(abs(ry[1] - ry[0]))
    cell = dx * dy
    foot = layer['foot']
    RZ = np.where(foot, layer['RZ'], np.nan)
    SB = layer['SB']
    zc = float(np.nanmax(RZ))
    out = dict(slug=slug, version=a['meta'].get('version_id'), cell_m=[dx, dy], crest_z_msl_m=round(zc, 3),
               footprint_area_m2=round(float(np.sum(foot)) * cell, 1),
               volume_total_m3=round(float(np.nansum(np.where(foot, np.maximum(RZ - SB, 0), 0))) * cell, 1),
               relative=[], absolute=[])
    for lv, key in [(REL_LEVELS, 'relative'), (ABS_LEVELS, 'absolute')]:
        for d in lv:
            level = zc + d if key == 'relative' else d
            sel = foot & (RZ >= level)
            area = float(np.sum(sel)) * cell
            base = np.maximum(level, SB)
            vol = float(np.nansum(np.where(foot, np.maximum(RZ - base, 0), 0))) * cell
            out[key].append(dict(level_m=round(d, 2), level_msl_m=round(level, 3), area_m2=round(area, 1), volume_above_m3=round(vol, 1)))
    return out


def main():
    res = dict(script='08_paper/analysis/hypsometry.py', status='DERIVED from the default 3D model surfaces (read only); footprint = reef - seabed >= 0.10 m',
               reefs={})
    for slug in ep.ADAPTERS:
        try:
            res['reefs'][slug] = one(slug)
            r = res['reefs'][slug]
            print('%-34s crest %6.2f  foot %8.0f m2  vol %8.0f m3  A(crest-0.5) %6.0f  A(crest-1) %6.0f' % (
                slug, r['crest_z_msl_m'], r['footprint_area_m2'], r['volume_total_m3'], r['relative'][2]['area_m2'], r['relative'][3]['area_m2']))
        except Exception as e:  # keep going; record the failure
            res['reefs'][slug] = dict(error=repr(e))
            print(slug, 'ERROR', e)
    with open(os.path.join(HERE, 'results_hypsometry.json'), 'w') as f:
        json.dump(res, f, indent=1)


if __name__ == '__main__':
    main()
