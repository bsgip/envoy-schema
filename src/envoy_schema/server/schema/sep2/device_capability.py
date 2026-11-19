from pydantic_xml import attr, element

from envoy_schema.server.schema import uri
from envoy_schema.server.schema.sep2.function_set_assignments import FunctionSetAssignmentsBase
from envoy_schema.server.schema.sep2.identification import ListLink
from envoy_schema.server.schema.sep2.types import DEFAULT_POLLRATE_SECONDS


class DeviceCapabilityResponse(FunctionSetAssignmentsBase, tag="DeviceCapability"):
    href: str = attr(default=uri.DeviceCapabilityUri)
    pollRate: int | None = attr(default=DEFAULT_POLLRATE_SECONDS)  # recommended client pollrate in seconds

    # (0..1) Link
    # Not supported at this time
    # SelfDeviceLink: Optional[Link] = element(default=None)

    # (0..1) ListLink
    EndDeviceListLink: ListLink | None = element(default=None)
    MirrorUsagePointListLink: ListLink | None = element(default=None)
