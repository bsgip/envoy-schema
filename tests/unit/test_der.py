import pytest
from assertical.fake.generator import generate_class_instance
from lxml import etree
from pydantic_core import ValidationError

from envoy_schema.server.schema.sep2.der import (
    DER,
    DemandResponseProgramListResponse,
    DERAvailability,
    DERCapability,
    DERControlListResponse,
    DERListResponse,
    DERProgramListResponse,
    DERProgramResponse,
    DERSettings,
    DERStatus,
    DERType,
)


def test_missing_list_defaults_empty():
    """Ensure the list objects fallback to empty list if unspecified in source"""
    assert not DERControlListResponse.model_validate({"all_": 0, "results": 0}).DERControl
    assert not DERProgramListResponse.model_validate({"all_": 0, "results": 0}).DERProgram
    assert not DemandResponseProgramListResponse.model_validate({"all_": 0, "results": 0}).DemandResponseProgram
    assert not DERListResponse.model_validate({"all_": 0, "results": 0}).DER_


def test_DERCapability_roundtrip():
    original = DERCapability.model_validate(
        {"modesSupported": "0f", "rtgMaxW": {"multiplier": 5, "value": 456}, "type_": DERType.FUEL_CELL}
    )

    round_tripped = DERCapability.from_xml(original.to_xml(skip_empty=True))

    assert original.modesSupported == round_tripped.modesSupported
    assert original.rtgMaxW == round_tripped.rtgMaxW
    assert original.type_ == round_tripped.type_


def test_DERSettings_roundtrip():
    original = DERSettings.model_validate(
        {"setGradW": 123, "setMaxW": {"multiplier": 5, "value": 456}, "updatedTime": 789}
    )

    round_tripped = DERSettings.from_xml(original.to_xml(skip_empty=True))

    assert original.setGradW == round_tripped.setGradW
    assert original.setMaxW == round_tripped.setMaxW
    assert original.updatedTime == round_tripped.updatedTime


def test_DERStatus_roundtrip():
    original = DERStatus.model_validate({"readingTime": 789})

    round_tripped = DERStatus.from_xml(original.to_xml(skip_empty=True))

    assert original.readingTime == round_tripped.readingTime


def test_DERAvailability_roundtrip():
    original = DERAvailability.model_validate({"readingTime": 789})

    round_tripped = DERAvailability.from_xml(original.to_xml(skip_empty=True))

    assert original.readingTime == round_tripped.readingTime


def test_DERStatus_long_manufacturer():
    max_len = DERStatus.model_validate({"readingTime": 789, "manufacturerStatus": {"dateTime": 123, "value": "maxlen"}})
    with pytest.raises(ValidationError):
        DERStatus.model_validate({"readingTime": 789, "manufacturerStatus": {"dateTime": 123, "value": "toolong"}})

    assert max_len.manufacturerStatus.dateTime == 123
    assert max_len.manufacturerStatus.value == "maxlen"


@pytest.mark.parametrize("optional_is_none", [True, False])
def test_DERProgramList_xsd(optional_is_none: bool, csip_aus_schema: etree.XMLSchema, use_assertical_extensions):
    """Placeholder test for validating EndDeviceResponse against the csip-aus XSD"""

    # Generate XML string
    entity: DERProgramListResponse = generate_class_instance(
        DERProgramListResponse,
        optional_is_none=optional_is_none,
        type=None,
    )
    entity.DERProgram = [
        generate_class_instance(
            DERProgramResponse, optional_is_none=optional_is_none, mRID="1234567890abcdef", type=None
        )
    ]
    xml = entity.to_xml(skip_empty=True).decode()
    xml_doc = etree.fromstring(xml)

    is_valid = csip_aus_schema.validate(xml_doc)
    errors = "\n".join((f"{e.line}: {e.message}" for e in csip_aus_schema.error_log))
    assert is_valid, f"{xml}\nErrors:\n{errors}"


@pytest.mark.parametrize("optional_is_none", [True, False])
def test_DERList_xsd(optional_is_none: bool, csip_aus_schema: etree.XMLSchema, use_assertical_extensions):
    """Placeholder test for validating EndDeviceResponse against the csip-aus XSD"""

    # Generate XML string
    entity: DERListResponse = generate_class_instance(
        DERListResponse,
        optional_is_none=optional_is_none,
        type=None,
    )
    entity.DER_ = [generate_class_instance(DER, optional_is_none=optional_is_none, type=None)]
    xml = entity.to_xml(skip_empty=True).decode()
    xml_doc = etree.fromstring(xml)

    is_valid = csip_aus_schema.validate(xml_doc)
    errors = "\n".join((f"{e.line}: {e.message}" for e in csip_aus_schema.error_log))
    assert is_valid, f"{xml}\nErrors:\n{errors}"
