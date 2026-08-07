from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from envoy_schema.server.schema.sep2.der import (
    AbnormalCategoryType,
    AlarmStatusType,
    ConnectStatusType,
    DERControlType,
    DERType,
    DOESupportedMode,
    InverterStatusType,
    LocalControlModeStatusType,
    NormalCategoryType,
    OperationalModeStatusType,
    VPPControlType,
)
from envoy_schema.server.schema.sep2.types import DeviceCategory


class DERConfiguration(BaseModel):
    """Represents a combination of the sep2 DERSettings + DERCapability. The values here will use the current setting
    value (if specified) otherwise they will fallback to the nameplate rating (if available)"""

    # Mandatory values
    created_time: datetime
    changed_time: datetime
    modes_supported: DERControlType
    type: DERType
    doe_modes_supported: DOESupportedMode
    max_w: Decimal  # Max continuous active power in watts

    # Optional values
    vpp_modes_supported: VPPControlType | None
    abnormal_category: AbnormalCategoryType | None
    normal_category: NormalCategoryType | None
    max_a: Decimal | None  # Max continuous AC current capability in Amperes
    max_ah: Decimal | None  # Usable energy storage in AmpHours
    max_charge_rate_va: Decimal | None
    max_charge_rate_w: Decimal | None
    max_discharge_rate_va: Decimal | None
    max_discharge_rate_w: Decimal | None
    max_v: Decimal | None
    min_v: Decimal | None
    min_wh: Decimal | None
    max_va: Decimal | None
    max_var: Decimal | None  # Max reactive power delivered by the DER in VAR
    max_var_neg: Decimal | None  # Max reactive power receivable by the DER in VAR. Defaults to -'ve max_var
    max_wh: Decimal | None
    v_nom: Decimal | None  # Nominal AC voltage


class DERAvailability(BaseModel):
    """ "Represents the current availability values associated with a Site's DER. Typically used for communicating
    the current snapshot of DER energy held in reserve"""

    # Mandatory values
    created_time: datetime
    changed_time: datetime

    # Optional values
    availability_duration_sec: int | None
    max_charge_duration_sec: int | None
    reserved_charge_percent: Decimal | None
    reserved_deliver_percent: Decimal | None
    estimated_var_avail: Decimal | None
    estimated_w_avail: Decimal | None


class DERStatus(BaseModel):
    """Represents the current status values associated with a Site's DER. Typically used for communicating
    the current snapshot of DER status"""

    # Mandatory values
    created_time: datetime
    changed_time: datetime

    # Optional values
    alarm_status: AlarmStatusType | None
    generator_connect_status: ConnectStatusType | None
    generator_connect_status_time: datetime | None
    inverter_status: InverterStatusType | None
    inverter_status_time: datetime | None
    local_control_mode_status: LocalControlModeStatusType | None
    local_control_mode_status_time: datetime | None
    manufacturer_status: str | None
    manufacturer_status_time: datetime | None
    operational_mode_status: OperationalModeStatusType | None
    operational_mode_status_time: datetime | None


class SiteGroup(BaseModel):
    """Represents a named group that a site might belong to"""

    site_group_id: int
    name: str
    created_time: datetime
    changed_time: datetime


class SiteResponse(BaseModel):
    """Response model for Site - includes the common details"""

    aggregator_id: int
    site_id: int
    nmi: str | None
    timezone_id: str
    created_time: datetime
    changed_time: datetime
    lfdi: str
    sfdi: int
    device_category: DeviceCategory
    post_rate_seconds: int | None = None  # The current post rate (in seconds) set for this Site (if Any)

    groups: list[SiteGroup]

    der_config: DERConfiguration | None  # Metadata about site DER - no guarantee on availability
    der_availability: DERAvailability | None  # Metadata about site DER - no guarantee on availability
    der_status: DERStatus | None  # Metadata about site DER - no guarantee on availability


class SitePageResponse(BaseModel):
    """Represents a paginated response of Site"""

    total_count: int  # The total number of sites (independent of this page of results)
    limit: int  # The maximum number of sites that could've been returned (the limit set by the query)
    start: int  # The number of sites that have been skipped as part of this query (the start set by the query)
    group: str | None  # The "group" filter set by the query (if any)
    nmi: str | None  # The "nmi" filter set by the query (if any)
    aggregator_id: int | None  # The "aggregator_id" filter set by the query (if any)
    after: datetime | None  # The "after" filter set by the query (if any)
    sites: list[SiteResponse]  # The site models in this page


class SiteUpdateRequest(BaseModel):
    """Used for updating a specific site's configuration"""

    nmi: str | None = None  # If set - update the NMI value for the site. Set to empty string to "delete" the NMI
    timezone_id: str | None = None  # If set - update the timezone_id for the site
    device_category: DeviceCategory | None = None  # If set - update the device_category for the site
    post_rate_seconds: int | None = (
        None  # If set - update the site's post rate. Setting a zero or negative value will "delete" the post rate
    )
    group_ids: list[int] | None = None  # If set - replace all group assignments with these site_group_ids
