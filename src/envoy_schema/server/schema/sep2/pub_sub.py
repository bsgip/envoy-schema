from enum import IntEnum
from typing import Optional, Union

from pydantic import root_validator, validator
from pydantic.fields import ModelField
from pydantic_xml import attr, element

from envoy_schema.server.schema.sep2.base import BaseXmlModelWithNS
from envoy_schema.server.schema.sep2.der import DefaultDERControl, DERControlListResponse, DERControlResponse
from envoy_schema.server.schema.sep2.end_device import EndDeviceListResponse, EndDeviceResponse
from envoy_schema.server.schema.sep2.identification import List as Sep2List
from envoy_schema.server.schema.sep2.identification import Resource
from envoy_schema.server.schema.sep2.metering import Reading
from envoy_schema.server.schema.sep2.pricing import TimeTariffIntervalListResponse, TimeTariffIntervalResponse
from envoy_schema.server.schema.sep2.primitive_types import UriFullyQualified, UriWithoutHost


class NotificationStatus(IntEnum):
    """Status values pertaining to Notification.status as described by Notification schema"""

    DEFAULT = 0
    SUBSCRIPTION_CANCELLED_NO_INFO = 1
    SUBSCRIPTION_CANCELLED_RESOURCE_MOVED = 2
    SUBSCRIPTION_CANCELLED_RESOURCE_DEFINITION_CHANGED = 3  # eg - new version of IEEE 2030.5
    SUBSCRIPTION_CANCELLED_RESOURCE_DELETED = 4


class SubscriptionEncoding(IntEnum):
    """Status values pertaining to Subscription.encoding as described by Subscription schema"""

    XML = 0  # application/sep+xml
    EXI = 1  # application/sep-exi


class ConditionAttributeIdentifier(IntEnum):
    """Status values pertaining to Condition.attributeIdentifier as described by Condition schema"""

    READING_VALUE = 0


class SubscriptionBase(Resource):
    """Holds the information related to a client subscription to receive updates to a resource automatically.
    The actual resources may be passed in the Notification by specifying a specific xsi:type for the Resource and
    passing the full representation."""

    subscribedResource: UriWithoutHost = element()  # The resource for which the subscription applies.


# class NotificationResource(Sep2List, DefaultDERControl, Reading):
#     """This is a workaround for pydantic xml - the Resource element in Notification can essentially be ANY type
#     of which many are list types that pydantic struggles to pick the correct type as many of the types are
#     interchangeable once you start considering that many of the elements are optional

#     To workaround this limitation - we've manually merged the relevant types here - practically speaking this will
#     only return a list of a single type as indicated by the xsi:type attribute"""

#     # Only set if type is TimeTariffIntervalList
#     TimeTariffInterval: Optional[list[TimeTariffIntervalResponse]] = element()

#     # Only set if type is DERControlList
#     DERControl: Optional[list[DERControlResponse]] = element()

#     # Only set if type is EndDeviceList
#     EndDevice: Optional[list[EndDeviceResponse]] = element()


class Notification(SubscriptionBase):
    """Holds the information related to a client subscription to receive updates to a resource automatically.
    The actual resources may be passed in the Notification by specifying a specific xsi:type for the Resource and
    passing the full representation."""

    newResourceURI: Optional[UriWithoutHost] = element()  # The new location of the resource if moved.
    status: NotificationStatus = element()
    subscriptionURI: UriWithoutHost = element()  # Subscription from which this notification was triggered.

    # A resource is an addressable unit of information, either a collection (List) or instance of an object
    # (identifiedObject, or simply, Resource)
    #
    # The xsi:type attribute will define how the entity is parsed
    #
    # NOTE - Resource must be the LAST type in the union - pydantic tries left to right looking for the first match
    #
    resource: Optional[
        Union[
            TimeTariffIntervalListResponse,
            DERControlListResponse,
            DefaultDERControl,
            EndDeviceListResponse,
            Reading,
            Resource,
        ]
    ] = element(tag="Resource", union_mode="smart")

    @root_validator(pre=True)
    def prep_resource(cls, values: dict):
        xsi_type: Optional[str] = values.get("type", None)

        if xsi_type == "TimeTariffIntervalList":
            return TimeTariffIntervalListResponse.validate(values)
        elif xsi_type == "DERControlList":
            return DERControlListResponse.validate(values)
        elif xsi_type == "EndDeviceList":
            return EndDeviceListResponse.validate(values)
        elif xsi_type == "Reading":
            return Reading.validate(values)

        # if "TimeTariffInterval" in v:
        #     return TimeTariffIntervalListResponse.validate(v)
        # elif "DERControl" in v:
        #     return DERControlListResponse.validate(v)
        # elif "EndDevice" in v:
        #     return EndDeviceListResponse.validate(v)
        # elif "timePeriod" in v or "value" in v:
        #     return Reading.validate(v)

        return Resource.validate(values)

    # @validator("resource", pre=True)
    # def prepare_resource(cls, v, values: dict, field: ModelField):
    #     xsi_type: Optional[str] = values.get("type", None)

    #     if xsi_type == "TimeTariffIntervalList":
    #         return TimeTariffIntervalListResponse.validate(values)
    #     elif xsi_type == "DERControlList":
    #         return DERControlListResponse.validate(values)
    #     elif xsi_type == "EndDeviceList":
    #         return EndDeviceListResponse.validate(values)
    #     elif xsi_type == "Reading":
    #         return Reading.validate(values)

    #     # if "TimeTariffInterval" in v:
    #     #     return TimeTariffIntervalListResponse.validate(v)
    #     # elif "DERControl" in v:
    #     #     return DERControlListResponse.validate(v)
    #     # elif "EndDevice" in v:
    #     #     return EndDeviceListResponse.validate(v)
    #     # elif "timePeriod" in v or "value" in v:
    #     #     return Reading.validate(v)

    #     return Resource.validate(values)


class Condition(BaseXmlModelWithNS):
    """Indicates a condition that must be satisfied for the Notification to be triggered."""

    attributeIdentifier: ConditionAttributeIdentifier = element()
    lowerThreshold: int = element()  # The value of the lower threshold
    upperThreshold: int = element()  # The value of the upper threshold


class Subscription(SubscriptionBase):
    """Holds the information related to a client subscription to receive updates to a resource automatically."""

    encoding: SubscriptionEncoding = element()  # The resource for which the subscription applies.
    level: str = element()  # Contains the preferred schema and extensibility level indication such as "+S1"
    limit: int = element()  # This element is used to indicate the maximum number of list items that should be included
    # in a notification when the subscribed resource changes
    notificationURI: UriFullyQualified = element()  # The resource to which to post the notifications

    condition: Optional[Condition] = element(tag="Condition")


class SubscriptionListResponse(Sep2List, tag="SubscriptionList"):
    pollRate: Optional[int] = attr()  # The default polling rate for this function set in seconds
    subscriptions: list[Subscription] = element(tag="Subscription", default_factory=list)


class NotificationListResponse(Sep2List, tag="NotificationList"):
    notifications: list[Notification] = element(tag="Notification", default_factory=list)
