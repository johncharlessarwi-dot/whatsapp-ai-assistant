"""Regression tests for Meta webhook subscription verification."""
import unittest
from app.utils.subscription import verify_subscription


class WebhookVerificationTests(unittest.TestCase):
    TOKEN = 'test-secret-token'

    def test_valid_subscription(self):
        self.assertEqual(verify_subscription('subscribe', self.TOKEN, '12345', self.TOKEN), (200, '12345'))

    def test_missing_challenge_is_bad_request(self):
        self.assertEqual(verify_subscription('subscribe', self.TOKEN, None, self.TOKEN)[0], 400)

    def test_wrong_token_is_forbidden(self):
        self.assertEqual(verify_subscription('subscribe', 'wrong', '123', self.TOKEN)[0], 403)

    def test_missing_mode_is_bad_request(self):
        self.assertEqual(verify_subscription(None, self.TOKEN, '123', self.TOKEN)[0], 400)

    def test_unconfigured_token_fails_closed(self):
        self.assertEqual(verify_subscription('subscribe', self.TOKEN, '123', None)[0], 403)


if __name__ == '__main__':
    unittest.main()
