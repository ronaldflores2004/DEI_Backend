from collections import defaultdict

from sqlalchemy.orm import Session

from app.entries.models.emotional_entry import (
    EmotionalEntry
)

from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis
)

from app.therapy.models.patient_professional import (
    PatientProfessional
)


def get_risk_alerts(
    professional_id: int,
    db: Session
):

    patient_data = defaultdict(list)

    patient_relations = (
        db.query(PatientProfessional)
        .filter(
            PatientProfessional.professional_id
            == professional_id,
            PatientProfessional.active == True
        )
        .all()
    )

    allowed_patients = {
        relation.patient_id
        for relation in patient_relations
    }

    analyses = (
        db.query(EmotionalAnalysis)
        .all()
    )

    risk_order = {
        "Bajo": 1,
        "Medio": 2,
        "Alto": 3,
        "Crítico": 4
    }

    negative_emotions = [
        "Tristeza",
        "Ansiedad",
        "Miedo",
        "Estrés"
    ]

    for analysis in analyses:

        if analysis.risk_level not in [
            "Medio",
            "Alto",
            "Crítico"
        ]:
            continue

        entry = (
            db.query(EmotionalEntry)
            .filter(
                EmotionalEntry.id
                == analysis.entry_id
            )
            .first()
        )

        if not entry:
            continue

        if entry.patient_id not in allowed_patients:
            continue

        patient_data[
            entry.patient_id
        ].append(analysis)

    alerts = []

    for patient_id, analyses_list in patient_data.items():

        highest_risk = max(
            analyses_list,
            key=lambda a:
                risk_order.get(
                    a.risk_level,
                    0
                )
        ).risk_level

        latest_analysis = max(
            analyses_list,
            key=lambda a:
                a.analyzed_at
        )

        negative_count = sum(
            1
            for analysis in analyses_list
            if analysis.primary_emotion
            in negative_emotions
        )

        alerts.append({

            "patient_id":
                patient_id,

            "highest_risk":
                highest_risk,

            "alerts_count":
                len(analyses_list),

            "latest_emotion":
                latest_analysis.primary_emotion,

            "negative_emotions_count":
                negative_count,

            "message":
                (
                    f"El paciente presentó "
                    f"{len(analyses_list)} "
                    f"análisis con riesgo "
                    f"{highest_risk}."
                )
        })

    return alerts