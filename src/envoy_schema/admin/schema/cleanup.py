"""Models for admin endpoints that clear out old/expired data from the utility server database."""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class ExpiredCleanupMode(StrEnum):
    """How expired entities should be removed from their "active" table"""

    archive = "archive"  # DEFAULT - Remove the entities, copying them into the associated archive table first
    delete = "delete"  # Remove the entities permanently - nothing will be written to the archive table


class ExpiredCleanupRequest(BaseModel):
    """Requests the removal of all time bound entities (eg SiteControls / TariffGeneratedRates) that have expired.

    An entity is considered expired if its end time (start_time + duration_seconds) is at or before expired_before.
    Entities that are still active (or are yet to start) at expired_before will NOT be affected."""

    expired_before: datetime  # Only entities whose end time is <= this datetime will be removed
    mode: ExpiredCleanupMode = ExpiredCleanupMode.archive  # How the entities should be removed


class CleanupResponse(BaseModel):
    """The result of a cleanup request against a single table"""

    removed_count: int  # The number of entities that were removed


class ArchiveCleanupType(StrEnum):
    """The various archive tables that can be targeted for cleanup"""

    site = "site"
    site_group = "site_group"
    site_group_assignment = "site_group_assignment"
    site_der_rating = "site_der_rating"
    site_der_setting = "site_der_setting"
    site_der_availability = "site_der_availability"
    site_der_status = "site_der_status"
    site_reading_type = "site_reading_type"
    site_reading = "site_reading"
    site_control_group = "site_control_group"
    site_control_group_default = "site_control_group_default"
    site_control = "site_control"
    tariff = "tariff"
    tariff_component = "tariff_component"
    tariff_generated_rate = "tariff_generated_rate"
    subscription = "subscription"
    subscription_condition = "subscription_condition"
    runtime_server_config = "runtime_server_config"


class ArchiveCleanupRequest(BaseModel):
    """Requests the permanent deletion of archive table records whose archive_time is at or before archived_before."""

    archived_before: datetime  # Only archive records with archive_time <= this datetime will be deleted
    archive_types: list[ArchiveCleanupType] | None = None  # The archive tables to target. None means ALL tables


class ArchiveCleanupResponse(BaseModel):
    """The result of an ArchiveCleanupRequest"""

    archived_before: datetime  # The archived_before parameter from the original request
    removed_counts: dict[ArchiveCleanupType, int]  # Number of records deleted, keyed by each targeted archive table
