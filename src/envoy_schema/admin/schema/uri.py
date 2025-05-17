"""Defines all the URIs"""

AggregatorListUri = "/aggregator"
AggregatorUri = "/aggregator/{aggregator_id}"
ArchiveForPeriodSites = "/archive/{period_start}/{period_end}/sites"
ArchiveForPeriodDoes = "/archive/{period_start}/{period_end}/does"
ArchiveForPeriodTariffGeneratedRate = "/archive/{period_start}/{period_end}/tariff_generated_rates"
TariffCreateUri = "/tariff"
TariffUpdateUri = "/tariff/{tariff_id}"
TariffGeneratedRateCreateUri = "/tariff_generated_rate"
DoeUri = "/doe"
SiteUri = "/site"
SiteUri = "/site/{site_id}"  # Supports deleting single sites
SiteControlDefaultConfigUri = "/site/{site_id}/control_default"  # For managing ControlDefaultConfig per site
SiteGroupUri = "/site_group/{group_name}"
SiteGroupListUri = "/site_group"
AggregatorBillingUri = "/billing/aggregator/{aggregator_id}/tariff/{tariff_id}/period/{period_start}/{period_end}"
SitePeriodBillingUri = "/billing/site/period"
CalculationLogBillingUri = "/billing/calculation_log/{calculation_log_id}/tariff/{tariff_id}"
CalculationLogCreateUri = "/calculation_log"
CalculationLogUri = "/calculation_log/{calculation_log_id}"
CalculationLogsForPeriod = "/calculation_log/period/{period_start}/{period_end}"

SiteControlGroupUri = "/site_control"  # Fetching / Adding site control groups
SiteControlUri = "/site_control/{group_id}"  # Fetching / Adding site controls (under a group)
SiteControlRangeUri = (
    "/site_control/{group_id}/{period_start}/{period_end}"  # Fetching / deleting controls that are active in range
)

ServerConfigRuntimeUri = "/server_config/run_time"  # For getting/setting ServerRuntimeConfig
ServerConfigControlDefaultUri = "/server_config/control_default"  # For getting/setting ControlDefaultConfig
