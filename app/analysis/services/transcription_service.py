from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.identity.models.user import User

from app.identity.repositories.patient_repository import (
    PatientRepository
)

from app.entries.repositories.emotional_entry_repository import (
    EmotionalEntryRepository
)

from app.analysis.models.audio_transcription import (
    AudioTranscription
)

from app.analysis.repositories.transcription_repository import (
    TranscriptionRepository
)

from app.analysis.schemas.transcription_create import (
    TranscriptionCreate
)

from app.analysis.schemas.transcription_update import (
    TranscriptionUpdate
)

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.entries.models.emotional_entry import (
    EmotionalEntry
)


class TranscriptionService:
    """
    Servicio encargado de la gestión de
    transcripciones.
    """
    
    @staticmethod
    def _get_patient(
        db: Session,
        current_user: User,
    ) -> PatientProfile:

        patient = PatientRepository.get_by_user_id(
            db=db,
            user_id=current_user.id,
        )

        if not patient:
            raise HTTPException(
                status_code=403,
                detail="No tienes perfil de paciente",
            )

        return patient
    
    @staticmethod
    def _validate_entry_owner(
        entry: EmotionalEntry,
        patient: PatientProfile,
    ) -> None:

        if entry.patient_id != patient.id:
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para acceder a esta entrada"
            )
# =====================================
# Crear transcripción
# =====================================

    @staticmethod
    def create_transcription(
        entry_id: int,
        data: TranscriptionCreate,
        db: Session,
        current_user: User
    ) -> AudioTranscription:

        patient = TranscriptionService._get_patient(
            db,
            current_user
        )

        entry = (
            EmotionalEntryRepository.get_by_id(
                db=db,
                entry_id=entry_id
            )
        )

        if not entry:
            raise HTTPException(
                status_code=404,
                detail="Entrada no encontrada"
            )

        TranscriptionService._validate_entry_owner(
            entry,
            patient
        )
        
        existing = (
            TranscriptionRepository.get_by_entry(
                db=db,
                entry_id=entry.id
            )
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="La entrada ya tiene una transcripción"
            )

        transcription = AudioTranscription(
            entry_id=entry.id,
            transcription_text=data.transcription_text,
            provider="MANUAL"
        )

        return (
            TranscriptionRepository.create(
                db=db,
                transcription=transcription
            )
        )


    # =====================================
    # Actualizar transcripción
    # =====================================
    
    @staticmethod
    def update_transcription(
        transcription_id: int,
        data: TranscriptionUpdate,
        db: Session,
        current_user: User
    ) -> AudioTranscription:

        patient = TranscriptionService._get_patient(
            db,
            current_user
        )

        transcription = (
            TranscriptionRepository.get_by_id(
                db=db,
                transcription_id=transcription_id
            )
        )

        if not transcription:
            raise HTTPException(
                status_code=404,
                detail="Transcripción no encontrada"
            )

        entry = (
            EmotionalEntryRepository.get_by_id(
                db=db,
                entry_id=transcription.entry_id
            )
        )

        if not entry:
            raise HTTPException(
                status_code=404,
                detail="Entrada no encontrada"
            )

        TranscriptionService._validate_entry_owner(
            entry,
            patient
        )

        transcription.transcription_text = (
            data.transcription_text
        )

        transcription.provider = "MANUAL"

        return (
            TranscriptionRepository.update(
                db=db,
                transcription=transcription
            )
        )