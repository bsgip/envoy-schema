from typing import Optional

from pydantic_xml import attr, element

from envoy_schema.server.schema.sep2.identification import Resource
from envoy_schema.server.schema.sep2.types import TimeOffsetType, TimeQualityType, TimeType


class TimeResponse(Resource, tag="Time"):
    # xsd
    href: str = attr()

    currentTime: TimeType = element()
    dstEndTime: TimeType = element()
    dstOffset: TimeOffsetType = element()
    dstStartTime: TimeType = element()
    localTime: Optional[TimeType] = element(default=None)
    quality: TimeQualityType = element()
    tzOffset: TimeOffsetType = element()
