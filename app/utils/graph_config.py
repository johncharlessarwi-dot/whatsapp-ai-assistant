"""Strict configuration validation for Meta Graph API identifiers."""
import re


def validate_phone_number_id(value):
    """Accept only the numeric phone-number ID assigned by Meta."""
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]{1,20}", value):
        raise ValueError("Invalid WhatsApp phone number ID configuration")
    return value
