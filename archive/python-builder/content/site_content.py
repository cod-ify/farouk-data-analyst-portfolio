"""Site-wide copy: homepage hero, skills, about, contact, footer, glossary."""

META = {
    "title": "Farouk Yusuf — Data & BI Analyst Portfolio",
    "description": (
        "Data Analyst | Business Intelligence | MI & Reporting | Data & Insights. Portfolio "
        "featuring the Hearthstead Housing Group, Arden Automotive Group, Westborough Council, "
        "AeroVista Travel Group and Albion General Insurance case studies."
    ),
}

DISCLAIMER_STRIP = "Portfolio projects use fictional organisations and synthetic datasets for demonstration purposes."

HERO = {
    "eyebrow": "Data Analyst Portfolio",
    "h1": "Hi, I&rsquo;m Farouk.",
    "role": "Data Analyst &middot; Business Intelligence &middot; MI &amp; Reporting &middot; Data &amp; Insights",
    "lead": (
        "I use data to spot problems early, uncover cost-saving opportunities and support "
        "better business decisions."
    ),
    "sublead": (
        "I&rsquo;ve built my skills in <strong>Excel, SQL, Power BI and Python</strong> "
        "through realistic business projects using synthetic data modelled around "
        "organisations across housing, automotive, government, travel and insurance."
    ),
}

NOTE = (
    "Hopefully, some of the problems I&rsquo;ve tackled look familiar to your business "
    "&mdash; and if yours isn&rsquo;t represented yet, forgive me, I&rsquo;m still building!"
)

PROFILE_SNAPSHOT = {
    "count_label": "end-to-end business case studies",
    "tools": ["Excel", "SQL", "Power BI", "Python"],
    "industries": ["Housing", "Automotive", "Local Government", "Travel", "Insurance", "Operations"],
}

HOW_I_WORK = {
    "label": "How I Work",
    "big_text": "Question &rarr; Data &rarr; Insight",
    "title": "My approach",
    "meta": "From messy data to useful decisions",
    "body": (
        "I focus on making comparisons fair, identifying what actually drives performance, "
        "and translating the result into something decision-makers can use."
    ),
    "link_text": "More about me &rarr;",
    "href": "#about",
}

ABOUT_PARAGRAPHS = [
    (
        "I'm a data analyst focused on management information, reporting and business "
        "intelligence — turning operational data into numbers that hold up to scrutiny. Each "
        "project on this site starts the same way: a realistic, deliberately messy dataset "
        "(duplicate records, missing links, inconsistent timestamps) is cleaned with a "
        "documented, repeatable process, then analysed four separate ways — Excel, SQL, Python "
        "and a Power BI design — with every headline number checked against the others."
    ),
    (
        "What I look for in any dataset: whether a comparison — between contractors, suppliers, "
        "regions or time periods — is actually fair once you account for what made some cases "
        "harder than others; whether a pattern is being read as a cause when it's really just an "
        "association; and whether a good-looking result deserves the same scrutiny as a bad one. "
        "In the Hearthstead project, that meant testing contractors' own complaint that the "
        "rankings were unfair (they turned out to hold up) and flagging a suspiciously perfect "
        "score for a second look rather than reporting it uncritically."
    ),
]

ABOUT_LIST = [
    {"label": "Focus areas", "value": "Data cleaning, clear KPIs, management reporting, dashboard design"},
    {"label": "Tools", "value": "Excel, SQL, Power BI, Python (pandas, statsmodels, matplotlib)"},
    {"label": "Statistical methods", "value": "Confidence intervals, significance testing, fair before/after comparisons, sensitivity checks"},
    {"label": "Working style", "value": "Check every number against every tool; keep pattern separate from proof; document what was excluded rather than quietly dropping it"},
]

CONTACT = [
    {"icon": "mail", "label": "Email", "value_html": '<a href="mailto:faroukyusuf.e@gmail.com">faroukyusuf.e@gmail.com</a>'},
    {"icon": "linkedin", "label": "LinkedIn", "value_html": '<a href="https://www.linkedin.com/in/farouk-yusuf-fy" target="_blank" rel="noopener">linkedin.com/in/farouk-yusuf-fy</a>'},
]

FOOTER_DISCLAIMER = (
    "Hearthstead Housing Group, Arden Automotive Group, Westborough Council, AeroVista Travel "
    "Group, Albion General Insurance and all other companies referenced on this site are fictional."
)

# Glossary — plain-English definitions for inline .term buttons, shared by every page.
GLOSSARY = {
    "p-value": (
        "A measure of how likely a result this size would happen by chance alone. Small "
        "(under 0.05) usually means the pattern is probably real; large means it could easily "
        "be random noise."
    ),
    "statistically significant": (
        "The difference is unlikely to be down to chance. “Not significant” doesn't mean "
        "“no difference” — it means the data can't rule out chance as the explanation."
    ),
    "case-mix adjustment": (
        "A fair way of comparing suppliers, regions or providers that accounts for how hard "
        "their jobs actually were, instead of just comparing raw averages."
    ),
    "r-squared": (
        "How much of the variation in an outcome a model explains, from 0 (none) to 1 (all of "
        "it). A low value means other, unmeasured factors matter too."
    ),
    "regression": (
        "A statistical method for estimating how one factor relates to an outcome while holding "
        "other factors constant — the main tool used here for fair before/after comparisons."
    ),
    "decomposition": (
        "Splitting a total change into its exact contributing parts (e.g. more cases happening "
        "vs. each case costing more), so they add up precisely to the real figure."
    ),
    "confidence interval": (
        "A range that's likely to contain the true value. A narrow range means a precise "
        "estimate; a wide one means more uncertainty."
    ),
    "reconciled": (
        "Checked and confirmed to match exactly across every tool used (Excel, SQL, Python) — "
        "no figure is reported unless it agrees everywhere it's calculated."
    ),
}
