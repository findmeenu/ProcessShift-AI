"""Reproducible, independently specified synthetic test cases for invoice-field validation."""
import csv
import io

# Expected labels are manually specified fixtures, not inferred from the validator.
FIXTURES = [
    ('INV-001', 'PO-001', 'Ava', False),
    ('INV-002', '', 'Ava', True),
    ('INV-003', 'PO-003', '', True),
    ('', 'PO-004', 'Ava', True),
    ('INV-005', 'PO-005', 'Ava', False),
    ('INV-006', ' ', 'Ava', True),
    ('INV-007', 'PO-007', ' ', True),
    ('INV-008', 'PO-008', 'Ava', False),
    ('INV-009', '', '', True),
    ('INV-010', 'PO-010', 'Ava', False),
    ('INV-011', 'PO-011', 'Ava', False),
    ('INV-012', 'PO-012', 'Ava', False),
]


def flag_missing_fields(invoice_number, po_number, owner):
    return any(not str(x).strip() for x in (invoice_number, po_number, owner))


def evaluate(fixtures=FIXTURES):
    tp = tn = fp = fn = 0
    for invoice, po, owner, expected in fixtures:
        actual = flag_missing_fields(invoice, po, owner)
        if actual and expected: tp += 1
        elif not actual and not expected: tn += 1
        elif actual: fp += 1
        else: fn += 1
    total = tp + tn + fp + fn
    return {'n': total, 'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn,
            'accuracy': (tp + tn) / total if total else 0,
            'precision': tp / (tp + fp) if tp + fp else None,
            'recall': tp / (tp + fn) if tp + fn else None}
