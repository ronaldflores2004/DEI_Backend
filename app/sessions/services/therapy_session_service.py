from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.identity.repositories.professional_repository import (
    ProfessionalRepository
)

from app.identity.repositories.patient_repository import (
    PatientRepository
)

from app.therapy.repositories.patient_professional_repository import (
    PatientProfessionalRepository
)

from app.sessions.repositories.therapy_session_repository import (
    TherapySessionRepository
)

from app.sessions.models.therapy_session import (
    TherapySession
)

from app.notifications.models.notification import (
    Notification
)

from app.notifications.repositories.notification_repository import (
    NotificationRepository
)

from app.therapy.services.access_policy_service import (
    has_active_consent
)



class TherapySessionService:
    
    @staticmethod
    def create_session(
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

        patient = (
            PatientRepository.get_by_id(
                db=db,
                patient_id=data.patient_id
            )
        )

        if not patient:
            raise HTTPException(
                status_code=404,
                detail="Paciente no encontrado"
            )

        relation = (
            PatientProfessionalRepository.get_active_relation(
                db=db,
                patient_id=patient.id,
                professional_id=professional.id
            )
        )

        if not relation:
            raise HTTPException(
                status_code=403,
                detail="No tienes acceso a este paciente"
            )

        if not has_active_consent(
            patient_id=patient.id,
            professional_id=professional.id,
            db=db
        ):
            raise HTTPException(
                status_code=403,
                detail="No existe consentimiento activo"
            )

        session = TherapySession(
            patient_id=patient.id,
            professional_id=professional.id,
            session_date=data.session_date,
            status="SCHEDULED"
        )

        session = (
            TherapySessionRepository.create(
                db=db,
                session=session
            )
        )

        # Se mantiene aquí hasta el Sprint Notifications
        notification = Notification(
            user_id=patient.user_id,
            title="Nueva sesión programada",
            message=(
                f"Tienes una sesión terapéutica "
                f"programada para "
                f"{data.session_date}"
            ),
            type="SESSION"
        )

        NotificationRepository.create(
            db=db,
            notification=notification
        )

        return session

    @staticmethod
    def get_sessions(
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

        return (
            TherapySessionRepository.get_by_professional(
                db=db,
                professional_id=professional.id
            )
        )

    @staticmethod
    def complete_session(
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

        if session.status == "COMPLETED":
            raise HTTPException(
                status_code=400,
                detail="La sesión ya fue completada"
            )

        if session.status == "CANCELLED":
            raise HTTPException(
                status_code=400,
                detail="La sesión fue cancelada"
            )

        session.status = "COMPLETED"

        return (
            TherapySessionRepository.update(
                db=db,
                session=session
            )
        )

    @staticmethod
    def cancel_session(
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

        if session.status == "CANCELLED":
            raise HTTPException(
                status_code=400,
                detail="La sesión ya fue cancelada"
            )

        if session.status == "COMPLETED":
            raise HTTPException(
                status_code=400,
                detail="La sesión ya fue completada"
            )

        session.status = "CANCELLED"

        return (
            TherapySessionRepository.update(
                db=db,
                session=session
            )
        )