"""Conservative bounds for incoming and outgoing WhatsApp text."""
MAX_INBOUND_CHARS = 4000
MAX_OUTBOUND_CHARS = 4000


def validate_inbound_text(value):
    if not isinstance(value, str):
        raise ValueError("Message body must be text")
    text = value.strip()
    if not text or len(text) > MAX_INBOUND_CHARS:
        raise ValueError("Incoming message length out of bounds")
    if "\x00" in text:
        raise ValueError("Null bytes are not allowed")
    return text


def validate_outbound_text(value):
    if not isinstance(value, str):
        raise ValueError("Response must be text")
    text = value.strip()
    if not text or len(text) > MAX_OUTBOUND_CHARS or "\x00" in text:
        raise ValueError("Outgoing message length out of bounds")
    return text
