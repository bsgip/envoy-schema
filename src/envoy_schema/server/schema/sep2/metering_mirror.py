from typing import List

from pydantic_xml import attr, element

from envoy_schema.server.schema.sep2 import primitive_types, types
from envoy_schema.server.schema.sep2.identification import IdentifiedObject, Resource
from envoy_schema.server.schema.sep2.identification import List as Sep2List
from envoy_schema.server.schema.sep2.metering import Reading, ReadingSetBase, ReadingType, UsagePointBase


class MirrorReadingSet(ReadingSetBase):
    readings: List[Reading] | None = element(tag="Reading", default=None)


class MeterReadingBase(IdentifiedObject):
    pass


class MirrorMeterReading(MeterReadingBase):
    lastUpdateTime: types.TimeType | None = element(default=None)
    mirrorReadingSets: List[MirrorReadingSet] | None = element(tag="MirrorReadingSet", default=None)
    nextUpdateTime: types.TimeType | None = element(default=None)
    reading: Reading | None = element(tag="Reading", default=None)
    readingType: ReadingType | None = element(tag="ReadingType", default=None)


class MirrorUsagePoint(UsagePointBase):
    deviceLFDI: primitive_types.HexBinary160 = element()
    mirrorMeterReadings: List[MirrorMeterReading] | None = element(tag="MirrorMeterReading", default=None)
    postRate: int | None = element(default=None)


class MirrorUsagePointList(Sep2List):
    pollRate: int | None = attr(default=types.DEFAULT_POLLRATE_SECONDS)  # recommended client pollrate in seconds
    mirrorUsagePoints: List[MirrorUsagePoint] | None = element(tag="MirrorUsagePoint", default=None)


class MirrorMeterReadingList(Sep2List):
    mirrorMeterReadings: List[MirrorMeterReading] | None = element(tag="MirrorMeterReading", default=None)


class MirrorMeterReadingRequest(MirrorMeterReading, tag="MirrorMeterReading"):
    pass


# Unlike MirrorMeterReadingList this is a list resource is doesn't subclass Sep2List. The reasons is that clients
# don't need to specify the attributes 'all' or 'result' for the list resources they are posting
class MirrorMeterReadingListRequest(Resource, tag="MirrorMeterReadingList"):
    mirrorMeterReadings: List[MirrorMeterReading] | None = element(tag="MirrorMeterReading", default=None)


class MirrorUsagePointListResponse(Sep2List, tag="MirrorUsagePointList"):
    pollRate: int | None = attr(default=types.DEFAULT_POLLRATE_SECONDS)  # recommended client pollrate in seconds
    mirrorUsagePoints: list[MirrorUsagePoint] = element(tag="MirrorUsagePoint", default_factory=list)


class MirrorUsagePointRequest(MirrorUsagePoint, tag="MirrorUsagePoint"):
    pass
