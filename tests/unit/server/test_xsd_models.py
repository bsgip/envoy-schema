import importlib
import inspect
import pkgutil
import re
from itertools import product
from typing import Any

import pytest
from assertical.fake.generator import (
    CollectionType,
    enumerate_class_properties,
    generate_class_instance,
    generate_value,
    register_value_generator,
)
from lxml import etree
from pydantic_xml import BaseXmlModel
from pydantic_xml.model import XmlModelMeta

from envoy_schema.server.schema.csip_aus.connection_point import ConnectionPointRequest
from envoy_schema.server.schema.sep2.base import BaseXmlModelWithNS
from envoy_schema.server.schema.sep2.der import (
    DefaultDERControl,
    DERAvailability,
    DERCapability,
    DERControlListResponse,
    DERProgramListResponse,
    DERSettings,
    DERStatus,
)
from envoy_schema.server.schema.sep2.end_device import EndDeviceListResponse, EndDeviceRequest
from envoy_schema.server.schema.sep2.error import ErrorResponse
from envoy_schema.server.schema.sep2.function_set_assignments import FunctionSetAssignmentsListResponse
from envoy_schema.server.schema.sep2.metering import ReadingListResponse
from envoy_schema.server.schema.sep2.metering_mirror import MirrorMeterReadingListRequest
from envoy_schema.server.schema.sep2.pricing import RateComponentListResponse, TimeTariffIntervalListResponse
from envoy_schema.server.schema.sep2.pub_sub import (
    XSI_TYPE_DEFAULT_DER_CONTROL,
    XSI_TYPE_DER_AVAILABILITY,
    XSI_TYPE_DER_CONTROL_LIST,
    XSI_TYPE_DER_PROGRAM_LIST,
    XSI_TYPE_DER_SETTINGS,
    XSI_TYPE_DER_STATUS,
    XSI_TYPE_END_DEVICE_LIST,
    XSI_TYPE_FUNCTION_SET_ASSIGNMENTS_LIST,
    XSI_TYPE_READING_LIST,
    XSI_TYPE_TIME_TARIFF_INTERVAL_LIST,
    Notification,
    NotificationListResponse,
    NotificationResourceCombined,
)


def import_all_classes_from_module(package_name: str) -> list[type]:
    """Dynamically load all the classes from the specified module AND sub modules.
    Returns a list of classes"""
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
    """Assertical does not get passed the correct pydantic_xml types: e.g. Int8, Uint8, hexbinary will generate as
    integers only and cause type issues for xml validation. This overwrites these with valid generated values.
    This will be unwound due to dep on the use_assertical_extensions fixture (see conftest)."""
    register_value_generator(int, lambda x: x % 64)
    register_value_generator(
        str, lambda x: f"{x % 256:02x}"
    )  # This will be unwound due to dep on use_assertical_extensions


def generate_and_validate_xml(
    xml_class: type[BaseXmlModel],
    csip_aus_schema: etree.XMLSchema,
    optional_is_none: bool,
) -> tuple[bool, str]:
    """Generate class instances using assertical, convert to xml and then validate against csip_aus_schema which
    contains sep, csipaus-core and csipaus-ext xsd files."""
    # Generate XML string
    entity = generate_class_instance(
        t=xml_class,
        optional_is_none=optional_is_none,
        generate_relationships=True,
    )
    xml = entity.to_xml(skip_empty=False, exclude_none=True, exclude_unset=True).decode()

    # Getting xsi:type set via assertical is painful because the "type" property exists on pydantic_xml BUT isn't
    # visible to assertical. We also can't set the type property at runtime (or haven't figured out a way)
    # so now we just munge the xsi:type into the generated XML
    xml = re.sub('xsi:type="[^"]*"', "", xml)
    xml_doc = etree.fromstring(xml)

    # Validate
    is_valid = csip_aus_schema.validate(xml_doc)
    errors = "\n".join((f"{e.line}: {e.message}" for e in csip_aus_schema.error_log))
    return is_valid, errors


# Main test against almost all xsd schema models with a few exceptions treated below
@pytest.mark.parametrize(
    "xml_class, optional_is_none", product(import_all_classes_from_module("envoy_schema.server.schema"), [True, False])
)
def test_all_xml_models_csip_aus(
    xml_class: type[BaseXmlModel],
    csip_aus_schema: etree.XMLSchema,
    custom_assertical_registrations,
    optional_is_none: bool,
):
    """Generate class instances using assertical, convert to xml and then validate against csip_aus_schema which
    contains sep, csipaus-core and csipaus-ext xsd files"""

    # Skip some classes which require individual handling for various reasons (separate tests provided where needed)
    for skip_classes in [
        BaseXmlModelWithNS,  # Not necessary to xsd validate.
        ConnectionPointRequest,  # Not necessary to xsd validate, but supports both csipaus311 and 311a.
        RateComponentListResponse,  # See separate test below, is also made subscribable.
        NotificationResourceCombined,  # Separate test below, this pydantic workaround affects two classes below.
        NotificationListResponse,  # See separate test below.
        Notification,  # See separate test below.
        MirrorMeterReadingListRequest,  # Not necessary to xsd validate.
        ErrorResponse,  # See separate test below, intentionally removes unnecessary information.
        EndDeviceRequest,  # Not necessary to xsd validate, is not generated, only sent by clients.
    ]:
        if xml_class is skip_classes:
            return

    is_valid, errors = generate_and_validate_xml(
        xml_class=xml_class,
        csip_aus_schema=csip_aus_schema,
        optional_is_none=optional_is_none,
    )

    assert is_valid, errors


@pytest.mark.parametrize("optional_is_none", [True, False])
def test_error_response_xsd(csip_aus_schema: etree.XMLSchema, optional_is_none: bool, custom_assertical_registrations):
    """Test ErrorResponse separately as an additional optional element (message) causes xsd validation issues"""
    is_valid, errors = generate_and_validate_xml(
        xml_class=ErrorResponse,
        csip_aus_schema=csip_aus_schema,
        optional_is_none=optional_is_none,
    )

    # ErrorResponse passes validation where True as the xsd addition is optional
    if optional_is_none is True:
        assert is_valid, errors
    # The only error should be that the message element is not expected.
    elif optional_is_none is False:
        assert errors == "1: Element '{urn:ieee:std:2030.5:ns}message': This element is not expected."


@pytest.mark.parametrize("optional_is_none", [True, False])
def test_RateComponentListResponse_xsd(
    csip_aus_schema: etree.XMLSchema, optional_is_none: bool, custom_assertical_registrations
):
    """Test RateComponentListResponse separately as it is intentionally a subscribable resource rather than
    simply a resource"""

    is_valid, errors = generate_and_validate_xml(
        xml_class=RateComponentListResponse,
        csip_aus_schema=csip_aus_schema,
        optional_is_none=optional_is_none,
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
    # These steps are common with the generate_and_validate_xml function but sets a resource to none prior to xml
    # conversion

    entity: Notification = generate_class_instance(
        t=Notification, optional_is_none=optional_is_none, generate_relationships=True
    )
    # Set resource to None to leave that aspects checking to another test
    entity.resource = None

    xml = entity.to_xml(skip_empty=False, exclude_none=True, exclude_unset=True).decode()
    xml = re.sub('xsi:type="[^"]*"', "", xml)
    xml_doc = etree.fromstring(xml)

    is_valid = csip_aus_schema.validate(xml_doc)
    errors = "\n".join((f"{e.line}: {e.message}" for e in csip_aus_schema.error_log))
    assert is_valid, f"{xml}\nErrors:\n{errors}"


@pytest.mark.parametrize("optional_is_none", [True, False])
def test_NotificationListResponse_xsd(
    optional_is_none: bool,
):
    """NotificationListResponse contains NotificationResourceCombined which only exists because pydantic-xml has limited
    support for pydantic discriminated unions. The test is very simple as it is a single element only, but cannot use
    the xsd validation function, so requires more manual matches."""
    # Generate XML string
    entity: NotificationListResponse = generate_class_instance(
        t=NotificationListResponse, optional_is_none=optional_is_none, generate_relationships=True
    )

    xml = entity.to_xml(skip_empty=False, exclude_none=True, exclude_unset=True).decode()
    xml = re.sub('xsi:type="[^"]*"', "", xml)
    assert (
        '<NotificationList xmlns="urn:ieee:std:2030.5:ns" xmlns:csipaus="https://csipaus.org/ns" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
    ) in xml
    assert "all=" in xml
    assert "results=" in xml

    # Check Notification is included as an optional element
    if optional_is_none is True:
        assert "</Notification>" not in xml
        assert "</NotificationList>" not in xml
    else:
        assert "</Notification></NotificationList>" in xml


def notification_resource_combined_parameters() -> list[tuple[type, str, bool]]:
    """Used to flatten the product of classes, xsi_types and optional_is_none values to pass to
    test_NotificationResourceCombined"""
    classes_list = [
        (TimeTariffIntervalListResponse, XSI_TYPE_TIME_TARIFF_INTERVAL_LIST),
        (EndDeviceListResponse, XSI_TYPE_END_DEVICE_LIST),
        (DERControlListResponse, XSI_TYPE_DER_CONTROL_LIST),
        (ReadingListResponse, XSI_TYPE_READING_LIST),
        (DefaultDERControl, XSI_TYPE_DEFAULT_DER_CONTROL),
        (DERStatus, XSI_TYPE_DER_STATUS),
        (DERAvailability, XSI_TYPE_DER_AVAILABILITY),
        (DERSettings, XSI_TYPE_DER_SETTINGS),
        (DERProgramListResponse, XSI_TYPE_DER_PROGRAM_LIST),
        (FunctionSetAssignmentsListResponse, XSI_TYPE_FUNCTION_SET_ASSIGNMENTS_LIST),
    ]
    bools = [True, False]
    return [(elem1, elem2, boolean) for (elem1, elem2) in classes_list for boolean in bools]


@pytest.mark.parametrize("sub_type, xsi_type, optional_is_none", notification_resource_combined_parameters())
def test_NotificationResourceCombined(
    sub_type: type,
    xsi_type: str,
    optional_is_none: bool,
    csip_aus_schema: etree.XMLSchema,
    custom_assertical_registrations,
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

    resource: NotificationResourceCombined = generate_class_instance(
        NotificationResourceCombined, optional_is_none=True, **kvps
    )

    entity: Notification = generate_class_instance(Notification, seed=201, optional_is_none=True, resource=resource)

    xml = entity.to_xml(skip_empty=False, exclude_none=True, exclude_unset=True).decode()

    # Getting xsi:type set via assertical is painful because the "type" property exists on pydantic_xml BUT isn't
    # visible to assertical. We also can't set the type property at runtime (or haven't figured out a way)
    # so now we just munge the xsi:type into the generated XML
    xml = re.sub('xsi:type="[^"]*" *', "", xml)
    xml = xml.replace("<Resource href=", f'<Resource xsi:type="{xsi_type}" href=')

    xml_doc = etree.fromstring(xml)
    is_valid = csip_aus_schema.validate(xml_doc)
    errors = "\n".join((f"{e.line}: {e.message}" for e in csip_aus_schema.error_log))
    assert is_valid, f"{xml}\nErrors:\n{errors}"


def test_hexbinary_doe_types():
    """
    Manual check that some hexbinary types are set as hexbinary. Easy to miss due to necessary assertical overrides
    """
    class_values = [
        (DERSettings, "modesEnabled"),
        (DERSettings, "doeModesEnabled"),
        (DERCapability, "modesSupported"),
        (DERCapability, "doeModesSupported"),
    ]

    for xml_class, value in class_values:
        # This is a workaround to identify an annotated type that uses one of our validate_HexBinaryXXX funcs
        value_type = xml_class.__annotations__.get(value)
        assert "HexBinary" in str(value_type), f"Expected a HexBinary type in {value} of the {xml_class}"

        # Additional check for NotificationResourceCombined
        notification_value = NotificationResourceCombined.__annotations__.get(value)
        assert "HexBinary" in str(
            notification_value
        ), f"Expected HexBinary type in {value} of NotificationResourceCombined"
