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
    CustomerAccountListLink: ListLink | None = element(default=None)
    DemandResponseProgramListLink: ListLink | None = element(default=None)
    DERProgramListLink: ListLink | None = element(default=None)
    FileListLink: ListLink | None = element(default=None)
    MessagingProgramListLink: ListLink | None = element(default=None)
    PrepaymentListLink: ListLink | None = element(default=None)
    ResponseSetListLink: ListLink | None = element(default=None)
    TariffProfileListLink: ListLink | None = element(default=None)
    TimeLink: Link | None = element(default=None)
    UsagePointListLink: ListLink | None = element(default=None)


# The SEP2 standard doesn't explicitly state that FunctionSetAssignments derives from
# IdentifiedObject nor SubscribableResource. However the fields present on FunctionSetAssignments
# matches those present in IdentifiedObject and SubscribableResource so we have decided to inherit from these
# in addition to explicitly stated parent class, namely, FunctionSetAssignmentsBase
class FunctionSetAssignmentsResponse(
    IdentifiedObject, FunctionSetAssignmentsBase, SubscribableResource, tag="FunctionSetAssignments"
):
    pass


class FunctionSetAssignmentsListResponse(SubscribableList, tag="FunctionSetAssignmentsList"):
    FunctionSetAssignments: list[FunctionSetAssignmentsResponse] | None = element(default=None)
    pollRate: int | None = attr(default=DEFAULT_POLLRATE_SECONDS)  # recommended client pollrate in seconds
