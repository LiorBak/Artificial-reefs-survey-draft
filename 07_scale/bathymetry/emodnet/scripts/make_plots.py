"""Profile plots (PNG) for Boscombe and Borth from the extracted CSVs. Output: figures/<slug>_profile_*.png"""
import json, math, os, sys
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Polygon
sys.path.insert(0, os.path.dirname(__file__))
import extract_site as E

DATA, FIG = E.DATA, os.path.join(E.OUT, "figures"); os.makedirs(FIG, exist_ok=True)
CRED = "Data: EMODnet Bathymetry Consortium (2024) EMODnet Digital Bathymetry (DTM 2024), https://doi.org/10.12770/cf51df64-56f9-4a99-b1aa-36b8d7b743a1 (CC BY 4.0)," + chr(10) + "accessed 2026-10-06. Private research copy. Not for navigation."


def reef_extent_on_line(polys, x):
    out = []
    for p in polys:
        seg = LineString([(x, -50), (x, 800)]).intersection(Polygon(p))
        if not seg.is_empty:
            for g in (seg.geoms if hasattr(seg, "geoms") else [seg]): out.append((g.bounds[1], g.bounds[3]))
    return out


def cell_runs(p):
    p = p.copy(); p["cid"] = p.cell_ki.astype(str) + "_" + p.cell_kj.astype(str); g = (p.cid != p.cid.shift()).cumsum()
    return p.groupby(g).agg(y0=("y_m", "min"), y1=("y_m", "max"), elev=("elev_LAT_m", "first"), mn=("elev_min", "first"), mx=("elev_max", "first"),
                            n=("value_count", "first"), interp=("interpolated", "first"), status=("status", "first"))


def boscombe():
    slug = "boscombe-surf-reef"; S = E.site_def(slug)
    p = pd.read_csv(f"{DATA}/{slug}_profile_through_reef_centre_with_model.csv"); R = cell_runs(p)
    rest = pd.read_csv(f"{DATA}/{slug}_profile_REST_depth_profile_y0_500.csv")
    M = json.load(open(os.path.join(E.SCRATCH, "boscombe_model.json"), encoding="utf-8"))
    off = 1.46
    fig, ax = plt.subplots(figsize=(12.5, 6.4))
    for a, b in reef_extent_on_line(S["polys"], S["centre_xy"][0]): ax.axvspan(a, b, color="gold", alpha=0.25, label="reef outline along the profile (shape.json)")
    for r in R.itertuples():
        if r.status.startswith("ERDDAP DTM"):
            ax.hlines(r.elev, r.y0, r.y1, color="tab:blue", lw=3, label="EMODnet DTM 2024 cell mean" if r.Index == R.index[2] else None)
            ax.fill_between([r.y0, r.y1], r.mn, r.mx, color="tab:blue", alpha=0.18, label="cell min-max (sub-cell soundings)" if r.Index == R.index[2] else None)
            ax.text(min(max((r.y0 + r.y1) / 2, 10), 490), r.mx + 0.15, f"n={int(r.n)}", ha="center", fontsize=8, color="tab:blue", clip_on=True)
    ax.plot(rest.y_m, rest.emodnet_LAT_m, color="navy", lw=0.8, ls=":", label="REST /depth_profile (1000 samples, same cells)")
    ax.plot(p.y_m, p.model_seabed_LAT_m, color="saddlebrown", lw=2, label="project model seabed (LAT frame = MSL + 1.46 m)")
    ax.plot(p.y_m, p.model_asbuilt_surface_LAT_m, color="crimson", lw=2, label="project model as-built reef surface (crest +0.5 m ACD)")
    ax.plot(p.y_m, p.model_apr2011_surface_LAT_m, color="darkorange", lw=1.5, ls="--", label="April 2011 DGPS surface (Rendle & Davidson 2012 Fig. 9)")
    for lab, z, c in [("LAT = 0", 0, "k"), ("MSL +1.46", 1.46, "tab:green"), ("MHWS +2.27", 2.27, "tab:cyan")]:
        ax.axhline(z, color=c, lw=0.8, ls="-.", alpha=0.7); ax.text(498, z + 0.08, lab, ha="right", fontsize=8, color=c)
    ax.set_xlim(0, 500); ax.set_ylim(-11, 3.4); ax.set_xlabel("distance offshore of the frame origin along the shore normal (bearing 173.4 deg), m")
    ax.set_ylabel("height above LAT, m (negative = below LAT)")
    ax.set_title("Boscombe Surf Reef: EMODnet DTM 2024 vs project model along the shore-normal line through the reef centre (x = 0.1 m)", fontsize=11)
    h, l = ax.get_legend_handles_labels(); u = dict(zip(l, h)); ax.legend(u.values(), u.keys(), fontsize=8, loc="lower left"); ax.grid(alpha=0.3)
    fig.text(0.01, 0.005, CRED + " Model: 07_scale/shapes/boscombe-surf-reef/3d/model.js (read only).", fontsize=6.5)
    fig.tight_layout(rect=(0, 0.035, 1, 1)); fig.savefig(f"{FIG}/{slug}_profile_emodnet_vs_model.png", dpi=150); plt.close(fig)

    # release history at the profile cells
    c = pd.read_csv(f"{DATA}/{slug}_cells_releases_wcs.csv"); c = c[c.erddap_elev.notna()]
    sel = c[(c.kj == 32794) & (c.ki >= 34285) & (c.ki <= 34289)].sort_values("y_m")
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    for col, lab, st in [("wcs_2018_signflipped", "release 2018 (sign flipped: file is positive-down)", "o--"), ("wcs_2020", "release 2020", "s-"), ("wcs_2022", "release 2022", "^:"), ("wcs_2024", "release 2024", "x-")]:
        ax.plot(sel.y_m, sel[col], st, label=lab, ms=6)
    ax.set_xlabel("cell centre, m offshore (frame y)"); ax.set_ylabel("cell mean, m rel. LAT"); ax.grid(alpha=0.3); ax.legend(fontsize=8)
    ax.set_title("Boscombe: the DTM cells along the profile in four releases (WCS emodnet__mean*)", fontsize=10)
    fig.text(0.01, 0.005, CRED, fontsize=6); fig.tight_layout(rect=(0, 0.05, 1, 1)); fig.savefig(f"{FIG}/{slug}_dtm_release_history.png", dpi=150); plt.close(fig)

    # cell comparison bars
    C = pd.read_csv(f"{DATA}/{slug}_cells_emodnet_vs_model.csv"); C = C[(C.cell_y >= 90) & (C.model_coverage >= 0.9)].sort_values("cell_y")
    fig, ax = plt.subplots(figsize=(10, 4.8)); xs = np.arange(len(C)); w = 0.2
    ax.bar(xs - 1.5 * w, C.emodnet_mean, w, color="tab:blue", label="EMODnet cell mean")
    ax.bar(xs - 0.5 * w, C.model_seabed_mean, w, color="saddlebrown", label="model seabed (no reef), cell mean")
    ax.bar(xs + 0.5 * w, C.model_asbuilt_mean, w, color="crimson", label="model as-built (with reef), cell mean")
    ax.bar(xs + 1.5 * w, C.model_apr2011_mean, w, color="darkorange", label="April 2011 survey surface, cell mean")
    ax.errorbar(xs - 1.5 * w, C.emodnet_mean, yerr=[C.emodnet_mean - C.emodnet_min, C.emodnet_max - C.emodnet_mean], fmt="none", ecolor="k", lw=1, capsize=2)
    ax.set_xticks(xs); ax.set_xticklabels([f"ki {int(a)}/kj {int(b)}\ny~{y:.0f} m\nn={int(n)}" for a, b, y, n in zip(C.ki, C.kj, C.cell_y, C.emodnet_n)], fontsize=7)
    ax.set_ylabel("m rel. LAT"); ax.legend(fontsize=7, loc="lower left"); ax.grid(alpha=0.3, axis="y")
    ax.set_title("Boscombe: EMODnet cell means vs the model averaged over the same cell footprints (cells fully inside the model grid)", fontsize=10)
    fig.text(0.01, 0.005, CRED, fontsize=6); fig.tight_layout(rect=(0, 0.05, 1, 1)); fig.savefig(f"{FIG}/{slug}_cells_emodnet_vs_model.png", dpi=150); plt.close(fig)


def borth():
    slug = "borth-coastal-defence-reef"; S = E.site_def(slug); fr = S["frame"]
    fig, axs = plt.subplots(2, 1, figsize=(12.5, 8.2), gridspec_kw=dict(height_ratios=[3, 1.6]))
    ax = axs[0]
    for tag, f, col in [("reef_centre", "reef_centre", "tab:blue"), ("N_hook_centre", "N_hook_centre", "tab:purple"), ("S_oval_centre", "S_oval_centre", "tab:green")]:
        p = pd.read_csv(f"{DATA}/{slug}_profile_through_{f}.csv"); R = cell_runs(p)
        for r in R.itertuples():
            ax.hlines(r.elev, r.y0, r.y1, color=col, lw=3 if tag == "reef_centre" else 1.5, alpha=1 if tag == "reef_centre" else 0.7,
                      ls="-" if not r.interp and r.status.startswith("ERDDAP DTM") else "--", label=None)
        ax.plot([], [], color=col, lw=3 if tag == "reef_centre" else 1.5, label=f"cells along x = {p.x_m.iloc[0]:.0f} m ({tag})")
    ax.plot([], [], color="k", lw=2, ls="--", label="dashed = interpolated cell (GEBCO 2024 fill)"); ax.plot([], [], color="k", lw=2, label="solid = cell with source sounding(s)")
    for xl, col in [(0.0, "tab:blue"), (38.9, "tab:purple"), (-85.3, "tab:green")]:
        for a, b in reef_extent_on_line(S["polys"], xl): ax.axvspan(a, b, color=col, alpha=0.12)
    ax.axhline(0, color="k", lw=0.8, ls="-."); ax.text(648, 0.1, "LAT = 0", ha="right", fontsize=8)
    ax.set_xlim(-100, 650); ax.set_ylim(-4.0, 6.5); ax.set_ylabel("m rel. LAT"); ax.grid(alpha=0.3); ax.legend(fontsize=8, loc="upper right")
    ax.set_title("Borth reef: EMODnet DTM 2024 cells along three shore-normal lines (shaded = reef extent on each line; frame origin on the defence line, offshore = west, bearing 269.57 deg)", fontsize=9.5)
    ax = axs[1]; rest = pd.read_csv(f"{DATA}/{slug}_profile_REST_depth_profile_y0_500.csv")
    ax.plot(rest.y_m, rest.emodnet_LAT_m, color="navy", lw=1.5, label="REST /depth_profile along x = 0 (0-500 m)"); ax.set_xlabel("distance offshore of the frame origin, m"); ax.set_ylabel("m rel. LAT")
    ax.grid(alpha=0.3); ax.legend(fontsize=8)
    fig.text(0.01, 0.005, CRED + " Reef outlines: 07_scale/shapes/borth-coastal-defence-reef/shape.json (sat2024).", fontsize=6.5)
    fig.tight_layout(rect=(0, 0.035, 1, 1)); fig.savefig(f"{FIG}/{slug}_profile_emodnet.png", dpi=150); plt.close(fig)


if __name__ == "__main__":
    boscombe(); borth(); print("ok")
