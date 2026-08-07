from pydantic_xml import attr, element

from envoy_schema.server.schema.csip_aus.connection_point import ConnectionPointLink as ConnectionPointLinkType
from envoy_schema.server.schema.sep2 import primitive_types
from envoy_schema.server.schema.sep2.identification import (
    Link,
    ListLink,
    Resource,
    SubscribableList,
    SubscribableResource,
)
from envoy_schema.server.schema.sep2.time import TimeType
from envoy_schema.server.schema.sep2.types import DEFAULT_POLLRATE_SECONDS, PINType


class AbstractDevice(SubscribableResource):
    ConfigurationLink: Link | None = element(default=None)
    DERListLink: ListLink | None = element(default=None)
    deviceCategory: primitive_types.HexBinary32 | None = element(default=None)
    DeviceInformationLink: Link | None = element(default=None)
    DeviceStatusLink: Link | None = element(default=None)
    FileStatusLink: Link | None = element(default=None)
    IPInterfaceListLink: Link | None = element(default=None)
    lFDI: str | None = element(default=None)
    LoadShedAvailabilityListLink: ListLink | None = element(default=None)
    LogEventListLink: ListLink | None = element(default=None)
    PowerStatusLink: Link | None = element(default=None)
    sFDI: int = element()


class EndDeviceRequest(AbstractDevice, tag="EndDevice"):
    changedTime: TimeType = element()
    enabled: bool | None = element(default=True)
    postRate: int | None = element(default=None)


class EndDeviceResponse(AbstractDevice, tag="EndDevice"):
    changedTime: TimeType = element()
    enabled: bool | None = element(default=True)

    FlowReservationRequestListLink: Link | None = element(default=None)
    FlowReservationResponseListLink: Link | None = element(default=None)
    FunctionSetAssignmentsListLink: ListLink | None = element(default=None)
    postRate: int | None = element(default=None)
    RegistrationLink: Link | None = element(default=None)
    SubscriptionListLink: ListLink | None = element(default=None)

    # csip extension
    ConnectionPointLink: ConnectionPointLinkType | None = element(ns="csipaus", default=None)


class EndDeviceListResponse(SubscribableList, tag="EndDeviceList"):
    pollRate: int | None = attr(default=DEFAULT_POLLRATE_SECONDS)  # recommended client pollrate in seconds
    EndDevice: list[EndDeviceResponse] | None = element(default=None)


class RegistrationResponse(Resource, tag="Registration"):
    pollRate: int | None = attr(default=DEFAULT_POLLRATE_SECONDS)  # recommended client pollrate in seconds
    dateTimeRegistered: TimeType = element()  # Contains the time at which this registration was created
    pIN: PINType = (
        element()
    )  # Contains the registration PIN number associated with the device, includes checksum digit.
