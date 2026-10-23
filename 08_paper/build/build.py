#!/usr/bin/env python3
"""Rebuild 08_paper/build/paper.pdf. Run from 08_paper/build/: python3 build.py"""
import subprocess, pathlib, sys
here = pathlib.Path(__file__).resolve().parent
root = here.parent
sec = root/'sections'
PB = '\n\n<div style="page-break-before: always;"></div>\n\n'
files = [l.strip() for l in (sec/'ORDER.txt').read_text().split('\n') if l.strip()]
parts = []
for f in files:
    t = (sec/(f if f.endswith('.md') else f+'.md')).read_text()
    if f.startswith('10_references') or f.startswith('appendix_A'):
        t = PB + t
    parts.append(t)
(here/'paper.md').write_text('\n\n'.join(parts))
subprocess.run(['pandoc','paper.md','-f','markdown+pipe_tables+tex_math_dollars','-s','--mathml','--toc','--toc-depth=2',
  '--resource-path',str(root),'-c','paper.css','--embed-resources','-o','paper.html'],cwd=here,check=True)
from playwright.sync_api import sync_playwright
foot = '<div style="width:100%;text-align:center;font-size:8pt;font-family:serif;color:#444;"><span class="pageNumber"></span></div>'
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args=['--no-sandbox','--disable-gpu'])
    pg = b.new_page()
    pg.goto('file://'+str(here/'paper.html')); pg.wait_for_timeout(1500)
    pg.pdf(path=str(here/'paper.pdf'), format='A4', margin=dict(top='2.2cm',bottom='2.4cm',left='2.2cm',right='2.2cm'),
           display_header_footer=True, header_template='<span></span>', footer_template=foot, print_background=True, prefer_css_page_size=False)
    b.close()
