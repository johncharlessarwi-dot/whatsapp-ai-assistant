"""Strict WhatsApp recipient identifiers; never pass arbitrary strings to Graph API."""
import re


def normalize_recipient(value):
    if not isinstance(value, str):
        raise ValueError("Recipient must be text")
    digits = value[1:] if value.startswith('+') else value
    if not re.fullmatch(r"[1-9][0-9]{8,14}", digits):
        raise ValueError("Invalid WhatsApp recipient number")
    return digits
