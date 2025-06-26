from datetime import datetime

import pytest
from assertical.asserts.type import assert_list_type
from assertical.fake.generator import generate_class_instance

from envoy_schema.admin.schema.archive import (
    ArchiveBase,
    ArchiveDynamicOperatingEnvelopeResponse,
    ArchivePageResponse,
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


@pytest.mark.parametrize(
    "t", [ArchiveDynamicOperatingEnvelopeResponse, ArchiveTariffGeneratedRateResponse, ArchiveSiteResponse]
)
def test_archive_page(t: type):
    """Sanity check that the generics don't introduce any weird behaviour"""
    does = [generate_class_instance(t)]
    doe_page = ArchivePageResponse(
        total_count=1,
        limit=2,
        start=3,
        period_start=datetime(2022, 11, 10),
        period_end=datetime(2023, 11, 10),
        entities=does,
    )
    assert isinstance(doe_page, ArchivePageResponse)
    assert_list_type(t, doe_page.entities, count=1)
