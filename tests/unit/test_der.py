import pytest
from pydantic_core import ValidationError

from envoy_schema.server.schema.sep2.der import (
    DemandResponseProgramListResponse,
    DERAvailability,
    DERCapability,
    DERControlListResponse,
    DERListResponse,
    DERProgramListResponse,
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
