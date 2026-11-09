"""Verify Meta webhook requests before reading or processing user messages."""
import hashlib
import hmac


def verify_meta_signature(raw_body, signature, app_secret):
    if not isinstance(raw_body, bytes) or not isinstance(signature, str) or not isinstance(app_secret, str) or not app_secret:
        return False
    if not app_secret.strip():
        return False
    if len(app_secret) > 4096:
        return False
    if len(raw_body) > 64 * 1024:
        return False
    if len(signature) > 80:
        return False
    prefix = "sha256="
    if not signature.startswith(prefix) or len(signature) != len(prefix) + 64:
        return False
    supplied = signature[len(prefix):]
    if any(char not in "0123456789abcdefABCDEF" for char in supplied):
        return False
    expected = hmac.new(app_secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, supplied.lower())
