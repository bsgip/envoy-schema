from envoy_schema.server.schema.sep2.function_set_assignments import FunctionSetAssignmentsListResponse


def test_missing_list_defaults_empty():
    """Ensure the list objects fallback to empty list if unspecified in source"""
    assert FunctionSetAssignmentsListResponse.validate({"all_": 0, "results": 0}).FunctionSetAssignments == []
