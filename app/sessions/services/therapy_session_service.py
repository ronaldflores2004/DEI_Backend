from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.identity.models.professional_profile import (
    ProfessionalProfile
)

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.therapy.models.patient_professional import (
    PatientProfessional
)

from app.sessions.models.therapy_session import (
    TherapySession
)


def create_session(
    current_user_id: int,
    data,
    db: Session
):

    professional = (
        db.query(ProfessionalProfile)
        .filter(
            ProfessionalProfile.user_id
            == current_user_id
        )
        .first()
    )

    if not professional:
        raise HTTPException(
            status_code=403,
            detail="No tienes perfil profesional"
        )

    patient = (
        db.query(PatientProfile)
        .filter(
            PatientProfile.id
            == data.patient_id
        )
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Paciente no encontrado"
        )

    relation = (
        db.query(PatientProfessional)
        .filter(
            PatientProfessional.patient_id
            == patient.id,
            PatientProfessional.professional_id
            == professional.id,
            PatientProfessional.active == True
        )
        .first()
    )

    if not relation:
        raise HTTPException(
            status_code=403,
            detail="No tienes acceso a este paciente"
        )

    session = TherapySession(
        patient_id=patient.id,
        professional_id=professional.id,
        session_date=data.session_date,
        status="SCHEDULED"
    )

    db.add(session)

    db.commit()

    db.refresh(session)

    return session


def get_sessions(
    current_user_id: int,
    db: Session
):

    professional = (
        db.query(ProfessionalProfile)
        .filter(
            ProfessionalProfile.user_id
            == current_user_id
        )
        .first()
    )

    if not professional:
        raise HTTPException(
            status_code=403,
            detail="No tienes perfil profesional"
        )

    sessions = (
        db.query(TherapySession)
        .filter(
            TherapySession.professional_id
            == professional.id
        )
        .all()
    )

    return sessions