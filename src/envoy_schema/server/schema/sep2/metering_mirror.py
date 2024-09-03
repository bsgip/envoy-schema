from typing import List, Optional

from pydantic_xml import attr, element

from envoy_schema.server.schema.sep2 import primitive_types, types
from envoy_schema.server.schema.sep2.identification import IdentifiedObject
from envoy_schema.server.schema.sep2.identification import List as Sep2List
from envoy_schema.server.schema.sep2.identification import Resource
from envoy_schema.server.schema.sep2.metering import Reading, ReadingSetBase, ReadingType, UsagePointBase


class MirrorReadingSet(ReadingSetBase):
    readings: Optional[List[Reading]] = element(tag="Reading", default=None)


class MeterReadingBase(IdentifiedObject):
    pass


class MirrorMeterReading(MeterReadingBase):
    lastUpdateTime: Optional[types.TimeType] = element(default=None)
    mirrorReadingSets: Optional[List[MirrorReadingSet]] = element(tag="MirrorReadingSet", default=None)
    nextUpdateTime: Optional[types.TimeType] = element(default=None)
    reading: Optional[Reading] = element(tag="Reading", default=None)
    readingType: Optional[ReadingType] = element(tag="ReadingType", default=None)


class MirrorUsagePoint(UsagePointBase):
    deviceLFDI: primitive_types.HexBinary160 = element()
    mirrorMeterReadings: Optional[List[MirrorMeterReading]] = element(tag="MirrorMeterReading", default=None)
    postRate: Optional[int] = element(default=None)


class MirrorUsagePointList(Sep2List):
    pollRate: Optional[int] = attr(default=types.DEFAULT_POLLRATE_SECONDS)  # recommended client pollrate in seconds
    mirrorUsagePoints: Optional[List[MirrorUsagePoint]] = element(tag="MirrorUsagePoint", default=None)


class MirrorMeterReadingList(Sep2List):
    mirrorMeterReadings: Optional[List[MirrorMeterReading]] = element(tag="MirrorMeterReading", default=None)


class MirrorMeterReadingRequest(MirrorMeterReading, tag="MirrorMeterReading"):
    pass


# Unlike MirrorMeterReadingList this is a list resource is doesn't subclass Sep2List. The reasons is that clients
# don't need to specify the attributes 'all' or 'result' for the list resources they are posting
class MirrorMeterReadingListRequest(Resource, tag="MirrorMeterReadingList"):
    mirrorMeterReadings: Optional[List[MirrorMeterReading]] = element(tag="MirrorMeterReading", default=None)


class MirrorUsagePointListResponse(Sep2List, tag="MirrorUsagePointList"):
    mirrorUsagePoints: list[MirrorUsagePoint] = element(tag="MirrorUsagePoint", default_factory=list)


class MirrorUsagePointRequest(MirrorUsagePoint, tag="MirrorUsagePoint"):
    pass
