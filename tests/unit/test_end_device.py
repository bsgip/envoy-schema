import pytest
from assertical.fake.generator import generate_class_instance
from lxml import etree

from envoy_schema.server.schema.sep2.end_device import EndDeviceListResponse, EndDeviceResponse
from envoy_schema.server.schema.sep2.identification import Link, ListLink


def test_missing_list_defaults_empty():
    """Ensure the list objects fallback to empty list if unspecified in source"""
    assert not EndDeviceListResponse.model_validate({"all_": 0, "results": 0}).EndDevice


@pytest.mark.parametrize("optional_is_none", [True, False])
def test_EndDeviceResponse_xsd(optional_is_none: bool, csip_aus_schema: etree.XMLSchema, use_assertical_extensions):
    """Placeholder test for validating EndDeviceResponse against the csip-aus XSD"""

    # Generate XML string
    entity: EndDeviceResponse = generate_class_instance(
        EndDeviceResponse,
        generate_relationships=True,
        optional_is_none=optional_is_none,
        type=None,
        deviceCategory="01",
        lFDI="11",
    )
    xml = entity.to_xml(skip_empty=True).decode()
    xml_doc = etree.fromstring(xml)

    is_valid = csip_aus_schema.validate(xml_doc)
    errors = "\n".join((f"{e.line}: {e.message}" for e in csip_aus_schema.error_log))
    assert is_valid, f"{xml}\nErrors:\n{errors}"
