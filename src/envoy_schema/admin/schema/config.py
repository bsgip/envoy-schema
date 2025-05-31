from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class UpdateDefaultValue(BaseModel):
    """Used to allow the setting of None or a specific value"""

    value: Optional[Decimal]  # The decimal value to update (or None to update the value to None)


class ControlDefaultRequest(BaseModel):
    """Used for updating the "failover" SiteControl defaults that are used if no specific control is active"""

    import_limit_watts: Optional[
        UpdateDefaultValue
    ]  # If set - update The default "import limit watts" used in absence of an active control
    export_limit_watts: Optional[
        UpdateDefaultValue
    ]  # If set - update The default "export limit watts" used in absence of an active control
    generation_limit_watts: Optional[
        UpdateDefaultValue
    ]  # If set - update The default "generation limit watts" used in absence of an active control
    load_limit_watts: Optional[
        UpdateDefaultValue
    ]  # If set - update The default "export limit watts" used in absence of an active control
    ramp_rate_percent_per_second: Optional[
        UpdateDefaultValue
    ]  # If set - update The default ramp rate expressed in a percent of max W per second


class ControlDefaultResponse(BaseModel):
    """Snapshot of the current "failover" SiteControl defaults that are used if no specific control is active"""

    server_default_import_limit_watts: Optional[Decimal]  # None means NO default
    server_default_export_limit_watts: Optional[Decimal]
    server_default_generation_limit_watts: Optional[Decimal]
    server_default_load_limit_watts: Optional[Decimal]
    ramp_rate_percent_per_second: Optional[Decimal]

    created_time: datetime
    changed_time: datetime


class RuntimeServerConfigRequest(BaseModel):
    """Used for updating the server configuration associated with runtime behavior"""

    dcap_pollrate_seconds: Optional[int] = None  # If set - update the DeviceCapability pollRate
    edevl_pollrate_seconds: Optional[int] = None  # If set - update the EndDeviceList pollRate
    fsal_pollrate_seconds: Optional[int] = None  # If set - update the FunctionSetAssignmentList pollRate
    derpl_pollrate_seconds: Optional[int] = None  # If set - update the DERProgram pollRate
    derl_pollrate_seconds: Optional[int] = None  # If set - update the DERList pollRate
    mup_postrate_seconds: Optional[int] = None  # If set - update the MirrorUsagePoint postRate

    # pow10 Values affect the associated integer sent. Eg for a "watts" value, setting pow10 to -3 will mean that
    # the encoded value of 12345 should be interpreted as 12.345 watts by the client. Setting a value of 2 will mean
    # that a value of 12345 should be interpreted as 1234500 watts.
    site_control_pow10_encoding: Optional[int] = None  # If set - update the pow10 encoded for sent DERControl values.
    tariff_pow10_encoding: Optional[int] = None  # If set - update the pow10 encoded for sent RateComponent values

    disable_edev_registration: Optional[bool] = None  # If True - EndDevice RegistrationLink's will be disabled


class RuntimeServerConfigResponse(BaseModel):
    """Snapshot of the server configuration associated with runtime behavior"""

    dcap_pollrate_seconds: int
    edevl_pollrate_seconds: int
    fsal_pollrate_seconds: int
    derpl_pollrate_seconds: int
    derl_pollrate_seconds: int
    mup_postrate_seconds: int

    site_control_pow10_encoding: int
    tariff_pow10_encoding: int

    disable_edev_registration: bool

    created_time: datetime
    changed_time: datetime
