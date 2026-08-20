"""Hearthstead Housing Group — case-study content, in the plain-language schema."""

import charts_data
import templates as T
from templates import term

SLUG = "hearthstead"
NAV_PREFIX = "../"

META = {
    "title": "Hearthstead Housing Group Case Study — Farouk Yusuf",
    "description": (
        "Repairs performance & contractor intelligence case study: Excel, SQL, Python and Power "
        "BI analysis of a fictional housing association's repairs data, testing whether "
        "contractor performance differences survive a fair, case-mix-adjusted comparison."
    ),
}

DISCLAIMER_STRIP = (
    "Hearthstead Housing Group is fictional. All data on this page is synthetically generated "
    "for portfolio purposes — see the disclaimer below for detail."
)

DISCLAIMER_BOX = (
    "<strong>Synthetic-data disclaimer:</strong> Hearthstead Housing Group is a fictional "
    "housing association. Every property, repair, contractor, area and figure on this page was "
    "generated for data-analytics portfolio purposes — none of it describes a real housing "
    "association, and no figure should be read as representing an actual organisation. No "
    "individual tenant, resident or contractor operative is identified, ranked or scored anywhere "
    "in this project."
)

HERO = {
    "breadcrumb_label": "Hearthstead Housing Group",
    "h1": "Repairs Performance &amp; Contractor Intelligence",
    "sub": (
        "External contractors said their rankings were unfair because they get harder jobs than "
        "everyone else. Does that hold up once you account for it fairly? An end-to-end analysis "
        "across Excel, SQL, Python and Power BI on 26,000 repairs from a fictional housing "
        "association's two-year repairs book."
    ),
}

SHORT_VERSION = [
    (
        "Hearthstead is a made-up housing association, used here to practise a real analytics "
        "workflow end to end. Its external contractors pushed back on being ranked against each "
        "other, arguing they get harder jobs — but fairly adjusting for exactly that changes "
        "nothing: the ranking from best to worst contractor comes out <strong>identical</strong> "
        "either way."
    ),
    (
        "Along the way, the same analysis found that a worrying mid-2025 dip in service "
        "performance was really one contractor's four-month collapse, that one contractor's "
        "near-perfect score needs independent checking rather than celebrating uncritically, and "
        "that repeat/rework repairs — the thing everyone worried about — turn out to be only 3% "
        "of total cost."
    ),
]

ANCHOR_NAV = [
    {"id": "findings", "label": "Key Findings"},
    {"id": "problem", "label": "Business Problem"},
    {"id": "stakeholders", "label": "Stakeholders"},
    {"id": "dataset", "label": "Dataset"},
    {"id": "approach", "label": "Approach &amp; Tools"},
    {"id": "distributions", "label": "Why Medians, Not Averages"},
    {"id": "casemix", "label": "Contractor Case-Mix Analysis"},
    {"id": "ftf", "label": "First-Time Fix"},
    {"id": "apex", "label": "The Apex Episode"},
    {"id": "cost", "label": "Cost Concentration"},
    {"id": "recommendations", "label": "Recommendations"},
    {"id": "limitations", "label": "Limitations &amp; Debugging"},
    {"id": "technical", "label": "Technical Evidence"},
]

KPIS = [
    {"num": "0 of 6", "label": "Contractor rank changes after fairly adjusting for job difficulty", "tag": None},
    {"num": "-2.8pp", "label": "SLA compliance decline, 2024 → 2025 (excl. Dec-2025 boundary month)", "tag": "significant"},
    {"num": "63.6% → 29.4%", "label": "Apex Property Solutions' SLA compliance during its 4-month episode", "tag": None},
    {"num": "-11.0pp", "label": "Lower SLA compliance when a contractor misses an appointment", "tag": "significant"},
]

FINDINGS = [
    {
        "plain_headline": "Contractors said the rankings were unfair because they get harder jobs — the data says otherwise.",
        "plain_body": "Fairly re-scoring every contractor's performance for the exact mix of urgent jobs, trade types and areas it actually worked produces the same order from best to worst as the simple raw comparison. Their objection doesn't hold up.",
        "figure_line": "All 6 contractors keep the same rank after adjusting for job difficulty (e.g. Keystone 99.8% → 99.8% adjusted, Pinnacle 45.3% → 45.1% adjusted)",
        "technical_detail": f"Logistic regression of SLA compliance on contractor + priority + trade + operating area (n=20,657, pseudo-{term('R²', 'r-squared')}=0.183), used to directly standardise each contractor's predicted rate to the population-average job mix — this is the {term('case-mix adjustment', 'case-mix adjustment')} referenced throughout this page. Emergency-priority share alone ranges from 11.8% to 39.2% across contractors, so the mix genuinely differs; it just doesn't change who's strongest or weakest.",
    },
    {
        "plain_headline": "One contractor is the weakest performer on every single measure that matters, all at once.",
        "plain_body": "Pinnacle Repairs isn't just behind on one number — it has the lowest compliance rate, the lowest first-time-fix rate, the highest rate of missed appointments and the slowest average repair, simultaneously. That kind of consistency across four separate measures is much harder to explain away than one bad number.",
        "figure_line": "Pinnacle Repairs: 45.3% SLA compliance &middot; 62.0% first-time-fix rate (vs 68.8%-77.2% for peers) &middot; 15.0% missed appointments (2-4x every other contractor) &middot; 11.3-day median completion",
        "technical_detail": f"Lowest on both raw (45.3%) and {term('case-mix adjusted', 'case-mix adjustment')} (45.1%) SLA compliance of all six external contractors — the weak position is not an artefact of an easier or harder caseload.",
    },
    {
        "plain_headline": "A worrying portfolio-wide dip turned out to be one contractor's four-month collapse.",
        "plain_body": "When overall compliance dropped noticeably for four months in a row, it looked like a general service problem. Breaking it down by contractor showed almost the entire dip came from a single contractor going badly wrong for exactly those four months — everyone else stayed close to normal.",
        "figure_line": "Apex Property Solutions: 63.6% full-period average &rarr; 29.4% during July-October 2025 &middot; every other contractor moved by only a few points over the same window (e.g. Keystone 99.8% &rarr; 100.0%, Orion 88.7% &rarr; 88.1%)",
        "technical_detail": None,
    },
    {
        "plain_headline": "Performance really did get worse year over year — not by a huge amount, but it's real.",
        "plain_body": "Comparing 2024 to 2025 (excluding the final month, which is skewed by an unrelated data cut-off issue — see the next finding), compliance fell by about three points. That's a small but genuine decline, not just noise in the numbers — and most of it traces back to the one contractor's episode above.",
        "figure_line": "SLA compliance: 73.7% (2024) &rarr; 70.9% (2025, excl. December) — a 2.79 percentage-point fall",
        "technical_detail": f"Two-proportion z-test on SLA compliance, 2024 vs 2025 excluding December 2025: z=4.931, {term('p&lt;0.001', 'p-value')} ({term('statistically significant', 'statistically significant')}).",
    },
    {
        "plain_headline": "One month looked like a service collapse — it was actually just how the data was cut off, not a real problem.",
        "plain_body": "First-time-fix performance appeared to crash in the dataset's final month. Looking closer, almost every repair in the whole two-year dataset that was still open (not yet finished) happened to fall in that exact month — because the data was extracted right then, before those jobs had a fair chance to finish. Compliance in that same month, measured a different way, was completely normal.",
        "figure_line": "346 of the whole dataset's 348 open (not-yet-completed) repairs fall in December 2025 &middot; that month's own SLA compliance was a normal 73.4%",
        "technical_detail": "Consistent with right-censoring: repairs reported late in the extraction window haven't had time to reach an appointment or completion. All year-on-year comparisons on this page are shown excluding December 2025 for this reason.",
    },
    {
        "plain_headline": "One contractor's near-perfect score is being flagged for a second look, not celebrated as a top performer.",
        "plain_body": "Keystone Maintenance Ltd's compliance rate is far above every other contractor and well above the in-house teams used as an internal benchmark — even after fairly adjusting for job difficulty. A result this close to perfect, isolated to one provider, deserves independent verification against the source system before anyone relies on it operationally.",
        "figure_line": "Keystone: 99.8% SLA compliance vs 56.0%-88.7% for the other five contractors and 73.8% for internal teams &middot; unchanged after adjusting for job difficulty",
        "technical_detail": None,
    },
    {
        "plain_headline": "When a contractor misses a scheduled appointment, the whole job is more likely to go wrong.",
        "plain_body": "Repairs with at least one missed appointment are noticeably less likely to meet their target and take longer to finish. This pattern holds up even after accounting for how urgent the job was and what type of work it involved — though it remains an association, not proof that the missed appointment itself caused the problem.",
        "figure_line": "62.3% SLA compliance with a missed appointment vs 73.3% without it (an 11.0-point gap) &middot; 23.6 vs 20.8 days at the 90th percentile for completion time",
        "technical_detail": f"Logistic regression: repairs with &ge;1 missed appointment have roughly 40% lower odds of meeting SLA after adjusting for priority and trade (adjusted odds ratio 0.599, 95% {term('CI', 'confidence interval')} 0.544-0.660, {term('p&lt;0.001', 'p-value')}). A non-parametric bootstrap on the raw gap gives a 95% {term('CI', 'confidence interval')} of 8.6-13.2 points, which does not cross zero.",
    },
    {
        "plain_headline": "Repeat repairs aren't the big cost problem people assumed — a handful of repair types are.",
        "plain_body": "Reworked or repeated jobs make up a tiny slice of total spend. The real cost is concentrated in a small number of repair categories — roof leaks, boiler breakdowns, no hot water and no heating — which together account for a disproportionate share of everything spent on repairs.",
        "figure_line": "Follow-on/rework cost: £121,080, just 3.0% of total direct cost &middot; Roof Leak, Boiler Breakdown, No Hot Water &amp; No Heating: 40.3% of total cost from a much smaller share of jobs",
        "technical_detail": None,
    },
]

PROBLEM_PARAGRAPHS = [
    (
        "Hearthstead is a fictional UK housing association whose Executive Director of "
        "Operations and Head of Repairs were concerned that repairs costs might be rising, "
        "service performance might be slipping, some contractors might be underperforming, and "
        "repeat repairs might be creating avoidable cost. External contractors pushed back on "
        "simple headline rankings, arguing they receive different volumes, priorities, "
        "geographies and job complexity — so any comparison needed to account for that before it "
        "could be trusted."
    ),
    (
        "One rule was non-negotiable: <strong>no contractor comparison could be presented as a "
        "simple ranking</strong> without first checking whether it still held up once job "
        "difficulty was taken into account."
    ),
]

STAKEHOLDERS = [
    {"role": "Executive Director of Operations", "need": "Needed to know whether repairs performance had genuinely declined, and where repair cost concentrates, to prioritise where to intervene."},
    {"role": "Head of Repairs", "need": "Needed to know which contractors underperform, what drives SLA failures and long completion times, and how much missed appointments matter."},
    {"role": "Contractor &amp; Supplier Management", "need": "Needed a fair, defensible basis for contractor performance conversations that accounts for job-mix differences, since contractors had directly disputed raw rankings."},
    {"role": "Finance &amp; Repairs Operations", "need": "Needed to know whether repeat/rework repairs were driving avoidable cost, or whether cost concentrated somewhere else entirely."},
]

DATASET_ROWS = [
    [{"value": "Coverage"}, {"value": "4,000 properties, 6 external contractors, 4 internal maintenance teams, 6 operating areas, 24 repair categories"}],
    [{"value": "Period"}, {"value": "January 2024 – December 2025 (24 months)"}],
    [{"value": "Properties"}, {"value": "4,000", "num": True}],
    [{"value": "Repairs"}, {"value": "26,000 (26,078 raw rows; 78 duplicate records were found and removed during cleaning)", "num": True}],
    [{"value": "Appointments"}, {"value": "33,460", "num": True}],
    [{"value": "Repair relationships (repeat/rework links)"}, {"value": "1,528", "num": True}],
    [{"value": "Cost events"}, {"value": "53,270, reconciling to £4,020,286.81 total net cost", "num": True}],
    [{"value": "Open (not-yet-completed) repairs at extraction"}, {"value": "348 (346 of which fall in the final month — see Finding 5)", "num": True}],
]

TOOLS = [
    {"name": "Excel", "desc": "A 33-sheet workbook (10 visible, 23 supporting) where every KPI is a live formula or PivotTable over the processed data — not a pasted-in report."},
    {"name": "SQL", "desc": "Six portable, CTE/window-function-based queries covering KPIs, contractor performance, repeat repairs, appointments, costs and root causes — validated against a SQLite load of the same processed data."},
    {"name": "Python", "desc": "The statistical validation stage: a logistic regression to fairly adjust contractor performance for job mix, Wilson-score confidence intervals, a two-proportion significance test, a bootstrap cross-check and multiple sensitivity checks."},
    {"name": "Power BI", "desc": "A full dashboard build specification — the data model, DAX measure library and page layouts — ready to build, not yet a live workspace."},
]

CASEMIX_ROWS = [
    [{"value": "Keystone Maintenance Ltd"}, {"value": "99.78%"}, {"value": "99.78%"}, {"value": "1 / 1"}],
    [{"value": "Orion Facilities"}, {"value": "88.69%"}, {"value": "88.59%"}, {"value": "2 / 2"}],
    [{"value": "Vertex Property Care"}, {"value": "74.59%"}, {"value": "74.47%"}, {"value": "3 / 3"}],
    [{"value": "Apex Property Solutions"}, {"value": "63.56%"}, {"value": "63.37%"}, {"value": "4 / 4"}],
    [{"value": "Nexus Building Services"}, {"value": "56.03%"}, {"value": "57.22%"}, {"value": "5 / 5"}],
    [{"value": "Pinnacle Repairs"}, {"value": "45.26%"}, {"value": "45.09%"}, {"value": "6 / 6"}],
]

RECOMMENDATIONS = [
    "<strong>Open a specific, time-bounded conversation with Apex Property Solutions about July–October 2025.</strong> This isolated four-month episode is a far more tractable issue than a vague “did performance decline” question, and likely has a concrete operational cause worth asking about directly.",
    "<strong>Escalate Pinnacle Repairs for contract review</strong>, on the basis of consistent underperformance across four independent measures that survives fairly adjusting for job difficulty — the weak position is not an artefact of a harder caseload.",
    "<strong>Verify Keystone Maintenance Ltd's reported SLA compliance against source system data before relying on it operationally.</strong> A 99.8% result should be confirmed, not simply celebrated, before it's used in supplier scorecards or contract renewals.",
    "<strong>Investigate missed-appointment root causes as a service-wide lever</strong>, not a single-contractor issue — a process-level fix such as scheduling or access coordination could plausibly benefit every contractor simultaneously.",
    "<strong>Prioritise category-level cost review over broad cost-cutting.</strong> Roof Leak and Boiler Breakdown alone justify a targeted process/procurement review given their disproportionate share of the £4.02m cost base, whereas rework reduction has limited headroom (already only 3.0% of direct cost).",
]

LIMITATIONS_DEBUG = [
    "<strong>An early version of the repair-cost data looked completely broken — the vast majority of cost rows contained garbled text instead of numbers.</strong> The root cause turned out to be a lookup keyed on trade rather than repair category: several repair categories share the same trade (e.g. four different categories are all classed as “Heating”), so the lookup returned multiple rows instead of one clean number. Re-keying the lookup on the always-unique repair category fixed it — zero non-numeric rows remained afterwards.",
    "<strong>First-time-fix performance appeared to collapse in the dataset's final month.</strong> Rather than reporting it as a real service collapse, the near-total overlap with the dataset's still-open repairs prompted a cross-check against a different metric (SLA compliance) for that same month — which came back completely normal, confirming the apparent collapse was a data cut-off artefact, not a genuine deterioration.",
]

LIMITATIONS_STANDARD = [
    "<strong>Made-up data throughout</strong> — every figure describes patterns in a generated dataset built for this portfolio, not a real housing association.",
    "<strong>Association, not proof of cause</strong> — the missed-appointment link to lower SLA compliance is adjusted for priority and trade, but doesn't prove a missed appointment directly causes the shortfall; repairs that are already complex may simply be more likely to have both a missed appointment and a longer job.",
    "<strong>Keystone Maintenance Ltd's anomalous result is flagged, not resolved</strong> — this analysis does not determine whether it reflects genuine performance, a data-generation artefact, or something else.",
    "<strong>The December 2025 boundary effect could only be identified and excluded, not corrected</strong> — a live operational dataset without a fixed extraction date would not have this issue.",
    "<strong>39 repairs with no valid property link and 26 repairs with an implausible timestamp</strong> are correctly excluded from the relevant measures rather than guessed at — a small amount of information that could not be used.",
    "<strong>A “deliberately multi-stage” repair flag currently mirrors a separate “planned follow-on” flag</strong>, with no independent source signal yet distinguishing them — the two concepts can't be told apart in this version of the data.",
]

TECH_CARDS = [
    {"heading": "03_excel/", "items": ["build_excel_workbook.py — reproducible build script", "hearthstead_repairs_analysis.xlsx — 10 visible sheets (33 total), 13 charts, 3 PivotTables"]},
    {"heading": "04_sql/", "items": ["01_kpi_analysis.sql &middot; 02_contractor_analysis.sql", "03_repeat_repairs.sql &middot; 04_appointments.sql", "05_cost_analysis.sql &middot; 06_root_cause_analysis.sql"]},
    {"heading": "07_python/", "items": ["hearthstead_repairs_analysis.py — full analysis script", "hearthstead_repairs_analysis.ipynb — narrated notebook", "results/hearthstead_results.json — machine-readable results"]},
    {"heading": "05_power_bi/documentation/", "items": ["dashboard_specification.md — dashboard design", "dax_measures.md — full DAX measure library", "data_model.md — data model design"]},
]

# No standalone gallery: all six source charts now have a dedicated home in the
# narrative sections below (distribution shape, case-mix, first-time fix, the
# Apex episode and cost concentration), so a separate leftover-images gallery
# would just duplicate content shown elsewhere on the page.
GALLERY_IMAGES = []

FOOTER_DISCLAIMER = "Hearthstead Housing Group is fictional; all data is synthetic."


def _load():
    return charts_data.load_results(
        "hearthstead_housing_group/projects/01_repairs_contractor_intelligence/07_python/results/hearthstead_results.json"
    )


def get_charts():
    s = _load()
    charts = {}

    contractors = s["contractor_case_mix_adjustment"]["comparison_table"]
    charts["c1"] = {
        "id": "c1", "type": "comparison",
        "title": "Raw vs case-mix-adjusted SLA compliance by contractor",
        "caption": "Adjusting each contractor's compliance rate for the exact mix of priority, trade and area it actually worked (case-mix adjustment) produces the same 1-through-6 ranking as the simple raw comparison — the contractors' objection that raw rankings are unfair doesn't hold up.",
        "payload": {
            "rows": [
                {
                    "label": r["provider_name"], "before": round(r["raw_sla_rate"] * 100, 2), "after": round(r["adjusted_sla_rate"] * 100, 2),
                    "meta": {"n": r["n"], "rank_change": r["rank_change"]},
                }
                for r in contractors
            ],
            "options": {
                "valueFormat": "percent", "beforeLabel": "Raw SLA rate", "afterLabel": "Case-mix adjusted",
                "categoryLabel": "Contractor",
                "metaColumns": [
                    {"key": "n", "label": "Repairs", "numeric": True, "format": "number"},
                    {"key": "rank_change", "label": "Rank change", "numeric": True, "format": "number"},
                ],
            },
        },
    }

    kpis = s["headline_kpis"]
    charts["c2"] = {
        "id": "c2", "type": "bar",
        "title": "Operational vs Verified First-Time Fix rate",
        "caption": "The gap between the two definitions is small — only 158 repairs, 0.6 percentage points — confirming that confirmed repeat/rework repairs are not a large driver of apparent first-time-fix performance.",
        "payload": {
            "categories": ["Operational (self-reported)", "Verified (independently checked)"],
            "series": [
                {"label": "First-time fix rate", "values": [round(kpis["operational_ftf"]["rate"] * 100, 2), round(kpis["verified_ftf"]["rate"] * 100, 2)]},
            ],
            "options": {"valueFormat": "percent", "categoryLabel": "Definition"},
        },
    }

    eda = s["eda"]
    cdd = s["completion_days_distribution"]
    charts["c3"] = {
        "id": "c3", "type": "histogram",
        "title": "Repair completion time is right-skewed",
        "caption": f"Mean completion time ({eda['completion_days_mean']} days) sits well above the median ({eda['completion_days_median']} days) — most repairs finish quickly, with a long tail of slower ones, which is why this analysis uses medians and percentiles rather than the mean.",
        "payload": {
            "binEdges": cdd["bin_edges"],
            "counts": cdd["counts"],
            "options": {"valueFormat": "days", "meanLine": eda["completion_days_mean"], "medianLine": eda["completion_days_median"]},
        },
    }

    ncd = s["net_cost_distribution"]
    charts["c4"] = {
        "id": "c4", "type": "histogram",
        "title": "Repair cost is right-skewed",
        "caption": f"Mean cost (£{eda['net_cost_mean']}) sits well above the median (£{eda['net_cost_median']}) — most repairs are modest, with a long tail of expensive ones. Distribution clipped at £1,000 for readability; a small number of larger repairs extend beyond this.",
        "payload": {
            "binEdges": ncd["bin_edges"],
            "counts": ncd["counts"],
            "options": {"valueFormat": "gbp", "meanLine": eda["net_cost_mean"], "medianLine": eda["net_cost_median"]},
        },
    }

    monthly = s["monthly_trend"]
    charts["c5"] = {
        "id": "c5", "type": "line",
        "title": "Monthly SLA compliance and Operational First-Time Fix, 2024-2025",
        "caption": "SLA compliance sits in a steady 70%-75% band for almost the whole two years, with one clear four-month dip from July to October 2025 — traced in the Apex Episode section below to a single contractor, not a general decline.",
        "payload": {
            "xLabels": [charts_data.month_label(m["month"]) for m in monthly],
            "series": [
                {"label": "SLA compliance", "values": [round(m["sla_rate"] * 100, 2) for m in monthly], "valueFormat": "percent"},
                {"label": "Operational FTF", "values": [round(m["op_ftf_rate"] * 100, 2) for m in monthly], "valueFormat": "percent"},
            ],
            "options": {"annotations": [{"x": "Jul 2025", "label": "Apex episode begins"}]},
        },
    }

    pareto = s["cost_pareto_by_category"]
    charts["c6"] = {
        "id": "c6", "type": "bar",
        "title": "Net repair cost by category",
        "caption": "The top 4 of 24 repair categories (Roof Leak, Boiler Breakdown, No Hot Water, No Heating) already account for 40.3% of total net operational cost — hover any bar for its exact cumulative share.",
        "payload": {
            "categories": [r["category"] for r in pareto],
            "series": [{"label": "Net cost", "values": [round(r["net_cost"], 2) for r in pareto]}],
            "options": {"horizontal": True, "valueFormat": "gbp", "categoryLabel": "Repair category"},
        },
    }

    return charts


def render_sections(charts):
    findings_section = f"""<section id="findings" style="padding-top:0;">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">At a Glance</span>
      <h2>Headline Numbers</h2>
      <p>Every figure below is {term('reconciled', 'reconciled')} exactly across the Excel workbook, every SQL script and the Python notebook.</p>
    </div>
    {T.render_short_version(SHORT_VERSION)}
    {T.render_kpi_grid(KPIS)}
    <div class="two-col" style="margin-top:32px;">
      {T.render_chart_block(charts['c1'])}
      {T.render_chart_block(charts['c5'])}
    </div>
    <h3 style="margin-top:8px;">Eight strongest findings</h3>
    {T.render_findings(FINDINGS)}
  </div>
</section>"""

    problem_section = f"""<section id="problem" class="section-alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">1. Business Problem</span>
      <h2>What management wanted answered</h2>
    </div>
    {''.join(f'<p>{p}</p>' for p in PROBLEM_PARAGRAPHS)}
  </div>
</section>"""

    stakeholders_section = f"""<section id="stakeholders">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">2. Stakeholders &amp; Business Decision</span>
      <h2>Who this was for, and what they needed to decide</h2>
    </div>
    {T.render_stakeholder_grid(STAKEHOLDERS)}
  </div>
</section>"""

    dataset_section = f"""<section id="dataset" class="section-alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">3. Dataset Overview</span>
      <h2>What the data covers</h2>
    </div>
    {T.render_kv_table(DATASET_ROWS)}
  </div>
</section>"""

    approach_section = f"""<section id="approach">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">4. Analytical Approach &amp; Tools Used</span>
      <h2>Four tools, one reconciled set of numbers</h2>
      <p>Each tool answers a different part of the brief, but every headline number reconciles exactly across all of them.</p>
    </div>
    {T.render_tool_grid(TOOLS)}
  </div>
</section>"""

    distributions_section = f"""<section id="distributions" class="section-alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">5. Why This Analysis Uses Medians, Not Averages</span>
      <h2>Completion time and cost both have a long tail</h2>
      <p>Both distributions are right-skewed — a small share of repairs take much longer or cost much more than the typical case — so a simple average is misleading on its own. That's why medians and percentiles are used throughout this page.</p>
    </div>
    <div class="two-col">
      {T.render_chart_block(charts['c3'])}
      {T.render_chart_block(charts['c4'])}
    </div>
  </div>
</section>"""

    casemix_section = f"""<section id="casemix">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">6. Contractor {term('Case-Mix', 'case-mix adjustment')} Analysis</span>
      <h2>Testing the contractors' own objection, using their data</h2>
      <p>The interactive chart above (Headline Numbers) shows the raw vs adjusted comparison directly. The table below spells out exactly what changed — and what didn't.</p>
    </div>
    {T.render_static_table(["Contractor", "Raw SLA rate", "Case-mix-adjusted rate", "Rank (raw / adjusted)"], CASEMIX_ROWS)}
  </div>
</section>"""

    ftf_section = f"""<section id="ftf" class="section-alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">7. Operational vs Verified First-Time Fix</span>
      <h2>Does confirmed rework change the first-time-fix picture?</h2>
    </div>
    {T.render_chart_block(charts['c2'])}
  </div>
</section>"""

    apex_section = f"""<section id="apex">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">8. The Apex Episode</span>
      <h2>Finding the one contractor behind a portfolio-wide dip</h2>
      <p>The monthly trend chart above (Headline Numbers) shows the dip itself. Portfolio SLA compliance fell sharply for four consecutive months, July-October 2025 (65.4%-68.1%, against a 70%-75% band in every other month) — breaking it down by contractor shows this is very largely one contractor's episode, not a general deterioration.</p>
    </div>
    {T.render_static_chart_figure({
        "src": "../assets/images/hearthstead/06_apex_july_october_2025_episode.png",
        "alt": "Bar chart comparing each provider's full-period SLA compliance to its July-October 2025 rate",
        "caption": "Every provider except Apex Property Solutions stayed within a few points of its own full-period average across July-October 2025 (e.g. Keystone 99.8% → 100.0%, Orion 88.7% → 88.1%). Apex alone collapsed from a 63.6% full-period average to 29.4% during exactly those four months.",
    })}
  </div>
</section>"""

    cost_section = f"""<section id="cost" class="section-alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">9. Cost Concentration</span>
      <h2>Where the £4.02m actually goes</h2>
    </div>
    {T.render_chart_block(charts['c6'])}
  </div>
</section>"""

    recommendations_section = f"""<section id="recommendations">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">10. Management Recommendations</span>
      <h2>What follows from the evidence</h2>
    </div>
    {T.render_rec_list(RECOMMENDATIONS)}
  </div>
</section>"""

    limitations_section = f"""<section id="limitations" class="section-alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">11. Limitations &amp; Debugging Lessons</span>
      <h2>What this analysis does not claim — and two things caught before they shipped</h2>
    </div>
    {T.render_limit_list(LIMITATIONS_DEBUG)}
    {T.render_limit_list(LIMITATIONS_STANDARD)}
  </div>
</section>"""

    technical_section = f"""<section id="technical">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">12. Technical Evidence</span>
      <h2>Source deliverables</h2>
      <p>Source files for this project are organised as shown below (not yet published to a public GitHub repository). Every deliverable reconciles to the same figures shown on this page.</p>
    </div>
    {T.render_tech_grid(TECH_CARDS)}
    <p class="tech-note">See also: <code>08_outputs/executive_summary/</code> for the full written analysis and <code>09_case_study/portfolio_case_study.md</code> for the source of this page.</p>
  </div>
</section>"""

    return "\n".join([
        findings_section, problem_section, stakeholders_section, dataset_section,
        approach_section, distributions_section, casemix_section, ftf_section, apex_section,
        cost_section, recommendations_section, limitations_section, technical_section,
    ])


def get_card():
    return {
        "industry": "Housing",
        "title": "Hearthstead Housing Group",
        "meta": "Contractor performance analysis",
        "question": "Are contractors genuinely underperforming, or are some simply receiving harder jobs?",
        "tags": ["SQL", "Power BI", "Excel"],
        "href": "case-studies/hearthstead.html",
    }
