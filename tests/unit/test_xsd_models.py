from typing import Any
import pytest
import inspect
import importlib
import pkgutil
from assertical.fake.generator import (
    generate_class_instance,
    register_value_generator,
    enumerate_class_properties,
    generate_value,
)
from lxml import etree
from itertools import product
from pydantic_xml.model import XmlModelMeta
from envoy_schema.server.schema.sep2.base import BaseXmlModelWithNS
from envoy_schema.server.schema.csip_aus.connection_point import ConnectionPointRequest
from envoy_schema.server.schema.sep2.pricing import RateComponentListResponse
from envoy_schema.server.schema.sep2.types import DateTimeIntervalType
from envoy_schema.server.schema.sep2.error import ErrorResponse
from envoy_schema.server.schema.sep2.der import DERCapability, DERStatus, DefaultDERControl
from envoy_schema.server.schema.sep2.end_device import EndDeviceRequest

from envoy_schema.server.schema.sep2.metering_mirror import MirrorMeterReadingListRequest
from envoy_schema.server.schema.sep2.pub_sub import NotificationResourceCombined, NotificationListResponse, Notification
from envoy_schema.server.schema.sep2.identification import Resource


def import_all_classes_from_module(package_name: str) -> list:
    """Dynamically load all the classes from the specified module AND sub modules. Returns a list."""
    classes_list = []

    package = importlib.import_module(package_name)

    # Traverse the package
    for _, module_name, _ in pkgutil.walk_packages(package.__path__, package_name + "."):
        # Exlude init files
        if module_name.endswith("__init__"):
            continue

        try:
            module = importlib.import_module(module_name)
            # Extract classes from the module
            for _, obj in inspect.getmembers(module, inspect.isclass):
                # Exclude built-in and internal classes
                if obj.__module__ == module_name:
                    # Filter out enum types, keep only xml models
                    if issubclass(obj.__class__, XmlModelMeta):
                        classes_list.append(obj)
        except Exception as e:
            print(f"Failed to import module {module_name}: {e}")

    return classes_list


@pytest.mark.parametrize(
    "xml_class, optional_is_none", product(import_all_classes_from_module("envoy_schema.server.schema"), [True, False])
)
def test_validate_xml_model_csip_aus(
    xml_class: type,
    csip_aus_schema: etree.XMLSchema,
    optional_is_none: bool,
):
    # Skip some classes which require individual handling for various reasons (separate tests provided where needed)

    # ConnectionPointRequest has differences between the csipaus311 and 311a frameworks which will both be supported
    # DERCapability is made subscribable intentionally differing from the framework, same for RateComponentListResponse
    # NotificationResourceCombined is a pydantic workaround, which affects NotificationListResponse and Notification
    # MirrorMeterReadingListRequest and EndDeviceRequest intentionally remove unnecessary information

    for skip_classes in [
        BaseXmlModelWithNS,  # Not necessary to xsd validate
        ConnectionPointRequest,  # Not necessary to xsd validate
        DERCapability,  # See Separate test below
        RateComponentListResponse,  # See Separate test below
        NotificationResourceCombined,
        NotificationListResponse,  # See Separate test below
        Notification,  # See Separate test below
        MirrorMeterReadingListRequest,  # Not necessary to xsd validate
        ErrorResponse,  # See Separate test below
        EndDeviceRequest,  # Not necessary to xsd validate, is not generated, only sent by clients
    ]:
        if xml_class is skip_classes:
            return

    # Circumvent issues with assertical generating invalid Int8, Uint8 etc values and hexbinary (str subclass)
    register_value_generator(int, lambda x: x % 64)  # This will be unwound due to dep on use_assertical_extensions
    register_value_generator(
        str, lambda x: f"{x % 256:02x}"
    )  # This will be unwound due to dep on use_assertical_extensions

    # Generate XML string
    entity: xml_class = generate_class_instance(
        t=xml_class, optional_is_none=optional_is_none, generate_relationships=True
    )

    xml = entity.to_xml(skip_empty=False, exclude_none=True, exclude_unset=True).decode()
    xml_doc = etree.fromstring(xml)

    is_valid = csip_aus_schema.validate(xml_doc)
    errors = "\n".join((f"{e.line}: {e.message}" for e in csip_aus_schema.error_log))
    assert is_valid, f"{xml}\nErrors:\n{errors}"


def generate_non_standard_xml_models(
    xml_class: type,
    csip_aus_schema: etree.XMLSchema,
    optional_is_none: bool,
) -> tuple[bool, str]:

    # Circumvent issues with assertical generating invalid Int8, Uint8 etc values and hexbinary (str subclass)
    register_value_generator(int, lambda x: x % 64)  # This will be unwound due to dep on use_assertical_extensions
    register_value_generator(
        str, lambda x: f"{x % 256:02x}"
    )  # This will be unwound due to dep on use_assertical_extensions

    # Generate XML string
    entity: xml_class = generate_class_instance(
        t=xml_class, optional_is_none=optional_is_none, generate_relationships=True
    )

    xml = entity.to_xml(skip_empty=False, exclude_none=True, exclude_unset=True).decode()
    xml_doc = etree.fromstring(xml)

    is_valid = csip_aus_schema.validate(xml_doc)
    errors = "\n".join((f"{e.line}: {e.message}" for e in csip_aus_schema.error_log))
    return is_valid, errors


@pytest.mark.parametrize("optional_is_none", [True, False])
def test_error_response_xsd(
    csip_aus_schema: etree.XMLSchema,
    optional_is_none: bool,
):
    """Test ErrorResponse separately as an additional optional element (message) causes xsd validation issues"""
    is_valid, errors = generate_non_standard_xml_models(
        xml_class=ErrorResponse, csip_aus_schema=csip_aus_schema, optional_is_none=optional_is_none
    )

    # ErrorResponse passes validation where True as the xsd addition is optional
    if optional_is_none is True:
        assert is_valid, errors
    # The only error should be that the message element is not expected.
    elif optional_is_none is False:
        assert errors == "1: Element '{urn:ieee:std:2030.5:ns}message': This element is not expected."


@pytest.mark.parametrize("optional_is_none", [True, False])
def test_DERCapability_xsd(
    csip_aus_schema: etree.XMLSchema,
    optional_is_none: bool,
):
    """Test DERCapability separately as it is intentionally a subscribable resource rather than simply a resource"""

    is_valid, errors = generate_non_standard_xml_models(
        xml_class=DERCapability, csip_aus_schema=csip_aus_schema, optional_is_none=optional_is_none
    )

    # if optional_is_none is True there should be no difference from the schema (subscribable is optional)
    if optional_is_none is True:
        assert is_valid, errors

    # The only issue should be an error about the subscribable definition
    if optional_is_none is False:
        assert errors == (
            "1: Element '{urn:ieee:std:2030.5:ns}DERCapability', attribute 'subscribable': "
            "The attribute 'subscribable' is not allowed."
        )


@pytest.mark.parametrize("optional_is_none", [True, False])
def test_RateComponentListResponse_xsd(
    csip_aus_schema: etree.XMLSchema,
    optional_is_none: bool,
):
    """Test RateComponentListResponse separately as it is intentionally a subscribable resource rather than
    simply a resource"""

    is_valid, errors = generate_non_standard_xml_models(
        xml_class=RateComponentListResponse, csip_aus_schema=csip_aus_schema, optional_is_none=optional_is_none
    )

    # if optional_is_none is True there should be no difference from the schema (subscribable is optional)
    if optional_is_none is True:
        assert is_valid, errors

    # The only issue should be an error about the subscribable definition
    if optional_is_none is False:
        print(errors)
        assert errors == (
            "1: Element '{urn:ieee:std:2030.5:ns}RateComponentList', attribute 'subscribable': "
            "The attribute 'subscribable' is not allowed."
        )


@pytest.mark.parametrize("optional_is_none", [True, False])
def test_Notification_xsd(
    csip_aus_schema: etree.XMLSchema,
    optional_is_none: bool,
):
    """Notification contains NotificationResourceCombined which only exists because pydantic-xml has limited
    support for pydantic discriminated unions, here NotificationResourceCombined is not testsed, simply set to a
    valid value"""

    # Generate XML string
    entity: Notification = generate_class_instance(
        t=Notification, optional_is_none=optional_is_none, generate_relationships=True
    )
    # Set 'href' to "04" and delete all other attributes from 'resource'
    entity.resource = NotificationResourceCombined(href="04")

    xml = entity.to_xml(skip_empty=False, exclude_none=True, exclude_unset=True).decode()
    xml_doc = etree.fromstring(xml)

    is_valid = csip_aus_schema.validate(xml_doc)
    errors = "\n".join((f"{e.line}: {e.message}" for e in csip_aus_schema.error_log))
    assert is_valid, f"{xml}\nErrors:\n{errors}"


@pytest.mark.parametrize("optional_is_none", [True, False])
def test_NotificationListResponse_xsd(
    optional_is_none: bool,
):
    """NotificationListResponse contains NotificationResourceCombined which only exists because pydantic-xml has limited
    support for pydantic discriminated unions"""
    # Generate XML string
    entity: NotificationListResponse = generate_class_instance(
        t=NotificationListResponse, optional_is_none=optional_is_none, generate_relationships=True
    )

    xml = entity.to_xml(skip_empty=False, exclude_none=True, exclude_unset=True).decode()

    assert (
        '<NotificationList xmlns="urn:ieee:std:2030.5:ns" xmlns:csipaus="https://csipaus.org/ns" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" href="'
    ) in xml
    assert "all=" in xml
    assert "results=" in xml

    # Check notification is included as an optional element, but not its contents
    if optional_is_none is True:
        assert "</Notification>" not in xml
        assert "</NotificationList>" not in xml
    else:
        assert "</Notification></NotificationList>" in xml


@pytest.mark.parametrize("sub_type", [DERCapability, DefaultDERControl, DERStatus])
def test_NotificationResourceCombined(csip_aus_schema, sub_type: type):
    NotificationResourceCombined
    kvps: dict[str, Any] = {}
    for p in enumerate_class_properties(sub_type):
        kvps[p.name] = (
            generate_value(p.type_to_generate) if p.is_primitive_type else generate_class_instance(p.type_to_generate)
        )

    resource: NotificationResourceCombined = generate_class_instance(
        NotificationResourceCombined, optional_is_none=True, **kvps
    )
    entity: Notification = generate_class_instance(Notification, optional_is_none=True, resource=resource)

    xml = entity.to_xml(skip_empty=False, exclude_none=True, exclude_unset=True).decode()
    xml_doc = etree.fromstring(xml)

    is_valid = csip_aus_schema.validate(xml_doc)
    errors = "\n".join((f"{e.line}: {e.message}" for e in csip_aus_schema.error_log))
    assert is_valid, f"{xml}\nErrors:\n{errors}"
