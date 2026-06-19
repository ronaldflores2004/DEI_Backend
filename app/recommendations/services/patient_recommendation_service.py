from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.recommendations.models.patient_recommendation import (
    PatientRecommendation
)


def create_recommendation(
    current_user_id: int,
    data,
    db: Session
):

    patient = (
        db.query(PatientProfile)
        .filter(
            PatientProfile.user_id == current_user_id
        )
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=403,
            detail="No tienes perfil de paciente"
        )

    recommendation = PatientRecommendation(
        patient_id=patient.id,
        title=data.title,
        content=data.content,
        source=data.source
    )

    db.add(recommendation)

    db.commit()

    db.refresh(recommendation)

    return recommendation


def get_my_recommendations(
    current_user_id: int,
    db: Session
):

    patient = (
        db.query(PatientProfile)
        .filter(
            PatientProfile.user_id == current_user_id
        )
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=403,
            detail="No tienes perfil de paciente"
        )

    return (
        db.query(PatientRecommendation)
        .filter(
            PatientRecommendation.patient_id == patient.id
        )
        .order_by(
            PatientRecommendation.created_at.desc()
        )
        .all()
    )