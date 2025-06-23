import datetime as dt

import pytest
import pydantic

from envoy_schema.admin.schema.certificate import CertificateAssignmentRequest  # type: ignore[attr-defined]


@pytest.mark.parametrize(
    "lfdi,certificate_id,expiry",
    [
        (None, None, dt.datetime(1985, 9, 30, 0, 0, 0)),
        (None, None, None),
    ],
)
def test_assignment_request_invalid_no_lfdi_or_id(
    lfdi: str | None, certificate_id: int | None, expiry: dt.datetime | None
) -> None:
    """Tests the CertificateAssignmentRequest custom validator works as expected, missing id and lfdi"""
    with pytest.raises(pydantic.ValidationError, match="Either lfdi or id needs to be provided"):
        CertificateAssignmentRequest(lfdi=lfdi, certificate_id=certificate_id, expiry=expiry)


@pytest.mark.parametrize(
    "lfdi,certificate_id,expiry",
    [
        ("ARST123456" * 4, 123, dt.datetime(1985, 9, 30, 0, 0, 0)),
        ("ARST123456" * 4, 321, None),
    ],
)
def test_assignment_request_invalid_both_lfdi_and_id(
    lfdi: str | None, certificate_id: int | None, expiry: dt.datetime | None
) -> None:
    """Tests the CertificateAssignmentRequest custom validator works as expected, missing id and lfdi"""
    with pytest.raises(pydantic.ValidationError, match="Only one of lfdi or id can be provided, not both"):
        CertificateAssignmentRequest(lfdi=lfdi, certificate_id=certificate_id, expiry=expiry)


@pytest.mark.parametrize(
    "lfdi,certificate_id,expiry",
    [
        ("ARST123456" * 4, None, dt.datetime(1985, 9, 30, 0, 0, 0)),
        ("ARST123456" * 4, None, None),
        (None, 121, dt.datetime(1985, 9, 30, 0, 0, 0)),
        (None, 45664564, None),
    ],
)
def test_assignment_request_valid(lfdi: str | None, certificate_id: int | None, expiry: dt.datetime | None) -> None:
    """Tests the CertificateAssignmentRequest model works as expected excluding the custom validator"""
    cert_ass_req = CertificateAssignmentRequest(
        lfdi=lfdi,
        certificate_id=certificate_id,
        expiry=expiry,
    )

    # Simple assertion for completeness
    assert cert_ass_req.certificate_id or cert_ass_req.lfdi
