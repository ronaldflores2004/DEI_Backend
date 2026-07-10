from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.analysis.repositories.emotional_analysis_repository import (
    EmotionalAnalysisRepository
)

from app.entries.repositories.emotional_entry_repository import (
    EmotionalEntryRepository
)

from app.recommendations.models.patient_recommendation import (
    PatientRecommendation
)

from app.recommendations.repositories.patient_recommendation_repository import (
    PatientRecommendationRepository
)

from app.recommendations.schemas.patient_recommendation_create import (
    PatientRecommendationCreate
)


# =====================================
# Crear recomendación manual
# =====================================

def create_recommendation(
    analysis_id: int,
    patient: PatientProfile,
    data: PatientRecommendationCreate,
    db: Session
):

    analysis = EmotionalAnalysisRepository.get_by_id(
        db=db,
        analysis_id=analysis_id
    )

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Análisis no encontrado"
        )

    entry = EmotionalEntryRepository.get_by_id(
        db=db,
        entry_id=analysis.entry_id
    )

    if not entry:
        raise HTTPException(
            status_code=404,
            detail="Entrada no encontrada"
        )

    if entry.patient_id != patient.id:
        raise HTTPException(
            status_code=403,
            detail="No tienes acceso a este análisis"
        )

    existing = (
        PatientRecommendationRepository.get_by_analysis(
            db=db,
            analysis_id=analysis_id
        )
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Este análisis ya tiene una recomendación"
        )

    recommendation = PatientRecommendation(
        patient_id=patient.id,
        analysis_id=analysis_id,
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