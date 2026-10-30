import logging

from sqlalchemy.orm import Session

from app.audit.models.access_audit_log import (
    AccessAuditLog
)

from app.audit.repositories.access_audit_repository import (
    AccessAuditRepository
)

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.identity.repositories.professional_repository import (
    ProfessionalRepository
)

from app.shared.enums.audit_action_enum import (
    AuditActionEnum
)

logger = logging.getLogger(__name__)


class AccessAuditService:
    """
    Auditoría de accesos de profesionales a
    datos de pacientes.
    """

    @staticmethod
    def log(
        professional_id: int,
        patient_ids: list[int] | set[int],
        action: AuditActionEnum,
        db: Session,
    ) -> None:

        if not patient_ids:
            return

        try:

            AccessAuditRepository.create_many(
                db=db,
                logs=[
                    AccessAuditLog(
                        professional_id=professional_id,
                        patient_id=patient_id,
                        action=action.value
                    )
                    for patient_id in set(patient_ids)
                ]
            )

        except Exception:

            db.rollback()

            # La auditoría no debe bloquear la atención,
            # pero el fallo queda registrado.
            logger.exception(
                "No se pudo registrar la auditoría %s",
                action.value
            )

    @staticmethod
    def get_my_access_log(
        patient: PatientProfile,
        db: Session,
    ) -> list[dict]:

        logs = AccessAuditRepository.get_by_patient(
            db=db,
            patient_id=patient.id
        )

        names = {}

        for log in logs:

            if log.professional_id not in names:

                professional = ProfessionalRepository.get_by_id(
                    db,
                    log.professional_id
                )

                names[log.professional_id] = (
                    f"{professional.first_name} "
                    f"{professional.last_name}"
                    if professional
                    else "Profesional"
                )

        return [
            {
                "professional_id": log.professional_id,
                "professional_name": names[log.professional_id],
                "action": log.action,
                "created_at": log.created_at,
            }
            for log in logs
        ]
