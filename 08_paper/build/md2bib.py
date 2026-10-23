#!/usr/bin/env python3
"""Build references.bib (and citekeys.json) from ../sections/10_references.md.

Usage (from 08_paper/build/):  python3 md2bib.py
Parses the APA-style entries heuristically; entries that the heuristic cannot
read are listed on stdout as FALLBACK. Hand fixes are in OVERRIDES below.
Trailing [bracketed notes] and "(not verified)" go to `addendum` so that
Lior's verification notes stay visible in the reference list.
"""
import re, json, pathlib, unicodedata

here = pathlib.Path(__file__).resolve().parent
src = (here.parent / 'sections' / '10_references.md').read_text(encoding='utf-8')

MONTHS = {m: i + 1 for i, m in enumerate(
    ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
     'September', 'October', 'November', 'December'])}
DATE = (r'(?:\d{4}[a-z]?(?:-\d{4})?(?:, [A-Z][a-z]+(?:-[A-Z][a-z]+)?(?: \d+)?)?'
        r'|n\.d\.(?:-[a-z])?|c\. \d{4})')


def ascii_slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]', '', s.lower())


def tex(s):
    """Escape LaTeX specials in plain text (markdown *emphasis* handled by caller)."""
    s = s.replace('\\', r'\textbackslash{}')
    for a, b in (('&', r'\&'), ('%', r'\%'), ('$', r'\$'), ('#', r'\#'), ('_', r'\_')):
        s = s.replace(a, b)
    s = re.sub(r'\*([^*]+)\*', r'\\emph{\1}', s)
    s = s.replace('`', "'")
    return s


def parse_people(a):
    """Return list of (family, given) or None if corporate."""
    a = a.strip().rstrip(',')
    pos, out = 0, []
    pat = re.compile(r"\s*(?:&\s*)?([^,&]+?),\s*((?:[A-Z]\.\s?(?:-?[A-Z]\.\s?)*)(?:Jr\.)?)\s*(?:,|$)")
    while pos < len(a):
        m = pat.match(a, pos)
        if not m:
            mm = re.match(r'\s*&\s*([A-Z][a-z]+)\.?\s*$', a[pos:])
            if mm and out:
                out.append((mm.group(1), '')); break
            return None
        out.append((m.group(1).strip(), m.group(2).strip()))
        pos = m.end()
    return out or None


entries = []
body = src.split('## Works cited only')[0]
for para in re.split(r'\n\s*\n', body):
    para = ' '.join(para.split())
    if not para or para.startswith('#') or para.startswith('Alphabetical'):
        continue
    entries.append(para)

keys_used = {}
bib = []
meta = []  # for the citation converter
fallback = []

for e in entries:
    m = re.match(r'^(.*?) \((' + DATE + r')\)\.\s*(.*)$', e)
    if not m:
        fallback.append(('NOHEAD', e[:100])); continue
    auth, date, rest = m.groups()
    # ---- authors
    people = parse_people(auth)
    if people:
        authbib = ' and '.join(f'{f}, {g}' if g else f for f, g in people)
        fam = [f for f, g in people]
        n = len(fam)
        if n == 1: narr = par = fam[0]
        elif n == 2: narr, par = f'{fam[0]} and {fam[1]}', f'{fam[0]} & {fam[1]}'
        else: narr = par = f'{fam[0]} et al.'
        slug = ascii_slug(fam[0])
    else:
        corp = re.sub(r'\s*\[[^\]]*\]', '', auth).strip().rstrip('.')
        authbib = '{' + corp + '}'
        narr = par = corp
        words = re.findall(r'[A-Za-z0-9]+', corp)
        slug = ascii_slug(''.join(words[:2])) if len(words) > 1 else ascii_slug(words[0])
        if corp.startswith('Western Australia Department'): slug = 'wadot'
        if corp.startswith('Government Company'): slug = 'mccp'
        if corp.startswith('Esri'): slug = 'esri'
        if corp.startswith('US Army Coastal'): slug = 'cerc'
        if corp.startswith('US Army Corps'): slug = 'usace'
        if corp.startswith('Royal Commission'): slug = 'rcahmw'
        if corp.startswith('NOAA Center'): slug = 'noaacops'
        if corp.startswith('NOAA National'): slug = 'noaandgc'
    # ---- date
    dm = re.match(r'^(\d{4})([a-z]?)(?:-(\d{4}))?(?:, ([A-Z][a-z]+)(?:-([A-Z][a-z]+))?(?: (\d+))?)?$', date)
    suffix = ''
    fields = {}
    if dm:
        y, suffix, y2, mon, mon2, day = dm.groups()
        ylabel = y + suffix + (('-' + y2) if y2 else '')
        if y2:
            fields['date'] = f'{y}/{y2}'
        elif mon and not mon2:
            fields['date'] = f'{y}-{MONTHS[mon]:02d}' + (f'-{int(day):02d}' if day else '')
        else:
            fields['date'] = y
            if mon2: fields['month'] = f'{mon}-{mon2}'
        ykey = y + suffix + (y2 or '')
    elif date.startswith('n.d.'):
        suffix = date[5:] if len(date) > 5 else ''
        ylabel = date
        ykey = 'nd' + suffix.lstrip('-')
        fields['date'] = ''
    else:  # c. 2000
        ylabel = date; ykey = 'c' + date[-4:]
        fields['date'] = date[-4:]
    # key
    key = slug + ykey
    if key in keys_used:
        i = 2
        while f'{key}{chr(96+i)}' in keys_used: i += 1
        key = f'{key}{chr(96+i)}'
    keys_used[key] = e[:60]
    # ---- url / doi / notes
    notes = []
    rest = rest.strip()
    while True:
        m2 = re.search(r'\s*\[([^\[\]]*)\]\.?\s*$', rest)
        m3 = re.search(r'\s*\((not verified|accessed [^)]*)\)\.?\s*$', rest)
        if m2 and ('http' in rest[:m2.start()] or not re.search(r'\[[^\]]*\]\s*\.', rest[:m2.start()]) or True) and (
                rest[:m2.start()].count('[') == rest[:m2.start()].count(']')) and (
                'http' in rest[:m2.start()] or '. ' in rest[:m2.start()] or rest[:m2.start()].endswith('.')):
            notes.insert(0, '[' + m2.group(1).strip() + ']'); rest = rest[:m2.start()]; continue
        if m3:
            notes.insert(0, '(' + m3.group(1) + ')'); rest = rest[:m3.start()]; continue
        break
    url = doi = None
    um = re.search(r'\s*(https?://\S+?)\.?\s*(?=\(accessed|\(file|$)', rest)
    um_all = list(re.finditer(r'https?://\S+', rest))
    if um_all:
        u = um_all[-1]
        url = u.group(0).rstrip('.')
        import urllib.parse
        url = urllib.parse.quote(url, safe="%:/?#[]@!$&'()*+,;=~-._")
        rest = (rest[:u.start()] + rest[u.end():]).strip()
        rest = re.sub(r'\s+', ' ', rest)
        dmm = re.match(r'https?://(?:dx\.)?doi\.org/(.+)$', url)
        if dmm: doi, url = dmm.group(1), None
    rest = rest.strip()
    # trailing parenthetical about accessed etc. stay in rest
    # ---- type and container
    typ = 'misc'
    b = rest
    origdate = None
    om = re.search(r'\s*\(Original work published (\d{4})[^)]*\)\.?', b)
    if om:
        origdate = om.group(1); b = b[:om.start()] + b[om.end():]
    b = b.strip()
    if b.endswith(' .'): b = b[:-2]
    f = fields
    kind = None
    mi = re.match(r'^(.+?)\. In (?:(.+?) \(Eds?\.\), )?\*([^*]+)\*(.*)$', b)
    ma = re.match(r'^([^*]+?)\. \*([^*]+)\*(.*)$', b)
    mb = re.match(r'^\*([^*]+?)\.?\*(.*)$', b)
    if mi:
        typ = 'inproceedings'
        f['title'] = mi.group(1)
        f['booktitle'] = mi.group(3)
        if mi.group(2):
            eds = re.findall(r'([A-Z]\.(?: ?[A-Z]\.)*) ([A-Za-z\-]+)(?: &|$)', mi.group(2) + ' ')
            f['editor'] = ' and '.join(f'{s}, {i}' for i, s in eds) if eds else '{' + mi.group(2) + '}'
        tail = mi.group(4).strip()
        pm = re.match(r'^\s*\(pp\. ([^)]+)\)\.?(.*)$', tail)
        if pm:
            f['pages'] = pm.group(1); tail = pm.group(2)
        tail = tail.strip(' .')
        if tail: f['publisher'] = tail
        kind = 'proc'
    elif ma and not b.startswith('*'):
        typ = 'article'
        title, jt, tail = ma.groups()
        f['title'] = title
        # journal part inside italics: "Name, vol"
        jm = re.match(r'^(.*?), (\d+[A-Za-z]?|[A-Z]?\d+[a-z]?)$', jt)
        if jm: jt, vol = jm.groups()
        else: vol = None
        f['journaltitle'] = jt
        if vol: f['volume'] = vol
        tail = tail.strip()
        im = re.match(r'^\((\d+(?:-\d+)?)\)(.*)$', tail)
        if im:
            f['number'] = im.group(1); tail = im.group(2)
        tail = tail.strip(' ,.')
        if tail:
            if re.match(r'^[\w.\-]+(?:\.\d+)?$', tail) and re.search(r'\d', tail):
                f['pages'] = tail
            else:
                f['addendum_tail'] = tail
        kind = 'art'
    elif mb:
        title, tail = mb.groups()
        f['title'] = title
        tail = tail.strip()
        sm = re.match(r'^\(([^)]*)\)(.*)$', tail)
        if sm:
            f['series'] = sm.group(1); tail = sm.group(2).strip()
        dm2 = re.match(r'^\[([^\]]*)\](.*)$', tail)
        if dm2:
            f['titleaddon'] = dm2.group(1); tail = dm2.group(2).strip()
        tail = tail.strip(' .')
        low = (f.get('titleaddon', '') or '').lower()
        if 'dissertation' in low or 'thesis' in low:
            typ = 'thesis'
            tm = re.match(r'^(.*?),\s*(.*)$', f.pop('titleaddon'))
            f['type'] = tm.group(1); f['institution'] = tm.group(2)
            if tail: f['addendum_tail'] = tail
        else:
            typ = 'misc'
            if tail: f['publisher'] = tail
        kind = 'ital'
    else:
        # plain title; maybe "Title. Publisher" without italics
        typ = 'online' if url else 'misc'
        parts = b.split('. ', 1)
        f['title'] = parts[0].strip(' .')
        if len(parts) > 1 and parts[1].strip(' .'):
            f['publisher'] = parts[1].strip(' .')
        kind = 'plain'
    f['author'] = authbib
    if doi: f['doi'] = doi
    if url: f['url'] = url
    if origdate: f['origdate'] = origdate
    if suffix.startswith('-') or (suffix and date.startswith('n.d.')): pass
    if (suffix and not date.startswith('n.d.')) or date.startswith('n.d.-'):
        f['sorttitle'] = suffix.lstrip('-')  # keep the md letters
    adds = notes[:]
    if f.get('addendum_tail'): adds.insert(0, f.pop('addendum_tail'))
    if adds: f['addendum'] = ' '.join(adds)
    meta.append(dict(key=key, narr=narr, par=par, year=ylabel, type=typ, kind=kind, raw=e))
    bib.append((typ, key, f))

OVERRIDES = {}
exec((here / 'bib_overrides.py').read_text(encoding='utf-8')) if (here / 'bib_overrides.py').exists() else None


def fmt(v, k):
    if k in ('doi', 'url', 'date', 'origdate', 'month', 'sorttitle', 'pages', 'volume', 'number', 'author', 'editor'):
        if k in ('author', 'editor'):
            return v.replace('&', r'\&') if not v.startswith('{') else '{' + v[1:-1].replace('&', r'\&') + '}'
        return v.replace('_', r'\_') if k == 'sorttitle' else v
    if 'http' in v:   # URLs inside notes: clickable and breakable
        out, pos = '', 0
        for m in re.finditer(r'https?://[^\s\]]+', v):
            u = m.group(0); tail = ''
            while u and u[-1] in '.,;)': tail = u[-1] + tail; u = u[:-1]
            out += tex(v[pos:m.start()]) + '\\url{' + u.replace('%', r'\%').replace('#', r'\#').replace('&', r'\&') + '}' + tex(tail)
            pos = m.end()
        return out + tex(v[pos:])
    return tex(v)


out = []
for typ, key, f in bib:
    if typ in ('misc', 'online') and 'series' in f and key != 'dean1991':
        f['title'] += ' (' + f.pop('series') + ')'
    ov = OVERRIDES.get(key)
    if ov:
        if 'type' in ov and ov['type'] is None: pass
        for k, v in ov.items():
            if k == '_type': typ = v
            elif v is None: f.pop(k, None)
            else: f[k] = v
    lines = [f'@{typ}{{{key},']
    order = ['author', 'editor', 'date', 'origdate', 'month', 'sorttitle', 'title', 'titleaddon', 'journaltitle',
             'booktitle', 'series', 'volume', 'number', 'pages', 'type', 'institution', 'publisher', 'doi', 'url', 'addendum']
    for k in order + [x for x in f if x not in order]:
        if k in f and not (k == 'date' and f[k] == ''):
            v = f[k]
            if k == 'sorttitle': pass
            lines.append(f'  {k} = {{{fmt(v, k)}}},')
    lines.append('}')
    out.append('\n'.join(lines))

# secondary sources: cite works, but not listed (skipbib)
SEC = '''
@misc{shand2011,
  author = {Shand, T. D.},
  date = {2011},
  title = {Making waves? A philosophical review of artificial surfing reef projects},
  addendum = {Submitted to Shore and Beach; cited as quoted in Mead and Borrero (2011)},
  options = {skipbib},
}
@misc{weppe2007,
  author = {Weppe, S. and others},
  date = {2007},
  title = {Mount Maunganui monitoring},
  addendum = {Cited as quoted in Blacka et al. (2013, p. 103)},
  options = {skipbib},
}
@misc{geofabrics2013,
  author = {{Geofabrics}},
  date = {2013},
  title = {Design life of geotextile containers},
  addendum = {Cited as quoted in Blacka et al. (2013, p. 35)},
  options = {skipbib},
}
'''
meta += [dict(key='shand2011', narr='Shand', par='Shand', year='2011', type='misc', kind='sec', raw=''),
         dict(key='weppe2007', narr='Weppe et al.', par='Weppe et al.', year='2007', type='misc', kind='sec', raw=''),
         dict(key='geofabrics2013', narr='Geofabrics', par='Geofabrics', year='2013', type='misc', kind='sec', raw='')]
(here / 'references.bib').write_text('\n\n'.join(out) + '\n' + SEC, encoding='utf-8')
(here / 'citekeys.json').write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding='utf-8')
print('entries in md:', len(entries), ' bib entries:', len(out), '+3 secondary; no-head failures:', fallback)
for mm in meta:
    if mm['kind'] in ('plain', None): print('PLAIN', mm['key'], '|', mm['raw'][:90])
