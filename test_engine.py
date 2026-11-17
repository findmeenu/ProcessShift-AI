import unittest
from pathlib import Path
from engine import analyze, load_rows, recommendations, safe_ai_payload, scenario


class ProcessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parent / 'demo_invoices.csv'
        cls.rows = load_rows(path.read_text(encoding='utf-8'))
        cls.stats = analyze(cls.rows, 72)

    def test_demo_has_real_bottlenecks(self):
        self.assertEqual(self.stats['cases'], 36)
        self.assertGreater(self.stats['rework_count'], 0)
        self.assertGreater(self.stats['missing_info_count'], 0)
        self.assertTrue(self.stats['transitions'])

    def test_value_scenario(self):
        output = scenario(self.stats, 18, 25, 350, 400)
        self.assertEqual(output['saved_hours_month'], 26.2)
        self.assertEqual(output['estimated_sek_month'], 10500)

    def test_sensitive_event_fields_excluded_from_model_prompt(self):
        msg = safe_ai_payload(self.stats, recommendations(self.stats))
        self.assertNotIn('Synthetic Vendor', msg)
        self.assertNotIn('INV-001', msg)
        self.assertNotIn('Missing PO reference', msg)

    def test_bad_csv_is_rejected(self):
        with self.assertRaises(ValueError):
            load_rows('case_id,activity\na,b\n')


if __name__ == '__main__':
    unittest.main()
