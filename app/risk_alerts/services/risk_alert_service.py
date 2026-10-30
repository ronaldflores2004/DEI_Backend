from collections import defaultdict
from datetime import datetime

from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.risk_alerts.models.risk_alert import (
    RiskAlert
)

from app.risk_alerts.repositories.risk_alert_repository import (
    RiskAlertRepository
)

from app.shared.enums.risk_alert_status_enum import (
    RiskAlertStatusEnum
)

from app.analysis.repositories.emotional_analysis_repository import (
    EmotionalAnalysisRepository
)

from app.therapy.repositories.patient_professional_repository import (
    PatientProfessionalRepository
)

from app.therapy.services.access_policy_service import (
    AccessPolicyService
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

        # patient_id -> fecha desde la que comparte
        # (None = todo el historial)
        allowed_patients = {}

        for relation in patient_relations:

            if AccessPolicyService.has_active_consent(
                patient_id=relation.patient_id,
                professional_id=professional_id,
                db=db
            ):
                allowed_patients[relation.patient_id] = (
                    AccessPolicyService.get_shared_since(
                        patient_id=relation.patient_id,
                        professional_id=professional_id,
                        db=db
                    )
                )

        # =====================================
        # ANÁLISIS EMOCIONALES
        # =====================================

        analyses = (
            EmotionalAnalysisRepository.get_with_entries(
                db,
                patient_ids=list(allowed_patients)
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

            shared_since = allowed_patients[entry.patient_id]

            if shared_since and entry.created_at < shared_since:
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

class RiskAlertTrackingService:
    """
    Seguimiento de alertas HIGH o CRITICAL:
    bandeja del profesional, vista y resolución.
    """

    @staticmethod
    def get_inbox(
        professional_id: int,
        db: Session,
        status: RiskAlertStatusEnum | None = None,
    ) -> list[RiskAlert]:

        return RiskAlertRepository.get_by_professional(
            db=db,
            professional_id=professional_id,
            status=status.value if status else None
        )

    @staticmethod
    def _get_own_alert(
        alert_id: int,
        professional_id: int,
        db: Session,
    ) -> RiskAlert:

        alert = RiskAlertRepository.get_by_id(
            db=db,
            alert_id=alert_id
        )

        if (
            not alert
            or alert.professional_id != professional_id
        ):
            raise HTTPException(
                status_code=404,
                detail="Alerta no encontrada"
            )

        return alert

    @staticmethod
    def mark_seen(
        alert_id: int,
        professional_id: int,
        db: Session,
    ) -> RiskAlert:

        alert = RiskAlertTrackingService._get_own_alert(
            alert_id=alert_id,
            professional_id=professional_id,
            db=db
        )

        if alert.status == RiskAlertStatusEnum.NEW:
            alert.status = RiskAlertStatusEnum.SEEN
            alert.seen_at = datetime.utcnow()

        return RiskAlertRepository.update(
            db=db,
            alert=alert
        )

    @staticmethod
    def resolve(
        alert_id: int,
        professional_id: int,
        resolution_note: str,
        db: Session,
    ) -> RiskAlert:

        alert = RiskAlertTrackingService._get_own_alert(
            alert_id=alert_id,
            professional_id=professional_id,
            db=db
        )

        now = datetime.utcnow()

        alert.status = RiskAlertStatusEnum.RESOLVED
        alert.seen_at = alert.seen_at or now
        alert.resolved_at = now
        alert.resolution_note = resolution_note

        return RiskAlertRepository.update(
            db=db,
            alert=alert
        )
