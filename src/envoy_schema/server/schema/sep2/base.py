from pydantic_xml import BaseXmlModel
from pydantic_xml.element import SearchMode

nsmap = {
    "": "urn:ieee:std:2030.5:ns",
    "csipaus": "https://csipaus.org/ns",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}


class BaseXmlModelWithNS(BaseXmlModel):
    model_config = {"arbitrary_types_allowed": True}

    def __init_subclass__(
        cls,
        *args,
        **kwargs,
    ):
        super().__init_subclass__(*args, **kwargs)
        cls.__xml_nsmap__ = nsmap
        cls.__xml_search_mode__ = SearchMode.UNORDERED
