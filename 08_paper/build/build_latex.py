#!/usr/bin/env python3
"""One-command rebuild of the LaTeX/APA PDF.  From 08_paper/build/:  python3 build_latex.py
Pipeline: sections (ORDER.txt, minus 10_references.md) -> paper_tex.md -> pandoc (biblatex, own template)
          -> xelatex + biber (biblatex-apa) -> build/paper.pdf.   Work files and logs go to WORK (scratch).
Prerequisite (once, or after changing 10_references.md): python3 md2bib.py   (writes references.bib)
Citation markup in the sections comes from md2cite.py (already applied; idempotent)."""
import subprocess, pathlib, shutil, os, re, sys
here = pathlib.Path(__file__).resolve().parent
root = here.parent
sec = root / 'sections'
WORK = pathlib.Path(os.environ.get('LATEX_WORK',
        '/tmp/claude-0/-home-user-artificial-reef-survey/a15463be-9870-58d0-a03c-7b5bb85bb876/scratchpad/latex'))
WORK.mkdir(parents=True, exist_ok=True)

# 0. reference groups: ref_groups.csv (+ ref_groups_new.csv, re-read now) -> keywords injected into a work copy of the bib
import csv
groups = {}
for fn in ('ref_groups.csv', 'ref_groups_new.csv'):
    p = here / fn
    if p.exists():
        for row in csv.reader(p.read_text(encoding='utf-8').splitlines()):
            if len(row) >= 2 and row[0].strip() and row[0].strip() != 'key':
                groups[row[0].strip()] = row[1].strip()
bad = sorted(k for k, g in groups.items() if g not in ('academic', 'other'))
if bad:
    sys.exit('Invalid group (must be academic|other) for: ' + ', '.join(bad))
bibtext = (here / 'references.bib').read_text(encoding='utf-8')
bibkeys = re.findall(r'^@\w+\{([^,\s]+),', bibtext, re.M)
REFS = ('\\section*{References}\\addcontentsline{toc}{section}{References}\n'
        '\\printbibliography[keyword=academic,heading=subbibintoc,title={Scholarly and technical sources}]\n'
        '\\printbibliography[keyword=other,heading=subbibintoc,title={Media, web and other non-academic sources}]\n')

# 1. concatenate
files = [l.strip() for l in (sec / 'ORDER.txt').read_text().split('\n') if l.strip()]
parts, seen_app = [], False
for f in files:
    f = f if f.endswith('.md') else f + '.md'
    if f.startswith('10_references'):
        continue          # the list is generated from references.bib
    t = (sec / f).read_text(encoding='utf-8')
    if f.startswith('appendix_'):
        if not seen_app:
            parts.append('\\clearpage\n\n```{=latex}\n\\begingroup\\raggedright\n'+REFS+'\\endgroup\n```\n')
            seen_app = True
        t = '\\clearpage\n\n' + t
    parts.append(t)
if not seen_app:
    parts.append('\n```{=latex}\n\\clearpage\n'+REFS+'```\n')
(WORK / 'paper_tex.md').write_text('\n\n'.join(parts), encoding='utf-8')

# 2. template = pandoc default minus the automatic \printbibliography at the end
tpl = subprocess.run(['pandoc', '-D', 'latex'], capture_output=True, text=True, check=True).stdout
tpl = tpl.replace('\\printbibliography$if(biblio-title)$[title=$biblio-title$]$endif$', '')
(here / 'template.latex').write_text(tpl, encoding='utf-8')
(WORK / 'references.bib').write_text(
    re.sub(r'^(@\w+\{([^,\s]+),)', lambda m: m.group(1) + '\n  keywords = {' + groups.get(m.group(2), 'ungrouped') + '},',
           bibtext, flags=re.M), encoding='utf-8')
# every bib entry (listed or only cited) must have a group: fail loudly
missing = [k for k in bibkeys if k not in groups]
if missing:
    print('ERROR: %d bib keys have no group in ref_groups.csv / ref_groups_new.csv:' % len(missing))
    print('\n'.join('  ' + k for k in missing))
    sys.exit(1)
shutil.copy(here / 'latex_header.tex', WORK / 'latex_header.tex')

# 3. pandoc -> tex
cmd = ['pandoc', 'paper_tex.md', '-f', 'markdown+pipe_tables+tex_math_dollars+raw_tex', '-t', 'latex', '-s',
       '--template', str(here / 'template.latex'), '--biblatex', '--bibliography=references.bib',
       '--toc', '--toc-depth=2', '--include-in-header=latex_header.tex', '--resource-path', str(root), '--lua-filter', str(here / 'xref.lua'), '--lua-filter', str(here / 'tables.lua'),
       '-V', 'documentclass=article', '-V', 'fontsize=11pt', '-V', 'papersize=a4',
       '-V', 'geometry:margin=2.5cm', '-V', 'indent=true', '-V', 'colorlinks=true',
       '-V', 'mainfont=Latin Modern Roman', '-V', 'sansfont=Latin Modern Sans', '-V', 'monofont=Latin Modern Mono',
       '-V', 'mathfont=Latin Modern Math', '-V', 'linestretch=1.08',
       '-M', 'biblio-style=apa', '-M', 'biblatexoptions=backend=biber', '-M', 'biblatexoptions=hyperref=true',
       '-M', 'biblatexoptions=uniquename=false', '-M', 'biblatexoptions=useprefix=true',
       '-o', 'paper.tex']
subprocess.run(cmd, cwd=WORK, check=True)

# 4. xelatex + biber + xelatex x2 (images are found through TEXINPUTS = 08_paper/)
env = dict(os.environ, TEXINPUTS=str(root) + '//:' + os.environ.get('TEXINPUTS', ''))
def run(*a):
    r = subprocess.run(list(a), cwd=WORK, env=env, capture_output=True, text=True)
    return r.returncode
xe = ['xelatex', '-interaction=nonstopmode', '-halt-on-error', 'paper.tex']
rc = run(*xe)
rc_b = run('biber', 'paper')
rc2 = run(*xe); rc3 = run(*xe)
print('xelatex rc', rc, rc2, rc3, ' biber rc', rc_b)
pdf = WORK / 'paper.pdf'
if rc3 == 0 and pdf.exists():
    old = here / 'paper.pdf'
    if old.exists() and not (here / 'paper_html.pdf').exists():
        shutil.copy(old, here / 'paper_html.pdf')
    shutil.copy(pdf, here / 'paper.pdf')
    print('wrote', here / 'paper.pdf')
else:
    print('FAILED; tail of log:')
    print('\n'.join((WORK / 'paper.log').read_text(errors='replace').splitlines()[-15:]))
    sys.exit(1)
