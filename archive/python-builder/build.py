"""
build.py — orchestrator. Renders index.html and case-studies/*.html from
content/*.py + templates.py, and writes them to their live locations.

Run with:  python build.py   (from this build/ directory, or anywhere —
paths are resolved relative to this file).

Validates before writing: every icon file referenced exists, every gallery
image path resolves, and every case-study module exposes the expected
attributes — fails loudly rather than emitting silently-broken output.
"""

import os
import sys

BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.dirname(BUILD_DIR)
sys.path.insert(0, BUILD_DIR)
sys.path.insert(0, os.path.join(BUILD_DIR, "content"))

import templates as T  # noqa: E402
import site_content as SC  # noqa: E402

ICONS_DIR = os.path.join(SITE_DIR, "assets", "icons")

# Registered case-study content modules, in homepage display order.
CASE_STUDY_MODULES = ["hearthstead", "arden", "westborough", "aerovista", "albion"]


def _load_module(name):
    return __import__(name)


def validate_icon_exists(icon_name):
    path = os.path.join(ICONS_DIR, f"{icon_name}.svg")
    if not os.path.exists(path):
        raise SystemExit(f"BUILD ERROR: icon '{icon_name}.svg' not found at {path}")


def validate_image_exists(rel_path, from_dir):
    resolved = os.path.normpath(os.path.join(from_dir, rel_path))
    if not os.path.exists(resolved):
        raise SystemExit(f"BUILD ERROR: image not found: {rel_path} (resolved to {resolved})")


# ------------------------------------------------------------- case study --

def render_case_study_page(c):
    for skill in getattr(c, "REQUIRED_ICONS", []):
        validate_icon_exists(skill)

    charts = c.get_charts()
    if not charts:
        raise SystemExit(f"BUILD ERROR: {c.SLUG} produced no charts")

    prefix = c.NAV_PREFIX
    case_studies_dir = os.path.join(SITE_DIR, "case-studies")
    for img in c.GALLERY_IMAGES:
        validate_image_exists(img["src"], case_studies_dir)

    head = T.render_head(c.META["title"], c.META["description"], prefix)
    header = T.render_header(prefix)
    disclaimer_strip = T.render_disclaimer_strip(c.DISCLAIMER_STRIP)
    scripts = T.render_scripts(prefix)
    glossary_script = T.render_glossary_script(SC.GLOSSARY)
    footer = T.render_footer(prefix, c.FOOTER_DISCLAIMER)

    anchor_nav = T.render_anchor_nav(c.ANCHOR_NAV)
    hero = f"""<section class="cs-hero">
  <div class="container">
    <div class="cs-breadcrumb"><a href="{prefix}index.html">Home</a> / Case Studies / {c.HERO['breadcrumb_label']}</div>
    <span class="eyebrow">Case Study</span>
    <h1>{c.HERO['h1']}</h1>
    <p class="cs-sub">{c.HERO['sub']}</p>
    {anchor_nav}
  </div>
</section>"""

    disclaimer_box = f"""<div class="container">
  <div class="disclaimer-box">
    <span class="dot">i</span>
    <div>{c.DISCLAIMER_BOX}</div>
  </div>
</div>"""

    # Each project's body sections (findings through technical evidence) are
    # genuinely different in structure (e.g. only Albion has a "Reserve
    # Accuracy" section), so each content module builds its own via
    # render_sections(charts) using the templates.py toolkit directly.
    sections_html = c.render_sections(charts)

    body = f"""{disclaimer_strip}

{header}

{hero}

{disclaimer_box}

{sections_html}

{footer}

{glossary_script}
{scripts}"""

    return T.wrap_page(head, body)


# ------------------------------------------------------------------ homepage --

def render_index_page(cards):
    for contact in SC.CONTACT:
        validate_icon_exists(contact["icon"])

    prefix = ""
    head = T.render_head(SC.META["title"], SC.META["description"], prefix)
    header = T.render_header(prefix)
    disclaimer_strip = T.render_disclaimer_strip(SC.DISCLAIMER_STRIP)
    scripts = T.render_scripts(prefix)
    footer_content = f"""<footer class="site-footer">
  <div class="container">
    <p>© 2026 Farouk Yusuf</p>
    <p>{SC.FOOTER_DISCLAIMER}</p>
  </div>
</footer>"""

    hero = f"""<section class="hero">
  <div class="hero-inner">
    <div>
      <div class="eyebrow">{SC.HERO['eyebrow']}</div>
      <h1>{SC.HERO['h1']}</h1>
      <div class="role">{SC.HERO['role']}</div>
      <p class="lead">{SC.HERO['lead']}</p>
      <p class="sublead">{SC.HERO['sublead']}</p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="#case-studies">Explore case studies &rarr;</a>
        <a class="btn btn-secondary" href="#contact">Get in touch</a>
      </div>
    </div>
    {T.render_profile_card(SC.PROFILE_SNAPSHOT, len(cards))}
  </div>
</section>"""

    case_studies_section = f"""<section id="case-studies">
  <div class="container">
    <div class="section-head-row">
      <div>
        <div class="eyebrow">Selected work</div>
        <h2>Business problems, not just dashboards.</h2>
      </div>
      <p>Each project starts with a practical question, works through messy data, and ends with an analysis or recommendation someone could actually use.</p>
    </div>
    <div class="cards">
      {T.render_case_cards(cards)}
      {T.render_how_i_work_card(SC.HOW_I_WORK)}
    </div>
    <div class="note">{SC.NOTE}</div>
  </div>
</section>"""

    about_section = f"""<section id="about">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">About</span>
      <h2>About Me</h2>
    </div>
    <div class="about-grid">
      <div>
        {''.join(f'<p>{p}</p>' for p in SC.ABOUT_PARAGRAPHS)}
      </div>
      {T.render_about_list(SC.ABOUT_LIST)}
    </div>
  </div>
</section>"""

    contact_section = f"""<section id="contact" class="section-alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Get in Touch</span>
      <h2>Contact</h2>
      <p>Happy to talk through any of these projects in more detail, or discuss a role.</p>
    </div>
    {T.render_contact_grid(SC.CONTACT)}
  </div>
</section>"""

    body = f"""{disclaimer_strip}

{header}

{hero}

{case_studies_section}

{about_section}

{contact_section}

{footer_content}

{scripts}"""

    return T.wrap_page(head, body)


# ----------------------------------------------------------------------- main --

def main():
    modules = [_load_module(name) for name in CASE_STUDY_MODULES]

    for c in modules:
        html = render_case_study_page(c)
        out_path = os.path.join(SITE_DIR, "case-studies", f"{c.SLUG}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"wrote {out_path} ({len(html):,} bytes)")

    cards = [c.get_card() for c in modules]

    index_html = render_index_page(cards)
    index_path = os.path.join(SITE_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"wrote {index_path} ({len(index_html):,} bytes)")


if __name__ == "__main__":
    main()
