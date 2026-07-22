from sqlalchemy.orm import Session

from app.shared.enums.risk_level_enum import RiskLevelEnum
from app.identity.models.professional_profile import (
    ProfessionalProfile
)

from app.therapy.repositories.patient_professional_repository import (
    PatientProfessionalRepository
)

from app.therapy.repositories.link_request_repository import (
    LinkRequestRepository
)

from app.analysis.repositories.emotional_analysis_repository import (
    EmotionalAnalysisRepository
)

from app.therapy_insights.services.insight_generator_service import (
    TherapyInsightService
)

from app.therapy.services.access_policy_service import (
    has_active_consent
)


class ProfessionalDashboardService:

    @staticmethod
    def get_dashboard(
        professional: ProfessionalProfile,
        db: Session
    ):

        # =====================================
        # PACIENTES ACTIVOS
        # =====================================

        relations = (
            PatientProfessionalRepository.get_by_professional(
                db=db,
                professional_id=professional.id
            )
        )

        patient_ids = []

        for relation in relations:

            if (
                relation.active
                and has_active_consent(
                    patient_id=relation.patient_id,
                    professional_id=professional.id,
                    db=db
                )
            ):

                patient_ids.append(
                    relation.patient_id
                )

        active_patients = len(patient_ids)

        # =====================================
        # SOLICITUDES PENDIENTES
        # =====================================

        pending_requests = len(
            LinkRequestRepository.get_pending_by_professional(
                db=db,
                professional_id=professional.id
            )
        )

        # =====================================
        # PACIENTES CON RIESGO
        # =====================================

        patients_with_risk = set()

        total_insights = 0

        for patient_id in patient_ids:

            analyses = (
                EmotionalAnalysisRepository.get_by_patient(
                    db=db,
                    patient_id=patient_id
                )
            )

            for analysis in analyses:

                if analysis.risk_level in [
                    RiskLevelEnum.MEDIUM,
                    RiskLevelEnum.HIGH,
                    RiskLevelEnum.CRITICAL
                ]:

                    patients_with_risk.add(
                        patient_id
                    )

            insights = TherapyInsightService.generate_insights(
                patient_id=patient_id,
                db=db
            )

            total_insights += len(insights)

        # =====================================
        # DASHBOARD
        # =====================================

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