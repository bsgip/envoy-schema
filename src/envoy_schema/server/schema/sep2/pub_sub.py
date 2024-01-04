from enum import IntEnum
from typing import Optional, Union

from pydantic_xml import attr, element

from envoy_schema.server.schema.sep2.base import BaseXmlModelWithNS
from envoy_schema.server.schema.sep2.der import DefaultDERControl, DERControlListResponse
from envoy_schema.server.schema.sep2.end_device import EndDeviceListResponse
from envoy_schema.server.schema.sep2.identification import List as Sep2List
from envoy_schema.server.schema.sep2.identification import Resource
from envoy_schema.server.schema.sep2.metering import Reading
from envoy_schema.server.schema.sep2.pricing import TimeTariffIntervalListResponse
from envoy_schema.server.schema.sep2.primitive_types import HttpUri, LocalAbsoluteUri


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

    subscribedResource: LocalAbsoluteUri = element()  # The resource for which the subscription applies.


class Notification(SubscriptionBase):
    """Holds the information related to a client subscription to receive updates to a resource automatically.
    The actual resources may be passed in the Notification by specifying a specific xsi:type for the Resource and
    passing the full representation."""

    newResourceURI: Optional[LocalAbsoluteUri] = element(default=None)  # The new location of the resource if moved.
    status: NotificationStatus = element()
    subscriptionURI: LocalAbsoluteUri = element()  # Subscription from which this notification was triggered.

    # A resource is an addressable unit of information, either a collection (List) or instance of an object
    # (identifiedObject, or simply, Resource)
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
    ] = element(tag="Resource", default=None)


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
    notificationURI: HttpUri = element()  # The resource to which to post the notifications

    condition: Optional[Condition] = element(tag="Condition", default=None)


class SubscriptionListResponse(Sep2List, tag="SubscriptionList"):
    pollRate: Optional[int] = attr(default=None)  # The default polling rate for this function set in seconds
    subscriptions: list[Subscription] = element(tag="Subscription")


class NotificationListResponse(Sep2List, tag="NotificationList"):
    notifications: list[Notification] = element(tag="Notification")
