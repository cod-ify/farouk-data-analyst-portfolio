"""Westborough Council — case-study content, in the plain-language schema."""

import charts_data
import templates as T
from templates import term

SLUG = "westborough"
NAV_PREFIX = "../"

META = {
    "title": "Westborough Council Case Study — Farouk Yusuf",
    "description": (
        "Adult social-care demand & financial sustainability analytics case study: Excel, SQL, "
        "Python and Power BI analysis of a fictional council's expenditure-growth decomposition "
        "and provider/locality cost fairness, on a synthetic, ethically-constrained social-care "
        "dataset."
    ),
}

DISCLAIMER_STRIP = (
    "Westborough Council is fictional. All data on this page is synthetically generated for "
    "portfolio purposes — see the disclaimer below for detail."
)

DISCLAIMER_BOX = (
    "<strong>Synthetic-data disclaimer:</strong> Westborough Council is a fictional local "
    "authority. Every service user, care package, provider, locality and figure on this page was "
    "generated for data-analytics portfolio purposes — none of it describes a real council, and "
    "no figure should be read as representing an actual local authority. No individual service "
    "user, referral or care package is identified, ranked or scored anywhere in this project."
)

HERO = {
    "breadcrumb_label": "Westborough Council",
    "h1": "Adult Social Care Demand &amp; Financial Sustainability Analytics",
    "sub": (
        "Is a fictional council's rising adult social-care bill down to more people needing care, "
        "or care itself costing more? And do the care providers and areas that look expensive "
        "still look expensive once you account for how hard their caseloads really are — without "
        "ever ranking a single person? An end-to-end analysis across Excel, SQL, Python and Power "
        "BI on two years of synthetic social-care data."
    ),
}

SHORT_VERSION = [
    (
        "Westborough is a made-up local council, used here to practise a real analytics workflow "
        "on a sensitive, ethically-constrained dataset. Its adult social-care bill grew by 11% in "
        "a year — a real but modest amount faster than the 9.2% growth in the number of people "
        "receiving care — and the data shows that gap is the net result of "
        "<strong>six different effects pulling in different directions</strong>, not one runaway "
        "cause."
    ),
    (
        "Along the way, the same analysis found two care homes whose cost position flips once you "
        "account for how hard their caseloads really are, two areas of the council that stay "
        "genuinely more expensive even after accounting for case difficulty, and a data-generation "
        "bug that briefly made spending look like it was falling by almost a third before it was "
        "caught and fixed."
    ),
]

ANCHOR_NAV = [
    {"id": "findings", "label": "Key Findings"},
    {"id": "problem", "label": "Business Problem"},
    {"id": "stakeholders", "label": "Stakeholders"},
    {"id": "dataset", "label": "Dataset"},
    {"id": "approach", "label": "Approach &amp; Tools"},
    {"id": "decomposition", "label": "Expenditure Growth Decomposition"},
    {"id": "providers", "label": "Provider Case-Mix Analysis"},
    {"id": "localities", "label": "Locality Case-Mix Analysis"},
    {"id": "caseload", "label": "New vs Continuing Users"},
    {"id": "recommendations", "label": "Recommendations"},
    {"id": "limitations", "label": "Limitations &amp; Debugging"},
    {"id": "gallery", "label": "More Charts"},
    {"id": "technical", "label": "Technical Evidence"},
]

KPIS = [
    {"num": "+11.0%", "label": "Total adult social-care expenditure growth, 2024 → 2025", "tag": None},
    {"num": "+9.2%", "label": "Growth in people receiving care — the main driver", "tag": None},
    {"num": "+1.65%", "label": "Average cost per person served", "tag": "not_significant"},
    {"num": "£8.25m", "label": "Expenditure increase, fully broken into six exact drivers", "tag": None},
]

FINDINGS = [
    {
        "plain_headline": "Spending on adult social care grew faster than the number of people receiving it — but only by a little.",
        "plain_body": "In a year, total spending went up by just over a tenth, while the number of people getting care went up by under a tenth. That's a real gap between the two, but it's a modest one — not a runaway trend.",
        "figure_line": "+11.0% total expenditure (£75.0m &rarr; £83.3m) &middot; +9.2% people served (3,608 &rarr; 3,940)",
        "technical_detail": None,
    },
    {
        "plain_headline": "The extra £8.25m in spending splits exactly into six separate reasons — no single one explains all of it.",
        "plain_body": "Instead of guessing at one cause, the entire increase was traced, penny by penny, into six distinct effects — from more people needing care, to how long people needed it for, to changes in care-home fees.",
        "figure_line": "More people needing care +£6.96m &middot; Care lasting less time per person, on average &minus;£5.30m &middot; Shift away from residential care &minus;£1.07m &middot; Hourly-care rates rising +£1.00m &middot; Hourly care getting slightly more intensive +£2.53m &middot; Care-home fee changes +£4.13m",
        "technical_detail": f"An exact three-level {term('decomposition', 'decomposition')} (Logarithmic Mean Divisia Index, then two Bennet shift-share splits) of expenditure into users × average weeks per user × average weekly cost, then rate into service-mix and within-type effects, then within-type into price and intensity for hourly services. All six components sum exactly to the £8,253,713.99 total change.",
    },
    {
        "plain_headline": "One of the six reasons looks like care is getting shorter — but that's a quirk of the calendar, not a real cut in care.",
        "plain_body": "People who join partway through a year only receive care for part of that year, which mechanically drags the average down — even though no one's actual care package got shorter. Far more people joined newly in 2025 than in 2024, which is what's really behind this effect.",
        "figure_line": "New-in-year average cost: £9,266 (2024) &rarr; £12,059 (2025) &middot; Continuing recipients: around £23,000 in both years &middot; New referrals: 962 (2024) &rarr; 1,594 (2025)",
        "technical_detail": None,
    },
    {
        "plain_headline": "The typical person's care didn't get meaningfully more expensive.",
        "plain_body": "The average yearly cost per person barely moved, and a statistical check can't rule out that even this small rise is just down to chance rather than a genuine change.",
        "figure_line": "£20,800 &rarr; £21,142 average cost per person per year (+1.65%)",
        "technical_detail": f"Welch's t-test on mean annual cost per person: t=0.68, {term('p=0.495', 'p-value')} ({term('not significant', 'statistically significant')}).",
    },
    {
        "plain_headline": "Most provider cost comparisons hold up fairly as they stand — but two residential care homes tell opposite stories once you account for how hard their caseloads are.",
        "plain_body": "Providers were only ever compared against others delivering the exact same kind of care, and adjusted for how complex their caseload was. Most rankings didn't move at all. One care home looks like the second most expensive in its category — but it also handles the hardest cases, and once that's accounted for it drops down the ranking. Another looks mid-priced — but it has an easier caseload than most, and once accounted for, becomes one of the most expensive.",
        "figure_line": "33 of 38 provider comparisons unchanged after adjustment &middot; Hollybank Manor Care Home: raw rank 2nd &rarr; adjusted rank 4th (87.9% high-complexity cases) &middot; Rosewood Care Home: raw rank 4th &rarr; adjusted rank 3rd",
        "technical_detail": f"Separate OLS log-rate {term('regression', 'regression')} per service type (never blending £/hour and £/week rates), controlling for complexity-tier mix — this is the {term('case-mix adjustment', 'case-mix adjustment')} referenced throughout this page. Average {term('R²', 'r-squared')}=0.79 across 8 service-type models (n=69,127).",
    },
    {
        "plain_headline": "Cost differences between areas of the council shrink once you account for how complex people's needs are — but a real gap remains in two areas.",
        "plain_body": "Some areas cost more partly because they have harder cases and more residential care. Adjusting for that narrows the gap by around a third — but two areas still cost noticeably more than the rest even after adjusting, which is worth investigating on the ground.",
        "figure_line": "Raw gap £3,205 (16.6%): Westborough Central highest, Rural Downlands lowest &middot; Adjusted gap £1,876 (about a third narrower): Northfield highest, Ashcombe Vale lowest",
        "technical_detail": f"OLS {term('regression', 'regression')} of log annual cost per person on locality, dominant complexity tier and % of cost delivered in a Residential setting ({term('R²', 'r-squared')}=0.34, n=7,548), with Duan's smearing correction (factor 1.407) applied when converting back to £ — the {term('case-mix adjustment', 'case-mix adjustment')} used throughout this page.",
    },
    {
        "plain_headline": "The areas that cost more also tend to have harder cases and more referrals — which is part of the explanation, but not proof on its own.",
        "plain_body": "Westborough Central and Northfield, the two busiest areas, also have the highest share of people assessed as having substantial or critical needs. That lines up with them costing more, though it doesn't by itself prove that's the only reason.",
        "figure_line": "Highest complexity share: Westborough Central 53.8%, Northfield 49.9% &middot; Lowest: Rural Downlands 43.1%",
        "technical_detail": None,
    },
    {
        "plain_headline": "A data-setup quirk briefly made the first three months of the analysis look unusual — but it doesn't change the headline figures.",
        "plain_body": "The very start of the two-year window shows a small, artificial dip-and-recovery pattern, a known side-effect of how the underlying data was generated rather than anything real. Removing that period and recalculating shifts the headline growth figure by only a fraction of a percentage point.",
        "figure_line": "Growth excluding Jan&ndash;Mar 2024: 10.91% vs the reported 11.0%",
        "technical_detail": "Sensitivity check: re-annualising 2024 expenditure from April&ndash;December only, then comparing to 2025, changes the headline growth figure from 11.0% to 10.91%.",
    },
]

PROBLEM_PARAGRAPHS = [
    (
        "Westborough is a fictional local authority whose adult social-care spending has been "
        "rising faster than the number of people receiving services. Senior management wanted a "
        "straight answer to a wide brief: is the pressure caused by more people needing care, "
        "harder cases, more intensive care packages, longer service duration, rising provider "
        "prices, a shift between residential and home-based care, geography, or specific "
        "providers — and, critically, whether raw provider and locality cost comparisons would "
        "hold up once case difficulty was properly accounted for."
    ),
    (
        "One rule was non-negotiable throughout: <strong>this analysis must never produce a "
        "“high-cost person” ranking or a simplistic provider league table</strong>. No individual "
        "service user, referral or care package is ranked, scored or singled out anywhere in this "
        "project — every comparison sits at group level (provider, locality, service type or "
        "complexity tier), and every raw comparison is presented alongside its case-mix-adjusted "
        "counterpart rather than on its own."
    ),
]

STAKEHOLDERS = [
    {"role": "Director of Adult Social Care", "need": "Needed to know whether rising spend is a “more people need care” problem or a “care itself costs more” problem, to decide where to focus commissioning and budget conversations."},
    {"role": "Finance &amp; Budget Setting", "need": "Needed the expenditure increase broken into its exact drivers, to separate legitimate demand growth from controllable cost pressures like provider fee changes."},
    {"role": "Provider &amp; Contracts Management", "need": "Needed a fair basis for provider conversations that never blames a care home simply for taking on harder cases — and never ranks any individual."},
    {"role": "Locality &amp; Operations Managers", "need": "Needed to know which areas of the council genuinely cost more once case difficulty is accounted for, versus which just have harder caseloads."},
]

DATASET_ROWS = [
    [{"value": "Coverage"}, {"value": "6 localities, 32 care providers, 8 service types, 4 complexity tiers"}],
    [{"value": "Period"}, {"value": "January 2024 – December 2025 (24 months)"}],
    [{"value": "Service users (synthetic population)"}, {"value": "~6,000", "num": True}],
    [{"value": "Distinct users receiving care"}, {"value": "3,608 in 2024, 3,940 in 2025", "num": True}],
    [{"value": "Care packages"}, {"value": "5,674", "num": True}],
    [{"value": "Monthly service-delivery records"}, {"value": "69,149", "num": True}],
    [{"value": "New referrals"}, {"value": "962 in 2024, 1,594 in 2025", "num": True}],
]

TOOLS = [
    {"name": "Excel", "desc": "A 10-sheet workbook where every KPI is a live formula or PivotTable over the processed data — not typed in by hand."},
    {"name": "SQL", "desc": "Six CTE/window-function-based scripts covering KPIs, referrals, providers, localities and service mix — including an independent rebuild of the decomposition inputs as a cross-check."},
    {"name": "Python", "desc": "The statistical work: an exact three-level expenditure-growth decomposition, two separate case-mix regressions (provider and locality), confidence intervals, significance testing and sensitivity checks."},
    {"name": "Power BI", "desc": "A full build specification, DAX measure library and 4-page dashboard design, with explicit documentation of what a live DAX model can and can't reproduce from a Python regression."},
]

PROVIDER_CASEMIX_ROWS = [
    [{"value": "Hollybank Manor Care Home"}, {"value": "2nd most expensive"}, {"value": "4th"}, {"value": "Explained by a genuinely harder caseload — 87.9% Substantial/Critical needs, the highest of the five Residential Care providers compared"}],
    [{"value": "Rosewood Care Home"}, {"value": "4th most expensive"}, {"value": "3rd"}, {"value": "A mirror pattern to Hollybank's — its comparatively easier caseload was flattering its raw position"}],
]

LOCALITY_CASEMIX_ROWS = [
    [{"value": "Westborough Central"}, {"value": "Most expensive"}, {"value": "2nd most expensive"}, {"value": "Still relatively higher-cost after adjustment — remains worth operational investigation"}],
    [{"value": "Northfield"}, {"value": "2nd most expensive"}, {"value": "Most expensive"}, {"value": "Becomes the highest-cost locality once adjusted — complexity-tier mix alone doesn't fully explain its position"}],
]

RECOMMENDATIONS = [
    "<strong>Don't treat the expenditure/caseload gap as a single problem to solve</strong> — it's the net of six offsetting drivers; prioritise the two actionable, non-mechanical ones (the residential/nursing fee effect and the hourly-care intensity effect) over the volume and duration effects, which mostly reflect legitimate demand growth and a calendar artefact.",
    "<strong>Review commissioning and banding practice for Residential and Nursing Care specifically</strong> — it's where the single largest driver sits, and where price and case complexity currently can't be told apart from routine data; consider capturing them as separate fields going forward.",
    "<strong>Use Hollybank Manor Care Home and Rosewood Care Home as the test case for fairer, case-mix-aware provider conversations</strong> — one's raw cost is explained by a genuinely harder caseload, the other's favourable raw position isn't.",
    "<strong>Investigate Westborough Central and Northfield's remaining cost premium</strong> after case-mix adjustment — since complexity mix doesn't fully explain it, provider availability, travel/logistics and local commissioning practice are worth a direct operational look.",
    "<strong>Track new-referral volume and its partial-year cost pattern as a standing planning input</strong>, not just total caseload — it materially affects year-on-year duration and average-cost metrics in ways that are easy to misread as service changes.",
]

LIMITATIONS_DEBUG = [
    "<strong>An early version of the data generator made spending look like it was falling by more than 30%, the opposite of the intended trend.</strong> Every pre-existing service user's care package was accidentally started on day one of the two-year window with a freshly-drawn full duration — since durations cluster around a typical length, almost the entire pre-existing caseload appeared to end care at the same time, producing an artificial mass drop-off. This was traced by checking the monthly active-caseload trend, and fixed by giving existing care packages a staggered, already-partway-through duration instead of a fresh one.",
    "<strong>A statistical bug initially made every locality's case-mix-adjusted cost look like roughly half its raw cost — a suspiciously uniform gap that didn't look like genuine adjustment.</strong> The first version of the locality model converted its statistical predictions back into pounds in a way that systematically understates the true average for this kind of right-skewed cost data. The fix (a standard correction called Duan's smearing estimator) brought raw and adjusted figures back into the same plausible range.",
    "<strong>An early version of the provider comparison blended every service type onto one rate, which broke down for providers who only ever deliver one kind of care.</strong> Comparing an hourly home-care rate and a weekly care-home fee on the same basis isn't just statistically unstable, it's the wrong comparison to make — and it risked implying a home-care agency should be judged against a care home's fee. The fix was to compare providers only within the service type(s) they actually deliver.",
]

LIMITATIONS_STANDARD = [
    "<strong>Made-up data throughout</strong> — every figure describes patterns in a generated dataset built for this portfolio, not a real council.",
    "<strong>Association, not proof of cause</strong> — the provider and locality case-mix adjustments control for known differences in complexity and setting, but don't prove a provider or locality directly causes higher cost.",
    "<strong>A known simulation settling pattern affects the first quarter of the time series</strong> (January–March 2024) — documented and shown to shift the headline growth figure only marginally (Finding 8), rather than hidden.",
    "<strong>Price and case complexity can't be fully separated for weekly-fee services</strong> (Residential, Nursing, Respite, Reablement) using routine data alone — the banded weekly fee bundles both, stated explicitly rather than forced apart.",
    "<strong>The case-mix adjustment is less precise for providers with a narrow, small caseload</strong> — provider models are fitted separately per service type, so a provider offering only one service type to a small number of people has a wider margin of uncertainty on its adjusted figure.",
    "<strong>Who counts as a “new” referral is based on care-package start date only</strong>, not a full multi-year history — someone whose package started just before the two-year window began is treated as “continuing from before” even without visibility into how long they'd actually been receiving care.",
]

TECH_CARDS = [
    {"heading": "03_excel/", "items": ["workbook/westborough_asc_analysis.xlsx — 10 sheets, live formulas and PivotTables", "documentation/build_excel_workbook.py — reproducible build script", "documentation/validate_workbook.py &amp; excel_workbook_validation.json — automated validation"]},
    {"heading": "04_sql/", "items": ["01_kpi_analysis.sql &middot; 02_referral_assessment_flow.sql", "03_provider_analysis.sql &middot; 04_locality_complexity_analysis.sql", "05_service_mix_duration_analysis.sql &middot; 06_expenditure_decomposition_support.sql"]},
    {"heading": "07_python/", "items": ["westborough_asc_analysis.py — full analysis script", "westborough_asc_analysis.ipynb — narrated notebook", "results/westborough_results.json — machine-readable results"]},
    {"heading": "05_power_bi/documentation/", "items": ["dashboard_specification.md — 4-page dashboard design", "dax_measures.md — full DAX measure library", "data_model.md — data model design, incl. what DAX can/can't reproduce from the Python regression"]},
]

GALLERY_IMAGES = [
    {"src": "../assets/images/westborough/01_distribution_shape.png", "alt": "Histogram showing annual cost per service user is right-skewed", "caption": "Annual cost per service user is right-skewed — most people's care costs a modest amount, with a long tail of high-cost care packages (mean £20,978 vs median £12,274)."},
    {"src": "../assets/images/westborough/02_expenditure_caseload_trend.png", "alt": "Monthly expenditure and active caseload trend, 2024–2025", "caption": "Monthly expenditure and active caseload both trend upward across the two years, with a modest dip-then-recovery in Jan–Mar 2024 — a known data-generation settling pattern that doesn't materially affect the headline growth figure (Finding 8)."},
]

FOOTER_DISCLAIMER = "Westborough Council is fictional; all data is synthetic. No individual is represented or identifiable."


def _load():
    return charts_data.load_results(
        "westborough_council/projects/01_adult_social_care_demand/07_python/results/westborough_results.json"
    )


def get_charts():
    s = _load()
    charts = {}

    kpis = s["headline_kpis"]
    comp = s["expenditure_growth_decomposition"]["components_gbp"]
    charts["c1"] = {
        "id": "c1", "type": "waterfall",
        "title": "Expenditure growth decomposition, 2024 → 2025",
        "caption": "Volume, duration, service mix, price, intensity and the residential/nursing banded-fee change sum exactly to the £8.25m change — no single driver dominates, and the negative duration effect is a measurement artefact (see Finding 3), not a real cut in care.",
        "payload": {
            "steps": [
                {"label": "2024 Total", "value": round(kpis["2024"]["total_expenditure"], 2), "isTotal": True},
                {"label": "Volume", "value": round(comp["volume_effect"], 2)},
                {"label": "Duration", "value": round(comp["duration_effect"], 2)},
                {"label": "Service Mix", "value": round(comp["service_mix_effect"], 2)},
                {"label": "Price (Hourly)", "value": round(comp["price_effect_hourly_services"], 2)},
                {"label": "Intensity (Hourly)", "value": round(comp["intensity_effect_hourly_services"], 2)},
                {"label": "Banded Fee (Res./Nursing)", "value": round(comp["banded_fee_effect_residential_services"], 2)},
                {"label": "2025 Total", "value": round(kpis["2025"]["total_expenditure"], 2), "isTotal": True},
            ],
            "options": {"valueFormat": "gbp"},
        },
    }

    providers = s["provider_case_mix_adjustment"]["comparison_table"]
    service_types = ["Residential Care", "Day Care", "Direct Payments", "Domiciliary Care", "Nursing Care", "Reablement", "Respite/Short Break Care", "Supported Living"]
    charts["c2"] = {
        "id": "c2", "type": "comparison",
        "title": "Raw vs case-mix-adjusted average rate by provider",
        "caption": "Hollybank Manor Care Home (2nd most expensive raw → 4th adjusted) and Rosewood Care Home (4th raw → 3rd adjusted) show the clearest, opposite case-mix stories in Residential Care. Use the toggle to switch service type — 33 of the 38 provider comparisons across all service types don't change rank at all once adjusted. Rates are £/hour for hourly services and £/week for residential and other block-contract services.",
        "payload": {
            "rows": [
                {
                    "label": r["provider_name"], "before": round(r["raw_avg_rate"], 2), "after": round(r["adjusted_avg_rate"], 2),
                    "meta": {
                        "service_type_name": r["service_type_name"],
                        "pct_substantial_or_critical": r["pct_substantial_or_critical"],
                        "n": r["n"],
                        "cqc_rating": r["cqc_rating"],
                    },
                }
                for r in providers
            ],
            "options": {
                "valueFormat": "gbp", "beforeLabel": "Raw average rate", "afterLabel": "Case-mix adjusted",
                "categoryLabel": "Provider", "limit": 15,
                "filterKey": "service_type_name", "filterValues": service_types, "filterDefault": "Residential Care",
                "metaColumns": [
                    {"key": "pct_substantial_or_critical", "label": "% Substantial/Critical needs", "numeric": True, "format": "percent"},
                    {"key": "n", "label": "Records", "numeric": True, "format": "number"},
                    {"key": "cqc_rating", "label": "CQC rating", "numeric": False},
                ],
            },
        },
    }

    localities = s["locality_case_mix_adjustment"]["comparison_table"]
    charts["c3"] = {
        "id": "c3", "type": "comparison",
        "title": "Raw vs case-mix-adjusted average annual cost per person, by locality",
        "caption": "Raw locality cost gap of £3,205 (16.6%) narrows to £1,876 once each locality's complexity-tier mix and share of residential care are accounted for — about a third smaller, but Westborough Central and Northfield remain the two highest-cost areas even after adjustment.",
        "payload": {
            "rows": [
                {
                    "label": r["locality_name"], "before": round(r["raw_avg_annual_cost_per_user"], 2), "after": round(r["adjusted_avg_annual_cost_per_user"], 2),
                    "meta": {
                        "pct_substantial_or_critical": r["pct_substantial_or_critical"],
                        "avg_pct_residential_cost": r["avg_pct_residential_cost"],
                        "n": r["n"],
                    },
                }
                for r in localities
            ],
            "options": {
                "valueFormat": "gbp", "beforeLabel": "Raw avg annual cost/person", "afterLabel": "Case-mix adjusted",
                "categoryLabel": "Locality",
                "metaColumns": [
                    {"key": "pct_substantial_or_critical", "label": "% Substantial/Critical needs", "numeric": True, "format": "percent"},
                    {"key": "avg_pct_residential_cost", "label": "% cost in Residential care", "numeric": True, "format": "percent"},
                    {"key": "n", "label": "People", "numeric": True, "format": "number"},
                ],
            },
        },
    }

    nvc = s["new_vs_continuing_users"]
    by_year = {}
    for r in nvc:
        by_year.setdefault(r["period_year"], {})[r["user_status"]] = r
    years = sorted(by_year.keys())
    charts["c4"] = {
        "id": "c4", "type": "bar",
        "title": "Average annual cost per person, new vs continuing users",
        "caption": "New referrals cost roughly half as much per person as continuing recipients in both years — because they only receive care for part of the year they join — and 2025 saw far more new referrals (1,594) than 2024 (962), which is what pulls the average duration/cost metrics down (Finding 3).",
        "payload": {
            "categories": [str(y) for y in years],
            "series": [
                {"label": "New in year", "values": [round(by_year[y]["New in Year"]["cost_per_user"], 2) for y in years]},
                {"label": "Continuing from before", "values": [round(by_year[y]["Continuing from Before"]["cost_per_user"], 2) for y in years]},
            ],
            "options": {"valueFormat": "gbp", "categoryLabel": "Year"},
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
      {T.render_chart_block(charts['c1'], instance_suffix='-preview')}
      {T.render_chart_block(charts['c2'], instance_suffix='-preview')}
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
      <span class="eyebrow">5. Expenditure Growth Decomposition</span>
      <h2>Volume, duration, mix, price, intensity and fees — exactly broken down</h2>
      <p>Every part below is calculated so it sums exactly to the real £8,253,713.99 change — nothing is rounded to fit. Price and complexity-banding cannot be separated for weekly-fee services (Residential, Nursing, Respite, Reablement), so that effect is reported as a single bundled term.</p>
    </div>
    {T.render_chart_block(charts['c1'])}
  </div>
</section>"""

    providers_section = f"""<section id="providers">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">6. Provider {term('Case-Mix', 'case-mix adjustment')} Analysis</span>
      <h2>Testing whether raw provider comparisons are fair</h2>
      <p>Providers are only ever compared against others delivering the same service type, on a consistent rate unit. The interactive chart above (Headline Numbers) lets you switch service type. The table below names the two Residential Care outliers.</p>
    </div>
    {T.render_chart_block(charts['c2'])}
    {T.render_static_table(["Provider", "Raw rank", "Adjusted rank", "Interpretation"], PROVIDER_CASEMIX_ROWS)}
  </div>
</section>"""

    localities_section = f"""<section id="localities" class="section-alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">7. Locality {term('Case-Mix', 'case-mix adjustment')} Analysis</span>
      <h2>Testing whether raw locality comparisons are fair</h2>
    </div>
    {T.render_chart_block(charts['c3'])}
    {T.render_static_table(["Locality", "Raw rank", "Adjusted rank", "Interpretation"], LOCALITY_CASEMIX_ROWS)}
  </div>
</section>"""

    caseload_section = f"""<section id="caseload">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">8. New vs Continuing Users</span>
      <h2>Why the “duration” effect isn't a real cut in care</h2>
    </div>
    {T.render_chart_block(charts['c4'])}
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
      <h2>What this analysis does not claim — and three things caught before they shipped</h2>
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
    {T.render_chart_gallery(GALLERY_IMAGES)}
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
        approach_section, decomposition_section, providers_section, localities_section,
        caseload_section, recommendations_section, limitations_section,
        gallery_section, technical_section,
    ])


def get_card():
    return {
        "industry": "Local Government",
        "title": "Westborough Council",
        "meta": "Adult social care spending",
        "question": "Is the rising social-care bill down to more people needing care, or care itself costing more?",
        "tags": ["SQL", "Power BI", "Python"],
        "href": "case-studies/westborough.html",
    }
