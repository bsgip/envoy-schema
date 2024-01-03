from envoy_schema.server.schema.sep2.der import (
    DemandResponseProgramListResponse,
    DERControlListResponse,
    DERProgramListResponse,
)


def test_missing_list_defaults_empty():
    """Ensure the list objects fallback to empty list if unspecified in source"""
    assert DERControlListResponse.validate({"all_": 0, "results": 0}).DERControl == []
    assert DERProgramListResponse.validate({"all_": 0, "results": 0}).DERProgram == []
    assert DemandResponseProgramListResponse.validate({"all_": 0, "results": 0}).DemandResponseProgram == []
