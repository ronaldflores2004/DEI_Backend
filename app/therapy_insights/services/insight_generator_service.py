from collections import Counter

from sqlalchemy.orm import Session

from app.entries.models.emotional_entry import (
    EmotionalEntry
)

from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis
)


def generate_insights(
    patient_id: int,
    db: Session
):

    insights = []

    analyses = (
        db.query(EmotionalAnalysis)
        .join(
            EmotionalEntry,
            EmotionalAnalysis.entry_id == EmotionalEntry.id
        )
        .filter(
            EmotionalEntry.patient_id == patient_id
        )
        .all()
    )

    if not analyses:
        return insights

    # -------------------------
    # Emociones
    # -------------------------

    emotions = [
        analysis.primary_emotion
        for analysis in analyses
        if analysis.primary_emotion
    ]

    emotion_count = Counter(
        emotions
    )

    if emotion_count:

        dominant_emotion = (
            emotion_count
            .most_common(1)[0][0]
        )

        if dominant_emotion in [
            "Tristeza",
            "Ansiedad",
            "Miedo",
            "Estrés"
        ]:

            insights.append({
                "title":
                    "Persistencia emocional negativa",

                "content":
                    (
                        f"La emoción predominante "
                        f"es {dominant_emotion}."
                    ),

                "priority":
                    "HIGH"
            })

    # -------------------------
    # Topics
    # -------------------------

    topics = []

    for analysis in analyses:

        analysis_json = (
            analysis.analysis_json or {}
        )

        topics.extend(
            analysis_json.get(
                "topics",
                []
            )
        )

    topic_count = Counter(
        topics
    )

    for topic, count in (
        topic_count.most_common(3)
    ):

        if count >= 2:

            insights.append({
                "title":
                    "Tema recurrente",

                "content":
                    (
                        f"{topic} aparece "
                        f"{count} veces "
                        f"en los registros."
                    ),

                "priority":
                    "HIGH"
                    if count >= 3
                    else "MEDIUM"
            })

    # -------------------------
    # Triggers
    # -------------------------

    triggers = []

    for analysis in analyses:

        analysis_json = (
            analysis.analysis_json or {}
        )

        triggers.extend(
            analysis_json.get(
                "triggers",
                []
            )
        )

    trigger_count = Counter(
        triggers
    )

    for trigger, count in (
        trigger_count.most_common(3)
    ):

        if count >= 2:

            insights.append({
                "title":
                    "Desencadenante frecuente",

                "content":
                    (
                        f"{trigger} aparece "
                        f"{count} veces "
                        f"en los análisis."
                    ),

                "priority":
                    "HIGH"
                    if count >= 3
                    else "MEDIUM"
            })

    return insights