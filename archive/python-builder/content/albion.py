"""Albion General Insurance — case-study content, in the plain-language schema."""

import charts_data
import templates as T
from templates import term

SLUG = "albion"
NAV_PREFIX = "../"

META = {
    "title": "Albion General Insurance Case Study — Farouk Yusuf",
    "description": (
        "Claims cost, settlement & operational performance analytics case study: Excel, SQL, "
        "Python and Power BI analysis of a synthetic general insurer's claims-cost growth, "
        "supplier/regional fairness and reserve-accuracy data."
    ),
}

DISCLAIMER_STRIP = (
    "Albion General Insurance is fictional. All data on this page is synthetically generated "
    "for portfolio purposes — see the disclaimer below for detail."
)

DISCLAIMER_BOX = (
    "<strong>Synthetic-data disclaimer:</strong> Albion General Insurance is a fictional "
    "insurer. Every policy, claim, supplier, region and figure on this page was generated for "
    "data-analytics portfolio purposes — none of it describes a real insurer, and no figure "
    "should be read as representing an actual insurer. No individual policyholder or claimant "
    "is identified, ranked or scored anywhere in this project."
)

HERO = {
    "breadcrumb_label": "Albion General Insurance",
    "h1": "Claims Cost, Settlement &amp; Operational Performance Analytics",
    "sub": (
        "Is a fictional insurer's rising claims bill down to more claims happening, or each "
        "claim costing more? And do the suppliers and regions that look expensive still look "
        "expensive once you account for how hard their claims actually were? An end-to-end "
        "analysis across Excel, SQL, Python and Power BI on 9,263 claims from a two-year book "
        "of business."
    ),
}

SHORT_VERSION = [
    (
        "Albion is a made-up general insurer, used here to practise a real analytics workflow "
        "end to end. Its claims bill grew by a fifth in a year — and the data shows that's "
        "almost entirely because <strong>more claims are happening</strong>, not because each "
        "claim costs more."
    ),
    (
        "Along the way, the same analysis found two suppliers whose reputations flip once you "
        "account for how hard their jobs really were, a reserve-setting habit that's backwards "
        "(cheap claims are over-funded, expensive ones are under-funded), and one claim type "
        "that gets reopened three times more often than any other."
    ),
]

ANCHOR_NAV = [
    {"id": "findings", "label": "Key Findings"},
    {"id": "problem", "label": "Business Problem"},
    {"id": "dataset", "label": "Dataset"},
    {"id": "approach", "label": "Approach &amp; Tools"},
    {"id": "decomposition", "label": "Cost-Growth Decomposition"},
    {"id": "duration", "label": "Settlement Duration &amp; Reopens"},
    {"id": "casemix", "label": "Case-Mix Analysis"},
    {"id": "reserves", "label": "Reserve Accuracy"},
    {"id": "recommendations", "label": "Recommendations"},
    {"id": "limitations", "label": "Limitations &amp; Debugging"},
    {"id": "gallery", "label": "More Charts"},
    {"id": "technical", "label": "Technical Evidence"},
]

KPIS = [
    {"num": "+21.10%", "label": "Total claims paid growth, 2024 → 2025", "tag": None},
    {"num": "+19.87%", "label": "Claim frequency growth — the main driver", "tag": "significant"},
    {"num": "+1.03%", "label": "Average cost per claim (severity)", "tag": "not_significant"},
    {"num": "£3.13m", "label": "Cost increase, fully broken down into its parts", "tag": None},
]

FINDINGS = [
    {
        "plain_headline": "Claims are rising because there are more of them — not because each one costs more.",
        "plain_body": "The total Albion paid out grew by a fifth in a year. Almost all of that came from more claims happening, not from each claim getting pricier.",
        "figure_line": "+21.10% total paid &middot; +19.87% claim frequency &middot; +1.03% average cost per claim",
        "technical_detail": f"Two-proportion z-test on claim frequency: z=9.64, {term('p&lt;0.0001', 'p-value')} ({term('significant', 'statistically significant')}). Welch's t-test on average severity: t=0.24, {term('p=0.809', 'p-value')} ({term('not significant', 'statistically significant')}).",
    },
    {
        "plain_headline": "A closer look shows two opposite effects hiding inside that flat severity number.",
        "plain_body": "Splitting the £3.13m cost increase into its exact parts shows claim mix shifted toward cheaper claim types (pulling the average down) while genuine severity inflation pushed it back up — they nearly cancel out, which is exactly why the headline severity number looked like nothing was happening.",
        "figure_line": "Frequency +£2.96m &middot; Mix &minus;£0.75m &middot; Within-type severity +£0.91m",
        "technical_detail": f"Exact LMDI (Logarithmic Mean Divisia Index) {term('decomposition', 'decomposition')} of cost into frequency × severity, followed by a Bennet shift-share split of the severity effect into mix and within-type components. All parts sum exactly to the £3,132,122 total change.",
    },
    {
        "plain_headline": "A small number of claim types create most of the cost.",
        "plain_body": "Theft and Fire make up only about one claim in seven, but together they account for nearly half of everything Albion pays out. Accidental Damage is the single most common claim type, but it's comparatively cheap per claim.",
        "figure_line": "Theft + Fire: 14.5% of claims, 43.5% of cost &middot; Accidental Damage: 40.1% of claims, 15.6% of cost",
        "technical_detail": None,
    },
    {
        "plain_headline": "A single storm explains part of the rise — but not most of it.",
        "plain_body": "A severe storm hit three regions for five days in January 2025, adding hundreds of claims and a meaningful chunk of cost. But even without it, claims were still rising by more than one in ten — this is mostly a genuine underlying trend, not one bad week.",
        "figure_line": "Storm Edwina: 267 claims, £789,607 &middot; Without it, frequency growth falls from 19.87% to 13.53%",
        "technical_detail": "Sensitivity check excluding all storm-window claims (20–24 Jan 2025, regions RG02/RG06/RG07): cost growth falls from 21.10% to 15.78%.",
    },
    {
        "plain_headline": "Albion is reserving money backwards — cautious on cheap claims, optimistic on expensive ones.",
        "plain_body": "When a claim first comes in, Albion sets aside money for it before knowing the full picture. For small claims, it sets aside far more than it ends up paying. For the most serious claims, it sets aside far less — the opposite of what careful reserving should look like.",
        "figure_line": "Minor claims: reserved at 224% of what's eventually paid &middot; Total Loss claims: reserved at just 28%",
        "technical_detail": None,
    },
    {
        "plain_headline": "One claim type gets reopened three times more often than any other — and reopening adds real delay.",
        "plain_body": "Escape of Water claims (burst pipes, leaks) get reopened far more often than any other type, most likely because more damage is found after the first repair. Every reopened claim also takes noticeably longer to finally settle.",
        "figure_line": "Escape of Water reopen rate: 14.13% vs 5.44% network average &middot; A reopen adds 43.7 days to settlement time",
        "technical_detail": f"Overall reopen rate 5.44% (Wilson 95% {term('CI', 'confidence interval')} 4.98%–5.95%). {term('Regression', 'regression')} of settlement duration on severity band, claim type and reopen status: reopening adds 43.7 days, {term('R²', 'r-squared')}=0.770.",
    },
    {
        "plain_headline": "Two suppliers tell opposite stories once you account for how hard their jobs actually were.",
        "plain_body": "Cobblestone Motor Repairs looks expensive at first glance — but its caseload is genuinely much harder than average, and once that's accounted for, its cost position looks normal. Foxglove Building Contractors looks cheap at first glance — but it's actually been handling an easy caseload, and once that's accounted for, it becomes the single most expensive supplier in its category.",
        "figure_line": "Cobblestone: raw rank 3rd &rarr; adjusted rank 15th &middot; Foxglove: raw rank 8th cheapest &rarr; adjusted rank most expensive",
        "technical_detail": f"Per-supplier-type log-cost {term('regression', 'regression')} with Duan's smearing correction — this is the {term('case-mix adjustment', 'case-mix adjustment')} referenced throughout this page. Bootstrap 95% {term('CI', 'confidence interval')} on the best-vs-worst Motor Repairer cost gap: £3,500.34–£7,029.80 (excludes zero, i.e. the gap is real).",
    },
    {
        "plain_headline": "The same pattern shows up geographically — one region looks cheap but isn't.",
        "plain_body": "Regional cost differences shrink once you account for how difficult each region's claims tend to be, but they don't disappear. One region, Bellcross, looks like one of the cheapest areas on a raw basis — but it has the easiest claims of any region, and once that's accounted for, it's actually the most expensive.",
        "figure_line": "Raw regional cost gap £1,499.78 &rarr; adjusted gap £1,252.19 (16.5% narrower) &middot; Bellcross: raw rank 9th cheapest &rarr; adjusted rank most expensive",
        "technical_detail": f"Single OLS log-cost {term('regression', 'regression')} across all regions, controlling for severity-band mix and policy type ({term('R²', 'r-squared')}=0.753, n=7,943), with Duan's smearing correction (factor 1.3428).",
    },
]

PROBLEM_PARAGRAPHS = [
    (
        "Albion is a fictional general insurer whose claims costs and settlement times have been "
        "creeping up. Management wanted a straight answer to a simple-sounding question: is this "
        "happening because more people are claiming, or because each claim costs more? They also "
        "wanted to know what's driving long settlement times, which claim types cost the most, "
        "whether some suppliers and regions really do cost more once you account for how hard "
        "their work is, whether the money set aside for claims at the start is realistic, and how "
        "much reopened claims cost in wasted time."
    ),
    (
        "One rule was non-negotiable: <strong>no supplier or region comparison could be presented "
        "as a simple ranking</strong> without first checking whether it still held up once claim "
        "difficulty was taken into account."
    ),
]

STAKEHOLDERS = [
    {"role": "Director of Claims Operations", "need": "Needed to know whether rising cost is a “more claims” problem or a “pricier claims” problem, to decide between hiring more claims handlers or reviewing pricing."},
    {"role": "Reserving &amp; Actuarial", "need": "Needed to know how accurate the money set aside for claims turns out to be, by how serious the claim is."},
    {"role": "Supplier &amp; Network Management", "need": "Needed a fair basis for supplier and regional conversations that doesn't punish a supplier simply for getting harder jobs."},
    {"role": "Claims Operations / Finance", "need": "Needed to know where cost concentrates and which claim type wastes the most time through reopened cases."},
]

DATASET_ROWS = [
    [{"value": "Coverage"}, {"value": "10 regions, 30 repair/restoration suppliers, 10 claim types, 4 severity bands"}],
    [{"value": "Period"}, {"value": "January 2024 – December 2025 (24 months)"}],
    [{"value": "Policies"}, {"value": "25,000", "num": True}],
    [{"value": "Claims"}, {"value": "9,263 (a small number of duplicate records were found and removed during cleaning)", "num": True}],
    [{"value": "Claim-handling events"}, {"value": "54,442 (from first notice of loss through to settlement)", "num": True}],
    [{"value": "Payments"}, {"value": "18,216", "num": True}],
    [{"value": "Reopened claims"}, {"value": "458", "num": True}],
]

TOOLS = [
    {"name": "Excel", "desc": "A 10-sheet workbook where every number that can be calculated live is a real formula or PivotTable — not typed in by hand."},
    {"name": "SQL", "desc": "Six database queries covering costs, settlement times, suppliers and regions — checked against a real database."},
    {"name": "Python", "desc": "The statistical work: splitting the cost increase into its exact causes, testing whether patterns are real or just chance, and checking two fairness comparisons for suppliers and regions."},
    {"name": "Power BI", "desc": "A full dashboard design — the data model, the formulas and the page layouts — ready to build, including a check for two ways the numbers could accidentally be counted twice."},
]

CASEMIX_ROWS = [
    [{"value": "Cobblestone Motor Repairs"}, {"value": "3rd most expensive"}, {"value": "15th"}, {"value": "Explained by a genuinely harder caseload — 41.0% Major/Total Loss claims, more than double the supplier average"}],
    [{"value": "Foxglove Building Contractors"}, {"value": "8th cheapest"}, {"value": "Most expensive"}, {"value": "A genuine outlier — not explained by caseload; only 12.9% Major/Total Loss claims (one of the easiest)"}],
    [{"value": "Bellcross (region)"}, {"value": "9th cheapest"}, {"value": "Most expensive"}, {"value": "A genuine outlier — easiest severity mix of any region (10.0% Major/Total Loss)"}],
]

RECOMMENDATIONS = [
    "<strong>Treat this as a “more claims are happening” problem, not a “claims are getting pricier” problem</strong>, in both claims-handling and pricing conversations.",
    "<strong>Focus cost-control effort on Theft and Fire claims</strong> — a far more concentrated lever than the higher-volume but comparatively cheap Accidental Damage claims.",
    "<strong>Revisit how much money gets set aside for Major and Total Loss claims at first notice</strong> — they're currently under-funded, while small claims are over-funded and tying up money unnecessarily.",
    "<strong>Use Cobblestone Motor Repairs and Foxglove Building Contractors as the test case for fairer supplier conversations</strong> — one's raw cost is explained by a harder caseload, the other's isn't.",
    "<strong>Start a focused effort to reduce reopened Escape of Water claims</strong> — the single most tractable operational-delay lever identified in this analysis.",
]

LIMITATIONS_DEBUG = [
    "<strong>An early version of the data generator produced an unrealistic 36% year-on-year rise in claims.</strong> The code wasn't broken, but the number didn't make business sense for a general insurer — so the growth trend was dialled back to a more defensible 20% before it was treated as a real finding.",
    "<strong>A data check that looked like a bug turned out to be correct behaviour.</strong> The raw and cleaned claim totals didn't match, which in every prior project has meant a real data-loss bug. Investigating first showed the gap was exactly explained by 111 duplicate records the cleaning process had rightly removed — so the fix was to how the check was worded, not to the data.",
]

LIMITATIONS_STANDARD = [
    "<strong>Made-up data throughout</strong> — every figure describes patterns in a generated dataset built for this portfolio, not a real insurer.",
    "<strong>Association, not proof of cause</strong> — the supplier and region comparisons account for known differences in claim difficulty, but don't prove a supplier or region directly causes higher cost.",
    "<strong>The fairness adjustment uses a statistical model, not an exact recalculation</strong> (a log-cost regression with a right-skew correction) — adjusted figures are a considered estimate.",
    "<strong>The model for predicting which claims get reopened only explains a modest part of the pattern</strong> (pseudo-R²=0.063) — claim type, severity and supplier rating matter, but plenty is left unexplained.",
    "<strong>15 claim-handling records out of 54,442 were excluded</strong> from one duration check because of a known data-quality issue — nothing else is affected.",
    "<strong>A reopened claim has two lifecycle-event chains under the same claim ID</strong> (documented in the Power BI data model's grain-consistency check) — any duration analysis has to account for this or risk double-counting.",
]

TECH_CARDS = [
    {"heading": "03_excel/", "items": ["build_excel_workbook.py — reproducible build script", "albion_claims_analysis.xlsx — 10 sheets, 4 charts, 1 PivotTable, 24 Excel Tables"]},
    {"heading": "04_sql/", "items": ["01_kpi_analysis.sql &middot; 02_frequency_severity_mix_analysis.sql", "03_settlement_duration_analysis.sql &middot; 04_supplier_performance_analysis.sql", "05_reserve_accuracy_reopen_analysis.sql &middot; 06_geographic_cost_concentration_analysis.sql"]},
    {"heading": "07_python/", "items": ["albion_claims_analysis.py — full analysis script", "albion_claims_analysis.ipynb — narrated notebook", "results/albion_results.json — machine-readable results"]},
    {"heading": "05_power_bi/documentation/", "items": ["dashboard_specification.md — 4-page dashboard design", "dax_measures.md — full DAX measure library", "data_model.md — data model design, incl. grain-consistency check"]},
]

GALLERY_IMAGES = []

FOOTER_DISCLAIMER = "Albion General Insurance is fictional; all data is synthetic."


def _load():
    return charts_data.load_results(
        "albion_general_insurance/projects/01_claims_performance/07_python/results/albion_results.json"
    )


def get_charts():
    s = _load()
    charts = {}

    monthly = s["monthly_trend"]
    charts["c1"] = {
        "id": "c1", "type": "line",
        "title": "Monthly claims cost and claim count, 2024–2025",
        "caption": "A sharp spike in January 2025 (Storm Edwina) sits on top of a steadier, more gradual rise across the full two years — two different patterns, visible in one chart.",
        "payload": {
            "xLabels": [charts_data.month_label(m["incident_year_month"]) for m in monthly],
            "series": [
                {"label": "Total paid", "values": [round(m["total_paid"], 2) for m in monthly], "valueFormat": "gbp"},
                {"label": "Claim count", "values": [m["claim_count"] for m in monthly], "valueFormat": "number", "axis": "secondary"},
            ],
            "options": {"annotations": [{"x": "Jan 2025", "label": "Storm Edwina"}]},
        },
    }

    d = s["cost_growth_decomposition"]
    charts["c2"] = {
        "id": "c2", "type": "waterfall",
        "title": "Claims-cost growth decomposition, 2024 → 2025",
        "caption": "Frequency, mix and within-type severity effects sum exactly to the £3.13m change — the mix and severity effects mostly cancel out, which is why the raw severity change looked negligible on its own.",
        "payload": {
            "steps": [
                {"label": "2024 Total", "value": round(d["inputs"]["C_2024"], 2), "isTotal": True},
                {"label": "Frequency", "value": round(d["frequency_effect_gbp"], 2)},
                {"label": "Mix", "value": round(d["mix_effect_gbp"], 2)},
                {"label": "Within-Type Severity", "value": round(d["within_type_severity_effect_gbp"], 2)},
                {"label": "2025 Total", "value": round(d["inputs"]["C_2025"], 2), "isTotal": True},
            ],
            "options": {"valueFormat": "gbp"},
        },
    }

    stages = sorted(s["settlement_duration"]["by_stage"], key=lambda r: r["avg_days"], reverse=True)
    charts["c3"] = {
        "id": "c3", "type": "bar",
        "title": "Average settlement duration by claim-handling stage",
        "caption": "Settlement duration is built from summed claim-lifecycle stage days, reconciling exactly to the total — no stage is double-counted.",
        "payload": {
            "categories": [r["event_type"] for r in stages],
            "series": [{"label": "Avg days", "values": [round(r["avg_days"], 1) for r in stages]}],
            "options": {"horizontal": True, "valueFormat": "days", "categoryLabel": "Stage"},
        },
    }

    suppliers = s["supplier_case_mix"]["table"]
    charts["c4"] = {
        "id": "c4", "type": "comparison",
        "title": "Raw vs case-mix-adjusted average cost by supplier",
        "caption": "Cobblestone Motor Repairs (3rd most expensive raw → 15th adjusted) and Foxglove Building Contractors (8th cheapest raw → most expensive adjusted) show the two clearest, opposite case-mix stories in the network. Use the toggle to switch supplier type.",
        "payload": {
            "rows": [
                {
                    "label": r["supplier_name"], "before": round(r["raw_avg_cost"], 2), "after": round(r["adjusted_avg_cost"], 2),
                    "meta": {"supplier_type": r["supplier_type"], "pct_major_or_total_loss": r["pct_major_or_total_loss"], "n_claims": r["n_claims"]},
                }
                for r in suppliers
            ],
            "options": {
                "valueFormat": "gbp", "beforeLabel": "Raw average cost", "afterLabel": "Case-mix adjusted",
                "categoryLabel": "Supplier", "limit": 15,
                "filterKey": "supplier_type", "filterValues": ["Motor Repairer", "Home Contractor"], "filterDefault": "Motor Repairer",
                "metaColumns": [
                    {"key": "pct_major_or_total_loss", "label": "% Major/Total Loss", "numeric": True, "format": "percent"},
                    {"key": "n_claims", "label": "Claims", "numeric": True, "format": "number"},
                ],
            },
        },
    }

    bands_order = ["Minor", "Moderate", "Major", "Total Loss"]
    bands = sorted(s["reserve_accuracy"]["by_severity_band"], key=lambda r: bands_order.index(r["severity_band_name"]))
    charts["c5"] = {
        "id": "c5", "type": "bar",
        "title": "Initial reserve vs eventual paid, by severity band",
        "caption": "Reserves cross over from heavily over-reserved (Minor, 224% of eventual paid) to severely under-reserved (Total Loss, 28%) — a textbook reserve-accuracy pattern.",
        "payload": {
            "categories": [r["severity_band_name"] for r in bands],
            "series": [
                {"label": "Initial reserve", "values": [round(r["avg_initial_reserve"], 2) for r in bands]},
                {"label": "Eventual paid", "values": [round(r["avg_total_paid"], 2) for r in bands]},
            ],
            "options": {"valueFormat": "gbp", "categoryLabel": "Severity band"},
        },
    }

    reopens = sorted(s["reopen_analysis"]["by_claim_type"], key=lambda r: r["reopen_rate_pct"], reverse=True)
    charts["c6"] = {
        "id": "c6", "type": "bar",
        "title": "Reopen rate by claim type",
        "caption": "Escape of Water reopens at 14.13% — nearly 3x the 5.44% network average — consistent with further water damage being found after an initial repair.",
        "payload": {
            "categories": [r["claim_type_name"] for r in reopens],
            "series": [{"label": "Reopen rate", "values": [r["reopen_rate_pct"] for r in reopens]}],
            "options": {"horizontal": True, "valueFormat": "percent", "categoryLabel": "Claim type"},
        },
    }

    dist = s["claim_cost_distribution"]
    charts["c7"] = {
        "id": "c7", "type": "histogram",
        "title": "Distribution of claim cost",
        "caption": "Claim cost is right-skewed — most claims settle for modest amounts, with a long tail of large losses (values above £20,000 are grouped into the final bar).",
        "payload": {
            "binEdges": dist["bin_edges"],
            "counts": dist["counts"],
            "options": {"valueFormat": "gbp", "meanLine": dist["mean_gbp"], "medianLine": dist["median_gbp"]},
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
      {T.render_chart_block(charts['c4'])}
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

    decomposition_section = f"""<section id="decomposition" class="section-alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">5. Claims-Cost Growth Decomposition</span>
      <h2>Frequency, mix and severity — exactly broken down</h2>
      <p>Every part below is calculated so it sums exactly to the real £3.13m change — nothing is rounded to fit.</p>
    </div>
    {T.render_chart_block(charts['c2'])}
  </div>
</section>"""

    duration_section = f"""<section id="duration">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">6. Settlement Duration &amp; Reopened Claims</span>
      <h2>What drives long settlement times</h2>
    </div>
    <div class="two-col">
      {T.render_chart_block(charts['c3'])}
      {T.render_chart_block(charts['c6'])}
    </div>
  </div>
</section>"""

    casemix_section = f"""<section id="casemix" class="section-alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">7. Supplier &amp; Regional {term('Case-Mix', 'case-mix adjustment')} Analysis</span>
      <h2>Testing whether raw supplier and regional comparisons are fair</h2>
      <p>The interactive chart above (Headline Numbers) lets you switch between Motor Repairers and Home Contractors. The table below names the specific outliers.</p>
    </div>
    {T.render_static_table(["Supplier / Region", "Raw rank", "Adjusted rank", "Interpretation"], CASEMIX_ROWS)}
  </div>
</section>"""

    reserves_section = f"""<section id="reserves">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">8. Reserve Accuracy</span>
      <h2>How accurate is the money set aside for claims?</h2>
    </div>
    {T.render_chart_block(charts['c5'])}
  </div>
</section>"""

    recommendations_section = f"""<section id="recommendations" class="section-alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">9. Management Recommendations</span>
      <h2>What follows from the evidence</h2>
    </div>
    {T.render_rec_list(RECOMMENDATIONS)}
  </div>
</section>"""

    limitations_section = f"""<section id="limitations">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">10. Limitations &amp; Debugging Lessons</span>
      <h2>What this analysis does not claim — and two things caught before they shipped</h2>
    </div>
    {T.render_limit_list(LIMITATIONS_DEBUG)}
    {T.render_limit_list(LIMITATIONS_STANDARD)}
  </div>
</section>"""

    gallery_section = f"""<section id="gallery" class="section-alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">11. More Charts</span>
      <h2>Supporting visuals</h2>
    </div>
    {T.render_chart_block(charts['c7'])}
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
        approach_section, decomposition_section, duration_section, casemix_section,
        reserves_section, recommendations_section, limitations_section,
        gallery_section, technical_section,
    ])


def get_card():
    return {
        "industry": "Insurance",
        "title": "Albion General Insurance",
        "meta": "Claims & operational insights",
        "question": "Is the rising claims bill down to more claims happening, or each claim costing more?",
        "tags": ["Power BI", "SQL", "Excel"],
        "href": "case-studies/albion.html",
    }
