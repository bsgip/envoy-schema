from pydantic_xml import attr, element

from envoy_schema.server.schema.sep2.event import RandomizableEvent
from envoy_schema.server.schema.sep2.identification import IdentifiedObject, Link, ListLink, Resource, SubscribableList
from envoy_schema.server.schema.sep2.identification import List as SepList
from envoy_schema.server.schema.sep2.primitive_types import HexBinary16
from envoy_schema.server.schema.sep2.types import (
    DEFAULT_POLLRATE_SECONDS,
    ConsumptionBlockType,
    CurrencyCode,
    ServiceKind,
    TOUType,
    UnitValueType,
)


class TariffProfileResponse(IdentifiedObject, tag="TariffProfile"):
    """A schedule of charges; structure that allows the definition of tariff structures such as step (block) and
    time of use (tier) when used in conjunction with TimeTariffInterval and ConsumptionTariffInterval."""

    currency: CurrencyCode | None = element(default=None)
    pricePowerOfTenMultiplier: int | None = element(default=None)
    primacyType: int = element(
        default=None, tag="primacy"
    )  # Should map to sep2.types.PrimacyType - left as integer to allow deployments with broader values
    rateCode: str | None = element(default=None)
    RateComponentListLink: ListLink | None = element(default=None)
    serviceCategoryKind: ServiceKind = element()
    CombinedTimeTariffIntervalListLink: ListLink = element(ns="csipaus")  # csipaus extension


class RateComponentResponse(IdentifiedObject, tag="RateComponent"):
    """Specifies the applicable charges for a single component of the rate, which could be generation price or
    consumption price, for example."""

    ActiveTimeTariffIntervalListLink: ListLink | None = element(default=None)
    flowRateEndLimit: UnitValueType | None = element(default=None)
    flowRateStartLimit: UnitValueType | None = element(default=None)
    ReadingTypeLink: Link = element()
    roleFlags: HexBinary16 = element()  # See RoleFlagsType

    TimeTariffIntervalListLink: ListLink = element()


class ConsumptionTariffIntervalResponse(Resource, tag="ConsumptionTariffInterval"):
    """One of a sequence of thresholds defined in terms of consumption quantity of a service such as electricity,
    water, gas, etc. It defines the steps or blocks in a step tariff structure, where startValue simultaneously
    defines the entry value of this step and the closing value of the previous step. Where consumption is greater
    than startValue, it falls within this block and where consumption is less than or equal to startValue, it falls
    within one of the previous blocks."""

    consumptionBlock: ConsumptionBlockType = element()
    price: int | None = element(default=None)  # The charge for this rate component, per unit of measure defined by the
    # associated ReadingType, in currency specified in TariffProfile.  # noqa e114
    startValue: int = element()  # The lowest level of consumption that defines the starting point of this consumption
    # step or block. Thresholds start at zero for each billing period. # noqa e114


class ConsumptionTariffIntervalListResponse(SepList, tag="ConsumptionTariffIntervalList"):
    ConsumptionTariffInterval: list[ConsumptionTariffIntervalResponse] | None = element(default=None)


class ConsumptionTariffIntervalListSummaryResponse(SepList, tag="ConsumptionTariffIntervalListSummary", ns="csipaus"):
    """A list extension to allow clients to retrieve ConsumptionTariffInterval information without making a request
    against the ConsumptionTariffIntervalList resource"""

    ConsumptionTariffInterval: list[ConsumptionTariffIntervalResponse] | None = element(default=None, ns="")


class TimeTariffIntervalResponse(RandomizableEvent, tag="TimeTariffInterval"):
    """Describes the time-differentiated portion of the RateComponent, if applicable, and provides the ability to
    specify multiple time intervals, each with its own consumption-based components and other attributes."""

    ConsumptionTariffIntervalListLink: ListLink = element()
    touTier: TOUType = element()
    ConsumptionTariffIntervalListSummary: ConsumptionTariffIntervalListSummaryResponse = element(ns="csipaus")
    RateComponentLink: Link = element()


class TariffProfileListResponse(SubscribableList, tag="TariffProfileList"):
    pollRate: int | None = attr(default=DEFAULT_POLLRATE_SECONDS)
    TariffProfile: list[TariffProfileResponse] | None = element(default=None)


class RateComponentListResponse(SubscribableList, tag="RateComponentList"):
    RateComponent: list[RateComponentResponse] | None = element(default=None)


class TimeTariffIntervalListResponse(SubscribableList, tag="TimeTariffIntervalList"):
    pollRate: int | None = attr(default=DEFAULT_POLLRATE_SECONDS)
    TimeTariffInterval: list[TimeTariffIntervalResponse] | None = element(default=None)
