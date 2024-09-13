from enum import IntEnum
from typing import Any, Optional

from pydantic_xml import attr, element

from envoy_schema.server.schema.sep2.base import BaseXmlModelWithNS
from envoy_schema.server.schema.sep2.der import (
    AbnormalCategoryType,
    ConnectStatusTypeValue,
    DERControlBase,
    DERControlResponse,
    DERType,
    InverterStatusTypeValue,
    LocalControlModeStatusTypeValue,
    ManufacturerStatusValue,
    NormalCategoryType,
    OperationalModeStatusTypeValue,
    StateOfChargeStatusValue,
    StorageModeStatusTypeValue,
)
from envoy_schema.server.schema.sep2.der_control_types import (
    ActivePower,
    AmpereHour,
    ApparentPower,
    CurrentRMS,
    PowerFactor,
    ReactivePower,
    ReactiveSusceptance,
    VoltageRMS,
    WattHour,
)
from envoy_schema.server.schema.sep2.end_device import EndDeviceResponse
from envoy_schema.server.schema.sep2.identification import List as Sep2List
from envoy_schema.server.schema.sep2.identification import Resource
from envoy_schema.server.schema.sep2.metering import Reading
from envoy_schema.server.schema.sep2.pricing import TimeTariffIntervalResponse
from envoy_schema.server.schema.sep2.primitive_types import (
    HexBinary8,
    HexBinary32,
    HttpUri,
    LocalAbsoluteUri,
    HexBinary128,
)
from envoy_schema.server.schema.sep2.types import PerCent, SubscribableType, TimeType, VersionType

XSI_TYPE_TIME_TARIFF_INTERVAL_LIST = "TimeTariffIntervalList"
XSI_TYPE_DER_CONTROL_LIST = "DERControlList"
XSI_TYPE_DER_AVAILABILITY = "DERAvailability"
XSI_TYPE_DER_CAPABILITY = "DERCapability"
XSI_TYPE_DER_SETTINGS = "DERSettings"
XSI_TYPE_DER_STATUS = "DERStatus"
XSI_TYPE_DEFAULT_DER_CONTROL = "DefaultDERControl"
XSI_TYPE_END_DEVICE_LIST = "EndDeviceList"
XSI_TYPE_READING_LIST = "ReadingList"
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


def get_notification_resource_discriminator(v: Any) -> str:
    if not v:
        return XSI_TYPE_DEFAULT

    if isinstance(v, dict):
        return v.get("type", XSI_TYPE_DEFAULT)
    return getattr(v, "type", XSI_TYPE_DEFAULT)


class NotificationResourceCombined(Resource):
    """This class only exists because pydantic-xml has limited support for pydantic discriminated unions

    Ultimately we have a single element in notification called <Resource> that can be filled with any number
    of types - the pydantic xml typing struggles to represent this via discriminators.

    One major limitation: https://github.com/dapper91/pydantic-xml/issues/157
    Pydantic XML also only support discriminating between sub models with the exact same attributes

    This class essentially combines (manually) the following classes:
        TimeTariffIntervalListResponse, DERControlListResponse, DefaultDERControl, EndDeviceListResponse, Reading

    The plan is for the server to only fill out the fields relevant for the notification being served (based on
    the xsi:type attribute). Clients using this to parse Notifications will have to manually map the fields to
    the appropriate types.

    HERE BE DRAGONS FOR XSD VALIDITY:
        In order to keep XSD element ordering, we've had to do a few "creative" element orderings to ensure that
        generated notifications have elements in the XSD valid order. Because a couple of element names are shared
        between the combined resource types (eg setESDelay on DefaultDERControl / DERSettings) - We've had to define
        things in a confusing order - There isn't another way around this. See highlighted items marked with SORRY.
    """

    subscribable: Optional[SubscribableType] = attr(default=None)

    # List
    all_: Optional[int] = attr(name="all", default=None)
    results: Optional[int] = attr(default=None)

    # TimeTariffIntervalListResponse
    TimeTariffInterval: Optional[list[TimeTariffIntervalResponse]] = element(default=None)

    # DERControlListResponse
    DERControl: Optional[list[DERControlResponse]] = element(default=None)

    # EndDeviceListResponse
    EndDevice: Optional[list[EndDeviceResponse]] = element(default=None)

    # ReadingListResponse
    Readings: Optional[list[Reading]] = element(default=None, tag="Reading")

    # SubscribableIdentifiedObject
    mRID: Optional[HexBinary128] = element(default=None)
    description: Optional[str] = element(default=None)
    version: Optional[VersionType] = element(default=None)

    # SORRY (see docstring): DERSettings:  but because of the shared elements with DefaultDERControl, this must
    # appear above DefaultDERControl
    modesEnabled: Optional[HexBinary32] = element(default=None)  # SORRY

    # DefaultDERControl
    DERControlBase_: Optional[DERControlBase] = element(tag="DERControlBase", default=None)
    setESDelay: Optional[int] = element(default=None)
    setESHighFreq: Optional[int] = element(default=None)
    setESHighVolt: Optional[int] = element(default=None)
    setESLowFreq: Optional[int] = element(default=None)
    setESLowVolt: Optional[int] = element(default=None)
    setESRampTms: Optional[int] = element(default=None)
    setESRandomDelay: Optional[int] = element(default=None)
    setGradW: Optional[int] = element(default=None)
    # setSoftGradW: Optional[int] = element(default=None) # Duplicated from DERSettings

    # SORRY (see docstring): DERAvailability but unfortunately DERAvailability/DERStatus: both share readingTime, these
    # need to be brought up there to ensure they work if either resource type is populated
    availabilityDuration: Optional[int] = element(default=None)  # SORRY
    maxChargeDuration: Optional[int] = element(default=None)  # SORRY

    # DERStatus
    alarmStatus: Optional[HexBinary32] = element(default=None)
    genConnectStatus: Optional[ConnectStatusTypeValue] = element(default=None, tag="genConnectStatus")
    inverterStatus: Optional[InverterStatusTypeValue] = element(default=None, tag="inverterStatus")
    localControlModeStatus: Optional[LocalControlModeStatusTypeValue] = element(
        default=None, tag="localControlModeStatus"
    )
    manufacturerStatus: Optional[ManufacturerStatusValue] = element(default=None, tag="manufacturerStatus")
    operationalModeStatus: Optional[OperationalModeStatusTypeValue] = element(default=None, tag="operationalModeStatus")
    readingTime: Optional[TimeType] = element(default=None)
    stateOfChargeStatus: Optional[StateOfChargeStatusValue] = element(default=None, tag="stateOfChargeStatus")
    storageModeStatus: Optional[StorageModeStatusTypeValue] = element(default=None, tag="storageModeStatus")
    storConnectStatus: Optional[ConnectStatusTypeValue] = element(default=None, tag="storConnectStatus")

    # DERAvailability
    # readingTime: TimeType = element()  # Duplicated from DERStatus
    reserveChargePercent: Optional[PerCent] = element(default=None)
    reservePercent: Optional[PerCent] = element(default=None)
    statVarAvail: Optional[ReactivePower] = element(default=None)
    statWAvail: Optional[ActivePower] = element(default=None)

    # DERCapability
    modesSupported: Optional[HexBinary32] = element(default=None)
    rtgAbnormalCategory: Optional[AbnormalCategoryType] = element(default=None)
    rtgMaxA: Optional[CurrentRMS] = element(default=None)
    rtgMaxAh: Optional[AmpereHour] = element(default=None)
    rtgMaxChargeRateVA: Optional[ApparentPower] = element(default=None)
    rtgMaxChargeRateW: Optional[ActivePower] = element(default=None)
    rtgMaxDischargeRateVA: Optional[ApparentPower] = element(default=None)
    rtgMaxDischargeRateW: Optional[ActivePower] = element(default=None)
    rtgMaxV: Optional[VoltageRMS] = element(default=None)
    rtgMaxVA: Optional[ApparentPower] = element(default=None)
    rtgMaxVar: Optional[ReactivePower] = element(default=None)
    rtgMaxVarNeg: Optional[ReactivePower] = element(default=None)
    rtgMaxW: Optional[ActivePower] = element(default=None)
    rtgMaxWh: Optional[WattHour] = element(default=None)
    rtgMinPFOverExcited: Optional[PowerFactor] = element(default=None)
    rtgMinPFUnderExcited: Optional[PowerFactor] = element(default=None)
    rtgMinV: Optional[VoltageRMS] = element(default=None)
    rtgNormalCategory: Optional[NormalCategoryType] = element(default=None)
    rtgOverExcitedPF: Optional[PowerFactor] = element(default=None)
    rtgOverExcitedW: Optional[ActivePower] = element(default=None)
    rtgReactiveSusceptance: Optional[ReactiveSusceptance] = element(default=None)
    rtgUnderExcitedPF: Optional[PowerFactor] = element(default=None)
    rtgUnderExcitedW: Optional[ActivePower] = element(default=None)
    rtgVNom: Optional[VoltageRMS] = element(default=None)
    type_: Optional[DERType] = element(tag="type", default=None)
    doeModesSupported: Optional[HexBinary8] = element(ns="csipaus", default=None)

    # DERSettings
    # setESDelay: Optional[int] = element(default=None)  # Duplicated from DERControl
    # setESHighFreq: Optional[int] = element(default=None) # Duplicated from DERControl
    # setESHighVolt: Optional[int] = element(default=None) # Duplicated from DERControl
    # setESLowFreq: Optional[int] = element(default=None) # Duplicated from DERControl
    # setESLowVolt: Optional[int] = element(default=None) # Duplicated from DERControl
    # setESRampTms: Optional[int] = element(default=None) # Duplicated from DERControl
    # setESRandomDelay: Optional[int] = element(default=None) # Duplicated from DERControl
    # setGradW: int = element() # Duplicated from DERControl
    setMaxA: Optional[CurrentRMS] = element(default=None)
    setMaxAh: Optional[AmpereHour] = element(default=None)
    setMaxChargeRateVA: Optional[ApparentPower] = element(default=None)
    setMaxChargeRateW: Optional[ActivePower] = element(default=None)
    setMaxDischargeRateVA: Optional[ApparentPower] = element(default=None)
    setMaxDischargeRateW: Optional[ActivePower] = element(default=None)
    setMaxV: Optional[VoltageRMS] = element(default=None)
    setMaxVar: Optional[ReactivePower] = element(default=None)
    setMaxVarNeg: Optional[ReactivePower] = element(default=None)
    setMaxW: Optional[ActivePower] = element(default=None)
    setMaxWh: Optional[WattHour] = element(default=None)
    setMinPFOverExcited: Optional[PowerFactor] = element(default=None)
    setMinPFUnderExcited: Optional[PowerFactor] = element(default=None)
    setMinV: Optional[VoltageRMS] = element(default=None)
    setSoftGradW: Optional[int] = element(default=None)
    setVNom: Optional[VoltageRMS] = element(default=None)
    setVRef: Optional[VoltageRMS] = element(default=None)
    setVRefOfs: Optional[VoltageRMS] = element(default=None)
    updatedTime: Optional[TimeType] = element(default=None)
    doeModesEnabled: Optional[HexBinary8] = element(ns="csipaus", default=None)


class Notification(SubscriptionBase):
    """Holds the information related to a client subscription to receive updates to a resource automatically.
    The actual resources may be passed in the Notification by specifying a specific xsi:type for the Resource and
    passing the full representation."""

    newResourceURI: Optional[LocalAbsoluteUri] = element(default=None)  # The new location of the resource if moved.

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
        #         Annotated[ReadingListResponse, Tag(XSI_TYPE_READING)],
        #         Annotated[Resource, Tag(XSI_TYPE_RESOURCE)],
        #     ],
        #     Discriminator(get_notification_resource_discriminator),
        # ]
        NotificationResourceCombined  # Instead we use this as our workaround for now
    ] = element(tag="Resource", default=None)
    status: NotificationStatus = element()
    subscriptionURI: LocalAbsoluteUri = element()  # Subscription from which this notification was triggered.


class Condition(BaseXmlModelWithNS):
    """Indicates a condition that must be satisfied for the Notification to be triggered."""

    attributeIdentifier: ConditionAttributeIdentifier = element()
    lowerThreshold: int = element(default=None)  # The value of the lower threshold
    upperThreshold: int = element(default=None)  # The value of the upper threshold


class Subscription(SubscriptionBase):
    """Holds the information related to a client subscription to receive updates to a resource automatically."""

    condition: Optional[Condition] = element(tag="Condition", default=None)
    encoding: SubscriptionEncoding = element()  # The resource for which the subscription applies.
    level: str = element()  # Contains the preferred schema and extensibility level indication such as "+S1"
    limit: int = element()  # This element is used to indicate the maximum number of list items that should be included
    # in a notification when the subscribed resource changes
    notificationURI: HttpUri = element()  # The resource to which to post the notifications


class SubscriptionListResponse(Sep2List, tag="SubscriptionList"):
    subscriptions: Optional[list[Subscription]] = element(tag="Subscription", default=None)
    pollRate: Optional[int] = attr(default=None)  # The default polling rate for this function set in seconds


class NotificationListResponse(Sep2List, tag="NotificationList"):
    notifications: Optional[list[Notification]] = element(tag="Notification", default=None)
