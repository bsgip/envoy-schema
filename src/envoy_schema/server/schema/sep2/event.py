from typing import Optional

from pydantic_xml import element

from envoy_schema.server.schema.sep2.identification import RespondableSubscribableIdentifiedObject
from envoy_schema.server.schema.sep2.types import DateTimeIntervalType, OneHourRangeType, TimeType
from envoy_schema.server.schema.sep2.primitive_types import String192
from envoy_schema.server.schema.sep2.base import BaseXmlModelWithNS


class EventStatus(BaseXmlModelWithNS):
    """Current status information relevant to a specific object. The Status object is used to indicate the current
    status of an Event. Devices can read the containing resource (e.g. TextMessage) to get the most up to date status of
    the event.  Devices can also subscribe to a specific resource instance to get updates when any of its attributes
    change, including the Status object."""

    currentStatus: int = element()
    dateTime: TimeType = element()
    potentiallySuperseded: bool = element()
    potentiallySupersededTime: Optional[TimeType] = element(default=None)
    reason: Optional[String192] = element(default=None)


class Event(RespondableSubscribableIdentifiedObject):
    """An Event indicates information that applies to a particular period of time. Events SHALL be executed relative
    to the time of the server, as described in the Time function set section 11.1."""

    creationTime: TimeType = element()
    EventStatus_: EventStatus = element(tag="EventStatus")
    interval: DateTimeIntervalType = element(tag="interval")


class RandomizableEvent(Event):
    """An Event that can indicate time ranges over which the start time and duration SHALL be randomized."""

    randomizeDuration: Optional[OneHourRangeType] = element(default=None)
    randomizeStart: Optional[OneHourRangeType] = element(default=None)
