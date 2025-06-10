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
SiteListUri = "/site"
SiteUri = "/site/{site_id}"  # Supports deleting single sites
SiteControlDefaultConfigUri = "/site/{site_id}/control_default"  # For managing ControlDefaultConfig per site
SiteGroupUri = "/site_group/{group_name}"
SiteGroupListUri = "/site_group"
SiteReading = "/site-reading"
AggregatorBillingUri = "/billing/aggregator/{aggregator_id}/tariff/{tariff_id}/period/{period_start}/{period_end}"
SitePeriodBillingUri = "/billing/site/period"
CalculationLogBillingUri = "/billing/calculation_log/{calculation_log_id}/tariff/{tariff_id}"
CalculationLogCreateUri = "/calculation_log"
CalculationLogUri = "/calculation_log/{calculation_log_id}"
CalculationLogsForPeriod = "/calculation_log/period/{period_start}/{period_end}"

SiteControlGroupListUri = "/site_control_group"  # Fetching / Adding site control groups
SiteControlGroupUri = "/site_control_group/{group_id}"  # Fetching / Changing site control groups
SiteControlUri = "/site_control_group/{group_id}/controls"  # Fetching / Adding site controls (under a group)
SiteControlRangeUri = "/site_control_group/{group_id}/controls/{period_start}/{period_end}"  # Fetching/deleting controls that start in range # noqa: E501

ServerConfigRuntimeUri = "/server_config/run_time"  # For getting/setting ServerRuntimeConfig
ServerConfigControlDefaultUri = "/server_config/control_default"  # For getting/setting ControlDefaultConfig
