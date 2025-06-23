from envoy_schema.server.schema.sep2.metering import ReadingListResponse


def test_missing_list_defaults_empty():
    """Ensure the list objects fallback to empty list if unspecified in source"""
    assert not ReadingListResponse.model_validate({"all_": 0, "results": 0}).Readings
