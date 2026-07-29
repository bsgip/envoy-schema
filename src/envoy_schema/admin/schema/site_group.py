from datetime import datetime

from pydantic import BaseModel


class SiteGroupRequest(BaseModel):
    """Request model for SiteGroup - used for creating"""

    name: str  # Unique name of this SiteGroup
    default_group: bool  # If set - all "new" site registrations (in/out of band) will be assigned to this group\


class SiteGroupResponse(SiteGroupRequest):
    """Response model for SiteGroup - includes basic summary information"""

    site_group_id: int
    created_time: datetime
    changed_time: datetime

    total_sites: int  # How many sites/assignments are linked to this group


class SiteGroupPageResponse(BaseModel):
    """Represents a paginated response of SiteGroup"""

    total_count: int  # The total number of groups (independent of this page of results)
    limit: int  # The maximum number of groups that could've been returned (the limit set by the query)
    start: int  # The number of groups that have been skipped as part of this query (the start set by the query)
    groups: list[SiteGroupResponse]  # The group models in this page


class SiteGroupAssignmentRequest(BaseModel):
    """Request model for SiteGroupAssignment - used for creating new assignments to a SiteGroup"""

    site_id: int  # The site_id whose membership is being added to a group


class SiteGroupAssignmentResponse(SiteGroupAssignmentRequest):
    """Response model for SiteGroupAssignment - used for checking membership"""

    site_group_assignment_id: int
    created_time: datetime
    changed_time: datetime


class SiteGroupAssignmentPageResponse(BaseModel):
    """Represents a paginated response of SiteGroupAssignment"""

    total_count: int  # The total number of assignments (independent of this page of results)
    limit: int  # The maximum number of assignments that could've been returned (the limit set by the query)
    start: int  # The number of assignments that have been skipped as part of this query (the start set by the query)
    assignments: list[SiteGroupAssignmentResponse]  # The assignment models in this page
