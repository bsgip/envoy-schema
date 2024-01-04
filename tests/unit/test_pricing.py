from envoy_schema.server.schema.sep2.pricing import (
    ConsumptionTariffIntervalListResponse,
    RateComponentListResponse,
    TariffProfileListResponse,
    TimeTariffIntervalListResponse,
)


def test_missing_list_defaults_empty():
    """Ensure the list objects fallback to empty list if unspecified in source"""
    assert not RateComponentListResponse.model_validate({"all_": 0, "results": 0}).RateComponent
    assert not TariffProfileListResponse.model_validate({"all_": 0, "results": 0}).TariffProfile
    assert not TimeTariffIntervalListResponse.model_validate({"all_": 0, "results": 0}).TimeTariffInterval
    assert not ConsumptionTariffIntervalListResponse.model_validate({"all_": 0, "results": 0}).ConsumptionTariffInterval
