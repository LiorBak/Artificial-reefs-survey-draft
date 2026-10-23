#!/usr/bin/env python3
"""Convert plain author-year citations in ../sections/*.md (those in ORDER.txt except 10_references)
to pandoc citation syntax, using citekeys.json written by md2bib.py.
Idempotent. Originals of the first run are kept in build/sections_plain_backup/.
Usage (from 08_paper/build/): python3 md2cite.py [--check]"""
import re, json, sys, pathlib, shutil
here = pathlib.Path(__file__).resolve().parent
sec = here.parent / 'sections'
meta = json.loads((here / 'citekeys.json').read_text(encoding='utf-8'))
D = {}
for m in meta:
    for a in {m['narr'], m['par'], m['narr'].replace(' and ', ' & '), m['par'].replace(' & ', ' and ')}:
        D[(a, m['year'])] = m['key']
D[('MCCP', '2026')] = 'mccp2026'
for a_, y_, k_ in [('Esri et al.', 'n.d.', 'esrind'), ('LINZ', 'n.d.', 'landinformationnd'),
                   ('NOAA CO-OPS', '2026', 'noaacops2026'), ('RCAHMW', '2020', 'rcahmw2020'),
                   ('Western Australia Department of Transport & Bureau of Meteorology', '2024', 'wadot2024'),
                   ('Western Australia Department of Transport & Bureau of Meteorology', '2026', 'wadot2026')]:
    D[(a_, y_)] = k_
authors = sorted({a for a, y in D}, key=len, reverse=True)
def arx(a): return re.escape(a).replace(r'\ ', r'\s+').replace("'", "['’]")
ALT = '|'.join(arx(a) for a in authors)
YEAR = r'(?:\d{4}[a-z]?(?:-\d{4})?|n\.d\.(?:-[a-z])?|c\. \d{4})'
LOC = r'(?:pp?\.|Chapter|Chapters|Ch\.|Tables?|Fig\.|Figs\.|Figures?|Sections?|Eqs?\.|Appendix|abstract)(?:\s[^;]*?)?'
CITE = re.compile(r"(?<![\w@])(?P<a>" + ALT + r"),\s+(?P<y>" + YEAR + r")(?:,\s+(?P<loc>" + LOC + r"))?(?=\s*(?:;|$)|,\s+[a-z])")
POSS = re.compile(r"(?<![\w@])(?P<a>" + ALT + r")(?P<s>['\u2019]s)\s+\((?P<y>" + YEAR + r")(?:,\s+(?P<loc>" + LOC + r"))?\)")
NARR = re.compile(r"(?<![\w@])(?P<a>" + ALT + r")\s+\((?P<y>" + YEAR + r")(?:,\s+(?P<loc>" + LOC + r"))?\)")
GROUP = re.compile(r'\(([^()]*)\)')
count = 0; problems = []

def key_of(a, y):
    a = re.sub(r'\s+', ' ', a.replace('’', "'"))
    return D[(a, y)]

def raw(cmd, loc, key):
    o = '[' + re.sub(r'\s+', ' ', loc.strip()) + ']' if loc else ''
    return '`\\' + cmd + o + '{' + key + '}`{=latex}'

CONT = re.compile(r"\s*;\s*(?P<y>" + YEAR + r")(?:,\s+(?P<loc>" + LOC + r"))?(?=\s*(?:;|$))")

def conv_group(mo):
    """Pure citation groups become [@a; @b]; groups that also hold other text keep their
    parentheses and the citations become raw biblatex \\cite (author, year without parentheses)."""
    global count
    S = mo.group(1)
    ms = list(CITE.finditer(S))
    if not ms: return mo.group(0)
    tail = S[ms[-1].end():].strip(' ;,')
    pres = [re.sub(r'\s+', ' ', S[(ms[i-1].end() if i else 0):m.start()]).strip(' ,;') for i, m in enumerate(ms)]
    plain = (not tail) and all(p == '' or (i == 0 and p in ('for example', 'see', 'see also', 'e.g.')) for i, p in enumerate(pres))
    if not plain:
        out = ''; pos = 0
        for i, m in enumerate(ms):
            out += S[pos:m.start()]
            out += raw('cite', m.group('loc'), key_of(m.group('a'), m.group('y')))
            pos = m.end(); count += 1
            while True:
                c = CONT.match(S, pos)
                if not c or (m.group('a'), c.group('y')) not in [(x, c.group('y')) for x in [m.group('a')]]:
                    break
                try: k2 = key_of(m.group('a'), c.group('y'))
                except KeyError: break
                out += '; ' + raw('citeyear', c.group('loc'), k2); pos = c.end(); count += 1
        out += S[pos:]
        problems.append(('RAW', S[:90]))
        return '(' + out + ')'
    pos = 0; items = []
    for m in ms:
        pre = S[pos:m.start()].replace(';', ',').strip(' ,')
        pre = re.sub(r'\s+', ' ', pre)
        it = (pre + ' ' if pre else '') + '@' + key_of(m.group('a'), m.group('y'))
        if m.group('loc'): it += ', ' + re.sub(r'\s+', ' ', m.group('loc').strip())
        items.append(it); pos = m.end(); count += 1
    return '[' + '; '.join(items) + ']'

def conv_narr(mo):
    global count
    count += 1
    it = '@' + key_of(mo.group('a'), mo.group('y'))
    if mo.group('loc'): it += ' [' + re.sub(r'\s+', ' ', mo.group('loc').strip()) + ']'
    return it

def conv_poss(mo):
    global count
    count += 1
    return mo.group('a') + mo.group('s') + ' (' + raw('citeyear', mo.group('loc'), key_of(mo.group('a'), mo.group('y'))) + ')'

def convert(t):
    t = POSS.sub(conv_poss, t)
    t = GROUP.sub(conv_group, t)
    t = NARR.sub(conv_narr, t)
    return t

if __name__ == '__main__':
    files = [l.strip() for l in (sec / 'ORDER.txt').read_text().split('\n') if l.strip()]
    files = [f if f.endswith('.md') else f + '.md' for f in files if not f.startswith('10_references')]
    bk = here / 'sections_plain_backup'
    for f in files:
        p = sec / f; t = p.read_text(encoding='utf-8')
        if '--check' not in sys.argv:
            bk.mkdir(exist_ok=True)
            if not (bk / f).exists(): shutil.copy(p, bk / f)
            n = convert(t)
            if n != t: p.write_text(n, encoding='utf-8')
    print('converted citations:', count)
    for p in problems: print(p)
