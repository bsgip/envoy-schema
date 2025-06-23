import pydantic
import datetime as dt

from . import base


class CertificateResponse(pydantic.BaseModel):
    """Represents a specific certificate registered in the utility server"""

    certificate_id: int
    created: dt.datetime
    lfdi: str
    expiry: dt.datetime


class CertificatePageResponse(base.BasePageModel):
    """Represents a paginated response of certificates"""

    certificates: list[CertificateResponse]
