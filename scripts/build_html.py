#!/usr/bin/env python3
"""
Single-file index.html generator for the 28-polygon 2027 BC drought-storage
dashboard.  Builds two method-specific content sections (single basin-wide
tessellation + three-zone per-management-area tessellation) and wires up a
toggle UI at the top to switch between them.

Called by scripts/build_dashboard.py with a `results_by_method` dict
keyed by 'single' and 'three-zone'.
"""

from __future__ import annotations
from collections import defaultdict as _dd

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

METHOD_LABEL = {
    "single":     "Single basin-wide tessellation",
    "three-zone": "Three-zone (per management area)",
}
METHOD_SHORT = {"single": "Single", "three-zone": "Three-zone"}


def year_type_full(y: int) -> str:
    return SVI_YEAR_TYPE.get(y, "Wet")


def loss_or_gain_span(v, decimals=0):
    cls = "gain" if v > 0 else "loss" if v < 0 else ""
    fmt = f"{{:+,.{decimals}f}}".format(v) if v != 0 else f"{{:,.{decimals}f}}".format(v)
    return f'<span class="{cls}">{fmt}</span>' if cls else fmt


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
.subtitle { color: var(--ink-muted); font-size: 14px; font-family: 'Inter', sans-serif; margin: 0 0 18px 0; }
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
.reassigned-tag { color: #7c4a86; font-style: italic; font-size: 11px; }
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

/* Method toggle */
.method-toggle {
  display: inline-flex;
  gap: 0;
  margin: 18px 0 32px 0;
  border: 1px solid var(--rule);
  border-radius: 6px;
  background: var(--bg-card);
  padding: 4px;
  font-family: 'Inter', sans-serif;
  flex-wrap: wrap;
}
.method-toggle button {
  background: transparent;
  border: none;
  padding: 8px 16px;
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: var(--ink-muted);
  cursor: pointer;
  border-radius: 4px;
  transition: background 0.12s, color 0.12s;
}
.method-toggle button:hover { background: #f1ede2; color: var(--ink); }
.method-toggle button.active {
  background: var(--accent);
  color: white;
}
.method-toggle-label {
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--ink-muted);
  font-weight: 600;
  margin-right: 12px;
  align-self: center;
}
.method-content { display: block; }
.method-content.hidden { display: none; }
.method-banner {
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  color: var(--ink-muted);
  padding: 6px 0 0 2px;
  margin-bottom: 6px;
}
.method-banner strong { color: var(--ink); }
"""

POPUP_JS = """
(function() {
  const popup = document.getElementById('polygon-popup');
  const ppName = document.getElementById('pp-name');
  const ppBody = document.getElementById('pp-body');
  const closeBtn = popup.querySelector('.popup-close');

  function fmtClass(s) {
    if (!s) return '';
    if (s.startsWith('+')) return 'gain';
    if (s.startsWith('-')) return 'loss';
    return '';
  }

  function showPopup(path, evt) {
    const d = path.dataset;
    const wrap = path.closest('.map-wrap');
    ppName.textContent = d.short + ' (' + d.ma + ')';
    let html = '';
    if (d.reassigned === '1') {
      html += `<div class="popup-row"><span class="k">Zone (spatial)</span><span class="v" style="color:#7c4a86;">${d.ma} — reassigned from ${d.workbookMa}</span></div>`;
    }
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

    // Position popup relative to the visible map-wrap that owns this path
    const rect = wrap.getBoundingClientRect();
    let x = evt.clientX - rect.left + 12;
    let y = evt.clientY - rect.top + 12;
    // Move popup into this wrap (so absolute positioning is relative to it)
    if (popup.parentElement !== wrap) wrap.appendChild(popup);
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

TOGGLE_JS = """
(function() {
  const popup = document.getElementById('polygon-popup');
  document.querySelectorAll('.method-toggle button').forEach(btn => {
    btn.addEventListener('click', () => {
      const m = btn.dataset.method;
      document.querySelectorAll('.method-toggle button').forEach(b =>
        b.classList.toggle('active', b === btn));
      document.querySelectorAll('.method-content').forEach(c =>
        c.classList.toggle('hidden', !c.classList.contains('method-' + m)));
      if (popup) popup.style.display = 'none';
      // Scroll to top of method content
      const visible = document.querySelector('.method-content:not(.hidden)');
      if (visible) visible.scrollIntoView({behavior: 'smooth', block: 'start'});
    });
  });
})();
"""


def _render_method_section(method, results, portfolio):
    """Build the per-method HTML content block.  Returns an HTML string
    (no <html>/<body> wrappers — to be inserted inside method-content div)."""
    pol_summaries = results["pol_summaries"]
    basin_buckets = results["basin_buckets"]
    basin_net = results["basin_cumulative_2025"]
    basin_polygon_summed_need = results["basin_polygon_summed_need"]
    basin_loss_rate = results["basin_loss_rate"]
    basin_portfolio_margin = results["basin_portfolio_margin"]
    basin_annual = results["basin_annual"]
    polygon_map_svg = results["polygon_map_svg"]
    bar_svg = results["bar_svg"]
    ts_svg = results["ts_svg"]
    context_svg = results["context_svg"]
    sy_lookup = results["sy_lookup"]
    trough_cum = results["trough_cum"]
    trough_year = results["trough_year"]
    n_by_type = results["n_by_type"]
    basin_normalized_cum_2025 = results["basin_normalized_cumulative_2025"]
    basin_normalized_avg_rate = results["basin_normalized_avg_rate"]
    basin_normalized_summed_need = results["basin_normalized_polygon_summed_need"]
    basin_normalized_margin = results["basin_normalized_portfolio_margin"]
    n_by_type_full = results["n_by_type_full"]
    project_total_afy = results["project_total_afy"]

    worst_year_deficit_int = int(round(abs(trough_cum)))
    abs_2022_cushion_int = int(round(abs(trough_cum) - abs(basin_net)))
    sorted_pols = sorted(pol_summaries,
                         key=lambda s: -s["hold_steady_need_AF_per_yr"])
    short_pols = [s for s in pol_summaries if s["coverage_net_AF_per_yr"] < 0]
    short_pols.sort(key=lambda s: s["coverage_net_AF_per_yr"])
    over_pols  = [s for s in pol_summaries if s["coverage_net_AF_per_yr"] > 0
                  and s["project_alloc_AF_per_yr"] > 0]
    over_pols.sort(key=lambda s: -s["coverage_net_AF_per_yr"])

    n_polygons = len(pol_summaries)

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

    short_rows = []
    for s in short_pols:
        short_rows.append(f"""<tr>
      <td><strong>{s["zone_label"]}</strong> <span style="color:#8a8a8a;font-size:11px;">{s['ma']}</span></td>
      <td class="num">{int(s["hold_steady_need_AF_per_yr"]):,}</td>
      <td class="num">{int(s["project_alloc_AF_per_yr"]):,}</td>
      <td class="num"><span class="loss">{int(s["coverage_net_AF_per_yr"]):,}</span></td>
    </tr>""")
    short_total = sum(s["coverage_net_AF_per_yr"] for s in short_pols)

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

    n_north = sum(1 for s in pol_summaries if s["ma"] == "North")
    n_chico = sum(1 for s in pol_summaries if s["ma"] == "Chico")
    n_south = sum(1 for s in pol_summaries if s["ma"] == "South")

    sy_min = min(sy_lookup.values())
    sy_max = max(sy_lookup.values())

    # Reassignment notice — only for three-zone method
    reassigned_polys = [s for s in pol_summaries
                        if any(p.get("reassigned") and p.get("zone_label") == s["zone_label"]
                                for p in results["polygons_meta"])]
    reassigned_meta = [p for p in results["polygons_meta"] if p.get("reassigned")]
    reassignment_callout = ""
    if reassigned_meta and method == "three-zone":
        items = "; ".join(
            f"<code>{p['zone_label']}</code> (workbook tag: {p.get('workbook_mgmt_area', '?')} → spatial: {p.get('mgmt_area_full')})"
            for p in reassigned_meta
        )
        reassignment_callout = (
            f'<div class="callout tan"><strong>Spatial zone reassignment.</strong> '
            f'In the three-zone method, polygons are assigned to management areas by '
            f'<em>spatial containment</em> in the management-area boundary polygons, not by '
            f'workbook tag. {len(reassigned_meta)} polygon{"s" if len(reassigned_meta) != 1 else ""} '
            f'reassigned: {items}. This is a deliberate on-the-record boundary call for SMC '
            f'defensibility (where the well physically sits matters for subsidence/SMC).</div>'
        )

    # Category breakdown
    cat_totals = _dd(int)
    recharge_by_name = _dd(int)
    for proj in portfolio.get("projects", []):
        cat_totals[proj.get("category", "other")] += int(proj.get("af_per_yr", 0))
        if proj.get("category") == "recharge":
            recharge_by_name[proj.get("name", "Recharge project")] += int(proj.get("af_per_yr", 0))
    portfolio_breakdown_parts = []
    if cat_totals.get("conjunctive-use"):
        portfolio_breakdown_parts.append(
            f"{cat_totals['conjunctive-use']:,} AF/yr conjunctive use (surface water replaces groundwater)")
    for name, afy in recharge_by_name.items():
        portfolio_breakdown_parts.append(f"{afy:,} AF/yr {name}")
    portfolio_breakdown = " + ".join(portfolio_breakdown_parts) if portfolio_breakdown_parts else f"{project_total_afy:,} AF/yr"

    svi_years_listing = []
    for label in ["Wet", "Above Normal", "Below Normal", "Dry", "Critical"]:
        yrs = [str(y) for y, t in SVI_YEAR_TYPE.items() if t == label]
        svi_years_listing.append(
            f'<li><strong>{label}:</strong> {", ".join(yrs)} ({len(yrs)} years)</li>')

    method_pretty = METHOD_LABEL[method]
    method_summary = (
        f"<strong>{method_pretty}.</strong> "
        + ("All 28 polygons built as one Voronoi tessellation clipped to the basin boundary; "
           "cells can cross management-area lines."
           if method == "single" else
           "Three independent Voronoi tessellations (one per management area), each clipped to "
           "its own boundary; cells do NOT cross management-area lines.")
        + f" {n_polygons} polygons total ({n_north} North · {n_chico} Chico · {n_south} South)."
    )

    return f"""<div class="method-banner">{method_summary}</div>

<p class="lead">Across WY 1999–2025, loss is sharply concentrated in <strong>Critical and Dry</strong> water-year types, with <strong>Wet and Above-Normal</strong> years doing the recovery work. The basin's <strong>observed</strong> net deficit is <strong>{abs(basin_net)/1000:.0f}k AF — about {abs(basin_net)/TOTAL_FRESH_STORAGE_AF*100:.2f}% of the {int(TOTAL_FRESH_STORAGE_AF/1_000_000)}+ MAF in basin storage</strong>; the <strong>year-type-normalized</strong> deficit is <strong>{abs(basin_normalized_cum_2025)/1000:.0f}k AF</strong> ({abs(basin_normalized_cum_2025)/TOTAL_FRESH_STORAGE_AF*100:.2f}%). Holding current conditions through 2042 takes a basin-wide <strong>{basin_loss_rate:,.0f} AF/yr</strong> (observed) / <strong>{-basin_normalized_avg_rate:,.0f} AF/yr</strong> (normalized) of new recharge or demand reduction; the project portfolio totaling <strong>{project_total_afy:,} AF/yr</strong> (online by ~{PROJECTS_ONLINE_YEAR}) would cover that with margin.</p>

{reassignment_callout}

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

<div class="callout"><strong>The picture in one sentence.</strong> Across 1999–2025, Critical and Dry years removed about <strong>{abs(crit_dry_total):,.0f} AF</strong>, Below-Normal years moved storage by <strong>{basin_buckets["bn"]:+,.0f} AF</strong>, and Wet + Above-Normal years recovered <strong>{wet_an_total:+,.0f} AF</strong>. Net basin deficit through 2025: <strong>{basin_net:+,.0f} AF observed / {basin_normalized_cum_2025:+,.0f} AF year-type-normalized</strong>, summed across all {n_polygons} polygons.</div>

<h2>Method, in brief</h2>
<p>Per polygon: ΔStorage<sub>p,y</sub> = (GWE<sub>p,y</sub> − GWE<sub>p,baseline</sub>) × Sy<sub>p</sub> × Area<sub>p</sub>. GWE<sub>p,y</sub> is the polygon's 2027 GWL RMS well's spring composite (March mean for SWN-named wells), Good-quality DWR records only. Each polygon is anchored to WY 1999 if it has a Good spring composite that year; otherwise to the polygon's first observation after 1999. We then take the per-polygon cumulative storage time series, compute year-over-year deltas (distributing multi-year DWR gaps evenly), and bucket each year by its <strong>official Sacramento Valley Index water-year type</strong>.</p>

<p><strong>Specific yield is polygon-by-polygon</strong>, derived from DWR's SVSim Texture Data (Sacramento Valley Simulation Model v1.0). Coarse-grained sediments → Sy = 0.15, fine-grained → Sy = 0.05, area-weighted by borehole lithology in the 0–500 ft below ground surface analysis window. Polygon Sy values range <strong>{sy_min:.4f}</strong> to <strong>{sy_max:.4f}</strong>; basin area-weighted mean ≈ 0.087.</p>

<p style="font-size:13px;color:var(--ink-muted);">{len(fallback_polys)} polygon{"s" if len(fallback_polys) != 1 else ""} ({fallback_summary}) have insufficient SVSim borehole coverage and use the basin area-weighted mean as a Sy fallback. Flagged with "(mean)" in the table.</p>

<p>Year-type classification uses DWR's Sacramento Valley Index (Northern Sierra 8-Station Index):</p>
<ul>
{chr(10).join(svi_years_listing)}
</ul>

<p><strong>Baseline asymmetry.</strong> Polygons anchored to WY 1999: those whose 2027 GWL RMS well had a Good March measurement that year ({n_polygons - len(late_polys)} of {n_polygons}). The rest baseline later: {late_summary}.</p>

<h2>When and where the basin loses water</h2>

<div class="figure">{bar_svg}</div>
<div class="figcaption">Figure 1. Sum across all {n_polygons} polygons, gap-attributed by year, bucketed by official Sacramento Valley Index water-year type. Critical years alone average {crit_per_yr:,.0f} AF/yr of loss — about {(crit_per_yr/dry_per_yr if dry_per_yr else 0):.1f}× the per-year loss rate of Dry years.</div>

<div class="figure">{ts_svg}</div>
<div class="figcaption">Figure 2. Basin cumulative ΔStorage. <strong>Solid blue line = observed</strong> (each polygon contributes only years its RMS well actually measured). <strong>Dashed purple line = year-type-weighted normalized</strong> (corrects for late-baseline drag — see callout below).</div>

<div class="callout warn"><strong>Late-baseline drag and the year-type-weighted normalization.</strong> Of the {n_polygons} polygons, only {n_polygons - len(late_polys)} have a Good March measurement in WY 1999. The other {len(late_polys)} baseline later — between 2000 and 2019 — because their 2027 GWL RMS well wasn't measured in 1999. Late-baseline polygons cannot register their pre-baseline drawdown, so the <strong>observed</strong> basin cumulative ({basin_net:+,.0f} AF through 2025) <em>understates</em> what the basin would show if every polygon had a full record.<br><br>The <strong>year-type-weighted normalized</strong> series corrects this. For each polygon, we compute its average ΔStorage <em>per Sacramento Valley Index year type</em> using <em>only its own observations</em>. We then synthesize what that polygon would have contributed across the full WY 1999–2025 record by applying its per-type rates to the basin's actual year-type mix ({n_by_type_full["wet"]} Wet, {n_by_type_full["an"]} AN, {n_by_type_full["bn"]} BN, {n_by_type_full["dry"]} Dry, {n_by_type_full["critical"]} Critical = 26 transition years). Summed across all {n_polygons} polygons, that gives the normalized basin total: <strong>{basin_normalized_cum_2025:+,.0f} AF</strong> through 2025 — an avg loss rate of <strong>{-basin_normalized_avg_rate:,.0f} AF/yr</strong>, vs. the observed {basin_loss_rate:,.0f} AF/yr.</div>

<h3>Putting the deficit in proportion</h3>
<div class="figure">{context_svg}</div>
<div class="figcaption">Figure 3. Source: total storage from the Vina Subbasin GSP (Dec 15, 2021), p. ES-5 (BBGM-2020 estimate). WY {trough_year} trough = deepest observed deficit in this {method_pretty.lower()}.</div>

<h2>The 2042 sustainability target — hold the line, with the project portfolio</h2>

<p>The Vina Subbasin has lost storage across the WY 1999–2025 record through {n_critical} Critical years, {n_dry} Dry years, {n_bn} Below-Normal years, and a long-term decline rate of about 0.07%/yr. The basin's historic low was the <strong>WY {trough_year} trough</strong> at roughly {worst_year_deficit_int:,} AF below baseline — and even at that low, <strong>no SGMA sustainability indicator registered an undesirable result</strong>.</p>

<p>The framing here is therefore not "recover to the WY 1999 baseline." The operational target is: <strong>GWE at each Groundwater Level RMS well stays at or above its WY {trough_year} level going forward</strong>. MTs for the GSP would be set <em>lower</em> than WY {trough_year}, creating operational range and margin for an unforeseen 7–10 year drought, similar to what the subbasin experienced between 1985 and 1994. The portfolio's job is to ensure the next major drought doesn't push observed GWE below WY {trough_year}.</p>

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
      <div class="lab">Recovery margin (vs. observed loss)</div>
      <div style="font-size:12px;color:var(--ink-muted);margin-top:2px;">Against normalized loss: <strong>+{basin_normalized_margin:,.0f}</strong> AF/yr</div>
    </div>
    <div class="desc">Portfolio = {portfolio_breakdown}. The recovery margin remains comfortably positive against both the observed and normalized loss rates ({basin_normalized_margin / SUSTAINABLE_YIELD_AFY * 100:+.1f}% of the {SUSTAINABLE_YIELD_AFY:,} AF/yr GSP-stated sustainable yield).</div>
  </div>
</div>

<h2>Where the projects land — coverage by polygon</h2>
<table>
  <thead>
    <tr><th>Polygon</th><th>Project</th><th class="num">Allocation (AF/yr)</th><th class="num">Polygon avg loss (AF/yr)</th><th class="num">Net coverage</th></tr>
  </thead>
  <tbody>{chr(10).join(project_rows)}</tbody>
  <tfoot>
    <tr><th>Total portfolio</th><th>—</th><th class="num"><strong>{project_total_afy:,}</strong></th><th class="num">{basin_loss_rate:,.0f}</th><th class="num"><strong><span class="gain">+{basin_portfolio_margin:,.0f}</span></strong></th></tr>
  </tfoot>
</table>

<p>The polygon map below is colored by <strong>net coverage after the project portfolio comes online</strong>. {len(short_pols)} polygons remain partially uncovered (combined shortfall {abs(short_total):,.0f} AF/yr)
{f' — most prominently <strong>{short_pols[0]["zone_label"]}</strong> at {abs(short_pols[0]["coverage_net_AF_per_yr"]):,.0f} AF/yr below its loss rate' if short_pols else ''}.</p>

<div class="map-wrap">
<div class="figure">{polygon_map_svg}</div>
</div>
<div class="figcaption">Figure 4. Click any polygon for full detail. Color = project allocation minus polygon avg loss rate (AF/yr).</div>

{('<h3>Residual shortfall polygons</h3><table><thead><tr><th>Polygon</th><th class="num">Avg loss (AF/yr)</th><th class="num">Project alloc (AF/yr)</th><th class="num">Shortfall (AF/yr)</th></tr></thead><tbody>' + chr(10).join(short_rows) + '</tbody></table>') if short_rows else ''}

<h2>Per-polygon detail (technical)</h2>
<table>
  <thead>
    <tr>
      <th>Polygon</th>
      <th class="num">Span</th>
      <th class="num">Sy</th>
      <th class="num">Cum 2025 obs (AF)</th>
      <th class="num">Avg obs (AF/yr)</th>
      <th class="num">Cum 2025 norm (AF)</th>
      <th class="num">Avg norm (AF/yr)</th>
      <th class="num">Crit+Dry (AF)</th>
      <th class="num">Crit+Dry share</th>
      <th class="num">Hold (AF/yr)</th>
      <th class="num">Project (AF/yr)</th>
      <th class="num">Net</th>
    </tr>
  </thead>
  <tbody>{chr(10).join(detail_rows)}</tbody>
  <tfoot>
    <tr>
      <th>Basin (sum)</th><th class="num">—</th><th class="num">—</th>
      <th class="num"><strong>{basin_net:+,.0f}</strong></th>
      <th class="num">{-basin_loss_rate:+,.0f}</th>
      <th class="num"><strong>{basin_normalized_cum_2025:+,.0f}</strong></th>
      <th class="num">{-basin_normalized_avg_rate:+,.0f}</th>
      <th class="num">{crit_dry_total:+,.0f}</th><th class="num">—</th>
      <th class="num"><strong>{basin_polygon_summed_need:,.0f}</strong></th>
      <th class="num"><strong>{project_total_afy:,}</strong></th>
      <th class="num"><strong><span class="gain">+{basin_portfolio_margin:,.0f}</span></strong></th>
    </tr>
  </tfoot>
</table>

<details>
<summary>Annual basin time series (2000–2025), gap-attributed</summary>
<p style="font-size:13px;color:var(--ink-muted);">Sum of all {n_polygons} polygons' year-over-year storage change with polygon-by-polygon Sy.</p>
<table>
  <thead><tr><th class="num">Year</th><th>Condition</th><th class="num">ΔStor (AF)</th><th class="num">Cumulative (AF)</th></tr></thead>
  <tbody>{chr(10).join(annual_rows)}</tbody>
</table>
</details>
"""


def write_index_html(out_path, results_by_method, portfolio):
    """Build the toggle-able single-file dashboard."""
    method_sections = {
        m: _render_method_section(m, r, portfolio)
        for m, r in results_by_method.items()
    }

    # Buttons in stable order: single first, then three-zone
    toggle_buttons = []
    for m in ("single", "three-zone"):
        if m in method_sections:
            active = " active" if m == "single" else ""
            toggle_buttons.append(
                f'<button data-method="{m}" class="{active.strip()}">{METHOD_LABEL[m]}</button>'
            )
    toggle_html = (
        '<div class="method-toggle">'
        '<span class="method-toggle-label">Polygon method:</span>'
        + "".join(toggle_buttons)
        + '</div>'
    )

    sections_html = []
    for m in ("single", "three-zone"):
        if m in method_sections:
            hidden = "" if m == "single" else " hidden"
            sections_html.append(
                f'<div class="method-content method-{m}{hidden}">'
                + method_sections[m]
                + '</div>'
            )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Vina Subbasin: Where the Losses Happen — 2027 BC RMS Network</title>
<style>{INDEX_CSS}</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Spectral:wght@400;500;700&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
</head>
<body>
<div class="container">

<h1>Where the Losses Happen — A Drought-Conditioned Look at the 2027 BC RMS Network</h1>
<p class="subtitle">May 2026 · Prepared by AGUBC · 28 polygons · polygon-by-polygon Sy from DWR SVSim Texture Data · WY 1999–2025 · ΔGWE × Sy<sub>p</sub> × Area<sub>p</sub>, sliced by hydrologic condition and read against a project-portfolio sustainability target.</p>

{toggle_html}

{chr(10).join(sections_html)}

<!-- Shared polygon popup (moved into the active map-wrap on click) -->
<div id="polygon-popup">
  <button class="popup-close" type="button">×</button>
  <h4 id="pp-name">—</h4>
  <div id="pp-body"></div>
</div>

<div class="footer">
<p><strong>Files in this folder.</strong> <code>index.html</code> (this page) · <code>data/condition_analysis_{{single,three_zone}}.json</code> · <code>data/sustainability_2042_{{single,three_zone}}.json</code> · <code>data/basin_annual_{{single,three_zone}}.json</code> (observed + normalized) · <code>data/model_data_{{single,three_zone}}.json</code> · <code>data/polygon_storage_2025_{{single,three_zone}}.csv</code> · <code>data/storage_timeseries_{{single,three_zone}}.csv</code> · <code>data/polygon_sy_svsim_{{single,three_zone}}.csv</code> · <code>data/project_portfolio.json</code> (editable input) · per-method SVGs (<code>polygon_map_*.svg</code>, <code>basin_buckets_chart_*.svg</code>, <code>basin_cumulative_chart_*.svg</code>, <code>storage_context_*.svg</code>).</p>
<p><strong>Upstream.</strong> Polygons, wells, and DWR periodic GWL measurements come from the companion <a href="https://cosmo1007.github.io/2027-BC-prop-network/">2027-BC-prop-network</a> framework — both <code>polygons-data-single.js</code> (single basin-wide tessellation) and <code>polygons-data-three-zone.js</code> (three independent tessellations per management area) are read here.</p>
<p><strong>Status.</strong> Independent analysis prepared for AGUBC technical staff and Board. Comments and corrections welcomed.</p>
</div>

</div>

<script>{POPUP_JS}{TOGGLE_JS}</script>

</body>
</html>
"""
    out_path.write_text(html)
