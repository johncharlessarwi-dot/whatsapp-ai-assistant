"""Regression coverage for Meta webhook subscription verification."""
import unittest
from flask import Flask
from app.routes.webhook import webhook_bp


class WebhookVerificationTests(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config['WHATSAPP_VERIFY_TOKEN'] = 'test-secret-token'
        app.register_blueprint(webhook_bp, url_prefix='/webhook')
        self.client = app.test_client()

    def test_valid_subscription(self):
        response = self.client.get('/webhook/', query_string={
            'hub.mode': 'subscribe', 'hub.verify_token': 'test-secret-token',
            'hub.challenge': '12345',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), '12345')

    def test_missing_challenge_is_bad_request(self):
        response = self.client.get('/webhook/', query_string={
            'hub.mode': 'subscribe', 'hub.verify_token': 'test-secret-token',
        })
        self.assertEqual(response.status_code, 400)

    def test_wrong_token_is_forbidden(self):
        response = self.client.get('/webhook/', query_string={
            'hub.mode': 'subscribe', 'hub.verify_token': 'wrong', 'hub.challenge': '123',
        })
        self.assertEqual(response.status_code, 403)

    def test_missing_mode_is_bad_request(self):
        response = self.client.get('/webhook/', query_string={
            'hub.verify_token': 'test-secret-token', 'hub.challenge': '123',
        })
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
