from datetime import datetime
from decimal import Decimal
from typing import Optional

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
    abnormal_category: Optional[AbnormalCategoryType]
    normal_category: Optional[NormalCategoryType]
    max_a: Optional[Decimal]  # Max continuous AC current capability in Amperes
    max_ah: Optional[Decimal]  # Usable energy storage in AmpHours
    max_charge_rate_va: Optional[Decimal]
    max_charge_rate_w: Optional[Decimal]
    max_discharge_rate_va: Optional[Decimal]
    max_discharge_rate_w: Optional[Decimal]
    max_v: Optional[Decimal]
    min_v: Optional[Decimal]
    max_va: Optional[Decimal]
    max_var: Optional[Decimal]  # Max reactive power delivered by the DER in VAR
    max_var_neg: Optional[Decimal]  # Max reactive power receivable by the DER in VAR. Defaults to -'ve max_var
    max_wh: Optional[Decimal]
    v_nom: Optional[Decimal]  # Nominal AC voltage


class DERAvailability(BaseModel):
    """ "Represents the current availability values associated with a Site's DER. Typically used for communicating
    the current snapshot of DER energy held in reserve"""

    # Mandatory values
    created_time: datetime
    changed_time: datetime

    # Optional values
    availability_duration_sec: Optional[int]
    max_charge_duration_sec: Optional[int]
    reserved_charge_percent: Optional[Decimal]
    reserved_deliver_percent: Optional[Decimal]
    estimated_var_avail: Optional[Decimal]
    estimated_w_avail: Optional[Decimal]


class DERStatus(BaseModel):
    """Represents the current status values associated with a Site's DER. Typically used for communicating
    the current snapshot of DER status"""

    # Mandatory values
    created_time: datetime
    changed_time: datetime

    # Optional values
    alarm_status: Optional[AlarmStatusType]
    generator_connect_status: Optional[ConnectStatusType]
    generator_connect_status_time: Optional[datetime]
    inverter_status: Optional[InverterStatusType]
    inverter_status_time: Optional[datetime]
    local_control_mode_status: Optional[LocalControlModeStatusType]
    local_control_mode_status_time: Optional[datetime]
    manufacturer_status: Optional[str]
    manufacturer_status_time: Optional[datetime]
    operational_mode_status: Optional[OperationalModeStatusType]
    operational_mode_status_time: Optional[datetime]


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
    nmi: Optional[str]
    timezone_id: str
    created_time: datetime
    changed_time: datetime
    lfdi: str
    sfdi: int
    device_category: DeviceCategory

    groups: list[SiteGroup]

    der_config: Optional[DERConfiguration]  # Metadata about site DER - no guarantee on availability
    der_availability: Optional[DERAvailability]  # Metadata about site DER - no guarantee on availability
    der_status: Optional[DERStatus]  # Metadata about site DER - no guarantee on availability


class SitePageResponse(BaseModel):
    """Represents a paginated response of Site"""

    total_count: int  # The total number of sites (independent of this page of results)
    limit: int  # The maximum number of sites that could've been returned (the limit set by the query)
    start: int  # The number of sites that have been skipped as part of this query (the start set by the query)
    group: Optional[str]  # The "group" filter set by the query (if any)
    after: Optional[datetime]  # The "after" filter set by the query (if any)
    sites: list[SiteResponse]  # The site models in this page
