import pytest
from assertical.fake.generator import generate_class_instance
from lxml import etree

from envoy_schema.server.schema.sep2.device_capability import DeviceCapabilityResponse


@pytest.mark.parametrize("optional_is_none", [True, False])
def test_DeviceCapabilityResponse_pollRate(optional_is_none: bool):
    """Ensure pollRate is encoded as an attribute (not an element) - This is a really basic regression test"""
    entity: DeviceCapabilityResponse = generate_class_instance(
        DeviceCapabilityResponse, optional_is_none=optional_is_none
    )
    entity.pollRate = 123654
    xml = entity.to_xml(skip_empty=True).decode()
    assert f'pollRate="{entity.pollRate}"' in xml


@pytest.mark.parametrize("optional_is_none", [True, False])
def test_DeviceCapabilityResponse_xsd(optional_is_none, csip_aus_schema: etree.XMLSchema, use_assertical_extensions):
    """Placeholder test for validating EndDeviceResponse against the csip-aus XSD"""

    # Generate XML string
    entity: DeviceCapabilityResponse = generate_class_instance(
        DeviceCapabilityResponse,
        generate_relationships=True,
        optional_is_none=optional_is_none,
        type=None,
    )
    xml = entity.to_xml(skip_empty=True).decode()
    xml_doc = etree.fromstring(xml)

    is_valid = csip_aus_schema.validate(xml_doc)
    errors = "\n".join((f"{e.line}: {e.message}" for e in csip_aus_schema.error_log))
    assert is_valid, f"{xml}\nErrors:\n{errors}"
