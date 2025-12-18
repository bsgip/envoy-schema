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
    set_point_percentage: Optional[Decimal] = (
        None  # percent of device max power settings to charge (if negative) or discharge (if positive) at. 100 = 100%
    )
    ramp_time_seconds: Optional[Decimal] = (
        None  # Corresponds to rampTms (None will not encode anything). 100 = 100 seconds
    )


class SiteControlResponse(SiteControlRequest):
    """Site Control basic model when being queried externally"""

    site_control_id: int  # Internal identifier for this DOE
    created_time: datetime  # When this control was created
    changed_time: datetime  # When this control was last changed
    superseded: bool  # Whether this control has been superseded by a higher priority control since its creation


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
    fsa_id: int = 1  # The function set assignment ID that this SiteControl group will be grouped under


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


class UpdateDefaultValue(BaseModel):
    """Used to allow the setting of None or a specific value"""

    value: Optional[Decimal]  # The decimal value to update (or None to update the value to None)


class SiteControlGroupDefaultRequest(BaseModel):
    """Used for updating fields associated with the SiteControlGroupDefault values - used when there is no active
    control"""

    import_limit_watts: Optional[
        UpdateDefaultValue
    ]  # If set - update The default "import limit watts" used in absence of an active control
    export_limit_watts: Optional[
        UpdateDefaultValue
    ]  # If set - update The default "export limit watts" used in absence of an active control
    generation_limit_watts: Optional[
        UpdateDefaultValue
    ]  # If set - update The default "generation limit watts" used in absence of an active control
    load_limit_watts: Optional[
        UpdateDefaultValue
    ]  # If set - update The default "export limit watts" used in absence of an active control
    ramp_rate_percent_per_second: Optional[
        UpdateDefaultValue
    ]  # If set - update The default ramp rate expressed in a percent of max W per second


class SiteControlGroupDefaultResponse(BaseModel):
    """Snapshot of the current SiteControlGroupDefault values that are used if no specific control is active"""

    server_default_import_limit_watts: Optional[Decimal]  # None means NO default
    server_default_export_limit_watts: Optional[Decimal]
    server_default_generation_limit_watts: Optional[Decimal]
    server_default_load_limit_watts: Optional[Decimal]
    ramp_rate_percent_per_second: Optional[Decimal]

    created_time: datetime
    changed_time: datetime
