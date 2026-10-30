from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.shared.enums.sharing_mode_enum import (
    SharingModeEnum
)

from app.therapy.repositories.consent_repository import (
    ConsentRepository
)

from app.therapy.repositories.patient_professional_repository import (
    PatientProfessionalRepository
)


class AccessPolicyService:
    """
    Servicio centralizado para las políticas
    de acceso clínico entre profesionales
    y pacientes.
    """

    @staticmethod
    def has_active_consent(
        patient_id: int,
        professional_id: int,
        db: Session,
    ) -> bool:

        consent = ConsentRepository.get_active(
            db=db,
            patient_id=patient_id,
            professional_id=professional_id,
        )

        return consent is not None

    @staticmethod
    def has_active_relation(
        patient_id: int,
        professional_id: int,
        db: Session,
    ) -> bool:

        relation = (
            PatientProfessionalRepository.get_active_relation(
                db=db,
                patient_id=patient_id,
                professional_id=professional_id,
            )
        )

        return relation is not None

    @staticmethod
    def get_shared_since(
        patient_id: int,
        professional_id: int,
        db: Session,
    ) -> datetime | None:
        """
        Fecha desde la que el profesional puede ver
        entradas del paciente. None significa todo
        el historial.
        """

        relation = (
            PatientProfessionalRepository.get_active_relation(
                db=db,
                patient_id=patient_id,
                professional_id=professional_id,
            )
        )

        if not relation:
            return None

        if relation.sharing_mode == SharingModeEnum.FULL_HISTORY:
            return None

        if (
            relation.sharing_mode == SharingModeEnum.FROM_DATE
            and relation.share_from
        ):
            return relation.share_from

        return relation.created_at

    @staticmethod
    def require_patient_access(
        patient_id: int,
        professional_id: int,
        db: Session,
    ) -> None:
        """
        Exige una relación terapéutica activa
        y consentimiento vigente.
        """

        if not AccessPolicyService.has_active_relation(
            patient_id=patient_id,
            professional_id=professional_id,
            db=db,
        ):
            raise HTTPException(
                status_code=403,
                detail="No tienes acceso a este paciente"
            )

        if not AccessPolicyService.has_active_consent(
            patient_id=patient_id,
            professional_id=professional_id,
            db=db,
        ):
            raise HTTPException(
                status_code=403,
                detail="No existe consentimiento activo"
            )