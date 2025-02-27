from typing import Optional

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

    ConfigurationLink: Optional[Link] = element(default=None)
    DERListLink: Optional[ListLink] = element(default=None)
    deviceCategory: Optional[primitive_types.HexBinary32] = element(default=None)
    DeviceInformationLink: Optional[Link] = element(default=None)
    DeviceStatusLink: Optional[Link] = element(default=None)
    FileStatusLink: Optional[Link] = element(default=None)
    IPInterfaceListLink: Optional[Link] = element(default=None)
    lFDI: Optional[str] = element(default=None)
    LoadShedAvailabilityListLink: Optional[ListLink] = element(default=None)
    LogEventListLink: Optional[Link] = element(default=None)
    PowerStatusLink: Optional[Link] = element(default=None)
    sFDI: int = element()


class EndDeviceRequest(AbstractDevice, tag="EndDevice"):
    postRate: Optional[int] = element(default=None)


class EndDeviceResponse(AbstractDevice, tag="EndDevice"):
    changedTime: TimeType = element()
    enabled: Optional[bool] = element(default=True)

    FlowReservationRequestListLink: Optional[Link] = element(default=None)
    FlowReservationResponseListLink: Optional[Link] = element(default=None)
    FunctionSetAssignmentsListLink: Optional[ListLink] = element(default=None)
    postRate: Optional[int] = element(default=None)
    RegistrationLink: Optional[Link] = element(default=None)
    SubscriptionListLink: Optional[ListLink] = element(default=None)

    # csip extension
    ConnectionPointLink: Optional[ConnectionPointLinkType] = element(ns="csipaus", default=None)


class EndDeviceListResponse(SubscribableList, tag="EndDeviceList"):
    EndDevice: Optional[list[EndDeviceResponse]] = element(default=None)


class RegistrationResponse(Resource, tag="Registration"):
    pollRate: Optional[int] = attr(default=DEFAULT_POLLRATE_SECONDS)  # recommended client pollrate in seconds
    dateTimeRegistered: TimeType = element()  # Contains the time at which this registration was created
    pIN: PINType = (
        element()
    )  # Contains the registration PIN number associated with the device, includes checksum digit.
