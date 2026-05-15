# Vina Subbasin — Where the Losses Happen (2027 BC RMS Network · 28 polygons)

A drought-conditioned look at groundwater storage in the Vina Subbasin,
prepared by **AGUBC** for the Vina GSA technical group and AGUBC Board.

This is the **28-polygon rebuild** of the original
[2027-drought-analysis](https://cosmo1007.github.io/2027-drought-analysis/)
(which used a 17-polygon network). The polygons, RMS wells, and DWR
periodic GWL measurements all come from the companion
[2027-BC-prop-network](https://cosmo1007.github.io/2027-BC-prop-network/)
framework, where every 2027 GWL RMS well gets its own Voronoi cell clipped
to the DWR B118 5-021.57 Vina Subbasin boundary.

## The two questions this dashboard answers

> **When and where is the basin losing water, and what would it take to be
> sustainable by 2042?**

## Headline finding

Loss is concentrated in drought years, not uniform. **Critical and Dry years
remove about 442k AF** across WY 1999–2025; **Wet and Above-Normal years
recover about 334k AF**. The basin net deficit through WY 2025 is
**−145,732 AF** (about **0.91% of the 16+ MAF** in fresh groundwater storage
per the 2022 Vina GSP, p. ES-5). The WY 2022 trough reaches **−285,567 AF**
(≈1.78% of total storage).

| Condition                    | Years | Total ΔStorage (AF) | Avg per year |
|------------------------------|------:|--------------------:|-------------:|
| Wet                          | 6     | **+287,071**        | +47,845      |
| Above Normal                 | 4     | **+47,014**         | +11,753      |
| Below Normal                 | 5     | **−37,848**         | −7,570       |
| Dry                          | 6     | **−212,081**        | −35,347      |
| Critical                     | 5     | **−229,887**        | −45,977      |
| Net basin (WY 1999–2025)     | 26    | **−145,732**        | —            |

Year-type classification uses DWR's official **Sacramento Valley Index**
(Northern Sierra 8-Station Index).

## What's different from the 17-polygon original

| Aspect | 17-polygon original | 28-polygon rebuild |
|--------|---------------------|--------------------|
| Polygons | 17 LWA-authored cells | 28 Voronoi cells, one per 2027 GWL RMS well |
| RMS wells | 21 wells (some polygons had 2+) | 28 wells (1:1 with polygons) |
| Chico | Single dissolved cell | Split into two cells (22N01E09B001M, 22N01E20K001M) |
| Sy method | DWR SVSim Texture Data, area-weighted | Same — recomputed against new polygon geometry |
| Basin net WY 2025 | −193,010 AF | **−145,732 AF** |
| Basin avg loss rate | 8,558 AF/yr | **6,322 AF/yr** |
| Project portfolio | 14,500 AF/yr | **14,500 AF/yr** (same projects, 30L → 32E remap) |
| Recovery margin | +5,942 AF/yr | **+8,178 AF/yr** |

The basin deficit comes out smaller in the 28-polygon rebuild for three
reasons:

1. **`21N02E18C003M` is larger** in the new tessellation (no Chico-dissolve
   geometry constraint) and posts a +23,569 AF surplus.
2. **The two new Chico cells are smaller** than the old dissolved Chico
   polygon and capture less area-weighted drawdown.
3. **More late-baseline polygons** in the 28-set means more years where some
   polygons can't yet contribute to the basin sum.

The shape of the curve (drought losses concentrated in Critical/Dry years,
Wet/Above-Normal years recovering) is unchanged.

## 2042 sustainability target — hold the line, with the project portfolio

The basin has lost storage across the WY 1999–2025 record — and even at the
WY 2022 trough, no SGMA sustainability indicator registered an undesirable
result. The framing is: **hold GWE at each Groundwater Level RMS well at or
above its WY 2022 level**, with the project portfolio bending the curve
back upward.

| Metric                                                 | AF/yr        | % of 233,500 AF/yr SY |
|--------------------------------------------------------|-------------:|----------------------:|
| Basin avg loss rate (hold-steady need)                 | **6,322**    | 2.7%                  |
| Project portfolio (online by 2032)                     | **14,500**   | 6.2%                  |
| **Recovery margin** (portfolio − loss)                 | **+8,178**   | **+3.5%**             |

Sustainable yield = 233,500 AF/yr per the 2022 Vina GSP (Dec 15, 2021),
p. ES-5: 243,500 AFY historical pumping minus 10,000 AFY decrease in
storage. Used here as a denominator only; volumetric needs (AF/yr) do not
depend on it.

## Project portfolio

Edit `data/project_portfolio.json` and re-run `scripts/build_dashboard.py` to
refresh allocations.

| Polygon (full SWN) | Project | AF/yr |
|----|----|----:|
| `20N02E08H003M` | Conjunctive use | 2,250 |
| `20N02E09G001M` | Conjunctive use | 2,250 |
| `20N02E24C001M` | Conjunctive use | 1,250 |
| `20N03E33L001M` | Conjunctive use | 1,250 |
| `21N01E10B003M` | Comanche Creek recharge | 1,500 |
| `23N01W36P001M` | Rock Creek recharge | 2,000 |
| `23N01E29P002M` | Rock Creek recharge | 2,000 |
| `23N01E33A001M` | Recharge project (TBD) | 2,000 |
| **Total** |  | **14,500** |

After the portfolio is online, the largest residual shortfalls are:
**`21N01E13L004M`** (~1,000 AF/yr), **`22N01E20K001M`** Chico-S (~858),
**`22N01E09B001M`** Chico-N (~622), **`21N01E27D001M`** (~581), and
**`21N02E26E006M`** (~536) — combined ~3,600 AF/yr deficit not covered by
any current project. The
project portfolio's basin-level recovery margin of **+8,178 AF/yr** means
surplus capacity in over-allocated polygons more than offsets these
shortfalls at basin scale; whether that holds at each RMS well depends on
lateral hydraulic connectivity that this dashboard does not model.

## Polygon set + baseline anchoring

The 2027 BC RMS network is **28 Voronoi polygons** (one per 2027 GWL RMS
well, clipped to the DWR B118 Vina Subbasin boundary, projected through
EPSG:3310 NAD-83 California Albers Equal Area). Polygon roster comes from
the `2027-BC-prop-network` build (`scripts/build_polygons.py` there), tied
to `BC Network 2026 v8.xlsx` column E (`2027 GWL RMS?`).

Each polygon is baseline-anchored to the first WY 1999–2025 year with a
Good-quality March measurement at its RMS well. Eleven polygons anchor to
WY 1999; the rest baseline later because their 2027 RMS well wasn't
measured in 1999.

## Method, in brief

- **Storage:** ΔStorage<sub>p,y</sub> = (GWE<sub>p,y</sub> − GWE<sub>p,baseline</sub>) × Sy<sub>p</sub> × Area<sub>p</sub>.
- **Specific yield:** polygon-by-polygon, derived from DWR's SVSim
  Texture Data (Sacramento Valley Simulation Model v1.0, CKAN resource
  `544623e2-0cd5-4c5b-827f-affa4abf4e16`). Coarse-grained sediments →
  0.15, fine-grained → 0.05, area-weighted by borehole lithology in the
  0–500 ft below ground surface analysis window. Polygon Sy values for
  the 28-polygon network range **0.0594 to 0.1172**; basin area-weighted
  mean ≈ 0.087. Three polygons with insufficient SVSim borehole density
  (`23N02W25C001M`, `23N01E29P002M`, `21N01E25K001M`) use the basin
  area-weighted mean as a fallback. See [`scripts/build_sy_svsim.py`](scripts/build_sy_svsim.py)
  for the full pipeline.
- **GWE:** spring composite for each polygon's single 2027 GWL RMS well
  (March mean for SWN-named wells; Feb–Apr mean for CWSCH wells), Good-quality DWR
  records only.
- **Hydrologic year classification** uses DWR's official Sacramento Valley
  Index (Northern Sierra 8-Station Index) — Wet / Above Normal / Below
  Normal / Dry / Critical.
- **Gap attribution:** when a polygon has a multi-year gap in DWR Good
  measurements, the cumulative storage delta across the gap is distributed
  evenly across the missing years and bucketed by each year's hydrologic
  condition.
- **2042 framing:** per polygon, hold-steady need = max(0, |avg loss
  rate|). Project allocations are then subtracted from each polygon's
  hold-steady need to compute net coverage. Basin-level recovery margin =
  project portfolio − basin avg loss rate.

## What's in this repo

| File                              | Purpose                                                        |
|-----------------------------------|----------------------------------------------------------------|
| `index.html`                      | The dashboard — single-file HTML, ready to push to GitHub Pages |
| `scripts/build_sy_svsim.py`       | Recomputes polygon Sy from DWR's SVSim Texture Data            |
| `scripts/build_dashboard.py`      | Main analysis — reads polygons + measurements, computes storage |
| `scripts/build_html.py`           | Single-file HTML/CSS/JS template (called by build_dashboard.py) |
| `data/polygon_sy_svsim.csv`       | Polygon-by-polygon Sy values (output of build_sy_svsim.py)     |
| `data/project_portfolio.json`     | Project allocations per polygon (editable input)               |
| `data/condition_analysis.json`    | Per-polygon storage attribution by SVI water-year type         |
| `data/sustainability_2042.json`   | Per-polygon and basin sustainability target + project coverage  |
| `data/basin_annual.json`          | Basin-wide gap-attributed annual ΔStorage                      |
| `data/model_data.json`            | Per-polygon annual GWE + storage time series                   |
| `data/polygon_storage_2025.csv`   | Per-polygon WY 2025 detail (csv)                               |
| `data/storage_timeseries.csv`     | Annual basin cumulative storage 1999–2025 (csv)                |
| `data/polygon_map.svg`            | Interactive polygon map (colored by net coverage)              |
| `data/basin_buckets_chart.svg`    | Bar chart — basin storage by SVI year type                     |
| `data/basin_cumulative_chart.svg` | Time series — basin cumulative ΔStorage with SVI bands         |
| `data/storage_context.svg`        | Two-panel proportion view (16 MAF total vs cumulative deficit) |

## Reproducing

```bash
# 1. (one-time) Python deps used by build_sy_svsim.py
pip3 install --user pyproj shapely

# 2. (one-time per Sy refresh) recompute polygon Sy via SVSim
python3 scripts/build_sy_svsim.py
# downloads /tmp/svsim/svsim_texture_data.csv (~9 MB) on first run,
# writes data/polygon_sy_svsim.csv

# 3. Build the dashboard
python3 scripts/build_dashboard.py
# reads polygons, wells, and measurements from sibling 2027-BC-prop-network/,
# reads data/polygon_sy_svsim.csv and data/project_portfolio.json,
# writes all data/*.json, data/*.svg, data/*.csv files and index.html
```

Both scripts read polygons + wells + measurements from the sibling
[`2027-BC-prop-network`](https://github.com/cosmo1007/2027-BC-prop-network)
repo (`../2027-BC-prop-network/js/*.js`). To refresh upstream data, re-run
the prop-network repo's `scripts/fetch_dwr_measurements.py` and then
rebuild here.

## Editing the project portfolio

`data/project_portfolio.json` is a hand-edited input. Each entry has a
target polygon (full SWN), project name, category, and AF/yr allocation.
Edit it and re-run `python3 scripts/build_dashboard.py` to refresh the
coverage map, the per-polygon table, and the 2042 sustainability framing.

## Live dashboard

Push this folder to a GitHub repo (e.g., `cosmo1007/2027-BC-storage`) and
enable Pages → branch `main`, folder `/ (root)`. The interactive briefing
at `index.html` is single-file (all SVGs and JS inlined), so no asset paths
to fix up after deploy.

Click any polygon on the map for per-polygon detail (Sy, ΔGWE/yr, drought
share of drawdown, project allocation, and net coverage status).

## Status

Independent analysis prepared by AGUBC for internal discussion with
Vina GSA technical staff and AGUBC Board members. Comments and corrections
welcomed.
