#!/usr/bin/env python3
"""
Single-file index.html generator for the 28-polygon 2027 BC drought-storage
dashboard.  Called by build_dashboard.py.
"""

from __future__ import annotations

# Year-type metadata duplicated from build_dashboard.py so this module can
# format SVI badges without circular imports.
SVI_YEAR_TYPE = {
    1999: "Wet",            2000: "Above Normal",   2001: "Dry",
    2002: "Dry",            2003: "Above Normal",   2004: "Below Normal",
    2005: "Above Normal",   2006: "Wet",            2007: "Dry",
    2008: "Critical",       2009: "Dry",            2010: "Below Normal",
    2011: "Wet",            2012: "Below Normal",   2013: "Dry",
    2014: "Critical",       2015: "Critical",       2016: "Below Normal",
    2017: "Wet",            2018: "Below Normal",   2019: "Wet",
    2020: "Dry",            2021: "Critical",       2022: "Critical",
    2023: "Wet",            2024: "Above Normal",   2025: "Wet",
}
START_YEAR = 1999
END_YEAR = 2025
PROJECTS_ONLINE_YEAR = 2032
SUSTAINABLE_YIELD_AFY = 233_500
TOTAL_FRESH_STORAGE_AF = 16_000_000


def classify_year(y: int) -> str:
    return {"Wet": "wet", "Above Normal": "an", "Below Normal": "bn",
            "Dry": "dry", "Critical": "critical"}.get(
        SVI_YEAR_TYPE.get(y, "Wet"), "wet")


def year_type_full(y: int) -> str:
    return SVI_YEAR_TYPE.get(y, "Wet")


INDEX_CSS = """
:root {
  --bg: #faf8f3; --bg-card: #ffffff; --ink: #1a1612; --ink-muted: #5b5547;
  --rule: #cfc9b8; --accent: #1f3a5f; --warn: #a32d2d; --tan: #7c6a3e;
  --tan-soft: #d99a4f; --grey-soft: #c8cdc6; --good: #2e6f3f;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: 'Spectral', 'Iowan Old Style', 'Palatino', Georgia, 'Times New Roman', serif;
  font-size: 17px; line-height: 1.55; color: var(--ink); background: var(--bg);
  -webkit-font-smoothing: antialiased;
}
h1, h2, h3, h4 {
  font-family: 'Inter', -apple-system, ui-sans-serif, system-ui, sans-serif;
  font-weight: 700; letter-spacing: -0.012em; line-height: 1.2; color: var(--ink);
}
h1 { font-size: 30px; margin: 0 0 4px 0; }
h2 { font-size: 22px; margin: 36px 0 14px 0; padding-top: 18px; border-top: 1.5px solid var(--rule); }
h3 { font-size: 17px; margin: 22px 0 8px 0; }
h4 { font-size: 14px; margin: 14px 0 6px 0; text-transform: uppercase; letter-spacing: 0.04em; color: var(--ink-muted); }
p { margin: 0 0 14px 0; }
ul, ol { margin: 8px 0 16px 0; padding-left: 24px; }
li { margin-bottom: 5px; }
em { font-style: italic; color: var(--ink); }
strong { font-weight: 700; }
code { font-family: 'JetBrains Mono', 'SF Mono', ui-monospace, monospace; font-size: 0.92em; background: #f1ede2; padding: 1px 5px; border-radius: 3px; color: var(--ink); }
.container { max-width: 980px; margin: 0 auto; padding: 36px 28px 80px 28px; }
.subtitle { color: var(--ink-muted); font-size: 14px; font-family: 'Inter', sans-serif; margin: 0 0 32px 0; }
.lead { font-size: 18px; line-height: 1.55; color: var(--ink); }
.headline { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; margin: 28px 0 18px 0; }
@media (max-width: 720px) { .headline { grid-template-columns: 1fr; } }
.stat { background: var(--bg-card); border: 1px solid var(--rule); padding: 20px 22px; border-left-width: 4px; }
.stat.warn { border-left-color: var(--warn); }
.stat.acc { border-left-color: var(--accent); }
.stat.tan { border-left-color: var(--tan-soft); }
.stat.good { border-left-color: var(--good); }
.stat .num { font-family: 'Inter', sans-serif; font-size: 32px; font-weight: 800; letter-spacing: -0.02em; line-height: 1.05; color: var(--ink); }
.stat .num.warn { color: var(--warn); }
.stat .num.acc { color: var(--accent); }
.stat .num.tan { color: var(--tan); }
.stat .num.good { color: var(--good); }
.stat .lab { font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--ink-muted); margin-top: 8px; }
.stat .det { font-size: 13px; color: var(--ink-muted); margin-top: 8px; line-height: 1.5; }
.callout { background: #f5f1e8; border-left: 4px solid var(--accent); padding: 18px 22px; margin: 22px 0; font-size: 16px; line-height: 1.55; }
.callout.warn { border-left-color: var(--warn); background: #fbf3ee; }
.callout.tan { border-left-color: var(--tan); background: #f7f1e1; }
.callout.good { border-left-color: var(--good); background: #ecf3ed; }
table { border-collapse: collapse; width: 100%; font-family: 'Inter', sans-serif; font-size: 13px; margin: 14px 0 22px 0; background: var(--bg-card); }
th, td { padding: 8px 10px; text-align: left; border-bottom: 1px solid var(--rule); }
th { background: #f1ede2; font-weight: 700; text-transform: uppercase; letter-spacing: 0.03em; font-size: 11px; color: var(--ink); }
td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; }
tr:hover td { background: #f9f6ee; }
.gain { color: var(--good); font-weight: 600; }
.loss { color: var(--warn); font-weight: 600; }
.late { color: var(--tan); font-style: italic; font-weight: 500; }
.fallback { color: #8a5a18; font-style: italic; font-size: 11px; }
.figure { margin: 18px 0 6px 0; }
.figure svg { display: block; max-width: 100%; height: auto; border: 1px solid var(--rule); background: #fafaf7; }
.figcaption { font-size: 12px; color: var(--ink-muted); margin: 6px 0 18px 2px; font-style: italic; }
.bigstat { background: var(--bg-card); border: 1px solid var(--rule); padding: 28px 32px; border-left: 4px solid var(--good); margin: 24px 0; }
.bigstat .row { display: flex; gap: 36px; align-items: baseline; flex-wrap: wrap; }
.bigstat .num { font-family: 'Inter', sans-serif; font-size: 44px; font-weight: 800; letter-spacing: -0.02em; line-height: 1; color: var(--good); }
.bigstat .lab { font-family: 'Inter', sans-serif; font-size: 13px; color: var(--ink-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; margin-top: 6px; }
.bigstat .pct { font-family: 'Inter', sans-serif; font-size: 28px; font-weight: 700; color: var(--ink); }
.bigstat .desc { flex: 1 1 280px; font-size: 14px; color: var(--ink); line-height: 1.55; }
.map-wrap { position: relative; }
#polygon-popup { position: absolute; display: none; background: var(--bg-card); border: 1px solid var(--ink-muted); border-radius: 4px; box-shadow: 0 4px 16px rgba(0,0,0,0.16); padding: 14px 16px 12px 16px; font-family: 'Inter', sans-serif; font-size: 13px; line-height: 1.5; max-width: 380px; z-index: 100; pointer-events: auto; }
#polygon-popup .popup-close { position: absolute; top: 6px; right: 8px; background: none; border: none; font-size: 18px; cursor: pointer; color: var(--ink-muted); padding: 2px 6px; line-height: 1; }
#polygon-popup h4 { margin: 0 18px 8px 0; font-size: 14px; }
#polygon-popup .popup-row { display: flex; justify-content: space-between; gap: 14px; padding: 3px 0; border-bottom: 1px dashed #e7e1cf; }
#polygon-popup .popup-row:last-child { border-bottom: none; }
#polygon-popup .popup-row .k { color: var(--ink-muted); font-weight: 500; }
#polygon-popup .popup-row .v { font-weight: 700; font-variant-numeric: tabular-nums; }
#polygon-popup .popup-row .v.gain { color: var(--good); }
#polygon-popup .popup-row .v.loss { color: var(--warn); }
#polygon-popup .popup-section { font-weight: 700; font-size: 11px; text-transform: uppercase; color: var(--ink-muted); margin-top: 10px; letter-spacing: 0.03em; }
#polygon-popup .popup-need { background: #ecf3ed; padding: 10px 12px; margin-top: 10px; border-radius: 3px; font-size: 13px; line-height: 1.4; border-left: 3px solid var(--good); }
#polygon-popup .popup-need .big { font-size: 22px; font-weight: 800; color: var(--good); display: block; margin-top: 2px; }
#polygon-popup .popup-late { background: #faf1dc; color: #6e5615; padding: 8px 10px; margin-top: 10px; border-radius: 3px; font-size: 12px; line-height: 1.4; }
details { margin: 16px 0; padding: 12px 18px; background: var(--bg-card); border: 1px solid var(--rule); border-left: 4px solid var(--tan); }
details summary { cursor: pointer; font-family: 'Inter', sans-serif; font-weight: 600; font-size: 14px; color: var(--ink); }
details[open] summary { margin-bottom: 12px; }
.footer { margin-top: 60px; padding-top: 18px; border-top: 1.5px solid var(--rule); font-size: 13px; color: var(--ink-muted); font-family: 'Inter', sans-serif; line-height: 1.5; }
a { color: var(--accent); text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 2px; }
a:hover { background: #fff1cc; }
"""

POPUP_JS = """
(function() {
  const popup = document.getElementById('polygon-popup');
  const ppName = document.getElementById('pp-name');
  const ppBody = document.getElementById('pp-body');
  const closeBtn = popup.querySelector('.popup-close');
  const wrap = document.querySelector('.map-wrap');

  function fmtClass(s) {
    if (!s) return '';
    if (s.startsWith('+')) return 'gain';
    if (s.startsWith('-')) return 'loss';
    return '';
  }

  function showPopup(path, evt) {
    const d = path.dataset;
    ppName.textContent = d.short + ' (' + d.ma + ')';
    let html = '';
    html += `<div class="popup-row"><span class="k">RMS well(s)</span><span class="v">${d.rmsWells.replace(/;/g, ', ')}</span></div>`;
    html += `<div class="popup-row"><span class="k">Area</span><span class="v">${d.area} ac</span></div>`;
    html += `<div class="popup-row"><span class="k">Span</span><span class="v">${d.baseYear}–${d.endYear} (${d.span} yr)</span></div>`;
    html += `<div class="popup-row"><span class="k">Avg ΔGWE/yr</span><span class="v ${fmtClass(d.avgDgwe)}">${d.avgDgwe} ft</span></div>`;
    html += `<div class="popup-row"><span class="k">Cumulative ΔStorage</span><span class="v ${fmtClass(d.cumStor)}">${d.cumStor} AF</span></div>`;
    html += `<div class="popup-row"><span class="k">Avg storage rate</span><span class="v ${fmtClass(d.avgRate)}">${d.avgRate} AF/yr</span></div>`;
    html += `<div class="popup-row"><span class="k">Critical + Dry share of drawdown</span><span class="v">${d.critdryShare}</span></div>`;
    html += `<div class="popup-row"><span class="k">Critical only</span><span class="v">${d.critShare}</span></div>`;
    html += `<div class="popup-section">By Sac Valley Index year type</div>`;
    html += `<div class="popup-row"><span class="k">Wet</span><span class="v ${fmtClass(d.bucketWet)}">${d.bucketWet} AF</span></div>`;
    html += `<div class="popup-row"><span class="k">Above Normal</span><span class="v ${fmtClass(d.bucketAn)}">${d.bucketAn} AF</span></div>`;
    html += `<div class="popup-row"><span class="k">Below Normal</span><span class="v ${fmtClass(d.bucketBn)}">${d.bucketBn} AF</span></div>`;
    html += `<div class="popup-row"><span class="k">Dry</span><span class="v ${fmtClass(d.bucketDry)}">${d.bucketDry} AF</span></div>`;
    html += `<div class="popup-row"><span class="k">Critical</span><span class="v ${fmtClass(d.bucketCritical)}">${d.bucketCritical} AF</span></div>`;
    const syExtra = d.sySource === 'SVSim' ? '' : ' <span style="color:#8a5a18;font-style:italic;font-size:11px;">(basin-mean fallback)</span>';
    html += `<div class="popup-row"><span class="k">Specific yield</span><span class="v">${d.sy}${syExtra}</span></div>`;
    html += `<div class="popup-section">Hold-current sustainability</div>`;
    const hold = parseInt(d.hold.replace(/,/g, ''), 10);
    const project = parseInt(d.project.replace(/,/g, ''), 10);
    html += `<div class="popup-row"><span class="k">Avg loss rate</span><span class="v">${d.hold} AF/yr</span></div>`;
    const projDisplay = project > 0 ? `${d.project} AF/yr <span style="font-weight:400;color:#5b5547;font-size:11px;">(${d.projectName})</span>` : '— none here —';
    html += `<div class="popup-row"><span class="k">Project allocation</span><span class="v">${projDisplay}</span></div>`;
    const coverage = parseInt(d.coverage.replace(/,/g, '').replace('+', ''), 10);
    let coverageBg, coverageColor, coverageLabel;
    if (hold === 0 && project === 0) {
      coverageBg = '#ecf3ed'; coverageColor = '#2e6f3f';
      coverageLabel = 'Surplus polygon — no loss to offset, no project sited here.';
    } else if (coverage >= 0) {
      coverageBg = '#ecf3ed'; coverageColor = '#2e6f3f';
      coverageLabel = `Project covers loss with +${coverage.toLocaleString()} AF/yr to spare.`;
    } else {
      coverageBg = '#fbf0e7'; coverageColor = '#8a3a18';
      coverageLabel = `Polygon-level shortfall of ${Math.abs(coverage).toLocaleString()} AF/yr after project portfolio.`;
    }
    html += `<div class="popup-need" style="background:${coverageBg};border-left-color:${coverageColor}"><div style="font-size:11px;text-transform:uppercase;letter-spacing:0.04em;color:#5b5547;font-weight:700;">Net coverage after portfolio</div><span class="big" style="color:${coverageColor}">${d.coverage} AF/yr</span><div style="font-size:12px;margin-top:4px;color:#5b5547;">${coverageLabel}</div></div>`;
    if (d.late === '1') {
      html += `<div class="popup-late">Late baseline: this polygon's RMS well wasn't measured in 1999, so its record starts at ${d.baseYear}. Pre-${d.baseYear} drawdown is not captured.</div>`;
    }
    ppBody.innerHTML = html;

    const rect = wrap.getBoundingClientRect();
    let x = evt.clientX - rect.left + 12;
    let y = evt.clientY - rect.top + 12;
    popup.style.display = 'block';
    const popRect = popup.getBoundingClientRect();
    if (x + popRect.width > rect.width) x = rect.width - popRect.width - 8;
    if (y + popRect.height > rect.height) y = rect.height - popRect.height - 8;
    popup.style.left = x + 'px';
    popup.style.top = y + 'px';
  }

  document.querySelectorAll('path.poly').forEach(p => {
    p.addEventListener('click', (e) => { e.stopPropagation(); showPopup(p, e); });
  });
  closeBtn.addEventListener('click', () => popup.style.display = 'none');
  document.addEventListener('click', (e) => {
    if (!popup.contains(e.target) && !e.target.closest('path.poly')) {
      popup.style.display = 'none';
    }
  });
})();
"""


def loss_or_gain_span(v, decimals=0):
    cls = "gain" if v > 0 else "loss" if v < 0 else ""
    fmt = f"{{:+,.{decimals}f}}".format(v) if v != 0 else f"{{:,.{decimals}f}}".format(v)
    return f'<span class="{cls}">{fmt}</span>' if cls else fmt


def write_index_html(out_path, pol_summaries, basin_buckets, basin_net,
                     basin_polygon_summed_need, basin_loss_rate,
                     basin_portfolio_margin, basin_annual,
                     polygon_map_svg, bar_svg, ts_svg, context_svg, sy_lookup,
                     trough_cum, trough_year, portfolio, project_total_afy,
                     n_by_type,
                     basin_normalized_cum_2025,
                     basin_normalized_avg_rate,
                     basin_normalized_summed_need,
                     basin_normalized_margin,
                     n_by_type_full):
    worst_year_deficit_int = int(round(abs(trough_cum)))
    abs_2022_cushion_int = int(round(abs(trough_cum) - abs(basin_net)))
    sorted_pols = sorted(pol_summaries,
                         key=lambda s: -s["hold_steady_need_AF_per_yr"])
    deficit_pols = [s for s in sorted_pols if s["hold_steady_need_AF_per_yr"] > 0]
    surplus_pols = [s for s in sorted_pols if s["hold_steady_need_AF_per_yr"] == 0]

    short_pols = [s for s in pol_summaries if s["coverage_net_AF_per_yr"] < 0]
    short_pols.sort(key=lambda s: s["coverage_net_AF_per_yr"])
    over_pols  = [s for s in pol_summaries if s["coverage_net_AF_per_yr"] > 0
                  and s["project_alloc_AF_per_yr"] > 0]
    over_pols.sort(key=lambda s: -s["coverage_net_AF_per_yr"])

    n_polygons = len(pol_summaries)

    # Per-polygon detail rows
    detail_rows = []
    for s in sorted_pols:
        late_marker = (' <span class="late" title="Baseline year > 1999">'
                       f'(record starts {s["baseline_year"]})</span>'
                       if s["baseline_year"] > START_YEAR else "")
        sy_marker = (f' <span class="fallback" title="Insufficient SVSim borehole '
                     f'coverage — using basin area-weighted mean">(mean)</span>'
                     if s.get("sy_source", "") != "SVSim" else "")
        cum = s["endpoint_cum_storage_AF"]
        avg = s["avg_rate_AF_per_yr"]
        norm_cum = s.get("normalized_cum_2025_AF", 0)
        norm_avg = s.get("normalized_avg_rate_AF_per_yr", 0)
        hold = s["hold_steady_need_AF_per_yr"]
        proj = s["project_alloc_AF_per_yr"]
        net = s["coverage_net_AF_per_yr"]
        net_str = (f'<span class="gain">+{int(net):,}</span>' if net > 0
                   else (f'<span class="loss">{int(net):,}</span>' if net < 0 else "0"))
        proj_str = f"{int(proj):,}" if proj > 0 else "—"
        crit_dry_af = s["bucket_storage_AF"]["critical"] + s["bucket_storage_AF"]["dry"]
        # Fallback indicator if any year-type was unobserved
        fallback_types = [k for k, src in (s.get("rate_per_bucket_source") or {}).items()
                          if "fallback" in src]
        fallback_marker = (f' <span class="fallback" title="Year-type(s) not observed; '
                          f'using polygon overall avg as fallback: {", ".join(fallback_types)}">'
                          f'(fb)</span>' if fallback_types else "")
        detail_rows.append(f"""<tr>
      <td><strong>{s["zone_label"]}</strong> <span style="color:#8a8a8a;font-size:11px;">{s["ma"]}</span>{late_marker}</td>
      <td class="num">{s["span_years"]} yr ({s["baseline_year"]}–{s["endpoint_year"]})</td>
      <td class="num">{s["sy"]:.4f}{sy_marker}</td>
      <td class="num">{loss_or_gain_span(cum, 0)}</td>
      <td class="num">{loss_or_gain_span(avg, 0)}</td>
      <td class="num">{loss_or_gain_span(norm_cum, 0)}{fallback_marker}</td>
      <td class="num">{loss_or_gain_span(norm_avg, 0)}</td>
      <td class="num">{loss_or_gain_span(crit_dry_af, 0)}</td>
      <td class="num">{s["crit_dry_share_of_drawdown_pct"]:.0f}%</td>
      <td class="num">{int(hold):,}</td>
      <td class="num">{proj_str}</td>
      <td class="num">{net_str}</td>
    </tr>""")

    # Project allocation table — read from portfolio JSON
    project_rows = []
    for proj in portfolio.get("projects", []):
        zone = proj["polygon"]
        afy = proj["af_per_yr"]
        name = proj["name"]
        s = next((p for p in pol_summaries if p["zone_label"] == zone), None)
        if s is None:
            continue
        loss = s["hold_steady_need_AF_per_yr"]
        net = s["coverage_net_AF_per_yr"]
        net_str = (f'<span class="gain">+{int(net):,}</span>' if net > 0
                   else (f'<span class="loss">{int(net):,}</span>' if net < 0 else "0"))
        project_rows.append(f"""<tr>
      <td><strong>{zone}</strong> <span style="color:#8a8a8a;font-size:11px;">{s['ma']}</span></td>
      <td>{name}</td>
      <td class="num">{int(afy):,}</td>
      <td class="num">{int(loss):,}</td>
      <td class="num">{net_str}</td>
    </tr>""")

    # Shortfall table
    short_rows = []
    for s in short_pols:
        short_rows.append(f"""<tr>
      <td><strong>{s["zone_label"]}</strong> <span style="color:#8a8a8a;font-size:11px;">{s['ma']}</span></td>
      <td class="num">{int(s["hold_steady_need_AF_per_yr"]):,}</td>
      <td class="num">{int(s["project_alloc_AF_per_yr"]):,}</td>
      <td class="num"><span class="loss">{int(s["coverage_net_AF_per_yr"]):,}</span></td>
    </tr>""")
    short_total = sum(s["coverage_net_AF_per_yr"] for s in short_pols)

    # Annual basin time series rows
    basin_running = 0.0
    annual_rows = []
    SVI_BADGE_STYLE = {
        "Wet":           "background:#e6f0e8;color:#2e6f3f;",
        "Above Normal":  "background:#eef5ee;color:#3a8050;",
        "Below Normal":  "background:#f7e8d2;color:#8a5a18;",
        "Dry":           "background:#fadcc9;color:#9c4521;",
        "Critical":      "background:#fbe6e6;color:#a32d2d;",
    }
    for y_str, delta in basin_annual.items():
        y = int(y_str)
        full = year_type_full(y)
        style = SVI_BADGE_STYLE.get(full, "background:#eee;color:#333;")
        basin_running += delta
        annual_rows.append(
            f'<tr><td class="num">{y}</td>'
            f'<td><span style="{style}padding:1px 6px;border-radius:3px;font-size:11px;font-weight:600;">{full}</span></td>'
            f'<td class="num">{loss_or_gain_span(delta, 0)}</td>'
            f'<td class="num">{loss_or_gain_span(basin_running, 0)}</td></tr>'
        )

    # Hero stats by SVI type
    n_critical = n_by_type["critical"]
    n_dry      = n_by_type["dry"]
    n_bn       = n_by_type["bn"]
    n_an       = n_by_type["an"]
    n_wet      = n_by_type["wet"]
    crit_per_yr = abs(basin_buckets["critical"] / n_critical) if n_critical else 0
    dry_per_yr  = abs(basin_buckets["dry"] / n_dry) if n_dry else 0
    crit_dry_total = basin_buckets["critical"] + basin_buckets["dry"]
    wet_an_total   = basin_buckets["wet"] + basin_buckets["an"]

    late_polys = [s for s in pol_summaries if s["baseline_year"] > START_YEAR]
    late_summary = "; ".join(f"{s['zone_label']} ({s['baseline_year']})" for s in late_polys)

    fallback_polys = [s for s in pol_summaries if s.get("sy_source", "") != "SVSim"]
    fallback_summary = (", ".join(s["zone_label"] for s in fallback_polys)
                        if fallback_polys else "none")

    # Counts by management area
    n_north = sum(1 for s in pol_summaries if s["ma"] == "North")
    n_chico = sum(1 for s in pol_summaries if s["ma"] == "Chico")
    n_south = sum(1 for s in pol_summaries if s["ma"] == "South")

    sy_min = min(sy_lookup.values())
    sy_max = max(sy_lookup.values())

    # Category breakdown for the portfolio summary line.
    from collections import defaultdict as _dd
    cat_totals = _dd(int)
    cat_names = {
        "conjunctive-use": "conjunctive use (surface water replaces groundwater)",
        "recharge": "recharge",
    }
    for proj in portfolio.get("projects", []):
        cat_totals[proj.get("category", "other")] += int(proj.get("af_per_yr", 0))
    # If recharge spans multiple creeks, separate them out
    recharge_by_name = _dd(int)
    for proj in portfolio.get("projects", []):
        if proj.get("category") == "recharge":
            recharge_by_name[proj.get("name", "Recharge project")] += int(proj.get("af_per_yr", 0))
    portfolio_breakdown_parts = []
    if cat_totals.get("conjunctive-use"):
        portfolio_breakdown_parts.append(
            f"{cat_totals['conjunctive-use']:,} AF/yr conjunctive use (surface water replaces groundwater)")
    for name, afy in recharge_by_name.items():
        portfolio_breakdown_parts.append(f"{afy:,} AF/yr {name}")
    portfolio_breakdown = " + ".join(portfolio_breakdown_parts) if portfolio_breakdown_parts else f"{project_total_afy:,} AF/yr"

    # SVI year listings
    svi_years_listing = []
    for label in ["Wet", "Above Normal", "Below Normal", "Dry", "Critical"]:
        yrs = [str(y) for y, t in SVI_YEAR_TYPE.items() if t == label]
        svi_years_listing.append(
            f'<li><strong>{label}:</strong> {", ".join(yrs)} ({len(yrs)} years)</li>')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Vina Subbasin: Where the Losses Happen — 2027 BC RMS Network (28 polygons)</title>
<style>{INDEX_CSS}</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Spectral:wght@400;500;700&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
</head>
<body>
<div class="container">

<h1>Where the Losses Happen — A Drought-Conditioned Look at the 2027 BC RMS Network</h1>
<p class="subtitle">May 2026 · Prepared by AGUBC · {n_polygons} Voronoi polygons ({n_north} North · {n_chico} Chico · {n_south} South) · {n_polygons} 2027 GWL RMS wells · polygon-by-polygon Sy from DWR SVSim Texture Data · WY 1999–2025 · ΔGWE × Sy<sub>p</sub> × Area<sub>p</sub>, sliced by hydrologic condition and read against a project-portfolio sustainability target.</p>

<p class="lead">Two questions: <strong>when and where is the basin losing water, and what would it take to be sustainable by 2042?</strong> Across WY 1999–2025, loss isn't a steady year-over-year decline — it's sharply concentrated in <strong>Critical and Dry</strong> water-year types, with <strong>Wet and Above-Normal</strong> years doing the recovery work. The basin's net deficit is <strong>{abs(basin_net)/1000:.0f}k AF — about {abs(basin_net)/TOTAL_FRESH_STORAGE_AF*100:.2f}% of the {int(TOTAL_FRESH_STORAGE_AF/1_000_000)}+ MAF in basin storage</strong>. <strong>Assuming the next 17 years see a roughly similar mix of year types as WY 1999–2025</strong>, holding current conditions through 2042 takes a basin-wide <strong>{basin_loss_rate:,.0f} AF/yr</strong> of new recharge or demand reduction; a project portfolio totaling <strong>{project_total_afy:,} AF/yr</strong> (online by ~{PROJECTS_ONLINE_YEAR}) would cover that with room to spare.</p>

<div class="callout"><strong>What's new vs. the 17-polygon version.</strong> This dashboard uses the 28-polygon Voronoi tessellation from the <em>2027-BC-prop-network</em> framework — every 2027 GWL RMS well gets its own cell (the old build dissolved the three Chico cells and merged some southern wells). New polygon Sy values are recomputed from DWR SVSim Texture Data against the new geometry. The basin deficit comes out smaller here ({basin_net:+,.0f} AF vs. −193,010 AF in the 17-polygon build) because (a) the new <code>21N02E18C003M</code> polygon is larger and posts a recovery surplus, (b) the new Chico cells are smaller and capture less area-weighted drawdown, and (c) the new set adds late-baseline polygons that contribute less to early-record buckets.</div>

<div class="headline">
  <div class="stat warn">
    <div class="num warn">{crit_dry_total:+,.0f}</div>
    <div class="lab">AF lost in Critical + Dry years</div>
    <div class="det">{n_critical} Critical + {n_dry} Dry years ({(n_critical+n_dry)*100/(n_wet+n_an+n_bn+n_dry+n_critical):.0f}% of the record). Critical years alone removed {basin_buckets["critical"]:+,.0f} AF.</div>
  </div>
  <div class="stat tan">
    <div class="num tan">{basin_buckets["bn"]:+,.0f}</div>
    <div class="lab">AF in Below-Normal years</div>
    <div class="det">{n_bn} Below-Normal years. Mixed contribution — typically small net loss.</div>
  </div>
  <div class="stat acc">
    <div class="num acc">{wet_an_total:+,.0f}</div>
    <div class="lab">AF gained in Wet + Above-Normal years</div>
    <div class="det">{n_wet} Wet + {n_an} Above-Normal years. The basin is already recharging — just not fast enough to keep up with Critical years on its own.</div>
  </div>
</div>

<div class="callout"><strong>The picture in one sentence.</strong> Across 1999–2025, Critical and Dry years removed about <strong>{abs(crit_dry_total):,.0f} AF</strong>, Below-Normal years moved storage by <strong>{basin_buckets["bn"]:+,.0f} AF</strong>, and Wet + Above-Normal years recovered <strong>{wet_an_total:+,.0f} AF</strong>. Net basin deficit through 2025: <strong>{basin_net:+,.0f} AF</strong>, summed across all {n_polygons} polygons.</div>

<h2>Method, in brief</h2>
<p>Per polygon: ΔStorage<sub>p,y</sub> = (GWE<sub>p,y</sub> − GWE<sub>p,baseline</sub>) × Sy<sub>p</sub> × Area<sub>p</sub>. GWE<sub>p,y</sub> is the polygon's 2027 GWL RMS well's spring composite (March mean for SWN-named wells; Feb–Apr mean for CWSCH wells), Good-quality DWR records only. In the 28-polygon network there is exactly one RMS well per polygon — the well that seeded the polygon's Voronoi cell. Each polygon is anchored to WY 1999 if it has a Good spring composite that year; otherwise to the polygon's first observation after 1999. We then take the per-polygon cumulative storage time series, compute year-over-year deltas (distributing multi-year DWR gaps evenly), and bucket each year by its <strong>official Sacramento Valley Index water-year type</strong>.</p>

<p><strong>Specific yield is polygon-by-polygon</strong>, derived from DWR's SVSim Texture Data (Sacramento Valley Simulation Model v1.0, CKAN resource <code>544623e2-0cd5-4c5b-827f-affa4abf4e16</code>): coarse-grained sediments → Sy = 0.15, fine-grained → Sy = 0.05, Sy<sub>p</sub> = (% coarse × 0.15) + (% fine × 0.05) over the 0–500 ft below ground surface analysis window across the polygon's boreholes (≥200 ft of valid lithology required per borehole). Polygon Sy values for the 28-polygon network range <strong>{sy_min:.4f}</strong> to <strong>{sy_max:.4f}</strong>; basin area-weighted mean is roughly 0.087.</p>

<p style="font-size:13px;color:var(--ink-muted);">Three polygons ({fallback_summary}) have insufficient SVSim borehole coverage (≤2 boreholes, none meeting the 200-ft valid-thickness threshold) and use the basin area-weighted mean as a Sy fallback. These are flagged in the table below with "(mean)". This is mostly a function of the new polygons being smaller and more numerous than the 17-polygon set, leaving some cells with thin SVSim coverage.</p>

<p>Year-type classification uses DWR's Sacramento Valley Index (Northern Sierra 8-Station Index) — the same five-tier system DWR publishes annually:</p>
<ul>
{chr(10).join(svi_years_listing)}
</ul>
<p style="font-size:13px;color:var(--ink-muted);">WY 2025 is preliminary (DWR upgraded to Wet in April 2025; final May-1 designation to verify). The 1991–2020 long-term 8SI average is 53.2 inches; SVI thresholds: Wet ≥ 9.2 MAF; Above Normal &gt; 7.8 ≤ 9.2; Below Normal &gt; 6.5 ≤ 7.8; Dry &gt; 5.4 ≤ 6.5; Critical ≤ 5.4.</p>

<p><strong>Baseline asymmetry.</strong> Polygons anchored to WY 1999: those whose 2027 GWL RMS well had a Good March measurement that year. The rest baseline later: {late_summary}. Each polygon contributes year-over-year deltas only for years it has a baseline-anchored record, so early-record buckets reflect fewer polygons than late-record buckets. Polygons with shorter records cannot register pre-baseline drawdown.</p>

<h2>When and where the basin loses water</h2>

<div class="figure">{bar_svg}</div>
<div class="figcaption">Figure 1. Sum across all {n_polygons} polygons in the 2027 BC RMS network, gap-attributed by year, bucketed by official Sacramento Valley Index water-year type. Critical years alone average {crit_per_yr:,.0f} AF/yr of loss — about {(crit_per_yr/dry_per_yr if dry_per_yr else 0):.1f}× the per-year loss rate of Dry years.</div>

<div class="figure">{ts_svg}</div>
<div class="figcaption">Figure 2. Basin cumulative ΔStorage. <strong>Solid blue line = observed</strong> (each polygon contributes only the years its RMS well actually measured). <strong>Dashed purple line = year-type-weighted normalized</strong> (corrects for late-baseline drag — see methodology section below). Red-tinted vertical bands = Critical years; orange = Dry; light tan = Below Normal. Wet and Above-Normal years remain untinted. Almost every steep drop falls inside a tinted band; almost every recovery falls outside one.</div>

<div class="callout warn"><strong>Late-baseline drag and the year-type-weighted normalization.</strong> Of the 28 polygons, only 11 have a Good March measurement in WY 1999. The other 17 baseline later — between 2000 and 2019 — because their RMS well wasn't measured in 1999. Each polygon contributes year-over-year deltas only for the years it has a baseline-anchored record, which means the early-record buckets reflect fewer polygons than the late-record buckets. Late-baseline polygons cannot register their pre-baseline drawdown, so the <strong>observed</strong> basin cumulative ({basin_net:+,.0f} AF through 2025) <em>understates</em> what the basin would show if every polygon had a full record.<br><br>The <strong>year-type-weighted normalized</strong> series corrects this. For each polygon, we compute its average ΔStorage <em>per Sacramento Valley Index year type</em> (Wet, Above Normal, Below Normal, Dry, Critical) using <em>only its own observations</em>. We then synthesize what that polygon would have contributed across the full WY 1999–2025 record by applying its per-type rates to the basin's actual year-type mix ({n_by_type_full["wet"]} Wet, {n_by_type_full["an"]} AN, {n_by_type_full["bn"]} BN, {n_by_type_full["dry"]} Dry, {n_by_type_full["critical"]} Critical = 26 transition years). Summed across all 28 polygons, that gives the normalized basin total: <strong>{basin_normalized_cum_2025:+,.0f} AF</strong> through 2025 — an avg loss rate of <strong>{-basin_normalized_avg_rate:,.0f} AF/yr</strong>, vs. the observed {basin_loss_rate:,.0f} AF/yr. The late-baseline drag in the observed series is therefore worth ≈{abs(basin_normalized_cum_2025 - basin_net):,.0f} AF cumulative ({abs(basin_normalized_avg_rate + basin_loss_rate * -1 if basin_loss_rate else 0):,.0f} AF/yr rate equivalent — note: this is the bound from the polygon's own data and is independent of any neighboring-well proxying).</div>

<h3>Putting the deficit in proportion</h3>
<p>The cumulative deficit looks alarming on a chart that runs from 0 to almost −300k AF, but it is a small fraction of the fresh groundwater that exists in the subbasin. Panel 1 below shows the deficit at full scale (the small red sliver). Panel 2 zooms in so the deficit is actually visible.</p>
<div class="figure">{context_svg}</div>
<div class="figcaption">Figure 3. Source: total storage from the Vina Subbasin GSP (Dec 15, 2021), p. ES-5 (BBGM-2020 estimate). Cumulative ΔStorage from this dashboard. WY {trough_year} trough = deepest observed deficit in the 28-polygon analysis.</div>

<div class="callout good"><strong>Why this matters for project design.</strong> Losses are concentrated in Critical and Dry years; recovery happens in Wet and Above-Normal years. But the project portfolio doesn't have to follow that pattern year by year — it's <em>permanent infrastructure</em> (recharge facilities, surface-water deliveries) that produces yield year after year. Annual yields will vary with hydrology, but the long-run average matters more than year-by-year matching: with portfolio yield at ≈{project_total_afy:,} AF/yr against a basin loss rate of ≈{basin_loss_rate:,.0f} AF/yr, surplus from Wet and Above-Normal years carries through Critical ones. The goal isn't to offset every drought-year loss in the year it happens; it's to install enough permanent supply that the multi-year trend bends back toward equilibrium.</div>

<h2>The 2042 sustainability target — hold current conditions, with the project portfolio</h2>

<p>The Vina Subbasin has lost storage across the WY 1999–2025 record through {n_critical} Critical years, {n_dry} Dry years, {n_bn} Below-Normal years, and a long-term decline rate of about 0.07%/yr. The basin's historic low was the <strong>WY {trough_year} trough</strong> at roughly {worst_year_deficit_int:,} AF below baseline — and even at that low, <strong>no SGMA sustainability indicator registered an undesirable result</strong>.</p>

<p>The framing here is therefore not "recover to the WY 1999 baseline." The operational target is: <strong>GWE at each Groundwater Level RMS well stays at or above its WY {trough_year} level going forward</strong>. MTs for the GSP would be set <em>lower</em> than WY {trough_year}, creating operational range and margin for an unforeseen 7–10 year drought, similar to what the subbasin experienced between 1985 and 1994. The portfolio's job is to ensure the next major drought doesn't push observed GWE below WY {trough_year}, with projects coming online in roughly 3–5 years (by ~{PROJECTS_ONLINE_YEAR} at the latest).</p>

<p>The sizing test below uses the basin's <strong>average annual loss rate</strong> as the volumetric need — a stronger target than "stay above WY {trough_year}" alone, because matching average loss keeps the basin near today's WY 2025 level (which sits ≈{abs_2022_cushion_int:,} AF above the WY {trough_year} trough) and provides built-in cushion against drought. Per polygon, the volume needed to hold steady is just the polygon's average annual loss rate. Surplus polygons need zero. Sum across the {n_polygons} polygons:</p>

<div class="bigstat">
  <div class="row">
    <div>
      <div class="num">{basin_loss_rate:,.0f} <span style="font-size:18px;color:var(--ink-muted);">AF/yr</span></div>
      <div class="lab">Basin avg loss rate — observed</div>
      <div style="font-size:12px;color:var(--ink-muted);margin-top:2px;">Normalized: <strong>{-basin_normalized_avg_rate:,.0f}</strong> AF/yr</div>
    </div>
    <div>
      <div class="num" style="color:var(--accent);">{project_total_afy:,} <span style="font-size:18px;color:var(--ink-muted);">AF/yr</span></div>
      <div class="lab">Project portfolio (online by {PROJECTS_ONLINE_YEAR})</div>
    </div>
    <div>
      <div class="num">+{basin_portfolio_margin:,.0f} <span style="font-size:18px;color:var(--ink-muted);">AF/yr</span></div>
      <div class="lab">Recovery margin (portfolio − observed loss)</div>
      <div style="font-size:12px;color:var(--ink-muted);margin-top:2px;">Against normalized loss: <strong>+{basin_normalized_margin:,.0f}</strong> AF/yr</div>
    </div>
    <div class="desc">Portfolio = {portfolio_breakdown}. The portfolio's recovery margin remains comfortably positive against either the observed or the normalized loss rate, with a cushion of <strong>+{basin_normalized_margin:,.0f} AF/yr against the normalized rate</strong> ({basin_normalized_margin / SUSTAINABLE_YIELD_AFY * 100:+.1f}% of the {SUSTAINABLE_YIELD_AFY:,} AF/yr GSP-stated sustainable yield) starting ~{PROJECTS_ONLINE_YEAR}.</div>
  </div>
</div>

<h2>Where the projects land — coverage by polygon</h2>

<p>Project allocations under the {project_total_afy:,} AF/yr portfolio:</p>

<table>
  <thead>
    <tr>
      <th>Polygon</th>
      <th>Project</th>
      <th class="num">Allocation (AF/yr)</th>
      <th class="num">Polygon avg loss (AF/yr)</th>
      <th class="num">Net coverage</th>
    </tr>
  </thead>
  <tbody>
{chr(10).join(project_rows)}
  </tbody>
  <tfoot>
    <tr>
      <th>Total portfolio</th>
      <th>—</th>
      <th class="num"><strong>{project_total_afy:,}</strong></th>
      <th class="num">{basin_loss_rate:,.0f}</th>
      <th class="num"><strong><span class="gain">+{basin_portfolio_margin:,.0f}</span></strong></th>
    </tr>
  </tfoot>
</table>

<p>The polygon map below is colored by <strong>net coverage after the project portfolio comes online</strong>: greens are at-or-above their hold-steady need, oranges and reds remain short. {len(short_pols)} polygons remain partially uncovered (combined shortfall {abs(short_total):,.0f} AF/yr) — most prominently <strong>{short_pols[0]['zone_label'] if short_pols else ''}</strong>{f' at {abs(short_pols[0]["coverage_net_AF_per_yr"]):,.0f} AF/yr below its loss rate' if short_pols else ''}. At basin scale the portfolio's surplus capacity in over-allocated polygons (combined +{sum(s["coverage_net_AF_per_yr"] for s in over_pols):,.0f} AF/yr) more than covers the residual shortfalls; whether that holds at each RMS well depends on lateral connectivity, which is outside this analysis.</p>

<div class="map-wrap">
<div class="figure">{polygon_map_svg}</div>
<div id="polygon-popup">
  <button class="popup-close" type="button">×</button>
  <h4 id="pp-name">—</h4>
  <div id="pp-body"></div>
</div>
</div>
<div class="figcaption">Figure 4. Click any polygon for full detail. Color = project allocation minus polygon avg loss rate (AF/yr). Greens = covered or surplus; oranges/reds = polygon-level shortfall after the project portfolio. Larger dots mark polygons hosting a project.</div>

{('<h3>Residual shortfall polygons</h3><table><thead><tr><th>Polygon</th><th class="num">Avg loss (AF/yr)</th><th class="num">Project alloc (AF/yr)</th><th class="num">Shortfall (AF/yr)</th></tr></thead><tbody>' + chr(10).join(short_rows) + '</tbody></table>') if short_rows else ''}

<h2>Per-polygon detail (technical)</h2>

<p>Polygons sorted by hold-steady need (avg annual loss rate), descending. Late-baseline polygons (record starts after 1999) are flagged. "Crit+Dry share" is the share of each polygon's <em>gross drawdown</em> (sum of losing years) that occurred in Critical and Dry water-year types. Sy values marked "(mean)" use the basin area-weighted mean as a fallback for polygons with insufficient SVSim borehole coverage.</p>

<table>
  <thead>
    <tr>
      <th>Polygon</th>
      <th class="num">Span</th>
      <th class="num">Sy</th>
      <th class="num">Cum 2025 obs (AF)</th>
      <th class="num">Avg rate obs (AF/yr)</th>
      <th class="num">Cum 2025 norm (AF)</th>
      <th class="num">Avg rate norm (AF/yr)</th>
      <th class="num">Crit+Dry (AF)</th>
      <th class="num">Crit+Dry share</th>
      <th class="num">Hold need (AF/yr)</th>
      <th class="num">Project (AF/yr)</th>
      <th class="num">Net coverage</th>
    </tr>
  </thead>
  <tbody>
{chr(10).join(detail_rows)}
  </tbody>
  <tfoot>
    <tr>
      <th>Basin (sum)</th>
      <th class="num">—</th>
      <th class="num">—</th>
      <th class="num"><strong>{basin_net:+,.0f}</strong></th>
      <th class="num">{-basin_loss_rate:+,.0f}</th>
      <th class="num"><strong>{basin_normalized_cum_2025:+,.0f}</strong></th>
      <th class="num">{-basin_normalized_avg_rate:+,.0f}</th>
      <th class="num">{crit_dry_total:+,.0f}</th>
      <th class="num">—</th>
      <th class="num"><strong>{basin_polygon_summed_need:,.0f}</strong></th>
      <th class="num"><strong>{project_total_afy:,}</strong></th>
      <th class="num"><strong><span class="gain">+{basin_portfolio_margin:,.0f}</span></strong></th>
    </tr>
  </tfoot>
</table>

<details>
<summary>Annual basin time series (2000–2025), gap-attributed</summary>
<p style="font-size:13px;color:var(--ink-muted);">Sum of all {n_polygons} polygons' year-over-year storage change with polygon-by-polygon Sy. Multi-year DWR data gaps within a polygon are distributed evenly across the gap and bucketed by each year's hydrologic condition. Late-baseline polygons contribute zero to years before their baseline.</p>
<table>
  <thead>
    <tr><th class="num">Year</th><th>Condition</th><th class="num">ΔStor (AF)</th><th class="num">Cumulative (AF)</th></tr>
  </thead>
  <tbody>
{chr(10).join(annual_rows)}
  </tbody>
</table>
</details>

<h2>Caveats</h2>

<ul>
  <li><strong>Specific yield is polygon-by-polygon</strong> from SVSim Texture Data (range {sy_min:.4f}–{sy_max:.4f}); basin area-weighted mean is ≈0.087. The textural classifier (coarse vs. fine) is documented in <code>scripts/build_sy_svsim.py</code> and is reproducible from the DWR CKAN dataset. Three polygons ({fallback_summary}) lack sufficient SVSim borehole density and use the basin area-weighted mean as a fallback — a known limitation when fragmenting the basin into 28 smaller cells.</li>
  <li><strong>Baseline asymmetry.</strong> Late-baseline polygons — {late_summary} — have shorter records. <code>21N02E18C003M</code>'s large apparent surplus is partly an artifact of starting near the bottom of the 2011 drought; it cannot register pre-2011 drawdown.</li>
  <li><strong>Sustainable yield = {SUSTAINABLE_YIELD_AFY:,} AF/yr</strong> per the 2022 GSP (Dec 15, 2021), p. ES-5: 243,500 AFY historical pumping minus 10,000 AFY decrease in storage. Used here as a denominator only; volumetric needs (AF/yr) do not depend on it.</li>
  <li><strong>Total storage = {int(TOTAL_FRESH_STORAGE_AF/1_000_000)}+ MAF</strong> per the GSP, BBGM-2020 estimate. Used in the proportion visual; not a calibration input.</li>
  <li><strong>Sustainability target.</strong> "Sustainability" here means GWE at each Groundwater Level RMS well stays at or above its <strong>WY {trough_year}</strong> level going forward — the basin's historic low, at which no sustainability indicator registered an undesirable result. MTs for the GSP would be set <em>lower</em> than WY {trough_year} to create operational range and margin in the event of an unforeseen 7–10 year drought, similar to what the subbasin experienced between 1985 and 1994. The volumetric sizing in this dashboard uses the basin's average annual loss rate as the need, which is a stronger target than "stay above WY {trough_year}" alone — matching average loss keeps the basin near WY 2025 conditions, providing built-in drought cushion.</li>
  <li><strong>Project portfolio is at-yield, not at-design.</strong> Conjunctive-use figures assume successful surface-water substitution. <strong>Recharge figures assume 2–3 storm events per year</strong> where excess flow can be diverted into recharge basins; drought-year recharge rates will be lower, wet-year rates higher.</li>
  <li><strong>Per-polygon vs. basin-wide.</strong> The portfolio covers basin loss with margin, but {len(short_pols)} polygons remain locally short. The two Chico cells (<code>22N01E09B001M</code> and <code>22N01E20K001M</code>) together are the largest residual shortfall — Chico may be able to add recharge capacity by directing more flow into Lindo Channel, but evaluating that potential is outside this scope. Whether one polygon's neighbors' surplus reaches its RMS well depends on lateral hydraulic conductivity that this dashboard does not model.</li>
  <li><strong>Hold-current target assumes a representative year-type mix going forward.</strong> The {basin_loss_rate:,.0f} AF/yr basin avg loss rate is the average over WY 1999–2025, which had {n_wet} Wet, {n_an} Above Normal, {n_bn} Below Normal, {n_dry} Dry, and {n_critical} Critical years. If WY 2026–2042 sees materially more Critical years, the realized loss rate will be higher; if more Wet years, lower. The portfolio's recovery margin (≈{basin_portfolio_margin:,.0f} AF/yr) is the buffer for that uncertainty.</li>
  <li><strong>Year-type definitions are the official Sacramento Valley Index types,</strong> published annually by DWR from the Northern Sierra 8-Station Index.</li>
  <li><strong>Comparison to the 17-polygon version.</strong> The basin deficit through WY 2025 is smaller here ({basin_net:+,.0f} AF vs. −193,010 AF in the 17-polygon build), and the avg loss rate is smaller too ({basin_loss_rate:,.0f} AF/yr vs. 8,558). The difference traces to (a) the new <code>21N02E18C003M</code> polygon being larger and posting a recovering surplus, (b) the new Chico cells being smaller than the old dissolved Chico polygon, (c) the addition of late-baseline polygons that contribute less to early-record buckets, and (d) different per-polygon Sy values from the SVSim recompute against the new geometry.</li>
</ul>

<div class="footer">
<p><strong>Files in this folder.</strong> <code>index.html</code> (this page) · <code>data/condition_analysis.json</code> (per-polygon bucket totals) · <code>data/basin_annual.json</code> (basin annual ΔStor) · <code>data/sustainability_2042.json</code> (per-polygon and basin 2042 targets) · <code>data/model_data.json</code>, <code>data/polygon_storage_2025.csv</code>, <code>data/storage_timeseries.csv</code> (model data) · <code>data/polygon_map.svg</code>, <code>data/basin_buckets_chart.svg</code>, <code>data/basin_cumulative_chart.svg</code>, <code>data/storage_context.svg</code> (figures) · <code>data/polygon_sy_svsim.csv</code> (per-polygon Sy) · <code>data/project_portfolio.json</code> (project allocations).</p>
<p><strong>Upstream.</strong> Polygons, wells, and DWR periodic GWL measurements come from the companion <a href="https://cosmo1007.github.io/2027-BC-prop-network/">2027-BC-prop-network</a> framework (28 Voronoi polygons, 79 wells including 28 GWL RMS, measurements fetched fresh from DWR CKAN).</p>
<p><strong>Status.</strong> Independent analysis prepared for AGUBC technical staff and Board. Comments and corrections welcomed; this work is expected to evolve as feedback comes in.</p>
</div>

</div>

<script>{POPUP_JS}</script>

</body>
</html>
"""
    out_path.write_text(html)
