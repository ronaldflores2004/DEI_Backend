from sqlalchemy.orm import Session

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.recommendations.models.patient_recommendation import (
    PatientRecommendation
)

from app.recommendations.repositories.patient_recommendation_repository import (
    PatientRecommendationRepository
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
        analysis_id=data.analysis_id,
        title=data.title,
        content=data.content,
        source=data.source
    )

    recommendation = (
        PatientRecommendationRepository.create(
            db=db,
            recommendation=recommendation
        )
    )

    return recommendation


# =====================================
# Obtener recomendaciones del paciente
# =====================================

def get_my_recommendations(
    patient: PatientProfile,
    db: Session
):

    return (
        PatientRecommendationRepository.get_by_patient(
            db=db,
            patient_id=patient.id
        )
    )