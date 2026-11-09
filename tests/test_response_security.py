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


class ReferrerPolicyTests(unittest.TestCase):
    def test_referrer_policy_disallows_leakage(self):
        response = apply_security_headers(Response('ok'))
        self.assertEqual(response.headers['Referrer-Policy'], 'no-referrer')


class SensitiveCacheTests(unittest.TestCase):
    def test_cache_disabled(self):
        response = apply_security_headers(Response('ok'))
        self.assertEqual(response.headers['Cache-Control'], 'no-store')


class BrowserPermissionTests(unittest.TestCase):
    def test_disallows_sensitive_browser_features(self):
        response = apply_security_headers(Response('ok'))
        self.assertIn('camera=()', response.headers['Permissions-Policy'])


class ResourcePolicyTests(unittest.TestCase):
    def test_cross_origin_resource_policy(self):
        response = apply_security_headers(Response('ok'))
        self.assertEqual(response.headers['Cross-Origin-Resource-Policy'], 'same-origin')


class CrossDomainPolicyTests(unittest.TestCase):
    def test_cross_domain_policy_is_disabled(self):
        response = apply_security_headers(Response('ok'))
        self.assertEqual(response.headers['X-Permitted-Cross-Domain-Policies'], 'none')


class OpenerIsolationTests(unittest.TestCase):
    def test_opener_policy_enforces_same_origin(self):
        response = apply_security_headers(Response('ok'))
        self.assertEqual(response.headers['Cross-Origin-Opener-Policy'], 'same-origin')
