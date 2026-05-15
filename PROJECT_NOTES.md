# Project Notes — What We Did

A working-notes file recording **what was built, why, and how** for the
28-polygon 2027 BC RMS drought-storage dashboard. The README is the
audience-facing methodology document; this file is the project history.

---

## Goal

Re-create the original 17-polygon
[2027-drought-analysis](https://cosmo1007.github.io/2027-drought-analysis/)
dashboard against the new **28-polygon Voronoi tessellation** from the
[2027-BC-prop-network](https://cosmo1007.github.io/2027-BC-prop-network/)
framework, with appropriate methodological corrections for the late-baseline
polygons that the new (more granular) network introduces.

Audience: Vina GSA technical staff and the AGUBC Board.

---

## Inputs (all read-only)

| Source | Files used | What we pulled |
|---|---|---|
| `../2027-BC-prop-network/js/polygons-data.js` | 28 Voronoi polygons clipped to DWR B118 5-021.57 | zone_label, rms_well_swn, mgmt_area, rings, area_acres |
| `../2027-BC-prop-network/js/wells-data.js` | 79 wells | well_name → site_code mapping, lat/lon, RMS membership |
| `../2027-BC-prop-network/js/measurements-data.js` | DWR CKAN periodic GWL (fetched 2026-05-15) | 227,647 records across 77 wells |
| DWR SVSim Texture Data | `/tmp/svsim/svsim_texture_data.csv` (CKAN `544623e2-…`) | 4,691 boreholes with USCS/lith descriptions |
| 2022 Vina GSP (Dec 15, 2021) | Doc reference only | Sustainable yield = 233,500 AFY (p. ES-5), total fresh storage 16+ MAF |

---

## Steps taken

### 1. Scaffolded the project (5 min)

Created `2027-BC-storage/` with `scripts/`, `data/`, `raw/`, and (later)
`.claude/launch.json` for local preview. The repo reads directly from the
sibling `2027-BC-prop-network/` directory — single source of truth for
polygons and measurements.

### 2. Recomputed polygon Sy from SVSim Texture Data (15 min)

Ported the original `build_sy_svsim.py` to the new 28-polygon geometry.
Same methodology as before: coarse-grained sediments → Sy = 0.15,
fine-grained → 0.05, area-weighted by borehole lithology in the
0–500 ft below-ground analysis window, ≥200 ft of valid lithology
required per borehole.

**Sy range:** 0.0594 (`23N01W14R002M`) to 0.1172 (`20N03E33L001M`).
Basin area-weighted mean ≈ 0.087.

**Fallback for sparse coverage:** three polygons (`23N02W25C001M`,
`23N01E29P002M`, `21N01E25K001M`) have ≤2 boreholes in their footprint
or no boreholes meeting the 200-ft thickness threshold. These use the
basin area-weighted mean as a Sy fallback, flagged with "(mean)" in the
per-polygon detail table.

Output: `data/polygon_sy_svsim.csv`.

### 3. Built per-polygon GWE spring composites (10 min)

For each polygon's single 2027 GWL RMS well, computed the spring-composite
groundwater elevation:

- SWN-named wells (all 28): mean of Good-QA March measurements per year
- (CWSCH wells use Feb–Apr; not applicable here — no CWSCH wells in the
  28-polygon set since 2027-BC-prop-network dropped them)

Each polygon was baseline-anchored to its first WY 1999–2025 year with
Good March data. 11 polygons anchor to WY 1999; the rest baseline later
(2000–2019).

Notable: Continuous-logger wells produce many March readings per year, but
DWR flags them "Questionable" QA. Following the original methodology, we
use **Good QA only** for storage analysis. This is more restrictive than
the prop-network's threshold-derivation pipeline, which uses all QA flags
because it wants more data points for drought-window statistics. Different
choices for different purposes.

### 4. Computed annual ΔStorage and bucketed by SVI year type (5 min)

For each polygon and year y:

```
ΔStorage_p,y = (GWE_p,y − GWE_p,baseline) × Sy_p × Area_p
```

Multi-year DWR gaps within a polygon were distributed evenly across the
gap and bucketed by each year's Sacramento Valley Index water-year type
(Wet, Above Normal, Below Normal, Dry, Critical).

### 5. Proposed project portfolio mapping → user confirmed (5 min)

The original 17-polygon portfolio (14,500 AF/yr across 6 projects) used
zone labels (24C, 26E, 30L, 29P, 36P, 10B, Chico). Mapped these to the
new full-SWN polygons.

The user provided an updated allocation on review (8 projects, still
14,500 AF/yr total). Final allocations in `data/project_portfolio.json`.

### 6. Computed 2042 sustainability framing (5 min)

Per polygon: hold-steady need = max(0, |avg loss rate|). Project allocation
subtracted from each polygon's hold-steady need = net coverage.

Basin recovery margin = portfolio − basin avg loss rate.

### 7. Rendered SVGs and assembled the single-file index.html (30 min)

Four inlined SVGs:
1. **Polygon map** (700×820, clickable) — colored by net coverage,
   project-bearing wells marked with larger dots
2. **Bar chart** by SVI year type — basin totals across 5 buckets
3. **Cumulative time series** with SVI condition shading bands
4. **Storage context** — proportion view vs. 16 MAF total storage

HTML: single-file `index.html` (~125 KB), all SVGs and the popup JS
inlined. No external dependencies except Google Fonts. Single-file means
no asset paths to fix when deploying to GitHub Pages.

### 8. Pushed to GitHub (cosmo1007/2027-BC-Storage, private) — May 2026

`git init`, `.gitignore` for `.claude/` and `raw/`, initial commit, push
to `main`.

### 9. Added year-type-weighted normalization (Option A) — methodology upgrade

In response to a user question about whether the late-baseline drag could
be corrected scientifically: yes — implemented the year-type-weighted
backcast described in the README §Year-type-weighted normalization.

Key idea: each polygon's per-year-type avg ΔStorage rate (using only its
own observations) is projected across the basin's actual WY 2000–2025
year-type mix. This corrects for the fact that late-baseline polygons
contribute zero to early-record years.

**Outcome:**
- Observed basin cumulative WY 2025: −145,732 AF
- Normalized basin cumulative WY 2025: **−189,209 AF**
- The normalized number is within 2% of the original 17-polygon
  analysis's −193,010 AF — strong validation that the normalization
  reconstructs the basin-wide story consistently.

The dashboard now shows both numbers side by side. The cumulative chart
overlays both lines (solid = observed, dashed = normalized). The
per-polygon detail table has two added columns for normalized cumulative
and normalized avg rate.

---

## Key methodological decisions

| Decision | What we chose | Why |
|---|---|---|
| Polygon framework | 28 Voronoi cells from 2027-BC-prop-network | Each 2027 GWL RMS well gets its own cell; no Chico-dissolve |
| Sy method | DWR SVSim Texture Data, area-weighted | Standard, polygon-by-polygon, reproducible |
| Sy fallback | Basin area-weighted mean (3 polygons) | Honest acknowledgment of borehole-density limits |
| GWE QA filter | Good only | Consistency with original 17-polygon methodology; storage analysis benefits from conservative filter |
| Baseline anchoring | First WY 1999–2025 year with Good March data | Honest per-polygon record start |
| Gap attribution | Linear interpolation across DWR gaps | Standard practice; gap years bucketed by their year type |
| Year-type classification | Sacramento Valley Index (Northern Sierra 8-Station Index) | DWR's official water-year typing |
| Project portfolio | User-specified 8 projects, 14,500 AF/yr | Per AGUBC May 2026 allocation memo |
| Late-baseline correction | Year-type-weighted backcast (Option A) | Each polygon uses only its own data; transparent math; standard SGMA technique |
| Fallback for unobserved year-types | Polygon's overall avg rate | Stays within polygon-own-data principle |

---

## Files produced

```
2027-BC-storage/
├── README.md                          Methodology document for the audience
├── PROJECT_NOTES.md                   This file — project history
├── index.html                         Single-file dashboard
├── scripts/
│   ├── build_sy_svsim.py              Polygon Sy from SVSim
│   ├── build_dashboard.py             Main analysis pipeline
│   └── build_html.py                  index.html template (called by build_dashboard.py)
└── data/
    ├── project_portfolio.json         Editable input — project allocations per polygon
    ├── polygon_sy_svsim.csv           Per-polygon Sy values
    ├── condition_analysis.json        Per-polygon bucket totals + per-type rates
    ├── sustainability_2042.json       Per-polygon + basin 2042 framing (observed + normalized)
    ├── basin_annual.json              Basin annual ΔStorage (observed + normalized series)
    ├── model_data.json                Per-polygon annual GWE + storage
    ├── polygon_storage_2025.csv       Per-polygon WY 2025 detail
    ├── storage_timeseries.csv         Annual basin cumulative
    ├── polygon_map.svg                Interactive polygon map
    ├── basin_buckets_chart.svg        Bar chart by SVI year type
    ├── basin_cumulative_chart.svg     Cumulative time series (both lines)
    └── storage_context.svg            Proportion view vs. 16 MAF
```

---

## Comparison to the 17-polygon original

| | 17-polygon | 28-polygon observed | 28-polygon normalized |
|---|---:|---:|---:|
| Polygons | 17 LWA-authored | 28 Voronoi | 28 Voronoi |
| RMS wells | 21 | 28 | 28 |
| Basin cumulative WY 2025 (AF) | −193,010 | −145,732 | **−189,209** |
| Basin avg loss rate (AF/yr) | 8,558 | 6,322 | **7,277** |
| WY 2022 trough (AF) | −347,215 | −285,567 | (not separately computed) |
| Project portfolio (AF/yr) | 14,500 | 14,500 | 14,500 |
| Recovery margin (AF/yr) | +5,942 | +8,178 | **+7,223** |

The 28-polygon **normalized** numbers are within ~2% of the 17-polygon
basin total. The 28-polygon **observed** numbers are smaller because of
the late-baseline drag.

---

## Outstanding items

- **Project name for `23N01E33A001M`.** Labeled "Recharge project (TBD)"
  pending a specific name. Edit `data/project_portfolio.json` to update.
- **GitHub Pages.** Private-repo Pages requires a manual toggle in the
  repo settings; not enabled here. (User can flip it via Settings → Pages
  → Source: Deploy from a branch → `main` / root.)
- **Continuous-logger data inclusion.** Currently filtered out by
  Good-QA-only rule. If the GSA wants to include them, switch the QA
  filter in `well_spring_year()` in `scripts/build_dashboard.py`.

---

## Reproducing

```bash
# One-time
pip3 install --user pyproj shapely

# Refresh polygon Sy (downloads ~9 MB SVSim CSV on first run)
python3 scripts/build_sy_svsim.py

# Rebuild dashboard
python3 scripts/build_dashboard.py
```

Edit `data/project_portfolio.json` and re-run `build_dashboard.py` to
refresh allocations.
