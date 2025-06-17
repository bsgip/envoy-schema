from datetime import datetime
from decimal import Decimal
from enum import IntEnum

from pydantic import BaseModel


class CSIPAusSiteReadingUnit(IntEnum):
    """
    This enum aims to capture allowed csip aus compliant readings for a site as a single value.

    It assumes the following:
        - The Kind is 37 (POWER) or 0 (NA)
        - The data qualifier is 2 (Average) or 0 (NA)
        - Any RoleFlags are allowed, does not show whether sites are mirrors, DER, submeter, or aggregation points.
            If both site and device information are present (role flags 3 and 73, respectively, site data is returned)
        - Load convention applies: positive is import from the grid. If FlowDirectionType is stored it will be used,
            otherwise it is provided as stored (e.g. Flow type = 0 is not converted).
        - Other options are not filtered (DeviceCategory, CommodityType, etc). All are allowed, none are returned.
    """

    ACTIVEPOWER = 1  # W, UOM =  38
    REACTIVEPOWER = 2  # Var, UOM = 63
    FREQUENCY = 3  # Hz, UOM = 33

    SINGLEPHASEVOLTAGE = 4  # V, UOM = 29, Phase code = 0 (NA)
    VOLTAGEPHASEAN = 5  # V, UOM = 29, Phase code = 129 (AN)
    VOLTAGEPHASEBN = 6  # V, UOM = 29, Phase code  = 65 (BN)
    VOLTAGEPHASECN = 7  # V, UOM = 29, Phase code  = 33 (CN)


class CSIPAusSiteReading(BaseModel):
    """
    Admin representation of a csip aus compliant reading for a specific site and reading unit (CSIPReadingUnit).
    """

    reading_start_time: datetime
    duration_seconds: int
    value: Decimal


class CSIPAusSiteReadingPageResponse(BaseModel):
    """Paginated response for csip aus site reading queries."""

    total_count: int  # Total number of readings matching the query
    limit: int  # Maximum number of readings that could be returned
    start: int  # Number of readings skipped for pagination
    site_id: int  # Site ID filter used in the query
    csip_aus_unit: CSIPAusSiteReadingUnit  # # CSIP Aus unit enum used for the query
    start_time: datetime  # Start time filter used in the query
    end_time: datetime  # End time filter used in the query
    readings: list[CSIPAusSiteReading]  # The readings in this page
