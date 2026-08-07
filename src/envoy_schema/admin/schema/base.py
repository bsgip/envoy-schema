from enum import StrEnum

from pydantic import BaseModel


class BasePageModel(BaseModel):
    total_count: int  # The total number of objects (independent of this page of results)
    limit: int  # The maximum number of objects that could've been returned (the limit set by the query)
    start: int  # The number of objects that have been skipped as part of this query (the start set by the query)


class BatchCreateResponse(BaseModel):
    """Returns all IDs that were inserted/updated - they will correspond 1-1 with the submitted batch request such
    that ids[X] corresponds to the entity at request[X]"""

    ids: list[int]  # Corresponds 1-1 with the incoming request entities


class OnCollide(StrEnum):
    """For certain batch operations that have a unique constraint - these options can be applied to define what should
    happen in the event of a collision"""

    error = "error"  # DEFAULT - Abort the entire operation - nothing will be written to the DB
    ignore = "ignore"  # Skip (don't insert) any colliding entities - all other entities will still be inserted
    cancel = "cancel"  # Cancel (archive/delete) any colliding entities before inserting the new entities


class BatchCreateCollidableResponse(BaseModel):
    """Similar to BatchCreateResponse but for when OnCollide methods are in use"""

    on_collide: OnCollide  # The option for on_collide that was used when generating this response
    ids: list[
        int | None
    ]  # Corresponds 1-1 with the incoming request entities - None means ignore was used and that entry was NOT inserted
