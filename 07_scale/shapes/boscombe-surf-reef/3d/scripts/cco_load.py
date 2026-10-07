"""Load the saved CCO profile text files into canonical (x, y, z_ODN) arrays (helper for cco_fetch.py outputs)."""
import sys, glob, re
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from canon import osgb2can
SRC = HERE.parents[1] / "src" / "cco_profiles"

def load(pid, date):
    f = SRC / f"{pid}_{date}.txt"
    rows = [ln.split("\t") for ln in f.read_text().splitlines()[1:] if ln.strip()]
    E = np.array([float(r[0]) for r in rows]); N = np.array([float(r[1]) for r in rows]); Z = np.array([float(r[2]) for r in rows])
    ch = np.array([float(r[3]) for r in rows]); fc = [r[4].strip() for r in rows]
    can = osgb2can(E, N)
    return dict(pid=pid, date=date, E=E, N=N, z=Z, ch=ch, fc=fc, x=can[:, 0], y=can[:, 1])

def dates(pid):
    return sorted(re.match(rf"{pid}_(.*)\.txt", p.name).group(1) for p in SRC.glob(f"{pid}_*.txt"))
