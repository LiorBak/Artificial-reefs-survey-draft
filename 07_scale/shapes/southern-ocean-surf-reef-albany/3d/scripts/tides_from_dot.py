"""tides_from_dot.py - statistics of the 2024 predicted high and low waters at Albany (WA Department of Transport / Bureau of Meteorology
'Tide Predictions by Location', 2024, Albany pages 3-5 of the PDF; datum of predictions = Lowest Astronomical Tide).
Reads ../../src/tides/WA_DoT_BOM_tide_predictions_2024_by_location.pdf, takes every 'HHMM h.hh' pair on the three Albany pages,
writes ../src/tides_derived.json.  Method: all heights printed as extremes (high or low water) are pooled; split at 0.62 m (valley of the
bimodal histogram) into highs and lows; MSL(proxy) = mean of ALL extremes (valid only because highs and lows are roughly symmetric)."""
import pymupdf, re, json, os, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))
pdf = os.path.join(HERE, '..', '..', 'src', 'tides', 'WA_DoT_BOM_tide_predictions_2024_by_location.pdf')
d = pymupdf.open(pdf)
pages = [i for i, p in enumerate(d) if 'SOUTH COAST – ALBANY' in p.get_text()]
vals = []
for i in pages:
    toks = d[i].get_text().split()
    for a, b in zip(toks, toks[1:]):
        if re.fullmatch(r'\d{4}', a) and re.fullmatch(r'\d\.\d\d', b):
            vals.append(float(b))
hi = [v for v in vals if v > 0.62]; lo = [v for v in vals if v <= 0.62]
out = dict(source='WA DoT / BoM Tide Predictions by Location 2024, Albany (LAT 35 02 S, LONG 117 53 E), pages (0-based) %s' % pages,
           datum='Lowest Astronomical Tide (stated on the page)', n_extremes=len(vals),
           max_m=max(vals), min_m=min(vals), mean_all_m=round(st.mean(vals), 3),
           mean_high_m=round(st.mean(hi), 3), mean_low_m=round(st.mean(lo), 3), n_high=len(hi), n_low=len(lo))
json.dump(out, open(os.path.join(HERE, '..', 'src', 'tides_derived.json'), 'w'), indent=1)
print(out)
