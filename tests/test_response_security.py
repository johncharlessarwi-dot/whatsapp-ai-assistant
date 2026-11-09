import unittest
from flask import Response
from app.utils.response_security import apply_security_headers


class ResponseSecurityTests(unittest.TestCase):
    def test_disables_mime_sniffing(self):
        result = apply_security_headers(Response('ok'))
        self.assertEqual(result.headers['X-Content-Type-Options'], 'nosniff')


class FramePolicyTests(unittest.TestCase):
    def test_frame_protection_enabled(self):
        response = apply_security_headers(Response('ok'))
        self.assertEqual(response.headers['X-Frame-Options'], 'DENY')
