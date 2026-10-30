from datetime import datetime

from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.analysis.repositories.emotional_analysis_repository import (
    EmotionalAnalysisRepository
)

from app.entries.repositories.emotional_entry_repository import (
    EmotionalEntryRepository
)

from app.recommendations.models.patient_recommendation import (
    PatientRecommendation
)

from app.recommendations.repositories.patient_recommendation_repository import (
    PatientRecommendationRepository
)

from app.recommendations.schemas.patient_recommendation_create import (
    PatientRecommendationCreate
)

from app.recommendations.providers.provider_factory import (
    RecommendationProviderFactory
)

from app.shared.ai.provider_chain import (
    AIProviderChain
)


from app.audit.services.access_audit_service import (
    AccessAuditService
)

from app.identity.models.professional_profile import (
    ProfessionalProfile
)

from app.identity.repositories.patient_repository import (
    PatientRepository
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

from app.shared.enums.audit_action_enum import (
    AuditActionEnum
)

from app.shared.enums.notification_type_enum import (
    NotificationTypeEnum
)

from app.shared.enums.recommendation_status_enum import (
    RecommendationStatusEnum
)

from app.shared.enums.risk_level_enum import (
    RiskLevelEnum
)

class PatientRecommendationService:
    """
    Servicio encargado de la gestión de
    recomendaciones para pacientes.
    """

    
    
    @staticmethod
    def _validate_analysis_owner(
        analysis_id: int,
        patient: PatientProfile,
        db: Session,
    ):

        analysis = EmotionalAnalysisRepository.get_by_id(
            db=db,
            analysis_id=analysis_id
        )

        if not analysis:
            raise HTTPException(
                status_code=404,
                detail="Análisis no encontrado"
            )

        entry = EmotionalEntryRepository.get_by_id(
            db=db,
            entry_id=analysis.entry_id
        )

        if not entry:
            raise HTTPException(
                status_code=404,
                detail="Entrada no encontrada"
            )

        if entry.patient_id != patient.id:
            raise HTTPException(
                status_code=403,
                detail="No tienes acceso a este análisis"
            )

        return analysis
    # =====================================
    # Crear recomendación manual
    # =====================================
    
    @staticmethod
    def create_recommendation(
        analysis_id: int,
        patient: PatientProfile,
        data: PatientRecommendationCreate,
        db: Session
    ):

        analysis = PatientRecommendationService._validate_analysis_owner(
            analysis_id=analysis_id,
            patient=patient,
            db=db
        )

        existing = (
            PatientRecommendationRepository.get_by_analysis(
                db=db,
                analysis_id=analysis_id
            )
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Este análisis ya tiene una recomendación"
            )

        recommendation = PatientRecommendation(
            patient_id=patient.id,
            analysis_id=analysis_id,
            title=data.title,
            content=data.content,
            source=data.source
        )

        recommendation = (
            PatientRecommendationRepository.create(
                db=db,
                recommendation=recommendation
            )
        )

        return recommendation


    # =====================================
    # Obtener recomendaciones del paciente
    # =====================================
    @staticmethod
    def get_my_recommendations(
        patient: PatientProfile,
        db: Session
    ):

        return (
            PatientRecommendationRepository.get_by_patient(
                db=db,
                patient_id=patient.id
            )
        )
    
    # =====================================
    # Generar recomendación desde análisis
    # =====================================
    @staticmethod
    def generate_from_analysis(
        analysis_id: int,
        patient: PatientProfile,
        db: Session
    ):

        # =====================================
        # Buscar análisis
        # =====================================

        analysis = PatientRecommendationService._validate_analysis_owner(
            analysis_id=analysis_id,
            patient=patient,
            db=db
        )

        # =====================================
        # Evitar duplicados
        # =====================================

        existing = (
            PatientRecommendationRepository.get_by_analysis(
                db=db,
                analysis_id=analysis_id
            )
        )

        if existing:
            return existing

        # =====================================
        # Generar contenido
        # =====================================

        has_professional = (
            PatientRecommendationService._has_reviewing_professional(
                patient_id=patient.id,
                db=db
            )
        )

        # Con riesgo alto, un consejo genérico de IA
        # puede ser contraproducente. Sin profesional
        # que lo revise, no se genera.
        if (
            not has_professional
            and analysis.risk_level in [
                RiskLevelEnum.HIGH,
                RiskLevelEnum.CRITICAL
            ]
        ):
            raise HTTPException(
                status_code=409,
                detail=(
                    "Por el nivel de riesgo de esta entrada "
                    "no se generan recomendaciones "
                    "automáticas. Busca apoyo de un "
                    "profesional o de una línea de crisis."
                )
            )

        recommendation_data = AIProviderChain.run(
            task="recomendación",
            get_provider=RecommendationProviderFactory.get_provider,
            call=lambda provider: provider.generate(
                analysis
            )
        )

        recommendation = PatientRecommendation(
            patient_id=patient.id,
            analysis_id=analysis.id,
            title=recommendation_data["title"],
            content=recommendation_data["content"],
            source=recommendation_data["source"],
            # Si tiene profesional, la revisa antes
            # de que llegue al paciente.
            status=(
                RecommendationStatusEnum.PENDING_REVIEW
                if has_professional
                else RecommendationStatusEnum.APPROVED
            )
        )

        recommendation = (
            PatientRecommendationRepository.create(
                db=db,
                recommendation=recommendation
            )
        )

        return recommendation

    # =====================================
    # Revisión por el profesional
    # =====================================

    @staticmethod
    def _has_reviewing_professional(
        patient_id: int,
        db: Session
    ) -> bool:

        return any(
            relation.active
            and AccessPolicyService.has_active_consent(
                patient_id=patient_id,
                professional_id=relation.professional_id,
                db=db
            )
            for relation in PatientProfessionalRepository.get_by_patient(
                db=db,
                patient_id=patient_id
            )
        )

    @staticmethod
    def get_pending_reviews(
        professional: ProfessionalProfile,
        db: Session
    ) -> list[PatientRecommendation]:

        patient_ids = [
            relation.patient_id
            for relation in PatientProfessionalRepository.get_active_by_professional(
                db=db,
                professional_id=professional.id
            )
            if AccessPolicyService.has_active_consent(
                patient_id=relation.patient_id,
                professional_id=professional.id,
                db=db
            )
        ]

        pending = PatientRecommendationRepository.get_pending_by_patients(
            db=db,
            patient_ids=patient_ids
        )

        AccessAuditService.log(
            professional_id=professional.id,
            patient_ids=[item.patient_id for item in pending],
            action=AuditActionEnum.REVIEW_RECOMMENDATION,
            db=db
        )

        return pending

    @staticmethod
    def review(
        recommendation_id: int,
        professional: ProfessionalProfile,
        approve: bool,
        db: Session,
        title: str | None = None,
        content: str | None = None,
    ) -> PatientRecommendation:

        recommendation = PatientRecommendationRepository.get_by_id(
            db=db,
            recommendation_id=recommendation_id
        )

        if not recommendation:
            raise HTTPException(
                status_code=404,
                detail="Recomendación no encontrada"
            )

        AccessPolicyService.require_patient_access(
            patient_id=recommendation.patient_id,
            professional_id=professional.id,
            db=db,
            action=AuditActionEnum.REVIEW_RECOMMENDATION
        )

        if (
            recommendation.status
            != RecommendationStatusEnum.PENDING_REVIEW
        ):
            raise HTTPException(
                status_code=400,
                detail="La recomendación ya fue revisada"
            )

        recommendation.status = (
            RecommendationStatusEnum.APPROVED
            if approve
            else RecommendationStatusEnum.REJECTED
        )
        recommendation.reviewed_by_professional_id = professional.id
        recommendation.reviewed_at = datetime.utcnow()

        if approve:

            # El profesional puede ajustar el texto.
            if title:
                recommendation.title = title

            if content:
                recommendation.content = content

            patient = PatientRepository.get_by_id(
                db=db,
                patient_id=recommendation.patient_id
            )

            if patient:
                NotificationRepository.create_no_commit(
                    db=db,
                    notification=Notification(
                        user_id=patient.user_id,
                        title="Nueva recomendación",
                        message=(
                            "Tu profesional revisó y aprobó "
                            "una recomendación para ti."
                        ),
                        type=NotificationTypeEnum.RECOMMENDATION
                    )
                )

        return PatientRecommendationRepository.update(
            db=db,
            recommendation=recommendation
        )
