from typing import Any, Generator
import pytest
import inspect
import importlib
import pkgutil
from assertical.fake.generator import (
    generate_class_instance,
    register_value_generator,
    enumerate_class_properties,
    generate_value,
    CollectionType,
    BASE_CLASS_PUBLIC_MEMBERS,
)
from lxml import etree
from itertools import product
from pydantic_xml.model import XmlModelMeta
from envoy_schema.server.schema.sep2.base import BaseXmlModelWithNS
from envoy_schema.server.schema.csip_aus.connection_point import ConnectionPointRequest
from envoy_schema.server.schema.sep2.metering import Reading, ReadingListResponse
from envoy_schema.server.schema.sep2.pricing import RateComponentListResponse, TimeTariffIntervalListResponse
from envoy_schema.server.schema.sep2.types import DateTimeIntervalType
from envoy_schema.server.schema.sep2.error import ErrorResponse
from envoy_schema.server.schema.sep2.der import (
    DERAvailability,
    DERCapability,
    DERControlListResponse,
    DERSettings,
    DERStatus,
    DefaultDERControl,
)
from envoy_schema.server.schema.sep2.end_device import EndDeviceListResponse, EndDeviceRequest

from envoy_schema.server.schema.sep2.metering_mirror import MirrorMeterReadingListRequest
from envoy_schema.server.schema.sep2.pub_sub import (
    XSI_TYPE_DEFAULT_DER_CONTROL,
    XSI_TYPE_DER_AVAILABILITY,
    XSI_TYPE_DER_CAPABILITY,
    XSI_TYPE_DER_CONTROL_LIST,
    XSI_TYPE_DER_SETTINGS,
    XSI_TYPE_DER_STATUS,
    XSI_TYPE_END_DEVICE_LIST,
    XSI_TYPE_READING_LIST,
    XSI_TYPE_TIME_TARIFF_INTERVAL_LIST,
    NotificationResourceCombined,
    NotificationListResponse,
    Notification,
)
from envoy_schema.server.schema.sep2.identification import Resource, SubscribableIdentifiedObject, List


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


@pytest.fixture
def custom_assertical_registrations(csip_aus_schema):
    # Circumvent issues with assertical generating invalid Int8, Uint8 etc values and hexbinary (str subclass)
    register_value_generator(int, lambda x: x % 64)  # This will be unwound due to dep on use_assertical_extensions
    register_value_generator(
        str, lambda x: f"{x % 256:02x}"
    )  # This will be unwound due to dep on use_assertical_extensions


# Main test against almost all xsd schema models with a few exceptions treated below
@pytest.mark.parametrize(
    "xml_class, optional_is_none", product(import_all_classes_from_module("envoy_schema.server.schema"), [True, False])
)
def test_validate_xml_model_csip_aus(
    xml_class: type,
    csip_aus_schema: etree.XMLSchema,
    custom_assertical_registrations,
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
    """Perform setup of xml by generating class instance, converting to xml and validating against the schema.
    Returns is_valid: bool and errors: str as a tuple."""

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
    support for pydantic discriminated unions, here NotificationResourceCombined is not tested, simply set to a
    valid value (None)"""

    # Generate XML string
    entity: Notification = generate_class_instance(
        t=Notification, optional_is_none=optional_is_none, generate_relationships=True
    )
    # Set resource to None to
    entity.resource = None

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
    support for pydantic discriminated unions. The test is very simple as it is a single element only"""
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


@pytest.mark.parametrize(
    "sub_type, xsi_type",
    [
        (TimeTariffIntervalListResponse, XSI_TYPE_TIME_TARIFF_INTERVAL_LIST),
        (EndDeviceListResponse, XSI_TYPE_END_DEVICE_LIST),
        (DERControlListResponse, XSI_TYPE_DER_CONTROL_LIST),
        (ReadingListResponse, XSI_TYPE_READING_LIST),
        (DefaultDERControl, XSI_TYPE_DEFAULT_DER_CONTROL),
        (DERStatus, XSI_TYPE_DER_STATUS),
        (DERAvailability, XSI_TYPE_DER_AVAILABILITY),
        (DERCapability, XSI_TYPE_DER_CAPABILITY),
        (DERSettings, XSI_TYPE_DER_SETTINGS),
    ],
)
def test_NotificationResourceCombined(
    csip_aus_schema: etree.XMLSchema, sub_type: type, xsi_type: str, custom_assertical_registrations
):

    # There are a ton sub_types that have been munged together into NotificationResourceCombined (see comments on type)
    # This will generate ONLY the subtype specific properties and assign them into NotificationResourceCombined
    # in an effort to simplify the generation (and guard against future property changes)
    kvps: dict[str, Any] = {}
    for p in enumerate_class_properties(sub_type):

        if p.is_primitive_type:
            kvps[p.name] = generate_value(p.type_to_generate)
        else:
            val = generate_class_instance(t=p.type_to_generate, generate_relationships=True)
            if p.collection_type in [CollectionType.REQUIRED_LIST, CollectionType.OPTIONAL_LIST]:
                # If we have a list - turn it into a list
                val = [val]
            elif p.collection_type is not None:
                raise NotImplementedError(f"Haven't added support in this test for {p.collection_type}")
            kvps[p.name] = val

    # Subscribable on DERCap was something unique to this implementation - it's not in the standard
    # but was added because it was a nice feature - here we unpick it so we can XSD validate
    if sub_type == DERCapability:
        del kvps["subscribable"]

    resource: NotificationResourceCombined = generate_class_instance(
        NotificationResourceCombined, optional_is_none=True, **kvps
    )

    entity: Notification = generate_class_instance(Notification, seed=201, optional_is_none=True, resource=resource)

    xml = entity.to_xml(skip_empty=False, exclude_none=True, exclude_unset=True).decode()

    # Getting xsi:type set via assertical is painful because the "type" property exists on pydantic_xml BUT isn't
    # visible to assertical. We also can't set the type property at runtime (or haven't figured out a way)
    # so now we just munge the xsi:type into the generated XML

    xml = xml.replace("<Resource href=", f'<Resource xsi:type="{xsi_type}" href=')
    xml_doc = etree.fromstring(xml)

    is_valid = csip_aus_schema.validate(xml_doc)
    errors = "\n".join((f"{e.line}: {e.message}" for e in csip_aus_schema.error_log))
    assert is_valid, f"{xml}\nErrors:\n{errors}"
