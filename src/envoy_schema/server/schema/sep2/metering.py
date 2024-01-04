from typing import Optional

from pydantic_xml import attr, element

from envoy_schema.server.schema.sep2 import primitive_types, types
from envoy_schema.server.schema.sep2.identification import IdentifiedObject, Resource


class ReadingBase(Resource):
    consumptionBlock: Optional[types.ConsumptionBlockType] = element(default=0)
    qualityFlags: Optional[primitive_types.HexBinary16] = element(
        default=primitive_types.HexBinary16("00")
    )  # string (hex encoded) form that maps to QualityFlagsType
    timePeriod: Optional[types.DateTimeIntervalType] = element(default=None)
    touTier: Optional[types.TOUType] = element(default=0)
    value: Optional[int] = element(default=None)


class Reading(ReadingBase):
    subscribable: Optional[types.SubscribableType] = attr(default=None)
    localID: Optional[primitive_types.HexBinary16] = element(default=None)


class ReadingSetBase(IdentifiedObject):
    timePeriod: types.DateTimeIntervalType = element()


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
    roleFlags: int = element()  # This should be of type RoleFlagsType
    serviceCategoryKind: types.ServiceKind = element()
    status: int = element()
