import hashlib
import hmac
import unittest

from app.utils.webhook_security import verify_meta_signature


class MetaSignatureTests(unittest.TestCase):
    def test_valid_signature(self):
        raw = b'{"entry":[]}'
        digest = hmac.new(b"secret", raw, hashlib.sha256).hexdigest()
        self.assertTrue(verify_meta_signature(raw, "sha256=" + digest, "secret"))

    def test_invalid_signatures_fail_closed(self):
        self.assertFalse(verify_meta_signature(b"{}", "", "secret"))
        self.assertFalse(verify_meta_signature(b"{}", "sha256=abc", "secret"))
        self.assertFalse(verify_meta_signature(b"{}", "sha256=" + "0" * 64, "secret"))
        self.assertFalse(verify_meta_signature(b"{}", "sha256=" + "0" * 64, ""))
