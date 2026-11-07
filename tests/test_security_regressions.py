import hashlib
import hmac
import unittest

from app.utils.phone import normalize_recipient
from app.utils.message_policy import validate_inbound_text, validate_outbound_text
from app.utils.webhook_security import verify_meta_signature
from app.utils.webhook_events import extract_text_events


class SecurityRegressionTests(unittest.TestCase):
    RAW = b'{"entry":[]}'
    SECRET = 'strong-unit-test-app-secret'

    def signature(self, body=None):
        body = self.RAW if body is None else body
        return 'sha256=' + hmac.new(self.SECRET.encode(), body, hashlib.sha256).hexdigest()

    def event(self, sender='255698170989', body='Habari'):
        return {'entry': [{'changes': [{'value': {'messages': [
            {'type': 'text', 'from': sender, 'text': {'body': body}}
        ]}}]}]}


    def test_phone_rejects_multiple_plus_prefixes(self):
        with self.assertRaises(ValueError):
            normalize_recipient('++255698170989')

    def test_phone_rejects_triple_plus_prefixes(self):
        with self.assertRaises(ValueError):
            normalize_recipient('+++255698170989')

    def test_phone_accepts_single_plus_prefix(self):
        self.assertEqual(normalize_recipient('+255698170989'), '255698170989')

    def test_phone_rejects_leading_whitespace(self):
        with self.assertRaises(ValueError):
            normalize_recipient(' 255698170989')

    def test_phone_rejects_trailing_whitespace(self):
        with self.assertRaises(ValueError):
            normalize_recipient('255698170989 ')

    def test_phone_rejects_long_phone_inputs(self):
        with self.assertRaises(ValueError):
            normalize_recipient('1' * 17)

    def test_phone_rejects_non_string_inputs(self):
        with self.assertRaises(ValueError):
            normalize_recipient(255698170989)

    def test_phone_rejects_embedded_newlines(self):
        with self.assertRaises(ValueError):
            normalize_recipient('255698\n170989')

    def test_phone_rejects_unsafe_phone_symbols(self):
        with self.assertRaises(ValueError):
            normalize_recipient('255698@170989')

    def test_phone_accepts_plain_digits(self):
        self.assertEqual(normalize_recipient('255698170989'), '255698170989')

    def test_signature_rejects_numeric_signing_key(self):
        self.assertFalse(verify_meta_signature(self.RAW, self.signature(), 12345))

    def test_signature_rejects_empty_signing_key(self):
        self.assertFalse(verify_meta_signature(self.RAW, self.signature(), ''))

    def test_signature_rejects_oversized_signing_key(self):
        self.assertFalse(verify_meta_signature(self.RAW, self.signature(), 'k' * 4097))

    def test_signature_accepts_valid_raw_signature(self):
        self.assertTrue(verify_meta_signature(self.RAW, self.signature(), self.SECRET))

    def test_signature_rejects_oversized_event_body(self):
        body = b'x' * (64 * 1024 + 1)
        self.assertFalse(verify_meta_signature(body, self.signature(body), self.SECRET))

    def test_signature_accepts_body_within_limit(self):
        self.assertTrue(verify_meta_signature(self.RAW, self.signature(), self.SECRET))

    def test_signature_rejects_oversized_header(self):
        self.assertFalse(verify_meta_signature(self.RAW, 'sha256=' + 'a' * 100, self.SECRET))

    def test_signature_rejects_missing_algorithm_prefix(self):
        self.assertFalse(verify_meta_signature(self.RAW, self.signature()[7:], self.SECRET))

    def test_signature_rejects_wrong_body(self):
        self.assertFalse(verify_meta_signature(self.RAW + b'!', self.signature(), self.SECRET))

    def test_signature_rejects_non_bytes_body(self):
        self.assertFalse(verify_meta_signature('text', self.signature(), self.SECRET))

    def test_signature_rejects_non_hex_digest(self):
        self.assertFalse(verify_meta_signature(self.RAW, 'sha256=' + 'z' * 64, self.SECRET))

    def test_signature_accepts_uppercase_hex_digest(self):
        self.assertTrue(verify_meta_signature(self.RAW, self.signature().upper().replace('SHA256=', 'sha256='), self.SECRET))

    def test_inbound_messages_reject_bidi_overrides(self):
        with self.assertRaises(ValueError):
            validate_inbound_text('Hello\u202EWorld')

    def test_outbound_messages_reject_bidi_overrides(self):
        with self.assertRaises(ValueError):
            validate_outbound_text('Hello\u202DWorld')

    def test_inbound_messages_reject_direction_marks(self):
        with self.assertRaises(ValueError):
            validate_inbound_text('Hello\u200FWorld')

    def test_outbound_messages_reject_direction_marks(self):
        with self.assertRaises(ValueError):
            validate_outbound_text('Hello\u200EWorld')

    def test_inbound_messages_allow_newlines(self):
        self.assertEqual(validate_inbound_text('Habari\nJohn'), 'Habari\nJohn')

    def test_outbound_messages_allow_tabs(self):
        self.assertEqual(validate_outbound_text('Habari\tJohn'), 'Habari\tJohn')

    def test_inbound_messages_reject_control_bytes(self):
        with self.assertRaises(ValueError):
            validate_inbound_text('Habari\x00John')
