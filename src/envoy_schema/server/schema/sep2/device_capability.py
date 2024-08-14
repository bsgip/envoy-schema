from typing import Optional

from pydantic_xml import attr, element

from envoy_schema.server.schema import uri
from envoy_schema.server.schema.sep2.identification import ListLink, Resource
from envoy_schema.server.schema.sep2.types import DEFAULT_POLLRATE_SECONDS


# Per the Sep2, DeviceCapability should be a subclass of FunctionSetAssignmentsBase
# However, DERProgramListUri and TariffProfileListUri are now site-scoped, which
# breaks how links are populated in DeviceCapability.
# Since clients are expected to access DERProgramList and TariffProfileList through
# FunctionSetAssignments rather than through DeviceCapability, we can disable them
# by not subclassing FunctionSetAssignmentsBase but subclassing Resource instead.
class DeviceCapabilityResponse(Resource, tag="DeviceCapability"):
    href: str = attr(default=uri.DeviceCapabilityUri)
    pollRate: Optional[int] = attr(default=DEFAULT_POLLRATE_SECONDS)  # recommended client pollrate in seconds

    # (0..1) Link
    # Not supported at this time
    # SelfDeviceLink: Optional[Link] = element(default=None)

    # (0..1) ListLink
    EndDeviceListLink: Optional[ListLink] = element(default=None)
    MirrorUsagePointListLink: Optional[ListLink] = element(default=None)
