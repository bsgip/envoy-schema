from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CalculationLogMetadata(BaseModel):
    """This is purely descriptive metadata to highlight what an opaque CalculationLogVariable represents"""

    variable_id: int  # The variable that this metadata applies to
    name: str  # Short, human readable name for the referenced variable
    description: str  # Longer, human readable description of the variable


class CalculationLogVariableValues(BaseModel):
    """This is a compact representation of MANY variable instances. It's expected that EVERY property list has the
    same number of elements (i.e. there is a 1-1 correspondence between lists).

    eg: {
      variable_ids: [1,2]
      site_ids: [3, None]
      interval_periods: [5, 6]
      values: [7.7, 8.8]
    }

    Logically represents:

    [
        {variable_id: 1, site_id: 3, interval_period: 5, value: 7.7},
        {variable_id: 2, site_id: None, interval_period: 6, value: 8.8},
    ]

    A single variable value represents a single time series observation for a specific variable. The definition
    of what a variable represents is opaque to the utility server.

    Within a CalculationLog, the combination of variable_id, site_id and interval_period are a unique index
    """

    # ID defined by the client that disambiguate one set of time-series from another data from another. eg: a value of 1
    # might represent weather forecast temperature, a value of 2 might represent forecast load etc. The actual
    # definitions are completely opaque to utility server.
    variable_ids: list[int]  # Must correspond 1-1 with each other list in this type

    # Foreign key reference to a specific site ID that the variable value applies to or NONE if this time series
    # observation is NOT tied to a specific site.
    site_ids: list[Optional[int]]  # Must correspond 1-1 with each other list in this type

    # When does this time series observation occur? Defines the numbered "interval" relative to the parent
    # CalculationLog.calculation_range_start. A value of N uses the following formula for calculating datetime:
    # CalculationLog.calculation_range_start + N * CalculationLog.interval_width_seconds
    interval_periods: list[int]  # Must correspond 1-1 with each other list in this type

    # The actual time series value associated with the linked variable_id, site_id and interval_period
    values: list[float]  # Must correspond 1-1 with each other list in this type


class CalculationLogRequest(BaseModel):
    """Represents the top level entity describing a single audit log of a historical calculation run.

    Calculation runs typically represent running powerflow / other model for some network. A calculation log represents
    a (mostly) opaque log of values defined by an external calculation engine. Any given calculation log has the
    following assumptions:
        * A calculation log represents a defined "range" of time for which the output calculations apply for
           eg: A single log might represent a 24 hour period of time - typically this range is in advance of when the
               calculations are being made.
        * A calculation log is divided into fixed width intervals of a known size, eg 5 minutes. All input data/outputs
          are aligned with these intervals. Eg - A 24 hour period is broken down into intervals of length 1 hour.
        * A calculation log has logged "variable" data representing input/intermediate/output data. This data is opaque
          to the utility server but it WILL align with intervals.
    """

    calculation_range_start: datetime  # The start time of the first interval within this calculation log.
    calculation_range_duration_seconds: int  # Number of seconds that define the width of this entire calculation log
    interval_width_seconds: int  # Number of seconds for the fixed width intervals that comprise this calculation log

    topology_id: Optional[str] = None  # The ID of the network topology being forecast (eg feeder ID)
    external_id: Optional[str] = None  # An ID for the external submitting client to identify this calculation log
    description: Optional[str] = None  # A human readable description of this calculation log

    power_forecast_creation_time: Optional[datetime] = None  # Datetime for when any power forecast was created

    # When was the last (most recent) historical lag. The time between this and the calculation_range_start represents
    # how stale the lag data was.
    power_forecast_basis_time: Optional[datetime] = None

    weather_forecast_creation_time: Optional[datetime] = None  # Datetime for when any weather forecast was created
    weather_forecast_location_id: Optional[str] = None  # ID associated the weather location that the forecast is for

    variable_metadata: list[CalculationLogMetadata]  # Metadata associated with the variables defined in variable_values
    variable_values: Optional[CalculationLogVariableValues]  # The actual time series observations in this calculation


class CalculationLogResponse(CalculationLogRequest):
    """Represents the top level entity describing a single audit log of a historical calculation run.

    Calculation runs typically represent running powerflow / other model for some network based on forecast
    power/weather data (usually over multiple time steps) that may propose certain changes in DER behavior
    in order to satisfy certain network constraints"""

    calculation_log_id: int
    created_time: datetime


class CalculationLogListResponse(BaseModel):
    """A list response of CalculationLogResponse entities. Don't expect CalculationLogResponse to include
    any child logs - those can be fetched using calculation_log_id in a subsequent request.

    Represents a page of items and a total of all available items"""

    start: int
    limit: int
    total_calculation_logs: int
    calculation_logs: list[CalculationLogResponse]
