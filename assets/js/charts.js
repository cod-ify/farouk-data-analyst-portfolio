/* ==========================================================================
   charts.js — dependency-free SVG chart engine.

   Public API (window.Charts):
     renderBar(el, {categories, series, options})
     renderLine(el, {xLabels, series, options})
     renderWaterfall(el, {steps, options})
     renderComparison(el, {rows, options})
     renderHistogram(el, {binEdges, counts, options})
     autoInit()  — scans the page for [data-chart][data-chart-type] elements,
                   reads the adjacent <script type="application/json"> data
                   block, and dispatches to the matching renderer. Called
                   once by main.js on DOMContentLoaded.

   Every renderer also emits an accessible <table> (behind a "View as table"
   <details>) so chart data is available with JS disabled or via a screen
   reader — see renderAccessibleTable().
   ========================================================================== */

(function () {
  'use strict';

  var SVG_NS = 'http://www.w3.org/2000/svg';
  var VB_W = 640;   // internal SVG coordinate width — scales fluidly via viewBox
  var PAD = { top: 18, right: 20, bottom: 34, left: 56 };

  // -------------------------------------------------------------- helpers --

  function svgEl(tag, attrs) {
    var el = document.createElementNS(SVG_NS, tag);
    if (attrs) {
      for (var k in attrs) {
        if (Object.prototype.hasOwnProperty.call(attrs, k)) el.setAttribute(k, attrs[k]);
      }
    }
    return el;
  }

  function textEl(x, y, content, attrs) {
    var t = svgEl('text', Object.assign({ x: x, y: y }, attrs || {}));
    t.textContent = content;
    return t;
  }

  function fmtNum(v, opts) {
    opts = opts || {};
    if (typeof v !== 'number' || isNaN(v)) return String(v);
    if (opts.prefix === '£') {
      var abs = Math.abs(v);
      var str;
      if (abs >= 1000000) str = (v / 1000000).toFixed(v % 1000000 === 0 ? 0 : 2) + 'm';
      else if (abs >= 1000) str = Math.round(v).toLocaleString('en-GB');
      else str = v.toLocaleString('en-GB', { maximumFractionDigits: 0 });
      return (v < 0 ? '-£' : '£') + str.replace('-', '');
    }
    if (opts.suffix === '%') return v.toLocaleString('en-GB', { maximumFractionDigits: 1 }) + '%';
    if (opts.suffix === 'd') return Math.round(v) + 'd';
    return v.toLocaleString('en-GB', { maximumFractionDigits: 1 });
  }

  // Chart payloads travel through JSON (embedded <script type="application/json">),
  // so options.valueFormat/etc. arrive as string specs, not functions — resolve here.
  function resolveFormatter(spec) {
    if (typeof spec === 'function') return spec;
    if (spec === 'gbp') return function (v) { return fmtNum(v, { prefix: '£' }); };
    if (spec === 'percent') return function (v) { return fmtNum(v, { suffix: '%' }); };
    if (spec === 'days') return function (v) { return fmtNum(v, { suffix: 'd' }); };
    return function (v) { return fmtNum(v); };
  }

  function niceMax(v) {
    if (v <= 0) return 1;
    var mag = Math.pow(10, Math.floor(Math.log10(v)));
    var norm = v / mag;
    var step = norm <= 1 ? 1 : norm <= 2 ? 2 : norm <= 5 ? 5 : 10;
    return step * mag;
  }

  function linearScale(domain, range) {
    var d0 = domain[0], d1 = domain[1], r0 = range[0], r1 = range[1];
    var span = (d1 - d0) || 1;
    return function (v) { return r0 + ((v - d0) / span) * (r1 - r0); };
  }

  // ------------------------------------------------------------- tooltip --

  var tooltipEl = null;
  function getTooltip() {
    if (!tooltipEl) {
      tooltipEl = document.createElement('div');
      tooltipEl.className = 'chart-tooltip';
      tooltipEl.setAttribute('role', 'status');
      tooltipEl.hidden = true;
      document.body.appendChild(tooltipEl);
    }
    return tooltipEl;
  }
  function showTooltip(evt, html) {
    var tt = getTooltip();
    tt.innerHTML = html;
    tt.hidden = false;
    var x = evt.clientX + 14, y = evt.clientY + 14;
    var rect = tt.getBoundingClientRect();
    if (x + rect.width > window.innerWidth - 8) x = evt.clientX - rect.width - 14;
    if (y + rect.height > window.innerHeight - 8) y = evt.clientY - rect.height - 14;
    tt.style.left = x + 'px';
    tt.style.top = y + 'px';
  }
  function hideTooltip() {
    if (tooltipEl) tooltipEl.hidden = true;
  }
  function wireHover(el, htmlFn) {
    el.addEventListener('mousemove', function (e) { showTooltip(e, htmlFn()); });
    el.addEventListener('mouseleave', hideTooltip);
    el.addEventListener('focus', function (e) {
      var rect = el.getBoundingClientRect();
      showTooltip({ clientX: rect.left + rect.width / 2, clientY: rect.top }, htmlFn());
    });
    el.addEventListener('blur', hideTooltip);
    el.setAttribute('tabindex', '0');
  }

  // ------------------------------------------------------- accessible table --

  function cellText(v) {
    return typeof v === 'number' ? String(v) : (v == null ? '' : String(v));
  }

  function renderAccessibleTable(container, headers, rows, opts) {
    opts = opts || {};
    var wrap = document.createElement('details');
    wrap.className = 'chart-table-toggle';
    var summary = document.createElement('summary');
    summary.textContent = opts.summaryLabel || 'View as table';
    wrap.appendChild(summary);

    var table = document.createElement('table');
    table.className = 'data-table';
    var thead = document.createElement('thead');
    var trh = document.createElement('tr');
    headers.forEach(function (h, i) {
      var th = document.createElement('th');
      th.textContent = h.label;
      if (h.sortable !== false) {
        th.classList.add('sortable');
        th.dataset.colIndex = String(i);
        th.dataset.numeric = h.numeric ? '1' : '0';
      }
      trh.appendChild(th);
    });
    thead.appendChild(trh);
    table.appendChild(thead);

    var tbody = document.createElement('tbody');
    rows.forEach(function (row) {
      var tr = document.createElement('tr');
      headers.forEach(function (h) {
        var td = document.createElement('td');
        var val = row[h.key];
        td.textContent = h.format ? resolveFormatter(h.format)(val) : cellText(val);
        if (h.numeric) td.classList.add('num');
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    wrap.appendChild(table);
    container.appendChild(wrap);

    makeSortable(table);
    return wrap;
  }

  function makeSortable(table) {
    var thead = table.querySelector('thead');
    if (!thead) return;
    var ths = Array.prototype.slice.call(thead.querySelectorAll('th.sortable'));
    ths.forEach(function (th) {
      th.addEventListener('click', function () {
        var idx = parseInt(th.dataset.colIndex, 10);
        var numeric = th.dataset.numeric === '1';
        var asc = !th.classList.contains('sort-asc');
        ths.forEach(function (t) { t.classList.remove('sort-asc', 'sort-desc'); });
        th.classList.add(asc ? 'sort-asc' : 'sort-desc');
        var tbody = table.querySelector('tbody');
        var rows = Array.prototype.slice.call(tbody.querySelectorAll('tr'));
        rows.sort(function (a, b) {
          var av = a.children[idx].textContent.trim();
          var bv = b.children[idx].textContent.trim();
          if (numeric) {
            av = parseFloat(av.replace(/[^0-9.\-]/g, '')) || 0;
            bv = parseFloat(bv.replace(/[^0-9.\-]/g, '')) || 0;
            return asc ? av - bv : bv - av;
          }
          return asc ? av.localeCompare(bv) : bv.localeCompare(av);
        });
        rows.forEach(function (r) { tbody.appendChild(r); });
      });
    });
  }

  // ------------------------------------------------------------ chart shell --

  function buildChartRoot(el, height) {
    el.innerHTML = '';
    var canvas = document.createElement('div');
    canvas.className = 'chart-canvas';
    var svg = svgEl('svg', { viewBox: '0 0 ' + VB_W + ' ' + height, preserveAspectRatio: 'xMinYMin meet', role: 'img' });
    canvas.appendChild(svg);
    el.appendChild(canvas);
    return { canvas: canvas, svg: svg };
  }

  function buildFilterBar(el, filterKey, values, activeValue, onChange) {
    var bar = document.createElement('div');
    bar.className = 'chart-filter';
    bar.setAttribute('role', 'group');
    values.forEach(function (v) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.textContent = v;
      if (v === activeValue) btn.classList.add('active');
      btn.addEventListener('click', function () {
        Array.prototype.forEach.call(bar.children, function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
        onChange(v);
      });
      bar.appendChild(btn);
    });
    el.appendChild(bar);
    return bar;
  }

  // ==========================================================================
  // renderBar — vertical or horizontal bar chart, single or grouped series
  // ==========================================================================

  function renderBar(el, cfg) {
    var categories = cfg.categories || [];
    var series = cfg.series || [];
    var opts = cfg.options || {};
    var horizontal = !!opts.horizontal;
    // Horizontal bars are normally used for ranked comparisons, so label their
    // values directly by default. Individual charts can opt out when crowded.
    var showValues = opts.showValues == null ? horizontal : !!opts.showValues;
    var highlightCategories = opts.highlightCategories || [];
    var hasHighlights = highlightCategories.length > 0;
    var valueFmt = resolveFormatter(opts.valueFormat);
    var n = categories.length;
    var height = opts.height || (horizontal ? Math.max(220, n * 26 + 60) : 320);

    var root = buildChartRoot(el, height);
    var svg = root.svg;
    var allVals = [];
    series.forEach(function (s) { allVals = allVals.concat(s.values); });
    var maxV = opts.maxValue == null ? niceMax(Math.max.apply(null, allVals.concat([0]))) : opts.maxValue;
    var minV = opts.minValue == null ? Math.min(0, Math.min.apply(null, allVals.concat([0]))) : opts.minValue;
    if (maxV <= minV) maxV = minV + 1;

    var longestCategory = categories.reduce(function (longest, category) {
      return Math.max(longest, String(category).length);
    }, 0);
    var horizontalLabelSpace = Math.min(176, Math.max(72, longestCategory * 6.2));
    var plot = {
      left: PAD.left + (horizontal ? horizontalLabelSpace : 0),
      right: VB_W - PAD.right - (horizontal ? (showValues ? 76 : 26) : 0),
      top: PAD.top + (!horizontal && showValues ? 16 : 0),
      bottom: height - PAD.bottom
    };

    var groupCount = series.length;
    var band = ((horizontal ? plot.bottom - plot.top : plot.right - plot.left)) / n;
    var barGap = band * 0.28;
    var barW = (band - barGap) / groupCount;

    if (horizontal) {
      var xScale = linearScale([minV, maxV], [plot.left, plot.right]);
      // gridlines + axis
      var ticks = 4;
      for (var t = 0; t <= ticks; t++) {
        var v = minV + (t / ticks) * (maxV - minV);
        var gx = xScale(v);
        svg.appendChild(svgEl('line', { class: 'chart-gridline', x1: gx, x2: gx, y1: plot.top, y2: plot.bottom }));
        svg.appendChild(textEl(gx, plot.bottom + 18, valueFmt(v), { 'text-anchor': 'middle', class: 'chart-axis' }));
      }
      categories.forEach(function (cat, i) {
        var y0 = plot.top + i * band;
        svg.appendChild(textEl(plot.left - 8, y0 + band / 2 + 4, truncateLabel(cat, 26), { 'text-anchor': 'end', class: 'chart-axis' }));
        series.forEach(function (s, si) {
          var val = s.values[i];
          var y = y0 + barGap / 2 + si * barW;
          var x0 = xScale(Math.min(0, val)), x1 = xScale(Math.max(0, val));
          var rect = svgEl('rect', {
            x: x0, y: y, width: Math.max(1, x1 - x0), height: Math.max(1, barW - 2),
            class: 'chart-bar ' + seriesClass(si), fill: s.color || '',
            opacity: hasHighlights && highlightCategories.indexOf(cat) === -1 ? 0.38 : 1
          });
          wireHover(rect, function () {
            return '<span class="tt-label">' + cat + '</span><br>' + (s.label ? s.label + ': ' : '') + valueFmt(val);
          });
          svg.appendChild(rect);
          if (showValues) {
            svg.appendChild(textEl(x1 + 6, y + barW / 2 + 3.5, valueFmt(val), {
              'text-anchor': 'start', class: 'chart-value-label'
            }));
          }
        });
      });
      svg.appendChild(svgEl('line', { class: 'chart-axis', x1: plot.left, x2: plot.left, y1: plot.top, y2: plot.bottom }));
    } else {
      var yScale = linearScale([minV, maxV], [plot.bottom, plot.top]);
      var ticksV = 4;
      for (var tv = 0; tv <= ticksV; tv++) {
        var vv = minV + (tv / ticksV) * (maxV - minV);
        var gy = yScale(vv);
        svg.appendChild(svgEl('line', { class: 'chart-gridline', x1: plot.left, x2: plot.right, y1: gy, y2: gy }));
        svg.appendChild(textEl(plot.left - 8, gy + 4, valueFmt(vv), { 'text-anchor': 'end', class: 'chart-axis' }));
      }
      categories.forEach(function (cat, i) {
        var x0 = plot.left + i * band;
        svg.appendChild(textEl(x0 + band / 2, plot.bottom + 20, truncateLabel(cat, 14), { 'text-anchor': 'middle', class: 'chart-axis' }));
        series.forEach(function (s, si) {
          var val = s.values[i];
          var x = x0 + barGap / 2 + si * barW;
          var yTop = yScale(Math.max(0, val)), yBase = yScale(Math.min(0, val));
          var rect = svgEl('rect', {
            x: x, y: Math.min(yTop, yBase), width: Math.max(1, barW - 2), height: Math.max(1, Math.abs(yBase - yTop)),
            class: 'chart-bar ' + seriesClass(si),
            opacity: hasHighlights && highlightCategories.indexOf(cat) === -1 ? 0.38 : 1
          });
          wireHover(rect, function () {
            return '<span class="tt-label">' + cat + '</span><br>' + (s.label ? s.label + ': ' : '') + valueFmt(val);
          });
          svg.appendChild(rect);
          if (showValues) {
            svg.appendChild(textEl(x + (barW - 2) / 2, Math.min(yTop, yBase) - 5, valueFmt(val), {
              'text-anchor': 'middle', class: 'chart-value-label'
            }));
          }
        });
      });
      svg.appendChild(svgEl('line', { class: 'chart-axis', x1: plot.left, x2: plot.right, y1: plot.bottom, y2: plot.bottom }));
    }

    if (series.length > 1) appendLegend(root.canvas, series);

    var headers = [{ key: 'category', label: opts.categoryLabel || 'Category' }];
    series.forEach(function (s) { headers.push({ key: s.label, label: s.label, numeric: true, format: function (v) { return valueFmt(v); } }); });
    var rows = categories.map(function (cat, i) {
      var row = { category: cat };
      series.forEach(function (s) { row[s.label] = s.values[i]; });
      return row;
    });
    renderAccessibleTable(el, headers, rows);
  }

  var SERIES_CLASSES = ['is-primary', 'is-secondary', 'is-tertiary', 'is-quaternary'];
  var SERIES_COLOR_VARS = ['--teal', '--navy', '--warn', '--muted'];
  function seriesClass(index) {
    return SERIES_CLASSES[index % SERIES_CLASSES.length];
  }
  function seriesColorVar(index) {
    return 'var(' + SERIES_COLOR_VARS[index % SERIES_COLOR_VARS.length] + ')';
  }

  function truncateLabel(s, max) {
    s = String(s);
    return s.length > max ? s.slice(0, max - 1) + '…' : s;
  }

  function formatPeriodLabel(label) {
    var value = String(label);
    var match = value.match(/^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})$/i);
    return match ? match[1] + ' \u2019' + match[2].slice(-2) : value;
  }

  function evenlySpacedIndices(count, maxTicks) {
    if (count <= 0) return [];
    if (count <= maxTicks) {
      return Array.from({ length: count }, function (_, index) { return index; });
    }
    var last = count - 1;
    var indices = [];
    for (var i = 0; i < maxTicks; i++) {
      var index = Math.round(i * last / (maxTicks - 1));
      if (indices.indexOf(index) === -1) indices.push(index);
    }
    return indices;
  }

  function appendLegend(container, series) {
    var legend = document.createElement('div');
    legend.className = 'chart-legend';
    series.forEach(function (s, i) {
      var item = document.createElement('span');
      item.className = 'swatch';
      var dot = document.createElement('span');
      dot.className = 'dot';
      dot.style.background = seriesColorVar(i);
      item.appendChild(dot);
      item.appendChild(document.createTextNode(s.label));
      legend.appendChild(item);
    });
    container.parentNode.insertBefore(legend, container.nextSibling);
  }

  // ==========================================================================
  // renderLine — monthly trend, up to two series (primary + secondary axis)
  // ==========================================================================

  function renderLine(el, cfg) {
    var xLabels = cfg.xLabels || [];
    var series = cfg.series || [];
    var opts = cfg.options || {};
    var height = opts.height || 320;
    var n = xLabels.length;

    var root = buildChartRoot(el, height);
    var svg = root.svg;

    var hasSecondary = series.some(function (s) { return s.axis === 'secondary'; });
    var plot = { left: PAD.left, right: VB_W - (hasSecondary ? PAD.left : PAD.right), top: PAD.top, bottom: height - PAD.bottom };
    var xScale = linearScale([0, n - 1], [plot.left, plot.right]);

    function seriesScale(s) {
      var fmt = resolveFormatter(s.valueFormat);
      var vMax = s.maxValue == null ? niceMax(Math.max.apply(null, s.values)) : s.maxValue;
      var vMin = s.minValue == null ? Math.min(0, Math.min.apply(null, s.values)) : s.minValue;
      if (vMax <= vMin) vMax = vMin + 1;
      return { scale: linearScale([vMin, vMax], [plot.bottom, plot.top]), min: vMin, max: vMax, fmt: fmt };
    }

    var primary = series.filter(function (s) { return s.axis !== 'secondary'; })[0];
    var secondary = series.filter(function (s) { return s.axis === 'secondary'; })[0];
    var pScale = primary ? seriesScale(primary) : null;
    var sScale = secondary ? seriesScale(secondary) : null;

    var ticks = 4;
    if (pScale) {
      for (var t = 0; t <= ticks; t++) {
        var v = pScale.min + (t / ticks) * (pScale.max - pScale.min);
        var gy = pScale.scale(v);
        svg.appendChild(svgEl('line', { class: 'chart-gridline', x1: plot.left, x2: plot.right, y1: gy, y2: gy }));
        svg.appendChild(textEl(plot.left - 8, gy + 4, pScale.fmt(v), { 'text-anchor': 'end', class: 'chart-axis' }));
      }
    }
    if (sScale) {
      for (var t2 = 0; t2 <= ticks; t2++) {
        var v2 = sScale.min + (t2 / ticks) * (sScale.max - sScale.min);
        var gy2 = sScale.scale(v2);
        svg.appendChild(textEl(plot.right + 8, gy2 + 4, sScale.fmt(v2), { 'text-anchor': 'start', class: 'chart-axis' }));
      }
    }

    var xTickIndices = evenlySpacedIndices(n, opts.maxXTicks || 6);
    xTickIndices.forEach(function (i) {
      var anchor = i === 0 ? 'start' : (i === n - 1 ? 'end' : 'middle');
      svg.appendChild(textEl(xScale(i), plot.bottom + 18, formatPeriodLabel(xLabels[i]), { 'text-anchor': anchor, class: 'chart-axis' }));
    });
    svg.appendChild(svgEl('line', { class: 'chart-axis', x1: plot.left, x2: plot.right, y1: plot.bottom, y2: plot.bottom }));

    (opts.annotations || []).forEach(function (ann) {
      var idx = typeof ann.x === 'number' ? ann.x : xLabels.indexOf(ann.x);
      if (idx < 0) return;
      var ax = xScale(idx);
      svg.appendChild(svgEl('line', { class: 'chart-annotation-line', x1: ax, x2: ax, y1: plot.top, y2: plot.bottom }));
      svg.appendChild(textEl(ax, plot.top - 6, ann.label, { 'text-anchor': 'middle', class: 'chart-annotation-label' }));
    });

    function drawSeries(s, scale, isSecondary) {
      var pts = s.values.map(function (v, i) { return [xScale(i), scale.scale(v)]; });
      var d = pts.map(function (p, i) { return (i === 0 ? 'M' : 'L') + p[0].toFixed(1) + ',' + p[1].toFixed(1); }).join(' ');
      var path = svgEl('path', { d: d, class: 'chart-line-path', stroke: isSecondary ? 'var(--navy)' : '' });
      svg.appendChild(path);
      pts.forEach(function (p, i) {
        var dot = svgEl('circle', { cx: p[0], cy: p[1], r: 3.2, class: 'chart-line-dot', fill: isSecondary ? 'var(--navy)' : '' });
        wireHover(dot, function () {
          return '<span class="tt-label">' + xLabels[i] + '</span><br>' + s.label + ': ' + scale.fmt(s.values[i]);
        });
        svg.appendChild(dot);
      });
    }
    if (primary) drawSeries(primary, pScale, false);
    if (secondary) drawSeries(secondary, sScale, true);

    if (series.length > 1) appendLegend(root.canvas, series);

    var headers = [{ key: 'x', label: opts.xLabel || 'Period' }];
    series.forEach(function (s) { headers.push({ key: s.label, label: s.label, numeric: true, format: resolveFormatter(s.valueFormat) }); });
    var rows = xLabels.map(function (lbl, i) {
      var row = { x: lbl };
      series.forEach(function (s) { row[s.label] = s.values[i]; });
      return row;
    });
    renderAccessibleTable(el, headers, rows);
  }

  // ==========================================================================
  // renderWaterfall — cost/expenditure decomposition
  // ==========================================================================

  function renderWaterfall(el, cfg) {
    var steps = cfg.steps || [];
    var opts = cfg.options || {};
    var valueFmt = resolveFormatter(opts.valueFormat || 'gbp');
    var height = opts.height || 340;

    var root = buildChartRoot(el, height);
    var svg = root.svg;
    var plot = { left: PAD.left + 8, right: VB_W - PAD.right, top: PAD.top + 10, bottom: height - PAD.bottom };

    var running = 0;
    var bars = steps.map(function (s) {
      var start = s.isTotal ? 0 : running;
      var end = s.isTotal ? s.value : running + s.value;
      if (!s.isTotal) running = end;
      else running = s.value;
      return { label: s.label, from: Math.min(start, end), to: Math.max(start, end), raw: s.value, isTotal: !!s.isTotal, isNegative: s.value < 0 };
    });

    var allVals = [];
    bars.forEach(function (b) { allVals.push(b.from, b.to); });
    var maxV = niceMax(Math.max.apply(null, allVals));
    var minV = Math.min(0, Math.min.apply(null, allVals));
    var yScale = linearScale([minV, maxV], [plot.bottom, plot.top]);

    var ticks = 4;
    for (var t = 0; t <= ticks; t++) {
      var v = minV + (t / ticks) * (maxV - minV);
      var gy = yScale(v);
      svg.appendChild(svgEl('line', { class: 'chart-gridline', x1: plot.left, x2: plot.right, y1: gy, y2: gy }));
      svg.appendChild(textEl(plot.left - 8, gy + 4, valueFmt(v), { 'text-anchor': 'end', class: 'chart-axis' }));
    }

    var n = bars.length;
    var band = (plot.right - plot.left) / n;
    var barW = band * 0.55;

    bars.forEach(function (b, i) {
      var x = plot.left + i * band + (band - barW) / 2;
      var yTop = yScale(b.to), yBottom = yScale(b.from);
      var cls = 'chart-waterfall-bar ' + (b.isTotal ? 'is-total' : (b.isNegative ? 'is-negative' : 'is-positive'));
      var rect = svgEl('rect', { x: x, y: Math.min(yTop, yBottom), width: barW, height: Math.max(1, Math.abs(yBottom - yTop)), class: cls });
      wireHover(rect, function () {
        return '<span class="tt-label">' + b.label + '</span><br>' + (b.isTotal ? valueFmt(b.raw) : (b.raw >= 0 ? '+' : '') + valueFmt(b.raw));
      });
      svg.appendChild(rect);
      svg.appendChild(textEl(x + barW / 2, Math.min(yTop, yBottom) - 6, (b.isTotal ? '' : (b.raw >= 0 ? '+' : '')) + valueFmt(b.raw), { 'text-anchor': 'middle', class: 'chart-axis', 'font-weight': '700' }));
      svg.appendChild(textEl(x + barW / 2, plot.bottom + 20, truncateLabel(b.label, 16), { 'text-anchor': 'middle', class: 'chart-axis' }));
      if (i < n - 1) {
        var nextX = plot.left + (i + 1) * band + (band - barW) / 2;
        var connectorY = yScale(b.isTotal ? b.raw : b.to);
        svg.appendChild(svgEl('line', { class: 'chart-waterfall-connector', x1: x + barW, x2: nextX, y1: connectorY, y2: connectorY }));
      }
    });
    svg.appendChild(svgEl('line', { class: 'chart-axis', x1: plot.left, x2: plot.right, y1: yScale(0), y2: yScale(0) }));

    var headers = [
      { key: 'label', label: 'Component' },
      { key: 'value', label: 'Value', numeric: true, format: function (v) { return valueFmt(v); } }
    ];
    var rows = steps.map(function (s) { return { label: s.label, value: s.value }; });
    renderAccessibleTable(el, headers, rows);
  }

  // ==========================================================================
  // renderComparison — raw-vs-adjusted dumbbell chart, with optional filter
  // ==========================================================================

  function renderComparison(el, cfg) {
    var opts = cfg.options || {};
    var allRows = cfg.rows || [];

    var wrap = document.createElement('div');
    var canvasHolder = document.createElement('div');

    function draw(rows) {
      canvasHolder.innerHTML = '';
      var sorted = rows.slice().sort(function (a, b) {
        return (opts.sortBy === 'after') ? b.after - a.after : (b.before - a.before);
      });
      var limit = opts.limit || sorted.length;
      var shown = sorted.slice(0, limit);
      var n = shown.length;
      var height = Math.max(220, n * 24 + 60);
      var valueFmt = resolveFormatter(opts.valueFormat || 'gbp');

      var svgWrap = document.createElement('div');
      var root = buildChartRoot(svgWrap, height);
      var svg = root.svg;
      var longestLabel = shown.reduce(function (longest, row) {
        return Math.max(longest, String(row.label).length);
      }, 0);
      var labelSpace = Math.min(190, Math.max(120, longestLabel * 6.2));
      var plot = { left: PAD.left + labelSpace, right: VB_W - PAD.right - 10, top: PAD.top, bottom: height - PAD.bottom };
      var allVals = [];
      shown.forEach(function (r) { allVals.push(r.before, r.after); });
      var minV = opts.minValue == null ? 0 : opts.minValue;
      var maxV = opts.maxValue == null ? niceMax(Math.max.apply(null, allVals.concat([0]))) : opts.maxValue;
      if (maxV <= minV) maxV = minV + 1;
      var xScale = linearScale([minV, maxV], [plot.left, plot.right]);

      var ticks = 4;
      for (var t = 0; t <= ticks; t++) {
        var v = minV + (t / ticks) * (maxV - minV);
        var gx = xScale(v);
        svg.appendChild(svgEl('line', { class: 'chart-gridline', x1: gx, x2: gx, y1: plot.top, y2: plot.bottom }));
        svg.appendChild(textEl(gx, plot.bottom + 18, valueFmt(v), { 'text-anchor': 'middle', class: 'chart-axis' }));
      }

      var band = (plot.bottom - plot.top) / n;
      shown.forEach(function (r, i) {
        var y = plot.top + i * band + band / 2;
        svg.appendChild(textEl(plot.left - 10, y + 4, r.label, { 'text-anchor': 'end', class: 'chart-comparison-label' }));
        var x0 = xScale(r.before), x1 = xScale(r.after);
        svg.appendChild(svgEl('line', { class: 'chart-comparison-line', x1: x0, x2: x1, y1: y, y2: y }));
        var dotBefore = svgEl('circle', { cx: x0, cy: y, r: 4.5, class: 'chart-comparison-dot is-before' });
        wireHover(dotBefore, function () { return '<span class="tt-label">' + r.label + '</span><br>' + (opts.beforeLabel || 'Raw') + ': ' + valueFmt(r.before); });
        var dotAfter = svgEl('circle', { cx: x1, cy: y, r: 4.5, class: 'chart-comparison-dot is-after' });
        wireHover(dotAfter, function () { return '<span class="tt-label">' + r.label + '</span><br>' + (opts.afterLabel || 'Adjusted') + ': ' + valueFmt(r.after); });
        svg.appendChild(dotBefore);
        svg.appendChild(dotAfter);
      });
      svg.appendChild(svgEl('line', { class: 'chart-axis', x1: plot.left, x2: plot.left, y1: plot.top, y2: plot.bottom }));

      var legend = document.createElement('div');
      legend.className = 'chart-legend';
      [[opts.beforeLabel || 'Raw', 'var(--muted)'], [opts.afterLabel || 'Adjusted', 'var(--teal)']].forEach(function (pair) {
        var item = document.createElement('span');
        item.className = 'swatch';
        var dot = document.createElement('span');
        dot.className = 'dot';
        dot.style.background = pair[1];
        item.appendChild(dot);
        item.appendChild(document.createTextNode(pair[0]));
        legend.appendChild(item);
      });

      canvasHolder.appendChild(legend);
      canvasHolder.appendChild(svgWrap);

      var headers = [
        { key: 'label', label: opts.categoryLabel || 'Name' },
        { key: 'before', label: opts.beforeLabel || 'Raw', numeric: true, format: function (v) { return valueFmt(v); } },
        { key: 'after', label: opts.afterLabel || 'Adjusted', numeric: true, format: function (v) { return valueFmt(v); } }
      ];
      if (opts.metaColumns) {
        opts.metaColumns.forEach(function (mc) {
          headers.push({ key: 'meta_' + mc.key, label: mc.label, numeric: !!mc.numeric, format: mc.format });
        });
      }
      var tableRows = rows.map(function (r) {
        var row = { label: r.label, before: r.before, after: r.after };
        if (opts.metaColumns) opts.metaColumns.forEach(function (mc) { row['meta_' + mc.key] = r.meta ? r.meta[mc.key] : ''; });
        return row;
      });
      var existingToggle = canvasHolder.parentNode ? canvasHolder.parentNode.querySelector('.chart-table-toggle') : null;
      if (existingToggle) existingToggle.remove();
      renderAccessibleTable(wrap, headers, tableRows, { summaryLabel: 'View all ' + rows.length + ' rows as a sortable table' });
    }

    el.innerHTML = '';
    if (opts.filterKey && opts.filterValues && opts.filterValues.length) {
      var active = opts.filterDefault || opts.filterValues[0];
      buildFilterBar(wrap, opts.filterKey, opts.filterValues, active, function (val) {
        draw(allRows.filter(function (r) { return r.meta && r.meta[opts.filterKey] === val; }));
      });
      draw(allRows.filter(function (r) { return r.meta && r.meta[opts.filterKey] === active; }));
    } else {
      draw(allRows);
    }
    wrap.appendChild(canvasHolder);
    el.appendChild(wrap);
  }

  // ==========================================================================
  // renderHistogram — right-skew distribution with mean/median markers
  // ==========================================================================

  function renderHistogram(el, cfg) {
    var binEdges = cfg.binEdges || [];
    var counts = cfg.counts || [];
    var opts = cfg.options || {};
    var valueFmt = resolveFormatter(opts.valueFormat || 'gbp');
    var height = opts.height || 300;

    var root = buildChartRoot(el, height);
    var svg = root.svg;
    var plot = { left: PAD.left, right: VB_W - PAD.right, top: PAD.top + 30, bottom: height - PAD.bottom };

    var maxC = niceMax(Math.max.apply(null, counts.concat([0])));
    var xMin = binEdges[0], xMax = binEdges[binEdges.length - 1];
    var xScale = linearScale([xMin, xMax], [plot.left, plot.right]);
    var yScale = linearScale([0, maxC], [plot.bottom, plot.top]);

    var ticks = 4;
    for (var t = 0; t <= ticks; t++) {
      var v = (t / ticks) * maxC;
      var gy = yScale(v);
      svg.appendChild(svgEl('line', { class: 'chart-gridline', x1: plot.left, x2: plot.right, y1: gy, y2: gy }));
      svg.appendChild(textEl(plot.left - 8, gy + 4, Math.round(v), { 'text-anchor': 'end', class: 'chart-axis' }));
    }

    counts.forEach(function (c, i) {
      var x0 = xScale(binEdges[i]), x1 = xScale(binEdges[i + 1]);
      var y = yScale(c);
      var rect = svgEl('rect', { x: x0, y: y, width: Math.max(1, x1 - x0 - 1), height: Math.max(0, plot.bottom - y), class: 'chart-histogram-bar' });
      wireHover(rect, function () {
        return valueFmt(binEdges[i]) + ' – ' + valueFmt(binEdges[i + 1]) + '<br>' + c.toLocaleString('en-GB') + ' claims';
      });
      svg.appendChild(rect);
    });

    var xTickCount = 5;
    for (var xt = 0; xt <= xTickCount; xt++) {
      var xv = xMin + (xt / xTickCount) * (xMax - xMin);
      svg.appendChild(textEl(xScale(xv), plot.bottom + 18, valueFmt(xv), { 'text-anchor': 'middle', class: 'chart-axis' }));
    }
    svg.appendChild(svgEl('line', { class: 'chart-axis', x1: plot.left, x2: plot.right, y1: plot.bottom, y2: plot.bottom }));

    function marker(val, label, row) {
      if (val == null) return;
      var mx = xScale(val);
      svg.appendChild(svgEl('line', { class: 'chart-histogram-marker', x1: mx, x2: mx, y1: plot.top, y2: plot.bottom }));
      svg.appendChild(textEl(mx, plot.top - 7 - (row * 20), label + ' ' + valueFmt(val), { 'text-anchor': 'middle', class: 'chart-annotation-label chart-histogram-label', fill: 'var(--navy)' }));
    }
    marker(opts.meanLine, 'Mean', 0);
    marker(opts.medianLine, 'Median', 1);

    var headers = [
      { key: 'range', label: 'Range' },
      { key: 'count', label: 'Count', numeric: true }
    ];
    var rows = counts.map(function (c, i) { return { range: valueFmt(binEdges[i]) + ' – ' + valueFmt(binEdges[i + 1]), count: c }; });
    renderAccessibleTable(el, headers, rows);
  }

  // ==================================================================== auto-init --

  function autoInit() {
    var nodes = document.querySelectorAll('[data-chart][data-chart-type]');
    Array.prototype.forEach.call(nodes, function (el) {
      var type = el.getAttribute('data-chart-type');
      var dataId = el.getAttribute('data-chart');
      var dataScript = document.getElementById(dataId);
      if (!dataScript) return;
      var payload;
      try {
        payload = JSON.parse(dataScript.textContent);
      } catch (e) {
        return;
      }
      switch (type) {
        case 'bar': renderBar(el, payload); break;
        case 'line': renderLine(el, payload); break;
        case 'waterfall': renderWaterfall(el, payload); break;
        case 'comparison': renderComparison(el, payload); break;
        case 'histogram': renderHistogram(el, payload); break;
      }
    });
  }

  window.Charts = {
    renderBar: renderBar,
    renderLine: renderLine,
    renderWaterfall: renderWaterfall,
    renderComparison: renderComparison,
    renderHistogram: renderHistogram,
    renderAccessibleTable: renderAccessibleTable,
    autoInit: autoInit
  };
})();
