from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.identity.models.professional_profile import (
    ProfessionalProfile
)

from app.sessions.models.therapy_session import (
    TherapySession
)

from app.sessions.models.clinical_note import (
    ClinicalNote
)

from app.therapy.services.access_policy_service import (
    has_active_consent
)

def create_note(
    session_id: int,
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

    session = (
        db.query(TherapySession)
        .filter(
            TherapySession.id
            == session_id
        )
        .first()
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
    if not has_active_consent(
        patient_id=session.patient_id,
        professional_id=professional.id,
        db=db
    ):
        raise HTTPException(
            status_code=403,
            detail="No existe consentimiento activo"
        )

    note = ClinicalNote(
        session_id=session.id,
        professional_id=professional.id,
        note=data.note
    )

    db.add(note)

    db.commit()

    db.refresh(note)

    return note


def get_notes(
    session_id: int,
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

    session = (
        db.query(TherapySession)
        .filter(
            TherapySession.id
            == session_id
        )
        .first()
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
    
    if not has_active_consent(
        patient_id=session.patient_id,
        professional_id=professional.id,
        db=db
    ):
        raise HTTPException(
            status_code=403,
            detail="No existe consentimiento activo"
        )

    notes = (
        db.query(ClinicalNote)
        .filter(
            ClinicalNote.session_id
            == session_id
        )
        .all()
    )

    return notes