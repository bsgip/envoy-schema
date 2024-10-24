from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class DynamicOperatingEnvelopeRequest(BaseModel):
    """Dynamic Operating Envelope basic model"""

    site_id: int  # Corresponds to EndDevice id
    calculation_log_id: Optional[int]  # The ID of the CalculationLog that created this DOE (or NULL if no link)
    duration_seconds: int
    import_limit_active_watts: Decimal
    export_limit_watts: Decimal
    start_time: datetime


class DynamicOperatingEnvelopeResponse(DynamicOperatingEnvelopeRequest):
    """Dynamic Operating Envelope basic model when being queried externally"""

    dynamic_operating_envelope_id: int  # Internal identifier for this DOE
    created_time: datetime
    changed_time: datetime  # When this DOE was last changed/created


class DoePageResponse(BaseModel):
    """Represents a paginated response of DynamicOperatingEnvelopeRequest"""

    total_count: int  # The total number of does (independent of this page of results)
    limit: int  # The maximum number of does that could've been returned (the limit set by the query)
    start: int  # The number of does that have been skipped as part of this query (the start set by the query)
    after: Optional[datetime]  # The "after" filter set by the query
    does: list[DynamicOperatingEnvelopeResponse]  # The doe models in this paged response
