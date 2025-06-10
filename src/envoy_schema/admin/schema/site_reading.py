from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from envoy_schema.server.schema.sep2.types import (
    AccumulationBehaviourType,
    DataQualifierType,
    FlowDirectionType,
    KindType,
    PhaseCode,
    QualityFlagsType,
    RoleFlagsType,
    UomType,
)


class AdminSiteReading(BaseModel):
    """
    Admin representation of a site reading with embedded reading type metadata.

    This class combines data from SiteReading and SiteReadingType models for convenience without requiring separate
    queries or multiple objects.
    """

    # Reading data
    site_reading_id: int
    site_id: int
    time_period_start: datetime
    time_period_seconds: int
    value: int
    local_id: Optional[int]
    quality_flags: QualityFlagsType
    reading_created_time: datetime
    reading_changed_time: datetime

    # Flattened reading type metadata
    site_reading_type_id: int
    aggregator_id: int
    uom: UomType
    data_qualifier: DataQualifierType
    flow_direction: FlowDirectionType
    accumulation_behaviour: AccumulationBehaviourType
    kind: KindType
    phase: PhaseCode
    power_of_ten_multiplier: int
    default_interval_seconds: int
    role_flags: RoleFlagsType
    reading_type_created_time: datetime
    reading_type_changed_time: datetime


class AdminSiteReadingPageResponse(BaseModel):
    """Paginated response for admin site reading queries."""

    total_count: int  # Total number of readings matching the query
    limit: int  # Maximum number of readings that could be returned
    start: int  # Number of readings skipped for pagination
    site_ids: list[int]  # Site IDs filter used in the query
    start_time: datetime  # Start time filter used in the query
    end_time: datetime  # End time filter used in the query
    readings: list[AdminSiteReading]  # The readings in this page
