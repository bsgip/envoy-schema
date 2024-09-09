from typing import Optional

from pydantic_xml import attr, element

from envoy_schema.server.schema.sep2 import primitive_types, types
from envoy_schema.server.schema.sep2.identification import IdentifiedObject, Link, ListLink, Resource, SubscribableList


class ReadingBase(Resource):
    consumptionBlock: Optional[types.ConsumptionBlockType] = element(default=0)
    qualityFlags: Optional[primitive_types.HexBinary16] = element(
        default=primitive_types.HexBinary16("00")
    )  # string (hex encoded) form that maps to QualityFlagsType
    timePeriod: Optional[types.DateTimeIntervalType] = element(
        default=None, tag="timePeriod"
    )  # Necessary due to DateTimeIntervalType defn
    touTier: Optional[types.TOUType] = element(default=0)
    value: Optional[int] = element(default=None)


class Reading(ReadingBase):
    localID: Optional[primitive_types.HexBinary16] = element(default=None)
    subscribable: Optional[types.SubscribableType] = attr(default=None)


class ReadingSetBase(IdentifiedObject):
    timePeriod: types.DateTimeIntervalType = element(tag="timePeriod")  # Necessary due to DateTimeIntervalType defn


class ReadingType(Resource):
    """Type of data conveyed by a specific Reading. See IEC 61968 Part 9 Annex C for full definitions
    of these values."""

    accumulationBehaviour: Optional[types.AccumulationBehaviourType] = element(default=None)
    calorificValue: Optional[types.UnitValueType] = element(default=None)
    commodity: Optional[types.CommodityType] = element(default=None)
    conversionFactor: Optional[types.UnitValueType] = element(default=None)
    dataQualifier: Optional[types.DataQualifierType] = element(default=None)
    flowDirection: Optional[types.FlowDirectionType] = element(default=None)
    intervalLength: Optional[int] = element(default=None)
    kind: Optional[types.KindType] = element(default=None)
    maxNumberOfIntervals: Optional[int] = element(default=None)
    numberOfConsumptionBlocks: Optional[int] = element(default=None)
    numberOfTouTiers: Optional[int] = element(default=None)
    phase: Optional[types.PhaseCode] = element(default=None)
    powerOfTenMultiplier: Optional[int] = element(default=None)
    subIntervalLength: Optional[int] = element(default=None)
    supplyLimit: Optional[int] = element(default=None)
    tieredConsumptionBlocks: Optional[bool] = element(default=None)
    uom: Optional[types.UomType] = element(default=None)


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
    MeterReadingListLink: Optional[ListLink] = element(default=None)


class MeterReading(IdentifiedObject):
    """Set of values obtained from the meter."""

    RateComponentListLink: Optional[ListLink] = element(default=None)
    ReadingLink: Optional[Link] = element(default=None)
    ReadingSetListLink: Optional[ListLink] = element(default=None)
    ReadingTypeLink: Link = element()


class ReadingSet(ReadingSetBase):
    """A set of Readings of the ReadingType indicated by the parent MeterReading."""

    ReadingListLink: Optional[ListLink] = element(default=None)


class ReadingListResponse(SubscribableList, tag="ReadingList"):
    Readings: Optional[list["Reading"]] = element(default=None, tag="Reading")
