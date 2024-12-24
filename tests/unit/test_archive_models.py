import pytest
from assertical.fake.generator import generate_class_instance

from envoy_schema.admin.schema.archive import (
    ArchiveBase,
    ArchiveDynamicOperatingEnvelopeResponse,
    ArchiveSiteResponse,
    ArchiveTariffGeneratedRateResponse,
)


@pytest.mark.parametrize(
    "t", [ArchiveDynamicOperatingEnvelopeResponse, ArchiveTariffGeneratedRateResponse, ArchiveSiteResponse]
)
def test_archive_types_generate(t: type):
    """Simple check to ensure multi inheritance doesn't introduce any weird behaviour"""
    obj: ArchiveBase = generate_class_instance(t, generate_relationships=True)
    assert isinstance(obj, t), "Type should be the type we specified"
    assert isinstance(obj, ArchiveBase), "Type should also be an ArchiveBase"

    assert obj.archive_id is not None
    assert obj.deleted_time is not None
