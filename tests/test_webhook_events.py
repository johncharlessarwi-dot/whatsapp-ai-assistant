import unittest

from app.utils.webhook_events import extract_text_events


class WebhookEventTests(unittest.TestCase):
    def test_extracts_text_only(self):
        payload = {"entry": [{"changes": [{"value": {"messages": [
            {"type": "text", "from": "255698170989", "text": {"body": "Habari"}},
            {"type": "image", "from": "255698170989"},
        ]}}]}]}
        self.assertEqual(extract_text_events(payload), [("255698170989", "Habari")])

    def test_handles_malformed_data_without_throwing(self):
        for value in (None, {}, {"entry": [None]}, {"entry": "wrong"}):
            self.assertEqual(extract_text_events(value), [])


class ExtractorLimitTests(unittest.TestCase):
    def test_boolean_limit_is_rejected(self):
        self.assertEqual(extract_text_events({'entry': []}, max_entries=True), [])

    def test_unbounded_limit_is_rejected(self):
        self.assertEqual(extract_text_events({'entry': []}, max_entries=1000000), [])


class LegacySenderValidationTests(unittest.TestCase):
    def test_rejects_alphabetic_sender_before_processing(self):
        message = {'type': 'text', 'from': 'abcdefghi', 'text': {'body': 'Hello'}}
        payload = {'entry': [{'changes': [{'value': {'messages': [message]}}]}]}
        self.assertEqual(extract_text_events(payload), [])
