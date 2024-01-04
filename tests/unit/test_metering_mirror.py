from envoy_schema.server.schema.sep2.metering_mirror import MirrorUsagePointListResponse


def test_missing_list_defaults_empty():
    """Ensure the list objects fallback to empty list if unspecified in source"""
    assert not MirrorUsagePointListResponse.model_validate({"all_": 0, "results": 0}).mirrorUsagePoints
