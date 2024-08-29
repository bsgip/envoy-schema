import pytest
import inspect
import importlib
import pkgutil
import pydantic_xml
from itertools import product
from assertical.fake.generator import generate_class_instance
from lxml import etree


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
                    classes_list.append(obj)
        except Exception as e:
            print(f"Failed to import module {module_name}: {e}")

    return classes_list


def true_false_tuple(class_list: list) -> list[tuple[str, bool]]:
    """Create list of tuples where optional_is_none provides either True or False values to the fixture"""
    pairs = [[(item, True), (item, False)] for item in class_list]
    return list(product(*pairs))


@pytest.mark.parametrize("xml_class", import_all_classes_from_module("envoy_schema.server.schema"))
def test_validate_xml_model_csip_aus(xml_class: type, csip_aus_schema: etree.XMLSchema, use_assertical_extensions):
    # Generate XML string
    entity: xml_class = generate_class_instance(
        xml_class,
        optional_is_none=True,
        type=None,
    )

    xml = entity.to_xml(skip_empty=True).decode()
    xml_doc = etree.fromstring(xml)

    is_valid = csip_aus_schema.validate(xml_doc)
    errors = "\n".join((f"{e.line}: {e.message}" for e in csip_aus_schema.error_log))
    assert is_valid, f"{xml}\nErrors:\n{errors}"


# Screwing around:
# class_list = import_all_classes_from_module("envoy_schema.server.schema")
# print((class_list[0]))

# print(class_list[1].__class__)

# for xml_class in class_list:
#     # Filter for only xml models (not enum, flag etc)
#     if issubclass(xml_class.__class__, pydantic_xml.model.XmlModelMeta):
#         ns = xml_class.__xml_ns__
#         if ns is not None:
#             print(ns)
#         else:
#             print(xml_class.__xml_nsmap__)
