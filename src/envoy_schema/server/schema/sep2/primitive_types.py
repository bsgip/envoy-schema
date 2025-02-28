from urllib.parse import urlparse

from pydantic import AfterValidator
from typing_extensions import Annotated


def validate_String6(v: str):
    if len(v) > 6:
        raise ValueError("String6 max length of 6.")
    return v


def validate_String192(v: str):
    if len(v) > 192:
        raise ValueError("String192 max length of 192.")
    return v


def validate_HexBinary8(v: str):
    if len(v) > 2:
        raise ValueError("HexBinary8 max length of 2.")
    return v


def validate_HexBinary16(v: str):
    if len(v) > 4:
        raise ValueError("HexBinary16 max length of 4.")
    return v


def validate_HexBinary32(v: str):
    if len(v) > 8:
        raise ValueError("HexBinary32 max length of 8.")
    return v


def validate_HexBinary48(v: str):
    if len(v) > 12:
        raise ValueError("HexBinary48 max length of 12.")
    return v


def validate_HexBinary64(v: str):
    if len(v) > 16:
        raise ValueError("HexBinary64 max length of 16.")
    return v


def validate_HexBinary128(v: str):
    if len(v) > 32:
        raise ValueError("HexBinary128 max length of 32.")
    return v


def validate_HexBinary160(v: str):
    if len(v) > 40:
        raise ValueError("HexBinary160 max length of 40.")
    return v


def validate_LocalAbsoluteUri(v: str):
    """Only does a cursory check that a URI looks like a local absolute URI eg: /edev/123/cp"""
    v = v.strip()
    if len(v) > 4096:
        raise ValueError("LocalUri length has a max of 4096")

    parsed = urlparse(v)
    if parsed.scheme or parsed.netloc:
        raise ValueError("LocalUri should not include a scheme or host")

    if not v.startswith("/"):
        raise ValueError("LocalUri should be an absolute URI")

    return v


def validate_HttpUri(v: str):
    """Only does a cursory check that a URI looks like a remote server HTTP(S) query eg: https://example.com:123/hook"""

    v = v.strip()
    if len(v) > 4096:
        raise ValueError("HttpUri length has a max of 4096")

    parsed = urlparse(v)
    if parsed.scheme != "https" and parsed.scheme != "http":
        raise ValueError("HttpUri should have a http or https scheme")

    if len(parsed.netloc) < 3:
        raise ValueError("HttpUri requires a remote host")

    if not parsed.path.startswith("/"):
        raise ValueError("HttpUri should be an absolute path")

    return v


String6 = Annotated[str, AfterValidator(validate_String6)]
String192 = Annotated[str, AfterValidator(validate_String192)]

HexBinary8 = Annotated[str, AfterValidator(validate_HexBinary8)]
HexBinary16 = Annotated[str, AfterValidator(validate_HexBinary16)]
HexBinary32 = Annotated[str, AfterValidator(validate_HexBinary32)]
HexBinary48 = Annotated[str, AfterValidator(validate_HexBinary48)]
HexBinary64 = Annotated[str, AfterValidator(validate_HexBinary64)]
HexBinary128 = Annotated[str, AfterValidator(validate_HexBinary128)]
HexBinary160 = Annotated[str, AfterValidator(validate_HexBinary160)]


LocalAbsoluteUri = Annotated[str, AfterValidator(validate_LocalAbsoluteUri)]
HttpUri = Annotated[str, AfterValidator(validate_HttpUri)]
