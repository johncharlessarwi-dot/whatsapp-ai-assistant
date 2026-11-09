"""Extract only supported text events without trusting arbitrary nested JSON."""
def extract_text_events(payload, max_entries=10):
    if not isinstance(payload, dict):
        return []
    entries = payload.get("entry")
    if type(max_entries) is not int or not 1 <= max_entries <= 10:
        return []
    if not isinstance(entries, list) or len(entries) > max_entries:
        return []
    result = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        changes = entry.get("changes", [])
        if not isinstance(changes, list) or len(changes) > 20:
            continue
        for change in changes:
            if not isinstance(change, dict) or not isinstance(change.get("value"), dict):
                continue
            messages = change["value"].get("messages", [])
            if not isinstance(messages, list) or len(messages) > 20:
                continue
            for message in messages:
                if not isinstance(message, dict) or message.get("type") != "text":
                    continue
                text = message.get("text")
                if isinstance(text, dict) and isinstance(text.get("body"), str) and 0 < len(text["body"]) <= 4000 and isinstance(message.get("from"), str) and message["from"].isascii() and message["from"].isdigit() and 9 <= len(message["from"]) <= 16:
                    result.append((message["from"], text["body"]))
                    if len(result) >= 100:
                        return result
    return result[:100]


def extract_identified_text_events(payload):
    """Return text events with Meta message IDs, rejecting unidentifiable events.

    IDs are needed for durable deduplication; never use text or phone as a key.
    The original extractor remains for backwards compatibility.
    """
    if not isinstance(payload, dict):
        return []
    entries = payload.get("entry")
    if not isinstance(entries, list) or len(entries) > 10:
        return []
    events = []
    seen_ids = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        changes = entry.get("changes", [])
        if not isinstance(changes, list) or len(changes) > 20:
            continue
        for change in changes:
            if not isinstance(change, dict):
                continue
            value = change.get("value")
            if not isinstance(value, dict):
                continue
            messages = value.get("messages", [])
            if not isinstance(messages, list) or len(messages) > 20:
                continue
            for message in messages:
                if not isinstance(message, dict) or message.get("type") != "text":
                    continue
                sender, message_id, text = message.get("from"), message.get("id"), message.get("text")
                if not (isinstance(sender, str) and sender.isascii() and sender.isdigit() and 9 <= len(sender) <= 16):
                    continue
                if not (isinstance(message_id, str) and 7 <= len(message_id) <= 255 and message_id.startswith("wamid.")):
                    continue
                if not (isinstance(text, dict) and isinstance(text.get("body"), str) and 0 < len(text["body"]) <= 4000):
                    continue
                if message_id in seen_ids:
                    continue
                seen_ids.add(message_id)
                events.append((message_id, sender, text["body"]))
                if len(events) >= 100:
                    return events
    return events
