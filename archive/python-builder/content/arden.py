"""Arden Automotive Group — case-study content, in the plain-language schema."""

import charts_data
import templates as T
from templates import term

SLUG = "arden"
NAV_PREFIX = "../"

META = {
    "title": "Arden Automotive Group Case Study — Farouk Yusuf",
    "description": (
        "Supplier reliability, inventory risk & freight-cost analytics case study: Excel, SQL, "
        "Python and Power BI analysis of a fictional premium vehicle manufacturer's component "
        "supply chain, supplier fairness and shortage root causes."
    ),
}

DISCLAIMER_STRIP = (
    "Arden Automotive Group is fictional. All data on this page is synthetically generated for "
    "portfolio purposes — see the disclaimer below for detail."
)

DISCLAIMER_BOX = (
    "<strong>Synthetic-data disclaimer:</strong> Arden Automotive Group is a fictional vehicle "
    "manufacturer. Every supplier, component, purchase order, plant and figure on this page was "
    "generated for data-analytics portfolio purposes — none of it describes a real manufacturer "
    "or supplier, and no figure should be read as representing an actual business. No individual "
    "is identified, ranked or scored anywhere in this project."
)

HERO = {
    "breadcrumb_label": "Arden Automotive Group",
    "h1": "Global Parts Supply &amp; Production Risk Intelligence",
    "sub": (
        "Are Arden's worst-performing suppliers actually unreliable — or are they just stuck "
        "with harder parts to deliver? An end-to-end analysis across Excel, SQL, Python and "
        "Power BI on 14,403 purchase orders from a fictional premium vehicle manufacturer's "
        "two-year, 30-supplier component supply chain."
    ),
}

SHORT_VERSION = [
    (
        "Arden is a made-up premium UK vehicle manufacturer, used here to practise a real "
        "supply-chain analytics workflow end to end. Its two worst-performing suppliers stay "
        "its two worst-performing suppliers even after fairly adjusting for how hard the parts "
        "they supply actually are — their poor delivery record is real, not an artefact of a "
        "tough job."
    ),
    (
        "Along the way, the same analysis found a supplier whose sudden five-month slump turned "
        "out to be an isolated, fixable episode rather than a trend, confirmed that on-time "
        "delivery barely moved across the whole network year on year, and found that rushed "
        "shipping costs three and a half times more than standard freight while eating over half "
        "the freight budget — despite being only a quarter of all shipments."
    ),
]

ANCHOR_NAV = [
    {"id": "findings", "label": "Key Findings"},
    {"id": "problem", "label": "Business Problem"},
    {"id": "stakeholders", "label": "Stakeholders"},
    {"id": "dataset", "label": "Dataset"},
    {"id": "approach", "label": "Approach &amp; Tools"},
    {"id": "casemix", "label": "Supplier Case-Mix Analysis"},
    {"id": "shortages", "label": "Shortage Root Causes"},
    {"id": "freight", "label": "Freight Cost Concentration"},
    {"id": "recommendations", "label": "Recommendations"},
    {"id": "limitations", "label": "Limitations &amp; Debugging"},
    {"id": "gallery", "label": "More Charts"},
    {"id": "technical", "label": "Technical Evidence"},
]

KPIS = [
    {"num": "70.3%", "label": "Overall on-time-in-full (OTIF) delivery rate, across 14,383 orders", "tag": None},
    {"num": "69.9% &rarr; 70.8%", "label": "Network-wide OTIF, 2024 &rarr; 2025", "tag": "not_significant"},
    {"num": "3.56x", "label": "Cost premium for expedited vs standard freight shipments", "tag": None},
    {"num": "92.4%", "label": "Of shortage events caused by supplier or logistics delay, not demand swings", "tag": None},
]

FINDINGS = [
    {
        "plain_headline": "The two suppliers with the worst delivery records stay the worst — even after fairly accounting for how hard their parts are to supply.",
        "plain_body": "Some suppliers' rankings do shift a lot once you account for job difficulty — one moves by seven places. But the two suppliers with the worst on-time-in-full delivery records, Cliffgate Logistics Components and Kestrel Precision Components, are still the two worst performers after that adjustment. Their poor delivery record is real, not an excuse.",
        "figure_line": "Cliffgate: 46.8% raw OTIF &middot; Kestrel: 49.2% raw OTIF &middot; Gap vs. the rest of the network stays at roughly 25 percentage points even after adjustment",
        "technical_detail": f"Logistic {term('regression', 'regression')} of OTIF on supplier + criticality tier + commodity group (pseudo {term('R&sup2;', 'r-squared')}=0.10, n=14,383) — this is the {term('case-mix adjustment', 'case-mix adjustment')} referenced throughout this page. Bootstrap 95% {term('CI', 'confidence interval')} on the OTIF gap between the two worst suppliers and the rest of the network: 23.2&ndash;27.7 percentage points (2,000 resamples; excludes zero, i.e. the gap is real).",
    },
    {
        "plain_headline": "One of those two, Kestrel Precision Components, does supply genuinely harder parts — but that alone doesn't explain its poor record.",
        "plain_body": "Kestrel's components are the hardest mix of any major supplier — nearly three-quarters are rated Critical or High criticality, roughly double the network average. If a hard job were the whole story, adjusting for it should make Kestrel look meaningfully better. It barely moves.",
        "figure_line": "72.9% of Kestrel's parts are Critical/High criticality vs. 36.3% network average &middot; Adjusted OTIF: 49.2% raw &rarr; 47.4% adjusted (slightly worse, not better)",
        "technical_detail": f"Kestrel's {term('case-mix adjustment', 'case-mix adjustment')}-adjusted OTIF (47.4%) is not meaningfully better than its raw rate (49.2%) — its adjusted rank actually falls slightly, from 29th to 28th of 30 — confirming its harder parts mix does not explain its performance.",
    },
    {
        "plain_headline": "Another supplier, Solmar Fasteners Ltd, has an easy parts mix — and performs just as poorly.",
        "plain_body": "Solmar's components lean toward the easier end of the difficulty scale, not the harder end. Yet its on-time-in-full record is nearly identical to Kestrel's, and adjusting for job difficulty doesn't help it either — this is the cleanest example in the whole dataset of a supplier whose weak record can't be blamed on what it was asked to supply.",
        "figure_line": "50.9% raw OTIF across 900 orders &middot; 67.5% of Solmar's parts are Medium/Low criticality — an easier-than-average mix &middot; Adjusted OTIF falls slightly, to 47.9%",
        "technical_detail": None,
    },
    {
        "plain_headline": "One supplier's reliability collapsed suddenly for five months — but it looks like a one-off, not a trend.",
        "plain_body": "Ashcombe Precision delivered normally for most of the two-year period, then its on-time-in-full rate fell off a cliff for five months running, right at the end of the data. That kind of sudden, isolated drop is usually more fixable than a slow, structural decline — it points to a specific, recent problem worth a direct conversation.",
        "figure_line": "Normal range: roughly 60%&ndash;90% OTIF most months &middot; Aug&ndash;Dec 2025: 21.4%, 36.4%, 20.0%, 30.0%, 40.0%",
        "technical_detail": None,
    },
    {
        "plain_headline": "Across the whole network, on-time delivery barely changed year on year — despite Ashcombe's collapse.",
        "plain_body": "Zoom out from any one supplier, and the network's overall on-time-in-full rate was essentially flat between 2024 and 2025. A formal check confirms the small change is easily explained by chance, not a real network-wide trend — concern about “declining performance” belongs at the supplier level, not the portfolio level.",
        "figure_line": "69.9% (2024) &rarr; 70.8% (2025) &middot; 14,383 OTIF-eligible orders",
        "technical_detail": f"Two-proportion z-test on network-wide OTIF, 2024 vs. 2025: z=&minus;1.214, {term('p=0.225', 'p-value')} ({term('not significant', 'statistically significant')}).",
    },
    {
        "plain_headline": "Rushed shipping costs three and a half times more than standard shipping — and eats over half the freight budget.",
        "plain_body": "When a part has to be shipped by air to catch up on a late delivery, it costs far more than shipping it the normal way. These rushed shipments are a minority of all shipments, but they're eating the majority of the money spent on freight.",
        "figure_line": "Average expedited shipment: £616.66 vs. standard: £173.04 (3.56x) &middot; 26.0% of shipments were expedited, but made up 55.6% of the £4.16m total freight spend (£2.31m)",
        "technical_detail": None,
    },
    {
        "plain_headline": "Inventory risk is low overall, but it isn't spread evenly — it's concentrated in a specific plant and a short list of parts.",
        "plain_body": "Across the whole network, the share of stock checks showing dangerously low inventory cover is small. But a group of 20 components sit below their safety-stock level nearly half the time, and one plant carries more of this risk in its most critical components than the other two.",
        "figure_line": "Low-cover rate: 1.5% (excluding a documented data warm-up period) &middot; 20 components below safety stock in 40%+ of monthly checks &middot; Ridgeway Powertrain Plant: 8.0% vs. 6.9%&ndash;7.5% at the other two plants",
        "technical_detail": f"Overall low-cover rate 4.32% including two documented simulation warm-up months, 95% {term('CI', 'confidence interval')} 4.07%&ndash;4.58%; 1.47% excluding them &mdash; see Limitations &amp; Debugging.",
    },
    {
        "plain_headline": "Shortages are overwhelmingly a supplier and logistics problem — not a forecasting problem.",
        "plain_body": "When production-risk events were traced back to a cause, the overwhelming majority came down to suppliers delivering late or shipments being delayed in transit. Getting the demand forecast wrong was a minor factor by comparison.",
        "figure_line": "57.8% Supplier Late Delivery + 34.6% Logistics Delay = 92.4% of 334 events &middot; Only 5.2% Demand Spike",
        "technical_detail": None,
    },
]

PROBLEM_PARAGRAPHS = [
    (
        "Arden is a fictional premium UK vehicle manufacturer experiencing component shortages, "
        "late deliveries, volatile lead times and expensive expedited freight. Management wanted "
        "to know which suppliers genuinely create production risk, which components are most "
        "likely to disrupt production, where inventory cover is dangerously low, whether "
        "shortages are driven by supplier reliability or demand changes, and where expedited "
        "freight is increasing cost."
    ),
    (
        "One rule was non-negotiable: <strong>no supplier could be labelled a poor performer</strong> "
        "without first checking whether its raw delivery record still held up once the difficulty "
        "of the components it actually supplies was taken into account."
    ),
]

STAKEHOLDERS = [
    {"role": "Director of Procurement &amp; Supply Chain", "need": "Needed to know which suppliers genuinely create production risk, and which just look bad because they carry harder-to-supply components."},
    {"role": "Production Planning", "need": "Needed to know where inventory cover is dangerously low, and whether that risk is spread evenly or concentrated in specific components and plants."},
    {"role": "Logistics &amp; Freight Management", "need": "Needed to know how much expedited freight is really costing, and whether it's a symptom of a deeper supplier-reliability problem rather than a freight-policy problem."},
    {"role": "Supplier Quality &amp; Category Management", "need": "Needed a fair basis for supplier conversations that doesn't punish a supplier simply for being asked to supply harder, more critical components."},
]

DATASET_ROWS = [
    [{"value": "Coverage"}, {"value": "30 suppliers, 650 components, 3 manufacturing plants, multiple commodity groups and criticality tiers"}],
    [{"value": "Period"}, {"value": "January 2024 – December 2025 (24 months)"}],
    [{"value": "Purchase orders"}, {"value": "14,403 (canonical, processed layer)", "num": True}],
    [{"value": "OTIF-eligible orders"}, {"value": "14,383 (used for on-time-in-full rate calculations)", "num": True}],
    [{"value": "Shipments"}, {"value": "14,418", "num": True}],
    [{"value": "Inventory stock snapshots"}, {"value": "23,925 (monthly stock-level checks across components and plants)", "num": True}],
    [{"value": "Shortage / production-risk events"}, {"value": "334", "num": True}],
]

TOOLS = [
    {"name": "Excel", "desc": "A 10-sheet workbook where every KPI is a live formula or PivotTable over the processed purchase-order, delivery and inventory data — not typed in by hand."},
    {"name": "SQL", "desc": "Six portable, CTE/window-function-based queries covering KPIs, supplier performance, inventory coverage, shortages, freight cost and component criticality — validated against a SQLite load of the same tables."},
    {"name": "Python", "desc": "The statistical work: a logistic-regression case-mix adjustment for supplier fairness, Wilson-score confidence intervals, a significance test on the year-over-year OTIF change, and a bootstrap sensitivity check."},
    {"name": "Power BI", "desc": "A full dashboard build specification — the data model, the DAX measure library and the page layouts — ready to build."},
]

CASEMIX_ROWS = [
    [{"value": "Kestrel Precision Components"}, {"value": "29th of 30 (49.2%)"}, {"value": "28th of 30 (47.4%)"}, {"value": "Genuinely harder mix (72.9% Critical/High vs. 36.3% average) — but adjustment barely moves it; poor record stands even after accounting for the harder job"}],
    [{"value": "Solmar Fasteners Ltd"}, {"value": "26th of 30 (50.9%)"}, {"value": "27th of 30 (47.9%)"}, {"value": "Easier-than-average mix (67.5% Medium/Low criticality) — adjustment makes its position slightly worse, not better; the cleanest genuinely-poor-supplier case in the dataset"}],
    [{"value": "Cliffgate Logistics Components"}, {"value": "30th of 30, worst raw OTIF (46.8%)"}, {"value": "26th of 30 (51.7%)"}, {"value": "Adjustment does lift Cliffgate meaningfully (+4 ranks) — but it's still bottom-tier even adjusted; forms the other half of the “two worst suppliers stay worst” finding"}],
    [{"value": "Ravensworth Chassis"}, {"value": "15th of 30 (80.0%)"}, {"value": "8th of 30 (83.3%)"}, {"value": "The single biggest mover in the whole supplier set (+7 ranks) — proof the adjustment is meaningful generally, just not for the two worst performers"}],
]

RECOMMENDATIONS = [
    "<strong>Open a specific, time-bounded conversation with Ashcombe Precision</strong> about its August&ndash;December 2025 performance — the isolated, recent, severe nature of this episode makes it the single most tractable issue in this report.",
    "<strong>Escalate Solmar Fasteners Ltd for contract review</strong>, on the basis of consistently poor performance on an easier-than-average parts mix — its weak position is not an artefact of job difficulty.",
    "<strong>Treat Kestrel Precision Components as a genuine reliability risk, not merely a hard-parts victim</strong> — continue sourcing it for what it does well, but don't excuse its OTIF record purely on job-mix grounds; a joint improvement plan is more appropriate than either dismissing the concern or replacing a supplier that does carry real technical difficulty.",
    "<strong>Prioritise the 20 chronically low-cover components and Ridgeway Powertrain Plant specifically</strong> for safety-stock review, rather than a blanket inventory policy change — the risk is concentrated, not systemic.",
    "<strong>Investigate expedited-freight triggers as a cost-reduction lever</strong> — since shortages are overwhelmingly supplier- and logistics-driven, improving upstream delivery reliability for the highest-expediting suppliers is likely to reduce freight cost more effectively than freight-policy changes alone.",
]

LIMITATIONS_DEBUG = [
    "<strong>The synthetic data was originally scripted with a different headline story.</strong> The plan was for Kestrel Precision Components to look poor mainly because of a harder parts mix, while Solmar Fasteners Ltd would be genuinely poor regardless of mix. Running the actual case-mix regression told a more honest story: Kestrel's harder mix (72.9% Critical/High components) barely moves its adjusted rating at all — its poor record is real, not just a reflection of what it was asked to supply. The write-up was rewritten to match what the regression actually showed, not the story that was originally planned.",
    "<strong>An early version of the inventory simulation produced an implausible reliability swing.</strong> A first pass showed an implausible swing from around 81% to around 4% in an inventory-reliability metric within the first eight months of the dataset — a simulation cold-start effect (component reorder cycles hadn't reached steady state yet), not a real pattern. The generator's order-scheduling logic was fixed and the affected data regenerated before any analysis was built on it. A smaller residual version of the same effect remains in January&ndash;February 2024 and is documented and excluded from the headline low-cover figure throughout this project (4.32% including those two months vs. 1.47% excluding them).",
]

LIMITATIONS_STANDARD = [
    "<strong>Synthetic data throughout</strong> — every figure describes patterns in a generated dataset built for this portfolio, not a real vehicle manufacturer.",
    "<strong>Association, not proof of cause</strong> — the case-mix adjustment controls for observed criticality and commodity-group differences, but doesn't prove a causal supplier effect. The expedited-freight/lateness relationship is a plausible operational pattern built into the data, not independently proven causal.",
    "<strong>The case-mix regression is less precise for suppliers with narrow, concentrated component portfolios</strong> (e.g. a supplier operating in only one commodity group) — individual supplier rank-change magnitudes should be read as indicative, not exact.",
    "<strong>Supplier order counts range from 146 to 1,427</strong> — comparisons involving the smaller-volume suppliers carry wider uncertainty than headline suppliers like Kestrel (n=1,427) or Solmar (n=900).",
    "<strong>Shortage cause is recorded as a single label per event</strong>, not a full multi-cause decomposition — a shortage with several contributing factors is recorded under its primary cause only.",
]

TECH_CARDS = [
    {"heading": "03_excel/", "items": ["documentation/build_excel_workbook.py — reproducible build script", "workbook/arden_supply_risk_analysis.xlsx — 10-sheet workbook"]},
    {"heading": "04_sql/", "items": ["01_kpi_analysis.sql &middot; 02_supplier_analysis.sql", "03_inventory_coverage.sql &middot; 04_shortage_root_cause.sql", "05_cost_freight_analysis.sql &middot; 06_component_criticality_analysis.sql"]},
    {"heading": "07_python/", "items": ["arden_supply_risk_analysis.py — full analysis script", "arden_supply_risk_analysis.ipynb — narrated notebook", "results/arden_results.json — machine-readable results"]},
    {"heading": "05_power_bi/documentation/", "items": ["dashboard_specification.md — build specification", "dax_measures.md — full DAX measure library", "data_model.md — data model design"]},
]

GALLERY_IMAGES = [
    {
        "src": "../assets/images/arden/01_distribution_shape.png",
        "alt": "Histogram showing purchase-order lead time is right-skewed",
        "caption": "Purchase-order lead time is right-skewed (mean 25.0 days, median 22.0 days, 90th percentile 41 days) — most orders arrive within a few weeks, with a long tail of much slower ones, which is why medians rather than averages are used for lead time throughout this project.",
    },
    {
        "src": "../assets/images/arden/02_monthly_otif_trend.png",
        "alt": "Line chart of monthly OTIF rate across the two-year period",
        "caption": "Month-by-month OTIF rate across the full two-year window. The year-over-year change is not statistically significant (Finding 5) — the visible movement mostly reflects Ashcombe Precision's isolated Aug&ndash;Dec 2025 collapse (Finding 4), not a network-wide trend.",
    },
]

FOOTER_DISCLAIMER = "Arden Automotive Group is fictional; all data is synthetic."


def _load():
    return charts_data.load_results(
        "arden_automotive_group/projects/01_supply_risk_intelligence/07_python/results/arden_results.json"
    )


def get_charts():
    s = _load()
    charts = {}

    table = s["supplier_case_mix_adjustment"]["comparison_table"]
    charts["casemix"] = {
        "id": "casemix", "type": "comparison",
        "title": "Raw vs. case-mix-adjusted OTIF rate, by supplier",
        "caption": "All 30 suppliers, sorted by raw OTIF rate. Ravensworth Chassis moves the furthest under adjustment (15th &rarr; 8th) — proof the adjustment is meaningful generally. Kestrel Precision Components and Solmar Fasteners Ltd barely move, and stay near the bottom either way.",
        "payload": {
            "rows": [
                {
                    "label": r["supplier_name"],
                    "before": round(r["raw_otif_rate"] * 100, 1),
                    "after": round(r["adjusted_otif_rate"] * 100, 1),
                    "meta": {"n": r["n"], "rank_change": r["rank_change"]},
                }
                for r in table
            ],
            "options": {
                "valueFormat": "percent",
                "beforeLabel": "Raw OTIF rate",
                "afterLabel": "Case-mix adjusted OTIF rate",
                "categoryLabel": "Supplier",
                "metaColumns": [
                    {"key": "n", "label": "Orders", "numeric": True, "format": "number"},
                    {"key": "rank_change", "label": "Rank change", "numeric": True, "format": "number"},
                ],
            },
        },
    }

    f = s["expedited_freight_premium"]
    charts["freight"] = {
        "id": "freight", "type": "bar",
        "title": "Average shipment cost: standard vs. expedited freight",
        "caption": f"Expedited (air) shipments cost {f['premium_multiple']}x more on average than standard freight, and account for over half of total freight spend despite being just over a quarter of shipments (Finding 6).",
        "payload": {
            "categories": ["Standard freight", "Expedited freight"],
            "series": [
                {"label": "Average shipment cost", "values": [round(f["avg_standard_cost"], 2), round(f["avg_expedited_cost"], 2)]},
            ],
            "options": {"valueFormat": "gbp", "categoryLabel": "Freight type"},
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
      {T.render_chart_block(charts['casemix'])}
      {T.render_chart_block(charts['freight'])}
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
      <p>Each tool answers a different part of the brief, but every headline number reconciles exactly across all of them. Lead time and purchase-order value are both right-skewed (see the gallery below), so medians and percentiles are used throughout rather than simple averages.</p>
    </div>
    {T.render_tool_grid(TOOLS)}
  </div>
</section>"""

    casemix_section = f"""<section id="casemix" class="section-alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">5. Supplier {term('Case-Mix', 'case-mix adjustment')} Analysis</span>
      <h2>Testing whether raw supplier comparisons are fair</h2>
      <p>The interactive chart above (Headline Numbers) shows raw vs. case-mix-adjusted OTIF for all 30 suppliers, sorted from best to worst raw performer. The table below names the specific suppliers this analysis turned out to be about.</p>
    </div>
    {T.render_static_table(["Supplier", "Raw rank", "Adjusted rank", "Interpretation"], CASEMIX_ROWS)}
  </div>
</section>"""

    shortages_section = f"""<section id="shortages">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">6. Shortage Root Causes</span>
      <h2>Why parts actually run short</h2>
      <p>Every shortage/production-risk event was traced back to a single primary cause. The result answers the "supplier reliability vs. demand changes" question management asked directly.</p>
    </div>
    {T.render_static_chart_figure({
        "src": "../assets/images/arden/04_shortage_root_cause.png",
        "alt": "Bar chart of shortage events by root cause",
        "caption": "Of 334 shortage/production-risk events, 57.8% are attributed to Supplier Late Delivery and 34.6% to Logistics Delay — together over 92% of events — versus just 5.2% for Demand Spike.",
    })}
  </div>
</section>"""

    freight_section = f"""<section id="freight" class="section-alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">7. Freight Cost Concentration</span>
      <h2>Where the freight budget actually goes</h2>
      <p>The interactive chart above (Headline Numbers) compares average standard vs. expedited shipment cost. The chart below breaks total freight spend down by commodity group.</p>
    </div>
    {T.render_static_chart_figure({
        "src": "../assets/images/arden/05_cost_pareto_by_commodity.png",
        "alt": "Pareto chart of freight cost by commodity group",
        "caption": "Freight cost concentrates heavily in a small number of commodity groups — consistent with the pattern in Finding 6, where a minority of expedited shipments drive a disproportionate share of the £4.16m total freight spend.",
    })}
  </div>
</section>"""

    recommendations_section = f"""<section id="recommendations">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">8. Management Recommendations</span>
      <h2>What follows from the evidence</h2>
    </div>
    {T.render_rec_list(RECOMMENDATIONS)}
  </div>
</section>"""

    limitations_section = f"""<section id="limitations" class="section-alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">9. Limitations &amp; Debugging Lessons</span>
      <h2>What this analysis does not claim — and two things caught before they shipped</h2>
    </div>
    {T.render_limit_list(LIMITATIONS_DEBUG)}
    {T.render_limit_list(LIMITATIONS_STANDARD)}
  </div>
</section>"""

    gallery_section = f"""<section id="gallery">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">10. More Charts</span>
      <h2>Supporting visuals</h2>
    </div>
    {T.render_chart_gallery(GALLERY_IMAGES)}
  </div>
</section>"""

    technical_section = f"""<section id="technical" class="section-alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">11. Technical Evidence</span>
      <h2>Source deliverables</h2>
      <p>Source files for this project are organised as shown below (not yet published to a public GitHub repository). Every deliverable reconciles to the same figures shown on this page.</p>
    </div>
    {T.render_tech_grid(TECH_CARDS)}
    <p class="tech-note">See also: <code>08_outputs/executive_summary/</code> for the full written analysis and <code>09_case_study/portfolio_case_study.md</code> for the source of this page.</p>
  </div>
</section>"""

    return "\n".join([
        findings_section, problem_section, stakeholders_section, dataset_section,
        approach_section, casemix_section, shortages_section, freight_section,
        recommendations_section, limitations_section, gallery_section, technical_section,
    ])


def get_card():
    return {
        "industry": "Automotive",
        "title": "Arden Automotive Group",
        "meta": "Supplier performance & cost",
        "question": "Are the worst-performing suppliers genuinely unreliable, or just stuck with harder parts to deliver?",
        "tags": ["Excel", "Python", "Power BI"],
        "href": "case-studies/arden.html",
    }
