from typing import Optional

from pydantic_xml import element

from envoy_schema.server.schema.sep2 import base
from envoy_schema.server.schema.sep2.identification import Link


class ConnectionPointLink(Link, ns="csipaus"):
    pass


class ConnectionPointRequest(base.BaseXmlModelWithNS, tag="ConnectionPoint", ns="csipaus"):
    """Contains identification information related to the network location at which the EndDevice is installed."""

    id_v11: Optional[str] = element(default=None, tag="id")  # Typically used as the NMI (legacy version for csip1.1)
    id: Optional[str] = element(default=None, tag="connectionPointId")  # Typically used as the NMI (valid from 1.1a)


class ConnectionPointResponse(base.BaseXmlModelWithNS, tag="ConnectionPoint", ns="csipaus"):
    """Contains identification information related to the network location at which the EndDevice is installed."""

    id: str = element(default=None, tag="connectionPointId")  # Typically used as the NMI (valid from 1.1a)
