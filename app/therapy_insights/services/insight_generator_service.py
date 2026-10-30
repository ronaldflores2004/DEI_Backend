from datetime import datetime

from collections import Counter

from sqlalchemy.orm import Session

from app.analysis.repositories.emotional_analysis_repository import (
    EmotionalAnalysisRepository
)

from app.shared.enums.insight_priority_enum import (
    InsightPriorityEnum
)

from app.shared.emotions import (
    is_negative,
    normalize_emotion
)


class TherapyInsightService:

    @staticmethod
    def generate_insights(
        patient_id: int,
        db: Session,
        since: datetime | None = None
    ):

        # =====================================
        # OBTENER ANÁLISIS DEL PACIENTE
        # =====================================

        analyses = (
            EmotionalAnalysisRepository.get_by_patient(
                db=db,
                patient_id=patient_id,
                since=since
            )
        )

        insights = []

        if not analyses:
            return insights

        # =====================================
        # EMOCIONES DOMINANTES
        # =====================================

        # Normalizar para que "TRISTEZA" y "Tristeza"
        # cuenten como la misma emoción.
        emotions = [
            normalize_emotion(analysis.primary_emotion)
            for analysis in analyses
            if analysis.primary_emotion
        ]

        emotion_counter = Counter(
            emotions
        )

        for emotion, count in (
            emotion_counter.most_common(3)
        ):

            if (
                count >= 3
                and is_negative(emotion)
            ):

                insights.append({

                    "title":
                        "Patrón emocional recurrente",

                    "content":
                        (
                            f"{emotion} aparece "
                            f"{count} veces en los análisis."
                        ),

                    "priority":
                        InsightPriorityEnum.HIGH
                })

        # =====================================
        # TOPICS Y TRIGGERS
        # =====================================

        topics = []

        triggers = []

        for analysis in analyses:

            analysis_data = (
                analysis.analysis_json
                or {}
            )

            topics.extend(
                analysis_data.get(
                    "topics",
                    []
                )
            )

            triggers.extend(
                analysis_data.get(
                    "triggers",
                    []
                )
            )

        # =====================================
        # TEMAS RECURRENTES
        # =====================================

        topic_counter = Counter(
            topics
        )

        for topic, count in (
            topic_counter.most_common(5)
        ):

            if count >= 2:

                insights.append({

                    "title":
                        "Tema recurrente",

                    "content":
                        (
                            f"{topic} aparece "
                            f"{count} veces "
                            "en los análisis."
                        ),

                    "priority":
                        InsightPriorityEnum.MEDIUM
                })

        # =====================================
        # DESENCADENANTES FRECUENTES
        # =====================================

        trigger_counter = Counter(
            triggers
        )

        for trigger, count in (
            trigger_counter.most_common(5)
        ):

            if count >= 2:

                insights.append({

                    "title":
                        "Desencadenante frecuente",

                    "content":
                        (
                            f"{trigger} aparece "
                            f"{count} veces "
                            "como posible detonante."
                        ),

                    "priority":
                        InsightPriorityEnum.HIGH
                })

        return insights
    