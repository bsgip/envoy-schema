from typing import Optional

from pydantic_xml import element

from envoy_schema.server.schema.sep2.event import RandomizableEvent
from envoy_schema.server.schema.sep2.identification import IdentifiedObject, Link
from envoy_schema.server.schema.sep2.identification import List as SepList
from envoy_schema.server.schema.sep2.identification import ListLink, Resource, SubscribableList
from envoy_schema.server.schema.sep2.types import (
    ConsumptionBlockType,
    CurrencyCode,
    PrimacyType,
    ServiceKind,
    TOUType,
    UnitValueType,
)
from envoy_schema.server.schema.sep2.primitive_types import HexBinary16


class TariffProfileResponse(IdentifiedObject, tag="TariffProfile"):
    """A schedule of charges; structure that allows the definition of tariff structures such as step (block) and
    time of use (tier) when used in conjunction with TimeTariffInterval and ConsumptionTariffInterval."""

    currency: Optional[CurrencyCode] = element(default=None)
    pricePowerOfTenMultiplier: Optional[int] = element(default=None)
    primacyType: PrimacyType = element(default=None, tag="primacy")
    rateCode: Optional[str] = element(default=None)
    RateComponentListLink: Optional[ListLink] = element(default=None)
    serviceCategoryKind: ServiceKind = element()


class RateComponentResponse(IdentifiedObject, tag="RateComponent"):
    """Specifies the applicable charges for a single component of the rate, which could be generation price or
    consumption price, for example."""

    ActiveTimeTariffIntervalListLink: Optional[ListLink] = element(default=None)
    flowRateEndLimit: Optional[UnitValueType] = element(default=None)
    flowRateStartLimit: Optional[UnitValueType] = element(default=None)
    ReadingTypeLink: Link = element()
    roleFlags: HexBinary16 = element()  # See RoleFlagsType

    TimeTariffIntervalListLink: ListLink = element()


class TimeTariffIntervalResponse(RandomizableEvent, tag="TimeTariffInterval"):
    """Describes the time-differentiated portion of the RateComponent, if applicable, and provides the ability to
    specify multiple time intervals, each with its own consumption-based components and other attributes."""

    ConsumptionTariffIntervalListLink: ListLink = element()
    touTier: TOUType = element()


class ConsumptionTariffIntervalResponse(Resource, tag="ConsumptionTariffInterval"):
    """One of a sequence of thresholds defined in terms of consumption quantity of a service such as electricity,
    water, gas, etc. It defines the steps or blocks in a step tariff structure, where startValue simultaneously
    defines the entry value of this step and the closing value of the previous step. Where consumption is greater
    than startValue, it falls within this block and where consumption is less than or equal to startValue, it falls
    within one of the previous blocks."""

    consumptionBlock: ConsumptionBlockType = element()
    price: Optional[int] = element(
        default=None
    )  # The charge for this rate component, per unit of measure defined by the
    # associated ReadingType, in currency specified in TariffProfile.  # noqa e114
    startValue: int = element()  # The lowest level of consumption that defines the starting point of this consumption
    # step or block. Thresholds start at zero for each billing period. # noqa e114


class TariffProfileListResponse(SepList, tag="TariffProfileList"):
    TariffProfile: Optional[list[TariffProfileResponse]] = element(default=None)


class RateComponentListResponse(SubscribableList, tag="RateComponentList"):
    """Worth noting that the standard describes RateComponentList as a standard list but it's an envoy
    specific extension to support subscriptions via SubscribableList"""

    RateComponent: Optional[list[RateComponentResponse]] = element(default=None)


class TimeTariffIntervalListResponse(SepList, tag="TimeTariffIntervalList"):
    TimeTariffInterval: Optional[list[TimeTariffIntervalResponse]] = element(default=None)


class ConsumptionTariffIntervalListResponse(SepList, tag="ConsumptionTariffIntervalList"):
    ConsumptionTariffInterval: Optional[list[ConsumptionTariffIntervalResponse]] = element(default=None)
