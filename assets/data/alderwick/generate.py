"""
Alderwick Reporting Council — synthetic dataset generator.

Deterministic (seeded). Produces the six source CSVs and one compiled JSON
(alderwick_dashboard_data.json) that the interactive dashboard reads.

Every headline figure quoted in the case study is reproduced here by construction:
  - 2,880 audits total, 960 active
  - 38 active audits score >= 65 (the deep-dive threshold)
  - 25 of those 38 sit in three firms
  - supervisory routes: 2 routine / 3 ask / 4 group review / 3 deep-dive
  - SoQM high-risk flags by area: 31/28/25/19/14/11/8/8 % of 36 firm-years
  - 47 remediation actions deferred two or more times
  - score weights: current audit risk 40, firm staffing & quality 35,
    past inspections & fixes 15, market importance 10

Run:  python generate.py
"""
import csv, json, random, datetime, os

SEED = 42
random.seed(SEED)
HERE = os.path.dirname(os.path.abspath(__file__))
AS_OF = datetime.date(2026, 8, 30)

# ---------------------------------------------------------------- firms --
# (id, name, supervisory route, lead supervisor, active audits, priority audits)
FIRMS = [
    ("F01", "Harlow & Vance",      "deep-dive", "Priya Raman",       105, 10),
    ("F02", "Castlereagh Audit",   "deep-dive", "Douglas Mearns",     98,  9),
    ("F03", "Ashby Kellerman",     "deep-dive", "Ruth Odede",         92,  6),
    ("F04", "Thornfield & Co",     "group",     "Martin Yau",         86,  3),
    ("F05", "Corveth Audit Group", "group",     "Elena Poplavska",    84,  3),
    ("F06", "Pellow & Rhodes",     "group",     "Sam Whitfield",      80,  2),
    ("F07", "Ingleby Foulkes",     "group",     "Grace Nkemelu",      78,  1),
    ("F08", "Prentice Meridian",   "ask",       "Tomasz Halloran",    74,  2),
    ("F09", "Whitmark LLP",        "ask",       "Aisha Farooqi",      70,  1),
    ("F10", "Stanmere Partners",   "ask",       "Colin Ebbsworth",    68,  1),
    ("F11", "Dunmore Audit",       "routine",   "Hannah Leung",       63,  0),
    ("F12", "Marrable Quaid",      "routine",   "Peter Okafor",       62,  0),
]
ELEVATED = {"F01", "F02", "F03"}
assert sum(f[4] for f in FIRMS) == 960
assert sum(f[5] for f in FIRMS) == 38

SECTORS = ["Banking", "Insurance", "Listed manufacturing", "Retail group",
           "Energy & utilities", "Technology", "Healthcare", "Real estate",
           "Public interest entity", "Asset management"]

SOQM_AREAS = ["Staffing resources", "Overdue fixes", "Communication",
              "Audit performance", "Risk assessment", "Client acceptance",
              "Leadership", "Ethics"]
# flagged firm-years (out of 36) — reproduces the case-study percentages
SOQM_FLAGS = {"Staffing resources": 11, "Overdue fixes": 10, "Communication": 9,
              "Audit performance": 7, "Risk assessment": 5, "Client acceptance": 4,
              "Leadership": 3, "Ethics": 3}

RISK_SIGNALS = [("Overdue fixes", 36), ("Complex IT dependency", 34),
                ("High-stakes audit", 31), ("Overworked staff", 29),
                ("Low partner input", 27)]
RISK_BASELINE = 20

OWNERS_EXTRA = ["Nadia Suleiman", "Owen Pryce", "Bella Cheng", "Marcus Ilori",
                "Freya Donnelly", "Rajiv Menon", "Louisa Trent", "Karl Adeyemi"]


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def band_for(score):
    if score >= 65: return "deep-dive"
    if score >= 50: return "group"
    if score >= 35: return "ask"
    return "routine"


# ------------------------------------------------------------ audits ----
def gen_components(elevated, priority):
    if priority:
        car = clamp(round(random.gauss(30, 4)), 20, 40)
        fsq = clamp(round(random.gauss(26 if elevated else 21, 4)), 10, 35)
        pif = clamp(round(random.gauss(8, 3)), 0, 15)
        mkt = clamp(round(random.gauss(6, 2)), 0, 10)
        total = car + fsq + pif + mkt
        # nudge up to clear 65 without breaking component ceilings
        while total < 65:
            for name, ceil in (("car", 40), ("fsq", 35), ("pif", 15), ("mkt", 10)):
                v = {"car": car, "fsq": fsq, "pif": pif, "mkt": mkt}[name]
                if v < ceil:
                    add = min(ceil - v, 65 - total)
                    if name == "car": car += add
                    elif name == "fsq": fsq += add
                    elif name == "pif": pif += add
                    else: mkt += add
                    total += add
                if total >= 65: break
    else:
        car = clamp(round(random.gauss(13, 6)), 0, 40)
        fsq = clamp(round(random.gauss(12 if not elevated else 15, 5)), 0, 35)
        pif = clamp(round(random.gauss(5, 3)), 0, 15)
        mkt = clamp(round(random.gauss(4, 2)), 0, 10)
        total = car + fsq + pif + mkt
        if total > 64:  # scale down proportionally, keep <= 64
            factor = 62 / total
            car, fsq, pif, mkt = (round(car * factor), round(fsq * factor),
                                  round(pif * factor), round(mkt * factor))
    return car, fsq, pif, mkt


FLAG_RULES = [
    (lambda c, a: c["car"] >= 30, "Significant judgement in revenue recognition"),
    (lambda c, a: c["car"] >= 26, "Complex accounting estimates"),
    (lambda c, a: a["estimate_heavy"], "Goodwill or asset impairment risk"),
    (lambda c, a: a["it_reliance"] == "High", "Heavy reliance on client IT systems"),
    (lambda c, a: a["group_structure"], "Multi-component group audit"),
    (lambda c, a: c["fsq"] >= 24, "Audit team below planned staffing"),
    (lambda c, a: c["fsq"] >= 20, "Partner involvement hours below plan"),
    (lambda c, a: c["pif"] >= 9, "Repeat finding from a prior inspection"),
    (lambda c, a: c["pif"] >= 7, "Overdue remediation on this engagement"),
]


def gen_audits():
    audits = []
    n = 0
    for fid, name, route, sup, active, prio in FIRMS:
        elevated = fid in ELEVATED
        priority_idx = set(random.sample(range(active), prio))
        for i in range(active):
            n += 1
            is_priority = i in priority_idx
            car, fsq, pif, mkt = gen_components(elevated, is_priority)
            score = car + fsq + pif + mkt
            attrs = {
                "it_reliance": random.choices(["Low", "Medium", "High"],
                    weights=[3, 4, 5] if is_priority else [5, 4, 2])[0],
                "group_structure": random.random() < (0.34 if is_priority else 0.12),
                "estimate_heavy": random.random() < (0.55 if is_priority else 0.18),
            }
            comp = {"car": car, "fsq": fsq, "pif": pif, "mkt": mkt}
            flags = [msg for rule, msg in FLAG_RULES if rule(comp, attrs)]
            flags = flags[:5] if is_priority else flags[:2]
            complexity = "High" if car >= 28 else "Medium" if car >= 17 else "Low"
            audits.append({
                "id": f"AU-{n:04d}",
                "firm_id": fid,
                "sector": random.choice(SECTORS),
                "year": 2025,
                "score": score,
                "components": comp,
                "band": band_for(score),
                "complexity": complexity,
                "it_reliance": attrs["it_reliance"],
                "group_structure": attrs["group_structure"],
                "estimate_heavy": attrs["estimate_heavy"],
                "flags": flags,
            })
    return audits


# --------------------------------------------------- firm capacity -----
def gen_capacity():
    rows = []
    for fid, name, route, sup, active, prio in FIRMS:
        elevated = fid in ELEVATED
        base_turn = random.uniform(19, 24) if elevated else random.uniform(9, 14)
        for yi, year in enumerate((2023, 2024, 2025)):
            turnover = round(clamp(base_turn + random.uniform(-1.5, 1.5)
                                   + (1.2 * yi if elevated else -0.6 * yi), 6, 28), 1)
            rows.append({
                "firm_id": fid, "year": year,
                "headcount": random.randint(140, 620),
                "staff_turnover_pct": turnover,
                "chargeable_hours_per_head": random.randint(1560, 1660) if elevated
                    else random.randint(1390, 1500),
                "partner_hours_per_audit": random.randint(52, 70) if elevated
                    else random.randint(82, 112),
                "vacancy_rate_pct": round(random.uniform(8, 16) if elevated
                    else random.uniform(2, 7), 1),
            })
    return rows


# --------------------------------------------------- quality systems --
def gen_quality():
    rows = []
    firm_years = [(f[0], y) for f in FIRMS for y in (2023, 2024, 2025)]
    group_firms = {f[0] for f in FIRMS if f[2] == "group"}

    def fy_weight(fy):
        fid, year = fy
        w = 6.0 if fid in ELEVATED else 1.8 if fid in group_firms else 0.6
        w *= {2023: 0.7, 2024: 1.0, 2025: 1.3}[year]
        return w

    for area in SOQM_AREAS:
        target = SOQM_FLAGS[area]
        pool = firm_years[:]
        flagged = set()
        while len(flagged) < target and pool:
            weights = [fy_weight(fy) for fy in pool]
            pick = random.choices(pool, weights=weights)[0]
            flagged.add(pick)
            pool.remove(pick)
        for fid, year in firm_years:
            is_flag = (fid, year) in flagged
            if is_flag:
                rating = "Deficient" if random.random() < 0.45 else "Needs improvement"
            else:
                rating = "Effective" if random.random() < 0.8 else "Needs improvement"
            rows.append({"firm_id": fid, "year": year, "area": area,
                         "rating": rating, "high_risk_flag": is_flag})
    return rows


# ------------------------------------------------------ inspections ----
GRADES = ["Good", "Limited improvements needed", "Improvements needed",
          "Significant improvements needed", "Unacceptable"]
INSPECTION_AREAS = ["Revenue", "Estimates & judgements", "Group audit oversight",
                    "Going concern", "Impairment", "Journals & controls",
                    "Engagement quality review"]


def gen_inspections():
    rows = []
    n = 0
    weights = [1.35, 1.3, 1.25, 1.05, 1.05, 1.0, 1.0, 0.9, 0.85, 0.85, 0.6, 0.55]
    total_insp = 426
    raw = [w / sum(weights) * total_insp for w in weights]
    per_firm = [int(x) for x in raw]
    for i in range(total_insp - sum(per_firm)):
        per_firm[i % len(per_firm)] += 1
    assert sum(per_firm) == 426
    for (fid, name, route, sup, active, prio), count in zip(FIRMS, per_firm):
        elevated = fid in ELEVATED
        for _ in range(count):
            n += 1
            year = random.choice([2021, 2022, 2023, 2024, 2025])
            grade = random.choices(GRADES,
                weights=[1, 2, 3, 4, 2] if elevated else [5, 4, 2, 1, 0])[0]
            rows.append({
                "inspection_id": f"IN-{n:04d}", "firm_id": fid, "year": year,
                "area": random.choice(INSPECTION_AREAS), "grade": grade,
                "findings_count": random.randint(3, 12) if elevated else random.randint(0, 5),
            })
    return rows


# ------------------------------------------------------- remediation ---
ACTION_TEMPLATES = [
    ("Staffing resources", "Recruit {n} experienced seniors to close the resourcing gap"),
    ("Staffing resources", "Rebalance engagement teams so no senior runs more than {n} audits"),
    ("Overdue fixes", "Complete root-cause analysis for the prior {area} finding"),
    ("Overdue fixes", "Evidence sign-off on the outstanding {area} remediation"),
    ("Communication", "Formalise escalation route between component and group teams"),
    ("Audit performance", "Re-perform {area} testing on a sample of {n} engagements"),
    ("Risk assessment", "Update the firm risk-assessment methodology for {area}"),
    ("Client acceptance", "Re-run client acceptance checks on {n} higher-risk clients"),
    ("Leadership", "Add a second partner review on public-interest engagements"),
    ("Ethics", "Refresh independence declarations across the {area} portfolio"),
]


def gen_remediation(inspections):
    rows = []
    n = 0
    # spread ~612 actions across inspections, weighted to elevated firms
    insp_pool = []
    for ins in inspections:
        w = 3 if ins["firm_id"] in ELEVATED else 1
        insp_pool += [ins] * w
    deferred_two_plus = 0
    TARGET_DEFERRED = 47
    total = 612
    for k in range(total):
        n += 1
        ins = random.choice(insp_pool)
        area, tmpl = random.choice(ACTION_TEMPLATES)
        raised = datetime.date(2025, 1, 1) + datetime.timedelta(days=random.randint(0, 480))
        due = raised + datetime.timedelta(days=random.choice([60, 90, 90, 120, 150]))
        # decide deferrals
        remaining = TARGET_DEFERRED - deferred_two_plus
        slots_left = total - k
        want_deferred = remaining > 0 and random.random() < (remaining / slots_left) * 1.15
        times_deferred = random.choice([2, 3]) if want_deferred else random.choice([0, 0, 0, 1])
        if times_deferred >= 2:
            deferred_two_plus += 1
        due_effective = due + datetime.timedelta(days=75 * times_deferred)
        # closure
        if random.random() < 0.72:
            close_lag = random.randint(35, 140) + 20 * times_deferred
            closed = raised + datetime.timedelta(days=close_lag)
            closed = None if closed > AS_OF else closed
        else:
            closed = None
        if closed is not None:
            status = "Closed"
        elif due_effective < AS_OF:
            status = "Overdue"
        else:
            status = "Open"
        owner = dict((f[0], f[3]) for f in FIRMS)[ins["firm_id"]] \
            if random.random() < 0.4 else random.choice(OWNERS_EXTRA)
        rows.append({
            "action_id": f"RA-{n:04d}", "inspection_id": ins["inspection_id"],
            "firm_id": ins["firm_id"], "category": area,
            "description": tmpl.format(n=random.choice([2, 3, 4, 5]),
                                       area=random.choice(INSPECTION_AREAS).lower()),
            "owner": owner,
            "raised": raised.isoformat(),
            "due": due_effective.isoformat(),
            "closed": closed.isoformat() if closed else "",
            "status": status,
            "times_deferred": times_deferred,
        })
    # top up / trim to exactly 47 deferred-twice-or-more
    diff = TARGET_DEFERRED - sum(1 for r in rows if r["times_deferred"] >= 2)
    i = 0
    while diff != 0 and i < len(rows):
        r = rows[i]; i += 1
        if diff > 0 and r["times_deferred"] < 2:
            r["times_deferred"] = 2; diff -= 1
        elif diff < 0 and r["times_deferred"] >= 2:
            r["times_deferred"] = 1; diff += 1

    # a task deferred two or more times is, by definition, still outstanding and past due
    for r in rows:
        if r["times_deferred"] >= 2:
            r["status"] = "Overdue"
            r["closed"] = ""
            if datetime.date.fromisoformat(r["due"]) >= AS_OF:
                r["due"] = (AS_OF - datetime.timedelta(days=random.randint(15, 240))).isoformat()

    # reconcile the currently-overdue count to ~18% of all actions (case-study trend endpoint).
    # keep the most-recently-due breaches open; the older ones are treated as since closed.
    target_overdue = round(total * 0.18)
    extra = [r for r in rows if r["status"] == "Overdue" and r["times_deferred"] < 2]
    extra.sort(key=lambda r: r["due"], reverse=True)
    keep_extra = max(0, target_overdue - TARGET_DEFERRED)
    for r in extra[keep_extra:]:
        r["status"] = "Closed"
        due = datetime.date.fromisoformat(r["due"])
        r["closed"] = (due - datetime.timedelta(days=random.randint(3, 40))).isoformat()
    return rows


# ------------------------------------------------------------- build ---
def write_csv(name, rows):
    if not rows:
        return
    path = os.path.join(HERE, name)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"  {name:28s} {len(rows):>5d} rows")


def main():
    audits = gen_audits()
    capacity = gen_capacity()
    quality = gen_quality()
    inspections = gen_inspections()
    remediation = gen_remediation(inspections)

    # sanity checks against the case study
    prio = [a for a in audits if a["score"] >= 65]
    in_top3 = sum(1 for a in prio if a["firm_id"] in ELEVATED)
    assert len(audits) == 960, len(audits)
    assert len(prio) == 38, len(prio)
    assert in_top3 == 25, in_top3
    assert sum(1 for r in remediation if r["times_deferred"] >= 2) == 47

    print("CSV files:")
    write_csv("firms.csv", [dict(id=f[0], name=f[1], supervisory_route=f[2],
              lead_supervisor=f[3], active_audits=f[4], priority_audits=f[5])
              for f in FIRMS])
    write_csv("firm_capacity.csv", capacity)
    write_csv("quality_systems.csv", quality)
    write_csv("audits.csv", [dict(
        audit_id=a["id"], firm_id=a["firm_id"], sector=a["sector"], year=a["year"],
        priority_score=a["score"], current_audit_risk=a["components"]["car"],
        firm_staffing_quality=a["components"]["fsq"],
        past_inspections_fixes=a["components"]["pif"],
        market_importance=a["components"]["mkt"], band=a["band"],
        complexity=a["complexity"], it_reliance=a["it_reliance"],
        group_structure=a["group_structure"], estimate_heavy=a["estimate_heavy"],
        red_flags="; ".join(a["flags"])) for a in audits])
    write_csv("inspections.csv", inspections)
    write_csv("remediation.csv", remediation)

    # compiled JSON for the dashboard
    cap_by_firm = {}
    for r in capacity:
        cap_by_firm.setdefault(r["firm_id"], []).append(r)
    soqm_by_firm = {}
    for r in quality:
        if r["year"] == 2025:
            soqm_by_firm.setdefault(r["firm_id"], []).append(
                {"area": r["area"], "rating": r["rating"], "flag": r["high_risk_flag"]})
    findings_by_firm = {}
    for r in inspections:
        findings_by_firm[r["firm_id"]] = findings_by_firm.get(r["firm_id"], 0) + r["findings_count"]

    firms_json = []
    for fid, name, route, sup, active, prio_n in FIRMS:
        cap = sorted(cap_by_firm[fid], key=lambda x: x["year"])
        latest = cap[-1]
        firms_json.append({
            "id": fid, "name": name, "route": route, "supervisor": sup,
            "active_audits": active, "priority_audits": prio_n,
            "staff_turnover": latest["staff_turnover_pct"],
            "partner_hours_per_audit": latest["partner_hours_per_audit"],
            "chargeable_hours": latest["chargeable_hours_per_head"],
            "open_findings": findings_by_firm.get(fid, 0),
            "capacity": [{"year": c["year"], "turnover": c["staff_turnover_pct"],
                          "chargeable": c["chargeable_hours_per_head"],
                          "partner_hours": c["partner_hours_per_audit"],
                          "headcount": c["headcount"]} for c in cap],
            "soqm": soqm_by_firm.get(fid, []),
        })

    # legends to keep the inlined JSON compact
    flag_legend = []
    for a in audits:
        for fl in a["flags"]:
            if fl not in flag_legend:
                flag_legend.append(fl)
    sector_legend = SECTORS
    band_legend = ["routine", "ask", "group", "deep-dive"]
    lvl_legend = ["Low", "Medium", "High"]

    data = {
        "meta": {"generated": datetime.date.today().isoformat(),
                 "as_of": AS_OF.isoformat(), "total_audits": 2880,
                 "active_audits": 960, "priority_threshold": 65,
                 "weights": {"Current audit risk": 40, "Firm staffing & quality": 35,
                             "Past inspections & fixes": 15, "Market importance": 10}},
        "legends": {"flags": flag_legend, "sectors": sector_legend,
                    "bands": band_legend, "levels": lvl_legend},
        "firms": firms_json,
        "audits": [[a["id"], a["firm_id"], sector_legend.index(a["sector"]),
                    a["score"], a["components"]["car"], a["components"]["fsq"],
                    a["components"]["pif"], a["components"]["mkt"],
                    band_legend.index(a["band"]), lvl_legend.index(a["complexity"]),
                    lvl_legend.index(a["it_reliance"]),
                    1 if a["group_structure"] else 0,
                    1 if a["estimate_heavy"] else 0,
                    [flag_legend.index(f) for f in a["flags"]]] for a in audits],
        "actions": [{"id": r["action_id"], "f": r["firm_id"], "cat": r["category"],
                     "d": r["description"], "o": r["owner"],
                     "due": r["due"], "closed": r["closed"], "st": r["status"],
                     "def": r["times_deferred"]} for r in remediation],
        "soqm_summary": [{"area": a, "flagged": SOQM_FLAGS[a], "total": 36}
                         for a in SOQM_AREAS],
        "risk_signals": [{"signal": s, "rate": r} for s, r in RISK_SIGNALS],
        "risk_baseline": RISK_BASELINE,
    }
    out = os.path.join(HERE, "alderwick_dashboard_data.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(data, fh, separators=(",", ":"))
    print(f"\nJSON: alderwick_dashboard_data.json  ({os.path.getsize(out) // 1024} KB)")
    print("All case-study figures reconciled.")


if __name__ == "__main__":
    main()
