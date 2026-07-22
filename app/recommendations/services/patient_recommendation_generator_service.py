from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.entries.repositories.emotional_entry_repository import (
    EmotionalEntryRepository
)

from app.analysis.repositories.emotional_analysis_repository import (
    EmotionalAnalysisRepository
)

from app.recommendations.models.patient_recommendation import (
    PatientRecommendation
)

from app.recommendations.repositories.patient_recommendation_repository import (
    PatientRecommendationRepository
)

from app.recommendations.services.recommendation_generator_service import (
    generate_recommendation
)


# =====================================
# Generar recomendación desde análisis
# =====================================

def generate_from_analysis(
    analysis_id: int,
    patient: PatientProfile,
    db: Session
):

    # =====================================
    # Buscar análisis
    # =====================================

    analysis = (
        EmotionalAnalysisRepository.get_by_id(
            db=db,
            analysis_id=analysis_id
        )
    )

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Análisis no encontrado"
        )

    # =====================================
    # Buscar entrada relacionada
    # =====================================

    entry = (
        EmotionalEntryRepository.get_by_id(
            db=db,
            entry_id=analysis.entry_id
        )
    )

    if not entry:
        raise HTTPException(
            status_code=404,
            detail="Entrada no encontrada"
        )

    # =====================================
    # Validar propiedad del análisis
    # =====================================

    if entry.patient_id != patient.id:
        raise HTTPException(
            status_code=403,
            detail=(
                "No tienes permiso para generar "
                "recomendaciones de este análisis"
            )
        )

    # =====================================
    # Evitar duplicados
    # =====================================

    existing = (
        PatientRecommendationRepository.get_by_analysis(
            db=db,
            analysis_id=analysis_id
        )
    )

    if existing:
        return existing

    # =====================================
    # Generar contenido
    # =====================================

    recommendation_data = (
        generate_recommendation(
            analysis.primary_emotion
        )
    )

    recommendation = PatientRecommendation(
        patient_id=patient.id,
        analysis_id=analysis.id,
        title=recommendation_data["title"],
        content=recommendation_data["content"],
        source="AI"
    )

    recommendation = (
        PatientRecommendationRepository.create(
            db=db,
            recommendation=recommendation
        )
    )

    return recommendation