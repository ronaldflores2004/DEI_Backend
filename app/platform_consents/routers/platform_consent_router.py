from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_patient_profile
)

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.platform_consents.schemas.platform_consent_create import (
    PlatformConsentCreate
)

from app.platform_consents.schemas.platform_consent_response import (
    ConsentDocumentResponse,
    PlatformConsentResponse
)

from app.platform_consents.services.platform_consent_service import (
    PlatformConsentService
)

from app.shared.enums.platform_consent_type_enum import (
    PlatformConsentTypeEnum
)


router = APIRouter(
    prefix="/platform-consents",
    tags=["Platform Consents"]
)


# =====================================
# Textos vigentes y si ya fueron aceptados
# =====================================

@router.get(
    "/documents",
    response_model=list[ConsentDocumentResponse]
)
def get_documents(
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    return PlatformConsentService.get_documents(
        patient=patient,
        db=db
    )


# =====================================
# Aceptar consentimiento
# =====================================

@router.post(
    "",
    response_model=PlatformConsentResponse
)
def accept_consent(
    data: PlatformConsentCreate,
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    return PlatformConsentService.accept(
        data=data,
        patient=patient,
        db=db
    )


# =====================================
# Historial de consentimientos
# =====================================

@router.get(
    "",
    response_model=list[PlatformConsentResponse]
)
def get_my_consents(
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    return PlatformConsentService.get_my_consents(
        patient=patient,
        db=db
    )


# =====================================
# Revocar consentimiento de IA
# =====================================

@router.patch(
    "/{consent_type}/revoke",
    response_model=PlatformConsentResponse
)
def revoke_consent(
    consent_type: PlatformConsentTypeEnum,
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    return PlatformConsentService.revoke(
        consent_type=consent_type,
        patient=patient,
        db=db
    )
