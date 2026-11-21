"""Transparent investment comparison. All financial inputs are hypothetical."""
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class Option:
    name: str
    setup_sek: float
    annual_license_sek: float
    annual_support_sek: float
    minutes_saved_per_invoice: float
    adoption: float
    residual_error_rate: float
    risk: str
    evidence_needed: str


def options_default():
    return [
        Option('Process redesign', 35000, 0, 12000, 2, .80, .07, 'Low: adoption and inconsistent procedures', 'Time-and-motion study; staff adoption'),
        Option('Rules-based automation', 125000, 18000, 25000, 5, .75, .045, 'Medium: integration and exception coverage', 'ERP integration test; false-positive review'),
        Option('AI-assisted automation', 260000, 85000, 55000, 8, .65, .035, 'High: data privacy, output reliability, oversight', 'Security approval; blinded evaluation; human review'),
    ]


def compare(options, monthly_volume=350, minutes_baseline=18, hourly_cost=400,
            baseline_error_rate=.10, cost_per_error=180, discount_rate=.10, years=3):
    """Discounted incremental benefits versus doing nothing. Savings are capacity value, not cash."""
    if monthly_volume < 0 or minutes_baseline < 0 or hourly_cost < 0 or cost_per_error < 0 or not 0 <= baseline_error_rate <= 1 or discount_rate < 0 or years < 1:
        raise ValueError('Invalid financial assumptions')
    rows = []
    for o in options:
        if min(o.setup_sek, o.annual_license_sek, o.annual_support_sek, o.minutes_saved_per_invoice) < 0 or not 0 <= o.adoption <= 1 or not 0 <= o.residual_error_rate <= 1:
            raise ValueError('Invalid option inputs')
        effective_minutes = min(o.minutes_saved_per_invoice, minutes_baseline) * o.adoption
        annual_capacity = monthly_volume * 12 * effective_minutes / 60 * hourly_cost
        annual_avoided_errors = monthly_volume * 12 * max(0, baseline_error_rate - o.residual_error_rate) * o.adoption * cost_per_error
        annual_benefit = annual_capacity + annual_avoided_errors
        annual_cost = o.annual_license_sek + o.annual_support_sek
        net_annual = annual_benefit - annual_cost
        npv = -o.setup_sek + sum(net_annual / ((1 + discount_rate) ** t) for t in range(1, years + 1))
        total_cost = o.setup_sek + annual_cost * years
        total_benefit = annual_benefit * years
        roi = (total_benefit - total_cost) / total_cost * 100 if total_cost else None
        payback = o.setup_sek / net_annual * 12 if net_annual > 0 else None
        rows.append({**asdict(o), 'annual_capacity_value_sek': round(annual_capacity),
                     'annual_error_avoidance_sek': round(annual_avoided_errors),
                     'annual_benefit_sek': round(annual_benefit), 'annual_recurring_cost_sek': round(annual_cost),
                     'net_annual_sek': round(net_annual), 'npv_sek': round(npv),
                     'roi_pct': round(roi, 1) if roi is not None else None,
                     'payback_months': round(payback, 1) if payback is not None else None})
    return rows


def recommend(rows):
    """Choose highest positive modeled NPV, otherwise no investment; subject to validation gates."""
    eligible = [r for r in rows if r['npv_sek'] > 0]
    if not eligible:
        return None
    return max(eligible, key=lambda r: r['npv_sek'])


def sensitivity(options, monthly_volume, minutes_baseline, hourly_cost, baseline_error_rate, cost_per_error, discount_rate, years):
    cases = []
    for name, volume_factor, adoption_factor in [('Conservative', .7, .7), ('Base', 1, 1), ('Optimistic', 1.3, 1.1)]:
        adjusted = [Option(**{**asdict(o), 'adoption': min(1, o.adoption * adoption_factor)}) for o in options]
        for row in compare(adjusted, monthly_volume * volume_factor, minutes_baseline, hourly_cost,
                           baseline_error_rate, cost_per_error, discount_rate, years):
            cases.append({'scenario': name, 'option': row['name'], 'npv_sek': row['npv_sek']})
    return cases


def report(rows, selected, sample, assumptions, scenarios):
    lines = ['PROCESSSHIFT 2.0 | TECHNOLOGY INVESTMENT DECISION BRIEF',
             'SYNTHETIC CASE STUDY — NOT A REAL CLIENT ENGAGEMENT', '',
             'DECISION QUESTION', 'Which invoice-process improvement should be piloted, if any?', '',
             'OBSERVED IN SYNTHETIC EVENT LOG',
             f"{sample['cases']} cases; median lead time {sample['median_lead_hours']} hours; "
             f"{sample['late_pct']}% beyond target; {sample['rework_pct']}% with repeated activities.",
             'These event-log observations do not establish root causes or actual manual handling time.', '',
             'MODELING ASSUMPTIONS (not measured)',
             *[f'{k}: {v}' for k, v in assumptions.items()], '', 'OPTIONS']
    for r in rows:
        lines.append(f"- {r['name']}: setup SEK {r['setup_sek']:,.0f}; annual operating SEK {r['annual_recurring_cost_sek']:,.0f}; "
                     f"3-year-model NPV SEK {r['npv_sek']:,.0f}; ROI {r['roi_pct']}%; "
                     f"payback {r['payback_months'] if r['payback_months'] is not None else 'not reached'} months")
        lines.append(f"  Key risk: {r['risk']}; validation: {r['evidence_needed']}")
    lines.extend(['', 'PROVISIONAL RECOMMENDATION',
                  f"Pilot {selected['name']} because it has the highest positive modeled NPV." if selected else
                  'Do not invest under these assumptions; validate the baseline and revisit alternatives.',
                  'This is a modeled decision, not a demonstrated outcome or implementation approval.', '',
                  'SCENARIO TEST (NPV SEK)'])
    lines += [f"- {s['scenario']} | {s['option']}: {s['npv_sek']:,.0f}" for s in scenarios]
    lines += ['', 'PILOT AND GOVERNANCE',
              '1. Confirm real baseline with AP staff; validate volumes, handling minutes, exception costs and working hours.',
              '2. Obtain security/privacy and integration approvals; retain human invoice approval.',
              '3. Randomize or match pilot and control cases; measure end-to-end time, rework, errors and employee adoption.',
              '4. Review results and update assumptions before any scaled investment.', '',
              'LIMITATIONS',
              'Synthetic events; hypothetical investment prices, adoption, labor capacity and error avoidance.',
              'Capacity value is not necessarily cash savings. ROI excludes tax and financing effects.',
              'No independent customer deployment or measured business impact is claimed.']
    return '\n'.join(lines)
