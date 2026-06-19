from fastapi import HTTPException

from sqlalchemy.orm import Session

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



def generate_from_analysis(
    analysis_id: int,
    db: Session
):

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
    existing = (
        db.query(PatientRecommendation)
        .filter(
            PatientRecommendation.analysis_id == analysis_id
        )
        .first()
    )

    if existing:
        return existing

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

    recommendation_data = generate_recommendation(
        analysis.primary_emotion
    )

    recommendation = PatientRecommendation(
    patient_id=entry.patient_id,
    analysis_id=analysis.id,
    title=recommendation_data["title"],
    content=recommendation_data["content"],
    source="AI"
    )

    db.add(recommendation)

    db.commit()

    db.refresh(recommendation)

    return recommendation