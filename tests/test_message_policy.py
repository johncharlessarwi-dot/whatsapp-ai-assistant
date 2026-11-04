import unittest

from app.utils.message_policy import validate_inbound_text, validate_outbound_text


class MessagePolicyTests(unittest.TestCase):
    def test_trims_normal_messages(self):
        self.assertEqual(validate_inbound_text("  Habari  "), "Habari")
        self.assertEqual(validate_outbound_text("  Sawa  "), "Sawa")

    def test_rejects_malformed_messages(self):
        for value in ("", "x" * 4001, "a\x00b", None):
            with self.subTest(value_type=type(value).__name__), self.assertRaises(ValueError):
                validate_inbound_text(value)
        with self.assertRaises(ValueError):
            validate_outbound_text("x" * 4001)
