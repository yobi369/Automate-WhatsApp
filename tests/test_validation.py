import unittest

from validation import normalize_phone, validate_daily_time, validate_message, validate_recipients


class ValidationTests(unittest.TestCase):
    def test_normalizes_whitespace(self):
        self.assertEqual(normalize_phone("  +254712345678 "), "+254712345678")

    def test_rejects_local_number(self):
        with self.assertRaises(ValueError):
            normalize_phone("0712345678")

    def test_rejects_duplicate_recipients(self):
        with self.assertRaises(ValueError):
            validate_recipients("+254712345678, +254712345678")

    def test_rejects_empty_recipient_list(self):
        with self.assertRaises(ValueError):
            validate_recipients(" , ")

    def test_rejects_empty_message(self):
        with self.assertRaises(ValueError):
            validate_message("   ")

    def test_rejects_unknown_template_field(self):
        with self.assertRaises(ValueError):
            validate_message("Hello {customer}")

    def test_accepts_name_placeholder(self):
        self.assertEqual(validate_message("Hello {name}"), "Hello {name}")

    def test_validates_24_hour_time(self):
        self.assertEqual(validate_daily_time("09:30"), "09:30")
        with self.assertRaises(ValueError):
            validate_daily_time("29:75")


if __name__ == "__main__":
    unittest.main()
