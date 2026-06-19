from collections import Counter

from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.entries.models.emotional_entry import (
    EmotionalEntry
)

from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis
)


def get_weekly_summary(
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

    analyses = (
        db.query(EmotionalAnalysis)
        .join(
            EmotionalEntry,
            EmotionalAnalysis.entry_id == EmotionalEntry.id
        )
        .filter(
            EmotionalEntry.patient_id == patient.id
        )
        .all()
    )

    if not analyses:
        return {
            "entries_count": 0,
            "dominant_emotion": None,
            "risk_level": None,
            "recommendation": (
                "Todavía no existen análisis emocionales."
            )
        }

    emotions = [
        analysis.primary_emotion
        for analysis in analyses
        if analysis.primary_emotion
    ]

    dominant_emotion = (
        Counter(emotions)
        .most_common(1)[0][0]
    )

    risks = [
        analysis.risk_level
        for analysis in analyses
        if analysis.risk_level
    ]

    risk_level = (
        Counter(risks)
        .most_common(1)[0][0]
    )

    return {
        "entries_count": len(analyses),
        "dominant_emotion": dominant_emotion,
        "risk_level": risk_level,
        "recommendation":
            f"Tu emoción predominante fue {dominant_emotion}. Continúa registrando tus emociones para identificar patrones."
    }