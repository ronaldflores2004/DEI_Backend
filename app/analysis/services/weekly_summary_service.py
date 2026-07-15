from collections import Counter
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.analysis.repositories.emotional_analysis_repository import (
    EmotionalAnalysisRepository
)

from app.analysis.summary_providers.provider_factory import (
    SummaryProviderFactory
)

from app.core.config import (
    settings
)

NEGATIVE_EMOTIONS = [
    "Ansiedad",
    "Tristeza",
    "Miedo",
    "Estrés",
    "Soledad",
    "Frustración",
    "Preocupación"
]

POSITIVE_EMOTIONS = [
    "Calma",
    "Alegría",
    "Gratitud"
]

class WeeklySummaryService:
    """
    Servicio encargado de generar el resumen
    semanal del paciente.
    """
    
    @staticmethod
    def _calculate_average_intensity(
        intensities: list[str],
    ) -> str:

        intensity_values = {
            "Baja": 1,
            "Media": 2,
            "Alta": 3,
        }

        reverse_values = {
            1: "Baja",
            2: "Media",
            3: "Alta",
        }

        valid = [
            intensity
            for intensity in intensities
            if intensity in intensity_values
        ]

        if not valid:
            return "Baja"

        average = round(
            sum(
                intensity_values[value]
                for value in valid
            ) / len(valid)
        )

        return reverse_values[average]

    @staticmethod
    def get_weekly_summary(
        patient: PatientProfile,
        db: Session
    ):

        week_ago = (
            datetime.utcnow()
            - timedelta(days=7)
        )

        analyses = (
            EmotionalAnalysisRepository.get_weekly_by_patient(
                db=db,
                patient_id=patient.id,
                since=week_ago
            )
        )

        if not analyses:

            return {
                "entries_count": 0,
                "dominant_emotion": None,
                "latest_emotion": None,
                "average_intensity": None,
                "risk_level": None,
                "trend": "SIN_DATOS",
                "ai_summary": None,
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

        intensities = [
            analysis.emotion_intensity
            for analysis in analyses
            if analysis.emotion_intensity
        ]

        average_intensity = (
            WeeklySummaryService
            ._calculate_average_intensity(
                intensities
            )
        )
        
        latest_analysis = max(
            analyses,
            key=lambda analysis:
                analysis.analyzed_at
        )

        latest_emotion = (
            latest_analysis.primary_emotion
        )

        trend = "ESTABLE"

        if latest_emotion in NEGATIVE_EMOTIONS:

            trend = "ATENCION"

        elif latest_emotion in POSITIVE_EMOTIONS:

            trend = "MEJORA"

        topics = []

        triggers = []

        for analysis in analyses:

            data = (
                analysis.analysis_json
                or {}
            )

            topics.extend(
                data.get(
                    "topics",
                    []
                )
            )

            triggers.extend(
                data.get(
                    "triggers",
                    []
                )
            )

        try:

            provider = (
                SummaryProviderFactory.get_provider(
                    settings.AI_PROVIDER
                )
            )

            ai_summary = provider.generate(
                dominant_emotion,
                latest_emotion,
                risk_level,
                topics,
                triggers
            )

        except Exception as e:

            print(e)

            provider = (
                SummaryProviderFactory.get_provider(
                    "FAKE"
                )
            )

            ai_summary = provider.generate(
                dominant_emotion,
                latest_emotion,
                risk_level,
                topics,
                triggers
            )

        return {

            "entries_count":
                len(analyses),

            "dominant_emotion":
                dominant_emotion,

            "latest_emotion":
                latest_emotion,

            "risk_level":
                risk_level,

            "trend":
                trend,

            "average_intensity":
                average_intensity,

            "ai_summary":
                ai_summary,

            "recommendation":
                (
                    f"Tu emoción predominante fue "
                    f"{dominant_emotion}. "
                    f"Continúa registrando tus emociones "
                    f"para identificar patrones."
                )
        }