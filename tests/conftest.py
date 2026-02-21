import pytest
from assertical.fake.generator import register_value_generator
from assertical.fixtures.generator import generator_registry_snapshot
from lxml import etree

from envoy_schema.server.schema.sep2.identification import Link, ListLink


class LocalXsdResolver(etree.Resolver):
    """Finds specific XSD files in our test XSD repository"""

    def resolve(self, url, id, context):
        if url == "sep.xsd":
            return self.resolve_filename("tests/xsd/sep.xsd", context)
        elif url == "csipaus-core.xsd":
            return self.resolve_filename("tests/xsd/csipaus-core.xsd", context)
        elif url == "csipaus-core-v1.3.xsd":
            return self.resolve_filename("tests/xsd/csipaus-core-v1.3.xsd", context)
        elif url == "csipaus-ext-v1.3.xsd":
            return self.resolve_filename("tests/xsd/csipaus-ext-v1.3.xsd", context)
        elif url == "csipaus-ext.xsd":
            return self.resolve_filename("tests/xsd/csipaus-ext.xsd", context)
        return None


def load_xml_schema(csip_aus_core_path: str) -> etree.XMLSchema:
    # Register the custom resolver
    parser = etree.XMLParser(load_dtd=True)
    parser.resolvers.add(LocalXsdResolver())
    # Load schema
    with open(csip_aus_core_path, "r") as fp:
        xsd_content = fp.read()
    schema_root = etree.XML(xsd_content, parser)
    return etree.XMLSchema(schema_root)


@pytest.fixture
def csip_aus_v12_schema() -> etree.XMLSchema:
    """Yields a etree.XMLSchema that's loaded with the CSIP Aus XSD document (which incorporates sep2)"""
    return load_xml_schema("tests/xsd/csipaus-core-v1.2.xsd")


@pytest.fixture
def csip_aus_v13_schema() -> etree.XMLSchema:
    """Yields a etree.XMLSchema that's loaded with the CSIP Aus XSD document (which incorporates sep2)"""
    return load_xml_schema("tests/xsd/csipaus-core-v1.3.xsd")


@pytest.fixture
def use_assertical_extensions():
    """If enabled - loads ASSERTICAL_EXTENSIONS into the primitive generators in assertical"""
    with generator_registry_snapshot():
        register_value_generator(Link, lambda seed: Link(type=None, href=f"/link/{seed}"))
        register_value_generator(ListLink, lambda seed: ListLink(type=None, href=f"/listlink/{seed}"))
        yield
