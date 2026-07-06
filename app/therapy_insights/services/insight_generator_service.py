from collections import Counter

from sqlalchemy.orm import Session


from app.analysis.repositories.emotional_analysis_repository import (
    EmotionalAnalysisRepository
)

def generate_insights(
    patient_id: int,
    db: Session
):

    # =====================================
    # OBTENER ANÁLISIS DEL PACIENTE
    # =====================================

    analyses = (
        EmotionalAnalysisRepository.get_by_patient(
            db=db,
            patient_id=patient_id
        )
    )

    insights = []

    if not analyses:
        return insights

    # =====================================
    # EMOCIONES DOMINANTES
    # =====================================

    emotions = [
        analysis.primary_emotion
        for analysis in analyses
        if analysis.primary_emotion
    ]

    emotion_counter = Counter(
        emotions
    )

    negative_emotions = [
        "Tristeza",
        "Ansiedad",
        "Miedo",
        "Estrés",
        "Soledad",
        "Frustración",
        "Preocupación",
        "Culpa",
        "Desesperanza",
        "Agotamiento"
    ]

    for emotion, count in (
        emotion_counter.most_common(3)
    ):

        if (
            count >= 3
            and emotion in negative_emotions
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
                    "HIGH"
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
                    "MEDIUM"
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
                    "HIGH"
            })

    return insights