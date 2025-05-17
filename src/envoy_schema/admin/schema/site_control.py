from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class SiteControlRequest(BaseModel):
    """Used for encoding a "SiteControl" which can represent things like a Dynamic Operating Envelope, Setpoint or
    other form of control"""

    site_id: int  # Corresponds to EndDevice id - the site that this control is targeting
    calculation_log_id: Optional[int]  # The ID of the CalculationLog that created this control (or NULL if no link)
    duration_seconds: int
    start_time: datetime

    randomize_start_seconds: Optional[int] = (
        None  # A number of seconds from -3600 to 3600 that a site should treat as a random range to vary start_time by
    )

    set_energized: Optional[bool] = None  # Corresponds to CSIP-Aus opModEnergize (None will not encode anything)
    set_connect: Optional[bool] = None  # Corresponds to CSIP-Aus opModConnect (None will not encode anything)

    import_limit_watts: Optional[Decimal] = None  # Corresponds to CSIP-Aus opModImpLimW (None will not encode anything)
    export_limit_watts: Optional[Decimal] = None  # Corresponds to CSIP-Aus opModExpLimW (None will not encode anything)
    generation_limit_watts: Optional[Decimal] = (
        None  # Corresponds to CSIP-Aus opModGenLimW (None will not encode anything)
    )
    load_limit_watts: Optional[Decimal] = None  # Corresponds to CSIP-Aus opModLoadLimW (None will not encode anything)


class SiteControlResponse(SiteControlRequest):
    """Site Control basic model when being queried externally"""

    site_control_id: int  # Internal identifier for this DOE
    created_time: datetime  # When this control was created
    changed_time: datetime  # When this control was last changed


class SiteControlPageResponse(BaseModel):
    """Represents a paginated response of SiteControlResponse"""

    total_count: int  # The total number of controls (independent of this page of results)
    limit: int  # The maximum number of controls that could've been returned (the limit set by the query)
    start: int  # The number of controls that have been skipped as part of this query (the start set by the query)
    after: Optional[datetime]  # The "after" filter set by the query
    controls: list[SiteControlResponse]  # The control models in this paged response


class SiteControlGroupRequest(BaseModel):
    """Used for creating new SiteControlGroups (used for grouping SiteControls)"""

    description: str  # Human readable description (32 char max)
    primacy: int  # Lower = Higher priority. Affects "child" controls relative priority when compared to other groups


class SiteControlGroupResponse(SiteControlGroupRequest):
    """Represents a server side view of current SiteControls"""

    site_control_group_id: int  # Primary key
    created_time: datetime  # When this group was created
    changed_time: datetime  # When this group was last changed


class SiteControlGroupPageResponse(BaseModel):
    """Represents a page of SiteControlGroups"""

    total_count: int  # The total number of groups (independent of this page of results)
    limit: int  # The maximum number of groups that could've been returned (the limit set by the query)
    start: int  # The number of groups that have been skipped as part of this query (the start set by the query)
    after: Optional[datetime]  # The "after" filter set by the query
    site_control_groups: list[SiteControlGroupResponse]  # The control group models in this paged response
