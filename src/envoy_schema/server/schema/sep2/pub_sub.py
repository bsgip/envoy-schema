from enum import IntEnum
from typing import Any

from pydantic_xml import attr, element

from envoy_schema.server.schema.sep2.base import BaseXmlModelWithNS
from envoy_schema.server.schema.sep2.der import (
    AbnormalCategoryType,
    ConnectStatusTypeValue,
    DERControlBase,
    DERControlResponse,
    DERProgramResponse,
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
from envoy_schema.server.schema.sep2.function_set_assignments import FunctionSetAssignmentsResponse
from envoy_schema.server.schema.sep2.identification import List as Sep2List
from envoy_schema.server.schema.sep2.identification import Resource
from envoy_schema.server.schema.sep2.metering import Reading
from envoy_schema.server.schema.sep2.pricing import (
    RateComponentResponse,
    TariffProfileResponse,
    TimeTariffIntervalResponse,
)
from envoy_schema.server.schema.sep2.primitive_types import (
    AbsoluteUri,
    HexBinary8,
    HexBinary32,
    HexBinary128,
    HttpUri,
    LocalAbsoluteUri,
)
from envoy_schema.server.schema.sep2.types import PerCent, SubscribableType, TimeType, VersionType

XSI_TYPE_TIME_TARIFF_INTERVAL_LIST = "TimeTariffIntervalList"
XSI_TYPE_DER_CONTROL_LIST = "DERControlList"
XSI_TYPE_DER_AVAILABILITY = "DERAvailability"
XSI_TYPE_DER_CAPABILITY = "DERCapability"
XSI_TYPE_DER_SETTINGS = "DERSettings"
XSI_TYPE_DER_STATUS = "DERStatus"
XSI_TYPE_DER_PROGRAM_LIST = "DERProgramList"
XSI_TYPE_FUNCTION_SET_ASSIGNMENTS_LIST = "FunctionSetAssignmentsList"
XSI_TYPE_DEFAULT_DER_CONTROL = "DefaultDERControl"
XSI_TYPE_END_DEVICE_LIST = "EndDeviceList"
XSI_TYPE_READING_LIST = "ReadingList"
XSI_TYPE_RESOURCE = "Resource"
XSI_TYPE_RATE_COMPONENT_LIST = "RateComponentList"
XSI_TYPE_TARIFF_PROFILE_LIST = "TariffProfileList"
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


def get_notification_resource_discriminator(v: Any) -> str:  # noqa: ANN401
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
        TimeTariffIntervalListResponse, DERControlListResponse, DefaultDERControl, EndDeviceListResponse, Reading,
        TariffProfileListResponse, RateComponentListResponse

    The plan is for the server to only fill out the fields relevant for the notification being served (based on
    the xsi:type attribute). Clients using this to parse Notifications will have to manually map the fields to
    the appropriate types.

    HERE BE DRAGONS FOR XSD VALIDITY:
        In order to keep XSD element ordering, we've had to do a few "creative" element orderings to ensure that
        generated notifications have elements in the XSD valid order. Because a couple of element names are shared
        between the combined resource types (eg setESDelay on DefaultDERControl / DERSettings) - We've had to define
        things in a confusing order - There isn't another way around this. See highlighted items marked with SORRY.
    """

    subscribable: SubscribableType | None = attr(default=None)

    # List
    pollRate: int | None = attr(default=None)
    all_: int | None = attr(name="all", default=None)
    results: int | None = attr(default=None)

    # TimeTariffIntervalListResponse
    TimeTariffInterval: list[TimeTariffIntervalResponse] | None = element(default=None)

    # DERControlListResponse
    DERControl: list[DERControlResponse] | None = element(default=None)

    # EndDeviceListResponse
    EndDevice: list[EndDeviceResponse] | None = element(default=None)

    # ReadingListResponse
    Readings: list[Reading] | None = element(default=None, tag="Reading")

    # DERProgramListResponse
    DERProgram: list[DERProgramResponse] | None = element(default=None)

    # FunctionSetAssignmentsListResponse
    FunctionSetAssignments: list[FunctionSetAssignmentsResponse] | None = element(default=None)

    # TariffProfileListResponse
    TariffProfile: list[TariffProfileResponse] | None = element(default=None)

    # RateComponentListResponse
    RateComponent: list[RateComponentResponse] | None = element(default=None)

    # SubscribableIdentifiedObject
    mRID: HexBinary128 | None = element(default=None)
    description: str | None = element(default=None)
    version: VersionType | None = element(default=None)

    # SORRY (see docstring): DERSettings:  but because of the shared elements with DefaultDERControl, this must
    # appear above DefaultDERControl
    modesEnabled: HexBinary32 | None = element(default=None)  # SORRY

    # DefaultDERControl
    DERControlBase_: DERControlBase | None = element(tag="DERControlBase", default=None)
    setESDelay: int | None = element(default=None)
    setESHighFreq: int | None = element(default=None)
    setESHighVolt: int | None = element(default=None)
    setESLowFreq: int | None = element(default=None)
    setESLowVolt: int | None = element(default=None)
    setESRampTms: int | None = element(default=None)
    setESRandomDelay: int | None = element(default=None)
    setGradW: int | None = element(default=None)
    # setSoftGradW: Optional[int] = element(default=None) # Duplicated from DERSettings

    # SORRY (see docstring): DERAvailability but unfortunately DERAvailability/DERStatus: both share readingTime, these
    # need to be brought up there to ensure they work if either resource type is populated
    availabilityDuration: int | None = element(default=None)  # SORRY
    maxChargeDuration: int | None = element(default=None)  # SORRY

    # DERStatus
    alarmStatus: HexBinary32 | None = element(default=None)
    genConnectStatus: ConnectStatusTypeValue | None = element(default=None, tag="genConnectStatus")
    inverterStatus: InverterStatusTypeValue | None = element(default=None, tag="inverterStatus")
    localControlModeStatus: LocalControlModeStatusTypeValue | None = element(default=None, tag="localControlModeStatus")
    manufacturerStatus: ManufacturerStatusValue | None = element(default=None, tag="manufacturerStatus")
    operationalModeStatus: OperationalModeStatusTypeValue | None = element(default=None, tag="operationalModeStatus")
    readingTime: TimeType | None = element(default=None)
    stateOfChargeStatus: StateOfChargeStatusValue | None = element(default=None, tag="stateOfChargeStatus")
    storageModeStatus: StorageModeStatusTypeValue | None = element(default=None, tag="storageModeStatus")
    storConnectStatus: ConnectStatusTypeValue | None = element(default=None, tag="storConnectStatus")

    # DERAvailability
    # readingTime: TimeType = element()  # Duplicated from DERStatus
    reserveChargePercent: PerCent | None = element(default=None)
    reservePercent: PerCent | None = element(default=None)
    statVarAvail: ReactivePower | None = element(default=None)
    statWAvail: ActivePower | None = element(default=None)

    # DERCapability
    modesSupported: HexBinary32 | None = element(default=None)
    rtgAbnormalCategory: AbnormalCategoryType | None = element(default=None)
    rtgMaxA: CurrentRMS | None = element(default=None)
    rtgMaxAh: AmpereHour | None = element(default=None)
    rtgMaxChargeRateVA: ApparentPower | None = element(default=None)
    rtgMaxChargeRateW: ActivePower | None = element(default=None)
    rtgMaxDischargeRateVA: ApparentPower | None = element(default=None)
    rtgMaxDischargeRateW: ActivePower | None = element(default=None)
    rtgMaxV: VoltageRMS | None = element(default=None)
    rtgMaxVA: ApparentPower | None = element(default=None)
    rtgMaxVar: ReactivePower | None = element(default=None)
    rtgMaxVarNeg: ReactivePower | None = element(default=None)
    rtgMaxW: ActivePower | None = element(default=None)
    rtgMaxWh: WattHour | None = element(default=None)
    rtgMinPFOverExcited: PowerFactor | None = element(default=None)
    rtgMinPFUnderExcited: PowerFactor | None = element(default=None)
    rtgMinV: VoltageRMS | None = element(default=None)
    rtgNormalCategory: NormalCategoryType | None = element(default=None)
    rtgOverExcitedPF: PowerFactor | None = element(default=None)
    rtgOverExcitedW: ActivePower | None = element(default=None)
    rtgReactiveSusceptance: ReactiveSusceptance | None = element(default=None)
    rtgUnderExcitedPF: PowerFactor | None = element(default=None)
    rtgUnderExcitedW: ActivePower | None = element(default=None)
    rtgVNom: VoltageRMS | None = element(default=None)
    type_: DERType | None = element(tag="type", default=None)
    doeModesSupported: HexBinary8 | None = element(ns="csipaus", default=None)
    vppModesSupported: HexBinary8 | None = element(ns="csipaus", default=None)

    # DERSettings
    # setESDelay: Optional[int] = element(default=None)  # Duplicated from DERControl
    # setESHighFreq: Optional[int] = element(default=None) # Duplicated from DERControl
    # setESHighVolt: Optional[int] = element(default=None) # Duplicated from DERControl
    # setESLowFreq: Optional[int] = element(default=None) # Duplicated from DERControl
    # setESLowVolt: Optional[int] = element(default=None) # Duplicated from DERControl
    # setESRampTms: Optional[int] = element(default=None) # Duplicated from DERControl
    # setESRandomDelay: Optional[int] = element(default=None) # Duplicated from DERControl
    # setGradW: int = element() # Duplicated from DERControl
    setMaxA: CurrentRMS | None = element(default=None)
    setMaxAh: AmpereHour | None = element(default=None)
    setMaxChargeRateVA: ApparentPower | None = element(default=None)
    setMaxChargeRateW: ActivePower | None = element(default=None)
    setMaxDischargeRateVA: ApparentPower | None = element(default=None)
    setMaxDischargeRateW: ActivePower | None = element(default=None)
    setMaxV: VoltageRMS | None = element(default=None)
    setMaxVA: ApparentPower | None = element(default=None)
    setMaxVar: ReactivePower | None = element(default=None)
    setMaxVarNeg: ReactivePower | None = element(default=None)
    setMaxW: ActivePower | None = element(default=None)
    setMaxWh: WattHour | None = element(default=None)
    setMinPFOverExcited: PowerFactor | None = element(default=None)
    setMinPFUnderExcited: PowerFactor | None = element(default=None)
    setMinV: VoltageRMS | None = element(default=None)
    setSoftGradW: int | None = element(default=None)
    setVNom: VoltageRMS | None = element(default=None)
    setVRef: VoltageRMS | None = element(default=None)
    setVRefOfs: VoltageRMS | None = element(default=None)
    updatedTime: TimeType | None = element(default=None)
    doeModesEnabled: HexBinary8 | None = element(ns="csipaus", default=None)
    vppModesEnabled: HexBinary8 | None = element(ns="csipaus", default=None)
    setMinWh: WattHour | None = element(ns="csipaus", default=None)


class Notification(SubscriptionBase):
    """Holds the information related to a client subscription to receive updates to a resource automatically.
    The actual resources may be passed in the Notification by specifying a specific xsi:type for the Resource and
    passing the full representation."""

    newResourceURI: LocalAbsoluteUri | None = element(default=None)  # The new location of the resource if moved.

    # A resource is an addressable unit of information, either a collection (List) or instance of an object
    # (identifiedObject, or simply, Resource)
    #
    # The xsi:type attribute will define how the entity is parsed
    #
    # NOTE - Resource must define an xsi:type attribute otherwise it will parse to Resource - logic is handled
    #      - in the pydantic Discriminator function get_notification_resource_discriminator
    #
    # NOTE - For more info - see pydantic docs on Unions / Discriminated Unions - Feature introduced in 2.5
    resource: NotificationResourceCombined | None = element(tag="Resource", default=None)
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
    # Instead we use this as our workaround for now

    status: NotificationStatus = element()
    subscriptionURI: AbsoluteUri = element()  # Subscription from which this notification was triggered.


class Condition(BaseXmlModelWithNS):
    """Indicates a condition that must be satisfied for the Notification to be triggered."""

    attributeIdentifier: ConditionAttributeIdentifier = element()
    lowerThreshold: int = element(default=None)  # The value of the lower threshold
    upperThreshold: int = element(default=None)  # The value of the upper threshold


class Subscription(SubscriptionBase):
    """Holds the information related to a client subscription to receive updates to a resource automatically."""

    condition: Condition | None = element(tag="Condition", default=None)
    encoding: SubscriptionEncoding = element()  # The resource for which the subscription applies.
    level: str = element()  # Contains the preferred schema and extensibility level indication such as "+S1"
    limit: int = element()  # This element is used to indicate the maximum number of list items that should be included
    # in a notification when the subscribed resource changes
    notificationURI: HttpUri = element()  # The resource to which to post the notifications


class SubscriptionListResponse(Sep2List, tag="SubscriptionList"):
    subscriptions: list[Subscription] | None = element(tag="Subscription", default=None)
    pollRate: int | None = attr(default=None)  # The default polling rate for this function set in seconds


class NotificationListResponse(Sep2List, tag="NotificationList"):
    notifications: list[Notification] | None = element(tag="Notification", default=None)
