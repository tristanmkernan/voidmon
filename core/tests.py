import pytest

from .services import is_external_resource


def test_is_external_resource():
    # same domain
    assert not is_external_resource(
        "https://example.com", "https://example.com/script.js"
    )

    # subdomain
    assert not is_external_resource(
        "https://example.com", "https://sub.example.com/script.js"
    )

    # domain-less resource
    assert not is_external_resource("https://example.com", "/script.js")

    # same domain, but site_url has a path
    assert not is_external_resource(
        "https://example.com/path", "https://example.com/script.js"
    )

    # different domain
    assert is_external_resource("https://example.com", "https://evil.com/script.js")

    # protocol-relative
    assert is_external_resource("https://example.com", "//evil.com/script.js")
