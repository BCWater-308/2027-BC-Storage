# Vina Subbasin — Where the Losses Happen (2027 BC RMS Network · 29 polygons)

A drought-conditioned look at groundwater storage in the Vina Subbasin,
prepared by **AGUBC** for the Vina GSA technical group and AGUBC Board.

This is the **29-polygon rebuild** of the original
[2027-drought-analysis](https://cosmo1007.github.io/2027-drought-analysis/)
(which used a 17-polygon network). The polygons, RMS wells, and DWR
periodic GWL measurements all come from the companion
[2027-BC-prop-network](https://agubc-vina.github.io/2027-BC-prop-network/)
framework, where every 2027 GWL RMS well gets its own Voronoi cell.

## Two polygon methods, one dashboard

The dashboard has a **toggle at the top** to switch between two polygon
methods. The 28 RMS seed wells are the same in both; only the polygon
shapes (and therefore the area-weighted storage attribution) differ.

| Method | How polygons are built | Cells cross management-area lines? |
|---|---|---|
| **Single basin-wide tessellation** | One Voronoi tessellation across all 28 seed wells, clipped to the DWR B118 Vina Subbasin boundary | Yes |
| **Three-zone (per management area)** | Three INDEPENDENT Voronoi tessellations — one per management area (Vina-North, Vina-Chico, Vina-South) — each clipped to its own management-area boundary | No — hard seams at management-area lines |

The three-zone method is the more SMC-defensible framework: the three
management areas carry distinct sustainable management criteria (especially
for subsidence), so it matters that a polygon's hydrology rolls up to the
zone where the well physically sits, not across boundaries.

**Spatial reassignment:** The three-zone build assigns each seed well to a
management area by spatial containment in the management-area boundary
polygons, not by the workbook tag. **One well (`23N01E33A001M`)** sits in
Vina-Chico but was workbook-tagged Vina-North — the three-zone view shows
it as Chico, and the audit trail (`workbook_mgmt_area` + `reassigned`
flag) is preserved on every polygon for transparency.

### Headline numbers, side by side

|  | Single basin-wide | Three-zone |
|---|---:|---:|
| Polygons in North / Chico / South | 13 / 2 / 13 | 12 / 3 / 13 |
| Basin cumulative WY 2025 (observed, AF) | −145,732 | **−173,395** |
| Basin cumulative WY 2025 (normalized, AF) | −189,209 | **−209,594** |
| Basin avg loss rate (observed, AF/yr) | 6,322 | **7,940** |
| Basin avg loss rate (normalized, AF/yr) | 7,277 | **8,061** |
| Recovery margin vs. 15,500 AF/yr portfolio (observed) | +9,178 | **+7,560** |
| Recovery margin vs. 15,500 AF/yr portfolio (normalized) | +8,223 | **+7,439** |

Both methods show the basin in deficit and the portfolio comfortably
covering the average loss rate. The three-zone method reports a larger
deficit primarily because `23N01E33A001M` (the spatially-reassigned well)
contributes a deeper loss when sited in its new Chico polygon, and because
several polygons get different Sy values after the SVSim recompute against
the new shapes (e.g. `23N01E29P002M` jumps from a basin-mean fallback to a
proper 0.0629 SVSim value in three-zone because the smaller Chico-bounded
polygon now captures enough boreholes).

## The two questions this dashboard answers

> **When and where is the basin losing water, and what would it take to be
> sustainable by 2042?**

## Headline finding

Loss is concentrated in drought years, not uniform. **Critical and Dry years
remove about 442k AF** across WY 1999–2025; **Wet and Above-Normal years
recover about 334k AF**. Two basin totals (see [Year-type-weighted normalization](#year-type-weighted-normalization) below for why both):

- **Observed** basin net deficit through WY 2025: **−145,732 AF** — what the
  data show directly, with late-baseline polygons contributing only the
  years they observed.
- **Normalized** basin net deficit through WY 2025: **−189,209 AF** — what
  the basin would show if every polygon had a full WY 1999–2025 record,
  computed by year-type-weighted backcast from each polygon's own data.

Both are small relative to the **16+ MAF** of fresh groundwater storage in
the subbasin (2022 Vina GSP, p. ES-5): observed is **0.91%** of total
storage; normalized is **1.18%**. The observed WY 2022 trough reaches
**−285,567 AF** (≈1.78% of total storage).

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

| Aspect | 17-polygon original | 29-polygon rebuild |
|--------|---------------------|--------------------|
| Polygons | 17 LWA-authored cells | 29 Voronoi cells, one per 2027 GWL RMS well |
| RMS wells | 21 wells (some polygons had 2+) | 29 wells (1:1 with polygons) |
| Chico | Single dissolved cell | Split into two cells (22N01E09B001M, 22N01E20K001M) |
| Sy method | DWR SVSim Texture Data, area-weighted | Same — recomputed against new polygon geometry |
| Basin net WY 2025 | −193,010 AF | **−145,732 AF** |
| Basin avg loss rate | 8,558 AF/yr | **6,322 AF/yr** |
| Project portfolio | 14,500 AF/yr | **15,500 AF/yr** (Rock Creek concentrated at 36P + 29P) |
| Recovery margin | +5,942 AF/yr | **+9,178 AF/yr** (single, observed) |

The basin deficit comes out smaller in the 29-polygon rebuild for three
reasons:

1. **`21N02E18C003M` is larger** in the new tessellation (no Chico-dissolve
   geometry constraint) and posts a +23,569 AF surplus.
2. **The two new Chico cells are smaller** than the old dissolved Chico
   polygon and capture less area-weighted drawdown.
3. **More late-baseline polygons** in the 28-set means more years where some
   polygons can't yet contribute to the basin sum.

The shape of the curve (drought losses concentrated in Critical/Dry years,
Wet/Above-Normal years recovering) is unchanged.

## Year-type-weighted normalization

### The problem this corrects

Of the 29 polygons, only **11 have a Good-quality March measurement in WY
1999** and can baseline there. The other 17 baseline later — between 2000
and 2019 — because their 2027 GWL RMS well wasn't measured in 1999. Each
polygon contributes year-over-year deltas only for the years it has a
baseline-anchored record. Late-baseline polygons therefore cannot register
their pre-baseline drawdown.

| Baseline year cohort | Polygons |
|---|---|
| WY 1999 | 11 (e.g. 05M, 36P, 25C, 29P, 09E, 10M, 14R, 27L, 10B, 25K, 27D, 33L) |
| 2000 | 24C, 32B |
| 2002 | 02H, 09G, 10M |
| 2003 | 33A |
| 2008 | 08H |
| 2009 | 28M, 31M, 32E |
| 2011 | 18C |
| 2012 | 03H, 13L |
| 2019 | 07H |

This creates a real bias: the basin's observed 1999–2025 cumulative
*understates* the deficit because polygons that started drawing down before
their first measurement get a "free pass" on their pre-baseline losses.
The 18C surplus of +23,569 AF, for example, is partly an artifact of
starting after the 2007–09 dry stretch.

### The normalization method (Option A — year-type-weighted backcast)

For each polygon, we use only its own observations to compute an average
ΔStorage rate *per Sacramento Valley Index year type* (Wet, Above Normal,
Below Normal, Dry, Critical):

```
rate_p,t = sum of polygon p's ΔStorage in years of type t / # years of
           type t the polygon observed
```

We then synthesize what each polygon would have contributed across the
full WY 1999–2025 record by applying its per-type rates to the basin's
actual year-type mix:

```
normalized_cum_p = sum over t of (rate_p,t × N_t)
```

where `N_t` is the number of years of type t in WY 2000–2025:
**6 Wet, 4 Above Normal, 5 Below Normal, 6 Dry, 5 Critical = 26
transition years**.

Summing across all 28 polygons gives the normalized basin total.

### Why this is defensible

- **Each polygon uses only its own observations.** No proxying from
  neighboring wells, no model fill. The normalized rate at polygon X is
  built entirely from what was measured at polygon X.
- **Captures the dominant hydrologic signal.** Drought-year loss rates and
  wet-year recovery rates are fundamentally different. Lumping them
  together (as a simple "AF/yr × years" multiplier would) understates the
  asymmetry. The year-type-weighted approach preserves it.
- **Standard normalization in SGMA storage assessments.** The Vina GSP
  itself uses water-year-type weighting for various basin-scale stats; this
  is the same idea applied to per-polygon storage rates.
- **The math is fully transparent.** Reviewers can audit every polygon's
  rates_per_bucket in `data/condition_analysis.json` and re-derive the
  basin total by hand if they want.

### Fallback for unobserved year-types

A late-baseline polygon may not have observed every SVI year type. The
fallback rule: if polygon p never observed year-type t, use p's own
overall average rate (sum of all its deltas ÷ its span years) as the
rate for that year type. The dashboard flags any polygon using a fallback
with "(fb)" in the per-polygon detail table.

In practice this only affects **one polygon-type combination** in the
current data: `23N01E07H001M` baselines in WY 2019 and has not observed a
Below-Normal year (no BN years occurred in 2019–2025). Its overall avg
rate is substituted for its BN-year rate. The effect on the basin total
is small (~70 AF/yr at most).

### Headline impact

| | Observed | Normalized | Delta |
|---|---:|---:|---:|
| Basin cumulative WY 2025 | −145,732 AF | **−189,209 AF** | +43,477 AF more deficit |
| Basin avg loss rate | 6,322 AF/yr | **7,277 AF/yr** | +955 AF/yr more loss |
| Polygon-summed hold-steady need | 8,122 AF/yr | **8,136 AF/yr** | ~unchanged |
| Recovery margin (vs. 15,500 AF/yr portfolio) | +9,178 AF/yr | **+8,223 AF/yr** | −955 AF/yr |

The portfolio's recovery margin remains comfortably positive against
either basis (+9,178 AF/yr observed, +8,223 AF/yr normalized — about
3.5% of GSP-stated sustainable yield).

The normalized basin cumulative (−189k AF) is very close to the original
17-polygon analysis's −193k AF — strong validation that the late-baseline
drag is real, that the normalization corrects it, and that the underlying
hydrologic story is consistent across both polygon networks.

### Limitations to disclose

- **Stationarity assumption.** The normalization assumes each polygon's
  year-type response is stationary — i.e., a Critical year in 2008 would
  draw the polygon down at the same rate as a Critical year in 2014. This
  is reasonable for short windows but may not hold over multi-decade
  windows if pumping patterns or recharge sources shift.
- **Small-sample noise on late-baseline polygons.** Polygons with short
  records have noisier per-type rates. `23N01E07H001M` (baselines 2019)
  has only 6 transition years observed across 4 of the 5 year types.
  Other late-baseline polygons (baselines 2008–2012) have more years
  observed and noise is lower.
- **No spatial correction.** The normalization adjusts each polygon
  individually; it doesn't reconcile across polygons (e.g., a recovering
  18C area can't "lend" surplus to a draining Chico area). That's a
  feature, not a bug — connectivity isn't modeled here anyway.
- **Below-Normal-year coverage for `23N01E07H001M`.** As noted, the
  fallback rule applies. Small numerical effect; flagged for transparency.

## 2042 sustainability target — hold the line, with the project portfolio

The basin has lost storage across the WY 1999–2025 record — and even at the
WY 2022 trough, no SGMA sustainability indicator registered an undesirable
result. The framing is: **hold GWE at each Groundwater Level RMS well at or
above its WY 2022 level**, with the project portfolio bending the curve
back upward.

| Metric                                                 | AF/yr        | % of 233,500 AF/yr SY |
|--------------------------------------------------------|-------------:|----------------------:|
| Basin avg loss rate (hold-steady need)                 | **6,322**    | 2.7%                  |
| Project portfolio (online by 2032)                     | **15,500**   | 6.6%                  |
| **Recovery margin** (portfolio − loss)                 | **+9,178**   | **+3.9%**             |

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
| `23N01W36P001M` | Rock Creek recharge | 3,500 |
| `23N01E29P002M` | Rock Creek recharge | 3,500 |
| **Total** |  | **15,500** |

After the portfolio is online, the largest residual shortfalls are:
**`21N01E13L004M`** (~1,000 AF/yr), **`22N01E20K001M`** Chico-S (~858),
**`22N01E09B001M`** Chico-N (~622), **`21N01E27D001M`** (~581), and
**`21N02E26E006M`** (~536) — combined ~3,600 AF/yr deficit not covered by
any current project. The
project portfolio's basin-level recovery margin of **+9,178 AF/yr** means
surplus capacity in over-allocated polygons more than offsets these
shortfalls at basin scale; whether that holds at each RMS well depends on
lateral hydraulic connectivity that this dashboard does not model.

## Polygon set + baseline anchoring

The 2027 BC RMS network is **29 Voronoi polygons** (one per 2027 GWL RMS
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
  the 29-polygon network range **0.0594 to 0.1172**; basin area-weighted
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

# 2. (one-time per Sy refresh) recompute polygon Sy via SVSim for BOTH methods
python3 scripts/build_sy_svsim.py
# downloads /tmp/svsim/svsim_texture_data.csv (~9 MB) on first run,
# writes data/polygon_sy_svsim_single.csv and data/polygon_sy_svsim_three_zone.csv

# 3. Build the dashboard
python3 scripts/build_dashboard.py
# reads polygons (both methods), wells, and measurements from 2027-BC-prop-network/,
# reads the per-method Sy CSVs and data/project_portfolio.json,
# writes per-method JSON/CSV/SVG outputs and the single-file index.html with toggle
```

Both scripts read polygons + wells + measurements from the sibling
[`2027-BC-prop-network`](https://github.com/agubc-vina/2027-BC-prop-network)
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
