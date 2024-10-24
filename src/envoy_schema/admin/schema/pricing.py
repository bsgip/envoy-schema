from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from envoy_schema.server.schema.sep2.types import CurrencyCode


class TariffRequest(BaseModel):
    """Basic attributes for the creation of a new tariff structure."""

    name: str
    dnsp_code: str
    currency_code: CurrencyCode


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
    import_active_price: float  # Price in dollars per kw/h
    export_active_price: float  # Price in dollars per kw/h
    import_reactive_price: float  # Price is dollars per kvar/h
    export_reactive_price: float  # Price is dollars per kvar/h


class TariffGeneratedRateResponse(TariffGeneratedRateRequest):
    tariff_generated_rate_id: int
    created_time: datetime
    changed_time: datetime
