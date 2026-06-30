from sqlalchemy.orm import Session

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.recommendations.models.patient_recommendation import (
    PatientRecommendation
)


# =====================================
# Crear recomendación manual
# =====================================

def create_recommendation(
    patient: PatientProfile,
    data,
    db: Session
):

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


# =====================================
# Obtener recomendaciones del paciente
# =====================================

def get_my_recommendations(
    patient: PatientProfile,
    db: Session
):

    return (
        db.query(PatientRecommendation)
        .filter(
            PatientRecommendation.patient_id
            == patient.id
        )
        .order_by(
            PatientRecommendation.created_at.desc()
        )
        .all()
    )