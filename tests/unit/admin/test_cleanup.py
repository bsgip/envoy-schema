from datetime import UTC, datetime

import pydantic
import pytest

from envoy_schema.admin.schema.aggregator import AggregatorDomainRequest
from envoy_schema.admin.schema.cleanup import (
    ArchiveCleanupRequest,
    ArchiveCleanupResponse,
    ArchiveCleanupType,
    ExpiredCleanupMode,
    ExpiredCleanupRequest,
)


def test_expired_cleanup_request_defaults_to_archive() -> None:
    req = ExpiredCleanupRequest.model_validate({"expired_before": "2026-01-02T03:04:05Z"})
    assert req.mode == ExpiredCleanupMode.archive
    assert req.expired_before == datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)


@pytest.mark.parametrize("mode", list(ExpiredCleanupMode))
def test_expired_cleanup_request_roundtrip(mode: ExpiredCleanupMode) -> None:
    req = ExpiredCleanupRequest(expired_before=datetime(2026, 1, 1, tzinfo=UTC), mode=mode)
    assert ExpiredCleanupRequest.model_validate_json(req.model_dump_json()) == req


def test_expired_cleanup_request_invalid_mode() -> None:
    with pytest.raises(pydantic.ValidationError):
        ExpiredCleanupRequest.model_validate({"expired_before": "2026-01-02T03:04:05Z", "mode": "shred"})


def test_archive_cleanup_request() -> None:
    req = ArchiveCleanupRequest.model_validate({"archived_before": "2026-01-02T03:04:05Z"})
    assert req.archive_types is None

    req = ArchiveCleanupRequest.model_validate(
        {"archived_before": "2026-01-02T03:04:05Z", "archive_types": ["site_control", "tariff_generated_rate"]}
    )
    assert req.archive_types == [ArchiveCleanupType.site_control, ArchiveCleanupType.tariff_generated_rate]

    with pytest.raises(pydantic.ValidationError):
        ArchiveCleanupRequest.model_validate({"archived_before": "2026-01-02T03:04:05Z", "archive_types": ["foo"]})


def test_archive_cleanup_response_roundtrip() -> None:
    resp = ArchiveCleanupResponse(
        archived_before=datetime(2026, 1, 1, tzinfo=UTC),
        removed_counts={ArchiveCleanupType.site: 1, ArchiveCleanupType.site_control: 0},
    )
    assert ArchiveCleanupResponse.model_validate_json(resp.model_dump_json()) == resp


@pytest.mark.parametrize("domain", ["", "a" * 513])
def test_aggregator_domain_request_invalid(domain: str) -> None:
    with pytest.raises(pydantic.ValidationError):
        AggregatorDomainRequest(domain=domain)


def test_aggregator_domain_request_valid() -> None:
    assert AggregatorDomainRequest(domain="example.com").domain == "example.com"
