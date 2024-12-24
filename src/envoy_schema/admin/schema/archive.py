from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from envoy_schema.admin.schema.doe import DynamicOperatingEnvelopeResponse
from envoy_schema.admin.schema.pricing import TariffGeneratedRateResponse
from envoy_schema.admin.schema.site import SiteResponse


class ArchiveBase(BaseModel):
    """The common properties for all archive responses"""

    archive_id: int  # Unique PK for identifying an individual archive record
    archive_time: datetime  # When was this archive record created
    deleted_time: Optional[datetime]  # When was this archive record marked as deleted (if None - not deleted)


class ArchiveDynamicOperatingEnvelopeResponse(ArchiveBase, DynamicOperatingEnvelopeResponse):
    """Archived version of DynamicOperatingEnvelopeResponse"""

    pass


class ArchiveTariffGeneratedRateResponse(ArchiveBase, TariffGeneratedRateResponse):
    """Archived version of TariffGeneratedRateResponse"""

    pass


class ArchiveSiteResponse(ArchiveBase, SiteResponse):
    """Archived version of SiteResponse"""

    pass
