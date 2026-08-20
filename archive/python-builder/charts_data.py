"""
charts_data.py — shared helpers for shaping each project's
07_python/results/*_results.json into chart payloads.

Company-specific chart-shaping functions live inside each company's own
content/{company}.py module (not here), so that module only reshapes numbers
that already exist in its own results file — it never recomputes or invents
a figure, and every value traces back to the same processed dataset that
produced the original static PNG chart it replaces.
"""

import json
import os

COMPANIES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "01_companies",
)

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def load_results(relative_path):
    """relative_path is e.g. 'albion_general_insurance/projects/01_claims_performance/
    07_python/results/albion_results.json'."""
    path = os.path.join(COMPANIES_DIR, relative_path)
    with open(path, encoding="utf-8") as f:
        return json.load(f)["sections"]


def month_label(ym):
    """'2024-01' -> 'Jan 2024'"""
    year, month = ym.split("-")
    return f"{MONTH_NAMES[int(month) - 1]} {year}"
