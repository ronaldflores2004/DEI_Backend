from sqlalchemy.orm import Session

from app.identity.models.professional_profile import (
    ProfessionalProfile
)

from app.therapy.models.patient_professional import (
    PatientProfessional
)

from app.therapy.models.link_request import (
    LinkRequest
)

from app.entries.models.emotional_entry import (
    EmotionalEntry
)

from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis
)

from app.therapy_insights.services.insight_generator_service import (
    generate_insights
)


def get_professional_dashboard(
    current_user_id: int,
    db: Session
):

    professional = (
        db.query(ProfessionalProfile)
        .filter(
            ProfessionalProfile.user_id == current_user_id
        )
        .first()
    )

    if not professional:
        return {
            "active_patients": 0,
            "patients_with_risk": 0,
            "pending_link_requests": 0,
            "total_insights": 0
        }

    relations = (
        db.query(PatientProfessional)
        .filter(
            PatientProfessional.professional_id
            == professional.id,
            PatientProfessional.active == True
        )
        .all()
    )

    patient_ids = [
        relation.patient_id
        for relation in relations
    ]

    active_patients = len(patient_ids)

    pending_requests = (
        db.query(LinkRequest)
        .filter(
            LinkRequest.professional_id
            == professional.id,
            LinkRequest.status == "PENDING"
        )
        .count()
    )

    patients_with_risk = set()

    total_insights = 0

    for patient_id in patient_ids:

        analyses = (
            db.query(EmotionalAnalysis)
            .join(
                EmotionalEntry,
                EmotionalAnalysis.entry_id
                == EmotionalEntry.id
            )
            .filter(
                EmotionalEntry.patient_id
                == patient_id
            )
            .all()
        )

        for analysis in analyses:

            if analysis.risk_level in [
                "Medio",
                "Alto",
                "Crítico"
            ]:
                patients_with_risk.add(
                    patient_id
                )

        insights = generate_insights(
            patient_id,
            db
        )

        total_insights += len(
            insights
        )

    return {
        "active_patients":
            active_patients,

        "patients_with_risk":
            len(patients_with_risk),

        "pending_link_requests":
            pending_requests,

        "total_insights":
            total_insights
    }