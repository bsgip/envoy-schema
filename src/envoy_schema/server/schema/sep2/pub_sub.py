from enum import IntEnum
from typing import Any, Optional

from pydantic import root_validator, validator
from pydantic.fields import ModelField
from pydantic_xml import attr, element

from envoy_schema.server.schema.sep2.base import BaseXmlModelWithNS
from envoy_schema.server.schema.sep2.der import DERControlBase, DERControlResponse
from envoy_schema.server.schema.sep2.end_device import EndDeviceResponse
from envoy_schema.server.schema.sep2.identification import List as Sep2List
from envoy_schema.server.schema.sep2.identification import Resource
from envoy_schema.server.schema.sep2.pricing import TimeTariffIntervalResponse
from envoy_schema.server.schema.sep2.primitive_types import HexBinary16, HttpUri, LocalAbsoluteUri
from envoy_schema.server.schema.sep2.types import (
    ConsumptionBlockType,
    DateTimeIntervalType,
    SubscribableType,
    TOUType,
    VersionType,
    mRIDType,
)

XSI_TYPE_TIME_TARIFF_INTERVAL_LIST = "TimeTariffIntervalList"
XSI_TYPE_DER_CONTROL_LIST = "DERControlList"
XSI_TYPE_DEFAULT_DER_CONTROL = "DefaultDERControl"
XSI_TYPE_END_DEVICE_LIST = "EndDeviceList"
XSI_TYPE_READING = "Reading"
XSI_TYPE_RESOURCE = "Resource"
XSI_TYPE_DEFAULT = XSI_TYPE_RESOURCE


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
    # The xsi:type attribute will define how the entity is parsed
    #
    # NOTE - Resource must define an xsi:type attribute otherwise it will parse to Resource - logic is handled
    #      - in the pydantic Discriminator function get_notification_resource_discriminator
    #
    # NOTE - For more info - see pydantic docs on Unions / Discriminated Unions - Feature introduced in 2.5
    resource: Optional[
        # This callable discriminator union isn't supported by pydantic XML
        # see: https://github.com/dapper91/pydantic-xml/issues/157 - we might be able to swap to this in the future
        # Annotated[
        #     Union[
        #         Annotated[TimeTariffIntervalListResponse, Tag(XSI_TYPE_TIME_TARIFF_INTERVAL_LIST)],
        #         Annotated[DERControlListResponse, Tag(XSI_TYPE_DER_CONTROL_LIST)],
        #         Annotated[DefaultDERControl, Tag(XSI_TYPE_DEFAULT_DER_CONTROL)],
        #         Annotated[EndDeviceListResponse, Tag(XSI_TYPE_END_DEVICE_LIST)],
        #         Annotated[Reading, Tag(XSI_TYPE_READING)],
        #         Annotated[Resource, Tag(XSI_TYPE_RESOURCE)],
        #     ],
        #     Discriminator(get_notification_resource_discriminator),
        # ]
        NotificationResourceCombined  # Instead we use this as our workaround for now
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
    notifications: list[Notification] = element(tag="Notification", default_factory=list)
