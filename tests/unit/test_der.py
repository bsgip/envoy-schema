from envoy_schema.server.schema.sep2.der import (
    DemandResponseProgramListResponse,
    DERControlListResponse,
    DERProgramListResponse,
)


def test_missing_list_defaults_empty():
    """Ensure the list objects fallback to empty list if unspecified in source"""
    assert not DERControlListResponse.model_validate({"all_": 0, "results": 0}).DERControl
    assert not DERProgramListResponse.model_validate({"all_": 0, "results": 0}).DERProgram
    assert not DemandResponseProgramListResponse.model_validate({"all_": 0, "results": 0}).DemandResponseProgram
