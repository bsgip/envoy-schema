from datetime import datetime

from pydantic import BaseModel

from envoy_schema.server.schema.sep2.types import (
    AccumulationBehaviourType,
    CommodityType,
    CurrencyCode,
    DataQualifierType,
    FlowDirectionType,
    KindType,
    PhaseCode,
    RoleFlagsType,
    UomType,
)


class TariffRequest(BaseModel):
    """Basic attributes for the creation of a new tariff."""

    name: str
    dnsp_code: str
    currency_code: CurrencyCode
    price_power_of_ten_multiplier: int
    primacy: int
    fsa_id: int = 1  # The function set assignment ID that this Tariff will be grouped under
    required_site_group_id: int | None = (
        None  # If set - only sites in this SiteGroup will "see" this Tariff. Globally visible otherwise
    )


class TariffResponse(TariffRequest):
    """Response model for Tariff including id and modification time."""

    tariff_id: int
    created_time: datetime
    changed_time: datetime


class TariffPageResponse(BaseModel):
    """Paginated response for listing tariffs."""

    total_count: int
    limit: int
    start: int
    group: str | None  # the "group" filter set by the query
    tariffs: list[TariffResponse]


class TariffComponentRequest(BaseModel):
    """Basic attributes for the creation of a new tariff component that sits underneath a specific Tariff"""

    tariff_id: int

    role_flags: RoleFlagsType
    description: str | None = None

    # ReadingType fields
    accumulation_behaviour: AccumulationBehaviourType | None = None
    commodity: CommodityType | None = None
    data_qualifier: DataQualifierType | None = None
    flow_direction: FlowDirectionType | None = None
    kind: KindType | None = None
    phase: PhaseCode | None = None
    power_of_ten_multiplier: int | None = None
    uom: UomType | None = None


class TariffComponentResponse(TariffComponentRequest):
    """Response model for TariffComponent including id and modification time."""

    tariff_component_id: int
    created_time: datetime
    changed_time: datetime


class TariffGeneratedRateRequest(BaseModel):
    """Time of use tariff pricing - represents a price for a specific site group for a specific range of time as defined
    by the parent TariffComponent."""

    tariff_component_id: int  # The TariffComponent ID that this price entry sits underneath
    site_group_id: int  # The SiteGroup id whose members will have this price available to them
    calculation_log_id: int | None  # The ID of the CalculationLog that created this rate (or NULL if no link)
    start_time: datetime
    duration_seconds: int
    price_pow10_encoded: int  # Price encoded as per parent Tariff.price_power_of_ten_multiplier
    block_1_start_pow10_encoded: int | None = None  # This much consumption of TariffComponent triggers a new price
    price_pow10_encoded_block_1: int | None = None  # Price used after price_pow10_encoded_block_1 consumption


class TariffGeneratedRateResponse(TariffGeneratedRateRequest):
    tariff_generated_rate_id: int
    tariff_id: int
    created_time: datetime
    changed_time: datetime


class TariffGeneratedRatePageResponse(BaseModel):
    """Paginated response for listing tariff generated rates under a TariffComponent. All rates on the page share
    the same TariffComponent"""

    total_count: int
    limit: int
    start: int
    tariff_component_id: int  # The "tariff_component_id" filter set on the path
    start_time_since: datetime | None  # The "start_time_since" filter set by the query
    start_time_until: datetime | None  # The "start_time_until" filter set by the query
    group: str | None  # the "group" filter set by the query (applied to SiteGroup owner)
    site_id: int | None  # the "site_id" filter set by the query (applied to Site and SiteGroup membership)
    rates: list[TariffGeneratedRateResponse]
