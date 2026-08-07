from pydantic_xml import attr, element

from envoy_schema.server.schema.sep2 import primitive_types, types
from envoy_schema.server.schema.sep2.identification import IdentifiedObject, Link, ListLink, Resource, SubscribableList


class ReadingBase(Resource):
    consumptionBlock: types.ConsumptionBlockType | None = element(default=0)
    qualityFlags: primitive_types.HexBinary16 | None = element(
        default=primitive_types.HexBinary16("00")  # ty:ignore[call-non-callable]
    )  # string (hex encoded) form that maps to QualityFlagsType
    timePeriod: types.DateTimeIntervalType | None = element(
        default=None, tag="timePeriod"
    )  # Necessary due to DateTimeIntervalType defn
    touTier: types.TOUType | None = element(default=0)
    value: int | None = element(default=None)


class Reading(ReadingBase):
    localID: primitive_types.HexBinary16 | None = element(default=None)
    subscribable: types.SubscribableType | None = attr(default=None)


class ReadingSetBase(IdentifiedObject):
    timePeriod: types.DateTimeIntervalType = element(tag="timePeriod")  # Necessary due to DateTimeIntervalType defn


class ReadingType(Resource):
    """Type of data conveyed by a specific Reading. See IEC 61968 Part 9 Annex C for full definitions
    of these values."""

    accumulationBehaviour: types.AccumulationBehaviourType | None = element(default=None)
    calorificValue: types.UnitValueType | None = element(default=None)
    commodity: types.CommodityType | None = element(default=None)
    conversionFactor: types.UnitValueType | None = element(default=None)
    dataQualifier: types.DataQualifierType | None = element(default=None)
    flowDirection: types.FlowDirectionType | None = element(default=None)
    intervalLength: int | None = element(default=None)
    kind: types.KindType | None = element(default=None)
    maxNumberOfIntervals: int | None = element(default=None)
    numberOfConsumptionBlocks: int | None = element(default=None)
    numberOfTouTiers: int | None = element(default=None)
    phase: types.PhaseCode | None = element(default=None)
    powerOfTenMultiplier: int | None = element(default=None)
    subIntervalLength: int | None = element(default=None)
    supplyLimit: int | None = element(default=None)
    tieredConsumptionBlocks: bool | None = element(default=None)
    uom: types.UomType | None = element(default=None)


class UsagePointBase(IdentifiedObject):
    """Logical point on a network at which consumption or production is either physically measured (e.g. metered) or
    estimated (e.g. unmetered street lights)."""

    roleFlags: primitive_types.HexBinary16 = element()
    serviceCategoryKind: types.ServiceKind = element()
    status: int = element()


class UsagePoint(UsagePointBase):
    """Logical point on a network at which consumption or production is either physically measured (e.g. metered) or
    estimated (e.g. unmetered street lights)."""

    deviceLFDI: str = element()
    MeterReadingListLink: ListLink | None = element(default=None)


class MeterReading(IdentifiedObject):
    """Set of values obtained from the meter."""

    RateComponentListLink: ListLink | None = element(default=None)
    ReadingLink: Link | None = element(default=None)
    ReadingSetListLink: ListLink | None = element(default=None)
    ReadingTypeLink: Link = element()


class ReadingSet(ReadingSetBase):
    """A set of Readings of the ReadingType indicated by the parent MeterReading."""

    ReadingListLink: ListLink | None = element(default=None)


class ReadingListResponse(SubscribableList, tag="ReadingList"):
    Readings: list["Reading"] | None = element(default=None, tag="Reading")
