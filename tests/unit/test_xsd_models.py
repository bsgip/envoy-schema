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
from envoy_schema.server.schema.sep2.pricing import RateComponentListResponse
from envoy_schema.server.schema.sep2.types import DateTimeIntervalType
from envoy_schema.server.schema.sep2.error import ErrorResponse
from envoy_schema.server.schema.sep2.der import DERCapability

from envoy_schema.server.schema.sep2.metering_mirror import MirrorMeterReadingListRequest
from envoy_schema.server.schema.sep2.pub_sub import NotificationResourceCombined, NotificationListResponse, Notification


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
    # Notes for later:
    # BaseXmlModelWithNS is not part of the 2030.5 framework
    # ConnectionPointRequest has differences between the csipaus311 and 311a frameworks which will both be supported
    # DERCapability is made subscribable intentionally differing from the framework, same for RateComponentListResponse
    # NotificationResourceCombined is a pydantic workaround, which affects NotificationListResponse and Notification
    # DateTimeIntervalType skipped as only used as a sub-class for other classes, will never be instantiated by itself.
    # MirrorMeterReadingListRequest intentionally differs to remove unnecessary info
    # ErrorResponse has an additional item in it
    for skip_classes in [
        BaseXmlModelWithNS,
        ConnectionPointRequest,
        DERCapability,
        RateComponentListResponse,
        NotificationResourceCombined,
        NotificationListResponse,
        Notification,
        DateTimeIntervalType,
        MirrorMeterReadingListRequest,
        ErrorResponse,
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
