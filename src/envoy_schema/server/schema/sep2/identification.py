from typing import Optional

from pydantic_xml import attr, element

from envoy_schema.server.schema.sep2 import base, primitive_types, types


class Resource(base.BaseXmlModelWithNS):
    href: Optional[str] = attr(default=None)
    type: Optional[str] = attr(ns="xsi", default=None)


class IdentifiedObject(Resource):
    description: Optional[str] = element(default=None)
    mRID: types.mRIDType = element()
    version: Optional[types.VersionType] = element(default=None)


class SubscribableResource(Resource):
    subscribable: Optional[types.SubscribableType] = attr(default=None)


class SubscribableList(SubscribableResource):
    """A List to which a Subscription can be requested."""

    all_: int = attr(name="all")  # The number specifying "all" of the items in the list. Required on GET
    results: int = attr()  # Indicates the number of items in this page of results.


class SubscribableIdentifiedObject(SubscribableResource):
    description: Optional[str] = element(
        default=None
    )  # The description is a human readable text describing or naming the object.
    mRID: types.mRIDType = element()  # The global identifier of the object
    version: Optional[types.VersionType] = element(default=None)  # Contains the version number of the object.


class RespondableResource(Resource):
    """A Resource to which a Response can be requested."""

    replyTo: Optional[str] = attr(default=None)
    responseRequired: Optional[primitive_types.HexBinary32] = attr(default=None)


class RespondableSubscribableIdentifiedObject(RespondableResource):
    """An IdentifiedObject to which a Response can be requested."""

    subscribable: Optional[types.SubscribableType] = attr(default=None)

    description: Optional[str] = element(default=None)
    mRID: primitive_types.HexBinary128 = element()
    version: Optional[types.VersionType] = element(default=None)


class List(Resource):
    """Container to hold a collection of object instances or references. See Design Pattern section for additional
    details."""

    all_: int = attr(name="all")  # The number specifying "all" of the items in the list. Required on GET
    results: int = attr()  # Indicates the number of items in this page of results.


class Link(Resource):
    pass


class ListLink(Link):
    all_: Optional[int] = attr(name="all", default=None)
