from enum import IntEnum
from typing import Optional

from pydantic_xml import attr, element

from envoy_schema.server.schema.sep2 import primitive_types
from envoy_schema.server.schema.sep2.base import BaseXmlModelWithNS
from envoy_schema.server.schema.sep2.identification import IdentifiedObject
from envoy_schema.server.schema.sep2.identification import List as Sep2List
from envoy_schema.server.schema.sep2.identification import ListLink, Resource
from envoy_schema.server.schema.sep2.time import TimeType
from envoy_schema.server.schema.sep2.types import DEFAULT_POLLRATE_SECONDS, PerCent


class ResponseType(IntEnum):
    """Derived from sep2 Table 27 - Response types by function set. All other values reserved"""

    EVENT_RECEIVED = 1
    EVENT_STARTED = 2
    EVENT_COMPLETED = 3
    USER_CHOSE_OPT_OUT = 4
    USER_CHOSE_OPT_IN = 5
    EVENT_CANCELLED = 6
    EVENT_SUPERSEDED = 7
    EVENT_PARTIAL_COMPLETE_USER_OPT_OUT = 8
    EVENT_PARTIAL_COMPLETE_USER_OPT_IN = 9
    EVENT_COMPLETE_NO_USER_PARTICIPATION = 10
    USER_ACKNOWLEDGED_EVENT = 11
    CANNOT_BE_DISPLAYED = 12
    EVENT_ABORTED_DUE_TO_ALTERNATE_SERVER_EVENT = 13
    EVENT_ABORTED_DUE_TO_ALTERNATE_PROGRAM_EVENT = 14
    REJECTED_CONTROL_PARAM_NOT_APPLICABLE = 252
    REJECTED_INVALID_EVENT = 253
    REJECTED_EVENT_RECEIVED_LATE = 254


class ApplianceLoadReductionType(IntEnum):
    """Full definition of how appliances react when receiving each parameter is document in the EPA document,
    ENERGY STAR® Program Requirements, Product Specification for Residential Refrigerators and
    Freezers, Eligibility Criteria 5, Draft 2 Version 5.0.
    All other values reserved"""

    DELAY_APPLIANCE_LOAD = 0
    TEMPORARY_APPLIANCE_LOAD_REDUCTION = 1


class ResponseSet(IdentifiedObject):
    """A container for a ResponseList"""

    ResponseListLink: Optional[ListLink] = element(default=None)


class Response(Resource):
    """The Response object is the generic response data repository which is extended for specific function sets."""

    createdDateTime: Optional[TimeType] = element(default=None)
    endDeviceLFDI: primitive_types.HexBinary160 = element()
    status: Optional[ResponseType] = element(default=None)
    subject: primitive_types.HexBinary128 = element()


class ResponseListResponse(Sep2List, tag="ResponseList"):
    """List element for holding Response objects"""

    Response_: Optional[list[Response]] = element(default=None, tag="Response")


class ResponseSetList(Sep2List):
    """A List element to hold ResponseSet objects."""

    pollRate: Optional[int] = attr(default=DEFAULT_POLLRATE_SECONDS)  # recommended client pollrate in seconds
    ResponseSet_: Optional[list[ResponseSet]] = element(default=None, tag="ResponseSet")


class DERControlResponse(Response):
    """A response to a DERControl"""

    pass


class FlowReservationResponseResponse(Response):
    """A response to a FlowReservationResponse"""

    pass


class PriceResponse(Response):
    """A response related to a price message."""

    pass


class TextResponse(Response):
    """A response related to a text message."""

    pass


class ApplianceLoadReduction(BaseXmlModelWithNS):
    """The ApplianceLoadReduction object is used by a Demand Response service provider to provide signals for ENERGY
    STAR compliant appliances. See the definition of ApplianceLoadReductionType for more information."""

    type: int = element()  # Values drawn from ApplianceLoadReductionType


class AppliedTargetReduction(BaseXmlModelWithNS):
    """Specifies the value of the TargetReduction applied by the device."""

    type: int = element()  # Values drawn from UnitValueType
    value: int = element()  # The requested amount of the relevant commodity to be reduced.


class SetPoint(BaseXmlModelWithNS):
    """The SetPoint object is used to apply specific temperature set points to a temperature control device. The values
    of the heatingSetpoint and coolingSetpoint attributes SHALL be calculated as follows:

    Cooling/Heating Temperature Set Point / 100 = temperature in degrees Celsius where
    -273.15°C <= temperature <= 327.67°C, corresponding to a Cooling and/or Heating Temperature Set Point.

    The maximum resolution this format allows is 0.01°C.

    The field not present in a Response indicates that this field has not been used by the end device.
    If a temperature is sent that exceeds the temperature limit boundaries that are programmed into the device,
    the device SHALL respond by setting the temperature at the limit."""

    coolingSetpoint: int = (
        element()
    )  # This attribute represents the cooling temp set point in degrees Celsius / 100. (Hundredths of a degree C)

    heatingSetpoint: int = (
        element()
    )  # This attribute represents the heating temp set point in degrees Celsius / 100. (Hundredths of a degree C)


class Offset(BaseXmlModelWithNS):
    """If a temperature offset is sent that causes the heating or cooling temperature set point to exceed the limit
    boundaries that are programmed into the device, the device SHALL respond by setting the temperature at the limit.

    If an EDC is being targeted at multiple devices or to a device that controls multiple devices (e.g., EMS), it can
    provide multiple Offset types within one EDC. For events with multiple Offset types, a client SHALL select the
    Offset that best fits their operating function.

    Alternatively, an event with a single Offset type can be targeted at an EMS in order to request a percentage load
    reduction on the average energy usage of the entire premise. An EMS SHOULD use the Metering function set to
    determine the initial load in the premise, reduce energy consumption by controlling devices at its disposal, and
    at the conclusion of the event, once again use the Metering function set to determine if the desired load reduction
    was achieved."""

    # The value change requested for the cooling offset, in degree C / 10. The value should be added to the normal set
    # point for cooling, or if loadShiftForward is true, then the value should be subtracted from the normal set point.
    coolingOffset: Optional[int] = element(default=None)

    # The value change requested for the heating offset, in degree C / 10. The value should be subtracted for heating,
    # or if loadShiftForward is true, then the value should be added to the normal set point.
    heatingOffset: Optional[int] = element(default=None)

    # The value change requested for the load adjustment percentage. The value should be subtracted from the normal
    # setting, or if loadShiftForward is true, then the value should be added to the normal setting.
    loadAdjustmentPercentageOffset: Optional[PerCent] = element(default=None)


class DutyCycle(BaseXmlModelWithNS):
    """Duty cycle control is a device specific issue and is managed by the device.  The duty cycle of the device under
    control should span the shortest practical time period in accordance with the nature of the device under control
    and the intent of the request for demand reduction.

    The default factory setting SHOULD be three minutes for each 10% of duty cycle.  This indicates that the default
    time period over which a duty cycle is applied is 30 minutes, meaning a 10% duty cycle would cause a device to be
    ON for 3 minutes.

    The “off state” SHALL precede the “on state”."""

    # Contains the maximum On state duty cycle applied by the end device, as a percentage of time.  The field not
    # present indicates that this field has not been used by the end device.
    normalValue: int = element()


class DrResponse(Response):
    """A response to a Demand Response Load Control (EndDeviceControl) message."""

    ApplianceLoadReduction_: Optional[ApplianceLoadReduction] = element(default=None, tag="ApplianceLoadReduction")

    AppliedTargetReduction_: Optional[AppliedTargetReduction] = element(default=None, tag="AppliedTargetReduction")
    DutyCycle_: Optional[DutyCycle] = element(default=None, tag="DutyCycle")
    Offset_: Optional[Offset] = element(default=None, tag="Offset")
    # Indicates the amount of time, in seconds, that the client partially opts-out during the demand response event.
    # When overriding within the allowed override duration, the client SHALL send a partial opt-out (Response status
    # code 8) for partial opt-out upon completion, with the total time the event was overridden (this attribute)
    # populated. The client SHALL send a no participation status response (status type 10) if the user partially
    # opts-out for longer than EndDeviceControl.overrideDuration.
    overrideDuration: Optional[int] = element(default=None)
    SetPoint_: Optional[SetPoint] = element(default=None, tag="SetPoint")
