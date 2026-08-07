from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class SiteControlRequest(BaseModel):
    """Used for encoding a "SiteControl" which can represent things like a Dynamic Operating Envelope, Setpoint or
    other form of control"""

    site_group_id: int  # Corresponds to SiteGroup id - the members of this SiteGroup are targeted by this control
    calculation_log_id: int | None  # The ID of the CalculationLog that created this control (or NULL if no link)
    duration_seconds: int
    start_time: datetime

    randomize_start_seconds: int | None = (
        None  # A number of seconds from -3600 to 3600 that a site should treat as a random range to vary start_time by
    )

    set_energized: bool | None = None  # Corresponds to CSIP-Aus opModEnergize (None will not encode anything)
    set_connect: bool | None = None  # Corresponds to CSIP-Aus opModConnect (None will not encode anything)

    import_limit_watts: Decimal | None = None  # Corresponds to CSIP-Aus opModImpLimW (None will not encode anything)
    export_limit_watts: Decimal | None = None  # Corresponds to CSIP-Aus opModExpLimW (None will not encode anything)
    generation_limit_watts: Decimal | None = (
        None  # Corresponds to CSIP-Aus opModGenLimW (None will not encode anything)
    )
    load_limit_watts: Decimal | None = None  # Corresponds to CSIP-Aus opModLoadLimW (None will not encode anything)
    set_point_percentage: Decimal | None = (
        None  # percent of device max power settings to charge (if negative) or discharge (if positive) at. 100 = 100%
    )
    ramp_time_seconds: Decimal | None = (
        None  # Corresponds to rampTms (None will not encode anything). 100 = 100 seconds
    )

    # Storage extension
    storage_target_watts: Decimal | None = None

    display_id: int | None = (
        None  # If set - seed the auto generated MRID with this value. equal display_id means equal mrid
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
    after: datetime | None  # The "after" filter set by the query
    site_id: int | None  # The "site_id" filter set by the query (Applied to a site's group membership)
    group: str | None  # the "group" filter set by the query (applied to SiteGroup owner)
    start_time_since: datetime | None  # The "start_time_since" filter set by the query
    start_time_until: datetime | None  # The "start_time_until" filter set by the query

    controls: list[SiteControlResponse]  # The control models in this paged response


class SiteControlGroupRequest(BaseModel):
    """Used for creating new SiteControlGroups (used for grouping SiteControls)"""

    description: str  # Human readable description (32 char max)
    primacy: int  # Lower = Higher priority. Affects "child" controls relative priority when compared to other groups
    fsa_id: int | None = 1  # The function set assignment ID that this SiteControl group will be grouped under
    display_id: int | None = (
        None  # If set - seed the auto generated MRID with this value. equal display_id means equal mrid
    )
    required_site_group_id: int | None = (
        None  # If set - only sites in this SiteGroup will "see" this SiteControlGroup. Globally visible otherwise
    )


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
    after: datetime | None  # The "after" filter set by the query
    group: str | None  # the "group" filter set by the query
    site_control_groups: list[SiteControlGroupResponse]  # The control group models in this paged response


class UpdateDefaultValue(BaseModel):
    """Used to allow the setting of None or a specific value"""

    value: Decimal | None  # The decimal value to update (or None to update the value to None)


class SiteControlGroupDefaultRequest(BaseModel):
    """Used for updating fields associated with the SiteControlGroupDefault values - used when there is no active
    control"""

    import_limit_watts: (
        UpdateDefaultValue | None
    )  # If set - update The default "import limit watts" used in absence of an active control
    export_limit_watts: (
        UpdateDefaultValue | None
    )  # If set - update The default "export limit watts" used in absence of an active control
    generation_limit_watts: (
        UpdateDefaultValue | None
    )  # If set - update The default "generation limit watts" used in absence of an active control
    load_limit_watts: (
        UpdateDefaultValue | None
    )  # If set - update The default "export limit watts" used in absence of an active control
    ramp_rate_percent_per_second: (
        UpdateDefaultValue | None
    )  # If set - update The default ramp rate expressed in a percent of max W per second

    # Storage extension
    # If set - update the default "storage target watts" used in absence of an active control
    storage_target_watts: UpdateDefaultValue | None


class SiteControlGroupDefaultResponse(BaseModel):
    """Snapshot of the current SiteControlGroupDefault values that are used if no specific control is active"""

    server_default_import_limit_watts: Decimal | None  # None means NO default
    server_default_export_limit_watts: Decimal | None
    server_default_generation_limit_watts: Decimal | None
    server_default_load_limit_watts: Decimal | None
    ramp_rate_percent_per_second: Decimal | None

    # Storage extension
    server_default_storage_target_watts: Decimal | None

    created_time: datetime
    changed_time: datetime
