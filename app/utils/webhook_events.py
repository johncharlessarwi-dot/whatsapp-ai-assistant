"""Extract only supported text events without trusting arbitrary nested JSON."""
def extract_text_events(payload, max_entries=10):
    if not isinstance(payload, dict):
        return []
    entries = payload.get("entry")
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
                if isinstance(text, dict) and isinstance(text.get("body"), str) and isinstance(message.get("from"), str) and 9 <= len(message["from"]) <= 16:
                    result.append((message["from"], text["body"]))
    return result[:100]
