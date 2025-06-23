import pytest
from assertical.fake.generator import generate_class_instance

from envoy_schema.server.schema.sep2.function_set_assignments import FunctionSetAssignmentsListResponse


def test_missing_list_defaults_empty():
    """Ensure the list objects fallback to empty list if unspecified in source"""
    assert not FunctionSetAssignmentsListResponse.model_validate({"all_": 0, "results": 0}).FunctionSetAssignments


@pytest.mark.parametrize("optional_is_none", [True, False])
def test_FunctionSetAssignmentsListResponse_pollRate(optional_is_none: bool):
    """Ensure pollRate is encoded as an attribute (not an element) - This is a really basic regression test"""
    entity: FunctionSetAssignmentsListResponse = generate_class_instance(
        FunctionSetAssignmentsListResponse, optional_is_none=optional_is_none
    )
    entity.pollRate = 123654
    xml = entity.to_xml(skip_empty=False, exclude_none=True, exclude_unset=True).decode()
    assert f'pollRate="{entity.pollRate}"' in xml
