from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.entries.repositories.emotional_entry_repository import (
    EmotionalEntryRepository
)

from app.identity.models.professional_profile import (
    ProfessionalProfile
)

from app.identity.models.user import User

from app.identity.repositories.professional_repository import (
    ProfessionalRepository
)

from app.identity.schemas.professional_portal import (
    ProfessionalPatientEntryResponse,
    ProfessionalPatientResponse,
)

from app.shared.enums.audit_action_enum import (
    AuditActionEnum
)

from app.shared.enums.role_enum import RoleEnum

from app.therapy.repositories.patient_professional_repository import (
    PatientProfessionalRepository
)

from app.therapy.services.access_policy_service import (
    AccessPolicyService
)


class ProfessionalPortalService:
    """
    Consultas del panel del profesional: su perfil,
    sus pacientes y las entradas que estos comparten.
    """

    @staticmethod
    def get_my_profile(
        db: Session,
        current_user: User,
    ) -> ProfessionalProfile:

        if current_user.role != RoleEnum.PROFESSIONAL:
            raise HTTPException(
                status_code=403,
                detail="Acceso permitido solo para profesionales"
            )

        profile = ProfessionalRepository.get_by_user_id(
            db=db,
            user_id=current_user.id
        )

        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Aún no tienes perfil profesional"
            )

        return profile

    @staticmethod
    def get_my_patients(
        db: Session,
        professional: ProfessionalProfile,
    ) -> list[ProfessionalPatientResponse]:

        relations = (
            PatientProfessionalRepository.get_active_by_professional(
                db=db,
                professional_id=professional.id
            )
        )

        patients = [
            ProfessionalPatientResponse(
                patient_id=relation.patient_id,
                first_name=relation.patient.first_name,
                last_name=relation.patient.last_name,
                sharing_mode=relation.sharing_mode,
                share_from=relation.share_from,
                linked_at=relation.created_at,
            )
            for relation in relations
        ]

        return sorted(
            patients,
            key=lambda p: (p.last_name, p.first_name)
        )

    @staticmethod
    def get_patient_entries(
        db: Session,
        professional: ProfessionalProfile,
        patient_id: int,
    ) -> list[ProfessionalPatientEntryResponse]:

        # Relación activa + consentimiento vigente,
        # y deja constancia en la auditoría.
        AccessPolicyService.require_patient_access(
            patient_id=patient_id,
            professional_id=professional.id,
            db=db,
            action=AuditActionEnum.VIEW_ENTRIES
        )

        # Solo lo que el paciente eligió compartir.
        since = AccessPolicyService.get_shared_since(
            patient_id=patient_id,
            professional_id=professional.id,
            db=db
        )

        if since is None:
            entries = EmotionalEntryRepository.get_by_patient(
                db=db,
                patient_id=patient_id
            )
        else:
            entries = EmotionalEntryRepository.get_recent_entries(
                db=db,
                patient_id=patient_id,
                since=since
            )

        return [
            ProfessionalPatientEntryResponse(
                id=entry.id,
                entry_type=entry.entry_type,
                text_content=entry.text_content,
                created_at=entry.created_at,
                primary_emotion=(
                    entry.analysis.primary_emotion
                    if entry.analysis else None
                ),
                emotion_intensity=(
                    entry.analysis.emotion_intensity
                    if entry.analysis else None
                ),
                risk_level=(
                    entry.analysis.risk_level
                    if entry.analysis else None
                ),
            )
            for entry in entries
        ]

    @staticmethod
    def get_directory(
        db: Session,
    ) -> list[ProfessionalProfile]:

        return ProfessionalRepository.get_verified(
            db=db
        )
