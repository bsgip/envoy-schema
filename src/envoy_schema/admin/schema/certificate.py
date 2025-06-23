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


class CertificateRequest(pydantic.BaseModel):
    """Represents a specific certificate to be created by the utility server"""

    lfdi: str
    expiry: dt.datetime


class CertificateAssignmentRequest(pydantic.BaseModel):
    """Represents a single assignment of a certificate to another entity

    The intent is that the certificate can be created from the model or simply assigned e.g. to an aggregator
    """

    certificate_id: int | None = None
    lfdi: str | None = None
    expiry: dt.datetime | None = None

    @pydantic.model_validator(mode="after")
    def id_or_lfdi_provided_xor(self) -> "CertificateAssignmentRequest":
        """Validates either one of lfdi or id provided, but not both (exclusive or).

        Both are identifiers of a single certificate, so ambiguity could be
        created if both are provided. To avoid, this model rejects validation.

        Raises:
            ValueError if neither id or lfdi provided, or if both are provided
        """
        if self.certificate_id is None and self.lfdi is None:
            raise ValueError("Either lfdi or id needs to be provided")
        elif self.certificate_id is not None and self.lfdi is not None:
            raise ValueError("Only one of lfdi or id can be provided, not both")
        return self
