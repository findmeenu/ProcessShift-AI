"""Generate clearly synthetic AP workflow event data for the demonstration."""
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


def generate(path: Path, n: int = 36, seed: int = 7) -> None:
    random.seed(seed)
    events = []
    base = datetime(2026, 10, 5, 9, 0)
    for idx in range(1, n + 1):
        case_id = f'INV-{idx:03d}'
        timestamp = base + timedelta(hours=idx * 7)
        amount = random.choice([1200, 3900, 8800, 16500, 41000, 92000])
        vendor = f'Synthetic Vendor {idx % 7 + 1}'
        missing = idx % 4 == 0 or idx % 9 == 0
        repeated = idx % 6 == 0
        path_events = [("Received", "AP", "")]
        path_events += [("Validated", "AP", "Missing PO reference" if missing else "")]
        if missing:
            path_events += [("Request clarification", "AP", "Missing required field; awaiting business owner")]
            path_events += [("Clarification received", "Operations", "Business owner clarifies reference")]
            path_events += [("Validated", "AP", "Revalidated after missing information")]
        path_events += [("Awaiting approval", "Operations", "")]
        if repeated:
            path_events += [("Awaiting approval", "Operations", "Second review required")]
        path_events += [("Approved", "Finance", "Human-approved in fictional dataset"),
                        ("Posted", "Finance", "")]
        for step, (activity, team, note) in enumerate(path_events):
            events.append({"case_id": case_id, "activity": activity,
                           "timestamp": timestamp.strftime('%Y-%m-%d %H:%M'), "team": team,
                           "amount_sek": amount, "vendor": vendor, "note": note})
            if step < len(path_events) - 1:
                if activity == "Request clarification":
                    hours = random.randint(19, 68)
                elif activity == "Awaiting approval":
                    hours = random.randint(12, 48)
                else:
                    hours = random.randint(1, 9)
                timestamp += timedelta(hours=hours)
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['case_id', 'activity', 'timestamp', 'team', 'amount_sek', 'vendor', 'note'])
        writer.writeheader()
        writer.writerows(events)


if __name__ == '__main__':
    generate(Path(__file__).resolve().parent / 'demo_invoices.csv')
