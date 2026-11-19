from pydantic_xml import element

from envoy_schema.server.schema.sep2 import base, types


class ErrorResponse(base.BaseXmlModelWithNS, tag="Error"):
    """Represents a description of a request error and how the client should respond"""

    maxRetryDuration: int | None = element(
        default=None
    )  # Contains the number of seconds the client SHOULD wait before retrying
    reasonCode: types.ReasonCodeType = element()  # Code indicating the reason for failure.

    # These properties sit outside the sep2 definition and are our own custom extensions to provide clients
    # with some QoL improvements
    message: str | None = element(default=None)
