from envoy_schema.server.schema.sep2.end_device import EndDeviceListResponse


def test_missing_list_defaults_empty():
    """Ensure the list objects fallback to empty list if unspecified in source"""
    assert EndDeviceListResponse.validate({"all_": 0, "results": 0}).EndDevice == []
