"""Conservative bounds for incoming and outgoing WhatsApp text."""

MAX_INBOUND_CHARS = 4000
MAX_OUTBOUND_CHARS = 4000


def _contains_disallowed_control(text):
    """Keep multiline and tabbed messages, but reject other ASCII controls."""
    return any((ord(char) < 32 and char not in "\t\n\r") or ord(char) == 127 or 0x202A <= ord(char) <= 0x202E or 0x2066 <= ord(char) <= 0x2069 for char in text)


def validate_inbound_text(value):
    if not isinstance(value, str):
        raise ValueError("Message body must be text")
    text = value.strip()
    if not text or len(text) > MAX_INBOUND_CHARS:
        raise ValueError("Incoming message length out of bounds")
    if _contains_disallowed_control(text):
        raise ValueError("Control characters are not allowed")
    return text


def validate_outbound_text(value):
    if not isinstance(value, str):
        raise ValueError("Response must be text")
    text = value.strip()
    if not text or len(text) > MAX_OUTBOUND_CHARS or _contains_disallowed_control(text):
        raise ValueError("Outgoing message length or characters out of bounds")
    return text
