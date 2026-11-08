"""Security regression tests for Meta Graph API configuration."""
import unittest
from app.utils.graph_config import validate_phone_number_id


class GraphConfigTests(unittest.TestCase):
    def test_accepts_numeric_meta_id(self):
        self.assertEqual(validate_phone_number_id('123456789012345'), '123456789012345')

    def test_rejects_url_path_injection(self):
        for value in ('123/other', '123?token=abc', '123#fragment', '123\\n'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_phone_number_id(value)

    def test_rejects_wrong_types(self):
        for value in (None, 123456, [], ''):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_phone_number_id(value)

    def test_rejects_excessively_long_id(self):
        with self.assertRaises(ValueError):
            validate_phone_number_id('1' * 21)

    def test_rejects_surrounding_whitespace(self):
        with self.assertRaises(ValueError):
            validate_phone_number_id(' 12345 ')


if __name__ == '__main__':
    unittest.main()
