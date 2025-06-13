from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class AdminSiteReading(BaseModel):
    """
    Admin representation of a site reading.
    For now this is kept simple as only active power watts.
    """

    reading_start_time: datetime
    duration_seconds: int
    active_watts_sum: Decimal


class AdminSiteReadingPageResponse(BaseModel):
    """Paginated response for admin site reading queries."""

    total_count: int  # Total number of readings matching the query
    limit: int  # Maximum number of readings that could be returned
    start: int  # Number of readings skipped for pagination
    site_id: int  # Site ID filter used in the query
    start_time: datetime  # Start time filter used in the query
    end_time: datetime  # End time filter used in the query
    readings: list[AdminSiteReading]  # The readings in this page
