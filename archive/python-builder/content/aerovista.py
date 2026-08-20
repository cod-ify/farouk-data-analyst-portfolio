"""AeroVista Travel Group — case-study content, in the plain-language schema."""

import charts_data
import templates as T
from templates import term

SLUG = "aerovista"
NAV_PREFIX = "../"

META = {
    "title": "AeroVista Travel Group Case Study — Farouk Yusuf",
    "description": (
        "Flight disruption, delay & operational recovery analytics case study: Excel, SQL, "
        "Python and Power BI analysis of a synthetic airline's delay-propagation, case-mix "
        "route/airport and recovery-cost data."
    ),
}

DISCLAIMER_STRIP = (
    "AeroVista Travel Group is fictional. All data on this page is synthetically generated "
    "for portfolio purposes — see the disclaimer below for detail."
)

DISCLAIMER_BOX = (
    "<strong>Synthetic-data disclaimer:</strong> AeroVista Travel Group is a fictional "
    "airline. Every airport, route, aircraft, flight and figure on this page was generated "
    "for data-analytics portfolio purposes — none of it describes a real airline or its "
    "operational performance, and no figure should be read as representing an actual "
    "carrier. No individual passenger is identified, ranked or scored anywhere in this "
    "project."
)

HERO = {
    "breadcrumb_label": "AeroVista Travel Group",
    "h1": "Flight Disruption, Delay &amp; Operational Recovery Analytics",
    "sub": (
        "Why is on-time performance declining, how much delay actually propagates from a late "
        "inbound aircraft, and do raw route and airport disruption comparisons hold up once "
        "operational complexity is accounted for? An end-to-end analysis across Excel, SQL, "
        "Python and Power BI on 25,204 scheduled flights from a fictional airline's two-year "
        "operation."
    ),
}

SHORT_VERSION = [
    (
        "AeroVista is a made-up airline, used here to practise a real operational-analytics "
        "workflow end to end. Its on-time performance genuinely got worse over two years — and "
        "the data shows that decline is <strong>real, not just bad luck</strong>: it's still "
        "there even after removing the three worst known disruption episodes from the numbers."
    ),
    (
        "Along the way, the same analysis found that cancellations tell the opposite story — "
        "almost entirely explained by an 8-day grounding of one aircraft type — that delay "
        "from a late aircraft only really spreads once a built-in schedule cushion runs out, "
        "and that a small number of long-haul disruptions account for a disproportionate share "
        "of the £20.40m yearly recovery bill."
    ),
]

ANCHOR_NAV = [
    {"id": "findings", "label": "Key Findings"},
    {"id": "problem", "label": "Business Problem"},
    {"id": "dataset", "label": "Dataset"},
    {"id": "approach", "label": "Approach &amp; Tools"},
    {"id": "decomposition", "label": "Delay Decomposition"},
    {"id": "propagation", "label": "Propagation &amp; Turnaround"},
    {"id": "casemix", "label": "Case-Mix Analysis"},
    {"id": "recovery", "label": "Recovery Cost"},
    {"id": "recommendations", "label": "Recommendations"},
    {"id": "limitations", "label": "Limitations &amp; Debugging"},
    {"id": "gallery", "label": "More Charts"},
    {"id": "technical", "label": "Technical Evidence"},
]

KPIS = [
    {"num": "87.72% → 86.18%", "label": "On-time performance, 2024 → 2025", "tag": "significant"},
    {"num": "1.77% → 2.22%", "label": "Cancellation rate, 2024 → 2025 — almost entirely one grounding episode", "tag": "caution"},
    {"num": "0.658", "label": "Minutes of reactionary delay per minute of inbound lateness, once the buffer's used up", "tag": None},
    {"num": "£20.40m", "label": "Total passenger recovery cost, concentrated in a small number of events", "tag": None},
]

FINDINGS = [
    {
        "plain_headline": "On-time performance really did get worse — and it's not just a run of bad weeks.",
        "plain_body": "The share of flights arriving broadly on time fell over the two years covered by this data. Even after removing the three known bad-weather and grounding episodes from the numbers, the decline is still there — this is a genuine underlying trend, not one-off bad luck.",
        "figure_line": "On-time performance: 87.72% (2024) &rarr; 86.18% (2025) &middot; Still falls to 86.25% (&minus;1.52pp) even with the 3 disruption episodes removed",
        "technical_detail": f"Two-proportion z-test on on-time performance: z=&minus;3.57, {term('p=0.0004', 'p-value')} ({term('significant', 'statistically significant')}). Sensitivity check excluding all 3 disruption-episode windows: on-time performance still falls from 87.77% to 86.25%.",
    },
    {
        "plain_headline": "Cancellations went up too — but almost all of that is one grounding, not the airline getting worse overall.",
        "plain_body": "The share of flights cancelled rose over the same period. But once you take out an 8-day grounding of one aircraft type, that rise almost completely disappears — this is really a story about one fleet problem, not a general decline.",
        "figure_line": "Cancellation rate: 1.77% (2024) &rarr; 2.22% (2025) &middot; Falls to essentially flat (&minus;0.03pp) once the 8-day Turboprop grounding window is excluded",
        "technical_detail": f"Two-proportion z-test: z=2.56, {term('p=0.0106', 'p-value')} ({term('significant', 'statistically significant')}). Sensitivity check excluding the 3 disruption episodes turns the +0.45pp headline rise into &minus;0.03pp.",
    },
    {
        "plain_headline": "Flight delay has three roughly-sized causes — there's no single lever to pull.",
        "plain_body": "About half of all delay minutes come from things outside the airline's control, like weather and air-traffic congestion. Just under a third come from things the airline could fix directly, like crew and maintenance. The rest is delay inherited from a previous late flight.",
        "figure_line": "External: 50.3% &middot; Airline-controllable: 31.7% &middot; Reactionary (inherited from a late aircraft): 17.9% of all delay minutes",
        "technical_detail": f"Exact {term('decomposition', 'decomposition')} of departure-delay minutes into three causal categories, verified independently in SQL and Python — 24,687 of 24,702 completed flights reconcile exactly (the remaining 15 are a documented data-quality exclusion, not a defect).",
    },
    {
        "plain_headline": "Cancellations are almost never about the weather — they're almost always something the airline could have controlled.",
        "plain_body": "Unlike delay, which is roughly half outside anyone's control, cancellations are overwhelmingly down to things inside the airline: maintenance issues, crew availability and ground handling. Weather barely features at all.",
        "figure_line": "Weather causes just 0.6% of cancellations &middot; The remaining 99.4% are airline-controllable (Technical/Maintenance 40.4%, Other 21.7%, Ground Handling 18.7%, Crew 18.5%)",
        "technical_detail": None,
    },
    {
        "plain_headline": "A late incoming plane doesn't automatically make the next flight late too — there's a built-in cushion that soaks up the first bit of lateness.",
        "plain_body": "When a plane arrives late, the schedule has some slack built in to make up time before it flies again. Small delays get absorbed almost completely. It's only once a delay runs past about 15 minutes that it starts spilling over into the next flight, and once it's past an hour, nearly all of it carries through.",
        "figure_line": "Inbound delay under 15 min: fully absorbed, 0 minutes carries over on average &middot; Inbound delay over 60 min: 63.7 minutes carries over on average",
        "technical_detail": f"{term('Regression', 'regression')} of reactionary delay on inbound-aircraft lateness (legs where the inbound aircraft was already late, n=7,072): slope=0.658 minutes per minute, {term('R²', 'r-squared')}=0.863, 95% {term('CI', 'confidence interval')} on the slope 0.652–0.664.",
    },
    {
        "plain_headline": "The route that looks worst on paper is mostly just a very long flight — but a different route is a genuine problem case.",
        "plain_body": "The five worst-performing routes for on-time arrival are all long-haul flights from the airline's busiest hub — no surprise, since longer flights pick up more weather and air-traffic delay along the way. Once that's accounted for, the single worst route on paper turns out to be almost entirely explained by its length. But one other route stood out as genuinely underperforming, worse than its own difficulty would predict.",
        "figure_line": "Worst route on paper (Northgate&ndash;Solmara-Vantage): 69.67% raw on-time rate, only &minus;0.65pp gap once route difficulty is accounted for &middot; Northgate&ndash;Bellhaven Intl: &minus;5.46pp gap, the worst in the network &mdash; a genuine outlier",
        "technical_detail": f"{term('Case-mix adjustment', 'case-mix adjustment')}: expected-vs-actual residual {term('regression', 'regression')} on distance, haul type and daily congestion (not route fixed effects, since distance and haul type are fixed within a route), n=24,702 flights across 55 routes, pseudo-{term('R²', 'r-squared')}=0.0129. Of the worst-raw-OTP quartile (14 routes), 8 are genuine outliers and 6 are explained by complexity.",
    },
    {
        "plain_headline": "The busiest airport looks bad on delay — but that's mostly just because it's busy; two quieter airports have a real problem.",
        "plain_body": "The busiest hub airport has some of the highest average delays in the network. But once you account for how much traffic and complexity it handles, most of that delay is explained away — it's simply a very complex airport to run. Two much smaller, quieter airports show high delays that aren't explained by complexity at all, which makes them the more genuine concern.",
        "figure_line": "Northgate International (busiest hub, 6,254 flights): raw rank 2nd-highest delay &rarr; adjusted rank 8th &middot; Porthaven &amp; Millbeck: stay 1st and 2nd highest delay even after adjustment",
        "technical_detail": f"{term('Case-mix adjustment', 'case-mix adjustment')}: {term('regression', 'regression')} of departure delay on haul-type mix and daily congestion, n=24,702, {term('R²', 'r-squared')}=0.0025 &mdash; a low value, so this adjustment is read as directional, not precise.",
    },
    {
        "plain_headline": "A small number of big, long-haul disruptions account for a disproportionate share of the total recovery bill.",
        "plain_body": "Most disruption events are short or medium-haul flights, and together they account for most of the total cost simply because there are so many of them. But long-haul disruptions, while rare, cost far more each time — because compensation, rebooking and hotel costs all scale up with a much bigger number of passengers on board.",
        "figure_line": "Long-haul disruptions: just 21 of 521 events (4%) but £161,627 average cost each &middot; Medium-haul: the largest total-cost bucket at £12.38m of £20.40m (61%), on volume alone",
        "technical_detail": None,
    },
]

PROBLEM_PARAGRAPHS = [
    (
        "AeroVista is a fictional airline whose delays, cancellations, passenger disruption and "
        "recovery costs have been rising. Management wanted a straight answer to several "
        "questions: what actually causes delay, how much of it is inherited from a previous "
        "late flight rather than caused directly, whether specific routes or airports create "
        "disproportionate disruption once operational complexity is accounted for, how much "
        "disruption is genuinely outside the airline's control, what drives cancellations, and "
        "where Operations should intervene first."
    ),
    (
        "One rule was non-negotiable: <strong>no route or airport comparison could be presented "
        "as a simple ranking</strong> without first checking whether it still held up once "
        "distance, haul type and traffic complexity were taken into account."
    ),
]

STAKEHOLDERS = [
    {"role": "Director of Operations", "need": "Needed to know whether the on-time-performance decline is a broad structural trend or a handful of bad episodes, to decide between a capacity review and a targeted fix."},
    {"role": "Fleet &amp; Maintenance Planning", "need": "Needed to understand how concentrated the September 2025 cancellation spike was in a single fleet type, and what that means for maintenance scheduling."},
    {"role": "Network Planning", "need": "Needed a fair, case-mix-aware basis for route and airport performance conversations, without a raw ranking that ignores complexity differences."},
    {"role": "Customer Experience / Finance", "need": "Needed to know where the £20.40m annual recovery cost concentrates, to prioritise the highest-impact disruption types."},
]

DATASET_ROWS = [
    [{"value": "Coverage"}, {"value": "24 airports (3 Major Hub, 8 Regional, 9 Small, 4 International), 55 routes"}],
    [{"value": "Period"}, {"value": "January 2024 – December 2025 (24 months)"}],
    [{"value": "Fleet"}, {"value": "55 aircraft across 4 types (Regional Turboprop, 2 Narrowbody types, Widebody)", "num": True}],
    [{"value": "Scheduled flights"}, {"value": "25,204 (25,242 unique, before a known duplication issue was cleaned)", "num": True}],
    [{"value": "Delay-cause events"}, {"value": "5,743 (one row per flight × triggered delay cause)", "num": True}],
    [{"value": "Turnaround events"}, {"value": "12,275 (aircraft ground-turn records)", "num": True}],
    [{"value": "Passenger disruption records"}, {"value": "521 (cancellations plus long delays/diversions)", "num": True}],
    [{"value": "Airport-day weather/congestion records"}, {"value": "17,544", "num": True}],
]

TOOLS = [
    {"name": "Excel", "desc": "A 10-sheet workbook where every KPI that can be computed live is a genuine formula or PivotTable — route and airport case-mix figures are imported as clearly-labelled reference tables instead."},
    {"name": "SQL", "desc": "Six database queries covering KPIs, delay causes, route/airport performance, turnaround propagation, cancellations and fleet use — checked against a real database."},
    {"name": "Python", "desc": "The statistical work: splitting delay into its exact causes, modelling how delay spreads from a late inbound aircraft, and testing whether route and airport performance differences hold up once complexity is accounted for."},
    {"name": "Power BI", "desc": "A full dashboard design — the data model, the DAX measures and the page layouts — ready to build, including a check for two ways the numbers could be modelled wrong before they reached a dashboard."},
]

CASEMIX_ROWS = [
    [{"value": "Northgate&ndash;Solmara-Vantage"}, {"value": "Worst raw OTP (69.67%)"}, {"value": "&minus;0.65pp gap"}, {"value": "Mostly explained by being a very long route (6,223.8km) — one of the network's longest"}],
    [{"value": "Northgate&ndash;Bellhaven Intl"}, {"value": "3rd-worst raw OTP (72.25%)"}, {"value": "&minus;5.46pp gap (worst in the network)"}, {"value": "A genuine outlier — not explained by distance, haul type or congestion"}],
    [{"value": "Northgate International (airport)"}, {"value": "2nd-highest raw delay"}, {"value": "Drops to 8th once adjusted"}, {"value": "Mostly explained by being the network's busiest, most complex hub (6,254 flights)"}],
    [{"value": "Porthaven &amp; Millbeck (airports)"}, {"value": "1st &amp; 2nd highest raw delay"}, {"value": "Stay 1st &amp; 2nd once adjusted"}, {"value": "Not explained by complexity — genuine operational review warranted"}],
]

RECOMMENDATIONS = [
    "<strong>Treat the on-time-performance decline and the cancellation-rate rise as two separate problems with two separate responses.</strong> The former is structural (network growth vs. capacity) and needs an Operations-capacity review; the latter is concentrated in the September 2025 Turboprop grounding and needs a fleet-maintenance-scheduling review, not a network-wide policy change.",
    "<strong>Prioritise controllable causes for the cancellation problem specifically</strong> — 99.4% of cancellations are airline-controllable, essentially none weather-driven, unlike delay (which is half external).",
    "<strong>Investigate Northgate&ndash;Bellhaven Intl specifically</strong>, using its case-mix-adjusted gap (&minus;5.46pp, the worst in the network) as the concrete test case — not explained by distance, haul type or congestion, unlike most other worst-raw-OTP routes.",
    "<strong>Review scheduled turnaround buffers on routes and aircraft with frequent inbound delays beyond 15 minutes</strong> — the buffer absorbs almost all reactionary delay up to that point, so a modest buffer increase on the most delay-prone rotations would disproportionately reduce reactionary delay.",
    "<strong>Do not treat Northgate International's high raw departure delay as a standalone airport problem</strong> — most of it is explained by being the network's busiest, most complex hub; Porthaven and Millbeck's delay positions are not explained by complexity and warrant more direct operational review despite their smaller size.",
]

LIMITATIONS_DEBUG = [
    "<strong>An early version of the schedule generator produced 7x too many flights.</strong> Every aircraft was made to fly at its maximum physical capacity regardless of its route's target frequency, producing 183,772 flights against a ~25,000 target and an unrealistic 41% on-time performance. Diagnosed by comparing actual vs target flight counts per route, and fixed by deriving each aircraft's flight count and daily operating probability jointly from the route's own target.",
    "<strong>A missing turnaround buffer made delay propagation suspiciously perfect.</strong> An early version of the propagation logic used the already-padded scheduled turnaround time as the absorbable buffer — leaving mechanically no slack to absorb anything, so a late aircraft's delay passed straight through 1-for-1 (slope=1.000, R²=0.999, an unrealistically clean result). Fixed by letting ground crews compress a turnaround under pressure down to the aircraft type's minimum feasible time — after which the relationship became realistic and buffered (slope 0.658, R²=0.863).",
    "<strong>A route fairness check, copied from a previous project's supplier fairness check, produced meaningless results.</strong> It tried to control for each individual route while also controlling for that route's distance — but a route's distance never changes from flight to flight, so the two were fighting over the same information and the model explained almost nothing (rank changes of up to 33 out of 55 routes). Recognising that the earlier method didn't transfer, it was redesigned from scratch as a genuinely different comparison: predicting each flight's expected on-time chance from its distance and complexity alone, then comparing each route's actual performance to that expectation.",
]

LIMITATIONS_STANDARD = [
    "<strong>Made-up data throughout</strong> — every figure describes patterns in a generated dataset built for this portfolio, not a real airline.",
    "<strong>Association, not proof of cause</strong> — the route and airport comparisons account for known differences in distance, haul type and congestion, but don't prove a route or airport directly causes worse performance.",
    "<strong>The route fairness adjustment explains only a modest part of the pattern</strong> (pseudo-R²=0.013) — a deliberate trade-off, since the simpler design it replaced couldn't isolate a route's real effect at all.",
    "<strong>The airport fairness adjustment explains very little of the pattern in delay</strong> (R²=0.0025) — useful as a directional signal, not as a precise correction.",
    "<strong>15 completed flights out of 24,702 were excluded</strong> from the delay-cause reconciliation check because of a known data-quality issue — nothing else is affected.",
    "<strong>Compensation, rebooking and care costs use a simplified, purely synthetic cost model</strong> — not a reproduction of any real regulatory compensation scheme.",
]

TECH_CARDS = [
    {"heading": "03_excel/", "items": ["build_excel_workbook.py — reproducible COM-automation build script", "aerovista_disruption_analysis.xlsx — 10 sheets, 4 charts, 3 PivotTables, 22 Excel Tables"]},
    {"heading": "04_sql/", "items": ["01_kpi_analysis.sql &middot; 02_delay_cause_decomposition.sql", "03_route_airport_performance.sql &middot; 04_turnaround_propagation_analysis.sql", "05_cancellation_passenger_recovery_analysis.sql &middot; 06_fleet_utilisation_analysis.sql"]},
    {"heading": "07_python/", "items": ["aerovista_disruption_analysis.py — full analysis script", "aerovista_disruption_analysis.ipynb — narrated notebook", "results/aerovista_results.json — machine-readable results"]},
    {"heading": "05_power_bi/documentation/", "items": ["dashboard_specification.md — 4-page dashboard design", "dax_measures.md — full DAX measure library", "data_model.md — data model design, incl. grain-consistency audit"]},
]

GALLERY_IMAGES = [
    {"src": "../assets/images/aerovista/01_distribution_shape.png", "alt": "Histogram showing departure delay is right-skewed", "caption": "Departure delay is right-skewed — most flights depart close to on time, with a long tail of larger delays."},
]

FOOTER_DISCLAIMER = "AeroVista Travel Group is fictional; all data is synthetic."

# Small, static airport code → name lookup (24 airports, from the project's own reference
# data) used only to make route/airport labels readable — no figures are derived from it.
AIRPORT_NAMES = {
    "MER": "Merrivale Central", "CAS": "Castellan Gateway", "NOR": "Northgate International",
    "FEN": "Fenwick Regional", "BRA": "Bramcote Field", "DUN": "Dunraven", "ASH": "Ashcombe Regional",
    "KIR": "Kirriemuir", "POR": "Porthaven", "SIL": "Silverdale", "GRE": "Greybourne", "MIL": "Millbeck",
    "SAN": "Sandpiper Cove", "THO": "Thornhaven", "LAR": "Larkspur Fell", "RED": "Redmarsh",
    "COP": "Copperfield", "WRE": "Wrenfield", "HOL": "Hollowbrook", "FAR": "Farrow Down",
    "SOL": "Solmara-Vantage", "KES": "Kestria Skyport", "BEL": "Bellhaven Intl", "LPN": "Norlandia Nordport",
}


def _load():
    return charts_data.load_results(
        "aerovista_travel_group/projects/01_flight_disruption_recovery/07_python/results/aerovista_results.json"
    )


def get_charts():
    s = _load()
    charts = {}

    monthly = s["monthly_trend"]
    charts["c1"] = {
        "id": "c1", "type": "line",
        "title": "Monthly on-time performance and cancellation rate, 2024–2025",
        "caption": "A sharp cancellation spike in September 2025 (the Turboprop grounding) sits on top of a steadier, more gradual on-time-performance decline across the full two years — two different problems, visible in one chart.",
        "payload": {
            "xLabels": [charts_data.month_label(m["year_month"]) for m in monthly],
            "series": [
                {"label": "On-time performance", "values": [round(m["otp15_pct"], 2) for m in monthly], "valueFormat": "percent"},
                {"label": "Cancellation rate", "values": [round(m["cancellation_rate_pct"], 2) for m in monthly], "valueFormat": "percent", "axis": "secondary"},
            ],
            "options": {
                "annotations": [
                    {"x": "Jul 2024", "label": "ATC staffing crisis"},
                    {"x": "Jan 2025", "label": "Storm Brannigan"},
                    {"x": "Sep 2025", "label": "Turboprop AD grounding"},
                ],
            },
        },
    }

    dd = s["delay_decomposition"]["by_category_pct"]
    charts["c2"] = {
        "id": "c2", "type": "bar",
        "title": "What causes delay minutes",
        "caption": "No single cause dominates — roughly half of all delay is outside the airline's control, a third is within its control, and the rest is inherited from a previous late aircraft.",
        "payload": {
            "categories": ["External", "Airline Controllable", "Reactionary"],
            "series": [{
                "label": "% of delay minutes",
                "values": [
                    round(dd["external_minutes"], 1),
                    round(dd["controllable_minutes"], 1),
                    round(dd["reactionary_minutes"], 1),
                ],
            }],
            "options": {"valueFormat": "percent", "categoryLabel": "Delay category"},
        },
    }

    bands = s["propagation_analysis"]["by_inbound_delay_band"]
    charts["c3"] = {
        "id": "c3", "type": "bar",
        "title": "Average reactionary delay by inbound-aircraft lateness band",
        "caption": "Inbound delay under 15 minutes is almost fully absorbed by the scheduled turnaround buffer (average reactionary delay: 0 minutes). Once inbound lateness passes 60 minutes, the buffer is exhausted and delay passes through almost 1-for-1 (63.7 minutes on average).",
        "payload": {
            "categories": [r["inbound_delay_band"] for r in bands],
            "series": [{"label": "Avg reactionary delay (minutes)", "values": [round(r["avg_reactionary_delay"], 1) for r in bands]}],
            "options": {"categoryLabel": "Inbound delay band"},
        },
    }

    route_tbl = s["route_case_mix"]["table"]
    worst15 = sorted(route_tbl, key=lambda r: r["raw_rank"])[:15]
    charts["c4"] = {
        "id": "c4", "type": "comparison",
        "title": "Raw vs case-mix-expected on-time performance, worst 15 routes",
        "caption": "Northgate–Solmara-Vantage (raw-worst) has only a small case-mix gap — mostly explained by being a very long route. Northgate–Bellhaven Intl has the largest negative gap in the entire network — a genuine outlier, not explained by distance, haul type or congestion.",
        "payload": {
            "rows": [
                {
                    "label": f"{AIRPORT_NAMES.get(r['origin_code'], r['origin_code'])}–{AIRPORT_NAMES.get(r['dest_code'], r['dest_code'])}",
                    "before": round(r["raw_otp_pct"], 2), "after": round(r["expected_otp_pct"], 2),
                    "meta": {"haul_type": r["haul_type"], "distance_km": r["distance_km"], "n_flights": r["n_flights"]},
                }
                for r in worst15
            ],
            "options": {
                "valueFormat": "percent", "beforeLabel": "Raw OTP", "afterLabel": "Case-mix expected OTP",
                "categoryLabel": "Route", "limit": 15,
                "metaColumns": [
                    {"key": "haul_type", "label": "Haul type", "numeric": False},
                    {"key": "distance_km", "label": "Distance (km)", "numeric": True, "format": "number"},
                    {"key": "n_flights", "label": "Flights", "numeric": True, "format": "number"},
                ],
            },
        },
    }

    haul_order = ["Short", "Medium", "Long"]
    haul_rows = {r["haul_type"]: r for r in s["passenger_recovery"]["by_haul_type"]}
    ordered = [haul_rows[h] for h in haul_order]
    charts["c5"] = {
        "id": "c5", "type": "bar",
        "title": "Passenger recovery cost by haul type and cost component",
        "caption": "Medium-haul disruptions are the largest total-cost bucket simply on volume; long-haul disruptions are rare but average far more per event (£161,627), driven by full-widebody cancellations where compensation, rebooking and care costs all scale with a much larger passenger count.",
        "payload": {
            "categories": haul_order,
            "series": [
                {"label": "Compensation", "values": [round(r["total_compensation"], 2) for r in ordered]},
                {"label": "Rebooking", "values": [round(r["total_rebooking"], 2) for r in ordered]},
                {"label": "Care (hotel/meals)", "values": [round(r["total_care"], 2) for r in ordered]},
            ],
            "options": {"valueFormat": "gbp", "categoryLabel": "Haul type"},
        },
    }

    causes = s["cancellation_analysis"]["by_cause"]
    charts["c6"] = {
        "id": "c6", "type": "bar",
        "title": "Cancellation cause breakdown",
        "caption": "Cancellations are a near-total airline-controllable story — Weather accounts for just 0.6%, the opposite pattern from delay (which is half external).",
        "payload": {
            "categories": [r["cancellation_reason_name"] for r in causes],
            "series": [{"label": "% of cancellations", "values": [round(r["pct"], 2) for r in causes]}],
            "options": {"horizontal": True, "valueFormat": "percent", "categoryLabel": "Cause"},
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
      <span class="eyebrow">5. Delay-Cause Decomposition</span>
      <h2>What actually causes delay — and what causes cancellations</h2>
      <p>Every completed flight's departure delay is, by construction, the exact sum of its logged delay-event minutes across three categories — verified independently in SQL and Python (24,687 of 24,702 completed flights reconcile exactly; the remaining 15 are a documented data-quality exclusion).</p>
    </div>
    <div class="two-col">
      {T.render_chart_block(charts['c2'])}
      {T.render_chart_block(charts['c6'])}
    </div>
  </div>
</section>"""

    propagation_section = f"""<section id="propagation">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">6. Turnaround Performance &amp; Delay Propagation</span>
      <h2>How much of a late inbound aircraft's delay actually reaches the next departure</h2>
    </div>
    {T.render_chart_block(charts['c3'])}
  </div>
</section>"""

    casemix_section = f"""<section id="casemix" class="section-alt">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">7. Route &amp; Airport {term('Case-Mix', 'case-mix adjustment')} Analysis</span>
      <h2>Testing whether raw route and airport comparisons are fair</h2>
      <p>The interactive chart above (Headline Numbers) shows the worst 15 routes by raw on-time performance next to what their own distance, haul type and congestion profile would predict. The table below names the specific outliers.</p>
    </div>
    {T.render_static_table(["Route / Airport", "Raw position", "Case-mix result", "Interpretation"], CASEMIX_ROWS)}
  </div>
</section>"""

    recovery_section = f"""<section id="recovery">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">8. Passenger Disruption &amp; Recovery Cost</span>
      <h2>Where the £20.40m recovery cost concentrates</h2>
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
      <h2>What this analysis does not claim — and three bugs caught before they shipped</h2>
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
        approach_section, decomposition_section, propagation_section, casemix_section,
        recovery_section, recommendations_section, limitations_section,
        gallery_section, technical_section,
    ])


def get_card():
    return {
        "industry": "Travel",
        "title": "AeroVista Travel Group",
        "meta": "Flight delay & disruption analytics",
        "question": "Why is on-time performance declining, and how much delay actually spreads from one late aircraft?",
        "tags": ["Python", "SQL", "Excel"],
        "href": "case-studies/aerovista.html",
    }
