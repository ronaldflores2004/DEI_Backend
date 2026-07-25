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

from app.shared.exceptions.ai_provider_exception import (
    AIProviderException
)

from app.core.config import settings


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

        try:

            provider = (
                RecommendationProviderFactory.get_provider(
                    settings.AI_PROVIDER
                )
            )

            recommendation_data = provider.generate(
                analysis
            )

        except AIProviderException:

            provider = (
                RecommendationProviderFactory.get_provider(
                    settings.AI_FALLBACK_PROVIDER
                )
            )

            recommendation_data = provider.generate(
                analysis
            )

        recommendation = PatientRecommendation(
            patient_id=patient.id,
            analysis_id=analysis.id,
            title=recommendation_data["title"],
            content=recommendation_data["content"],
            source=recommendation_data["source"]
        )

        recommendation = (
            PatientRecommendationRepository.create(
                db=db,
                recommendation=recommendation
            )
        )

        return recommendation