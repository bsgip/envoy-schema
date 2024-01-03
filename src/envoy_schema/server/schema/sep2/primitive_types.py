from pydantic import AfterValidator
from pydantic.networks import AnyUrl
from typing_extensions import Annotated


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


HexBinary8 = Annotated[str, AfterValidator(validate_HexBinary8)]
HexBinary16 = Annotated[str, AfterValidator(validate_HexBinary16)]
HexBinary32 = Annotated[str, AfterValidator(validate_HexBinary32)]
HexBinary48 = Annotated[str, AfterValidator(validate_HexBinary48)]
HexBinary64 = Annotated[str, AfterValidator(validate_HexBinary64)]
HexBinary128 = Annotated[str, AfterValidator(validate_HexBinary128)]
HexBinary160 = Annotated[str, AfterValidator(validate_HexBinary160)]


class UriWithoutHost(AnyUrl):
    """Allows URIs without a host/scheme (i.e. - just a path like /edev/123)"""

    # XSD anyURI type -
    host_required = False

    @staticmethod
    def get_default_parts(parts):
        return {"scheme": "https"}


class UriFullyQualified(AnyUrl):
    """Allows only strings that match a fully qualified URI (i.e. requires host/scheme)"""

    # XSD anyURI type with a requirement of a HOST
    host_required = True
