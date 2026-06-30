from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis
)

from app.entries.models.emotional_entry import (
    EmotionalEntry
)

from app.recommendations.models.patient_recommendation import (
    PatientRecommendation
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
        db.query(EmotionalAnalysis)
        .filter(
            EmotionalAnalysis.id == analysis_id
        )
        .first()
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
        db.query(EmotionalEntry)
        .filter(
            EmotionalEntry.id == analysis.entry_id
        )
        .first()
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
        db.query(PatientRecommendation)
        .filter(
            PatientRecommendation.analysis_id
            == analysis_id
        )
        .first()
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

    db.add(recommendation)

    db.commit()

    db.refresh(recommendation)

    return recommendation