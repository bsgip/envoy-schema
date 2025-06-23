from datetime import datetime

import pydantic
from envoy_schema.admin.schema import base


class AggregatorDomain(pydantic.BaseModel):
    """A domain whitelisted by the utility server as being controlled by the parent aggregator"""

    domain: str
    created_time: datetime
    changed_time: datetime


class AggregatorResponse(pydantic.BaseModel):
    """Metadata about a specific aggregator registered in the utility server"""

    aggregator_id: int
    name: str
    domains: list[AggregatorDomain]


class AggregatorPageResponse(base.BasePageModel):
    """Represents a paginated response of Aggregators"""

    aggregators: list[AggregatorResponse]  # The aggregator models in this page


class AggregatorDomainResponse(pydantic.BaseModel):
    """Represents a specific aggregator domain registered in the utility server"""

    aggregator_domain_id: int
    aggregator_id: int
    created_time: datetime
    changed_time: datetime
    domain: str


class AggregatorDomainPageResponse(base.BasePageModel):
    """Represents a paginated response of aggregator domains"""

    aggregator_domains: list[AggregatorDomainResponse]
