from enum import IntEnum
from typing import Optional

from pydantic_xml import element

from envoy_schema.server.schema.sep2.base import BaseXmlModelWithNS
from envoy_schema.server.schema.sep2.identification import RespondableSubscribableIdentifiedObject
from envoy_schema.server.schema.sep2.primitive_types import String192
from envoy_schema.server.schema.sep2.types import DateTimeIntervalType, OneHourRangeType, TimeType


class EventStatusType(IntEnum):
    """Field representing the current status type. All other values reserved."""

    # This status indicates that the event has been scheduled and the event has not yet started.
    # The server SHALL set the event to this status when the event is first scheduled and persist until the event has
    # become active or has been cancelled.  For events with a start time less than or equal to the current time, this
    # status SHALL never be indicated, the event SHALL start with a status of “Active”.
    Scheduled = 0

    # This status indicates that the event is currently active. The server SHALL set the event to this status when the
    #  event reaches its earliest Effective Start Time.
    Active = 1

    # When events are cancelled, the Status.dateTime attribute SHALL be set to the time the cancellation occurred,
    # which cannot be in the future.  The server is responsible for maintaining the cancelled event in its collection
    # for the duration of the original event, or until the server has run out of space and needs to store a new event.
    # Client devices SHALL be aware of Cancelled events, determine if the Cancelled event applies to them, and cancel
    # the event immediately if applicable.
    Cancelled = 2

    # The server is responsible for maintaining the cancelled event in its collection for the duration of the Effective
    #  Scheduled Period. Client devices SHALL be aware of Cancelled with Randomization events, determine if the
    # Cancelled event applies to them, and cancel the event immediately, using the larger of (absolute value of
    # randomizeStart) and (absolute value of randomizeDuration) as the end randomization, in seconds. This Status.type
    #  SHALL NOT be used with "regular" Events, only with specializations of RandomizableEvent.
    CancelledWithRandomization = 3

    # Events marked as Superseded by servers are events that may have been replaced by new events from the same program
    # that target the exact same set of deviceCategory's (if applicable) AND DERControl controls (e.g., opModTargetW)
    # (if applicable) and overlap for a given period of time. Servers SHALL mark an event as Superseded at the earliest
    # Effective Start Time of the overlapping event. Servers are responsible for maintaining the Superseded event in
    # their collection for the duration of the Effective Scheduled Period.
    #
    # Client devices encountering a Superseded event SHALL terminate execution of the event immediately and commence
    # execution of the new event immediately, unless the current time is within the start randomization window of the
    # superseded event, in which case the client SHALL obey the start randomization of the new event. This Status.type
    # SHALL NOT be used with TextMessage, since multiple text messages can be active.
    Superseded = 4


class EventStatus(BaseXmlModelWithNS):
    """Current status information relevant to a specific object. The Status object is used to indicate the current
    status of an Event. Devices can read the containing resource (e.g. TextMessage) to get the most up to date status of
    the event.  Devices can also subscribe to a specific resource instance to get updates when any of its attributes
    change, including the Status object."""

    currentStatus: int = element()  # encodes EventStatusType enum values
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
