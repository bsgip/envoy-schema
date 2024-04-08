from datetime import datetime

from pydantic import BaseModel


class AggregatorDomain(BaseModel):
    """A domain whitelisted by the utility server as being controlled by the parent aggregator"""

    domain: str
    changed_time: datetime


class AggregatorResponse(BaseModel):
    """Metadata about a specific aggregator registered in the utility server"""

    aggregator_id: int
    name: str
    domains: list[AggregatorDomain]
