#!/usr/bin/env python3
"""run_all.py - rerun the whole 08_paper analysis in order (about 3 minutes). Usage: python3 08_paper/analysis/run_all.py"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for s in ['hypsometry.py', 'surf_analysis.py', 'coastal_analysis.py', 'stability_analysis.py', 'israel_analysis.py', 'summarize.py', 'post_break.py']:
    print('==', s, flush=True)
    r = subprocess.run([sys.executable, os.path.join(HERE, s)], env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    if r.returncode:
        sys.exit('failed: ' + s)
