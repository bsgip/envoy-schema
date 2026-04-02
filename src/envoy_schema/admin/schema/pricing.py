from datetime import datetime
from typing import Optional

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


class TariffResponse(TariffRequest):
    """Response model for Tariff including id and modification time."""

    tariff_id: int
    created_time: datetime
    changed_time: datetime


class TariffComponentRequest(BaseModel):
    """Basic attributes for the creation of a new tariff component that sits underneath a specific Tariff"""

    tariff_id: int

    role_flags: RoleFlagsType
    description: Optional[str] = None

    # ReadingType fields
    accumulation_behaviour: Optional[AccumulationBehaviourType] = None
    commodity: Optional[CommodityType] = None
    data_qualifier: Optional[DataQualifierType] = None
    flow_direction: Optional[FlowDirectionType] = None
    kind: Optional[KindType] = None
    phase: Optional[PhaseCode] = None
    power_of_ten_multiplier: Optional[int] = None
    uom: Optional[UomType] = None


class TariffComponentResponse(TariffComponentRequest):
    """Response model for TariffComponent including id and modification time."""

    tariff_component_id: int
    created_time: datetime
    changed_time: datetime


class TariffGeneratedRateRequest(BaseModel):
    """Time of use tariff pricing - represents a price for a specific site for a specific range of time as defined
    by the parent TariffComponent."""

    tariff_component_id: int  # The TariffComponent ID that this price entry sits underneath
    site_id: int
    calculation_log_id: Optional[int]  # The ID of the CalculationLog that created this rate (or NULL if no link)
    start_time: datetime
    duration_seconds: int
    price_pow10_encoded: int  # Price encoded as per parent Tariff.price_power_of_ten_multiplier
    block_1_start_pow10_encoded: Optional[int] = None  # This much consumption of TariffComponent triggers a new price
    price_pow10_encoded_block_1: Optional[int] = None  # Price used after price_pow10_encoded_block_1 consumption


class TariffGeneratedRateResponse(TariffGeneratedRateRequest):
    tariff_generated_rate_id: int
    tariff_id: int
    created_time: datetime
    changed_time: datetime
