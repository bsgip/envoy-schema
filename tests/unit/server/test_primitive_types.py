import pytest

from envoy_schema.server.schema.sep2.primitive_types import validate_HttpUri, validate_LocalAbsoluteUri


@pytest.mark.parametrize(
    "raw,valid",
    [
        ("http://foo.bar/", True),
        ("https://foo.bar/", True),
        ("http://example/", True),
        ("https://foo.com:1234/", True),
        ("http://nopath", True),  # no path
        ("http://foo.bar", True),  # no path
        ("http://foo.bar:1234", True),  # no path
        ("https://foo.bar:1234/example/path/4321", True),
        ("https://foo.bar:1234/example/path/4321?q=1&q2=2", True),
        ("file://foo.bar:1234/example/path/4321?q=1&q2=2", False),  # bad scheme
        ("file://root/secret/", False),  # bad scheme
        ("/example/local", False),  # local uri
        ("/", False),  # local uri
        ("example.com/path/123/", False),  # no scheme
    ],
)
def test_http_uri(raw: str, valid: bool):
    """Tests that certain strings validate/dont validate as HTTP uris (and are also invariant to leading/trailing
    whitespace)"""
    whitespace_variations = [raw, raw + "   ", "  " + raw, " " + raw + " ", "\t" + raw]
    for v in whitespace_variations:
        if valid:
            assert validate_HttpUri(v) == raw, "Whitespace should be stripped"
        else:
            with pytest.raises(ValueError):
                validate_HttpUri(v)


@pytest.mark.parametrize(
    "raw,valid",
    [
        ("/edev/123", True),
        ("/edev", True),
        ("/edev/123/cp?a=123", True),
        ("https://foo.com", False),  # has a host/scheme
        ("https://foo.com/", False),  # has a host/scheme
        ("foo.com/example/file", False),  # has a host
        ("foo.com/", False),  # has a host
        ("edev/123", False),  # not absolute
        ("./edev/123", False),  # not absolute
        ("../edev/123", False),  # not absolute
        ("https://foo.bar:1234/example/path/4321", False),
    ],
)
def test_local_uri(raw: str, valid: bool):
    """Tests that certain strings validate/dont validate as local absolute uris (and are also invariant to
    leading/trailing whitespace)"""
    whitespace_variations = [raw, raw + "   ", "  " + raw, " " + raw + " ", "\t" + raw]
    for v in whitespace_variations:
        if valid:
            assert validate_LocalAbsoluteUri(v) == raw, "Whitespace should be stripped"
        else:
            with pytest.raises(ValueError):
                validate_LocalAbsoluteUri(v)
