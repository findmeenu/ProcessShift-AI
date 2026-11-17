"""Transparent, auditable process analytics for an AI-assisted transformation demo.

No machine learning model is used for the core metrics. A language model is optional
and is used only for drafting a recommendation from aggregate statistics.
"""
from __future__ import annotations

import csv
import io
import json
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from typing import Any

REQUIRED = {"case_id", "activity", "timestamp", "team", "amount_sek", "vendor", "note"}
DATE_FORMAT = "%Y-%m-%d %H:%M"


def load_rows(text: str) -> list[dict[str, Any]]:
    reader = csv.DictReader(io.StringIO(text.lstrip("\ufeff")))
    if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
        raise ValueError("CSV must contain: " + ", ".join(sorted(REQUIRED)))
    rows: list[dict[str, Any]] = []
    for i, row in enumerate(reader, start=2):
        try:
            when = datetime.strptime(row["timestamp"].strip(), DATE_FORMAT)
            amount = float(row["amount_sek"].replace(",", "."))
            if amount < 0:
                raise ValueError("negative amount")
        except (ValueError, TypeError, AttributeError) as exc:
            raise ValueError(f"Invalid date or amount on CSV line {i}: {exc}") from exc
        if not row["case_id"].strip() or not row["activity"].strip() or not row["team"].strip():
            raise ValueError(f"Missing case ID, activity, or team on line {i}")
        rows.append({"case_id": row["case_id"].strip(), "activity": row["activity"].strip(),
                     "when": when, "team": row["team"].strip(), "amount": amount,
                     "vendor": row["vendor"].strip(), "note": row["note"].strip()})
    if not rows:
        raise ValueError("CSV has no event rows")
    return rows


def percentile(values: list[float], q: float) -> float:
    values = sorted(values)
    if len(values) == 1:
        return values[0]
    p = (len(values) - 1) * q
    left = int(p)
    return values[left] + (values[min(left + 1, len(values) - 1)] - values[left]) * (p - left)


def analyze(rows: list[dict[str, Any]], sla_hours: float = 72) -> dict[str, Any]:
    cases: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        cases[r["case_id"]].append(r)
    case_results = []
    transition_delays: dict[str, list[float]] = defaultdict(list)
    transition_counts = Counter()
    activity_counts = Counter()
    gap_rows = []
    for case_id, events in cases.items():
        events.sort(key=lambda r: r["when"])
        for event in events:
            activity_counts[event["activity"]] += 1
        elapsed = (events[-1]["when"] - events[0]["when"]).total_seconds() / 3600
        repeats = sum(n - 1 for n in Counter(e["activity"] for e in events).values() if n > 1)
        needs_more_info = any("missing" in e["note"].lower() or "clarif" in e["note"].lower() for e in events)
        case_results.append({"case_id": case_id, "lead_hours": round(elapsed, 1), "rework_events": repeats,
                             "missing_info": needs_more_info, "late": elapsed > sla_hours,
                             "amount_sek": events[0]["amount"], "event_count": len(events)})
        for a, b in zip(events, events[1:]):
            hours = (b["when"] - a["when"]).total_seconds() / 3600
            key = f'{a["activity"]} → {b["activity"]}'
            transition_delays[key].append(hours)
            transition_counts[key] += 1
            gap_rows.append({"case_id": case_id, "from": a["activity"], "to": b["activity"],
                             "hours": round(hours, 1), "team_handoff": a["team"] != b["team"]})
    durations = [c["lead_hours"] for c in case_results]
    transitions = [{"transition": name, "count": len(hours), "median_hours": round(statistics.median(hours), 1),
                    "total_hours": round(sum(hours), 1)} for name, hours in transition_delays.items()]
    transitions.sort(key=lambda t: t["total_hours"], reverse=True)
    reworked = sum(c["rework_events"] > 0 for c in case_results)
    missing = sum(c["missing_info"] for c in case_results)
    late = sum(c["late"] for c in case_results)
    return {"cases": len(cases), "events": len(rows), "median_lead_hours": round(statistics.median(durations), 1),
            "p90_lead_hours": round(percentile(durations, .9), 1), "late_count": late,
            "late_pct": round(100 * late / len(cases), 1), "rework_count": reworked,
            "rework_pct": round(100 * reworked / len(cases), 1),
            "missing_info_count": missing, "missing_info_pct": round(100 * missing / len(cases), 1),
            "activity_counts": dict(activity_counts), "transitions": transitions,
            "cases_detail": sorted(case_results, key=lambda c: c["lead_hours"], reverse=True),
            "gaps": sorted(gap_rows, key=lambda g: g["hours"], reverse=True),
            "sla_hours": sla_hours}


def recommendations(result: dict[str, Any]) -> list[dict[str, str]]:
    suggestions = []
    if result["missing_info_count"]:
        suggestions.append({"finding": f'{result["missing_info_count"]} cases flagged missing information',
                            "change": "Require invoice number, PO reference, owner and exception reason at intake; show missing-field prompts.",
                            "human_control": "AP lead approves changes to mandatory fields; employees can override with reason.",
                            "pilot_metric": "% of cases returned for missing information"})
    if result["rework_count"]:
        suggestions.append({"finding": f'{result["rework_count"]} cases include repeated process steps',
                            "change": "Create a structured exception checklist and standard handover summary for reviewers.",
                            "human_control": "Review suggested handovers before any notification; do not auto-approve invoices.",
                            "pilot_metric": "Rework cases / completed cases"})
    if result["transitions"]:
        slow = result["transitions"][0]
        suggestions.append({"finding": f'Largest cumulative wait: {slow["transition"]} ({slow["total_hours"]} hours in sample)',
                            "change": "Test a daily prioritized exception queue and explicit ownership for this handoff.",
                            "human_control": "Team lead approves priority rules and escalations; record a change log.",
                            "pilot_metric": "Median handoff waiting time"})
    return suggestions


def scenario(result: dict[str, Any], manual_minutes_per_case: float, percent_reduction: float,
             monthly_cases: int, hourly_cost_sek: float) -> dict[str, float]:
    """Illustrative prospective scenario, never a measured saving."""
    if not (0 <= percent_reduction <= 100 and manual_minutes_per_case >= 0 and monthly_cases >= 0 and hourly_cost_sek >= 0):
        raise ValueError("Scenario inputs must be nonnegative and reduction 0–100%")
    saved_hours = monthly_cases * manual_minutes_per_case / 60 * percent_reduction / 100
    return {"saved_hours_month": round(saved_hours, 1), "estimated_sek_month": round(saved_hours * hourly_cost_sek),
            "estimated_sek_year": round(saved_hours * hourly_cost_sek * 12)}


def safe_ai_payload(result: dict[str, Any], suggestions: list[dict[str, str]]) -> str:
    """Keep event comments, supplier identifiers, invoice IDs out of external-model prompts."""
    keys = ["cases", "median_lead_hours", "p90_lead_hours", "late_pct", "rework_pct", "missing_info_pct", "sla_hours"]
    return json.dumps({"aggregate_metrics": {k: result[k] for k in keys},
                       "top_transitions": result["transitions"][:4], "analyst_recommendations": suggestions}, indent=2)


def executive_brief(result: dict[str, Any], suggestions: list[dict[str, str]], scenario_result: dict[str, float]) -> str:
    lines = ["PROCESS SHIFT | Invoice exception workflow diagnostic", "",
             "DEMO: all input data is synthetic. No real customer deployment or measured savings.",
             f'Cases: {result["cases"]} | Median lead: {result["median_lead_hours"]} h | P90: {result["p90_lead_hours"]} h',
             f'Late vs {result["sla_hours"]:g} h target: {result["late_pct"]}% | Rework: {result["rework_pct"]}% | Missing-info: {result["missing_info_pct"]}%',
             "", "SUGGESTED PILOT CHANGES"]
    for i, s in enumerate(suggestions, 1):
        lines.extend([f'{i}. Evidence: {s["finding"]}', f'   Change: {s["change"]}',
                      f'   Human check: {s["human_control"]}', f'   KPI: {s["pilot_metric"]}'])
    lines += ["", "ILLUSTRATIVE VALUE SCENARIO (assumptions, not realized results)",
              f'Hours / month: {scenario_result["saved_hours_month"]:,.1f}',
              f'SEK / month: {scenario_result["estimated_sek_month"]:,.0f}',
              "", "PILOT PLAN", "Week 1: observe process, validate baseline with users, agree success metrics.",
              "Week 2: trial intake checklist & prioritized queue with human review.",
              "Weeks 3–4: compare results, interview staff, check errors and adoption.",
              "", "GUARDRAILS", "Use approved or synthetic data only; no automatic approvals or payments.",
              "Aggregate-only AI prompt; verify claims against source metrics; never treat AI suggestions as facts.",
              "", "LIMITATION", "Elapsed intervals include off-hours and cannot by themselves prove the cause of delays."]
    return "\n".join(lines)
