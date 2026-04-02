from datetime import datetime
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

from envoy_schema.admin.schema.pricing import TariffGeneratedRateResponse
from envoy_schema.admin.schema.site import SiteResponse
from envoy_schema.admin.schema.site_control import SiteControlResponse


class ArchiveBase(BaseModel):
    """The common properties for all archive responses"""

    archive_id: int  # Unique PK for identifying an individual archive record
    archive_time: datetime  # When was this archive record created
    deleted_time: Optional[datetime]  # When was this archive record marked as deleted (if None - not deleted)


class ArchiveSiteControlResponse(ArchiveBase, SiteControlResponse):
    """Archived version of SiteControlResponse"""

    pass


class ArchiveTariffGeneratedRateResponse(ArchiveBase, TariffGeneratedRateResponse):
    """Archived version of TariffGeneratedRateResponse"""

    pass


class ArchiveSiteResponse(ArchiveBase, SiteResponse):
    """Archived version of SiteResponse"""

    pass


ArchiveType = TypeVar(
    "ArchiveType", ArchiveSiteControlResponse, ArchiveTariffGeneratedRateResponse, ArchiveSiteResponse
)


class ArchivePageResponse(BaseModel, Generic[ArchiveType]):
    """Represents a paginated response of archive entities"""

    total_count: int  # The total number of entities (independent of this page of results)
    limit: int  # The maximum number of entities that could've been returned (the limit set by the query)
    start: int  # The number of entities that have been skipped as part of this query (the start set by the query)
    period_start: datetime  # The period_start parameter from the original request
    period_end: datetime  # The period_end parameter from the original request
    entities: list[ArchiveType]  # The entity models in this paged response
