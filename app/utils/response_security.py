"""Consistent defensive HTTP headers for webhook and dashboard responses."""


def apply_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response
