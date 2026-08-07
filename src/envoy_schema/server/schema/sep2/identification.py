from pydantic_xml import attr, element

from envoy_schema.server.schema.sep2 import base, primitive_types, types


class Resource(base.BaseXmlModelWithNS):
    type: str | None = attr(ns="xsi", default=None)
    href: str | None = attr(default=None)


class IdentifiedObject(Resource):
    mRID: primitive_types.HexBinary128 = element()
    description: str | None = element(default=None)
    version: types.VersionType | None = element(default=None)


class SubscribableResource(Resource):
    subscribable: types.SubscribableType | None = attr(default=None)


class SubscribableList(SubscribableResource):
    """A List to which a Subscription can be requested."""

    all_: int = attr(name="all")  # The number specifying "all" of the items in the list. Required on GET
    results: int = attr()  # Indicates the number of items in this page of results.


class SubscribableIdentifiedObject(SubscribableResource):
    mRID: primitive_types.HexBinary128 = element()  # The global identifier of the object
    description: str | None = element(
        default=None
    )  # The description is a human readable text describing or naming the object.
    version: types.VersionType | None = element(default=None)  # Contains the version number of the object.


class RespondableResource(Resource):
    """A Resource to which a Response can be requested."""

    replyTo: str | None = attr(default=None)
    responseRequired: primitive_types.HexBinary8 | None = attr(default=00)


class RespondableSubscribableIdentifiedObject(RespondableResource):
    """An IdentifiedObject to which a Response can be requested."""

    mRID: primitive_types.HexBinary128 = element()
    description: str | None = element(default=None)
    version: types.VersionType | None = element(default=None)
    subscribable: types.SubscribableType | None = attr(default=None)


class List(Resource):
    """Container to hold a collection of object instances or references. See Design Pattern section for additional
    details."""

    all_: int = attr(name="all")  # The number specifying "all" of the items in the list. Required on GET
    results: int = attr()  # Indicates the number of items in this page of results.


class Link(base.BaseXmlModelWithNS):
    href: str = attr()


class ListLink(Link):
    all_: int | None = attr(name="all", default=None)
