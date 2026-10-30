from pydantic import BaseModel, Field

from app.shared.enums.platform_consent_type_enum import (
    PlatformConsentTypeEnum
)


class PlatformConsentCreate(BaseModel):

    consent_type: PlatformConsentTypeEnum

    # Versión del texto que el paciente leyó.
    version: str = Field(
        min_length=1,
        max_length=20
    )
