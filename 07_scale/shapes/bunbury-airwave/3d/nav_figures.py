"""nav_figures.py - draws the annotated Navionics figures N1-N4 into annotated/ from the screenshots in src/navionics/ and data/nav_transects.json.
Run: python nav_figures.py   (needs data/nav_transects.json from nav_annotate.py; build_3d.py --annotations calls both)
"""
import json
import math
import os

import matplotlib
import numpy as np
from PIL import Image

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, Polygon as MPoly  # noqa: E402

import nav_annotate as NA  # noqa: E402

NAV, DATA, ANN = NA.NAV, NA.DATA, NA.ANN


def main():
    o = json.load(open(os.path.join(DATA, "nav_transects.json"), encoding="utf-8"))
    d, bx, by, y_site = NA.load_summary()
    os.makedirs(ANN, exist_ok=True)
    img = np.array(Image.open(os.path.join(NAV, "sonar_m_z18_dpr2.png")).convert("RGB"))
    res = o["res_m_per_px"]
    H, W = img.shape[:2]
    cx, cy = W / 2.0, H / 2.0

    def P(x, y):
        return NA.px_of(x, y, y_site, bx, by, res, cx, cy)

    th = np.linspace(0, 2 * np.pi, 120)

    # ---------------- N1: SonarChart + transects + readings
    fig, ax = plt.subplots(figsize=(13, 11.3), dpi=110)
    ax.imshow(img)
    for t in o["transects"]:
        a = t["a"]
        p0, p1 = P(a, y_site - 60), P(a, y_site + 215)
        main = a == 0
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color="magenta" if main else "darkorange", lw=2.6 if main else 1.1, alpha=0.95 if main else 0.8, zorder=5)
        for n, s_ in enumerate(t["crossings_s"]):
            q = P(a, y_site + s_)
            ax.plot(q[0], q[1], "o", ms=5 if main else 3.2, mfc="yellow" if main else "none", mec="k" if main else "darkorange", mew=0.8, zorder=6)
            if main and (n % 2 == 0 or n < 5):
                dy_ = 26 if n < 6 else -18                 # labels of the near-shore lines go below the transect (avoids the site marker)
                ax.annotate("%.1f" % (0.5 * n), q, xytext=(q[0] - 8, q[1] + dy_), fontsize=8.5, fontweight="bold", color="black",
                            bbox=dict(boxstyle="round,pad=0.12", fc="yellow", ec="none", alpha=0.9), zorder=7)
    s0 = P(0, y_site)
    ax.plot(s0[0], s0[1], "x", color="white", mew=3, ms=11, zorder=8)
    ax.plot(s0[0], s0[1], "x", color="red", mew=1.5, ms=9, zorder=9)
    ax.annotate("site point -33.3276, 115.6284 = image centre = model (x 0, y %.1f)\n(text/satellite-derived; reef position known to about +-100 m)" % y_site, s0,
                xytext=(s0[0] + 40, s0[1] + 120), fontsize=8.5, color="white", bbox=dict(boxstyle="round", fc="black", alpha=0.65),
                arrowprops=dict(arrowstyle="->", color="white"), zorder=9)
    qx, qy = zip(*[P(6 * math.cos(t_), 37.5 + 6 * math.sin(t_)) for t_ in th])
    ax.plot(qx, qy, color="red", lw=2, zorder=8)
    band = [P(-100, 30), P(100, 30), P(100, 50), P(-100, 50)]
    ax.add_patch(MPoly(np.array(band), closed=True, fc="red", ec="red", alpha=0.12, zorder=4))
    ax.text(band[3][0] + 6, band[3][1] - 6, "30-50 m offshore band (text); red circle = 12 m reef at the model default y = 37.5 m", color="red", fontsize=8.5, zorder=9,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))
    o_ = P(-200, y_site - 40)
    for (ddx, ddy, lab) in ((40, 0, "+x alongshore (%.0f deg true)" % bx), (0, 40, "+y seaward (%.0f deg true)" % by)):
        e_ = P(-200 + ddx, y_site - 40 + ddy)
        ax.annotate("", xy=e_, xytext=o_, arrowprops=dict(arrowstyle="-|>", color="blue", lw=2.2), zorder=9)
        ax.text(e_[0] + 6, e_[1] - 6, lab, color="blue", fontsize=9, fontweight="bold", zorder=9, bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.8))
    bx0, by0 = 130, H - 130
    ax.plot([bx0, bx0 + 50 / res], [by0, by0], color="black", lw=6, zorder=9)
    ax.plot([bx0, bx0 + 50 / res], [by0, by0], color="white", lw=3, zorder=10)
    ax.text(bx0, by0 - 18, "50 m (%.4f m per image px)" % res, fontsize=9, color="black", zorder=10, bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.85))
    ax.annotate("", xy=(W - 150, 330), xytext=(W - 150, 470), arrowprops=dict(arrowstyle="-|>", color="black", lw=3), zorder=10)
    ax.text(W - 150, 310, "N", fontsize=14, fontweight="bold", ha="center", zorder=10, bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.85))
    ax.set_axis_off()
    ax.set_title("bunbury-airwave N1: Garmin Navionics 'SonarChart Maps' (metres), read 2026-10-05; (c) Garmin Navionics, private research copy, NOT FOR NAVIGATION.\n"
                 "Magenta = main shore-normal transect through the site; yellow dots + numbers = contour crossings counted from the 0 m line (green/blue edge) at 0.5 m interval;\n"
                 "orange = 8 more transects (alongshore offsets -120 ... +120 m). The structure was removed in Dec 2019: no reef is visible; the chart is used for the SEABED only.", fontsize=8.4)
    fig.tight_layout()
    fig.savefig(os.path.join(ANN, "N1_navionics_sonarchart_contours_transects.png"))
    plt.close(fig)

    # ---------------- N2: datum test
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 6.4), dpi=110, gridspec_kw={"width_ratios": [1.7, 1]})
    pr = d["profile"]
    yy, zm = np.array(pr["y"]), np.array(pr["median_ahd"], dtype=float)
    ok = np.isfinite(zm)
    a1.fill_between(yy[ok], np.array(pr["p10_ahd"], dtype=float)[ok], np.array(pr["p90_ahd"], dtype=float)[ok], color="tab:blue", alpha=0.2, label="lidar 2009, 10th-90th percentile (|x| <= 100 m)")
    a1.plot(yy[ok], zm[ok], color="tab:blue", lw=2.2, label="lidar 2009 median profile (m AHD)")
    t0 = [t for t in o["transects"] if t["a"] == 0][0]
    ysn = np.array(t0["y_model_m"])
    dn = np.array(t0["depth_m"])
    for name, col, mk in (("LAT", "tab:purple", "o"), ("MLLW", "tab:orange", "s"), ("AHD", "tab:green", "^")):
        Dc = NA.CANDIDATES[name]
        a1.plot(ysn, Dc - dn, mk + "-", color=col, ms=5, lw=1, label="Navionics main transect, depths read as below %s (%+.2f m AHD)" % (name, Dc))
    a1.axvspan(30, 50, color="red", alpha=0.1, label="reef text range 30-50 m")
    a1.set_xlim(-10, 215)
    a1.set_ylim(-9, 1)
    a1.set_xlabel("y: metres seaward of the fitted 0 m AHD contour (2009)")
    a1.set_ylabel("elevation, m AHD")
    a1.grid(alpha=0.3)
    a1.legend(fontsize=7.6, loc="lower left")
    a1.set_title("Navionics contour crossings (main transect) converted to AHD with each candidate datum, against the lidar profile", fontsize=9)
    names = [k for k in o["datum_test_all"] if not k.startswith("_") and k != "LAT (DoT index)"]
    rms_all = [o["datum_test_all"][k]["rms_m"] for k in names]
    rms_main = [o["datum_test_main"][k]["rms_m"] for k in names]
    xx = np.arange(len(names))
    a2.bar(xx - 0.2, rms_main, 0.38, label="main transect (n=%d)" % o["datum_test_main"]["LAT"]["n"], color="tab:cyan")
    a2.bar(xx + 0.2, rms_all, 0.38, label="9 transects (n=%d)" % o["datum_test_all"]["LAT"]["n"], color="tab:red")
    for i_, (r1, r2) in enumerate(zip(rms_main, rms_all)):
        a2.text(i_ - 0.2, r1 + 0.01, "%.2f" % r1, ha="center", fontsize=8)
        a2.text(i_ + 0.2, r2 + 0.01, "%.2f" % r2, ha="center", fontsize=8)
    a2.set_xticks(xx)
    a2.set_xticklabels(["%s\n%+.2f" % (k, NA.CANDIDATES[k]) for k in names], fontsize=8.5)
    a2.set_ylabel("RMS of (lidar - Navionics-implied elevation), m")
    a2.legend(fontsize=8)
    fr = o["datum_test_all"]["_implied_free_datum_ahd"]
    a2.set_title("Datum RMS test (valid lidar lines only, y >= 30 m)\nfree-fit datum %+.2f m AHD (sd %.2f, n=%d lines)" % (fr["mean"], fr["sd"], fr["n"]), fontsize=9)
    fig.suptitle("bunbury-airwave N2: which depth datum does the Navionics chart use? (the app states none) - test against the independent WA DoT 2009 lidar", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(ANN, "N2_navionics_datum_rms_test.png"))
    plt.close(fig)

    # ---------------- N3: nautical chart readings
    imn = np.array(Image.open(os.path.join(NAV, "nautical_m_z18_dpr2.png")).convert("RGB"))
    fig, ax = plt.subplots(figsize=(11, 9.5), dpi=110)
    ax.imshow(imn)
    for r in o["nautical_soundings"]:
        px, py = r["px"]
        col = "limegreen" if r["lidar_valid"] else "red"
        ax.add_patch(Circle((px, py), 34, fc="none", ec=col, lw=2.2))
        ax.text(px + 40, py - 30, "%s m\nlidar %+.2f AHD\n-> datum %+.2f%s" % (r["label"], r["lidar_ahd"], r["implied_datum_ahd"], "" if r["lidar_valid"] else "\n(outside lidar grid / gap: not used)"),
                fontsize=7.8, color="black", bbox=dict(boxstyle="round,pad=0.15", fc="white", ec=col, alpha=0.9))
    p0, p1 = P(0, y_site - 60), P(0, y_site + 215)
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color="magenta", lw=2)
    for r in o["nautical_contours_main"][:3]:
        q = P(0, r["y_m"])
        if 0 <= q[0] < W and 0 <= q[1] < H:
            ax.plot(q[0], q[1], "o", mfc="yellow", mec="k", ms=7)
            ax.text(q[0] + 12, q[1] - 14, "%g m contour (chart): lidar %+.2f AHD -> datum %+.2f" % (r["depth_m"], r["lidar_ahd"], r["implied_datum_ahd"]), fontsize=8,
                    bbox=dict(boxstyle="round,pad=0.1", fc="yellow", ec="none", alpha=0.9))
    ax.set_axis_off()
    ax.set_title("bunbury-airwave N3: Garmin Navionics 'Nautical Charts' layer (metres), zoom 18, 2026-10-05; (c) Garmin, private research copy, NOT FOR NAVIGATION.\n"
                 "Spot soundings (subscript = decimal: 3_5 = 3.5 m) and the 2 m contour (edge of the blue band); magenta = main transect through the site; green circle = used in the datum check.", fontsize=8.4)
    fig.tight_layout()
    fig.savefig(os.path.join(ANN, "N3_navionics_nautical_soundings.png"))
    plt.close(fig)

    # ---------------- N4: zoom on the reef site (is the bladder visible in the SonarChart contours?)
    sc = P(0, y_site)
    x0, x1 = int(sc[0] - 400), int(sc[0] + 400)          # +-100 m around the site point (0.2495 m/px)
    y0, y1 = int(sc[1] - 330), int(sc[1] + 330)
    fig, ax = plt.subplots(figsize=(11.5, 8), dpi=110)
    ax.imshow(img)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y1, y0)
    for yc, lab, c in ((30, "y = 30 m", "red"), (37.5, "model default y = 37.5 m", "magenta"), (50, "y = 50 m", "red")):
        a_, b_ = P(-78, yc), P(78, yc)
        ax.plot([a_[0], b_[0]], [a_[1], b_[1]], color=c, lw=1.2, ls="--")
        ax.text(b_[0], b_[1] + 14, " " + lab, color=c, fontsize=8, va="bottom", clip_on=True)
    for xc in (-60, 0, 60):
        qx, qy = zip(*[P(xc + 6 * math.cos(t_), 37.5 + 6 * math.sin(t_)) for t_ in th])
        ax.plot(qx, qy, color="magenta" if xc == 0 else "red", lw=2)
    ax.text(P(0, 37.5)[0] + 30, P(0, 37.5)[1] + 22, "12 m reef circle (x = 0; also drawn at x = +-60 m)", color="magenta", fontsize=9,
            bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.85))
    ax.set_axis_off()
    ax.set_title("bunbury-airwave N4: SonarChart contours (0.5 m interval) around the reef site, zoomed. A 12 m bladder 1.6-2.0 m high would make closed contour rings; none exist at the three positions drawn.\n"
                 "The reef was removed within days (Dec 2019) and its lateral position is unknown (+-100 m), so this is only a weak check. (c) Garmin Navionics, private research copy, NOT FOR NAVIGATION.", fontsize=8.2)
    fig.tight_layout()
    fig.savefig(os.path.join(ANN, "N4_navionics_reef_site_zoom_no_structure.png"))
    plt.close(fig)
    print("annotated N1-N4 written")


if __name__ == "__main__":
    main()
