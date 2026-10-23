"""Figures for the seabed extension (re-check run 2026-10-07).  Writes into ../annotated/:
  cco_profile_lines_plan.png        plan view: the 11 CCO beach-profile lines (2010-04-20) on the extended model seabed (z colour), reef toe outline, shorelines
  cco_profiles_cross_sections.png   the 11 profiles z_ODN(=z_MSL) vs y with the model tide lines, the Fig. 9 survey spline (base) and the model seabed at the line x
  seabed_zone_map.png               zone map of the extended seabed grid (codes 0-5), survey extent, reef toe outline, y axis to 650 m
All figures are made from model.js + the raw CCO files only; no new data.
"""
import json, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import extend_seabed as ex

OUT = HERE.parent / "annotated"
M = json.loads(open(HERE.parent / "model.js", encoding="utf8").read().split("=", 1)[1].rstrip().rstrip(";"))
sb = M["seabed"]
nx, ny = sb["nx"], sb["ny"]
Z = np.array(sb["z_cm"]).reshape(ny, nx) / 100.0
C = np.array([int(c) for c in sb["code"]]).reshape(ny, nx)
xs = sb["x0"] + np.arange(nx) * sb["dx"]; ys = sb["y0"] + np.arange(ny) * sb["dy"]
toe = np.array(M["reef"]["toe_polygon_xyzz"])[:, :2]
toe = np.vstack([toe, toe[:1]])
lines = ex.beach_lines()
WL = {w["key"]: w["z"] for w in M["water_levels"]}
CODES = {0: ("Fig. 9 survey (Apr 2011)", "#2a7fbf"), 1: ("spline extrapolation, no data", "#b9b9b9"), 2: ("interpolated under the reef", "#e0b030"),
         3: ("CCO beach profile (2010-04-20)", "#2e9e4f"), 4: ("CCO-to-survey blend (40 m)", "#9fd36a"), 5: ("EMODnet slope extrapolation (+-1.2 m)", "#d9534f")}

# ---- 1. plan of the profile lines on the seabed z
fig, ax = plt.subplots(figsize=(8, 6.8), dpi=130)
im = ax.imshow(Z, origin="lower", extent=(xs[0] - 1, xs[-1] + 1, ys[0] - 1, ys[-1] + 1), cmap="terrain", vmin=-11, vmax=4, aspect="equal")
ax.contour(xs, ys, Z, levels=[WL["LAT"], WL["MLWS"], 0.0, WL["MHWS"], WL["HAT"]], colors=["#5a0080", "#0050b0", "#000000", "#c06000", "#c00000"], linewidths=1.0)
for l in lines:
    ax.plot(l["x"], l["y"], "-", color="k", lw=1.4)
    ax.text(float(np.interp(0, l["y"], l["x"])), -69, l["pid"].replace("5f00", ""), rotation=90, ha="center", va="top", fontsize=6.5)
ax.plot(toe[:, 0], toe[:, 1], "-", color="#ff2020", lw=1.4)
ax.axhline(0, color="c", lw=1.0, ls="--")
ax.set_xlim(-175, 175); ax.set_ylim(300, -100)
ax.set_xlabel("x alongshore (canonical m)"); ax.set_ylabel("y offshore (m)")
ax.set_title("11 CCO beach-profile lines (survey 2010-04-20, black) on the extended seabed (colour = z m MSL)\ncontours: LAT, MLWS, MSL, MHWS, HAT; red = reef toe; cyan dashed = y = 0 (surf line of 28 Sep 2011)", fontsize=8)
plt.colorbar(im, ax=ax, shrink=0.6, label="z (m MSL = m ODN)")
fig.tight_layout(); fig.savefig(OUT / "cco_profile_lines_plan.png"); plt.close(fig)

# ---- 2. cross sections
fig, ax = plt.subplots(figsize=(9, 5.2), dpi=130)
cmap = plt.get_cmap("viridis")
for k, l in enumerate(lines):
    xm = float(np.interp(0, l["y"], l["x"]))
    ax.plot(l["y"], l["z"], "-", color=cmap(k / (len(lines) - 1)), lw=1.2, label="%s (x %+.0f m)" % (l["pid"].replace("5f00", ""), xm))
for key, col in (("HAT", "#c00000"), ("MHWS", "#c06000"), ("MSL", "k"), ("MLWS", "#0050b0"), ("LAT", "#5a0080")):
    ax.axhline(WL[key], color=col, lw=0.8, ls=":"); ax.text(104, WL[key] + 0.04, key, color=col, fontsize=7, ha="right")
# model seabed along the middle line (x about 0) over the same range
i0 = int(round((0 - sb["x0"]) / sb["dx"]))
sel = (ys >= -66) & (ys <= 110)
ax.plot(ys[sel], Z[sel, i0], "--", color="r", lw=1.5, label="model seabed at x = 0 (this grid)")
ax.axvline(0, color="c", lw=0.8); ax.text(1, 3.4, "y = 0 (surf line)", color="c", fontsize=7)
ax.set_xlim(-70, 105); ax.set_ylim(-3.2, 3.8)
ax.set_xlabel("y offshore (canonical m)"); ax.set_ylabel("z_ODN = z_MSL (m)")
ax.set_title("CCO profiles 2010-04-20, Elevation_OD (m ODN), same y axis as the model; tide lines from Mead et al. (2010) Table 1", fontsize=8)
ax.legend(fontsize=6, ncol=2, loc="lower right"); ax.grid(alpha=0.25)
fig.tight_layout(); fig.savefig(OUT / "cco_profiles_cross_sections.png"); plt.close(fig)

# ---- 3. zone map
fig, ax = plt.subplots(figsize=(6.6, 9.6), dpi=130)
cm = ListedColormap([CODES[k][1] for k in range(6)])
ax.imshow(C, origin="lower", extent=(xs[0] - 1, xs[-1] + 1, ys[0] - 1, ys[-1] + 1), cmap=cm, norm=BoundaryNorm(np.arange(-0.5, 6.5, 1), cm.N), aspect="equal")
ax.plot(toe[:, 0], toe[:, 1], "-", color="k", lw=1.4)
ax.axhline(0, color="c", lw=1.0, ls="--")
ax.contour(xs, ys, Z, levels=[0.0], colors="k", linewidths=0.8)
for yy, t in ((0, "y = 0 shoreline"), (380, "y = 380: end of original grid"), (650, "y = 650: end of extension")):
    ax.text(-158, yy - 6, t, fontsize=7, color="k")
ax.set_ylim(660, -75); ax.set_xlim(-165, 165)
ax.set_xlabel("x alongshore (canonical m)"); ax.set_ylabel("y offshore (m)")
ax.set_title("Zone map of the extended seabed (161 x 359 cells, 2 m); black polygon = reef toe; black line = MSL contour", fontsize=8)
ax.legend(handles=[Patch(color=CODES[k][1], label="%d  %s" % (k, CODES[k][0])) for k in range(6)], fontsize=7, loc="lower left", framealpha=0.95)
fig.tight_layout(); fig.savefig(OUT / "seabed_zone_map.png"); plt.close(fig)
print("ok", [p.name for p in OUT.glob("cco_*")] + ["seabed_zone_map.png"])
