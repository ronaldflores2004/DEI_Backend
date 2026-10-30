from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_patient_profile
)

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.platform_consents.services.platform_consent_service import (
    PlatformConsentService
)

from app.shared.enums.platform_consent_type_enum import (
    PlatformConsentTypeEnum
)


def require_platform_consent(
    consent_type: PlatformConsentTypeEnum
):
    """
    Dependencia que exige al paciente un
    consentimiento vigente del tipo indicado.
    """

    def checker(
        db: Session = Depends(get_db),
        patient: PatientProfile = Depends(
            get_current_patient_profile
        )
    ) -> None:

        PlatformConsentService.require_consent(
            patient_id=patient.id,
            consent_type=consent_type,
            db=db
        )

    return checker


require_informed_consent = require_platform_consent(
    PlatformConsentTypeEnum.INFORMED_CONSENT
)

require_ai_consent = require_platform_consent(
    PlatformConsentTypeEnum.AI_PROCESSING
)
