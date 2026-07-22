from collections import defaultdict

from sqlalchemy.orm import Session

from app.analysis.repositories.emotional_analysis_repository import (
    EmotionalAnalysisRepository
)

from app.therapy.repositories.patient_professional_repository import (
    PatientProfessionalRepository
)

from app.therapy.services.access_policy_service import (
    has_active_consent
)

from app.shared.enums.risk_level_enum import (
    RiskLevelEnum
)

class RiskAlertService:
    
    @staticmethod
    def get_risk_alerts(
        professional_id: int,
        db: Session
    ):

        # =====================================
        # PACIENTES CON RELACIÓN Y CONSENTIMIENTO
        # =====================================

        patient_relations = (
            PatientProfessionalRepository.get_active_by_professional(
                db=db,
                professional_id=professional_id
            )
        )

        allowed_patients = set()

        for relation in patient_relations:

            if has_active_consent(
                patient_id=relation.patient_id,
                professional_id=professional_id,
                db=db
            ):
                allowed_patients.add(
                    relation.patient_id
                )

        # =====================================
        # ANÁLISIS EMOCIONALES
        # =====================================

        analyses = (
            EmotionalAnalysisRepository.get_with_entries(
                db
            )
        )

        patient_data = defaultdict(list)

        risk_order = {
            RiskLevelEnum.LOW: 1,
            RiskLevelEnum.MEDIUM: 2,
            RiskLevelEnum.HIGH: 3,
            RiskLevelEnum.CRITICAL: 4
        }

        negative_emotions = [
            "Tristeza",
            "Ansiedad",
            "Miedo",
            "Estrés"
        ]

        # =====================================
        # AGRUPAR ANÁLISIS POR PACIENTE
        # =====================================

        for analysis, entry in analyses:

            if analysis.risk_level not in [
                RiskLevelEnum.MEDIUM,
                RiskLevelEnum.HIGH,
                RiskLevelEnum.CRITICAL
            ]:
                continue

            if entry.patient_id not in allowed_patients:
                continue

            patient_data[
                entry.patient_id
            ].append(
                analysis
            )

        # =====================================
        # GENERAR ALERTAS
        # =====================================

        alerts = []

        for patient_id, analyses_list in patient_data.items():

            highest_risk = max(
                analyses_list,
                key=lambda analysis:
                    risk_order.get(
                        analysis.risk_level,
                        0
                    )
            ).risk_level

            latest_analysis = max(
                analyses_list,
                key=lambda analysis:
                    analysis.analyzed_at
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