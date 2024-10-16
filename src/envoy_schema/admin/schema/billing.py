from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class BillingReading(BaseModel):
    """Billing readings are a total across all phases for the period"""

    site_id: int
    period_start: datetime
    duration_seconds: int
    value: Decimal  # Positive indicates import, negative indicates export


class BillingTariffRate(BaseModel):
    site_id: int
    period_start: datetime
    duration_seconds: int
    import_active_price: Decimal
    export_active_price: Decimal
    import_reactive_price: Decimal
    export_reactive_price: Decimal


class BillingDoe(BaseModel):
    site_id: int
    period_start: datetime
    duration_seconds: int
    import_limit_active_watts: Decimal
    export_limit_watts: Decimal


class BaseBillingResponse(BaseModel):
    """Billing data common to all billing responses. All readings will come back as a total usage across all phases"""

    tariff_id: int

    varh_readings: list[BillingReading]  # Will be ordered by site_id then period_start
    wh_readings: list[BillingReading]  # Will be ordered by site_id then period_start
    watt_readings: list[BillingReading]  # Will be ordered by site_id then period_start
    active_tariffs: list[BillingTariffRate]  # Will be ordered by site_id then period_start
    active_does: list[BillingDoe]  # Will be ordered by site_id then period_start


class AggregatorBillingResponse(BaseBillingResponse):
    """Response model for a billing report scoped to a particular aggregator for a period of time"""

    aggregator_id: int
    aggregator_name: str
    period_start: datetime
    period_end: datetime


class CalculationLogBillingResponse(BaseBillingResponse):
    """Response model for a billing report scoped to a particular calculation log"""

    calculation_log_id: int


class SiteBillingResponse(BaseBillingResponse):
    """Response model for a billing report scoped to a particular set of site id's for a period of time"""

    site_ids: list[int]
    period_start: datetime
    period_end: datetime


MAX_SITE_IDS_IN_REQUEST = 100


class SiteBillingRequest(BaseModel):
    """Request to send to utility server to request a SiteBillingResponse for the specified parameters.
    (used with uri.SitePeriodBillingUri)"""

    site_ids: list[int] = Field(max_length=MAX_SITE_IDS_IN_REQUEST)  # Limited to MAX_SITE_IDS_IN_REQUEST items
    period_start: datetime
    period_end: datetime
    tariff_id: int
