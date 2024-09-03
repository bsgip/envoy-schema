from typing import Optional

from pydantic_xml import attr, element

from envoy_schema.server.schema.sep2.identification import (
    IdentifiedObject,
    Link,
    ListLink,
    Resource,
    SubscribableList,
    SubscribableResource,
)
from envoy_schema.server.schema.sep2.types import DEFAULT_POLLRATE_SECONDS


class FunctionSetAssignmentsBase(Resource):
    # Optional (0..1) Links and ListLinks
    CustomerAccountListLink: Optional[ListLink] = element(default=None)
    DemandResponseProgramListLink: Optional[ListLink] = element(default=None)
    DERProgramListLink: Optional[ListLink] = element(default=None)
    FileListLink: Optional[ListLink] = element(default=None)
    MessagingProgramListLink: Optional[ListLink] = element(default=None)
    PrepaymentListLink: Optional[ListLink] = element(default=None)
    ResponseSetListLink: Optional[ListLink] = element(default=None)
    TariffProfileListLink: Optional[ListLink] = element(default=None)
    TimeLink: Optional[Link] = element(default=None)
    UsagePointListLink: Optional[ListLink] = element(default=None)


# The SEP2 standard doesn't explicitly state that FunctionSetAssignments derives from
# IdentifiedObject nor SubscribableResource. However the fields present on FunctionSetAssignments
# matches those present in IdentifiedObject and SubscribableResource so we have decided to inherit from these
# in addition to explicitly stated parent class, namely, FunctionSetAssignmentsBase
class FunctionSetAssignmentsResponse(
    IdentifiedObject, FunctionSetAssignmentsBase, SubscribableResource, tag="FunctionSetAssignments"
):
    pass


class FunctionSetAssignmentsListResponse(SubscribableList, tag="FunctionSetAssignmentsList"):

    FunctionSetAssignments: list[FunctionSetAssignmentsResponse] = element(default_factory=list)
    pollRate: Optional[int] = attr(default=DEFAULT_POLLRATE_SECONDS)  # recommended client pollrate in seconds
