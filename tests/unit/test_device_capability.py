import pytest
from assertical.fake.generator import generate_class_instance

from envoy_schema.server.schema.sep2.device_capability import DeviceCapabilityResponse


@pytest.mark.parametrize("optional_is_none", [True, False])
def test_DeviceCapabilityResponse_pollRate(optional_is_none: bool):
    """Ensure pollRate is encoded as an attribute (not an element) - This is a really basic regression test"""
    entity: DeviceCapabilityResponse = generate_class_instance(
        DeviceCapabilityResponse, optional_is_none=optional_is_none
    )
    entity.pollRate = 123654
    xml = entity.to_xml(skip_empty=False, exclude_none=True, exclude_unset=True).decode()
    assert f'pollRate="{entity.pollRate}"' in xml
