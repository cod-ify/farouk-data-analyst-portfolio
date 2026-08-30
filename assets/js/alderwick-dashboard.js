/* ==========================================================================
   alderwick-dashboard.js — interactive prototype of the Alderwick priority
   dashboard. Four linked views (Portfolio -> Firm -> Audit -> Actions),
   hash-routed, keyboard-navigable, every chart backed by charts.js (which
   supplies its own tooltip + "View as table" fallback).

   Data: inline <script type="application/json" id="ald-data"> — see
   assets/data/alderwick/generate.py for how it is built. The audits array is
   positional to keep the payload small:
     [id, firmId, sectorIdx, score, car, fsq, pif, mkt, bandIdx, cxIdx, itIdx,
      groupStructure(0|1), estimateHeavy(0|1), [flagIdx...]]
   ========================================================================== */
(function () {
  'use strict';

  var root = document.getElementById('ald-dash');
  var dataEl = document.getElementById('ald-data');
  if (!root || !dataEl) return;

  var DB = JSON.parse(dataEl.textContent);
  var L = DB.legends;
  var AS_OF = new Date(DB.meta.as_of + 'T00:00:00');

  // ---- decode --------------------------------------------------------------
  var AUDITS = DB.audits.map(function (a) {
    return {
      id: a[0], firmId: a[1], sector: L.sectors[a[2]], score: a[3],
      comp: { car: a[4], fsq: a[5], pif: a[6], mkt: a[7] },
      band: L.bands[a[8]], complexity: L.levels[a[9]], itReliance: L.levels[a[10]],
      groupStructure: !!a[11], estimateHeavy: !!a[12],
      flags: a[13].map(function (i) { return L.flags[i]; })
    };
  });
  var FIRMS = DB.firms;
  var FIRM_BY_ID = {};
  FIRMS.forEach(function (f) { FIRM_BY_ID[f.id] = f; });
  var ACTIONS = DB.actions;
  var OVERRIDES = {}; // audit id -> decision string (session only)

  var BAND_LABEL = { 'deep-dive': 'Deep-dive inspection', 'group': 'Group review',
    'ask': 'Ask for information', 'routine': 'Routine monitoring' };
  var ROUTE_LABEL = BAND_LABEL;

  // ---- tiny DOM helper ----------------------------------------------------
  function el(tag, attrs, kids) {
    var node = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'text') node.textContent = attrs[k];
      else if (k === 'html') node.innerHTML = attrs[k];
      else if (k === 'class') node.className = attrs[k];
      else if (k in node && k !== 'list') { try { node[k] = attrs[k]; } catch (e) { node.setAttribute(k, attrs[k]); } }
      else node.setAttribute(k, attrs[k]);
    });
    (kids || []).forEach(function (c) {
      if (c == null) return;
      node.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
    });
    return node;
  }
  function pct(n) { return Math.round(n) + '%'; }
  function daysBetween(a, b) { return Math.round((a - b) / 86400000); }

  function routeBadge(route) {
    return el('span', { class: 'route-badge r-' + route.replace('-dive', ''), text: ROUTE_LABEL[route] || route });
  }
  function bandBadge(band) {
    return el('span', { class: 'band-badge b-' + band, text: BAND_LABEL[band] || band });
  }

  // ---- derived aggregates ----------------------------------------------
  function firmAudits(fid) { return AUDITS.filter(function (a) { return a.firmId === fid; }); }
  function firmPriority(fid) { return firmAudits(fid).filter(function (a) { return a.score >= DB.meta.priority_threshold; }); }
  function firmOverdue(fid) { return ACTIONS.filter(function (r) { return r.f === fid && r.st === 'Overdue'; }); }
  var TOTAL_OVERDUE = ACTIONS.filter(function (r) { return r.st === 'Overdue'; }).length;
  var TOTAL_DEFERRED = ACTIONS.filter(function (r) { return r.def >= 2; }).length;
  var TOTAL_CLOSED = ACTIONS.filter(function (r) { return r.st === 'Closed'; }).length;
  var DEEP_DIVE_FIRMS = FIRMS.filter(function (f) { return f.route === 'deep-dive'; }).length;

  // ---- shared chrome ----------------------------------------------------
  function crumbs(items) {
    if (items.length < 2) return document.createComment('no-crumb');
    var c = el('nav', { class: 'ald-crumbs', 'aria-label': 'Breadcrumb' });
    items.forEach(function (it, i) {
      if (i) c.appendChild(el('span', { class: 'sep', text: '/' }));
      if (it.href) c.appendChild(el('a', { href: it.href, text: it.label }));
      else c.appendChild(el('span', { 'aria-current': 'page', text: it.label }));
    });
    return c;
  }
  function tabs(active) {
    var defs = [['#/', 'Portfolio'], ['#/actions', 'Remediation actions']];
    var t = el('div', { class: 'ald-tabs', role: 'navigation', 'aria-label': 'Dashboard views' });
    defs.forEach(function (d) {
      var a = el('a', { href: d[0], text: d[1] });
      if (d[0] === active) a.setAttribute('aria-current', 'page');
      t.appendChild(a);
    });
    return t;
  }
  function kpi(n, label, flag) {
    return el('div', { class: 'ald-kpi' + (flag ? ' is-flag' : '') }, [
      el('span', { class: 'n', text: String(n) }),
      el('span', { class: 'l', text: label })
    ]);
  }
  function kpiRow(list) {
    return el('div', { class: 'ald-kpis' }, list.map(function (k) { return kpi(k[0], k[1], k[2]); }));
  }

  // ---- sortable table -------------------------------------------------
  // cols: [{key,label,num,render(row)->node|string, sortVal(row)}]
  function table(cols, rows, opts) {
    opts = opts || {};
    var state = { key: opts.sortKey || null, dir: opts.sortDir || 'descending' };
    var wrap = el('div', { class: 'ald-table-wrap' });
    var tbl = el('table', { class: 'ald-table' });
    var thead = el('thead');
    var trh = el('tr');
    cols.forEach(function (col) {
      var th = el('th', { scope: 'col', class: col.num ? 'num' : '' });
      if (col.sortVal) {
        var btn = el('button', { class: 'sorth', type: 'button', text: col.label });
        btn.addEventListener('click', function () {
          if (state.key === col.key) state.dir = state.dir === 'ascending' ? 'descending' : 'ascending';
          else { state.key = col.key; state.dir = 'descending'; }
          paint();
        });
        th.appendChild(btn);
      } else {
        th.textContent = col.label;
      }
      trh.appendChild(th);
    });
    thead.appendChild(trh);
    tbl.appendChild(thead);
    var tbody = el('tbody');
    tbl.appendChild(tbody);
    wrap.appendChild(tbl);

    function paint() {
      var r = rows.slice();
      if (state.key) {
        var col = cols.filter(function (c) { return c.key === state.key; })[0];
        r.sort(function (a, b) {
          var va = col.sortVal(a), vb = col.sortVal(b);
          if (va < vb) return state.dir === 'ascending' ? -1 : 1;
          if (va > vb) return state.dir === 'ascending' ? 1 : -1;
          return 0;
        });
      }
      Array.prototype.forEach.call(trh.children, function (th, i) {
        if (cols[i].sortVal) th.setAttribute('aria-sort', cols[i].key === state.key ? state.dir : 'none');
      });
      tbody.textContent = '';
      if (!r.length) {
        var tr = el('tr');
        tr.appendChild(el('td', { colspan: String(cols.length), class: 'ald-empty', text: opts.empty || 'Nothing to show.' }));
        tbody.appendChild(tr);
        return;
      }
      r.forEach(function (row) {
        var tr = el('tr');
        cols.forEach(function (col) {
          var td = el('td', { class: col.cls || (col.num ? 'num' : '') });
          var v = col.render(row);
          if (v == null) v = '';
          td.appendChild(typeof v === 'string' ? document.createTextNode(v) : v);
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });
    }
    paint();
    return wrap;
  }

  // ---- chart mount ----------------------------------------------------
  function chartCard(title, caption, mount) {
    var card = el('div', { class: 'ald-card' }, [el('h3', { text: title })]);
    var holder = el('div');
    card.appendChild(holder);
    if (caption) card.appendChild(el('p', { class: 'ald-card-cap', text: caption }));
    mount(holder);
    return card;
  }

  // ======================================================================
  // VIEW: Portfolio
  // ======================================================================
  function viewPortfolio(view) {
    view.appendChild(crumbs([{ label: 'Portfolio' }]));
    view.appendChild(tabs('#/'));
    var h = el('h2', { tabindex: '-1', text: 'Portfolio view — all 12 firms' });
    view.appendChild(h);
    view.appendChild(el('p', { class: 'ald-sub', text: 'Every active audit scored on the same 100-point scale. Start with the firms carrying the most priority audits.' }));

    view.appendChild(kpiRow([
      [DB.meta.active_audits, 'Active audits scored'],
      [firmPriorityTotal(), 'Priority audits (score 65+)'],
      [DEEP_DIVE_FIRMS + ' firms', 'On the deep-dive route'],
      [TOTAL_OVERDUE, 'Remediation actions overdue', true]
    ]));

    // route strip
    var routeOrder = ['routine', 'ask', 'group', 'deep-dive'];
    view.appendChild(el('div', { class: 'ald-routes' }, routeOrder.map(function (rt) {
      var n = FIRMS.filter(function (f) { return f.route === rt; }).length;
      return el('div', { class: 'ald-route' + (rt === 'deep-dive' ? ' is-deep' : '') }, [
        el('span', { class: 'n', text: String(n) }),
        el('span', { class: 'l', text: ROUTE_LABEL[rt] })
      ]);
    })));

    // chart: firms by priority-audit count, top 3 emphasised
    var ranked = FIRMS.slice().sort(function (a, b) { return b.priority_audits - a.priority_audits; });
    view.appendChild(chartCard(
      'Priority audits by firm',
      'Three firms hold 25 of the 38 priority audits. They are the firms already on the deep-dive route.',
      function (holder) {
        window.Charts.renderBar(holder, {
          categories: ranked.map(function (f) { return f.name; }),
          series: [{ label: 'Priority audits', values: ranked.map(function (f) { return f.priority_audits; }) }],
          options: {
            horizontal: true, valueFormat: 'number', maxValue: 12, height: 340,
            categoryLabel: 'Firm',
            emphasis: ranked.filter(function (f) { return f.route === 'deep-dive'; }).map(function (f) { return f.name; })
          }
        });
      }
    ));

    // firm table
    var cols = [
      { key: 'name', label: 'Firm', sortVal: function (f) { return f.name.toLowerCase(); },
        render: function (f) { return el('a', { href: '#/firm/' + f.id, text: f.name }); } },
      { key: 'route', label: 'Route', sortVal: function (f) { return ['routine', 'ask', 'group', 'deep-dive'].indexOf(f.route); },
        render: function (f) { return routeBadge(f.route); } },
      { key: 'active', label: 'Active audits', num: true, sortVal: function (f) { return f.active_audits; },
        render: function (f) { return String(f.active_audits); } },
      { key: 'prio', label: 'Priority (65+)', num: true, sortVal: function (f) { return f.priority_audits; },
        render: function (f) { return String(f.priority_audits); } },
      { key: 'turn', label: 'Staff turnover', num: true, sortVal: function (f) { return f.staff_turnover; },
        render: function (f) { return f.staff_turnover + '%'; } },
      { key: 'od', label: 'Overdue actions', num: true, sortVal: function (f) { return firmOverdue(f.id).length; },
        render: function (f) { return String(firmOverdue(f.id).length); } }
    ];
    view.appendChild(chartCardShell('All 12 firms', 'Select a firm to see its staffing trend, quality ratings and priority audits.',
      table(cols, FIRMS, { sortKey: 'prio', sortDir: 'descending' })));
  }
  function firmPriorityTotal() {
    return AUDITS.filter(function (a) { return a.score >= DB.meta.priority_threshold; }).length;
  }
  function chartCardShell(title, caption, contentNode) {
    var card = el('div', { class: 'ald-card' }, [el('h3', { text: title }), contentNode]);
    if (caption) card.appendChild(el('p', { class: 'ald-card-cap', text: caption }));
    return card;
  }

  // ======================================================================
  // VIEW: Firm
  // ======================================================================
  function viewFirm(view, fid) {
    var f = FIRM_BY_ID[fid];
    if (!f) return notFound(view, 'firm');
    view.appendChild(crumbs([{ label: 'Portfolio', href: '#/' }, { label: f.name }]));
    view.appendChild(tabs('#/'));
    var h = el('h2', { tabindex: '-1', text: f.name });
    view.appendChild(h);
    var sub = el('p', { class: 'ald-sub' }, [routeBadge(f.route), '  Lead supervisor: ' + f.supervisor]);
    view.appendChild(sub);

    var prio = firmPriority(fid);
    view.appendChild(kpiRow([
      [f.active_audits, 'Active audits'],
      [prio.length, 'Priority audits (65+)'],
      [f.staff_turnover + '%', 'Staff turnover, 2025'],
      [f.partner_hours_per_audit, 'Partner hours per audit']
    ]));

    view.appendChild(el('div', { class: 'ald-two' }, [
      chartCard('Staff turnover, three-year trend', null, function (holder) {
        window.Charts.renderLine(holder, {
          xLabels: f.capacity.map(function (c) { return String(c.year); }),
          series: [{ label: 'Staff turnover %', values: f.capacity.map(function (c) { return c.turnover; }),
            valueFormat: 'percent', maxValue: 30 }],
          options: { height: 230, xLabel: 'Year', endLabels: true }
        });
      }),
      chartCard('Partner hours per audit, three-year trend', null, function (holder) {
        window.Charts.renderLine(holder, {
          xLabels: f.capacity.map(function (c) { return String(c.year); }),
          series: [{ label: 'Partner hours per audit', values: f.capacity.map(function (c) { return c.partner_hours; }), maxValue: 120 }],
          options: { height: 230, xLabel: 'Year', endLabels: true }
        });
      })
    ]));

    // SoQM ratings
    if (f.soqm && f.soqm.length) {
      var soqm = el('div', { class: 'ald-soqm' }, f.soqm.map(function (s) {
        return el('div', { class: 'row' + (s.flag ? ' flagged' : '') }, [
          el('span', { text: s.area }),
          el('span', { class: 'rating', text: s.rating })
        ]);
      }));
      view.appendChild(chartCardShell('Quality management ratings, 2025', 'Areas shaded red are rated a high risk and feed the firm-level part of every audit score.', soqm));
    }

    // priority audit table (fall back to top 8 by score if none clear the line)
    var list = prio.length ? prio : firmAudits(fid).slice().sort(function (a, b) { return b.score - a.score; }).slice(0, 8);
    var cols = [
      { key: 'id', label: 'Audit', sortVal: function (a) { return a.id; },
        render: function (a) { return el('a', { href: '#/audit/' + a.id, text: a.id }); } },
      { key: 'sec', label: 'Sector', sortVal: function (a) { return a.sector; }, render: function (a) { return a.sector; } },
      { key: 'score', label: 'Priority score', num: true, sortVal: function (a) { return a.score; }, render: function (a) { return String(a.score); } },
      { key: 'band', label: 'Route', sortVal: function (a) { return ['routine', 'ask', 'group', 'deep-dive'].indexOf(a.band); }, render: function (a) { return bandBadge(a.band); } },
      { key: 'cx', label: 'Complexity', sortVal: function (a) { return ['Low', 'Medium', 'High'].indexOf(a.complexity); }, render: function (a) { return a.complexity; } },
      { key: 'it', label: 'IT reliance', sortVal: function (a) { return ['Low', 'Medium', 'High'].indexOf(a.itReliance); }, render: function (a) { return a.itReliance; } }
    ];
    view.appendChild(chartCardShell(
      prio.length ? ('Priority audits at ' + f.name) : ('Highest-scoring audits at ' + f.name),
      'Open an audit to see the score breakdown and the specific findings behind it.',
      table(cols, list, { sortKey: 'score', sortDir: 'descending' })
    ));

    view.appendChild(el('a', { class: 'ald-back', href: '#/', text: '← Back to portfolio' }));
  }

  // ======================================================================
  // VIEW: Audit
  // ======================================================================
  function viewAudit(view, aid) {
    var a = AUDITS.filter(function (x) { return x.id === aid; })[0];
    if (!a) return notFound(view, 'audit');
    var f = FIRM_BY_ID[a.firmId];
    view.appendChild(crumbs([
      { label: 'Portfolio', href: '#/' },
      { label: f.name, href: '#/firm/' + f.id },
      { label: a.id }
    ]));
    view.appendChild(tabs('#/'));
    var h = el('h2', { tabindex: '-1', text: 'Audit ' + a.id });
    view.appendChild(h);
    view.appendChild(el('p', { class: 'ald-sub', text: f.name + '  ·  ' + a.sector + '  ·  FY2025' }));

    view.appendChild(el('div', { class: 'ald-score-hero' }, [
      el('span', { class: 'score', text: String(a.score) }),
      el('span', { class: 'of', text: '/ 100 priority score' }),
      bandBadge(a.band)
    ]));

    view.appendChild(chartCard(
      'How the 100 points break down',
      'The two green segments are present-day evidence; the grey segments are historical and market context.',
      function (holder) {
        window.Charts.renderStackedBar(holder, {
          segments: [
            { label: 'Current audit risk', value: a.comp.car, tone: 'tone-accent' },
            { label: 'Firm staffing and quality', value: a.comp.fsq, tone: 'tone-accent-2' },
            { label: 'Past inspections and fixes', value: a.comp.pif, tone: 'tone-context' },
            { label: 'Market importance', value: a.comp.mkt, tone: 'tone-context-2' }
          ],
          options: { valueFormat: 'number', unit: 'pts', total: 100, height: 50,
            categoryLabel: 'Scoring component', valueLabel: 'Points' }
        });
      }
    ));

    view.appendChild(el('div', { class: 'ald-two' }, [
      (function () {
        var card = el('div', { class: 'ald-card' }, [el('h3', { text: 'Warning signs on this audit' })]);
        if (a.flags.length) {
          card.appendChild(el('ul', { class: 'ald-flags' }, a.flags.map(function (fl) { return el('li', { text: fl }); })));
        } else {
          card.appendChild(el('ul', { class: 'ald-flags' }, [el('li', { class: 'none', text: 'No individual warning signs recorded. Score is driven by firm-level and context factors.' })]));
        }
        return card;
      })(),
      (function () {
        var dl = el('dl', { class: 'ald-attrs' }, [
          attr('Complexity', a.complexity),
          attr('Reliance on client IT', a.itReliance),
          attr('Group structure', a.groupStructure ? 'Yes — multi-component' : 'No'),
          attr('Estimate-heavy', a.estimateHeavy ? 'Yes' : 'No')
        ]);
        return el('div', { class: 'ald-card' }, [el('h3', { text: 'Audit characteristics' }), dl]);
      })()
    ]));

    // human override
    view.appendChild(overrideControl(a));

    // linked remediation for the firm
    var od = firmOverdue(a.firmId);
    var cols = [
      { key: 'cat', label: 'Area', sortVal: function (r) { return r.cat; }, render: function (r) { return r.cat; } },
      { key: 'd', label: 'Action', cls: 'act', sortVal: function (r) { return r.d; }, render: function (r) { return r.d; } },
      { key: 'o', label: 'Owner', sortVal: function (r) { return r.o; }, render: function (r) { return r.o; } },
      { key: 'due', label: 'Days overdue', num: true, sortVal: function (r) { return daysBetween(AS_OF, new Date(r.due)); },
        render: function (r) { return String(daysBetween(AS_OF, new Date(r.due))); } }
    ];
    view.appendChild(chartCardShell(
      'Overdue remediation at ' + f.name + ' (' + od.length + ')',
      'Every audit score is traceable to items like these. Full list on the Remediation actions tab.',
      table(cols, od.slice(0, 8), { sortKey: 'due', sortDir: 'descending', empty: 'No overdue actions at this firm.' })
    ));

    view.appendChild(el('a', { class: 'ald-back', href: '#/firm/' + f.id, text: '← Back to ' + f.name }));
  }
  function attr(dt, dd) { return el('div', { class: 'ald-attr' }, [el('dt', { text: dt }), el('dd', { text: dd })]); }

  function overrideControl(a) {
    var box = el('div', { class: 'ald-override' }, [
      el('h3', { text: 'Supervisor decision' }),
      el('p', { text: 'The model recommends a route. A supervisor confirms it, changes it, or holds for evidence — and the choice is logged.' })
    ]);
    var sel = el('select', { 'aria-label': 'Supervisor decision for ' + a.id });
    ['Accept model priority', 'Hold for evidence', 'Downgrade after review', 'Escalate for immediate inspection']
      .forEach(function (o) { sel.appendChild(el('option', { value: o, text: o })); });
    if (OVERRIDES[a.id]) sel.value = OVERRIDES[a.id];
    var recorded = el('span', { class: 'recorded' });
    function say() {
      recorded.textContent = '';
      recorded.appendChild(document.createTextNode('Recorded: '));
      recorded.appendChild(el('strong', { text: OVERRIDES[a.id] || 'Accept model priority' }));
      recorded.appendChild(document.createTextNode('  (' + DB.meta.as_of + ', ' + FIRM_BY_ID[a.firmId].supervisor + ')'));
    }
    sel.addEventListener('change', function () { OVERRIDES[a.id] = sel.value; say(); });
    say();
    box.appendChild(el('div', { class: 'row' }, [sel, recorded]));
    return box;
  }

  // ======================================================================
  // VIEW: Actions
  // ======================================================================
  function viewActions(view) {
    view.appendChild(crumbs([{ label: 'Remediation actions' }]));
    view.appendChild(tabs('#/actions'));
    var h = el('h2', { tabindex: '-1', text: 'Remediation actions — what is overdue and who owns it' });
    view.appendChild(h);
    view.appendChild(el('p', { class: 'ald-sub', text: 'The bottom of every drill-down. Filter to a firm, or to the actions that have slipped their deadline more than once.' }));

    view.appendChild(kpiRow([
      [TOTAL_OVERDUE, 'Actions overdue now', true],
      [TOTAL_DEFERRED, 'Deferred two or more times', true],
      [TOTAL_CLOSED, 'Closed this supervision cycle'],
      [ACTIONS.length, 'Remediation actions in total']
    ]));

    var filters = { firm: 'all', mode: 'overdue' };
    var fbar = el('div', { class: 'ald-filters' });
    var firmSel = el('select', { 'aria-label': 'Filter by firm' });
    firmSel.appendChild(el('option', { value: 'all', text: 'All firms' }));
    FIRMS.forEach(function (f) { firmSel.appendChild(el('option', { value: f.id, text: f.name })); });
    var modeSel = el('select', { 'aria-label': 'Filter by status' });
    [['overdue', 'Overdue now'], ['deferred', 'Deferred 2+ times'], ['all', 'All actions']]
      .forEach(function (o) { modeSel.appendChild(el('option', { value: o[0], text: o[1] })); });
    fbar.appendChild(el('label', {}, ['Firm', firmSel]));
    fbar.appendChild(el('label', {}, ['Show', modeSel]));
    view.appendChild(fbar);

    var tableHolder = el('div');
    view.appendChild(tableHolder);

    function rowsForFilter() {
      return ACTIONS.filter(function (r) {
        if (filters.firm !== 'all' && r.f !== filters.firm) return false;
        if (filters.mode === 'overdue') return r.st === 'Overdue';
        if (filters.mode === 'deferred') return r.def >= 2;
        return true;
      });
    }
    var cols = [
      { key: 'firm', label: 'Firm', sortVal: function (r) { return FIRM_BY_ID[r.f].name; },
        render: function (r) { return el('a', { href: '#/firm/' + r.f, text: FIRM_BY_ID[r.f].name }); } },
      { key: 'cat', label: 'Area', sortVal: function (r) { return r.cat; }, render: function (r) { return r.cat; } },
      { key: 'd', label: 'Action', cls: 'act', sortVal: function (r) { return r.d; }, render: function (r) { return r.d; } },
      { key: 'o', label: 'Owner', sortVal: function (r) { return r.o; }, render: function (r) { return r.o; } },
      { key: 'due', label: 'Due', sortVal: function (r) { return r.due; }, render: function (r) { return r.due; } },
      { key: 'od', label: 'Days overdue', num: true, sortVal: function (r) { return daysBetween(AS_OF, new Date(r.due)); },
        render: function (r) { var d = daysBetween(AS_OF, new Date(r.due)); return d > 0 ? String(d) : '—'; } },
      { key: 'def', label: 'Deferrals', num: true, sortVal: function (r) { return r.def; },
        render: function (r) { return r.def >= 2 ? el('span', { class: 'defer-badge', text: r.def + '×' }) : String(r.def); } }
    ];
    function repaint() {
      tableHolder.textContent = '';
      tableHolder.appendChild(chartCardShell(
        'Actions (' + rowsForFilter().length + ')', null,
        table(cols, rowsForFilter(), { sortKey: 'od', sortDir: 'descending', empty: 'No actions match this filter.' })
      ));
    }
    firmSel.addEventListener('change', function () { filters.firm = firmSel.value; repaint(); });
    modeSel.addEventListener('change', function () { filters.mode = modeSel.value; repaint(); });
    repaint();

    view.appendChild(el('a', { class: 'ald-back', href: '#/', text: '← Back to portfolio' }));
  }

  // ======================================================================
  // router
  // ======================================================================
  function notFound(view, kind) {
    view.appendChild(tabs('#/'));
    view.appendChild(el('h2', { tabindex: '-1', text: 'That ' + kind + ' was not found' }));
    view.appendChild(el('p', { class: 'ald-sub', text: 'It may have been renamed. Return to the portfolio to pick again.' }));
    view.appendChild(el('a', { class: 'ald-back', href: '#/', text: '← Back to portfolio' }));
  }

  function render() {
    var hash = window.location.hash.replace(/^#\/?/, '');
    var parts = hash.split('/').filter(Boolean);
    var view = el('div', { class: 'ald-view' });

    if (!parts.length || parts[0] === 'portfolio') viewPortfolio(view);
    else if (parts[0] === 'firm') viewFirm(view, parts[1]);
    else if (parts[0] === 'audit') viewAudit(view, parts[1]);
    else if (parts[0] === 'actions') viewActions(view);
    else viewPortfolio(view);

    var mountPoint = document.getElementById('ald-view');
    mountPoint.textContent = '';
    mountPoint.appendChild(view);
    if (!render._first) {
      var heading = view.querySelector('h2');
      if (heading) heading.focus();
      window.scrollTo({ top: mountPoint.getBoundingClientRect().top + window.pageYOffset - 90, behavior: 'auto' });
    }
    render._first = false;
  }
  render._first = true;

  window.addEventListener('hashchange', render);
  render();
})();
