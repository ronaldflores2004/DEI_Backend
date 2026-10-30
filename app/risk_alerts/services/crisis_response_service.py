import logging

from sqlalchemy.orm import Session

from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis
)

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.identity.repositories.professional_repository import (
    ProfessionalRepository
)

from app.risk_alerts.models.risk_alert import (
    RiskAlert
)

from app.risk_alerts.repositories.risk_alert_repository import (
    RiskAlertRepository
)

from app.shared.enums.risk_alert_status_enum import (
    RiskAlertStatusEnum
)

from app.notifications.models.notification import (
    Notification
)

from app.notifications.repositories.notification_repository import (
    NotificationRepository
)

from app.therapy.repositories.patient_professional_repository import (
    PatientProfessionalRepository
)

from app.therapy.services.access_policy_service import (
    AccessPolicyService
)

from app.shared.enums.notification_type_enum import (
    NotificationTypeEnum
)

from app.shared.enums.risk_level_enum import (
    RiskLevelEnum
)

from app.shared.safety.crisis_resources import (
    get_crisis_resources
)

logger = logging.getLogger(__name__)

CRISIS_RISK_LEVELS = [
    RiskLevelEnum.HIGH,
    RiskLevelEnum.CRITICAL
]


class CrisisResponseService:
    """
    Respuesta inmediata cuando un análisis
    detecta riesgo HIGH o CRITICAL: ayuda para
    el paciente y aviso a sus profesionales.
    """

    @staticmethod
    def handle(
        analysis: EmotionalAnalysis,
        patient: PatientProfile,
        db: Session,
    ) -> dict | None:

        if analysis.risk_level not in CRISIS_RISK_LEVELS:
            return None

        professional_notified = (
            CrisisResponseService._notify_professionals(
                analysis=analysis,
                patient=patient,
                db=db
            )
        )

        return {
            **get_crisis_resources(db=db),
            "professional_notified": professional_notified,
        }

    @staticmethod
    def _notify_professionals(
        analysis: EmotionalAnalysis,
        patient: PatientProfile,
        db: Session,
    ) -> bool:
        """
        Notifica solo a profesionales con relación
        activa y consentimiento vigente. El mensaje
        no incluye el texto de la entrada.
        """

        relations = PatientProfessionalRepository.get_by_patient(
            db=db,
            patient_id=patient.id
        )

        notified = False

        for relation in relations:

            if not relation.active:
                continue

            if not AccessPolicyService.has_active_consent(
                patient_id=patient.id,
                professional_id=relation.professional_id,
                db=db
            ):
                continue

            # No avisar de entradas que el paciente
            # no comparte con este profesional.
            shared_since = AccessPolicyService.get_shared_since(
                patient_id=patient.id,
                professional_id=relation.professional_id,
                db=db
            )

            if (
                shared_since
                and analysis.entry.created_at < shared_since
            ):
                continue

            professional = ProfessionalRepository.get_by_id(
                db,
                relation.professional_id
            )

            if not professional:
                continue

            risk_level = RiskLevelEnum(analysis.risk_level).value

            if not CrisisResponseService._register_alert(
                analysis=analysis,
                patient=patient,
                professional_id=professional.id,
                risk_level=risk_level,
                db=db
            ):
                # Ya avisado por este análisis con el
                # mismo nivel: no repetir la notificación.
                notified = True
                continue

            NotificationRepository.create_no_commit(
                db=db,
                notification=Notification(
                    user_id=professional.user_id,
                    title=f"Alerta de riesgo {risk_level}",
                    message=(
                        f"{patient.first_name} {patient.last_name} "
                        f"registró una entrada con riesgo "
                        f"{risk_level}. Revisa sus alertas."
                    ),
                    type=NotificationTypeEnum.RISK_ALERT
                )
            )

            notified = True

        try:

            db.commit()

        except Exception:

            db.rollback()

            logger.exception(
                "No se pudo notificar el riesgo del "
                "análisis %s",
                analysis.id
            )

            return False

        return notified

    @staticmethod
    def _register_alert(
        analysis: EmotionalAnalysis,
        patient: PatientProfile,
        professional_id: int,
        risk_level: str,
        db: Session,
    ) -> bool:
        """
        Crea la alerta, o la reabre si un reanálisis
        sube el nivel. Devuelve True si hay que notificar.
        """

        alert = (
            RiskAlertRepository.get_by_analysis_and_professional(
                db=db,
                analysis_id=analysis.id,
                professional_id=professional_id
            )
        )

        if not alert:

            RiskAlertRepository.create_no_commit(
                db=db,
                alert=RiskAlert(
                    patient_id=patient.id,
                    professional_id=professional_id,
                    analysis_id=analysis.id,
                    risk_level=risk_level,
                    status=RiskAlertStatusEnum.NEW
                )
            )

            return True

        escalated = (
            alert.risk_level == RiskLevelEnum.HIGH
            and risk_level == RiskLevelEnum.CRITICAL
        )

        if not escalated:
            return False

        alert.risk_level = risk_level
        alert.status = RiskAlertStatusEnum.NEW
        alert.seen_at = None
        alert.resolved_at = None

        return True
