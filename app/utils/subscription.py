"""Pure verification logic for the Meta webhook subscription handshake."""
import hmac


def verify_subscription(mode, token, challenge, expected_token):
    """Return an HTTP status and response body without exposing the verify token."""
    if mode != 'subscribe' or not isinstance(token, str) or not token or not isinstance(challenge, str) or not challenge:
        return 400, 'Bad Request'
    if not challenge.isascii() or not challenge.isdecimal() or len(challenge) > 128:
        return 400, 'Bad Request'
    if not isinstance(expected_token, str) or not expected_token:
        return 403, 'Forbidden'
    if hmac.compare_digest(token, expected_token):
        return 200, challenge
    return 403, 'Forbidden'
