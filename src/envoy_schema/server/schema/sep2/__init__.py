"""Schemas representing IEEE 2030.5 (smart energy profile 2)"""

from pydantic_xml import BaseXmlModel


def to_xml(entity: BaseXmlModel) -> str:
    """Quick utility for converting a pydantic-xml instance to an XML string"""

    raw = entity.to_xml(skip_empty=False, exclude_none=True, exclude_unset=True)
    if isinstance(raw, bytes):
        return raw.decode()
    else:
        return raw


def to_validated_xml(t: type[BaseXmlModel], opts: dict) -> str:
    """Quick utility for calling the pydantic xml 'model_validate' on a new instance of the specified type and returning
    the generated XML"""

    return to_xml(t.model_validate(opts))
