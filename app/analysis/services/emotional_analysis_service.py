from fastapi import HTTPException

from datetime import datetime

from sqlalchemy.orm import Session

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.entries.models.emotional_entry import (
    EmotionalEntry
)

from app.entries.repositories.emotional_entry_repository import (
    EmotionalEntryRepository
)

from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis
)

from app.analysis.repositories.emotional_analysis_repository import (
    EmotionalAnalysisRepository
)

from app.analysis.repositories.transcription_repository import (
    TranscriptionRepository
)

from app.analysis.services.fake_analysis_service import (
    analyze_text_with_fake
)

from app.analysis.services.gemini_analysis_service import (
    GeminiAnalysisService,
)

from app.shared.enums.entry_type_enum import (
    EntryTypeEnum
)

from app.analysis.schemas.emotional_analysis_create import (
    EmotionalAnalysisCreate
)

class EmotionalAnalysisService:
    """
    Servicio encargado de la gestión de
    análisis emocionales.
    """
    
    @staticmethod
    def _validate_entry_owner(
        entry: EmotionalEntry,
        patient: PatientProfile
    ) -> None:

        if entry.patient_id != patient.id:
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para acceder a esta entrada"
            )


    @staticmethod
    def create_analysis(
        entry_id: int,
        patient: PatientProfile,
        data: EmotionalAnalysisCreate,
        db: Session
    ) -> EmotionalAnalysis:

        entry = EmotionalEntryRepository.get_by_id(
            db,
            entry_id
        )

        if not entry:
            raise HTTPException(
                status_code=404,
                detail="Entrada no encontrada"
            )

        EmotionalAnalysisService._validate_entry_owner(
            entry,
            patient
        )

        existing = (
            EmotionalAnalysisRepository.get_by_entry(
                db,
                entry_id
            )
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="La entrada ya tiene análisis"
            )

        analysis = EmotionalAnalysis(
            entry_id=entry.id,
            primary_emotion=data.primary_emotion,
            emotion_intensity=data.emotion_intensity,
            risk_level=data.risk_level,
            analysis_json=data.analysis_json
        )

        return EmotionalAnalysisRepository.create(
            db,
            analysis
        )

    
    @staticmethod
    def get_analysis(
        entry_id: int,
        patient: PatientProfile,
        db: Session
    ) -> EmotionalAnalysis:

        analysis = (
            EmotionalAnalysisRepository.get_by_entry(
                db,
                entry_id
            )
        )

        if not analysis:
            raise HTTPException(
                status_code=404,
                detail="Análisis no encontrado"
            )

        entry = EmotionalEntryRepository.get_by_id(
            db,
            entry_id
        )

        if not entry:
            raise HTTPException(
                status_code=404,
                detail="Entrada no encontrada"
            )

        EmotionalAnalysisService._validate_entry_owner(
            entry,
            patient
        )

        return analysis


    @staticmethod
    def create_analysis_from_entry(
        entry_id: int,
        patient: PatientProfile,
        db: Session
    ) -> EmotionalAnalysis:

        entry = EmotionalEntryRepository.get_by_id(
            db,
            entry_id
        )

        if not entry:
            raise HTTPException(
                status_code=404,
                detail="Entrada no encontrada"
            )

        EmotionalAnalysisService._validate_entry_owner(
            entry,
            patient
        )

        text_to_analyze = None

        if entry.entry_type == EntryTypeEnum.TEXT:

            text_to_analyze = entry.text_content

        elif entry.entry_type == EntryTypeEnum.AUDIO:

            transcription = (
                TranscriptionRepository.get_by_entry(
                    db,
                    entry.id
                )
            )

            if not transcription:
                raise HTTPException(
                    status_code=400,
                    detail="El audio aún no tiene transcripción"
                )

            text_to_analyze = (
                transcription.transcription_text
            )

        else:
            raise HTTPException(
                status_code=400,
                detail="Tipo de entrada no soportado"
            )

        if not text_to_analyze:
            raise HTTPException(
                status_code=400,
                detail="No existe texto para analizar"
            )

        existing = (
            EmotionalAnalysisRepository.get_by_entry(
                db=db,
                entry_id=entry_id
            )
        )

        try:

            result = (
                GeminiAnalysisService.analyze_text_with_gemini(
                    text_to_analyze
                )
            )

        except Exception as e:

            print("ERROR GEMINI:")
            print(e)

            result = analyze_text_with_fake(
                text_to_analyze
            )

        if existing:
            
            existing.entry_id = entry.id

            existing.primary_emotion = (
                result["primary_emotion"]
            )

            existing.emotion_intensity = (
                result["emotion_intensity"]
            )

            existing.risk_level = (
                result["risk_level"]
            )

            existing.analysis_json = (
                result["analysis_json"]
            )

            existing.analyzed_at = (
                datetime.utcnow()
            )

            return (
                EmotionalAnalysisRepository.update(
                    db=db,
                    analysis=existing
                )
            )

        analysis = EmotionalAnalysis(
            entry_id=entry.id,
            primary_emotion=result["primary_emotion"],
            emotion_intensity=result["emotion_intensity"],
            risk_level=result["risk_level"],
            analysis_json=result["analysis_json"]
        )

        return EmotionalAnalysisRepository.create(
            db,
            analysis
        )