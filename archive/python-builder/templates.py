"""
templates.py — plain-Python HTML rendering functions for the portfolio site.

No templating engine, no external dependency: every function takes plain
Python data (dicts/lists/strings) and returns an HTML string via f-strings.
build.py calls these to assemble each page; nothing here writes files.

Content schema (what content/*.py modules must provide) is documented
inline above each render_* function that consumes it.
"""

import json
import os

BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.dirname(BUILD_DIR)
ICONS_DIR = os.path.join(SITE_DIR, "assets", "icons")

FAVICON = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
    "%3Crect width='100' height='100' rx='20' fill='%231f374d'/%3E"
    "%3Ctext x='50' y='68' font-size='58' font-family='Arial' font-weight='bold' fill='white' "
    "text-anchor='middle'%3EFY%3C/text%3E%3C/svg%3E"
)

CSS_FILES = ["tokens", "base", "layout", "components", "charts", "case-study"]
JS_FILES = ["nav", "tooltip", "charts", "main"]

_icon_cache = {}


def icon(name, css_class=""):
    """Return the inlined SVG markup for assets/icons/{name}.svg."""
    if name not in _icon_cache:
        path = os.path.join(ICONS_DIR, f"{name}.svg")
        with open(path, encoding="utf-8") as f:
            content = f.read()
        idx = content.find("<svg")
        _icon_cache[name] = content[idx:]
    svg = _icon_cache[name]
    if css_class:
        svg = svg.replace("<svg", f'<svg class="{css_class}"', 1)
    return svg


def term(label, term_key):
    """An inline glossary-term trigger, e.g. term('p-value', 'p-value')."""
    return (
        f'<button type="button" class="term" data-term="{term_key}">'
        f"{label} {icon('info')}</button>"
    )


# ---------------------------------------------------------------- page shell --

def render_head(title, description, prefix):
    links = "\n".join(
        f'<link rel="stylesheet" href="{prefix}assets/css/{f}.css">' for f in CSS_FILES
    )
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
{links}
<link rel="icon" href="{FAVICON}">"""


def render_header(prefix):
    home = "index.html" if prefix == "" else f"{prefix}index.html"
    return f"""<header class="site-header">
  <div class="container nav">
    <a href="{home}" class="brand">
      <span class="brand-mark">FY</span>
      Farouk Yusuf
    </a>
    <button class="nav-toggle" aria-label="Toggle navigation"><span></span><span></span><span></span></button>
    <ul class="nav-links">
      <li><a href="{home}#case-studies">Case Studies</a></li>
      <li><a href="{home}#skills">Skills</a></li>
      <li><a href="{home}#about">About</a></li>
      <li><a href="{home}#contact" class="nav-cta">Contact</a></li>
    </ul>
  </div>
</header>"""


def render_footer(prefix, disclaimer_text, back_link=True):
    home = "index.html" if prefix == "" else f"{prefix}index.html"
    back = f'<p><a href="{home}">← Back to portfolio home</a></p>' if back_link else ""
    return f"""<footer class="site-footer">
  <div class="container">
    <p>© 2026 Farouk Yusuf. {disclaimer_text}</p>
    {back}
  </div>
</footer>"""


def render_scripts(prefix):
    return "\n".join(f'<script src="{prefix}assets/js/{f}.js"></script>' for f in JS_FILES)


def render_glossary_script(glossary):
    return f'<script type="application/json" id="glossary-data">{json.dumps(glossary)}</script>'


def render_disclaimer_strip(text):
    return f'<div class="disclaimer-strip">{text}</div>'


def wrap_page(head, body):
    return f"""<!doctype html>
<html lang="en">
<head>
{head}
</head>
<body>

{body}

</body>
</html>
"""


# ------------------------------------------------------------------- charts --
# chart config shape: {"id": "cN", "type": "bar|line|waterfall|comparison|histogram",
#                       "payload": {...matches charts.js render*() input...},
#                       "title": str|None, "caption": str}

def render_chart_block(chart, extra_class="", instance_suffix=""):
    """instance_suffix disambiguates the DOM/script id when the same chart config
    is deliberately shown twice on one page (e.g. a headline preview + a full
    section later) — without it, two instances would emit duplicate HTML ids."""
    data_id = f"{chart['id']}{instance_suffix}-data"
    head = f'<div class="chart-head"><span class="chart-title">{chart["title"]}</span></div>' if chart.get("title") else ""
    caption = f'<div class="chart-caption">{chart["caption"]}</div>' if chart.get("caption") else ""
    return f"""<div class="chart-block {extra_class}">
  {head}
  <div data-chart="{data_id}" data-chart-type="{chart['type']}"></div>
  <script type="application/json" id="{data_id}">{json.dumps(chart['payload'])}</script>
  {caption}
</div>"""


# --------------------------------------------------------------- homepage --
# card schema: {"industry": str, "title": str, "meta": str, "question": str,
#               "tags": [str, ...], "href": "case-studies/x.html"}

def render_card_top(label, inner=None):
    inner = inner or '<div class="chart">' + "".join('<span class="bar"></span>' for _ in range(5)) + "</div>"
    return f'<div class="card-top"><span class="mini-label">{label}</span>{inner}</div>'


def render_case_cards(cards):
    items = []
    for c in cards:
        tags = "".join(f'<span class="card-tag">{t}</span>' for t in c["tags"])
        items.append(f"""<article class="card">
        {render_card_top(c['industry'])}
        <h3>{c['title']}</h3>
        <div class="meta">{c['meta']}</div>
        <p class="question">{c['question']}</p>
        <div class="card-tags">{tags}</div>
        <a href="{c['href']}">View case study &rarr;</a>
      </article>""")
    return "".join(items)


# how-i-work schema: {"label", "big_text", "title", "meta", "body", "link_text", "href"}

def render_how_i_work_card(item):
    big_text_html = f'<div class="card-top-big">{item["big_text"]}</div>'
    return f"""<article class="card">
        {render_card_top(item['label'], big_text_html)}
        <h3>{item['title']}</h3>
        <div class="meta">{item['meta']}</div>
        <p class="question">{item['body']}</p>
        <a href="{item['href']}">{item['link_text']}</a>
      </article>"""


# profile-snapshot schema: {"count_label", "tools": [str,...], "industries": [str,...]}

def render_profile_card(snapshot, count):
    tools = "".join(f'<span class="pill">{t}</span>' for t in snapshot["tools"])
    sectors = "".join(f'<div class="sector">{s}</div>' for s in snapshot["industries"])
    return f"""<aside class="profile-card" id="skills">
      <h3>Portfolio snapshot</h3>
      <div class="number">{count}</div>
      <div class="tiny">{snapshot['count_label']}</div>
      <div class="tool-row">{tools}</div>
      <h3>Industries explored</h3>
      <div class="sector-list">{sectors}</div>
    </aside>"""


def render_contact_grid(contacts):
    items = []
    for c in contacts:
        items.append(f"""<div class="contact-card">
        <div class="contact-icon">{icon(c['icon'])}</div>
        <h3>{c['label']}</h3>
        <p>{c['value_html']}</p>
      </div>""")
    return f'<div class="contact-grid">\n      {"".join(items)}\n    </div>'


def render_about_list(items):
    lis = "".join(f"<li><strong>{i['label']}</strong><br>{i['value']}</li>" for i in items)
    return f'<ul class="about-list">{lis}</ul>'


# ----------------------------------------------------------- case-study page --
# kpi schema: {"num": str, "label": str, "tag": "significant"|"not_significant"|"caution"|None}

_TAG_LABELS = {
    "significant": "Statistically significant",
    "not_significant": "Not statistically significant",
    "caution": "Caution",
}


def render_kpi_grid(kpis):
    tiles = []
    for k in kpis:
        tag_html = ""
        if k.get("tag"):
            tag_html = f'<span class="tag tag-{k["tag"].replace("_", "-")}">{_TAG_LABELS[k["tag"]]}</span>'
        tiles.append(
            f'<div class="kpi-tile"><span class="kpi-num">{k["num"]}</span>'
            f'<span class="kpi-lbl">{k["label"]}</span>{tag_html}</div>'
        )
    return f'<div class="kpi-grid">{"".join(tiles)}</div>'


# finding schema: {"plain_headline": str, "plain_body": str, "figure_line": str|None,
#                   "technical_detail": str|None}

def render_finding_card(index, f):
    detail = ""
    if f.get("technical_detail"):
        detail = (
            f'<details class="detail"><summary>Show the statistical detail</summary>'
            f'<div class="detail-body">{f["technical_detail"]}</div></details>'
        )
    figure = f'<div class="figure-line">{f["figure_line"]}</div>' if f.get("figure_line") else ""
    return f"""<div class="finding-card">
      <span class="finding-num">FINDING {index}</span>
      <h4>{f['plain_headline']}</h4>
      <p>{f['plain_body']}</p>
      {figure}
      {detail}
    </div>"""


def render_findings(findings):
    return "\n".join(render_finding_card(i + 1, f) for i, f in enumerate(findings))


def render_short_version(paragraphs):
    ps = "".join(f"<p>{p}</p>" for p in paragraphs)
    return f"""<div class="short-version">
      <span class="eyebrow">The Short Version</span>
      {ps}
    </div>"""


def render_stakeholder_grid(items):
    cards = "".join(
        f'<div class="stakeholder-card"><strong>{i["role"]}</strong><span>{i["need"]}</span></div>'
        for i in items
    )
    return f'<div class="stakeholder-grid">{cards}</div>'


def render_static_table(headers, rows):
    thead = "".join(f"<th>{h}</th>" for h in headers)
    trs = []
    for row in rows:
        tds = "".join(
            f'<td{" class=\"num\"" if cell.get("num") else ""}>{cell["value"]}</td>'
            for cell in row
        )
        trs.append(f"<tr>{tds}</tr>")
    return f"""<table class="data-table">
      <thead><tr>{thead}</tr></thead>
      <tbody>{''.join(trs)}</tbody>
    </table>"""


def render_kv_table(rows):
    """rows: list of [{"value": label}, {"value": value, "num": bool?}] — renders
    <th>label</th><td>value</td> pairs, no header row (e.g. the dataset overview table)."""
    trs = []
    for label_cell, value_cell in rows:
        num_cls = ' class="num"' if value_cell.get("num") else ""
        trs.append(f"<tr><th>{label_cell['value']}</th><td{num_cls}>{value_cell['value']}</td></tr>")
    return f'<table class="data-table"><tbody>{"".join(trs)}</tbody></table>'


def render_tool_grid(tools):
    chips = "".join(
        f'<div class="tool-chip"><strong>{t["name"]}</strong><span>{t["desc"]}</span></div>'
        for t in tools
    )
    return f'<div class="tool-grid">{chips}</div>'


def render_rec_list(items):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f'<ol class="rec-list">{lis}</ol>'


def render_limit_list(items):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f'<ul class="limit-list">{lis}</ul>'


def render_tech_grid(cards):
    items = []
    for c in cards:
        lis = "".join(f"<li>{i}</li>" for i in c["items"])
        items.append(f'<div class="tech-card"><h4>{c["heading"]}</h4><ul>{lis}</ul></div>')
    return f'<div class="tech-grid">{"".join(items)}</div>'


def render_static_chart_figure(image):
    """A single static PNG chart-figure (for charts not yet wired to live data —
    e.g. pending a Python re-export). Same visual treatment as a chart-block."""
    return f"""<figure class="chart-figure">
    <img src="{image['src']}" alt="{image['alt']}">
    <figcaption>{image['caption']}</figcaption>
  </figure>"""


def render_chart_gallery(images):
    figs = []
    for im in images:
        figs.append(f"""<figure class="chart-figure">
        <img src="{im['src']}" alt="{im['alt']}">
        <figcaption>{im['caption']}</figcaption>
      </figure>""")
    return f'<div class="chart-gallery">{"".join(figs)}</div>'


def render_anchor_nav(items):
    links = "".join(f'<a href="#{i["id"]}">{i["label"]}</a>' for i in items)
    return f'<nav class="anchor-nav">{links}</nav>'
