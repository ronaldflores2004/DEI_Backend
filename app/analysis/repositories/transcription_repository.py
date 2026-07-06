from sqlalchemy.orm import Session

from app.analysis.models.audio_transcription import (
    AudioTranscription,
)


class TranscriptionRepository:
    """
    Repositorio para el acceso a datos de
    AudioTranscription.
    """

    @staticmethod
    def get_by_id(
        db: Session,
        transcription_id: int,
    ) -> AudioTranscription | None:

        return (
            db.query(AudioTranscription)
            .filter(
                AudioTranscription.id == transcription_id
            )
            .first()
        )

    @staticmethod
    def get_by_entry(
        db: Session,
        entry_id: int,
    ) -> AudioTranscription | None:

        return (
            db.query(AudioTranscription)
            .filter(
                AudioTranscription.entry_id == entry_id
            )
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        transcription: AudioTranscription,
    ) -> AudioTranscription:

        db.add(transcription)

        db.commit()

        db.refresh(transcription)

        return transcription