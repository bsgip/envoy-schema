from typing import Optional

from pydantic_xml import element

from envoy_schema.server.schema.sep2 import base
from envoy_schema.server.schema.sep2.identification import Link


class ConnectionPointLink(Link, ns="csipaus"):
    pass


class ConnectionPointRequest(base.BaseXmlModelWithNS, tag="ConnectionPoint", ns="csipaus"):
    """Contains identification information related to the network location at which the EndDevice is installed."""

    id: Optional[str] = element(default=None)  # Typically used as the NMI


class ConnectionPointResponse(base.BaseXmlModelWithNS, tag="ConnectionPoint", ns="csipaus"):
    """Contains identification information related to the network location at which the EndDevice is installed."""

    id: Optional[str] = element(default=None)  # Typically used as the NMI
