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
