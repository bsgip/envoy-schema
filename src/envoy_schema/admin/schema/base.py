from pydantic import BaseModel


class BasePageModel(BaseModel):
    total_count: int  # The total number of objects (independent of this page of results)
    limit: int  # The maximum number of objects that could've been returned (the limit set by the query)
    start: int  # The number of objects that have been skipped as part of this query (the start set by the query)
