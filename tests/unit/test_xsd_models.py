from typing import Any, Optional
import pytest
import inspect
import importlib
import pkgutil
from assertical.fake.generator import generate_class_instance, register_value_generator
from lxml import etree
from itertools import product
from pydantic_xml.model import XmlModelMeta
from envoy_schema.server.schema.sep2.base import BaseXmlModelWithNS
from envoy_schema.server.schema.csip_aus.connection_point import ConnectionPointRequest

# imports for asserticle generator override
from envoy_schema.server.schema.sep2.primitive_types import (
    HexBinary8,
    HexBinary16,
    HexBinary32,
    HexBinary48,
    HexBinary64,
    HexBinary128,
    HexBinary160,
)
from envoy_schema.server.schema.sep2.der import (
    DERControlResponse,
    ConnectStatusTypeValue,
    DERStatus,
    DERCapability,
    DERSettings,
)
from envoy_schema.server.schema.sep2.end_device import AbstractDevice
from envoy_schema.server.schema.sep2.identification import (
    RespondableResource,
    RespondableSubscribableIdentifiedObject,
    IdentifiedObject,
    SubscribableIdentifiedObject,
)
from envoy_schema.server.schema.sep2.metering_mirror import MirrorUsagePoint
from envoy_schema.server.schema.sep2.metering import ReadingBase, Reading
from envoy_schema.server.schema.sep2.pub_sub import NotificationResourceCombined


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
    use_assertical_extensions,
):
    # Skip some classes which require individual handling for various reasons
    for skip_classes in [
        BaseXmlModelWithNS,
        ConnectionPointRequest,
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

    xml = entity.to_xml(skip_empty=True).decode()
    xml_doc = etree.fromstring(xml)

    is_valid = csip_aus_schema.validate(xml_doc)
    errors = "\n".join((f"{e.line}: {e.message}" for e in csip_aus_schema.error_log))
    assert is_valid, f"{xml}\nErrors:\n{errors}"
