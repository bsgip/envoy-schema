from enum import IntEnum
from typing import Optional

from pydantic_xml import attr, element

from envoy_schema.server.schema.sep2 import primitive_types, types
from envoy_schema.server.schema.sep2.identification import Resource, SubscribableList


class FunctionSetIdentifier(IntEnum):
    """The various FunctionSetIdentifiers defined in sep2. All other values are reserved."""

    GENERAL = 0
    PUBLISH_AND_SUBSCRIBE = 1
    END_DEVICE = 2
    FUNCTION_SET_ASSIGNMENT = 3
    RESPONSE = 4
    DEMAND_RESPONSE_LOAD_CONTROL = 5
    METERING = 6
    PRICING = 7
    MESSAGING = 8
    BILLING = 9
    PREPAYMENT = 10
    DISTRIBUTED_ENERGY_RESOURCES = 11
    TIME = 12
    SOFTWARE_DOWNLOAD = 13
    DEVICE_INFORMATION = 14
    POWER_STATUS = 15
    NETWORK_STATUS = 16
    LOG_EVENT_LIST = 17
    CONFIGURATION = 18
    SECURITY = 19


class ProfileIdentifier(IntEnum):
    """All other values are reserved"""

    NOT_PROFILE_SPECIFIC = 0
    VENDOR_DEFINED = 1
    IEEE_2030_5 = 2
    HOM_AUTOMATION = 3
    BUILDING_AUTOMATION = 4


class LogEvent(Resource):
    """A time stamped instance of a significant event detected by the device."""

    createdDateTime: types.TimeType = element()
    details: Optional[primitive_types.String32] = element(
        default=None
    )  # Human readable text that MAY be used to transmit additional details about the event. Host may remove this.

    extendedData: Optional[int] = element()  # May be used to transmit additional details about the event.
    functionSet: FunctionSetIdentifier = element()
    logEventCode: int = element()  # An 8 bit unsigned integer. logEventCodes are scoped to a profile and a function set
    logEventID: int = element()  # An 16 bit unsigned integer.
    logEventPEN: int = element()  # A 32 bit private enterprise number (PEN) of the entity creating this LogEvent
    profileID: ProfileIdentifier = element()  # An 8 bit unsigned integer.


class LogEventList(SubscribableList):
    pollRate: Optional[int] = attr(default=types.DEFAULT_POLLRATE_SECONDS)  # recommended client pollrate in seconds
    LogEvent_: Optional[list[LogEvent]] = element(default=None, tag="LogEvent")
