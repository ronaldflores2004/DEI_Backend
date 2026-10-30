from datetime import datetime

from pydantic import BaseModel

from app.shared.enums.platform_consent_type_enum import (
    PlatformConsentTypeEnum
)


class PlatformConsentResponse(BaseModel):

    id: int

    consent_type: PlatformConsentTypeEnum

    version: str

    granted_at: datetime

    revoked_at: datetime | None

    class Config:
        from_attributes = True


class ConsentDocumentResponse(BaseModel):

    consent_type: PlatformConsentTypeEnum

    version: str

    title: str

    content: str

    # Si el paciente ya aceptó esta versión.
    accepted: bool
