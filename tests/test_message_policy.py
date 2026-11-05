import unittest

from app.utils.message_policy import validate_inbound_text, validate_outbound_text


class MessagePolicyTests(unittest.TestCase):
    def test_trims_normal_messages(self):
        self.assertEqual(validate_inbound_text("  Habari  "), "Habari")
        self.assertEqual(validate_outbound_text("  Sawa  "), "Sawa")

    def test_allows_multiline_text_and_length_boundary(self):
        for validator in (validate_inbound_text, validate_outbound_text):
            with self.subTest(validator=validator.__name__):
                self.assertEqual(validator("Habari\nJohn\t!\r\n"), "Habari\nJohn\t!")
                self.assertEqual(validator("x" * 4000), "x" * 4000)

    def test_rejects_malformed_messages(self):
        for validator in (validate_inbound_text, validate_outbound_text):
            for value in ("", "x" * 4001, "a\x00b", "a\x1bb", "a\x7fb", None):
                with self.subTest(validator=validator.__name__, value=repr(value)):
                    with self.assertRaises(ValueError):
                        validator(value)
