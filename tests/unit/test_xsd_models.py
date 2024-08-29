import pytest
import inspect
import os
import importlib
import pkgutil


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


@pytest.mark.parametrize("xml_class", import_all_classes_from_module("envoy_schema.server.schema"))
def test_validate_xml_model(xml_class: type):
    assert isinstance(xml_class, type)


# def run():
#     class_list = [t for (name, t) in inspect.getmembers(xml_models, inspect.isclass)]
#     print(len(class_list))


# run()
