from typing import Any
import pytest
import inspect
import importlib
import pkgutil
from assertical.fake.generator import generate_class_instance
from lxml import etree
from itertools import product
from pydantic_xml.model import XmlModelMeta


# imports for asserticle generator override
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


def import_all_classes_from_module(package_name: str) -> dict:
    """Dynamically load all the classes from the specified module AND sub modules! Returns a list.
    Used for testing purposes."""
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


ASSERTICAL_PROPERTY_OVERRIDES: dict[tuple[type, str], Any] = {
    (DERControlResponse, "modesSupported"): "aa",
    (ConnectStatusTypeValue, "value"): "aa",
    (DERStatus, "alarmStatus"): "aa",
    (DERCapability, "modesSupported"): "aa",
    (DERSettings, "modesEnabled"): "aa",
    (AbstractDevice, "deviceCategory"): "aa",
    (AbstractDevice, "lFDI"): "aa",
    (RespondableResource, "responseRequired"): "aa",
    (RespondableSubscribableIdentifiedObject, "mRID"): "aa",
    (MirrorUsagePoint, "deviceLFDI"): "aa",
    (ReadingBase, "qualityFlags"): "aa",
    (Reading, "localID"): "aa",
    (NotificationResourceCombined, "alarmStatus"): "aa",
    (NotificationResourceCombined, "modesSupported"): "aa",
    (NotificationResourceCombined, "modesEnabled"): "aa",
    (IdentifiedObject, "mRID"): "aa",
    (SubscribableIdentifiedObject, "mRID"): "aa",
    (NotificationResourceCombined, "mRID"): "aa",
}


def apply_assertical_overrides(entity: Any):
    """Applies the ASSERTICAL_PROPERTY_OVERRIDES dict values to a class. This is to circumvent the pydantic loss of
    type information: hexbinary is being represented as str by assertical, so is overriden here."""
    for type_in_hierarchy in inspect.getmro(type(entity)):
        for (cls_key, prop), value in ASSERTICAL_PROPERTY_OVERRIDES.items():
            if type_in_hierarchy is cls_key:
                if hasattr(entity, prop):
                    setattr(entity, prop, value)


@pytest.mark.parametrize(
    "xml_class, optional_is_none", product(import_all_classes_from_module("envoy_schema.server.schema"), [True, False])
)
def test_validate_xml_model_csip_aus(
    xml_class: type,
    csip_aus_schema: etree.XMLSchema,
    optional_is_none: bool,
    use_assertical_extensions,
):

    # Generate XML string
    entity: xml_class = generate_class_instance(
        t=xml_class, optional_is_none=optional_is_none, generate_relationships=True
    )
    # print(dir(entity))
    apply_assertical_overrides(entity)

    xml = entity.to_xml(skip_empty=True).decode()
    xml_doc = etree.fromstring(xml)

    is_valid = csip_aus_schema.validate(xml_doc)
    errors = "\n".join((f"{e.line}: {e.message}" for e in csip_aus_schema.error_log))
    assert is_valid, f"{xml}\nErrors:\n{errors}"
