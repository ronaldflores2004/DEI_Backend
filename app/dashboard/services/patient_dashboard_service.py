from sqlalchemy.orm import Session

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.entries.repositories.emotional_entry_repository import (
    EmotionalEntryRepository
)

from app.recommendations.repositories.patient_recommendation_repository import (
    PatientRecommendationRepository
)

from app.analysis.services.weekly_summary_service import (
    get_weekly_summary
)


def get_patient_dashboard(
    patient: PatientProfile,
    db: Session
):

    # =====================================
    # RESUMEN SEMANAL
    # =====================================

    weekly = get_weekly_summary(
        patient,
        db
    )

    # =====================================
    # ÚLTIMA RECOMENDACIÓN
    # =====================================

    latest_recommendation = (
        PatientRecommendationRepository.get_latest_by_patient(
            db=db,
            patient_id=patient.id
        )
    )

    # =====================================
    # TOTAL DE ENTRADAS
    # =====================================

    entries_count = (
        EmotionalEntryRepository.count_by_patient(
            db=db,
            patient_id=patient.id
        )
    )

    # =====================================
    # DASHBOARD
    # =====================================

    return {

        "entries_count":
            entries_count,

        "dominant_emotion":
            weekly["dominant_emotion"],

        "latest_emotion":
            weekly["latest_emotion"],

        "average_intensity":
            weekly["average_intensity"],

        "risk_level":
            weekly["risk_level"],

        "trend":
            weekly["trend"],

        "ai_summary":
            weekly["ai_summary"],

        "latest_recommendation":
            (
                latest_recommendation.content
                if latest_recommendation
                else None
            )
    }