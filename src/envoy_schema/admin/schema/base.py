from pydantic import BaseModel


class BasePageModel(BaseModel):
    total_count: int  # The total number of objects (independent of this page of results)
    limit: int  # The maximum number of objects that could've been returned (the limit set by the query)
    start: int  # The number of objects that have been skipped as part of this query (the start set by the query)


class BatchCreateResponse(BaseModel):
    """Returns all IDs that were inserted/updated - they will correspond 1-1 with the submitted batch request such
    that ids[X] corresponds to the entity at request[X]"""

    ids: list[int]  # Corresponds 1-1 with the incoming request entities
