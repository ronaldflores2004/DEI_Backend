from datetime import datetime

from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.platform_consents.documents import (
    CONSENT_DOCUMENTS
)

from app.platform_consents.models.platform_consent import (
    PlatformConsent
)

from app.platform_consents.repositories.platform_consent_repository import (
    PlatformConsentRepository
)

from app.platform_consents.schemas.platform_consent_create import (
    PlatformConsentCreate
)

from app.shared.enums.platform_consent_type_enum import (
    PlatformConsentTypeEnum
)


MISSING_CONSENT_DETAIL = {
    PlatformConsentTypeEnum.INFORMED_CONSENT: (
        "Debes aceptar el consentimiento informado "
        "vigente para usar el diario"
    ),
    PlatformConsentTypeEnum.AI_PROCESSING: (
        "Debes aceptar el uso de inteligencia "
        "artificial para el análisis automático"
    ),
}


class PlatformConsentService:
    """
    Consentimientos del paciente hacia la plataforma:
    consentimiento informado y uso de IA.
    """

    @staticmethod
    def has_current_consent(
        patient_id: int,
        consent_type: PlatformConsentTypeEnum,
        db: Session,
    ) -> bool:
        """
        True solo si hay un consentimiento activo para
        la versión vigente del texto.
        """

        consent = PlatformConsentRepository.get_active(
            db=db,
            patient_id=patient_id,
            consent_type=consent_type.value
        )

        return (
            consent is not None
            and consent.version
            == CONSENT_DOCUMENTS[consent_type]["version"]
        )

    @staticmethod
    def require_consent(
        patient_id: int,
        consent_type: PlatformConsentTypeEnum,
        db: Session,
    ) -> None:

        if not PlatformConsentService.has_current_consent(
            patient_id=patient_id,
            consent_type=consent_type,
            db=db
        ):
            raise HTTPException(
                status_code=403,
                detail=MISSING_CONSENT_DETAIL[consent_type]
            )

    @staticmethod
    def get_documents(
        patient: PatientProfile,
        db: Session,
    ) -> list[dict]:

        return [
            {
                "consent_type": consent_type,
                **document,
                "accepted": (
                    PlatformConsentService.has_current_consent(
                        patient_id=patient.id,
                        consent_type=consent_type,
                        db=db
                    )
                ),
            }
            for consent_type, document
            in CONSENT_DOCUMENTS.items()
        ]

    @staticmethod
    def accept(
        data: PlatformConsentCreate,
        patient: PatientProfile,
        db: Session,
    ) -> PlatformConsent:

        current_version = (
            CONSENT_DOCUMENTS[data.consent_type]["version"]
        )

        if data.version != current_version:
            raise HTTPException(
                status_code=400,
                detail=(
                    "La versión aceptada no es la vigente "
                    f"({current_version})"
                )
            )

        active = PlatformConsentRepository.get_active(
            db=db,
            patient_id=patient.id,
            consent_type=data.consent_type.value
        )

        if active and active.version == current_version:
            return active

        # Una versión anterior queda revocada al
        # aceptar la nueva, para conservar el historial.
        if active:
            active.revoked_at = datetime.utcnow()

        return PlatformConsentRepository.create(
            db=db,
            consent=PlatformConsent(
                patient_id=patient.id,
                consent_type=data.consent_type.value,
                version=current_version
            )
        )

    @staticmethod
    def get_my_consents(
        patient: PatientProfile,
        db: Session,
    ) -> list[PlatformConsent]:

        return PlatformConsentRepository.get_by_patient(
            db=db,
            patient_id=patient.id
        )

    @staticmethod
    def revoke(
        consent_type: PlatformConsentTypeEnum,
        patient: PatientProfile,
        db: Session,
    ) -> PlatformConsent:

        if consent_type != PlatformConsentTypeEnum.AI_PROCESSING:
            raise HTTPException(
                status_code=400,
                detail=(
                    "El consentimiento informado no se "
                    "revoca: para dejar de usar DEI "
                    "solicita la baja de tu cuenta"
                )
            )

        active = PlatformConsentRepository.get_active(
            db=db,
            patient_id=patient.id,
            consent_type=consent_type.value
        )

        if not active:
            raise HTTPException(
                status_code=404,
                detail="No existe consentimiento activo"
            )

        active.revoked_at = datetime.utcnow()

        return PlatformConsentRepository.update(
            db=db,
            consent=active
        )
