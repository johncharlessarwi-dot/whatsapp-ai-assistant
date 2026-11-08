"""Tests for extracting Meta message identifiers safely."""
import unittest
from app.utils.webhook_events import extract_identified_text_events


class IdentifiedEventsTests(unittest.TestCase):
    def payload(self, message):
        return {'entry': [{'changes': [{'value': {'messages': [message]}}]}]}

    def test_extracts_message_id_sender_and_body(self):
        event = {'id': 'wamid.ABC123', 'type': 'text', 'from': '255698170989', 'text': {'body': 'Habari'}}
        self.assertEqual(extract_identified_text_events(self.payload(event)), [('wamid.ABC123', '255698170989', 'Habari')])

    def test_rejects_missing_id(self):
        event = {'type': 'text', 'from': '255698170989', 'text': {'body': 'Habari'}}
        self.assertEqual(extract_identified_text_events(self.payload(event)), [])

    def test_rejects_invalid_id(self):
        event = {'id': 'random', 'type': 'text', 'from': '255698170989', 'text': {'body': 'Habari'}}
        self.assertEqual(extract_identified_text_events(self.payload(event)), [])

    def test_rejects_oversized_id(self):
        event = {'id': 'wamid.' + 'X' * 256, 'type': 'text', 'from': '255698170989', 'text': {'body': 'Habari'}}
        self.assertEqual(extract_identified_text_events(self.payload(event)), [])

    def test_rejects_malformed_payload(self):
        self.assertEqual(extract_identified_text_events({'entry': 'bad'}), [])


if __name__ == '__main__':
    unittest.main()
