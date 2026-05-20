#!/usr/bin/env python3
"""
Compute polygon-by-polygon specific yield from DWR SVSim Texture Data for
the 2027 BC RMS network polygons (both single and three-zone methods).

Method (per the Sacramento Valley Simulation Model TM-1B):
    Coarse-grained sediments → Sy = 0.15
    Fine-grained sediments   → Sy = 0.05
    Polygon Sy = (% coarse × 0.15) + (% fine × 0.05)
where percent coarse = total coarse-thickness summed over all valid boreholes
in the polygon, divided by total valid thickness, evaluated within the
0–500 ft below ground surface analysis window.

Inputs:
  - /tmp/svsim/svsim_texture_data.csv
        DWR CKAN resource 544623e2-0cd5-4c5b-827f-affa4abf4e16
        (downloaded automatically on first run; ~9 MB).
  - ../2027-BC-prop-network/js/polygons-data-single.js
  - ../2027-BC-prop-network/js/polygons-data-three-zone.js
        Voronoi polygons (lat/lon rings) keyed by full SWN.

Outputs:
  - data/polygon_sy_svsim_single.csv
  - data/polygon_sy_svsim_three_zone.csv
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

from pyproj import Transformer
from shapely.geometry import Point, Polygon, MultiPolygon

HERE = Path(__file__).resolve().parent
WORKTREE = HERE.parent
DATA_DIR = WORKTREE / "data"

REF_REPO = (WORKTREE / ".." / "2027-BC-prop-network").resolve()
POLY_JS_SINGLE = REF_REPO / "js" / "polygons-data-single.js"
POLY_JS_THREE_ZONE = REF_REPO / "js" / "polygons-data-three-zone.js"
POLY_VAR_BY_METHOD = {
    "single":     ("RMS_POLYGONS_SINGLE",     POLY_JS_SINGLE),
    "three-zone": ("RMS_POLYGONS_THREE_ZONE", POLY_JS_THREE_ZONE),
}

SVSIM_DIR = Path("/tmp/svsim")
SVSIM_CSV = SVSIM_DIR / "svsim_texture_data.csv"
SVSIM_URL = ("https://data.cnra.ca.gov/dataset/"
             "5f06b5e9-39c2-411a-a39c-cc0e76e6a35f/resource/"
             "544623e2-0cd5-4c5b-827f-affa4abf4e16/download/"
             "svsim_texture_data.csv")

DEPTH_TOP_FT = 0
DEPTH_BASE_FT = 500
MIN_VALID_THICKNESS_FT = 200

SY_COARSE = 0.15
SY_FINE   = 0.05

US_SURVEY_FT_TO_M = 0.3048006096
TRANSFORMER = Transformer.from_crs("EPSG:26910", "EPSG:4326", always_xy=True)

USCS_COARSE_PREFIX = ("G", "S")
USCS_FINE_PREFIX   = ("M", "C", "O", "P")
USCS_FINE_LITERAL = {"TPSL", "HP", "TOPSOIL", "TUFF", "TUFF/ASH",
                     "VOLCANIC FRAGS", "ASH", "VLCU"}
USCS_SKIP_LITERAL = {"FILL", "ROCK", "XLN", "XLN/FRCT", "UNKNOWN", "NR", "N/A"}

COARSE_TERMS = ("sand", "gravel", "cobble", "boulder", "pebble", "grit",
                "sandstone")
FINE_TERMS   = ("clay", "silt", "mud", "muck", "peat", "loam", "adobe",
                "hardpan", "hard pan", "topsoil", "top soil", "shale",
                "ash", "lava", "tuff")
SKIP_TERMS = ("rock", "unknown", "decomposed")


def _last_match(text: str, terms):
    best = -1
    for term in terms:
        i = text.rfind(term)
        if i > best:
            best = i
    return best


def classify_lith(uscs: str, lith_desc: str) -> str | None:
    u = (uscs or "").strip()
    u_upper = u.upper()
    if u_upper in USCS_SKIP_LITERAL:
        u = ""
    elif u_upper in USCS_FINE_LITERAL:
        return "fine"
    elif u:
        for ch in u_upper:
            if ch in USCS_COARSE_PREFIX:
                return "coarse"
            if ch in USCS_FINE_PREFIX:
                return "fine"
            if ch.isalpha():
                break

    d = (lith_desc or "").strip().lower()
    if not d:
        return None
    if any(t in d for t in SKIP_TERMS):
        return None
    coarse_at = _last_match(d, COARSE_TERMS)
    fine_at = _last_match(d, FINE_TERMS)
    if coarse_at < 0 and fine_at < 0:
        return None
    if fine_at < 0:
        return "coarse"
    if coarse_at < 0:
        return "fine"
    return "coarse" if coarse_at > fine_at else "fine"


def aggregate_borehole(layers):
    total = 0.0
    coarse = 0.0
    for L in layers:
        top = max(L["top"], DEPTH_TOP_FT)
        base = min(L["base"], DEPTH_BASE_FT)
        if base <= top:
            continue
        thick = base - top
        if L["classification"] is None:
            continue
        total += thick
        if L["classification"] == "coarse":
            coarse += thick
    return total, coarse


def load_polygons_from_js(path: Path, var_name: str = "RMS_POLYGONS"):
    text = path.read_text()
    m = re.search(rf"const\s+{var_name}\s*=\s*(.*?);\s*$", text,
                  re.DOTALL | re.MULTILINE)
    return json.loads(m.group(1))


def polygons_to_shapely(polygons):
    """{zone_label: shapely (lon/lat) geometry}.  Input rings are [lat, lon]."""
    out = {}
    for p in polygons:
        polys = [Polygon([(lon, lat) for lat, lon in ring]) for ring in p["rings"]]
        if len(polys) == 1:
            out[p["zone_label"]] = polys[0]
        else:
            out[p["zone_label"]] = MultiPolygon(polys)
    return out


def ensure_svsim_csv():
    if SVSIM_CSV.exists():
        return
    SVSIM_DIR.mkdir(parents=True, exist_ok=True)
    print(f"downloading SVSim Texture Data → {SVSIM_CSV} (~9 MB)…")
    subprocess.run(["curl", "-sSL", SVSIM_URL, "-o", str(SVSIM_CSV)], check=True)


def build_borehole_records():
    boreholes = {}
    with SVSIM_CSV.open(encoding="latin-1") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["SVSIM_NAME"]
            try:
                x_ft = float(row["X"])
                y_ft = float(row["Y"])
            except (ValueError, TypeError):
                continue
            try:
                top = float(row["TOP_BGS"])
                base = float(row["BASE_BGS"])
            except (ValueError, TypeError):
                continue
            if base <= top:
                continue
            cls = classify_lith(row.get("USCS", ""), row.get("LITH_DESC", ""))
            if name not in boreholes:
                x_m = x_ft * US_SURVEY_FT_TO_M
                y_m = y_ft * US_SURVEY_FT_TO_M
                lon, lat = TRANSFORMER.transform(x_m, y_m)
                boreholes[name] = {
                    "name": name,
                    "swn": row.get("SWN", ""),
                    "lat": lat,
                    "lon": lon,
                    "layers": [],
                }
            boreholes[name]["layers"].append({
                "top": top, "base": base, "classification": cls,
            })
    return list(boreholes.values())


def assign_boreholes_to_polygons(boreholes, polygons_shapely):
    by_zone = {z: [] for z in polygons_shapely}
    for bh in boreholes:
        pt = Point(bh["lon"], bh["lat"])
        for zone, geom in polygons_shapely.items():
            if geom.contains(pt):
                by_zone[zone].append(bh)
                break
    return by_zone


def compute_polygon_sy(by_zone):
    rows = []
    for zone, boreholes in by_zone.items():
        total_thick = 0.0
        coarse_thick = 0.0
        n_valid = 0
        for bh in boreholes:
            t, c = aggregate_borehole(bh["layers"])
            if t < MIN_VALID_THICKNESS_FT:
                continue
            n_valid += 1
            total_thick += t
            coarse_thick += c
        pct_coarse = coarse_thick / total_thick if total_thick > 0 else None
        sy = (pct_coarse * SY_COARSE + (1 - pct_coarse) * SY_FINE
              if pct_coarse is not None else None)
        rows.append({
            "zone_label": zone,
            "n_boreholes_in_polygon": len(boreholes),
            "n_boreholes_with_>=200ft": n_valid,
            "total_thick_ft": round(total_thick, 0),
            "coarse_thick_ft": round(coarse_thick, 0),
            "pct_coarse": round(pct_coarse, 4) if pct_coarse is not None else None,
            "sy": round(sy, 4) if sy is not None else None,
        })
    return rows


def run_one_method(method: str, boreholes):
    var_name, poly_js = POLY_VAR_BY_METHOD[method]
    print(f"\n=== {method} method ({poly_js.name}) ===")
    polygons = load_polygons_from_js(poly_js, var_name)
    polygons_shapely = polygons_to_shapely(polygons)
    by_zone = assign_boreholes_to_polygons(boreholes, polygons_shapely)
    rows = compute_polygon_sy(by_zone)

    print(f"{'Polygon':<18} {'n_bh':>5} {'≥200ft':>7} {'%coarse':>9} {'Sy':>8}")
    print("-" * 54)
    for r in rows:
        zone = r["zone_label"]
        sy_str = f"{r['sy']:.4f}" if r["sy"] is not None else "n/a"
        pct_str = f"{r['pct_coarse']*100:.1f}%" if r["pct_coarse"] is not None else "n/a"
        print(f"{zone:<18} {r['n_boreholes_in_polygon']:>5} "
              f"{r['n_boreholes_with_>=200ft']:>7} {pct_str:>9} {sy_str:>8}")

    suffix = method.replace("-", "_")
    out_csv = DATA_DIR / f"polygon_sy_svsim_{suffix}.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["zone_label", "n_boreholes_in_polygon",
                    "n_boreholes_with_>=200ft_valid", "total_thick_ft",
                    "coarse_thick_ft", "pct_coarse", "sy"])
        for r in rows:
            w.writerow([
                r["zone_label"], r["n_boreholes_in_polygon"],
                r["n_boreholes_with_>=200ft"], r["total_thick_ft"],
                r["coarse_thick_ft"],
                f"{r['pct_coarse']:.4f}" if r["pct_coarse"] is not None else "",
                f"{r['sy']:.4f}" if r["sy"] is not None else "",
            ])
    print(f"Wrote {out_csv}")


def main():
    methods = ["single", "three-zone"]
    if len(sys.argv) > 1 and sys.argv[1] in POLY_VAR_BY_METHOD:
        methods = [sys.argv[1]]
    ensure_svsim_csv()
    print(f"Loading SVSim borehole records from {SVSIM_CSV}…")
    boreholes = build_borehole_records()
    print(f"  {len(boreholes):,} boreholes total in SVSim")
    for m in methods:
        run_one_method(m, boreholes)


if __name__ == "__main__":
    main()
