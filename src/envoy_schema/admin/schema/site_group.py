from datetime import datetime

from pydantic import BaseModel


class SiteGroupResponse(BaseModel):
    """Response model for SiteGroup - includes basic summary information"""

    site_group_id: int
    name: str
    created_time: datetime
    changed_time: datetime
    total_sites: int  # How many sites are linked to this group


class SiteGroupPageResponse(BaseModel):
    """Represents a paginated response of SiteGroup"""

    total_count: int  # The total number of groups (independent of this page of results)
    limit: int  # The maximum number of groups that could've been returned (the limit set by the query)
    start: int  # The number of groups that have been skipped as part of this query (the start set by the query)
    groups: list[SiteGroupResponse]  # The group models in this page
