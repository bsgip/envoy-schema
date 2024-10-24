from datetime import datetime

from pydantic import BaseModel


class AggregatorDomain(BaseModel):
    """A domain whitelisted by the utility server as being controlled by the parent aggregator"""

    domain: str
    created_time: datetime
    changed_time: datetime


class AggregatorResponse(BaseModel):
    """Metadata about a specific aggregator registered in the utility server"""

    aggregator_id: int
    name: str
    domains: list[AggregatorDomain]


class AggregatorPageResponse(BaseModel):
    """Represents a paginated response of Aggregators"""

    total_count: int  # The total number of aggregators (independent of this page of results)
    limit: int  # The maximum number of aggregators that could've been returned (the limit set by the query)
    start: int  # The number of aggregators that have been skipped as part of this query (the start set by the query)
    aggregators: list[AggregatorResponse]  # The aggregator models in this page
