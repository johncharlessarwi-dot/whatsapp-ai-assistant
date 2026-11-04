import unittest

from app.utils.phone import normalize_recipient


class RecipientTests(unittest.TestCase):
    def test_accepts_e164_digits(self):
        self.assertEqual(normalize_recipient("+255698170989"), "255698170989")

    def test_rejects_malformed_numbers(self):
        for value in ("+abc", "0", "255 698 170 989", None, "255698170989x"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_recipient(value)
