"""D2 before/after check (2026-10-10): compares a model.js with the pre-D2 copy (3d/archive/pre_D2/model.js).
Prints a short table and writes d2_check.json.  Usage: python d2_check.py  (run in 3d/scripts)."""
import json, sys, hashlib
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
D3 = HERE.parent


def load(p):
    return json.loads(open(p, encoding="utf8").read().split("=", 1)[1].rstrip().rstrip(";"))


def grid(M):
    sb = M["seabed"]
    Z = np.array(sb["z_cm"]).reshape(sb["ny"], sb["nx"]) / 100.0
    C = np.array([int(c) for c in sb["code"]]).reshape(sb["ny"], sb["nx"])
    return Z, C, sb["x0"] + np.arange(sb["nx"]) * sb["dx"], sb["y0"] + np.arange(sb["ny"]) * sb["dy"]


def nav_rms(M, rows):
    Z, C, xs, ys = grid(M)
    d = []
    for r in rows:
        i = (r["x"] - xs[0]) / 2.0; j = (r["y"] - ys[0]) / 2.0
        i0, j0 = int(i), int(j); fi, fj = i - i0, j - j0
        z = (Z[j0, i0] * (1 - fi) * (1 - fj) + Z[j0, i0 + 1] * fi * (1 - fj) + Z[j0 + 1, i0] * (1 - fi) * fj + Z[j0 + 1, i0 + 1] * fi * fj)
        d.append(-(z + 1.40) - r["depth_nav_m"])
    d = np.array(d)
    return dict(mean=round(float(d.mean()), 2), sd=round(float(d.std(ddof=1)), 2), rms=round(float(np.sqrt((d ** 2).mean())), 2), n=len(d))


def summarise(M, rows):
    Z, C, xs, ys = grid(M)
    out = {"nav": nav_rms(M, rows)}
    for y in (380, 450, 520, 650):
        row = Z[int(round((y - ys[0]) / 2.0))]
        out["slope_per100m_y%d" % y] = round(float(np.polyfit(xs, row, 1)[0] * 100), 3)
        out["range_y%d" % y] = round(float(row.max() - row.min()), 2)
    off = (ys >= 380)
    # whole-zone alongshore trend: slope of (z minus its column-mean over rows) vs x
    zz = Z[off]
    out["trend_zone_ge380_per100m"] = round(float(np.polyfit(np.repeat(xs[None, :], zz.shape[0], 0).ravel(), zz.ravel() - (zz.mean(axis=1, keepdims=True) * np.ones_like(zz)).ravel(), 1)[0] * 100), 3)
    out["cross_shore_slope_ge382"] = round(float(np.polyfit(np.repeat(ys[ys >= 382], len(xs)), Z[ys >= 382].ravel(), 1)[0]), 5)
    out["row380_codes"] = sorted(set(int(c) for c in C[int(round((380 - ys[0]) / 2.0))]))
    out["step_378_380_max_abs_m"] = round(float(np.abs(Z[int(round((380 - ys[0]) / 2.0))] - Z[int(round((378 - ys[0]) / 2.0))]).max()), 2)
    out["edge_x-160_z380"] = round(float(Z[int(round((380 - ys[0]) / 2.0)), 0]), 2)
    out["edge_x+160_z380"] = round(float(Z[int(round((380 - ys[0]) / 2.0)), -1]), 2)
    out["z_mean_ge380"] = round(float(zz.mean()), 3)
    out["min_z"] = round(float(Z.min()), 2); out["max_z"] = round(float(Z.max()), 2)
    return out


def main():
    rows = json.load(open(HERE / "nav_z16_offshore.json"))["rows"]
    A = load(D3 / "archive" / "pre_D2" / "model.js"); B = load(D3 / "model.js")
    res = {"before": summarise(A, rows), "after": summarise(B, rows)}
    ZA, CA, xs, ys = grid(A); ZB, CB, _, _ = grid(B)
    assert ZA.shape == ZB.shape
    j380 = int(round((380 - ys[0]) / 2.0))
    ch = ZA != ZB
    res["cells_changed_total"] = int(ch.sum())
    res["cells_changed_rows_min_y"] = float(ys[np.where(ch.any(axis=1))[0].min()]) if ch.any() else None
    res["cells_changed_below_380"] = int(ch[:j380].sum())
    res["codes_identical"] = bool((CA == CB).all())
    res["datum_w_identical"] = A["seabed"]["datum_w"] == B["seabed"]["datum_w"]
    # reef and everything outside the seabed grid
    res["reef_identical"] = json.dumps(A["reef"], sort_keys=True) == json.dumps(B["reef"], sort_keys=True)
    res["reef_sha1"] = hashlib.sha1(json.dumps(B["reef"], sort_keys=True).encode()).hexdigest()[:10]
    res["stats_identical"] = json.dumps(A["stats"], sort_keys=True) == json.dumps(B["stats"], sort_keys=True)
    res["shoreline_identical"] = json.dumps(A["shoreline"], sort_keys=True) == json.dumps(B["shoreline"], sort_keys=True)
    res["water_levels_identical"] = json.dumps(A["water_levels"], sort_keys=True) == json.dumps(B["water_levels"], sort_keys=True)
    # grid coverage (Borth lesson): every node of the grid is finite and every column/row of zone 5 is used
    res["all_finite"] = bool(np.isfinite(ZB).all())
    res["zone5_cells"] = int((CB == 5).sum()); res["zone5_cells_before"] = int((CA == 5).sum())
    res["zone5_all_rows_flat_in_x"] = bool(all(np.ptp(ZB[j][CB[j] == 5]) < 0.006 for j in range(len(ys)) if (CB[j] == 5).any()))
    json.dump(res, open(HERE / "d2_check.json", "w"), indent=1)
    print(json.dumps(res, indent=0)[:3500])


if __name__ == "__main__":
    main()
