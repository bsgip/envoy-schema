from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from envoy_schema.server.schema.sep2.types import CurrencyCode


class TariffRequest(BaseModel):
    """Basic attributes for the creation of a new tariff structure."""

    name: str
    dnsp_code: str
    currency_code: CurrencyCode
    fsa_id: int = 1  # The function set assignment ID that this Tariff will be grouped under


class TariffResponse(BaseModel):
    """Response model for Tariff including id and modification time."""

    tariff_id: int
    name: str
    dnsp_code: str
    currency_code: CurrencyCode
    created_time: datetime
    changed_time: datetime


class TariffGeneratedRateRequest(BaseModel):
    """Time of use tariff pricing - represents a price for a specific site for a specific range of time"""

    tariff_id: int
    site_id: int
    calculation_log_id: Optional[int]  # The ID of the CalculationLog that created this rate (or NULL if no link)
    start_time: datetime
    duration_seconds: int
    import_active_price: Decimal  # Price in dollars per kw/h (holds 4 decimal places of precision)
    export_active_price: Decimal  # Price in dollars per kw/h (holds 4 decimal places of precision)
    import_reactive_price: Decimal  # Price is dollars per kvar/h (holds 4 decimal places of precision)
    export_reactive_price: Decimal  # Price is dollars per kvar/h (holds 4 decimal places of precision)


class TariffGeneratedRateResponse(TariffGeneratedRateRequest):
    tariff_generated_rate_id: int
    created_time: datetime
    changed_time: datetime
