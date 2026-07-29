from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.identity.repositories.professional_repository import (
    ProfessionalRepository
)

from app.sessions.repositories.therapy_session_repository import (
    TherapySessionRepository
)

from app.sessions.repositories.clinical_note_repository import (
    ClinicalNoteRepository
)

from app.sessions.models.clinical_note import (
    ClinicalNote
)

from app.therapy.services.access_policy_service import (
    AccessPolicyService
)



class ClinicalNoteService:

    @staticmethod
    def create_note(
        session_id: int,
        current_user_id: int,
        data,
        db: Session
    ):

        professional = (
            ProfessionalRepository.get_by_user_id(
                db=db,
                user_id=current_user_id
            )
        )

        if not professional:
            raise HTTPException(
                status_code=403,
                detail="No tienes perfil profesional"
            )

        session = (
            TherapySessionRepository.get_by_id(
                db=db,
                session_id=session_id
            )
        )

        if not session:
            raise HTTPException(
                status_code=404,
                detail="Sesión no encontrada"
            )

        if session.professional_id != professional.id:
            raise HTTPException(
                status_code=403,
                detail="No tienes acceso a esta sesión"
            )

        AccessPolicyService.require_patient_access(
            patient_id=session.patient_id,
            professional_id=professional.id,
            db=db
        )

        note = ClinicalNote(
            session_id=session.id,
            professional_id=professional.id,
            note=data.note
        )

        note = (
            ClinicalNoteRepository.create(
                db=db,
                note=note
            )
        )

        return note

    @staticmethod
    def get_notes(
        session_id: int,
        current_user_id: int,
        db: Session
    ):

        professional = (
            ProfessionalRepository.get_by_user_id(
                db=db,
                user_id=current_user_id
            )
        )

        if not professional:
            raise HTTPException(
                status_code=403,
                detail="No tienes perfil profesional"
            )

        session = (
            TherapySessionRepository.get_by_id(
                db=db,
                session_id=session_id
            )
        )

        if not session:
            raise HTTPException(
                status_code=404,
                detail="Sesión no encontrada"
            )

        if session.professional_id != professional.id:
            raise HTTPException(
                status_code=403,
                detail="No tienes acceso a esta sesión"
            )

        AccessPolicyService.require_patient_access(
            patient_id=session.patient_id,
            professional_id=professional.id,
            db=db
        )

        return (
            ClinicalNoteRepository.get_by_session(
                db=db,
                session_id=session_id
            )
        )